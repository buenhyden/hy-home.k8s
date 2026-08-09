from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
from collections import OrderedDict
from pathlib import Path
from types import MappingProxyType
from unittest import mock

import yaml
from scripts.archive_recovery import recover_git_blob, render_fixture_archive_envelope


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
        self.assertEqual(
            self.tool.validate_work_unit_paths({"052": {"plan.md"}}),
            (
                "WORK-UNIT-MISSING-SPEC:052",
                "WORK-UNIT-MISSING-TASK:052",
            ),
        )

    def test_plan_and_spec_require_task(self):
        self.assertEqual(
            self.tool.validate_work_unit_paths({"052": {"plan.md", "spec.md"}}),
            ("WORK-UNIT-MISSING-TASK:052",),
        )

    def test_transition_accepts_complete_siblings(self):
        self.assertEqual(self.tool.validate_work_unit_paths({"052": {"spec.md", "plan.md", "tasks.md"}}), ())

    def test_terminal_rejects_stage04(self):
        self.assertEqual(self.tool.validate_route_paths(("docs/04.execution/plans/a.md",), "terminal"), ("ROUTE-TERMINAL-STAGE04",))

    def test_manifest_totals_are_closed(self):
        with self.assertRaises(self.tool.MigrationAbort):
            self.tool.validate_counts(move_count=81, archive_count=50, source_count=131)

    def test_production_manifest_is_exact(self):
        raw = json.loads((ROOT / "scripts/document-taxonomy-migration.json").read_text(encoding="utf-8"))
        manifest = self.tool.load_manifest(ROOT / "scripts/document-taxonomy-migration.json")
        plan = self.tool.validate_manifest_data(ROOT, raw, True)
        self.assertEqual((plan.source_count, plan.move_count, plan.archive_count), (132, 82, 50))
        self.assertIsInstance(manifest, tuple)
        self.assertIsInstance(manifest[0], MappingProxyType)
        first = manifest[0]
        self.assertEqual({k: first[k] for k in ("source", "target", "workUnit", "disposition", "reviewed")}, {"source": "docs/04.execution/plans/2026-08-07-document-taxonomy-consolidation.md", "target": "docs/03.specs/052-document-taxonomy-consolidation/plan.md", "workUnit": "Spec-052", "disposition": "move-current", "reviewed": True})
        move_units = {
            row["workUnit"] for row in manifest if row["disposition"] == "move-current"
        }
        self.assertEqual(len(move_units), 41)

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

    def phase_fixture(self, root: Path):
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
        (root / ".gitleaks.toml").write_text("[allowlist]\n", encoding="utf-8")
        paths = [
            "docs/04.execution/plans/2026-01-01-zeta.md",
            "docs/04.execution/tasks/2026-01-01-alpha.md",
            "docs/04.execution/plans/2026-01-01-current.md",
            "docs/04.execution/tasks/2026-01-01-current.md",
        ]
        for path in paths:
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(path + "\n", encoding="utf-8")
        spec = root / "docs/03.specs/052-current/spec.md"
        spec.parent.mkdir(parents=True)
        spec.write_text("spec\n", encoding="utf-8")
        subprocess.run(["git", "add", "docs", ".gitleaks.toml"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
        commit = self.git(root, "rev-parse", "HEAD")
        rows = []
        for path in paths[:2]:
            rows.append({"source": path, "target": path.replace("docs/04.execution", "docs/98.archive/04.execution"), "workUnit": "Archive-unique-fixture", "disposition": "archive-unique", "sourceBlob": self.git(root, "rev-parse", f"HEAD:{path}"), "reviewed": True})
        for path, name in zip(paths[2:], ("plan.md", "tasks.md"), strict=True):
            rows.append({"source": path, "target": f"docs/03.specs/052-current/{name}", "workUnit": "Spec-052", "disposition": "move-current", "sourceBlob": self.git(root, "rev-parse", f"HEAD:{path}"), "reviewed": True})
        return commit, tuple(MappingProxyType(row) for row in rows)

    def write_manifest(self, root: Path, commit: str, entries) -> None:
        target = root / "scripts/document-taxonomy-migration.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(
                {
                    "state": "transition",
                    "sourceCommit": commit,
                    "entries": [dict(row) for row in entries],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "scripts/document-taxonomy-migration.json"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "manifest fixture"], cwd=root, check=True)

    def test_validate_manifest_returns_sorted_diagnostics_without_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, entries = self.phase_fixture(root)
            changed = root / entries[0]["source"]
            changed.write_text("changed\n", encoding="utf-8")
            before = changed.read_bytes()
            diagnostics = self.tool.validate_manifest(root, entries, commit)
            self.assertEqual(diagnostics, tuple(sorted(diagnostics)))
            self.assertIn("MIGRATION-CHANGED-SOURCE:" + entries[0]["source"], diagnostics)
            self.assertEqual(changed.read_bytes(), before)

    def test_plan_phase_is_ordered_and_enforces_prerequisites(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, entries = self.phase_fixture(root)
            archive = self.tool.plan_phase(root, entries, "archive")
            self.assertEqual(archive, tuple(sorted(archive)))
            with self.assertRaisesRegex(self.tool.MigrationAbort, "PHASE-PREREQUISITE"):
                self.tool.plan_phase(root, entries, "move")

    def _complete_fixture_archives(self, root: Path, commit: str, entries):
        for row in entries:
            if row["disposition"] != "archive-unique":
                continue
            recovered = recover_git_blob(root, row["source"], commit)
            metadata = {
                "title": "Fixture archive",
                "type": "content/archive",
                "status": "archived",
                "owner": "test",
                "updated": "2026-08-09",
                "original_type": "sdlc/plan",
                "original_path": row["source"],
                "archived_on": "2026-08-09",
                "archive_reason": "retired",
                "replacement": None,
                "source_commit": commit,
                "source_blob": row["sourceBlob"],
                "content_sha256": recovered.content_sha256,
            }
            target = root / row["target"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(
                render_fixture_archive_envelope(
                    metadata, recovered, recovered.source_bytes
                )
            )
            (root / row["source"]).unlink()
        subprocess.run(["git", "add", "docs"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "archive fixture"], cwd=root, check=True)

    def test_move_phase_accepts_exact_archive_envelopes_and_rejects_corruption(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, entries = self.phase_fixture(root)
            self._complete_fixture_archives(root, commit, entries)
            self.assertEqual(self.tool.validate_manifest(root, entries, commit), ())
            planned = self.tool.plan_phase(root, entries, "move")
            self.assertEqual(len(planned), 2)
            archive_target = root / entries[0]["target"]
            archive_target.write_bytes(archive_target.read_bytes() + b"corrupt")
            subprocess.run(["git", "add", "docs"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "corrupt fixture"], cwd=root, check=True)
            with self.assertRaisesRegex(self.tool.MigrationAbort, "ARCHIVE-ENVELOPE"):
                self.tool.plan_phase(root, entries, "move")

    def test_apply_phase_preflights_every_pair_before_first_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, entries = self.phase_fixture(root)
            self.write_manifest(root, commit, entries)
            valid = (Path(entries[0]["source"]), Path(entries[0]["target"]))
            invalid = (Path("docs/04.execution/plans/missing.md"), Path("docs/98.archive/04.execution/plans/missing.md"))
            with (
                mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                self.assertRaises(self.tool.MigrationAbort),
            ):
                self.tool.apply_phase(root, (valid, invalid), "archive")
            self.assertTrue((root / valid[0]).is_file())
            self.assertFalse((root / valid[1]).exists())

    def test_archive_apply_builds_valid_envelopes_then_move_plans(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, entries = self.phase_fixture(root)
            self.write_manifest(root, commit, entries)
            archive_pairs = self.tool.plan_phase(root, entries, "archive")
            with (
                mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                mock.patch.object(self.tool, "validate_counts"),
                mock.patch.object(self.tool, "_classify_secret_payload"),
            ):
                self.tool.apply_phase(root, archive_pairs, "archive")
            self.assertEqual(self.tool.validate_manifest(root, entries, commit), ())
            subprocess.run(["git", "add", "docs"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "archive apply"], cwd=root, check=True)
            self.assertEqual(len(self.tool.plan_phase(root, entries, "move")), 2)
            self.assertFalse((root / "docs/98.archive/README.md").exists())

    def test_archive_apply_rejects_secret_classifier_outcomes_without_payload(self):
        payload = b"sensitive-payload-must-not-appear"
        cases = (
            (None, None, "MIGRATION-SECRET-CLASSIFIER-UNAVAILABLE"),
            (Path("/usr/bin/gitleaks"), 17, "MIGRATION-SECRET-DETECTED"),
            (Path("/usr/bin/gitleaks"), 2, "MIGRATION-SECRET-CLASSIFIER-ERROR"),
        )
        for executable, result, expected in cases:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as tmp:
                config_path = Path(tmp) / "gitleaks.toml"
                config_path.write_text("[allowlist]\n", encoding="utf-8")
                config_path.chmod(0o600)
                descriptor = self.tool.os.open(config_path, self.tool.os.O_RDONLY)
                metadata = self.tool.os.fstat(descriptor)
                config = self.tool._ConfigHandle(
                    descriptor,
                    metadata.st_dev,
                    metadata.st_ino,
                    metadata.st_mode,
                )
                try:
                    with (
                        mock.patch.object(
                            self.tool, "_gitleaks_executable", return_value=executable
                        ),
                        mock.patch.object(
                            self.tool, "_run_gitleaks", return_value=result
                        ),
                        self.assertRaisesRegex(
                            self.tool.MigrationAbort, expected
                        ) as raised,
                    ):
                        self.tool._classify_secret_payload(
                            Path.cwd(), "archive.md", payload, config
                        )
                    self.assertNotIn(payload.decode(), str(raised.exception))
                finally:
                    self.tool.os.close(descriptor)
        with (
            tempfile.TemporaryFile() as config,
            mock.patch.object(
                self.tool.subprocess,
                "run",
                side_effect=subprocess.TimeoutExpired("gitleaks", 20),
            ),
            self.assertRaisesRegex(
                self.tool.MigrationAbort, "MIGRATION-SECRET-CLASSIFIER-ERROR"
            ),
        ):
            self.tool._run_gitleaks(
                Path("/usr/bin/gitleaks"), config.fileno(), payload
            )

    def test_gitleaks_discovery_admits_safe_path_and_rejects_workspace_or_tmp(self):
        safe = Path("/home/test/.local/bin/gitleaks")
        with (
            mock.patch.object(self.tool.shutil, "which", return_value=str(safe)),
            mock.patch.object(
                self.tool,
                "_gitleaks_candidate_is_safe",
                side_effect=lambda candidate, _root: candidate == safe,
            ),
        ):
            self.assertEqual(self.tool._gitleaks_executable(ROOT), safe)
        self.assertFalse(
            self.tool._gitleaks_candidate_is_safe(ROOT / "gitleaks", ROOT)
        )
        self.assertFalse(
            self.tool._gitleaks_candidate_is_safe(Path("/tmp/gitleaks"), ROOT)
        )

    def test_work_unit_number_must_match_target_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, entries = self.phase_fixture(root)
            changed = [dict(row) for row in entries]
            move_index = next(
                index
                for index, row in enumerate(changed)
                if row["disposition"] == "move-current"
            )
            changed[move_index]["target"] = changed[move_index]["target"].replace(
                "052-current", "053-current"
            )
            diagnostics = self.tool.validate_manifest(
                root,
                tuple(MappingProxyType(row) for row in changed),
                commit,
            )
            self.assertTrue(
                any(item.startswith("MIGRATION-WORK-UNIT:") for item in diagnostics)
            )

    def test_archive_apply_invalid_metadata_and_late_write_roll_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, entries = self.phase_fixture(root)
            self.write_manifest(root, commit, entries)
            pairs = self.tool.plan_phase(root, entries, "archive")
            original = {source: (root / source).read_bytes() for source, _ in pairs}
            invalid = OrderedDict(
                (
                    ("title", "invalid"),
                    ("type", "content/archive"),
                )
            )
            with (
                mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                mock.patch.object(self.tool, "validate_counts"),
                mock.patch.object(self.tool, "_classify_secret_payload"),
                mock.patch.object(self.tool, "_archive_metadata", return_value=invalid),
                self.assertRaisesRegex(self.tool.MigrationAbort, "ARCHIVE-METADATA"),
            ):
                self.tool.apply_phase(root, pairs, "archive")
            for source, target in pairs:
                self.assertEqual((root / source).read_bytes(), original[source])
                self.assertFalse((root / target).exists())

    def test_apply_rejects_dirty_or_alternate_control_surfaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, entries = self.phase_fixture(root)
            self.write_manifest(root, commit, entries)
            pairs = self.tool.plan_phase(root, entries, "archive")
            manifest = root / "scripts/document-taxonomy-migration.json"
            manifest.write_text(manifest.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            with (
                mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                self.assertRaisesRegex(self.tool.MigrationAbort, "CONTROL-DIRTY"),
            ):
                self.tool.apply_phase(root, pairs, "archive")
            subprocess.run(["git", "restore", ".gitleaks.toml"], cwd=root, check=True)
            data = json.loads(manifest.read_text(encoding="utf-8"))
            data["sourceCommit"] = self.git(root, "rev-parse", "HEAD")
            manifest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            subprocess.run(["git", "add", str(manifest.relative_to(root))], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "alternate commit"], cwd=root, check=True)
            with (
                mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                self.assertRaisesRegex(self.tool.MigrationAbort, "SOURCE-COMMIT"),
            ):
                self.tool.apply_phase(root, pairs, "archive")
            subprocess.run(["git", "restore", "scripts/document-taxonomy-migration.json"], cwd=root, check=True)
            (root / ".gitleaks.toml").write_text("[allowlist]\npaths = []\n", encoding="utf-8")
            with (
                mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                self.assertRaisesRegex(self.tool.MigrationAbort, "CONTROL-DIRTY"),
            ):
                self.tool.apply_phase(root, pairs, "archive")

    def test_archive_apply_cleans_temp_on_staging_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, entries = self.phase_fixture(root)
            self.write_manifest(root, commit, entries)
            pairs = self.tool.plan_phase(root, entries, "archive")
            real_fsync = self.tool.os.fsync
            fsync_calls = 0

            def fail_first_staged_output(descriptor):
                nonlocal fsync_calls
                fsync_calls += 1
                if fsync_calls == 2:
                    raise OSError("fsync")
                return real_fsync(descriptor)

            with (
                mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                mock.patch.object(self.tool, "validate_counts"),
                mock.patch.object(self.tool, "_classify_secret_payload"),
                mock.patch.object(
                    self.tool.os, "fsync", side_effect=fail_first_staged_output
                ),
                self.assertRaisesRegex(self.tool.MigrationAbort, "MIGRATION-FILESYSTEM"),
            ):
                self.tool.apply_phase(root, pairs, "archive")
            self.assertEqual(tuple(root.rglob(".migration-*")), ())
            for source, target in pairs:
                self.assertTrue((root / source).is_file())
                self.assertFalse((root / target).exists())

    def test_duplicate_source_frontmatter_and_build_slugs_fail_closed(self):
        duplicate = b"---\ntitle: one\ntitle: two\n---\n# Body\n"
        with self.assertRaisesRegex(self.tool.MigrationAbort, "ARCHIVE-METADATA"):
            self.tool._source_frontmatter(duplicate)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.phase_fixture(root)
            duplicate_path = root / "docs/04.execution/plans/2026-02-02-current.md"
            duplicate_path.write_text("duplicate slug\n", encoding="utf-8")
            subprocess.run(["git", "add", "docs"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "duplicate slug"], cwd=root, check=True)
            duplicate_commit = self.git(root, "rev-parse", "HEAD")
            with (
                mock.patch.object(
                    self.tool, "EXPECTED_SOURCE_COMMIT", duplicate_commit
                ),
                self.assertRaisesRegex(self.tool.MigrationAbort, "DUPLICATE-SLUG"),
            ):
                self.tool.build_manifest(root)

    def test_archive_apply_late_write_failure_rolls_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, entries = self.phase_fixture(root)
            self.write_manifest(root, commit, entries)
            pairs = self.tool.plan_phase(root, entries, "archive")
            original = {source: (root / source).read_bytes() for source, _ in pairs}
            real_link = self.tool.os.link
            installs = 0

            def fail_second_install(source, target, **kwargs):
                nonlocal installs
                if str(source).startswith("stage-") and str(target).endswith(".md"):
                    installs += 1
                    if installs == 2:
                        raise OSError("injected late failure")
                return real_link(source, target, **kwargs)

            with (
                mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                mock.patch.object(self.tool, "validate_counts"),
                mock.patch.object(self.tool, "_classify_secret_payload"),
                mock.patch.object(self.tool.os, "link", side_effect=fail_second_install),
                self.assertRaisesRegex(self.tool.MigrationAbort, "MIGRATION-FILESYSTEM"),
            ):
                self.tool.apply_phase(root, pairs, "archive")
            for source, target in pairs:
                self.assertEqual((root / source).read_bytes(), original[source])
                self.assertFalse((root / target).exists())

    def test_move_apply_uses_pinned_blob_instead_of_worktree_read_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, entries = self.phase_fixture(root)
            self.write_manifest(root, commit, entries)
            self._complete_fixture_archives(root, commit, entries)
            pairs = self.tool.plan_phase(root, entries, "move")
            move_source = root / pairs[0][0]
            pinned = recover_git_blob(root, pairs[0][0].as_posix(), commit).source_bytes
            real_read_bytes = Path.read_bytes

            def substitute_worktree_read(path):
                if path == move_source:
                    return b"attacker bytes that still leave the source hash unchanged"
                return real_read_bytes(path)

            with (
                mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                mock.patch.object(self.tool, "validate_counts"),
                mock.patch.object(Path, "read_bytes", substitute_worktree_read),
            ):
                self.tool.apply_phase(root, pairs, "move")
            self.assertEqual((root / pairs[0][1]).read_bytes(), pinned)

    def test_apply_lock_contention_fails_without_residue(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, entries = self.phase_fixture(root)
            self.write_manifest(root, commit, entries)
            pairs = self.tool.plan_phase(root, entries, "archive")
            lock_path = self.tool._repository_lock_path(root)
            with self.tool._repository_lock(root):
                with (
                    mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                    self.assertRaisesRegex(self.tool.MigrationAbort, "LOCK-CONTENDED"),
                ):
                    self.tool.apply_phase(root, pairs, "archive")
            self.assertFalse(lock_path.exists())
            self.assertEqual(tuple(root.rglob(".migration-*")), ())

    def test_late_target_creation_is_not_clobbered(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, entries = self.phase_fixture(root)
            self.write_manifest(root, commit, entries)
            pairs = self.tool.plan_phase(root, entries, "archive")
            first_target = root / pairs[0][1]
            concurrent = b"concurrent target must survive"
            real_link = self.tool.os.link
            injected = False

            def create_target_then_link(source, target, **kwargs):
                nonlocal injected
                if not injected and str(target).endswith(".md"):
                    injected = True
                    first_target.write_bytes(concurrent)
                return real_link(source, target, **kwargs)

            with (
                mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                mock.patch.object(self.tool, "validate_counts"),
                mock.patch.object(self.tool, "_run_gitleaks", return_value=0),
                mock.patch.object(self.tool.os, "link", side_effect=create_target_then_link),
                self.assertRaisesRegex(
                    self.tool.MigrationAbort,
                    "MIGRATION-(?:FILESYSTEM|ROLLBACK)",
                ),
            ):
                self.tool.apply_phase(root, pairs, "archive")
            self.assertEqual(first_target.read_bytes(), concurrent)
            self.assertEqual(tuple(root.rglob(".migration-*")), ())

    def test_rollback_preserves_replaced_third_party_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, entries = self.phase_fixture(root)
            self.write_manifest(root, commit, entries)
            pairs = self.tool.plan_phase(root, entries, "archive")
            first_target = root / pairs[0][1]
            replacement = b"third-party replacement must survive rollback"
            real_link = self.tool.os.link
            installs = 0

            def replace_first_before_second_failure(source, target, **kwargs):
                nonlocal installs
                if str(target).endswith(".md"):
                    installs += 1
                    if installs == 2:
                        replacement_path = first_target.with_suffix(".third-party")
                        replacement_path.write_bytes(replacement)
                        self.tool.os.replace(replacement_path, first_target)
                        raise OSError("late target install failure")
                return real_link(source, target, **kwargs)

            with (
                mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                mock.patch.object(self.tool, "validate_counts"),
                mock.patch.object(self.tool, "_run_gitleaks", return_value=0),
                mock.patch.object(
                    self.tool.os,
                    "link",
                    side_effect=replace_first_before_second_failure,
                ),
                self.assertRaisesRegex(self.tool.MigrationAbort, "MIGRATION-ROLLBACK"),
            ):
                self.tool.apply_phase(root, pairs, "archive")
            self.assertEqual(first_target.read_bytes(), replacement)
            self.assertEqual(tuple(root.rglob(".migration-*")), ())

    def test_control_surfaces_reject_hidden_index_flags(self):
        for flag, clear in (
            ("--assume-unchanged", "--no-assume-unchanged"),
            ("--skip-worktree", "--no-skip-worktree"),
        ):
            with self.subTest(flag=flag), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                commit, entries = self.phase_fixture(root)
                self.write_manifest(root, commit, entries)
                pairs = self.tool.plan_phase(root, entries, "archive")
                manifest = "scripts/document-taxonomy-migration.json"
                subprocess.run(
                    ["git", "update-index", flag, manifest], cwd=root, check=True
                )
                (root / manifest).write_text(
                    (root / manifest).read_text(encoding="utf-8") + "\n",
                    encoding="utf-8",
                )
                with (
                    mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                    self.assertRaisesRegex(
                        self.tool.MigrationAbort, "CONTROL-INDEX-FLAGS"
                    ),
                ):
                    self.tool.apply_phase(root, pairs, "archive")
                subprocess.run(
                    ["git", "update-index", clear, manifest], cwd=root, check=True
                )

    def test_control_surface_snapshots_drive_parser_and_classifier(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, entries = self.phase_fixture(root)
            self.write_manifest(root, commit, entries)
            pairs = self.tool.plan_phase(root, entries, "archive")
            original_capture = self.tool._capture_control_surface
            original_config = (root / ".gitleaks.toml").read_bytes()
            configs_seen = []

            def replace_after_capture(capture_root, relative):
                snapshot = original_capture(capture_root, relative)
                if relative == self.tool.MANIFEST_PATH:
                    (capture_root / relative).write_bytes(b"{}\n")
                elif relative == self.tool.GITLEAKS_CONFIG_PATH:
                    (capture_root / relative).write_bytes(
                        b"[allowlist]\nregexes = ['.*']\n"
                    )
                return snapshot

            def inspect_temp_config(_executable, config_path, _payload):
                configs_seen.append(
                    Path(f"/proc/self/fd/{config_path}").read_bytes()
                )
                return 0

            with (
                mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                mock.patch.object(self.tool, "validate_counts"),
                mock.patch.object(
                    self.tool,
                    "_capture_control_surface",
                    side_effect=replace_after_capture,
                ),
                mock.patch.object(
                    self.tool, "_gitleaks_executable", return_value=Path("/usr/bin/gitleaks")
                ),
                mock.patch.object(
                    self.tool, "_run_gitleaks", side_effect=inspect_temp_config
                ),
            ):
                self.tool.apply_phase(root, pairs, "archive")
            self.assertEqual(configs_seen, [original_config, original_config])
            self.assertEqual(tuple(root.glob(".migration-gitleaks-*")), ())
            self.assertEqual(tuple(root.rglob(".migration-*")), ())

    def test_gitleaks_uses_exact_open_config_descriptor(self):
        completed = mock.Mock(returncode=0)
        with tempfile.TemporaryFile() as config, mock.patch.object(
            self.tool.subprocess, "run", return_value=completed
        ) as run:
            config_fd = config.fileno()
            self.assertEqual(
                self.tool._run_gitleaks(
                    Path("/usr/bin/gitleaks"), config_fd, b"payload"
                ),
                0,
            )
        arguments, keywords = run.call_args
        command = arguments[0]
        self.assertIn(f"/proc/self/fd/{config_fd}", command)
        self.assertEqual(keywords["pass_fds"], (config_fd,))
        self.assertIs(keywords["stdout"], subprocess.DEVNULL)
        self.assertIs(keywords["stderr"], subprocess.DEVNULL)

    def test_lock_cleanup_failure_preserves_body_diagnostic(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.phase_fixture(root)
            with mock.patch.object(
                self.tool,
                "_cleanup_repository_lock",
                side_effect=self.tool.MigrationAbort("MIGRATION-LOCK-CLEANUP"),
            ):
                try:
                    with self.tool._repository_lock(root):
                        raise self.tool.MigrationAbort("MIGRATION-BODY-FAILURE")
                except self.tool.MigrationAbort as raised:
                    self.assertEqual(str(raised), "MIGRATION-BODY-FAILURE")
                    self.assertTrue(
                        any(
                            "MIGRATION-LOCK-CLEANUP" in note
                            for note in getattr(raised, "__notes__", ())
                        )
                    )
                else:
                    self.fail("body failure was not preserved")

    def test_lock_identity_failure_preserves_unknown_lock_object(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.phase_fixture(root)
            lock_path = self.tool._repository_lock_path(root)
            with (
                mock.patch.object(
                    self.tool,
                    "_fd_identity",
                    side_effect=self.tool.MigrationAbort("MIGRATION-FILESYSTEM"),
                ),
                self.assertRaisesRegex(
                    self.tool.MigrationAbort, "MIGRATION-FILESYSTEM"
                ) as raised,
            ):
                with self.tool._repository_lock(root):
                    self.fail("lock body must not run")
            self.assertTrue(lock_path.is_file())
            self.assertTrue(
                any(
                    "LOCK-IDENTITY-UNAVAILABLE" in note
                    for note in getattr(raised.exception, "__notes__", ())
                )
            )

    def test_direct_apply_validates_full_manifest_and_closed_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, entries = self.phase_fixture(root)
            self.write_manifest(root, commit, entries)
            pairs = self.tool.plan_phase(root, entries, "archive")
            before = {(root / source).read_bytes() for source, _ in pairs}
            with (
                mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                self.assertRaisesRegex(self.tool.MigrationAbort, "MIGRATION-COUNTS"),
            ):
                self.tool.apply_phase(root, pairs, "archive")
            self.assertEqual(
                {(root / source).read_bytes() for source, _ in pairs}, before
            )
            self.assertTrue(all(not (root / target).exists() for _, target in pairs))

    def test_direct_apply_rejects_broken_opposite_phase_before_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, entries = self.phase_fixture(root)
            self.write_manifest(root, commit, entries)
            pairs = self.tool.plan_phase(root, entries, "archive")
            manifest_path = root / "scripts/document-taxonomy-migration.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            opposite = next(
                row
                for row in manifest["entries"]
                if row["disposition"] == "move-current"
            )
            opposite["sourceBlob"] = "0" * 40
            manifest_path.write_text(
                json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
            )
            subprocess.run(["git", "add", str(manifest_path.relative_to(root))], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "break opposite phase"], cwd=root, check=True)
            with (
                mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                mock.patch.object(self.tool, "validate_counts"),
                self.assertRaisesRegex(
                    self.tool.MigrationAbort, "(?:SOURCE-BLOB|CHANGED-SOURCE)"
                ),
            ):
                self.tool.apply_phase(root, pairs, "archive")
            self.assertTrue(all((root / source).is_file() for source, _ in pairs))
            self.assertTrue(all(not (root / target).exists() for _, target in pairs))

    def test_target_parent_dirfd_and_precommit_revalidation_preserve_replacement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, entries = self.phase_fixture(root)
            self.write_manifest(root, commit, entries)
            pairs = self.tool.plan_phase(root, entries, "archive")
            first_target = root / pairs[0][1]
            replacement = b"third-party target replacement"
            real_verify = getattr(self.tool, "_verify_all_targets", None)
            calls = 0

            def replace_before_commit(transaction):
                nonlocal calls
                calls += 1
                if calls == 2:
                    replacement_path = first_target.with_suffix(".third-party")
                    replacement_path.write_bytes(replacement)
                    self.tool.os.replace(replacement_path, first_target)
                return real_verify(transaction)

            with (
                mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                mock.patch.object(self.tool, "validate_counts"),
                mock.patch.object(self.tool, "_run_gitleaks", return_value=0),
                mock.patch.object(
                    self.tool, "_verify_all_targets", side_effect=replace_before_commit
                ),
                self.assertRaisesRegex(self.tool.MigrationAbort, "MIGRATION-ROLLBACK"),
            ):
                self.tool.apply_phase(root, pairs, "archive")
            self.assertEqual(first_target.read_bytes(), replacement)
            self.assertTrue(all((root / source).is_file() for source, _ in pairs))

    def test_commit_revalidation_restores_sources_and_preserves_replacement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, entries = self.phase_fixture(root)
            self.write_manifest(root, commit, entries)
            pairs = self.tool.plan_phase(root, entries, "archive")
            source_payloads = {
                root / source: (root / source).read_bytes() for source, _ in pairs
            }
            first_target = root / pairs[0][1]
            replacement = b"third-party replacement at commit boundary"
            real_verify = self.tool._verify_all_targets
            calls = 0

            def replace_at_commit(transaction):
                nonlocal calls
                calls += 1
                if calls == len(pairs) + 2:
                    replacement_path = first_target.with_suffix(".third-party")
                    replacement_path.write_bytes(replacement)
                    self.tool.os.replace(replacement_path, first_target)
                return real_verify(transaction)

            with (
                mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                mock.patch.object(self.tool, "validate_counts"),
                mock.patch.object(self.tool, "_run_gitleaks", return_value=0),
                mock.patch.object(
                    self.tool, "_verify_all_targets", side_effect=replace_at_commit
                ),
                self.assertRaisesRegex(self.tool.MigrationAbort, "MIGRATION-ROLLBACK"),
            ):
                self.tool.apply_phase(root, pairs, "archive")
            self.assertEqual(calls, len(pairs) + 2)
            self.assertEqual(first_target.read_bytes(), replacement)
            for source, payload in source_payloads.items():
                self.assertEqual(source.read_bytes(), payload)
            self.assertEqual(tuple(root.rglob(".migration-*")), ())

    def test_source_replacement_is_preserved_with_original_recovery_residue(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, entries = self.phase_fixture(root)
            self.write_manifest(root, commit, entries)
            pairs = self.tool.plan_phase(root, entries, "archive")
            first_source = root / pairs[0][0]
            original = first_source.read_bytes()
            replacement = b"third-party source replacement"
            real_rename = self.tool.os.rename
            injected = False

            def replace_before_quarantine(source, target, **kwargs):
                nonlocal injected
                if not injected and str(target).startswith("removed-"):
                    injected = True
                    replacement_path = first_source.with_suffix(".third-party")
                    replacement_path.write_bytes(replacement)
                    self.tool.os.replace(replacement_path, first_source)
                return real_rename(source, target, **kwargs)

            with (
                mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                mock.patch.object(self.tool, "validate_counts"),
                mock.patch.object(self.tool, "_run_gitleaks", return_value=0),
                mock.patch.object(
                    self.tool.os, "rename", side_effect=replace_before_quarantine
                ),
                self.assertRaisesRegex(self.tool.MigrationAbort, "MIGRATION-ROLLBACK"),
            ):
                self.tool.apply_phase(root, pairs, "archive")
            self.assertTrue(injected)
            self.assertEqual(first_source.read_bytes(), replacement)
            recovery = tuple(root.glob(".migration-recovery-*"))
            self.assertEqual(len(recovery), 1)
            self.assertIn(original, [path.read_bytes() for path in recovery[0].iterdir()])

    def test_builder_pins_expected_commit_and_rejects_census_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            commit, _ = self.phase_fixture(root)
            unrelated = root / "unrelated.txt"
            unrelated.write_text("later head\n", encoding="utf-8")
            subprocess.run(["git", "add", "unrelated.txt"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "later head"], cwd=root, check=True)
            with (
                mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                mock.patch.object(self.tool, "validate_manifest_data"),
            ):
                manifest = self.tool.build_manifest(root)
            self.assertEqual(manifest["sourceCommit"], commit)
            for row in manifest["entries"]:
                self.assertEqual(
                    row["sourceBlob"],
                    self.git(root, "rev-parse", f"{commit}:{row['source']}"),
                )
            drift = root / "docs/04.execution/plans/2026-02-02-drift.md"
            drift.write_text("drift\n", encoding="utf-8")
            subprocess.run(["git", "add", "docs"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "source census drift"], cwd=root, check=True)
            with (
                mock.patch.object(self.tool, "EXPECTED_SOURCE_COMMIT", commit),
                self.assertRaisesRegex(self.tool.MigrationAbort, "MIGRATION-CENSUS"),
            ):
                self.tool.build_manifest(root)

    def test_git_ignores_hostile_environment_and_rejects_non_root(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as hostile:
            root = Path(tmp)
            self.phase_fixture(root)
            with mock.patch.dict(
                self.tool.os.environ,
                {"GIT_DIR": hostile, "GIT_WORK_TREE": hostile, "GIT_INDEX_FILE": hostile},
            ):
                self.assertEqual(self.tool._git(root, "rev-parse", "--show-toplevel"), str(root))
            with self.assertRaisesRegex(self.tool.MigrationAbort, "MIGRATION-ROOT"):
                self.tool._git(root / "docs", "status", "--short")

    def test_plan_phase_rejects_dirty_controlled_path_but_not_unrelated_edit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, entries = self.phase_fixture(root)
            unrelated = root / "tests/focused.txt"
            unrelated.parent.mkdir()
            unrelated.write_text("allowed\n", encoding="utf-8")
            self.tool.plan_phase(root, entries, "archive")
            (root / entries[0]["source"]).write_text("dirty\n", encoding="utf-8")
            with self.assertRaisesRegex(self.tool.MigrationAbort, "CONTROLLED-DIRTY"):
                self.tool.plan_phase(root, entries, "archive")

    def test_cli_fixed_phase_apply_forms_parse(self):
        archive = self.tool._parser().parse_args(["--phase", "archive", "--apply"])
        move = self.tool._parser().parse_args(["--phase", "move", "--apply"])
        self.assertTrue(archive.apply and move.apply)
        self.assertEqual((archive.phase, move.phase), ("archive", "move"))
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                self.tool._parser().parse_args(["--build"])

    def test_cli_rejects_alternate_manifest_path(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(
                self.tool.main(
                    [
                        "--root",
                        str(ROOT),
                        "--manifest",
                        str(ROOT / "scripts/document-taxonomy-migration.json"),
                        "--check",
                    ]
                ),
                1,
            )

    def test_cli_apply_runs_plan_before_apply_without_production_writes(self):
        entries = tuple(
            MappingProxyType(
                {
                    "source": f"docs/04.execution/plans/{index}.md",
                    "target": f"docs/98.archive/04.execution/plans/{index}.md",
                    "workUnit": f"Archive-{index}",
                    "disposition": "archive-unique",
                    "sourceBlob": "a" * 40,
                    "reviewed": True,
                }
            )
            for index in range(132)
        )
        planned = ((Path(entries[0]["source"]), Path(entries[0]["target"])),)
        with (
            mock.patch.object(
                self.tool,
                "load_manifest_document",
                return_value=self.tool.ManifestDocument(
                    self.tool.EXPECTED_SOURCE_COMMIT, entries
                ),
            ),
            mock.patch.object(self.tool, "_controlled_dirty", return_value=()),
            mock.patch.object(self.tool, "validate_manifest", return_value=()),
            mock.patch.object(self.tool, "validate_counts"),
            mock.patch.object(self.tool, "plan_phase", return_value=planned) as plan,
            mock.patch.object(self.tool, "apply_phase") as apply,
            contextlib.redirect_stdout(io.StringIO()),
        ):
            self.assertEqual(self.tool.main(["--phase", "archive", "--apply"]), 0)
        plan.assert_called_once()
        apply.assert_called_once_with(Path.cwd(), planned, "archive")


if __name__ == "__main__":
    unittest.main()
