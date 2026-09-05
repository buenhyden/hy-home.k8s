from __future__ import annotations

import contextlib
import importlib.util
import io
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path, PurePosixPath
from typing import Any
from unittest import mock

from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPOSITORY_ROOT / "scripts"
REGISTRY_PATH = REPOSITORY_ROOT / "docs/99.templates/registry.json"
PROFILE_SCHEMA_PATH = (
    REPOSITORY_ROOT / "docs/99.templates/contracts/document-profile.schema.json"
)
FRONTMATTER_SCHEMA_PATH = (
    REPOSITORY_ROOT / "docs/99.templates/contracts/frontmatter.schema.json"
)
VALIDATOR_PATHS = {
    "registry": SCRIPTS_ROOT / "validate-document-contract-registry.py",
    "lifecycle": SCRIPTS_ROOT / "validate-document-lifecycle.py",
    "markdown": SCRIPTS_ROOT / "validate-markdown-profiles.py",
    "links": SCRIPTS_ROOT / "validate-links-and-owners.py",
}
STAGE99_TEMPLATES_ROOT = REPOSITORY_ROOT / "docs/99.templates/templates"
STAGE05_ROOT = REPOSITORY_ROOT / "docs/05.operations"
SPEC0054_PACKAGE = (
    REPOSITORY_ROOT
    / "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation"
)
MIG0004_PATH = (
    REPOSITORY_ROOT
    / "docs/98.archive/migrations/0004-document-authority-convergence.md"
)
RETIRED_PROFILE_IDS = frozenset(
    {
        "sdlc/prd",
        "sdlc/srs",
        "sdlc/interface",
        "sdlc/agent-design",
        "sdlc/tests",
        "sdlc/release",
        "governance/template-support",
        "template/sdlc/prd",
        "template/sdlc/srs",
        "template/sdlc/interface",
        "template/sdlc/agent-design",
        "template/sdlc/tests",
        "template/sdlc/release",
        "template/governance/template-support",
        "governance/progress-ledger",
        "governance/progress-entry",
        "governance/memory",
        "template/governance/memory",
        "sdlc/data-model",
        "governance/control",
        "common/native-contract-openapi",
        "common/native-contract-graphql",
        "common/native-contract-protobuf",
    }
)
DELIBERATELY_EMPTY_PROFILE_IDS = frozenset(
    {
        "operation/incident",
        "operation/postmortem",
        "reference/audit",
        "reference/data",
        "common/readme-audit-pack",
        "common/readme-data-pack",
    }
)
RETIRED_UNUSED_CAPACITY_PROFILE_IDS = frozenset(
    {
        "sdlc/data-model",
        "governance/control",
        "common/native-contract-openapi",
        "common/native-contract-graphql",
        "common/native-contract-protobuf",
    }
)
RETIRED_UNUSED_CAPACITY_FORM_PATHS = frozenset(
    {
        "docs/99.templates/templates/specs/contracts/data-model.template.md",
        "docs/99.templates/templates/governance/control.template.md",
        "docs/99.templates/templates/specs/contracts/openapi.template.yaml",
        "docs/99.templates/templates/specs/contracts/schema.template.graphql",
        "docs/99.templates/templates/specs/contracts/service.template.proto",
    }
)
DOCUMENT_FAMILIES = frozenset(
    {"common", "governance", "sdlc", "operation", "reference", "archive"}
)
COMMON_FRONTMATTER_PREFIX = [
    "title",
    "version",
    "type",
    "status",
    "owner",
    "updated",
]


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


def load_document_contracts():
    return load_validator("terminal_contracts", SCRIPTS_ROOT / "document_contracts.py")


def clone_registry(registry: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(registry))


def migration_rows() -> list[dict[str, Any]]:
    contents = MIG0004_PATH.read_text(encoding="utf-8")
    return json.loads(contents.split("```json\n", 1)[1].split("\n```", 1)[0])


