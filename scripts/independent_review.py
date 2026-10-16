#!/usr/bin/env python3
"""Publish a local independent review verdict as the review App's check run."""

from __future__ import annotations

import argparse
import base64
import http.client
import json
import os
import re
import stat
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


API = "https://api.github.com"
CHECK_NAME = "independent-review"
REPO = re.compile(r"[A-Za-z0-9-]+/[A-Za-z0-9._-]+")
SHA = re.compile(r"[0-9a-f]{40}")
SEVERITIES = ("critical", "high", "medium", "low")
BLOCKING = {"critical", "high"}
VERDICT_KEYS = {"head_sha", "reviewer", "decision", "summary", "findings"}
FINDING_KEYS = {"severity", "path", "message"}
MAX_FINDINGS = 100
MAX_TEXT = 4000
MAX_SUMMARY = 60000


class ReviewError(Exception):
    """Raised when a verdict, key or remote state cannot be published."""


def _text(value: object, name: str, limit: int, *, empty: bool = False) -> str:
    if not isinstance(value, str) or (not empty and not value.strip()):
        raise ReviewError(f"{name} must be a non-empty string")
    if len(value) > limit:
        raise ReviewError(f"{name} exceeds {limit} characters")
    return value


def load_verdict(data: object) -> dict:
    """Return a verdict after checking its exact shape."""

    if not isinstance(data, dict) or set(data) != VERDICT_KEYS:
        raise ReviewError(f"verdict keys must be exactly {sorted(VERDICT_KEYS)}")
    if not isinstance(data["head_sha"], str) or not SHA.fullmatch(data["head_sha"]):
        raise ReviewError("head_sha must be a forty-character commit SHA")
    if data["decision"] not in ("approve", "request_changes"):
        raise ReviewError("decision must be approve or request_changes")
    _text(data["reviewer"], "reviewer", 200)
    _text(data["summary"], "summary", MAX_TEXT)
    findings = data["findings"]
    if not isinstance(findings, list) or len(findings) > MAX_FINDINGS:
        raise ReviewError(f"findings must be a list of at most {MAX_FINDINGS}")
    for finding in findings:
        if not isinstance(finding, dict) or set(finding) != FINDING_KEYS:
            raise ReviewError(f"finding keys must be exactly {sorted(FINDING_KEYS)}")
        if finding["severity"] not in SEVERITIES:
            raise ReviewError(f"finding severity must be one of {SEVERITIES}")
        _text(finding["path"], "finding path", 500, empty=True)
        _text(finding["message"], "finding message", MAX_TEXT)
    return data


def conclusion(verdict: dict) -> str:
    """Pass only an approval that carries no blocking finding."""

    blocked = any(f["severity"] in BLOCKING for f in verdict["findings"])
    return "success" if verdict["decision"] == "approve" and not blocked else "failure"


def render(verdict: dict) -> tuple[str, str]:
    """Return the check-run title and Markdown summary."""

    result = conclusion(verdict)
    title = f"{verdict['decision']} by {verdict['reviewer']}"
    if verdict["decision"] == "approve" and result == "failure":
        title += " (blocked by critical/high finding)"
    truncated = "\n\n_Summary truncated; see the reviewer's full verdict._"
    lines = [
        f"Reviewed head `{verdict['head_sha']}`; conclusion `{result}`.",
        "",
        verdict["summary"],
    ]
    if verdict["findings"]:
        lines += ["", "| Severity | Path | Finding |", "| --- | --- | --- |"]
        for finding in verdict["findings"]:
            path = f"`{finding['path'].replace('`', '')}`" if finding["path"] else "-"
            cells = [finding["severity"], path, finding["message"]]
            lines.append(
                "| "
                + " | ".join(c.replace("|", "\\|").replace("\n", " ") for c in cells)
                + " |"
            )
    summary = "\n".join(lines)
    if len(summary) > MAX_SUMMARY:
        summary = summary[: MAX_SUMMARY - len(truncated)] + truncated
    return title[:200], summary


def check_key_file(path: Path) -> Path:
    """Require a regular private key file owned by and readable only by us."""

    try:
        info = path.lstat()
    except OSError as exc:
        raise ReviewError("review App key file is unreadable") from exc
    if (
        not stat.S_ISREG(info.st_mode)
        or info.st_mode & 0o077
        or info.st_uid != os.getuid()
    ):
        raise ReviewError("review App key must be our own regular file with mode 0600")
    return path


