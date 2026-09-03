#!/usr/bin/env python3
"""Focused contract tests for package-local delegated execution ownership."""

from __future__ import annotations

import dataclasses
import importlib.util
import sys
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate-links-and-owners.py"
SCRIPTS = str(SCRIPT.parent)
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

SPEC = importlib.util.spec_from_file_location("delegated_execution_validator", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("link validator is unavailable")
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


PARENT = PurePosixPath("docs/03.specs/0054-parent/spec.md")
CHILD = PurePosixPath("docs/03.specs/0066-child/spec.md")
PLAN = PurePosixPath("docs/03.specs/0066-child/plan.md")
TASK = PurePosixPath("docs/03.specs/0066-child/tasks/tsk-0001-vto-000.md")
ROUTER = PurePosixPath("docs/03.specs/0066-child/README.md")
ADR = PurePosixPath("docs/02.architecture/decisions/0031-delegation.md")


def _link(label: str, target: str) -> str:
    return f"[{label}]({target})"


def _context():
    profiles = {
        PARENT: validator.ProfileView("sdlc/spec", "sdlc", "authored"),
        CHILD: validator.ProfileView("sdlc/spec", "sdlc", "authored"),
        PLAN: validator.ProfileView("sdlc/plan", "sdlc", "authored"),
        TASK: validator.ProfileView("sdlc/task", "sdlc", "authored"),
        ROUTER: validator.ProfileView(
            "readme/collection-index", "navigation", "projection"
        ),
        ADR: validator.ProfileView("sdlc/architecture-decision", "sdlc", "authored"),
    }
    texts = {
        PARENT: "\n".join(
            (
                _link("child", "../0066-child/spec.md"),
                _link("decision", "../../02.architecture/decisions/0031-delegation.md"),
            )
        ),
        CHILD: "\n".join(
            (
                _link("parent", "../0054-parent/spec.md"),
                _link("decision", "../../02.architecture/decisions/0031-delegation.md"),
                _link("plan", "plan.md"),
                _link("task", "tasks/tsk-0001-vto-000.md"),
            )
        ),
        PLAN: "\n".join(
            (
                _link("spec", "spec.md"),
                _link("task", "tasks/tsk-0001-vto-000.md"),
            )
        ),
        TASK: "\n".join(
            (
                _link("spec", "../spec.md"),
                _link("plan", "../plan.md"),
            )
        ),
        ROUTER: _link("task", "tasks/tsk-0001-vto-000.md"),
        ADR: "\n".join(
            (
                _link("parent", "../../03.specs/0054-parent/spec.md"),
                _link("child", "../../03.specs/0066-child/spec.md"),
            )
        ),
    }
    metadata = {
        PARENT: {"status": "active", "artifact_id": "SPEC-0054"},
        CHILD: {"status": "active", "artifact_id": "SPEC-0066"},
        PLAN: {"status": "active", "artifact_id": "SPEC-0066-PLAN-0001"},
        TASK: {"status": "in-progress", "artifact_id": "SPEC-0066-TSK-0001"},
        ROUTER: {},
        ADR: {"status": "accepted", "artifact_id": "ADR-0031"},
    }
    paths = tuple(sorted(profiles, key=lambda path: path.as_posix()))
    return validator.Context(
        root=ROOT,
        paths=paths,
        baseline_paths=frozenset(paths),
        profiles=profiles,
        texts=texts,
        metadata=metadata,
        adapter_targets={},
        governance_current_paths=(),
        governance_current_states=(),
        tracked_regular_paths=frozenset(paths),
    )


def _evaluate(
    context,
    *,
    registry_owned: frozenset[str] = frozenset({"0054"}),
    standalone: frozenset[str] = frozenset({"0054"}),
):
    graph = validator._current_execution_link_graph(context)
    index = validator._current_execution_index(graph)
    return validator._delegated_execution_diagnostics(
        context,
        registry_owned,
        standalone,
        graph,
        index,
    )


class DelegatedExecutionOwnershipTests(unittest.TestCase):
    def test_accepts_one_closed_package_local_component(self) -> None:
        diagnostics, owned = _evaluate(_context())

        self.assertEqual(diagnostics, [])
        self.assertEqual(owned, {PLAN, TASK})

    def test_rejects_missing_parent_reciprocity(self) -> None:
        context = _context()
        context.texts[PARENT] = _link(
            "decision", "../../02.architecture/decisions/0031-delegation.md"
        )

        diagnostics, _ = _evaluate(context)

        self.assertIn(
            "DELEGATED-EXECUTION-PARENT",
            {diagnostic.rule_id for diagnostic in diagnostics},
        )

    def test_rejects_proposed_authority(self) -> None:
        context = _context()
        context.metadata[ADR] = {"status": "proposed", "artifact_id": "ADR-0031"}

        diagnostics, _ = _evaluate(context)

        self.assertIn(
            "DELEGATED-EXECUTION-AUTHORITY",
            {diagnostic.rule_id for diagnostic in diagnostics},
        )

    def test_accepts_multiple_reciprocal_accepted_authorities(self) -> None:
        context = _context()
        second = PurePosixPath("docs/02.architecture/decisions/0030-context.md")
        context = dataclasses.replace(
            context,
            paths=tuple(
                sorted((*context.paths, second), key=lambda path: path.as_posix())
            ),
            profiles={
                **context.profiles,
                second: validator.ProfileView(
                    "sdlc/architecture-decision", "sdlc", "authored"
                ),
            },
            texts={
                **context.texts,
                PARENT: context.texts[PARENT]
                + "\n"
                + _link("context", "../../02.architecture/decisions/0030-context.md"),
                CHILD: context.texts[CHILD]
                + "\n"
                + _link("context", "../../02.architecture/decisions/0030-context.md"),
                second: "\n".join(
                    (
                        _link("parent", "../../03.specs/0054-parent/spec.md"),
                        _link("child", "../../03.specs/0066-child/spec.md"),
                    )
                ),
            },
            metadata={
                **context.metadata,
                second: {"status": "accepted", "artifact_id": "ADR-0030"},
            },
            tracked_regular_paths=context.tracked_regular_paths | {second},
        )

        diagnostics, _ = _evaluate(context)

        self.assertNotIn(
            "DELEGATED-EXECUTION-AUTHORITY",
            {diagnostic.rule_id for diagnostic in diagnostics},
        )

    def test_rejects_multiple_candidate_parents(self) -> None:
        context = _context()
        second = PurePosixPath("docs/03.specs/0065-second-parent/spec.md")
        context = dataclasses.replace(
            context,
            paths=tuple(
                sorted((*context.paths, second), key=lambda path: path.as_posix())
            ),
            profiles={
                **context.profiles,
                second: validator.ProfileView("sdlc/spec", "sdlc", "authored"),
            },
            texts={
                **context.texts,
                CHILD: context.texts[CHILD]
                + "\n"
                + _link("second", "../0065-second-parent/spec.md"),
                ADR: context.texts[ADR]
                + "\n"
                + _link("second", "../../03.specs/0065-second-parent/spec.md"),
                second: "\n".join(
                    (
                        _link("child", "../0066-child/spec.md"),
                        _link(
                            "decision",
                            "../../02.architecture/decisions/0031-delegation.md",
                        ),
                    )
                ),
            },
            metadata={
                **context.metadata,
                second: {"status": "active", "artifact_id": "SPEC-0065"},
            },
            tracked_regular_paths=context.tracked_regular_paths | {second},
        )

        diagnostics, _ = _evaluate(
            context,
            registry_owned=frozenset({"0054", "0065"}),
            standalone=frozenset({"0054", "0065"}),
        )

        self.assertIn(
            "DELEGATED-EXECUTION-PARENT",
            {diagnostic.rule_id for diagnostic in diagnostics},
        )

    def test_rejects_foreign_execution_link(self) -> None:
        context = _context()
        foreign = PurePosixPath("docs/03.specs/0054-parent/plan.md")
        context = dataclasses.replace(
            context,
            paths=tuple(
                sorted((*context.paths, foreign), key=lambda path: path.as_posix())
            ),
            profiles={
                **context.profiles,
                foreign: validator.ProfileView("sdlc/plan", "sdlc", "authored"),
            },
            texts={
                **context.texts,
                PLAN: context.texts[PLAN]
                + "\n"
                + _link("foreign", "../0054-parent/plan.md"),
                foreign: "",
            },
            metadata={
                **context.metadata,
                foreign: {"status": "done", "artifact_id": "SPEC-0054-PLAN-0001"},
            },
            tracked_regular_paths=context.tracked_regular_paths | {foreign},
        )

        diagnostics, _ = _evaluate(context)

        self.assertIn(
            "DELEGATED-EXECUTION-PACKAGE",
            {diagnostic.rule_id for diagnostic in diagnostics},
        )

    def test_rejects_state_mismatch(self) -> None:
        context = _context()
        context.metadata[TASK] = {
            "status": "queued",
            "artifact_id": "SPEC-0066-TSK-0001",
        }

        diagnostics, _ = _evaluate(context)

        self.assertIn(
            "DELEGATED-EXECUTION-STATE",
            {diagnostic.rule_id for diagnostic in diagnostics},
        )

    def test_rejects_duplicate_child_standalone_authority(self) -> None:
        diagnostics, _ = _evaluate(
            _context(),
            registry_owned=frozenset({"0054", "0066"}),
            standalone=frozenset({"0054", "0066"}),
        )

        self.assertIn(
            "DELEGATED-EXECUTION-DUPLICATE-AUTHORITY",
            {diagnostic.rule_id for diagnostic in diagnostics},
        )


if __name__ == "__main__":
    unittest.main()
