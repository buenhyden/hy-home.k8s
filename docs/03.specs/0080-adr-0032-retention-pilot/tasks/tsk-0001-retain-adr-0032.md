---
title: "Retain ADR-0032"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0080-TSK-0001"
---

# Task: Retain ADR-0032

## Overview

This Task records the first ADR-0038 disposition and the fixes it required. It
records observed results only and never promotes a repository-static result to
hosted, provider-runtime, or live evidence.

## Inputs

- [Spec](../spec.md) owns the contract, and [Plan](../plan.md) owns order and
  risk.
- On 2026-09-15 the request owner asked to review and proceed on the SPEC-0079
  residual risks, the pending dispositions, and the scratch clean-up, and chose
  a pilot that retains ADR-0032 alone.

## Task Table

| ID       | Upstream criterion | Work item                                                              | Owner    | Status | Result                                                                 | Evidence                    |
| -------- | ------------------ | ---------------------------------------------------------------------- | -------- | ------ | ---------------------------------------------------------------------- | --------------------------- |
| WORK-001 | VAL-ARP-004        | Compare moved bodies through link rebasing; derive the frozen registry | platform | Done   | Committed before this change; fidelity test equals the merged registry | Unit discovery              |
| WORK-002 | VAL-ARP-002        | Resolve frozen Stage 98 links to a catalog-retained source             | platform | Done   | `_catalog_retained_link` admits frozen sources only                    | Link regressions            |
| WORK-003 | VAL-ARP-003        | Repoint present-rule citations of ADR-0032 and the skill               | platform | Done   | Links and plain-text rules moved to ADR-0038; dated history kept       | Link gate and census        |
| WORK-004 | VAL-ARP-001        | Retain ADR-0032 under `superseded/` with one catalog row               | platform | Done   | Rebased body and one Retention Envelope                                | Lifecycle and archive gates |

## Approval and Safety Boundaries

- **Allowed Paths**: ADR-0032 and its retained path, ADR-0038,
  `docs/02.architecture/decisions/README.md`, `docs/98.archive/README.md` outside
  its frozen manifest comment and record table,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `docs/01.requirements/README.md`, AD-0006, AD-0007, ADR-0014, ADR-0030, the
  SPEC-0054 Spec, Plan, and TSK-0013, `docs/03.specs/README.md`,
  `.agents/skills/archive-cutover/SKILL.md`, `scripts/archive_dispositions.py`,
  `scripts/validate-document-lifecycle.py`, `scripts/validate-links-and-owners.py`,
  the archive, lifecycle, and link tests under `tests/`, and this package.
- **Forbidden Paths**: frozen records, ledgers, and retained packages under
  `docs/98.archive/`, `gitops/`, `infrastructure/`, `policy/`, `secrets/`,
  `.github/`.
- **Approval Required**: The request owner approved the pilot. Moving any other
  decision, push, pull request, and merge are not approved.
- **Static Validation**: `python3 scripts/qa.py staged` over the exact index and
  one `python3 scripts/qa.py full` on the final tree.
- **Live Validation**: DEFER. No live cluster, provider runtime, or network
  action is authorized.
- **Secret / Vault Handling**: No secret, credential, or private configuration
  file is read or printed.
- **Rollback Plan**: Revert the pilot commit; ADR-0032 returns to Stage 02.
- **Evidence Location**: This Task record.

## Verification Summary

Final: `python3 scripts/qa.py full` returned `EXIT=0` with 22 of 22 gates
`PASS` on the staged final tree of this change, before this summary was
written. `python3 scripts/qa.py staged` passed 12 of 12 gates over the exact
index after the last repair and again after this Task-only summary.

Repairs during the work: `INDEX-TREE` rejected the decisions index after the
ADR-0032 row was removed, so its tree was rebuilt. An earlier full run failed
two unit tests only. `test_index_manifest_rejects_missing_duplicate_and_extra_rows`
read every table row in the Stage 98 index, and now reads only the rows under
the frozen record header. `test_both_frozen_index_parsers_skip_the_catalog_table`
appended a second catalog, and now reuses the catalog the index carries. No
gate or contract was weakened.

Review: two independent read-only review rounds ran. The first round reported
two HIGH findings, immutability after disposition and the envelope binding to
the base object, and one MEDIUM finding, retaining a resolved Incident without
its Postmortem. Each was reproduced by a failing test and then fixed. The
second round reported one HIGH finding: plain-text rules that still named
ADR-0032 as current authority. Those rules now name ADR-0038. It also reported
one MEDIUM finding: `_catalog_retained_link` admitted any source, so it is now
narrowed to frozen `archive/migration` and `archive/tombstone` records. Its one
LOW finding, a missing test for held text, was covered by a new test. Dated
history that names ADR-0032 is kept.

Limitation: direct working-tree runs of the archive and lifecycle checks report
index drift while changes are unstaged, so every run used the staged index.

Residual risk: the frozen-registry fidelity test skips when commit
`c652331c` is absent, as in a shallow clone. Hosted CI fetches full history.
Hosted CI, provider runtime, and live evidence were not observed.

Next owner: the architecture decision owner, for the fifteen remaining
superseded decisions the request owner approved on 2026-09-15.

## Traceability

Each work item carries its observed result.

### Lifecycle Traceability

| Criterion / work item                 | Result | Evidence                     |
| ------------------------------------- | ------ | ---------------------------- |
| [WORK-001](../plan.md#work-breakdown) | Done.  | Unit discovery.              |
| [WORK-002](../plan.md#work-breakdown) | Done.  | Link regressions.            |
| [WORK-003](../plan.md#work-breakdown) | Done.  | Link gate.                   |
| [WORK-004](../plan.md#work-breakdown) | Done.  | Lifecycle and archive gates. |
