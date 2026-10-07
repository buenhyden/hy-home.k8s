#!/usr/bin/env python3
"""Prepare a main changelog PR and explicitly publish one SemVer GitHub Release.

The default of both commands is a local, read-only preview. `publish --execute`
is an operator action requiring separately verified authority; this program
does not authenticate an approving actor.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import pwd
import re
import stat
import sys
import tempfile
from functools import lru_cache
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import quote
from typing import Sequence


REPOSITORY = "github.com/buenhyden/hy-home.k8s"
_VERSION = re.compile(
    r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-((?:0|[1-9][0-9]*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9][0-9]*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?\Z"
)
_RELEASE_HEADING = re.compile(r"^## \[([^]]+)\] - (\d{4}-\d{2}-\d{2})$", re.M)
_REMOTE = re.compile(
    r"(?:git@github\.com:|https://github\.com/|ssh://git@github\.com/)"
    r"buenhyden/hy-home\.k8s(?:\.git)?/?\Z"
)
_ASSET_ROOTS = frozenset({"dist", "release-assets"})
_STDOUT_LIMIT = 4 * 1024 * 1024
_STDERR_LIMIT = 64 * 1024


class ReleaseError(Exception):
    def __init__(self, code: str, path: str):
        self.code = code
        self.path = path
        super().__init__(f"{code} path={path}")


@dataclass(frozen=True)
class SemVer:
    tag: str
    major: int
    minor: int
    patch: int
    prerelease: tuple[str, ...]

    @property
    def label(self) -> str:
        return self.tag[1:]


def parse_version(raw: str) -> SemVer:
    match = _VERSION.fullmatch(raw)
    if match is None:
        raise ReleaseError("RELEASE-VERSION-INVALID", "<version>")
    prerelease = tuple(match.group(4).split(".")) if match.group(4) else ()
    return SemVer(
        raw, int(match.group(1)), int(match.group(2)), int(match.group(3)), prerelease
    )


def _precedence(version: SemVer) -> tuple[object, ...]:
    pre = tuple(
        (0, int(part)) if part.isdecimal() else (1, part) for part in version.prerelease
    )
    return (version.major, version.minor, version.patch, 1 if not pre else 0, pre)


def _command(root: Path, argv: Sequence[str], *, timeout: int = 20) -> str:
    if not argv or argv[0] not in {"git", "git-cliff", "gh"}:
        raise ReleaseError("RELEASE-TOOL-UNAVAILABLE", "<tool>")
    executable = _trusted_executable(root, argv[0])
    if executable is None:
        raise ReleaseError("RELEASE-TOOL-UNAVAILABLE", argv[0])
    runner = _trusted_runner()
    try:
        account_home = pwd.getpwuid(os.geteuid()).pw_dir
    except (KeyError, OSError) as exc:
        raise ReleaseError("RELEASE-COMMAND-BOUNDARY", argv[0]) from exc
    environment = {
        **runner.closed_subprocess_environment(),
        "HOME": account_home,
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_PARAMETERS": "",
        "GIT_CONFIG_COUNT": "2",
        "GIT_CONFIG_KEY_0": "core.fsmonitor",
        "GIT_CONFIG_VALUE_0": "false",
        "GIT_CONFIG_KEY_1": "core.hooksPath",
        "GIT_CONFIG_VALUE_1": os.devnull,
        "GH_HOST": "github.com",
        "GH_REPO": REPOSITORY,
    }
    for name in ("GH_TOKEN", "GITHUB_TOKEN", "GH_ENTERPRISE_TOKEN"):
        if value := os.environ.get(name):
            environment[name] = value
    if (socket := os.environ.get("SSH_AUTH_SOCK")) and Path(socket).is_absolute():
        environment["SSH_AUTH_SOCK"] = socket
    try:
        result = runner.run_bounded_command(
            [executable, *argv[1:]],
            cwd=root,
            env=environment,
            timeout_seconds=timeout,
            stdout_limit_bytes=_STDOUT_LIMIT,
            stderr_limit_bytes=_STDERR_LIMIT,
            cleanup_seconds=2,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        raise ReleaseError("RELEASE-COMMAND-BOUNDARY", argv[0]) from exc
    if (
        result.stdout.observed_bytes > _STDOUT_LIMIT
        or result.stderr.observed_bytes > _STDERR_LIMIT
    ):
        raise ReleaseError("RELEASE-OUTPUT-LIMIT", argv[0])
    if (
        result.status != "completed"
        or not result.cleanup_complete
        or result.escaped_descendants
        or not result.stdout.complete
        or not result.stderr.complete
    ):
        raise ReleaseError("RELEASE-COMMAND-BOUNDARY", argv[0])
    if result.returncode != 0:
        raise ReleaseError("RELEASE-COMMAND-FAILED", argv[0])
    try:
        return result.stdout.retained.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        raise ReleaseError("RELEASE-COMMAND-BOUNDARY", argv[0]) from exc


@lru_cache(maxsize=1)
def _trusted_runner():
    path = Path(__file__).with_name("run-validation-lane.py")
    spec = importlib.util.spec_from_file_location("release_validation_runner", path)
    if spec is None or spec.loader is None:
        raise ReleaseError("RELEASE-TOOL-UNAVAILABLE", "<tool>")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _trusted_executable(root: Path, name: str) -> str | None:
    try:
        return _trusted_runner().secure_tool_executable(root, name)
    except (OSError, ImportError, RuntimeError):
        return None


def _repository_root(path: Path) -> Path:
    try:
        root = path.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise ReleaseError("RELEASE-ROOT-INVALID", "<repository>") from exc
    if not root.is_dir():
        raise ReleaseError("RELEASE-ROOT-INVALID", "<repository>")
    actual = _command(root, ("git", "rev-parse", "--show-toplevel")).strip()
    if Path(actual).resolve() != root:
        raise ReleaseError("RELEASE-ROOT-INVALID", "<repository>")
    return root


def _local_state(root: Path, expected_branch: str) -> str:
    branch = _command(
        root, ("git", "symbolic-ref", "--quiet", "--short", "HEAD")
    ).strip()
    if branch != expected_branch:
        raise ReleaseError("RELEASE-BRANCH-INVALID", "<branch>")
    if _command(root, ("git", "status", "--porcelain", "--untracked-files=normal")):
        raise ReleaseError("RELEASE-WORKTREE-DIRTY", "<repository>")
    return _command(root, ("git", "rev-parse", "--verify", "HEAD")).strip()


def _local_versions(root: Path) -> tuple[SemVer, ...]:
    result = _command(root, ("git", "tag", "--list", "v*"))
    versions: list[SemVer] = []
    for tag in result.splitlines():
        versions.append(parse_version(tag))
    return tuple(versions)


def _check_order(version: SemVer, previous: Sequence[SemVer], initial: bool) -> None:
    if not previous:
        if not initial:
            raise ReleaseError("RELEASE-INITIAL-INTENT-REQUIRED", "<version>")
        return
    if initial:
        raise ReleaseError("RELEASE-INITIAL-ALREADY-USED", "<version>")
    if _precedence(version) <= max(_precedence(item) for item in previous):
        raise ReleaseError("RELEASE-VERSION-NOT-INCREASING", "<version>")


def _changelog(root: Path) -> bytes:
    path = root / "CHANGELOG.md"
    try:
        info = path.lstat()
        if not stat.S_ISREG(info.st_mode) or info.st_size > 4 * 1024 * 1024:
            raise OSError
        content = path.read_bytes()
    except OSError as exc:
        raise ReleaseError("RELEASE-CHANGELOG-INVALID", "CHANGELOG.md") from exc
    if not content.startswith(b"# Changelog\n"):
        raise ReleaseError("RELEASE-CHANGELOG-INVALID", "CHANGELOG.md")
    return content


def _release_notes(content: bytes, version: SemVer) -> str:
    try:
        text = content.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        raise ReleaseError("RELEASE-CHANGELOG-INVALID", "CHANGELOG.md") from exc
    headings = list(_RELEASE_HEADING.finditer(text))
    matches = [item for item in headings if item.group(1) == version.label]
    if len(matches) != 1:
        raise ReleaseError("RELEASE-CHANGELOG-VERSION", "CHANGELOG.md")
    heading = matches[0]
    try:
        date.fromisoformat(heading.group(2))
    except ValueError as exc:
        raise ReleaseError("RELEASE-CHANGELOG-DATE", "CHANGELOG.md") from exc
    next_heading = next(
        (item for item in headings if item.start() > heading.start()), None
    )
    end = next_heading.start() if next_heading is not None else len(text)
    section = text[heading.start() : end].rstrip()
    if not re.search(r"(?m)^\s*-\s+\S", section):
        raise ReleaseError("RELEASE-CHANGELOG-EMPTY", "CHANGELOG.md")
    return section + "\n"


def _release_section_bytes(content: bytes, version: SemVer) -> bytes:
    try:
        text = content.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        raise ReleaseError("RELEASE-CHANGELOG-INVALID", "CHANGELOG.md") from exc
    headings = list(_RELEASE_HEADING.finditer(text))
    matches = [item for item in headings if item.group(1) == version.label]
    if len(matches) != 1:
        raise ReleaseError("RELEASE-CHANGELOG-VERSION", "CHANGELOG.md")
    next_heading = next(
        (item for item in headings if item.start() > matches[0].start()), None
    )
    end = next_heading.start() if next_heading is not None else len(text)
    return text[matches[0].start() : end].encode("utf-8")


def _verify_history(root: Path, content: bytes, previous: Sequence[SemVer]) -> None:
    for prior in previous:
        try:
            tagged = _command(
                root, ("git", "show", f"{prior.tag}:CHANGELOG.md")
            ).encode()
            current_section = _release_section_bytes(content, prior)
            tagged_section = _release_section_bytes(tagged, prior)
            _release_notes(content, prior)
            if current_section != tagged_section:
                raise ReleaseError("RELEASE-CHANGELOG-HISTORY-DRIFT", "CHANGELOG.md")
        except ReleaseError as exc:
            raise ReleaseError(
                "RELEASE-CHANGELOG-HISTORY-DRIFT", "CHANGELOG.md"
            ) from exc


def _prepared_changelog(content: bytes, version: SemVer, new_section: str) -> bytes:
    try:
        text = content.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        raise ReleaseError("RELEASE-CHANGELOG-INVALID", "CHANGELOG.md") from exc
    headings = list(_RELEASE_HEADING.finditer(text))
    if any(item.group(1) == version.label for item in headings):
        if _release_notes(content, version) != new_section:
            raise ReleaseError("RELEASE-CHANGELOG-DRIFT", "CHANGELOG.md")
        return content
    first = headings[0].start() if headings else len(text)
    prefix = text[:first].rstrip("\n")
    suffix = text[first:]
    return (prefix + "\n\n" + new_section + ("\n" if suffix else "") + suffix).encode(
        "utf-8"
    )


def _write_changelog(root: Path, content: bytes) -> bool:
    path = root / "CHANGELOG.md"
    previous = _changelog(root)
    if previous == content:
        return False
    mode = stat.S_IMODE(path.stat().st_mode)
    descriptor, temporary = tempfile.mkstemp(prefix=".CHANGELOG-", dir=root)
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return True


def prepare(root: Path, version: SemVer, *, initial: bool, write: bool) -> None:
    _local_state(root, f"release/{version.tag}")
    try:
        _command(
            root, ("git", "merge-base", "--is-ancestor", "refs/heads/main", "HEAD")
        )
    except ReleaseError as exc:
        raise ReleaseError("RELEASE-BASE-NOT-MAIN", "<branch>") from exc
    previous = _local_versions(root)
    _check_order(version, previous, initial)
    current = _changelog(root)
    _verify_history(root, current, previous)
    generated = _command(
        root, ("git-cliff", "--config", "cliff.toml", "--tag", version.tag), timeout=60
    ).encode()
    section = _release_notes(generated, version)
    prepared = _prepared_changelog(current, version, section)
    digest = hashlib.sha256(prepared).hexdigest()
    if write:
        changed = _write_changelog(root, prepared)
        print(
            f"{'WRITTEN' if changed else 'UNCHANGED'} release prepare version={version.tag} sha256={digest}"
        )
    else:
        print(
            f"PREVIEW release prepare version={version.tag} bytes={len(prepared)} sha256={digest}"
        )


def _assets(root: Path, requested: Sequence[str]) -> tuple[Path, ...]:
    if len(requested) > 32:
        raise ReleaseError("RELEASE-ASSET-LIMIT", "<asset>")
    assets: list[Path] = []
    for raw in requested:
        relative = Path(raw)
        if (
            relative.is_absolute()
            or not relative.parts
            or relative.parts[0] not in _ASSET_ROOTS
            or any(part in (".", "..") for part in relative.parts)
        ):
            raise ReleaseError("RELEASE-ASSET-PATH", "<asset>")
        current = root
        for part in relative.parts:
            current = current / part
            try:
                info = current.lstat()
            except OSError as exc:
                raise ReleaseError("RELEASE-ASSET-PATH", "<asset>") from exc
            if stat.S_ISLNK(info.st_mode):
                raise ReleaseError("RELEASE-ASSET-PATH", "<asset>")
        if not stat.S_ISREG(info.st_mode) or current.stat().st_size > 256 * 1024 * 1024:
            raise ReleaseError("RELEASE-ASSET-PATH", "<asset>")
        assets.append(current)
    if len({path.name for path in assets}) != len(assets):
        raise ReleaseError("RELEASE-ASSET-DUPLICATE", "<asset>")
    return tuple(assets)


def _snapshot_assets(
    root: Path, assets: Sequence[Path], destination: Path
) -> tuple[Path, ...]:
    """Copy approved bytes through no-follow descriptors before remote work."""

    copied: list[Path] = []
    total = 0
    for asset in assets:
        parts = asset.relative_to(root).parts
        descriptors: list[int] = []
        try:
            current = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            descriptors.append(current)
            for part in parts[:-1]:
                current = os.open(
                    part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=current
                )
                descriptors.append(current)
            source = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=current)
            descriptors.append(source)
            before = os.fstat(source)
            if not stat.S_ISREG(before.st_mode) or before.st_size > 256 * 1024 * 1024:
                raise ReleaseError("RELEASE-ASSET-CHANGED", "<asset>")
            target = destination / asset.name
            digest = hashlib.sha256()
            with target.open("xb") as output:
                while chunk := os.read(source, 1024 * 1024):
                    total += len(chunk)
                    if total > 512 * 1024 * 1024:
                        raise ReleaseError("RELEASE-ASSET-LIMIT", "<asset>")
                    digest.update(chunk)
                    output.write(chunk)
                output.flush()
                os.fsync(output.fileno())
            after = os.fstat(source)

            def identity(info: os.stat_result) -> tuple[int, ...]:
                return (
                    info.st_dev,
                    info.st_ino,
                    info.st_size,
                    info.st_mtime_ns,
                    info.st_ctime_ns,
                )

            if (
                identity(before) != identity(after)
                or target.stat().st_size != before.st_size
            ):
                raise ReleaseError("RELEASE-ASSET-CHANGED", "<asset>")
            copied_digest = hashlib.sha256()
            with target.open("rb") as check:
                while chunk := check.read(1024 * 1024):
                    copied_digest.update(chunk)
            if copied_digest.digest() != digest.digest():
                raise ReleaseError("RELEASE-ASSET-CHANGED", "<asset>")
            copied.append(target)
        except OSError as exc:
            raise ReleaseError("RELEASE-ASSET-CHANGED", "<asset>") from exc
        finally:
            for descriptor in reversed(descriptors):
                os.close(descriptor)
    return tuple(copied)


def _remote_main(
    root: Path,
    version: SemVer,
    local_sha: str,
    *,
    initial: bool,
    draft_created: bool = False,
    require_tag: bool = False,
) -> None:
    remote = _command(root, ("git", "remote", "get-url", "origin")).strip()
    if _REMOTE.fullmatch(remote) is None:
        raise ReleaseError("RELEASE-REMOTE-IDENTITY", "origin")
    references = _command(
        root,
        ("git", "ls-remote", "--refs", "origin", "refs/heads/main", "refs/tags/v*"),
        timeout=30,
    )
    rows = dict(
        line.split("\t", 1)[::-1] for line in references.splitlines() if "\t" in line
    )
    if rows.get("refs/heads/main") != local_sha:
        raise ReleaseError("RELEASE-REMOTE-MAIN-DRIFT", "origin/main")
    remote_versions = tuple(
        parse_version(ref.removeprefix("refs/tags/"))
        for ref in rows
        if ref.startswith("refs/tags/v")
    )
    tag_ref = f"refs/tags/{version.tag}"
    if draft_created:
        _check_order(
            version,
            tuple(item for item in remote_versions if item.tag != version.tag),
            initial,
        )
        if (tag_ref in rows and rows[tag_ref] != local_sha) or (
            require_tag and tag_ref not in rows
        ):
            raise ReleaseError("RELEASE-DRAFT-TAG-DRIFT", version.tag)
    else:
        if tag_ref in rows:
            raise ReleaseError("RELEASE-TAG-COLLISION", version.tag)
        _check_order(version, remote_versions, initial)


def _verify_release(
    root: Path, version: SemVer, sha: str, assets: Sequence[Path], *, draft: bool
) -> None:
    raw = _command(
        root,
        (
            "gh",
            "release",
            "view",
            version.tag,
            "--repo",
            REPOSITORY,
            "--json",
            "isDraft,tagName,targetCommitish,assets",
        ),
        timeout=30,
    )
    try:
        body = json.loads(raw)
        names = {item["name"] for item in body["assets"]}
        valid = (
            body["isDraft"] is draft
            and body["tagName"] == version.tag
            and body["targetCommitish"] == sha
            and names == {item.name for item in assets}
            and len(body["assets"]) == len(assets)
        )
    except (ValueError, KeyError, TypeError):
        valid = False
    if not valid:
        raise ReleaseError(
            "RELEASE-DRAFT-VERIFY" if draft else "RELEASE-PUBLISH-VERIFY", version.tag
        )
    if assets:
        endpoint = "repos/buenhyden/hy-home.k8s/releases/tags/" + quote(
            version.tag, safe=""
        )
        raw_assets = _command(
            root, ("gh", "api", endpoint, "--hostname", "github.com"), timeout=30
        )
        try:
            remote_assets = json.loads(raw_assets)["assets"]
            observed = {
                item["name"]: (item["size"], item["digest"]) for item in remote_assets
            }
            expected = {
                item.name: (item.stat().st_size, f"sha256:{_digest_file(item)}")
                for item in assets
            }
            valid = len(remote_assets) == len(assets) and observed == expected
        except (ValueError, KeyError, TypeError, OSError):
            valid = False
        if not valid:
            raise ReleaseError("RELEASE-ASSET-VERIFY", version.tag)


def _digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def publish(
    root: Path,
    version: SemVer,
    *,
    initial: bool,
    requested_assets: Sequence[str],
    execute: bool,
) -> None:
    local_sha = _local_state(root, "main")
    previous = _local_versions(root)
    _check_order(version, previous, initial)
    content = _changelog(root)
    notes = _release_notes(content, version)
    _verify_history(root, content, previous)
    assets = _assets(root, requested_assets)
    if not execute:
        print(
            f"PREVIEW release publish version={version.tag} main={local_sha} assets={len(assets)} remote=NOT_RUN"
        )
        return
    with tempfile.TemporaryDirectory(prefix="release-payload-") as temp:
        snapshot_dir = Path(temp) / "assets"
        snapshot_dir.mkdir(mode=0o700)
        copied = _snapshot_assets(root, assets, snapshot_dir)
        _remote_main(root, version, local_sha, initial=initial)
        notes_path = Path(temp) / "notes.md"
        notes_path.write_text(notes, encoding="utf-8")
        command = [
            "gh",
            "release",
            "create",
            version.tag,
            "--repo",
            REPOSITORY,
            "--target",
            local_sha,
            "--draft",
            "--title",
            version.tag,
            "--notes-file",
            str(notes_path),
        ]
        if version.prerelease:
            command.append("--prerelease")
        command.extend(str(asset) for asset in copied)
        try:
            _command(root, command, timeout=180)
        except ReleaseError as exc:
            raise ReleaseError("RELEASE-DRAFT-INCOMPLETE", version.tag) from exc
        # Draft tags may be pending until publication. Verify the actual draft
        # target and uploaded assets before making the release visible.
        _verify_release(root, version, local_sha, copied, draft=True)
        _remote_main(root, version, local_sha, initial=initial, draft_created=True)
        try:
            _command(
                root,
                (
                    "gh",
                    "release",
                    "edit",
                    version.tag,
                    "--repo",
                    REPOSITORY,
                    "--draft=false",
                ),
                timeout=60,
            )
        except ReleaseError as exc:
            raise ReleaseError("RELEASE-DRAFT-UNPUBLISHED", version.tag) from exc
        _verify_release(root, version, local_sha, copied, draft=False)
        _remote_main(
            root,
            version,
            local_sha,
            initial=initial,
            draft_created=True,
            require_tag=True,
        )
    print(
        f"PUBLISHED release version={version.tag} main={local_sha} assets={len(assets)}"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    modes = parser.add_subparsers(dest="mode", required=True)
    for name in ("prepare", "publish"):
        option = modes.add_parser(name)
        option.add_argument("--version", required=True)
        option.add_argument("--initial-version", action="store_true")
        if name == "prepare":
            option.add_argument("--write", action="store_true")
        else:
            option.add_argument("--asset", action="append", default=[])
            option.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)
    try:
        root = _repository_root(args.root)
        version = parse_version(args.version)
        if args.mode == "prepare":
            prepare(root, version, initial=args.initial_version, write=args.write)
        else:
            publish(
                root,
                version,
                initial=args.initial_version,
                requested_assets=args.asset,
                execute=args.execute,
            )
    except ReleaseError as error:
        print(f"FAIL {error.code} path={error.path}", file=__import__("sys").stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
