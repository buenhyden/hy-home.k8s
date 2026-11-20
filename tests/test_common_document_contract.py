"""Common shell projection keeps role meaning and native bytes intact."""

from __future__ import annotations

import sys
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import common_document_contract as COMMON  # noqa: E402
from common_document_contract import (  # noqa: E402
    CommonDocumentError,
    has_common_envelope,
    metadata_projection,
    payload_markdown,
    relation_rows,
)
from document_contracts import (  # noqa: E402
    DocumentContractError,
    is_criterion_id,
    load_registry,
    task_status,
    validate_registry,
)

ROOT = Path(__file__).resolve().parents[1]


FRONTMATTER = "---\ntitle: Example\nstatus: draft\n---\n"
SHELL = """# Example

## 문서 개요
### 목적과 독자
Purpose.
### 책임과 적용 범위
Scope.
## 내용 계약
### 입력과 전제
Input.
### 본문과 규칙
#### Role section
Body.
##### Detail
Detail.
## 적용과 확인
### 적용 방법
Method.
### 확인 기준
Check.
## 관계와 출처
### 관련 문서
Links.
### 외부 근거
Sources.
"""


class CommonDocumentProjectionTests(unittest.TestCase):
    def test_common_reader_imports_with_only_standard_library(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-S",
                "-c",
                "import sys; sys.path.insert(0, sys.argv[1]); import common_document_contract",
                str(ROOT / "scripts"),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_common_reader_rejects_unsafe_oversized_and_non_utf8_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "contract.json"
            original = COMMON.CONTRACT_PATH.read_bytes()
            with mock.patch.object(COMMON, "CONTRACT_PATH", path):
                path.write_bytes(original)
                self.assertEqual(len(COMMON._headings()), 4)
                for content in (b" " * (1024 * 1024 + 1), b"\xff"):
                    path.write_bytes(content)
                    with self.assertRaises(CommonDocumentError):
                        COMMON._headings()
                path.unlink()
                path.symlink_to(
                    ROOT
                    / "docs/99.templates/01.contracts/common-document-contract.json"
                )
                with self.assertRaises(CommonDocumentError):
                    COMMON._headings()

            real = Path(directory) / "real"
            real.mkdir()
            (real / "contract.json").write_bytes(original)
            alias = Path(directory) / "alias"
            alias.symlink_to(real, target_is_directory=True)
            with mock.patch.object(COMMON, "CONTRACT_PATH", alias / "contract.json"):
                with self.assertRaises(CommonDocumentError):
                    COMMON._headings()

            duplicate = original.replace(
                b'"contract_id":', b'"contract_id": "duplicate", "contract_id":', 1
            )
            with mock.patch.object(COMMON, "CONTRACT_PATH", real / "contract.json"):
                (real / "contract.json").write_bytes(duplicate)
                with self.assertRaises(CommonDocumentError):
                    COMMON._headings()

    def test_task_status_reads_multirow_work_items_inside_common_shell(self) -> None:
        registry = load_registry(ROOT)
        profile = next(p for p in registry.profiles if p.profile_id == "sdlc/task")
        role = (
            "#### Execution Log\n"
            "##### Work Performed\n"
            "| Item | Work Unit | Owner | Status | Blocker |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| WORK-001 | WORK-001 | platform | completed | none |\n"
            "| WORK-002 | WORK-002 | platform | in-progress | none |\n"
            "##### Lifecycle Traceability\n"
            "| Item | Upstream criterion | Result | Evidence |\n"
            "| --- | --- | --- | --- |\n"
            "| WORK-001 | AC-0001 | PASS | focused test |\n"
            "| WORK-002 | AC-0001 | NOT_RUN | none |\n"
        )
        text = SHELL.replace("#### Role section\nBody.\n##### Detail\nDetail.\n", role)
        self.assertEqual(task_status({}, text, profile), "in-progress")
        completed = text.replace("| in-progress |", "| completed |")
        self.assertEqual(task_status({}, completed, profile), "completed")
        self.assertEqual(task_status({"status": "draft"}, text, profile), "draft")

    def test_authored_projection_keeps_frontmatter_and_role_headings(self) -> None:
        text = FRONTMATTER + SHELL
        projected = payload_markdown(text, profile_id="sdlc/spec")
        self.assertTrue(has_common_envelope(text))
        self.assertTrue(projected.startswith(FRONTMATTER))
        self.assertIn("## Role section\nBody.\n### Detail\nDetail.", projected)
        self.assertNotIn("## 문서 개요", projected)

    def test_native_payload_is_exact_including_terminal_newline(self) -> None:
        native = "---\nname: example\n---\n# Native\n\n```text\nexample\n```\n"
        wrapper = FRONTMATTER + SHELL.replace(
            "#### Role section\nBody.\n##### Detail\nDetail.",
            "~~~~~~~native-payload\n" + native + "~~~~~~~",
        )
        self.assertEqual(
            payload_markdown(wrapper, profile_id="common/folder-agents-guide"), native
        )

    def test_old_or_duplicate_shell_refuses(self) -> None:
        old = FRONTMATTER + "## Old role\n"
        self.assertFalse(has_common_envelope(old))
        with self.assertRaises(CommonDocumentError):
            payload_markdown(old, profile_id="sdlc/spec")
        with self.assertRaises(CommonDocumentError):
            payload_markdown(
                FRONTMATTER + SHELL + "## 문서 개요\n", profile_id="sdlc/spec"
            )

    def test_native_fence_must_close(self) -> None:
        malformed = FRONTMATTER + SHELL.replace(
            "#### Role section\nBody.\n##### Detail\nDetail.",
            "~~~~~~~native-payload\nbody\n",
        )
        with self.assertRaises(CommonDocumentError):
            payload_markdown(malformed, profile_id="common/folder-agents-guide")

    def test_literal_headings_inside_role_code_fence_are_unchanged(self) -> None:
        text = FRONTMATTER + SHELL.replace(
            "#### Role section\nBody.\n##### Detail\nDetail.",
            "#### Role section\n```md\n#### Literal heading\n```\n##### Detail\nDetail.",
        )
        projected = payload_markdown(text, profile_id="sdlc/spec")
        self.assertIn("## Role section\n```md\n#### Literal heading\n```", projected)

    def test_html_block_headings_are_not_shell_sections(self) -> None:
        text = FRONTMATTER + SHELL.replace(
            "#### Role section\nBody.",
            "<pre>\n## 문서 개요\n```\n</pre>\n#### Role section\nBody.",
        )
        projected = payload_markdown(text, profile_id="sdlc/spec")
        self.assertIn("<pre>\n## 문서 개요\n```\n</pre>", projected)

    def test_h3_under_wrong_h2_is_rejected(self) -> None:
        malformed = FRONTMATTER + SHELL.replace(
            "### 책임과 적용 범위\nScope.\n## 내용 계약",
            "## 내용 계약\n### 책임과 적용 범위\nScope.",
        )
        with self.assertRaises(CommonDocumentError):
            payload_markdown(malformed, profile_id="sdlc/spec")

    def test_authored_profile_cannot_hide_native_payload(self) -> None:
        wrapper = FRONTMATTER + SHELL.replace(
            "#### Role section\nBody.\n##### Detail\nDetail.",
            "~~~~~~~native-payload\nbody\n~~~~~~~",
        )
        with self.assertRaises(CommonDocumentError):
            payload_markdown(wrapper, profile_id="sdlc/spec")

    def test_typed_relation_table_accepts_each_core_kind(self) -> None:
        kinds = (
            "requires",
            "designs",
            "implements",
            "verifies",
            "operates",
            "defines",
            "cites",
        )
        rows = "\n".join(f"| {kind} | [{kind}](../{kind}.md) |" for kind in kinds)
        text = FRONTMATTER + SHELL.replace(
            "### 관련 문서\nLinks.",
            "### 관련 문서\n| Relation | Target |\n| --- | --- |\n" + rows,
        )
        self.assertEqual(
            relation_rows(text), tuple((kind, f"../{kind}.md") for kind in kinds)
        )

    def test_unknown_relation_kind_and_plain_target_are_rejected(self) -> None:
        for row in ("| approves | [x](../x.md) |", "| requires | ../x.md |"):
            with self.subTest(row=row):
                text = FRONTMATTER + SHELL.replace(
                    "### 관련 문서\nLinks.",
                    "### 관련 문서\n| Relation | Target |\n| --- | --- |\n" + row,
                )
                with self.assertRaises(CommonDocumentError):
                    relation_rows(text)

    def test_registry_binding_rejects_unknown_kind_and_digest_drift(self) -> None:
        original = json.loads((ROOT / "docs/99.templates/registry.json").read_text())
        for mutation in ("kind", "digest"):
            with self.subTest(mutation=mutation):
                raw = json.loads(json.dumps(original))
                binding = raw["common_document_contract"]
                if mutation == "kind":
                    binding["profile_kinds"]["sdlc/spec"] = "made-up"
                else:
                    binding["content_digest"] = "sha256:" + "0" * 64
                with self.assertRaises(DocumentContractError) as caught:
                    validate_registry(ROOT, raw)
                self.assertIn(
                    "REGISTRY_COMMON_DOCUMENT",
                    {d.rule_id for d in caught.exception.diagnostics},
                )

    def test_workspace_scope_artifact_binding_is_exact_and_unique(self) -> None:
        original = json.loads((ROOT / "docs/99.templates/registry.json").read_text())
        ids = original["common_document_contract"]["workspace_scope_artifact_ids"]
        self.assertEqual(
            set(ids),
            {"REQ-0003", "SPEC-0226", "SPEC-0227", "AD-0006", "GDE-0011"},
        )
        for replacement in ("REQ-0999", "SPEC-0226"):
            with self.subTest(replacement=replacement):
                raw = json.loads(json.dumps(original))
                raw["common_document_contract"]["workspace_scope_artifact_ids"][0] = (
                    replacement
                )
                with self.assertRaises(DocumentContractError):
                    validate_registry(ROOT, raw)

    def test_metadata_adapter_keeps_task_execution_separate_from_document_lifecycle(
        self,
    ) -> None:
        binding = json.loads((ROOT / "docs/99.templates/registry.json").read_text())[
            "common_document_contract"
        ]
        source = {
            "title": "A task",
            "version": "0.1.0",
            "type": "sdlc/task",
            "status": "completed",
            "owner": "platform",
        }
        projected = metadata_projection(
            source,
            profile_id="sdlc/task",
            binding=binding,
            scope_subject="hy-home.k8s",
            scope_layer="workspace",
        )
        self.assertEqual(projected["kind"], "task")
        self.assertEqual(projected["lifecycle"], "draft")
        self.assertEqual(source["status"], "completed")
        with self.assertRaises(CommonDocumentError):
            metadata_projection(
                source,
                profile_id="sdlc/task",
                binding=binding,
                scope_subject="hy-home.k8s",
                scope_layer="workspace",
                document_lifecycle="active",
            )
        active = metadata_projection(
            source,
            profile_id="sdlc/task",
            binding=binding,
            scope_subject="hy-home.k8s",
            scope_layer="workspace",
            document_lifecycle="active",
            adoption_verified=True,
        )
        self.assertEqual(active["lifecycle"], "active")
        without_status = {
            key: value for key, value in source.items() if key != "status"
        }
        self.assertEqual(
            metadata_projection(
                without_status,
                profile_id="sdlc/task",
                binding=binding,
                scope_subject="hy-home.k8s",
                scope_layer="workspace",
            )["lifecycle"],
            "draft",
        )

    def test_metadata_adapter_rejects_unknown_status_or_kind(self) -> None:
        binding = json.loads((ROOT / "docs/99.templates/registry.json").read_text())[
            "common_document_contract"
        ]
        source = {
            "title": "A spec",
            "version": "1.0.0",
            "type": "sdlc/spec",
            "status": "mystery",
            "owner": "platform",
        }
        for profile_id in ("sdlc/spec", "unknown/profile"):
            with (
                self.subTest(profile_id=profile_id),
                self.assertRaises(CommonDocumentError),
            ):
                metadata_projection(
                    source,
                    profile_id=profile_id,
                    binding=binding,
                    scope_subject="hy-home.k8s",
                    scope_layer="workspace",
                )

    def test_spec_local_criterion_id_starts_at_one(self) -> None:
        self.assertTrue(is_criterion_id("AC-0001"))
        self.assertFalse(is_criterion_id("AC-0000"))
        self.assertTrue(is_criterion_id("VAL-FEATURE-001"))


if __name__ == "__main__":
    unittest.main()
