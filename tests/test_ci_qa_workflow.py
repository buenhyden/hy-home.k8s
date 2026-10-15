"""Independent execution boundaries for hosted branch metadata."""

from pathlib import Path
import os
import subprocess
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


class CiQaWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.workflow = yaml.safe_load((ROOT / ".github/workflows/ci.yml").read_text())

    def test_pr_title_edit_rechecks_required_metadata_job(self):
        events = self.workflow.get("on", self.workflow.get(True))
        self.assertEqual(
            events["pull_request"],
            {
                "branches": ["main"],
                "types": ["opened", "synchronize", "reopened", "edited"],
            },
        )

    def test_summary_uses_event_metadata_and_enforces_branch_policy(self):
        step = self.workflow["jobs"]["ci-summary"]["steps"][0]
        cases = (
            ("pull_request", "main", "feat/topic", "refs/pull/1/merge", 0, "PASS"),
            ("pull_request", "main", "codex/topic", "refs/pull/1/merge", 0, "PASS"),
            ("pull_request", "main", "claude/topic", "refs/pull/1/merge", 0, "PASS"),
            (
                "pull_request",
                "main",
                "dependabot/topic",
                "refs/pull/1/merge",
                0,
                "PASS",
            ),
            ("pull_request", "develop", "feat/topic", "refs/pull/1/merge", 1, "FAIL"),
            ("pull_request", "main", "other/topic", "refs/pull/1/merge", 1, "FAIL"),
            ("pull_request", "main", "", "refs/pull/1/merge", 1, "FAIL"),
            ("push", "", "", "refs/heads/main", 0, "NOT_APPLICABLE"),
            ("workflow_dispatch", "", "", "refs/heads/main", 0, "NOT_APPLICABLE"),
            ("push", "", "", "refs/heads/feat/topic", 1, "FAIL"),
            ("workflow_dispatch", "", "", "refs/heads/feat/topic", 1, "FAIL"),
            ("unknown", "", "", "refs/heads/main", 1, "FAIL"),
        )
        for event, base, head, ref, expected_code, verdict in cases:
            with self.subTest(event=event, base=base, head=head, ref=ref):
                result = subprocess.run(
                    ["/bin/bash", "-c", step["run"]],
                    env={
                        "EVENT_NAME": event,
                        "BASE_REF": base,
                        "HEAD_REF": head,
                        "SOURCE_REF": ref,
                    },
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                self.assertEqual(result.returncode, expected_code, result.stderr)
                self.assertIn(f"verdict={verdict}", result.stdout)
        for missing in ("EVENT_NAME", "BASE_REF", "HEAD_REF", "SOURCE_REF"):
            with self.subTest(missing=missing):
                env = {
                    "EVENT_NAME": "pull_request",
                    "BASE_REF": "main",
                    "HEAD_REF": "feat/topic",
                    "SOURCE_REF": "refs/pull/1/merge",
                }
                del env[missing]
                result = subprocess.run(
                    ["/bin/bash", "-c", step["run"]],
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                self.assertNotEqual(result.returncode, 0)

    def test_manifest_validator_rejects_missing_and_empty_roots(self):
        script = ROOT / "scripts/validate-k8s-manifests.sh"
        with tempfile.TemporaryDirectory(prefix="manifest-presence-") as directory:
            root = Path(directory)
            (root / "gitops").mkdir()
            missing = subprocess.run(
                ["bash", str(script), str(root)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("missing infrastructure/", missing.stderr)
            (root / "infrastructure").mkdir()
            empty = subprocess.run(
                ["bash", str(script), str(root)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertNotEqual(empty.returncode, 0)
            self.assertIn("no YAML manifests matched", empty.stderr)

    def test_pr_title_reads_only_checked_out_base_schema(self):
        steps = self.workflow["jobs"]["ci-summary"]["steps"]
        self.assertEqual(len(steps), 5)
        checkout, candidate_checkout, setup_python, title_check = steps[1:]
        self.assertEqual(checkout["if"], "github.event_name == 'pull_request'")
        self.assertEqual(
            checkout["with"]["ref"], "${{ github.event.pull_request.base.sha }}"
        )
        self.assertFalse(checkout["with"]["persist-credentials"])
        self.assertEqual(candidate_checkout["with"]["path"], "candidate-commits")
        self.assertEqual(candidate_checkout["with"]["fetch-depth"], 0)
        self.assertFalse(candidate_checkout["with"]["persist-credentials"])
        self.assertEqual(setup_python["if"], "github.event_name == 'pull_request'")
        self.assertEqual(title_check["if"], "github.event_name == 'pull_request'")
        self.assertEqual(
            title_check["env"]["PR_TITLE"], "${{ github.event.pull_request.title }}"
        )

        with tempfile.TemporaryDirectory(prefix="pr-title-boundary-") as directory:
            root = Path(directory)
            trusted = root / "trusted-base"
            candidate = root / "candidate-commits"
            candidate.mkdir()
            git_env = {
                **os.environ,
                "GIT_AUTHOR_NAME": "Test",
                "GIT_AUTHOR_EMAIL": "test@example.invalid",
                "GIT_COMMITTER_NAME": "Test",
                "GIT_COMMITTER_EMAIL": "test@example.invalid",
            }

            def git(*args, cwd=candidate, input=None):
                return (
                    subprocess.run(
                        ["git", *args],
                        cwd=cwd,
                        env=git_env,
                        input=input,
                        capture_output=True,
                        check=True,
                        timeout=10,
                    )
                    .stdout.decode()
                    .strip()
                )

            git("init", "-q")
            (candidate / ".cz.toml").write_text(
                (ROOT / ".cz.toml").read_text(encoding="utf-8"), encoding="utf-8"
            )
            git("add", ".cz.toml")
            git("commit", "-q", "-m", "docs: base")
            base_sha = git("rev-parse", "HEAD")
            git("clone", "-q", str(candidate), str(trusted), cwd=root)
            (candidate / ".cz.toml").write_text(
                '[tool.commitizen.customize]\nschema_pattern = ".*"\n', encoding="utf-8"
            )
            git("add", ".cz.toml")
            git("commit", "-q", "-m", "fix: valid change")
            head_sha = git("rev-parse", "HEAD")

            def merge_for(head):
                tree = git("rev-parse", f"{head}^{{tree}}")
                return git(
                    "commit-tree",
                    tree,
                    "-p",
                    base_sha,
                    "-p",
                    head,
                    input=b"Merge pull request #1 from feat/topic\n",
                )

            merge_sha = merge_for(head_sha)
            git("checkout", "-q", "--detach", merge_sha)
            common_env = {
                "BASE_SHA": base_sha,
                "HEAD_SHA": head_sha,
                "MERGE_SHA": merge_sha,
                "PATH": os.environ["PATH"],
            }

            def run(title="docs: title", **overrides):
                return subprocess.run(
                    ["/bin/bash", "-c", title_check["run"]],
                    cwd=root,
                    env={**common_env, "PR_TITLE": title, **overrides},
                    capture_output=True,
                    text=True,
                    timeout=15,
                )

            cases = (
                ("docs: 문장.", 0),
                ("DOCS: Subject.", 0),
                ("fix!: compatible marker", 0),
                ("Merge pull request #1 from evil/topic", 1),
                ('Revert "old"\n\nThis reverts commit ' + base_sha + ".", 1),
                ("docs: ", 1),
                ("docs: anything\nextra", 1),
            )
            for title, expected in cases:
                with self.subTest(title=title):
                    result = run(title)
                    self.assertEqual(result.returncode, expected, result.stderr)

            marker = root / "should-not-run"
            injected_title = f"docs: $(touch {marker})"
            result = run(injected_title)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(marker.exists())

            for key in ("BASE_SHA", "HEAD_SHA", "MERGE_SHA"):
                with self.subTest(mismatch=key):
                    self.assertNotEqual(run(**{key: "b" * 40}).returncode, 0)

            git("checkout", "-q", "--detach", base_sha)
            git("commit", "-q", "--allow-empty", "-m", "docs: side branch")
            side_sha = git("rev-parse", "HEAD")
            tree = git("rev-parse", f"{head_sha}^{{tree}}")
            generated_head = git(
                "commit-tree",
                tree,
                "-p",
                head_sha,
                "-p",
                side_sha,
                input=b"Merge branch 'side' into feat/topic\n",
            )
            generated_merge = merge_for(generated_head)
            git("checkout", "-q", "--detach", generated_merge)
            self.assertEqual(
                run(HEAD_SHA=generated_head, MERGE_SHA=generated_merge).returncode, 0
            )

            empty_merge = merge_for(base_sha)
            git("checkout", "-q", "--detach", empty_merge)
            self.assertNotEqual(
                run(HEAD_SHA=base_sha, MERGE_SHA=empty_merge).returncode, 0
            )

            oversized_head = git(
                "commit-tree",
                tree,
                "-p",
                head_sha,
                input=b"fix: oversized\n\n" + b"x" * 65536 + b"\n",
            )
            oversized_merge = merge_for(oversized_head)
            git("checkout", "-q", "--detach", oversized_merge)
            self.assertNotEqual(
                run(HEAD_SHA=oversized_head, MERGE_SHA=oversized_merge).returncode, 0
            )

            git("checkout", "-q", "--detach", head_sha)
            git("commit", "-q", "--allow-empty", "-m", "bad middle subject")
            git("commit", "-q", "--allow-empty", "-m", "fix: valid tip")
            bad_head = git("rev-parse", "HEAD")
            bad_merge = merge_for(bad_head)
            git("checkout", "-q", "--detach", bad_merge)
            self.assertNotEqual(
                run(HEAD_SHA=bad_head, MERGE_SHA=bad_merge).returncode, 0
            )

            git("checkout", "-q", "--detach", base_sha)
            git(
                "commit",
                "-q",
                "--allow-empty",
                "-m",
                "Merge pull request #2 from feat/forged",
            )
            forged_head = git("rev-parse", "HEAD")
            forged_merge = merge_for(forged_head)
            git("checkout", "-q", "--detach", forged_merge)
            self.assertNotEqual(
                run(HEAD_SHA=forged_head, MERGE_SHA=forged_merge).returncode, 0
            )

            git("checkout", "-q", "--detach", base_sha)
            git(
                "commit",
                "-q",
                "--allow-empty",
                "--cleanup=verbatim",
                "-m",
                "fix: trailing space ",
            )
            spaced_head = git("rev-parse", "HEAD")
            spaced_merge = merge_for(spaced_head)
            git("checkout", "-q", "--detach", spaced_merge)
            self.assertNotEqual(
                run(HEAD_SHA=spaced_head, MERGE_SHA=spaced_merge).returncode, 0
            )

            (trusted / ".cz.toml").unlink()
            (trusted / ".cz.toml").symlink_to(candidate / ".cz.toml")
            self.assertNotEqual(run().returncode, 0)


if __name__ == "__main__":
    unittest.main()
