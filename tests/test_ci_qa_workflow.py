"""Independent execution boundaries for hosted branch metadata."""

from pathlib import Path
import json
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
        self.assertEqual(
            step["env"],
            {
                "EVENT_NAME": "${{ github.event_name }}",
                "BASE_REF": "${{ github.base_ref }}",
                "HEAD_REF": "${{ github.head_ref }}",
                "SOURCE_REF": "${{ github.ref }}",
            },
        )
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
        for missing in step["env"]:
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

    def test_local_full_unit_test_registry_is_retained(self):
        registry = json.loads((ROOT / "scripts/validation/registry.json").read_text())
        unit = next(row for row in registry["validators"] if row["id"] == "unit-tests")
        self.assertIn("ci", unit["lanes"])
        self.assertIn("all-files", unit["lanes"])
        self.assertIn("unittest", str(unit))
        self.assertFalse(unit["optional"])

    def test_pr_template_routes_delivery_evidence_to_quality_policy(self):
        template = (ROOT / ".github/PULL_REQUEST_TEMPLATE.md").read_text()
        self.assertIn(".agents/governance/quality.md", template)
        self.assertNotIn("python3 scripts/qa.py full", template)
        self.assertNotIn("`full` result", template)

    def test_issue_contact_does_not_route_to_disabled_discussions(self):
        config = yaml.safe_load(
            (ROOT / ".github/ISSUE_TEMPLATE/config.yml").read_text()
        )
        self.assertFalse(
            any("/discussions" in link["url"] for link in config["contact_links"])
        )

    def test_dependabot_uses_existing_actions_label(self):
        config = yaml.safe_load((ROOT / ".github/dependabot.yml").read_text())
        actions = next(
            item
            for item in config["updates"]
            if item["package-ecosystem"] == "github-actions"
        )
        self.assertIn("github_actions", actions["labels"])
        self.assertNotIn("github-actions", actions["labels"])

    def test_cluster_paths_use_existing_gitops_label(self):
        labels = yaml.safe_load((ROOT / ".github/labeler.yml").read_text())
        self.assertNotIn("area/cluster", labels)
        self.assertIn("gitops/clusters/**", str(labels["area/gitops"]))

    def test_security_notice_routes_to_private_reporting_ui(self):
        notice = (ROOT / ".github/SECURITY.md").read_text()
        self.assertIn(
            "https://github.com/buenhyden/hy-home.k8s/security/advisories/new", notice
        )

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
