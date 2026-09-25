---
title: "README Navigation Contract Implementation Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "active"
owner: "platform"
updated: "2026-09-25"
layer: "specs"
artifact_id: "SPEC-0091-PLAN-0001"
---

# README Navigation Contract Implementation Plan

## Global Constraints

- Goal: every tracked README lists only its direct children, under one
  registry contract that one validator enforces.
- Spec: [SPEC-0091](spec.md). Every work package implicitly includes these
  constraints.
- The request owner approved the design and the Spec on 2026-09-25. Work runs
  on the local branch `readme-navigation-contract` from `main` at `438e69aa`.
  Push, pull request, merge, and live actions are not authorized.
- Each commit runs `python3 scripts/qa.py staged` over its exact index and
  `git diff --check`. No hook bypass, no `--no-verify`, no weakened assertion.
- Contract values are exact: placeholders `README.md`, `.gitkeep`;
  `max_deep_links_per_child` is `1`; forbidden index columns `Status`,
  `Updated`, `Last Updated`, and the Korean status, last-updated, and currency headers (JSON escapes `\uc0c1\ud0dc`, `\ucd5c\uc885 \uc218\uc815`, `\ud604\uc7ac\uc131`).
- Out of scope: `docs/98.archive/README.md` tables, document language, the
  `.agents`/`.claude`/`.codex` English-only rule, template language, retained
  bodies, lifecycle states and edges.
- READMEs rewritten under `docs/` and implementation folders are written
  Korean-first; `.agents`, `.claude`, and `.codex` READMEs change structure
  only and stay English until the language package.

## Overview

The Plan adds the `readme_navigation` registry contract and its validator
first, with every currently violating README in `pending_paths`. Each later
work package rewrites one area, removes it from `pending_paths`, and deletes
the exhaustive-list check that area used, so every commit is green and the
temporary list only shrinks.

## Context

The survey on 2026-09-25 ran a prototype of the rules over the 43 tracked
READMEs. Violations cluster in `docs/03.specs`, `docs/90.references`,
`docs/99.templates/templates`, `gitops`, `infrastructure`, the root README,
and the collection READMEs that repeat a tree and a table. The checks that
force those lists are `DECLARED_INDEXES` and `COLLECTION_INDEXES` in
`scripts/validate-links-and-owners.py`, `_check_index` in
`scripts/validate-knowledge-surface.py`, and the Stage 05 Korean document-index block
in `scripts/validation/repository/quality.py`. Links in this repository are
extracted by `_extract_links` and resolved by `_local_destination` in
`validate-links-and-owners.py`; registry contracts are typed and loaded in
`scripts/document_contracts.py`; top-level registry keys are admitted by
`OPTIONAL_TOP_LEVEL_KEYS` in `scripts/document_authority.py`.

## Goals & In-Scope

Deliver WP-001 to WP-010 below: the contract, the validator, the four check
replacements, the README rewrites, two matrix READMEs, template guidance, and
the evidence.

## Non-Goals & Out-of-Scope

No archive ledger move, no language contract, no new README for a folder that
does not carry a matrix, no lifecycle change, no push.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Propose the package | None | Spec approved | Staged QA |
| WP-002 | Contract, schema, loader, validator, tests; initial `pending_paths`; activation; SPEC-0008 handoff | WP-001 | Plan approved | Focused tests, staged QA |
| WP-003 | `docs/03.specs` README; remove `INDEX-*` | WP-002 | Validator green | Focused tests, staged QA |
| WP-004 | `docs/90.references` READMEs; remove `COLLECTION-INDEX-*` | WP-003 | Validator green | Focused tests, staged QA |
| WP-005 | `.agents/knowledge` README; remove `KNOWLEDGE-INDEX-MISSING` | WP-004 | Validator green | Focused tests, staged QA |
| WP-006 | `docs/05.operations` READMEs; remove the Korean document-index status and date parity | WP-005 | Validator green | Staged QA |
| WP-007 | `gitops` and `infrastructure` matrices move to the folders they enumerate | WP-006 | Validator green | Staged QA |
| WP-008 | Remaining READMEs, by disjoint area | WP-007 | Only non-code READMEs remain pending | Staged QA per area |
| WP-009 | Navigation guidance in the `readme-*` templates | WP-008 | `pending_paths` is the Stage 98 README alone | Staged QA |
| WP-010 | Evidence, full QA, close | WP-009 | All exit evidence met | Full QA |

Execution: WP-001 to WP-007 and WP-009 to WP-010 run directly in order,
because they share `validate-links-and-owners.py` and `quality.py`. WP-008
is delegated per area to one implementer subagent each, with a spec and a
quality review per area, and one commit per area made sequentially by the
integrator.

### WP-001: Propose the package

**Files:** create `spec.md`, `plan.md`, `tasks/tsk-0001-converge-readme-navigation.md`
in this package; modify `docs/03.specs/README.md` (tree entry and index row,
following the existing 0090 entries) and
`docs/01.requirements/0003-workspace-agent-governance-platform.md` (one
reciprocal sentence after the SPEC-0090 sentence).

