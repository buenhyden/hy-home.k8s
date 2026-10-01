#!/usr/bin/env python3
"""Create immutable main checkpoints after independent App-verdict authentication.

Run only with python3 -I from protected default-branch control. The publisher
App's contents:write ceiling is NOT tag immutability: operator-owned creation
and update/deletion rulesets must be observed before QA_TAG_ENABLED is enabled.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import importlib.util
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.error import HTTPError, URLError

# -I keeps PR/import-path injection out; use the protected verifier's exact parser.
_spec = importlib.util.spec_from_file_location(
    "qa_tag_provenance", Path(__file__).with_name("qa_provenance.py")
)
core = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = core
_spec.loader.exec_module(core)
MainVerdict = core.MainVerdict
require = core.require
APP_PERMISSIONS = {"contents": "write", "metadata": "read"}


@dataclass(frozen=True)
class Publication:
    status: str
    ref: str
    sha: str


def require_target(value, ref, target):
    require(
        value["ref"] == ref
        and value["object"]["type"] == "commit"
        and value["object"]["sha"] == target,
        "reference is not the exact expected commit",
    )


def current_main(github, target):
    require_target(github.get("git/ref/heads/main"), "refs/heads/main", target)


def existing_tag(github, target):
    try:
        existing = github.get("git/ref/tags/main-" + target)
    except HTTPError as error:
        if error.code == 404:
            return False
        raise
    require_target(existing, "refs/tags/main-" + target, target)
    return True


def authenticate(event, github, verifier_app_id):
    """Rebuild the complete main verdict and require the verifier App's check."""
    expected = core.verify_main(event, github)
    require(isinstance(expected, MainVerdict), "main source rejected")
    baseline = github.controls(github.commit(github.baseline))
    for path in ("scripts/publish_main_tag.py", ".github/workflows/qa-verifier.yml"):
        core.trusted_bytes(github, baseline, path)
    target = expected.record["checkout"]["commit"]
    checks = github.pages(
        f"commits/{target}/check-runs?check_name=qa-main-verdict&filter=all",
        field="check_runs",
    )
    check_ids = []
    for check in checks:
        if (
            check["name"] == "qa-main-verdict"
            and check["app"]["id"] == core.positive(verifier_app_id)
            and check["external_id"] == core.source_id(expected)
        ):
            observed = core.read_main_check(check, verifier_app_id)
            require(
                isinstance(observed, MainVerdict)
                and observed.record == expected.record,
                "protected main verdict differs from authenticated source",
            )
            check_ids.append(core.positive(check["id"]))
    require(check_ids, "no exact verifier-App main verdict")
    if not existing_tag(github, target):
        current_main(github, target)
    # A verifier rerun may issue identical checks; conflicting records fail above.
    return expected, max(check_ids)


class GitHubWriter(core.GitHubReader):
    """Publisher-token transport permits reference reads and one create shape only."""

    def request(self, route, *, method="GET", body=None, token=None):
        prefix = "/repos/" + self.repository + "/git/"
        if method == "GET":
            require(
                route == prefix + "ref/heads/main"
                or re.fullmatch(
                    re.escape(prefix) + r"ref/tags/main-[0-9a-f]{40}", route
                ),
                "publisher read route denied",
            )
            require(body is None, "publisher read body denied")
        else:
            require(
                method == "POST"
                and route == prefix + "refs"
                and isinstance(body, dict)
                and set(body) == {"ref", "sha"}
                and body["ref"] == "refs/tags/main-" + core.sha(body["sha"]),
                "publisher may only create an exact main tag",
            )
        return super().request(route, method=method, body=body, token=token)


def publish_main_tag(
    repository: str,
    ref: str,
    after_sha: str,
    verdict: MainVerdict,
    github: GitHubWriter,
) -> Publication:
    """Publish one source push tip; workflow_run has no original push `after` field.

    The caller binds after_sha to the authenticated push run head_sha and the
    protected verdict's actual tested checkout, never workflow_run GITHUB_SHA.
    """
    require(isinstance(verdict, MainVerdict), "protected main verdict required")
    record = core.parse_main_verdict(core.encode_proof(verdict).encode()).record
    require(
        repository == github.repository
        and record["repository"] == {"id": github.repository_id, "name": repository}
        and record["workflow"]["id"] == github.workflow_id
        and ref == record["ref"] == "refs/heads/main"
        and core.sha(after_sha) == record["checkout"]["commit"],
        "publication source mismatch",
    )
    tag = "refs/tags/main-" + after_sha
    route = "git/ref/tags/main-" + after_sha
    if existing_tag(github, after_sha):
        return Publication("noop", tag, after_sha)
    current_main(github, after_sha)
    try:
        created = github.request(
            "/repos/" + repository + "/git/refs",
            method="POST",
            body={"ref": tag, "sha": after_sha},
        )
    except HTTPError as error:
        # GitHub reports an existing/concurrently created ref as conflict/validation.
        # Other API errors remain failures, even if an unrelated writer made a tag.
        if error.code not in (409, 422):
            raise
        require_target(github.get(route), tag, after_sha)
        return Publication("noop", tag, after_sha)
    require_target(created, tag, after_sha)
    return Publication("created", tag, after_sha)


