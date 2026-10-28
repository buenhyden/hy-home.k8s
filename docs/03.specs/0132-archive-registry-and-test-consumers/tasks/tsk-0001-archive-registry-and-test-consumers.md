---
title: "Archive Registry and Test Consumers"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0132-TSK-0001"
parent_ids: ["SPEC-0132-PLAN-0001"]
---

# Task: Archive Registry and Test Consumers

## Overview

Move the document consumers of 26 retained Archive units to plain identifiers
and the Git recovery route, and remove the 26 units as `git-history-only`. It
executes [SPEC-0132](../spec.md) through
[WORK-001–004](../plan.md#work-breakdown). This Task is the Decision document
that the 26 Retention Assessment rows name.

## Inputs

- Request: on 2026-10-28 the operator approved the next Archive batch, the
  units whose census consumers were the registry, validators or tests.
- Approval: the operator approved that batch; this Task disposes of exactly
  these 26 units:
  - `superseded/02.architecture/decisions/0013-stage-00-canonical-adapter-model.md`
  - `superseded/02.architecture/decisions/0015-declarative-document-contract-registry.md`
  - `superseded/02.architecture/decisions/0016-program-to-tranche-document-lineage.md`
  - `superseded/02.architecture/decisions/0017-program-follow-up-lineage-semantics.md`
  - `superseded/02.architecture/decisions/0018-full-body-archive-record-and-retention.md`
  - `superseded/02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md`
  - `superseded/02.architecture/decisions/0020-document-lifecycle-program-closure-evidence.md`
  - `superseded/02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md`
  - `superseded/02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md`
  - `superseded/02.architecture/decisions/0023-work-unit-document-taxonomy-and-governance-authority.md`
  - `superseded/02.architecture/decisions/0024-terminal-artifact-identity-and-archive-layout.md`
  - `superseded/02.architecture/decisions/0025-four-digit-document-path-identity.md`
  - `superseded/02.architecture/decisions/0027-pod-security-standards-staged-adoption.md`
  - `superseded/02.architecture/decisions/0034-stage-00-governance-and-unified-quality-gates.md`
  - `superseded/02.architecture/decisions/0035-common-agents-authority-and-native-skill-routing.md`
  - `superseded/02.architecture/decisions/0038-six-disposition-archive-stage.md`
  - `completed/03.specs/0082-unit-archive-retention-contract`
  - `superseded/02.architecture/decisions/0003-eso-vault-k8s-auth.md`
  - `completed/03.specs/0062-workspace-research-full-corpus-reverification`
  - `completed/03.specs/0085-archive-reappraisal-and-document-standards`
  - `completed/03.specs/0091-readme-navigation-contract`
  - `completed/03.specs/0093-document-language-contract`
  - `completed/03.specs/0095-closed-package-retention`
  - `completed/03.specs/0098-claude-search-grant-and-retention`
  - `completed/03.specs/0099-workspace-engineering-research-refresh`
  - `completed/03.specs/0102-agent-contracts-and-skill-ownership`
- Kept: ADR-0032 (frozen migration ledgers resolve a link through it),
  SPEC-0080 (a lifecycle test seeds from its package), SPEC-0103 (a
  link-boundary test reads its Spec), SPEC-0004, SPEC-0005, SPEC-0008 and
  SPEC-0104 (current delivery evidence), SPEC-0054 (78 current links), and
  SPEC-0072, which REQ-0003 names as the trace owner of FR-0011 and acceptance
  criterion 09; this was found while editing its consumers.
- Start: `9bab5067`, branch `docs/archive-batch3`.
- Scope changes after approval, recorded in Spec 0.1.1: SPEC-0072 stays as a
  REQ-0003 trace owner; VAL-RT-002 accepts link-target-only differences for
  the fifteen rebased decisions; and after review the scope adds the two
  README sentences and the lifecycle test that read ADR-0035, which the
  operator approved on 2026-10-28.

### Trial Result

A scratch worktree from main `8d1ddd2b` removed the 34 units other than
SPEC-0104 on 2026-10-28.

| Check | Result | What it showed |
| --- | --- | --- |
| `validate-archive-integrity.py` | PASS | The catalog check skips removed records |
| `validate-document-lifecycle.py --mode strict` | PASS | Removal rows are admitted |
| `validate-document-contract-registry.py --mode strict` | PASS | The rebased-path list is classified by path |
| `validate-links-and-owners.py --mode strict` | 272 failures | Current documents link to SPEC-0004, 0005, 0008, 0054, 0062, 0072, 0080, 0082, 0085, 0091, 0093, 0095, 0098, 0102 and 0103; three frozen migration ledgers resolve a link through ADR-0032 |
| Test modules naming a unit | 3 modules failed | `test_task_acceptance_contract` and `test_archive_disposition_lifecycle` read SPEC-0080; `test_documentation_link_boundary` reads SPEC-0103; review later found that `test_archive_disposition_lifecycle` also reads ADR-0035, masked here by the earlier SPEC-0080 error |

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RT-001](../spec.md#success-criteria--verification-plan) | Move the consumers to identifiers and the recovery route | platform | in-progress | PASS | EVD-008 closes EVD-001, EVD-006 |
| WORK-002 | [VAL-RT-002](../spec.md#success-criteria--verification-plan) | Isolated recovery of the twenty-six units | platform | in-progress | PASS | EVD-005, EVD-009 close EVD-002, EVD-007 |
| WORK-003 | [VAL-RT-003](../spec.md#success-criteria--verification-plan) | Remove the twenty-six units and add their assessment rows | platform | in-progress | PASS | EVD-010 closes EVD-003 |
| WORK-004 | [VAL-RT-004](../spec.md#success-criteria--verification-plan) | Independent review and hosted checks | platform | in-progress | PASS | EVD-011 closes EVD-004 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-RT-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Consumer validation | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-RT-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Isolated recovery | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-RT-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Canonical staged QA | Exact disposition index | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-RT-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Review and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-RT-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Isolated recovery | Base `9378b5c5`: per unit, `git rev-parse` of the current object against the envelope object, then `git archive` of the envelope into a scratch directory; for unequal blobs, a comparison with every Markdown link target masked | PASS | 11 objects equal; the 15 rebased decisions differ only in link targets; 26/26 restored, 63 files, matching the current file counts | yes | EVD-002 |
| EVD-006 | [VAL-RT-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Consumer validation | PR #188 independent review of `fe3bd418` | FAIL | `test_archive_disposition_lifecycle` read ADR-0035 from the working tree (46 errors); `docs/README.md` and `docs/02.architecture/README.md` still said every superseded ADR stays in `superseded/`; ADR-0047 named SPEC-0102 as a future owner | yes | none |
| EVD-007 | [VAL-RT-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Isolated recovery | PR #188 independent review of `fe3bd418` | FAIL | EVD-005 counted 63 restored files; the envelopes and the removed trees hold 64 | yes | none |
| EVD-008 | [VAL-RT-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Consumer validation | Removal commit `fe3bd418`: `validate-archive-integrity.py`, `validate-document-lifecycle.py --mode strict`, `validate-document-contract-registry.py --mode strict` and `validate-links-and-owners.py --mode strict`; then 17 test modules that name a unit, run on that tree with the test change later committed as `c7374cce`; PR #188 re-review of `c7374cce` | PASS | All four validators exited 0, links in 454 seconds; 482 tests ran OK in 1169 seconds; `test_archive_disposition_lifecycle` ran 46 OK after its change and 46 errors before it; the reviewer found no other test that reads a removed unit and confirmed the README and ADR-0047 corrections | yes | EVD-001, EVD-006 |
| EVD-009 | [VAL-RT-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Isolated recovery | PR #188 re-review of `c7374cce`, with the per-unit counts of EVD-005 | PASS | The 26 envelopes restore 64 files, matching the 64 removed; 11 objects are equal and 15 rebased decisions differ only in link targets | yes | EVD-007 |
| EVD-010 | [VAL-RT-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Canonical staged QA | Commits `fe3bd418` and `c7374cce`, committed from a worktree without `graphify-out/`, CI-lock environment first on `PATH` | PASS | The pre-commit staged QA, `commitizen check` and generated-message hooks passed in 574 and 723 seconds; an earlier attempt of the second commit failed on a formatter change to the test and was reformatted; the 26 rows validate | yes | EVD-003 |
| EVD-011 | [VAL-RT-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Review and hosted checks | PR #188 independent review of `fe3bd418` and re-review of `c7374cce`; heads `fe3bd418` (CI run `40622072052`) and `c7374cce` (CI run `40625360280`) | PASS | The reviewer approved after the fix; `ci-summary`, `style-pr`, `label` and GitGuardian passed on both heads | yes | EVD-004 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-RT-001](../spec.md#success-criteria--verification-plan) | pending | none | Consumer edits remain | platform |
| [VAL-RT-002](../spec.md#success-criteria--verification-plan) | pending | none | Recovery remains | platform |
| [VAL-RT-003](../spec.md#success-criteria--verification-plan) | pending | none | Removal remains | platform |
| [VAL-RT-004](../spec.md#success-criteria--verification-plan) | pending | none | Review and hosted checks remain | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index, REQ-0003,
  ADR-0039, ADR-0040, ADR-0047, the archive research README and
  m0001, research note m0012, `.claude/provider.md`, `docs/README.md`,
  `docs/02.architecture/README.md`,
  `tests/test_archive_disposition_lifecycle.py`, the 26 units and the
  Retention Assessment table in `docs/98.archive/README.md`.
- **Forbidden Paths**: the nine kept units, frozen Archive records, catalog
  rows and envelopes, validators, the registry and other tests.
- **Approval Required**: the operator approved the batch on 2026-10-28. Push,
  pull request and merge follow RUN-0013.
- **Static Validation**: `python3 scripts/qa.py staged` on each exact index.
- **Live Validation**: not applicable; no cluster or host state changes.
- **Secret / Vault Handling**: no secret-bearing content is read or printed.
- **Rollback Plan**: availability never returns to `retained` (ADR-0040).
  Content is recovered with `git archive <envelope commit> <original path>`;
  bringing it back is a new unit under a new decision. The consumer edits
  revert with the pull request.
- **Evidence Location**: this Task.

## Verification Summary

Not run yet.