- [ ] Add to REQ-0003 after the SPEC-0090 sentence:
  `Constraining every README to its direct children under one registry
  navigation contract is owned by
  [SPEC-0091](../03.specs/0091-readme-navigation-contract/spec.md).`
- [ ] Run `python3 scripts/qa.py staged`; expected: every selected gate PASS.
- [ ] Commit `docs(specs): propose SPEC-0091 for a README navigation contract`.

### WP-002: Contract, validator, and tests

**Files:**
- Modify: `docs/99.templates/contracts/document-profile.schema.json` (top-level `properties`)
- Modify: `docs/99.templates/registry.json` (new top-level `readme_navigation`)
- Modify: `scripts/document_authority.py` (`OPTIONAL_TOP_LEVEL_KEYS`)
- Modify: `scripts/document_contracts.py` (dataclasses, `Registry` field, loader, self-check)
- Modify: `scripts/validate-links-and-owners.py` (validator and wiring)
- Create: `tests/test_readme_navigation.py`
- Modify: `docs/03.specs/0008-current-local-gitops-platform/spec.md` (scope sentence, version bump)
- Modify: this package's Spec, Plan, and Task (`draft` to `active`, `queued` to `in-progress`)

**Interfaces produced:**
- `document_contracts.ReadmeNavigationProfile(section: str, complete: bool)`
- `document_contracts.ReadmeNavigation(placeholders: frozenset[str], forbidden_index_columns: frozenset[str], max_deep_links_per_child: int, profiles: Mapping[str, ReadmeNavigationProfile], pending_paths: frozenset[PurePosixPath])`
- `Registry.readme_navigation: ReadmeNavigation | None`
- `validate-links-and-owners.TrackedTree.from_modes(modes: Mapping[PurePosixPath, str]) -> TrackedTree`
- `validate-links-and-owners.ReadmeSource(profile_id: str, text: str)`
- `validate-links-and-owners.readme_navigation_diagnostics(navigation, readmes: Mapping[PurePosixPath, ReadmeSource], tree: TrackedTree) -> list[Diagnostic]`

- [ ] **Step 1: Write the failing tests** in `tests/test_readme_navigation.py`:

```python
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
        forbidden_index_columns=frozenset({"Status", "\uc0c1\ud0dc", "\ucd5c\uc885 \uc218\uc815"}),
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
        files = tree("s/README.md", "s/0001-a/README.md", "s/0001-a/x.md", "s/0002-b/y.md")
        text = GOOD_ROUTER.replace("[0001-a/](./0001-a/)", "[0001-a](./0001-a/README.md)")
        self.assertEqual(codes(text, files=files), [])

    def test_member_link_in_navigation_fails_depth(self):
        text = GOOD_ROUTER.replace("[0001-a/](./0001-a/)", "[0001-a](./0001-a/spec.md)")
        self.assertIn("README-NAV-DEPTH", codes(text))

    def test_folder_label_on_file_link_fails(self):
        text = GOOD_ROUTER.replace("(./0001-a/)", "(./0001-a/spec.md)")
        self.assertIn("README-NAV-LABEL", codes(text))

    def test_nested_tree_fails_and_flat_tree_passes(self):
        nested = GOOD_ROUTER + f"\n{FENCE}text\ns/\n├── 0001-a/\n│   └── spec.md\n└── 0002-b/\n{FENCE}\n"
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
        text = GOOD_ROUTER.replace("| Package | Purpose |", "| Package | \uc0c1\ud0dc |")
        self.assertIn("README-NAV-COPY", codes(text))

    def test_placeholder_only_and_empty_folders_need_nothing(self):
        files = tree("e/README.md", "e/.gitkeep")
        self.assertEqual(
            codes("# E\n\n## Document Index\n\nEmpty.\n", files=files, path="e/README.md"),
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
        self.assertEqual(codes("# W\n\n- [a](./0001-a/spec.md)\n", profile="x/other"), [])

    def test_pending_readme_is_skipped_until_it_passes(self):
        bad = GOOD_ROUTER.replace("(./0001-a/)", "(./0001-a/spec.md)")
        self.assertEqual(codes(bad, pending=("s/README.md",)), [])
        self.assertEqual(
            codes(GOOD_ROUTER, pending=("s/README.md",)), ["README-NAV-PENDING"]
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


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run to verify failure.** Run
  `python3 -m unittest tests.test_readme_navigation`; expected: errors such as
  `AttributeError: module 'document_contracts' has no attribute 'ReadmeNavigation'`.

- [ ] **Step 3: Add the contract types and loader** in `scripts/document_contracts.py`.
  After `class ArchiveCitation` add:

```python
@dataclass(frozen=True)
class ReadmeNavigationProfile:
    """The navigation section a README profile owns and whether it is complete."""

    section: str
    complete: bool


@dataclass(frozen=True)
class ReadmeNavigation:
    """SPEC-0091: what a README may list, owned by the registry alone."""

    placeholders: frozenset[str]
    forbidden_index_columns: frozenset[str]
    max_deep_links_per_child: int
    profiles: Mapping[str, ReadmeNavigationProfile]
    pending_paths: frozenset[PurePosixPath]
