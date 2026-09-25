---
title: "Archive Ledger Split Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-09-26"
layer: "specs"
artifact_id: "SPEC-0092-PLAN-0001"
---

# Archive Ledger Split Implementation Plan

## Global Constraints

- Goal: the archive tables live in `docs/98.archive/ledger.md`, the README is
  navigation only, and every table reader follows one registry path.
- Spec: [SPEC-0092](spec.md); decision: ADR-0047. Every work package
  implicitly includes these constraints.
- The request owner approved the design on 2026-09-26 and the Spec on
  2026-09-26. Work continues on the local branch `readme-navigation-contract`
  after SPEC-0091. Push, pull request, merge, and live actions are not
  authorized.
- Each commit runs `python3 scripts/qa.py staged` over its exact index and
  `git diff --check`. No hook bypass, no `--no-verify`, no weakened assertion.
- Exact values: ledger path `docs/98.archive/ledger.md`; profile
  `archive/ledger` (family `archive`, mode `router`, lifecycle `null`);
  ledger H2s `Overview`, `Record Manifest`, `Retention Ledger`,
  `Related Documents`; new codes `ARCHIVE-LEDGER-MISSING`,
  `ARCHIVE-LEDGER-RESIDUE`, `REGISTRY_ARCHIVE_LEDGER`.
- `ARCHIVE_INDEX` keeps meaning the README identity everywhere it names a
  replacement, a lifecycle default, or a citation target. Only table reads move.
- No byte of `docs/98.archive/{completed,retired,superseded,migrations}/**`
  changes.
- Run the whole unit suite, not only focused tests, before each code commit:
  SPEC-0091 showed that fixture registries and closed key sets break outside
  the focused modules.

## Overview

WP-002 adds the mechanism with the ledger path still equal to the README, so
behavior is unchanged and every reader is already routed through the registry.
WP-003 creates the ledger, flips the registry path, moves the tables, and
rewrites the README in one commit. WP-004 updates the instructions that name
the old location, and WP-005 closes the package.

## Context

Three scripts copy `docs/98.archive/README.md` as `ARCHIVE_INDEX`
(`scripts/archive_validation.py:171`, `scripts/archive_dispositions.py:65`,
`scripts/archive_cutover.py:178`) and one as `ARCHIVE_INDEX_PATH`
(`scripts/validate-links-and-owners.py:137`). Table reads happen at
`archive_validation._read_repository_index` (manifest, catalog, and assessment
text), `archive_cutover.py:573` and `:1411`, and
`validate-links-and-owners.py:2810`. Every other use of those constants is the
index identity and stays. The registry pins both `archive_citation.index` and
`archive_assessment.index` to the README with a schema `const`.

## Goals & In-Scope

The registry field, schema, loader, self-check, and path helper; the reader
switch; the residue and missing-ledger checks; the ledger profile, template,
and file; the README rewrite; `pending_paths`; the author instructions; and
ADR-0047 acceptance.

## Non-Goals & Out-of-Scope

Table columns, rows, and parsers; sealed, retained, or frozen files; the
language contract; the decisions README status table.

## Work Breakdown

| ID | Work package | Criteria |
| --- | --- | --- |
| WP-001 | Propose the package | VAL-ALS-007 |
| WP-002 | Registry ledger path and reader routing | VAL-ALS-001, VAL-ALS-003, VAL-ALS-004 |
| WP-003 | Move the tables | VAL-ALS-002, VAL-ALS-005, VAL-ALS-006 |
| WP-004 | Author instructions | VAL-ALS-003 |
| WP-005 | Evidence and closure | VAL-ALS-007 |

### WP-001: Propose the package

**Files:** this package, ADR-0047, `docs/03.specs/README.md`,
`docs/02.architecture/decisions/README.md`, REQ-0003.

- [ ] Add the Stage 03 index row for `0092-archive-ledger-split/` and the
  ADR-0047 row in the decisions README Item Index.
- [ ] Add to REQ-0003, after the SPEC-0091 sentence: "Moving the archive
  tables out of the Stage 98 README into one ledger is owned by
  SPEC-0092 (linked to this Spec)."
- [ ] Run `python3 scripts/qa.py staged`; expected PASS. Commit
  `docs(specs): propose SPEC-0092 for the archive ledger split`.

### WP-002: Registry ledger path and reader routing

**Files:** `docs/99.templates/registry.json`,
`docs/99.templates/contracts/document-profile.schema.json`,
`scripts/document_contracts.py`, `scripts/archive_dispositions.py`,
`scripts/archive_validation.py`, `scripts/archive_cutover.py`,
`scripts/validate-links-and-owners.py`, `tests/test_archive_ledger.py`
(new), and every test the whole suite shows reading a copied path.

**Interfaces produced:**

