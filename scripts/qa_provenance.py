#!/usr/bin/env python3
"""Authenticate PR QA before the isolated verifier App can issue a proof.

Only stdlib imports: run with python3 -I, from a default-branch checkout.
Fetched trees, job metadata and proof records are data, never executable input.
"""

from __future__ import annotations

import argparse
import base64
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from typing import Any, Mapping
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

PROOF_LIMIT = 16 * 1024
API_LIMIT = 8 * 1024 * 1024
MAX_PAGES = 3
MAX_COMMITS = 250
CI_PATH = ".github/workflows/ci.yml"
REGISTRY_PATH = "scripts/validation/registry.json"
LOCK_PATH = ".github/requirements/ci-validation.txt"
CHECKOUT_PREFIX = "Checkout QA commit "
APP_PERMISSIONS = {
    "metadata": "read",
    "actions": "read",
    "contents": "read",
    "pull_requests": "read",
    "checks": "write",
}
CONTROL_PREFIXES = (
    "scripts/",
    ".github/workflows/",
    ".github/actions/",
    ".github/requirements/",
    ".agents/evaluations/",
)
CONTROL_FILES = {".pre-commit-config.yaml", ".python-version", "pyproject.toml"}


@dataclass(frozen=True)
class Proof:
    record: dict


@dataclass(frozen=True)
class Reject:
    reason: str


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def sha(value):
    require(
        isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value),
        "invalid Git identity",
    )
    return value


def positive(value):
    require(type(value) is int and 0 < value < 2**63, "invalid provider ID")
    return value


def utc_now():
    return datetime.now(timezone.utc)


def fresh(value):
    require(
        isinstance(value, str) and re.fullmatch(r"[0-9-]{10}T[0-9:]{8}Z", value),
        "invalid timestamp",
    )
    age = (
        utc_now() - datetime.fromisoformat(value.replace("Z", "+00:00"))
    ).total_seconds()
    require(0 <= age <= 30 * 86400, "proof is expired or from the future")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def decode(payload, limit):
    require(
        isinstance(payload, bytes) and len(payload) <= limit, "JSON byte limit exceeded"
    )
    return json.loads(payload, object_pairs_hook=unique_object)


def encode_proof(proof):
    payload = json.dumps(proof.record, sort_keys=True, separators=(",", ":"))
    require(len(payload.encode()) <= PROOF_LIMIT, "proof byte limit exceeded")
    return payload


def parse_proof(payload):
    record = decode(payload, PROOF_LIMIT)
    require(
        set(record)
        == {
            "version",
            "repository",
            "pr",
            "base",
            "head",
            "checkout",
            "workflow",
            "source",
            "registry",
            "tools",
            "gates",
            "completed_at",
        },
        "invalid proof fields",
    )
    require(
        type(record["version"]) is int and record["version"] == 1,
        "unsupported proof version",
    )
    repository = record["repository"]
    require(
        set(repository) == {"id", "name"}
        and re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository["name"]),
        "invalid repository",
    )
    positive(repository["id"])
    positive(record["pr"])
    for key in ("base", "head", "registry"):
        sha(record[key])
    require(set(record["checkout"]) == {"commit", "tree"}, "invalid checkout")
    for value in record["checkout"].values():
        sha(value)
    require(
        set(record["workflow"]) == {"id", "path", "revision", "blob"},
        "invalid workflow",
    )
    positive(record["workflow"]["id"])
    require(record["workflow"]["path"] == CI_PATH, "wrong workflow")
    sha(record["workflow"]["revision"])
    sha(record["workflow"]["blob"])
    require(set(record["source"]) == {"run", "attempt", "job"}, "invalid source")
    for value in record["source"].values():
        positive(value)
    require(
        set(record["tools"]) == {"lock", "runtime"}
        and record["tools"]["runtime"] == "unattested",
        "invalid tools",
    )
    sha(record["tools"]["lock"])
    gates = record["gates"]
    require(isinstance(gates, dict) and 0 < len(gates) <= 128, "invalid gates")
    for name, disposition in gates.items():
        require(
            re.fullmatch(r"[a-z][a-z0-9-]{0,127}", name) and disposition == "PASS",
            "incomplete gate",
        )
    fresh(record["completed_at"])
    return Proof(record)