def validate_installation(installation, publisher_app_id, verifier_app_id):
    require(
        core.positive(publisher_app_id) != core.positive(verifier_app_id)
        and installation["app_id"] == publisher_app_id
        and installation["suspended_at"] is None,
        "publisher must be a separate active App",
    )
    require(
        installation["permissions"] == APP_PERMISSIONS,
        "publisher installation permission ceiling differs",
    )


def publish_with_app(verdict, github, publisher_app_id, verifier_app_id, key):
    require(publisher_app_id != verifier_app_id, "verifier cannot publish tags")
    jwt = core.app_jwt(publisher_app_id, key)
    installation = github.request(
        "/repos/" + github.repository + "/installation", token=jwt
    )
    validate_installation(installation, publisher_app_id, verifier_app_id)
    installation_id = core.positive(installation["id"])
    result = github.request(
        f"/app/installations/{installation_id}/access_tokens",
        method="POST",
        token=jwt,
        body={"repository_ids": [github.repository_id], "permissions": APP_PERMISSIONS},
    )
    token = result["token"]
    try:
        require(isinstance(token, str) and 0 < len(token) <= 4096, "invalid App token")
        require(result["permissions"] == APP_PERMISSIONS, "token permissions differ")
        require(
            [(row["id"], row["full_name"]) for row in result["repositories"]]
            == [(github.repository_id, github.repository)],
            "token repository scope differs",
        )
        writer = GitHubWriter(
            token,
            github.repository,
            github.repository_id,
            github.workflow_id,
            github.baseline,
        )
        return publish_main_tag(
            github.repository,
            verdict.record["ref"],
            verdict.record["checkout"]["commit"],
            verdict,
            writer,
        )
    finally:
        # Revocation is the only DELETE; published Git refs are never changed.
        github.request("/installation/token", method="DELETE", token=token)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("authenticate", "publish"))
    parser.add_argument("--proof", type=Path, required=True)
    args = parser.parse_args()
    try:
        require(
            os.environ.get("QA_TAG_ENABLED") == "true"
            and os.environ.get("GITHUB_EVENT_NAME") == "workflow_run"
            and os.environ.get("GITHUB_REF") == "refs/heads/main",
            "publisher requires enabled default-branch workflow_run",
        )
        verifier_app_id = core.positive(int(os.environ["QA_VERIFIER_APP_ID"]))
        publisher_app_id = core.positive(int(os.environ["QA_PUBLISHER_APP_ID"]))
        require(
            publisher_app_id != verifier_app_id, "publisher identity is not distinct"
        )
        github = core.GitHubReader(
            os.environ["GH_TOKEN"],
            os.environ["GITHUB_REPOSITORY"],
            int(os.environ["GITHUB_REPOSITORY_ID"]),
            int(os.environ["QA_CI_WORKFLOW_ID"]),
            os.environ["GITHUB_SHA"],
        )
        with open(os.environ["GITHUB_EVENT_PATH"], "rb") as source:
            event = core.decode(source.read(core.API_LIMIT + 1), core.API_LIMIT)
        verdict, check_id = authenticate(event, github, verifier_app_id)
        if args.mode == "authenticate":
            with args.proof.open("x", encoding="utf-8") as output:
                os.chmod(args.proof, 0o600)
                output.write(core.encode_proof(verdict))
            print(f"main-tag: authenticated verifier check {check_id}")
        else:
            with args.proof.open("rb") as source:
                previous = core.parse_main_verdict(source.read(core.PROOF_LIMIT + 1))
            require(
                previous.record == verdict.record, "source changed after authentication"
            )
            # Independently authenticated source and App check precede any key read.
            publication = publish_with_app(
                verdict,
                github,
                publisher_app_id,
                verifier_app_id,
                os.environ["QA_PUBLISHER_PRIVATE_KEY"],
            )
            print(
                f"main-tag: {publication.status} {publication.ref}; verifier check {check_id}"
            )
        return 0
    except (
        ValueError,
        TypeError,
        KeyError,
        IndexError,
        AttributeError,
        OSError,
        RecursionError,
        subprocess.SubprocessError,
        HTTPError,
        URLError,
    ):
        print(
            "main-tag: rejected; inspect source verdict, current main tip and protected publisher configuration",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
