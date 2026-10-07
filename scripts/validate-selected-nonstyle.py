#!/usr/bin/env python3
"""Run the reviewed non-style hooks on selected paths in an isolated QA snapshot."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, Iterator, Sequence

import yaml

# Direct CLI and import-based focused tests use the same canonical package root.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validation.repository.bounded_io import (
    BoundedInputError,
    BoundedOutputError,
    read_bytes,
    run,
)


NONSTYLE_IDS = frozenset(
    (
        "check-added-large-files",
        "check-case-conflict",
        "check-merge-conflict",
        "check-symlinks",
        "check-yaml",
        "check-toml",
        "check-json",
        "gitleaks",
        "detect-secrets",
        "check-dependabot",
        "zizmor",
        "actionlint",
        "kube-linter",
    )
)
STYLE_IDS = frozenset(
    (
        "end-of-file-fixer",
        "mixed-line-ending",
        "trailing-whitespace",
        "markdownlint-cli2",
        "shellcheck",
        "shfmt",
        "ruff-check",
        "ruff-format",
    )
)
MAX_CONFIG_BYTES = 1024 * 1024
MAX_PATHS = 2048
MAX_PATH_BYTES = 4096
MAX_INDEX_BYTES = 16 * 1024 * 1024


class NonstyleError(ValueError):
    """A selected non-style input or execution failure."""


def _closed_environment() -> dict[str, str]:
    return {
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_TERMINAL_PROMPT": "0",
        "HOME": "/nonexistent",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "NO_COLOR": "1",
        "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "PYTHONNOUSERSITE": "1",
        "TZ": "UTC",
    }


def _git(root: Path, *args: str, index: Path | None = None) -> bytes:
    environment = _closed_environment()
    if index is not None:
        environment["GIT_INDEX_FILE"] = str(index)
    result = run(
        ["git", *args],
        cwd=root,
        env=environment,
        timeout=15,
        stdout_limit=MAX_CONFIG_BYTES,
        stderr_limit=4096,
    )
    if result.returncode:
        raise NonstyleError("NONSTYLE-GIT: exact snapshot is unavailable")
    return result.stdout


@contextmanager
def _disposable_index(root: Path) -> Iterator[tuple[Path, bytes]]:
    """Project the full index into an exclusive file for Git's stat refreshes."""
    index_path = root / ".git/index"
    index_before = read_bytes(index_path, max_bytes=MAX_INDEX_BYTES)
    temporary = tempfile.NamedTemporaryFile(
        mode="w+b", prefix="qa-index-diff-", dir=index_path.parent, delete=False
    )
    disposable_index = Path(temporary.name)
    try:
        with temporary:
            temporary.write(index_before)
            temporary.flush()
        yield disposable_index, index_before
    finally:
        disposable_index.unlink(missing_ok=True)


def _worktree_diff(root: Path) -> bytes:
    """Inspect worktree drift without refreshing the canonical private index."""
    with _disposable_index(root) as (disposable_index, index_before):
        result = _git(root, "diff", "--name-only", "-z", index=disposable_index)
        index_path = root / ".git/index"
        if read_bytes(index_path, max_bytes=MAX_INDEX_BYTES) != index_before:
            raise NonstyleError("NONSTYLE-MUTATION: snapshot index changed")
        return result


def _path(raw: str) -> str:
    path = PurePosixPath(raw)
    if (
        not raw
        or raw.startswith(("-", "./"))
        or path.is_absolute()
        or ".." in path.parts
        or "\\" in raw
        or "//" in raw
        or raw.endswith("/")
        or raw.startswith(".git/")
        or path.as_posix() != raw
        or len(raw.encode("utf-8")) > MAX_PATH_BYTES
    ):
        raise NonstyleError("NONSTYLE-PATH: selected path is not normalized")
    return raw


