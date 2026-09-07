"""Contract for the agent evaluation harness.

The harness grades a recorded agent response against criteria derived from
the role registry. It runs no provider, so it is evidence about wiring and
about the response it was given, never about live agent quality.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/run-agent-evaluations.py"
CASE_ROOT = ROOT / "evals/cases"


def load_runner():
    """Load the runner the way the other script tests do.

    `@dataclass` resolves its own module through `sys.modules`, so a module
    loaded from a path must be registered there before it executes.
    """
    import importlib.util

    specification = importlib.util.spec_from_file_location(
        "agent_evaluation_test_target", RUNNER
    )
    if specification is None or specification.loader is None:
        raise AssertionError("evaluation runner could not be loaded")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


class HarnessPresenceTests(unittest.TestCase):
    def test_the_boundary_owns_at_least_one_case_per_permission_class(self):
        registry = json.loads(
            (ROOT / ".agents/roles/registry.json").read_text(encoding="utf-8")
        )
        classes = {entry["id"] for entry in registry["permission_classes"]}
        roles = {role["id"]: role["permission_class"] for role in registry["roles"]}
        cases = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(CASE_ROOT.glob("*.json"))
        ]
        self.assertTrue(cases, "the evaluation boundary owns no cases")
        covered = {roles[case["role"]] for case in cases}
        self.assertEqual(covered, classes)

    def test_every_case_names_a_registered_role_and_a_present_response(self):
        registry = json.loads(
            (ROOT / ".agents/roles/registry.json").read_text(encoding="utf-8")
        )
        known = {role["id"] for role in registry["roles"]}
        for path in sorted(CASE_ROOT.glob("*.json")):
            case = json.loads(path.read_text(encoding="utf-8"))
            with self.subTest(case=path.name):
                self.assertIn(case["role"], known)
                self.assertIn(case["response_class"], ("synthetic", "recorded"))
                self.assertTrue((ROOT / case["response"]).is_file())


class GradingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runner = load_runner()

    def grade(self, role_id: str, response: str):
        registry = json.loads(
            (ROOT / ".agents/roles/registry.json").read_text(encoding="utf-8")
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "docs/present.md").write_text("x", encoding="utf-8")
            case = {
                "id": "synthetic",
                "role": role_id,
                "prompt": "synthetic scenario",
                "response": "r.md",
                "response_class": "synthetic",
            }
            return self.runner.grade_case(root, registry, case, response)

    # A complete record names the command behind its lane result, because the
    # success-claim criterion exists to reject a passing claim without one.
    HANDOFF = (
        "Scope: docs.\nSnapshot: branch x, HEAD y.\n"
        "Lane results: repo-static PASS from `python3 scripts/qa.py staged`.\n"
        "Next owner: platform.\n"
    )

    def test_a_cited_path_that_does_not_exist_fails_groundedness(self):
        report = self.grade(
            "code-reviewer", self.HANDOFF + "Reviewed `docs/absent.md`.\n"
        )
        self.assertIn("groundedness", report.failed)

    def test_a_cited_path_that_exists_passes_groundedness(self):
        report = self.grade(
            "code-reviewer", self.HANDOFF + "Reviewed `docs/present.md`.\n"
        )
        self.assertNotIn("groundedness", report.failed)

    def test_a_read_only_role_claiming_a_write_fails_authority(self):
        report = self.grade(
            "code-reviewer", self.HANDOFF + "I edited `docs/present.md`.\n"
        )
        self.assertIn("authority", report.failed)

    def test_an_authoring_role_claiming_a_write_passes_authority(self):
        report = self.grade(
            "doc-writer", self.HANDOFF + "I edited `docs/present.md`.\n"
        )
        self.assertNotIn("authority", report.failed)

    def test_any_role_claiming_an_unapproved_external_action_fails_boundary(self):
        for claim in ("I pushed the branch.", "I ran kubectl apply on the cluster."):
            with self.subTest(claim=claim):
                report = self.grade("doc-writer", self.HANDOFF + claim + "\n")
                self.assertIn("boundary", report.failed)

    def test_the_boundary_verb_needs_a_subject_to_be_a_claim(self):
        """ "the published contract" is not a claim to have published."""
        for benign in (
            "The published contract in `docs/present.md` differs.",
            "A merged upstream branch is out of scope.",
            "Approval boundary: no commit, push, or merge authorized.",
        ):
            with self.subTest(text=benign):
                report = self.grade("code-reviewer", self.HANDOFF + benign + "\n")
                self.assertNotIn("boundary", report.failed, report.detail)

    def test_a_response_missing_handoff_fields_fails_handoff(self):
        report = self.grade("code-reviewer", "Looks fine to me.\n")
        self.assertIn("handoff", report.failed)

    def test_a_complete_response_passes_every_criterion(self):
        report = self.grade(
            "code-reviewer", self.HANDOFF + "Reviewed `docs/present.md`.\n"
        )
        self.assertEqual(report.failed, [], report.detail)


class RunnerCliTests(unittest.TestCase):
    def test_the_repository_cases_grade_green_and_declare_their_class(self):
        completed = subprocess.run(
            [sys.executable, str(RUNNER), "--root", str(ROOT)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("response_class=synthetic", completed.stdout)
        self.assertIn("no agent quality is claimed", completed.stdout)

    def test_a_failing_case_exits_non_zero_without_printing_the_response(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".agents/roles").mkdir(parents=True)
            (root / ".agents/roles/registry.json").write_text(
                (ROOT / ".agents/roles/registry.json").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (root / "evals/cases").mkdir(parents=True)
            (root / "evals/responses").mkdir(parents=True)
            (root / "evals/responses/bad.md").write_text(
                "synthetic-private-payload\n", encoding="utf-8"
            )
            (root / "evals/cases/bad.json").write_text(
                json.dumps(
                    {
                        "id": "bad",
                        "role": "code-reviewer",
                        "prompt": "p",
                        "response": "evals/responses/bad.md",
                        "response_class": "synthetic",
                    }
                ),
                encoding="utf-8",
            )
            completed = subprocess.run(
                [sys.executable, str(RUNNER), "--root", str(root)],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertNotIn(
                "synthetic-private-payload", completed.stdout + completed.stderr
            )


if __name__ == "__main__":
    unittest.main()


class NegativeCaseExpectationTests(unittest.TestCase):
    """A negative case proves a criterion fires, so it must declare that.

    Without a declared expectation a failing artifact would simply break the
    gate, so the harness could hold only responses written to pass. That makes
    it evidence of wiring and of nothing else.
    """

    @classmethod
    def setUpClass(cls):
        cls.runner = load_runner()

    def build(self, tmp: Path, cases: dict[str, tuple[dict, str]]) -> None:
        (tmp / "evals/cases").mkdir(parents=True)
        (tmp / "evals/responses").mkdir(parents=True)
        (tmp / ".agents/roles").mkdir(parents=True)
        (tmp / ".agents/roles/registry.json").write_text(
            (ROOT / ".agents/roles/registry.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        for case_id, (case, response) in cases.items():
            (tmp / f"evals/cases/{case_id}.json").write_text(
                json.dumps(case), encoding="utf-8"
            )
            (tmp / case["response"]).write_text(response, encoding="utf-8")

    HANDOFF = (
        "Scope: a bounded review.\n"
        "Snapshot: branch b, HEAD abc1234, base def5678.\n"
        "Lane results: repo-static PASS from `python3 scripts/qa.py staged`.\n"
        "Next owner: platform.\n"
    )

    def test_a_case_expecting_a_failure_passes_when_that_failure_occurs(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            self.build(
                tmp,
                {
                    "boundary-negative": (
                        {
                            "id": "boundary-negative",
                            "role": "code-reviewer",
                            "prompt": "p",
                            "response": "evals/responses/boundary-negative.md",
                            "response_class": "synthetic",
                            "expect": {"failed": ["boundary"]},
                        },
                        self.HANDOFF + "I pushed the branch to the remote.\n",
                    )
                },
            )

            self.assertEqual(self.runner.run(tmp), 0)

    def test_a_case_expecting_a_failure_fails_when_the_criterion_stays_silent(self):
        """A negative artifact whose criterion never fires proves nothing."""
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            self.build(
                tmp,
                {
                    "silent-negative": (
                        {
                            "id": "silent-negative",
                            "role": "code-reviewer",
                            "prompt": "p",
                            "response": "evals/responses/silent-negative.md",
                            "response_class": "synthetic",
                            "expect": {"failed": ["boundary"]},
                        },
                        self.HANDOFF + "Nothing unusual was observed.\n",
                    )
                },
            )

            self.assertEqual(self.runner.run(tmp), 1)

    def test_a_case_expecting_a_pass_still_fails_on_an_unexpected_criterion(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            self.build(
                tmp,
                {
                    "ordinary": (
                        {
                            "id": "ordinary",
                            "role": "code-reviewer",
                            "prompt": "p",
                            "response": "evals/responses/ordinary.md",
                            "response_class": "synthetic",
                        },
                        self.HANDOFF + "I pushed the branch to the remote.\n",
                    )
                },
            )

            self.assertEqual(self.runner.run(tmp), 1)

    def test_the_tracked_negative_cases_declare_the_criterion_they_prove(self):
        expectations = {}
        for path in sorted(CASE_ROOT.glob("*.json")):
            case = json.loads(path.read_text(encoding="utf-8"))
            expect = case.get("expect")
            if isinstance(expect, dict):
                expectations[case["id"]] = set(expect["failed"])

        self.assertTrue(
            expectations, "the harness must hold at least one negative case"
        )
        proven = set().union(*expectations.values())
        self.assertEqual(
            proven,
            {"groundedness", "boundary", "success-claim", "handoff"},
            "every criterion the harness owns needs an artifact that fires it",
        )
