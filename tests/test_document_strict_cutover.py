from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock

from jsonschema import Draft202012Validator


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
    / "document-contract.md",
    REPOSITORY_ROOT
    / "docs"
    / "99.templates"
    / "support"
    / "document-lifecycle.md",
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
WORK109_BASE_COMMIT = "160ce006969ddb49965c8af193f3e9ee290e18a8"
WORK109_PROSE_OWNERS = (
    "docs/00.agent-governance/rules/document-authoring.md",
    "docs/99.templates/support/document-contract.md",
    "docs/99.templates/support/document-lifecycle.md",
)
WORK109_RETIRED_PROSE_OWNERS = (
    "docs/00.agent-governance/rules/document-stage-routing.md",
    "docs/00.agent-governance/rules/documentation-protocol.md",
    "docs/00.agent-governance/rules/stage-authoring-matrix.md",
    "docs/00.agent-governance/rules/stage-checklists.md",
    "docs/99.templates/support/common-documentation-governance.md",
    "docs/99.templates/support/documentation-contract.md",
    "docs/99.templates/support/frontmatter-schema.md",
    "docs/99.templates/support/legacy-cleanup-rules.md",
    "docs/99.templates/support/sdlc-governance.md",
    "docs/99.templates/support/template-routing.md",
)


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
    relative = {
        "docs/03.specs/0019-template-path-numbering-contract/spec.md": (
            "docs/03.specs/019-template-path-numbering-contract/spec.md"
        ),
        "docs/03.specs/0019-template-path-numbering-contract/plan.md": (
            "docs/03.specs/019-template-path-numbering-contract/plan.md"
        ),
    }.get(relative, relative)
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


