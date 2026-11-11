---
title: "Requirement Owner Crosswalk"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0154"
---

# Requirement Owner Crosswalk Technical Specification (Spec)

## Overview

This approved change contract covers stages W00–W01 of the follow-up roadmap that completed SPEC-0152 deferred (`git show 4033d38e:docs/03.specs/0152-manual-document-disposition-policy/plan.md`, section `Deferred Roadmap`, order 1: link requirement-level current owners, evidence and differences in existing work records, and keep satisfied contracts). The input is the externally supplied v14.2 W00 execution package in the git-ignored `_workspace/workspace_execution_tasks/` directory. That package is evidence, never repository authority. It declares 106 common requirement IDs and three hy-home-k8s profile IDs (K8S-01..03). [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) owns the governance requirements this crosswalk is judged against. The [Plan](plan.md) orders the work; [Task 0001](tasks/tsk-0001-requirement-owner-crosswalk.md) records execution, the full crosswalk and acceptance.

## Strategic Boundaries & Non-goals

- Scope is one requirement-level crosswalk: for each of the 109 package IDs, name the current repository owner, the observed fit (PASS, GAP, CONFLICT, UNVERIFIED or N/A), the action (KEEP, ADD, CHANGE or DEFER), the next stage owner (W01–W11) and the read level. Then record how the observed conflicts are resolved.
- This package changes no policy, validator, test, setting, hook, workflow, manifest or README outside the package and its Stage 03 router. Each GAP is implemented later under its own stage owner and package, not here.
- Kept without reopening: the PR #220 and SPEC-0153 active lifecycle replay; ADR-0056 manual disposition review (no new Spec, retention ledger or archive-wide gate for routine disposition); the Stage 01–03 and Stage 99 Git-only closure; accepted SPEC-0149–0151 and completed numbering.
- The package's own ledgers, question register and 1,250-line, 208-work-item and 14,028-pair history stay read-only inherited inputs. Building this crosswalk does not certify them, reopen them, or close them.
- No remote push, PR, merge, branch deletion, cluster access, secret read or paid external call. The local `main` branch stays 12 commits behind `origin/main`, untouched.
- Open question: none that changes a criterion. The user decided the two questions this survey raised on 2026-11-11 (see [Task Inputs](tasks/tsk-0001-requirement-owner-crosswalk.md#inputs)).

## Contracts

- Every package requirement ID appears exactly once, with a non-empty current owner and next owner. Each cited repository path resolves at the recorded HEAD.
- KEEP requires PASS with a concrete fitness reason. A file, a test name or a merged PR alone is UNVERIFIED. Facts about the native client, hosted CI, remote settings or a live cluster stay UNVERIFIED with NOT_RUN in the open condition, never PASS.
- When a package requirement contradicts an accepted repository contract, the repository contract governs. The crosswalk records the rejected part of the package requirement and does not change the contract.
- The crosswalk lives only in this package's Task, as REQ-0003-FR-0019 and FR-0022 require. No separate ledger, register or memory entry holds its state.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance system view, and accepted [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) constrains disposition. This design conforms to both and changes neither. Four independent read-only reviewers each covered one scope group: W00–W02, W03–W04, W05–W06 with K8S-02, and W07–W10 with K8S-01 and K8S-03. They read the owning lines rather than grep hits and returned one row per ID. The supervising session merged the rows and checked them mechanically. It recorded the baseline Git, PR and remote observations itself.

## Data Modeling & Storage Strategy

No persistent data structure is introduced. The crosswalk is a Markdown table under the Task's `Task Evidence` section. Its working CSV stays outside the repository; the Task records that CSV's SHA-256 and the SHA-256 of each package input file. Git history recovers this package after its exit.

## Interfaces & Data Structures

Crosswalk columns: `Package ID`, `Observation`, `Action`, `Next owner`, `Read level`, `Current repository owner`, `Evidence`, `Open condition`. Observation values are PASS, GAP, CONFLICT, UNVERIFIED and N/A. Action values are KEEP, ADD, CHANGE and DEFER. Read levels are SEMANTICALLY_REVIEWED, READ and PARTIAL. These are survey labels, not repository lifecycle or schema states.

## Edge Cases & Error Handling

- A missing or duplicate ID, an empty owner or next owner, or a cited path that does not exist at HEAD fails the completeness check. Task evidence records a negative fixture that injects each of these four defects.
- A reviewer claim that contradicts directly observed Git state is corrected in the Task and keeps the original claim visible. Example: a reviewer read "dev 12 commits ahead of main" from the out-of-date local `main`, while `origin/main` equals `origin/dev`.
- A row whose source was only partly read is labelled PARTIAL or READ, never SEMANTICALLY_REVIEWED.

## Failure Modes & Fallback / Human Escalation

If the independent review finds a row whose owner or observation is wrong, correct that row with a new evidence entry and keep the earlier one. If a correction changes a criterion, return this Spec to review. A newly found conflict with an accepted contract is shown to the user and does not change that contract. If a stage owner is unavailable, the row stays DEFER with its open condition.

## Verification Commands

- Completeness: an inline Python check over the crosswalk CSV against the package's `REQUIREMENTS.json` and `PROFILE-REQUIREMENTS.json` and `git ls-files`. The command and the exact input hashes are in Task evidence.
- Document checks: `python3 scripts/validate-markdown-profiles.py --mode strict`, `python3 scripts/validate-document-contract-registry.py --mode strict`, `python3 scripts/validate-links-and-owners.py`, `python3 scripts/validate-document-lifecycle.py --root . --mode staged`, and `python3 scripts/qa.py staged` on the exact index before any commit.
- Independent read-only semantic review of the crosswalk against the cited lines.

These are repository-static checks. They do not establish native, hosted or live results.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-TRACE-001 | The completeness check passes on all 109 IDs: no missing or duplicate ID, no empty owner or next owner, every cited path present at HEAD. A negative fixture shows each injected defect is detected. |
| VAL-TRACE-002 | An independent read-only review of the crosswalk against the cited lines finds no blocking error. It confirms that KEEP appears only with PASS (or, for a conflict, KEEP of the repository contract), that runtime-only claims stay UNVERIFIED, and that the settled PR #220, ADR-0056 and Git-only items stay KEEP. |
| VAL-TRACE-003 | Each non-PASS row names a next stage owner and an open condition. Each conflict carries a recorded disposition: GOV-06 ledger part rejected under FR-0019/FR-0022; GIT-09 kept under FR-0018; DOC-12 renumbering rejected under FR-0023; K8S-01 README correction handed to W10; GIT-01 user decision on the `dev` branch handed to W06. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-TRACE-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Completeness check with negative fixture; each row names its basis and owner, and the table states its observation HEAD and date once. |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-TRACE-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Independent read-only semantic review of evidence classes. |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-TRACE-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) | Task review of handoffs and conflict dispositions; no ledger outside the Task. |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-TRACE-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | GOV-06 disposition review: the package's machine ledger is rejected and no progress ledger is restored. |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-TRACE-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | GIT-09 disposition review: the accepted independent-review requirement is kept. |
| [REQ-0003-FR-0023](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-TRACE-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | DOC-12 disposition review: stable identities stay append-only and the renumbering clause is rejected. |
