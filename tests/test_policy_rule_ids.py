"""SPEC-0194: the policy rule ID contract, its registry section and document rules."""

from __future__ import annotations

import copy
import dataclasses
import importlib.util
import json
import sys
import unittest
from pathlib import Path, PurePosixPath

from tests.form_headings import form_body

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import document_authority as AUTHORITY  # noqa: E402
import document_contracts as CONTRACTS  # noqa: E402
from common_document_contract import payload_markdown  # noqa: E402

REGISTRY_FILE = ROOT / "docs/99.templates/registry.json"
SCHEMA_FILE = ROOT / "docs/99.templates/01.contracts/document-profile.schema.json"
TEMPLATES = {
    "common/template-governance-rule": "docs/99.templates/02.templates/93.common/rule.template.md",
    "common/template-operation-policy": "docs/99.templates/02.templates/05.operations/policy.template.md",
}
# SPEC-0222: the core Rules table and the local Rule Levels table keyed by Rule ID.
CORE_COLUMNS = ("Rule ID", "Condition", "Requirement", "Enforcement", "Evidence")
LEVEL_COLUMNS = ("Rule ID", "Level", "Status")
FORMER_COLUMNS = ("Rule ID", "Condition", "Level", "Evidence", "Status")
CODES = {
    ".agents/governance/agent-execution.md": "EXEC",
    ".agents/governance/approval-and-safety.md": "SAFE",
    ".agents/governance/git.md": "GIT",
    "docs/00.workspace/04.quality/approval-and-safety.md": "SAFE",
    ".agents/governance/context-and-memory.md": "CTX",
    "docs/00.workspace/03.process/document-authoring.md": "AUTHOR",
    "docs/00.workspace/03.process/document-lifecycle.md": "DOCLIFE",
    "docs/00.workspace/04.quality/formatting-and-linting.md": "FMT",
    "docs/00.workspace/03.process/git.md": "GIT",
    ".agents/governance/model-selection.md": "MODEL",
    "docs/00.workspace/04.quality/quality.md": "QUAL",
    "docs/00.workspace/03.process/sdlc.md": "SDLC",
    "docs/05.operations/02.policies/0001-k8s-gitops-operations-policy.md": "GITOPS",
    "docs/05.operations/02.policies/0003-service-mesh-cert-manager-policy.md": "MESH",
    "docs/05.operations/02.policies/0004-rollouts-notifications-headlamp-policy.md": "ROLLOUT",
    "docs/05.operations/02.policies/0005-observability-platform-operations-policy.md": "OBSERV",
    "docs/05.operations/02.policies/0007-app-gitops-onboarding-policy.md": "ONBOARD",
}
LEVELS = ["required", "recommended", "optional"]
SYNTHETIC = PurePosixPath(".agents/governance/synthetic.md")
KOREAN = PurePosixPath("docs/05.operations/02.policies/9999-synthetic.md")


