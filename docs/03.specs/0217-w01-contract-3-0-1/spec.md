---
title: "W01 3.0.1 Governance Contract Fit"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
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
- `.agents/governance/agent-execution.md`: EXEC-R004 and EXEC-R006 reduced to their common rule with a link to the owner; EXEC-R012 retired (`retired;` row kept, ID never reused).
- `.agents/governance/document-authoring.md`: the AUTHOR-R007 sentences on the single status marker and `not-required` replaced by a link to DOCLIFE-R003 and DOCLIFE-R009.
- `.claude/provider.md`: the `read-only-evidence` bullet keeps the Claude-native facts and links to SAFE-R018 for the common meaning.
- The SPEC-0161 Task: an appended `W01 3.0.1 Rule Fit` table, an appended `W00 Verdict Owner Corrections` table, one EVD row, and its frontmatter `version` and `updated`.
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

W01-H02 (the "rule_id binding" seeded from the r1 package) has no basis in the current requirements: U13 fixes only the seven columns, definition, owner and numeric version, and the W05 prompt reads no binding. Q04 forbids hiding unfinished work by deletion and requires an explicit per-item approval to withdraw, so W01-H02 stays open and non-blocking. Its Residue cell records the missing basis, and withdrawing it waits for the user's separate decision.

Open question: none that changes a criterion.

### Non-goals

- No change to the rules recorded for other owners in the table above, to any validator or test, to the registry, or to the work residue ledger entries.
- No change to `.codex/`, which holds no copy of SAFE-R018.
- Any write to `_workspace/`.

## Behavior Contract

### Normal Behavior

- **Vocabulary contract.**
  - Every common row whose meaning matches 3.0.1 keeps its English text and takes Contract Version `3.0.1`.
  - Rows whose meaning differs take the 3.0.1 meaning, translated into English: `TERM-ARCHIVE`, `TERM-REMOVAL`, `TERM-PRERELEASE`, `TERM-BUILD-METADATA`, `TERM-CONTRACT-VERSION`, `TERM-REGISTRY-SCHEMA-VERSION`, `TERM-DOCUMENT-REVISION`, `TERM-BASELINE-NAMESPACE`, `TERM-PUBLIC-CONTRACT` and `TERM-COMPATIBILITY`. The last two move their owner to the version and identity rules of `document-authoring.md`.
  - `TERM-DRAFT`, `TERM-READINESS` and `TERM-DESIGN-FIT` are added.
  - `TERM-HISTORICAL-AUDIT` is removed.
  - Local Extensions rows take numeric versions (`1.0.0`, `1.1.0`); their contract identity is the Local Extensions table.
  - The Policy Owner cell keeps one owner-role name and its local link (D01: the link is a local binding).
- **Single author.** Each named rule keeps one author. The other place keeps only what it alone owns (for example the Claude-native facts in `.claude/provider.md`) and links to the owner. A retired rule keeps its row as `retired;` and is never made active again.
- **Records.**
  - `W01 3.0.1 Rule Fit` lists every governance rule judged not `KEEP_VERIFIED`, with verdict, reason, file and line, and one owning stage, plus a count of `KEEP_VERIFIED` rules per file. The verdict is text-level: the evidence checks named in the rule tables are not run here, and the row says so.
  - `W00 Verdict Owner Corrections` moves W00 verdict rows to their primary owners: row 9 to Q07-CUTOVER; row 10 to W03-FORMS; row 11's recovery part to Q07-CUTOVER and its strict-command part to W05.
  - The recorded W00 rows stay as written.
  - Neither table is a residue table, and the ledger keeps 57 entries.

### Failure and Edge Cases

- A glossary definition would copy a span of its owner: the knowledge validator refuses it, and the row is reworded.
- A glossary meaning (for example `TERM-PRERELEASE`) differs from a current policy rule (AUTHOR-R015): the glossary carries the 3.0.1 meaning, the conflict is recorded in the rule-fit table under GOV-07 with its owner (W03-VERSION), and the policy is not changed here.
- A link or anchor breaks: the link validator refuses it.
- Rollback before merge is deleting the branch; after merge, reverting the merge commit.

## Acceptance Criteria

### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| VAL-W01C-001 | The glossary matches vocabulary 3.0.1. Each common row's meaning matches the PKG row and has Contract Version `3.0.1`. The three new terms exist, `TERM-HISTORICAL-AUDIT` is gone, and every Contract Version is numeric. The knowledge validator passes. |
| VAL-W01C-002 | Each named duplicate has one author, and its other place links to it. EXEC-R012 is `retired;`. The governance and lifecycle validators pass, including the rule-ID history check. |
| VAL-W01C-003 | The two tables and the EVD row are appended to the SPEC-0161 Task. Every non-KEEP rule names one owning stage. No requirement is lowered, and the ledger gate passes at 57 entries. |

### Evidence Requirements

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
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-W01C-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Ledger gate; appended tables read against their sources. |
