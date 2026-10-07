#!/usr/bin/env python3
"""Check changed files with the reviewed style hooks in disposable repositories."""

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
from typing import Iterator, Mapping, Sequence

import yaml

# Hosted callers use isolated Python from the trusted base checkout. Restore
# only this script's own package root, never the candidate working directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validation.repository.bounded_io import (
    BoundedInputError,
    BoundedOutputError,
    open_parent,
    read_bytes,
    read_regular_file,
    run,
)


STYLE_IDS = (
    "end-of-file-fixer",
    "mixed-line-ending",
    "trailing-whitespace",
    "markdownlint-cli2",
    "shellcheck",
    "shfmt",
    "ruff-check",
    "ruff-format",
)
WHITESPACE_IDS = frozenset(STYLE_IDS[:3])
LANGUAGE_IDS = frozenset(STYLE_IDS[4:])
MAX_PATH_BYTES = 4096
MAX_PATHS = 2048
MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_TOTAL_BYTES = 32 * 1024 * 1024
MAX_CONFIG_BYTES = 1024 * 1024


class StyleError(ValueError):
    """A bounded selected-style input or execution failure."""


def _git(root: Path, *args: str) -> bytes:
    result = run(
        ["git", *args],
        cwd=root,
        timeout=15,
        stdout_limit=MAX_CONFIG_BYTES,
        stderr_limit=4096,
    )
    if result.returncode:
        raise StyleError("STYLE-GIT-INPUT: reviewed Git input is unavailable")
    return result.stdout


def _trusted_bytes(root: Path, path: Path, expected: str) -> bytes:
    absolute = Path(os.path.abspath(path))
    if absolute.is_relative_to(root):
        if absolute != root / expected:
            raise StyleError("STYLE-CONFIG-PATH: local config path differs from owner")
        # Staged config changes cannot redefine a hook that runs before the
        # candidate has passed review. Hosted passes its separate base copy.
        return _git(root, "show", f"HEAD:{expected}")
    return read_bytes(absolute, max_bytes=MAX_CONFIG_BYTES)


def _normalized_path(raw: str) -> str:
    path = PurePosixPath(raw)
    if (
        not raw
        or raw.startswith("-")
        or raw.startswith("./")
        or path.is_absolute()
        or ".." in path.parts
        or "\\" in raw
        or path.as_posix() != raw
        or raw.endswith("/")
        or "//" in raw
        or raw.startswith(".git/")
        or len(raw.encode("utf-8")) > MAX_PATH_BYTES
    ):
        raise StyleError("STYLE-PATH: selected path is not normalized")
    return raw


def _selected_paths(args: argparse.Namespace) -> list[str]:
    if args.paths_file is not None and args.include_path:
        raise StyleError("STYLE-PATH: select one path transport")
    if args.paths_file is not None:
        payload = read_bytes(args.paths_file, max_bytes=MAX_PATHS * MAX_PATH_BYTES)
        if payload and not payload.endswith(b"\0"):
            raise StyleError("STYLE-PATH: NUL path list is unterminated")
        try:
            raw_paths = [part.decode("utf-8") for part in payload.split(b"\0")[:-1]]
        except UnicodeError as exc:
            raise StyleError("STYLE-PATH: NUL path list is not UTF-8") from exc
    else:
        raw_paths = args.include_path
    if len(raw_paths) > MAX_PATHS:
        raise StyleError("STYLE-PATH: too many selected paths")
    return sorted({_normalized_path(raw) for raw in raw_paths})


def _selected_regular_files(
    root: Path, paths: Sequence[str], *, missing_is_error: bool
) -> dict[str, bytes]:
    selected: dict[str, bytes] = {}
    total = 0
    for raw in paths:
        target = root.joinpath(*PurePosixPath(raw).parts)
        try:
            with open_parent(target) as (parent, name):
                metadata = os.stat(name, dir_fd=parent, follow_symlinks=False)
                if stat.S_ISLNK(metadata.st_mode):
                    continue  # the pinned style hook's file type excludes links
                if not stat.S_ISREG(metadata.st_mode):
                    raise StyleError("STYLE-NODE: selected path is not a regular file")
                _, contents = read_regular_file(parent, name, max_bytes=MAX_FILE_BYTES)
        except FileNotFoundError:
            if missing_is_error:
                raise StyleError("STYLE-NODE: selected hosted path is absent") from None
            continue  # a local staged deletion has no formatter input
        selected[raw] = contents
        total += len(contents)
        if total > MAX_TOTAL_BYTES:
            raise StyleError("STYLE-BUDGET: selected bytes exceed the budget")
    return selected