class Stage99TerminalAuthorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_v9_registry_uses_the_common_public_model(self) -> None:
        self.assertEqual(
            set(self.registry),
            {"$id", "$schema", "schema_version", "profiles", "lifecycle_domains"},
        )
        self.assertEqual(self.registry["schema_version"], 9)
        self.assertNotIn("programLineage", self.registry)
        self.assertNotIn("standaloneExecutions", self.registry)
        for profile in self.registry["profiles"]:
            with self.subTest(profile=profile["id"]):
                self.assertIn(profile["family"], DOCUMENT_FAMILIES)
                self.assertEqual(profile["id"].split("/", 1)[0], profile["family"])
                self.assertIn("path_pattern", profile)
                self.assertIn("template_source", profile)
                self.assertIn("frontmatter", profile)
                self.assertIn("sections", profile)
                self.assertIn("placeholder_policy", profile)
                self.assertNotIn("pathPattern", profile)
                self.assertNotIn("requiredFrontmatter", profile)
                self.assertNotIn("requiredSections", profile)

    def test_governed_readmes_use_identity_free_envelopes(self) -> None:
        readmes = [
            profile
            for profile in self.registry["profiles"]
            if profile["id"].startswith("common/readme-")
            and profile["mode"] == "router"
        ]
        self.assertTrue(readmes)
        for profile in readmes:
            with self.subTest(profile=profile["id"]):
                frontmatter = profile["frontmatter"]
                self.assertEqual(frontmatter["mode"], "required")
                self.assertEqual(
                    frontmatter["order"][: len(COMMON_FRONTMATTER_PREFIX)],
                    COMMON_FRONTMATTER_PREFIX,
                )
                self.assertNotIn("artifact_id", frontmatter["required"])
                self.assertIn("artifact_id", frontmatter["forbidden"])
                self.assertIsNone(profile["artifact_id_pattern"])
                self.assertIsNone(profile["lifecycle"])

    def test_authored_frontmatter_uses_one_common_prefix(self) -> None:
        for profile in self.registry["profiles"]:
            if profile["mode"] not in {"authored", "router"}:
                continue
            with self.subTest(profile=profile["id"]):
                frontmatter = profile["frontmatter"]
                self.assertEqual(
                    frontmatter["order"][: len(COMMON_FRONTMATTER_PREFIX)],
                    COMMON_FRONTMATTER_PREFIX,
                )
                self.assertEqual(frontmatter["constants"].get("type"), profile["id"])

    def test_templates_use_only_current_placeholder_grammars(self) -> None:
        legacy_markdown = re.compile(
            r"(?:(?<!\{)\{[A-Za-z][^{}]*\}(?!\})|#\.#[.#]*|\b(?:[A-Z]+-)?#{4}\b|YYYY-MM-DD)"
        )
        current_markdown = re.compile(r"\{\{[A-Z][A-Z0-9_]*\}\}")
        current_native = re.compile(r"__[A-Z][A-Z0-9_]*__")
        for path in STAGE99_TEMPLATES_ROOT.rglob("*"):
            if not path.is_file() or path.name == "README.md":
                continue
            text = path.read_text(encoding="utf-8")
            with self.subTest(template=path.relative_to(REPOSITORY_ROOT).as_posix()):
                self.assertIsNone(legacy_markdown.search(text))
                placeholders = re.findall(r"\{\{[^{}]+\}\}", text)
                self.assertTrue(
                    all(current_markdown.fullmatch(item) for item in placeholders)
                )
                native = re.findall(r"__[A-Za-z0-9_]+__", text)
                self.assertTrue(all(current_native.fullmatch(item) for item in native))

    def test_release_evidence_remains_external(self) -> None:
        profile_ids = {profile["id"] for profile in self.registry["profiles"]}
        self.assertNotIn("operation/release", profile_ids)
        self.assertFalse(
            any(
                "release.template" in (profile["template_source"] or "")
                for profile in self.registry["profiles"]
            )
        )

    def test_terminal_stage99_topology_is_exact(self) -> None:
        stage99 = REPOSITORY_ROOT / "docs/99.templates"
        self.assertEqual(
            sorted(path.name for path in stage99.iterdir()),
            ["README.md", "contracts", "registry.json", "templates"],
        )
        self.assertEqual(
            sorted(path.name for path in (stage99 / "contracts").iterdir()),
            ["document-profile.schema.json", "frontmatter.schema.json"],
        )
        self.assertEqual(
            sorted(path.name for path in (stage99 / "templates").iterdir()),
            [
                "README.md",
                "architecture",
                "archive",
                "common",
                "governance",
                "operations",
                "references",
                "requirements",
                "runtime",
                "specs",
            ],
        )

    def test_root_registry_is_the_single_closed_machine_authority(self) -> None:
        self.assertEqual(
            set(self.registry),
            {
                "$id",
                "$schema",
                "lifecycle_domains",
                "profiles",
                "schema_version",
            },
        )
        profile_ids = [profile["id"] for profile in self.registry["profiles"]]
        self.assertEqual(len(profile_ids), len(set(profile_ids)))
        self.assertTrue(
            {
                "reference/audit",
                "reference/data",
                "reference/research",
                "common/readme-audit-pack",
                "common/readme-data-pack",
                "common/readme-research-pack",
                "operation/incident",
                "operation/postmortem",
            }.issubset(profile_ids)
        )

        lifecycle_families = [
            domain["family"] for domain in self.registry["lifecycle_domains"]
        ]
        self.assertEqual(len(lifecycle_families), len(set(lifecycle_families)))
        # Forms do not transition: the lifecycle state machine skips
        # `mode: template`, so a transition graph for them asserted movement
        # that cannot happen.  Migration and tombstone are separate families
        # because a migration progresses and a tombstone is created finished.
        self.assertTrue(
            {"incident", "postmortem", "task", "migration", "tombstone"}.issubset(
                lifecycle_families
            )
        )
        self.assertNotIn("template-profile", lifecycle_families)

    def test_only_unused_capacity_profiles_and_forms_are_retired(self) -> None:
        profile_ids = {profile["id"] for profile in self.registry["profiles"]}
        self.assertTrue(DELIBERATELY_EMPTY_PROFILE_IDS.issubset(profile_ids))
        self.assertTrue(RETIRED_UNUSED_CAPACITY_PROFILE_IDS.isdisjoint(profile_ids))
        frontmatter_schema = FRONTMATTER_SCHEMA_PATH.read_text(encoding="utf-8")
        self.assertNotIn("DATA-MODEL-[0-9]", frontmatter_schema)
        for relative_path in RETIRED_UNUSED_CAPACITY_FORM_PATHS:
            with self.subTest(form=relative_path):
                self.assertFalse((REPOSITORY_ROOT / relative_path).exists())

    def test_retired_capacity_documents_and_executables_have_no_current_owner(
        self,
    ) -> None:
        contracts = load_document_contracts()
        registry = contracts.load_registry(REPOSITORY_ROOT)
        retired_surfaces = (
            "docs/00.agent-governance/controls/duplicate-rule.md",
            "docs/03.specs/9999-example/data-model.md",
            "docs/03.specs/9999-example/contracts/openapi.yaml",
            "docs/03.specs/9999-example/contracts/schema.graphql",
            "docs/03.specs/9999-example/contracts/service.proto",
        )
        for relative_path in retired_surfaces:
            with (
                self.subTest(path=relative_path),
                self.assertRaises(contracts.DocumentContractError),
            ):
                contracts.classify_path(registry, PurePosixPath(relative_path))

    def test_stage99_authority_rejects_restored_unused_capacity_profiles(
        self,
    ) -> None:
        authority = load_document_authority()
        profiles_by_family = {
            profile["family"]: profile for profile in self.registry["profiles"]
        }
        for profile_id in sorted(RETIRED_UNUSED_CAPACITY_PROFILE_IDS):
            with self.subTest(profile=profile_id):
                registry = clone_registry(self.registry)
                if profile_id not in {
                    profile["id"] for profile in registry["profiles"]
                }:
                    family = profile_id.split("/", 1)[0]
                    restored = clone_registry(profiles_by_family[family])
                    restored["id"] = profile_id
                    restored["lifecycle"] = None
                    registry["profiles"].append(restored)
                with self.assertRaisesRegex(
                    authority.AuthorityError,
                    "RETIRED_UNUSED_CAPACITY_PROFILE",
                ):
                    authority.validate_registry_authority(registry)

    def test_profile_schema_accepts_terminal_registry(self) -> None:
        schema = json.loads(PROFILE_SCHEMA_PATH.read_text(encoding="utf-8"))
        errors = sorted(
            Draft202012Validator(schema).iter_errors(self.registry),
            key=lambda error: list(error.absolute_path),
        )
        self.assertEqual(errors, [])

    def test_v9_archive_no_successor_uses_one_unambiguous_literal(self) -> None:
        schema = json.loads(FRONTMATTER_SCHEMA_PATH.read_text(encoding="utf-8"))
        replacement_schema = {
            "$defs": schema["$defs"],
            **schema["properties"]["replacement"],
        }
        validator = Draft202012Validator(replacement_schema)
        self.assertEqual(list(validator.iter_errors("none")), [])
        self.assertEqual(
            list(validator.iter_errors("docs/03.specs/0054-example/spec.md")),
            [],
        )
        self.assertTrue(list(validator.iter_errors(None)))

    def test_profile_schema_rejects_a_retired_contract_plane(self) -> None:
        schema = json.loads(PROFILE_SCHEMA_PATH.read_text(encoding="utf-8"))
        mutated = json.loads(json.dumps(self.registry))
        mutated["documentContracts"] = {"valueContracts": []}
        errors = list(Draft202012Validator(schema).iter_errors(mutated))
        self.assertTrue(errors)
        self.assertTrue(
            any(error.validator == "additionalProperties" for error in errors)
        )

    def test_terminal_templates_are_profile_led(self) -> None:
        profiles = {profile["id"]: profile for profile in self.registry["profiles"]}
        self.assertTrue(RETIRED_PROFILE_IDS.isdisjoint(profiles))
        for profile in profiles.values():
            template = profile.get("template_source")
            if not template:
                continue
            template_path = REPOSITORY_ROOT / template
            with self.subTest(profile=profile["id"], template=template):
                self.assertTrue(template_path.is_file())
                self.assertNotIn("/templates/sdlc/", template)
                contents = template_path.read_text(encoding="utf-8")
                self.assertNotRegex(
                    contents,
                    r"(?im)^\s*<!--\s*(?:destination|target-path)\s*:",
                )
                match = re.search(r"(?m)^type:\s*[\"']?([^\"'\s]+)", contents)
                if match is not None:
                    self.assertIn(match.group(1), profiles)

    def test_retired_stage99_paths_are_not_profile_routes(self) -> None:
        source = (SCRIPTS_ROOT / "document_contracts.py").read_text(encoding="utf-8")
        self.assertNotIn("route-contract.json", source)
        self.assertNotIn("support/document-profiles.json", source)
        collection_profile = next(
            profile
            for profile in self.registry["profiles"]
            if profile["id"] == "common/readme-collection-index"
        )
        self.assertNotIn(
            "docs/99\\.templates/support", collection_profile["path_pattern"]
        )
        # The form catalog is a route again.  MIG-0004 retired a support-era
        # document, not the location: the row pins the bytes it retired, and the
        # archive control refuses those bytes returning rather than the path.
        self.assertIn(
            "docs/99\\.templates/templates/README",
            collection_profile["path_pattern"],
        )
        catalog = REPOSITORY_ROOT / "docs/99.templates/templates/README.md"
        self.assertNotEqual(
            hashlib.sha256(catalog.read_bytes()).hexdigest(),
            "568c84c88ab19c876aa4416660853005130631b088061b81b713cc71a6e5d097",  # pragma: allowlist secret
        )

    def test_stage99_support_prose_cannot_be_a_machine_owner(self) -> None:
        authority = load_document_authority()
        registry = json.loads(json.dumps(self.registry))
        registry["profiles"][0]["path_pattern"] = (
            "^docs/99\\.templates/support/document-contract\\.md$"
        )
        with self.assertRaisesRegex(authority.AuthorityError, "STAGE99_SUPPORT_OWNER"):
            authority.validate_registry_authority(registry)

    def test_stage99_registry_rejects_agent_roster_fields(self) -> None:
        authority = load_document_authority()
        registry = json.loads(json.dumps(self.registry))
        registry["profiles"][0]["permissions"] = ["write"]
        with self.assertRaisesRegex(authority.AuthorityError, "STAGE99_AGENT_FIELD"):
            authority.validate_registry_authority(registry)

    def test_template_references_a_profile_not_a_destination(self) -> None:
        authority = load_document_authority()
        with self.assertRaisesRegex(authority.AuthorityError, "TEMPLATE_DESTINATION"):
            authority.validate_template_profile_reference(
                "<!-- destination: docs/03.specs/9999-example/spec.md -->\n",
                self.registry,
            )

    def test_production_authority_scans_mutated_real_template(self) -> None:
        authority = load_document_authority()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry_path = root / authority.REGISTRY_PATH
            registry_path.parent.mkdir(parents=True)
            shutil.copy2(REGISTRY_PATH, registry_path)
            shutil.copytree(
                STAGE99_TEMPLATES_ROOT,
                root / "docs/99.templates/templates",
            )
            template = root / "docs/99.templates/templates/specs/spec.template.md"
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

    def test_router_profiles_have_identity_free_null_fields(self) -> None:
        routers = [
            profile
            for profile in self.registry["profiles"]
            if profile["mode"] == "router"
        ]
        self.assertTrue(routers)
        for profile in routers:
            with self.subTest(profile=profile["id"]):
                self.assertIsNone(profile["artifact_id_pattern"])
                self.assertIsNone(profile["lifecycle"])
                self.assertIn("artifact_id", profile["frontmatter"]["forbidden"])

    def test_root_registry_loader_exposes_terminal_profile_contract(self) -> None:
        contracts = load_document_contracts()
        registry = contracts.load_registry(REPOSITORY_ROOT)
        requirement = next(
            profile
            for profile in registry.profiles
            if profile.profile_id == "sdlc/requirement"
        )
        self.assertEqual(requirement.frontmatter.required[-1], "artifact_id")
        self.assertEqual(requirement.artifact_id_pattern, "^REQ-[0-9]{4}$")
        self.assertIsNotNone(requirement.lifecycle_domain)
        self.assertIn(("draft", "active"), requirement.lifecycle_domain.transitions)

    def test_terminal_profile_relationships_reject_unknown_sources(self) -> None:
        contracts = load_document_contracts()
        registry = clone_registry(self.registry)
        registry["profiles"][0]["relationships"]["source_profile_ids"] = [
            "sdlc/unknown"
        ]
        with self.assertRaisesRegex(
            contracts.DocumentContractError, "REGISTRY_SOURCE_PROFILE"
        ):
            contracts.validate_registry(REPOSITORY_ROOT, registry)

    def test_terminal_profile_patterns_must_compile(self) -> None:
        contracts = load_document_contracts()
        mutations = {
            "path-pattern": (
                "REGISTRY_ROUTE_REGEX",
                lambda profile: profile.update(path_pattern="^[$"),
            ),
            "artifact-id-pattern": (
                "REGISTRY_ARTIFACT_ID_PATTERN",
                lambda profile: profile.update(artifact_id_pattern="^[$"),
            ),
        }
        for name, (rule_id, mutate) in mutations.items():
            registry = clone_registry(self.registry)
            mutate(registry["profiles"][0])
            with self.subTest(name=name):
                with self.assertRaisesRegex(contracts.DocumentContractError, rule_id):
                    contracts.validate_registry(REPOSITORY_ROOT, registry)

    def test_a_form_declares_no_status_domain_of_its_own(self) -> None:
        # The loader replaces a form's status domain with its source profile's,
        # so a domain written on the form governs nothing. Sixteen of them had
        # drifted unnoticed, one carrying the incident vocabulary on an
        # architecture description. A form declares none and inherits one.
        contracts = load_document_contracts()
        registry = clone_registry(self.registry)
        form = next(
            profile for profile in registry["profiles"] if profile["mode"] == "template"
        )
        self.assertIsNone(form["lifecycle"])
        form["lifecycle"] = {"status_domain": ["draft"]}
        with self.assertRaisesRegex(
            contracts.DocumentContractError, "REGISTRY_FORM_STATUS_DOMAIN"
        ):
            contracts.validate_registry(REPOSITORY_ROOT, registry)

    def test_a_form_enforces_only_statuses_its_source_admits(self) -> None:
        # The check compared a form's enforced statuses against themselves, so
        # it could not fail. It now compares them against the domain the form
        # actually inherits.
        contracts = load_document_contracts()
        registry = clone_registry(self.registry)
        form = next(
            profile
            for profile in registry["profiles"]
            if profile["id"] == "common/template-operation-incident"
        )
        form["relationships"]["body_contract"]["enforced_statuses"] = ["retired"]
        with self.assertRaisesRegex(
            contracts.DocumentContractError, "REGISTRY_BODY_STATUS"
        ):
            contracts.validate_registry(REPOSITORY_ROOT, registry)

    def test_terminal_body_relationship_invariants_fail_closed(self) -> None:
        contracts = load_document_contracts()

        def mutate_body(registry: dict[str, Any]) -> dict[str, Any]:
            return registry["profiles"][1]["relationships"]["body_contract"]

        mutations = {
            "section": (
                "REGISTRY_BODY_SECTION",
                lambda body: body.update(section="Missing section"),
            ),
            "status": (
                "REGISTRY_BODY_STATUS",
                lambda body: body.update(enforced_statuses=["unknown"]),
            ),
            "identifier-column": (
                "REGISTRY_BODY_IDENTIFIER_COLUMN",
                lambda body: body.update(
                    identifier_columns=[
                        {"column": "Missing column", "kind": "requirement"}
                    ]
                ),
            ),
            "source-link-column": (
                "REGISTRY_BODY_SOURCE_PROFILE",
                lambda body: body.update(source_link_column="Missing column"),
            ),
            "unknown-target-profile": (
                "REGISTRY_BODY_TARGET_PROFILE",
                lambda body: body.update(allowed_target_profile_ids=["sdlc/unknown"]),
            ),
            "reciprocal-without-link": (
                "REGISTRY_BODY_RECIPROCAL",
                lambda body: body.update(
                    source_link_column=None,
                    target_link_column=None,
                    allowed_source_profile_ids=[],
                    allowed_target_profile_ids=[],
                ),
            ),
        }
        for name, (rule_id, mutate) in mutations.items():
            registry = clone_registry(self.registry)
            mutate(mutate_body(registry))
            with self.subTest(name=name):
                with self.assertRaisesRegex(contracts.DocumentContractError, rule_id):
                    contracts.validate_registry(REPOSITORY_ROOT, registry)

    def test_terminal_lifecycle_domains_reject_unknown_or_duplicate_profiles(
        self,
    ) -> None:
        contracts = load_document_contracts()
        mutations = {
            "unknown": lambda domains: domains[0]["profile_ids"].append("sdlc/unknown"),
            "duplicate": lambda domains: domains[1]["profile_ids"].append(
                "sdlc/requirement"
            ),
        }
        for name, mutate in mutations.items():
            registry = clone_registry(self.registry)
            mutate(registry["lifecycle_domains"])
            with self.subTest(name=name):
                with self.assertRaisesRegex(
                    contracts.DocumentContractError, "REGISTRY_LIFECYCLE_DOMAIN"
                ):
                    contracts.validate_registry(REPOSITORY_ROOT, registry)

    def test_authored_lifecycle_profiles_have_one_exact_state_classification(
        self,
    ) -> None:
        profiles = {
            profile["id"]: profile
            for profile in self.registry["profiles"]
            if profile["mode"] == "authored" and profile["lifecycle"] is not None
        }
        domains = self.registry["lifecycle_domains"]
        assignments = {
            profile_id: domain
            for domain in domains
            for profile_id in domain["profile_ids"]
        }
        self.assertTrue(all(domain["profile_ids"] for domain in domains))
        self.assertTrue(set(profiles).issubset(assignments))
        for profile_id, profile in profiles.items():
            with self.subTest(profile=profile_id):
                self.assertEqual(
                    set(profile["lifecycle"]["status_domain"]),
                    set(assignments[profile_id]["states"]),
                )

    def test_retired_program_and_standalone_planes_are_absent(self) -> None:
        contracts = load_document_contracts()
        self.assertNotIn("programLineage", self.registry)
        self.assertNotIn("standaloneExecutions", self.registry)
        typed = contracts.load_registry(REPOSITORY_ROOT)
        self.assertEqual(typed.program_lineage, ())
        self.assertEqual(typed.standalone_executions, ())

    def test_terminal_templates_must_be_regular_non_symlink_files(self) -> None:
        contracts = load_document_contracts()
        missing = clone_registry(self.registry)
        missing["profiles"][0]["template_source"] = (
            "docs/99.templates/templates/requirements/missing.template.md"
        )
        with self.assertRaisesRegex(
            contracts.DocumentContractError, "REGISTRY_TEMPLATE"
        ):
            contracts.validate_registry(REPOSITORY_ROOT, missing)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            schema = root / contracts.PROFILE_SCHEMA_PATH
            schema.parent.mkdir(parents=True)
            shutil.copy2(PROFILE_SCHEMA_PATH, schema)
            templates = root / "docs/99.templates/templates"
            shutil.copytree(STAGE99_TEMPLATES_ROOT, templates)
            linked_template = templates / "requirements/linked.template.md"
            linked_template.symlink_to(
                templates / "requirements/requirement-package.template.md"
            )
            linked = clone_registry(self.registry)
            linked["profiles"][0]["template_source"] = linked_template.relative_to(
                root
            ).as_posix()
            with self.assertRaisesRegex(
                contracts.DocumentContractError, "REGISTRY_TEMPLATE"
            ):
                contracts.validate_registry(root, linked)

    def test_load_registry_uses_terminal_semantic_validation(self) -> None:
        contracts = load_document_contracts()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry = clone_registry(self.registry)
            registry["profiles"][0]["relationships"]["source_profile_ids"] = [
                "sdlc/unknown"
            ]
            registry_path = root / contracts.REGISTRY_PATH
            schema_path = root / contracts.PROFILE_SCHEMA_PATH
            registry_path.parent.mkdir(parents=True)
            schema_path.parent.mkdir(parents=True, exist_ok=True)
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            shutil.copy2(PROFILE_SCHEMA_PATH, schema_path)
            shutil.copytree(
                STAGE99_TEMPLATES_ROOT,
                root / "docs/99.templates/templates",
            )
            with self.assertRaisesRegex(
                contracts.DocumentContractError, "REGISTRY_SOURCE_PROFILE"
            ):
                contracts.load_registry(root)

    def test_spec0054_common_execution_contract_lives_in_its_plan(self) -> None:
        """The shared execution contract has an authorized owner, not a router.

        It used to sit under an ``H2`` the package router profile had to allow
        by name.  The router retired, so the Plan that already owns the
        package's execution boundary carries it under ``Global Constraints``
        and the Plan profile authorizes it without a form-specific exception.
        """

        markdown = load_validator(
            "common_execution_contract", VALIDATOR_PATHS["markdown"]
        )
        registry = markdown.load_registry(REPOSITORY_ROOT)
        path = PurePosixPath(
            "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation"
            "/plan.md"
        )
        contents = (REPOSITORY_ROOT / path).read_text(encoding="utf-8")
        self.assertIn("\n## Global Constraints\n", contents)
        self.assertIn("\n### Common Execution Contract\n", contents)
        self.assertNotIn("\n## Common Execution Contract\n", contents)

        profile = markdown.classify_path(registry, path)
        self.assertEqual(profile.profile_id, "sdlc/plan")
        self.assertNotIn("Common Execution Contract", profile.headings.allowed)
        self.assertEqual(
            markdown.validate_document(REPOSITORY_ROOT, path, profile, "strict"),
            [],
        )

    def test_current_frontmatter_requires_double_quoted_values(self) -> None:
        markdown = load_validator("frontmatter_quote", VALIDATOR_PATHS["markdown"])
        registry = markdown.load_registry(REPOSITORY_ROOT)
        path = PurePosixPath(
            "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation"
            "/plan.md"
        )
        profile = markdown.classify_path(registry, path)
        source = (REPOSITORY_ROOT / path).read_text(encoding="utf-8")
        diagnostics = markdown.validate_document_text(
            source.replace('owner: "platform"', "owner: platform", 1),
            path,
            profile,
            "strict",
        )
        self.assertIn("FM-QUOTE", {item.rule_id for item in diagnostics})

    def test_artifact_id_validation_uses_profile_pattern(self) -> None:
        markdown = load_validator("artifact_id_contract", VALIDATOR_PATHS["markdown"])
        registry = markdown.load_registry(REPOSITORY_ROOT)
        path = PurePosixPath(
            "docs/01.requirements/0001-argo-rollouts-progressive-delivery.md"
        )
        profile = markdown.classify_path(registry, path)
        source = (REPOSITORY_ROOT / path).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / path
            target.parent.mkdir(parents=True)
            target.write_text(
                source.replace('artifact_id: "REQ-0001"', 'artifact_id: "FR-0001"'),
                encoding="utf-8",
            )
            diagnostics = markdown.validate_document(root, path, profile, "strict")
        self.assertIn(
            "FM-VALUE-PATTERN",
            {diagnostic.rule_id for diagnostic in diagnostics},
        )

    def test_requirement_package_artifact_id_matches_path_number(self) -> None:
        markdown = load_validator(
            "requirement_package_identity", VALIDATOR_PATHS["markdown"]
        )
        registry = markdown.load_registry(REPOSITORY_ROOT)
        path = PurePosixPath(
            "docs/01.requirements/0001-argo-rollouts-progressive-delivery.md"
        )
        profile = markdown.classify_path(registry, path)
        source = (REPOSITORY_ROOT / path).read_text(encoding="utf-8")
        for artifact_id in ("PRD-0001", "SRS-0001", "IFC-0001", "REQ-0002"):
            with (
                self.subTest(artifact_id=artifact_id),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                target = root / path
                target.parent.mkdir(parents=True)
                target.write_text(
                    source.replace(
                        'artifact_id: "REQ-0001"', f'artifact_id: "{artifact_id}"'
                    ),
                    encoding="utf-8",
                )
                rule_ids = {
                    diagnostic.rule_id
                    for diagnostic in markdown.validate_document(
                        root, path, profile, "strict"
                    )
                }
            self.assertIn("REQUIREMENT-PACKAGE-IDENTITY", rule_ids)

    def test_requirement_package_member_ids_are_full_and_package_bound(self) -> None:
        markdown = load_validator(
            "requirement_package_members", VALIDATOR_PATHS["markdown"]
        )
        registry = markdown.load_registry(REPOSITORY_ROOT)
        path = PurePosixPath(
            "docs/01.requirements/0001-argo-rollouts-progressive-delivery.md"
        )
        profile = markdown.classify_path(registry, path)
        source = (REPOSITORY_ROOT / path).read_text(encoding="utf-8")

        mutations = {
            "wrong-package": (
                "REQ-0002-FR-0001",
                "REQUIREMENT-PACKAGE-MEMBER-ID",
            ),
            "abbreviated": ("FR-0001", "BODY-CONTRACT-IDENTIFIER"),
        }
        for name, (identifier, expected_rule) in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                target = root / path
                target.parent.mkdir(parents=True)
                target.write_text(
                    source.replace("REQ-0001-FR-0001", identifier),
                    encoding="utf-8",
                )
                rule_ids = {
                    diagnostic.rule_id
                    for diagnostic in markdown.validate_document(
                        root, path, profile, "strict"
                    )
                }
            self.assertIn(expected_rule, rule_ids)

        for identifier in (
            "REQ-0001-FR-0001",
            "REQ-0001-NFR-0001",
            "REQ-0001-IF-0001",
        ):
            with (
                self.subTest(identifier=identifier),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                target = root / path
                target.parent.mkdir(parents=True)
                target.write_text(
                    source.replace("REQ-0001-FR-0001", identifier),
                    encoding="utf-8",
                )
                rule_ids = {
                    diagnostic.rule_id
                    for diagnostic in markdown.validate_document(
                        root, path, profile, "strict"
                    )
                }
            self.assertNotIn("BODY-CONTRACT-IDENTIFIER", rule_ids)
            self.assertNotIn("REQUIREMENT-PACKAGE-MEMBER-ID", rule_ids)

    def test_current_traceability_headers_and_template_requirement_ids_are_exact(
        self,
    ) -> None:
        profiles = {profile["id"]: profile for profile in self.registry["profiles"]}
        for profile_id in (
            "sdlc/spec",
            "common/template-sdlc-spec",
        ):
            with self.subTest(profile=profile_id):
                body_contract = profiles[profile_id]["relationships"]["body_contract"]
                self.assertEqual(body_contract["required_columns"][0], "Requirement ID")
                self.assertEqual(
                    body_contract["identifier_columns"][0]["column"],
                    "Requirement ID",
                )
                self.assertEqual(body_contract["source_link_column"], "Requirement ID")

        for relative_path in (
            "requirements/requirement-package.template.md",
            "architecture/description.template.md",
            "specs/spec.template.md",
        ):
            contents = (STAGE99_TEMPLATES_ROOT / relative_path).read_text(
                encoding="utf-8"
            )
            with self.subTest(template=relative_path):
                self.assertNotIn("REQ-FEATURE-001", contents)
                self.assertRegex(contents, r"REQ-0001-(?:FR|NFR|IF)-0001")
        self.assertIn(
            'artifact_id: "{{ARTIFACT_ID}}"',
            (
                STAGE99_TEMPLATES_ROOT / "requirements/requirement-package.template.md"
            ).read_text(encoding="utf-8"),
        )

    def test_document_validators_have_no_embedded_self_test_switch(self) -> None:
        for name, path in VALIDATOR_PATHS.items():
            source = path.read_text(encoding="utf-8")
            with self.subTest(validator=name):
                self.assertNotIn('add_argument("--self-test"', source)

    def test_spec0054_has_exact_append_only_task_records(self) -> None:
        self.assertFalse((SPEC0054_PACKAGE / "tasks.md").exists())
        records = sorted((SPEC0054_PACKAGE / "tasks").glob("tsk-*.md"))
        self.assertEqual(len(records), 14)
        for index, record in enumerate(records, 1):
            contents = record.read_text(encoding="utf-8")
            with self.subTest(record=record.name):
                self.assertEqual(record.name[4:8], f"{index:04d}")
                self.assertIn(f'artifact_id: "SPEC-0054-TSK-{index:04d}"', contents)
                self.assertIn("../plan.md#common-execution-contract", contents)
                for section in (
                    "## Task Table",
                    "## Approval and Safety Boundaries",
                    "## Verification Summary",
                    "## Traceability",
                ):
                    self.assertIn(section, contents)

    def test_root_readme_routes_package_tasks_to_task_records(self) -> None:
        contents = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("docs/03.specs/<id>-<slug>/tasks.md", contents)
        self.assertIn(
            "docs/03.specs/<id>-<slug>/tasks/tsk-####-<slug>.md",
            contents,
        )

    def test_mig0004_recovers_one_retired_spec0054_ledger(self) -> None:
        rows = [
            row
            for row in migration_rows()
            if row["legacy_path"].endswith(
                "0054-sdlc-document-and-agent-governance-consolidation/tasks.md"
            )
        ]
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["action"], "replaced")
        self.assertEqual(
            row["replacement"],
            "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/README.md",
        )
        self.assertEqual(
            row["source_commit"],
            "7a770c3c0eabaeda554c4030fc08fb17de164fe5",  # pragma: allowlist secret - pinned Git commit fixture
        )
        self.assertEqual(
            row["source_blob"],
            "465f24340b99c03a38b5150d517627b69fa7c717",  # pragma: allowlist secret - pinned Git blob fixture
        )
        self.assertEqual(
            row["content_sha256"],
            "3fd4925824ad0b92748ff0f27e3a252dee3619c415caff02cc59a385e4c8fc08",  # pragma: allowlist secret - pinned SHA-256 recovery fixture
        )


class Stage05TerminalOwnershipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_terminal_guide_owner_is_singular(self) -> None:
        guides = sorted(
            path.name
            for path in (STAGE05_ROOT / "guides").glob("*.md")
            if path.name != "README.md"
        )
        self.assertEqual(guides, ["0010-ci-cd-qa-reference-guide.md"])
        self.assertFalse((STAGE05_ROOT / "releases").exists())

    def test_operation_artifact_ids_match_path_numbers(self) -> None:
        seen: set[str] = set()
        for directory, prefix in (
            ("guides", "GDE"),
            ("policies", "POL"),
            ("runbooks", "RUN"),
        ):
            for path in sorted((STAGE05_ROOT / directory).glob("*.md")):
                if path.name == "README.md":
                    continue
                contents = path.read_text(encoding="utf-8")
                match = re.search(
                    r"(?m)^artifact_id:\s*[\"']?([^\"'\s]+)",
                    contents,
                )
                with self.subTest(path=path.relative_to(REPOSITORY_ROOT).as_posix()):
                    self.assertIsNotNone(match)
                    artifact_id = match.group(1)
                    self.assertEqual(artifact_id, f"{prefix}-{path.name[:4]}")
                    self.assertNotIn(artifact_id, seen)
                seen.add(artifact_id)

    def test_active_operations_do_not_reference_retired_stages(self) -> None:
        retired_stage = re.compile(r"(?:docs/)?(?:04\.execution|98\.archive)")
        for path in sorted(STAGE05_ROOT.rglob("*.md")):
            with self.subTest(path=path.relative_to(REPOSITORY_ROOT).as_posix()):
                self.assertIsNone(
                    retired_stage.search(path.read_text(encoding="utf-8"))
                )

    def test_active_operations_omit_secret_value_examples(self) -> None:
        unsafe_examples = re.compile(
            r"xoxb-|changeme|export\s+VAULT_TOKEN",
            re.IGNORECASE,
        )
        for path in sorted(STAGE05_ROOT.rglob("*.md")):
            with self.subTest(path=path.relative_to(REPOSITORY_ROOT).as_posix()):
                self.assertIsNone(
                    unsafe_examples.search(path.read_text(encoding="utf-8"))
                )

    def test_operation_templates_share_authored_lifecycle_and_fields(self) -> None:
        profiles = {profile["id"]: profile for profile in self.registry["profiles"]}
        expectations = {
            "operation/guide": ("common/template-operation-guide",),
            "operation/incident": (
                "common/template-operation-incident",
                "Roles and Coordination",
                "Closure",
            ),
            "operation/postmortem": (
                "common/template-operation-postmortem",
                "Detection and Response Review",
                "Action Closure",
            ),
            "operation/policy": ("common/template-operation-policy",),
            "operation/runbook": ("common/template-operation-runbook",),
        }
        for authored_id, expected in expectations.items():
            template_id, *sections = expected
            authored = profiles[authored_id]
            template = profiles[template_id]
            with self.subTest(profile=authored_id):
                # The form used to restate the authored domain and this test
                # pinned the two together -- for Stage 05 only, which is why
                # these five stayed right while sixteen elsewhere drifted. The
                # form now declares none and the loader hands it the authored
                # one, so sharing is inherited rather than copied and checked.
                self.assertIsNone(template["lifecycle"])
                loaded = next(
                    item
                    for item in load_document_contracts()
                    .load_registry(REPOSITORY_ROOT)
                    .profiles
                    if item.profile_id == template_id
                )
                self.assertEqual(
                    loaded.status_domain,
                    tuple(authored["lifecycle"]["status_domain"]),
                )
                self.assertTrue(
                    set(sections).issubset(authored["sections"]["required"])
                )
                self.assertTrue(
                    set(sections).issubset(template["sections"]["required"])
                )
                self.assertIn(
                    "artifact_id",
                    template["frontmatter"]["required"],
                )


class TerminalStrictValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validators = {
            name: load_validator(name, path) for name, path in VALIDATOR_PATHS.items()
        }

    def parse(self, name: str, arguments: list[str]):
        validator = self.validators[name]
        if name == "registry":
            with mock.patch.object(
                sys, "argv", [str(VALIDATOR_PATHS[name]), *arguments]
            ):
                return validator._parse_args()
        return validator._parser().parse_args(arguments)

    def test_validator_mode_defaults_are_strict(self) -> None:
        for name in VALIDATOR_PATHS:
            with self.subTest(validator=name):
                self.assertEqual(self.parse(name, []).mode, "strict")

    def test_compatibility_mode_is_rejected_by_argparse(self) -> None:
        for name in VALIDATOR_PATHS:
            with self.subTest(validator=name):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as raised:
                        self.parse(name, ["--mode", "compatibility"])
                self.assertEqual(raised.exception.code, 2)

    def test_route_state_argument_is_parse_only_compatibility(self) -> None:
        args = self.parse("registry", ["--route-state", "transition"])
        self.assertEqual(args.route_state, "transition")
        registry = self.validators["registry"].load_registry(REPOSITORY_ROOT)
        self.assertFalse(hasattr(registry, "route_state"))

    def test_terminal_router_rejects_retired_stage99_support_path(self) -> None:
        validator = self.validators["registry"]
        registry = validator.load_registry(REPOSITORY_ROOT)
        with self.assertRaisesRegex(
            validator.DocumentContractError, "REGISTRY_ROUTE_UNCOVERED"
        ):
            validator.classify_path(
                registry,
                PurePosixPath("docs/99.templates/support/document-contract.md"),
            )

    def test_terminal_router_rejects_ambiguous_profile_match(self) -> None:
        validator = self.validators["registry"]
        registry = validator.load_registry(REPOSITORY_ROOT)
        profile = next(
            item for item in registry.profiles if item.profile_id == "sdlc/requirement"
        )
        ambiguous = replace(registry, profiles=(*registry.profiles, profile))
        with self.assertRaisesRegex(
            validator.DocumentContractError, "REGISTRY_ROUTE_AMBIGUOUS"
        ):
            validator.classify_path(
                ambiguous,
                PurePosixPath(
                    "docs/01.requirements/0001-argo-rollouts-progressive-delivery.md"
                ),
            )

    def test_retired_provider_surface_is_outside_the_document_corpus(self) -> None:
        contracts = sys.modules["document_contracts"]
        for retired in (
            "GEMINI.md",
            ".gemini/README.md",
            ".gemini/agents/doc-writer.md",
            ".gemini/agents/nested/doc-writer.md",
            ".gemini/agents/doc-writer.txt",
            ".gemini/settings.md",
        ):
            with self.subTest(retired=retired):
                self.assertFalse(
                    contracts._is_target_markdown(contracts.PurePosixPath(retired))
                )

    def test_provider_native_profile_routes_only_claude_markdown(self) -> None:
        validator = self.validators["registry"]
        registry = validator.load_registry(REPOSITORY_ROOT)
        self.assertEqual(
            validator.classify_path(
                registry,
                PurePosixPath(".claude/agents/doc-writer.md"),
            ).profile_id,
            "common/provider-native-metadata",
        )
        with self.assertRaisesRegex(
            validator.DocumentContractError, "REGISTRY_ROUTE_UNCOVERED"
        ):
            validator.classify_path(
                registry,
                PurePosixPath(".gemini/agents/doc-writer.md"),
            )

    def test_retired_surface_git_inventory_maps_bounded_process_failures(self) -> None:
        validator = self.validators["registry"]
        for failure in ("AUTHORITY_TIMEOUT", "AUTHORITY_SIZE"):
            with self.subTest(failure=failure):
                with mock.patch.object(
                    validator,
                    "run_bounded_process",
                    side_effect=validator.AuthorityError(failure),
                ):
                    with self.assertRaisesRegex(
                        AssertionError, "REGISTRY_RETIRED_CLOUD_SDLC_SURFACE"
                    ):
                        validator._assert_retired_cloud_sdlc_surfaces_absent(
                            REPOSITORY_ROOT
                        )

    def test_current_command_docs_do_not_advertise_compatibility_mode(self) -> None:
        compatibility_invocation = re.compile(r"--mode(?:[ =`]+)compatibility\b")
        for path in (
            SCRIPTS_ROOT / "README.md",
            REPOSITORY_ROOT / "tests/README.md",
            REPOSITORY_ROOT / "docs/99.templates/README.md",
        ):
            with self.subTest(path=path.relative_to(REPOSITORY_ROOT).as_posix()):
                self.assertIsNone(
                    compatibility_invocation.search(path.read_text(encoding="utf-8"))
                )

    def test_registry_and_markdown_strict_include_paths_pass(self) -> None:
        commands = (
            (
                "registry",
                "--mode",
                "strict",
                "--route-state",
                "transition",
                "--include-path",
                "docs/99.templates/README.md",
            ),
            (
                "markdown",
                "--mode",
                "strict",
                "--include-path",
                "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/plan.md",
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


if __name__ == "__main__":
    unittest.main()
