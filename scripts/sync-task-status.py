#!/usr/bin/env python3
"""Preview or explicitly synchronize one current Task's frontmatter summary."""

from __future__ import annotations

import argparse
import importlib.util
import os
import re
import secrets
import stat
import sys
from functools import lru_cache
from pathlib import Path, PurePosixPath
from types import ModuleType

from document_authority import AuthorityError, load_bounded_json
from document_contracts import (
    DOCUMENT_TEXT_MAX_BYTES,
    PROFILE_SCHEMA_PATH,
    REGISTRY_PATH,
    DocumentContractError,
    classify_path,
    derive_task_summary,
    load_registry,
)


class SyncError(ValueError):
    """A stable authoring diagnostic that never exposes source contents."""

    def __init__(self, rule: str, detail: str):
        self.rule = rule
        self.detail = detail
        super().__init__(detail)


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise SyncError("SYNC-TASK-ARGUMENT", message)


@lru_cache(maxsize=1)
def markdown_parser() -> ModuleType:
    """Import trusted implementation siblings, never code from --root."""

    location = Path(__file__).resolve().with_name("validate-markdown-profiles.py")
    spec = importlib.util.spec_from_file_location("_sync_task_markdown", location)
    if spec is None or spec.loader is None:
        raise SyncError("SYNC-TASK-INVALID", "trusted Markdown parser unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def open_directory(path: Path) -> int:
    """Hold a directory descriptor after rejecting every symlink ancestor."""

    descriptor = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parts[1:]:
            child = os.open(
                part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor
            )
            os.close(descriptor)
            descriptor = child
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def target_path(root: Path, value: str) -> tuple[Path, PurePosixPath]:
    if "\\" in value or "\x00" in value:
        raise SyncError("SYNC-TASK-PATH", "use a normalized repository Task path")
    supplied = Path(value)
    if ".." in supplied.parts or ".." in root.parts:
        raise SyncError("SYNC-TASK-PATH", "parent traversal is forbidden")
    try:
        relative = supplied.relative_to(root) if supplied.is_absolute() else supplied
    except ValueError as exc:
        raise SyncError("SYNC-TASK-PATH", "path is outside --root") from exc
    path = PurePosixPath(relative.as_posix())
    if path.parts[:2] != ("docs", "03.specs"):
        raise SyncError("SYNC-TASK-PATH", "only current authored Tasks are supported")
    return root / relative, path


def source_identity(observation: os.stat_result) -> tuple[int, ...]:
    """Ignore access time, which our own reads may update."""

    return (
        observation.st_dev,
        observation.st_ino,
        observation.st_size,
        observation.st_mtime_ns,
        observation.st_ctime_ns,
        observation.st_mode,
    )


def read_source(parent: int, name: str) -> tuple[bytes, os.stat_result]:
    descriptor = os.open(
        name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent
    )
    with os.fdopen(descriptor, "rb") as source:
        observation = os.fstat(source.fileno())
        if not stat.S_ISREG(observation.st_mode):
            raise SyncError("SYNC-TASK-PATH", "target must be an ordinary regular file")
        raw = source.read(DOCUMENT_TEXT_MAX_BYTES + 1)
        if len(raw) > DOCUMENT_TEXT_MAX_BYTES:
            raise SyncError("SYNC-TASK-INVALID", "Task exceeds the document byte limit")
        if source_identity(observation) != source_identity(os.fstat(source.fileno())):
            raise SyncError(
                "SYNC-TASK-SOURCE-CHANGED",
                "source changed while reading; retry after review",
            )
    return raw, observation


def parse_rows(parser: ModuleType, body: str, contract) -> list[dict[str, str]]:
    section = parser._exact_heading_section(body, f"## {contract.section}")
    nested = parser._exact_heading_section(
        section or "", f"### {contract.table_heading}"
    )
    table = parser._first_visible_table(nested or "")
    if table is None or not table[1] or tuple(table[0]) != contract.required_columns:
        raise SyncError("SYNC-TASK-INVALID", "repair the Registry-bound Task table")
    if any(len(row) != len(table[0]) for row in table[1]):
        raise SyncError("SYNC-TASK-INVALID", "repair ragged Task table rows")
    return [dict(zip(table[0], row, strict=True)) for row in table[1]]


def replacement(raw: bytes, expected: str) -> bytes:
    """Replace exactly the scalar token, preserving all other bytes."""

    closing = re.search(rb"\r?\n---\r?\n", raw[4:])
    if closing is None:
        raise SyncError("SYNC-TASK-INVALID", "repair frontmatter delimiters")
    end = closing.start() + 4
    matches = list(re.finditer(rb'(?m)^status:[ \t]+"([^"\r\n]*)"', raw[:end]))
    if len(matches) != 1:
        raise SyncError(
            "SYNC-TASK-INVALID", "one canonical top-level status scalar is required"
        )
    start, stop = matches[0].span(1)
    return raw[:start] + expected.encode("utf-8") + raw[stop:]


def prepare(root: Path, path: PurePosixPath, raw: bytes) -> tuple[str, str, bytes]:
    parser = markdown_parser()
    for relative in (
        REGISTRY_PATH,
        PROFILE_SCHEMA_PATH,
        parser.FRONTMATTER_SCHEMA_PATH,
    ):
        descriptor = open_directory((root / relative).parent)
        os.close(descriptor)
    registry = load_registry(root)
    profile = classify_path(registry, path)
    if (
        profile.profile_id != "sdlc/task"
        or profile.mode != "authored"
        or profile.body_contract is None
    ):
        raise SyncError(
            "SYNC-TASK-PATH", "target must classify exactly as authored sdlc/task"
        )
    binding = profile.body_contract.task_execution
    if binding is None or profile.lifecycle_domain is None:
        raise SyncError(
            "SYNC-TASK-INVALID", "Task execution/lifecycle binding is required"
        )
    schema = load_bounded_json(root / parser.FRONTMATTER_SCHEMA_PATH)
    if not isinstance(schema, dict):
        raise SyncError("SYNC-TASK-INVALID", "frontmatter schema must be an object")
    text = raw.decode("utf-8").replace("\r\n", "\n")
    _, metadata, body = parser.extract_frontmatter(text)
    issues = parser.validate_document_text(
        text, path, profile, "strict", frontmatter_schema=schema
    )
    unexpected = sorted(
        {item.rule_id for item in issues if item.rule_id != "TASK-EXECUTION-SUMMARY"}
    )
    if unexpected:
        raise SyncError(
            "SYNC-TASK-INVALID", "repair source contract: " + ", ".join(unexpected)
        )
    rows = parse_rows(parser, body, profile.body_contract)
    current = metadata["status"]
    expected = (
        current
        if len(rows) == 1
        else derive_task_summary([row["Status"].strip() for row in rows], binding)
    )
    candidate = raw if current == expected else replacement(raw, expected)
    diagnostics = parser.validate_document_text(
        candidate.decode("utf-8").replace("\r\n", "\n"),
        path,
        profile,
        "strict",
        frontmatter_schema=schema,
    )
    if diagnostics:
        raise SyncError(
            "SYNC-TASK-CANDIDATE",
            "candidate contract refused: "
            + ", ".join(sorted({item.rule_id for item in diagnostics})),
        )
    if current != expected and not profile.lifecycle_domain.allows(current, expected):
        raise SyncError(
            "SYNC-TASK-TRANSITION",
            f"illegal Registry lifecycle edge {current} -> {expected}; review rows",
        )
    return current, expected, candidate


def assert_original(
    target: Path, parent: int, original: bytes, observation: os.stat_result
) -> None:
    try:
        reopened = open_directory(target.parent)
        try:
            first, second = os.fstat(parent), os.fstat(reopened)
            if (first.st_dev, first.st_ino) != (second.st_dev, second.st_ino):
                raise SyncError(
                    "SYNC-TASK-SOURCE-CHANGED",
                    "parent path changed; review before retry",
                )
        finally:
            os.close(reopened)
        raw, current = read_source(parent, target.name)
        if raw != original or source_identity(current) != source_identity(observation):
            raise SyncError(
                "SYNC-TASK-SOURCE-CHANGED", "source changed; review before retry"
            )
    except (OSError, SyncError) as exc:
        raise SyncError(
            "SYNC-TASK-SOURCE-CHANGED", "source or parent changed; review before retry"
        ) from exc


def write_candidate(
    target: Path,
    parent: int,
    original: bytes,
    candidate: bytes,
    observation: os.stat_result,
) -> None:
    temporary = ".task-status-" + secrets.token_hex(12)
    created = False
    try:
        descriptor = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o600,
            dir_fd=parent,
        )
        created = True
        with os.fdopen(descriptor, "wb", buffering=0) as output:
            remaining = memoryview(candidate)
            while remaining:
                written = os.write(output.fileno(), remaining)
                if written <= 0:
                    raise OSError("short temporary write")
                remaining = remaining[written:]
            os.fchmod(output.fileno(), stat.S_IMODE(observation.st_mode))
            os.fsync(output.fileno())
        assert_original(target, parent, original, observation)
        os.replace(temporary, target.name, src_dir_fd=parent, dst_dir_fd=parent)
        created = False
    except OSError as exc:
        raise SyncError(
            "SYNC-TASK-WRITE",
            "atomic write failed; original retained; check file permissions",
        ) from exc
    finally:
        if created:
            try:
                os.unlink(temporary, dir_fd=parent)
            except OSError as exc:
                raise SyncError(
                    "SYNC-TASK-WRITE",
                    "original retained; remove the task-owned temporary file after review",
                ) from exc