def _style_repositories(
    config: bytes,
) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    try:
        parsed = yaml.safe_load(config)
    except yaml.YAMLError as exc:
        raise StyleError("STYLE-CONFIG: reviewed hook config is invalid") from exc
    if not isinstance(parsed, dict) or not isinstance(parsed.get("repos"), list):
        raise StyleError("STYLE-CONFIG: reviewed hook repositories are unavailable")
    default_stages = parsed.get("default_stages", ["pre-commit"])
    if not isinstance(default_stages, list) or "manual" not in default_stages:
        raise StyleError("STYLE-CONFIG: manual stage is required")
    whitespace: list[dict[str, object]] = []
    language: list[dict[str, object]] = []
    markdown: list[dict[str, object]] = []
    seen: set[str] = set()
    for repo in parsed["repos"]:
        if not isinstance(repo, dict) or not isinstance(repo.get("hooks"), list):
            raise StyleError("STYLE-CONFIG: hook repository is malformed")
        simple = []
        chosen = []
        md = []
        for hook in repo["hooks"]:
            if not isinstance(hook, dict):
                raise StyleError("STYLE-CONFIG: hook is malformed")
            identifier = hook.get("id")
            if identifier not in STYLE_IDS:
                continue
            stages = hook.get("stages", default_stages)
            if not isinstance(stages, list) or "manual" not in stages:
                raise StyleError("STYLE-CONFIG: manual stage is required")
            if identifier in seen:
                raise StyleError("STYLE-CONFIG: style hook is duplicated")
            seen.add(identifier)
            if identifier in ("ruff-check", "ruff-format"):
                hook = {
                    **hook,
                    "args": [
                        *hook.get("args", []),
                        "--config",
                        ".git/trusted-ruff.toml",
                    ],
                }
            if identifier in WHITESPACE_IDS:
                simple.append(hook)
            elif identifier == "markdownlint-cli2":
                md.append(hook)
            else:
                chosen.append(hook)
        if simple:
            whitespace.append({**repo, "hooks": simple})
        if chosen:
            language.append({**repo, "hooks": chosen})
        if md:
            markdown.append({**repo, "hooks": md})
    if seen != set(STYLE_IDS):
        raise StyleError("STYLE-CONFIG: reviewed style hook set is incomplete")
    common = {key: value for key, value in parsed.items() if key != "repos"}
    return (
        {**common, "repos": whitespace},
        {**common, "repos": language},
        {**common, "repos": markdown},
    )


def _language_files(
    selected: dict[str, bytes], language: dict[str, object]
) -> dict[str, bytes]:
    shell_patterns = [
        re.compile(hook["files"])
        for repo in language["repos"]
        for hook in repo["hooks"]
        if hook["id"] in ("shellcheck", "shfmt")
    ]
    return {
        path: contents
        for path, contents in selected.items()
        if path.endswith((".py", ".pyi"))
        or any(pattern.match(path) for pattern in shell_patterns)
    }


@contextmanager
def _hook_cache_environment(root: Path) -> Iterator[dict[str, str]]:
    """Use the runner's trusted cache or one private cache for all style phases."""

    existing = os.environ.get("PRE_COMMIT_HOME")
    if existing is not None:
        cache = Path(existing)
        if not cache.is_absolute() or cache.resolve().is_relative_to(root.resolve()):
            raise StyleError("STYLE-CACHE: hook cache must be outside the candidate")
        yield _cache_paths(cache)
        return
    with tempfile.TemporaryDirectory(prefix="hy-style-cache-") as temporary:
        yield _cache_paths(Path(temporary))


def _cache_paths(cache: Path) -> dict[str, str]:
    toolchains = cache / "toolchains"
    paths = {
        "PRE_COMMIT_HOME": str(cache),
        "CARGO_HOME": str(toolchains / "cargo"),
        "GOCACHE": str(toolchains / "go-build"),
        "GOPATH": str(toolchains / "go"),
        "XDG_CACHE_HOME": str(toolchains / "xdg"),
        "npm_config_cache": str(toolchains / "npm"),
    }
    for value in paths.values():
        Path(value).mkdir(mode=0o700, parents=True, exist_ok=True)
    return paths