def _b64(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def app_jwt(app_id: str, key_file: Path) -> str:
    """Sign a short-lived App JWT with the local key through openssl."""

    now = int(time.time())
    header = _b64(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    payload = _b64(
        json.dumps({"iat": now - 60, "exp": now + 540, "iss": app_id}).encode()
    )
    signing_input = f"{header}.{payload}".encode("ascii")
    try:
        signed = subprocess.run(
            ["openssl", "dgst", "-sha256", "-sign", str(key_file)],
            input=signing_input,
            capture_output=True,
            check=False,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ReviewError(f"openssl failed: {type(exc).__name__}") from None
    if signed.returncode != 0 or not signed.stdout:
        raise ReviewError("openssl could not sign the App JWT")
    return f"{header}.{payload}.{_b64(signed.stdout)}"


def github(method: str, path: str, auth: str, body: dict | None = None) -> dict:
    data = None if body is None else json.dumps(body).encode()
    request = urllib.request.Request(
        API + path,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": auth,
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "hy-home-independent-review",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
        return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raise ReviewError(f"GitHub {method} {path} returned {exc.code}") from None
    except (OSError, http.client.HTTPException, ValueError) as exc:
        raise ReviewError(f"GitHub {method} {path} failed: {type(exc).__name__}")


def publish(repo: str, pr: int, verdict: dict, app_id: str, key_file: Path) -> dict:
    """Bind the verdict to the open PR head and create the check run."""

    jwt = "Bearer " + app_jwt(app_id, key_file)
    installation = github("GET", f"/repos/{repo}/installation", jwt)
    token = github(
        "POST",
        f"/app/installations/{installation['id']}/access_tokens",
        jwt,
        {
            "repositories": [repo.split("/", 1)[1]],
            "permissions": {"checks": "write", "pull_requests": "read"},
        },
    )["token"]
    auth = "token " + token
    try:
        pull = github("GET", f"/repos/{repo}/pulls/{pr}", auth)
        if pull["state"] != "open" or pull["base"]["ref"] != "main":
            raise ReviewError("pull request must be open against main")
        if pull["head"]["sha"] != verdict["head_sha"]:
            raise ReviewError("verdict head_sha is not the pull request's current head")
        title, summary = render(verdict)
        return github(
            "POST",
            f"/repos/{repo}/check-runs",
            auth,
            {
                "name": CHECK_NAME,
                "head_sha": verdict["head_sha"],
                "status": "completed",
                "conclusion": conclusion(verdict),
                "output": {"title": title, "summary": summary},
            },
        )
    finally:
        try:
            github("DELETE", "/installation/token", auth)
        except ReviewError:
            print(
                "WARN: token revocation failed; it expires within one hour",
                file=sys.stderr,
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--pr", type=int, required=True)
    parser.add_argument("--verdict", type=Path, required=True)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="validate the verdict and print its conclusion without publishing",
    )
    args = parser.parse_args()
    try:
        if not REPO.fullmatch(args.repo) or args.pr < 1:
            raise ReviewError("repo must be owner/name and pr a positive number")
        try:
            data = json.loads(args.verdict.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ReviewError("verdict must be a readable JSON file") from exc
        verdict = load_verdict(data)
        if args.check_only:
            print(f"{CHECK_NAME} conclusion={conclusion(verdict)} (not published)")
            return 0
        app_id = os.environ.get("REVIEW_APP_ID", "")
        if not app_id.isdecimal():
            raise ReviewError("REVIEW_APP_ID must name the review App ID")
        key_file = check_key_file(Path(os.environ.get("REVIEW_APP_KEY_FILE", "")))
        run = publish(args.repo, args.pr, verdict, app_id, key_file)
        line = (
            f"{CHECK_NAME} id={run['id']} app={run['app']['id']} "
            f"head={run['head_sha']} conclusion={run['conclusion']} {run['html_url']}"
        )
    except (KeyError, TypeError):
        print("FAIL: unexpected GitHub response shape", file=sys.stderr)
        return 1
    except ReviewError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