```

  Add `readme_navigation: ReadmeNavigation | None = None` as the last field of
  `Registry`; in the typed-registry builder add
  `readme_navigation=_readme_navigation_from_mapping(raw.get("readme_navigation")),`
  after `legacy_rebased_retained_paths=...`; and add beside
  `_archive_assessment_from_mapping`:

```python
def _readme_navigation_from_mapping(
    raw: Mapping[str, Any] | None,
) -> ReadmeNavigation | None:
    if raw is None:
        return None
    return ReadmeNavigation(
        placeholders=frozenset(raw["placeholders"]),
        forbidden_index_columns=frozenset(raw["forbidden_index_columns"]),
        max_deep_links_per_child=raw["max_deep_links_per_child"],
        profiles=MappingProxyType(
            {
                profile_id: ReadmeNavigationProfile(
                    section=entry["section"], complete=entry["complete"]
                )
                for profile_id, entry in raw["profiles"].items()
            }
        ),
        pending_paths=frozenset(PurePosixPath(value) for value in raw["pending_paths"]),
    )


def _readme_navigation_registry_diagnostics(
    raw_registry: Mapping[str, Any],
    profiles_by_id: Mapping[str, Mapping[str, Any]],
) -> list[Diagnostic]:
    """Require navigation entries to name router profiles and their own H2s."""

    contract = raw_registry.get("readme_navigation")
    if contract is None:
        return []
    faults: list[str] = []
    for profile_id, entry in contract["profiles"].items():
        profile = profiles_by_id.get(profile_id)
        if profile is None:
            faults.append(f"unknown profile {profile_id}")
            continue
        if profile.get("mode") != "router":
            faults.append(f"{profile_id} is not a router profile")
        if entry["section"] not in profile.get("sections", {}).get("required", ()):
            faults.append(f"{profile_id} section {entry['section']!r} is not required")
    if contract["max_deep_links_per_child"] < 1:
        faults.append("max_deep_links_per_child is below one")
    for value in contract["pending_paths"]:
        if PurePosixPath(value).name != "README.md":
            faults.append(f"pending path {value} is not a README")
    return [
        _diagnostic(
            "REGISTRY_README_NAVIGATION",
            expected="router profiles, their required H2 sections, and README paths",
            actual=fault,
        )
        for fault in faults
    ]
```

  Import `MappingProxyType` from `types` if the module does not already, and
  add `*_readme_navigation_registry_diagnostics(raw_registry, profiles_by_id),`
  to the diagnostics list in `validate_registry` after the assessment entry.
  In `scripts/document_authority.py` add `"readme_navigation"` to
  `OPTIONAL_TOP_LEVEL_KEYS` and extend the comment above it with
  `# SPEC-0091 adds the README navigation contract.`

- [ ] **Step 4: Declare the schema** in `document-profile.schema.json` under
  top-level `properties`:

```json
"readme_navigation": {
  "type": "object",
  "additionalProperties": false,
  "required": ["placeholders", "forbidden_index_columns", "max_deep_links_per_child", "profiles", "pending_paths"],
  "properties": {
    "placeholders": {"type": "array", "uniqueItems": true, "items": {"type": "string", "minLength": 1}},
    "forbidden_index_columns": {"type": "array", "uniqueItems": true, "items": {"type": "string", "minLength": 1}},
    "max_deep_links_per_child": {"type": "integer", "minimum": 1},
    "profiles": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "additionalProperties": false,
        "required": ["section", "complete"],
        "properties": {"section": {"type": "string", "minLength": 1}, "complete": {"type": "boolean"}}
      }
    },
    "pending_paths": {"type": "array", "uniqueItems": true, "items": {"type": "string", "pattern": "(^|/)README\\.md$"}}
  }
}
```

- [ ] **Step 5: Add the validator** to `scripts/validate-links-and-owners.py`
  after `_collection_index_diagnostics`:

```python
README_NAV_NESTED_TREE = re.compile(r"^(?:[│|] {2,3}| {4})+[├└]──", re.M)
README_NAV_CODE_SPAN = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")
README_NAV_FOLDER_LABEL = re.compile(r"\[([^\]\n]*/)\]\(<?([^)\s>]+)>?")
README_NAV_TABLE_RULE = re.compile(r"\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)*\|?")
README_NAV_HTML_HREF = re.compile(r"<a\s[^>]*?href\s*=\s*[\"']([^\"']+)[\"']", re.I)
REGULAR_MODES = frozenset({"100644", "100755"})


@dataclass(frozen=True)
class ReadmeSource:
    profile_id: str
    text: str


@dataclass(frozen=True)
class TrackedTree:
    """Stage-0 index entries by mode, plus every folder they imply."""

    modes: Mapping[PurePosixPath, str]
    folders: frozenset[PurePosixPath]

    @classmethod
    def from_modes(cls, modes: Mapping[PurePosixPath, str]) -> "TrackedTree":
        folders = {
            parent
            for path in modes
            for parent in path.parents
            if parent != PurePosixPath(".")
        }
        return cls(dict(modes), frozenset(folders))

    def kind(self, path: PurePosixPath) -> str | None:
        if path in self.folders:
            return "folder"
        mode = self.modes.get(path)
        if mode is None:
            return None
        return "file" if mode in REGULAR_MODES else "leaf"

    def children(
        self, folder: PurePosixPath, placeholders: frozenset[str]
    ) -> dict[str, str]:
        prefix = "" if folder == PurePosixPath(".") else f"{folder.as_posix()}/"
        found: dict[str, str] = {}
        for path in self.modes:
            value = path.as_posix()
            if not value.startswith(prefix):
                continue
            head, separator, _ = value[len(prefix) :].partition("/")
            if not separator and head in placeholders:
                continue
            found[head] = "folder" if separator else self.kind(path) or "file"
        return found


def _readme_visible_lines(text: str) -> tuple[list[str], list[str]]:
    """Split Markdown into lines outside fences and the fenced block bodies."""

    visible: list[str] = []
    blocks: list[str] = []
    fence: str | None = None
    body: list[str] = []
    for line in text.split("\n"):
        opener = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence is None and opener:
            fence, body = opener.group(1), []
            visible.append("")
            continue
        if fence is not None:
            if line.strip().startswith(fence):
                blocks.append("\n".join(body))
                fence = None
            else:
                body.append(line)
            visible.append("")
            continue
        visible.append(line)
    return visible, blocks


def _readme_section(text: str, heading: str) -> str:
    visible, _ = _readme_visible_lines(text)
    chosen: list[str] = []
    inside = False
    for raw, line in zip(text.split("\n"), visible):
        match = re.match(r"^(#{1,2})\s+(.+?)\s*#*\s*$", line)
        if match:
            inside = len(match.group(1)) == 2 and match.group(2) == heading
            continue
        if inside:
            chosen.append(raw)
    return "\n".join(chosen)


def _readme_targets(
    source: PurePosixPath, markdown: str, definitions: str
) -> list[tuple[str, PurePosixPath]]:
    # The canonical extractor masks inline HTML; a listing hidden in raw HTML
    # anchors still lists children, so their href values count here too.
    visible, _ = _readme_visible_lines(markdown)
    hrefs = README_NAV_HTML_HREF.findall("\n".join(visible))
    found = []
    for raw in (*_extract_links(markdown, definitions_text=definitions), *hrefs):
        kind, target = _local_destination(source, raw)
        if kind == "local" and target is not None:
            found.append((raw, target))
    return found


def _readme_relative(
    folder: PurePosixPath, target: PurePosixPath
) -> tuple[str, ...] | None:
    if folder == PurePosixPath("."):
        return target.parts
    try:
        return target.relative_to(folder).parts
    except ValueError:
        return None


def _readme_is_deep(parts: tuple[str, ...]) -> bool:
    return len(parts) > 1 and not (len(parts) == 2 and parts[1] == "README.md")


def _readme_table_headers(markdown: str) -> list[frozenset[str]]:
    headers: list[frozenset[str]] = []
    previous = ""
    for line in markdown.split("\n"):
        stripped = line.strip()
        if previous.startswith("|") and README_NAV_TABLE_RULE.fullmatch(stripped):
            headers.append(
                frozenset(cell.strip() for cell in previous.strip("|").split("|"))
            )
        previous = stripped
    return headers


def _readme_findings(
    path: PurePosixPath,
    source: ReadmeSource,
    rule: Any,
    navigation: Any,
    tree: TrackedTree,
) -> list[Diagnostic]:
    folder = path.parent
    text = source.text
    visible, blocks = _readme_visible_lines(text)
    section = _readme_section(text, rule.section)
    found: list[Diagnostic] = []

    def report(code: str, expected: str, actual: str) -> None:
        found.append(_diag(code, path, source.profile_id, expected, actual))

    section_targets = _readme_targets(path, section, text)
    for raw, target in section_targets:
        parts = _readme_relative(folder, target)
        if parts and _readme_is_deep(parts):
            report(
                "README-NAV-DEPTH",
                "navigation links reach direct children",
                f"{raw} reaches {'/'.join(parts)}",
            )
    for block in blocks:
        if "──" in block and README_NAV_NESTED_TREE.search(block):
            report(
                "README-NAV-TREE",
                "a fenced tree of direct children",
                "a fenced tree nests below the first level",
            )
    for label, raw in README_NAV_FOLDER_LABEL.findall("\n".join(visible)):
        kind, target = _local_destination(path, raw)
        if kind == "local" and target is not None and tree.kind(target) != "folder":
            report(
                "README-NAV-LABEL",
                f"label {label} resolves to a folder",
                f"{raw} is not a folder",
            )
    deep: dict[str, set[str]] = collections.defaultdict(set)
    for _, target in _readme_targets(path, text, text):
        parts = _readme_relative(folder, target)
        if parts and _readme_is_deep(parts):
            deep[parts[0]].add("/".join(parts))
    scoped = [section, *(line for line in visible if line.lstrip().startswith("|"))]
    for chunk in scoped:
        for value in README_NAV_CODE_SPAN.findall(chunk):
            value = value.strip().rstrip("/")
            if not value or " " in value or value.startswith(("/", "-", "~")):
                continue
            candidate = PurePosixPath(posixpath.normpath((folder / value).as_posix()))
            parts = _readme_relative(folder, candidate)
            if tree.kind(candidate) is not None and parts and _readme_is_deep(parts):
                deep[parts[0]].add("/".join(parts))
    for child, targets in sorted(deep.items()):
        if len(targets) > navigation.max_deep_links_per_child:
            report(
                "README-NAV-ENUMERATION",
                f"at most {navigation.max_deep_links_per_child} deep target in {child}/",
                f"{len(targets)} targets: {', '.join(sorted(targets)[:4])}",
            )
    if rule.complete:
        reached = {
            parts[0]
            for _, target in section_targets
            if (parts := _readme_relative(folder, target))
        }
        for child, kind in sorted(tree.children(folder, navigation.placeholders).items()):
            if (kind == "folder" or child.endswith(".md")) and child not in reached:
                report(
                    "README-NAV-COMPLETE",
                    f"{rule.section} reaches {child}",
                    f"{child} is unreachable",
                )
    for header in _readme_table_headers(section):
        banned = sorted(header & navigation.forbidden_index_columns)
        if banned:
            report(
                "README-NAV-COPY",
                "no copied status or date columns",
                ", ".join(banned),
            )
    return found


def readme_navigation_diagnostics(
    navigation: Any,
    readmes: Mapping[PurePosixPath, ReadmeSource],
    tree: TrackedTree,
) -> list[Diagnostic]:
    """SPEC-0091: each README lists only its direct children."""

    diagnostics: list[Diagnostic] = []
    for path, source in sorted(readmes.items(), key=lambda item: item[0].as_posix()):
        rule = navigation.profiles.get(source.profile_id)
        if rule is None:
            continue
        found = _readme_findings(path, source, rule, navigation, tree)
        if path in navigation.pending_paths:
            if not found:
                diagnostics.append(
                    _diag(
                        "README-NAV-PENDING",
                        path,
                        source.profile_id,
                        "a pending README that still violates the contract",
                        "it passes; remove it from pending_paths",
                    )
                )
            continue
        diagnostics.extend(found)
    for pending in sorted(navigation.pending_paths, key=PurePosixPath.as_posix):
        if tree.kind(pending) is None:
            diagnostics.append(
                _diag(
                    "README-NAV-PENDING",
                    pending,
                    "",
                    "a tracked README",
                    "pending path is not tracked",
                )
            )
    return diagnostics


def _readme_navigation_diagnostics(context: Context) -> list[Diagnostic]:
    registry = context.document_registry or load_registry(context.root)
    navigation = getattr(registry, "readme_navigation", None)
    if navigation is None:
        return []
    readmes = {
        path: ReadmeSource(context.profiles[path].profile_id, context.texts[path])
        for path in context.paths
        if path.name == "README.md" and path in context.texts
    }
    modes = {
        entry.path: entry.mode
        for entry in _parse_ls_files_stage_z(
            _run_git(context.root, ("ls-files", "--stage", "-z"))
        )
        if entry.stage == 0
    }
    return readme_navigation_diagnostics(navigation, readmes, TrackedTree.from_modes(modes))
```

  Wire it: add `diagnostics.extend(_readme_navigation_diagnostics(context))`
  after `_collection_index_diagnostics(context)` in the strict diagnostics
  function, and `+ _readme_navigation_diagnostics(context)` after
  `_collection_index_diagnostics(context)` in the inventory branch. Confirm the
  names `load_registry`, `_parse_ls_files_stage_z`, `_run_git`, `posixpath`,
  and `collections` are already imported in the module; import any that are
  not.

