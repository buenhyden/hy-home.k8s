from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "scripts/migrate-document-work-units.py"


def load_tool():
    spec = importlib.util.spec_from_file_location("wdtc_migration", TOOL)
    if spec is None or spec.loader is None:
        raise AssertionError("migration tool unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class MigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool()

    def fixture_repo(self, root: Path):
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
        source = root / "docs/04.execution/plans/2026-08-07-example.md"
        spec = root / "docs/03.specs/052-example/spec.md"
        source.parent.mkdir(parents=True)
        spec.parent.mkdir(parents=True)
        source.write_text("source\n", encoding="utf-8")
        spec.write_text("spec\n", encoding="utf-8")
        subprocess.run(["git", "add", "docs"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
        commit = self.git(root, "rev-parse", "HEAD")
        blob = self.git(root, "rev-parse", "HEAD:docs/04.execution/plans/2026-08-07-example.md")
        return commit, blob

    @staticmethod
    def git(root: Path, *args: str) -> str:
        return subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=True).stdout.strip()

    def entry(self, blob: str, **changes):
        row = {"source": "docs/04.execution/plans/2026-08-07-example.md", "target": "docs/03.specs/052-example/plan.md", "workUnit": "Spec-052", "disposition": "move-current", "sourceBlob": blob, "reviewed": True}
        row.update(changes)
        return row

    def data(self, commit: str, entries):
        return {"state": "transition", "sourceCommit": commit, "entries": entries}

    def test_task_requires_spec_and_plan(self):
        self.assertEqual(self.tool.validate_work_unit_paths({"052": {"tasks.md", "spec.md"}}), ("WORK-UNIT-MISSING-PLAN:052",))

    def test_plan_requires_spec(self):
        self.assertEqual(self.tool.validate_work_unit_paths({"052": {"plan.md"}}), ("WORK-UNIT-MISSING-SPEC:052",))

    def test_transition_accepts_complete_siblings(self):
        self.assertEqual(self.tool.validate_work_unit_paths({"052": {"spec.md", "plan.md", "tasks.md"}}), ())

    def test_terminal_rejects_stage04(self):
        self.assertEqual(self.tool.validate_route_paths(("docs/04.execution/plans/a.md",), "terminal"), ("ROUTE-TERMINAL-STAGE04",))

    def test_manifest_totals_are_closed(self):
        with self.assertRaises(self.tool.MigrationAbort):
            self.tool.validate_counts(move_count=81, archive_count=50, source_count=131)

    def test_production_manifest_is_exact(self):
        manifest = self.tool.load_manifest(ROOT / "scripts/document-taxonomy-migration.json")
        plan = self.tool.validate_manifest_data(ROOT, manifest, True)
        self.assertEqual((plan.source_count, plan.move_count, plan.archive_count), (132, 82, 50))
        first = manifest["entries"][0]
        self.assertEqual({k: first[k] for k in ("source", "target", "workUnit", "disposition", "reviewed")}, {"source": "docs/04.execution/plans/2026-08-07-document-taxonomy-consolidation.md", "target": "docs/03.specs/052-document-taxonomy-consolidation/plan.md", "workUnit": "Spec-052", "disposition": "move-current", "reviewed": True})

    def test_named_unsafe_states_abort(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, blob = self.fixture_repo(root)
            cases = [
                self.data(commit, [self.entry(blob, source="docs/04.execution/plans/missing.md")]),
                self.data(commit, [self.entry("0" * 40)]),
                self.data(commit, [self.entry(blob), self.entry(blob)]),
                self.data(commit, [self.entry(blob), self.entry(blob, source="docs/04.execution/tasks/missing.md")]),
                self.data(commit, [self.entry(blob, disposition="unknown")]),
                self.data(commit, [self.entry(blob, reviewed=False)]),
                self.data(commit, [self.entry(blob, extra="forbidden")]),
            ]
            for case in cases:
                with self.subTest(case=case):
                    with self.assertRaises(self.tool.MigrationAbort):
                        self.tool.validate_manifest_data(root, case, False)

    def test_existing_target_and_archive_envelope_abort(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, blob = self.fixture_repo(root)
            target = root / "docs/03.specs/052-example/plan.md"
            target.write_text("duplicate\n", encoding="utf-8")
            with self.assertRaises(self.tool.MigrationAbort):
                self.tool.validate_manifest_data(root, self.data(commit, [self.entry(blob)]), False)
            target.unlink()
            envelope = root / "docs/98.archive/04.execution/plans/existing.md"
            envelope.parent.mkdir(parents=True)
            envelope.write_text("envelope\n", encoding="utf-8")
            row = self.entry(blob, target="docs/98.archive/04.execution/plans/existing.md/child.md", disposition="archive-unique", workUnit="Archive-example")
            with self.assertRaises(self.tool.MigrationAbort):
                self.tool.validate_manifest_data(root, self.data(commit, [row]), False)

    def test_missing_or_nonhex_provenance_aborts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, blob = self.fixture_repo(root)
            for value in (None, "not-hex"):
                data = self.data(commit, [self.entry(blob)])
                if value is None:
                    del data["sourceCommit"]
                else:
                    data["sourceCommit"] = value
                with self.assertRaises(self.tool.MigrationAbort):
                    self.tool.validate_manifest_data(root, data, False)

    def test_cli_check_reports_counts(self):
        result = subprocess.run([sys.executable, str(TOOL), "--root", str(ROOT), "--manifest", "scripts/document-taxonomy-migration.json", "--check"], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("moves=82 archives=50 sources=132", result.stdout)

    def test_detect_secrets_admits_only_canonical_manifest_identity_lines(self):
        config = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
        hook = next(hook for repository in config["repos"] for hook in repository["hooks"] if hook["id"] == "detect-secrets")
        pattern = hook["args"][hook["args"].index("--exclude-lines") + 1]
        compiled = re.compile(pattern)
        self.assertIsNotNone(compiled.fullmatch('  "sourceCommit": "' + "a" * 40 + '",'))
        self.assertIsNotNone(compiled.fullmatch('      "sourceBlob": "' + "b" * 40 + '",'))
        self.assertIsNone(compiled.fullmatch(' "sourceCommit": "' + "a" * 40 + '",'))
        self.assertIsNone(compiled.fullmatch('      "otherBlob": "' + "b" * 40 + '",'))
        baseline = json.loads((ROOT / ".secrets.baseline").read_text(encoding="utf-8"))
        baseline_pattern = next(item["pattern"][0] for item in baseline["filters_used"] if item["path"] == "detect_secrets.filters.regex.should_exclude_line")
        self.assertEqual(baseline_pattern, pattern)


if __name__ == "__main__":
    unittest.main()
