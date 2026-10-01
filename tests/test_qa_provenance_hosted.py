"""Isolated CI partitions and authenticated hosted reuse boundaries."""

import copy
import json
from pathlib import Path
import subprocess
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from scripts import qa_provenance as core
from tests.test_qa_provenance import FakeGitHub, BASE, HEAD, MERGE, TREE

from scripts import qa_provenance_hosted as hosted
from tests import test_qa_runner as qa_tests

ROOT = Path(__file__).resolve().parents[1]


class PartitionTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads(
            (ROOT / "scripts/validation/registry.json").read_text()
        )

    def test_registry_partitions_are_disjoint_and_cover_full_once(self):
        isolated = hosted.partition(self.registry, "isolated")
        complement = hosted.partition(self.registry, "complement")
        self.assertEqual(isolated, ["agent-evaluation-cases"])
        self.assertEqual(len(complement), 22)
        self.assertFalse(set(isolated) & set(complement))
        self.assertEqual(
            set(isolated + complement), set(self.registry["profiles"]["full"])
        )
        for required in (
            "archive-cutover",
            "document-lifecycle",
            "gitops-change-set",
            "unit-tests",
        ):
            self.assertIn(required, complement)

    def test_unaudited_candidate_or_runtime_change_fails_closed(self):
        for change in ("runtime", "argv", "candidate"):
            registry = copy.deepcopy(self.registry)
            gate = next(
                row
                for row in registry["validators"]
                if row["id"] == "agent-evaluation-cases"
            )
            if change == "runtime":
                gate["reuse"]["hosted"]["image"] = "python:3.12"
            elif change == "argv":
                gate["argv"].append("--changed")
            else:
                registry["validators"][0]["reuse"] = copy.deepcopy(gate["reuse"])
            with self.subTest(change=change), self.assertRaises(ValueError):
                hosted.partition(registry, "isolated")


class CommittedInputTests(unittest.TestCase):
    setUp = qa_tests.QaTests.setUp
    git = qa_tests.QaTests.git

    def test_git_accepts_only_its_canonical_checkout_when_owner_differs(self):
        commit = self.git("rev-parse", "HEAD")
        sibling = self.root.parent / "sibling"
        sibling.mkdir()
        subprocess.run(
            ["git", "init", "-q", str(sibling)], check=True, capture_output=True
        )
        with patch.dict(hosted.ENVIRONMENT, {"GIT_TEST_ASSUME_DIFFERENT_OWNER": "1"}):
            self.assertEqual(hosted.git(self.root, "rev-parse", "HEAD"), commit)
            with self.assertRaises(subprocess.CalledProcessError) as failed:
                hosted.git(self.root, "-C", str(sibling), "status", "--porcelain")
            self.assertIn(b"dubious ownership", failed.exception.stderr)

    def test_raw_checkout_accepts_exact_tree_and_rejects_checkout_transform(self):
        commit = self.git("rev-parse", "HEAD").decode().strip()
        hosted.require_committed_checkout(self.root, commit)
        self.git("config", "filter.fixture.clean", "sed s/transformed/original/")
        self.git("config", "filter.fixture.smudge", "sed s/original/transformed/")
        (self.root / ".gitattributes").write_text("file.txt filter=fixture\n")
        self.git("add", ".gitattributes")
        self.git("commit", "-qm", "filter fixture")
        commit = self.git("rev-parse", "HEAD").decode().strip()
        (self.root / "file.txt").write_text("transformed\n")
        self.assertEqual(self.git("diff", "--name-only"), b"")
        with self.assertRaisesRegex(ValueError, "committed"):
            hosted.require_committed_checkout(self.root, commit)

    def test_raw_checkout_rejects_staged_import_outside_commit(self):
        commit = self.git("rev-parse", "HEAD").decode().strip()
        (self.root / "json.py").write_text("raise SystemExit(0)\n")
        self.git("add", "json.py")
        with self.assertRaises(ValueError):
            hosted.require_committed_checkout(self.root, commit)

    def test_raw_checkout_rejects_wrong_commit_modes_and_untracked_imports(self):
        commit = self.git("rev-parse", "HEAD").decode().strip()
        with self.assertRaises(ValueError):
            hosted.require_committed_checkout(self.root, "0" * 40)
        (self.root / "file.txt").chmod(0o755)
        with self.assertRaises(ValueError):
            hosted.require_committed_checkout(self.root, commit)
        (self.root / "file.txt").chmod(0o644)
        (self.root / "malicious.py").write_text("raise SystemExit(0)\n")
        with self.assertRaises(ValueError):
            hosted.require_committed_checkout(self.root, commit)


