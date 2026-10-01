"""Protected main publication: source authentication and create-only Git refs."""

import copy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from scripts import publish_main_tag as publisher
from tests.test_qa_provenance import BASE, HEAD, MERGE, REPO, ROOT, FakeGitHub, blob

core = publisher.core
APP = 80
PUBLISHER = 81
REF = "refs/tags/main-" + MERGE


def ref_object(ref=REF, target=MERGE, kind="commit"):
    return {"ref": ref, "object": {"type": kind, "sha": target}}


def missing():
    return HTTPError("https://api.github.com/", 404, "missing", {}, None)


class TagReader(FakeGitHub):
    def get(self, route):
        if route.startswith("git/ref/tags/") and route not in self.data:
            raise missing()
        return super().get(route)


class PublisherTests(unittest.TestCase):
    def setUp(self):
        self.clock = patch.object(
            core, "utc_now", return_value=datetime(2026, 10, 2, tzinfo=timezone.utc)
        )
        self.clock.start()
        self.addCleanup(self.clock.stop)
        self.github = TagReader()
        self.github.run.update(
            event="push", head_branch="main", head_sha=MERGE, pull_requests=[]
        )
        self.github.event["workflow_run"] = copy.deepcopy(self.github.run)
        for job in self.github.jobs:
            job["head_sha"] = MERGE
        self.github.jobs[0]["conclusion"] = "skipped"
        self.github.jobs[3]["conclusion"] = "skipped"
        self.github.jobs[1]["steps"][1]["name"] = "Validate repository checkout"
        self.github.jobs[1]["steps"][2]["name"] = "Validate repository complement"
        for tree in ("e" * 40, "f" * 40, "d" * 40):
            entries = self.github.data["git/trees/" + tree + "?recursive=1"]["tree"]
            for name in (
                "scripts/publish_main_tag.py",
                ".github/workflows/qa-verifier.yml",
            ):
                entries.append(
                    {
                        "path": name,
                        "type": "blob",
                        "mode": "100644",
                        "sha": blob((ROOT / name).read_bytes()),
                    }
                )
        self.verdict = core.verify_main(self.github.event, self.github)
        self.assertIsInstance(self.verdict, core.MainVerdict)
        self.check = {
            "id": 90,
            "name": "qa-main-verdict",
            "app": {"id": APP},
            "head_sha": MERGE,
            "external_id": core.source_id(self.verdict),
            "status": "completed",
            "conclusion": "success",
            "output": {"text": core.encode_proof(self.verdict)},
        }
        self.github.data["git/ref/heads/main"] = ref_object("refs/heads/main")
        self.check_route = f"commits/{MERGE}/check-runs?check_name=qa-main-verdict&filter=all&per_page=100&page=1"
        self.github.data[self.check_route] = {
            "total_count": 1,
            "check_runs": [self.check],
        }
        self.writer = publisher.GitHubWriter("unused", REPO, 10, 20, BASE)

    def authenticate(self):
        return publisher.authenticate(self.github.event, self.github, APP)

    def publish(self):
        return publisher.publish_main_tag(
            REPO, "refs/heads/main", MERGE, self.verdict, self.writer
        )

    def test_main_source_and_protected_check_are_both_required(self):
        verdict, check_id = self.authenticate()
        self.assertEqual(verdict.record, self.verdict.record)
        self.assertEqual(check_id, 90)
        self.assertEqual(len(verdict.record["gates"]), 23)
        self.assertNotEqual(MERGE, self.github.baseline)
        self.assertNotIn("after", self.github.event)

    def test_rejects_pr_feature_tag_manual_and_wrong_provider_identity(self):
        original = copy.deepcopy(self.github.run)
        for change in (
            {"event": "pull_request"},
            {"event": "workflow_dispatch"},
            {"head_branch": "codex/feature"},
            {"head_branch": "main-deadbeef"},
            {"head_branch": "refs/tags/main"},
            {"head_sha": HEAD},
            {"workflow_id": 21},
            {"path": ".github/workflows/other.yml"},
            {"head_repository": {"id": 99, "full_name": REPO}},
            {"conclusion": "failure"},
            {"conclusion": "cancelled"},
            {"status": "in_progress"},
        ):
            with self.subTest(change=change):
                self.github.run.clear()
                self.github.run.update(copy.deepcopy(original) | change)
                self.github.event["workflow_run"] = copy.deepcopy(self.github.run)
                with self.assertRaises(ValueError):
                    self.authenticate()
        self.github.run.clear()
        self.github.run.update(original)
        self.github.event["workflow_run"] = copy.deepcopy(original)
        self.github.run["run_attempt"] = 3
        with self.assertRaises(ValueError):
            self.authenticate()

    def test_rejects_wrong_app_name_sha_attempt_or_incomplete_verdict(self):
        original = copy.deepcopy(self.check)
        changes = [
            {"app": {"id": 99}},
            {"name": "ci-summary"},
            {"head_sha": HEAD},
            {"external_id": "30:1:41"},
            {"conclusion": "failure"},
            {"status": "in_progress"},
            {"output": {"text": "x" * 16385}},
        ]
        for field, value in (
            ("checkout", {"commit": HEAD, "tree": "d" * 40}),
            ("source", {"run": 30, "attempt": 1, "job": 41}),
            ("gates", {"unit-tests": "PASS"}),
            ("version", 1),
        ):
            record = self.verdict.record | {field: value}
            changes.append({"output": {"text": json.dumps(record)}})
        for change in changes:
            with self.subTest(change=change):
                self.check.clear()
                self.check.update(copy.deepcopy(original) | change)
                with self.assertRaises(ValueError):
                    self.authenticate()

    def test_duplicate_identical_checks_support_retry_but_conflict_rejects(self):
        duplicate = copy.deepcopy(self.check) | {"id": 91}
        self.github.data[self.check_route] = {
            "total_count": 2,
            "check_runs": [self.check, duplicate],
        }
        self.assertEqual(self.authenticate()[1], 91)
        duplicate["output"]["text"] = "{}"
        with self.assertRaises(ValueError):
            self.authenticate()

    def test_advanced_main_exact_existing_tag_remains_authenticated_noop(self):
        self.github.data["git/ref/heads/main"] = ref_object("refs/heads/main", HEAD)
        self.github.data["git/ref/tags/main-" + MERGE] = ref_object()
        verdict, _ = self.authenticate()
        self.assertEqual(verdict.record, self.verdict.record)
        with patch.object(self.writer, "request", return_value=ref_object()) as request:
            self.assertEqual(self.publish().status, "noop")
        self.assertEqual(request.call_count, 1)
        self.assertEqual(
            request.call_args.args, ("/repos/" + REPO + "/git/ref/tags/main-" + MERGE,)
        )

    def test_advanced_main_missing_or_conflicting_tag_never_creates(self):
        self.github.data["git/ref/heads/main"] = ref_object("refs/heads/main", HEAD)
        with self.assertRaises(ValueError):
            self.authenticate()
        with patch.object(
            self.writer,
            "request",
            side_effect=[missing(), ref_object("refs/heads/main", HEAD)],
        ) as request:
            with self.assertRaises(ValueError):
                self.publish()
        self.assertFalse(
            any(call.kwargs.get("method") == "POST" for call in request.call_args_list)
        )
        self.github.data["git/ref/tags/main-" + MERGE] = ref_object(target=HEAD)
        with self.assertRaises(ValueError):
            self.authenticate()
        with patch.object(
            self.writer, "request", return_value=ref_object(target=HEAD)
        ) as request:
            with self.assertRaises(ValueError):
                self.publish()
        self.assertEqual(request.call_count, 1)

    def test_stale_tip_and_wrong_tested_checkout_fail_before_key_access(self):
        self.github.data["git/ref/heads/main"] = ref_object("refs/heads/main", HEAD)
        with self.assertRaises(ValueError):
            self.authenticate()
        self.github.data["git/ref/heads/main"] = ref_object("refs/heads/main")
        self.github.jobs[1]["steps"][0]["name"] = core.CHECKOUT_PREFIX + HEAD
        with self.assertRaises(ValueError):
            self.authenticate()

    def test_publisher_executing_bytes_must_match_the_control_baseline(self):
        for tree in ("e" * 40, "d" * 40):
            entry = next(
                row
                for row in self.github.data["git/trees/" + tree + "?recursive=1"][
                    "tree"
                ]
                if row["path"] == "scripts/publish_main_tag.py"
            )
            entry["sha"] = "0" * 40
        with self.assertRaises(ValueError):
            self.authenticate()

    def test_multicommit_push_creates_only_its_authenticated_tip_without_force(self):
        self.github.data["git/commits/" + MERGE]["parents"] = [{"sha": HEAD}]
        self.authenticate()
        with patch.object(
            self.writer,
            "request",
            side_effect=[
                missing(),
                ref_object("refs/heads/main"),
                ref_object(),
            ],
        ) as request:
            result = self.publish()
        self.assertEqual(result.status, "created")
        writes = [
            call
            for call in request.call_args_list
            if call.kwargs.get("method") == "POST"
        ]
        self.assertEqual(len(writes), 1)
        self.assertEqual(writes[0].args, ("/repos/" + REPO + "/git/refs",))
        self.assertEqual(writes[0].kwargs["body"], {"ref": REF, "sha": MERGE})

    def test_same_target_retry_is_noop_and_collision_never_mutates(self):
        for existing, accepted in (
            (ref_object(), True),
            (ref_object(target=HEAD), False),
            (ref_object(kind="tag"), False),
            (ref_object(ref="refs/tags/other"), False),
        ):
            with (
                self.subTest(existing=existing),
                patch.object(
                    self.writer,
                    "request",
                    side_effect=[existing],
                ) as request,
            ):
                if accepted:
                    self.assertEqual(self.publish().status, "noop")
                else:
                    with self.assertRaises(ValueError):
                        self.publish()
                self.assertFalse(
                    any(
                        call.kwargs.get("method") in ("POST", "PATCH", "DELETE")
                        for call in request.call_args_list
                    )
                )

    def test_concurrent_creation_accepts_only_same_commit_and_write_failure_rejects(
        self,
    ):
        for code, existing, accepted in (
            (422, ref_object(), True),
            (409, ref_object(), True),
            (422, ref_object(target=HEAD), False),
            (403, ref_object(), False),
            (500, ref_object(), False),
        ):
            with (
                self.subTest(code=code, existing=existing),
                patch.object(
                    self.writer,
                    "request",
                    side_effect=[
                        missing(),
                        ref_object("refs/heads/main"),
                        HTTPError("https://api.github.com/", code, "error", {}, None),
                        existing,
                    ],
                ) as request,
            ):
                if accepted:
                    self.assertEqual(self.publish().status, "noop")
                else:
                    with self.assertRaises((ValueError, HTTPError)):
                        self.publish()
                self.assertFalse(
                    any(
                        call.kwargs.get("method") in ("PATCH", "DELETE")
                        for call in request.call_args_list
                    )
                )

    def test_tip_advance_between_lookup_and_create_rejects_without_post(self):
        with patch.object(
            self.writer,
            "request",
            side_effect=[
                missing(),
                ref_object("refs/heads/main", HEAD),
            ],
        ) as request:
            with self.assertRaises(ValueError):
                self.publish()
        self.assertFalse(
            any(call.kwargs.get("method") == "POST" for call in request.call_args_list)
        )

    def test_writer_transport_denies_update_delete_and_other_refs_before_http(self):
        route = "/repos/" + REPO + "/git/refs"
        for method, target, body in (
            ("PATCH", route + "/tags/main-" + MERGE, {"sha": HEAD}),
            ("DELETE", route + "/tags/main-" + MERGE, None),
            ("POST", route, {"ref": "refs/heads/main", "sha": MERGE}),
            ("POST", route, {"ref": REF, "sha": HEAD}),
            ("POST", route, {"ref": REF, "sha": MERGE, "force": True}),
        ):
            with (
                self.subTest(method=method, body=body),
                patch.object(core.GitHubReader, "request") as http,
            ):
                with self.assertRaises(ValueError):
                    self.writer.request(target, method=method, body=body)
                http.assert_not_called()

    def test_failed_ref_reads_and_wrong_creation_response_remain_failures(self):
        for replies in (
            [
                HTTPError("https://api.github.com/", 403, "denied", {}, None),
            ],
            [
                missing(),
                ref_object("refs/heads/main"),
                ref_object(target=HEAD),
            ],
            [
                missing(),
                ref_object("refs/heads/main"),
                HTTPError("https://api.github.com/", 422, "invalid", {}, None),
                missing(),
            ],
        ):
            with (
                self.subTest(replies=replies),
                patch.object(self.writer, "request", side_effect=replies),
            ):
                with self.assertRaises((ValueError, HTTPError)):
                    self.publish()

    def test_disabled_or_non_workflow_run_cli_never_reads_key_or_provider(self):
        for env in (
            {},
            {"QA_TAG_ENABLED": "false"},
            {
                "QA_TAG_ENABLED": "true",
                "GITHUB_EVENT_NAME": "push",
                "GITHUB_REF": "refs/heads/main",
            },
            {
                "QA_TAG_ENABLED": "true",
                "GITHUB_EVENT_NAME": "workflow_run",
                "GITHUB_REF": "refs/tags/main",
            },
        ):
            with (
                self.subTest(env=env),
                patch.dict(os.environ, env, clear=True),
                patch.object(core, "GitHubReader") as reader,
                patch.object(core, "app_jwt") as sign,
                patch.object(
                    publisher.sys,
                    "argv",
                    ["publish_main_tag.py", "publish", "--proof", "/unused"],
                ),
            ):
                self.assertEqual(publisher.main(), 1)
                reader.assert_not_called()
                sign.assert_not_called()

    def test_installed_publisher_is_distinct_and_has_only_contents_write(self):
        installation = {
            "app_id": PUBLISHER,
            "suspended_at": None,
            "permissions": {"metadata": "read", "contents": "write"},
        }
        publisher.validate_installation(installation, PUBLISHER, APP)
        for candidate, app_id in (
            (installation, APP),
            (installation | {"app_id": APP}, APP),
            (installation | {"suspended_at": "2026-10-02T00:00:00Z"}, PUBLISHER),
            (installation | {"permissions": core.APP_PERMISSIONS}, PUBLISHER),
            (
                installation
                | {"permissions": installation["permissions"] | {"checks": "write"}},
                PUBLISHER,
            ),
        ):
            with self.subTest(candidate=candidate), self.assertRaises(ValueError):
                publisher.validate_installation(candidate, app_id, APP)
        with self.assertRaises(ValueError):
            core.validate_installation(installation | {"app_id": APP}, APP)

    def test_app_token_is_repository_restricted_narrowed_and_always_revoked(self):
        installation = {
            "id": 88,
            "app_id": PUBLISHER,
            "suspended_at": None,
            "permissions": publisher.APP_PERMISSIONS,
        }
        result = {
            "token": "unused",
            "permissions": publisher.APP_PERMISSIONS,
            "repositories": [{"id": 10, "full_name": REPO}],
        }
        for change, accepted in (
            ({}, True),
            ({"permissions": core.APP_PERMISSIONS}, False),
            ({"repositories": [{"id": 99, "full_name": REPO}]}, False),
            ({"repositories": []}, False),
        ):
            with (
                self.subTest(change=change),
                patch.object(core, "app_jwt", return_value="unused"),
                patch.object(
                    self.github,
                    "request",
                    side_effect=[installation, result | change, None],
                ) as request,
                patch.object(publisher, "publish_main_tag") as publish,
            ):
                if accepted:
                    publisher.publish_with_app(
                        self.verdict, self.github, PUBLISHER, APP, "unused"
                    )
                    publish.assert_called_once()
                else:
                    with self.assertRaises(ValueError):
                        publisher.publish_with_app(
                            self.verdict, self.github, PUBLISHER, APP, "unused"
                        )
                    publish.assert_not_called()
                self.assertEqual(
                    request.call_args_list[1].kwargs["body"],
                    {
                        "repository_ids": [10],
                        "permissions": {"contents": "write", "metadata": "read"},
                    },
                )
                self.assertEqual(
                    request.call_args_list[-1].args, ("/installation/token",)
                )
                self.assertEqual(request.call_args_list[-1].kwargs["method"], "DELETE")
        with patch.object(core, "app_jwt") as sign, self.assertRaises(ValueError):
            publisher.publish_with_app(self.verdict, self.github, APP, APP, "unused")
        sign.assert_not_called()

    def test_v4_protected_verdict_retains_22_executed_and_one_reauthenticated_gate(
        self,
    ):
        from tests import test_qa_provenance_hosted as fixtures

        fixture = fixtures.HostedSourceTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        github = fixture.github
        for tree in ("e" * 40, "f" * 40, "d" * 40):
            entries = github.data["git/trees/" + tree + "?recursive=1"]["tree"]
            entries.extend(
                copy.deepcopy(
                    self.github.data["git/trees/" + tree + "?recursive=1"]["tree"][-2:]
                )
            )
        run = copy.deepcopy(github.run) | {
            "id": 31,
            "run_attempt": 1,
            "event": "push",
            "head_sha": fixtures.AFTER,
            "head_branch": "main",
            "pull_requests": [],
        }
        github.data["actions/runs/31"] = github.data["actions/runs/31/attempts/1"] = run
        jobs = copy.deepcopy(github.jobs)
        for job in jobs:
            job.update(
                id=job["id"] + 10, run_id=31, run_attempt=1, head_sha=fixtures.AFTER
            )
        jobs[0]["conclusion"] = jobs[3]["conclusion"] = "skipped"
        jobs[4]["conclusion"] = "success"
        jobs[4]["steps"] = [
            {
                "number": 1,
                "name": fixtures.hosted.PUSH_PREFIX + BASE + " " + fixtures.AFTER,
                "status": "completed",
                "conclusion": "success",
            }
        ]
        jobs[1]["steps"][0]["name"] = core.CHECKOUT_PREFIX + fixtures.AFTER
        jobs[1]["steps"][1]["conclusion"] = "skipped"
        jobs[1]["steps"][3].update(
            name="Reuse isolated gate " + fixtures.hosted.source_text(fixture.proof),
            conclusion="success",
        )
        github.data["actions/runs/31/attempts/1/jobs?per_page=100&page=1"] = {
            "total_count": 5,
            "jobs": jobs,
        }
        event = {
            "action": "completed",
            "repository": run["repository"],
            "workflow_run": run,
        }
        github.data["git/ref/heads/main"] = ref_object(
            "refs/heads/main", fixtures.AFTER
        )
        github.data["git/ref/tags/main-" + fixtures.AFTER] = ref_object(
            "refs/tags/main-" + fixtures.AFTER, fixtures.AFTER
        )
        with patch.dict(os.environ, {"QA_VERIFIER_APP_ID": str(APP)}):
            verdict = core.verify_main(event, github)
            self.assertIsInstance(verdict, core.MainVerdict)
            check = self.check | {
                "head_sha": fixtures.AFTER,
                "external_id": core.source_id(verdict),
                "output": {"text": core.encode_proof(verdict)},
            }
            github.data[
                f"commits/{fixtures.AFTER}/check-runs?check_name=qa-main-verdict&filter=all&per_page=100&page=1"
            ] = {"total_count": 1, "check_runs": [check]}
            actual, _ = publisher.authenticate(event, github, APP)
            self.assertEqual(actual.record["version"], 4)
            self.assertEqual(list(actual.record["gates"].values()).count("PASS"), 22)
            self.assertEqual(list(actual.record["gates"].values()).count("REUSED"), 1)
            fixture.check["app"]["id"] = 99
            with self.assertRaises(ValueError):
                publisher.authenticate(event, github, APP)

    def test_invalid_publication_identity_rejects_without_any_http(self):
        for repository, ref, target in (
            ("other/repo", "refs/heads/main", MERGE),
            (REPO, "refs/tags/main", MERGE),
            (REPO, "refs/heads/main", HEAD),
            (REPO, "refs/heads/main", "bad"),
        ):
            with (
                self.subTest(ref=ref, target=target),
                patch.object(self.writer, "request") as http,
            ):
                with self.assertRaises(ValueError):
                    publisher.publish_main_tag(
                        repository, ref, target, self.verdict, self.writer
                    )
                http.assert_not_called()

    def test_cli_reauthenticates_before_reading_key_or_minting_token(self):
        with tempfile.TemporaryDirectory() as directory:
            event = Path(directory) / "event.json"
            proof = Path(directory) / "proof.json"
            event.write_text(json.dumps(self.github.event))
            env = {
                "GITHUB_EVENT_NAME": "workflow_run",
                "GITHUB_REF": "refs/heads/main",
                "GITHUB_REPOSITORY": REPO,
                "GITHUB_REPOSITORY_ID": "10",
                "GITHUB_SHA": BASE,
                "GITHUB_EVENT_PATH": str(event),
                "GH_TOKEN": "unused",
                "QA_CI_WORKFLOW_ID": "20",
                "QA_VERIFIER_APP_ID": str(APP),
                "QA_PUBLISHER_APP_ID": str(PUBLISHER),
                "QA_TAG_ENABLED": "true",
            }
            with (
                patch.dict(os.environ, env, clear=True),
                patch.object(core, "GitHubReader", return_value=self.github),
                patch.object(
                    publisher.sys,
                    "argv",
                    ["publish_main_tag.py", "authenticate", "--proof", str(proof)],
                ),
            ):
                self.assertEqual(publisher.main(), 0)
            self.assertEqual(proof.stat().st_mode & 0o777, 0o600)
            reads = []

            class KeyTrackingEnvironment(dict):
                def __getitem__(self, key):
                    if key == "QA_PUBLISHER_PRIVATE_KEY":
                        reads.append(key)
                    return super().__getitem__(key)

            observed_env = KeyTrackingEnvironment(
                env | {"QA_PUBLISHER_PRIVATE_KEY": "unused"}
            )
            with (
                patch.object(os, "environ", observed_env),
                patch.object(core, "GitHubReader", return_value=self.github),
                patch.object(
                    publisher,
                    "publish_with_app",
                    return_value=publisher.Publication("noop", REF, MERGE),
                ) as mint,
                patch.object(
                    publisher.sys,
                    "argv",
                    ["publish_main_tag.py", "publish", "--proof", str(proof)],
                ),
            ):
                self.assertEqual(publisher.main(), 0)
                mint.assert_called_once()
            self.assertEqual(len(reads), 1)
            reads.clear()
            self.github.run["conclusion"] = "cancelled"
            with (
                patch.object(os, "environ", observed_env),
                patch.object(core, "GitHubReader", return_value=self.github),
                patch.object(publisher, "publish_with_app") as mint,
                patch.object(
                    publisher.sys,
                    "argv",
                    ["publish_main_tag.py", "publish", "--proof", str(proof)],
                ),
            ):
                self.assertEqual(publisher.main(), 1)
                mint.assert_not_called()
            self.assertEqual(reads, [])


if __name__ == "__main__":
    unittest.main()
