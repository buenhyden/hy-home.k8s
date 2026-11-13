"""Regressions for the work residue ledger gate and its on-demand view.

Every case builds a temporary tree; none runs the gate over the repository.
"""

from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPOSITORY_ROOT / "scripts"
SCHEMA_REL = "docs/99.templates/contracts/work-residue-ledger.schema.json"
LEDGER_REL = "docs/03.specs/work-residue-ledger.json"
REGISTRY_REL = "docs/99.templates/registry.json"
TASK = "docs/03.specs/0001-x/tasks/tsk-0001-x.md"
OTHER_TASK = "docs/03.specs/0002-y/tasks/tsk-0001-y.md"
COLUMNS = ["ID", "Residue", "State", "Owner", "Resume condition", "Closure"]
EVIDENCE_HEADER = (
    "| Evidence | Criteria | Work Unit | Check | Input | Result | Location "
    "| Required | Resolves |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
)
HANDOFF_TABLE = "| ID | Gap |\n| --- | --- |\n| X-1 | gap |\n"
RESUME = "after the first package"


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    if spec is None or spec.loader is None:
        raise AssertionError(f"{filename} could not be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def entry(
    id: str = "H-1",
    *,
    kind: str = "handoff",
    state: str = "open",
    owner: str = "W03",
    resume: str = RESUME,
    path: str = TASK,
    **extra,
) -> dict:
    value = {
        "id": id,
        "kind": kind,
        "state": state,
        "owner": owner,
        "resume_condition": resume,
        "source": {"path": path},
    }
    value.update(extra)
    return value


def row(
    id: str = "H-1",
    state: str = "open",
    owner: str = "W03",
    resume: str = RESUME,
    closure: str = "none",
) -> str:
    return f"| {id} | text | {state} | {owner} | {resume} | {closure} |"


def table(header: list[str], rows: list[str]) -> str:
    return (
        "| "
        + " | ".join(header)
        + " |\n| "
        + " | ".join("---" for _ in header)
        + " |\n"
        + "\n".join(rows)
        + "\n"
    )


def task_text(
    rows: list[str] | None = None,
    evidence: dict[str, str] | None = None,
    extra: str = "",
) -> str:
    evidence = {"EVD-001": "PASS", "EVD-002": "FAIL"} if evidence is None else evidence
    text = "# Task\n\n## Task Evidence\n\n" + EVIDENCE_HEADER
    text += "".join(
        f"| {key} | c | w | k | i | {value} | l | yes | none |\n"
        for key, value in evidence.items()
    )
    if rows is not None:
        text += f"\n### Residue Handoff\n\n{table(COLUMNS, rows)}"
    return text + "\n" + extra


class Tree:
    def __init__(self, test: unittest.TestCase) -> None:
        directory = tempfile.TemporaryDirectory(prefix="residue-")
        test.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.write(SCHEMA_REL, (REPOSITORY_ROOT / SCHEMA_REL).read_text("utf-8"))
        self.registry = {
            "work_residue": {
                "task_table": {
                    "section": "Task Evidence",
                    "heading": "Residue Handoff",
                    "columns": COLUMNS,
                },
                "historical_tables": [],
            },
            "shared_contract": {
                "contract_id": "WGOV-CORE",
                "version": "3.0.0",
                "owner": "buenhyden",
                "content_digest": "sha256:" + "ab" * 32,
                "source_revision": "c" * 40,
                "approval_ref": "call_0123456789abcdef/0",
                "approved_by": "unverified",
            },
            "common_forms": {
                "contract_id": "COMMON-DOC-FORM-1",
                "version": "1.0.0",
                "forms": [],
            },
        }
        self.write_registry()

    def write(self, rel: str, text: str) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def write_registry(self) -> None:
        self.write(REGISTRY_REL, json.dumps(self.registry, indent=1))

    def ledger(self, entries: list[dict]) -> None:
        document = {
            "$schema": "../99.templates/contracts/work-residue-ledger.schema.json",
            "schema_version": 1,
            "entries": entries,
        }
        self.write(LEDGER_REL, json.dumps(document))

    def files(self) -> list[str]:
        return sorted(
            str(path.relative_to(self.root))
            for path in self.root.rglob("*")
            if path.is_file()
        )


class GateCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.gate = load("residue_gate_under_test", "validate-work-residue-ledger.py")

    def setUp(self) -> None:
        self.tree = Tree(self)

    def agree(self, entries=None, rows=None, **kwargs) -> None:
        entries = [entry()] if entries is None else entries
        rows = [row()] if rows is None else rows
        self.tree.ledger(entries)
        self.tree.write(TASK, task_text(rows, **kwargs))

    def findings(self, rule: str | None = None) -> list:
        found = self.gate.check(self.tree.root)
        return [item for item in found if rule is None or item.rule == rule]

    def rules(self) -> list[str]:
        return [item.rule for item in self.findings()]

    def assertRefused(self, rule: str) -> None:
        self.assertIn(rule, self.rules())


class AgreementTests(GateCase):
    def test_agreeing_ledger_and_task_pass(self) -> None:
        self.agree()
        self.assertEqual(self.rules(), [])

    def test_empty_ledger_with_no_residue_table_passes(self) -> None:
        self.tree.ledger([])
        self.tree.write(TASK, task_text())
        self.assertEqual(self.rules(), [])

    def test_pruned_terminal_row_passes(self) -> None:
        self.agree(entries=[], rows=[row(state="terminal", closure="EVD-001")])
        self.assertEqual(self.rules(), [])

    def test_ordinary_text_does_not_trip_the_copied_value_scan(self) -> None:
        text = "unverified until version 3.0.0 is adopted"
        self.agree(
            entries=[entry(owner="buenhyden", resume=text)],
            rows=[row(owner="buenhyden", resume=text)],
        )
        self.assertEqual(self.rules(), [])

    def test_main_prints_one_pass_line_and_exits_zero(self) -> None:
        self.agree()
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = self.gate.main(["--root", str(self.tree.root)])
        self.assertEqual(code, 0)
        self.assertEqual(len(out.getvalue().splitlines()), 1)
        self.assertTrue(out.getvalue().startswith("PASS"))

    def test_main_prints_one_fail_line_per_finding_and_exits_one(self) -> None:
        self.agree(entries=[])
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = self.gate.main(["--root", str(self.tree.root)])
        self.assertEqual(code, 1)
        lines = (out.getvalue() + err.getvalue()).splitlines()
        self.assertEqual(len(lines), 1)
        self.assertTrue(lines[0].startswith("FAIL RESIDUE-MARKDOWN-ONLY H-1 "))


class SchemaTests(GateCase):
    def test_unknown_key_is_refused(self) -> None:
        bad = entry()
        bad["status"] = "in-progress"
        self.agree(entries=[bad])
        self.assertRefused("RESIDUE-SCHEMA")

    def test_missing_ledger_is_refused(self) -> None:
        self.tree.write(TASK, task_text())
        self.assertRefused("RESIDUE-SCHEMA")

    def test_duplicate_and_unsorted_entries_are_refused(self) -> None:
        self.agree(entries=[entry("H-1"), entry("H-1")], rows=[row("H-1")])
        self.assertRefused("RESIDUE-SCHEMA")
        self.agree(entries=[entry("H-2"), entry("H-1")], rows=[row("H-1"), row("H-2")])
        self.assertRefused("RESIDUE-SCHEMA")

    def test_terminal_needs_closure_and_open_forbids_it(self) -> None:
        terminal = [row(state="terminal", closure="EVD-001")]
        self.agree(entries=[entry(state="terminal")], rows=terminal)
        self.assertRefused("RESIDUE-SCHEMA")
        closure = {"path": TASK, "evidence": "EVD-001"}
        self.agree(entries=[entry(closure=closure)])
        self.assertRefused("RESIDUE-SCHEMA")

    def test_registry_key_belongs_to_adoption_only(self) -> None:
        wrong = entry()
        wrong["source"]["registry_key"] = "common_forms"
        self.agree(entries=[wrong])
        self.assertRefused("RESIDUE-SCHEMA")
        self.agree(entries=[entry("A-1", kind="adoption")], rows=[row("A-1")])
        self.assertRefused("RESIDUE-SCHEMA")

    def test_missing_registry_block_is_refused(self) -> None:
        del self.tree.registry["work_residue"]
        self.tree.write_registry()
        self.agree()
        self.assertRefused("RESIDUE-SCHEMA")


