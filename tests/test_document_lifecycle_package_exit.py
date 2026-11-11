"""Staged shape of a Stage 03 package leaving the tree (LIFECYCLE-PACKAGE-EXIT)."""

from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path, PurePosixPath

from tests.git_fixture import GitFixture

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location(
    "validate_document_lifecycle_package_exit_tested",
    SCRIPTS / "validate-document-lifecycle.py",
)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import boundary
    raise RuntimeError("cannot load document lifecycle validator")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)

from document_lifecycle import (  # noqa: E402
    LifecycleDocument,
    package_exit_diagnostics,
)

PKG = "docs/03.specs/0042-sample-change"
SPEC_PATH = f"{PKG}/spec.md"
PLAN_PATH = f"{PKG}/plan.md"
TASK_PATH = f"{PKG}/tasks/tsk-0001-sample-change.md"
REQ_PATH = "docs/01.requirements/0007-sample-requirement.md"
PROFILES = {
    SPEC_PATH: "sdlc/spec",
    PLAN_PATH: "sdlc/plan",
    TASK_PATH: "sdlc/task",
    REQ_PATH: "sdlc/requirement",
}
PACKAGE = (SPEC_PATH, PLAN_PATH, TASK_PATH)
LINEAGE = f"| SPEC-0042 | completed spec | Summary. | `{PKG}/` |\n"


def requirement(lineage: str = "", heading: str = "###") -> str:
    return (
        f"# Requirement\n\n## Traceability\n\n{heading} Archived Lineage\n\n"
        f"{lineage}\n## Other\n\n`{PKG}/`\n"
    )


def snapshot(
    task_status: str = "completed",
    *,
    spec_status: str = "approved",
    omit: tuple[str, ...] = (),
    texts: dict[str, str] | None = None,
) -> tuple[dict[PurePosixPath, LifecycleDocument], dict[PurePosixPath, str]]:
    statuses = {
        SPEC_PATH: spec_status,
        PLAN_PATH: spec_status,
        TASK_PATH: task_status,
        REQ_PATH: "approved",
    }
    body = {path: f"body of {path}\n" for path in statuses}
    body[REQ_PATH] = requirement()
    body.update(texts or {})
    documents = {
        PurePosixPath(path): LifecycleDocument(
            path=PurePosixPath(path), profile_id=PROFILES[path], status=status
        )
        for path, status in statuses.items()
        if path not in omit
    }
    return documents, {
        PurePosixPath(path): text for path, text in body.items() if path not in omit
    }


def closed(**kwargs: object):
    return snapshot(omit=PACKAGE, texts={REQ_PATH: requirement(LINEAGE)}, **kwargs)


