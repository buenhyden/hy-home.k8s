"""Current successor closure and immutable recovery for common authority routing."""

from __future__ import annotations

import dataclasses
import hashlib
import types
import unittest
from pathlib import Path, PurePosixPath

from scripts import archive_validation as archive

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = "docs/98.archive/migrations/0021-common-agent-authority-routing.md"


class CommonAgentsArchiveRoutesTest(unittest.TestCase):
    def test_successor_record_closes_its_current_and_predecessor_endpoints(self):
        entries, _ = archive.parse_migration_control(
            MIGRATION, (ROOT / MIGRATION).read_bytes()
        )
        affected_sources = {row["legacy_path"] for row in entries}
        edges = {}
        departures = {}
        arrivals = {}
        for path in sorted((ROOT / "docs/98.archive/migrations").glob("*.md")):
            relative = path.relative_to(ROOT).as_posix()
            if archive.generic_migration_id(relative) is None:
                continue
            rows, _ = archive.parse_migration_control(relative, path.read_bytes())
            for row in rows:
                departures[row["legacy_path"]] = relative
                edges[row["legacy_path"]] = (
                    "docs/98.archive/README.md"
                    if row["action"] == "deleted"
                    else row["stable_path"] or row["replacement"]
                )
                target = edges[row["legacy_path"]]
                arrivals[target] = max(arrivals.get(target, relative), relative)
        reoccupied = {
            path
            for path, departure in departures.items()
            if arrivals.get(path, departure) > departure
        }
        for source, target in archive.compose_migration_targets(
            (edges,), reoccupied=reoccupied
        ).items():
            if source not in affected_sources and edges[source] not in affected_sources:
                continue
            with self.subTest(source=source, target=target):
                self.assertTrue((ROOT / target).is_file())
                self.assertFalse((ROOT / target).is_symlink())

    def test_successor_record_preserves_exact_git_source_identities(self):
        rows, _ = archive.parse_migration_control(
            MIGRATION, (ROOT / MIGRATION).read_bytes()
        )
        requests = {}
        for row in rows:
            requests.setdefault(row["source_commit"], []).append(row["legacy_path"])
        sources = archive._regular_source_bytes(
            ROOT, {commit: tuple(sorted(paths)) for commit, paths in requests.items()}
        )
        for row in rows:
            with self.subTest(source=row["legacy_path"]):
                blob, content = sources[row["source_commit"], row["legacy_path"]]
                self.assertEqual(blob, row["source_blob"])
                self.assertEqual(
                    hashlib.sha256(content).hexdigest(), row["content_sha256"]
                )

    def test_prior_sealed_records_keep_their_complete_baseline_bytes(self):
        rows, _ = archive.parse_migration_control(
            MIGRATION, (ROOT / MIGRATION).read_bytes()
        )
        commits = {
            row["source_commit"]
            for row in rows
            if row["legacy_path"].startswith("docs/00.agent-governance/")
        }
        self.assertEqual(len(commits), 1)
        paths = tuple(
            path.relative_to(ROOT).as_posix()
            for path in sorted((ROOT / "docs/98.archive/migrations").glob("*.md"))
            if path.relative_to(ROOT).as_posix() < MIGRATION
        )
        baseline = archive._regular_source_bytes(ROOT, {commits.pop(): paths})
        for (_commit, path), (_blob, content) in baseline.items():
            with self.subTest(record=path):
                self.assertEqual((ROOT / path).read_bytes(), content)


class CommonAuthorityOwnerDiagnosticsTest(unittest.TestCase):
    def context(self, profile):
        role = PurePosixPath(".agents/roles/quality-engineer.md")
        return types.SimpleNamespace(
            governance_current_paths=(role,),
            governance_current_states=("active", "accepted"),
            paths=(role,),
            profiles={role: profile},
            metadata={role: {"status": "active"}},
            texts={PurePosixPath(".agents/README.md"): "# Common authority\n"},
        )

    def test_current_owners_do_not_require_a_duplicate_lifecycle_table(self):
        links = archive._load_canonical_link_module()
        context = self.context(
            links.ProfileView("governance/role", "governance", "authored")
        )
        self.assertEqual(links._governance_current_owner_diagnostics(context), [])

    def test_wrong_current_owner_profile_is_rejected_without_a_mirror_table(self):
        links = archive._load_canonical_link_module()
        context = self.context(links.ProfileView("sdlc/spec", "sdlc", "authored"))
        diagnostics = links._governance_current_owner_diagnostics(context)
        self.assertIn(
            "REGISTRY_GOVERNANCE_CURRENT_OWNER_PROFILE",
            {item.rule_id for item in diagnostics},
        )


class SpecIndexNavigationTest(unittest.TestCase):
    """SPEC-0091 replaced the Stage 03 spec index with the navigation contract."""

    def diagnostics(self, text):
        links = archive._load_canonical_link_module()
        index = PurePosixPath("docs/03.specs/README.md")
        package = index.parent / "0999-status-fixture"
        tree = links.TrackedTree.from_modes(
            {
                index: "100644",
                package / "spec.md": "100644",
                package / "plan.md": "100644",
                package / "tasks/tsk-0001-fixture.md": "100644",
            }
        )
        navigation = dataclasses.replace(
            links.load_registry(ROOT).readme_navigation,
            pending_paths=frozenset(),
            exempt_paths=frozenset(),
        )
        return {
            item.rule_id
            for item in links.readme_navigation_diagnostics(
                navigation,
                {index: links.ReadmeSource("common/readme-stage-index", text)},
                tree,
            )
        }

    def test_member_listing_with_copied_status_is_rejected(self):
        fence = "`" * 3
        text = (
            f"## Document Index\n\n{fence}text\n03.specs/\n"
            f"└── 0999-status-fixture/\n    └── spec.md\n{fence}\n\n"
            "| Spec | Purpose | Status |\n| --- | --- | --- |\n"
            "| [Fixture](./0999-status-fixture/spec.md) | Fixture | `done` |\n"
        )
        self.assertLessEqual(
            {"README-NAV-DEPTH", "README-NAV-TREE", "README-NAV-COPY"},
            self.diagnostics(text),
        )

    def test_package_folder_rows_pass(self):
        text = (
            "## Document Index\n\n| Package | Purpose |\n| --- | --- |\n"
            "| [0999-status-fixture/](./0999-status-fixture/) | Fixture |\n"
        )
        self.assertEqual(self.diagnostics(text), set())


if __name__ == "__main__":
    unittest.main()
