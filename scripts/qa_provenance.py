#!/usr/bin/env python3
"""Authenticate PR or full main QA before the isolated verifier App issues a check.

Only stdlib imports: run with python3 -I, from a default-branch checkout.
Fetched trees, job metadata and proof records are data, never executable input.
"""

from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from typing import Any, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener

# Resolve the protected sibling explicitly: -I does not add the checkout to sys.path.
_records_spec = importlib.util.spec_from_file_location(
    "qa_provenance_records", Path(__file__).with_name("qa_provenance_records.py")
)
records = importlib.util.module_from_spec(_records_spec)
sys.modules[_records_spec.name] = records
_records_spec.loader.exec_module(records)
_hosted_spec = importlib.util.spec_from_file_location(
    "qa_provenance_hosted", Path(__file__).with_name("qa_provenance_hosted.py")
)
hosted = importlib.util.module_from_spec(_hosted_spec)
_hosted_spec.loader.exec_module(hosted)

PROOF_LIMIT = records.PROOF_LIMIT
Proof, MainVerdict, Reject = records.Proof, records.MainVerdict, records.Reject
require, sha, positive = records.require, records.sha, records.positive
decode, encode_proof = records.decode, records.encode_proof

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


def utc_now():
    return datetime.now(timezone.utc)


def parse_proof(payload):
    return records.parse_record(payload, main=False, now=utc_now())


def parse_main_verdict(payload):
    return records.parse_record(payload, main=True, now=utc_now())


def read_check(check, app_id):
    """Parse only the expected App's PR proof; never accept a main verdict for reuse."""
    return _read_check(check, app_id, "qa-provenance", parse_proof)


def read_main_check(check, app_id):
    """Authenticate the bounded App verdict; the consumer must bind the source run."""
    return _read_check(check, app_id, "qa-main-verdict", parse_main_verdict)


def _read_check(check, app_id, name, parse):
    try:
        require(
            check["name"] == name and check["app"]["id"] == positive(app_id),
            "wrong check author",
        )
        require(
            check["status"] == "completed" and check["conclusion"] == "success",
            "check did not pass",
        )
        proof = parse(check["output"]["text"].encode())
        expected_sha = (
            proof.record["checkout"]["commit"]
            if isinstance(proof, MainVerdict)
            else proof.record["head"]
        )
        require(check["head_sha"] == expected_sha, "wrong check SHA")
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
            and (
                ".." not in route
                or re.fullmatch(
                    rf"/repos/{re.escape(self.repository)}/compare/[0-9a-f]{{40}}\.\.\.[0-9a-f]{{40}}",
                    route,
                )
                is not None
            )
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
            separator = "&" if "?" in route else "?"
            response = self.get(route + separator + f"per_page=100&page={page}")
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
                or path.rsplit("/", 1)[-1] == ".gitattributes"
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


def source_pull(run, github, *, history=None):
    relations = run["pull_requests"]
    require(isinstance(relations, list) and len(relations) <= 1, "ambiguous PR source")
    discovered = not relations
    if discovered:
        repository = run["head_repository"]
        owner, branch = repository["owner"]["login"], run["head_branch"]
        require(
            isinstance(owner, str) and re.fullmatch(r"[A-Za-z0-9-]{1,100}", owner),
            "invalid head owner",
        )
        require(
            isinstance(branch, str)
            and 0 < len(branch) <= 1024
            and branch.isprintable(),
            "invalid head branch",
        )
        require(repository["full_name"].startswith(owner + "/"), "head owner mismatch")
        state = "closed" if history else "open"
        query = urlencode(
            {"state": state, "base": "main", "head": owner + ":" + branch}
        )
        relations = github.pages("pulls?" + query)
        if history:
            before, merged = history
            relations = [
                relation
                for relation in relations
                if relation["base"]["sha"] == before
                and relation["head"]["sha"] == run["head_sha"]
                and relation["merge_commit_sha"] == merged
            ]
    require(len(relations) == 1, "missing or ambiguous PR source")
    relation = relations[0]
    if discovered:
        require(
            relation["state"] == ("closed" if history else "open")
            and relation["base"]["ref"] == "main"
            and repo_matches(relation["base"]["repo"], github)
            and relation["head"]["ref"] == run["head_branch"]
            and relation["head"]["repo"]["id"] == run["head_repository"]["id"]
            and relation["head"]["repo"]["full_name"]
            == run["head_repository"]["full_name"],
            "PR lookup does not match source branch/repository",
        )
    return relation, github.get(f"pulls/{positive(relation['number'])}"), discovered