class HostedWorkflowTests(unittest.TestCase):
    def test_isolated_runtime_and_read_only_lookup_are_explicit(self):
        import yaml

        workflow = yaml.safe_load((ROOT / ".github/workflows/ci.yml").read_text())
        isolated = workflow["jobs"]["qa-isolated"]
        self.assertEqual(isolated["container"]["image"], hosted.IMAGE)
        self.assertEqual(isolated["container"]["options"], "--platform linux/amd64")
        text = json.dumps(isolated)
        self.assertNotIn("secrets.", text)
        self.assertNotIn("actions/cache", text)
        self.assertNotIn("pip install", text)
        source = workflow["jobs"]["qa-source"]
        self.assertIn("QA_REUSE_ENABLED == 'true'", source["if"])
        self.assertEqual(set(source["permissions"].values()), {"read"})
        self.assertNotIn("secrets.", json.dumps(source))
        self.assertEqual(
            set(workflow["jobs"]["ci-summary"]["needs"]),
            {"branch-policy", "qa", "qa-isolated", "qa-source"},
        )


AFTER = "1" * 40


class HostedSourceTests(unittest.TestCase):
    def setUp(self):
        self.github = FakeGitHub()
        self.clock = patch.object(
            core, "utc_now", return_value=datetime(2026, 10, 2, tzinfo=timezone.utc)
        )
        self.clock.start()
        self.addCleanup(self.clock.stop)
        proof = core.verify_pr(self.github.event, self.github)
        self.assertIsInstance(proof, core.Proof)
        self.proof = proof
        self.github.data["pulls/7"].update(
            state="closed", merged=True, merge_commit_sha=AFTER
        )
        self.github.data["git/commits/" + AFTER] = {
            "sha": AFTER,
            "tree": {"sha": TREE},
            "parents": [{"sha": BASE}, {"sha": HEAD}],
        }
        self.github.data[f"compare/{BASE}...{AFTER}"] = {
            "status": "ahead",
            "merge_base_commit": {"sha": BASE},
            "total_commits": 1,
            "commits": [{"sha": AFTER}],
        }
        self.github.data[f"commits/{AFTER}/pulls?per_page=100&page=1"] = [{"number": 7}]
        self.github.data[
            f"actions/workflows/20/runs?event=pull_request&head_sha={HEAD}&status=success&per_page=100&page=1"
        ] = {"total_count": 1, "workflow_runs": [self.github.run]}
        self.check = {
            "id": 90,
            "name": "qa-provenance",
            "app": {"id": 80},
            "head_sha": MERGE,
            "external_id": core.source_id(proof),
            "status": "completed",
            "conclusion": "success",
            "output": {"text": core.encode_proof(proof)},
        }
        self.github.data[f"commits/{MERGE}/check-runs?per_page=100&page=1"] = {
            "total_count": 1,
            "check_runs": [self.check],
        }

    def source(self, before=BASE):
        return hosted.source_for_main(core, self.github, before, AFTER, 80)

    def test_merge_squash_rebase_and_multicommit_push_bind_original_before(self):
        for parents in ([BASE, HEAD], [BASE], [HEAD]):
            with self.subTest(parents=parents):
                self.github.data["git/commits/" + AFTER]["parents"] = [
                    {"sha": value} for value in parents
                ]
                self.assertEqual(self.source().record, self.proof.record)
        comparison = self.github.data[f"compare/{BASE}...{AFTER}"]
        comparison.update(total_commits=2, commits=[{"sha": HEAD}, {"sha": AFTER}])
        self.assertEqual(self.source().record, self.proof.record)
        with self.assertRaises((ValueError, KeyError)):
            self.source(HEAD)

    def closed_fork_relation(self):
        from urllib.parse import urlencode

        fork = {
            "id": 90,
            "full_name": "fork-owner/hy-home.k8s",
            "owner": {"login": "fork-owner"},
        }
        branch = "codex/fork&title=encoded"
        self.github.run.update(
            pull_requests=[], head_repository=fork, head_branch=branch
        )
        self.github.data["pulls/7"]["head"] = {"sha": HEAD, "repo": fork, "ref": branch}
        pr = copy.deepcopy(self.github.data["pulls/7"])
        query = urlencode(
            {"state": "closed", "base": "main", "head": "fork-owner:" + branch}
        )
        route = "pulls?" + query + "&per_page=100&page=1"
        self.github.data[route] = [pr]
        return route

    def test_merged_empty_relation_source_reconstructs_unique_historical_pr(self):
        self.closed_fork_relation()
        self.assertEqual(self.source().record, self.proof.record)

    def test_historical_discovery_rejects_ambiguity_and_changed_identities(self):
        route = self.closed_fork_relation()
        original = copy.deepcopy(self.github.data[route])
        for change in (
            "ambiguous",
            "base",
            "head",
            "merge",
            "branch",
            "repository",
            "unmerged",
        ):
            with self.subTest(change=change):
                self.github.data[route] = copy.deepcopy(original)
                self.github.data["pulls/7"]["merged"] = True
                relation = self.github.data[route][0]
                if change == "ambiguous":
                    self.github.data[route].append(copy.deepcopy(relation))
                elif change == "base":
                    relation["base"]["sha"] = HEAD
                elif change == "head":
                    relation["head"]["sha"] = BASE
                elif change == "merge":
                    relation["merge_commit_sha"] = MERGE
                elif change == "branch":
                    relation["head"]["ref"] = "codex/other"
                elif change == "repository":
                    relation["head"]["repo"]["id"] = 99
                else:
                    self.github.data["pulls/7"]["merged"] = False
                with self.assertRaises(ValueError):
                    self.source()

    def test_stale_candidate_does_not_hide_one_current_authenticated_source(self):
        stale = copy.deepcopy(self.github.run)
        stale.update(id=29, run_attempt=1)
        current = copy.deepcopy(stale)
        current["run_attempt"] = 2
        self.github.data["actions/runs/29"] = current
        self.github.data["actions/runs/29/attempts/1"] = stale
        route = f"actions/workflows/20/runs?event=pull_request&head_sha={HEAD}&status=success&per_page=100&page=1"
        self.github.data[route] = {
            "total_count": 2,
            "workflow_runs": [stale, self.github.run],
        }
        self.assertEqual(self.source().record, self.proof.record)
        self.github.data[route] = {"total_count": 1, "workflow_runs": [stale]}
        with self.assertRaises(ValueError):
            self.source()

    def test_multiple_valid_source_matches_still_fall_back(self):
        route = f"commits/{MERGE}/check-runs?per_page=100&page=1"
        self.github.data[route] = {
            "total_count": 2,
            "check_runs": [self.check, copy.deepcopy(self.check)],
        }
        with self.assertRaises(ValueError):
            self.source()

    def test_failed_candidate_or_duplicate_full_execution_never_reuses(self):
        for conclusion in ("failure", "cancelled", "skipped"):
            with self.subTest(conclusion=conclusion):
                self.github.jobs[3]["conclusion"] = conclusion
                with self.assertRaises(ValueError):
                    self.source()
        self.github.jobs[3]["conclusion"] = "success"
        self.github.jobs[1]["steps"][2]["conclusion"] = "success"
        with self.assertRaises(ValueError):
            self.source()

    def test_same_name_wrong_app_unattested_runtime_and_expired_proof_fail_closed(self):
        original = copy.deepcopy(self.check)
        for change in ("app", "runtime", "expired", "unattested", "identity", "source"):
            with self.subTest(change=change):
                self.check.clear()
                self.check.update(copy.deepcopy(original))
                record = copy.deepcopy(self.proof.record)
                if change == "app":
                    self.check["app"]["id"] = 81
                elif change == "runtime":
                    record["isolated"]["runtime"]["image"] = (
                        "docker.io/library/python@sha256:" + "f" * 64
                    )
                elif change == "expired":
                    record["completed_at"] = "2026-01-01T00:00:00Z"
                elif change == "unattested":
                    record.pop("isolated")
                    record["version"] = 1
                elif change == "identity":
                    record["isolated"]["input"] = "0" * 64
                else:
                    self.check["external_id"] = "30:1:41"
                self.check["output"]["text"] = json.dumps(record)
                with self.assertRaises(ValueError):
                    self.source()

    def test_changed_tree_lock_control_and_intermediate_helper_force_full(self):
        initial = copy.deepcopy(self.github.data)
        for change in ("tree", "lock", "helper", "history", "advanced"):
            with self.subTest(change=change):
                self.github.data = copy.deepcopy(initial)
                if change == "tree":
                    self.github.data["git/commits/" + AFTER]["tree"]["sha"] = "f" * 40
                elif change in ("lock", "helper"):
                    path = (
                        core.LOCK_PATH
                        if change == "lock"
                        else "scripts/qa_provenance_hosted.py"
                    )
                    entry = next(
                        e
                        for e in self.github.data[f"git/trees/{TREE}?recursive=1"][
                            "tree"
                        ]
                        if e["path"] == path
                    )
                    entry["sha"] = "0" * 40
                elif change == "history":
                    entry = next(
                        e
                        for e in self.github.data[f"git/trees/{'f' * 40}?recursive=1"][
                            "tree"
                        ]
                        if e["path"] == "scripts/qa_provenance_hosted.py"
                    )
                    entry["sha"] = "0" * 40
                else:
                    self.github.data[f"compare/{BASE}...{AFTER}"]["merge_base_commit"][
                        "sha"
                    ] = HEAD
                with self.assertRaises(ValueError):
                    self.source()

    def test_wrong_interpreter_rejected_before_running_candidate(self):
        with (
            patch.object(hosted.sys, "executable", "/usr/bin/python3"),
            patch.object(hosted.subprocess, "run") as run,
        ):
            with self.assertRaisesRegex(ValueError, "interpreter"):
                hosted.isolated(ROOT, AFTER)
            run.assert_not_called()

    def test_main_reauthenticates_lookup_and_publishes_one_reused_gate(self):
        run = copy.deepcopy(self.github.run)
        run.update(
            id=31,
            run_attempt=1,
            event="push",
            head_sha=AFTER,
            head_branch="main",
            pull_requests=[],
        )
        self.github.data["actions/runs/31"] = run
        self.github.data["actions/runs/31/attempts/1"] = run
        jobs = copy.deepcopy(self.github.jobs)
        for job in jobs:
            job.update(id=job["id"] + 10, run_id=31, run_attempt=1, head_sha=AFTER)
        jobs[0]["conclusion"] = jobs[3]["conclusion"] = "skipped"
        jobs[4]["conclusion"] = "success"
        jobs[4]["steps"] = [
            {
                "number": 1,
                "name": hosted.PUSH_PREFIX + BASE + " " + AFTER,
                "status": "completed",
                "conclusion": "success",
            }
        ]
        jobs[1]["steps"][0]["name"] = core.CHECKOUT_PREFIX + AFTER
        jobs[1]["steps"][1]["conclusion"] = "skipped"
        jobs[1]["steps"][3].update(
            name="Reuse isolated gate " + hosted.source_text(self.proof),
            conclusion="success",
        )
        self.github.data["actions/runs/31/attempts/1/jobs?per_page=100&page=1"] = {
            "total_count": 5,
            "jobs": jobs,
        }
        event = {
            "action": "completed",
            "repository": run["repository"],
            "workflow_run": run,
        }
        with patch.dict("os.environ", {"QA_VERIFIER_APP_ID": "80"}):
            verdict = core.verify_main(event, self.github)
            self.assertIsInstance(verdict, core.MainVerdict)
            self.assertEqual(verdict.record["version"], 4)
            self.assertEqual(list(verdict.record["gates"].values()).count("REUSED"), 1)
            self.assertEqual(list(verdict.record["gates"].values()).count("PASS"), 22)
            with self.assertRaises(ValueError):
                core.parse_proof(core.encode_proof(verdict).encode())
            for change in ("source", "before", "app"):
                with self.subTest(change=change):
                    saved = copy.deepcopy(jobs[4]["steps"])
                    if change == "source":
                        jobs[1]["steps"][3]["name"] = (
                            "Reuse isolated gate 999:1:1:" + "0" * 64
                        )
                    elif change == "before":
                        jobs[1]["steps"][3]["name"] = (
                            "Reuse isolated gate " + hosted.source_text(self.proof)
                        )
                        jobs[4]["steps"][0]["name"] = (
                            hosted.PUSH_PREFIX + HEAD + " " + AFTER
                        )
                    else:
                        self.check["app"]["id"] = 81
                    self.assertIsInstance(
                        core.verify_main(event, self.github), core.Reject
                    )
                    jobs[4]["steps"] = saved


class LookupFallbackTests(unittest.TestCase):
    def test_missing_provider_configuration_yields_empty_source_and_full_fallback(self):
        import os
        import subprocess
        import sys
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            result = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    str(ROOT / "scripts/qa_provenance_hosted.py"),
                    "lookup",
                    "--before",
                    BASE,
                    "--commit",
                    AFTER,
                ],
                cwd=ROOT,
                env={"PATH": os.environ["PATH"], "GITHUB_OUTPUT": str(output)},
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(output.read_text(), "source=\n")
            self.assertIn("execute all full gates", result.stdout)
            self.assertNotIn("[REUSED]", result.stdout)