def read_check(check, app_id):
    """Parse only the expected App's bounded check; callers still bind its source."""
    try:
        require(
            check["name"] == "qa-provenance" and check["app"]["id"] == positive(app_id),
            "wrong check author",
        )
        require(
            check["status"] == "completed" and check["conclusion"] == "success",
            "check did not pass",
        )
        proof = parse_proof(check["output"]["text"].encode())
        require(
            check["head_sha"] == proof.record["checkout"]["commit"], "wrong check SHA"
        )
        require(check["external_id"] == source_id(proof), "wrong check source")
        return proof
    except (ValueError, TypeError, KeyError, AttributeError, RecursionError):
        return Reject("invalid or unauthenticated check proof")


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("API redirect refused")


class GitHubReader:
    def __init__(
        self, token, repository, repository_id, workflow_id, baseline, *, root=None
    ):
        require(
            re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository),
            "invalid repository",
        )
        self.token, self.repository = token, repository
        self.repository_id, self.workflow_id = (
            positive(repository_id),
            positive(workflow_id),
        )
        self.baseline = sha(baseline)
        self.root = root or Path(__file__).resolve().parents[1]
        self.deadline, self.requests = time.monotonic() + 180, 0

    def request(self, route, *, method="GET", body=None, token=None):
        self.requests += 1
        remaining = self.deadline - time.monotonic()
        require(
            self.requests <= 600 and remaining > 0, "API request/time limit exceeded"
        )
        require(
            route.startswith(("/repos/" + self.repository, "/app/", "/installation/"))
            and ".." not in route
            and not re.search(r"[\s#]", route),
            "invalid API route",
        )
        request = Request(
            "https://api.github.com" + route,
            data=None if body is None else json.dumps(body).encode(),
            method=method,
            headers={
                "Authorization": "Bearer " + (token or self.token),
                "Accept": "application/vnd.github+json",
                "Content-Type": "application/json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "qa-provenance",
            },
        )
        with build_opener(NoRedirect).open(
            request, timeout=min(10, remaining)
        ) as response:
            payload = response.read(API_LIMIT + 1)
        return decode(payload, API_LIMIT) if payload else None

    def get(self, route):
        return self.request(
            "/repos/" + self.repository + ("/" + route if route else "")
        )

    def pages(self, route, *, field=None, count=None):
        items = []
        for page in range(1, MAX_PAGES + 1):
            response = self.get(route + f"?per_page=100&page={page}")
            rows = response[field] if field else response
            require(isinstance(rows, list) and len(rows) <= 100, "invalid API page")
            if field:
                total = positive(response["total_count"])
                require(count is None or count == total, "API count changed")
                count = total
            items.extend(rows)
            if len(rows) < 100:
                require(count is None or len(items) == count, "incomplete API list")
                return items
        raise ValueError("API pagination limit exceeded")

    def commit(self, revision):
        result = self.get("git/commits/" + sha(revision))
        require(result["sha"] == revision, "wrong Git commit")
        sha(result["tree"]["sha"])
        return result

    def controls(self, commit):
        tree_sha = commit["tree"]["sha"]
        tree = self.get("git/trees/" + sha(tree_sha) + "?recursive=1")
        require(
            tree["sha"] == tree_sha and tree["truncated"] is False,
            "incomplete Git tree",
        )
        require(
            isinstance(tree["tree"], list) and len(tree["tree"]) <= 100000,
            "tree limit exceeded",
        )
        controls, seen = {}, set()
        for entry in tree["tree"]:
            path = entry["path"]
            require(
                isinstance(path, str) and len(path) <= 4096 and path not in seen,
                "invalid tree path",
            )
            seen.add(path)
            if entry["type"] != "tree" and (
                path.startswith(CONTROL_PREFIXES)
                or path in CONTROL_FILES
                or (path.startswith(".agents/skills/") and "/scripts/" in path)
            ):
                require(
                    entry["type"] == "blob" and entry["mode"] in ("100644", "100755"),
                    "unsafe control file mode",
                )
                controls[path] = (entry["mode"], sha(entry["sha"]))
        return controls