def authenticated_run(event, github, event_name):
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
    fields = (
        "id",
        "run_attempt",
        "workflow_id",
        "event",
        "head_sha",
        "head_branch",
        "path",
    )
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
        and run["event"] == event_name
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
    require(
        all(
            value["head_repository"]["id"] == run["head_repository"]["id"]
            for value in (source, current)
        ),
        "source head repository changed",
    )
    return run


def _verify_pr(event, github, *, proof_base=None, merged_to=None):
    require(
        (proof_base is None) == (merged_to is None),
        "incomplete historical source binding",
    )
    history = (sha(proof_base), sha(merged_to)) if proof_base else None
    run = authenticated_run(event, github, "pull_request")
    relation, pr, discovered = source_pull(run, github, history=history)
    number = positive(relation["number"])
    require(
        pr["number"] == number and pr["state"] == ("closed" if proof_base else "open"),
        "wrong PR state",
    )
    if proof_base:
        require(
            pr["merged"] is True and pr["merge_commit_sha"] == merged_to,
            "wrong merged PR target",
        )
    base, head = sha(proof_base or pr["base"]["sha"]), sha(pr["head"]["sha"])
    require(
        pr["base"]["ref"] == "main" and repo_matches(pr["base"]["repo"], github),
        "wrong PR base",
    )
    require(
        (proof_base or base == github.baseline) and head == run["head_sha"],
        "PR base/head changed",
    )
    require(
        relation["base"]["sha"] == base and relation["head"]["sha"] == head,
        "run PR relation changed",
    )
    require(
        run["head_repository"]["id"] == pr["head"]["repo"]["id"]
        and run["head_branch"] == pr["head"]["ref"],
        "wrong head branch or repository",
    )
    baseline = github.controls(github.commit(base))
    require(
        baseline == github.controls(github.commit(github.baseline)),
        "protected baseline changed",
    )
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
    gates = full_gate_contract(github, baseline)
    jobs, checkout_sha, _ = hosted.job_partition(
        sys.modules[__name__], run, github, main=False
    )
    qa = jobs["qa"]
    if discovered and not proof_base:
        require(
            pr["merge_commit_sha"] == checkout_sha, "PR lookup merge checkout changed"
        )
    checkout_commit = github.commit(checkout_sha)
    require(
        [parent["sha"] for parent in checkout_commit["parents"]] == [base, head],
        "checkout is not the PR merge",
    )
    require(
        github.controls(checkout_commit) == baseline, "checkout control closure changed"
    )
    proof = Proof(
        full_record(github, baseline, run, qa, checkout_commit, gates)
        | {
            "version": 3,
            "isolated": hosted.isolated_record(
                sys.modules[__name__], github, baseline, jobs, checkout_commit
            ),
            "pr": number,
            "base": base,
            "head": head,
        }
    )
    return parse_proof(encode_proof(proof).encode())


def full_gate_contract(github, baseline):
    ci = trusted_bytes(github, baseline, CI_PATH)
    trusted_bytes(github, baseline, "scripts/qa_provenance.py")
    trusted_bytes(github, baseline, "scripts/qa_provenance_records.py")
    trusted_bytes(github, baseline, "scripts/qa_provenance_hosted.py")
    require(
        b"name: Checkout QA commit ${{ github.sha }}" in ci
        and b"ref: ${{ github.sha }}" in ci
        and b'run: python3 scripts/qa.py ci --base-ref "$BASE_SHA"' in ci,
        "unsupported CI contract",
    )
    registry = decode(trusted_bytes(github, baseline, REGISTRY_PATH), API_LIMIT)
    hosted.partition(registry, "isolated")
    require(
        hosted.IMAGE.encode() in ci and b"/usr/local/bin/python3 -I -B -" in ci,
        "unsupported isolated runtime",
    )
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
    return gates


