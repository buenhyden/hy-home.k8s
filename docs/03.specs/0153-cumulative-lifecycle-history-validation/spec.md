---
title: "Cumulative Lifecycle History Validation"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0153"
---

# Cumulative Lifecycle History Validation Technical Specification (Spec)

## Overview

This approved change contract addresses two observed local cumulative-history failures after SPEC-0152 closed. Broad explicit-ref comparison from base `f6c1c8759870db73160da3023d2ba378d0b75fc5` to closure `38ec2bea2be4074203e8ba48491807b9404e3ec0` reported `LIFECYCLE-CREATE` for [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md), although it first entered Git as `proposed` and later became `accepted`. Comparison from the same base to completed source `4033d38e7ac6eac0130700c8cf259ea252f44916` separately reported `LIFECYCLE-CREATE` for the SPEC-0152 Task, although it first entered Git as `in-progress` under the existing local extension and later became `completed`. [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) owns lifecycle correctness. The [Plan](plan.md) orders a bounded repair; [Task 0001](tasks/tsk-0001-cumulative-lifecycle-history-validation.md) will record execution and acceptance.

## Strategic Boundaries & Non-goals

- Scope is the local cumulative ADR and Task history reader in `scripts/validate-document-lifecycle.py` and focused regressions in `tests/test_document_lifecycle_cumulative_history.py`. The observed failures are pre-approval evidence; the user separately approved this bounded implementation on 2026-11-11.
- Keep [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md), completed SPEC-0152 and its Task evidence immutable. Do not rewrite the two local commits or treat a passing adjacent comparison as a passing broad comparison.
- Preserve Stage 99 initial states, ordinary ADR transitions, distinct identity, contextual/supersession checks, the first-approved Spec/Plan receipt, ordinary unregistered Task-copy rejection, the existing 16 MiB cumulative snapshot-work cap and other bounded-history limits. No schema, Registry, new state, general copy allowance, gate bypass, hosted action or live operation is proposed.
- Git's `C` similarity score and chosen source are provenance heuristics, not proof of authorship or a decision relationship. Admission depends on typed source retention, identity and actual lifecycle evidence, never a newly invented similarity threshold or a mandatory link to Git's heuristic source.

## Contracts

- A broad local CI or explicit-ref comparison may admit a new ADR whose first committed state is `proposed` and whose later commits follow valid body or forward transitions even when Git reports a `C` copy from another ADR. The source ADR must remain present and byte-unchanged in that first commit; source and target have the same profile, the target was absent at the parent, and both carry distinct, path-canonical, unique artifact IDs. A rename `R` or a deleted source still fails. Each actual edge still passes existing lifecycle rules; neither `C004` nor `C095` alone decides validity.
- A first Task copied from its unchanged registered Task template may enter only an existing nonterminal initial state (`draft`, `ready`, `in-progress` or `blocked`). Ordinary `draft` creation keeps its existing route and needs no approved parent or execution evidence. Only `ready`, `in-progress` and `blocked` use the local first-record Task extension and their applicable approved-parent, execution, evidence and status prerequisites. Every route still requires an absent target, unchanged registered template, unique path-canonical artifact ID and the same historical first-edge checks. The template-copy exception alone grants no execution authority. A broad comparison may then replay a legitimate `in-progress` → `completed` history.
- Rename provenance, deleted or changed source, equal or mismatched IDs, cross-profile copies, first-record accepted ADR, terminal Task creation, invalid edges and deletion/recreation still fail. Ordinary unregistered Task copies and broken first-approved Spec/Plan receipts still fail. High or low Git similarity cannot override those semantic guards.
- Ordinary ADR path replay avoids full cross-document body context when the existing comparison does not require it. Task replay reduces repeated full-snapshot work while preserving exact parent approval, cancellation successor/waiver, receipt-hash, external link-profile, cross-document, terminal, evidence and identity checks wherever required. Supersession and first-approved Spec/Plan cases retain their required context. All work remains under the existing 16 MiB cumulative snapshot-work cap and candidate/event limits; exceeding a bound fails closed.