def source_id(proof):
    return ":".join(
        str(proof.record["source"][key]) for key in ("run", "attempt", "job")
    )


def repo_matches(value, github):
    return (
        value["id"] == github.repository_id and value["full_name"] == github.repository
    )


def successful(value):
    require(
        value["status"] == "completed" and value["conclusion"] == "success",
        "source did not complete successfully",
    )


def trusted_bytes(github, controls, path):
    payload = (github.root / path).read_bytes()
    require(len(payload) <= API_LIMIT, "control byte limit exceeded")
    identity = hashlib.sha1(
        b"blob " + str(len(payload)).encode() + b"\0" + payload
    ).hexdigest()
    require(controls[path][1] == identity, "executing control differs from baseline")
    return payload


def verify_pr(event: Mapping[str, Any], github: GitHubReader) -> Proof | Reject:
    try:
        return _verify_pr(event, github)
    except (
        ValueError,
        TypeError,
        KeyError,
        IndexError,
        AttributeError,
        OSError,
        RecursionError,
    ):
        return Reject(
            "PR source authentication failed; run full QA and inspect protected control settings"
        )


def _verify_pr(event, github):
    require(
        event["action"] == "completed" and repo_matches(event["repository"], github),
        "wrong event repository",
    )
    repo = github.get("")
    require(
        repo_matches(repo, github) and repo["default_branch"] == "main",
        "wrong repository",
    )
    source = event["workflow_run"]
    run_id, attempt = positive(source["id"]), positive(source["run_attempt"])
    route = f"actions/runs/{run_id}"
    current = github.get(route)
    run = github.get(route + f"/attempts/{attempt}")
    fields = ("id", "run_attempt", "workflow_id", "event", "head_sha", "path")
    require(
        all(run[key] == source[key] == current[key] for key in fields),
        "source run or attempt changed",
    )
    successful(source)
    successful(current)
    successful(run)
    require(
        all(
            repo_matches(value["repository"], github)
            for value in (source, current, run)
        ),
        "wrong source repository",
    )
    require(
        run["workflow_id"] == github.workflow_id
        and run["event"] == "pull_request"
        and run["path"] == CI_PATH,
        "wrong workflow/event",
    )
    workflow = github.get(f"actions/workflows/{github.workflow_id}")
    require(
        workflow["id"] == github.workflow_id
        and workflow["path"] == CI_PATH
        and workflow["state"] == "active",
        "workflow is not active CI",
    )
    require(len(run["pull_requests"]) == 1, "ambiguous PR source")
    relation = run["pull_requests"][0]
    number = positive(relation["number"])
    pr = github.get(f"pulls/{number}")
    require(pr["number"] == number and pr["state"] == "open", "PR no longer open")
    base, head = sha(pr["base"]["sha"]), sha(pr["head"]["sha"])
    require(
        pr["base"]["ref"] == "main" and repo_matches(pr["base"]["repo"], github),
        "wrong PR base",
    )
    require(base == github.baseline and head == run["head_sha"], "PR base/head changed")
    require(
        relation["base"]["sha"] == base and relation["head"]["sha"] == head,
        "run PR relation changed",
    )
    require(
        run["head_repository"]["id"] == pr["head"]["repo"]["id"],
        "wrong head repository",
    )
    baseline = github.controls(github.commit(base))
    # Audit every commit tree before interpreting any PR-controlled step name.
    # ponytail: all scripts are protected; narrow only after a dependency audit.
    count = positive(pr["commits"])
    require(count <= MAX_COMMITS, "PR history limit exceeded")
    commits = github.pages(f"pulls/{number}/commits", count=count)
    revisions = [sha(commit["sha"]) for commit in commits]
    require(
        len(set(revisions)) == count and revisions[-1] == head, "incomplete PR history"
    )
    for revision in revisions:
        require(
            github.controls(github.commit(revision)) == baseline,
            "PR changes protected control closure",
        )
    ci = trusted_bytes(github, baseline, CI_PATH)
    trusted_bytes(github, baseline, "scripts/qa_provenance.py")
    require(
        b"name: Checkout QA commit ${{ github.sha }}" in ci
        and b"ref: ${{ github.sha }}" in ci
        and b'run: python3 scripts/qa.py ci --base-ref "$BASE_SHA"' in ci,
        "unsupported CI contract",
    )
    registry = decode(trusted_bytes(github, baseline, REGISTRY_PATH), API_LIMIT)
    gates = registry["profiles"]["full"]
    require(
        registry["profileAliases"]["ci"] == "full"
        and 0 < len(gates) <= 128
        and len(set(gates)) == len(gates),
        "invalid full profile",
    )
    validators = {row["id"]: row for row in registry["validators"]}
    require(
        all(
            validators[key]["optional"] is False
            and validators[key]["evidenceLane"] == "repo-static"
            for key in gates
        ),
        "aggregate can skip a required gate",
    )
    jobs = github.pages(route + f"/attempts/{attempt}/jobs", field="jobs")
    require(
        len(jobs) == 3
        and {job["name"] for job in jobs} == {"qa", "branch-policy", "ci-summary"},
        "ambiguous CI jobs",
    )
    require(
        len({positive(job["id"]) for job in jobs}) == len(jobs),
        "duplicate job identity",
    )
    for job in jobs:
        require(
            job["run_id"] == run_id
            and job["run_attempt"] == attempt
            and job["head_sha"] == head,
            "wrong job source",
        )
        successful(job)
    qa = next(job for job in jobs if job["name"] == "qa")
    steps = qa["steps"]
    require(
        0 < len(steps) <= 100
        and len({positive(step["number"]) for step in steps}) == len(steps),
        "invalid steps",
    )
    checkout = [step for step in steps if step["name"].startswith(CHECKOUT_PREFIX)]
    aggregate = [
        step for step in steps if step["name"] == "Validate repository checkout"
    ]
    require(len(checkout) == len(aggregate) == 1, "missing or ambiguous QA step")
    successful(checkout[0])
    successful(aggregate[0])
    require(checkout[0]["number"] < aggregate[0]["number"], "wrong step order")
    checkout_sha = sha(checkout[0]["name"][len(CHECKOUT_PREFIX) :])
    checkout_commit = github.commit(checkout_sha)
    require(
        [parent["sha"] for parent in checkout_commit["parents"]] == [base, head],
        "checkout is not the PR merge",
    )
    require(
        github.controls(checkout_commit) == baseline, "checkout control closure changed"
    )
    proof = Proof(
        {
            "version": 1,
            "repository": {"id": github.repository_id, "name": github.repository},
            "pr": number,
            "base": base,
            "head": head,
            "checkout": {
                "commit": checkout_sha,
                "tree": checkout_commit["tree"]["sha"],
            },
            "workflow": {
                "id": github.workflow_id,
                "path": CI_PATH,
                "revision": checkout_sha,
                "blob": baseline[CI_PATH][1],
            },
            "source": {"run": run_id, "attempt": attempt, "job": qa["id"]},
            "registry": baseline[REGISTRY_PATH][1],
            # Lock identity is known; runner/Python equality is NOT attested.
            "tools": {"lock": baseline[LOCK_PATH][1], "runtime": "unattested"},
            "gates": dict.fromkeys(gates, "PASS"),
            "completed_at": run["updated_at"],
        }
    )
    return parse_proof(encode_proof(proof).encode())


