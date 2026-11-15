---
title: "W01 3.0.1 Governance Contract Fit"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0217"
---

# W01 3.0.1 Governance Contract Fit Technical Specification (Spec)

## Overview

### Intent

This Spec applies the W01-CONTRACT stage of the external workspace governance package 3.0.1 (`_workspace/governance/workspace_governance_3_0_1_20261115/`, called PKG below) to this repository. W01 owns the requirements that PKG `dependencies/coverage.json` maps to it: GOV-01 to GOV-08, U09, U12, U13, R04, R14 and R17. In this repository they reduce to three changes and one record:

- **Vocabulary 3.0.1 (U13).** The glossary adopts the meaning, owner role and numeric Contract Version of the PKG vocabulary contract `repository-vocabulary` 3.0.1.
- **One canon (GOV-06, U12, GOV-02).** A rule authored independently in two files keeps one author, and the other place links to it. Native provider detail stays in the provider note.
- **Records.** The rule-fit verdicts of all governance rules are recorded with their owning stage, together with the owner corrections of the W00 verdict table.

The consumers are the agents and stage owners that read the glossary and the governance policies. The [Plan](plan.md) orders the work and the [Task](tasks/tsk-0001-w01-contract-3-0-1.md) records execution.

A read of `main` at `588257c9` on 2026-11-15 found the following:

- **Glossary.** It has the seven common columns, but its Contract Version cells carry edition labels (`repository-vocabulary v14.5`, `v14.7`, `local 1.0.0`), against Q03 and against its own `TERM-CONTRACT-VERSION` row.
- **Vocabulary differences from 3.0.1.** Ten common rows differ in meaning or owner role from 3.0.1. Three 3.0.1 terms are missing (`TERM-DRAFT`, `TERM-READINESS`, `TERM-DESIGN-FIT`). `TERM-HISTORICAL-AUDIT` is not in 3.0.1 and keeps closed audit questions as a current term.
- **Duplicated authoring.** EXEC-R004 restates native AGENTS-chain delivery that `.claude/provider.md` and `.codex/provider.md` own. EXEC-R006 restates the language rule of `document-authoring.md`. AUTHOR-R007 restates the status-marker and `not-required` rules of DOCLIFE-R003 and DOCLIFE-R009. `.claude/provider.md` restates SAFE-R018. EXEC-R012 has no content of its own.

### Owning Requirements

[REQ-0003-FR-0032](../../01.requirements/0003-workspace-agent-governance-platform.md) (one Repository Vocabulary owns shared term meaning) and REQ-0003-FR-0030 (rules, scripts and surfaces trace to active consumers, with duplicates removed after their consumers transfer). [ADR-0058](../../02.architecture/decisions/0058-repository-vocabulary-in-knowledge-surface.md) admits the glossary into the knowledge surface; the glossary's Contract Version, not that decision, carries the edition. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view. This change conforms to all three and amends none.

## Scope

### In Scope

- `.agents/knowledge/glossary.md`: the common rows, Local Extensions rows and Maintenance text, per the vocabulary contract below.
- `.agents/governance/agent-execution.md`: EXEC-R004 keeps the common AGENTS-chain rule and links to the provider notes for native delivery. EXEC-R006 keeps what only it owns (preserve commands, quotations and raw evidence in their original form; responses to the user are in Korean) and links to `document-authoring.md` for document language. EXEC-R012 is retired (`retired;` row kept, ID never reused).
- `.agents/governance/document-authoring.md`: the AUTHOR-R007 sentences that restate DOCLIFE-R003 (`not-required` and cancellation) and DOCLIFE-R009 (row-derived status of a multi-row Task) are replaced by a link to those rules. The authoring instruction only AUTHOR-R007 holds stays: for one row, author the state in frontmatter and write literal `frontmatter` in the row.
- `.claude/provider.md`: the `read-only-evidence` bullet keeps the Claude-native facts and links to SAFE-R018 for the common meaning.
- The SPEC-0161 Task: an appended `W01 3.0.1 Rule Fit` table, an appended `W00 Verdict Owner Corrections` table, one EVD row, the Owner and Resume cells of the live W01-H02 row, and its frontmatter `version` and `updated`.
- `docs/03.specs/work-residue-ledger.json`: the W01-H02 entry, edited together with its live row.
- This package, the Stage 03 README entry, and reviewed `.secrets.baseline` entries.