class MarkdownOnlyTests(GateCase):
    def test_open_live_row_without_entry(self) -> None:
        self.agree(entries=[])
        self.assertRefused("RESIDUE-MARKDOWN-ONLY")

    def test_unregistered_handoff_table(self) -> None:
        self.agree(extra=f"### Stage Handoff\n\n{HANDOFF_TABLE}")
        self.assertRefused("RESIDUE-MARKDOWN-ONLY")

    def test_registered_historical_table_is_exempt(self) -> None:
        self.tree.registry["work_residue"]["historical_tables"] = [
            {"path": TASK, "heading": "Stage Handoff"}
        ]
        self.tree.write_registry()
        self.agree(extra=f"### Stage Handoff\n\n{HANDOFF_TABLE}")
        self.assertEqual(self.rules(), [])

    def test_conflicts_heading_is_a_residue_table(self) -> None:
        self.agree(extra=f"### Conflicts\n\n{HANDOFF_TABLE}")
        self.assertRefused("RESIDUE-MARKDOWN-ONLY")

    def test_first_cell_pattern_marks_a_residue_table(self) -> None:
        body = "| ID | Decision |\n| --- | --- |\n| W03-H01 | gap |\n"
        self.agree(extra=f"### Decisions\n\n{body}")
        self.assertRefused("RESIDUE-MARKDOWN-ONLY")

    def test_decision_row_is_not_a_handoff_row(self) -> None:
        body = "| ID | Decision |\n| --- | --- |\n| W03-D40 | chosen |\n"
        self.agree(extra=f"### Decisions\n\n{body}")
        self.assertEqual(self.rules(), [])

    def test_live_table_outside_task_evidence_is_refused(self) -> None:
        self.tree.ledger([])
        extra = f"## Elsewhere\n\n### Residue Handoff\n\n{table(COLUMNS, [row()])}"
        self.tree.write(TASK, task_text(extra=extra))
        self.assertRefused("RESIDUE-MARKDOWN-ONLY")

    def test_second_live_heading_is_refused(self) -> None:
        self.agree(extra="### Residue Handoff\n\n| ID |\n| --- |\n| H-9 |\n")
        self.assertRefused("RESIDUE-MARKDOWN-ONLY")

    def test_live_table_with_other_columns_is_refused(self) -> None:
        self.tree.ledger([])
        extra = "### Residue Handoff\n\n| ID | State |\n| --- | --- |\n| H-1 | open |\n"
        self.tree.write(TASK, task_text(extra=extra))
        self.assertRefused("RESIDUE-MARKDOWN-ONLY")


class JsonOnlyAndDriftTests(GateCase):
    def test_open_entry_without_a_live_row(self) -> None:
        self.agree(rows=[row("H-2")], entries=[entry("H-1"), entry("H-2")])
        self.assertRefused("RESIDUE-JSON-ONLY")

    def test_state_owner_and_resume_condition_drift(self) -> None:
        cases = (
            ({"state": "terminal", "closure": "EVD-001"}, "state"),
            ({"owner": "W05"}, "owner"),
            ({"resume": "later"}, "resume_condition"),
        )
        for kwargs, field in cases:
            with self.subTest(field):
                self.agree(rows=[row(**kwargs)])
                drift = self.findings("RESIDUE-DRIFT")
                self.assertEqual(len(drift), 1)
                self.assertIn(field, drift[0].detail)

    def test_row_text_is_compared_after_whitespace_removal_only(self) -> None:
        padded = f"|  H-1  | text |  open  |  W03  |  {RESUME}  | none |"
        self.agree(rows=[padded])
        self.assertEqual(self.rules(), [])
        self.agree(rows=[row(owner="w03")])
        self.assertRefused("RESIDUE-DRIFT")

    def test_entry_sourced_in_another_task_than_its_row(self) -> None:
        self.agree(entries=[entry(path=OTHER_TASK)])
        self.tree.write(OTHER_TASK, task_text([]))
        self.assertRefused("RESIDUE-DRIFT")