## Core Design

The current [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) and accepted [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) constrain this repair. Git reports `C004` from retained ADR-0055 into the proposed ADR-0056 and `C002` from the registered Task template into the first `in-progress` SPEC-0152 Task. Current copy helpers reject both before their otherwise valid first-edge checks. Read-only isolation of each copy signal found later repeated full evidence snapshots exceed the unchanged 16 MiB work budget. The repair narrows provenance admission to those two typed cases and avoids context that ordinary ADR edges do not need, while retaining Task's contextual validation and all original identity, state and receipt rules.

## Data Modeling & Storage Strategy

No persistent field or storage changes. The existing Git history, Stage 99 Registry and lifecycle diagnostics remain the inputs and outputs. This package's Task records the before/after local command results and limitations. No new lineage or QA ledger is created.

## Interfaces & Data Structures

The user-visible interface remains `scripts/validate-document-lifecycle.py` in local `--mode ci` and `--mode explicit-ref`. The repair is internal to cumulative create/provenance and per-edge comparison. The input is an exact base and tip plus existing Git objects; the output remains existing pass/fail diagnostics. No CLI flag, error identifier, JSON shape or profile schema changes.

## Edge Cases & Error Handling

Exercise valid absent → proposed → accepted ADR histories with both `C004` and `C095` heuristic scores and an absent → evidence-valid in-progress → completed Task history, plus unrelated large corpus under the unchanged 16 MiB budget. Negative fixtures include equal/wrong canonical ID, `C004` and `C095` with invalid semantic guards, rename, source mutation/deletion, cross-profile source, invalid edge, delete/recreate, unregistered Task copy, missing Task extension/approval/evidence, terminal Task create and broken first-approved Spec/Plan receipt. A missing Git object, malformed provenance or exceeded budget remains a failure.

## Failure Modes & Fallback / Human Escalation

The observed broad-history failure stays open until a reviewed code change and exact-history local check pass. If the narrow case cannot be admitted without changing global initial states or the budget, stop the repair and return the design to the Spec owner for review. Do not amend accepted ADR-0056, falsify SPEC-0152 evidence, bypass the validator or claim hosted CI.

## Verification Commands

First run focused `tests/test_document_lifecycle_cumulative_history.py` negative and positive cases, recording a failing case before implementation and subsequent passing cases. Then run affected local document/lifecycle checks through `python3 scripts/qa.py quick` and exact-index staged QA for an authorized commit. Re-run local `--mode explicit-ref` from `f6c1c8759870db73160da3023d2ba378d0b75fc5` to each observed tip (`4033d38e7ac6eac0130700c8cf259ea252f44916` for Task; `38ec2bea2be4074203e8ba48491807b9404e3ec0` for ADR), and local `--mode ci` on the relevant ranges. These are repository-static checks, not hosted CI.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-HIST-001 | Focused RED/GREEN regression and actual broad local explicit-ref/CI checks admit the valid ADR-0056 proposed → accepted history when Git heuristically reports a copy from a retained unchanged same-profile ADR with distinct unique canonical IDs; both low and high similarity valid examples pass only with all semantic guards. |
| VAL-HIST-002 | Focused RED/GREEN regression and actual broad local explicit-ref/CI checks admit the valid first `in-progress` → `completed` Task history through only the registered-template and existing evidence-bound first-record route. |
| VAL-HIST-003 | Negative provenance, identity, state, Task-copy and Spec/Plan-receipt cases remain rejected; large unrelated corpus stays within unchanged 16 MiB and excess still fails closed; affected QA and independent review report no blocking finding. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-HIST-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) | Focused ADR history and actual local broad explicit-ref/CI comparison. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-HIST-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Focused Task history and actual local broad explicit-ref/CI comparison. |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-HIST-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Negative profile, provenance, ID, Task and receipt regressions plus unchanged-budget review. |
