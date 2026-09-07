from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = REPOSITORY_ROOT / "scripts" / "prompt-input.py"
PROMPT_ROOT = REPOSITORY_ROOT / ".agents" / "prompts"

FRONTMATTER = (
    "---\n"
    'title: "Sample Contract"\n'
    'version: "0.1.0"\n'
    'type: "governance/prompt"\n'
    'status: "active"\n'
    'owner: "platform"\n'
    'updated: "2026-09-07"\n'
    "---\n\n"
)


def load_builder():
    specification = importlib.util.spec_from_file_location(
        "prompt_input_test_target", BUILDER_PATH
    )
    if specification is None or specification.loader is None:
        raise AssertionError("prompt input builder could not be loaded")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def contract(command: str, subject: str = "Subject") -> str:
    return (
        FRONTMATTER
        + "# Sample Contract\n\n## Overview\n\nIdentifier `sample`.\n\n"
        + "## Authority Boundary\n\nIt grants nothing.\n\n"
        + "## Inputs\n\n"
        + "| Input | Command | Why it is needed |\n"
        + "| --- | --- | --- |\n"
        + f"| {subject} | `{command}` | The subject |\n\n"
        + f"The subject input is `{subject}`. When it is empty the contract refuses.\n\n"
        + "## Output\n\nA draft.\n\n## Validation\n\nReviewed.\n\n"
        + "## Refusal Conditions\n\nEmpty subject.\n\n## Related Documents\n\n- none\n"
    )


class PromptInputBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_builder()
        self._directory = tempfile.TemporaryDirectory(prefix="prompt-input-")
        self.addCleanup(self._directory.cleanup)
        self.root = Path(self._directory.name)
        (self.root / ".agents" / "prompts").mkdir(parents=True)
        subprocess.run(["git", "init", "--quiet"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "config", "user.email", "t@example.invalid"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test"], cwd=self.root, check=True
        )

    def write(self, identifier: str, text: str) -> None:
        (self.root / ".agents" / "prompts" / f"{identifier}.md").write_text(
            text, encoding="utf-8"
        )

    def stage(self, name: str, content: str) -> None:
        (self.root / name).write_text(content, encoding="utf-8")
        subprocess.run(["git", "add", name], cwd=self.root, check=True)

    def test_unknown_identifier_exits_non_zero(self) -> None:
        with self.assertRaises(self.module.PromptInputError) as raised:
            self.module.assemble(self.root, "absent")
        self.assertEqual(raised.exception.code, "PROMPT-UNKNOWN")
        self.assertEqual(raised.exception.status, self.module.EXIT_CONTRACT)

    def test_empty_staged_difference_refuses_without_a_draft(self) -> None:
        self.write("sample", contract("git diff --cached", "Staged difference"))
        with self.assertRaises(self.module.PromptInputError) as raised:
            self.module.assemble(self.root, "sample")
        self.assertEqual(raised.exception.code, "PROMPT-REFUSED")
        self.assertEqual(raised.exception.status, self.module.EXIT_REFUSED)

    def test_staged_difference_is_read_and_the_working_tree_is_not(self) -> None:
        self.write("sample", contract("git diff --cached", "Staged difference"))
        self.stage("staged.txt", "staged marker\n")
        (self.root / "unstaged.txt").write_text("unstaged marker\n", encoding="utf-8")
        assembled = self.module.assemble(self.root, "sample")
        self.assertIn("staged marker", assembled)
        self.assertNotIn("unstaged marker", assembled)

    def test_undeclared_command_is_rejected(self) -> None:
        self.write("sample", contract("git push origin main"))
        with self.assertRaises(self.module.PromptInputError) as raised:
            self.module.assemble(self.root, "sample")
        self.assertEqual(raised.exception.code, "PROMPT-INPUT-FORBIDDEN")

    def test_no_allowed_command_writes_to_the_repository_or_git_state(self) -> None:
        write_verbs = {
            "add",
            "commit",
            "push",
            "checkout",
            "reset",
            "restore",
            "clean",
            "rebase",
            "merge",
            "stash",
            "tag",
            "branch",
            "apply",
            "mv",
            "rm",
        }
        for argv in self.module.ALLOWED_COMMANDS:
            self.assertEqual(argv[0], "git", argv)
            self.assertNotIn(argv[1], write_verbs, argv)

    def test_assembly_leaves_git_state_unchanged(self) -> None:
        self.write("sample", contract("git diff --cached", "Staged difference"))
        self.stage("staged.txt", "staged marker\n")
        before = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        self.module.assemble(self.root, "sample")
        after = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        self.assertEqual(before, after)

    def test_builder_opens_no_network_connection(self) -> None:
        source = BUILDER_PATH.read_text(encoding="utf-8")
        for forbidden in ("socket", "urllib", "http.client", "requests", "urlopen"):
            self.assertNotIn(forbidden, source)


class PromptContractRepositoryTests(unittest.TestCase):
    def test_every_contract_declares_only_allowed_commands(self) -> None:
        module = load_builder()
        contracts = sorted(p for p in PROMPT_ROOT.glob("*.md") if p.name != "README.md")
        self.assertTrue(contracts, "the prompt surface declares no contract")
        for path in contracts:
            text = module.body(path.read_text(encoding="utf-8"))
            declared = module.declared_inputs(text)
            self.assertTrue(declared, path.name)
            subject = module.subject_name(text)
            self.assertIn(subject, [name for name, _ in declared], path.name)

    def test_identifiers_do_not_collide_with_skill_identifiers(self) -> None:
        skills = {
            p.name
            for p in (REPOSITORY_ROOT / ".agents" / "skills").iterdir()
            if p.is_dir()
        }
        identifiers = {
            p.stem for p in PROMPT_ROOT.glob("*.md") if p.name != "README.md"
        }
        self.assertEqual(skills & identifiers, set())

    def test_no_contract_assumes_a_named_base_ref_exists(self) -> None:
        """A base ref is a property of the checkout, not of a contract.

        The isolated snapshot the quality profile builds carries only the
        working branch, so a contract that declared `main..HEAD` failed there
        while passing in the repository. Assert the absence of that assumption
        rather than the symptom."""
        module = load_builder()
        for argv in module.ALLOWED_COMMANDS:
            joined = " ".join(argv)
            for ref in ("main", "master", "origin/"):
                self.assertNotIn(ref, joined, joined)

    def test_builder_runs_in_a_checkout_without_the_default_branch(self) -> None:
        with tempfile.TemporaryDirectory(prefix="prompt-input-noref-") as directory:
            root = Path(directory)
            (root / ".agents" / "prompts").mkdir(parents=True)
            for path in PROMPT_ROOT.glob("*.md"):
                (root / ".agents" / "prompts" / path.name).write_text(
                    path.read_text(encoding="utf-8"), encoding="utf-8"
                )
            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
            subprocess.run(
                ["git", "config", "user.email", "t@example.invalid"],
                cwd=root,
                check=True,
            )
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
            subprocess.run(
                ["git", "checkout", "--quiet", "-b", "work"], cwd=root, check=False
            )
            (root / "seed.txt").write_text("seed\n", encoding="utf-8")
            subprocess.run(["git", "add", "seed.txt"], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "--quiet", "-m", "seed"], cwd=root, check=True
            )
            self.assertNotEqual(
                subprocess.run(
                    ["git", "rev-parse", "--verify", "-q", "main"],
                    cwd=root,
                    capture_output=True,
                ).returncode,
                0,
                "fixture must have no main ref",
            )
            result = subprocess.run(
                [sys.executable, str(BUILDER_PATH), "handoff", "--root", str(root)],
                capture_output=True,
                text=True,
                timeout=120,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_builder_runs_for_a_known_identifier(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(BUILDER_PATH),
                "handoff",
                "--root",
                str(REPOSITORY_ROOT),
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Prompt request: handoff", result.stdout)


if __name__ == "__main__":
    unittest.main()
