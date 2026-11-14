"""SPEC-0194: the policy rule ID contract, its registry section and document rules."""

from __future__ import annotations

import dataclasses
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import document_authority as AUTHORITY  # noqa: E402
import document_contracts as CONTRACTS  # noqa: E402

REGISTRY_FILE = ROOT / "docs/99.templates/registry.json"
SCHEMA_FILE = ROOT / "docs/99.templates/contracts/document-profile.schema.json"
TEMPLATES = {
    "common/template-governance-rule": "docs/99.templates/templates/governance/rule.template.md",
    "common/template-operation-policy": "docs/99.templates/templates/operations/policy.template.md",
}
COLUMNS = ("Rule ID", "Condition", "Level", "Evidence", "Status")
CODES = {
    ".agents/governance/agent-execution.md": "EXEC",
    ".agents/governance/approval-and-safety.md": "SAFE",
    ".agents/governance/context-and-memory.md": "CTX",
    ".agents/governance/document-authoring.md": "AUTHOR",
    ".agents/governance/document-lifecycle.md": "DOCLIFE",
    ".agents/governance/formatting-and-linting.md": "FMT",
    ".agents/governance/git.md": "GIT",
    ".agents/governance/model-selection.md": "MODEL",
    ".agents/governance/quality.md": "QUAL",
    ".agents/governance/sdlc.md": "SDLC",
    "docs/05.operations/policies/0001-k8s-gitops-operations-policy.md": "GITOPS",
    "docs/05.operations/policies/0003-service-mesh-cert-manager-policy.md": "MESH",
    "docs/05.operations/policies/0004-rollouts-notifications-headlamp-policy.md": "ROLLOUT",
    "docs/05.operations/policies/0005-observability-platform-operations-policy.md": "OBSERV",
    "docs/05.operations/policies/0007-app-gitops-onboarding-policy.md": "ONBOARD",
}
LEVELS = ["required", "recommended", "optional"]
SYNTHETIC = PurePosixPath(".agents/governance/synthetic.md")
KOREAN = PurePosixPath("docs/05.operations/policies/9999-synthetic.md")


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


