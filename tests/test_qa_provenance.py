"""Adversarial provider fixtures for isolated PR provenance."""

import copy
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.parse import urlencode

from scripts import qa_provenance as provenance

ROOT = Path(__file__).resolve().parents[1]
BASE, HEAD, MERGE, TREE = (letter * 40 for letter in "abcd")
REPO = "buenhyden/hy-home.k8s"
NOW = "2026-10-02T00:00:00Z"


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


class FakeGitHub(provenance.GitHubReader):
    def __init__(self):
        super().__init__("unused", REPO, 10, 20, BASE, root=ROOT)
        repo = {
            "id": 10,
            "full_name": REPO,
            "default_branch": "main",
            "owner": {"login": "buenhyden"},
        }
        pr_ref = {
            "number": 7,
            "base": {"sha": BASE, "repo": repo},
            "head": {"sha": HEAD, "repo": repo, "ref": "codex/test-provenance"},
        }
        self.run = {
            "id": 30,
            "run_attempt": 2,
            "workflow_id": 20,
            "event": "pull_request",
            "status": "completed",
            "conclusion": "success",
            "head_sha": HEAD,
            "head_branch": "codex/test-provenance",
            "path": ".github/workflows/ci.yml",
            "repository": repo,
            "head_repository": repo,
            "pull_requests": [pr_ref],
            "updated_at": NOW,
        }
        self.event = {
            "action": "completed",
            "repository": repo,
            "workflow_run": copy.deepcopy(self.run),
        }
        files = [
            ".github/workflows/ci.yml",
            "scripts/qa_provenance.py",
            "scripts/qa_provenance_records.py",
            "scripts/qa_provenance_hosted.py",
            "scripts/qa.py",
            "scripts/run-validation-lane.py",
            "scripts/validation/registry.json",
            ".github/requirements/ci-validation.txt",
        ]
        self.entries = [
            {
                "path": name,
                "type": "blob",
                "mode": "100644",
                "sha": blob((ROOT / name).read_bytes()),
            }
            for name in files
        ]
        self.data = {
            "": repo,
            "actions/workflows/20": {
                "id": 20,
                "path": ".github/workflows/ci.yml",
                "state": "active",
            },
            "actions/runs/30": self.run,
            "actions/runs/30/attempts/2": self.run,
            "pulls/7": dict(
                pr_ref,
                state="open",
                commits=1,
                merge_commit_sha=MERGE,
                base=dict(pr_ref["base"], ref="main"),
            ),
            "pulls/7/commits?per_page=100&page=1": [{"sha": HEAD}],
            "git/commits/" + BASE: {
                "sha": BASE,
                "tree": {"sha": "e" * 40},
                "parents": [],
            },
            "git/commits/" + HEAD: {
                "sha": HEAD,
                "tree": {"sha": "f" * 40},
                "parents": [{"sha": BASE}],
            },
            "git/commits/" + MERGE: {
                "sha": MERGE,
                "tree": {"sha": TREE},
                "parents": [{"sha": BASE}, {"sha": HEAD}],
            },
        }
        for sha in ("e" * 40, "f" * 40, TREE):
            self.data["git/trees/" + sha + "?recursive=1"] = {
                "sha": sha,
                "truncated": False,
                "tree": copy.deepcopy(self.entries),
            }
        self.jobs = [
            {
                "id": 40 + i,
                "run_id": 30,
                "run_attempt": 2,
                "head_sha": HEAD,
                "name": name,
                "status": "completed",
                "conclusion": "success",
                "steps": [],
            }
            for i, name in enumerate(
                ("branch-policy", "qa", "ci-summary", "qa-isolated", "qa-source")
            )
        ]
        self.jobs[1]["steps"] = [
            {
                "number": 1,
                "name": "Checkout QA commit " + MERGE,
                "status": "completed",
                "conclusion": "success",
            },
            {
                "number": 2,
                "name": "Validate repository complement",
                "status": "completed",
                "conclusion": "success",
            },
        ]
        self.jobs[1]["steps"] += [
            {
                "number": 3,
                "name": "Validate repository checkout",
                "status": "completed",
                "conclusion": "skipped",
            },
            {
                "number": 4,
                "name": "Reuse isolated gate ",
                "status": "completed",
                "conclusion": "skipped",
            },
        ]
        self.jobs[3]["steps"] = [
            {
                "number": 1,
                "name": "Checkout QA commit " + MERGE,
                "status": "completed",
                "conclusion": "success",
            },
            {
                "number": 2,
                "name": "Validate isolated repository gate",
                "status": "completed",
                "conclusion": "success",
            },
        ]
        self.jobs[4]["conclusion"] = "skipped"
        self.data["actions/runs/30/attempts/2/jobs?per_page=100&page=1"] = {
            "total_count": 5,
            "jobs": self.jobs,
        }
        self.calls = []

    def request(self, route, *, method="GET", body=None, token=None):
        self.calls.append((route, method, body))
        return copy.deepcopy(
            self.data[
                route.removeprefix("/repos/" + REPO + "/").removeprefix(
                    "/repos/" + REPO
                )
            ]
        )