Decisions applied, not asked again: PKG `decisions.json` Q01 to Q10 and Q-DRAFT. On 2026-11-15 the user answered the W01 questions with "follow the requirements; where they are silent, offer options again". The requirement mapping therefore decides the scope, and items with another primary owner are recorded, not changed:

| Item | Primary owner (PKG) | Here |
| --- | --- | --- |
| Risk-based review: high-risk independent review, low-risk focused check (U30, U31, Q08) | W10-REVIEW | Recorded |
| Draft boundary rules and their enforcement (R16, Q-DRAFT) | W04-LIFECYCLE | `TERM-DRAFT` meaning only (U13) |
| Final cutover recovery and retention (U55, R20, Q01, Q10) | Q07-CUTOVER | `TERM-ARCHIVE` and `TERM-REMOVAL` meaning only (U13) |
| Release document role (U19) | W03-FORMS | Recorded |
| Numeric version profile (Q03) | W03-VERSION | Glossary meaning only (U13) |
| Closed audit identifiers in the ledger (U23, R13) | W02-DISPOSITION | The glossary term is removed (W01 step 4) |
| Hosted product verification | W06 (`CI-SCOPE`) | Recorded |
| Memory capture, deletion and analysis (Q05, Q06) | W08 | Recorded |

Disposition of each requirement that PKG maps to W01:

| ID | Requirement (PKG) | Disposition | Basis |
| --- | --- | --- | --- |
| GOV-01 | Common scope: Task state ownership, approval apart from acceptance, state meaning, no hidden required failure, role transitions, archive protection, evidence trace, rule change | `KEEP_VERIFIED` (text) | DOCLIFE-R001 to R022, SAFE-R008 (status, QA and verdicts are no approval), QUAL rules; archive protection against Q10 is Q07-CUTOVER's |
| GOV-02 | Repository scope: paths, commands, native grammar, deployment, product measures | Changed here | Native detail stays in the provider notes (EXEC-R004, `.claude/provider.md`) |
| GOV-03 | A common contract records one owner, stable ID, version, adoption state, approver, scope and history | `KEEP_VERIFIED` (text); consumer `UNVERIFIED` | AUTHOR-R016, AUTHOR-R017, AUTHOR-R022; numeric version per Q03 is W03-VERSION's |
| GOV-04 | Approval apart from per-repository adoption; same-edition judgment | `KEEP_VERIFIED` (text); consumer `UNVERIFIED` | AUTHOR-R017, AUTHOR-R022, DOCLIFE-R007; D00 requires independent operation without the other repositories |
| GOV-05 | Shared decision roles in one-person operation | `KEEP_VERIFIED` (text) | SAFE-R008 to R011 (operator route) |
| GOV-06 | One canon; controlled projection | Changed here | The four duplicates below |
| GOV-07 | Record conflict priority and change order; no past criterion left as current | Recorded here | `W01 3.0.1 Rule Fit` names each conflict and its owner |
| GOV-08 | Safety policy does not block needed development work; risk approval kept for sensitive operations | `KEEP_VERIFIED` (text) | SAFE-R001 (scoped edits and local validation need no approval), SAFE-R007 (policy repair is ordinary authoring; a completed routine review is not asked again), SAFE-R004 to R006 (protected operations) |
| U09 | Common designs and research bundled in one `dependencies` | Not applicable | A property of PKG, not of this repository |
| U12 | Common governance apart from domain extensions | Changed here | Same as GOV-02 |
| U13 | Glossary seven columns, definition, owner, numeric version | Changed here | Vocabulary contract below |
| R04 | Target design from requirements, not automatic inheritance | Applied | This Spec's method: requirement mapping first, existing rules judged after |
| R14 | Every execution consumes the external evidence design | Applied | S02 to S07 and S27, recorded in the Task design summary |
| R17 | Revise governance, system and policy together with their consumers | Changed here | Each edit names its consumers; the validators below |