class ClosureTests(GateCase):
    def terminal(self, evidence: str = "EVD-001", path: str = TASK) -> dict:
        return entry(state="terminal", closure={"path": path, "evidence": evidence})

    def test_terminal_entry_with_pass_closure_and_terminal_row(self) -> None:
        self.agree(
            entries=[self.terminal()], rows=[row(state="terminal", closure="EVD-001")]
        )
        self.assertEqual(self.rules(), [])

    def test_terminal_entry_without_a_pass_row(self) -> None:
        for evidence in ("EVD-002", "EVD-009"):
            with self.subTest(evidence):
                self.agree(
                    entries=[self.terminal(evidence)],
                    rows=[row(state="terminal", closure=evidence)],
                )
                self.assertRefused("RESIDUE-CLOSURE")

    def test_terminal_entry_whose_live_row_is_open_or_differs(self) -> None:
        self.agree(entries=[self.terminal()], rows=[row()])
        self.assertRefused("RESIDUE-CLOSURE")
        self.agree(
            entries=[self.terminal()],
            rows=[row(state="terminal", closure="EVD-002")],
            evidence={"EVD-001": "PASS", "EVD-002": "PASS"},
        )
        self.assertRefused("RESIDUE-CLOSURE")

    def test_closure_path_differs_from_the_task_source(self) -> None:
        self.tree.write(OTHER_TASK, task_text())
        self.agree(
            entries=[self.terminal(path=OTHER_TASK)],
            rows=[row(state="terminal", closure="EVD-001")],
        )
        self.assertRefused("RESIDUE-CLOSURE")

    def test_terminal_live_row_must_resolve_to_a_pass_row(self) -> None:
        for closure in ("none", "EVD-002", "EVD-009"):
            with self.subTest(closure):
                self.agree(entries=[], rows=[row(state="terminal", closure=closure)])
                self.assertRefused("RESIDUE-CLOSURE")

    def test_open_live_row_carries_no_closure(self) -> None:
        self.agree(rows=[row(closure="EVD-001")])
        self.assertRefused("RESIDUE-CLOSURE")

    def test_survey_entry_may_close_in_a_task_without_a_row(self) -> None:
        self.tree.write("docs/03.specs/note.md", "# Note\n")
        survey = entry(
            "S-1",
            kind="survey",
            state="terminal",
            path="docs/03.specs/note.md",
            closure={"path": TASK, "evidence": "EVD-001"},
        )
        self.agree(entries=[entry(), survey])
        self.assertEqual(self.rules(), [])


class SourceTests(GateCase):
    def test_source_that_does_not_resolve(self) -> None:
        self.agree(entries=[entry(path="docs/03.specs/0009-z/tasks/tsk-0001-z.md")])
        self.assertRefused("RESIDUE-SOURCE")

    def test_source_task_that_left_the_tree(self) -> None:
        self.agree()
        (self.tree.root / TASK).unlink()
        self.assertRefused("RESIDUE-SOURCE")

    def test_closure_task_that_left_the_tree(self) -> None:
        closure = {"path": OTHER_TASK, "evidence": "EVD-001"}
        self.agree(
            entries=[entry(state="terminal", closure=closure)],
            rows=[row(state="terminal", closure="EVD-001")],
        )
        self.assertRefused("RESIDUE-SOURCE")

    def test_stage_90_and_archive_sources_are_refused(self) -> None:
        for path in ("docs/90.references/a.md", "docs/98.archive/a.md"):
            with self.subTest(path):
                self.tree.write(path, "# A\n")
                self.agree(entries=[entry("S-1", kind="survey", path=path)], rows=[])
                self.assertRefused("RESIDUE-SOURCE")

    def test_handoff_sourced_outside_a_task(self) -> None:
        self.tree.write("docs/03.specs/note.md", "# Note\n")
        self.agree(entries=[entry(path="docs/03.specs/note.md")])
        self.assertRefused("RESIDUE-SOURCE")

    def test_path_outside_the_root_is_refused(self) -> None:
        self.agree(
            entries=[entry("S-1", kind="survey", path="docs/../../outside.md")],
            rows=[],
        )
        self.assertRefused("RESIDUE-SOURCE")

    def test_historical_table_whose_task_left_the_tree(self) -> None:
        self.tree.registry["work_residue"]["historical_tables"] = [
            {"path": OTHER_TASK, "heading": "Stage Handoff"}
        ]
        self.tree.write_registry()
        self.agree()
        self.assertRefused("RESIDUE-SOURCE")

    def test_historical_table_whose_heading_is_absent(self) -> None:
        self.tree.registry["work_residue"]["historical_tables"] = [
            {"path": TASK, "heading": "Stage Handoff"}
        ]
        self.tree.write_registry()
        self.agree()
        self.assertRefused("RESIDUE-SOURCE")

    def test_adoption_entry_may_be_sourced_at_the_registry(self) -> None:
        adoption = entry("A-1", kind="adoption", path=REGISTRY_REL)
        adoption["source"]["registry_key"] = "common_forms"
        self.agree(entries=[adoption], rows=[])
        self.assertEqual(self.rules(), [])


