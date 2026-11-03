#!/usr/bin/env python3
"""Focused contract tests for the outside-docs stage link boundary."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from contextlib import redirect_stdout
from dataclasses import replace
from io import StringIO
from pathlib import Path, PurePosixPath
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate-links-and-owners.py"
SCRIPTS = str(SCRIPT.parent)
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

SPEC = importlib.util.spec_from_file_location("stage_boundary_validator", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("link validator is unavailable")
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


CONSUMER = PurePosixPath("scripts/README.md")
PROFILE = "common/readme-implementation"
HUB = PurePosixPath("docs/README.md")


def _report(source: PurePosixPath, target: str):
    return validator._stage_boundary_diagnostic(source, PROFILE, PurePosixPath(target))


STAGE_PREFIXES = validator._stage_document_prefixes(validator.load_registry(ROOT))


class RetainedReciprocalAndTemplateTests(unittest.TestCase):
    def test_deleted_target_selects_one_hop_incoming_body_reader(self) -> None:
        deleted = PurePosixPath("docs/05.operations/runbooks/deleted.md")
        incoming = PurePosixPath("docs/05.operations/guides/0001-incoming.md")
        unrelated = PurePosixPath("docs/05.operations/guides/0002-unrelated.md")
        context = SimpleNamespace(
            paths=(incoming, unrelated),
            profiles={
                incoming: SimpleNamespace(
                    profile_id="operation/guide", mode="authored"
                ),
                unrelated: SimpleNamespace(
                    profile_id="operation/guide", mode="authored"
                ),
            },
            texts={
                incoming: "[missing](../runbooks/deleted.md#step)",
                unrelated: "[incoming](0001-incoming.md)",
            },
        )
        with mock.patch.object(
            validator, "scoped_document_content_paths", return_value=frozenset()
        ):
            selected = validator._body_link_scope(
                context, (deleted.as_posix(),), SimpleNamespace()
            )
        self.assertEqual(selected, frozenset({incoming}))

    def test_change_scope_option_rejects_partial_or_audit_invocation(self) -> None:
        from contextlib import redirect_stderr

        for options in (
            ("--change-scope",),
            ("--changed-path=docs/README.md",),
            ("--change-scope", "--changed-path=docs//README.md"),
            (
                "--change-scope",
                "--changed-path=docs/README.md",
                "--body-contracts=audit",
            ),
        ):
            with self.subTest(options=options), redirect_stderr(StringIO()):
                self.assertEqual(validator.main(options), 2)

    def test_main_uses_current_context_registry_and_inventory_once(self) -> None:
        registry = SimpleNamespace(profiles=())
        inventory = SimpleNamespace(baseline_paths=(), current_paths=(), new_paths=())
        context = SimpleNamespace(
            root=ROOT,
            current_registry=registry,
            current_inventory=inventory,
        )
        with (
            mock.patch.object(validator, "_build_context", return_value=context),
            mock.patch.object(
                validator,
                "load_registry",
                side_effect=AssertionError("duplicate registry load"),
            ),
            mock.patch.object(
                validator,
                "enumerate_target_markdown",
                side_effect=AssertionError("duplicate inventory scan"),
            ),
            mock.patch.object(validator, "_raw_diagnostics", return_value=[]),
            mock.patch.object(
                sys,
                "argv",
                ["validate-links-and-owners.py", "--root", str(ROOT)],
            ),
            redirect_stdout(StringIO()),
        ):
            self.assertEqual(validator.main(), 0)

    def test_actual_plan_and_task_forms_accept_whole_placeholder_paths_with_fragments(
        self,
    ) -> None:
        forms = (
            PurePosixPath("docs/99.templates/templates/specs/plan.template.md"),
            PurePosixPath("docs/99.templates/templates/specs/task.template.md"),
        )
        # LINK-BROKEN comes only from the link pass, so check just the forms
        # instead of every diagnostic over the whole corpus.
        context = replace(validator._build_context(ROOT, forms), paths=forms)
        expected = "{{SPEC_RELATIVE_PATH}}#success-criteria--verification-plan"
        for path in forms:
            spec_links = [
                raw
                for raw in validator._extract_links(context.texts[path])
                if raw.startswith("{{SPEC_RELATIVE_PATH}}")
            ]
            self.assertTrue(spec_links, path)
            self.assertEqual(set(spec_links), {expected})
        diagnostics = validator._link_diagnostics(context)
        self.assertEqual(
            [
                item
                for item in diagnostics
                if item.rule_id == "LINK-BROKEN" and item.path in forms
            ],
            [],
        )
        for malformed in (
            "{{spec_relative_path}}#success-criteria",
            "{{SPEC_RELATIVE_PATH}}/extra#success-criteria",
            "{{SPEC_RELATIVE_PATH}}?query=value#success-criteria",
        ):
            context.texts[forms[0]] = (
                (ROOT / forms[0]).read_text().replace(expected, malformed)
            )
            diagnostics = validator._link_diagnostics(context)
            self.assertTrue(
                any(
                    item.rule_id == "LINK-BROKEN" and item.path == forms[0]
                    for item in diagnostics
                ),
                malformed,
            )
        authored = PurePosixPath("docs/03.specs/0140-archive-check-removal/spec.md")
        self.assertEqual(validator._local_destination(authored, expected)[0], "local")

    def test_current_backlink_is_still_required(self) -> None:
        owner = PurePosixPath("docs/03.specs/0140-archive-check-removal/spec.md")
        expected = PurePosixPath(
            "docs/01.requirements/0003-workspace-agent-governance-platform.md"
        )
        context = SimpleNamespace(
            texts={owner: "Current completed Spec without a backlink."},
        )
        self.assertFalse(validator._links_back_to(context, owner, expected))
        context.texts[owner] = (
            "[Requirement](../../01.requirements/0003-workspace-agent-governance-platform.md)"
        )
        self.assertTrue(validator._links_back_to(context, owner, expected))

    def test_full_uppercase_placeholder_is_only_a_template_destination(self) -> None:
        form = PurePosixPath("docs/99.templates/templates/specs/plan.template.md")
        for variable in (
            "CHILD_RELATIVE_PATH",
            "SPEC_RELATIVE_PATH",
            "TASK_RELATIVE_PATH",
        ):
            raw = "{{" + variable + "}}"
            self.assertEqual(
                validator._local_destination(form, raw, template=True),
                ("template", None),
            )
            self.assertEqual(
                validator._local_destination(
                    PurePosixPath("docs/03.specs/0140-archive-check-removal/spec.md"),
                    raw,
                )[0],
                "local",
            )
        for malformed in (
            "{{task_relative_path}}",
            "{{TASK RELATIVE_PATH}}",
            "{{TASK_RELATIVE_PATH}}/extra",
        ):
            self.assertEqual(
                validator._local_destination(form, malformed, template=True)[0], "local"
            )


def _grammar(
    text: str,
    *,
    source: PurePosixPath = CONSUMER,
    profile: str = PROFILE,
    exists=lambda target: False,
):
    return validator._stage_grammar_diagnostics(
        source, profile, text, STAGE_PREFIXES, exists
    )


class StageLinkBoundaryTests(unittest.TestCase):
    def test_reports_every_numbered_stage_target_written_outside_docs(self) -> None:
        for target in (
            "docs/02.architecture/decisions/0031-validation-ownership.md",
            "docs/03.specs/0140-archive-check-removal/spec.md",
            "docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md",
            "docs/99.templates/registry.json",
        ):
            with self.subTest(target=target):
                diagnostic = _report(CONSUMER, target)

                self.assertIsNotNone(diagnostic)
                assert diagnostic is not None
                self.assertEqual(diagnostic.rule_id, "LINK-STAGE-BOUNDARY")
                self.assertEqual(diagnostic.path, CONSUMER)
                self.assertEqual(diagnostic.actual, target)

    def test_stage_readmes_are_navigation_not_individual_authority(self) -> None:
        for target in (
            "docs/01.requirements/README.md",
            "docs/03.specs/README.md",
            "docs/99.templates/README.md",
        ):
            with self.subTest(target=target):
                self.assertIsNone(_report(CONSUMER, target))

    def test_normalized_reference_forms_cannot_hide_individual_documents(self) -> None:
        self.assertTrue(hasattr(validator, "_stage_reference_diagnostics"))
        forms = (
            "<https://github.com/buenhyden/hy-home.k8s/blob/main/docs/03.specs/0140-archive-check-removal/spec.md>",
            "Follow `../docs/03.specs/0140-archive-check-removal/spec.md`.",
            "Follow `/checkout/docs/03.specs/0140-archive-check-removal/spec.md`.",
            "[rule](../docs/03.specs/0140-archive-check-removal/spec.md)",
            "[rule][x]\n\n[x]: ../docs/03.specs/0140-archive-check-removal/spec.md",
            '<a href="../docs/03.specs/0140-archive-check-removal/spec.md">rule</a>',
            "<a href=../docs/03.specs/0140-archive-check-removal/spec.md>rule</a>",
            "[[docs/03.specs/0140-archive-check-removal/spec.md|rule]]",
            "[rule](https://github.com/buenhyden/hy-home.k8s/blob/main/docs/03.specs/0140-archive-check-removal/spec.md)",
            "[rule](https://raw.githubusercontent.com/buenhyden/hy-home.k8s/main/docs/03.specs/0140-archive-check-removal/spec.md)",
            "[rule](/checkout/docs/03.specs/0140-archive-check-removal/spec.md)",
            "[rule](../DOCS/03.SPECS/0140-archive-check-removal/SPEC.MD)",
            r"[[..\docs\03.specs\0008-current-local-gitops-platform\spec.md]]",
            "[rule](../docs%252f03.specs%252f0008-current-local-gitops-platform%252fspec.md)",
            "Follow `docs/03.specs/0140-archive-check-removal/spec.md` as current policy.",
        )
        for text in forms:
            with self.subTest(text=text):
                result = validator._stage_reference_diagnostics(CONSUMER, PROFILE, text)
                self.assertTrue(result)
                self.assertEqual(result[0].rule_id, "LINK-STAGE-BOUNDARY")
        for text in (
            "[index](../docs/03.specs/README.md)",
            "[source](https://example.org/docs/03.specs/example.md)",
        ):
            self.assertEqual(
                validator._stage_reference_diagnostics(CONSUMER, PROFILE, text), []
            )
        self.assertEqual(
            validator._stage_reference_diagnostics(HUB, PROFILE, forms[0]), []
        )

    def test_machine_exception_is_exact_in_all_three_dimensions(self) -> None:
        self.assertTrue(hasattr(validator, "_stage_machine_reference_allowed"))
        check = validator._stage_machine_reference_allowed
        source = PurePosixPath(".agents/skills/docs-stage-routing/SKILL.md")
        target = PurePosixPath("docs/99.templates/registry.json")
        self.assertTrue(check(source, target, "machine-read"))
        self.assertFalse(check(CONSUMER, target, "machine-read"))
        self.assertFalse(
            check(source, PurePosixPath("docs/99.templates/other.json"), "machine-read")
        )
        self.assertFalse(check(source, target, "link"))

    def test_leaves_the_documentation_hub_reachable_from_outside(self) -> None:
        self.assertIsNone(_report(CONSUMER, "docs/README.md"))

    def test_leaves_links_between_documents_inside_docs_alone(self) -> None:
        self.assertIsNone(
            validator._stage_boundary_diagnostic(
                HUB, PROFILE, PurePosixPath("docs/02.architecture/README.md")
            )
        )
        self.assertIsNone(
            validator._stage_boundary_diagnostic(
                PurePosixPath("docs/02.architecture/README.md"),
                PROFILE,
                PurePosixPath("docs/99.templates/README.md"),
            )
        )

    def test_leaves_targets_outside_the_numbered_stage_tree_alone(self) -> None:
        for target in (
            "scripts/README.md",
            ".agents/governance/quality.md",
            "docs-extra/notes.md",
        ):
            with self.subTest(target=target):
                self.assertIsNone(_report(CONSUMER, target))


class StagePathGrammarTests(unittest.TestCase):
    """A plain-text stage path names a document, never a second path pattern.

    The stage boundary above sends a file outside `docs/` to plain text instead
    of a link. These tests cover what that plain text may then say: the
    collection a profile owns, or a document that exists. A route written out
    as a grammar is a copy of the registry's `path_pattern` that no gate reads
    and nothing keeps current."""

    def test_derives_its_prefixes_from_the_registry(self) -> None:
        """A literal list here would be the same defect the rule exists to stop."""

        self.assertIn("docs/05.operations/incidents/", STAGE_PREFIXES)
        self.assertIn("docs/03.specs/", STAGE_PREFIXES)
        self.assertIn("docs/05.operations/runbooks/", STAGE_PREFIXES)
        self.assertNotIn("docs/99.templates/templates/operations/", STAGE_PREFIXES)

    def test_a_pattern_that_opens_on_a_branch_contributes_no_prefix(self) -> None:
        """Two roots share one profile, so no single directory literal holds."""

        self.assertEqual(
            validator._fixed_directory_prefix(
                r"^(?:docs/03\.specs|docs/05\.operations)"
                r"/[0-9]{4}-[a-z]+/spec\.md$"
            ),
            "",
        )
        self.assertEqual(
            validator._fixed_directory_prefix(
                r"^docs/05\.operations/incidents/[0-9]{4}/inc-[0-9]{4}-[a-z]+/incident\.md$"
            ),
            "docs/05.operations/incidents/",
        )

    def test_a_leading_root_group_contributes_one_prefix_per_root(self) -> None:
        """A pattern may name several roots that share one profile."""

        self.assertEqual(
            validator._fixed_directory_prefixes(
                r"^(?:docs/05\.operations|docs/90\.references)"
                r"/incidents/[0-9]{4}/inc-[0-9]{4}-[a-z]+/incident\.md$"
            ),
            (
                "docs/05.operations/incidents/",
                "docs/90.references/incidents/",
            ),
        )

    def test_reports_a_route_written_out_as_a_grammar(self) -> None:
        body = (
            "Durable incident bundles live under\n"
            "`docs/05.operations/incidents/YYYY/INC-###-<title>/`: the fact record is\n"
            "`INC-###-<title>.md`.\n"
        )
        diagnostics = _grammar(body)

        self.assertEqual([item.rule_id for item in diagnostics], ["PATH-STAGE-GRAMMAR"])
        self.assertEqual(
            diagnostics[0].actual, "docs/05.operations/incidents/YYYY/INC-###-<title>/"
        )

    def test_reports_each_distinct_grammar_once(self) -> None:
        body = (
            "records in `docs/05.operations/incidents/YYYY/INC-###-x/`\n"
            "reports in `docs/05.operations/incidents/YYYY/INC-###-x/`\n"
        )

        self.assertEqual(len(_grammar(body)), 1)

    def test_admits_the_collection_a_profile_owns(self) -> None:
        """Naming the collection couples nothing; the registry still owns the route."""

        for body in (
            "Save the file under `docs/05.operations/runbooks/`.",
            "Runbooks live in docs/05.operations/runbooks and nowhere else.",
        ):
            with self.subTest(body=body):
                self.assertEqual(_grammar(body), [])

    def test_admits_a_path_that_resolves_to_a_document(self) -> None:
        body = "See `docs/05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md`."

        self.assertEqual(_grammar(body, exists=lambda target: True), [])
        self.assertEqual(len(_grammar(body, exists=lambda target: False)), 1)

    def test_ignores_a_target_no_profile_prefix_covers(self) -> None:
        body = (
            "Read `docs/99.templates/registry.json` and `docs/05.operations/README.md`."
        )

        self.assertEqual(_grammar(body), [])

    def test_leaves_documents_inside_docs_to_their_own_contracts(self) -> None:
        body = "`docs/05.operations/incidents/YYYY/INC-###-<title>/incident.md`"
        source = PurePosixPath("docs/02.architecture/decisions/0024-terminal.md")

        self.assertEqual(_grammar(body, source=source), [])


if __name__ == "__main__":  # pragma: no cover - module entry guard
    unittest.main()
