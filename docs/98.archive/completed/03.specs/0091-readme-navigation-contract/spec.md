---
title: "README Navigation Contract Technical Specification"
version: "0.4.0"
type: "sdlc/spec"
status: "done"
owner: "platform"
updated: "2026-09-26"
layer: "specs"
artifact_id: "SPEC-0091"
---

# README Navigation Contract Technical Specification (Spec)

## Overview

README files in this workspace list the contents of their subfolders. The
Stage 03 index names every package's `spec.md`, `plan.md`, and `tasks/` and
copies each package status; the research collection lists every pack member;
collection READMEs repeat one list as a tree and as a table; implementation
READMEs carry matrices of paths two levels deep. Several copies are already
stale. The root cause is the validators: `DECLARED_INDEXES`,
`COLLECTION_INDEXES`, the knowledge `Item Index` check, and the Stage 05
Korean document-index check each require an exhaustive child list with copied status
and dates, and the Stage 99 registry has no field that states what a README
may list.

The request owner approved on 2026-09-25 a three-part program: this README
navigation contract first, then moving the machine-read archive ledger out of
the Stage 98 README, then a document language contract. This Spec owns the
first part. On 2026-09-26 the request owner withdrew the second part: the
archive keeps its machine tables in the Stage 98 README, which this contract
exempts.

## Strategic Boundaries & Non-goals

In scope: one registry contract for README navigation, its schema, loader, and
self-consistency check; one navigation validator that replaces the four
exhaustive-list checks; every tracked README that the contract finds in
violation; moving path matrices to the README of the folder whose members they
enumerate; the navigation guidance in the `readme-*` templates; and the
README ownership that SPEC-0008 names.

Out of scope: the machine tables in `docs/98.archive/README.md`, which stay
there; the document language contract, including the
English-only rule for `.agents/`, `.claude/`, and `.codex/` and template
language; any retained body, frozen record, or sealed ledger; any lifecycle
state or edge; any live cluster or provider action.

## Contracts

- A README's role comes from its folder's tracked direct children, not from
  its profile name. `README.md` and `.gitkeep` are placeholders. A folder whose
  children are all folders is a router; any other folder is a collection. A
  symlink or submodule is one leaf child and is not followed.
- A README's navigation section is the H2 the registry names for its profile.
  Its local links reach only the README's own folder, a direct child, or a
  direct child's `README.md`. Links outside the folder are not navigation
  depth and stay unrestricted.
- A fenced tree anywhere in a README shows direct children only.
- A link whose label ends in `/` resolves to a folder.
- Across the whole README, at most `max_deep_links_per_child` distinct deep
  targets fall inside one child subtree. Links count everywhere; inline code
  spans that resolve to a tracked path count inside the navigation section and
  inside tables. A child's own `README.md` is not deep.
- When the profile is marked complete, every direct child folder and every
  direct Markdown document is reachable from the navigation section.
- A table in the navigation section has no column the registry forbids, so
  status, dates, and currency are read from each document, not copied.
- A path matrix lives in the README of the folder whose direct members it
  enumerates.
- `pending_paths` names a README whose navigation is not yet checked. It
  starts with every README in violation, shrinks in each area commit, and ends
  empty.
- `exempt_paths` names a README the contract never checks. It holds
  `docs/98.archive/README.md` alone: its record manifest links every frozen
  record, and sealed and frozen proofs read its tables where they are.

## Core Design

The registry gains a top-level `readme_navigation` object, loaded by
`scripts/document_contracts.py` the way `archive_assessment` is. The navigation
validator lives in `scripts/validate-links-and-owners.py`, which already owns
the CommonMark link renderer, and emits `README-NAV-*` diagnostics. Each area
commit rewrites its READMEs, removes them from `pending_paths`, and deletes the
exhaustive-list check it replaces.

## Data Modeling & Storage Strategy

```json
"readme_navigation": {
  "placeholders": ["README.md", ".gitkeep"],
  "forbidden_index_columns": ["Status", "Updated", "Last Updated", "\uc0c1\ud0dc", "\ucd5c\uc885 \uc218\uc815", "\ud604\uc7ac\uc131"],
  "max_deep_links_per_child": 1,
  "profiles": {
    "common/readme-repository": {"section": "Repository Map", "complete": false},
    "common/readme-stage-index": {"section": "Document Index", "complete": true},
    "common/readme-collection-index": {"section": "Item Index", "complete": true},
    "common/readme-implementation": {"section": "Structure", "complete": false},
    "common/readme-audit-pack": {"section": "Report Index", "complete": true},
    "common/readme-data-pack": {"section": "Item Index", "complete": true},
    "common/readme-research-pack": {"section": "Report Index", "complete": true}
  },
  "pending_paths": [],
  "exempt_paths": ["docs/98.archive/README.md"]
}
```

