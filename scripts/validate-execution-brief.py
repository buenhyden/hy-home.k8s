#!/usr/bin/env python3
"""Check a local handoff against the current request before dependent work."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from contextlib import ExitStack
from pathlib import Path, PurePosixPath

from validation.repository.bounded_io import open_parent, read_bytes


BRIEF_VERSION = "3.0.0"
REQUEST_TEXT = (
    "request_ref",
    "request_digest",
    "request_revision",
    "workspace_id",
    "baseline_id",
    "goal",
)
REQUEST_LISTS = (
    "in_scope",
    "out_of_scope",
    "constraints",
    "acceptance_criteria",
    "allowed_mutations",
    "expected_checks",
)
BOUND_FIELDS = frozenset(
    (
        *REQUEST_TEXT,
        *REQUEST_LISTS,
        "risk",
        "authority_ref",
        "material_inputs",
        "brief_id",
        "revision",
        "unresolved_questions",
    )
)
BRIEF_FIELDS = BOUND_FIELDS | {
    "contract_version",
    "known_facts",
    "assumptions",
    "state",
}
CURRENT_FIELDS = BOUND_FIELDS | {"state", "allowed_actions"}
SOURCE_FIELDS = {
    "source_id",
    "kind",
    "logical_uri",
    "content_digest",
    "revision",
    "observed_at",
    "access_scope",
    "trust",
}
BYTE_LIMIT = 64 * 1024
MATERIAL_FILE_LIMIT = 8 * 1024 * 1024
DIGEST = re.compile(r"[0-9a-f]{64}")


class BriefError(ValueError):
    """A missing, stale, ambiguous or out-of-scope handoff."""


def _unique_object(pairs):
    result = {}
    for name, value in pairs:
        if name in result:
            raise BriefError("duplicate record field")
        result[name] = value
    return result


def _object(value, fields):
    if not isinstance(value, dict) or value.keys() != fields:
        raise BriefError("missing or unexpected record fields")


def _text(value):
    return isinstance(value, str) and bool(value.strip()) and value == value.strip()


def _strings(value, *, required=False):
    if (
        not isinstance(value, list)
        or (required and not value)
        or any(not _text(item) for item in value)
    ):
        raise BriefError("invalid scope, check or criterion list")


def _relative(value):
    path = PurePosixPath(value)
    if (
        not path.parts
        or path.is_absolute()
        or path.as_posix() != value
        or any(part == ".." or part.casefold() == ".git" for part in path.parts)
        or "\\" in value
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        raise BriefError("invalid workspace-relative path")
    return path


def _validate_binding(record):
    if any(not _text(record[key]) for key in REQUEST_TEXT):
        raise BriefError("missing goal or request identity")
    if not DIGEST.fullmatch(record["request_digest"]):
        raise BriefError("invalid request digest")
    if (
        not _text(record["brief_id"])
        or type(record["revision"]) is not int
        or record["revision"] < 1
    ):
        raise BriefError("invalid brief identity or revision")
    for key in REQUEST_LISTS:
        _strings(record[key], required=key in {"in_scope", "acceptance_criteria"})
    for value in record["allowed_mutations"]:
        _relative(value)
    if record["risk"] not in ("low", "medium", "high"):
        raise BriefError("invalid risk")
    authority = record["authority_ref"]
    if authority is not None and (
        not _text(authority)
        or authority.casefold() in {"none", "pending", "tbd", "todo"}
        or "{{" in authority
        or "}}" in authority
    ):
        raise BriefError("invalid authority reference")
    inputs = record["material_inputs"]
    if not isinstance(inputs, dict) or len(inputs) > 32:
        raise BriefError("invalid material input set")
    for path, expected in inputs.items():
        _relative(path)
        if expected != "absent" and (
            not isinstance(expected, str) or not DIGEST.fullmatch(expected)
        ):
            raise BriefError("invalid material input state")


def _validate_brief(brief):
    _object(brief, BRIEF_FIELDS)
    _validate_binding(brief)
    if brief["contract_version"] != BRIEF_VERSION:
        raise BriefError("invalid brief edition")
    _strings(brief["assumptions"])
    if not isinstance(brief["known_facts"], list):
        raise BriefError("invalid facts")
    for fact in brief["known_facts"]:
        _object(fact, {"claim", "source_refs"})
        if (
            not _text(fact["claim"])
            or not isinstance(fact["source_refs"], list)
            or not fact["source_refs"]
        ):
            raise BriefError("fact lacks source references")
        for source in fact["source_refs"]:
            _object(source, SOURCE_FIELDS)
            if (
                any(not _text(source[key]) for key in SOURCE_FIELDS)
                or source["kind"] not in ("document", "code", "session", "observation")
                or source["trust"] not in ("untrusted", "reviewed-source")
            ):
                raise BriefError("invalid fact source")
    questions = brief["unresolved_questions"]
    if not isinstance(questions, list):
        raise BriefError("invalid questions")
    for question in questions:
        _object(question, {"question", "affected_actions", "recommendation"})
        _strings(question["affected_actions"], required=True)
        if not _text(question["question"]) or not _text(question["recommendation"]):
            raise BriefError("unresolved question lacks context")
    if brief["state"] not in ("ready", "needs-clarification"):
        raise BriefError("brief is stale, withdrawn or unready")
    if bool(questions) != (brief["state"] == "needs-clarification"):
        raise BriefError("brief state contradicts its unresolved questions")


def _identity(root):
    result = subprocess.run(
        ["/usr/bin/git", "-C", str(root), "rev-parse", "--show-toplevel", "HEAD"],
        env={
            "PATH": "/usr/bin:/bin",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_OPTIONAL_LOCKS": "0",
        },
        check=True,
        capture_output=True,
        text=True,
        timeout=5,
    ).stdout.splitlines()
    if len(result) != 2 or result[0] != str(root):
        raise BriefError("root does not identify the Git workspace")
    return result[1]


def _check_material_input(path, expected):
    if expected != "absent":
        payload = read_bytes(path, max_bytes=MATERIAL_FILE_LIMIT)
        if hashlib.sha256(payload).hexdigest() != expected:
            raise BriefError("material input changed")
        return
    with ExitStack() as stack:
        try:
            parent, name = stack.enter_context(open_parent(path))
            os.stat(name, dir_fd=parent, follow_symlinks=False)
        except FileNotFoundError:
            return
    raise BriefError("material input changed")


def check(brief, current, root, *, operation, action, paths):
    """Compare current scope and inputs. Authenticity belongs to the caller."""
    _validate_brief(brief)
    _object(current, CURRENT_FIELDS)
    _validate_binding(current)
    actions = current["allowed_actions"]
    if not isinstance(actions, dict) or not actions:
        raise BriefError("current request lacks scoped actions")
    if current["state"] != "current":
        raise BriefError("current request was withdrawn or is unavailable")
    # D08 4.1.0: a material change invalidates only the work that reads it, so
    # material inputs are compared per action below; every other field binds all.
    for key in sorted(BOUND_FIELDS - {"material_inputs"}):
        if brief[key] != current[key]:
            raise BriefError(f"brief does not match current {key}")
    root = root.resolve(strict=True)
    if current["workspace_id"] != str(root) or current["baseline_id"] != _identity(
        root
    ):
        raise BriefError("workspace or Git baseline changed")
    if action not in actions or any(
        action in question["affected_actions"]
        for question in brief["unresolved_questions"]
    ):
        raise BriefError("action is outside current scope or needs clarification")
    selected = actions[action]
    if not isinstance(selected, dict) or set(selected) not in (
        {"operation", "paths"},
        {"operation", "paths", "inputs"},
    ):
        raise BriefError("invalid action binding")
    _strings(selected["paths"])
    if selected["operation"] != operation:
        raise BriefError("operation is outside current action scope")
    if operation == "state-change" and not paths:
        raise BriefError("state change lacks a target path")
    if paths and current["authority_ref"] is None:
        raise BriefError("mutation lacks a separately supplied authority reference")
    if set(paths) != set(selected["paths"]) or set(paths) - set(
        current["allowed_mutations"]
    ):
        raise BriefError("mutation path is outside current scope")
    material_inputs = current["material_inputs"]
    if set(paths) - material_inputs.keys():
        raise BriefError("mutation target lacks a material input binding")
    # An action that names its inputs reads only them and its targets; an
    # action that names none reads every material input, as before.
    if "inputs" in selected:
        _strings(selected["inputs"])
        if set(selected["inputs"]) - material_inputs.keys():
            raise BriefError("action names an unknown material input")
        read = set(paths) | set(selected["inputs"])
    else:
        read = set(material_inputs)
    for path in sorted(read):
        if brief["material_inputs"].get(path) != material_inputs[path]:
            raise BriefError("brief does not match current material_inputs")
        _check_material_input(root / _relative(path), material_inputs[path])
    if current["baseline_id"] != _identity(root):
        raise BriefError("Git baseline changed during preflight")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--brief", type=Path, required=True)
    parser.add_argument("--current-request", type=Path, required=True)
    parser.add_argument(
        "--operation", choices=("dispatch", "resume", "state-change"), required=True
    )
    parser.add_argument("--action", required=True)
    parser.add_argument("--path", action="append", default=[])
    args = parser.parse_args(argv)
    try:
        brief = json.loads(
            read_bytes(args.brief, max_bytes=BYTE_LIMIT),
            object_pairs_hook=_unique_object,
        )
        current = json.loads(
            read_bytes(args.current_request, max_bytes=BYTE_LIMIT),
            object_pairs_hook=_unique_object,
        )
        check(
            brief,
            current,
            args.root,
            operation=args.operation,
            action=args.action,
            paths=args.path,
        )
    except BriefError as exc:
        print(f"FAIL BRIEF: {exc}", file=sys.stderr)
        return 1
    except (ValueError, OSError, RecursionError, subprocess.SubprocessError):
        print("FAIL BRIEF: invalid or unavailable input", file=sys.stderr)
        return 1
    print("PASS BRIEF: current request and scope match; authorization is separate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