def project_nonstyle(config_bytes: bytes) -> dict[str, Any]:
    """Keep only reviewed filename hooks plus staged-diff Gitleaks."""
    try:
        config = yaml.safe_load(config_bytes)
    except yaml.YAMLError as exc:
        raise NonstyleError("NONSTYLE-CONFIG: reviewed hook config is invalid") from exc
    if not isinstance(config, dict) or not isinstance(config.get("repos"), list):
        raise NonstyleError("NONSTYLE-CONFIG: hook repositories are unavailable")
    default_stages = config.get("default_stages", ["pre-commit"])
    if (
        not isinstance(default_stages, list)
        or not all(isinstance(stage, str) for stage in default_stages)
        or "pre-commit" not in default_stages
    ):
        raise NonstyleError("NONSTYLE-CONFIG: pre-commit default stage is required")
    selected = []
    seen: set[str] = set()
    for repo in config["repos"]:
        if (
            not isinstance(repo, dict)
            or not isinstance(repo.get("repo"), str)
            or repo["repo"] == "local"
            or re.fullmatch(r"[0-9a-f]{40}", str(repo.get("rev", ""))) is None
            or not isinstance(repo.get("hooks"), list)
        ):
            raise NonstyleError("NONSTYLE-CONFIG: hook source is not pinned")
        hooks = []
        for hook in repo["hooks"]:
            if not isinstance(hook, dict) or not isinstance(hook.get("id"), str):
                raise NonstyleError("NONSTYLE-CONFIG: hook is malformed")
            identifier = hook["id"]
            stages = hook.get("stages", default_stages)
            if not isinstance(stages, list) or not all(
                isinstance(stage, str) for stage in stages
            ):
                raise NonstyleError("NONSTYLE-CONFIG: hook stages are malformed")
            if "pre-commit" not in stages:
                continue
            if identifier in STYLE_IDS or identifier == "commitizen":
                continue
            if identifier not in NONSTYLE_IDS or identifier in seen:
                raise NonstyleError("NONSTYLE-CONFIG: unreviewed or repeated hook")
            if identifier == "gitleaks" and (
                hook.get("entry") is not None
                or hook.get("pass_filenames") is not None
                or hook.get("stages") != ["pre-commit"]
                or hook.get("args") != ["--config=.gitleaks.toml"]
            ):
                raise NonstyleError("NONSTYLE-CONFIG: staged Gitleaks changed scope")
            if identifier == "gitleaks":
                hook = {**hook, "args": ["--config=.git/qa-trusted-gitleaks.toml"]}
            elif identifier == "detect-secrets":
                args = list(hook.get("args", ()))
                if args[:2] != ["--baseline", ".secrets.baseline"]:
                    raise NonstyleError(
                        "NONSTYLE-CONFIG: secret baseline changed scope"
                    )
                hook = {
                    **hook,
                    "args": [
                        "--baseline",
                        ".git/qa-trusted-secrets.baseline",
                        *args[2:],
                    ],
                }
            elif identifier == "kube-linter":
                if hook.get("args") != ["--config", ".kube-linter.yaml"]:
                    raise NonstyleError(
                        "NONSTYLE-CONFIG: kube-linter config changed scope"
                    )
                hook = {
                    **hook,
                    "args": ["--config", ".git/qa-trusted-kube-linter.yaml"],
                }
            elif identifier == "zizmor":
                hook = {**hook, "args": [*hook.get("args", ()), "--no-config"]}
            elif identifier == "actionlint":
                hook = {
                    **hook,
                    "args": [
                        *hook.get("args", ()),
                        "-config-file",
                        ".git/qa-trusted-actionlint.yaml",
                    ],
                }
            hooks.append(hook)
            seen.add(identifier)
        if hooks:
            selected.append({**repo, "hooks": hooks})
    if seen != NONSTYLE_IDS:
        raise NonstyleError("NONSTYLE-CONFIG: reviewed non-style set is incomplete")
    return {**config, "repos": selected}


def _selected_index_paths(root: Path, paths: Sequence[str]) -> list[str]:
    if len(paths) > MAX_PATHS:
        raise NonstyleError("NONSTYLE-PATH: too many selected paths")
    selected = sorted({_path(value) for value in paths})
    indexed = _git(root, "ls-files", "--stage", "-z")
    modes: dict[str, str] = {}
    for record in indexed.split(b"\0"):
        if not record:
            continue
        try:
            metadata, name = record.split(b"\t", 1)
            mode, _, stage = metadata.decode("ascii").split(" ")
            if stage == "0":
                modes[name.decode("utf-8")] = mode
        except (ValueError, UnicodeDecodeError) as exc:
            raise NonstyleError("NONSTYLE-INDEX: index entry is malformed") from exc
    for raw in selected:
        mode = modes.get(raw)
        if mode not in ("100644", "100755", "120000"):
            raise NonstyleError("NONSTYLE-INDEX: selected path has no safe index node")
        target = root.joinpath(*PurePosixPath(raw).parts)
        try:
            metadata = target.lstat()
        except OSError as exc:
            raise NonstyleError("NONSTYLE-NODE: selected index node is absent") from exc
        if not (
            (mode == "120000" and stat.S_ISLNK(metadata.st_mode))
            or (mode != "120000" and stat.S_ISREG(metadata.st_mode))
        ):
            raise NonstyleError("NONSTYLE-NODE: selected node differs from index")
    return selected


def _cache(root: Path, temporary: Path) -> Path:
    supplied = os.environ.get("PRE_COMMIT_HOME")
    cache = Path(supplied) if supplied else temporary / "cache"
    if not cache.is_absolute() or cache.resolve().is_relative_to(root.resolve()):
        raise NonstyleError("NONSTYLE-CACHE: hook cache is inside the repository")
    cache.mkdir(mode=0o700, parents=True, exist_ok=True)
    return cache


