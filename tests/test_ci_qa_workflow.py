"""Independent execution boundaries for the shared QA workflow."""

from pathlib import Path
import json
import re
import subprocess
import tempfile
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

    def _qa_steps(self):
        return self.workflow["jobs"]["qa"]["steps"]

    def test_checkout_is_bound_to_a_named_durable_ref(self):
        """An exact-SHA checkout detaches HEAD; archive retention needs a name.

        The step is executed here rather than pattern-matched, so the contract
        under test is the observable outcome: HEAD becomes symbolic and the
        branch tip is still exactly the commit the event selected.
        """

        steps = self._qa_steps()
        checkout = next(
            index
            for index, step in enumerate(steps)
            if step.get("uses", "").startswith("actions/checkout@")
        )
        binding = [
            step
            for step in steps[checkout + 1 :]
            if "git switch" in step.get("run", "")
        ]
        self.assertEqual(len(binding), 1)

        with tempfile.TemporaryDirectory(prefix="ci-binding-") as temporary:

            def git(*args):
                return subprocess.run(
                    ["git", *args], cwd=temporary, capture_output=True, check=True
                ).stdout.decode()

            git("init", "--quiet")
            git("config", "user.email", "ci-fixture@example.invalid")
            git("config", "user.name", "CI Fixture")
            Path(temporary, "seed.txt").write_text("seed\n", encoding="utf-8")
            git("add", "seed.txt")
            git("commit", "--quiet", "-m", "seed")
            selected = git("rev-parse", "HEAD").strip()
            git("checkout", "--quiet", "--detach", selected)
            self.assertNotEqual(
                subprocess.run(
                    ["git", "symbolic-ref", "-q", "HEAD"],
                    cwd=temporary,
                    capture_output=True,
                ).returncode,
                0,
                "fixture must start detached for this to test anything",
            )

            result = subprocess.run(
                ["/bin/bash", "-c", binding[0]["run"]],
                cwd=temporary,
                capture_output=True,
                timeout=30,
            )

            self.assertEqual(result.returncode, 0, result.stderr.decode())
            self.assertTrue(
                git("symbolic-ref", "HEAD").strip().startswith("refs/heads/")
            )
            self.assertEqual(git("rev-parse", "HEAD").strip(), selected)

    def test_pre_commit_is_published_to_the_validator_search_path(self):
        """Validators use a fixed system path, not the interpreter's bin dir."""

        installs = [
            step.get("run", "")
            for step in self._qa_steps()
            if "/usr/local/bin/pre-commit" in step.get("run", "")
        ]
        self.assertEqual(len(installs), 1)
        self.assertIn("sudo install", installs[0])

    def test_tool_publication_directory_satisfies_the_strict_resolver(self):
        """Publishing a root-owned file into a writable directory is not enough.

        `secure_tool_executable` rejects a candidate whose containing directory
        is group- or other-writable, because anyone holding that write bit can
        swap the executable the validator is about to trust.  A runner image is
        free to ship `/usr/local/bin` writable, so the workflow has to state the
        ownership it needs instead of inheriting whatever the image provides.
        """

        steps = self._qa_steps()
        published = [
            index
            for index, step in enumerate(steps)
            if re.search(r"sudo install\s+[^\n]*/usr/local/bin/\S", step.get("run", ""))
        ]
        self.assertTrue(published, "no tool is published to the search path")

        prepared = [
            (index, step.get("run", ""))
            for index, step in enumerate(steps)
            if re.search(
                r"sudo install\s+-d\b[^\n]*/usr/local/bin\b", step.get("run", "")
            )
        ]
        self.assertEqual(len(prepared), 1, "the directory contract is stated once")
        index, run = prepared[0]
        self.assertLess(
            index,
            min(published),
            "the directory is hardened before anything is published into it",
        )
        self.assertIn("-o root", run)
        self.assertIn("-g root", run)
        mode = re.search(r"-m\s*(\d+)", run)
        self.assertIsNotNone(mode, "the directory mode is stated explicitly")
        self.assertFalse(
            int(mode.group(1), 8) & 0o022,
            "a group- or other-writable directory is rejected by the resolver",
        )

    def test_hook_environments_are_cached_between_runs(self):
        """A cold cache builds every hook toolchain from source."""

        cache = [
            step
            for step in self._qa_steps()
            if step.get("uses", "").startswith("actions/cache@")
        ]
        self.assertEqual(len(cache), 1)
        pinned = cache[0]["uses"].split("@", 1)[1]
        self.assertRegex(pinned, r"^[0-9a-f]{40}$")

        with_ = cache[0]["with"]
        self.assertIn("pre-commit", with_["path"])
        # A key that ignores the hook configuration would restore environments
        # that no longer match the hooks being run.
        self.assertIn(".pre-commit-config.yaml", with_["key"])
        self.assertIn("runner.arch", with_["key"])
        self.assertIn("steps.validation-python.outputs.python-version", with_["key"])
        self.assertIn(".github/requirements/ci-validation.txt", with_["key"])

    def test_job_wall_clock_exceeds_the_slowest_declared_gate_budget(self):
        """A gate budget larger than its job's wall clock can never be reached."""

        registry = json.loads(
            (ROOT / "scripts/validation/registry.json").read_text(encoding="utf-8")
        )
        declared = [
            row["timeoutSeconds"]
            for row in registry["validators"]
            if "timeoutSeconds" in row
        ]
        self.assertTrue(declared)

        job_seconds = self.workflow["jobs"]["qa"]["timeout-minutes"] * 60
        self.assertGreater(job_seconds, max(declared))


if __name__ == "__main__":
    unittest.main()