- [ ] **Step 6: Run to verify the unit tests pass.** Run
  `python3 -m unittest tests.test_readme_navigation`; expected: `OK`.

- [ ] **Step 7: Register the contract.** Add the Spec's `readme_navigation`
  object to `registry.json` with an empty `pending_paths`, run
  `python3 scripts/validate-links-and-owners.py --root . --mode strict`, and
  collect every README that reports a `README-NAV-*` code. Put that sorted
  list in `pending_paths`, including `docs/98.archive/README.md`. Re-run the
  link gate; expected: no `README-NAV-*` diagnostic.

- [ ] **Step 8: Activate and hand off README ownership.** Set this package's
  Spec and Plan to `active` and its Task to `in-progress` with minor version
  bumps. In `docs/03.specs/0008-current-local-gitops-platform/spec.md`, change
  the ownership sentence to name `gitops/`, `infrastructure/`, and `scripts/`
  only, and append `README navigation is owned by
  [SPEC-0091](../0091-readme-navigation-contract/spec.md).`; bump its version.
  Update the Stage 03 index row for 0091 to `Active`.

- [ ] **Step 9: Run** `python3 scripts/validate-document-contract-registry.py --root . --mode strict`,
  `python3 -m unittest tests.test_readme_navigation tests.test_archive_registry_contract`,
  and `python3 scripts/qa.py staged`; expected: PASS.