def _toolchain_caches(cache: Path) -> dict[str, str]:
    """Name cold hook build caches under the already checked hook cache."""
    toolchains = cache / "toolchains"
    paths = {
        "CARGO_HOME": str(toolchains / "cargo"),
        "GOCACHE": str(toolchains / "go-build"),
        "GOPATH": str(toolchains / "go"),
        "XDG_CACHE_HOME": str(toolchains / "xdg"),
        "npm_config_cache": str(toolchains / "npm"),
    }
    for value in paths.values():
        Path(value).mkdir(mode=0o700, parents=True, exist_ok=True)
    return paths


def _write_git_control(root: Path, name: str, content: bytes) -> Path:
    git_dir = root / ".git"
    if not stat.S_ISDIR(git_dir.lstat().st_mode):
        raise NonstyleError("NONSTYLE-GIT: snapshot metadata is not a directory")
    target = git_dir / name
    descriptor = os.open(
        target,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
        0o600,
    )
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(content)
    return target


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--include-path", action="append", default=[])
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve(strict=True)
        paths = _selected_index_paths(root, args.include_path)
        if not paths:
            print("NONSTYLE-NOT_APPLICABLE: no selected index files")
            return 0
        if _worktree_diff(root):
            raise NonstyleError("NONSTYLE-INDEX: working tree differs from exact index")
        config_path = Path(os.path.abspath(args.config))
        if config_path != root / ".pre-commit-config.yaml":
            raise NonstyleError("NONSTYLE-CONFIG: canonical config path is required")
        # The candidate index may change the config; a pre-commit check must
        # use the reviewed HEAD definition until that change is accepted.
        config = project_nonstyle(_git(root, "show", "HEAD:.pre-commit-config.yaml"))
        trusted = {
            "qa-trusted-gitleaks.toml": _git(root, "show", "HEAD:.gitleaks.toml"),
            "qa-trusted-secrets.baseline": _git(root, "show", "HEAD:.secrets.baseline"),
            "qa-trusted-kube-linter.yaml": _git(root, "show", "HEAD:.kube-linter.yaml"),
            # No actionlint config is declared at this revision. An explicit
            # empty config prevents candidate .github/actionlint.yaml discovery.
            "qa-trusted-actionlint.yaml": b"{}\n",
        }
        index_before = _git(root, "ls-files", "--stage", "-z")
        flags_before = _git(root, "ls-files", "-v", "-z")
        with tempfile.TemporaryDirectory(prefix="hy-nonstyle-") as temporary:
            cache = _cache(root, Path(temporary))
            controls: list[Path] = []
            try:
                config_file = _write_git_control(
                    root,
                    "nonstyle-reviewed.yaml",
                    yaml.safe_dump(config, sort_keys=False).encode(),
                )
                controls.append(config_file)
                for name, content in trusted.items():
                    controls.append(_write_git_control(root, name, content))
                env = (
                    _closed_environment()
                    | {"PRE_COMMIT_HOME": str(cache)}
                    | _toolchain_caches(cache)
                )
                with _disposable_index(root) as (hook_index, canonical_raw_before):
                    result = run(
                        [
                            sys.executable,
                            "-I",
                            "-m",
                            "pre_commit",
                            "run",
                            "--config",
                            str(config_file),
                            "--hook-stage",
                            "pre-commit",
                            "--files",
                            *paths,
                        ],
                        cwd=root,
                        env=env | {"GIT_INDEX_FILE": str(hook_index)},
                        timeout=600,
                        stdout_limit=256 * 1024,
                        stderr_limit=64 * 1024,
                    )
                    if (
                        _git(root, "ls-files", "--stage", "-z", index=hook_index)
                        != index_before
                        or _git(root, "ls-files", "-v", "-z", index=hook_index)
                        != flags_before
                    ):
                        raise NonstyleError(
                            "NONSTYLE-MUTATION: hook changed index entries"
                        )
                    if (
                        read_bytes(root / ".git/index", max_bytes=MAX_INDEX_BYTES)
                        != canonical_raw_before
                    ):
                        raise NonstyleError("NONSTYLE-MUTATION: snapshot index changed")
            finally:
                for control in controls:
                    control.unlink(missing_ok=True)
        if _git(root, "ls-files", "--stage", "-z") != index_before:
            raise NonstyleError("NONSTYLE-MUTATION: snapshot index changed")
        if _worktree_diff(root):
            raise NonstyleError("NONSTYLE-MUTATION: snapshot files changed")
        if result.returncode:
            raise NonstyleError("NONSTYLE-HOOK-FAIL: selected non-style hook failed")
        print(f"NONSTYLE-PASS: checked {len(paths)} selected index paths")
        return 0
    except (
        NonstyleError,
        BoundedInputError,
        BoundedOutputError,
        OSError,
        UnicodeError,
        subprocess.TimeoutExpired,
    ) as exc:
        message = (
            str(exc)
            if isinstance(exc, NonstyleError)
            else "NONSTYLE-INPUT: unavailable"
        )
        print(message, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
