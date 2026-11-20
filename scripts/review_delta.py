#!/usr/bin/env python3
"""Decide what a change after a reviewed commit needs (W10-REVIEW, QUAL-R054).

A review covers one commit. When later commits only append factual Task check
rows, the review still stands. Other changes need review of the changed paths
and the findings they touch.

Evidence is an added factual row at the end of an existing Task's Verification
Evidence / Results table, with optional front matter `version` and `updated`
value changes. Authority and acceptance receipts, new Tasks and residue ledger
changes can change obligations and need review. Any other file in `01.tasks/`
(such as a folder `CLAUDE.md`), a deletion, a mode change, a symlink, a gitlink
or any other path is not evidence.
Rewritten history (the reviewed commit is no longer an ancestor) needs a full
review. The tool classifies changed paths only; whether a change widens the
review to its transitive impact or a whole boundary is the reviewer's call.
It compares commits, never the index or the working tree.
Exit codes: 0 NO_CHANGE or EVIDENCE_ONLY, 1 REREVIEW, 2 bad input.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

TASK = re.compile(r"docs/03\.specs/[^/]+/01\.tasks/tsk-[0-9]{4}-[^/]+\.md")
FRONT_MATTER = re.compile(r'(version|updated): "[^"\n]*"')
EVIDENCE_ID = re.compile(r"EVD-(?:[A-Z0-9]+-)*[0-9]{3}")
# shortcut: lexical cues cannot decide all prose semantics; reviewers resolve ambiguous rows.
SEMANTIC_ROW = re.compile(
    r"\b(?:approv\w*|accept\w*|adopt\w*|authori\w*|requirement\w*|promot\w*)\b",
    re.IGNORECASE,
)
REGULAR = "100644"
OUTPUT_LIMIT = 16 * 1024 * 1024


class DeltaError(ValueError):
    """The reviewed commit or the head cannot be read."""


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", "--no-replace-objects", "-c", "core.hooksPath=/dev/null", *args],
        cwd=root,
        capture_output=True,
        timeout=60,
        check=False,
    )
    if len(result.stdout) > OUTPUT_LIMIT:
        raise DeltaError(f"git {args[0]} output exceeds {OUTPUT_LIMIT} bytes")
    return result


def _commit(root: Path, name: str) -> str:
    result = _git(root, "rev-parse", "--verify", "--end-of-options", name + "^{commit}")
    if result.returncode != 0:
        raise DeltaError(f"{name!r} is not a commit")
    return result.stdout.decode().strip()


def _blob(root: Path, rev: str, path: str) -> bytes | None:
    shown = _git(root, "show", f"{rev}:{path}")
    return shown.stdout if shown.returncode == 0 else None


def _front_matter_end(lines: list[str]) -> int:
    """Index after the closing `---` of a leading front matter block, else 0."""
    if lines and lines[0] == "---":
        for index, line in enumerate(lines[1:], start=1):
            if line == "---":
                return index + 1
    return 0


def _evidence_end(lines: list[str]) -> int | None:
    """Insertion point after the existing Task check table, if unambiguous."""
    section = results = False
    found = []
    for index, line in enumerate(lines):
        heading = re.fullmatch(r"#{2,6} (.+)", line)
        if heading:
            title = heading.group(1)
            if title == "Verification Evidence":
                section, results = True, False
            elif title == "Results" and section:
                results = True
            else:
                section = results = False
        elif results and line.startswith("| Evidence ID |"):
            if index + 1 >= len(lines) or not lines[index + 1].startswith("| ---"):
                return None
            end = index + 2
            while end < len(lines) and lines[end].startswith("|"):
                end += 1
            found.append(end)
    return found[0] if len(found) == 1 else None


def _factual_row(line: str) -> bool:
    parts = line.split("|")
    if len(parts) != 14 or parts[0] or parts[-1]:
        return False
    cells = [part.strip() for part in parts[1:-1]]
    return bool(
        EVIDENCE_ID.fullmatch(cells[0])
        and cells[3] in {"automated", "review", "observation"}
        and cells[6]
        and not SEMANTIC_ROW.search(line)
        and not re.search(r'"(?:actor|accepted_by)"\s*:', line)
    )


def _grows(root: Path, old: str, new: str, path: str) -> bool:
    """Whether the Task only gained factual check rows, read from both blobs."""
    before, after = _blob(root, old, path), _blob(root, new, path)
    if before is None or after is None or b"\0" in before or b"\0" in after:
        return False
    try:
        old_lines = before.decode().splitlines()
        new_lines = after.decode().splitlines()
    except UnicodeDecodeError:
        return False
    limit = _front_matter_end(old_lines)
    evidence_end = _evidence_end(old_lines)
    if not limit or evidence_end is None:
        return False
    matcher = difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        if tag == "insert" and i1 == evidence_end:
            if all(_factual_row(line) for line in new_lines[j1:j2]):
                continue
        elif tag == "replace" and i2 <= limit and i2 - i1 == j2 - j1:
            prior = [FRONT_MATTER.fullmatch(line) for line in old_lines[i1:i2]]
            later = [FRONT_MATTER.fullmatch(line) for line in new_lines[j1:j2]]
            if (
                all(prior)
                and all(later)
                and [x.group(1) for x in prior] == [x.group(1) for x in later]
            ):
                continue
        return False
    return True


def classify(root: Path, reviewed: str, head: str = "HEAD") -> dict:
    root = Path(root)
    old, new = _commit(root, reviewed), _commit(root, head)
    result = {"reviewed": old, "head": new, "evidence": [], "rereview": []}
    if old == new:
        return {
            **result,
            "verdict": "NO_CHANGE",
            "reason": "head is the reviewed commit",
        }
    if _git(root, "merge-base", "--is-ancestor", old, new).returncode != 0:
        reason = (
            "the reviewed commit is not an ancestor of head; review the whole change"
        )
        return {**result, "verdict": "REREVIEW", "reason": reason}
    raw = _git(root, "diff", "--raw", "-z", "--no-renames", old, new)
    if raw.returncode != 0:
        raise DeltaError("git diff failed")
    fields = raw.stdout.split(b"\0")
    for meta, path in zip(fields[0::2], fields[1::2]):
        if not meta:
            continue
        old_mode, new_mode, _, _, status = meta.decode().lstrip(":").split()
        name = path.decode(errors="surrogateescape")
        evidence = (
            TASK.fullmatch(name)
            and new_mode == REGULAR
            and (status, old_mode) == ("M", REGULAR)
            and _grows(root, old, new, name)
        )
        result["evidence" if evidence else "rereview"].append(name)
    if not result["rereview"] and not result["evidence"]:
        return {**result, "verdict": "NO_CHANGE", "reason": "no path changed"}
    if result["rereview"]:
        reason = "these paths changed after the review; review them and the findings they touch"
        return {**result, "verdict": "REREVIEW", "reason": reason}
    return {
        **result,
        "verdict": "EVIDENCE_ONLY",
        "reason": "only factual-looking check rows were appended; confirm their meaning before carrying the review",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--reviewed", required=True, help="the commit the review covered"
    )
    parser.add_argument("--head", default="HEAD")
    args = parser.parse_args(argv)
    try:
        result = classify(args.root, args.reviewed, args.head)
    except (DeltaError, OSError, subprocess.SubprocessError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 1 if result["verdict"] == "REREVIEW" else 0


if __name__ == "__main__":
    raise SystemExit(main())
