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
        self.assertEqual(len(steps), 4)
        checkout, setup_python, title_check = steps[1:]
        self.assertEqual(checkout["if"], "github.event_name == 'pull_request'")
        self.assertEqual(
            checkout["with"]["ref"], "${{ github.event.pull_request.base.sha }}"
        )
        self.assertFalse(checkout["with"]["persist-credentials"])
        self.assertEqual(setup_python["if"], "github.event_name == 'pull_request'")
        self.assertEqual(title_check["if"], "github.event_name == 'pull_request'")
        self.assertEqual(
            title_check["env"]["PR_TITLE"], "${{ github.event.pull_request.title }}"
        )

        with tempfile.TemporaryDirectory(prefix="pr-title-boundary-") as directory:
            root = Path(directory)
            trusted = root / "trusted-base"
            candidate = root / "candidate"
            binary = root / "bin"
            trusted.mkdir()
            candidate.mkdir()
            binary.mkdir()
            (trusted / ".cz.toml").write_text(
                (ROOT / ".cz.toml").read_text(encoding="utf-8"), encoding="utf-8"
            )
            (candidate / ".cz.toml").write_text(
                '[tool.commitizen.customize]\nschema_pattern = ".*"\n',
                encoding="utf-8",
            )
            base_sha = "a" * 40
            git = binary / "git"
            git.write_text(
                f"#!/bin/sh\nprintf '%s\\n' '{base_sha}'\n", encoding="utf-8"
            )
            git.chmod(0o700)
            common_env = {
                "BASE_SHA": base_sha,
                "PATH": f"{binary}:{os.environ['PATH']}",
            }
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
                    result = subprocess.run(
                        ["/bin/bash", "-c", title_check["run"]],
                        cwd=root,
                        env={**common_env, "PR_TITLE": title},
                        capture_output=True,
                        text=True,
                        timeout=5,
                    )
                    self.assertEqual(result.returncode, expected, result.stderr)

            marker = root / "should-not-run"
            injected_title = f"docs: $(touch {marker})"
            result = subprocess.run(
                ["/bin/bash", "-c", title_check["run"]],
                cwd=root,
                env={**common_env, "PR_TITLE": injected_title},
                capture_output=True,
                text=True,
                timeout=5,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(marker.exists())

            result = subprocess.run(
                ["/bin/bash", "-c", title_check["run"]],
                cwd=root,
                env={**common_env, "BASE_SHA": "b" * 40, "PR_TITLE": "docs: title"},
                capture_output=True,
                text=True,
                timeout=5,
            )
            self.assertNotEqual(result.returncode, 0)

            (trusted / ".cz.toml").unlink()
            (trusted / ".cz.toml").symlink_to(candidate / ".cz.toml")
            result = subprocess.run(
                ["/bin/bash", "-c", title_check["run"]],
                cwd=root,
                env={**common_env, "PR_TITLE": "docs: title"},
                capture_output=True,
                text=True,
                timeout=5,
            )
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
