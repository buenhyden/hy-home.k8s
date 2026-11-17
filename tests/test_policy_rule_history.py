"""Policy rule ID and code history across Git snapshots (SPEC-0206)."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

from tests.git_fixture import GitFixture

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location(
    "validate_document_lifecycle_policy_history_tested",
    SCRIPTS / "validate-document-lifecycle.py",
)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import boundary
    raise RuntimeError("cannot load document lifecycle validator")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)

from document_contracts import load_registry  # noqa: E402

REGISTRY = "docs/99.templates/registry.json"
GIT_POLICY = ".agents/governance/git.md"
SDLC_POLICY = ".agents/governance/sdlc.md"
MOVED_POLICY = ".agents/governance/git-moved.md"
HISTORY_RULES = {"POLICY-RULE-DELETE", "POLICY-RULE-REISSUE", "POLICY-CODE-CHANGE"}


def policy(rows: list[tuple[int, str]] | None, *, code: str = "GIT") -> str:
    """One policy body whose Requirements section holds the given rule rows."""

    head = "# Policy\n\n## Rules\n\n### Requirements\n\n"
    if rows is None:
        return head + "No table.\n"
    # SPEC-0222: the core Rules table holds the active rules; the Rule Levels
    # table keyed by Rule ID holds every issued ID with its status.
    core = [
        "| Rule ID | Condition | Requirement | Enforcement | Evidence |",
        "| --- | --- | --- | --- | --- |",
    ]
    core += [
        f"| {code}-R{number:03d} | Always | Keep it. | `check` | none |"
        for number, status in rows
        if status == "active"
    ]
    levels = ["| Rule ID | Level | Status |", "| --- | --- | --- |"]
    levels += [
        f"| {code}-R{number:03d} | required | {status} |" for number, status in rows
    ]
    return head + "\n".join(core) + "\n\n" + "\n".join(levels) + "\n"


def registry_blob(codes: dict[str, str] | None, reserved: tuple[str, ...] = ()) -> str:
    """The registry blob; `None` is a registry from before SPEC-0194."""

    # MAJOR 1 is not readable by the history reader, so the typed reading falls
    # back to the current registry and only the plain section read is exercised.
    blob: dict[str, object] = {"schema_version": "1.0.0"}
    if codes is not None:
        blob["policy_rule_ids"] = {
            "reserved_codes": list(reserved),
            "codes": [{"path": path, "code": code} for path, code in codes.items()],
        }
    return json.dumps(blob, indent=2) + "\n"


class PolicyHistoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry(ROOT)

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.git = GitFixture(self.root)

    def snapshot(self, files: dict[str, str]) -> str:
        """Commit exactly `files` as the whole tree and return its commit."""

        for tracked in self.git.run("ls-files", "-z").decode().split("\0"):
            if tracked and tracked not in files:
                self.git.run("rm", "--quiet", "--", tracked)
        for relative, text in files.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        self.git.run("--literal-pathspecs", "add", "--", *files)
        self.git.run("commit", "--quiet", "--allow-empty", "-m", "fixture")
        return self.git.run("rev-parse", "HEAD").decode().strip()

    def history(self, base: str, proposed: str) -> set[str]:
        found = VALIDATOR._evaluate_comparison(
            self.root,
            self.registry,
            mode="explicit-ref",
            from_ref=base,
            to_ref=proposed,
        )
        return {item.rule_id for item in found if item.rule_id in HISTORY_RULES}

    def pair(
        self,
        before: list[tuple[int, str]] | None,
        after: list[tuple[int, str]] | None,
    ) -> set[str]:
        """Compare the git policy at two snapshots under one registry."""

        registry = registry_blob({GIT_POLICY: "GIT"})
        base = self.snapshot({REGISTRY: registry, GIT_POLICY: policy(before)})
        proposed = self.snapshot({REGISTRY: registry, GIT_POLICY: policy(after)})
        return self.history(base, proposed)

    def two_policies(self) -> dict[str, str]:
        return {
            REGISTRY: registry_blob({GIT_POLICY: "GIT", SDLC_POLICY: "SDLC"}),
            GIT_POLICY: policy([(1, "active")]),
            SDLC_POLICY: policy([(1, "active")], code="SDLC"),
        }

    # WORK-001: rule ID permanence and no reissue.

    def test_last_row_deleted_is_refused(self) -> None:
        both = [(1, "active"), (2, "active")]
        self.assertEqual(self.pair(both, both[:1]), {"POLICY-RULE-DELETE"})

    def test_last_row_deleted_then_reissued_is_refused_at_the_deletion(self) -> None:
        # The proposal alone cannot tell an edited R002 from a reissued one, so
        # the commit that removes the ID is the step that is refused.
        both = [(1, "active"), (2, "active")]
        registry = registry_blob({GIT_POLICY: "GIT"})
        first = self.snapshot({REGISTRY: registry, GIT_POLICY: policy(both)})
        second = self.snapshot({REGISTRY: registry, GIT_POLICY: policy(both[:1])})
        third = self.snapshot({REGISTRY: registry, GIT_POLICY: policy(both)})
        self.assertEqual(self.history(first, second), {"POLICY-RULE-DELETE"})
        self.assertEqual(self.history(second, third), set())

    def test_missing_table_loses_every_base_id(self) -> None:
        self.assertEqual(self.pair([(1, "active")], None), {"POLICY-RULE-DELETE"})

    def test_retired_row_made_active_is_refused(self) -> None:
        self.assertEqual(
            self.pair(
                [(1, "active"), (2, "retired; none")],
                [(1, "active"), (2, "active")],
            ),
            {"POLICY-RULE-REISSUE"},
        )

    def test_retirement_append_and_successor_correction_pass(self) -> None:
        self.assertEqual(
            self.pair(
                [(1, "active"), (2, "active")],
                [(1, "retired; none"), (2, "active"), (3, "active")],
            ),
            set(),
        )
        self.assertEqual(
            self.pair(
                [(1, "active"), (2, "retired; none")],
                [(1, "active"), (2, "retired; GIT-R003"), (3, "active")],
            ),
            set(),
        )

    def test_rule_moved_to_another_policy_keeps_its_old_row(self) -> None:
        base = self.snapshot(self.two_policies())
        proposed = self.snapshot(
            {
                **self.two_policies(),
                GIT_POLICY: policy([(1, "retired; SDLC-R002")]),
                SDLC_POLICY: policy([(1, "active"), (2, "active")], code="SDLC"),
            }
        )
        self.assertEqual(self.history(base, proposed), set())

    def test_renamed_policy_passes(self) -> None:
        rows = [(1, "active"), (2, "active")]
        base = self.snapshot(
            {REGISTRY: registry_blob({GIT_POLICY: "GIT"}), GIT_POLICY: policy(rows)}
        )
        proposed = self.snapshot(
            {
                REGISTRY: registry_blob({MOVED_POLICY: "GIT"}),
                MOVED_POLICY: policy(rows),
            }
        )
        self.assertEqual(self.history(base, proposed), set())

    # WORK-002: code permanence, the reserved list and a departing policy.

    def test_changed_code_is_refused(self) -> None:
        rows = [(1, "active")]
        base = self.snapshot(
            {REGISTRY: registry_blob({GIT_POLICY: "GIT"}), GIT_POLICY: policy(rows)}
        )
        proposed = self.snapshot(
            {
                REGISTRY: registry_blob({GIT_POLICY: "GITX"}),
                GIT_POLICY: policy(rows, code="GITX"),
            }
        )
        self.assertEqual(
            self.history(base, proposed),
            {"POLICY-CODE-CHANGE", "POLICY-RULE-DELETE"},
        )

    def test_code_given_to_another_policy_is_refused(self) -> None:
        base = self.snapshot(self.two_policies())
        proposed = self.snapshot(
            {
                REGISTRY: registry_blob({GIT_POLICY: "SDLC", SDLC_POLICY: "GIT"}),
                GIT_POLICY: policy([(1, "active")], code="SDLC"),
                SDLC_POLICY: policy([(1, "active")]),
            }
        )
        self.assertIn("POLICY-CODE-CHANGE", self.history(base, proposed))

    def test_removed_reserved_code_is_refused(self) -> None:
        base = self.snapshot(
            {
                REGISTRY: registry_blob({GIT_POLICY: "GIT"}, ("OLD",)),
                GIT_POLICY: policy([(1, "active")]),
            }
        )
        proposed = self.snapshot(
            {
                REGISTRY: registry_blob({GIT_POLICY: "GIT"}),
                GIT_POLICY: policy([(1, "active")]),
            }
        )
        self.assertEqual(self.history(base, proposed), {"POLICY-CODE-CHANGE"})

    def test_departing_policy_passes_only_with_its_code_reserved(self) -> None:
        kept = {SDLC_POLICY: policy([(1, "active")], code="SDLC")}
        base = self.snapshot(self.two_policies())
        reserved = self.snapshot(
            {REGISTRY: registry_blob({SDLC_POLICY: "SDLC"}, ("GIT",)), **kept}
        )
        self.assertEqual(self.history(base, reserved), set())
        base = self.snapshot(self.two_policies())
        unreserved = self.snapshot(
            {REGISTRY: registry_blob({SDLC_POLICY: "SDLC"}), **kept}
        )
        self.assertEqual(
            self.history(base, unreserved),
            {"POLICY-CODE-CHANGE", "POLICY-RULE-DELETE"},
        )

    def test_reserved_code_that_a_record_still_carries_excuses_no_loss(self) -> None:
        base = self.snapshot(
            {
                REGISTRY: registry_blob({GIT_POLICY: "GIT"}),
                GIT_POLICY: policy([(1, "active"), (2, "active")]),
            }
        )
        proposed = self.snapshot(
            {
                REGISTRY: registry_blob({GIT_POLICY: "GIT"}, ("GIT",)),
                GIT_POLICY: policy([(1, "active")]),
            }
        )
        self.assertIn("POLICY-RULE-DELETE", self.history(base, proposed))

    def test_base_without_the_section_or_without_a_table_yields_no_rule(self) -> None:
        none = self.snapshot({REGISTRY: registry_blob(None), GIT_POLICY: policy(None)})
        adopted = self.snapshot(
            {
                REGISTRY: registry_blob({GIT_POLICY: "GIT"}),
                GIT_POLICY: policy([(1, "active")]),
            }
        )
        self.assertEqual(self.history(none, adopted), set())
        before_table = self.snapshot(
            {REGISTRY: registry_blob({GIT_POLICY: "GIT"}), GIT_POLICY: policy(None)}
        )
        self.assertEqual(self.history(before_table, adopted), set())

    def test_new_policy_issues_from_r001(self) -> None:
        base = self.snapshot(
            {REGISTRY: registry_blob({}), SDLC_POLICY: policy(None, code="SDLC")}
        )
        proposed = self.snapshot(
            {
                REGISTRY: registry_blob({GIT_POLICY: "GIT"}),
                SDLC_POLICY: policy(None, code="SDLC"),
                GIT_POLICY: policy([(1, "active")]),
            }
        )
        self.assertEqual(self.history(base, proposed), set())

    def test_staged_mode_judges_the_index_against_head(self) -> None:
        self.snapshot(
            {
                REGISTRY: registry_blob({GIT_POLICY: "GIT"}),
                GIT_POLICY: policy([(1, "active"), (2, "active")]),
            }
        )
        (self.root / GIT_POLICY).write_text(policy([(1, "active")]), encoding="utf-8")
        self.git.run("--literal-pathspecs", "add", "--", GIT_POLICY)
        found = VALIDATOR._evaluate_comparison(self.root, self.registry, mode="staged")
        self.assertIn("POLICY-RULE-DELETE", {item.rule_id for item in found})


if __name__ == "__main__":
    unittest.main()