def _load_script(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


MARKDOWN = _load_script("policy_rule_ids_markdown", "validate-markdown-profiles.py")


def raw_registry() -> dict:
    return json.loads(REGISTRY_FILE.read_text("utf-8"))


def record_rules(raw: dict) -> set[str]:
    return {
        item.rule_id
        for item in CONTRACTS.current_registry_diagnostics(ROOT, raw)
        if item.rule_id == "REGISTRY_POLICY_RULE_CODE"
    }


def load_rules(raw: dict) -> set[str]:
    try:
        CONTRACTS.validate_registry(ROOT, raw)
    except CONTRACTS.DocumentContractError as error:
        return {item.rule_id for item in error.diagnostics}
    return set()


def policy_profile(profile_id: str, path: PurePosixPath, recorded: bool, code="SYN"):
    """The loaded profile with one synthetic record, or none when not recorded."""

    profile = {p.profile_id: p for p in CONTRACTS.load_registry(ROOT).profiles}[
        profile_id
    ]
    ids = profile.policy_rule_ids
    codes = (CONTRACTS.PolicyRuleCode(path.as_posix(), code),) if recorded else ()
    return dataclasses.replace(
        profile, policy_rule_ids=dataclasses.replace(ids, codes=codes)
    )


# One set of fragments per document language; the IDs, column names and the Level
# and Status values are the same ASCII text in both (W03-D42).
LANGUAGES = {
    "en": {
        "profile": "governance/rule",
        "path": SYNTHETIC,
        "one": "Review every change before merge.",
        "two": "Record the review result.",
        "when": "Every change",
        "proof": "CI log",
        "prose": "Reviewers keep changes small.",
        "control": "Platform owner",
    },
    "ko": {
        "profile": "operation/policy",
        "path": KOREAN,
        "one": "모든 변경은 병합 전에 검토한다.",
        "two": "검토 결과를 기록한다.",
        "when": "모든 변경",
        "proof": "CI 기록",
        "prose": "검토자는 변경을 작게 유지한다.",
        "control": "플랫폼 소유자",
    },
}


class Fixture:
    """One synthetic policy for a language; runs the document rules over a body.

    SPEC-0222: the core Rules table holds each active rule with its text, and the
    Rule Levels table keyed by Rule ID holds every issued ID, its level and status.
    """

    def __init__(self, language: str, recorded: bool = True, code="SYN"):
        self.text = LANGUAGES[language]
        self.path = self.text["path"]
        self.profile = policy_profile(self.text["profile"], self.path, recorded, code)

    def item(self, number: int, text: str, token: bool = True) -> str:
        lead = f"`SYN-R{number:03d}` " if token else ""
        return f"- {lead}{text}"

    def rule(self, number, text: str | None = None, code="SYN") -> str:
        identifier = f"{code}-R{number:03d}" if isinstance(number, int) else number
        text = self.text["one"] if text is None else text
        return f"| {identifier} | {self.text['when']} | {text} | {self.text['proof']} | none |"

    @staticmethod
    def level(number, level="required", status="active", code="SYN") -> str:
        identifier = f"{code}-R{number:03d}" if isinstance(number, int) else number
        return f"| {identifier} | {level} | {status} |"

    @staticmethod
    def table(*rows: str, header=CORE_COLUMNS) -> str:
        head = "| " + " | ".join(header) + " |"
        rule = "| " + " | ".join("---" for _ in header) + " |"
        return "\n".join([head, rule, *rows])

    def tables(self, *numbers: int, retired: tuple[int, ...] = ()) -> str:
        """Both rule tables for the given rule numbers; `retired` ones leave Rules."""

        core = self.table(*(self.rule(n) for n in numbers if n not in retired))
        levels = self.table(
            *(
                self.level(n, status="retired; none" if n in retired else "active")
                for n in numbers
            ),
            header=LEVEL_COLUMNS,
        )
        return core + "\n\n" + levels

    def good(self) -> str:
        return self.tables(1, 2)

    @staticmethod
    def body(requirements: str) -> str:
        # Requirements and the sibling section that ends it, from the policy form.
        sections = {
            "Requirements": [requirements.strip("\n")],
            "Exceptions": ["Checks run in CI."],
        }
        return (
            "# Policy\n\n"
            + "\n\n".join(form_body("policy", sections, partial=True))
            + "\n"
        )

    def found(self, body: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._policy_rule_diagnostics(self.path, self.profile, body)
        )

    def rules(self, requirements: str) -> list[str]:
        return self.found(self.body(requirements))

    def control(self) -> str:
        return (
            "#### Control Register\n\n"
            "| Control | Accountable role | Enforcement surface | Evidence |\n"
            "| --- | --- | --- | --- |\n"
            f"| PLAT-001 topology | {self.text['control']} | CI | log |\n"
            f"| `PLAT-002` | {self.text['control']} | CI | log |"
        )


class EachLanguage(unittest.TestCase):
    def each(self, check, recorded: bool = True) -> None:
        for language in LANGUAGES:
            with self.subTest(language=language):
                check(Fixture(language, recorded))


class RuleCodeTests(EachLanguage):
    def test_an_adopted_policy_with_rules_and_a_record_passes(self) -> None:
        self.each(lambda f: self.assertEqual(f.rules(f.good()), []))

    def test_a_policy_with_normative_rules_and_no_record_fails(self) -> None:
        self.each(
            lambda f: self.assertEqual(
                f.rules(f.item(1, f.text["one"], token=False)), ["POLICY-RULE-CODE"]
            ),
            recorded=False,
        )

    def test_a_policy_with_a_table_and_no_record_fails(self) -> None:
        self.each(
            lambda f: self.assertEqual(f.rules(f.good()), ["POLICY-RULE-CODE"]),
            recorded=False,
        )

    def test_a_policy_that_states_no_rule_needs_no_record(self) -> None:
        self.each(
            lambda f: self.assertEqual(f.rules(f.text["prose"]), []), recorded=False
        )

    def test_a_policy_without_a_requirements_section_is_not_read(self) -> None:
        sections = {"Exceptions": ["Checks run in CI."]}
        body = (
            "# Policy\n\n"
            + "\n\n".join(form_body("policy", sections, partial=True))
            + "\n"
        )
        self.each(lambda f: self.assertEqual(f.found(body), []), recorded=False)

    def test_a_profile_without_the_section_is_not_read(self) -> None:
        f = Fixture("en")
        f.profile = dataclasses.replace(f.profile, policy_rule_ids=None)
        self.assertEqual(f.rules(f.item(1, "x", token=False)), [])


class RuleTableTests(EachLanguage):
    def test_a_prose_only_policy_passes_without_a_table(self) -> None:
        self.each(lambda f: self.assertEqual(f.rules(f.text["prose"]), []))

    def test_header_only_tables_pass_when_no_rule_is_stated(self) -> None:
        self.each(lambda f: self.assertEqual(f.rules(f.tables()), []))

    def test_missing_tables_fail_when_rules_are_stated(self) -> None:
        def check(f: Fixture) -> None:
            found = f.rules(f.item(1, f.text["one"], token=False))
            self.assertEqual(set(found), {"POLICY-RULE-COVERAGE", "POLICY-RULE-TABLE"})
            # Each of the two tables is named once.
            self.assertEqual(found.count("POLICY-RULE-TABLE"), 2)
            only_core = f.table(f.rule(1))
            self.assertIn("POLICY-RULE-TABLE", f.rules(only_core))

        self.each(check)

    def test_the_former_five_column_table_is_not_read(self) -> None:
        def check(f: Fixture) -> None:
            former = f.table(
                "| SYN-R001 | when | required | proof | active |", header=FORMER_COLUMNS
            )
            self.assertIn("POLICY-RULE-TABLE", f.rules(former))
            self.assertEqual(MARKDOWN.policy_rule_rows(f.body(former)), ())

        self.each(check)

    def test_a_level_table_without_the_status_column_fails(self) -> None:
        def check(f: Fixture) -> None:
            levels = f.table("| SYN-R001 | required |", header=LEVEL_COLUMNS[:2])
            self.assertIn(
                "POLICY-RULE-TABLE", f.rules(f.table(f.rule(1)) + "\n\n" + levels)
            )

        self.each(check)

    def test_a_reordered_relabeled_or_extra_column_fails(self) -> None:
        def check(f: Fixture) -> None:
            for header in (
                (CORE_COLUMNS[0], CORE_COLUMNS[2], CORE_COLUMNS[1], *CORE_COLUMNS[3:]),
                (*CORE_COLUMNS, "Note"),
                (*CORE_COLUMNS[:3], "Evidence", "Enforcement"),
            ):
                row = "| SYN-R001 | " + " | ".join("x" for _ in header[1:]) + " |"
                tables = (
                    f.table(row, header=header)
                    + "\n\n"
                    + f.table(f.level(1), header=LEVEL_COLUMNS)
                )
                with self.subTest(header=header):
                    self.assertIn("POLICY-RULE-TABLE", f.rules(tables))

        self.each(check)

    def test_a_level_is_one_of_the_three_registered_values(self) -> None:
        def run(f: Fixture, level: str) -> list[str]:
            levels = f.table(f.level(1, level=level), header=LEVEL_COLUMNS)
            return f.rules(f.table(f.rule(1)) + "\n\n" + levels)

        def check(f: Fixture) -> None:
            for level in ("must", "Required", "", "required;"):
                with self.subTest(level=level):
                    self.assertEqual(run(f, level), ["POLICY-RULE-TABLE"])
            for level in LEVELS:
                with self.subTest(level=level):
                    self.assertEqual(run(f, level), [])

        self.each(check)

    def test_two_tables_or_a_table_outside_requirements_fail(self) -> None:
        def check(f: Fixture) -> None:
            self.assertIn(
                "POLICY-RULE-TABLE", f.rules(f.good() + "\n\n" + f.table(f.rule(1)))
            )
            outside = f.body(f.good()).replace(
                "Checks run in CI.", "Checks run in CI.\n\n" + f.table(f.rule(1))
            )
            self.assertIn("POLICY-RULE-TABLE", f.found(outside))

        self.each(check)

    def test_the_status_is_active_or_retired_with_a_successor(self) -> None:
        def run(f: Fixture, status: str) -> list[str]:
            levels = f.table(
                f.level(1), f.level(2, status=status), header=LEVEL_COLUMNS
            )
            core = f.table(f.rule(1), *((f.rule(2),) if status == "active" else ()))
            return f.rules(core + "\n\n" + levels)

        def check(f: Fixture) -> None:
            self.assertEqual(run(f, "retired; none"), [])
            self.assertEqual(run(f, "retired; SYN-R001"), [])
            for status in (
                "retired",
                "retired;none",
                "retired; SYN-R009",
                "retired; SYN-R002",
                "retired; OTH-R001",
                "Active",
                "",
            ):
                with self.subTest(status=status):
                    self.assertIn("POLICY-RULE-TABLE", run(f, status))

        self.each(check)

    def test_the_rules_table_holds_exactly_the_active_rules_in_order(self) -> None:
        def check(f: Fixture) -> None:
            self.assertEqual(f.rules(f.tables(1, 2, 3, retired=(2,))), [])
            levels = f.table(f.level(1), f.level(2), header=LEVEL_COLUMNS)
            for label, core in (
                ("missing", f.table(f.rule(1))),
                ("reordered", f.table(f.rule(2), f.rule(1))),
                ("extra", f.table(f.rule(1), f.rule(2), f.rule(3))),
            ):
                with self.subTest(case=label):
                    self.assertIn("POLICY-RULE-TABLE", f.rules(core + "\n\n" + levels))
            retired = f.table(
                f.level(1), f.level(2, status="retired; none"), header=LEVEL_COLUMNS
            )
            core = f.table(f.rule(1), f.rule(2))
            self.assertIn("POLICY-RULE-TABLE", f.rules(core + "\n\n" + retired))

        self.each(check)

    def test_every_core_cell_holds_a_value(self) -> None:
        def check(f: Fixture) -> None:
            levels = f.table(f.level(1), header=LEVEL_COLUMNS)
            for empty in (
                f"| SYN-R001 | {f.text['when']} |  | {f.text['proof']} | none |",
                f"| SYN-R001 |  | {f.text['one']} | {f.text['proof']} | none |",
                f"| SYN-R001 | {f.text['when']} | {f.text['one']} | {f.text['proof']} |  |",
            ):
                with self.subTest(row=empty):
                    self.assertEqual(
                        f.rules(f.table(empty) + "\n\n" + levels),
                        ["POLICY-RULE-TABLE"],
                    )

        self.each(check)

    def test_a_table_keyed_by_rule_id_names_active_rules_only(self) -> None:
        def check(f: Fixture) -> None:
            keyed = f.table(
                f"| SYN-R001 | {f.text['two']} |", header=("Rule ID", "Detail")
            )
            self.assertEqual(f.rules(f.good() + "\n\n" + keyed), [])
            for own in ("SYN-R003", "OTH-R001"):
                stray = f.table(f"| {own} | x |", header=("Rule ID", "Detail"))
                with self.subTest(row=own):
                    self.assertIn(
                        "POLICY-RULE-TABLE", f.rules(f.good() + "\n\n" + stray)
                    )
            retired = f.table("| SYN-R002 | x |", header=("Rule ID", "Detail"))
            self.assertIn(
                "POLICY-RULE-TABLE",
                f.rules(f.tables(1, 2, retired=(2,)) + "\n\n" + retired),
            )

        self.each(check)


class RuleIdTests(EachLanguage):
    def run_rows(self, f: Fixture, *rows: str) -> list[str]:
        levels = f.table(*rows, header=LEVEL_COLUMNS)
        ids = [row.split("|")[1].strip() for row in rows]
        core = f.table(*(f.rule(own) for own in ids))
        return f.rules(core + "\n\n" + levels)

    def test_ascending_rows_from_r001_without_a_gap_pass(self) -> None:
        self.each(
            lambda f: self.assertEqual(
                self.run_rows(f, f.level(1), f.level(2), f.level(3)), []
            )
        )

    def test_a_gap_a_duplicate_a_late_start_or_a_descent_fails(self) -> None:
        def check(f: Fixture) -> None:
            for label, rows in (
                ("gap", (f.level(1), f.level(3))),
                ("duplicate", (f.level(1), f.level(1))),
                ("late start", (f.level(2), f.level(3))),
                ("descent", (f.level(2), f.level(1))),
            ):
                with self.subTest(case=label):
                    self.assertIn("POLICY-RULE-ID", self.run_rows(f, *rows))

        self.each(check)

    def test_a_split_half_holds_exactly_its_registered_rules(self) -> None:
        # SDLC-R036: one half of a split code may skip the other half's IDs,
        # but must hold exactly the rule IDs its registry record lists.
        def check(f: Fixture) -> None:
            ids = f.profile.policy_rule_ids
            record = CONTRACTS.PolicyRuleCode(
                f.path.as_posix(), "SYN", ("SYN-R001", "SYN-R003")
            )
            f.profile = dataclasses.replace(
                f.profile, policy_rule_ids=dataclasses.replace(ids, codes=(record,))
            )
            self.assertEqual(self.run_rows(f, f.level(1), f.level(3)), [])
            for label, rows in (
                ("other half's ID", (f.level(1), f.level(2))),
                ("missing ID", (f.level(1),)),
                ("extra ID", (f.level(1), f.level(3), f.level(4))),
            ):
                with self.subTest(case=label):
                    self.assertIn("POLICY-RULE-ID", self.run_rows(f, *rows))

        self.each(check)

    def test_another_code_or_a_malformed_id_fails(self) -> None:
        def check(f: Fixture) -> None:
            for identifier in (
                "OTH-R001",
                "SYN-R01",
                "SYN-001",
                "syn-R001",
                "SYN-R0011",
            ):
                with self.subTest(identifier=identifier):
                    self.assertIn(
                        "POLICY-RULE-ID", self.run_rows(f, f.level(identifier))
                    )

        self.each(check)

    def test_a_control_cell_is_never_read_as_a_rule_id(self) -> None:
        self.each(
            lambda f: self.assertEqual(f.rules(f.good() + "\n\n" + f.control()), [])
        )


class ReferenceTokenTests(EachLanguage):
    """SPEC-0222: a token left in the body only refers to a current rule."""

    def test_an_h4_reference_names_one_active_row(self) -> None:
        def check(f: Fixture) -> None:
            group = f"#### Group\n\n`SYN-R001`\n\n{f.text['prose']}"
            self.assertEqual(f.rules(f.good() + "\n\n" + group), [])
            unknown = group.replace("SYN-R001", "SYN-R003")
            self.assertEqual(
                f.rules(f.good() + "\n\n" + unknown), ["POLICY-RULE-INLINE"]
            )
            twice = group + "\n\n" + group.replace("Group", "Other")
            self.assertEqual(f.rules(f.good() + "\n\n" + twice), ["POLICY-RULE-INLINE"])
            retired = group.replace("SYN-R001", "SYN-R002")
            self.assertEqual(
                f.rules(f.tables(1, 2, retired=(2,)) + "\n\n" + retired),
                ["POLICY-RULE-INLINE"],
            )

        self.each(check)

    def test_a_token_followed_by_rule_text_is_refused(self) -> None:
        def check(f: Fixture) -> None:
            item = f.item(1, f.text["one"])
            self.assertEqual(f.rules(item + "\n\n" + f.good()), ["POLICY-RULE-INLINE"])
            nested = f"- **Required**:\n  - `SYN-R001` {f.text['one']}"
            self.assertEqual(
                f.rules(nested + "\n\n" + f.good()), ["POLICY-RULE-INLINE"]
            )
            row = (
                "| Item | Meaning |\n| --- | --- |\n"
                f"| `SYN-R001` {f.text['one']} | {f.text['when']} |"
            )
            self.assertEqual(f.rules(row + "\n\n" + f.good()), ["POLICY-RULE-INLINE"])

        self.each(check)

    def test_a_token_only_item_anchors_its_supporting_content(self) -> None:
        def check(f: Fixture) -> None:
            anchored = f"- `SYN-R001`\n  - {f.text['two']}\n  - {f.text['prose']}"
            self.assertEqual(f.rules(anchored + "\n\n" + f.good()), [])

        self.each(check)

    def test_a_reference_outside_a_rule_position_is_not_counted(self) -> None:
        def check(f: Fixture) -> None:
            reference = f"- {f.text['one']} `SYN-R001`"
            self.assertEqual(
                f.rules(reference + "\n\n" + f.good()), ["POLICY-RULE-COVERAGE"]
            )
            prose = f.good() + "\n\nSee `SYN-R001` and `SYN-R002`."
            self.assertEqual(f.rules(prose), [])
            heading = f.good() + "\n\n#### Detail `SYN-R003`\n\nText."
            self.assertEqual(f.rules(heading), [])

        self.each(check)

    def test_a_token_in_a_fence_or_a_comment_is_not_read(self) -> None:
        def check(f: Fixture) -> None:
            for hidden in (
                "```\n- `SYN-R001` fenced\n```",
                "<!-- - `SYN-R001` commented -->",
                "<!--\n- `SYN-R001` commented\n-->",
            ):
                with self.subTest(hidden=hidden):
                    self.assertEqual(f.rules(hidden + "\n\n" + f.good()), [])

        self.each(check)


class CoverageFloorTests(EachLanguage):
    def test_an_item_or_row_without_a_token_fails(self) -> None:
        def check(f: Fixture) -> None:
            items = f.item(1, "x", token=False)
            self.assertEqual(
                f.rules(items + "\n\n" + f.good()), ["POLICY-RULE-COVERAGE"]
            )
            row = f"| Item | Meaning |\n| --- | --- |\n| plain | {f.text['when']} |"
            self.assertEqual(f.rules(row + "\n\n" + f.good()), ["POLICY-RULE-COVERAGE"])

        self.each(check)

    def test_an_h4_group_token_covers_the_items_in_the_group(self) -> None:
        def check(f: Fixture) -> None:
            group = f"#### Group\n\n`SYN-R001`\n\n- {f.text['one']}\n- {f.text['two']}"
            self.assertEqual(f.rules(f.good() + "\n\n" + group), [])
            late = f"#### Group\n\n{f.text['prose']}\n\n`SYN-R001`\n\n- {f.text['one']}"
            self.assertIn("POLICY-RULE-COVERAGE", f.rules(f.good() + "\n\n" + late))
            after = group + f"\n\n#### Other\n\n- {f.text['two']}"
            self.assertIn("POLICY-RULE-COVERAGE", f.rules(f.good() + "\n\n" + after))

        self.each(check)

    def test_a_nested_item_is_not_read_by_the_floor(self) -> None:
        def check(f: Fixture) -> None:
            nested = f"- `SYN-R001`\n  - {f.text['two']}"
            self.assertEqual(f.rules(nested + "\n\n" + f.good()), [])

        self.each(check)

    def test_a_label_over_token_only_nested_items_is_covered(self) -> None:
        def check(f: Fixture) -> None:
            nested = "  - `SYN-R001`\n  - `SYN-R002`"
            for label in (
                "**Required**:",
                "Allowed:",
                "**Disallowed**:",
                "__Allowed__:",
            ):
                with self.subTest(label=label):
                    self.assertEqual(f.rules(f"- {label}\n{nested}\n\n{f.good()}"), [])

        self.each(check)

    def test_a_label_over_a_partly_tokened_or_untokened_list_fails(self) -> None:
        def check(f: Fixture) -> None:
            partly = f"- **Required**:\n  - `SYN-R001`\n  - {f.text['two']}"
            self.assertEqual(
                f.rules(partly + "\n\n" + f.good()), ["POLICY-RULE-COVERAGE"]
            )
            plain = f"- **Required**:\n  - {f.text['one']}\n  - {f.text['two']}"
            self.assertIn("POLICY-RULE-COVERAGE", f.rules(plain + "\n\n" + f.good()))
            bare = "- **Required**:"
            self.assertIn("POLICY-RULE-COVERAGE", f.rules(f.good() + "\n\n" + bare))

        self.each(check)

    def test_control_register_and_rule_table_rows_are_exempt(self) -> None:
        def check(f: Fixture) -> None:
            self.assertEqual(f.rules(f.control()), [])
            self.assertEqual(f.rules(f.good() + "\n\n" + f.control()), [])

        self.each(check)

    def test_a_paragraph_outside_every_unit_is_not_read(self) -> None:
        self.each(
            lambda f: self.assertEqual(f.rules(f.good() + "\n\n" + f.text["prose"]), [])
        )


class GateRetiredTests(EachLanguage):
    """SPEC-0204: no adoption state stands between a policy and the contract."""

    def test_a_record_with_a_state_key_is_refused(self) -> None:
        for state in ("pending", "adopted"):
            with self.subTest(state=state):
                raw = raw_registry()
                raw["policy_rule_ids"]["codes"][0]["state"] = state
                self.assertIn("REGISTRY_SCHEMA", load_rules(raw))

    def test_rules_with_a_record_and_no_rule_tables_are_refused(self) -> None:
        self.each(
            lambda f: self.assertIn(
                "POLICY-RULE-TABLE", f.rules(f.item(1, f.text["one"], token=False))
            )
        )

    def test_header_only_rule_tables_are_refused_when_rules_are_stated(self) -> None:
        self.each(
            lambda f: self.assertIn(
                "POLICY-RULE-TABLE",
                f.rules("#### Group\n\n`SYN-R001`\n\n- x\n\n" + f.tables()),
            )
        )

    def test_a_policy_that_states_no_normative_rule_needs_no_table_or_record(
        self,
    ) -> None:
        self.each(lambda f: self.assertEqual(f.rules(f.text["prose"]), []))
        self.each(
            lambda f: self.assertEqual(f.rules(f.text["prose"]), []), recorded=False
        )


class RegistryRecordTests(unittest.TestCase):
    def test_the_repository_registry_carries_the_section(self) -> None:
        raw = raw_registry()
        section = raw["policy_rule_ids"]
        self.assertEqual(section["code_pattern"], "^[A-Z][A-Z0-9]{1,7}$")
        self.assertEqual(section["levels"], LEVELS)
        self.assertEqual(section["reserved_codes"], ["PLAT", "OBS"])
        self.assertEqual(
            section["rules_table"],
            {
                "condition": "the policy states normative rules",
                "minimum_rows": 1,
                "core_table": "Rules",
                "level_table": "Rule Levels",
            },
        )
        self.assertEqual({i["path"]: i["code"] for i in section["codes"]}, CODES)
        self.assertEqual(len({i["code"] for i in section["codes"]}), 15)
        split = {"SAFE", "GIT"}
        for item in section["codes"]:
            self.assertEqual(
                set(item),
                {"path", "code", "rules"}
                if item["code"] in split
                else {"path", "code"},
            )
            self.assertRegex(item["code"], section["code_pattern"])
            self.assertNotIn(item["code"], section["reserved_codes"])
        self.assertEqual(record_rules(raw), set())
        self.assertEqual(load_rules(raw), set())

    def test_a_split_code_gives_every_rule_id_one_owner(self) -> None:
        # SDLC-R036: SAFE and GIT span a workspace (W) and an agent (A) policy.
        raw = raw_registry()
        records = [i for i in raw["policy_rule_ids"]["codes"] if i["code"] == "SAFE"]
        self.assertEqual(len(records), 2)
        owned = [rule for item in records for rule in item["rules"]]
        self.assertEqual(len(owned), len(set(owned)))
        self.assertEqual(len(owned), 21)

        twice = copy.deepcopy(raw)
        first, second = [
            i for i in twice["policy_rule_ids"]["codes"] if i["code"] == "SAFE"
        ]
        second["rules"].append(first["rules"][0])
        self.assertEqual(record_rules(twice), {"REGISTRY_POLICY_RULE_CODE"})

        unlisted = copy.deepcopy(raw)
        half = next(
            i for i in unlisted["policy_rule_ids"]["codes"] if i["code"] == "GIT"
        )
        del half["rules"]
        self.assertEqual(record_rules(unlisted), {"REGISTRY_POLICY_RULE_CODE"})

        foreign = copy.deepcopy(raw)
        half = next(
            i for i in foreign["policy_rule_ids"]["codes"] if i["code"] == "GIT"
        )
        half["rules"].append("SAFE-R099")
        self.assertEqual(record_rules(foreign), {"REGISTRY_POLICY_RULE_CODE"})

    def test_the_loader_copies_the_section_to_the_authored_policy_profiles(
        self,
    ) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        ids = registry.policy_rule_ids
        self.assertEqual({r.path: r.code for r in ids.codes}, CODES)
        self.assertEqual(ids.levels, tuple(LEVELS))
        self.assertEqual(ids.rules_table_minimum_rows, 1)
        self.assertEqual(
            (ids.rules_table_name, ids.level_table_name), ("Rules", "Rule Levels")
        )
        for profile in registry.profiles:
            with self.subTest(profile=profile.profile_id):
                carries = (
                    profile.document_role == "policy" and profile.mode == "authored"
                )
                self.assertIs(profile.policy_rule_ids is ids, carries)

    def test_a_missing_section_is_refused_by_the_strict_check_only(self) -> None:
        raw = raw_registry()
        del raw["policy_rule_ids"]
        self.assertIn("REGISTRY_POLICY_RULE_CODE", record_rules(raw))
        loaded = CONTRACTS.validate_registry(ROOT, raw)
        self.assertIsNone(loaded.policy_rule_ids)
        self.assertTrue(all(p.policy_rule_ids is None for p in loaded.profiles))

    def test_each_registry_refusal(self) -> None:
        def refuse(mutate) -> set[str]:
            raw = raw_registry()
            mutate(raw["policy_rule_ids"])
            return record_rules(raw)

        cases = {
            "not a tracked document": lambda s: s["codes"][0].update(
                path=".agents/governance/absent.md"
            ),
            "not an authored policy document": lambda s: s["codes"][0].update(
                path="docs/05.operations/02.policies/README.md"
            ),
            "not a policy profile": lambda s: s["codes"][0].update(
                path="docs/03.specs/README.md"
            ),
            "repeated path": lambda s: s["codes"][1].update(path=s["codes"][0]["path"]),
            "repeated code": lambda s: s["codes"][1].update(code=s["codes"][0]["code"]),
            "code outside the pattern": lambda s: s["codes"][0].update(code="a"),
            "code too long": lambda s: s["codes"][0].update(code="ABCDEFGHI"),
            "reserved PLAT": lambda s: s["codes"][0].update(code="PLAT"),
            "reserved OBS": lambda s: s["codes"][0].update(code="OBS"),
            "levels short": lambda s: s.update(levels=["required", "optional"]),
            "levels extra": lambda s: s.update(levels=[*LEVELS, "never"]),
            "levels renamed": lambda s: s.update(
                levels=["required", "recommended", "mandatory"]
            ),
            "core table not a template table": lambda s: s["rules_table"].update(
                core_table="Rule Table"
            ),
            "level table not a template table": lambda s: s["rules_table"].update(
                level_table="Levels"
            ),
        }
        for label, mutate in cases.items():
            with self.subTest(case=label):
                self.assertEqual(refuse(mutate), {"REGISTRY_POLICY_RULE_CODE"})

    def test_the_schema_requires_the_table_condition_and_a_minimum_of_one(self) -> None:
        def refuses(mutate) -> bool:
            raw = raw_registry()
            mutate(raw["policy_rule_ids"])
            return "REGISTRY_SCHEMA" in load_rules(raw)

        for label, mutate in {
            "empty condition": lambda s: s["rules_table"].update(condition=""),
            "minimum zero": lambda s: s["rules_table"].update(minimum_rows=0),
            "no minimum": lambda s: s["rules_table"].pop("minimum_rows"),
            "no table": lambda s: s.pop("rules_table"),
            "no core table name": lambda s: s["rules_table"].pop("core_table"),
            "no level table name": lambda s: s["rules_table"].pop("level_table"),
            "a state key": lambda s: s["codes"][0].update(state="adopted"),
            "extra record field": lambda s: s["codes"][0].update(extra="x"),
            "extra section field": lambda s: s.update(extra="x"),
        }.items():
            with self.subTest(case=label):
                self.assertTrue(refuses(mutate))

    def test_the_authority_admits_the_key_and_a_base_registry_without_it(self) -> None:
        raw = raw_registry()
        AUTHORITY.validate_registry_authority(raw)
        del raw["policy_rule_ids"]
        AUTHORITY.validate_registry_authority(raw)
        self.assertIn("policy_rule_ids", AUTHORITY.OPTIONAL_TOP_LEVEL_KEYS)
        raw = {**raw_registry(), "policy_rule_id": {}}
        with self.assertRaisesRegex(AUTHORITY.AuthorityError, "REGISTRY_TOP_LEVEL"):
            AUTHORITY.validate_registry_authority(raw)

    def test_the_schema_names_the_key_and_the_current_major(self) -> None:
        schema = json.loads(SCHEMA_FILE.read_text("utf-8"))
        self.assertIn("policy_rule_ids", schema["properties"])
        version = schema["properties"]["schema_version"]["const"]
        self.assertEqual(version, raw_registry()["schema_version"])
        self.assertEqual(int(version.split(".")[0]), AUTHORITY.REGISTRY_MAJOR)


class RulesTableDefinitionTests(unittest.TestCase):
    def test_both_definitions_carry_the_core_table_and_the_level_table(self) -> None:
        raw = raw_registry()
        for profile_id in TEMPLATES:
            profile = next(p for p in raw["profiles"] if p["id"] == profile_id)
            definition = profile["template_definition"]
            tables = {t["name"]: t for t in definition["tables"]}
            core, level = tables["Rules"], tables["Rule Levels"]
            with self.subTest(profile=profile_id):
                self.assertEqual(
                    [c["key"] for c in core["columns"]], list(CORE_COLUMNS)
                )
                self.assertEqual(
                    [c["id"] for c in core["columns"]],
                    ["rule_id", "condition", "requirement", "enforcement", "evidence"],
                )
                self.assertEqual(
                    (core["table_id"], core["section"], core["required_when"]),
                    ("policy.rules", "policy.rules", "always"),
                )
                self.assertTrue(all(c["required"] for c in core["columns"]))
                self.assertEqual(
                    [c["key"] for c in level["columns"]], list(LEVEL_COLUMNS)
                )
                self.assertEqual(
                    [c["required"] for c in level["columns"]], [True, True, False]
                )
                self.assertNotIn("table_id", level)
                for table in (core, level):
                    self.assertEqual(table["row_identity"], "Rule ID")
                    self.assertEqual(table["minimum_rows"], 0)
                self.assertEqual(level["section"], "policy.rules.1")
                self.assertIn(
                    "tests/test_policy_rule_ids.py", definition["consumer_paths"]
                )

    def test_each_template_shows_both_tables_with_one_sample_row(self) -> None:
        for template in TEMPLATES.values():
            text = (ROOT / template).read_text("utf-8")
            tables = [
                (tuple(header), rows)
                for header, rows in MARKDOWN._visible_tables(text)
                if header[0] == "Rule ID"
            ]
            with self.subTest(template=template):
                self.assertEqual(
                    [header for header, _ in tables], [CORE_COLUMNS, LEVEL_COLUMNS]
                )
                self.assertEqual([len(rows) for _, rows in tables], [1, 1])
                # The prompt that made the table optional is gone.
                self.assertNotIn("helps the reader", text)
                self.assertNotIn("읽기 쉬울 때만", text)
                self.assertIn("-R<NNN>", text)
                self.assertIn("policy_rule_ids", text)

    def test_the_status_extension_is_registered_with_its_five_criteria(self) -> None:
        shared = raw_registry()["shared_contract"]
        entries = [
            item
            for item in shared["extensions"]
            if "Rules table Status" in CONTRACTS.extension_name(item)
        ]
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        for field in ("condition", "owner", "verification", "review", "removal"):
            self.assertTrue(entry[field].strip())
            self.assertNotEqual(entry[field], "unverified")
        self.assertEqual(entry["owner"], shared["owner"])
        self.assertIn("Rule Levels", entry["condition"])
        self.assertIn("POLICY-RULE-TABLE", entry["verification"])
        self.assertIn("tests/test_policy_rule_ids.py", entry["verification"])

    def test_a_table_headed_by_another_key_is_no_rule_table(self) -> None:
        f = Fixture("en")
        former = f.table("| a | b | c |", header=("Rule", "Condition", "Evidence"))
        scan = MARKDOWN.policy_rule_units(f.body(former))
        self.assertEqual((scan.rules_tables, len(scan.rows)), ((), 1))
        profile = {p.profile_id: p for p in CONTRACTS.load_registry(ROOT).profiles}[
            "governance/rule"
        ]
        names = {t.name: t for t in profile.tables}
        self.assertEqual(names["Rules"].columns[0].key, "Rule ID")
        self.assertEqual(names["Rule Levels"].columns[0].key, "Rule ID")
        self.assertEqual(MARKDOWN.RULE_LEVEL_COLUMNS, LEVEL_COLUMNS)

    def test_the_generic_table_check_leaves_both_rule_tables_to_the_rule_check(
        self,
    ) -> None:
        f = Fixture("en")
        body = f.body(f.good())
        self.assertEqual(MARKDOWN._table_diagnostics(f.path, f.profile, body), [])
        template = {p.profile_id: p for p in CONTRACTS.load_registry(ROOT).profiles}[
            "common/template-governance-rule"
        ]
        # A template has no rule check; each table is matched by its exact header.
        self.assertEqual(MARKDOWN._table_diagnostics(f.path, template, body), [])
        wrong = body.replace(
            "| Rule ID | Level | Status |", "| Rule ID | Status | Level |"
        )
        # SPEC-0222: inside the core H2 a header that is no registered table's
        # exact header drifts the core Rules table too, so both refuse it.
        self.assertEqual(
            [d.rule_id for d in MARKDOWN._table_diagnostics(f.path, template, wrong)],
            ["BODY-TABLE-COLUMNS", "BODY-TABLE-COLUMNS"],
        )


class RealPolicyTests(unittest.TestCase):
    """The fifteen real policies pass the document rules without an adoption state."""

    def test_the_reader_copes_with_every_registered_policy(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        for record in registry.policy_rule_ids.codes:
            path = PurePosixPath(record.path)
            profile = CONTRACTS.classify_path(registry, path)
            text = (ROOT / path).read_text("utf-8")
            with self.subTest(path=record.path):
                self.assertIsNotNone(profile.policy_rule_ids)
                self.assertEqual(
                    MARKDOWN._policy_rule_diagnostics(path, profile, text), []
                )

    def test_the_control_registers_are_not_rule_units(self) -> None:
        counts = [
            MARKDOWN.policy_rule_units(
                payload_markdown(
                    (ROOT / name).read_text("utf-8"), profile_id="operation/policy"
                )
            ).control_rows
            for name in (
                "docs/05.operations/02.policies/0001-k8s-gitops-operations-policy.md",
                "docs/05.operations/02.policies/0005-observability-platform-operations-policy.md",
            )
        ]
        self.assertEqual(counts, [6, 6])


class UnitReaderTests(unittest.TestCase):
    def test_the_reader_counts_each_unit_kind_once(self) -> None:
        text = Fixture.body(
            "- one\n  - nested\n- two\n\n"
            "| Item | Meaning |\n| --- | --- |\n| a | b |\n\n"
            "#### Group\n\nA paragraph.\n\n"
            "#### Control Register\n\n"
            "| Control | Role |\n| --- | --- |\n| C-1 | x |\n\n"
            "```\n- fenced\n```\n\n<!-- - commented -->\n"
        )
        scan = MARKDOWN.policy_rule_units(text)
        self.assertEqual(
            (len(scan.items), len(scan.rows), len(scan.groups), scan.control_rows),
            (2, 1, 1, 1),
        )
        self.assertEqual(len(scan.units), 4)


if __name__ == "__main__":
    unittest.main()