W01-H02 (the "rule_id binding" seeded from the r1 package) has no basis in the current requirements: U13 fixes only the seven columns, definition, owner and numeric version, and the W05 prompt reads no binding. Its resume condition ("When W01 is run for its r1 differences") is met by this package. Q04 forbids hiding unfinished work by deletion and requires an explicit per-item approval to withdraw. W01-H02 therefore stays open and non-blocking with owner W01 and the new resume condition "When the user decides its per-item withdrawal (Q04)". The live row and the ledger entry are edited together, and a `W01 3.0.1 Rule Fit` row records the missing basis. The author asks the user for that decision when reporting this package.

Open question: none that changes a criterion.

### Non-goals

- No change to the rules recorded for other owners in the table above, to any validator or test, or to the registry. No ledger entry other than W01-H02 changes, and the ledger keeps 57 entries.
- No change to `.codex/`, which holds no copy of SAFE-R018.
- Any write to `_workspace/`.

## Behavior Contract

### Normal Behavior

- **Vocabulary contract.**
  - Every common row whose meaning matches 3.0.1 keeps its English definition and takes Contract Version `3.0.1`.
  - The Korean column takes the 3.0.1 name in the 15 rows where it differs: `TERM-CANONICAL`, `TERM-VALIDATION`, `TERM-PROMOTION`, `TERM-RETIREMENT`, `TERM-ARCHIVE`, `TERM-REMOVAL`, `TERM-REGISTRY`, `TERM-TASK`, `TERM-RESOLVES`, `TERM-HARNESS`, `TERM-PROJECTION`, `TERM-EXCEPTION`, `TERM-UNVERIFIED`, `TERM-KEEP` and `TERM-RELEASE-OPERATION`.
  - Rows whose meaning differs take the 3.0.1 meaning, translated into English: `TERM-ARCHIVE`, `TERM-REMOVAL`, `TERM-PRERELEASE`, `TERM-BUILD-METADATA`, `TERM-CONTRACT-VERSION`, `TERM-REGISTRY-SCHEMA-VERSION`, `TERM-DOCUMENT-REVISION`, `TERM-BASELINE-NAMESPACE`, `TERM-PUBLIC-CONTRACT` and `TERM-COMPATIBILITY`. The last two move their owner to the version and identity rules of `document-authoring.md`.
  - `TERM-DRAFT` (owner: [document lifecycle](../../../.agents/governance/document-lifecycle.md)), `TERM-READINESS` (owner: [work lifecycle](../../../.agents/workflows/work-lifecycle.md)) and `TERM-DESIGN-FIT` (owner: [SDLC](../../../.agents/governance/sdlc.md)) are added.
  - `TERM-HISTORICAL-AUDIT` is removed.
  - Local Extensions rows take numeric versions (`1.0.0`, `1.1.0`); their contract identity is the Local Extensions table.
  - The Policy Owner cell keeps one owner-role name and its local link (D01: the link is a local binding).
  - The glossary `version` steps from 1.3.0 to 2.0.0, a MAJOR step, because a term is removed and meanings change.
- **Single author.** Each named rule keeps one author. The other place keeps only what it alone owns (for example the Claude-native facts in `.claude/provider.md`) and links to the owner. A retired rule keeps its row as `retired;` and is never made active again.
- **Records.**
  - `W01 3.0.1 Rule Fit` lists every governance rule judged not `KEEP_VERIFIED`, with verdict, reason, file and line, and one owning stage. It also lists the `KEEP_VERIFIED` rule IDs by file.
  - The lead text states how each rule's purpose, owner, consumer and enforcement are already explained: purpose by its body, owner by its file, consumer and enforcement by the Evidence column of its rule table. A named check is a mechanical control; `Semantic review` is not mechanically enforced.
  - The verdict is text-level: the evidence checks named in the rule tables are not run here, and the table says so.
  - `W00 Verdict Owner Corrections` moves W00 verdict row 9 (the REQ-0003 and AD-0006 recovery premise) from W01 to W04. PKG W04-CONTENT step 6 owns the conflicting history-recovery text in the 01 and 02 documents (R09), and Q07-CUTOVER (U55, R20) consumes it. Rows 10 and 11 stay with W04, because the same step owns Release re-introduction and always-full-check text. Row 10 is also consumed by W03-FORMS (U19, the Release document role), and the strict-command part of row 11 by W05 (U27).
  - The recorded W00 rows stay as written.
  - Neither table is a residue table.