def _commit_blob_inventory(
    commit: str, prefix: str
) -> dict[str, tuple[str, str]]:
    result = subprocess.run(
        ["git", "ls-tree", "-r", "-z", commit, "--", prefix],
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
            raise AssertionError("commit inventory is not unique regular blobs")
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


def _replace_mig0002_rows(contents: bytes, rows: list[dict[str, object]]) -> bytes:
    text = contents.decode("utf-8")
    prefix, remainder = text.split("```json", 1)
    _, suffix = remainder.split("```", 1)
    payload = json.dumps(rows, indent=2, ensure_ascii=False)
    return f"{prefix}```json\n{payload}\n```{suffix}".encode("utf-8")


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


def load_document_authority():
    return load_validator("authority", SCRIPTS_ROOT / "document_authority.py")


def terminal_registry_fixture() -> dict[str, object]:
    return {
        "$schema": "./contracts/document-profile.schema.json",
        "$id": "https://hy-home.k8s/docs/99.templates/registry.json",
        "schemaVersion": 9,
        "profiles": [
            {
                "id": "governance/policy",
                "pathPattern": "^docs/00\\.agent-governance/policies/[0-9]{4}-[a-z0-9-]+\\.md$",
                "artifactIdPattern": None,
                "template": "docs/99.templates/templates/governance/policy.template.md",
                "requiredFrontmatter": ["title", "type", "status", "owner", "updated"],
                "requiredSections": ["Overview", "Policy"],
                "lifecycle": {
                    "states": {
                        "draft": "mutable",
                        "active": "current",
                        "superseded": "terminal",
                        "retired": "terminal",
                    },
                    "transitions": {
                        "draft": ["active"],
                        "active": ["superseded", "retired"],
                        "superseded": [],
                        "retired": [],
                    },
                },
                "relationships": {"supersession": "reciprocal"},
            }
        ],
        "programLineage": [],
        "standaloneExecutions": [],
    }


class DocumentAuthorityFoundationTests(unittest.TestCase):
    def test_stage99_support_prose_cannot_be_a_machine_owner(self) -> None:
        authority = load_document_authority()
        registry = terminal_registry_fixture()
        registry["profiles"][0]["pathPattern"] = (
            "^docs/99\\.templates/support/document-contract\\.md$"
        )
        with self.assertRaisesRegex(authority.AuthorityError, "STAGE99_SUPPORT_OWNER"):
            authority.validate_registry_authority(registry)

    def test_stage99_registry_rejects_agent_roster_fields(self) -> None:
        authority = load_document_authority()
        registry = terminal_registry_fixture()
        registry["profiles"][0]["permissions"] = ["write"]
        with self.assertRaisesRegex(authority.AuthorityError, "STAGE99_AGENT_FIELD"):
            authority.validate_registry_authority(registry)

    def test_template_references_a_profile_not_a_destination(self) -> None:
        authority = load_document_authority()
        registry = terminal_registry_fixture()
        with self.assertRaisesRegex(authority.AuthorityError, "TEMPLATE_DESTINATION"):
            authority.validate_template_profile_reference(
                "<!-- destination: docs/00.agent-governance/policies/0001-example.md -->\n",
                registry,
            )

    def test_production_authority_scans_mutated_real_template(self) -> None:
        authority = load_document_authority()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry_path = root / authority.REGISTRY_PATH
            registry_path.parent.mkdir(parents=True)
            shutil.copy2(
                REPOSITORY_ROOT / authority.REGISTRY_PATH,
                registry_path,
            )
            shutil.copytree(
                STAGE99_TEMPLATES_ROOT,
                root / "docs/99.templates/templates",
            )
            template = (
                root
                / "docs/99.templates/templates/sdlc/specs/spec.template.md"
            )
            template.write_text(
                "<!-- destination: docs/03.specs/9999-example/spec.md -->\n"
                + template.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                result = authority.main(["--root", str(root)])
            self.assertEqual(result, 1)
            self.assertIn("TEMPLATE_DESTINATION", stderr.getvalue())

    def test_touched_lifecycle_validator_has_no_production_self_test_switch(self) -> None:
        source = VALIDATOR_PATHS["lifecycle"].read_text(encoding="utf-8")
        self.assertNotIn('add_argument("--self-test"', source)
        self.assertNotIn("def _run_self_test(", source)

    def test_registry_reader_is_bounded_and_strict_utf8(self) -> None:
        authority = load_document_authority()
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "registry.json"
            candidate.write_bytes(b"\xff")
            with self.assertRaisesRegex(authority.AuthorityError, "AUTHORITY_UTF8"):
                authority.read_bounded_utf8(candidate, max_bytes=16)
            candidate.write_bytes(b"x" * 17)
            with self.assertRaisesRegex(authority.AuthorityError, "AUTHORITY_SIZE"):
                authority.read_bounded_utf8(candidate, max_bytes=16)

    def test_router_profiles_omit_artifact_and_lifecycle_fields(self) -> None:
        registry = json.loads(
            (REPOSITORY_ROOT / "docs/99.templates/registry.json").read_text(
                encoding="utf-8"
            )
        )
        schema = json.loads(
            (
                REPOSITORY_ROOT
                / "docs/99.templates/contracts/document-profile.schema.json"
            ).read_text(encoding="utf-8")
        )
        errors = sorted(
            Draft202012Validator(schema).iter_errors(registry),
            key=lambda error: list(error.absolute_path),
        )
        self.assertEqual(errors, [])
        routers = [
            profile for profile in registry["profiles"] if profile["class"] == "readme"
        ]
        self.assertTrue(routers)
        for profile in routers:
            with self.subTest(profile=profile["id"]):
                self.assertNotIn("artifactIdPattern", profile)
                self.assertNotIn("lifecycle", profile)

    def test_current_classifiers_use_root_registry_only(self) -> None:
        retired = "docs/99.templates/support/document-profiles.json"
        active_sources = {
            "hook": REPOSITORY_ROOT
            / "docs/00.agent-governance/hooks/k8s-pre-edit.sh",
            "wiki": SCRIPTS_ROOT / "generate-llm-wiki-index.sh",
            "ria": SCRIPTS_ROOT / "reference_information_architecture.py",
            "eligibility": SCRIPTS_ROOT / "validate-active-corpus-eligibility.py",
        }
        root_registry = "docs/99.templates/registry.json"
        for name, path in active_sources.items():
            source = path.read_text(encoding="utf-8")
            with self.subTest(source=name):
                self.assertIn(root_registry, source)
                for line in source.splitlines():
                    if retired not in line:
                        continue
                    self.assertRegex(
                        line,
                        r"(?:RETIRED|TRANSITION|HISTORICAL).*document-profiles\.json",
                    )


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
        raw_registry = validator.load_internal_payload(REPOSITORY_ROOT)
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

    def test_work109_document_authority_is_consolidated_and_disjoint(self) -> None:
        staged = _staged_blob_inventory("docs")
        for path in WORK109_PROSE_OWNERS:
            with self.subTest(owner=path):
                self.assertIn(path, staged)
                self.assertEqual(
                    (REPOSITORY_ROOT / path).read_bytes(),
                    _staged_bytes(REPOSITORY_ROOT / path),
                )
        for path in WORK109_RETIRED_PROSE_OWNERS:
            with self.subTest(retired=path):
                self.assertNotIn(path, staged)
                self.assertFalse((REPOSITORY_ROOT / path).exists())

        registry = json.loads(
            _staged_bytes(
                REPOSITORY_ROOT
                / "docs/99.templates/support/document-profiles.json"
            )
        )
        current_owners = registry["governanceCurrentOwners"]["paths"]
        self.assertIn(WORK109_PROSE_OWNERS[0], current_owners)
        self.assertTrue(
            set(WORK109_RETIRED_PROSE_OWNERS[:4]).isdisjoint(current_owners)
        )

        expected_headings = {
            WORK109_PROSE_OWNERS[0]: {
                "Overview",
                "Authority Boundary",
                "Governance Context",
                "Current Contract",
                "Validation and Refresh",
                "Related Documents",
            },
            WORK109_PROSE_OWNERS[1]: {
                "Overview",
                "Purpose",
                "Owned Contract",
                "Authoring Rules",
                "Validation Contract",
                "Related Documents",
            },
            WORK109_PROSE_OWNERS[2]: {
                "Overview",
                "Purpose",
                "Owned Contract",
                "Authoring Rules",
                "Validation Contract",
                "Related Documents",
            },
        }
        for path, headings in expected_headings.items():
            text = _staged_bytes(REPOSITORY_ROOT / path).decode("utf-8")
            actual = set(re.findall(r"(?m)^## ([^#].+)$", text))
            with self.subTest(owner=path):
                self.assertEqual(actual, headings)

        authoring = _staged_bytes(
            REPOSITORY_ROOT / WORK109_PROSE_OWNERS[0]
        ).decode("utf-8")
        contract = _staged_bytes(
            REPOSITORY_ROOT / WORK109_PROSE_OWNERS[1]
        ).decode("utf-8")
        lifecycle = _staged_bytes(
            REPOSITORY_ROOT / WORK109_PROSE_OWNERS[2]
        ).decode("utf-8")
        self.assertIn("stage selection", authoring)
        self.assertIn("Exact-One-Profile", contract)
        self.assertIn("Supersession and Historical Preservation", lifecycle)
        for prose in (authoring, contract, lifecycle):
            self.assertNotIn('"profiles": [', prose)

    def test_work109_terminal_document_routes_close_stage04_and_preserve_transition_assets(
        self,
    ) -> None:
        self.assertEqual(_staged_blob_inventory("docs/04.execution"), {})
        self.assertFalse((REPOSITORY_ROOT / "docs/04.execution").exists())

        validator = self.validators["registry"]
        registry = validator.load_registry(REPOSITORY_ROOT)
        self.assertEqual(registry.route_state, "transition")
        self.assertEqual(
            validator.classify_path(
                registry,
                validator.PurePosixPath(
                    "scripts/document-taxonomy-migration.json"
                ),
            ).profile_id,
            "native/document-migration-manifest",
        )
        for path, profile_id in (
            ("docs/03.specs/0052-document-taxonomy-consolidation/plan.md", "sdlc/plan"),
            (
                "docs/03.specs/0052-document-taxonomy-consolidation/"
                "tasks/tsk-0001-work-100.md",
                "sdlc/task",
            ),
        ):
            with self.subTest(path=path):
                self.assertEqual(
                    validator.classify_path(
                        registry, validator.PurePosixPath(path)
                    ).profile_id,
                    profile_id,
                )

        contracts = sys.modules["document_contracts"]
        retired_or_invalid = (
            "docs/04.execution/README.md",
            "docs/04.execution/plans/README.md",
            "docs/04.execution/tasks/README.md",
            "docs/01.requirements/2026-08-13-dated.md",
            "docs/02.architecture/descriptions/2026-08-13-dated.md",
            "docs/03.specs/2026-08-13-dated/spec.md",
            "docs/06.release/rel-001.md",
        )
        for path in retired_or_invalid:
            with self.subTest(path=path):
                with self.assertRaises(contracts.DocumentContractError):
                    validator.classify_path(
                        registry, validator.PurePosixPath(path)
                    )

    def test_work109_limits_stage05_to_exact_current_link_normalization(self) -> None:
        base = _commit_blob_inventory(WORK109_BASE_COMMIT, "docs/05.operations")
        self.assertEqual(set(_staged_blob_inventory("docs/05.operations")), set(base))
        self.assertEqual(
            _worktree_regular_paths("docs/05.operations"), set(base)
        )
        changed_paths: set[str] = set()
        normalized_occurrences = 0
        route_replacements = {
            "docs/05.operations/README.md": ((
                "2. 사고가 없으면 `incidents/`는 README만 유지하고, 첫 사고 기록이 생길 때만 `incidents/YYYY/INC-###-<title>/` 폴더를 만든다. Incident 파일명은 폴더명과 같은 `INC-###-<title>.md`이고, postmortem은 같은 폴더의 `postmortem.md`로 추가한다.",
                "2. 사고가 없으면 `incidents/`는 README만 유지하고, 첫 사고 기록이 생길 때만 `incidents/<year>/inc-####-<slug>/` 폴더를 만든다. Incident와 Postmortem은 같은 폴더에서 각각 `incident.md`와 `postmortem.md`를 사용한다.",
            ), (
                "[Document Stage Routing](../00.agent-governance/rules/document-stage-routing.md)",
                "[Document Stage Routing](../00.agent-governance/rules/document-authoring.md)",
            ), (
                "[Harness Implementation Map](../00.agent-governance/harness-implementation-map.md)",
                "[Local Harness Catalog](../00.agent-governance/harness-catalog.md)",
            )),
            "docs/05.operations/guides/0009-llm-wiki-curation-guide.md": ((
                "../../00.agent-governance/rules/document-stage-routing.md",
                "../../00.agent-governance/rules/document-authoring.md",
            ),),
            "docs/05.operations/runbooks/0011-reference-maintenance-runbook.md": ((
                "../../00.agent-governance/rules/document-stage-routing.md",
                "../../00.agent-governance/rules/document-authoring.md",
            ),),
            "docs/05.operations/policies/README.md": ((
                "- Postmortems: `../incidents/YYYY/INC-###-<title>/postmortem.md`",
                "- Postmortems: `../incidents/<year>/inc-####-<slug>/postmortem.md`",
            ),),
            "docs/05.operations/runbooks/README.md": ((
                "- Postmortems: `../incidents/YYYY/INC-###-<title>/postmortem.md`",
                "- Postmortems: `../incidents/<year>/inc-####-<slug>/postmortem.md`",
            ),),
            "docs/05.operations/incidents/README.md": (
                (
                    "첫 사고 기록이 필요할 때만 `YYYY/INC-###-<title>/` 하위 경로를 만든다.\nIncident Record 파일명은 반드시 incident 폴더명과 동일한\n`INC-###-<title>.md`여야 한다.",
                    "첫 사고 기록이 필요할 때만 `<year>/inc-####-<slug>/` 하위 경로를 만든다.\nIncident Record와 Postmortem은 각각 고정 basename `incident.md`와\n`postmortem.md`를 사용한다.",
                ),
                ("`./YYYY/INC-###-<title>/INC-###-<title>.md`", "`./<year>/inc-####-<slug>/incident.md`"),
                ("`./YYYY/INC-###-<title>/postmortem.md`", "`./<year>/inc-####-<slug>/postmortem.md`"),
                ("├── YYYY/\n│   └── INC-###-<title>/\n│       ├── INC-###-<title>.md  # Incident fact record", "├── <year>/\n│   └── inc-####-<slug>/\n│       ├── incident.md         # Incident fact record"),
                ("2. Incident Record는 `YYYY/INC-###-<title>/INC-###-<title>.md`로 작성해 폴더 ID와 파일 ID를 일치시킨다.", "2. Incident Record는 `<year>/inc-####-<slug>/incident.md`로 작성하고 frontmatter `artifact_id`를 `INC-<YYYY>-<DDDD>`와 일치시킨다."),
            ),
        }
        for path in base:
            base_bytes = subprocess.run(
                ["git", "show", f"{WORK109_BASE_COMMIT}:{path}"],
                cwd=REPOSITORY_ROOT,
                check=True,
                capture_output=True,
            ).stdout
            expected, spec_count = re.subn(
                rb"((?:\.\./)+)03\.specs/([0-9]{3})-",
                rb"\g<1>03.specs/0\g<2>-",
                base_bytes,
            )
            expected, prd_count = re.subn(
                rb"((?:\.\./)+)01\.requirements/([0-9]{3})-",
                rb"\g<1>01.requirements/0\g<2>-",
                expected,
            )
            for old, new in route_replacements.get(path, ()):
                old_bytes = old.encode("utf-8")
                count = expected.count(old_bytes)
                self.assertGreater(count, 0)
                expected = expected.replace(old_bytes, new.encode("utf-8"))
            if expected != base_bytes:
                changed_paths.add(path)
                normalized_occurrences += spec_count + prd_count
            expected = re.sub(
                rb"(\]\((?:\.\./)+02\.architecture/descriptions/)ad-"
                rb"((?:000[4-9]|001[01])-[^)]+\.md\))",
                rb"\g<1>\g<2>",
                expected,
            )
            expected = re.sub(
                rb"(\]\((?:\.\./)+03\.specs/"
                rb"(?:0004-argo-rollouts-progressive-delivery|"
                rb"0005-argo-notifications-slack))/tasks\.md(?:#[^)]*)?\)",
                rb"\g<1>/README.md)",
                expected,
            )
            with self.subTest(path=path):
                _assert_staged_and_worktree_bytes(
                    REPOSITORY_ROOT / path, expected
                )
        self.assertEqual(len(changed_paths), 19)
        self.assertEqual(normalized_occurrences, 49)

    def test_work109_uses_four_digit_document_and_incident_routes(self) -> None:
        base = _commit_blob_inventory(WORK109_BASE_COMMIT, "docs")
        staged = _staged_blob_inventory("docs")
        base_requirements = {
            path
            for path in base
            if re.fullmatch(r"docs/01\.requirements/[0-9]{3}-[^/]+\.md", path)
        }
        base_work_units = {
            path.split("/", 3)[2]
            for path in base
            if re.match(r"docs/03\.specs/[0-9]{3}-[^/]+/", path)
        }
        self.assertEqual(len(base_requirements), 8)
        self.assertEqual(len(base_work_units), 49)

        expected_requirements = {
            path.replace("docs/01.requirements/", "docs/01.requirements/0", 1)
            for path in base_requirements
        }
        expected_work_units = {f"0{name}" for name in base_work_units}
        self.assertTrue(expected_requirements.issubset(staged))
        self.assertTrue(
            all(
                any(path.startswith(f"docs/03.specs/{name}/") for path in staged)
                for name in expected_work_units
            )
        )
        self.assertFalse(
            any(
                re.fullmatch(r"docs/01\.requirements/[0-9]{3}-[^/]+\.md", path)
                or re.match(r"docs/03\.specs/[0-9]{3}-[^/]+/", path)
                for path in staged
            )
        )

        validator = self.validators["registry"]
        registry = validator.load_registry(REPOSITORY_ROOT)
        valid = {
            "docs/01.requirements/0008-workspace-document-taxonomy-consolidation.md": "sdlc/requirement-package",
            "docs/03.specs/0052-document-taxonomy-consolidation/spec.md": "sdlc/spec",
            "docs/03.specs/0052-document-taxonomy-consolidation/plan.md": "sdlc/plan",
            "docs/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0001-work-100.md": "sdlc/task",
            "docs/05.operations/incidents/2026/inc-0001-database-latency/incident.md": "sdlc/incident",
            "docs/05.operations/incidents/2026/inc-0001-database-latency/postmortem.md": "sdlc/postmortem",
        }
        for path, profile_id in valid.items():
            with self.subTest(valid=path):
                self.assertEqual(
                    validator.classify_path(
                        registry, validator.PurePosixPath(path)
                    ).profile_id,
                    profile_id,
                )

        contracts = sys.modules["document_contracts"]
        invalid = (
            "docs/01.requirements/008-workspace-document-taxonomy-consolidation.md",
            "docs/01.requirements/00008-workspace-document-taxonomy-consolidation.md",
            "docs/03.specs/052-document-taxonomy-consolidation/spec.md",
            "docs/03.specs/00052-document-taxonomy-consolidation/spec.md",
            "docs/05.operations/incidents/2026/inc-001-database-latency/incident.md",
            "docs/05.operations/incidents/2026/INC-0001-database-latency/incident.md",
            "docs/05.operations/incidents/2026/inc-0001-database-latency/INC-0001-database-latency.md",
            "docs/05.operations/incidents/2026/inc-0001-database-latency/nested/incident.md",
        )
        for path in invalid:
            with self.subTest(invalid=path):
                with self.assertRaises(contracts.DocumentContractError):
                    validator.classify_path(
                        registry, validator.PurePosixPath(path)
                    )

    def test_work109_direct_approval_lineage_is_atomic(self) -> None:
        work_unit = "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation"
        for leaf in ("spec.md", "plan.md", "tasks.md"):
            with self.subTest(leaf=leaf):
                text = _staged_bytes(REPOSITORY_ROOT / work_unit / leaf).decode(
                    "utf-8"
                )
                self.assertIn("status: active\n", text)

        registry = json.loads(
            _staged_bytes(
                REPOSITORY_ROOT
                / "docs/99.templates/support/document-profiles.json"
            )
        )
        expected = {
            "spec": "0054",
            "plan": f"{work_unit}/plan.md",
            "task": f"{work_unit}/tasks.md",
            "state": "active",
            "reason": (
                "Direct human-approved B-scope SDLC and AI-agent governance "
                "consolidation including Stage 90"
            ),
            "decision": "0022",
            "approvalMode": "spec-body-record",
        }
        self.assertEqual(registry["standaloneExecutions"][-1], expected)
        self.assertEqual(
            [row["spec"] for row in registry["standaloneExecutions"]],
            sorted(row["spec"] for row in registry["standaloneExecutions"]),
        )
        stage03_index = _staged_bytes(
            REPOSITORY_ROOT / "docs/03.specs/README.md"
        ).decode("utf-8")
        self.assertIn(
            "./0054-sdlc-document-and-agent-governance-consolidation/spec.md",
            stage03_index,
        )
        transferred = {
            "109": "WORK-054-002",
            "110": "WORK-054-003",
            "111": "WORK-054-010",
            "112": "WORK-054-011",
            "113": "WORK-054-012",
            "114": "WORK-054-013",
            "115": "WORK-054-014",
        }
        package = REPOSITORY_ROOT / "docs/03.specs/0052-document-taxonomy-consolidation"
        plan_text = _staged_bytes(package / "plan.md").decode("utf-8")
        for legacy, successor in transferred.items():
            sequence = int(legacy) - 98
            task_path = package / "tasks" / f"tsk-{sequence:04d}-work-{legacy}.md"
            for leaf, text in (
                ("plan.md", plan_text),
                (task_path.name, _staged_bytes(task_path).decode("utf-8")),
            ):
                with self.subTest(leaf=leaf, legacy=legacy):
                    row = next(
                        line
                        for line in text.splitlines()
                        if line.startswith(f"| WORK-{legacy} |")
                    )
                    self.assertIn("| Transferred |", row)
                    self.assertIn(successor, row)
                    self.assertNotIn("| In Progress |", row)
                    self.assertNotIn("| Queued |", row)

    def test_work109_adr0022_history_admission_is_exact_and_atomic(self) -> None:
        validator = self.validators["registry"]
        adr_path = REPOSITORY_ROOT / validator.WORK109_DIRECT_APPROVAL_ADR_PATH
        required_paths = (
            validator.WORK109_DIRECT_APPROVAL_SPEC_PATH,
            validator.WORK109_REGISTRY_PATH,
            validator.WORK109_MANIFEST_PATH,
            validator.WORK109_MIGRATION_LEDGER_PATH.as_posix(),
        )
        staged = {
            path: _staged_bytes(REPOSITORY_ROOT / path) for path in required_paths
        }
        adr = _staged_bytes(adr_path)
        self.assertTrue(
            validator._work109_direct_approval_history_transition(
                REPOSITORY_ROOT,
                adr,
                staged,
            )
        )

        mutations: dict[str, tuple[bytes, dict[str, bytes]]] = {}
        mutations["ADR blob drift"] = (adr + b"\n", dict(staged))

        spec_drift = dict(staged)
        spec_drift[validator.WORK109_DIRECT_APPROVAL_SPEC_PATH] = spec_drift[
            validator.WORK109_DIRECT_APPROVAL_SPEC_PATH
        ].replace(
            b"authorizes this standalone execution relation",
            b"does not authorize this standalone execution relation",
            1,
        )
        mutations["Spec authority drift"] = (adr, spec_drift)

        registry_drift = dict(staged)
        registry = json.loads(
            registry_drift[validator.WORK109_REGISTRY_PATH].decode("utf-8")
        )
        registry["standaloneExecutions"][-1]["decision"] = "0021"
        registry_drift[validator.WORK109_REGISTRY_PATH] = json.dumps(
            registry, indent=2
        ).encode("utf-8")
        mutations["standalone authority drift"] = (adr, registry_drift)

        ledger_drift = dict(staged)
        ledger_bytes = ledger_drift[
            validator.WORK109_MIGRATION_LEDGER_PATH.as_posix()
        ]
        ledger_text = ledger_bytes.decode("utf-8")
        rows = json.loads(ledger_text.split("```json", 1)[1].split("```", 1)[0])
        rows.pop(next(index for index, row in enumerate(rows) if row["action"] == "moved"))
        ledger_drift[validator.WORK109_MIGRATION_LEDGER_PATH.as_posix()] = (
            _replace_mig0002_rows(ledger_bytes, rows)
        )
        mutations["MIG-0002 authority drift"] = (adr, ledger_drift)

        incomplete = dict(staged)
        incomplete.pop(validator.WORK109_DIRECT_APPROVAL_SPEC_PATH)
        mutations["incomplete authority"] = (adr, incomplete)

        for label, (candidate_adr, candidate_staged) in mutations.items():
            with self.subTest(label=label):
                with self.assertRaises(AssertionError):
                    validator._work109_direct_approval_history_transition(
                        REPOSITORY_ROOT,
                        candidate_adr,
                        candidate_staged,
                    )

    def test_work109_mig0002_exact_atomic_coverage(self) -> None:
        validator = self.validators["registry"]
        ledger_path = (
            REPOSITORY_ROOT
            / "docs/98.archive/migrations/"
            "mig-0002-sdlc-document-and-governance-consolidation.md"
        )
        source = _staged_bytes(ledger_path).decode("utf-8")
        match = re.search(
            r"<!-- archive-migration-ledger:v1 format=json -->\s*"
            r"```json\s*(\[.*?\])\s*```",
            source,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match)
        rows = json.loads(match.group(1))
        self.assertEqual(len(rows), 154)
        self.assertEqual(
            [row["legacy_path"] for row in rows],
            sorted(row["legacy_path"] for row in rows),
        )

        base = _commit_blob_inventory(WORK109_BASE_COMMIT, "docs")
        move_map: dict[str, str] = {}
        for path in base:
            if re.fullmatch(r"docs/01\.requirements/[0-9]{3}-[^/]+\.md", path):
                move_map[path] = path.replace(
                    "docs/01.requirements/", "docs/01.requirements/0", 1
                )
                continue
            matched = re.match(r"(docs/03\.specs/)([0-9]{3}-[^/]+)(/.*)", path)
            if matched:
                move_map[path] = f"{matched.group(1)}0{matched.group(2)}{matched.group(3)}"
        replacement_map = {
            "docs/04.execution/README.md": "docs/03.specs/README.md",
            "docs/04.execution/plans/README.md": (
                "docs/99.templates/templates/sdlc/execution/plan.template.md"
            ),
            "docs/04.execution/tasks/README.md": (
                "docs/99.templates/templates/sdlc/execution/task.template.md"
            ),
        }
        merge_map = {
            "docs/00.agent-governance/rules/document-stage-routing.md": (
                "docs/00.agent-governance/rules/document-authoring.md"
            ),
            "docs/00.agent-governance/rules/documentation-protocol.md": (
                "docs/00.agent-governance/rules/document-authoring.md"
            ),
            "docs/00.agent-governance/rules/stage-authoring-matrix.md": (
                "docs/00.agent-governance/rules/document-authoring.md"
            ),
            "docs/00.agent-governance/rules/stage-checklists.md": (
                "docs/00.agent-governance/rules/document-authoring.md"
            ),
            "docs/99.templates/support/common-documentation-governance.md": (
                "docs/99.templates/support/document-lifecycle.md"
            ),
            "docs/99.templates/support/documentation-contract.md": (
                "docs/99.templates/support/document-contract.md"
            ),
            "docs/99.templates/support/frontmatter-schema.md": (
                "docs/99.templates/support/document-contract.md"
            ),
            "docs/99.templates/support/legacy-cleanup-rules.md": (
                "docs/99.templates/support/document-lifecycle.md"
            ),
            "docs/99.templates/support/sdlc-governance.md": (
                "docs/99.templates/support/document-lifecycle.md"
            ),
            "docs/99.templates/support/template-routing.md": (
                "docs/99.templates/support/document-contract.md"
            ),
        }
        self.assertEqual(len(move_map), 141)
        self.assertEqual(
            set(row["legacy_path"] for row in rows),
            set(move_map) | set(replacement_map) | set(merge_map),
        )

        staged = _staged_blob_inventory("docs")
        wp004b_current_targets = validator._work054_wp004b_current_targets(
            REPOSITORY_ROOT
        )
        required_fields = {
            "legacy_path",
            "stable_path",
            "artifact_id",
            "action",
            "replacement",
            "source_commit",
            "source_blob",
            "content_sha256",
            "reason",
        }
        for row in rows:
            legacy_path = row["legacy_path"]
            with self.subTest(legacy_path=legacy_path):
                self.assertEqual(set(row), required_fields)
                self.assertEqual(row["source_commit"], WORK109_BASE_COMMIT)
                self.assertEqual(row["source_blob"], base[legacy_path][1])
                payload = subprocess.run(
                    ["git", "show", f"{WORK109_BASE_COMMIT}:{legacy_path}"],
                    cwd=REPOSITORY_ROOT,
                    check=True,
                    capture_output=True,
                ).stdout
                self.assertEqual(
                    row["content_sha256"], hashlib.sha256(payload).hexdigest()
                )
                self.assertTrue(row["reason"].strip())
                if legacy_path in move_map:
                    target = move_map[legacy_path]
                    self.assertEqual(row["stable_path"], target)
                    self.assertEqual(row["action"], "moved")
                    self.assertIsNone(row["replacement"])
                    current_target = wp004b_current_targets.get(target, target)
                    self.assertIn(current_target, staged)
                    if target in wp004b_current_targets:
                        continue
                    target_text = _staged_bytes(REPOSITORY_ROOT / current_target).decode(
                        "utf-8"
                    )
                    identity = re.search(
                        r'(?m)^artifact_id:\s*["\']?([^"\'\n]+)', target_text
                    )
                    self.assertIsNotNone(identity)
                    self.assertEqual(row["artifact_id"], identity.group(1))
                elif legacy_path in replacement_map:
                    self.assertIsNone(row["stable_path"])
                    self.assertIsNone(row["artifact_id"])
                    self.assertEqual(row["action"], "replaced")
                    self.assertEqual(row["replacement"], replacement_map[legacy_path])
                    self.assertIn(row["replacement"], staged)
                else:
                    self.assertIsNone(row["stable_path"])
                    self.assertIsNone(row["artifact_id"])
                    self.assertEqual(row["action"], "merged")
                    self.assertEqual(row["replacement"], merge_map[legacy_path])
                    self.assertIn(row["replacement"], staged)

    def test_work109_transition_overlay_is_finite_and_fail_closed(self) -> None:
        validator = self.validators["registry"]
        tool = validator._load_migration_tool(REPOSITORY_ROOT)
        document = tool.load_manifest_document(
            REPOSITORY_ROOT / "scripts/document-taxonomy-migration.json"
        )
        ledger_path = (
            REPOSITORY_ROOT
            / "docs/98.archive/migrations/"
            "mig-0002-sdlc-document-and-governance-consolidation.md"
        )
        ledger_bytes = ledger_path.read_bytes()

        projection = validator._work109_transition_manifest_projection(
            REPOSITORY_ROOT,
            document.entries,
            route_state="transition",
            ledger_bytes=ledger_bytes,
        )
        projected_moves = tuple(
            row for row in projection if row["disposition"] == "move-current"
        )
        projected_archives = tuple(
            row for row in projection if row["disposition"] == "archive-unique"
        )
        self.assertEqual(len(projection), 132)
        self.assertEqual(len(projected_moves), 82)
        self.assertEqual(len(projected_archives), 50)
        self.assertTrue(
            all(
                re.fullmatch(
                    r"docs/03\.specs/[0-9]{4}-[^/]+/(?:plan|README)\.md",
                    row["target"],
                )
                and re.fullmatch(r"Spec-[0-9]{4}", row["workUnit"])
                for row in projected_moves
            )
        )
        self.assertEqual(
            [row["source"] for row in projected_archives],
            [
                row["source"]
                for row in document.entries
                if row["disposition"] == "archive-unique"
            ],
        )

        ledger_text = ledger_bytes.decode("utf-8")
        rows = json.loads(ledger_text.split("```json", 1)[1].split("```", 1)[0])
        moved = [row for row in rows if row["action"] == "moved"]
        lifecycle_only = [row for row in rows if row["action"] != "moved"]
        self.assertEqual(len(moved), 141)
        self.assertEqual(len(lifecycle_only), 13)
        self.assertTrue(
            all(
                row["legacy_path"]
                not in {entry["target"] for entry in projected_moves}
                for row in lifecycle_only
            )
        )

        negative_rows: dict[str, list[dict[str, object]]] = {}
        wrong_source_commit = json.loads(json.dumps(rows))
        first_moved = next(row for row in wrong_source_commit if row["action"] == "moved")
        first_moved["source_commit"] = "0" * 40
        negative_rows["source commit drift"] = wrong_source_commit

        wrong_mapping = json.loads(json.dumps(rows))
        first_moved = next(row for row in wrong_mapping if row["action"] == "moved")
        first_moved["stable_path"] = first_moved["stable_path"].replace(
            "0001-", "9999-", 1
        )
        negative_rows["wrong stable mapping"] = wrong_mapping

        missing_move = json.loads(json.dumps(rows))
        missing_move.pop(
            next(index for index, row in enumerate(missing_move) if row["action"] == "moved")
        )
        negative_rows["missing move"] = missing_move

        extra_move = json.loads(json.dumps(rows))
        extra_move.append(
            json.loads(
                json.dumps(next(row for row in extra_move if row["action"] == "moved"))
            )
        )
        negative_rows["extra move"] = extra_move

        for label, mutated in negative_rows.items():
            with self.subTest(label=label):
                with self.assertRaises(AssertionError):
                    validator._work109_transition_manifest_projection(
                        REPOSITORY_ROOT,
                        document.entries,
                        route_state="transition",
                        ledger_bytes=_replace_mig0002_rows(ledger_bytes, mutated),
                    )

        with self.assertRaisesRegex(AssertionError, "transition-only"):
            validator._work109_transition_manifest_projection(
                REPOSITORY_ROOT,
                document.entries,
                route_state="terminal",
                ledger_bytes=ledger_bytes,
            )

    def test_work109_mig0002_parser_pins_the_complete_document(self) -> None:
        validator = self.validators["registry"]
        ledger_path = REPOSITORY_ROOT / validator.WORK109_MIGRATION_LEDGER_PATH
        raw = ledger_path.read_bytes()

        self.assertEqual(len(validator._work109_ledger_rows(raw)), 154)
        self.assertEqual(
            hashlib.sha256(raw).hexdigest(),
            validator.WORK109_MIGRATION_DOCUMENT_SHA256,
        )
        for name, candidate in (
            ("trailing", raw + b"\nUnreviewed trailing prose.\n"),
            (
                "oversize",
                raw
                + b"x"
                * (
                    validator.MIGRATION_DOCUMENT_MAX_BYTES + 1 - len(raw)
                ),
            ),
        ):
            with self.subTest(name=name), self.assertRaises(AssertionError):
                validator._work109_ledger_rows(candidate)

    def test_work109_default_projection_reads_mig0002_from_index(self) -> None:
        validator = self.validators["registry"]
        tool = validator._load_migration_tool(REPOSITORY_ROOT)
        document = tool.load_manifest_document(
            REPOSITORY_ROOT / "scripts/document-taxonomy-migration.json"
        )
        staged = {
            path.as_posix(): _staged_bytes(REPOSITORY_ROOT / path)
            for path in (
                validator.WORK109_MIGRATION_LEDGER_PATH,
                validator.WORK054_WP004B_MIGRATION_LEDGER_PATH,
            )
        }
        with mock.patch.object(
            validator,
            "read_staged_blob_bounded",
            side_effect=lambda _root, path, **_kwargs: staged[path],
        ) as reader:
            projection = validator._work109_transition_manifest_projection(
                REPOSITORY_ROOT,
                document.entries,
                route_state="transition",
            )
        self.assertEqual(len(projection), 132)
        self.assertEqual(
            reader.call_args_list,
            [
                mock.call(
                    REPOSITORY_ROOT.resolve(),
                    path.as_posix(),
                    max_bytes=validator.MIGRATION_DOCUMENT_MAX_BYTES,
                )
                for path in (
                    validator.WORK109_MIGRATION_LEDGER_PATH,
                    validator.WORK054_WP004B_MIGRATION_LEDGER_PATH,
                )
            ],
        )

    def test_work109_stage04_readme_retirement_profiles_are_exact(self) -> None:
        validator = self.validators["registry"]
        registry = validator.load_registry(REPOSITORY_ROOT)
        fixture_path = REPOSITORY_ROOT / validator.README_FIXTURE_PATH
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        expected = {
            "docs/04.execution/README.md": (
                "readme/stage-index",
                "docs/03.specs/README.md",
            ),
            "docs/04.execution/plans/README.md": (
                "readme/collection-index",
                "docs/99.templates/templates/sdlc/execution/plan.template.md",
            ),
            "docs/04.execution/tasks/README.md": (
                "readme/collection-index",
                "docs/99.templates/templates/sdlc/execution/task.template.md",
            ),
        }
        actual = {
            row["path"]: (row["profile"], row["destination"])
            for row in fixture["retiredPaths"]
            if row["retiredBy"] == "WORK-054-002"
        }
        self.assertEqual(actual, expected)
        routers = sorted(
            (REPOSITORY_ROOT / "docs/03.specs").glob(
                "[0-9][0-9][0-9][0-9]-*/README.md"
            )
        )
        self.assertEqual(len(routers), 57)
        for router in routers:
            relative = router.relative_to(REPOSITORY_ROOT)
            with self.subTest(path=relative.as_posix()):
                self.assertEqual(
                    validator.classify_path(registry, relative).profile_id,
                    "readme/collection-index",
                )
                self.assertFalse(_staged_bytes(router).startswith(b"---\n"))

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
            f"{identifier}-{slug}.md"
            for identifier, slug, _ in EXPECTED_AD_CORPUS
        }
        actual_paths = {
            path
            for path in architecture_inventory
            if re.fullmatch(
                r"docs/02\.architecture/descriptions/[0-9]{4}-[^/]+\.md",
                path,
            )
        }
        self.assertEqual(actual_paths, expected_paths)
        for identifier, slug, status in EXPECTED_AD_CORPUS:
            relative = (
                "docs/02.architecture/descriptions/"
                f"{identifier}-{slug}.md"
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
        prd008 = next(program for program in programs if program["prd"] == "0008")
        self.assertEqual(prd008["ad"], "0011")
        self.assertEqual(prd008["tranches"], [
            {
                "spec": "0052",
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
        self.assertIn("status: superseded\n", adr0024)
        self.assertIn("superseded_by: ADR-0030\n", adr0024)
        ad0011 = _staged_bytes(
            REPOSITORY_ROOT
            / "docs/02.architecture/descriptions/0011-document-taxonomy-consolidation-architecture.md"
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

    def test_work105_admits_only_the_exact_closure_implementation_alias(self) -> None:
        validator = self.validators["registry"]
        path = "scripts/validate-agent-governance-closure.py"
        exact = (
            '            "docs/02.architecture/'
            'requirements/0006-workspace-agent-governance-platform.md"'
        )
        self.assertTrue(
            validator._work054_wp004b_historical_ard_line(
                REPOSITORY_ROOT,
                path,
                exact,
            )
        )
        for wrong_path, wrong_line in (
            ("scripts/other.py", exact),
            (path, exact.replace("0006", "0007")),
            (path, exact + "  # broad fallback"),
        ):
            with self.subTest(path=wrong_path, line=wrong_line):
                self.assertFalse(
                    validator._work054_wp004b_historical_ard_line(
                        REPOSITORY_ROOT,
                        wrong_path,
                        wrong_line,
                    )
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
                        "docs/03.specs/0052-document-taxonomy-consolidation/"
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
            / "docs/01.requirements/0008-workspace-document-taxonomy-consolidation.md"
        ).decode("utf-8")
        spec = _staged_bytes(
            REPOSITORY_ROOT
            / "docs/03.specs/0052-document-taxonomy-consolidation/spec.md"
        ).decode("utf-8")
        adr = _staged_bytes(
            REPOSITORY_ROOT
            / "docs/02.architecture/decisions/0024-terminal-artifact-identity-and-archive-layout.md"
        ).decode("utf-8")
        self.assertNotIn("legacy ARD consumers", prd)
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
            / "docs/00.agent-governance/rules/document-authoring.md",
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

    def test_work105_spec0019_history_is_bounded_during_authority_convergence(self) -> None:
        validator = self.validators["registry"]
        for relative in (
            "docs/03.specs/0019-template-path-numbering-contract/spec.md",
            "docs/03.specs/0019-template-path-numbering-contract/plan.md",
        ):
            path = REPOSITORY_ROOT / relative
            with self.subTest(path=relative):
                self.assertIn(relative, validator.WORK105_PINNED_LEGACY_HISTORY_PATHS)
                self.assertNotEqual(
                    validator._work108_without_outer_artifact_id(
                        relative, _staged_bytes(path)
                    ),
                    _work105_base_bytes(path),
                )

    def test_work105_stage98_invariant_blocks_105_106_and_gates_107_plus(self) -> None:
        ad0011_path = (
            REPOSITORY_ROOT
            / "docs/02.architecture/descriptions/0011-document-taxonomy-consolidation-architecture.md"
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
        fixture = json.loads(native_fixture)
        base_fixture = json.loads(_work105_base_bytes(NATIVE_SURFACE_CASES))
        self.assertEqual(
            [
                {key: value for key, value in family.items() if key != "path"}
                for family in fixture["families"]
            ],
            [
                {key: value for key, value in family.items() if key != "path"}
                for family in base_fixture["families"]
            ],
        )
        self.assertEqual(
            [
                family["path"]
                for family in fixture["families"]
                if family["id"] in {"openapi", "graphql", "protobuf"}
            ],
            [
                "docs/03.specs/0999-native-fixture/contracts/openapi.yaml",
                "docs/03.specs/0999-native-fixture/contracts/schema.graphql",
                "docs/03.specs/0999-native-fixture/contracts/service.proto",
            ],
        )
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
            "docs/98.archive/migrations/mig-0002-sdlc-document-and-governance-consolidation.md",
            # WP-003 recorded the agent governance control-plane consolidation
            # as its own Stage 98 migration document.
            "docs/98.archive/migrations/mig-0003-agent-governance-control-plane-consolidation.md",
            "docs/98.archive/migrations/0004-document-authority-convergence.md",
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
            "docs/02.architecture/descriptions/011-short.md",
            "docs/03.specs/52-short/spec.md",
            "docs/98.archive/changes/chg-0001-bad/nested/plan.md",
            "docs/98.archive/tombstones/02.architecture/tmb-ar" + "d-0011.md",
        ):
            with self.subTest(invalid=invalid):
                self.assertIsNone(validator._work106_derive_artifact_identity(invalid))

    def test_work106_artifact_namespace_is_transition_aware_and_global(self) -> None:
        validator = self.validators["registry"]
        records = (
            ("docs/01.requirements/0008-program.md", {}),
            ("docs/02.architecture/descriptions/0011-program.md", {"artifact_id": "AD-0011"}),
            (
                "docs/90.references/current.md",
                {"original_artifact_id": "AR" + "D-0011"},
            ),
        )
        self.assertEqual(validator._work106_artifact_diagnostics(records, terminal=False), ())
        self.assertIn(
            "ARTIFACT-ID-MISSING:docs/01.requirements/0008-program.md",
            validator._work106_artifact_diagnostics(records, terminal=True),
        )

        mutations = (
            (("docs/01.requirements/0008-program.md", {"artifact_id": "REQ-0009"}), "ARTIFACT-ID-PATH"),
            (("docs/90.references/current.md", {"artifact_id": "REQ-0008"}), "ARTIFACT-ID-PROHIBITED"),
            (("docs/01.requirements/0009-second.md", {"artifact_id": "REQ-0008"}), "ARTIFACT-ID-PATH"),
        )
        for record, expected in mutations:
            with self.subTest(expected=expected):
                diagnostics = validator._work106_artifact_diagnostics(
                    (records[1], record), terminal=False
                )
                self.assertTrue(any(item.startswith(expected) for item in diagnostics))

        duplicate = (
            ("docs/01.requirements/0008-program.md", {"artifact_id": "REQ-0008"}),
            ("docs/01.requirements/0008-alias.md", {"artifact_id": "REQ-0008"}),
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
                if "artifact_id" in profile["requiredFrontmatter"]["required"]
            },
        )
        self.assertEqual(
            set(validator.WORK108_MANDATORY_PROFILE_IDS),
            {
                profile_id
                for profile_id, profile in profiles.items()
                if "artifact_id" in profile["requiredFrontmatter"]["allowed"]
                or "artifact_id" in profile["requiredFrontmatter"]["order"]
            },
        )
        for source_id in validator.WORK108_MANDATORY_PROFILE_IDS:
            with self.subTest(source_id=source_id):
                self.assertIn("artifact_id", profiles[source_id]["requiredFrontmatter"]["allowed"])
                self.assertIn("artifact_id", profiles[source_id]["requiredFrontmatter"]["order"])
                template_ids = (
                    (
                        "template/sdlc/prd",
                        "template/sdlc/srs",
                        "template/sdlc/interface",
                    )
                    if source_id == "sdlc/requirement-package"
                    else (f"template/{source_id}",)
                )
                for template_id in template_ids:
                    self.assertNotIn(
                        "artifact_id", profiles[template_id]["requiredFrontmatter"]["required"]
                    )
                    self.assertNotIn(
                        "artifact_id", profiles[template_id]["requiredFrontmatter"]["allowed"]
                    )
                    self.assertNotIn(
                        "artifact_id", profiles[template_id]["requiredFrontmatter"]["order"]
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
        self.assertTrue(identities)
        self.assertEqual(len(identities), len({path for path, _ in identities}))
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


class Wp004bCorpusCutoverTests(unittest.TestCase):
    """Independent terminal-corpus assertions for WP-004B."""

    TASK_COUNTS = {
        "0004": 5, "0005": 5, "0009": 6, "0010": 6, "0011": 7,
        "0012": 6, "0013": 5, "0014": 6, "0015": 5, "0016": 5,
        "0017": 8, "0018": 7, "0019": 5, "0020": 5, "0021": 4,
        "0022": 6, "0023": 5, "0024": 4, "0025": 6, "0026": 5,
        "0027": 6, "0028": 6, "0029": 4, "0030": 8, "0037": 6,
        "0038": 8, "0039": 7, "0040": 5, "0041": 6, "0042": 6,
        "0043": 5, "0044": 6, "0045": 7, "0046": 6, "0047": 6,
        "0048": 6, "0049": 7, "0050": 7, "0051": 6, "0052": 17,
        "0053": 11, "0055": 15, "0056": 6, "0057": 8, "0058": 8,
        "0059": 13, "0060": 4, "0061": 4,
    }

    @staticmethod
    def _metadata(path: Path) -> dict[str, object]:
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
        if match is None:
            raise AssertionError(f"missing frontmatter: {path}")
        metadata: dict[str, object] = {}
        for line in match.group(1).splitlines():
            key, separator, value = line.partition(":")
            if separator:
                metadata[key] = value.strip().strip("\"'")
        return metadata

    def test_requirement_packages_use_complete_unique_member_ids(self) -> None:
        requirements = sorted((REPOSITORY_ROOT / "docs/01.requirements").glob("[0-9][0-9][0-9][0-9]-*.md"))
        self.assertEqual(len(requirements), 8)
        all_members: list[str] = []
        expected_counts = (
            (3, 0, 3), (3, 1, 2), (11, 2, 2), (4, 2, 1),
            (10, 2, 0), (11, 2, 0), (10, 2, 0), (16, 6, 0),
        )
        for sequence, (path, counts) in enumerate(zip(requirements, expected_counts), 1):
            package = f"REQ-{sequence:04d}"
            metadata = self._metadata(path)
            self.assertEqual(metadata.get("type"), "sdlc/requirement-package")
            self.assertEqual(metadata.get("artifact_id"), package)
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("REQ-PRD-MET-", text)
            normative = text.split("## Success", 1)[0]
            self.assertNotRegex(normative, r"\bACC-[A-Z0-9-]+\b")
            members = re.findall(rf"\b{package}-(FR|NFR|IF)-([0-9]{{4}})\b", text)
            for family, expected in zip(("FR", "NFR", "IF"), counts):
                numbers = list(dict.fromkeys(number for actual, number in members if actual == family))
                self.assertEqual(numbers, [f"{number:04d}" for number in range(1, expected + 1)])
            all_members.extend(dict.fromkeys(f"{package}-{family}-{number}" for family, number in members))
        self.assertEqual(len(all_members), 93)
        self.assertEqual(len(all_members), len(set(all_members)))

    def test_requirement_supersession_is_reciprocal_and_done_is_absent(self) -> None:
        paths = sorted((REPOSITORY_ROOT / "docs/01.requirements").glob("[0-9][0-9][0-9][0-9]-*.md"))
        metadata = {path.name[:4]: self._metadata(path) for path in paths}
        self.assertEqual(metadata["0005"].get("status"), "superseded")
        self.assertEqual(metadata["0005"].get("superseded_by"), "REQ-0008")
        self.assertEqual(metadata["0006"].get("status"), "superseded")
        self.assertEqual(metadata["0006"].get("superseded_by"), "REQ-0008")
        self.assertEqual(metadata["0008"].get("status"), "active")
        self.assertEqual(metadata["0008"].get("supersedes"), "[REQ-0005, REQ-0006]")
        self.assertNotIn("done", {item.get("status") for item in metadata.values()})
        for identifier in ("0005", "0006"):
            text = paths[int(identifier) - 1].read_text(encoding="utf-8")
            self.assertEqual(text.count("superseded_by:"), 1)
        self.assertEqual(paths[7].read_text(encoding="utf-8").count("supersedes:"), 1)

    def test_only_three_legacy_requirement_templates_are_transitionally_admitted(self) -> None:
        registry = json.loads(
            (REPOSITORY_ROOT / "docs/99.templates/registry.json").read_text(
                encoding="utf-8"
            )
        )
        transitional = {
            profile["id"]
            for profile in registry["profiles"]
            if profile["mode"] == "template"
            and profile["relationships"]["sourceProfileIds"]
            == ["sdlc/requirement-package"]
        }
        self.assertEqual(
            transitional,
            {"template/sdlc/prd", "template/sdlc/srs", "template/sdlc/interface"},
        )

    def test_architecture_paths_and_adr0030_relations_are_terminal(self) -> None:
        descriptions = REPOSITORY_ROOT / "docs/02.architecture/descriptions"
        self.assertEqual(list(descriptions.glob("ad-[0-9][0-9][0-9][0-9]-*.md")), [])
        self.assertEqual(len(list(descriptions.glob("[0-9][0-9][0-9][0-9]-*.md"))), 8)
        decision_root = REPOSITORY_ROOT / "docs/02.architecture/decisions"
        predecessor_ids = ("0015", "0018", "0019", "0023", "0024", "0025")
        successor = self._metadata(next(decision_root.glob("0030-*.md")))
        self.assertEqual(successor.get("supersedes"), "[ADR-0015, ADR-0018, ADR-0019, ADR-0023, ADR-0024, ADR-0025]")
        for identifier in predecessor_ids:
            metadata = self._metadata(next(decision_root.glob(f"{identifier}-*.md")))
            self.assertEqual(metadata.get("status"), "superseded")
            self.assertEqual(metadata.get("superseded_by"), "ADR-0030")

    def test_spec_packages_have_thin_routers_and_exact_task_union(self) -> None:
        packages = sorted(path for path in (REPOSITORY_ROOT / "docs/03.specs").iterdir() if path.is_dir())
        self.assertEqual(len(packages), 57)
        task_ids: list[str] = []
        task_paths: list[str] = []
        for package in packages:
            router = package / "README.md"
            self.assertTrue(router.is_file(), package.name)
            self.assertFalse(router.read_text(encoding="utf-8").startswith("---\n"))
            self.assertFalse((package / "agent-design.md").exists(), package.name)
            spec_number = package.name[:4]
            if spec_number == "0054":
                self.assertTrue((package / "tasks.md").is_file())
                continue
            self.assertFalse((package / "tasks.md").exists(), package.name)
            records = sorted((package / "tasks").glob("tsk-[0-9][0-9][0-9][0-9]-*.md")) if (package / "tasks").is_dir() else []
            self.assertEqual(len(records), self.TASK_COUNTS.get(spec_number, 0), package.name)
            for sequence, record in enumerate(records, 1):
                expected_id = f"TSK-{spec_number}-{sequence:04d}"
                self.assertEqual(record.name[4:8], f"{sequence:04d}")
                self.assertEqual(self._metadata(record).get("artifact_id"), expected_id)
                record_text = record.read_text(encoding="utf-8")
                self.assertLess(len(record_text.encode("utf-8")), 12_000)
                self.assertNotIn("**Forbidden Paths**", record_text)
                self.assertIn("Legacy Task approval and rollback boundaries", (package / "plan.md").read_text(encoding="utf-8"))
                task_ids.append(expected_id)
                task_paths.append(record.relative_to(REPOSITORY_ROOT).as_posix())
        self.assertEqual(len(task_ids), 315)
        self.assertEqual(len(task_ids), len(set(task_ids)))
        self.assertEqual(len(task_paths), len(set(task_paths)))

    def test_generated_task_links_resolve_from_the_task_record_depth(self) -> None:
        links = load_validator("wp004b_task_links", VALIDATOR_PATHS["links"])
        records = sorted(
            (REPOSITORY_ROOT / "docs/03.specs").glob(
                "[0-9][0-9][0-9][0-9]-*/tasks/tsk-*.md"
            )
        )
        self.assertEqual(len(records), 315)
        missing: list[tuple[str, str, str]] = []
        for record in records:
            relative = record.relative_to(REPOSITORY_ROOT).as_posix()
            for link in links.rendered_local_links(
                record.read_text(encoding="utf-8"), relative
            ):
                if (
                    link.kind == "local"
                    and link.target is not None
                    and not (REPOSITORY_ROOT / link.target).exists()
                ):
                    missing.append((relative, link.raw_target, link.target.as_posix()))
        self.assertEqual(missing, [])

    def test_spec0052_plan_traceability_targets_current_task_records(self) -> None:
        plan = (
            REPOSITORY_ROOT
            / "docs/03.specs/0052-document-taxonomy-consolidation/plan.md"
        ).read_text(encoding="utf-8")
        table = plan.split("### Lifecycle Traceability\n", 1)[1].split(
            "\n\n### Legacy Task traceability", 1
        )[0]
        rows = [line for line in table.splitlines() if line.startswith("| [VAL-")]
        self.assertEqual(len(rows), 16)
        self.assertNotIn("README.md#task-records", table)
        expected = {
            f"tasks/tsk-{(work - 99 if work < 104 else work - 98):04d}-work-{work:03d}.md"
            for work in range(100, 116)
        }
        actual = set(re.findall(r"\]\((tasks/tsk-[^)]+\.md)\)", table))
        self.assertTrue(expected.issubset(actual))

    def test_pinned_work054_history_composes_the_exact_retired_template_route(self) -> None:
        links = load_validator("wp004b_history_links", VALIDATOR_PATHS["links"])
        context = links._build_context(REPOSITORY_ROOT, ())
        _, move_targets, _ = links._document_taxonomy_transition_manifest(context)
        edges = links._reviewed_work054_historical_owner_edges(context, move_targets)
        source = PurePosixPath(
            "docs/03.specs/0015-agent-governance-contract-normalization/spec.md"
        )
        retired = PurePosixPath("docs/99.templates/support/template-routing.md")
        expected = PurePosixPath("docs/99.templates/support/document-contract.md")
        self.assertEqual(edges[links.ArchiveTransitionEdge(source, retired)], expected)

    def test_work105_post_state_admits_only_exact_mig0004_ard_history(self) -> None:
        registry = load_validator("wp004b_registry_history", VALIDATOR_PATHS["registry"])
        source = "docs/02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md"
        line = next(
            item
            for item in (REPOSITORY_ROOT / source).read_text(encoding="utf-8").splitlines()
            if "N/A — shared " + "AR" + "D 0006 source above" in item
        )
        self.assertTrue(
            registry._work054_wp004b_historical_ard_line(
                REPOSITORY_ROOT, source, line
            )
        )
        for wrong_source, wrong_line in (
            (
                "docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md",
                line,
            ),
            (
                "docs/98.archive/migrations/0004-document-authority-convergence.md",
                line,
            ),
            (source, line.replace("AR" + "D 0006", "AR" + "D 9999")),
            (
                source,
                "- **" + "AR" + "D**: [unreviewed](../descriptions/9999-unreviewed.md)",
            ),
        ):
            with self.subTest(source=wrong_source, line=wrong_line):
                self.assertFalse(
                    registry._work054_wp004b_historical_ard_line(
                        REPOSITORY_ROOT, wrong_source, wrong_line
                    )
                )

    def test_spec0033_historical_exception_resolves_terminal_requirement_and_ad(self) -> None:
        links = load_validator("wp004b_program_history", VALIDATOR_PATHS["links"])
        context = links._build_context(REPOSITORY_ROOT, ())
        self.assertEqual(
            links._program_owner_path(context, "sdlc/prd", "0005"),
            PurePosixPath(
                "docs/01.requirements/0005-workspace-document-assurance-modernization.md"
            ),
        )
        self.assertEqual(
            links._program_owner_path(context, "sdlc/ad", "0008"),
            PurePosixPath(
                "docs/02.architecture/descriptions/0008-workspace-document-assurance-operating-model.md"
            ),
        )
        registry = links.load_registry(REPOSITORY_ROOT)
        program = next(item for item in registry.program_lineage if item.prd_id == "0005")
        follow_up = next(item for item in program.follow_ups if item.spec_id == "0033")
        self.assertEqual(
            links._historical_exception_diagnostics(context, program, follow_up), []
        )
        current_requirement = links._program_owner_path(context, "sdlc/prd", "0005")
        self.assertIsNotNone(current_requirement)
        missing_context = links.replace(
            context,
            paths=tuple(path for path in context.paths if path != current_requirement),
            profiles={
                path: value
                for path, value in context.profiles.items()
                if path != current_requirement
            },
            texts={
                path: value
                for path, value in context.texts.items()
                if path != current_requirement
            },
            metadata={
                path: value
                for path, value in context.metadata.items()
                if path != current_requirement
            },
            tracked_regular_paths=frozenset(
                path
                for path in context.tracked_regular_paths
                if path != current_requirement
            ),
        )
        with self.assertRaises(links.ConfigurationError):
            links._historical_exception_diagnostics(
                missing_context, program, follow_up
            )
        wrong_contracts = {
            **links.PROGRAM_TRANSITION_OWNER_CONTRACTS,
            "sdlc/prd": (
                "sdlc/requirement-package",
                re.compile(r"^docs/01\.requirements/9999-[^/]+\.md$"),
            ),
        }
        with mock.patch.object(
            links, "PROGRAM_TRANSITION_OWNER_CONTRACTS", wrong_contracts
        ):
            self.assertEqual(
                links._program_owner_path(context, "sdlc/prd", "0005"), None
            )
            self.assertTrue(
                links._historical_exception_diagnostics(context, program, follow_up)
            )

    def test_program_execution_gate_uses_exact_package_local_task_sets(self) -> None:
        links = load_validator("wp004b_program_tasks", VALIDATOR_PATHS["links"])
        context = links._build_context(REPOSITORY_ROOT, ())
        gated_specs = {"0047", "0048", "0049", "0050", "0051", "0052"}
        projections: dict[str, tuple[object, object, bool]] = {}
        for spec_id in gated_specs:
            spec = links._program_owner_path(context, "sdlc/spec", spec_id)
            self.assertIsNotNone(spec)
            projection = (
                links._program_package_task_projection(context, spec)
            )
            projections[spec_id] = projection
            package_tasks, current_tasks, router_complete = projection
            self.assertTrue(router_complete, spec_id)
            self.assertGreaterEqual(len(package_tasks), len(current_tasks))
            if current_tasks:
                self.assertTrue(
                    all(
                        links._program_status(context, task)
                        in {"queued", "in-progress", "blocked"}
                        for task in current_tasks
                    )
                )
            else:
                self.assertTrue(
                    all(
                        links._program_status(context, task) in {"done", "cancelled"}
                        for task in package_tasks
                    )
                )

        spec = links._program_owner_path(context, "sdlc/spec", "0047")
        self.assertIsNotNone(spec)
        package_tasks, _, _ = projections["0047"]
        router = spec.parent / "README.md"
        router_text = context.texts[router]
        first_task = package_tasks[0]
        first_target = f"tasks/{first_task.name}"
        missing_text, count = re.subn(
            rf"(?m)^.*\]\({re.escape(first_target)}\)\n", "", router_text, count=1
        )
        self.assertEqual(count, 1)
        missing_context = links.replace(
            context, texts={**context.texts, router: missing_text}
        )
        self.assertFalse(
            links._program_package_task_projection(missing_context, spec)[2]
        )
        duplicate_context = links.replace(
            context,
            texts={
                **context.texts,
                router: router_text + f"\n- [duplicate]({first_target})\n",
            },
        )
        self.assertFalse(
            links._program_package_task_projection(duplicate_context, spec)[2]
        )
        foreign_task = projections["0048"][0][0]
        foreign_target = f"../{foreign_task.parent.parent.name}/tasks/{foreign_task.name}"
        foreign_context = links.replace(
            context,
            texts={
                **context.texts,
                router: router_text + f"\n- [foreign]({foreign_target})\n",
            },
        )
        self.assertFalse(
            links._program_package_task_projection(foreign_context, spec)[2]
        )
        wrong_metadata = {
            **context.metadata,
            first_task: {**context.metadata[first_task], "status": "active"},
        }
        wrong_state_context = links.replace(context, metadata=wrong_metadata)
        self.assertFalse(
            links._program_package_task_projection(wrong_state_context, spec)[2]
        )
        registry = links.load_registry(REPOSITORY_ROOT)
        diagnostics = links._program_lineage_diagnostics(
            context, registry.program_lineage, registry.standalone_executions
        )
        failures = [
            item
            for item in diagnostics
            if item.rule_id == "PROGRAM-LINEAGE-EXECUTION-GATE"
            and item.path.parts[2][:4] in gated_specs
        ]
        self.assertEqual(failures, [])

    def test_terminal_task_lifecycle_is_exact_and_legacy_status_stays_row_owned(self) -> None:
        registry = json.loads(
            (REPOSITORY_ROOT / "docs/99.templates/registry.json").read_text(
                encoding="utf-8"
            )
        )
        profiles = {profile["id"]: profile for profile in registry["profiles"]}
        terminal_domain = ["queued", "in-progress", "blocked", "done", "cancelled"]
        self.assertEqual(
            profiles["sdlc/task"]["lifecycle"]["statusDomain"], terminal_domain
        )
        self.assertEqual(
            profiles["template/sdlc/task"]["lifecycle"]["statusDomain"],
            terminal_domain,
        )

        task_root = REPOSITORY_ROOT / "docs/03.specs"
        records = sorted(task_root.glob("[0-9][0-9][0-9][0-9]-*/tasks/tsk-*.md"))
        self.assertEqual(len(records), 315)
        self.assertTrue(
            all(self._metadata(record).get("status") in terminal_domain for record in records)
        )
        nonterminal: list[str] = []
        for record in records:
            record_text = record.read_text(encoding="utf-8")
            task_table = record_text.split("## Task Table\n", 1)[1]
            self.assertRegex(task_table, r"(?m)^\| [^\n]+ \|$")
            if self._metadata(record).get("status") != "done":
                match = re.search(
                    r"### Lifecycle Traceability\n\n"
                    r"\| Criterion / work item \| Result \| Evidence \|\n"
                    r"\| --- \| --- \| --- \|\n"
                    r"\| N/A — legacy work item `([^`]+)` \|",
                    record_text,
                )
                self.assertIsNotNone(match, record)
                nonterminal.append(match.group(1))
        self.assertEqual(len(nonterminal), 34)
        self.assertEqual(len(nonterminal), len(set(nonterminal)))

    def test_spec0054_legacy_task_status_admission_is_one_exact_path_and_content(self) -> None:
        markdown = load_validator(
            "wp004b_markdown", VALIDATOR_PATHS["markdown"]
        )
        path = PurePosixPath(
            "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/tasks.md"
        )
        data = {
            "type": "sdlc/task",
            "status": "active",
            "artifact_id": "TASK-0054",
        }
        self.assertTrue(markdown._is_work054_transitional_task_status(path, data))
        self.assertFalse(
            markdown._is_work054_transitional_task_status(
                PurePosixPath("docs/03.specs/0053-example/tasks.md"), data
            )
        )
        for key, value in (
            ("type", "sdlc/plan"),
            ("status", "draft"),
            ("artifact_id", "TASK-9999"),
        ):
            changed = {**data, key: value}
            self.assertFalse(markdown._is_work054_transitional_task_status(path, changed))

    def test_mig0004_has_exact_unique_66_row_disposition(self) -> None:
        migration = REPOSITORY_ROOT / "docs/98.archive/migrations/0004-document-authority-convergence.md"
        self.assertTrue(migration.is_file())
        self.assertEqual(self._metadata(migration).get("status"), "sealed")
        text = migration.read_text(encoding="utf-8")
        marker = "<!-- archive-migration-ledger:v1 format=json -->\n\n```json\n"
        self.assertEqual(text.count(marker), 1)
        rows = json.loads(text.split(marker, 1)[1].split("\n```", 1)[0])
        self.assertEqual(len(rows), 66)
        legacy_paths = [row["legacy_path"] for row in rows]
        self.assertEqual(legacy_paths, sorted(legacy_paths))
        self.assertEqual(len(legacy_paths), len(set(legacy_paths)))
        task_rows = [row for row in rows if row["legacy_path"].endswith("/tasks.md")]
        self.assertEqual(len(task_rows), 48)
        self.assertTrue(all(row["action"] == "replaced" for row in task_rows))
        self.assertTrue(all(row["stable_path"] is None and row["artifact_id"] is None for row in task_rows))

    def test_current_sdlc_corpus_has_no_retired_execution_or_prefixed_ad_consumer(self) -> None:
        for stage in ("01.requirements", "02.architecture", "03.specs"):
            for path in (REPOSITORY_ROOT / "docs" / stage).rglob("*.md"):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("docs/04.execution/", text, path)
                self.assertIsNone(
                    re.search(r"(?:descriptions/|\()ad-(?:000[4-9]|001[01])-", text),
                    path,
                )


if __name__ == "__main__":
    unittest.main()
