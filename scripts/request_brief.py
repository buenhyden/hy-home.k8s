#!/usr/bin/env python3
"""Bind a provider request to a shown brief before its first change (D08).

`intake` runs on each provider's UserPromptSubmit hook. It keeps one receipt per
provider session: a digest of the prompt (never its text), a generation, the
Codex turn, the workspace root, its branch and a digest of the policy files.
It tells the model to show the user a brief and record it.

`record` is the model's call after it has shown the brief in its reply. It
binds the brief to the current request and refuses a superseded request, a
different workspace or a branch or policy that changed since the request.

`admit` is called by scripts/provider_write_guard.py for a call it sees as a
change. It refuses a missing, stale, unrecorded or other-workspace receipt,
shows the recorded brief to the user through the hook's systemMessage on the
first admitted change, and then lets later changes of the same request
through. Read-only work never reaches it.

A receipt is local state, not evidence that the user saw the brief; that is a
separate native observation.
"""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

PROVIDERS = ("claude", "codex")
STATE_ENV = "HYK8S_REQUEST_BRIEF_STATE_DIR"
STATE_NAME = "request-briefs"
GIT_TIMEOUT_SECONDS = 5
BYTE_LIMIT = 64 * 1024
# The files whose change makes an earlier brief stale before its first change.
POLICY_FILES = (
    "AGENTS.md",
    "CLAUDE.md",
    ".agents/governance/agent-execution.md",
    ".agents/governance/approval-and-safety.md",
    ".agents/workflows/work-lifecycle.md",
    "docs/00.workspace/04.quality/quality.md",
    ".claude/settings.json",
    ".codex/hooks.json",
    ".codex/config.toml",
    "scripts/request_brief.py",
)
BRIEF_LISTS = ("scope", "keep", "change", "questions", "checks")
REQUIRED_LISTS = ("scope", "change", "checks")


