from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPOSITORY_ROOT / "scripts"
VALIDATOR_PATHS = {
    "registry": SCRIPTS_ROOT / "validate-document-contract-registry.py",
    "lifecycle": SCRIPTS_ROOT / "validate-document-lifecycle.py",
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
REGISTRY_CASES = (
    REPOSITORY_ROOT
    / "tests"
    / "fixtures"
    / "document-contracts"
    / "registry-cases.json"
)
NATIVE_SURFACE_CASES = (
    REPOSITORY_ROOT
    / "tests"
    / "fixtures"
    / "document-contracts"
    / "native-surface-cases.json"
)
WORK105_BASE_COMMIT = "a6fa1806364ea0472baaad0906e1b5e4ddac8602"


def _staged_bytes(path: Path) -> bytes:
    relative = path.relative_to(REPOSITORY_ROOT).as_posix()
    return subprocess.run(
        ["git", "show", f":{relative}"],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
    ).stdout


def _work105_base_bytes(path: Path) -> bytes:
    relative = path.relative_to(REPOSITORY_ROOT).as_posix()
    return subprocess.run(
        ["git", "show", f"{WORK105_BASE_COMMIT}:{relative}"],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
    ).stdout


def _staged_blob_inventory(prefix: str) -> dict[str, tuple[str, str]]:
    result = subprocess.run(
        ["git", "ls-files", "--stage", "-z", "--", prefix],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
    )
    inventory: dict[str, tuple[str, str]] = {}
    for record in result.stdout.split(b"\0")[:-1]:
        header, raw_path = record.split(b"\t", 1)
        mode, object_id, stage = header.split(b" ", 2)
        path = raw_path.decode("utf-8")
        if mode not in {b"100644", b"100755"} or stage != b"0" or path in inventory:
            raise AssertionError("staged inventory is not unique regular stage zero")
        inventory[path] = (mode.decode("ascii"), object_id.decode("ascii"))
    return inventory


def _base_blob_inventory(prefix: str) -> dict[str, tuple[str, str]]:
    result = subprocess.run(
        ["git", "ls-tree", "-r", "-z", WORK105_BASE_COMMIT, "--", prefix],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
    )
    inventory: dict[str, tuple[str, str]] = {}
    for record in result.stdout.split(b"\0")[:-1]:
        header, raw_path = record.split(b"\t", 1)
        mode, object_type, object_id = header.split(b" ", 2)
        path = raw_path.decode("utf-8")
        if (
            mode not in {b"100644", b"100755"}
            or object_type != b"blob"
            or path in inventory
        ):
            raise AssertionError("base inventory is not unique regular blobs")
        inventory[path] = (mode.decode("ascii"), object_id.decode("ascii"))
    return inventory


def _worktree_regular_paths(prefix: str) -> set[str]:
    root = REPOSITORY_ROOT / prefix
    if not root.is_dir() or root.is_symlink():
        raise AssertionError("worktree protected root is not a regular directory")
    result: set[str] = set()
    for path in root.rglob("*"):
        if path.is_symlink():
            raise AssertionError("worktree protected tree contains a symlink")
        if path.is_file():
            result.add(path.relative_to(REPOSITORY_ROOT).as_posix())
    return result


def _assert_staged_and_worktree_bytes(
    path: Path,
    expected: bytes,
    *,
    staged_bytes: bytes | None = None,
    worktree_bytes: bytes | None = None,
) -> None:
    candidate = _staged_bytes(path) if staged_bytes is None else staged_bytes
    working = path.read_bytes() if worktree_bytes is None else worktree_bytes
    if candidate != expected:
        raise AssertionError(f"staged bytes differ from base: {path}")
    if working != expected:
        raise AssertionError(f"worktree bytes differ from base: {path}")
EXPECTED_AD_CORPUS = (
    ("0004", "argo-rollouts-progressive-delivery", "active"),
    ("0005", "argo-notifications-slack", "active"),
    ("0006", "workspace-agent-governance-platform", "active"),
    ("0007", "current-local-gitops-platform", "active"),
    ("0008", "workspace-document-assurance-operating-model", "accepted"),
    ("0009", "document-lifecycle-evidence-operating-model", "accepted"),
    ("0010", "repository-delivery-evidence-architecture", "active"),
    ("0011", "document-taxonomy-consolidation-architecture", "active"),
)
NATIVE_TEMPLATE_SHA256 = {
    "openapi.template.yaml": "aba7ee08fd3c45e63edbc0557911c86ea8b31a47f9afbc3016d2439c65ed1176",
    "schema.template.graphql": "cd6d8b531799d3fd617fe404b441f80c5ab7dc2893bd8519c5ad053c3037dd4a",
    "service.template.proto": "b601274f4a078e14350e0d3694ad846544b266293d04764f68ac8decc7bca4b8",
}


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

    def test_gemini_role_markdown_is_an_exact_approved_provider_surface(self) -> None:
        contracts = sys.modules["document_contracts"]
        approved = contracts.PurePosixPath(".gemini/agents/doc-writer.md")
        self.assertTrue(contracts._is_target_markdown(approved))
        for rejected in (
            ".gemini/README.md",
            ".gemini/agents/nested/doc-writer.md",
            ".gemini/agents/doc-writer.txt",
            ".gemini/settings.md",
        ):
            with self.subTest(rejected=rejected):
                self.assertFalse(
                    contracts._is_target_markdown(contracts.PurePosixPath(rejected))
                )

        commands = (
            (
                "registry",
                "--mode",
                "strict",
                "--route-state",
                "transition",
                "--include-path",
                approved.as_posix(),
            ),
            (
                "markdown",
                "--mode",
                "strict",
                "--include-path",
                approved.as_posix(),
            ),
        )
        for name, *arguments in commands:
            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATHS[name]), *arguments],
                cwd=REPOSITORY_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            with self.subTest(validator=name):
                self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def test_registry_rejects_route_state_mismatch(self) -> None:
        registry = self.validators["registry"].load_registry(REPOSITORY_ROOT)
        with self.assertRaisesRegex(AssertionError, "route state differs"):
            self.validators["registry"]._assert_route_state(
                REPOSITORY_ROOT, registry, "terminal"
            )

    def test_transition_compares_manifest_declared_source_commit(self) -> None:
        validator = self.validators["registry"]
        registry = validator.load_registry(REPOSITORY_ROOT)
        fake_tool = mock.Mock()
        fake_tool.EXPECTED_SOURCE_COMMIT = "a" * 40
        fake_tool.load_manifest_document.return_value.source_commit = "b" * 40
        fake_tool.load_manifest_document.return_value.entries = ()
        with (
            mock.patch.object(validator, "_load_migration_tool", return_value=fake_tool),
            self.assertRaisesRegex(AssertionError, "source commit"),
        ):
            validator._assert_route_state(REPOSITORY_ROOT, registry, "transition")

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
                        "expectedMarkdownForms": 29,
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

    def test_work105_exact_ad_corpus_preserves_identity_slug_state_and_defers_ids(
        self,
    ) -> None:
        architecture_inventory = _staged_blob_inventory("docs/02.architecture")
        self.assertFalse(
            any(
                path.startswith("docs/02.architecture/requirements/")
                for path in architecture_inventory
            )
        )
        expected_paths = {
            "docs/02.architecture/descriptions/"
            f"ad-{identifier}-{slug}.md"
            for identifier, slug, _ in EXPECTED_AD_CORPUS
        }
        actual_paths = {
            path
            for path in architecture_inventory
            if re.fullmatch(
                r"docs/02\.architecture/descriptions/ad-[0-9]{4}-[^/]+\.md",
                path,
            )
        }
        self.assertEqual(actual_paths, expected_paths)
        for identifier, slug, status in EXPECTED_AD_CORPUS:
            relative = (
                "docs/02.architecture/descriptions/"
                f"ad-{identifier}-{slug}.md"
            )
            text = _staged_bytes(REPOSITORY_ROOT / relative).decode("utf-8")
            with self.subTest(path=relative):
                self.assertIn("type: sdlc/ad\n", text)
                self.assertIn(f"status: {status}\n", text)
                self.assertIn("Architecture Description", text.split("---", 2)[1])
                self.assertRegex(text, r"(?m)^# .*Architecture Description(?: \(AD\))?$")
                self.assertRegex(
                    text, rf'(?m)^artifact_id: "AD-{identifier}"$'
                )

    def test_work105_terminal_core_forms_and_retired_authored_routes(self) -> None:
        registry = json.loads(
            _staged_bytes(
                REPOSITORY_ROOT
                / "docs/99.templates/support/document-profiles.json"
            )
        )
        profiles = registry["profiles"]
        profile_ids = {profile["id"] for profile in profiles}
        self.assertEqual(len(profile_ids), 69)
        self.assertTrue(
            {
                "sdlc/prd",
                "sdlc/srs",
                "sdlc/interface",
                "sdlc/ad",
                "sdlc/adr",
                "template/sdlc/prd",
                "template/sdlc/srs",
                "template/sdlc/interface",
                "template/sdlc/ad",
                "template/sdlc/adr",
            }
            <= profile_ids
        )
        self.assertTrue(
            {
                "sdlc/ard",
                "sdlc/rfc",
                "sdlc/api-spec",
                "template/sdlc/ard",
                "template/sdlc/rfc",
                "template/sdlc/api-spec",
            }.isdisjoint(profile_ids)
        )
        for path in (
            "docs/02.architecture/requirements/0004-retired.md",
            "docs/02.architecture/requirements/rfc-0004-retired.md",
            "docs/03.specs/999-retired/api-spec.md",
        ):
            with self.subTest(path=path):
                matches = []
                for profile in profiles:
                    for route in profile["routes"]:
                        if (
                            route["kind"] == "exact" and route["value"] == path
                        ) or (
                            route["kind"] == "regex"
                            and re.fullmatch(route["value"], path) is not None
                        ):
                            matches.append(profile["id"])
                self.assertEqual(matches, [])

        expected_templates = {
            "docs/99.templates/templates/sdlc/requirements/prd.template.md",
            "docs/99.templates/templates/sdlc/requirements/srs.template.md",
            "docs/99.templates/templates/sdlc/requirements/interface.template.md",
            "docs/99.templates/templates/sdlc/architecture/ad.template.md",
            "docs/99.templates/templates/sdlc/architecture/adr.template.md",
        }
        template_inventory = _staged_blob_inventory(
            "docs/99.templates/templates/sdlc"
        )
        self.assertTrue(expected_templates <= set(template_inventory))
        self.assertNotIn(
            "docs/99.templates/templates/sdlc/architecture/ard.template.md",
            template_inventory,
        )
        self.assertNotIn(
            "docs/99.templates/templates/sdlc/specs/api-spec.template.md",
            template_inventory,
        )

    def test_work105_program_lineage_and_authority_gate_are_atomic(self) -> None:
        registry = json.loads(
            _staged_bytes(
                REPOSITORY_ROOT
                / "docs/99.templates/support/document-profiles.json"
            )
        )
        programs = registry["programLineage"]["programs"]
        self.assertEqual(len(programs), 5)
        self.assertTrue(all("ad" in program and "ard" not in program for program in programs))
        prd008 = next(program for program in programs if program["prd"] == "008")
        self.assertEqual(prd008["ad"], "0011")
        self.assertEqual(prd008["tranches"], [
            {
                "spec": "052",
                "order": 1,
                "state": "active",
                "reason": "Document taxonomy consolidation",
                "decision": "0024",
            }
        ])
        adr0024 = _staged_bytes(
            REPOSITORY_ROOT
            / "docs/02.architecture/decisions/0024-terminal-artifact-identity-and-archive-layout.md"
        ).decode("utf-8")
        self.assertIn("status: accepted\n", adr0024)
        ad0011 = _staged_bytes(
            REPOSITORY_ROOT
            / "docs/02.architecture/descriptions/ad-0011-document-taxonomy-consolidation-architecture.md"
        ).decode("utf-8")
        self.assertIn("93-row", ad0011)
        self.assertIn("payload", ad0011)
        self.assertIn("legacy envelope", ad0011.lower())
        self.assertIn('artifact_id: "AD-0011"', ad0011)

    def test_work105_consumer_disposition_is_pinned_complete_and_closed(self) -> None:
        fixture = json.loads(_staged_bytes(REGISTRY_CASES))
        disposition = fixture["work105ConsumerDisposition"]
        self.assertEqual(
            disposition["baseCommit"],
            "a6fa1806364ea0472baaad0906e1b5e4ddac8602",  # pragma: allowlist secret
        )
        self.assertEqual(
            [pattern["id"] for pattern in disposition["patterns"]],
            ["ard", "authored-api-spec"],
        )
        self.assertRegex(disposition["censusSha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(len(disposition["records"]), 2092)
        for record in disposition["records"]:
            self.assertEqual(
                set(record),
                {
                    "patternId",
                    "path",
                    "line",
                    "matchedLineSha256",
                    "occurrenceCount",
                    "consumerClass",
                    "disposition",
                    "target",
                    "reason",
                },
            )
            self.assertRegex(record["matchedLineSha256"], r"^[0-9a-f]{64}$")
            self.assertGreater(record["line"], 0)
            self.assertGreater(record["occurrenceCount"], 0)
            self.assertIn(
                record["disposition"],
                {
                    "migrate-current",
                    "retired-route-negative",
                    "retain-history",
                    "retain-native",
                },
            )
        self.assertEqual(
            disposition["postState"],
            {
                "ard": {"live": 0, "unclassified": 0},
                "authoredApiSpec": {
                    "instances": 0,
                    "live": 0,
                    "unclassified": 0,
                },
            },
        )

    def test_work105_consumer_census_covers_semantic_legacy_vocabulary(self) -> None:
        validator = self.validators["registry"]
        fixture = json.loads(_staged_bytes(REGISTRY_CASES))
        disposition = fixture["work105ConsumerDisposition"]
        ard_pattern = next(
            pattern["regex"]
            for pattern in disposition["patterns"]
            if pattern["id"] == "ard"
        )
        expression = re.compile(ard_pattern)
        for value in ("ARD", "ARD-0004", "ard_id", '"ard"'):
            with self.subTest(value=value):
                self.assertIsNotNone(expression.search(value))
        generated = validator._work105_base_consumer_records(
            REPOSITORY_ROOT,
            validator.WORK105_CONSUMER_PATTERNS,
        )
        self.assertEqual(len(generated), 2092)
        self.assertEqual(
            len({(record["path"], record["line"]) for record in generated}),
            2092,
        )
        self.assertEqual(
            sum("ard" in record["patternId"].split("+") for record in generated),
            1864,
        )
        self.assertEqual(
            sum(
                "authored-api-spec" in record["patternId"].split("+")
                for record in generated
            ),
            235,
        )
        self.assertEqual(
            sum("+" in record["patternId"] for record in generated),
            7,
        )

    def test_work105_consumer_post_state_reads_only_staged_index_blobs(self) -> None:
        validator = self.validators["registry"]
        with tempfile.TemporaryDirectory(prefix="work105-staged-index-") as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            path = root / "consumer.md"
            path.write_text("# Current AD consumer\n", encoding="utf-8")
            subprocess.run(["git", "add", "consumer.md"], cwd=root, check=True)
            path.write_text("# Current sdlc/ard consumer\n", encoding="utf-8")
            self.assertEqual(
                validator._work105_post_state(root, validator.WORK105_CONSUMER_PATTERNS)[
                    "ard"
                ],
                {"live": 0, "unclassified": 0},
            )
            subprocess.run(["git", "add", "consumer.md"], cwd=root, check=True)
            path.write_text("# Current AD consumer\n", encoding="utf-8")
            self.assertEqual(
                validator._work105_post_state(root, validator.WORK105_CONSUMER_PATTERNS)[
                    "ard"
                ],
                {"live": 1, "unclassified": 0},
            )

    def test_work105_staged_blob_reader_is_streamed_bounded_and_redacted(self) -> None:
        validator = self.validators["registry"]
        object_id = b"a" * 40
        second_id = b"b" * 40
        inventory = b"100644 " + object_id + b" 0\tconsumer.md\0"
        self.assertEqual(
            validator._work105_parse_staged_inventory(
                inventory, entry_limit=1, path_byte_limit=32
            ),
            (("consumer.md", object_id),),
        )
        for name, candidate, entry_limit, path_limit in (
            (
                "count",
                inventory + b"100644 " + second_id + b" 0\tsecond.md\0",
                1,
                32,
            ),
            (
                "path",
                b"100644 " + object_id + b" 0\tSECRET-PATH-SENTINEL\0",
                1,
                4,
            ),
        ):
            with self.subTest(name=name), self.assertRaises(AssertionError) as failure:
                validator._work105_parse_staged_inventory(
                    candidate,
                    entry_limit=entry_limit,
                    path_byte_limit=path_limit,
                )
            self.assertNotIn("SECRET-PATH-SENTINEL", str(failure.exception))

        payload = b"SECRET-PAYLOAD-SENTINEL"
        response = (
            object_id + f" blob {len(payload)}\n".encode("ascii") + payload + b"\n"
        )
        self.assertEqual(
            validator._work105_read_blob_batch_protocol(
                io.BytesIO(response),
                (object_id,),
                per_blob_limit=len(payload),
                aggregate_limit=len(payload),
                object_limit=1,
            ),
            {object_id: payload},
        )
        resource_cases = (
            ("object-count", response, (object_id, second_id), 1, 100, 200),
            ("per-blob", response, (object_id,), 1, len(payload) - 1, 200),
            (
                "aggregate",
                response
                + second_id
                + f" blob {len(payload)}\n".encode("ascii")
                + payload
                + b"\n",
                (object_id, second_id),
                2,
                len(payload),
                len(payload),
            ),
        )
        for name, raw, object_ids, object_limit, per_blob, aggregate in resource_cases:
            with self.subTest(name=name), self.assertRaises(AssertionError) as failure:
                validator._work105_read_blob_batch_protocol(
                    io.BytesIO(raw),
                    object_ids,
                    per_blob_limit=per_blob,
                    aggregate_limit=aggregate,
                    object_limit=object_limit,
                )
            self.assertNotIn(payload.decode("ascii"), str(failure.exception))
            self.assertNotIn(object_id.decode("ascii"), str(failure.exception))

        protocol_cases = {
            "truncated-header": object_id + b" blob",
            "truncated-body": object_id + b" blob 5\nabc",
            "wrong-kind": object_id + b" tree 0\n\n",
            "trailing": object_id + b" blob 0\n\nEXTRA-SENTINEL",
        }
        for name, raw in protocol_cases.items():
            with self.subTest(name=name), self.assertRaises(AssertionError) as failure:
                validator._work105_read_blob_batch_protocol(
                    io.BytesIO(raw), (object_id,)
                )
            self.assertNotIn("EXTRA-SENTINEL", str(failure.exception))
            self.assertNotIn(object_id.decode("ascii"), str(failure.exception))

        with tempfile.TemporaryDirectory(prefix="work105-streamed-index-") as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / "consumer.md").write_text("# Current AD consumer\n", encoding="utf-8")
            subprocess.run(["git", "add", "consumer.md"], cwd=root, check=True)
            original_run = validator.subprocess.run

            def reject_captured_cat_file(arguments, *args, **kwargs):
                if list(arguments[:3]) == ["git", "cat-file", "--batch"]:
                    raise AssertionError("cat-file must use the streaming reader")
                return original_run(arguments, *args, **kwargs)

            with mock.patch.object(
                validator.subprocess, "run", side_effect=reject_captured_cat_file
            ):
                self.assertEqual(
                    validator._work105_staged_blobs(root),
                    (("consumer.md", b"# Current AD consumer\n"),),
                )

    def test_work105_occurrence_classifier_does_not_mask_mixed_lines(self) -> None:
        validator = self.validators["registry"]
        patterns = {item["id"]: item for item in validator.WORK105_CONSUMER_PATTERNS}
        ard_line = '{"history":"historical ARD","current":"sdlc/ard"}'
        api_line = (
            '{"native":"OpenAPI Specification","current":"sdlc/api-spec"}'
        )
        self.assertEqual(
            [
                item[1]
                for item in validator._work105_occurrence_dispositions(
                    patterns["ard"], "consumer.json", ard_line
                )
            ],
            ["retain-history", "migrate-current"],
        )
        self.assertEqual(
            [
                item[1]
                for item in validator._work105_occurrence_dispositions(
                    patterns["authored-api-spec"], "consumer.json", api_line
                )
            ],
            ["retain-native", "migrate-current"],
        )
        ambiguous = "historical ARD remains current sdlc/ard"
        self.assertEqual(
            validator._work105_occurrence_dispositions(
                patterns["ard"], "consumer.md", ambiguous
            ),
            (None, None),
        )
        self.assertEqual(
            [
                item[1]
                for item in validator._work105_occurrence_dispositions(
                    patterns["ard"],
                    "tests/test_document_strict_cutover.py",
                    ambiguous,
                    semantic_context=f"ambiguous = {ambiguous}",
                )
            ],
            ["retired-route-negative", "retired-route-negative"],
        )
        current_before_history = (
            "Active "
            + "AR"
            + "D-0006 is current. ADR-0013 is a historical predecessor."
        )
        self.assertEqual(
            [
                item[1]
                for item in validator._work105_occurrence_dispositions(
                    patterns["ard"], "consumer.md", current_before_history
                )
            ],
            ["migrate-current"],
        )
        classifier_control = (
            "complete "
            + "AR"
            + "D classifier with migrate-current/retain-history evidence"
        )
        self.assertEqual(
            [
                item[1]
                for item in validator._work105_occurrence_dispositions(
                    patterns["ard"],
                    (
                        "docs/03.specs/052-document-taxonomy-consolidation/"
                        "spec.md"
                    ),
                    classifier_control,
                )
            ],
            ["retired-route-negative"],
        )
        code_line = 'must not route sdlc/ard; ACTIVE_ROUTE = "sdlc/ard"'
        self.assertEqual(
            [
                item[1] if item is not None else None
                for item in validator._work105_occurrence_dispositions(
                    patterns["ard"], "scripts/current.py", code_line
                )
            ],
            ["retired-route-negative", "migrate-current"],
        )
        self.assertEqual(
            validator._work105_consumer_disposition(
                "ard",
                "tests/test_active_corpus_retention.py",
                "programArd",
                line_context='self.assertNotIn("programArd", row)',
            )[1],
            "retired-route-negative",
        )
        with self.assertRaises(AssertionError):
            validator._work105_consumer_disposition(
                "ard", "consumer.json", "no WORK-105 token is present"
            )
        self.assertEqual(
            validator._work105_consumer_disposition(
                "ard",
                "tests/test_document_strict_cutover.py",
                "ard",
                line_context=", ".join(
                    ("ard", "consumer.json", "no WORK-105 token is present")
                ),
            )[1],
            "retired-route-negative",
        )

        graph_line = validator._work105_pinned_blob(
            REPOSITORY_ROOT, "graphify-out/graph.html"
        ).decode("utf-8").splitlines()[68]
        graph_dispositions = [
            item[1]
            for pattern in patterns.values()
            for item in validator._work105_occurrence_dispositions(
                pattern, "graphify-out/graph.html", graph_line
            )
        ]
        self.assertEqual(len(graph_dispositions), 224)
        self.assertIn("migrate-current", graph_dispositions)
        self.assertIn("retain-history", graph_dispositions)
        self.assertIn("retain-native", graph_dispositions)

        with tempfile.TemporaryDirectory(prefix="work105-mixed-line-") as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            mixed = root / "consumer.json"
            mixed.write_text(ard_line + "\n", encoding="utf-8")
            subprocess.run(["git", "add", mixed.name], cwd=root, check=True)
            self.assertEqual(
                validator._work105_post_state(root, validator.WORK105_CONSUMER_PATTERNS)[
                    "ard"
                ],
                {"live": 1, "unclassified": 0},
            )

    def test_work105_decision_evidence_exception_is_exact_and_fail_closed(self) -> None:
        validator = self.validators["lifecycle"]
        fixture = json.loads(_staged_bytes(REPOSITORY_ROOT / validator.FIXTURE_PATH))
        cases = fixture["work105DecisionEvidenceCases"]
        self.assertEqual(len(cases), 10)
        for case in cases:
            with self.subTest(name=case["name"]):
                inputs = validator._work105_decision_evidence_fixture_inputs(
                    REPOSITORY_ROOT, case["mutation"]
                )
                actual = validator._work105_predecessor_unresolved_links(**inputs)
                self.assertEqual(len(actual), case["expectedUnresolvedCount"])

    def test_work105_consumer_disposition_is_semantic_not_file_wide(self) -> None:
        validator = self.validators["registry"]
        self.assertEqual(
            validator._work105_consumer_disposition(
                "ard",
                "tests/test_document_strict_cutover.py",
                "A" + "RD is still the current authoring form",
            )[1],
            "migrate-current",
        )
        self.assertEqual(
            validator._work105_consumer_disposition(
                "ard",
                "docs/00.agent-governance/memory/progress.md",
                "Completed migration retained historical ARD evidence.",
            )[1],
            "retain-history",
        )

    def test_work105_wiki_generator_transition_control_is_exact(self) -> None:
        validator = self.validators["registry"]
        generator_path = REPOSITORY_ROOT / "scripts/generate-llm-wiki-index.sh"
        candidate = _staged_bytes(generator_path).decode("utf-8")
        control_lines = validator._work105_generator_transition_control_lines(
            candidate
        )
        base_assignment = validator.WORK105_WIKI_GENERATOR_BASE_ROW_ASSIGNMENT
        base_line_number = candidate.splitlines().index(base_assignment) + 1
        self.assertEqual(control_lines, frozenset({base_line_number}))

        dispositions = validator._work105_occurrence_dispositions(
            validator.WORK105_CONSUMER_PATTERNS[0],
            "scripts/generate-llm-wiki-index.sh",
            base_assignment,
            semantic_context=base_assignment,
            generator_transition_control=True,
        )
        self.assertEqual(
            [item[1] for item in dispositions if item is not None],
            ["retired-route-negative", "retired-route-negative"],
        )

        for reviewed_literal in validator.WORK105_WIKI_GENERATOR_REVIEWED_LITERALS:
            with self.subTest(reviewed_literal=reviewed_literal):
                mutated = candidate.replace(
                    reviewed_literal, f"MUTATED{reviewed_literal[1:]}", 1
                )
                self.assertEqual(
                    validator._work105_generator_transition_control_lines(mutated),
                    frozenset(),
                )

        pinned = validator._work105_pinned_blob(
            REPOSITORY_ROOT, "scripts/generate-llm-wiki-index.sh"
        ).decode("utf-8")
        self.assertEqual(
            validator._work105_generator_transition_control_lines(pinned),
            frozenset(),
        )
        pinned_row = next(
            line
            for line in pinned.splitlines()
            if "AR" "D-style architecture requirement index" in line
        )
        self.assertEqual(
            [
                item[1]
                for item in validator._work105_occurrence_dispositions(
                    validator.WORK105_CONSUMER_PATTERNS[0],
                    "scripts/generate-llm-wiki-index.sh",
                    pinned_row,
                )
                if item is not None
            ],
            ["migrate-current", "migrate-current"],
        )

    def test_work105_semantic_provenance_and_append_only_progress_are_preserved(self) -> None:
        progress_path = REPOSITORY_ROOT / "docs/00.agent-governance/memory/progress.md"
        self.assertTrue(_staged_bytes(progress_path).startswith(_work105_base_bytes(progress_path)))
        prd = _staged_bytes(
            REPOSITORY_ROOT
            / "docs/01.requirements/008-workspace-document-taxonomy-consolidation.md"
        ).decode("utf-8")
        spec = _staged_bytes(
            REPOSITORY_ROOT
            / "docs/03.specs/052-document-taxonomy-consolidation/spec.md"
        ).decode("utf-8")
        adr = _staged_bytes(
            REPOSITORY_ROOT
            / "docs/02.architecture/decisions/0024-terminal-artifact-identity-and-archive-layout.md"
        ).decode("utf-8")
        self.assertIn("legacy ARD consumers", prd)
        self.assertIn("unconverted current ARD", spec)
        self.assertIn("Source ARD", adr)
        self.assertIn("Terminal AD", adr)

    def test_work105_preserves_stage98_manifest_paths(self) -> None:
        manifest = _staged_bytes(
            REPOSITORY_ROOT / "scripts/archive_cutover_manifest.py"
        ).decode("utf-8")
        for identifier, slug in (
            ("0001", "wsl-k3d-argocd-platform"),
            ("0002", "wsl2-k3d-argocd-ha-platform"),
            ("0003", "platform-expansion-mesh-dashboard"),
        ):
            self.assertIn(
                f'docs/98.archive/02.architecture/requirements/{identifier}-{slug}.md',
                manifest,
            )
        self.assertNotIn("docs/98.archive/02.architecture/descriptions/", manifest)

    def test_work105_interface_requirement_route_is_ifc_everywhere(self) -> None:
        surfaces = (
            REPOSITORY_ROOT / "docs/00.agent-governance/hooks/k8s-pre-edit.sh",
            REPOSITORY_ROOT
            / "docs/00.agent-governance/rules/documentation-protocol.md",
            REPOSITORY_ROOT / "scripts/validate-document-lifecycle.py",
            REPOSITORY_ROOT / "scripts/validate-repo-quality-gates.sh",
            REPOSITORY_ROOT / "tests/fixtures/markdown-profiles.json",
        )
        for path in surfaces:
            text = _staged_bytes(path).decode("utf-8")
            with self.subTest(path=path.relative_to(REPOSITORY_ROOT).as_posix()):
                self.assertNotRegex(text, r"(?:^|[/\"'`])interface-(?:<|[0-9])")
        self.assertIn(
            'basename.startswith("ifc-")',
            _staged_bytes(surfaces[0]).decode("utf-8"),
        )

    def test_work105_completed_spec019_history_is_byte_exact(self) -> None:
        validator = self.validators["registry"]
        for relative in (
            "docs/03.specs/019-template-path-numbering-contract/spec.md",
            "docs/03.specs/019-template-path-numbering-contract/plan.md",
        ):
            path = REPOSITORY_ROOT / relative
            with self.subTest(path=relative):
                self.assertEqual(
                    validator._work108_without_outer_artifact_id(
                        relative, _staged_bytes(path)
                    ),
                    _work105_base_bytes(path),
                )

    def test_work105_stage98_invariant_blocks_105_106_and_gates_107_plus(self) -> None:
        ad0011_path = (
            REPOSITORY_ROOT
            / "docs/02.architecture/descriptions/ad-0011-document-taxonomy-consolidation-architecture.md"
        )
        ad0011 = _staged_bytes(ad0011_path).decode("utf-8")
        self.assertIn("WORK-105 and WORK-106 change no Stage 98 path or byte", ad0011)
        self.assertIn("WORK-105 acceptance", ad0011)
        self.assertIn("green WORK-106", ad0011)
        self.assertIn("WORK-107 only", ad0011)
        self.assertIn("WORK-108 and later", ad0011)
        self.assertIn("outer record location and terminal wrapper identity", ad0011)

    def test_work105_native_contract_bytes_and_ten_cases_are_preserved(self) -> None:
        native_fixture = _staged_bytes(NATIVE_SURFACE_CASES)
        self.assertEqual(
            hashlib.sha256(native_fixture).hexdigest(),
            "31d0d392e80a6151275282a76c220757222b61f3cf96afa63cd454592232056a",  # pragma: allowlist secret
        )
        fixture = json.loads(native_fixture)
        self.assertEqual(len(fixture["families"]), 5)
        self.assertEqual(
            sum(
                key in family
                for family in fixture["families"]
                for key in ("positiveSource", "negativeSource")
            ),
            10,
        )
        native_root = REPOSITORY_ROOT / "docs/99.templates/templates/sdlc/specs"
        for name, expected_sha256 in NATIVE_TEMPLATE_SHA256.items():
            with self.subTest(template=name):
                self.assertEqual(
                    hashlib.sha256(_staged_bytes(native_root / name)).hexdigest(),
                    expected_sha256,
                )

    def test_work107_stage98_rehome_is_exact_93_to_93(self) -> None:
        from scripts.archive_recovery import (
            WORK107_MIGRATION_PATH,
            parse_work107_migration_document,
            validate_work107_migration_rows,
        )

        result = subprocess.run(
            ["git", "rev-parse", f"{WORK105_BASE_COMMIT}:docs/98.archive"],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.stdout.strip(),
            "71b9e6f1394ab3805d887a50ba548a3221d11762",  # pragma: allowlist secret
        )
        base_inventory = _base_blob_inventory("docs/98.archive")
        staged_inventory = _staged_blob_inventory("docs/98.archive")
        migration_path = REPOSITORY_ROOT / WORK107_MIGRATION_PATH
        rows = validate_work107_migration_rows(
            REPOSITORY_ROOT,
            parse_work107_migration_document(_staged_bytes(migration_path)),
        )
        legacy_paths = {str(row["legacy_path"]) for row in rows}
        stable_paths = {str(row["stable_path"]) for row in rows}
        self.assertEqual(len(legacy_paths), 93)
        self.assertEqual(len(stable_paths), 93)
        self.assertEqual(
            set(base_inventory),
            legacy_paths | {"docs/98.archive/README.md"},
        )
        expected_current = stable_paths | {
            "docs/98.archive/README.md",
            WORK107_MIGRATION_PATH,
        }
        self.assertEqual(set(staged_inventory), expected_current)
        self.assertEqual(
            _worktree_regular_paths("docs/98.archive"), expected_current
        )
        self.assertFalse(legacy_paths & set(staged_inventory))
        for relative in expected_current:
            path = REPOSITORY_ROOT / relative
            with self.subTest(path=relative):
                self.assertEqual(_staged_bytes(path), path.read_bytes())

    def test_work105_stage98_partial_index_worktree_divergence_is_rejected(
        self,
    ) -> None:
        path = REPOSITORY_ROOT / "docs/98.archive/README.md"
        expected = _work105_base_bytes(path)
        with self.assertRaisesRegex(AssertionError, "staged"):
            _assert_staged_and_worktree_bytes(
                path,
                expected,
                staged_bytes=expected + b"staged divergence",
                worktree_bytes=expected,
            )
        with self.assertRaisesRegex(AssertionError, "worktree"):
            _assert_staged_and_worktree_bytes(
                path,
                expected,
                staged_bytes=expected,
                worktree_bytes=expected + b"worktree divergence",
            )

    def test_work106_path_derived_artifact_identity_fixture(self) -> None:
        validator = self.validators["registry"]
        fixture = json.loads(_staged_bytes(REGISTRY_CASES))
        cases = fixture["work106ArtifactIdentityCases"]
        self.assertEqual(len(cases), 20)
        for case in cases:
            with self.subTest(path=case["path"]):
                actual = validator._work106_derive_artifact_identity(case["path"])
                self.assertEqual(actual.artifact_id, case["artifactId"])
                self.assertEqual(actual.change_id, case.get("changeId"))
                self.assertEqual(actual.migration_id, case.get("migrationId"))

        for invalid in (
            "docs/01.requirements/ifc-09-bad.md",
            "docs/01.requirements/ifc-009-Bad.md",
            "docs/01.requirements/ifc-009-double--hyphen.md",
            "docs/02.architecture/descriptions/ad-011-short.md",
            "docs/03.specs/52-short/spec.md",
            "docs/98.archive/changes/chg-0001-bad/nested/plan.md",
            "docs/98.archive/tombstones/02.architecture/tmb-ar" + "d-0011.md",
        ):
            with self.subTest(invalid=invalid):
                self.assertIsNone(validator._work106_derive_artifact_identity(invalid))

    def test_work106_artifact_namespace_is_transition_aware_and_global(self) -> None:
        validator = self.validators["registry"]
        records = (
            ("docs/01.requirements/008-program.md", {}),
            ("docs/02.architecture/descriptions/ad-0011-program.md", {"artifact_id": "AD-0011"}),
            (
                "docs/90.references/current.md",
                {"original_artifact_id": "AR" + "D-0011"},
            ),
        )
        self.assertEqual(validator._work106_artifact_diagnostics(records, terminal=False), ())
        self.assertIn(
            "ARTIFACT-ID-MISSING:docs/01.requirements/008-program.md",
            validator._work106_artifact_diagnostics(records, terminal=True),
        )

        mutations = (
            (("docs/01.requirements/008-program.md", {"artifact_id": "PRD-009"}), "ARTIFACT-ID-PATH"),
            (("docs/90.references/current.md", {"artifact_id": "PRD-008"}), "ARTIFACT-ID-PROHIBITED"),
            (("docs/01.requirements/009-second.md", {"artifact_id": "PRD-008"}), "ARTIFACT-ID-PATH"),
        )
        for record, expected in mutations:
            with self.subTest(expected=expected):
                diagnostics = validator._work106_artifact_diagnostics(
                    (records[1], record), terminal=False
                )
                self.assertTrue(any(item.startswith(expected) for item in diagnostics))

        duplicate = (
            ("docs/01.requirements/008-program.md", {"artifact_id": "PRD-008"}),
            ("docs/01.requirements/008-alias.md", {"artifact_id": "PRD-008"}),
        )
        self.assertTrue(
            any(
                item.startswith("ARTIFACT-ID-DUPLICATE")
                for item in validator._work106_artifact_diagnostics(duplicate, terminal=False)
            )
        )

    def test_work106_tombstone_legacy_hash_is_canonical_and_full(self) -> None:
        validator = self.validators["registry"]
        legacy_path = "docs/04.execution/tasks/2026-07-05-audit-pack.md"
        source_blob = "a" * 40
        token = validator._work106_legacy_tombstone_token(legacy_path, source_blob)
        self.assertRegex(token, r"^LEGACY-[A-F0-9]{64}$")
        self.assertEqual(
            token,
            validator._work106_legacy_tombstone_token(legacy_path, source_blob),
        )
        for invalid in ("/absolute.md", "docs//bad.md", "docs/../bad.md", "./docs/bad.md"):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    validator._work106_legacy_tombstone_token(invalid, source_blob)
        self.assertEqual(
            validator._work106_tombstone_artifact_id(
                "02.architecture", "AD", "AR" + "D-0011", legacy_path, source_blob
            ),
            "TMB-AD-0011",
        )
        self.assertEqual(
            validator._work106_tombstone_artifact_id(
                "02.architecture", "AD", None, legacy_path, source_blob
            ),
            "TMB-AD-" + token,
        )
        with self.assertRaises(ValueError):
            validator._work106_tombstone_artifact_id(
                "02.architecture", "API-SPEC", None, legacy_path, source_blob
            )

    def test_work106_stable_leaf_group_metadata_is_mandatory_during_transition(self) -> None:
        validator = self.validators["registry"]
        plan_path = "docs/98.archive/changes/chg-0001-bootstrap/plan.md"
        migration_path = "docs/98.archive/migrations/mig-0001-convergence.md"
        valid = (
            (plan_path, {"artifact_id": "PLAN-CHG-0001", "change_id": "CHG-0001"}),
            (migration_path, {"artifact_id": "MIG-0001", "migration_id": "MIG-0001"}),
        )
        self.assertEqual(
            validator._work106_artifact_diagnostics(valid, terminal=False), ()
        )
        for path, metadata, expected in (
            (plan_path, {"artifact_id": "PLAN-CHG-0001"}, "ARTIFACT-CHANGE-ID"),
            (migration_path, {"artifact_id": "MIG-0001"}, "ARTIFACT-MIGRATION-ID"),
        ):
            with self.subTest(expected=expected):
                diagnostics = validator._work106_artifact_diagnostics(
                    ((path, metadata),), terminal=False
                )
                self.assertTrue(any(item.startswith(expected) for item in diagnostics))

    def test_work108_terminal_artifact_identity_census_is_exact_and_complete(self) -> None:
        validator = self.validators["registry"]
        registry = json.loads(
            _staged_bytes(REPOSITORY_ROOT / validator.REGISTRY_PATH)
        )
        profiles = {profile["id"]: profile for profile in registry["profiles"]}
        self.assertEqual(
            set(validator.WORK108_MANDATORY_PROFILE_IDS),
            {
                profile_id
                for profile_id, profile in profiles.items()
                if "artifact_id" in profile["frontmatter"]["required"]
            },
        )
        self.assertEqual(
            set(validator.WORK108_MANDATORY_PROFILE_IDS),
            {
                profile_id
                for profile_id, profile in profiles.items()
                if "artifact_id" in profile["frontmatter"]["allowed"]
                or "artifact_id" in profile["frontmatter"]["order"]
            },
        )
        for source_id in validator.WORK108_MANDATORY_PROFILE_IDS:
            template_id = f"template/{source_id}"
            with self.subTest(source_id=source_id):
                self.assertIn("artifact_id", profiles[source_id]["frontmatter"]["allowed"])
                self.assertIn("artifact_id", profiles[source_id]["frontmatter"]["order"])
                self.assertNotIn(
                    "artifact_id", profiles[template_id]["frontmatter"]["required"]
                )
                self.assertNotIn(
                    "artifact_id", profiles[template_id]["frontmatter"]["allowed"]
                )
                self.assertNotIn(
                    "artifact_id", profiles[template_id]["frontmatter"]["order"]
                )
        records = tuple(
            (path, validator._work106_frontmatter(raw))
            for path, raw in validator._work105_staged_blobs(REPOSITORY_ROOT)
            if path.endswith(".md")
        )
        identities = tuple(
            (path, identity)
            for path, _ in records
            if (identity := validator._work106_derive_artifact_identity(path))
            is not None
        )
        self.assertEqual(len(identities), 286)
        self.assertEqual(
            validator._work106_artifact_diagnostics(records, terminal=True), ()
        )

        tombstone_path = next(
            path
            for path, _ in records
            if path.startswith(
                "docs/98.archive/tombstones/01.requirements/tmb-prd-legacy-"
            )
        )
        tombstone = validator._work106_derive_artifact_identity(tombstone_path)
        self.assertIsNotNone(tombstone)
        self.assertRegex(tombstone.artifact_id, r"^TMB-PRD-LEGACY-[A-F0-9]{64}$")

        base = (
            b"---\n"
            b"title: Example\n"
            b"type: sdlc/adr\n"
            b"status: accepted\n"
            b"owner: platform\n"
            b"updated: 2026-08-12\n"
            b"---\n\n# Example\n"
        )
        current = base.replace(
            b"updated: 2026-08-12\n",
            b"updated: 2026-08-12\nartifact_id: \"ADR-0024\"\n",
        )
        path = (
            "docs/02.architecture/decisions/"
            "0024-terminal-artifact-identity-and-archive-layout.md"
        )
        self.assertEqual(
            validator._work108_without_outer_artifact_id(path, current), base
        )
        for invalid in (
            current.replace(b"ADR-0024", b"ADR-0023"),
            current.replace(
                b"artifact_id: \"ADR-0024\"\n",
                b"artifact_id: \"ADR-0024\"\nartifact_id: \"ADR-0024\"\n",
            ),
            current.replace(
                b"updated: 2026-08-12\nartifact_id: \"ADR-0024\"\n",
                b"artifact_id: \"ADR-0024\"\nupdated: 2026-08-12\n",
            ),
        ):
            with self.subTest(invalid=invalid):
                self.assertIsNone(
                    validator._work108_without_outer_artifact_id(path, invalid)
                )

        links = self.validators["links"]
        self.assertEqual(
            links._work108_without_history_artifact_id(
                PurePosixPath(path), current
            ),
            base,
        )
        self.assertIsNone(
            links._work108_without_history_artifact_id(
                PurePosixPath(path), current.replace(b"ADR-0024", b"ADR-0023")
            )
        )

    def test_work106_ledger_fixture_rejects_closed_negative_matrix(self) -> None:
        validator = self.validators["registry"]
        fixture = json.loads(_staged_bytes(REGISTRY_CASES))["work106MigrationLedger"]
        row = fixture["row"]
        self.assertEqual(validator._work106_ledger_diagnostics((row,), current=False), ())
        for mutation in fixture["negativeMutations"]:
            with self.subTest(mutation=mutation):
                rows = validator._work106_mutated_ledger_rows(row, mutation)
                self.assertNotEqual(
                    validator._work106_ledger_diagnostics(rows, current=False), ()
                )

    def test_work106_current_ledger_census_is_exact_93(self) -> None:
        validator = self.validators["registry"]
        rows = validator._work106_synthetic_current_ledger()
        self.assertEqual(len(rows), 93)
        self.assertEqual(validator._work106_ledger_diagnostics(rows, current=True), ())
        wrong = [dict(row) for row in rows]
        wrong[-1]["stable_path"] = wrong[-2]["stable_path"]
        diagnostics = validator._work106_ledger_diagnostics(tuple(wrong), current=True)
        self.assertTrue(any(item.startswith("LEDGER-STABLE-PATH-DUPLICATE") for item in diagnostics))


if __name__ == "__main__":
    unittest.main()
