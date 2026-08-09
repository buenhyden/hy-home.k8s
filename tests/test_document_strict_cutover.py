from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import re
import sys
import unittest
from pathlib import Path
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPOSITORY_ROOT / "scripts"
VALIDATOR_PATHS = {
    "registry": SCRIPTS_ROOT / "validate-document-contract-registry.py",
    "markdown": SCRIPTS_ROOT / "validate-markdown-profiles.py",
    "links": SCRIPTS_ROOT / "validate-links-and-owners.py",
}
CURRENT_COMMAND_CONTRACT_DOCS = (
    REPOSITORY_ROOT / "scripts" / "README.md",
    REPOSITORY_ROOT / "tests" / "README.md",
    REPOSITORY_ROOT
    / "docs"
    / "99.templates"
    / "support"
    / "common-documentation-governance.md",
    REPOSITORY_ROOT
    / "docs"
    / "99.templates"
    / "support"
    / "legacy-cleanup-rules.md",
    REPOSITORY_ROOT
    / "docs"
    / "99.templates"
    / "support"
    / "sdlc-governance.md",
    REPOSITORY_ROOT
    / "docs"
    / "99.templates"
    / "support"
    / "template-routing.md",
)
STAGE99_SUPPORT_DOCS = CURRENT_COMMAND_CONTRACT_DOCS[2:]
STAGE99_TEMPLATES_ROOT = REPOSITORY_ROOT / "docs" / "99.templates" / "templates"
STAGE99_SUPPORT_ROOT = REPOSITORY_ROOT / "docs" / "99.templates" / "support"
CURRENT_STAGE99_CONTRACT_SURFACES = tuple(
    sorted(
        {
            STAGE99_SUPPORT_ROOT / "document-profiles.json",
            *(
                path
                for root in (STAGE99_TEMPLATES_ROOT, STAGE99_SUPPORT_ROOT)
                for path in root.rglob("*")
                if path.is_file()
            ),
        }
    )
)
RETIREMENT_GUARD = (
    REPOSITORY_ROOT
    / "tests"
    / "fixtures"
    / "document-contracts"
    / "template-compatibility.json"
)
RETIRED_DEBT_FIXTURE = (
    REPOSITORY_ROOT
    / "tests"
    / "fixtures"
    / "document-contracts"
    / "semantic-compatibility-debt.json"
)


def load_validator(name: str, path: Path):
    scripts_path = str(SCRIPTS_ROOT)
    if scripts_path not in sys.path:
        sys.path.insert(0, scripts_path)
    module_name = f"document_strict_cutover_{name}_validator"
    specification = importlib.util.spec_from_file_location(module_name, path)
    if specification is None or specification.loader is None:
        raise AssertionError(f"{name} validator could not be loaded")
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    specification.loader.exec_module(module)
    return module


class DocumentStrictCutoverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validators = {
            name: load_validator(name, path)
            for name, path in VALIDATOR_PATHS.items()
        }

    def parse(self, name: str, arguments: list[str]):
        validator = self.validators[name]
        if name == "registry":
            with mock.patch.object(
                sys,
                "argv",
                [str(VALIDATOR_PATHS[name]), *arguments],
            ):
                return validator._parse_args()
        return validator._parser().parse_args(arguments)

    def test_validator_mode_defaults_are_strict(self) -> None:
        for name in VALIDATOR_PATHS:
            with self.subTest(validator=name):
                self.assertEqual(self.parse(name, []).mode, "strict")

    def test_registry_route_state_is_explicit_transition(self) -> None:
        args = self.parse("registry", ["--route-state", "transition"])
        self.assertEqual(args.route_state, "transition")
        registry = self.validators["registry"].load_registry(REPOSITORY_ROOT)
        self.assertEqual(registry.route_state, "transition")
        profile = self.validators["registry"].classify_path(
            registry,
            self.validators["registry"].PurePosixPath(
                "scripts/document-taxonomy-migration.json"
            ),
        )
        self.assertEqual(profile.profile_id, "native/document-migration-manifest")

    def test_registry_rejects_route_state_mismatch(self) -> None:
        registry = self.validators["registry"].load_registry(REPOSITORY_ROOT)
        with self.assertRaisesRegex(AssertionError, "route state differs"):
            self.validators["registry"]._assert_route_state(
                REPOSITORY_ROOT, registry, "terminal"
            )

    def test_terminal_retired_route_classification_is_closed(self) -> None:
        validator = self.validators["registry"]
        raw_registry = json.loads(
            (REPOSITORY_ROOT / validator.REGISTRY_PATH).read_text(encoding="utf-8")
        )
        accepted = {
            "docs/90.references/data/active-corpus-migration-results.json": "stage90/immutable-retired-route-evidence",
            "docs/98.archive/04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md": "stage98/immutable-retired-route-evidence",
        }
        for path, expected in accepted.items():
            with self.subTest(path=path):
                self.assertEqual(
                    validator._classify_retired_route_hit(
                        raw_registry, validator.PurePosixPath(path)
                    ),
                    expected,
                )
        for path in (
            "docs/90.references/mutable-note.md",
            "docs/98.archive/non-evidence.md",
            "scripts/current-consumer.py",
        ):
            with self.subTest(path=path):
                self.assertIsNone(
                    validator._classify_retired_route_hit(
                        raw_registry, validator.PurePosixPath(path)
                    )
                )

    def test_terminal_rejects_residual_native_migration_contract(self) -> None:
        validator = self.validators["registry"]
        raw_registry = json.loads(
            (REPOSITORY_ROOT / validator.REGISTRY_PATH).read_text(encoding="utf-8")
        )
        raw_schema = json.loads(
            (REPOSITORY_ROOT / validator.SCHEMA_PATH).read_text(encoding="utf-8")
        )
        diagnostics = validator._terminal_route_contract_diagnostics(
            REPOSITORY_ROOT,
            raw_registry,
            raw_schema,
            (),
        )
        self.assertIn("TERMINAL-MIGRATION-PROFILE", diagnostics)
        self.assertIn("TERMINAL-MIGRATION-SCHEMA", diagnostics)
        self.assertIn("TERMINAL-MIGRATION-FILE", diagnostics)

    def test_compatibility_mode_is_rejected_by_argparse(self) -> None:
        for name in VALIDATOR_PATHS:
            with self.subTest(validator=name):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as raised:
                        self.parse(name, ["--mode", "compatibility"])
                self.assertEqual(raised.exception.code, 2)

    def test_current_command_contracts_do_not_advertise_compatibility_mode(
        self,
    ) -> None:
        compatibility_invocation = re.compile(r"--mode(?:[ =`]+)compatibility\b")
        for path in CURRENT_COMMAND_CONTRACT_DOCS:
            with self.subTest(path=path.relative_to(REPOSITORY_ROOT).as_posix()):
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(compatibility_invocation.search(text))

    def test_current_contracts_do_not_claim_registry_v7(self) -> None:
        closed_v7 = re.compile(r"\bclosed[ -]v7\b", re.IGNORECASE)
        for path in STAGE99_SUPPORT_DOCS:
            with self.subTest(path=path.relative_to(REPOSITORY_ROOT).as_posix()):
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(closed_v7.search(text))

        scripts_readme = (SCRIPTS_ROOT / "README.md").read_text(encoding="utf-8")
        for stale_phrase in (
            "complete literal v7 typed projection",
            "typed registry-v7 program lineage",
        ):
            with self.subTest(path="scripts/README.md", phrase=stale_phrase):
                if stale_phrase in scripts_readme:
                    self.fail(f"stale current-contract phrase: {stale_phrase!r}")

    def test_current_stage99_contracts_do_not_reintroduce_tombstones(self) -> None:
        forbidden_patterns = {
            "content/archive-tombstone": re.compile(
                r"content/archive-tombstone", re.IGNORECASE
            ),
            "archive-tombstone": re.compile(r"archive-tombstone", re.IGNORECASE),
            "Tombstone form/profile": re.compile(
                r"\btombstone\s+(?:form|profile)\b", re.IGNORECASE
            ),
        }
        for path in CURRENT_STAGE99_CONTRACT_SURFACES:
            text = path.read_text(encoding="utf-8")
            relative_path = path.relative_to(REPOSITORY_ROOT).as_posix()
            for contract_name, pattern in forbidden_patterns.items():
                for surface, value in (
                    ("path", relative_path),
                    ("content", text),
                ):
                    with self.subTest(
                        path=relative_path,
                        contract=contract_name,
                        surface=surface,
                    ):
                        self.assertIsNone(pattern.search(value))

    def test_retirement_guard_remains_closed_and_debt_fixture_absent(self) -> None:
        self.assertFalse(RETIRED_DEBT_FIXTURE.exists())
        retirement_guard = json.loads(RETIREMENT_GUARD.read_text(encoding="utf-8"))
        self.assertEqual(
            list(retirement_guard),
            [
                "schemaVersion",
                "owner",
                "growthAllowed",
                "retiredFields",
                "behaviorCases",
            ],
        )
        self.assertEqual(
            retirement_guard,
            {
                "schemaVersion": 2,
                "owner": "Spec 033",
                "growthAllowed": False,
                "retiredFields": [
                    "compatibilityDebt",
                    "semanticDebtCaps",
                ],
                "behaviorCases": [
                    {
                        "name": "registry-derived-form-inventory",
                        "expectedMarkdownForms": 27,
                        "expectedNativeForms": 3,
                    },
                    {
                        "name": "retired-debt-fields-remain-absent",
                        "forbiddenFields": [
                            "compatibilityDebt",
                            "semanticDebtCaps",
                        ],
                    },
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