def main(argv: list[str] | None = None) -> int:
    display = "<arguments>"
    descriptor = None
    try:
        parser = Parser(description=__doc__)
        parser.add_argument("--root", required=True, type=Path)
        parser.add_argument("--path", required=True, action="append")
        parser.add_argument(
            "--write",
            action="store_true",
            help="explicitly change only the Task status scalar",
        )
        args = parser.parse_args(argv)
        display = ", ".join(args.path)
        if len(args.path) != 1:
            raise SyncError("SYNC-TASK-ARGUMENT", "exactly one --path is required")
        root = args.root.absolute()
        target, path = target_path(root, args.path[0])
        try:
            descriptor = open_directory(target.parent)
            raw, observation = read_source(descriptor, target.name)
        except OSError as exc:
            raise SyncError(
                "SYNC-TASK-PATH", "repair missing, symlink or nonregular target/parent"
            ) from exc
        current, expected, candidate = prepare(root, path, raw)
        action = "unchanged" if candidate == raw else "preview"
        if args.write and candidate != raw:
            write_candidate(target, descriptor, raw, candidate, observation)
            action = "changed"
        print(f"{display}: current={current} expected={expected} {action}")
        return 0
    except SyncError as exc:
        print(f"{exc.rule}: {display}: {exc.detail}", file=sys.stderr)
    except (
        AuthorityError,
        DocumentContractError,
        OSError,
        UnicodeError,
        ValueError,
        TypeError,
        RecursionError,
    ) as exc:
        print(
            f"SYNC-TASK-INVALID: {display}: repair the Task or its Registry/schema ({type(exc).__name__})",
            file=sys.stderr,
        )
    finally:
        if descriptor is not None:
            os.close(descriptor)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