- [ ] **Step 10: Commit** `feat(validation): add the README navigation contract and validator`.

### WP-003: Stage 03 index

**Files:** `docs/03.specs/README.md`; `scripts/validate-links-and-owners.py`
(delete `DeclaredIndex`, `DECLARED_INDEXES`, `_tree_targets`, `_table_rows`,
`_index_diagnostics`, and both call sites); `tests/test_common_agents_archive_routes.py`
(class `SpecIndexStatusTest`); `tests/test_archive_validation.py`
(`test_declared_spec_index_accepts_only_four_digit_work_units`);
`docs/99.templates/registry.json` (`pending_paths`).

- [ ] **Step 1: Replace the pinned tests first.** Rewrite `SpecIndexStatusTest`
  as `SpecIndexNavigationTest`, which feeds the old fixture text (tree with
  `spec.md`, row linking `./0999-status-fixture/spec.md` with a status cell)
  to `readme_navigation_diagnostics` with the repository contract and asserts
  `{"README-NAV-DEPTH", "README-NAV-TREE", "README-NAV-COPY"}` is a subset of
  the codes; and feeds a fixed text with `[0999-status-fixture/](./0999-status-fixture/)`
  and a purpose column and asserts no code. Change the four-digit test to
  assert that the navigation contract, not `DECLARED_INDEXES`, governs the
  Stage 03 index: `README-NAV-COMPLETE` fires when a four-digit package folder
  is unlisted.
- [ ] **Step 2: Rewrite the README.** In `## Document Index` keep one tree of
  package folders (depth 1, no `spec.md`/`plan.md`/`tasks/`) and one table
  `| Package | Purpose |` whose first cell is `[<package>/](./<package>/)`.
  Remove the status, currency, date, and approval-quote columns; the purpose
  is one Korean sentence. Remove the deep archive task link and replace it
  with a link to `../98.archive/README.md`. Remove the path from `pending_paths`.
- [ ] **Step 3: Delete** the `INDEX-*` machinery listed above.
- [ ] **Step 4: Run** `python3 -m unittest tests.test_common_agents_archive_routes tests.test_archive_validation tests.test_readme_navigation`
  and `python3 scripts/qa.py staged`; expected: PASS.
- [ ] **Step 5: Commit** `refactor(docs): route the Stage 03 index to package folders`.

### WP-004: Stage 90 references

**Files:** `docs/90.references/README.md`, `docs/90.references/research/README.md`,
the two research pack READMEs if reported; `scripts/validate-links-and-owners.py`
(delete `CollectionIndex`, `COLLECTION_INDEXES`, `_collection_table_targets`,
`_collection_index_diagnostics`, and both call sites); tests that assert
`COLLECTION-INDEX-*` (find with `grep -rn "COLLECTION-INDEX" tests`);
`pending_paths`.

- [ ] Rewrite each asserting test to assert `README-NAV-COMPLETE` for an
  unlisted pack member in a pack README, and `README-NAV-DEPTH` for a
  collection README that links pack members.
- [ ] Rewrite `research/README.md` to link each pack folder or its
  `README.md` only; the pack READMEs keep their own `Report Index` of direct
  members. Remove the stage README's nested tree. Remove the paths from
  `pending_paths`.
- [ ] Delete the collection index machinery; run the focused tests and
  `python3 scripts/qa.py staged`; expected: PASS.
- [ ] Commit `refactor(docs): route Stage 90 collections to their packs`.

### WP-005: Knowledge index

**Files:** `.agents/knowledge/README.md` if reported;
`scripts/validate-knowledge-surface.py` (`ITEM_INDEX_HEADING`, `_check_index`,
its call); `tests/test_validate_knowledge_surface.py`
(`test_unindexed_document_fails` and its fixture).

- [ ] Rewrite `test_unindexed_document_fails` to call
  `readme_navigation_diagnostics` with a `.agents/knowledge` fixture and assert
  `README-NAV-COMPLETE` (the collection-index profile is complete).
- [ ] Delete `_check_index` and its call; keep every other knowledge rule.
- [ ] Run `python3 -m unittest tests.test_validate_knowledge_surface tests.test_readme_navigation`
  and `python3 scripts/qa.py staged`; expected: PASS.
- [ ] Commit `refactor(validation): let the navigation contract own the knowledge index`.

### WP-006: Stage 05 operations

**Files:** `docs/05.operations/README.md` and its `guides/`, `policies/`,
`runbooks/`, `incidents/` READMEs; `scripts/validation/repository/quality.py`
(the Korean document-index block that requires a four-column header of
document, description, status, and last-updated, with status/date parity); `pending_paths`.

- [ ] Rewrite each collection README to one two-column table (document and
  description, Korean headers) under the existing Korean document-index H3 in
  `## Item Index`, drop the duplicate tree, and keep the
  Operations Routing Matrix. Rewrite the stage README's deep links (policy
  0001 and runbook 0011) to the owning collection folders.
