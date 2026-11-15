---
title: "W01 3.0.1 Governance Contract Fit"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0217-TSK-0001"
parent_ids: ["SPEC-0217-PLAN-0001"]
---

# Task: W01 3.0.1 Governance Contract Fit

## Scope

### Objective and Parent

This Task executes WORK-001 to WORK-004 of the [Plan](../plan.md) for [SPEC-0217](../spec.md) criteria VAL-W01C-001 to VAL-W01C-004.

### Inputs and Authority

- **Request:** on 2026-11-15 (Asia/Seoul) the user asked to continue with the next prompt after W00 (answer `이어서 계속 진행한다.`). To the W01 questions they answered that the requirements decide, and that options are offered again only where the requirements are silent. This approves no Spec or Plan bytes, no criterion and no commit, push or merge.
- **Base:** `main` at `588257c9`; branch `claude/w01-contract-3-0-1`.
- **PKG:** `_workspace/governance/workspace_governance_3_0_1_20261115/`, read-only. The W01 prompt `prompts/W01-CONTRACT.md` has sha256 `091ed4dc9444a21b6771f67b187d85d1ea1d1f21621d5faca0b9de168aa1d7a6`.
- **Survey:** three read-only `docs-researcher` subagents judged all governance rules at text level; this session then spot-checked the duplicates the Spec names. The survey ran no evidence check.
- **Design summary:**
  - Reference designs: D00, D01, D03 and D15, edition 3.0.1, with S02 to S07 and S27.
  - Current difference: the vocabulary is not at 3.0.1, and four rules are authored twice.
  - Choice: adopt the vocabulary and keep one author per rule; record the other owners' conflicts instead of changing their rules.
  - Rejected alternatives: change every conflicting rule here, which crosses into W03, W04, W08, W10 and Q07; leave the duplicates, which breaks GOV-06.
  - Interface: the glossary rows and the policy text that agents read.
  - Failure: the knowledge, governance, lifecycle and link validators refuse a malformed result.
  - Risk: meaning drift or a lost fact, mitigated by the independent review.
  - Acceptance: VAL-W01C-001 to VAL-W01C-004.

- **Allowed Paths**: `.agents/knowledge/glossary.md`, `.agents/governance/agent-execution.md`, `.agents/governance/document-authoring.md`, `.claude/provider.md`, `docs/03.specs/0217-w01-contract-3-0-1/`, `docs/03.specs/README.md`, `docs/03.specs/0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md` (appended tables and row, the W01-H02 Owner and Resume cells, frontmatter `version` and `updated`), `docs/03.specs/work-residue-ledger.json` (the W01-H02 entry only), `.secrets.baseline` (reviewed entries only)
- **Forbidden Paths**: `_workspace/`, `scripts/`, `tests/`, `docs/99.templates/registry.json`, `.codex/`, `.claude/settings.json`, every rule assigned to another stage in the Spec
- **Approval Required**: Spec and Plan approval with an independent review; criterion acceptance; any commit, push, PR or merge
- **Static Validation**: knowledge, governance, four strict document and ledger validators; `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface in scope
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: delete the branch `claude/w01-contract-3-0-1`; `main` is unchanged
- **Evidence Location**: this Task

## Execution Log

### Work Performed

Read-only survey on 2026-11-15: the W01 prompt, D00, D01, D03, D15, the S-items the prompt names, the PKG vocabulary and the requirement mapping; three subagent rule audits; spot reads of EXEC-R001 to R012, SAFE-R017 to R020, GIT-R012 to R014, FMT-R001 to R011, AUTHOR-R007, DOCLIFE-R003 and DOCLIFE-R009; and searches of `scripts/` and `tests/` for pinned text. No file outside this package is edited yet.

### Blockers and Decisions

Waiting for Spec and Plan approval. Resume when the user approves the exact bytes after the independent review.

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-W01C-001](../spec.md#criteria) | Glossary to vocabulary 3.0.1. | platform | draft | NOT_RUN | EVD-001 |
| WORK-002 | [VAL-W01C-002](../spec.md#criteria) | One author for the four duplicates; retire EXEC-R012. | platform | draft | NOT_RUN | EVD-002 |
| WORK-003 | [VAL-W01C-003](../spec.md#criteria) | Rule-fit, disposition and owner-correction records; W01-H02 row and entry. | platform | draft | NOT_RUN | EVD-003 |
| WORK-004 | [VAL-W01C-004](../spec.md#criteria) | Rule explanation and three violation cases. | platform | draft | NOT_RUN | EVD-004 |

## Verification Evidence

### Results

| Evidence ID | Consumer | Work Unit | Command | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-W01C-001](../spec.md#criteria) | WORK-001 | Knowledge validator and row comparison with the PKG vocabulary | Implementation snapshot | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-W01C-002](../spec.md#criteria) | WORK-002 | Governance and lifecycle validators and link check | Implementation snapshot | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-W01C-003](../spec.md#criteria) | WORK-003 | Ledger gate and strict document validators | Implementation snapshot | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-W01C-004](../spec.md#criteria) | WORK-004 | Three violation cases on scratch copies | Implementation snapshot | NOT_RUN | Pending | yes | none |

### Resolution Links

No earlier failure is open.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-W01C-001](../spec.md#criteria) | pending | none | Run WORK-001 after approval | platform |
| [VAL-W01C-002](../spec.md#criteria) | pending | none | Run WORK-002 after approval | platform |
| [VAL-W01C-003](../spec.md#criteria) | pending | none | Run WORK-003 after approval | platform |
| [VAL-W01C-004](../spec.md#criteria) | pending | none | Run WORK-004 after approval | platform |

### Remaining Conditions

Spec and Plan approval, the four work units and criterion acceptance remain.

## Handoff

### Promotion Receipt

The Plan promotes none.

### Next Owner

The independent reviewer and then the user, for Spec and Plan review and approval; then platform for WORK-001 to WORK-004.
