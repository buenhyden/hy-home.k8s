"""Focused failures for the common document envelope and role payload readers."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path, PurePosixPath
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from document_contracts import load_registry  # noqa: E402
from tests.form_headings import common_shell, form_body  # noqa: E402


def _script(name: str):
    path = SCRIPTS / name
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unavailable script: {name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


markdown = _script("validate-markdown-profiles.py")
links = _script("validate-links-and-owners.py")


def _profile(profile_id: str):
    return next(
        profile
        for profile in load_registry(ROOT).profiles
        if profile.profile_id == profile_id
    )


class InterfaceReferenceTests(unittest.TestCase):
    def test_if_requires_declared_same_package_fr_or_nfr(self) -> None:
        path = PurePosixPath("docs/01.requirements/0003-example.md")
        profile = _profile("sdlc/requirement")
        rows = (
            "| Requirement ID | Statement | Rationale | Acceptance | Priority |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| REQ-0003-FR-0001 | Function. | Reason. | Observable. | must |\n"
            "| REQ-0003-IF-0001 | Interface. | Reason; interface_refs: {ref} | Observable. | must |\n"
        )

        def issues(ref: str) -> set[str]:
            body = "# Example\n\n## Requirements\n\n### Functional Requirements\n\n"
            body += rows.format(ref=ref)
            body += "\n### Quality Requirements\n\nNo quality members.\n"
            return {
                item.rule_id
                for item in markdown._requirement_quality_diagnostics(
                    path, profile, body
                )
            }

        self.assertNotIn(
            "BODY-INTERFACE-REF",
            issues("REQ-0003-FR-0001"),
        )
        self.assertIn("BODY-INTERFACE-REF", issues("REQ-0003-FR-9999"))
        self.assertIn("BODY-INTERFACE-REF", issues("REQ-0004-FR-0001"))
        self.assertIn("BODY-INTERFACE-REF", issues("none"))

    def test_scoped_ac_criterion_is_not_a_global_val_alias(self) -> None:
        self.assertIsNotNone(
            markdown.IDENTIFIER_PATTERNS["criterion"].fullmatch("AC-0001")
        )
        self.assertIsNotNone(
            links.BODY_IDENTIFIER_PATTERNS["criterion"].fullmatch("AC-0001")
        )
        self.assertIsNone(
            markdown.IDENTIFIER_PATTERNS["criterion"].fullmatch("AC-0000")
        )
        self.assertIsNone(
            links.BODY_IDENTIFIER_PATTERNS["criterion"].fullmatch("AC-0000")
        )


class CommonEnvelopeConsumerTests(unittest.TestCase):
    def test_scope_projection_uses_declared_workspace_owner_and_artifact(self) -> None:
        binding = load_registry(ROOT).common_document_contract
        cases = (
            (
                "docs/00.workspace/02.architecture/01.descriptions/0006-example.md",
                "sdlc/architecture-description",
                "AD-0006",
                "workspace",
            ),
            (
                "docs/02.architecture/01.descriptions/0007-example.md",
                "sdlc/architecture-description",
                "AD-0007",
                "product",
            ),
            (
                "docs/00.workspace/05.environment/0011-example.md",
                "operation/guide",
                "GDE-0011",
                "workspace",
            ),
            (
                "docs/01.requirements/0003-example.md",
                "sdlc/requirement",
                "REQ-0003",
                "workspace",
            ),
            (
                "docs/03.specs/0226-example/spec.md",
                "sdlc/spec",
                "SPEC-0226",
                "workspace",
            ),
            (
                "docs/03.specs/0226-example/plan.md",
                "sdlc/plan",
                "SPEC-0226-PLAN-0001",
                "workspace",
            ),
            (
                "docs/03.specs/0226-example/01.tasks/tsk-0001-example.md",
                "sdlc/task",
                "SPEC-0226-TSK-0001",
                "workspace",
            ),
        )
        shell = "\n".join(common_shell(["#### Role", "Synthetic content."]))
        for path, profile_id, artifact_id, expected_layer in cases:
            with self.subTest(artifact_id=artifact_id):
                profile = _profile(profile_id)
                text = (
                    f'---\ntitle: "Fixture subject"\nversion: "1.0.0"\n'
                    f'type: "{profile_id}"\nstatus: "draft"\nowner: "platform"\n'
                    f'updated: "2026-11-20"\nartifact_id: "{artifact_id}"\n---\n'
                    f"# Fixture\n{shell}\n"
                )
                with mock.patch.object(
                    markdown, "metadata_projection", wraps=markdown.metadata_projection
                ) as projection:
                    markdown.validate_document_text(
                        text,
                        PurePosixPath(path),
                        profile,
                        "strict",
                        common_binding=binding,
                    )
                self.assertEqual(
                    projection.call_args.kwargs["scope_layer"], expected_layer
                )
                self.assertEqual(
                    projection.call_args.kwargs["scope_subject"],
                    "hy-home.k8s"
                    if expected_layer == "workspace"
                    else "Fixture subject",
                )

    def test_historical_task_needs_completed_acceptance_record(self) -> None:
        profile = _profile("sdlc/task")
        frontmatter = '---\ntitle: "Task"\nstatus: "{status}"\n---\n'
        decision = (
            "\n## Acceptance Decision\n\n"
            "| Criterion | Acceptance |\n| --- | --- |\n"
            "| [VAL-OLD-001](../spec.md#criteria) | accepted |\n"
        )
        self.assertFalse(
            markdown._accepted_completed_task(
                frontmatter.format(status="in-progress") + decision, profile
            )
        )
        self.assertFalse(
            markdown._accepted_completed_task(
                frontmatter.format(status="completed") + "\n## Handoff\n", profile
            )
        )
        self.assertTrue(
            markdown._accepted_completed_task(
                frontmatter.format(status="completed") + decision, profile
            )
        )

    def test_typed_citation_stays_provenance_and_other_edges_are_local(self) -> None:
        path = PurePosixPath("docs/README.md")

        def shell(kind: str) -> str:
            return (
                "# Example\n## 문서 개요\n### 목적과 독자\nExample.\n"
                "### 책임과 적용 범위\nExample.\n"
                "## 내용 계약\n### 입력과 전제\nExample.\n"
                "### 본문과 규칙\n#### Navigation\nExample.\n"
                "## 적용과 확인\n### 적용 방법\nExample.\n"
                "### 확인 기준\nExample.\n"
                "## 관계와 출처\n### 관련 문서\n"
                "| Relation | Target |\n| --- | --- |\n"
                f"| {kind} | [source](https://example.org/evidence) |\n"
                "### 외부 근거\nExample.\n"
            )

        def findings(kind: str) -> set[str]:
            context = SimpleNamespace(
                root=ROOT,
                paths=(path,),
                profiles={
                    path: SimpleNamespace(
                        profile_id="common/readme-stage-index", mode="router"
                    )
                },
                texts={path: shell(kind)},
                document_links={path: ()},
                adapter_targets={},
                tracked_regular_paths=frozenset(),
                current_registry=load_registry(ROOT),
            )
            return {item.rule_id for item in links._link_diagnostics(context)}

        self.assertNotIn("RELATION-AUTHORITY", findings("cites"))
        self.assertIn("RELATION-AUTHORITY", findings("requires"))
        self.assertIn("RELATION-TYPED", findings("unknown"))
        context = SimpleNamespace(
            paths=(path,),
            profiles={
                path: SimpleNamespace(
                    profile_id="common/readme-stage-index",
                    profile_class="readme",
                    mode="router",
                )
            },
            texts={path: shell("cites")},
            metadata={path: {}},
            baseline_paths=frozenset(),
        )
        with mock.patch.object(links, "_owner_state", return_value=({path: ""}, [])):
            inventory = links._inventory_documents(context)
        self.assertEqual(
            inventory[0]["typedRelations"],
            [{"kind": "cites", "target": "https://example.org/evidence"}],
        )

    def test_current_requirement_requires_exact_shell_and_reads_role_form(self) -> None:
        profile = _profile("sdlc/requirement")
        path = PurePosixPath("docs/01.requirements/0003-example.md")
        frontmatter = (
            '---\ntitle: "Example"\nversion: "1.0.0"\n'
            'type: "sdlc/requirement"\nstatus: "draft"\n'
            'owner: "platform"\nupdated: "2026-11-20"\n'
            'artifact_id: "REQ-0003"\n---\n\n# Example\n\n'
        )
        payload = "\n".join(
            "##" + line if line.startswith("## ") or line.startswith("### ") else line
            for line in form_body("requirement")
        )
        # The role form is nested at H4/H5 below the common H3 payload slot.
        shell = (
            "## 문서 개요\n### 목적과 독자\nExample.\n"
            "### 책임과 적용 범위\nExample.\n"
            "## 내용 계약\n### 입력과 전제\nExample.\n"
            "### 본문과 규칙\n" + payload + "\n"
            "## 적용과 확인\n### 적용 방법\nExample.\n"
            "### 확인 기준\nExample.\n"
            "## 관계와 출처\n### 관련 문서\nExample.\n"
            "### 외부 근거\nExample.\n"
        )

        def codes(body: str, *, title: str = "Example") -> set[str]:
            return {
                item.rule_id
                for item in markdown.validate_document_text(
                    frontmatter.replace('title: "Example"', f'title: "{title}"') + body,
                    path,
                    profile,
                    "strict",
                    common_binding=load_registry(ROOT).common_document_contract,
                )
            }

        self.assertIn("BODY-COMMON-ENVELOPE", codes("## Overview\n"))
        self.assertIn(
            "BODY-COMMON-ENVELOPE", codes(shell.replace("### 외부 근거", "### Other"))
        )
        self.assertNotIn("BODY-COMMON-ENVELOPE", codes(shell))
        self.assertNotIn("BODY-HEADING-REQUIRED", codes(shell))
        self.assertNotIn("FM-COMMON-METADATA", codes(shell))
        self.assertIn("FM-COMMON-METADATA", codes(shell, title=""))


if __name__ == "__main__":
    unittest.main()