class PackageExitRuleTest(unittest.TestCase):
    def rules(self, base, proposed) -> list[tuple[str, str]]:
        found = package_exit_diagnostics(
            base[0], proposed[0], base[1], proposed[1], base_mode="staged"
        )
        for item in found:
            self.assertEqual(item.rule_id, "LIFECYCLE-PACKAGE-EXIT")
            self.assertEqual(item.severity, "FAIL")
        return [(item.path.as_posix(), item.observed_transition[:2]) for item in found]

    def test_open_package_deletion_is_refused(self) -> None:
        self.assertEqual(self.rules(snapshot("in-progress"), closed()), [(PKG, "R1")])

    def test_task_less_package_is_finished_only_when_cancelled(self) -> None:
        self.assertEqual(
            self.rules(snapshot(omit=(TASK_PATH,)), closed()), [(PKG, "R1")]
        )
        self.assertEqual(
            self.rules(snapshot(spec_status="cancelled", omit=(TASK_PATH,)), closed()),
            [],
        )

    def test_cancelled_spec_with_open_task_is_not_finished(self) -> None:
        base = snapshot("in-progress", spec_status="cancelled")
        self.assertEqual(self.rules(base, closed()), [(PKG, "R1")])

    def test_one_open_task_among_several_keeps_the_package_open(self) -> None:
        second = PurePosixPath(f"{PKG}/tasks/tsk-0002-sample-change.md")
        base = snapshot()
        base[0][second] = LifecycleDocument(
            path=second, profile_id="sdlc/task", status="in-progress"
        )
        base[1][second] = "open\n"
        self.assertEqual(self.rules(base, closed()), [(PKG, "R1")])
        proposed = snapshot(texts={PLAN_PATH: "changed\n"})
        proposed[0][second] = base[0][second]
        proposed[1][second] = "open\n"
        self.assertEqual(self.rules(base, proposed), [])

    def test_partial_deletion_is_refused(self) -> None:
        proposed = snapshot(omit=(SPEC_PATH,), texts={REQ_PATH: requirement(LINEAGE)})
        self.assertEqual(self.rules(snapshot(), proposed), [(PKG, "R2")])

    def test_deletion_without_staged_lineage_is_refused(self) -> None:
        # A path mention outside Archived Lineage does not count.
        proposed = snapshot(omit=PACKAGE)
        self.assertEqual(self.rules(snapshot(), proposed), [(PKG, "R3")])
        # Lineage after a following level-3 heading is outside the section.
        proposed = snapshot(
            omit=PACKAGE,
            texts={REQ_PATH: requirement("\n### Next\n\n" + LINEAGE)},
        )
        self.assertEqual(self.rules(snapshot(), proposed), [(PKG, "R3")])
        # Lineage already present at the base is not updated in this change.
        base = snapshot(texts={REQ_PATH: requirement(LINEAGE)})
        self.assertEqual(self.rules(base, closed()), [(PKG, "R3")])

    def test_spec_or_plan_edit_after_terminal_task_is_refused(self) -> None:
        base = snapshot("cancelled")
        for path in (SPEC_PATH, PLAN_PATH):
            proposed = snapshot("cancelled", texts={path: "changed\n"})
            self.assertEqual(self.rules(base, proposed), [(path, "R4")])

    def test_admitted_shapes(self) -> None:
        cases = {
            "closure with level-3 lineage": (snapshot(), closed()),
            "closure with lineage before a following level-3 heading": (
                snapshot(),
                snapshot(
                    omit=PACKAGE,
                    texts={REQ_PATH: requirement(LINEAGE + "\n### Next\n\nx\n")},
                ),
            ),
            "closure with level-2 lineage": (
                snapshot(),
                snapshot(omit=PACKAGE, texts={REQ_PATH: requirement(LINEAGE, "##")}),
            ),
            "freeze append to a terminal Task": (
                snapshot(),
                snapshot(texts={TASK_PATH: "frozen\n"}),
            ),
            "unrelated change while a finished package stays": (
                snapshot(),
                snapshot(texts={REQ_PATH: requirement("x\n")}),
            ),
            "plan edit while the Task is open": (
                snapshot("in-progress"),
                snapshot("in-progress", texts={PLAN_PATH: "changed\n"}),
            ),
            "spec edit in a Task-less package": (
                snapshot(omit=(TASK_PATH,)),
                snapshot(omit=(TASK_PATH,), texts={SPEC_PATH: "changed\n"}),
            ),
            "cancellation with its Task": (
                snapshot("in-progress"),
                snapshot("cancelled", spec_status="cancelled"),
            ),
            "new package": (snapshot(omit=tuple(PROFILES)), snapshot()),
        }
        for name, (base, proposed) in cases.items():
            with self.subTest(name):
                self.assertEqual(self.rules(base, proposed), [])


class PackageExitStagedWiringTest(unittest.TestCase):
    """The rule runs in staged mode on a real index."""

    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="lifecycle-package-exit-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "repository"
        self.root.mkdir()
        registry_path = Path("docs/99.templates/registry.json")
        raw = json.loads((ROOT / registry_path).read_text())
        # README navigation and the language contract read files outside
        # this synthetic package; the lifecycle profiles stay complete.
        raw.pop("readme_navigation", None)
        raw.pop("document_language", None)
        target = self.root / registry_path
        target.parent.mkdir(parents=True)
        target.write_text(json.dumps(raw))
        for relative in {
            "docs/99.templates/contracts/document-profile.schema.json",
            *(
                item["template_source"]
                for item in raw["profiles"]
                if item["template_source"] is not None
            ),
        }:
            copy = self.root / relative
            copy.parent.mkdir(parents=True, exist_ok=True)
            copy.write_bytes((ROOT / relative).read_bytes())
        self.git = GitFixture(self.root)
        files = {}
        for path, profile in PROFILES.items():
            status = "completed" if profile == "sdlc/task" else "approved"
            files[path] = (
                f'---\ntype: "{profile}"\nstatus: "{status}"\n---\n\n'
                + (requirement() if path == REQ_PATH else "# Body\n")
            ).encode()
        self.git.run("add", "--", "docs/99.templates")
        self.git.commit_many(files)

    def staged(self) -> tuple[int, str]:
        output = io.StringIO()
        with redirect_stdout(output), redirect_stderr(output):
            result = VALIDATOR.main(["--root", str(self.root), "--mode", "staged"])
        return result, output.getvalue()

    def test_staged_mode_refuses_lineageless_closure(self) -> None:
        self.git.run("rm", "--quiet", "-r", "--", PKG)
        result, output = self.staged()
        self.assertEqual(result, 1, output)
        self.assertIn("LIFECYCLE-PACKAGE-EXIT", output)
        self.assertIn("R3", output)

    def test_staged_mode_admits_closure_with_lineage(self) -> None:
        self.git.run("rm", "--quiet", "-r", "--", PKG)
        path = self.root / REQ_PATH
        path.write_text(path.read_text().replace("## Other", LINEAGE + "\n## Other"))
        self.git.run("add", "--", REQ_PATH)
        result, output = self.staged()
        self.assertNotIn("LIFECYCLE-PACKAGE-EXIT", output)
        self.assertEqual(result, 0, output)


if __name__ == "__main__":
    unittest.main()