class ResidueOnlyTests(GateCase):
    def adoption(self, key: str = "common_forms", **kwargs) -> dict:
        value = entry("A-1", kind="adoption", path=REGISTRY_REL, **kwargs)
        value["source"]["registry_key"] = key
        return value

    def test_registry_key_absent_from_the_registry(self) -> None:
        del self.tree.registry["common_forms"]
        self.tree.write_registry()
        self.agree(entries=[self.adoption()], rows=[])
        self.assertRefused("RESIDUE-REGISTRY-COPY")

    def test_copied_contract_identifier_digest_revision_and_approval(self) -> None:
        shared = self.tree.registry["shared_contract"]
        values = (
            "COMMON-DOC-FORM-1",
            shared["contract_id"],
            shared["content_digest"],
            shared["source_revision"],
            shared["approval_ref"],
        )
        for value in values:
            with self.subTest(value):
                text = f"record {value} first"
                self.agree(
                    entries=[self.adoption(resume=text)],
                    rows=[row("A-1", resume=text)],
                )
                self.assertRefused("RESIDUE-REGISTRY-COPY")

    def test_every_task_status_and_result_state_is_refused(self) -> None:
        registry = json.loads((REPOSITORY_ROOT / REGISTRY_REL).read_text("utf-8"))
        profile = next(p for p in registry["profiles"] if p["id"] == "sdlc/task")
        execution = profile["relationships"]["body_contract"]["task_execution"]
        values = set(profile["lifecycle"]["status_domain"])
        values |= set(execution["evidence_result_states"])
        for states in execution["result_states"].values():
            values |= set(states)
        self.assertGreaterEqual(len(values), 8)
        for value in sorted(values):
            with self.subTest(value=value, where="row"):
                self.agree(rows=[row(state=value)])
                self.assertRefused("RESIDUE-TASK-STATUS")
            with self.subTest(value=value, where="entry"):
                self.agree(entries=[entry(state=value)])
                self.assertRefused("RESIDUE-TASK-STATUS")

    def test_location_and_name_are_not_a_progress_ledger(self) -> None:
        self.assertEqual(self.gate.LEDGER, LEDGER_REL)
        path = Path(self.gate.LEDGER)
        self.assertNotIn("memory", path.parts)
        self.assertNotIn(".agents", path.parts)
        self.assertFalse(path.name.startswith("progress."))
        schema = (REPOSITORY_ROOT / SCHEMA_REL).read_text("utf-8")
        self.assertNotIn("progress", schema.lower())


class ViewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.view = load("residue_view_under_test", "work-residue-ledger.py")

    def setUp(self) -> None:
        self.tree = Tree(self)
        closure = {"path": TASK, "evidence": "EVD-001"}
        self.tree.ledger(
            [
                entry("H-1", owner="W03"),
                entry("H-2", owner="W05", kind="conflict"),
                entry("H-3", state="terminal", owner="W03", closure=closure),
            ]
        )

    def run_view(self, *argv: str) -> tuple[int, list[str], str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = self.view.main(["--root", str(self.tree.root), *argv])
        return code, out.getvalue().splitlines(), err.getvalue()

    def ids(self, *argv: str) -> list[str]:
        code, lines, _ = self.run_view(*argv)
        self.assertEqual(code, 0)
        return [line.split("\t")[0] for line in lines]

    def test_one_line_per_entry_with_every_field(self) -> None:
        code, lines, _ = self.run_view()
        self.assertEqual(code, 0)
        self.assertEqual(len(lines), 3)
        self.assertEqual(
            lines[0].split("\t"),
            ["H-1", "handoff", "open", "W03", RESUME, TASK],
        )

    def test_filters_by_kind_state_and_owner(self) -> None:
        self.assertEqual(self.ids("--kind", "conflict"), ["H-2"])
        self.assertEqual(self.ids("--state", "terminal"), ["H-3"])
        self.assertEqual(self.ids("--owner", "W03"), ["H-1", "H-3"])
        self.assertEqual(self.ids("--owner", "W03", "--state", "open"), ["H-1"])

    def test_writes_no_file(self) -> None:
        before = self.tree.files()
        self.run_view("--state", "open")
        self.assertEqual(self.tree.files(), before)

    def test_unreadable_ledger_exits_two(self) -> None:
        (self.tree.root / LEDGER_REL).write_text("{", encoding="utf-8")
        code, lines, err = self.run_view()
        self.assertEqual((code, lines), (2, []))
        self.assertTrue(err.startswith("FAIL WORK-RESIDUE"))


if __name__ == "__main__":
    unittest.main()