`pending_paths` above is the final state. The registry self-consistency check
requires every named profile to be a `router` profile, its section to be one
of that profile's required H2 headings, the deep-link limit to be at least one,
every pending or exempt path to name a `README.md`, and no path to be both.
The navigation validator, which sees the tracked tree, requires every pending
path to be a tracked README that still violates the contract, so the list
cannot keep an entry that already passes, and every exempt path to be a
tracked README. The Korean column names are machine tokens that existing Korean
indexes use.

## Interfaces & Data Structures

| Code | Failure |
| --- | --- |
| `README-NAV-DEPTH` | A navigation-section link reaches below a direct child |
| `README-NAV-TREE` | A fenced tree nests below the first level |
| `README-NAV-LABEL` | A label ending in `/` resolves to a file |
| `README-NAV-ENUMERATION` | More than the allowed deep targets fall in one child subtree |
| `README-NAV-COMPLETE` | A required direct child is unreachable from the navigation section |
| `README-NAV-COPY` | A navigation table carries a forbidden column |
| `README-NAV-PENDING` | A pending path is untracked or already passes the contract |
| `README-NAV-EXEMPT` | An exempt path is untracked |
| `REGISTRY_README_NAVIGATION` | The registry contract contradicts its own profiles or paths |

Replaced diagnostics: `INDEX-*` and `COLLECTION-INDEX-*` in
`validate-links-and-owners.py`, `KNOWLEDGE-INDEX-MISSING` in
`validate-knowledge-surface.py`, and the Stage 05 Korean document-index checks in
`scripts/validation/repository/quality.py`. New READMEs are limited to
`gitops/platform/README.md` and `infrastructure/verify/README.md`, which
receive the matrices that enumerate their members; the stale
`traefik/README.md` route leaves the registry.

## Edge Cases & Error Handling

An empty folder or one holding only placeholders requires nothing. A mixed
folder is a collection. A README whose profile has no navigation entry, such
as the workspace staging README, is not checked. `README-NAV-ENUMERATION` is a
count of resolvable targets: a plain-text list that neither links nor names a
tracked path in a code span is outside it, and `README-NAV-TREE` and review
cover that case. A code span resolves from the README folder; inside the
navigation section it also resolves from the repository root, while a root
path in a table outside that section cites contract evidence and is not
counted. Code and emphasis markup around a link label or a table header cell
is ignored. A pending README whose profile has no navigation entry fails
`README-NAV-PENDING`.

## Failure Modes & Fallback / Human Escalation

A failing gate stops the commit; no assertion is weakened. A test that pinned
a replaced check is rewritten to assert the new code, not deleted. A README
that cannot meet the contract without a decision outside this Spec stays in
`pending_paths` and is recorded as a named deferral.

## Verification Commands

```bash
python3 -m unittest tests.test_readme_navigation
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/qa.py staged
python3 scripts/qa.py full
git diff --check
```

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-RNC-001 | The registry contract, schema, loader, and self-consistency check exist and reject contradictions | Focused tests and the registry gate |
| VAL-RNC-002 | Each `README-NAV-*` rule passes its allowed fixtures and fails its forbidden ones, including hidden forms in `Related Documents`, HTML, and tables | Focused tests |
| VAL-RNC-003 | The four exhaustive-list checks are removed and their tests assert the replacing codes | Focused tests and review |
| VAL-RNC-004 | Every tracked README passes the contract except the exempt Stage 98 README, and `pending_paths` is empty | Link gate over the whole corpus |
| VAL-RNC-005 | Path matrices live in the README of the folder they enumerate, and their quality checks read the new paths | Repository quality gate |
| VAL-RNC-006 | The `readme-*` templates describe the navigation contract | Profile gate and review |
| VAL-RNC-007 | Each commit passes staged QA and the final tree runs full QA | Staged and full QA |

## Traceability

The [Implementation Plan](plan.md) owns order and risk. The
[navigation Task](tasks/tsk-0001-converge-readme-navigation.md) owns the
evidence.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RNC-001 | Focused tests and the registry gate |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RNC-002 | Focused tests |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RNC-003 | Focused tests and review |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RNC-004 | Link gate over the whole corpus |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RNC-005 | Repository quality gate |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RNC-006 | Profile gate and review |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RNC-007 | Staged and full QA |
