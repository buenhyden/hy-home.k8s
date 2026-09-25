---
title: "Deferred Conflict Resolution Technical Specification"
version: "0.2.0"
type: "sdlc/spec"
status: "done"
owner: "platform"
updated: "2026-09-25"
layer: "specs"
artifact_id: "SPEC-0089"
---

# Deferred Conflict Resolution Technical Specification (Spec)

## Overview

[SPEC-0088](../0088-operations-corpus-convergence/spec.md) closed with four
conflicts deferred to named owners. On 2026-09-25 the request owner asked for
those conflicts to be resolved, and for every open Spec, Plan, or Task that
conflicts with current authority to be withdrawn, cleaned up, or corrected.
This Spec owns that round.

## Strategic Boundaries & Non-goals

In scope: the four SPEC-0088 deferrals; SPEC-0008, SPEC-0049, and SPEC-0086,
the open Stage 03 packages; the current documents that describe them; and this
package.

Out of scope: any manifest, bootstrap, or workflow change; any Stage 98 body;
the physical move of a withdrawn package into `98.archive/retired/`, which needs
its withdrawal commit on the default branch first; push, pull request, merge,
and any live or provider action.

## Contracts

- A gate runs once per identical input in a profile or lane. A fast-lane gate
  whose checks a full-profile gate already runs declares that gate as
  `coveredBy`; it stays out of `full` and shares no lane with its coverer, and
  the full profile still covers every registered gate directly or through that
  declaration.
- The English-first rule applies to every current Stage 03 `spec.md`,
  `plan.md`, and Task. A document in a terminal state, as the Stage 99 registry
  classifies it, keeps the generation it closed in.
- Current architecture states facts the tree supports.
- An open package whose scope, dependencies, or tools contradict accepted
  decisions is withdrawn through legal lifecycle edges, and its still-unowned
  requirement gap is recorded at the requirement that owns it.

## Core Design

Five ordered local commits: propose this package; resolve the validation
conflicts test-first and activate; correct architecture; withdraw SPEC-0049 and
open its Tasks for cancellation; cancel them and close.

## Data Modeling & Storage Strategy

`scripts/validation/registry.json` gains an optional `coveredBy` field on a
validator, declared in its schema. Git holds every changed byte.

## Interfaces & Data Structures

`coveredBy` names one registered validator. The affected-surface validator
rejects a covered gate that is listed in `full`, names an unknown or uncovered
coverer, or shares a lane with it (`SURFACE-COVERED-BY`).

## Edge Cases & Error Handling

A Task cannot move from `queued` to `cancelled` directly, so a withdrawn
package's Tasks pass through `in-progress` in a separate commit. A registry edit
that would invalidate the routing contract is validated in memory before it is
written, because the provider write guard reads that contract on every edit.

## Failure Modes & Fallback / Human Escalation

A failing gate stops the commit; no assertion is weakened. The retirement move
of SPEC-0049 is a named deferral with its next owner.

## Verification Commands

```bash
python3 scripts/validate-affected-surfaces.py --root .
python3 scripts/validate-document-lifecycle.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/qa.py staged
python3 scripts/qa.py full
git diff --check
```

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-DCR-001 | The archive contract modules run once in `full` and once in each lane, and the coverage invariant rejects every way to reintroduce the double run | Focused tests and the affected-surface gate |
| VAL-DCR-002 | Current Stage 03 plans and Tasks are English-first checked, and terminal documents are skipped by registry class | Focused test and the repository quality gate |
| VAL-DCR-003 | ADR-0031 and AD-0006 state the closed Spec 0054 and the real role registry path | Link gate and review |
| VAL-DCR-004 | The chart objects RUN-0004 names are confirmed by a render of the pinned chart | Task |
| VAL-DCR-005 | Each open package is kept with a reason or withdrawn through legal edges, and its current consumers and requirement gaps are updated | Lifecycle and link gates and the Task |
| VAL-DCR-006 | Staged QA passes for each commit and full QA runs on the final tree | Staged and full QA |

## Traceability

The [Implementation Plan](plan.md) owns order and risk. The
[resolution Task](tasks/tsk-0001-resolve-deferred-conflicts.md) owns the
evidence.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DCR-001 | Focused tests and the affected-surface gate |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DCR-002 | Focused test and the repository quality gate |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DCR-003 | Link gate and review |
| [REQ-0004-FR-0004](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-DCR-004 | Task |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DCR-005 | Lifecycle and link gates and the Task |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DCR-006 | Staged and full QA |
