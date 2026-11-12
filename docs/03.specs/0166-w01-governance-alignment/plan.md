---
title: "W01 Governance Alignment Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0166-PLAN-0001"
parent_ids: ["SPEC-0166"]
---

# W01 Governance Alignment Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds one constraint: only the six W01 files, this package, the Stage 03 README and reviewed baseline digests change.

## Overview

Edit the W01 governance owners so each meaning in the Spec's Contracts has one owner, point the other files to it, and record the handoffs. [Task 0001](tasks/tsk-0001-w01-governance-alignment.md) owns execution and evidence.

## Context

SPEC-0161 handed these W01 items over and recorded the user's decisions; SPEC-0162 to SPEC-0165 already delivered GOV-01, GIT-09, DOC-09 and the pinned hook environment. This branch continues `claude/w00-v14-7-intake` after `e3d72466`. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) is unchanged. No ADR changes: [ADR-0048](../../02.architecture/decisions/0048-local-qa-and-semver-release-ownership.md) and REQ-0003 FR-0017 keep governing hosted CI until the W06 change set, and [ADR-0058](../../02.architecture/decisions/0058-repository-vocabulary-in-knowledge-surface.md) places term meaning in the glossary.

## Goals & In-Scope

- `document-authoring.md`: approval versus adoption merged into the existing shared-contract paragraph, the target record, extension points, derived copies, a pointer to the Policy role, semantic-review wording.
- `sdlc.md`: conflict order replacing "neither side is presumed correct", three axes, Policy role, ADR approval wording.
- `quality.md`: result reuse equivalence, check timing, the adopted hosted CI target beside the current lane.
- `git.md`: the integration wording.
- Glossary: `TERM-CI` and linked Policy Owner cells.

## Non-Goals & Out-of-Scope

- Registry, schema, template, validator, test and workflow changes (W03, W05, W06, W07).
- Lifecycle state semantics (W04) and `approval-and-safety.md`, `agent-execution.md` (no change needed for W01).
- The hosted CI contract (FR-0017, criterion 11, ADR-0048), `ci.yml` and the hosted-lane wording in `sdlc.md`, `git.md` and `work-lifecycle.md`: one W06 change set.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-GOVALIGN-001](spec.md#success-criteria--verification-plan), [VAL-GOVALIGN-002](spec.md#success-criteria--verification-plan) | Edit the W01 files the Spec names. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w01-governance-alignment.md) | Phrase search, knowledge and strict document checks, suites. |
| WORK-002 | [VAL-GOVALIGN-003](spec.md#success-criteria--verification-plan) | Record the handoffs and the exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w01-governance-alignment.md) | Exact-index QA and commit hooks. |

## Verification Plan

- Run the phrase search before (hits) and after (no current-owner hit), and the anchor search after (one hit each in its owner).
- Run the commands in the Spec's Verification Commands.
- Architecture compliance: AD-0006 unchanged; ADR-0048 and FR-0017 still govern hosted CI; ADR-0058 followed.
- Record the risk class (`medium`: policy change) and the core-diff checklist; no permission, trigger or protected action changes.

## Risks & Mitigations

- **Policy text claims enforcement that does not exist.** Owner: W01 author. Mitigation: the hosted CI target and the contract-record fields are stated as targets with the observed state and the owning stage. Rollback: revert the implementation commit.
- **A meaning is restated in two owners.** Owner: W01 author. Mitigation: one owner per meaning, pointers elsewhere, checked in the core-diff checklist. Rollback: revert the implementation commit.

## Completion Criteria

All three criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Approval versus adoption and the contract record | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Shared contract paragraph |
| Conflict order, three axes and Policy role | [SDLC contract](../../../.agents/governance/sdlc.md) | Current Contract |
| Result reuse, check timing and the hosted CI target | [Quality policy](../../../.agents/governance/quality.md) | Validation runner envelope; hosted lane |