def _private_check(
    files: dict[str, bytes],
    config: dict[str, object],
    trusted_files: dict[str, bytes],
    cache_environment: Mapping[str, str],
) -> None:
    if not files:
        return
    with tempfile.TemporaryDirectory(prefix="hy-style-") as temporary:
        workspace = Path(temporary)
        for raw, contents in files.items():
            target = workspace.joinpath(*PurePosixPath(raw).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(contents)
        _git_init = run(
            ["git", "-c", "core.hooksPath=/dev/null", "init", "-q"],
            cwd=workspace,
            timeout=15,
            stdout_limit=4096,
            stderr_limit=4096,
        )
        if _git_init.returncode:
            raise StyleError("STYLE-EXEC: private Git workspace is unavailable")
        for name, contents in trusted_files.items():
            (workspace / name).write_bytes(contents)
        config_path = workspace / ".git/style-reviewed.yaml"
        config_path.write_text(
            yaml.safe_dump(config, sort_keys=False), encoding="utf-8"
        )
        env = {
            "GIT_TERMINAL_PROMPT": "0",
            "HOME": "/nonexistent",
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "NO_COLOR": "1",
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "PYTHONNOUSERSITE": "1",
            "TZ": "UTC",
        }
        env.update(cache_environment)
        command = [
            sys.executable,
            "-I",
            "-m",
            "pre_commit",
            "run",
            "--config",
            str(config_path),
            "--hook-stage",
            "manual",
            "--files",
            *files,
        ]
        try:
            result = run(
                command,
                cwd=workspace,
                env=env,
                timeout=300,
                stdout_limit=256 * 1024,
                stderr_limit=64 * 1024,
            )
        except (BoundedOutputError, subprocess.TimeoutExpired) as exc:
            raise StyleError("STYLE-EXEC: selected hook exceeded its budget") from exc
        altered = any(
            read_bytes(
                workspace.joinpath(*PurePosixPath(raw).parts),
                max_bytes=MAX_FILE_BYTES,
            )
            != contents
            for raw, contents in files.items()
        )
        if altered:
            raise StyleError("STYLE-FORMAT-MUTATION: selected hook proposed a change")
        if result.returncode:
            raise StyleError("STYLE-HOOK-FAIL: selected style hook failed")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--markdown-config", type=Path, required=True)
    parser.add_argument("--ruff-config", type=Path, required=True)
    parser.add_argument("--include-path", action="append", default=[])
    parser.add_argument("--paths-file", type=Path)
    parser.add_argument("--delimiter", choices=("nul",), default="nul")
    parser.add_argument("--expected-base-sha")
    args = parser.parse_args(argv)
    try:
        root = Path(os.path.abspath(args.root))
        if args.expected_base_sha is not None:
            if re.fullmatch(r"[0-9a-f]{40}", args.expected_base_sha) is None:
                raise StyleError("STYLE-BASE: base SHA is malformed")
            if (
                _git(root, "rev-parse", "HEAD^1").strip()
                != args.expected_base_sha.encode()
            ):
                raise StyleError(
                    "STYLE-BASE: merge first parent differs from event base"
                )
        paths = _selected_paths(args)
        selected = _selected_regular_files(
            root, paths, missing_is_error=args.paths_file is not None
        )
        if not selected:
            print("STYLE-NOT_APPLICABLE: no selected regular files")
            return 0
        config = _trusted_bytes(root, args.config, ".pre-commit-config.yaml")
        markdown_config = _trusted_bytes(
            root, args.markdown_config, ".markdownlint-cli2.yaml"
        )
        ruff_config = _trusted_bytes(root, args.ruff_config, ".ruff.toml")
        whitespace, language, markdown = _style_repositories(config)
        with _hook_cache_environment(root) as cache_environment:
            _private_check(selected, whitespace, {}, cache_environment)
            _private_check(
                _language_files(selected, language),
                language,
                {".git/trusted-ruff.toml": ruff_config},
                cache_environment,
            )
            markdown_files = {
                path: data for path, data in selected.items() if path.endswith(".md")
            }
            _private_check(
                markdown_files,
                markdown,
                {".markdownlint-cli2.yaml": markdown_config},
                cache_environment,
            )
        for raw, contents in selected.items():
            if (
                read_bytes(
                    root.joinpath(*PurePosixPath(raw).parts), max_bytes=MAX_FILE_BYTES
                )
                != contents
            ):
                raise StyleError(
                    "STYLE-SOURCE-CHANGED: selected source changed during check"
                )
        print(f"STYLE-PASS: checked {len(selected)} regular selected files")
        return 0
    except (StyleError, BoundedInputError, OSError, UnicodeError) as exc:
        label = (
            str(exc)
            if isinstance(exc, StyleError)
            else "STYLE-INPUT: selected input unavailable"
        )
        print(label, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
