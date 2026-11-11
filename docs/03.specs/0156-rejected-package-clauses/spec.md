---
title: "Rejected Package Clauses"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0156"
---

# Rejected Package Clauses Technical Specification (Spec)

## Overview

This approved change contract covers stage W01 of the externally supplied v14.2 execution package, which stays git-ignored evidence and never repository authority. A read-only W01 intake survey found that the current governance owners already satisfy W01's contract and responsibility items: the shared WGOV-CORE 3.0.0 edition is adopted with one consumer edition, approval, execution, verification, acceptance, integration and deployment are defined separately, and no machine path treats CI success or an owner string as approval. The one real gap is that four package clauses rejected because they conflict with accepted contracts are recorded only in the completed SPEC-0154 Task, which leaves the tree at package exit. This change records them durably in [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) "Scope and Non-goals". The [Plan](plan.md) orders the work; [Task 0001](tasks/tsk-0001-rejected-package-clauses.md) records the intake survey, execution and acceptance.

## Strategic Boundaries & Non-goals

- Scope is one sentence in REQ-0003 "Scope and Non-goals" naming four rejected package clauses with the accepted contract each conflicts with, the REQ-0003 version bump, and its Traceability back-link to this Spec.
- The four clauses:
  - a single machine ledger for unfinished, adoption and survey state (package GOV-06), rejected under REQ-0003-FR-0019 and FR-0022;
  - forbidding a mandatory extra model call in single-maintainer review (package GIT-09), rejected under REQ-0003-FR-0018;
  - renumbering Stage 03 from 1 (package DOC-12), rejected under REQ-0003-FR-0023 and stable append-only identities;
  - generated reverse traceability in place of hand-written, checked back-links (the W01 task's common-contract section 7, item 2), rejected under REQ-0003-IF-0001, the reciprocal-link acceptance criterion 02 in REQ-0003 Traceability and the `BODY-LINK-RECIPROCAL` check, by the user's decision on question Q-W01-01.
- No change to governance policy, the agent registry, Stage 99 registry or templates, validators, tests, provider settings, hooks, workflows or manifests. GOV-08 (permission allow rules) stays with stage W07.
- No new ledger, ADR or register: the sentence sits beside the existing non-goal that the removed shared progress ledger is not restored.
- No remote push, PR, merge, secret read, cluster access or cross-repository change; Project-Template stays outside this workspace's boundary.
- Open question: none. Q-W01-01 was answered on 2026-11-11.

## Contracts

- After the change, REQ-0003 "Scope and Non-goals" names each rejected clause once, with its package label and the accepted requirement or check it conflicts with, and states that the external package is evidence only.
- The sentence restates existing accepted contracts; it adds no new obligation and weakens none.
- REQ-0003 stays `approved`; its version moves from 3.0.2 to 3.0.3 and `updated` is set, as a body correction of an approved requirement.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance system view and accepted [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) constrains disposition; this change conforms to both and changes neither. The non-goals section is the current owner of what REQ-0003 deliberately does not do, so a rejected external clause belongs there rather than in a Task that will leave the tree.

## Data Modeling & Storage Strategy

No data structure changes. The intake survey's working CSV stays outside the repository and is identified by SHA-256 in Task evidence.

## Interfaces & Data Structures

No interface changes. The only consumer is a human or agent reader of REQ-0003.

## Edge Cases & Error Handling

- If a later stage needs one of these clauses, it must amend the accepted requirement it conflicts with first; this sentence is not an exception mechanism.
- If REQ-0003's text near the non-goals has moved since the survey, the sentence is placed by meaning, not line number.

## Failure Modes & Fallback / Human Escalation

If review finds the sentence changes meaning beyond restating accepted contracts, return the Spec to review. A newly found conflict with an accepted contract is shown to the user and does not change that contract here.

## Verification Commands

- The strict document validators in `docs/AGENTS.md`, the staged lifecycle check and the active commit hooks on the exact index.
- An inline check that the REQ-0003 sentence names all four clauses and cites FR-0019, FR-0022, FR-0018, FR-0023 and IF-0001, with a negative copy missing one clause detected.
- Independent read-only review of the sentence against the cited contracts.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-REJ-001 | REQ-0003 "Scope and Non-goals" names all four rejected clauses with their conflicting accepted requirements, and the inline check detects a negative copy missing a clause. |
| VAL-REJ-002 | An independent read-only review confirms the sentence restates accepted contracts only, adds no obligation, and matches the user's Q-W01-01 decision. |
| VAL-REJ-003 | The W01 intake survey is recorded with every item's owner and observation; every non-W01 gap names its stage owner, and the strict document checks and commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-REJ-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Inline check of the non-goals sentence with a negative copy. |
| [REQ-0003-IF-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-REJ-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Independent review against the cited contracts and the Q-W01-01 decision. |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-REJ-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) | Task review of the intake survey and handoffs; strict document checks and commit hooks. |
