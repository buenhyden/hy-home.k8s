"""Current executable-reference ownership with bounded historical recovery."""

from __future__ import annotations

import os
import re
import stat
import subprocess
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


_SEGMENT = r"[A-Za-z0-9_](?:[A-Za-z0-9_.-]*[A-Za-z0-9_])?"
_SCRIPT_REFERENCE = re.compile(
    rf"(?<![A-Za-z0-9_./-])(?:\./)?"
    rf"(?P<path>scripts/(?:{_SEGMENT}/)*{_SEGMENT})"
    rf"(?![A-Za-z0-9_./-])"
)
_TERMINAL_STATUSES = frozenset(
    {"accepted", "archived", "cancelled", "done", "rejected", "superseded"}
)
_GIT = "/usr/bin/git"
_GIT_TIMEOUT_SECONDS = 5.0
_CLOSED_GIT_ENVIRONMENT = {
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_TERMINAL_PROMPT": "0",
    "LANG": "C",
    "LC_ALL": "C",
    "PATH": "/usr/bin:/bin",
}


@dataclass(frozen=True, order=True)
class ExecutableReferenceDiagnostic:
    """One path-only executable-reference failure."""

    code: str
    source: PurePosixPath
    target: PurePosixPath

    def __str__(self) -> str:
        return f"{self.code} source={self.source} target={self.target}"


def executable_suffixes_from_registry(registry: object) -> frozenset[str]:
    """Derive executable suffixes from the current routing graph's argv paths."""

    if not isinstance(registry, Mapping):
        raise ValueError("validation registry must be an object")
    validators = registry.get("validators")
    if not isinstance(validators, list):
        raise ValueError("validation registry validators must be a list")

    suffixes: set[str] = set()
    for validator in validators:
        if not isinstance(validator, Mapping):
            raise ValueError("validation registry validator must be an object")
        argv = validator.get("argv")
        if not isinstance(argv, list) or not all(isinstance(item, str) for item in argv):
            raise ValueError("validation registry argv must be a string list")
        for token in argv:
            if not token.startswith("scripts/"):
                continue
            path = PurePosixPath(token)
            if path.suffix:
                suffixes.add(path.suffix)
    if not suffixes:
        raise ValueError("validation registry has no script executable suffixes")
    return frozenset(suffixes)


def _frontmatter_status(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    closing = text.find("\n---\n", 4)
    if closing < 0:
        return ""
    for line in text[4:closing].splitlines():
        match = re.fullmatch(
            r"status:\s*['\"]?([a-z][a-z0-9-]*)['\"]?\s*", line
        )
        if match is not None:
            return match.group(1)
    return ""


def _source_kind(path: PurePosixPath, text: str) -> str:
    if path == PurePosixPath("docs/98.archive") or PurePosixPath(
        "docs/98.archive"
    ) in path.parents:
        return "sealed"
    if path == PurePosixPath("docs/90.references") or PurePosixPath(
        "docs/90.references"
    ) in path.parents:
        return "historical"
    status = _frontmatter_status(text)
    if path == PurePosixPath("docs/03.specs") or PurePosixPath(
        "docs/03.specs"
    ) in path.parents:
        return "historical" if status in _TERMINAL_STATUSES else "proposal"
    return "historical" if status in _TERMINAL_STATUSES else "current"


def _reference_targets(
    text: str, executable_suffixes: frozenset[str]
) -> tuple[PurePosixPath, ...]:
    return tuple(
        sorted(
            {
                PurePosixPath(match.group("path"))
                for match in _SCRIPT_REFERENCE.finditer(text)
                if PurePosixPath(match.group("path")).suffix in executable_suffixes
            },
            key=PurePosixPath.as_posix,
        )
    )


def _tracked_regular_file(
    root: Path,
    target: PurePosixPath,
    tracked_paths: frozenset[PurePosixPath],
) -> bool:
    if target not in tracked_paths:
        return False
    try:
        return stat.S_ISREG((root / target).lstat().st_mode)
    except OSError:
        return False


def validate_current_executable_references(
    root: Path,
    *,
    tracked_paths: frozenset[PurePosixPath],
    source_texts: Mapping[PurePosixPath, str],
    executable_suffixes: frozenset[str],
    historical_path_exists: Callable[[PurePosixPath], bool],
) -> tuple[ExecutableReferenceDiagnostic, ...]:
    """Validate current refs and require Git-first recovery for historical refs."""

    if not executable_suffixes or any(not suffix.startswith(".") for suffix in executable_suffixes):
        raise ValueError("executable suffixes must be non-empty dotted values")

    diagnostics: list[ExecutableReferenceDiagnostic] = []
    recovered: dict[PurePosixPath, bool] = {}
    for source in sorted(source_texts, key=PurePosixPath.as_posix):
        text = source_texts[source]
        kind = _source_kind(source, text)
        if kind in {"proposal", "sealed"}:
            continue
        for target in _reference_targets(text, executable_suffixes):
            if _tracked_regular_file(root, target, tracked_paths):
                continue
            if kind == "current":
                diagnostics.append(
                    ExecutableReferenceDiagnostic("EXECUTABLE-CURRENT", source, target)
                )
                continue
            if target not in recovered:
                recovered[target] = historical_path_exists(target)
            if not recovered[target]:
                diagnostics.append(
                    ExecutableReferenceDiagnostic("EXECUTABLE-HISTORY", source, target)
                )
    return tuple(sorted(diagnostics))


def _run_git(root: Path, arguments: Iterable[str]) -> subprocess.CompletedProcess[bytes]:
    environment = dict(_CLOSED_GIT_ENVIRONMENT)
    for key, value in os.environ.items():
        if key.startswith("GIT_TRACE"):
            continue
        if key in {"SYSTEMROOT", "WINDIR"}:
            environment[key] = value
    return subprocess.run(
        [_GIT, *arguments],
        cwd=root,
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
        timeout=_GIT_TIMEOUT_SECONDS,
    )


def reachable_git_path_exists(root: Path, target: PurePosixPath) -> bool:
    """Return whether a reachable commit contains the historical path as a blob."""

    try:
        history = _run_git(
            root,
            (
                "log",
                "--all",
                "--format=%H",
                "--diff-filter=AM",
                "-n",
                "1",
                "--",
                target.as_posix(),
            ),
        )
        commit = history.stdout.decode("ascii", errors="strict").strip()
        if history.returncode != 0 or re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit) is None:
            return False
        recovered = _run_git(
            root,
            ("cat-file", "-e", f"{commit}:{target.as_posix()}"),
        )
        return recovered.returncode == 0 and recovered.stdout == b""
    except (OSError, subprocess.TimeoutExpired, UnicodeError):
        return False