### Failure and Edge Cases

- A glossary definition would copy a span of its owner: the knowledge validator refuses it, and the row is reworded.
- A glossary meaning differs from a current policy rule. The glossary carries the 3.0.1 meaning, the conflict is recorded in the rule-fit table under GOV-07 with its owner, and the policy is not changed here. The known pairs are: `TERM-PRERELEASE`, `TERM-BUILD-METADATA`, `TERM-CONTRACT-VERSION` and `TERM-DOCUMENT-REVISION` against AUTHOR-R015 (W03-VERSION); `TERM-ARCHIVE` and `TERM-REMOVAL` against AUTHOR-R013 and DOCLIFE-R008, R014, R015 and R019 (W04, consumed by Q07-CUTOVER).
- A link or anchor breaks: the link validator refuses it.
- Rollback before merge is deleting the branch; after merge, reverting the merge commit.

## Acceptance Criteria

### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| VAL-W01C-001 | The glossary matches vocabulary 3.0.1. Each common row's meaning matches the PKG row and has Contract Version `3.0.1`. The three new terms exist, `TERM-HISTORICAL-AUDIT` is gone, and every Contract Version is numeric. The knowledge validator passes. |
| VAL-W01C-002 | Each named duplicate has one author, and its other place links to it. EXEC-R012 is `retired;`. The governance and lifecycle validators pass, including the rule-ID history check. |
| VAL-W01C-003 | The two tables and the EVD row are appended to the SPEC-0161 Task. Every non-KEEP rule names one owning stage, and every W01 requirement ID has a disposition. The W01-H02 row and entry carry the new resume condition. No requirement is lowered, and the ledger gate passes at 57 entries. |
| VAL-W01C-004 | Each rule's purpose, owner, consumer and enforcement are explained, and the `KEEP_VERIFIED` IDs are listed. After WORK-002 no common rule is restated in a native provider note. Three violation cases, run on scratch copies, are refused: a retired EXEC-R012 made active (lifecycle rule-ID history), a duplicate glossary Term ID (knowledge validator), and a glossary owner link to a missing file (knowledge or link validator). |

### Evidence Requirements

- The three violation cases of VAL-W01C-004, on scratch copies outside the repository.
- Before and after: `scripts/validate-knowledge-surface.py`, `scripts/validate-agent-governance.py`, the four strict document validators and `scripts/validate-work-residue-ledger.py`.
- At commit: `python3 scripts/qa.py staged` through the hooks on the exact index.
- An independent review, because the risk class is `high` (governance policy and a provider note).
- Limits: repository-static only. No native runtime or hosted claim.

## References

### Normative and Evidence

- [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md), [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), [ADR-0058](../../02.architecture/decisions/0058-repository-vocabulary-in-knowledge-surface.md), the [glossary](../../../.agents/knowledge/glossary.md) and the governance policies under `.agents/governance/`.
- PKG inputs (read-only): `dependencies/repository-vocabulary.json` (`a8f595f5…`), D01 (`3141a458…`), D03 (`b65274c3…`), `current-requirements.json` (`3f011078…`), `original-requirements.json` (`42f2ef0d…`) and `revision-requirements.json` (`f8a08cea…`).

### Historical and Navigation

- [SPEC-0161](../0161-w00-v14-7-delta-intake/spec.md) holds the W00 3.0.1 record that this package corrects.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0032](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-W01C-001 | [ADR-0058](../../02.architecture/decisions/0058-repository-vocabulary-in-knowledge-surface.md) | Knowledge validator; row-by-row comparison with the PKG vocabulary. |
| [REQ-0003-FR-0030](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-W01C-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Governance and lifecycle validators; link check. |
| [REQ-0003-FR-0030](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-W01C-004 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Rule explanation read; three violation cases on scratch copies. |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-W01C-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Ledger gate; appended tables read against their sources. |
