"""Independent execution boundaries for the shared QA workflow."""

from pathlib import Path
import subprocess
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


class CiQaWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.workflow = yaml.safe_load((ROOT / ".github/workflows/ci.yml").read_text())

    def test_one_qa_job_owns_setup_and_execution(self):
        jobs = self.workflow["jobs"]
        self.assertEqual(set(jobs), {"branch-policy", "qa", "ci-summary"})
        runs = [step.get("run", "") for job in jobs.values() for step in job["steps"]]
        self.assertEqual(sum("python3 scripts/qa.py ci" in run for run in runs), 1)
        self.assertFalse(
            any("pre-commit run" in run or "unittest discover" in run for run in runs)
        )
        self.assertEqual(
            sum(
                "actions/setup-python@" in step.get("uses", "")
                for job in jobs.values()
                for step in job["steps"]
            ),
            1,
        )
        checkout = [
            s
            for s in jobs["qa"]["steps"]
            if s.get("uses", "").startswith("actions/checkout@")
        ]
        self.assertEqual(len(checkout), 1)
        self.assertEqual(
            checkout[0]["with"],
            {
                "ref": "${{ github.sha }}",
                "persist-credentials": False,
                "fetch-depth": 0,
            },
        )
        self.assertNotIn("if", jobs["qa"])
        self.assertEqual(self.workflow["permissions"], {"contents": "read"})

    def test_summary_fails_closed_for_required_results(self):
        job = self.workflow["jobs"]["ci-summary"]
        self.assertEqual(job["if"], "always()")
        self.assertEqual(set(job["needs"]), {"branch-policy", "qa"})
        script = job["steps"][0]["run"]
        for event, branch in [
            ("pull_request", "success"),
            ("push", "skipped"),
            ("workflow_dispatch", "skipped"),
        ]:
            for qa in ("success", "failure", "cancelled", "skipped", ""):
                with self.subTest(event=event, qa=qa):
                    result = subprocess.run(
                        ["/bin/bash", "-c", script],
                        env={
                            "EVENT_NAME": event,
                            "BRANCH_POLICY_RESULT": branch,
                            "QA_RESULT": qa,
                        },
                        capture_output=True,
                        timeout=5,
                    )
                    self.assertEqual(result.returncode, 0 if qa == "success" else 1)
        for branch in ("failure", "cancelled", "skipped", ""):
            result = subprocess.run(
                ["/bin/bash", "-c", script],
                env={
                    "EVENT_NAME": "pull_request",
                    "BRANCH_POLICY_RESULT": branch,
                    "QA_RESULT": "success",
                },
                capture_output=True,
                timeout=5,
            )
            self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