def verify_main(event: Mapping[str, Any], github: GitHubReader) -> MainVerdict | Reject:
    try:
        return _verify_main(event, github)
    except (
        ValueError,
        TypeError,
        KeyError,
        IndexError,
        AttributeError,
        OSError,
        RecursionError,
    ):
        return Reject("main source authentication failed; require complete full QA")


def _verify_main(event, github):
    run = authenticated_run(event, github, "push")
    require(
        run["head_branch"] == "main" and repo_matches(run["head_repository"], github),
        "not a main repository push",
    )
    checkout_sha = sha(run["head_sha"])
    checkout_commit = github.commit(checkout_sha)
    baseline = github.controls(github.commit(github.baseline))
    require(
        github.controls(checkout_commit) == baseline, "main control closure changed"
    )
    gates = full_gate_contract(github, baseline)
    jobs, observed_checkout, mode = hosted.job_partition(
        sys.modules[__name__], run, github, main=True
    )
    qa = jobs["qa"]
    require(observed_checkout == checkout_sha, "wrong QA checkout")
    reused = hosted.main_reuse(sys.modules[__name__], github, jobs, checkout_sha, mode)
    record = full_record(github, baseline, run, qa, checkout_commit, gates)
    if reused:
        record = record | {
            "gates": {**record["gates"], hosted.GATE: "REUSED"},
            "reuse": reused,
        }
    verdict = MainVerdict(
        record
        | {
            "version": 4 if reused else 2,
            "event": "push",
            "ref": "refs/heads/main",
            "control": github.baseline,
        }
    )
    return parse_main_verdict(encode_proof(verdict).encode())


def full_record(github, baseline, run, qa, commit, gates):
    return {
        "repository": {"id": github.repository_id, "name": github.repository},
        "checkout": {"commit": commit["sha"], "tree": commit["tree"]["sha"]},
        "workflow": {
            "id": github.workflow_id,
            "path": CI_PATH,
            "revision": commit["sha"],
            "blob": baseline[CI_PATH][1],
        },
        "source": {"run": run["id"], "attempt": run["run_attempt"], "job": qa["id"]},
        "registry": baseline[REGISTRY_PATH][1],
        # The lock is authenticated; runner/Python equality is NOT attested.
        "tools": {"lock": baseline[LOCK_PATH][1], "runtime": "unattested"},
        "gates": dict.fromkeys(gates, "PASS"),
        "completed_at": run["updated_at"],
    }


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
        main = isinstance(proof, MainVerdict)
        body = {
            "name": "qa-main-verdict" if main else "qa-provenance",
            "head_sha": record["checkout"]["commit"] if main else record["head"],
            "external_id": source_id(proof),
            "status": "completed",
            "conclusion": "success",
            "output": {
                "title": "Authenticated main full QA"
                if main
                else "Authenticated PR full QA",
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
        observed = (read_main_check if main else read_check)(check, app_id)
        require(
            type(observed) is type(proof) and observed.record == proof.record,
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
        main_push = event["workflow_run"]["event"] == "push"
        proof = (verify_main if main_push else verify_pr)(event, github)
        require(
            isinstance(proof, (Proof, MainVerdict)),
            "source authentication rejected; full QA required",
        )
        if args.mode == "authenticate":
            with args.proof.open("x", encoding="utf-8") as output:
                os.chmod(args.proof, 0o600)
                output.write(encode_proof(proof))
        else:
            with args.proof.open("rb") as source:
                previous = (parse_main_verdict if main_push else parse_proof)(
                    source.read(PROOF_LIMIT + 1)
                )
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