class MainVerdictTests(unittest.TestCase):
    def setUp(self):
        self.github = FakeGitHub()
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
        self.clock = patch.object(
            provenance,
            "utc_now",
            return_value=datetime(2026, 10, 2, tzinfo=timezone.utc),
        )
        self.clock.start()
        self.addCleanup(self.clock.stop)

    def verify(self):
        return provenance.verify_main(self.github.event, self.github)

    def test_main_full_verdict_binds_source_commit_not_verifier_tip(self):
        verdict = self.verify()
        self.assertIsInstance(verdict, provenance.MainVerdict)
        self.assertEqual(verdict.record["checkout"], {"commit": MERGE, "tree": TREE})
        self.assertEqual(verdict.record["control"], BASE)
        self.assertEqual(verdict.record["source"], {"run": 30, "attempt": 2, "job": 41})
        registry = json.loads((ROOT / provenance.REGISTRY_PATH).read_text())
        self.assertEqual(
            verdict.record["gates"], dict.fromkeys(registry["profiles"]["full"], "PASS")
        )
        self.assertEqual(verdict.record["event"], "push")
        self.assertEqual(verdict.record["ref"], "refs/heads/main")
        self.assertNotIn("base", verdict.record)
        with self.assertRaises(ValueError):
            provenance.parse_proof(provenance.encode_proof(verdict).encode())

    def test_full_main_does_not_assume_an_integration_strategy_or_parent(self):
        for parents in ([BASE, HEAD], [BASE], [HEAD], []):
            with self.subTest(parents=parents):
                self.github.data["git/commits/" + MERGE]["parents"] = [
                    {"sha": parent} for parent in parents
                ]
                self.assertIsInstance(self.verify(), provenance.MainVerdict)

    def test_main_rejects_wrong_event_branch_repository_attempt_and_checkout(self):
        for field, value in (
            ("event", "pull_request"),
            ("event", "workflow_dispatch"),
            ("head_branch", "codex/feature"),
            ("run_attempt", 3),
            ("workflow_id", 99),
            ("head_sha", HEAD),
        ):
            with self.subTest(field=field, value=value):
                original = self.github.run[field]
                self.github.run[field] = value
                self.assertIsInstance(self.verify(), provenance.Reject)
                self.github.run[field] = original
        self.github.event["repository"] = {"id": 99, "full_name": REPO}
        self.assertIsInstance(self.verify(), provenance.Reject)

    def test_main_rejects_failed_candidate_summary_or_aggregate(self):
        for job_index in (1, 2):
            for conclusion in ("failure", "skipped", "cancelled", None):
                with self.subTest(job=job_index, conclusion=conclusion):
                    self.github.jobs[job_index]["conclusion"] = conclusion
                    self.assertIsInstance(self.verify(), provenance.Reject)
            self.github.jobs[job_index]["conclusion"] = "success"
        self.github.jobs[1]["steps"][1]["conclusion"] = "skipped"
        self.assertIsInstance(self.verify(), provenance.Reject)

    def test_main_rejects_changed_control_lock_missing_commit_or_expired_run(self):
        for path in (
            "scripts/qa.py",
            "scripts/qa_provenance.py",
            ".github/workflows/ci.yml",
            provenance.LOCK_PATH,
        ):
            with self.subTest(path=path):
                entries = self.github.data["git/trees/" + TREE + "?recursive=1"]["tree"]
                entry = next(row for row in entries if row["path"] == path)
                original = entry["sha"]
                entry["sha"] = "1" * 40
                self.assertIsInstance(self.verify(), provenance.Reject)
                entry["sha"] = original
        self.github.run["updated_at"] = "2026-08-01T00:00:00Z"
        self.assertIsInstance(self.verify(), provenance.Reject)
        self.github.run["updated_at"] = NOW
        del self.github.data["git/commits/" + MERGE]
        self.assertIsInstance(self.verify(), provenance.Reject)

    def test_main_rejects_missing_duplicate_or_wrong_attempt_jobs(self):
        original = copy.deepcopy(self.github.jobs)
        for change in ("missing", "duplicate", "wrong-attempt", "wrong-checkout"):
            with self.subTest(change=change):
                self.github.jobs[:] = copy.deepcopy(original)
                if change == "missing":
                    self.github.jobs.pop()
                    self.github.data[
                        "actions/runs/30/attempts/2/jobs?per_page=100&page=1"
                    ]["total_count"] = 2
                elif change == "duplicate":
                    self.github.jobs[2]["id"] = self.github.jobs[1]["id"]
                elif change == "wrong-attempt":
                    self.github.jobs[1]["run_attempt"] = 1
                else:
                    self.github.jobs[1]["steps"][0]["name"] = (
                        "Checkout QA commit " + HEAD
                    )
                self.assertIsInstance(self.verify(), provenance.Reject)
                self.github.data["actions/runs/30/attempts/2/jobs?per_page=100&page=1"][
                    "total_count"
                ] = 3

    def test_main_cli_reauthenticates_before_publication_and_rejects_changed_source(
        self,
    ):
        with tempfile.TemporaryDirectory() as directory:
            event = Path(directory) / "event.json"
            output = Path(directory) / "proof.json"
            event.write_text(json.dumps(self.github.event))
            environment = {
                "GITHUB_EVENT_NAME": "workflow_run",
                "GITHUB_REF": "refs/heads/main",
                "GITHUB_REPOSITORY": REPO,
                "GITHUB_REPOSITORY_ID": "10",
                "GITHUB_SHA": BASE,
                "GITHUB_EVENT_PATH": str(event),
                "GH_TOKEN": "unused",
                "QA_CI_WORKFLOW_ID": "20",
                "QA_VERIFIER_APP_ID": "77",
            }
            with (
                patch.dict(os.environ, environment, clear=True),
                patch.object(provenance, "GitHubReader", return_value=self.github),
                patch.object(
                    provenance.sys,
                    "argv",
                    ["qa_provenance.py", "authenticate", "--proof", str(output)],
                ),
            ):
                self.assertEqual(provenance.main(), 0)
            recorded = provenance.parse_main_verdict(output.read_bytes())
            self.assertEqual(recorded.record["checkout"]["commit"], MERGE)
            self.assertEqual(output.stat().st_mode & 0o777, 0o600)
            self.github.run["conclusion"] = "failure"
            with (
                patch.dict(os.environ, environment, clear=True),
                patch.object(provenance, "GitHubReader", return_value=self.github),
                patch.object(provenance, "publish") as publish,
                patch.object(
                    provenance.sys,
                    "argv",
                    ["qa_provenance.py", "publish", "--proof", str(output)],
                ),
            ):
                self.assertEqual(provenance.main(), 1)
                publish.assert_not_called()

    def test_main_publication_names_exact_source_commit_and_revokes_narrow_token(self):
        verdict = self.verify()
        installation = {
            "app_id": 77,
            "id": 88,
            "permissions": provenance.APP_PERMISSIONS,
            "suspended_at": None,
        }
        check = {
            "name": "qa-main-verdict",
            "app": {"id": 77},
            "head_sha": MERGE,
            "status": "completed",
            "conclusion": "success",
            "external_id": "30:2:41",
            "output": {"text": provenance.encode_proof(verdict)},
        }
        with (
            patch.object(provenance, "app_jwt", return_value="unused"),
            patch.object(
                self.github,
                "request",
                side_effect=[
                    installation,
                    {"token": "unused", "permissions": provenance.APP_PERMISSIONS},
                    check,
                    None,
                ],
            ) as request,
        ):
            provenance.publish(verdict, self.github, 77, "unused")
        body = request.call_args_list[2].kwargs["body"]
        self.assertEqual(body["name"], "qa-main-verdict")
        self.assertEqual(body["head_sha"], MERGE)
        self.assertEqual(request.call_args_list[-1].kwargs["method"], "DELETE")
        self.assertEqual(
            request.call_args_list[1].kwargs["body"]["permissions"]["contents"], "read"
        )

    def test_main_check_is_app_bound_complete_and_never_a_reuse_source(self):
        verdict = self.verify()
        payload = provenance.encode_proof(verdict)
        check = {
            "name": "qa-main-verdict",
            "app": {"id": 77},
            "head_sha": MERGE,
            "status": "completed",
            "conclusion": "success",
            "external_id": "30:2:41",
            "output": {"text": payload},
        }
        self.assertEqual(provenance.read_main_check(check, 77).record, verdict.record)
        self.assertIsInstance(provenance.read_check(check, 77), provenance.Reject)
        for mutate in (
            lambda c: c["app"].update(id=88),
            lambda c: c.update(head_sha=BASE),
            lambda c: c.update(external_id="30:1:41"),
            lambda c: c["output"].update(text=payload.replace('"PASS"', '"REUSED"')),
            lambda c: c["output"].update(
                text=payload.replace('"unattested"', '"forged-runtime"')
            ),
            lambda c: c["output"].update(text="x" * 16385),
            lambda c: c["output"].update(
                text=payload.replace(NOW, "2026-08-01T00:00:00Z")
            ),
        ):
            candidate = copy.deepcopy(check)
            mutate(candidate)
            self.assertIsInstance(
                provenance.read_main_check(candidate, 77), provenance.Reject
            )


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.github = FakeGitHub()
        self.clock = patch.object(
            provenance,
            "utc_now",
            return_value=datetime(2026, 10, 2, tzinfo=timezone.utc),
        )
        self.clock.start()
        self.addCleanup(self.clock.stop)

    def verify(self):
        return provenance.verify_pr(self.github.event, self.github)

    def test_complete_pass_binds_merge_not_actions_head(self):
        proof = self.verify()
        self.assertIsInstance(proof, provenance.Proof)
        self.assertEqual(proof.record["checkout"], {"commit": MERGE, "tree": TREE})
        self.assertEqual(proof.record["head"], HEAD)
        self.assertEqual(proof.record["source"], {"run": 30, "attempt": 2, "job": 41})
        registry = json.loads((ROOT / "scripts/validation/registry.json").read_text())
        self.assertEqual(set(proof.record["gates"]), set(registry["profiles"]["full"]))
        self.assertEqual(set(proof.record["gates"].values()), {"PASS"})
        self.assertEqual(proof.record["tools"]["runtime"], "unattested")

    def fork_source(self):
        self.github = FakeGitHub()
        fork = {
            "id": 90,
            "full_name": "fork-owner/hy-home.k8s",
            "owner": {"login": "fork-owner"},
        }
        branch = "codex/fork&title=encoded"
        self.github.run.update(
            head_repository=fork, head_branch=branch, pull_requests=[]
        )
        self.github.event["workflow_run"] = copy.deepcopy(self.github.run)
        pr = self.github.data["pulls/7"]
        pr["head"] = {"repo": fork, "sha": HEAD, "ref": branch}
        query = urlencode(
            {"state": "open", "base": "main", "head": "fork-owner:" + branch}
        )
        route = "pulls?" + query + "&per_page=100&page=1"
        self.github.data[route] = [copy.deepcopy(pr)]
        return route, pr

    def test_empty_fork_relation_uses_unique_provider_lookup(self):
        route, _ = self.fork_source()
        proof = self.verify()
        self.assertIsInstance(proof, provenance.Proof)
        self.assertEqual(proof.record["pr"], 7)
        self.assertEqual(proof.record["checkout"]["commit"], MERGE)
        self.assertIn(("/repos/" + REPO + "/" + route, "GET", None), self.github.calls)
        self.assertIn("head=fork-owner%3Acodex%2Ffork%26title%3Dencoded", route)

    def test_fork_lookup_rejects_missing_ambiguous_or_changed_candidates(self):
        for change in (
            "missing",
            "ambiguous",
            "stale-list-head",
            "stale-list-repo",
            "closed",
            "head-ref",
            "head-repo",
            "head-sha",
            "base-sha",
            "merge-sha",
        ):
            with self.subTest(change=change):
                route, pr = self.fork_source()
                if change == "missing":
                    self.github.data[route] = []
                elif change == "ambiguous":
                    self.github.data[route].append(copy.deepcopy(pr))
                elif change == "stale-list-head":
                    self.github.data[route][0]["head"]["sha"] = BASE
                elif change == "stale-list-repo":
                    self.github.data[route][0]["head"]["repo"]["id"] = 91
                elif change == "closed":
                    pr["state"] = "closed"
                elif change.startswith("head-"):
                    pr["head"] = copy.deepcopy(pr["head"])
                    if change == "head-repo":
                        pr["head"]["repo"]["id"] = 91
                    else:
                        pr["head"][change[5:]] = BASE
                elif change == "base-sha":
                    pr["base"]["sha"] = HEAD
                else:
                    pr["merge_commit_sha"] = HEAD
                self.assertIsInstance(self.verify(), provenance.Reject)

    def test_empty_relation_requires_source_owner_and_branch_not_just_sha(self):
        for missing in ("head_repository", "owner", "head_branch"):
            with self.subTest(missing=missing):
                self.fork_source()
                if missing == "owner":
                    del self.github.run["head_repository"]["owner"]
                else:
                    del self.github.run[missing]
                self.assertIsInstance(self.verify(), provenance.Reject)

    def test_failed_missing_cancelled_or_wrong_source_is_rejected(self):
        for field, values in {
            "conclusion": [None, "failure", "cancelled", "skipped"],
            "run_attempt": [1, 3],
            "workflow_id": [999],
            "event": ["push", "pull_request_target"],
            "head_sha": [BASE],
            "status": ["in_progress"],
            "path": [".github/workflows/forged.yml"],
        }.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    self.github = FakeGitHub()
                    self.github.run[field] = value
                    self.assertIsInstance(self.verify(), provenance.Reject)
        self.github = FakeGitHub()
        del self.github.data["actions/runs/30"]
        self.assertIsInstance(self.verify(), provenance.Reject)

    def test_wrong_repository_pr_base_or_head_is_rejected(self):
        for target, field, value in [
            ("repository", "id", 999),
            ("base", "sha", HEAD),
            ("head", "sha", BASE),
        ]:
            with self.subTest(target=target):
                self.github = FakeGitHub()
                obj = (
                    self.github.run["repository"]
                    if target == "repository"
                    else self.github.data["pulls/7"][target]
                )
                obj[field] = value
                self.assertIsInstance(self.verify(), provenance.Reject)

    def test_wrong_job_attempt_id_and_missing_or_skipped_aggregate_fail(self):
        for field, value in [
            ("run_id", 999),
            ("run_attempt", 1),
            ("id", 40),
            ("conclusion", "failure"),
        ]:
            with self.subTest(field=field):
                self.github = FakeGitHub()
                self.github.jobs[1][field] = value
                self.assertIsInstance(self.verify(), provenance.Reject)
        for value in ("skipped", "failure", "cancelled", None):
            self.github = FakeGitHub()
            self.github.jobs[1]["steps"][1]["conclusion"] = value
            self.assertIsInstance(self.verify(), provenance.Reject)

    def test_checkout_requires_durable_merge_parents(self):
        self.github.jobs[1]["steps"][0]["name"] = "Checkout QA commit " + HEAD
        self.assertIsInstance(self.verify(), provenance.Reject)
        self.github = FakeGitHub()
        del self.github.data["git/commits/" + MERGE]
        self.assertIsInstance(self.verify(), provenance.Reject)
        self.github = FakeGitHub()
        self.github.data["git/commits/" + MERGE]["parents"].reverse()
        self.assertIsInstance(self.verify(), provenance.Reject)

    def test_any_commit_control_add_edit_delete_and_revert_is_rejected(self):
        paths = [
            ".github/workflows/evil.yml",
            "scripts/qa.py",
            "scripts/qa_provenance.py",
            "scripts/qa_provenance_records.py",
            "scripts/qa_provenance_hosted.py",
            "scripts/publish_main_tag.py",
            "scripts/validation/repository/bounded_io.py",
            "scripts/validation/registry.json",
            ".github/requirements/ci-validation.txt",
            ".agents/evaluations/helper.py",
            ".agents/skills/external-service-contract-audit/scripts/helper.py",
            ".github/actions/local/action.yml",
        ]
        for path in paths:
            for kind in ("add", "edit", "delete"):
                with self.subTest(path=path, kind=kind):
                    self.github = FakeGitHub()
                    baseline = self.github.data[
                        "git/trees/" + "e" * 40 + "?recursive=1"
                    ]["tree"]
                    changed = self.github.data[
                        "git/trees/" + "f" * 40 + "?recursive=1"
                    ]["tree"]
                    baseline[:] = [entry for entry in baseline if entry["path"] != path]
                    changed[:] = [entry for entry in changed if entry["path"] != path]
                    item = {
                        "path": path,
                        "type": "blob",
                        "mode": "100644",
                        "sha": "1" * 40,
                    }
                    if kind != "add":
                        baseline.append(item)
                    if kind != "delete":
                        changed.append(dict(item, sha="2" * 40))
                    # The final merge has restored the reviewed baseline.
                    self.github.data["git/trees/" + TREE + "?recursive=1"]["tree"] = (
                        copy.deepcopy(baseline)
                    )
                    self.assertIsInstance(self.verify(), provenance.Reject)

    def test_root_and_nested_attributes_reverted_before_head_still_reject(self):
        for path in (
            ".gitattributes",
            "docs/.gitattributes",
            "tests/fixtures/nested/.gitattributes",
        ):
            with self.subTest(path=path):
                self.github = FakeGitHub()
                intermediate, changed_tree = "2" * 40, "3" * 40
                self.github.data["pulls/7"]["commits"] = 2
                self.github.data["pulls/7/commits?per_page=100&page=1"] = [
                    {"sha": intermediate},
                    {"sha": HEAD},
                ]
                self.github.data["git/commits/" + intermediate] = {
                    "sha": intermediate,
                    "tree": {"sha": changed_tree},
                    "parents": [{"sha": BASE}],
                }
                self.github.data["git/commits/" + HEAD]["parents"] = [
                    {"sha": intermediate}
                ]
                entries = copy.deepcopy(self.github.entries)
                entries.append(
                    {"path": path, "type": "blob", "mode": "100644", "sha": "4" * 40}
                )
                self.github.data["git/trees/" + changed_tree + "?recursive=1"] = {
                    "sha": changed_tree,
                    "truncated": False,
                    "tree": entries,
                }
                self.assertIsInstance(self.verify(), provenance.Reject)

    def test_truncated_history_or_tree_is_not_a_clean_closure(self):
        self.github.data["pulls/7"]["commits"] = 2
        self.assertIsInstance(self.verify(), provenance.Reject)
        self.github = FakeGitHub()
        self.github.data["git/trees/" + "f" * 40 + "?recursive=1"]["truncated"] = True
        self.assertIsInstance(self.verify(), provenance.Reject)

    def test_qa_artifact_or_mutated_checkout_never_supplies_proof(self):
        self.github.event["artifact"] = {"gates": {"forged": "PASS"}, "checkout": HEAD}
        self.github.event["workflow_run"]["logs"] = (
            "passing test rewrote qa_provenance.py"
        )
        proof = self.verify()
        self.assertIsInstance(proof, provenance.Proof)
        self.assertNotIn("forged", proof.record["gates"])
        self.assertFalse(
            any(
                "artifact" in path or "logs" in path for path, _, _ in self.github.calls
            )
        )

    def test_proof_schema_size_age_and_author_are_checked(self):
        proof = self.verify()
        payload = provenance.encode_proof(proof)
        check = {
            "name": "qa-provenance",
            "app": {"id": 77},
            "head_sha": HEAD,
            "status": "completed",
            "conclusion": "success",
            "external_id": "30:2:41",
            "output": {"text": payload},
        }
        self.assertEqual(provenance.read_check(check, 77).record, proof.record)
        for mutate in (
            lambda c: c["app"].update(id=88),
            lambda c: c.update(head_sha=MERGE),
            lambda c: c.update(external_id="30:1:41"),
            lambda c: c["output"].update(text="{}"),
            lambda c: c["output"].update(text="x" * 16385),
            lambda c: c["output"].update(
                text=payload.replace(NOW, "2026-08-01T00:00:00Z")
            ),
            lambda c: c["output"].update(
                text=payload.replace('"version":3', '"version":3,"version":3')
            ),
        ):
            candidate = copy.deepcopy(check)
            mutate(candidate)
            self.assertIsInstance(
                provenance.read_check(candidate, 77), provenance.Reject
            )

    def test_passing_child_mutation_cannot_change_isolated_proof(self):
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            child = checkout / "test_pass.py"
            child.write_text(
                "from pathlib import Path\nPath('qa_provenance.py').write_text('forged proof producer')\n"
            )
            subprocess.run(["python3", str(child)], cwd=checkout, check=True, timeout=5)
            self.assertEqual(
                (checkout / "qa_provenance.py").read_text(), "forged proof producer"
            )
            self.github.event["artifact_path"] = str(checkout / "qa_provenance.py")
            proof = self.verify()
            self.assertIsInstance(proof, provenance.Proof)
            self.assertEqual(proof.record["checkout"]["commit"], MERGE)

    def test_incomplete_step_names_and_registry_skip_contract_fail(self):
        for mutation in (
            lambda g: g.jobs[1]["steps"].pop(),
            lambda g: g.jobs[1]["steps"].append(copy.deepcopy(g.jobs[1]["steps"][0])),
            lambda g: g.jobs[1]["steps"][0].update(number=3),
            lambda g: g.jobs[1]["steps"][0].update(
                name="Checkout QA commit " + "g" * 40
            ),
        ):
            self.github = FakeGitHub()
            mutation(self.github)
            self.assertIsInstance(self.verify(), provenance.Reject)
        original = provenance.trusted_bytes

        def optional_registry(github, controls, path):
            payload = original(github, controls, path)
            if path == provenance.REGISTRY_PATH:
                registry = json.loads(payload)
                name = registry["profiles"]["full"][0]
                next(row for row in registry["validators"] if row["id"] == name)[
                    "optional"
                ] = True
                return json.dumps(registry).encode()
            return payload

        self.github = FakeGitHub()
        with patch.object(provenance, "trusted_bytes", side_effect=optional_registry):
            self.assertIsInstance(self.verify(), provenance.Reject)

    def test_proof_rejects_malformed_nested_shape_and_non_pass(self):
        record = self.verify().record
        for mutation in (
            lambda r: r.update(version=True),
            lambda r: r.update(pr="7"),
            lambda r: r.update(gates={"test": "SKIP"}),
            lambda r: r.update(gates=[]),
            lambda r: r["checkout"].update(commit=HEAD + "\n"),
            lambda r: r["source"].update(attempt=0),
            lambda r: r.update(extra="unknown"),
        ):
            candidate = copy.deepcopy(record)
            mutation(candidate)
            with self.assertRaises((ValueError, TypeError)):
                provenance.parse_proof(json.dumps(candidate).encode())

    def test_pages_and_transport_are_bounded(self):
        with patch.object(self.github, "get", return_value=[{}] * 100) as get:
            with self.assertRaises(ValueError):
                self.github.pages("pulls/7/commits")
            self.assertEqual(get.call_count, provenance.MAX_PAGES)
        reader = provenance.GitHubReader("unused", REPO, 10, 20, BASE)
        reader.requests = 600
        with patch.object(provenance, "build_opener") as opener:
            with self.assertRaises(ValueError):
                reader.get("")
            opener.assert_not_called()
        with self.assertRaises(ValueError):
            provenance.decode(
                b"x" * (provenance.PROOF_LIMIT + 1), provenance.PROOF_LIMIT
            )
        with self.assertRaises(ValueError):
            provenance.NoRedirect().redirect_request(
                None, None, 302, "", {}, "https://elsewhere.invalid"
            )

    def test_compare_route_allows_exact_shas_but_rejects_traversal(self):
        reader = provenance.GitHubReader("unused", REPO, 10, 20, BASE)
        with patch.object(provenance, "build_opener") as opener:
            opener.return_value.open.return_value.__enter__.return_value.read.return_value = b"{}"
            self.assertEqual(reader.get(f"compare/{BASE}...{HEAD}"), {})
            self.assertIn(
                f"compare/{BASE}...{HEAD}",
                opener.return_value.open.call_args.args[0].full_url,
            )
            for route in (
                "../secret",
                f"compare/{BASE}...{HEAD}/../secret",
                f"compare/{BASE}...{'g' * 40}",
            ):
                with self.subTest(route=route), self.assertRaises(ValueError):
                    reader.get(route)

    def test_rejected_source_never_reads_app_key_or_publishes(self):
        with tempfile.TemporaryDirectory() as directory:
            event_path = Path(directory) / "event.json"
            event_path.write_text(json.dumps(self.github.event))
            environment = {
                "GITHUB_EVENT_NAME": "workflow_run",
                "GITHUB_REF": "refs/heads/main",
                "GITHUB_REPOSITORY": REPO,
                "GITHUB_REPOSITORY_ID": "10",
                "GITHUB_SHA": BASE,
                "GITHUB_EVENT_PATH": str(event_path),
                "GH_TOKEN": "unused",
                "QA_CI_WORKFLOW_ID": "20",
            }
            with (
                patch.dict(os.environ, environment, clear=True),
                patch.object(
                    provenance,
                    "verify_pr",
                    return_value=provenance.Reject("bad source"),
                ),
                patch.object(provenance, "publish") as publish,
                patch.object(
                    provenance.sys,
                    "argv",
                    [
                        "qa_provenance.py",
                        "publish",
                        "--proof",
                        str(Path(directory) / "proof"),
                    ],
                ),
            ):
                self.assertEqual(provenance.main(), 1)
                publish.assert_not_called()
            for event, ref in (
                ("pull_request", "refs/pull/7/merge"),
                ("workflow_run", "refs/heads/feature"),
                ("workflow_run", "refs/tags/main-x"),
            ):
                environment.update(GITHUB_EVENT_NAME=event, GITHUB_REF=ref)
                with (
                    patch.dict(os.environ, environment, clear=True),
                    patch.object(provenance, "GitHubReader") as reader,
                    patch.object(
                        provenance.sys,
                        "argv",
                        [
                            "qa_provenance.py",
                            "authenticate",
                            "--proof",
                            str(Path(directory) / "proof"),
                        ],
                    ),
                ):
                    self.assertEqual(provenance.main(), 1)
                    reader.assert_not_called()

    def test_publish_checks_ceiling_before_token_and_uses_only_narrow_permissions(self):
        proof = self.verify()
        installation = {
            "app_id": 77,
            "id": 88,
            "permissions": provenance.APP_PERMISSIONS,
            "suspended_at": None,
        }
        check = {
            "name": "qa-provenance",
            "app": {"id": 77},
            "head_sha": HEAD,
            "status": "completed",
            "conclusion": "success",
            "external_id": "30:2:41",
            "output": {"text": provenance.encode_proof(proof)},
        }
        with (
            patch.object(provenance, "app_jwt", return_value="unused"),
            patch.object(
                self.github,
                "request",
                side_effect=[
                    installation,
                    {"token": "unused", "permissions": provenance.APP_PERMISSIONS},
                    check,
                    None,
                ],
            ) as request,
        ):
            provenance.publish(proof, self.github, 77, "unused")
            body = request.call_args_list[2].kwargs["body"]
            self.assertEqual(body["head_sha"], HEAD)
            self.assertEqual(
                json.loads(body["output"]["text"])["checkout"]["commit"], MERGE
            )
            token_request = request.call_args_list[1].kwargs["body"]
            self.assertEqual(
                token_request,
                {"repository_ids": [10], "permissions": provenance.APP_PERMISSIONS},
            )
            self.assertEqual(request.call_args_list[-1].args[0], "/installation/token")
            self.assertEqual(request.call_args_list[-1].kwargs["method"], "DELETE")
        installation["permissions"] = dict(provenance.APP_PERMISSIONS, contents="write")
        with (
            patch.object(provenance, "app_jwt", return_value="unused"),
            patch.object(self.github, "request", return_value=installation) as request,
        ):
            with self.assertRaises(ValueError):
                provenance.publish(proof, self.github, 77, "unused")
            self.assertEqual(request.call_count, 1)

    def test_installation_cannot_hold_contents_write_or_extra_authority(self):
        allowed = provenance.APP_PERMISSIONS
        provenance.validate_installation(
            {"app_id": 77, "permissions": allowed, "suspended_at": None}, 77
        )
        for permission, value in (
            ("contents", "write"),
            ("administration", "read"),
            ("checks", "read"),
        ):
            with self.subTest(permission=permission):
                candidate = {
                    "app_id": 77,
                    "permissions": dict(allowed, **{permission: value}),
                    "suspended_at": None,
                }
                with self.assertRaises(ValueError):
                    provenance.validate_installation(candidate, 77)


if __name__ == "__main__":
    unittest.main()
