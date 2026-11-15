---
title: "W01 3.0.1 Governance Contract Fit"
version: "0.3.0"
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

Read-only survey on 2026-11-15: the W01 prompt, D00, D01, D03, D15, the S-items the prompt names, the PKG vocabulary and the requirement mapping; three subagent rule audits; spot reads of EXEC-R001 to R012, SAFE-R017 to R020, GIT-R012 to R014, FMT-R001 to R011, AUTHOR-R007, DOCLIFE-R003 and DOCLIFE-R009; and searches of `scripts/` and `tests/` for pinned text. The edits are in commits `c104f154`, `e2cdbd4d` and `c9c89b44`.

### Blockers and Decisions

The independent review passed (EVD-005), and the user approved the Spec and Plan (EVD-006). The user kept W01-H02 open for now. No question is open.

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-W01C-001](../spec.md#criteria) | Glossary to vocabulary 3.0.1. | platform | completed | PASS | EVD-007 |
| WORK-002 | [VAL-W01C-002](../spec.md#criteria) | One author for the four duplicates; retire EXEC-R012. | platform | completed | PASS | EVD-008 |
| WORK-003 | [VAL-W01C-003](../spec.md#criteria) | Rule-fit, disposition and owner-correction records; W01-H02 row and entry. | platform | completed | PASS | EVD-009 |
| WORK-004 | [VAL-W01C-004](../spec.md#criteria) | Rule explanation and three violation cases. | platform | completed | PASS | EVD-010 |

## Verification Evidence

### Results

| Evidence ID | Consumer | Work Unit | Command | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-W01C-001](../spec.md#criteria) | WORK-001 | Knowledge validator and row comparison with the PKG vocabulary | Implementation snapshot | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-W01C-002](../spec.md#criteria) | WORK-002 | Governance and lifecycle validators and link check | Implementation snapshot | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-W01C-003](../spec.md#criteria) | WORK-003 | Ledger gate and strict document validators | Implementation snapshot | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-W01C-004](../spec.md#criteria) | WORK-004 | Three violation cases on scratch copies | Implementation snapshot | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-W01C-001](../spec.md#criteria) | WORK-001 | Independent semantic review | Draft commit `202bf87d`: spec.md sha256 `8355a723a264242cfe6b416557a5e2df209e68999e8d127496cd0542b8622ded`, plan.md sha256 `456fff03f06392fc82f56b3e9e0575d09f60a7bd027eef907339ae43f2089d11` | PASS | Read-only `code-reviewer` subagent, separate context, 2026-11-15. The first pass on spec `7345f092` and plan `bb439ee1` returned REQUEST_CHANGES with five MAJOR and two NIT findings: per-requirement dispositions, a rule-explanation criterion with violation cases, facts only the duplicates held, the W01-H02 location and resume condition, the W04-CONTENT ownership of the recovery text, the Korean column with owner links and version, and the Task design summary. All seven were applied. The second pass on spec `f9c6c937` and plan `456fff03` returned APPROVE with one non-blocking NIT (also-consumed-by note for rows 10 and 11), which produced spec `8355a723`. Review only; it approves nothing. | yes | none |
| EVD-006 | [VAL-W01C-001](../spec.md#criteria) | WORK-001 | Spec/Plan approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes (Recommended) to the SPEC-0217 approval question naming spec.md 8355a723 and plan.md 456fff03, 2026-11-15","review_ref":"EVD-005","scope":["SPEC-0217","SPEC-0217-PLAN-0001"],"reviewed_spec_sha256":"8355a723a264242cfe6b416557a5e2df209e68999e8d127496cd0542b8622ded","reviewed_plan_sha256":"456fff03f06392fc82f56b3e9e0575d09f60a7bd027eef907339ae43f2089d11","validity":"confirmed","revocation":"none"} | PASS | Approves the reviewed Spec and Plan content of draft commit `202bf87d`; the approved files differ from it only in `status` and `version`. It accepts no criterion and authorizes no push or merge. | yes | none |
| EVD-007 | [VAL-W01C-001](../spec.md#criteria) | WORK-001 | Knowledge validator and row comparison with the PKG vocabulary | Commits `c104f154` (glossary to 3.0.1) and `c9c89b44` (maintenance sentence); PKG `repository-vocabulary.json` `a8f595f5`; pinned `hyhome-validation` environment, 2026-11-15 | PASS | `scripts/validate-knowledge-surface.py --root .`: `[PASS] knowledge surface: 3 documents, 0 violations`. A row-by-row script comparison found the 43 common Term IDs equal to 3.0.1 with no missing or extra ID, every Term and Korean cell equal to 3.0.1, every common Contract Version `3.0.1` and every Contract Version numeric. `TERM-HISTORICAL-AUDIT` is gone; the glossary is at version 2.0.0. | yes | EVD-001 |
| EVD-008 | [VAL-W01C-002](../spec.md#criteria) | WORK-002 | Governance and lifecycle validators and link check | Commit `c104f154`: EXEC-R004, EXEC-R006 and the retired EXEC-R012 in `agent-execution.md` (1.10.0), AUTHOR-R007 in `document-authoring.md` (3.37.1), the read-only bullet in `.claude/provider.md` (1.9.2); pinned environment, 2026-11-15 | PASS | `validate-agent-governance.py`: `[PASS] agent registry validation passed: providers=2 roles=17 permissionClasses=4 skills=17 handoffs=67 projections=51`. Lifecycle strict and staged PASS, including the rule-ID history check. Links and owners strict PASS. EXEC-R012 is `retired; none` and its body definition was removed, because `POLICY-RULE-INLINE` refuses a definition token without an active row. The Codex chain facts were confirmed in `.codex/provider.md` lines 152 and 155 before EXEC-R004 lost them. | yes | EVD-002 |
| EVD-009 | [VAL-W01C-003](../spec.md#criteria) | WORK-003 | Ledger gate and strict document validators | Commit `c9c89b44` (SPEC-0161 Task `W01 3.0.1 Rule Fit`, `W00 Verdict Owner Corrections`, EVD-133, W01-H02 row) after `e2cdbd4d` (two moved baseline lines); pinned environment, 2026-11-15 | PASS | `validate-work-residue-ledger.py`: `PASS work residue ledger: 57 entries`, with the W01-H02 row and entry agreeing on the new resume condition. The four strict document validators PASS. The table lists 58 non-KEEP rules with one owner each and 160 `KEEP_VERIFIED` rules, 218 in all; every W01 requirement ID has a disposition in the Spec. | yes | EVD-003 |
| EVD-010 | [VAL-W01C-004](../spec.md#criteria) | WORK-004 | Three violation cases on scratch copies | Three local clones of commit `c104f154` in the session scratchpad (`negA`, `negB`, `negC`), outside the repository; pinned environment, 2026-11-15 | PASS | (A) EXEC-R012 changed from `retired; none` to `active` and staged: lifecycle staged refused it with `POLICY-RULE-REISSUE` (`EXEC-R012 stays retired`). (B) A duplicated `TERM-DRAFT` row: the knowledge validator refused it with `KNOWLEDGE-TERM-DUPLICATE`. (C) The `TERM-DESIGN-FIT` owner link pointed at a missing file: the knowledge validator passed it, and the links validator refused it with `LINK-BROKEN`. That corrected the glossary's maintenance claim in `c9c89b44`. No common rule remains restated in `.claude/provider.md` or `.codex/provider.md`; the only match left is the new link sentence. The rule explanation is in the lead text of the SPEC-0161 `W01 3.0.1 Rule Fit` table. The scratch clones were left in the session scratchpad, because the delete command was denied by the permission mode. | yes | EVD-004 |
| EVD-011 | [VAL-W01C-003](../spec.md#criteria) | WORK-003 | Manual package-exit decision freeze | This package's `spec.md`, `plan.md` and Task; the consumers named below; the user's 2026-11-15 instruction to commit, push, open a PR and merge on completion; Git-history-only method | PASS | The consumer, preservation, hold, authority and method decision is frozen below before this package's final source commit. Each file's committed `commit:path`, retained-ref reachability and byte comparison are recorded in REQ-0003 Archived Lineage before deletion. An unresolved condition defers the affected deletion. | no | none |

### Resolution Links

The Resolves column names the earlier row each PASS row closes: EVD-007 to EVD-010 close EVD-001 to EVD-004.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-W01C-001](../spec.md#criteria) | accepted | EVD-007 | Accepted by the user on 2026-11-15 (direct answer "Accept all four (Recommended)" to the SPEC-0217 acceptance question naming commits `c104f154` to `4fd8d40d`) | platform |
| [VAL-W01C-002](../spec.md#criteria) | accepted | EVD-008 | Accepted by the user on 2026-11-15 (direct answer "Accept all four (Recommended)" to the SPEC-0217 acceptance question naming commits `c104f154` to `4fd8d40d`) | platform |
| [VAL-W01C-003](../spec.md#criteria) | accepted | EVD-009 | Accepted by the user on 2026-11-15 (direct answer "Accept all four (Recommended)" to the SPEC-0217 acceptance question naming commits `c104f154` to `4fd8d40d`) | platform |
| [VAL-W01C-004](../spec.md#criteria) | accepted | EVD-010 | Accepted by the user on 2026-11-15 (direct answer "Accept all four (Recommended)" to the SPEC-0217 acceptance question naming commits `c104f154` to `4fd8d40d`) | platform |

### Remaining Conditions

None remains for this package. On 2026-11-15 the user chose to keep W01-H02 open for now (answer "Keep open for now"). It stays in the ledger with owner W01 and the resume condition "When the user decides its per-item withdrawal (Q04)". The non-KEEP rules of the SPEC-0161 `W01 3.0.1 Rule Fit` table stay with their owning stages.

Frozen package disposition decision:

- **Target and method**: After the final source commit, retire only this Stage 03 package (`spec.md`, `plan.md` and this Task) through Git-history-only recovery. No other document is selected.
- **Consumers and preservation**: The glossary, the three policy files, the Claude provider note and the SPEC-0161 Task hold the lasting result, and they name SPEC-0217 by ID only. Current consumers: the Stage 03 README entry and this Task's `.secrets.baseline` entries, which the closure change removes.
- **Hold and authority**: The current repository documents and the user's request identify no hold on these files. The disposition authority is the user's 2026-11-15 instruction to commit, push, open a PR and merge on completion. If a hold or unmet consumer is identified before deletion, the affected deletion is deferred and its source kept. Remote retention is not inferred from local refs.
- **Proof handoff**: This Task freezes the decision before its final source commit. After that commit, each file's exact `commit:path`, blob availability, reachability from the retained local ref and a byte comparison with the source still in the tree are recorded in REQ-0003 Archived Lineage before any file is deleted.

## Handoff

### Promotion Receipt

The Plan promotes none.

### Next Owner

WORK-001 to WORK-004 passed (EVD-007 to EVD-010); the review of record is EVD-005, and the risk class is `high`. The user accepted all four criteria and kept W01-H02 open. Next: platform closes the package. After that, W02, W04, W05, W06, W07, W08, W10 and Q07-CUTOVER take their rule-fit rows in at their own intake.
