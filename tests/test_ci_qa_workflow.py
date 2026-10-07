"""Independent execution boundaries for hosted branch metadata."""

from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


class CiQaWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.workflow = yaml.safe_load((ROOT / ".github/workflows/ci.yml").read_text())

    def test_summary_uses_event_metadata_and_reports_full_qa_not_run(self):
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
                self.assertIn("full-qa result=NOT_RUN verdict=NOT_RUN", result.stdout)
                self.assertNotIn("qa-isolated result=", result.stdout)
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
                self.assertIn("full-qa result=NOT_RUN verdict=NOT_RUN", result.stdout)

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


if __name__ == "__main__":
    unittest.main()
