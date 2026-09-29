#!/usr/bin/env python3
"""Validate knowledge owner pointers and bounded observation provenance."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
import os
import re
import sys
import subprocess
from collections.abc import Sequence
from pathlib import Path, PurePosixPath
from typing import NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validation.repository.bounded_io import (
    BoundedInputError,
    BoundedOutputError,
    read_bytes,
    run as run_bounded_process,
)  # noqa: E402


KNOWLEDGE_ROOT = ".agents/knowledge"
KNOWLEDGE_README = f"{KNOWLEDGE_ROOT}/README.md"
POINTER_HEADING = "## Pointer Index"
MAX_DOCUMENT_BYTES = 256 * 1024
DUPLICATE_SPAN_WORDS = 12

INLINE_CODE = re.compile(r"`([^`\n]+)`")
TABLE_ROW = re.compile(r"^\s*\|(?P<cells>.+)\|\s*$")
TABLE_DIVIDER = re.compile(r"^\s*\|[\s:|-]+\|\s*$")
HEADING = re.compile(r"^##\s")
PATH_TOKEN = re.compile(r"^[.A-Za-z0-9_][A-Za-z0-9_./-]*$")
WORD = re.compile(r"[a-z0-9]+")
FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)


class Finding(NamedTuple):
    code: str
    path: str
    detail: str

    def __str__(self) -> str:
        return f"FAIL {self.code} {self.path}: {self.detail}"


class KnowledgeSurfaceError(Exception):
    """Raised when the surface cannot be read within its declared bounds."""


def _read_document(path: Path, relative: str) -> str:
    try:
        return read_bytes(path, max_bytes=MAX_DOCUMENT_BYTES).decode("utf-8")
    except (BoundedInputError, UnicodeError) as exc:
        raise KnowledgeSurfaceError(
            f"{relative} is unavailable, unsafe or exceeds its read bound"
        ) from exc


def _body(text: str) -> str:
    return FRONTMATTER.sub("", text, count=1)


def _section(text: str, heading: str) -> list[str]:
    lines = text.split("\n")
    collected: list[str] = []
    inside = False
    for line in lines:
        if line.strip() == heading:
            inside = True
            continue
        if inside and HEADING.match(line):
            break
        if inside:
            collected.append(line)
    return collected


def _pointer_rows(text: str) -> list[str]:
    rows: list[str] = []
    for line in _section(text, POINTER_HEADING):
        if TABLE_DIVIDER.match(line):
            continue
        match = TABLE_ROW.match(line)
        if match:
            rows.append(match.group("cells"))
    return rows[1:] if rows else rows


def _looks_like_path(token: str) -> bool:
    if not PATH_TOKEN.match(token) or ".." in PurePosixPath(token).parts:
        return False
    if "/" in token:
        return True
    return token.endswith((".md", ".py", ".sh", ".json", ".yaml", ".yml", ".toml"))


def _named_paths(rows: Sequence[str]) -> list[str]:
    seen: dict[str, None] = {}
    for row in rows:
        for token in INLINE_CODE.findall(row):
            candidate = token.strip()
            if _looks_like_path(candidate):
                seen.setdefault(candidate, None)
    return list(seen)


def _words(text: str) -> list[str]:
    return WORD.findall(text.lower())


def _spans(words: Sequence[str], size: int) -> set[tuple[str, ...]]:
    if len(words) < size:
        return set()
    return {
        tuple(words[index : index + size]) for index in range(len(words) - size + 1)
    }


def _knowledge_documents(root: Path) -> list[str]:
    directory = root / KNOWLEDGE_ROOT
    if not directory.is_dir():
        return []
    names = sorted(
        entry.name
        for entry in directory.iterdir()
        if entry.is_file() and entry.suffix == ".md" and entry.name != "README.md"
    )
    return [f"{KNOWLEDGE_ROOT}/{name}" for name in names]


def _check_readme(root: Path, documents: Sequence[str]) -> list[Finding]:
    # SPEC-0091: whether the README reaches each document is the README
    # navigation contract's completeness rule; this surface only requires the
    # README to exist once it has documents.
    if documents and not (root / KNOWLEDGE_README).is_file():
        return [
            Finding(
                "KNOWLEDGE-README-MISSING",
                KNOWLEDGE_README,
                "the surface has documents but no index",
            )
        ]
    return []


FACT_FIELDS = frozenset(
    (
        "owner",
        "scope",
        "source",
        "observed_at",
        "valid_for",
        "invalidated_by",
        "review_status",
        "sensitivity",
    )
)
FACT_BLOCK = re.compile(r"^```knowledge-fact\n(.*?)^```\s*$", re.MULTILINE | re.DOTALL)


def _unique_fact_pairs(pairs):
    if len(dict(pairs)) != len(pairs):
        raise ValueError("duplicate fact field")
    return dict(pairs)


def _check_facts(root: Path, document: str, text: str) -> list[Finding]:
    blocks = FACT_BLOCK.findall(text)
    invalid = len(blocks) != len(re.findall(r"^```knowledge-fact", text, re.MULTILINE))
    for block in blocks:
        try:
            fact = json.loads(block, object_pairs_hook=_unique_fact_pairs)
            if not isinstance(fact, dict) or set(fact) != FACT_FIELDS:
                raise ValueError("fact metadata differs")
            if any(
                not isinstance(fact[key], str) or not fact[key].strip()
                for key in ("owner", "scope", "observed_at", "valid_for")
            ):
                raise ValueError("fact metadata missing")
            if fact["sensitivity"] != "public" or fact["review_status"] not in (
                "advisory",
                "current",
            ):
                raise ValueError("fact is not reusable")
            if (
                not date.fromisoformat(fact["observed_at"])
                <= date.today()
                <= date.fromisoformat(fact["valid_for"])
            ):
                raise ValueError("fact validity expired")
            if not isinstance(fact["invalidated_by"], list) or set(
                fact["invalidated_by"]
            ) != {"source", "scope", "approval", "validity"}:
                raise ValueError("invalidation contract missing")
            source = fact["source"]
            if not isinstance(source, dict) or set(source) != {"path", "sha256"}:
                raise ValueError("source contract missing")
            path = source["path"]
            if (
                not isinstance(path, str)
                or not _looks_like_path(path)
                or PurePosixPath(path).is_absolute()
            ):
                raise ValueError("source is not repository local")
            tracked = run_bounded_process(
                ["git", "ls-files", "--error-unmatch", "--", path],
                cwd=root,
                timeout=5,
                stdout_limit=4096,
                stderr_limit=4096,
            )
            if tracked.returncode:
                raise ValueError("source is not tracked")
            payload = read_bytes(root / path, max_bytes=MAX_DOCUMENT_BYTES)
            if hashlib.sha256(payload).hexdigest() != source["sha256"]:
                raise ValueError("source changed")
        except (
            ValueError,
            TypeError,
            RecursionError,
            OSError,
            BoundedInputError,
            BoundedOutputError,
            subprocess.TimeoutExpired,
        ):
            invalid = True
    if invalid:
        return [
            Finding(
                "KNOWLEDGE-FACT-INVALID",
                document,
                "fact metadata, source hash, review, sensitivity or validity requires owner review; dependent cache is invalid",
            )
        ]
    return []


def _check_document(root: Path, document: str) -> list[Finding]:
    text = _read_document(root / document, document)
    body = _body(text)
    rows = _pointer_rows(body)
    findings = _check_facts(root, document, text)

    if not rows:
        findings.append(
            Finding("KNOWLEDGE-POINTER-EMPTY", document, "no pointer row was found")
        )
        return findings

    named = _named_paths(rows)
    existing: list[str] = []
    for candidate in named:
        target = root / candidate
        if target.exists():
            existing.append(candidate)
        else:
            findings.append(
                Finding(
                    "KNOWLEDGE-PATH-MISSING",
                    document,
                    f"the row names `{candidate}`, which is not in the tree",
                )
            )

    document_spans = _spans(_words(body), DUPLICATE_SPAN_WORDS)
    for candidate in existing:
        target = root / candidate
        if not target.is_file() or target.suffix != ".md":
            continue
        try:
            owner_text = _body(_read_document(target, candidate))
        except KnowledgeSurfaceError:
            continue
        shared = document_spans & _spans(_words(owner_text), DUPLICATE_SPAN_WORDS)
        if shared:
            span = " ".join(sorted(shared)[0])
            findings.append(
                Finding(
                    "KNOWLEDGE-DUPLICATED-SPAN",
                    document,
                    f"it reproduces `{span}` from {candidate}",
                )
            )
    return findings


def validate_knowledge_surface(root: str | os.PathLike[str]) -> list[Finding]:
    """Return every ordered finding for the knowledge surface under `root`."""

    repository_root = Path(root).resolve()
    documents = _knowledge_documents(repository_root)
    findings = list(_check_readme(repository_root, documents))
    for document in documents:
        findings.extend(_check_document(repository_root, document))
    return findings


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the common knowledge surface's pointers and non-duplication rule."
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--mode", default="strict", choices=("strict",))
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parse_args(sys.argv[1:] if argv is None else argv)
    try:
        findings = validate_knowledge_surface(arguments.root)
    except KnowledgeSurfaceError as exc:
        print(f"FAIL KNOWLEDGE-UNREADABLE {exc}", file=sys.stderr)
        return 1
    for finding in findings:
        print(str(finding), file=sys.stderr)
    if findings:
        return 1
    documents = _knowledge_documents(Path(arguments.root).resolve())
    print(f"[PASS] knowledge surface: {len(documents)} documents, 0 violations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
