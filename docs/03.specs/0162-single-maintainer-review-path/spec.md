---
title: "Single-Maintainer Review Path"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0162"
---

# Single-Maintainer Review Path Technical Specification (Spec)

## Overview

This approved change contract makes the review path match requirement GIT-09 of the external v14.7 execution package, which the user adopted on 2026-11-12 over the earlier SPEC-0156 rejection ([SPEC-0161](../0161-w00-v14-7-delta-intake/spec.md) Task, EVD-018). The package stays git-ignored evidence. Today the [quality policy](../../../.agents/governance/quality.md#semantic-review) requires an independent read-only agent review, and the [Git policy](../../../.agents/governance/git.md) makes a new-context review a pull-request completion condition. GIT-09 says an extra agent API call must never be a mandatory reviewer: a single-maintainer review combines a risk class, static and contract checks, a core-diff checklist, the owner's explicit acceptance and a recovery path, with evidence and release approval records. [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) FR-0018 owns the requirement. The [Plan](plan.md) orders the work; [Task 0001](tasks/tsk-0001-single-maintainer-review-path.md) records evidence and acceptance.

## Strategic Boundaries & Non-goals

- In scope: REQ-0003 FR-0018, its Traceability row, its Evaluation Expectation and the Scope and Non-goals sentence on rejected clauses; `.agents/governance/quality.md` Semantic review, its Pull request row and the handoff field `reviewer identity and disposition`; `.agents/governance/git.md` pull-request completion and the missing-second-reviewer sentence; the `Independent change review` role row in `docs/03.specs/AGENTS.md`; `.agents/workflows/work-lifecycle.md` Completion step 1; `.agents/governance/document-lifecycle.md` first-record approval review row wording.
- Out of scope: DOC-09 reverse traceability, CI-SCOPE hosted checks, Repository Vocabulary, common document forms and DOC-12 renumbering; each has its own package.
- No validator, test, hook, workflow, registry or template changes. The first-record approval validator keeps its `Independent semantic review` row name; renaming it belongs to W05.
- Accepted ADRs are not amended. ADR-0047, ADR-0056 and ADR-0057 say "independent review" without requiring an agent, and the quality policy defines that term. ADR-0052 also names the hosted `independent-review` check of review App `5341483`; `.github/rulesets/main-protection.md` records that check as removed on 2026-11-03 at the operator's request, so that clause is history, not a live agent requirement.
- `.agents/governance/document-authoring.md` ("independent review" as an adoption evidence kind) is reviewed and retained: the checklist path satisfies it.
- No push, PR or merge without separate approval.
- Open question: none.

## Contracts

- No rule, gate or completion condition requires an extra agent or model API call as a reviewer, and a proxy or summary agent does not restore that requirement.
- The required review path is a recorded risk class, the applicable static and contract checks, a core-diff checklist over the exact snapshot, the owner's explicit acceptance and a recovery path (rollback commit or bounded procedure), with the evidence and any release approval recorded. An optional separate agent review, when the operator asks for one, is supporting evidence.
- No review step, agent or human, is recorded as a second human approval.
- The first-record approval row named `Independent semantic review` is satisfied by the exact-byte checklist review of the approving owner or by an optional separate reviewer.
- `BLOCK`, `FIX` and `NOTE` keep their meaning; a failed required check or unresolved `BLOCK` still blocks completion.
- Missing applicable automation stays an evidence gap; acceptance is never inferred from a check PASS, a merge or an optional review.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view and is unchanged. [ADR-0052](../../02.architecture/decisions/0052-single-main-trunk-branch-strategy.md) names hosted checks and an independent review before merge; this design keeps the remaining hosted checks and defines independent review as the checklist path. Each policy file keeps one writer (W01); the requirement text changes in REQ-0003 in the same change.

## Data Modeling & Storage Strategy

No data changes. The risk class and checklist outcome are recorded in the existing Task evidence.

## Interfaces & Data Structures

This change is `high`: it rewrites the pull-request completion and merge-direction conditions, which guard a protected action. Risk classes: `low` for document-only changes outside policy, registry, validator, hook, workflow and permission files; `medium` for policy, registry, template, validator or test changes; `high` for permission, secret handling, hook, workflow, protected-action or data-loss paths.

## Edge Cases & Error Handling

- An optional agent review that reports `BLOCK` still blocks until fixed or dispositioned by the owner.
- A change whose risk class is disputed takes the higher class.
- Evidence recorded under the old rule stays unchanged; it is history, not a violation.
- Adding a model API call to the review path under another name (proxy, summary, gate helper) is the same violation as a mandatory agent reviewer.

## Failure Modes & Fallback / Human Escalation

If a current owner outside this scope still requires an agent reviewer, it is listed in the Task and changed in the same package before completion, or the package stops with that file named.

## Verification Commands

- A repository search for agent-review obligations (`independent read-only`, `independent review`, `new-context review`, `separate agent identity`, `reviewer identity`, `second reviewer`, `read-only agent`, `Independent change review`) over `.agents`, `.claude`, `.codex`, `docs/AGENTS.md`, `docs/*/AGENTS.md`, REQ-0003 and the accepted ADRs; every hit is listed in the Task as changed, optional or historical.
- The strict document validators, the staged lifecycle check and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-REVIEW-001 | The search finds no current rule that requires an agent reviewer, and every changed owner states the checklist path. |
| VAL-REVIEW-002 | The owner's checklist review finds no blocking error, and the strict document checks and commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-REVIEW-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), [ADR-0052](../../02.architecture/decisions/0052-single-main-trunk-branch-strategy.md) | Repository search over current owners. |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-REVIEW-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Owner checklist review; strict document checks and commit hooks. |