class Refusal(Exception):
    """A change the current request has not been briefed for."""

    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _git(root: str, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", root, *arguments],
        capture_output=True,
        text=True,
        timeout=GIT_TIMEOUT_SECONDS,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def branch(root: str) -> str:
    name = _git(root, "symbolic-ref", "--short", "-q", "HEAD")
    return name or "detached:" + _git(root, "rev-parse", "HEAD")


def workspace(root: str) -> str:
    """The repository a root belongs to; its linked worktrees share it."""
    return _git(root, "rev-parse", "--path-format=absolute", "--git-common-dir")


def policy_digest(root: str) -> str:
    digest = hashlib.sha256()
    for relative in POLICY_FILES:
        path = Path(root, relative)
        try:
            content = hashlib.sha256(path.read_bytes()).hexdigest()
        except FileNotFoundError:
            content = "absent"
        digest.update(f"{relative}\0{content}\n".encode())
    return digest.hexdigest()


def state_dir(root: str) -> Path:
    override = os.environ.get(STATE_ENV)
    if override:
        directory = Path(override)
    else:
        common = workspace(root)
        if not common:
            raise Refusal("BRIEF-STATE", "the workspace has no Git common directory")
        directory = Path(common) / STATE_NAME
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    status = os.lstat(directory)
    if status.st_uid != os.geteuid() or status.st_mode & 0o077:
        raise Refusal("BRIEF-STATE", "the receipt directory is not private")
    return directory


@contextlib.contextmanager
def _locked(directory: Path):
    # Parallel hook calls carry no order, so every read-modify-write holds it.
    with open(directory / ".lock", "a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def _path(directory: Path, provider: str, session: str) -> Path:
    key = hashlib.sha256(
        f"{provider}\0{session}".encode("utf-8", "surrogatepass")
    ).hexdigest()[:32]
    return directory / f"{key}.json"


def _load(path: Path) -> dict | None:
    try:
        if path.stat().st_size > BYTE_LIMIT:
            return None
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return value if isinstance(value, dict) else None


def _save(path: Path, receipt: dict) -> None:
    handle, temporary = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    with os.fdopen(handle, "w", encoding="utf-8") as stream:
        json.dump(receipt, stream, sort_keys=True)
    os.replace(temporary, path)


def _session(payload: dict) -> str:
    session = payload.get("session_id")
    if not isinstance(session, str) or not session.strip():
        raise Refusal("BRIEF-MISSING", "the hook payload names no session")
    return session


def intake(payload: dict, provider: str, root: str) -> dict:
    """Start a new request generation for this session; return the receipt."""
    session = _session(payload)
    prompt = payload.get("prompt")
    if not isinstance(prompt, str):
        raise Refusal("BRIEF-INTAKE", "the hook payload carries no prompt")
    directory = state_dir(root)
    path = _path(directory, provider, session)
    with _locked(directory):
        previous = _load(path) or {}
        generation = int(previous.get("generation", 0)) + 1
        request_digest = hashlib.sha256(prompt.encode()).hexdigest()
        receipt = {
            "request_id": hashlib.sha256(
                f"{provider}\0{session}\0{generation}\0{request_digest}".encode()
            ).hexdigest()[:16],
            "request_digest": request_digest,
            "provider": provider,
            "session": session,
            "surface": os.environ.get("CLAUDE_CODE_ENTRYPOINT", "cli"),
            "turn": payload.get("turn_id"),
            "generation": generation,
            "root": root,
            "workspace": workspace(root),
            "branch": branch(root),
            "policy_digest": policy_digest(root),
            "received_at": _now(),
            "state": "received",
        }
        _save(path, receipt)
    return receipt


def intake_context(receipt: dict) -> str:
    return (
        f"Request {receipt['request_id']} (generation {receipt['generation']}) "
        "is bound to this workspace. Read-only discovery needs nothing more. "
        "Before the first change, show the user a short brief in your reply "
        "(goal, scope, what you keep, what you change, open questions, checks), "
        "then record that same brief as JSON with keys goal, scope, keep, "
        "change, questions and checks: `python3 scripts/request_brief.py record "
        f"--request {receipt['request_id']}` with the JSON on stdin. The write "
        "guard refuses a change until then. Ask only about real conflicts."
    )


def _validate_brief(brief: object) -> dict:
    if not isinstance(brief, dict) or set(brief) != {"goal", *BRIEF_LISTS}:
        raise Refusal("BRIEF-SHAPE", "brief keys are goal, " + ", ".join(BRIEF_LISTS))
    if not isinstance(brief["goal"], str) or not brief["goal"].strip():
        raise Refusal("BRIEF-SHAPE", "the brief states no goal")
    for key in BRIEF_LISTS:
        items = brief[key]
        if not isinstance(items, list) or any(
            not isinstance(item, str) or not item.strip() for item in items
        ):
            raise Refusal("BRIEF-SHAPE", f"{key} is not a list of statements")
        if key in REQUIRED_LISTS and not items:
            raise Refusal("BRIEF-SHAPE", f"the brief states no {key}")
    return brief


def _same_workspace(receipt: dict, root: str) -> None:
    if receipt.get("workspace") != workspace(root):
        raise Refusal("BRIEF-WORKSPACE", "the request belongs to another workspace")


def _unchanged(receipt: dict) -> None:
    """Before the first change, the request's branch and policy still hold."""
    origin = receipt["root"]
    if receipt.get("branch") != branch(origin) or receipt.get(
        "policy_digest"
    ) != policy_digest(origin):
        raise Refusal(
            "BRIEF-STALE",
            "the branch or policy changed since the request; a new request is needed",
        )


def record(request_id: str, brief: object, root: str) -> dict:
    """Bind a brief the model has shown to the current request of its session."""
    brief = _validate_brief(brief)
    directory = state_dir(root)
    with _locked(directory):
        for path in sorted(directory.glob("*.json")):
            receipt = _load(path)
            if receipt and receipt.get("request_id") == request_id:
                break
        else:
            raise Refusal("BRIEF-STALE", "the request is unknown or superseded")
        _same_workspace(receipt, root)
        _unchanged(receipt)
        if receipt["state"] == "admitted":
            raise Refusal("BRIEF-STALE", "the request already made its first change")
        encoded = json.dumps(brief, sort_keys=True, ensure_ascii=False)
        receipt.update(
            brief=brief,
            brief_digest=hashlib.sha256(encoded.encode()).hexdigest(),
            recorded_at=_now(),
            state="recorded",
        )
        _save(path, receipt)
    return receipt


def current(request_id: str, root: str) -> dict:
    """The request's receipt, if its brief is recorded and still current.

    A dispatcher calls this before it starts a provider worker. A later
    request in the same session supersedes the receipt, and a policy change
    makes it stale; an admitted request may have moved to its work branch.
    """
    directory = state_dir(root)
    with _locked(directory):
        for path in sorted(directory.glob("*.json")):
            receipt = _load(path)
            if receipt and receipt.get("request_id") == request_id:
                break
        else:
            raise Refusal("BRIEF-STALE", "the request is unknown or superseded")
    _same_workspace(receipt, root)
    if receipt.get("state") == "admitted":
        if receipt.get("policy_digest") != policy_digest(receipt["root"]):
            raise Refusal("BRIEF-STALE", "the policy changed since the request")
    elif receipt.get("state") == "recorded":
        _unchanged(receipt)
    else:
        raise Refusal(
            "BRIEF-NOT-SHOWN",
            f"show the user a brief and record it for request {request_id} first",
        )
    return receipt


def display(receipt: dict) -> str:
    brief = receipt["brief"]
    lines = [
        f"Brief for request {receipt['request_id']} "
        f"(generation {receipt['generation']}, {receipt['provider']}): "
        f"{brief['goal']}"
    ]
    for key in BRIEF_LISTS:
        if brief[key]:
            lines.append(f"{key.capitalize()}: " + "; ".join(brief[key]))
    return "\n".join(lines)


def admit(payload: dict, provider: str, root: str) -> str | None:
    """Admit a change; return the brief to show on the first admitted change."""
    session = _session(payload)
    directory = state_dir(root)
    path = _path(directory, provider, session)
    with _locked(directory):
        receipt = _load(path)
        if receipt is None:
            raise Refusal("BRIEF-MISSING", "no request was received for this session")
        _same_workspace(receipt, root)
        turn = payload.get("turn_id")
        if turn is not None and turn != receipt.get("turn"):
            raise Refusal("BRIEF-STALE", "the change belongs to another turn")
        state = receipt.get("state")
        if state == "admitted":
            return None
        if state != "recorded":
            raise Refusal(
                "BRIEF-NOT-SHOWN",
                f"show the user a brief and record it for request "
                f"{receipt.get('request_id')} before the first change",
            )
        _unchanged(receipt)
        receipt.update(admitted_at=_now(), state="admitted")
        _save(path, receipt)
    return display(receipt)


def project_root(provider: str) -> str:
    directory = os.environ.get("CLAUDE_PROJECT_DIR", "") if provider == "claude" else ""
    if not directory:
        directory = _git(os.getcwd(), "rev-parse", "--show-toplevel") or os.getcwd()
    return str(Path(directory).resolve())


def _read_stdin() -> object:
    raw = sys.stdin.buffer.read(BYTE_LIMIT + 1)
    if len(raw) > BYTE_LIMIT:
        raise Refusal("BRIEF-SHAPE", "input is too large")
    return json.loads(raw.decode("utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    hook = commands.add_parser("intake")
    hook.add_argument("--provider", required=True, choices=PROVIDERS)
    recorder = commands.add_parser("record")
    recorder.add_argument("--request", required=True)
    recorder.add_argument("--root", default="")
    arguments = parser.parse_args(argv)

    if arguments.command == "intake":
        # Intake never blocks a prompt: without a receipt the guard refuses
        # the first change instead, and read-only work goes on.
        try:
            payload = _read_stdin()
            if not isinstance(payload, dict):
                return 0
            receipt = intake(
                payload, arguments.provider, project_root(arguments.provider)
            )
        except Exception:  # noqa: BLE001 - see above
            return 0
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "UserPromptSubmit",
                        "additionalContext": intake_context(receipt),
                    }
                }
            )
        )
        return 0

    root = str(Path(arguments.root or project_root("codex")).resolve())
    try:
        receipt = record(arguments.request, _read_stdin(), root)
    except Refusal as refusal:
        print(f"[FAIL] {refusal}", file=sys.stderr)
        return 1
    except (OSError, ValueError):
        print("[FAIL] BRIEF-SHAPE: the brief is not valid JSON", file=sys.stderr)
        return 1
    print(f"PASS BRIEF-RECORDED: {receipt['request_id']}; shown on the first change")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