def validate_installation(installation, app_id):
    require(
        installation["app_id"] == positive(app_id)
        and installation["suspended_at"] is None,
        "wrong or suspended App",
    )
    require(
        installation["permissions"] == APP_PERMISSIONS,
        "verifier installation permission ceiling differs",
    )


def app_jwt(app_id, key):
    """Sign without writing the private key to disk or passing it in argv."""

    def encode(value):
        return base64.urlsafe_b64encode(value).rstrip(b"=")

    now = int(time.time())
    payload = (
        encode(b'{"alg":"RS256","typ":"JWT"}')
        + b"."
        + encode(
            json.dumps(
                {"iat": now - 60, "exp": now + 300, "iss": positive(app_id)}
            ).encode()
        )
    )
    require(
        isinstance(key, str) and 0 < len(key.encode()) <= 4096, "invalid App key size"
    )
    read_fd, write_fd = os.pipe()
    try:
        os.write(write_fd, key.encode())
        os.close(write_fd)
        write_fd = None
        signed = subprocess.run(
            ["/usr/bin/openssl", "dgst", "-sha256", "-sign", f"/dev/fd/{read_fd}"],
            input=payload,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            pass_fds=(read_fd,),
            timeout=10,
            check=True,
            env={"PATH": "/usr/bin:/bin"},
        )
        return (payload + b"." + encode(signed.stdout)).decode()
    finally:
        os.close(read_fd)
        if write_fd is not None:
            os.close(write_fd)