- `ArchiveCitation.ledger: PurePosixPath` (new dataclass field).
- `archive_dispositions.ARCHIVE_LEDGER_DEFAULT = ARCHIVE_ROOT / "ledger.md"`.
- `archive_dispositions.archive_ledger_path(registry: Registry | None) -> PurePosixPath`:
  `registry.archive_citation.ledger` when present, otherwise
  `ARCHIVE_LEDGER_DEFAULT`.
- `archive_dispositions.ledger_residue_diagnostics(registry, readme_text: str) -> list[tuple[str, str]]`:
  empty when the ledger path equals the citation index; otherwise one
  `("ARCHIVE-LEDGER-RESIDUE", <README path>)` for each of the manifest marker
  regex, `_INDEX_HEADER`, `CATALOG_HEADER`, or `### <assessment heading>`
  found in `readme_text`.
- `document_contracts._archive_ledger_registry_diagnostics(raw_registry) -> list[Diagnostic]`:
  `REGISTRY_ARCHIVE_LEDGER` when `archive_citation` is present and its
  `ledger` differs from `archive_assessment.index`.

Steps:

- [ ] Write `tests/test_archive_ledger.py` first with these cases, and run it
  to see each fail:
  - the loader exposes `archive_citation.ledger`;
  - `archive_ledger_path` returns the registry value and the default;
  - `_archive_ledger_registry_diagnostics` passes when equal and fails when
    the two paths differ;
  - `ledger_residue_diagnostics` returns nothing while ledger equals index,
    and once they differ reports each of the four residues from a synthetic
    README text and nothing from a navigation-only README;
  - `archive_target_kind(registry, ledger)` is `("index", None)`;
  - the repository archive validation reports `ARCHIVE-LEDGER-MISSING` in a
    synthetic root whose registry names an absent ledger.
- [ ] Schema: `archive_citation` gains required `ledger` with
  `{"type": "string", "pattern": "^docs/98\\.archive/[a-z0-9-]+\\.md$"}`;
  `archive_assessment.index` loses its `const` and takes the same pattern.
  Registry: add `"ledger": "docs/98.archive/README.md"` to `archive_citation`
  (equal to the index for now) and leave `archive_assessment.index` unchanged.
- [ ] Loader and self-check in `scripts/document_contracts.py`, wired where
  `_readme_navigation_registry_diagnostics` is wired.
- [ ] Route reads: `_read_repository_index(root)` takes the ledger path from
  `archive_ledger_path(load_registry(root))` or the registry already in scope;
  `archive_cutover.py:573` and `:1411` and `validate-links-and-owners.py:2810`
  read `archive_ledger_path(...)`. Replace `archive_cutover.ARCHIVE_INDEX` and
  `validate-links-and-owners.ARCHIVE_INDEX_PATH` with imports from
  `archive_dispositions`, keeping their identity uses. Emit
  `ARCHIVE-LEDGER-MISSING` when the ledger path is not a regular file, and
  `ledger_residue_diagnostics` over the README text, from
  `validate_repository_archive`.
- [ ] Point the tests that read the live README as a table source
  (`tests/test_archive_registry_contract.py:226`,
  `tests/test_archive_catalog_reverification.py:178`) at
  `archive_ledger_path(REGISTRY)`. Fixture registries that pop or rebuild
  archive keys keep working because the new field travels with
  `archive_citation`; the frozen-generation fixture already removes it.
- [ ] Run the focused tests, then
  `timeout 3000 python3 -m unittest discover -s tests -t .`; expected: only the
  known environment failures. Run `python3 scripts/qa.py staged`. Commit
  `feat(archive): route archive table reads through one registry ledger path`.

### WP-003: Move the tables

**Files:** `docs/98.archive/ledger.md` (new), `docs/98.archive/README.md`,
`docs/99.templates/registry.json`,
`docs/99.templates/templates/archive/ledger.template.md` (new), the
`docs/99.templates/templates/README.md` archive row, and tests the whole suite
shows pinning the README tables.

- [ ] Record the before state: with a scratch script (session scratch, not
  committed) print `_parse_repository_index` rows, `parse_catalog` rows,
  `parse_assessment` rows, and the marker counts from the README; save the
  output.
- [ ] Add the profile `archive/ledger`: family `archive`, mode `router`,
  `path_pattern` `^docs/98\.archive/ledger\.md$`, `artifact_id_pattern`
  `null`, template `docs/99.templates/templates/archive/ledger.template.md`,
  frontmatter as `common/readme-stage-index` with constant type
  `archive/ledger`, required sections `Overview`, `Record Manifest`,
  `Retention Ledger`, `Related Documents`, lifecycle `null`, placeholder
  policy `forbidden`. Write the template with those headings and English
  author prompts.