def policy_profile(profile_id: str, path: PurePosixPath, state: str | None, code="SYN"):
    """The loaded profile with one synthetic record, or none when state is None."""

    profile = {p.profile_id: p for p in CONTRACTS.load_registry(ROOT).profiles}[
        profile_id
    ]
    ids = profile.policy_rule_ids
    codes = (
        ()
        if state is None
        else (CONTRACTS.PolicyRuleCode(path.as_posix(), code, state),)
    )
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
    """One synthetic policy for a language; runs the document rules over a body."""

    def __init__(self, language: str, state: str | None = "adopted", code="SYN"):
        self.text = LANGUAGES[language]
        self.path = self.text["path"]
        self.profile = policy_profile(self.text["profile"], self.path, state, code)

    def item(self, number: int, text: str, token: bool = True) -> str:
        lead = f"`SYN-R{number:03d}` " if token else ""
        return f"- {lead}{text}"

    def row(self, number, level="required", status="active", code="SYN") -> str:
        identifier = f"{code}-R{number:03d}" if isinstance(number, int) else number
        return (
            f"| {identifier} | {self.text['when']} | {level} | "
            f"{self.text['proof']} | {status} |"
        )

    @staticmethod
    def table(*rows: str, header=COLUMNS) -> str:
        head = "| " + " | ".join(header) + " |"
        rule = "| " + " | ".join("---" for _ in header) + " |"
        return "\n".join([head, rule, *rows])

    def good(self) -> str:
        return (
            f"{self.item(1, self.text['one'])}\n{self.item(2, self.text['two'])}\n\n"
            + self.table(self.row(1), self.row(2))
        )

    @staticmethod
    def body(requirements: str) -> str:
        return (
            "# Policy\n\n## Rules\n\n### Requirements\n\n"
            + requirements.strip("\n")
            + "\n\n### Enforcement\n\nChecks run in CI.\n"
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
    def each(self, check, state: str | None = "adopted") -> None:
        for language in LANGUAGES:
            with self.subTest(language=language):
                check(Fixture(language, state))


class RuleCodeTests(EachLanguage):
    def test_an_adopted_policy_with_rules_and_a_record_passes(self) -> None:
        self.each(lambda f: self.assertEqual(f.rules(f.good()), []))

    def test_a_policy_with_normative_rules_and_no_record_fails(self) -> None:
        self.each(
            lambda f: self.assertEqual(
                f.rules(f.item(1, f.text["one"], token=False)), ["POLICY-RULE-CODE"]
            ),
            state=None,
        )

    def test_a_policy_with_a_table_and_no_record_fails(self) -> None:
        self.each(
            lambda f: self.assertEqual(
                f.rules(f.table(f.row(1))), ["POLICY-RULE-CODE"]
            ),
            state=None,
        )

    def test_a_policy_that_states_no_rule_needs_no_record(self) -> None:
        self.each(lambda f: self.assertEqual(f.rules(f.text["prose"]), []), state=None)

    def test_a_policy_without_a_requirements_section_is_not_read(self) -> None:
        body = "# Policy\n\n## Rules\n\n### Enforcement\n\nChecks run in CI.\n"
        self.each(lambda f: self.assertEqual(f.found(body), []), state=None)

    def test_a_profile_without_the_section_is_not_read(self) -> None:
        f = Fixture("en")
        f.profile = dataclasses.replace(f.profile, policy_rule_ids=None)
        self.assertEqual(f.rules(f.item(1, "x", token=False)), [])


class RuleTableTests(EachLanguage):
    def test_a_prose_only_policy_passes_without_a_table(self) -> None:
        self.each(lambda f: self.assertEqual(f.rules(f.text["prose"]), []))

    def test_a_header_only_table_passes_when_no_rule_is_stated(self) -> None:
        self.each(lambda f: self.assertEqual(f.rules(f.table()), []))

    def test_a_missing_table_fails_when_rules_are_stated(self) -> None:
        def check(f: Fixture) -> None:
            self.assertEqual(
                f.rules(f.item(1, f.text["one"], token=False)),
                ["POLICY-RULE-COVERAGE", "POLICY-RULE-TABLE"],
            )
            # A token has no active row without a table.
            self.assertEqual(
                f.rules(f.item(1, f.text["one"])),
                ["POLICY-RULE-INLINE", "POLICY-RULE-TABLE"],
            )

        self.each(check)

    def test_a_table_without_rows_fails_when_rules_are_stated(self) -> None:
        self.each(
            lambda f: self.assertEqual(
                f.rules(f.item(1, f.text["one"]) + "\n\n" + f.table()),
                ["POLICY-RULE-INLINE", "POLICY-RULE-TABLE"],
            )
        )

    def test_a_table_without_the_status_column_fails(self) -> None:
        def check(f: Fixture) -> None:
            table = f.table(
                "| SYN-R001 | when | required | proof |", header=COLUMNS[:4]
            )
            self.assertEqual(
                f.rules(f.item(1, f.text["one"]) + "\n\n" + table),
                ["POLICY-RULE-TABLE"],
            )

        self.each(check)

    def test_a_reordered_or_extra_column_fails(self) -> None:
        def check(f: Fixture) -> None:
            for header in (
                (COLUMNS[0], COLUMNS[2], COLUMNS[1], *COLUMNS[3:]),
                (*COLUMNS, "Note"),
            ):
                row = "| " + " | ".join("x" for _ in header) + " |"
                table = f.table(row, header=header)
                with self.subTest(header=header):
                    self.assertIn(
                        "POLICY-RULE-TABLE",
                        f.rules(f.item(1, "x", token=False) + "\n\n" + table),
                    )

        self.each(check)

    def test_a_level_is_one_of_the_three_registered_values(self) -> None:
        def run(f: Fixture, level: str) -> list[str]:
            table = f.table(f.row(1, level=level))
            return f.rules(f.item(1, f.text["one"]) + "\n\n" + table)

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
                "POLICY-RULE-TABLE", f.rules(f.good() + "\n\n" + f.table(f.row(1)))
            )
            outside = f.body(f.good()).replace(
                "Checks run in CI.", "Checks run in CI.\n\n" + f.table(f.row(1))
            )
            self.assertIn("POLICY-RULE-TABLE", f.found(outside))

        self.each(check)

    def test_the_status_is_active_or_retired_with_a_successor(self) -> None:
        def run(f: Fixture, status: str) -> list[str]:
            table = f.table(f.row(1), f.row(2, status=status))
            return f.rules(f.item(1, f.text["one"]) + "\n\n" + table)

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