def publish(proof, github, app_id, key):
    jwt = app_jwt(app_id, key)
    installation = github.request(
        "/repos/" + github.repository + "/installation", token=jwt
    )
    validate_installation(installation, app_id)
    installation_id = positive(installation["id"])
    result = github.request(
        f"/app/installations/{installation_id}/access_tokens",
        method="POST",
        token=jwt,
        body={"repository_ids": [github.repository_id], "permissions": APP_PERMISSIONS},
    )
    token = result["token"]
    try:
        require(result["permissions"] == APP_PERMISSIONS, "token permissions differ")
        record = proof.record
        body = {
            "name": "qa-provenance",
            "head_sha": record["checkout"]["commit"],
            "external_id": source_id(proof),
            "status": "completed",
            "conclusion": "success",
            "output": {
                "title": "Authenticated PR full QA",
                "summary": "Protected source proof; runtime identity remains unattested.",
                "text": encode_proof(proof),
            },
        }
        check = github.request(
            "/repos/" + github.repository + "/check-runs",
            method="POST",
            token=token,
            body=body,
        )
        observed = read_check(check, app_id)
        require(
            isinstance(observed, Proof) and observed.record == proof.record,
            "App check response mismatch",
        )
    finally:
        github.request("/installation/token", method="DELETE", token=token)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("authenticate", "publish"))
    parser.add_argument("--proof", type=Path, required=True)
    args = parser.parse_args()
    try:
        require(
            os.environ.get("GITHUB_EVENT_NAME") == "workflow_run"
            and os.environ.get("GITHUB_REF") == "refs/heads/main",
            "verifier requires default-branch workflow_run",
        )
        github = GitHubReader(
            os.environ["GH_TOKEN"],
            os.environ["GITHUB_REPOSITORY"],
            int(os.environ["GITHUB_REPOSITORY_ID"]),
            int(os.environ["QA_CI_WORKFLOW_ID"]),
            os.environ["GITHUB_SHA"],
        )
        with open(os.environ["GITHUB_EVENT_PATH"], "rb") as source:
            event = decode(source.read(API_LIMIT + 1), API_LIMIT)
        proof = verify_pr(event, github)
        require(
            isinstance(proof, Proof), "source authentication rejected; full QA required"
        )
        if args.mode == "authenticate":
            with args.proof.open("x", encoding="utf-8") as output:
                os.chmod(args.proof, 0o600)
                output.write(encode_proof(proof))
        else:
            with args.proof.open("rb") as source:
                previous = parse_proof(source.read(PROOF_LIMIT + 1))
            require(
                previous.record == proof.record, "source changed after authentication"
            )
            # Source has been authenticated again before the App key is read.
            publish(
                proof,
                github,
                int(os.environ["QA_VERIFIER_APP_ID"]),
                os.environ["QA_VERIFIER_PRIVATE_KEY"],
            )
        print("qa-provenance: " + args.mode + " complete")
        return 0
    except (
        ValueError,
        TypeError,
        KeyError,
        OSError,
        RecursionError,
        subprocess.SubprocessError,
        HTTPError,
        URLError,
    ):
        print(
            "qa-provenance: rejected; inspect source identity and protected App configuration",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
