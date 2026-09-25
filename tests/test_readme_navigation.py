"""Synthetic cases for the README navigation contract (SPEC-0091)."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path, PurePosixPath
from types import MappingProxyType

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import document_contracts as contracts  # noqa: E402


def load_links():
    spec = importlib.util.spec_from_file_location(
        "validate_links_and_owners_nav", ROOT / "scripts/validate-links-and-owners.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


LINKS = load_links()
FENCE = "`" * 3
ROUTER = "common/readme-stage-index"
IMPLEMENTATION = "common/readme-implementation"


def navigation(pending=()):
    return contracts.ReadmeNavigation(
        placeholders=frozenset({"README.md", ".gitkeep"}),
        forbidden_index_columns=frozenset(
            {"Status", "\uc0c1\ud0dc", "\ucd5c\uc885 \uc218\uc815"}
        ),
        max_deep_links_per_child=1,
        profiles=MappingProxyType(
            {
                ROUTER: contracts.ReadmeNavigationProfile("Document Index", True),
                IMPLEMENTATION: contracts.ReadmeNavigationProfile("Structure", False),
            }
        ),
        pending_paths=frozenset(PurePosixPath(p) for p in pending),
    )


def tree(*files, modes=None):
    values = {PurePosixPath(f): "100644" for f in files}
    values.update({PurePosixPath(k): v for k, v in (modes or {}).items()})
    return LINKS.TrackedTree.from_modes(values)


SPECS = tree(
    "s/README.md",
    "s/0001-a/spec.md",
    "s/0001-a/plan.md",
    "s/0001-a/tasks/t.md",
    "s/0002-b/spec.md",
)


def run(text, files=SPECS, profile=ROUTER, pending=(), path="s/README.md"):
    readme = PurePosixPath(path)
    return LINKS.readme_navigation_diagnostics(
        navigation(pending), {readme: LINKS.ReadmeSource(profile, text)}, files
    )


def codes(text, **kwargs):
    return sorted({item.rule_id for item in run(text, **kwargs)})


GOOD_ROUTER = (
    "# S\n\n## Document Index\n\n"
    "| Package | Purpose |\n| --- | --- |\n"
    "| [0001-a/](./0001-a/) | A |\n| [0002-b/][b] | B |\n\n"
    "[b]: ./0002-b/\n"
)


class ReadmeNavigationTests(unittest.TestCase):
    def test_router_linking_direct_folders_passes(self):
        self.assertEqual(codes(GOOD_ROUTER), [])

    def test_child_readme_is_a_direct_entry(self):
        files = tree(
            "s/README.md", "s/0001-a/README.md", "s/0001-a/x.md", "s/0002-b/y.md"
        )
        text = GOOD_ROUTER.replace(
            "[0001-a/](./0001-a/)", "[0001-a](./0001-a/README.md)"
        )
        self.assertEqual(codes(text, files=files), [])

    def test_member_link_in_navigation_fails_depth(self):
        text = GOOD_ROUTER.replace("[0001-a/](./0001-a/)", "[0001-a](./0001-a/spec.md)")
        self.assertIn("README-NAV-DEPTH", codes(text))

    def test_folder_label_on_file_link_fails(self):
        text = GOOD_ROUTER.replace("(./0001-a/)", "(./0001-a/spec.md)")
        self.assertIn("README-NAV-LABEL", codes(text))

    def test_nested_tree_fails_and_flat_tree_passes(self):
        nested = (
            GOOD_ROUTER
            + f"\n{FENCE}text\ns/\n├── 0001-a/\n│   └── spec.md\n└── 0002-b/\n{FENCE}\n"
        )
        flat = GOOD_ROUTER + f"\n{FENCE}text\ns/\n├── 0001-a/\n└── 0002-b/\n{FENCE}\n"
        self.assertIn("README-NAV-TREE", codes(nested))
        self.assertEqual(codes(flat), [])

    def test_listing_hidden_in_related_documents_or_html_fails(self):
        related = GOOD_ROUTER + (
            "\n## Related Documents\n\n- [spec](./0001-a/spec.md)\n- [plan](./0001-a/plan.md)\n"
        )
        html = GOOD_ROUTER + (
            '\n<details><summary>x</summary>\n\n<a href="./0001-a/spec.md">s</a>\n'
            '<a href="./0001-a/plan.md">p</a>\n\n</details>\n'
        )
        self.assertIn("README-NAV-ENUMERATION", codes(related))
        self.assertIn("README-NAV-ENUMERATION", codes(html))

    def test_one_deep_citation_passes(self):
        text = GOOD_ROUTER + "\n## Related Documents\n\n- [spec](./0001-a/spec.md)\n"
        self.assertEqual(codes(text), [])

    def test_code_span_paths_in_tables_count(self):
        files = tree("g/README.md", "g/p/a/k.yaml", "g/p/b/k.yaml", "g/w/c/k.yaml")
        text = (
            "# G\n\n## Structure\n\n- [p/](./p/)\n- [w/](./w/)\n\n"
            "## Operations\n\n| Area | Owner |\n| --- | --- |\n"
            "| `p/a` | x |\n| `p/b` | y |\n"
        )
        found = codes(text, files=files, profile=IMPLEMENTATION, path="g/README.md")
        self.assertIn("README-NAV-ENUMERATION", found)

    def test_code_spans_in_prose_outside_navigation_do_not_count(self):
        files = tree("g/README.md", "g/p/a/k.yaml", "g/p/b/k.yaml")
        text = (
            "# G\n\n## Structure\n\n- [p/](./p/)\n\n"
            "## Operations\n\nEdit `p/a` before `p/b`.\n"
        )
        self.assertEqual(
            codes(text, files=files, profile=IMPLEMENTATION, path="g/README.md"), []
        )

    def test_missing_child_fails_complete(self):
        text = GOOD_ROUTER.replace("| [0002-b/][b] | B |\n", "")
        self.assertIn("README-NAV-COMPLETE", codes(text))

    def test_collection_lists_direct_documents(self):
        files = tree("r/README.md", "r/0001-x.md", "r/0002-y.md")
        text = (
            "# R\n\n## Document Index\n\n"
            "- [0001-x](./0001-x.md)\n- [0002-y](./0002-y.md)\n"
        )
        self.assertEqual(codes(text, files=files, path="r/README.md"), [])
        partial = text.replace("- [0002-y](./0002-y.md)\n", "")
        self.assertIn(
            "README-NAV-COMPLETE", codes(partial, files=files, path="r/README.md")
        )

    def test_copied_status_column_fails(self):
        text = GOOD_ROUTER.replace(
            "| Package | Purpose |", "| Package | \uc0c1\ud0dc |"
        )
        self.assertIn("README-NAV-COPY", codes(text))

    def test_placeholder_only_and_empty_folders_need_nothing(self):
        files = tree("e/README.md", "e/.gitkeep")
        self.assertEqual(
            codes(
                "# E\n\n## Document Index\n\nEmpty.\n", files=files, path="e/README.md"
            ),
            [],
        )

    def test_symlink_and_submodule_are_leaf_children(self):
        files = tree(
            "k/README.md",
            modes={"k/link": "120000", "k/module": "160000"},
        )
        text = "# K\n\n## Structure\n\n- [link](./link)\n- [module](./module)\n"
        self.assertEqual(
            codes(text, files=files, profile=IMPLEMENTATION, path="k/README.md"), []
        )

    def test_profile_without_navigation_entry_is_ignored(self):
        self.assertEqual(
            codes("# W\n\n- [a](./0001-a/spec.md)\n", profile="x/other"), []
        )

    def test_pending_readme_is_skipped_until_it_passes(self):
        bad = GOOD_ROUTER.replace("(./0001-a/)", "(./0001-a/spec.md)")
        self.assertEqual(codes(bad, pending=("s/README.md",)), [])
        self.assertEqual(
            codes(GOOD_ROUTER, pending=("s/README.md",)), ["README-NAV-PENDING"]
        )

    def test_root_relative_code_spans_count_in_navigation(self):
        rows = (
            "\n| Path | Use |\n| --- | --- |\n"
            "| `s/0001-a/spec.md` | A |\n| ``s/0001-a/plan.md`` | A |\n"
        )
        self.assertIn("README-NAV-ENUMERATION", codes(GOOD_ROUTER + rows))
        # Outside navigation a root path cites contract evidence.
        self.assertEqual(codes(GOOD_ROUTER + "\n## Other\n" + rows), [])

    def test_code_formatted_folder_label_on_file_fails(self):
        text = GOOD_ROUTER + "\nSee [`0001-a/`](./0001-a/spec.md).\n"
        self.assertIn("README-NAV-LABEL", codes(text))

    def test_emphasized_status_header_fails(self):
        text = GOOD_ROUTER.replace("| Package | Purpose |", "| Package | **Status** |")
        self.assertIn("README-NAV-COPY", codes(text))

    def test_pending_readme_without_navigation_profile_fails(self):
        self.assertEqual(
            codes("# W\n", profile="x/other", pending=("s/README.md",)),
            ["README-NAV-PENDING"],
        )

    def test_untracked_pending_path_fails(self):
        self.assertIn(
            "README-NAV-PENDING", codes(GOOD_ROUTER, pending=("missing/README.md",))
        )


class ReadmeNavigationRegistryTests(unittest.TestCase):
    def raw(self, **changes):
        contract = {
            "placeholders": ["README.md", ".gitkeep"],
            "forbidden_index_columns": ["Status"],
            "max_deep_links_per_child": 1,
            "profiles": {ROUTER: {"section": "Document Index", "complete": True}},
            "pending_paths": [],
        }
        contract.update(changes)
        return {"readme_navigation": contract}

    def profiles(self):
        return {
            ROUTER: {
                "mode": "router",
                "sections": {"required": ["Overview", "Document Index"]},
            },
            "sdlc/spec": {"mode": "authored", "sections": {"required": ["Overview"]}},
        }

    def faults(self, **changes):
        return [
            item.rule_id
            for item in contracts._readme_navigation_registry_diagnostics(
                self.raw(**changes), self.profiles()
            )
        ]

    def test_consistent_contract_passes(self):
        self.assertEqual(self.faults(), [])

    def test_contradictions_fail(self):
        for changes in (
            {"profiles": {"missing/profile": {"section": "X", "complete": True}}},
            {"profiles": {"sdlc/spec": {"section": "Overview", "complete": True}}},
            {"profiles": {ROUTER: {"section": "Not A Heading", "complete": True}}},
            {"max_deep_links_per_child": 0},
            {"pending_paths": ["docs/notes.md"]},
        ):
            with self.subTest(changes=changes):
                self.assertEqual(self.faults(**changes), ["REGISTRY_README_NAVIGATION"])

    def test_repository_registry_loads_the_contract(self):
        registry = contracts.load_registry(ROOT)
        self.assertIsNotNone(registry.readme_navigation)
        self.assertEqual(registry.readme_navigation.max_deep_links_per_child, 1)


class RepositoryContractTests(unittest.TestCase):
    """The repository contract replaces the collection index checks."""

    def diagnostics(self, path, profile, text, files):
        navigation = contracts.load_registry(ROOT).readme_navigation
        navigation = contracts.ReadmeNavigation(
            placeholders=navigation.placeholders,
            forbidden_index_columns=navigation.forbidden_index_columns,
            max_deep_links_per_child=navigation.max_deep_links_per_child,
            profiles=navigation.profiles,
            pending_paths=frozenset(),
        )
        return {
            item.rule_id
            for item in LINKS.readme_navigation_diagnostics(
                navigation,
                {PurePosixPath(path): LINKS.ReadmeSource(profile, text)},
                tree(path, *files),
            )
        }

    def test_research_pack_must_reach_every_report(self):
        path = "docs/90.references/research/0009-x/README.md"
        files = (
            "docs/90.references/research/0009-x/m0001-a.md",
            "docs/90.references/research/0009-x/m0002-b.md",
        )
        text = "# X\n\n## Report Index\n\n- [a](m0001-a.md)\n"
        self.assertEqual(
            self.diagnostics(path, "common/readme-research-pack", text, files),
            {"README-NAV-COMPLETE"},
        )

    def test_research_collection_may_not_link_pack_members(self):
        path = "docs/90.references/research/README.md"
        files = (
            "docs/90.references/research/0009-x/README.md",
            "docs/90.references/research/0009-x/m0001-a.md",
        )
        text = (
            "# R\n\n## Item Index\n\n- [0009-x/](./0009-x/)\n"
            "- [a](./0009-x/m0001-a.md)\n"
        )
        self.assertIn(
            "README-NAV-DEPTH",
            self.diagnostics(path, "common/readme-collection-index", text, files),
        )

    def test_knowledge_collection_must_reach_every_document(self):
        path = ".agents/knowledge/README.md"
        files = (".agents/knowledge/map.md", ".agents/knowledge/other.md")
        text = "# K\n\n## Item Index\n\n- [map](map.md)\n"
        self.assertEqual(
            self.diagnostics(path, "common/readme-collection-index", text, files),
            {"README-NAV-COMPLETE"},
        )


if __name__ == "__main__":
    unittest.main()