- [ ] Change the `quality.py` block to require the two-column document and description header,
  keep the missing-document, missing-target, and duplicate checks, and delete
  the status and `updated` parity checks. Update the matching assertion in
  `tests/test_repository_quality_rules.py` if one pins the old header.
- [ ] Remove the paths from `pending_paths`; run `python3 scripts/qa.py staged`;
  expected: PASS.
- [ ] Commit `refactor(docs): stop copying status and dates into operations indexes`.

### WP-007: Matrices follow their folders

**Files:** create `gitops/platform/README.md` and
`infrastructure/verify/README.md` (profile `common/readme-implementation`);
modify `gitops/README.md`, `infrastructure/README.md`,
`docs/99.templates/registry.json` (the `common/readme-implementation`
`path_pattern` gains `gitops/platform/README.md` and
`infrastructure/verify/README.md` and loses `traefik/README.md`),
`scripts/validation/repository/quality.py` (Service Coverage Matrix block
around lines 2728 to 2820 and Infrastructure Test Inventory block around line
4296), `pending_paths`.

- [ ] Move the `platform/*` rows of `Service Coverage Matrix` into
  `gitops/platform/README.md` under `## Structure` as `### Platform Coverage
  Matrix`, with the area cell written relative to that folder (for example
  `` `argocd` ``). Keep `clusters/local` and `apps/root` rows in
  `gitops/README.md`, and drop the `workloads/*` rows, which
  `gitops/workloads/README.md`'s `Workload Coverage Matrix` already owns.
- [ ] Replace the Service Coverage block with one function called twice:

```python
def check_area_matrix(
    readme_path: Path, heading: str, base: Path, expected_areas: list[str]
) -> None:
    label = f"{rel(readme_path)} {heading}"
    rows = markdown_table_after_heading(
        read_text(readme_path), profiled_readme_table_headings(heading)
    )
    if len(rows) < 2:
        fail(f"{label} must contain a header and service rows")
        return
    if rows[0] != expected_gitops_service_header:
        fail(f"{label} header must be: " + " | ".join(expected_gitops_service_header))
        return
    indexed: list[str] = []
    for row_number, row in enumerate(rows[1:], start=1):
        if len(row) != len(expected_gitops_service_header):
            fail(f"{label} row {row_number} must have {len(expected_gitops_service_header)} columns")
            continue
        area_cell, purpose, lifecycle, dependencies, validation = row
        match = re.fullmatch(r"`([^`]+)`", area_cell)
        if not match:
            fail(f"{label} row {row_number} must start with a backticked area path")
            continue
        area = match.group(1)
        if area in indexed:
            fail(f"{label} duplicates area: {area}")
        indexed.append(area)
        if not (base / area).is_dir():
            fail(f"{label} references missing directory: {rel(base / area)}")
        for name, value in [
            ("Purpose and owner", purpose),
            ("Lifecycle and config", lifecycle),
            ("Dependencies, routes, secrets", dependencies),
            ("Validation and operations", validation),
        ]:
            if not value:
                fail(f"{label} row {row_number} has empty {name}")
        if "owned by" not in purpose:
            fail(f"{label} row {row_number} must name ownership")
        if not any(
            marker in validation for marker in ["`bash ", "Validate", "validate-", "verify-"]
        ):
            fail(f"{label} row {row_number} must cite a validation command")
    if indexed != expected_areas:
        fail(f"{label} area order must match actual directories: " + ", ".join(expected_areas))


check_area_matrix(
    gitops_readme_path, "Service Coverage Matrix", gitops_dir, ["clusters/local", "apps/root"]
)
check_area_matrix(
    gitops_dir / "platform/README.md",
    "Platform Coverage Matrix",
    gitops_dir / "platform",
    sorted(path.name for path in (gitops_dir / "platform").iterdir() if path.is_dir()),
)
```

  Add `"Platform Coverage Matrix"` to the titles in
  `tests/test_repository_quality_rules.py::test_readme_tables_retain_visible_headings_and_unique_diagnostics`.
- [ ] Move `Infrastructure Test Inventory` to `infrastructure/verify/README.md`
  under `## Structure`, and change its reader to
  `read_text(infrastructure_dir / "verify/README.md")` with messages naming
  that path. Replace the section in `infrastructure/README.md` with one link
  to `./verify/`.
- [ ] Flatten both READMEs' `## Structure` trees to depth one. Run the
  navigation gate; if a gitops matrix still reports `README-NAV-ENUMERATION`
  because a Vault path equals a folder name, write that cell as plain text
  instead of a code span and record it in the Task.
- [ ] Remove the paths from `pending_paths`; run `python3 scripts/qa.py staged`;
  expected: PASS. Commit `refactor(gitops): keep each coverage matrix in the folder it enumerates`.

### WP-008: Remaining READMEs

Every README still in `pending_paths` except `docs/98.archive/README.md`. One
implementer subagent per area, disjoint files, sequential integration:

| Area | READMEs |
| --- | --- |
| Root and docs hub | `README.md`, `docs/README.md` |
| Stages 01, 02, 99 | `docs/01.requirements/README.md`, `docs/02.architecture/**/README.md`, `docs/99.templates/**/README.md` |
| Code and tools | `examples/**/README.md`, `policy/README.md`, `secrets/README.md`, `scripts/README.md`, `tests/README.md`, `evals/README.md` |
| Agent surfaces | `.agents/README.md`, `.claude/README.md`, `.codex/README.md` |

Each implementer receives: the Spec's Contracts section; the exact file list;
the rule "keep every required H2, keep facts, delete duplicate lists, link
child folders or their README, keep one deep citation per child at most, no
status or date columns"; the language rule of the Global Constraints; the
forbidden paths (anything outside the file list); and the check command
`python3 scripts/validate-links-and-owners.py --root . --mode strict` plus
`python3 scripts/validate-markdown-profiles.py --root . --mode strict`. The
implementer does not commit. The integrator reviews spec fit and quality,
removes the area's paths from `pending_paths`, runs `python3 scripts/qa.py staged`,
and commits `docs(readme): route <area> READMEs to direct children`. Stale
facts found on the way (the `evals/` claim in the root README, missing files
in `examples/azure/*` trees) are corrected in the same area commit.

### WP-009: Template guidance

**Files:** `docs/99.templates/templates/common/readme-*.template.md`,
`docs/99.templates/templates/references/*-pack*.template.md`.

- [ ] Replace each navigation section's author prompt with guidance that
  states the contract: a router links its direct child folders or their
  README; a collection lists its direct members once; no copied status, date,
  or count; a matrix belongs to the folder it enumerates. Keep English, which
  the language package changes.
- [ ] Run `python3 scripts/validate-markdown-profiles.py --root . --mode strict`
  and `python3 scripts/qa.py staged`; expected: PASS. Commit
  `docs(templates): state the README navigation contract`.

### WP-010: Evidence and closure

- [ ] Confirm `pending_paths` is `["docs/98.archive/README.md"]`.
- [ ] Run `timeout 3500 python3 scripts/qa.py full` and record every gate;
  separate environment failures (no Gitleaks, `pre-commit` off the trusted
  `PATH`, the two host-only unit tests) from new failures.
- [ ] Record commits, results, deferrals, and residual risk in the Task; set
  Spec, Plan, and Task to `done`; update the Stage 03 index row. Commit
  `docs(specs): record SPEC-0091 evidence and close the package`.

## Verification Plan

Each work package runs its focused tests, the gate it touches, and
`python3 scripts/qa.py staged`. WP-010 runs `python3 scripts/qa.py full`.
Hosted `ci-summary` is not observed.

### Review Focus

- A README whose navigation table is an H3 inside the navigation H2 (Stage 05
  uses a Korean document-index H3 inside `## Item Index`): the section reader takes the
  whole H2, so the H3 table is inside it. Pinned by WP-006's staged run.
- Reference-style links defined outside the navigation section: the section's
  links resolve against the whole text's definitions. Pinned by the `[b]`
  reference in `GOOD_ROUTER`.
- A code span that names a Vault path equal to a folder, such as
  `platform/argocd`: counted as a path. Handled in WP-007 and recorded.
- The repository root README, whose folder is `.`: `_readme_relative` returns
  the target's own parts. Pinned by the whole-corpus link gate in WP-008.
- A staged run whose tracked tree differs from the worktree: the tree comes
  from `git ls-files --stage`, the same index staged QA reads.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Removing a list check loses orphan detection | `README-NAV-COMPLETE` covers every complete profile, and each replaced test asserts it |
| `pending_paths` becomes a permanent exception list | `README-NAV-PENDING` fails a pending README that already passes, and WP-010 requires only the Stage 98 README |
| A matrix move weakens a quality check | The moved check keeps every assertion and only changes its source path |
| Subagents edit the same file | Areas are disjoint and only the integrator commits |

## Completion Criteria

WP-001 to WP-010 meet their exit evidence, VAL-RNC-001 to VAL-RNC-007 hold,
and full QA ran on the final tree with only known environment failures.

## Traceability

[Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-RNC-001](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-converge-readme-navigation.md) |
| [VAL-RNC-002](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-converge-readme-navigation.md) |
| [VAL-RNC-003](spec.md#success-criteria--verification-plan) | WP-003 to WP-006 | [tsk-0001](tasks/tsk-0001-converge-readme-navigation.md) |
| [VAL-RNC-004](spec.md#success-criteria--verification-plan) | WP-008 | [tsk-0001](tasks/tsk-0001-converge-readme-navigation.md) |
| [VAL-RNC-005](spec.md#success-criteria--verification-plan) | WP-007 | [tsk-0001](tasks/tsk-0001-converge-readme-navigation.md) |
| [VAL-RNC-006](spec.md#success-criteria--verification-plan) | WP-009 | [tsk-0001](tasks/tsk-0001-converge-readme-navigation.md) |
| [VAL-RNC-007](spec.md#success-criteria--verification-plan) | WP-010 | [tsk-0001](tasks/tsk-0001-converge-readme-navigation.md) |
