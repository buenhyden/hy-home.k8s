#!/usr/bin/env python3
"""Decide what a change after a reviewed commit needs (W10-REVIEW, QUAL-R054).

A review covers one commit. When later commits only append evidence, the
review still stands and no new review is replayed. When any other path
changes, only those paths and the findings they touch need review again.

Evidence is a regular `tsk-NNNN-*.md` record in a Spec package's `01.tasks/`
folder, or the work residue ledger, that only grows: a Task record may delete
no line except its front matter `version` and `updated`, and the ledger keeps
every earlier entry unchanged. Any other file in `01.tasks/` (such as a folder
`CLAUDE.md`), a deletion, a mode change, a symlink, a gitlink or any other
path is not evidence, so the exception cannot hide a change in behavior.
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
LEDGER = "docs/03.specs/work-residue-ledger.json"
FRONT_MATTER = re.compile(r'(?:version|updated): "[^"\n]*"')
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


def _grows(root: Path, old: str, new: str, path: str) -> bool:
    """Whether an evidence file only gained content, read from the two blobs.

    Diff text is never parsed: a NUL makes git print a binary notice, and a
    deleted line that starts with `--` looks like a header.
    """
    before, after = _blob(root, old, path), _blob(root, new, path)
    if before is None or after is None or b"\0" in before or b"\0" in after:
        return False
    if path == LEDGER:
        try:
            first, second = json.loads(before), json.loads(after)
            entries = [first.pop("entries"), second.pop("entries")]
            kept = {json.dumps(e, sort_keys=True) for e in entries[1]}
            return first == second and all(
                json.dumps(e, sort_keys=True) in kept for e in entries[0]
            )
        except (ValueError, AttributeError, TypeError, KeyError):
            return False
    try:
        old_lines = before.decode().splitlines()
        new_lines = after.decode().splitlines()
    except UnicodeDecodeError:
        return False
    limit = _front_matter_end(old_lines)
    matcher = difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False)
    for tag, i1, i2, _, _ in matcher.get_opcodes():
        if tag in ("delete", "replace"):
            for index in range(i1, i2):
                if index >= limit or not FRONT_MATTER.fullmatch(old_lines[index]):
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
            (TASK.fullmatch(name) or name == LEDGER)
            and new_mode == REGULAR
            and (status, old_mode) in (("A", "000000"), ("M", REGULAR))
            and (status == "A" or _grows(root, old, new, name))
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
        "reason": "only evidence was appended; the review of the reviewed commit stands",
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