class RuleIdTests(EachLanguage):
    def run_rows(self, f: Fixture, *rows: str) -> list[str]:
        numbers = sorted(
            {int(n) for row in rows for n in re.findall(r"R(\d{3})\b", row)}
        )
        items = "\n".join(f.item(n, f.text["one"]) for n in numbers)
        return f.rules(items + "\n\n" + f.table(*rows))

    def test_ascending_rows_from_r001_without_a_gap_pass(self) -> None:
        self.each(
            lambda f: self.assertEqual(
                self.run_rows(f, f.row(1), f.row(2), f.row(3)), []
            )
        )

    def test_a_gap_a_duplicate_a_late_start_or_a_descent_fails(self) -> None:
        def check(f: Fixture) -> None:
            for label, rows in (
                ("gap", (f.row(1), f.row(3))),
                ("duplicate", (f.row(1), f.row(1))),
                ("late start", (f.row(2), f.row(3))),
                ("descent", (f.row(2), f.row(1))),
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
                table = f.table(f.row(identifier))
                with self.subTest(identifier=identifier):
                    self.assertIn(
                        "POLICY-RULE-ID",
                        f.rules(f.item(1, f.text["one"]) + "\n\n" + table),
                    )

        self.each(check)

    def test_a_control_cell_is_never_read_as_a_rule_id(self) -> None:
        self.each(
            lambda f: self.assertEqual(f.rules(f.good() + "\n\n" + f.control()), [])
        )


class DefinitionTokenTests(EachLanguage):
    def test_every_active_row_has_exactly_one_token_and_the_reverse(self) -> None:
        def check(f: Fixture) -> None:
            table = f.table(f.row(1))
            none = f.item(1, f.text["one"], token=False)
            self.assertEqual(
                f.rules(none + "\n\n" + table),
                ["POLICY-RULE-COVERAGE", "POLICY-RULE-INLINE"],
            )
            stray = f.item(1, f.text["one"]) + "\n" + f.item(2, f.text["two"])
            self.assertEqual(f.rules(stray + "\n\n" + table), ["POLICY-RULE-INLINE"])
            twice = f.item(1, f.text["one"]) + "\n" + f.item(1, f.text["two"])
            self.assertEqual(f.rules(twice + "\n\n" + table), ["POLICY-RULE-INLINE"])

        self.each(check)

    def test_a_retired_row_has_no_token_and_a_token_on_it_fails(self) -> None:
        def check(f: Fixture) -> None:
            table = f.table(f.row(1), f.row(2, status="retired; none"))
            one = f.item(1, f.text["one"])
            self.assertEqual(f.rules(one + "\n\n" + table), [])
            both = one + "\n" + f.item(2, f.text["two"])
            self.assertEqual(f.rules(both + "\n\n" + table), ["POLICY-RULE-INLINE"])

        self.each(check)

    def test_a_reference_outside_a_definition_position_is_not_counted(self) -> None:
        def check(f: Fixture) -> None:
            reference = f"- {f.text['one']} `SYN-R001`"
            self.assertEqual(
                f.rules(reference + "\n\n" + f.table(f.row(1))),
                ["POLICY-RULE-COVERAGE", "POLICY-RULE-INLINE"],
            )
            prose = f.good() + "\n\nSee `SYN-R001` and `SYN-R002`."
            self.assertEqual(f.rules(prose), [])
            heading = f.good() + "\n\n#### Detail `SYN-R003`\n\nText."
            self.assertEqual(f.rules(heading), [])

        self.each(check)

    def test_a_token_in_a_fence_or_a_comment_is_not_read(self) -> None:
        def check(f: Fixture) -> None:
            table = f.table(f.row(1))
            for hidden in (
                "```\n- `SYN-R001` fenced\n```",
                "<!-- - `SYN-R001` commented -->",
                "<!--\n- `SYN-R001` commented\n-->",
            ):
                requirements = (
                    f.item(1, f.text["one"], token=False)
                    + "\n\n"
                    + hidden
                    + "\n\n"
                    + table
                )
                with self.subTest(hidden=hidden):
                    self.assertEqual(
                        f.rules(requirements),
                        ["POLICY-RULE-COVERAGE", "POLICY-RULE-INLINE"],
                    )

        self.each(check)

    def test_a_table_row_and_an_h4_paragraph_are_definition_positions(self) -> None:
        def check(f: Fixture) -> None:
            rows = (
                "| Item | Meaning |\n| --- | --- |\n"
                f"| `SYN-R001` {f.text['one']} | {f.text['when']} |"
            )
            group = f"#### Group\n\n`SYN-R002`\n\n{f.text['two']}\n\n- {f.text['one']}"
            table = f.table(f.row(1), f.row(2))
            self.assertEqual(f.rules(rows + "\n\n" + group + "\n\n" + table), [])

        self.each(check)


class CoverageFloorTests(EachLanguage):
    def test_an_item_or_row_without_a_token_fails(self) -> None:
        def check(f: Fixture) -> None:
            table = f.table(f.row(1))
            items = f.item(1, f.text["one"]) + "\n" + f.item(2, "x", token=False)
            self.assertEqual(f.rules(items + "\n\n" + table), ["POLICY-RULE-COVERAGE"])
            row = f"| Item | Meaning |\n| --- | --- |\n| plain | {f.text['when']} |"
            self.assertEqual(
                f.rules(f.item(1, f.text["one"]) + "\n\n" + row + "\n\n" + table),
                ["POLICY-RULE-COVERAGE"],
            )

        self.each(check)

    def test_an_h4_group_token_covers_the_items_in_the_group(self) -> None:
        def check(f: Fixture) -> None:
            table = f.table(f.row(1))
            group = f"#### Group\n\n`SYN-R001`\n\n- {f.text['one']}\n- {f.text['two']}"
            self.assertEqual(f.rules(group + "\n\n" + table), [])
            late = f"#### Group\n\n{f.text['prose']}\n\n`SYN-R001`\n\n- {f.text['one']}"
            self.assertIn("POLICY-RULE-COVERAGE", f.rules(late + "\n\n" + table))
            after = group + f"\n\n#### Other\n\n- {f.text['two']}"
            self.assertIn("POLICY-RULE-COVERAGE", f.rules(after + "\n\n" + table))

        self.each(check)

    def test_a_nested_item_is_not_read_by_the_floor_but_may_carry_a_token(self) -> None:
        def check(f: Fixture) -> None:
            nested = f"{f.item(1, f.text['one'])}\n  - {f.text['two']}"
            self.assertEqual(f.rules(nested + "\n\n" + f.table(f.row(1))), [])
            tokened = f"{f.item(1, f.text['one'])}\n  - `SYN-R002` {f.text['two']}"
            table = f.table(f.row(1), f.row(2))
            self.assertEqual(f.rules(tokened + "\n\n" + table), [])

        self.each(check)

    def test_control_register_and_rules_table_rows_are_exempt(self) -> None:
        def check(f: Fixture) -> None:
            self.assertEqual(f.rules(f.control()), [])
            self.assertEqual(f.rules(f.good() + "\n\n" + f.control()), [])

        self.each(check)

    def test_a_paragraph_outside_every_unit_is_not_read(self) -> None:
        self.each(
            lambda f: self.assertEqual(f.rules(f.good() + "\n\n" + f.text["prose"]), [])
        )


class AdoptionGateTests(EachLanguage):
    def test_a_pending_policy_with_neither_table_nor_token_passes(self) -> None:
        def check(f: Fixture) -> None:
            plain = f.item(1, f.text["one"], token=False)
            self.assertEqual(f.rules(plain + "\n" + f.text["prose"]), [])
            self.assertEqual(f.rules(f.text["prose"]), [])

        self.each(check, state="pending")

    def test_a_pending_policy_with_a_table_or_a_token_fails(self) -> None:
        def check(f: Fixture) -> None:
            plain = f.item(1, f.text["one"], token=False)
            gate = ["POLICY-RULE-ADOPTION"]
            self.assertEqual(f.rules(plain + "\n\n" + f.table(f.row(1))), gate)
            self.assertEqual(f.rules(f.table()), gate)
            self.assertEqual(f.rules(f.item(1, f.text["one"])), gate)
            self.assertEqual(
                f.rules(f"#### Group\n\n`SYN-R001`\n\n{f.text['one']}"), gate
            )

        self.each(check, state="pending")

    def test_a_pending_policy_applies_no_other_rule(self) -> None:
        row = "| Item | Meaning |\n| --- | --- |\n| plain | x |"
        self.each(lambda f: self.assertEqual(f.rules(row), []), state="pending")


class RegistryRecordTests(unittest.TestCase):
    def test_the_repository_registry_carries_the_section(self) -> None:
        raw = raw_registry()
        section = raw["policy_rule_ids"]
        self.assertEqual(section["code_pattern"], "^[A-Z][A-Z0-9]{1,7}$")
        self.assertEqual(section["levels"], LEVELS)
        self.assertEqual(section["reserved_codes"], ["PLAT", "OBS"])
        self.assertEqual(
            section["rules_table"],
            {"condition": "the policy states normative rules", "minimum_rows": 1},
        )
        self.assertEqual({i["path"]: i["code"] for i in section["codes"]}, CODES)
        self.assertEqual(len({i["code"] for i in section["codes"]}), 15)
        for item in section["codes"]:
            self.assertEqual(set(item), {"path", "code", "state"})
            self.assertIn(item["state"], {"pending", "adopted"})
            self.assertRegex(item["code"], section["code_pattern"])
            self.assertNotIn(item["code"], section["reserved_codes"])
        self.assertEqual(record_rules(raw), set())
        self.assertEqual(load_rules(raw), set())

    def test_the_loader_copies_the_section_to_the_authored_policy_profiles(
        self,
    ) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        ids = registry.policy_rule_ids
        self.assertEqual({r.path: r.code for r in ids.codes}, CODES)
        self.assertEqual(ids.levels, tuple(LEVELS))
        self.assertEqual(ids.rules_table_minimum_rows, 1)
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
                path="docs/05.operations/policies/README.md"
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
            "unknown state": lambda s: s["codes"][0].update(state="draft"),
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
        self.assertEqual(
            schema["properties"]["schema_version"]["const"],
            f"{AUTHORITY.REGISTRY_MAJOR}.0.0",
        )


class RulesTableDefinitionTests(unittest.TestCase):
    def test_both_definitions_carry_four_required_columns_and_the_optional_status(
        self,
    ) -> None:
        raw = raw_registry()
        for profile_id in TEMPLATES:
            profile = next(p for p in raw["profiles"] if p["id"] == profile_id)
            definition = profile["template_definition"]
            table = next(t for t in definition["tables"] if t["name"] == "Rules")
            with self.subTest(profile=profile_id):
                self.assertEqual([c["key"] for c in table["columns"]], list(COLUMNS))
                self.assertEqual(
                    [c["required"] for c in table["columns"]],
                    [True, True, True, True, False],
                )
                self.assertEqual(table["row_identity"], "Rule ID")
                self.assertEqual(table["minimum_rows"], 0)
                self.assertEqual(table["section"], "policy-rules-requirements")
                self.assertIn(
                    "tests/test_policy_rule_ids.py", definition["consumer_paths"]
                )

    def test_each_template_shows_the_table_with_one_sample_row(self) -> None:
        for template in TEMPLATES.values():
            text = (ROOT / template).read_text("utf-8")
            tables = [
                (header, rows)
                for header, rows in MARKDOWN._visible_tables(text)
                if header[0] == "Rule ID"
            ]
            with self.subTest(template=template):
                self.assertEqual(len(tables), 1)
                header, rows = tables[0]
                self.assertEqual(tuple(header), COLUMNS)
                self.assertEqual(len(rows), 1)
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
        self.assertIn("POLICY-RULE-TABLE", entry["verification"])
        self.assertIn("tests/test_policy_rule_ids.py", entry["verification"])

    def test_a_table_headed_by_the_former_key_is_no_longer_the_rules_table(
        self,
    ) -> None:
        f = Fixture("en", "adopted")
        former = f.table("| a | b | c |", header=("Rule", "Condition", "Evidence"))
        scan = MARKDOWN.policy_rule_units(f.body(former))
        self.assertEqual((scan.rules_tables, len(scan.rows)), ((), 1))
        profile = {p.profile_id: p for p in CONTRACTS.load_registry(ROOT).profiles}[
            "governance/rule"
        ]
        rules = next(t for t in profile.tables if t.name == "Rules")
        self.assertEqual(rules.columns[0].key, "Rule ID")


class RealPolicyTests(unittest.TestCase):
    """The fifteen real policies draw no rule while their records are pending."""

    def test_the_reader_copes_with_every_registered_policy(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        for record in registry.policy_rule_ids.codes:
            path = PurePosixPath(record.path)
            profile = CONTRACTS.classify_path(registry, path)
            text = (ROOT / path).read_text("utf-8")
            with self.subTest(path=record.path):
                self.assertIsNotNone(profile.policy_rule_ids)
                if record.state == "pending":
                    self.assertEqual(
                        MARKDOWN._policy_rule_diagnostics(path, profile, text), []
                    )
                    self.assertEqual(MARKDOWN.policy_rule_units(text).tokens, ())

    def test_the_control_registers_are_not_rule_units(self) -> None:
        counts = [
            MARKDOWN.policy_rule_units((ROOT / name).read_text("utf-8")).control_rows
            for name in (
                "docs/05.operations/policies/0001-k8s-gitops-operations-policy.md",
                "docs/05.operations/policies/0005-observability-platform-operations-policy.md",
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