- [ ] Create `ledger.md`: frontmatter; `## Overview` (one paragraph: the single
  archive index that validators read, and ADR-0047); `## Record Manifest` with
  the `archive-manifest:v1` marker line and the manifest table copied
  byte-for-byte, then the migration-record and Spec 0052 pointer paragraphs
  rewritten in English; `## Retention Ledger` with `### Retention Catalog` and
  `### Retention Assessment` copied byte-for-byte including their lead
  paragraphs; `## Related Documents` linking `README.md` and ADR-0047.
- [ ] Rewrite the README: remove the marker, the three tables, the totals
  sentence, and the pointer paragraphs; `## Document Index` becomes a
  two-column table linking `completed/`, `migrations/`, `retired/`,
  `superseded/`, and `ledger.md`; keep `## Document Index` and every other
  required H2. Bump its version and date.
- [ ] Registry: `archive_citation.ledger` and `archive_assessment.index` become
  `docs/98.archive/ledger.md`; remove `docs/98.archive/README.md` from
  `readme_navigation.pending_paths`, leaving `[]`.
- [ ] Record the after state with the same script over the ledger and compare;
  expected identical. Stop and report on any difference.
- [ ] `git diff --stat HEAD -- docs/98.archive/completed docs/98.archive/retired docs/98.archive/superseded docs/98.archive/migrations`
  prints nothing.
- [ ] Run the focused tests, the whole unit suite, `python3 scripts/archive_cutover.py --root .`
  (expect only `ARCHIVE-SECRET-CLASSIFIER-UNAVAILABLE`), and staged QA. Commit
  `refactor(archive): move the archive tables into the ledger`.

### WP-004: Author instructions

**Files:** `.agents/skills/archive-cutover/SKILL.md`,
`.agents/governance/document-lifecycle.md`,
`.agents/governance/document-authoring.md`, and any file that
`grep -rn "Stage 98 index\|Retention Catalog row" .agents docs/99.templates docs/05.operations`
shows instructing an author to edit README tables.

- [ ] Replace the location with the ledger (`docs/98.archive/ledger.md`),
  keeping English in `.agents`.
- [ ] Update SPEC-0091's Task deferral line to name SPEC-0092 as resolving it.
- [ ] Staged QA; commit `docs(governance): point retention authors at the archive ledger`.

### WP-005: Evidence and closure

- [ ] Run `timeout 3500 python3 scripts/qa.py full` and record every gate with
  the known environment failures separated.
- [ ] Set ADR-0047 to `accepted` and the Spec, Plan, and Task to `done`;
  record the before-and-after comparison, commits, and residual risk. Commit
  `docs(specs): record SPEC-0092 evidence and close the package`.

## Verification Plan

Each code package runs its focused tests, the whole unit suite, and staged QA.
WP-005 runs full QA. Hosted `ci-summary` is not observed.

### Review Focus

- A reader still opening the README for tables after WP-003: the residue check
  fails on the README, and the before-and-after comparison fails on an empty
  parse.
- A synthetic test root that writes tables into its README while its registry
  names a ledger: `ARCHIVE-LEDGER-RESIDUE`; such fixtures write the ledger.
- A sealed record whose replacement is `docs/98.archive/README.md#document-index`:
  the identity uses of `ARCHIVE_INDEX` stay, and the heading stays.
- A frozen body linking the README anchor: resolved by the kept heading.
- A link to the ledger from a current document: admitted as the index kind.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| A table read left on the README path | Residue check plus the recorded comparison |
| An identity use moved to the ledger by mistake | Only the four listed read sites change; review against the Context list |
| Profile inventory tests pin a profile count | The whole suite runs before each commit |
| The Git budget test shifts with an extra read | Measure; change the budget only with the measured value and a comment |

## Completion Criteria

VAL-ALS-001 through VAL-ALS-007 hold, full QA shows only the known
environment failures, and the Task records the evidence.

## Traceability

The [Spec](spec.md) owns the contract; the
[Task](tasks/tsk-0001-split-archive-ledger.md) owns the evidence.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-ALS-001](spec.md#success-criteria--verification-plan) | WP-002, WP-003 | [tsk-0001](tasks/tsk-0001-split-archive-ledger.md) |
| [VAL-ALS-002](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0001](tasks/tsk-0001-split-archive-ledger.md) |
| [VAL-ALS-003](spec.md#success-criteria--verification-plan) | WP-002, WP-004 | [tsk-0001](tasks/tsk-0001-split-archive-ledger.md) |
| [VAL-ALS-004](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-split-archive-ledger.md) |
| [VAL-ALS-005](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0001](tasks/tsk-0001-split-archive-ledger.md) |
| [VAL-ALS-006](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0001](tasks/tsk-0001-split-archive-ledger.md) |
| [VAL-ALS-007](spec.md#success-criteria--verification-plan) | WP-001 through WP-005 | [tsk-0001](tasks/tsk-0001-split-archive-ledger.md) |
