---
title: "W00 3.0.1 Delta Intake"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0216"
---

# W00 3.0.1 Delta Intake Technical Specification (Spec)

## Overview

### Intent

This Spec records the W00-DELTA intake of the external workspace governance package 3.0.1 of 2026-11-15 (`_workspace/governance/workspace_governance_3_0_1_20261115/`, called PKG below) in the existing W00 Task, the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md). It is records only. The consumers are the stage owners W01 to W11 and Q07, which read the verdicts at their own intake. The [Plan](plan.md) orders the work and the [Task](tasks/tsk-0001-w00-3-0-1-delta.md) records execution.

A read of `main` at `003b8350` on 2026-11-15 found the following. PKG replaces the r1 package as the current input. Its `tools/validate_package.py --root .` reports no error, and every input hash this Spec names equals the PKG `manifest.json` value. The PKG W00-DELTA prompt asks for a design summary in the existing Task and a verdict for each requirement (`KEEP_VERIFIED`, `CHANGE`, `REPLACE`, `REMOVE` or `UNVERIFIED`), with the read scope of each. The SPEC-0161 Task holds the v14.7 and r1 edition records and no 3.0.1 record. The local base equals the SHA that PKG observed (`repository-observations.json` E01 to E09, E17 and E18; `workspace-profiles.json` profile `k8s`). So PKG's observation and the tree do not differ; the differences are between the current requirements and the tree.

### Owning Requirements

[REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) (residue and handoff records) and [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) (evidence lanes kept apart). [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view and [ADR-0060](../../02.architecture/decisions/0060-work-residue-ledger-amendment.md) the ledger. This change conforms to both and changes neither: the two tables are analysis, not residue and not a progress record.

## Scope

### In Scope

- In the SPEC-0161 Task: two appended tables, `3.0.1 Edition Delta` and `3.0.1 Verdicts`, under Results after `W04 Entry Statement`; one appended EVD row; and the frontmatter `version` and `updated`.
- This package and its list entry in the Stage 03 README.
- Reviewed `.secrets.baseline` entries for the new digests, if the secret scan flags them.

Decision. On 2026-11-15 the user answered the write-route question of the W00-DELTA intake with "New small package (Recommended)". That means a branch with this Spec and Plan that add the 3.0.1 record to the SPEC-0161 Task and nothing else. Work stops for Spec and Plan approval before the Task is edited. A commit or PR is made only on the user's request.

Settled by the sources and not asked:

- The confirmed decisions Q01 to Q10 and Q-DRAFT of PKG `decisions.json` are applied, not asked again.
- Historical audit questions (OPEN-01 to OPEN-04, OPEN-06 and W00-H01) are not reactivated. Their live rows stay as recorded (PKG W00-DELTA step 5).
- A `CHANGE` row that a live row already carries gets no new row. A `CHANGE` row that no live row carries is named to the one stage whose PKG prompt carries it (`prompts/README.md`, `reports/continue-k8s.md`). That stage takes it in at its own intake, as the r1 record did for other prompts. No ledger entry is seeded.

Open question: none.

### Non-goals

- Any write to `_workspace/`. PKG is read-only input and is not copied into the tree.
- Any rewrite of a recorded row or cell of the SPEC-0161 Task.
- Any ledger entry or live `Residue Handoff` row.
- The work of the `CHANGE` rows: REQ-0003, AD-0006, `quality.md`, the 05 and 90 READMEs and the lifecycle policy.
- W01 to W11, Q07, other repositories and hosted CI.

## Behavior Contract

### Normal Behavior

- **3.0.1 Edition Delta.** Columns Input, SHA-256 and Effect. Rows:
  - the PKG root and `manifest.json` (`22f93d73…`; package version 3.0.1, built 2026-11-15);
  - the W00-DELTA prompt (`8e761f7b…`);
  - D00 (`e2f3e4f9…`), D15 (`6721e7a1…`) and D17 (`c78a57d1…`);
  - `decisions.json` (`52c46c3d…`), `pr-observations.json` (`0b3e5185…`), `repository-observations.json` (`7c73b0bc…`) and `workspace-profiles.json` (`efa9d04f…`);
  - `external-research.md` (`ed505da9…`);
  - the two input archives that `input-provenance.json` names (named only; they are not on disk).

  Full hashes are taken again at implementation. The r1 root stays on disk and is no longer the current input.
- **3.0.1 Verdicts.** Columns No., Item, Verdict, Read scope, Evidence, Owner and Carried by. The first column is a running number, never a residue ID. The heading contains neither "Handoff" nor "Conflicts". Each row has one owner stage. Read scope is `listed`, `partial read` (named lines), `read` or `executed`. The rows expected at draft are below; they are observed again at implementation.

| No. | Item | Verdict | Owner | Carried by |
| --- | --- | --- | --- | --- |
| 1 | Base `003b8350` equals `origin/main` and the PR #283 merge commit; the PR #283 hosted checks | `KEEP_VERIFIED` | none | none |
| 2 | Project-Template PR #202 merged into `dev` (`c2dba0d7`); another repository, observation only | `KEEP_VERIFIED` | none | none |
| 3 | W03 closed by PR #283. Its remaining residue is held by 57 open ledger entries with owners from W00 to W11 and Q07. W03 is not run again | `KEEP_VERIFIED` | W00 | the 57 live rows, each with its own owner |
| 4 | Registry `schema_version` 20.0.0 with the Requirement `draft` state; the removed per-profile H2 lists are not restored | `KEEP_VERIFIED` | none | none |
| 5 | Spec and Plan `draft` authority: `DOCLIFE-R001` (draft states unreviewed intent; approval comes before dependent execution) | `KEEP_VERIFIED` | none | none |
| 6 | Q-DRAFT for a Requirement: no rule was found that refuses implementation, operation or completion on a draft Requirement alone | `CHANGE` | W04 | W04-LIFECYCLE prompt |
| 7 | REQ-0003-FR-0017 and the `quality.md` hosted lane: purpose, unit and content QA run locally; hosted CI runs metadata and style only | `CHANGE` | W06 | `CI-SCOPE` |
| 8 | REQ-0003 Scope: full transcripts are not stored | `CHANGE` | W08 | W08-CAPTURE prompt |
| 9 | REQ-0003-FR-0020 and AD-0006: exact Git-history recovery as a disposition premise, against Q10 | `CHANGE` | W01 | W01-CONTRACT prompt |
| 10 | 05 README: conditional re-adoption of the `operation/release` document, against the removed Release document role | `CHANGE` | W04 | W04-CONTENT prompt |
| 11 | 90 README: the Git-history recovery premise, and whole-tree strict commands for a small reference change | `CHANGE` | W04 | W04-CONTENT prompt |
| 12 | Shared memory search, recall, provenance and permission (`scripts/workspace_memory.py`) | `UNVERIFIED` | W08 | W08-RETRIEVAL prompt |
| 13 | Native hooks, capture and live deny (`.claude/settings.json`) | `UNVERIFIED` | W07 | `AGENT-04` |
| 14 | Reviewer boundary: the reviewer does not run validators again (`.agents/roles/code-reviewer.md`) | `UNVERIFIED` | W10 | W10-REVIEW prompt |

  The Read scope and Evidence columns are filled in at implementation from the observation made then. `REPLACE` and `REMOVE` have no row at draft, and the table says so. A row read only through PKG's observation is `UNVERIFIED`, never `KEEP_VERIFIED`. No row lowers a requirement to match the tree.
- **EVD row.** One appended EVD row (the next free number; `EVD-132` at draft) records the two tables, their inputs and the read scope. `Required` is no. It accepts no criterion and closes no residue.
- No schema, registry, code or ledger change. The ledger keeps 57 entries. The gate `scripts/validate-work-residue-ledger.py --root .` is an unchanged consumer.

### Failure and Edge Cases

- `main` moves before implementation: read the base, PR state and ledger count again and update the rows that changed.
- A PKG file differs from its `manifest.json` hash: stop and record it; no row is written from that file.
- A `CHANGE` row turns out to be carried by a live row not named here: the Carried by cell names that row.
- A current document contradicts a row: the author stops and asks, and does not edit the document.
- Rollback before commit is deleting the branch; after commit, it is reverting the commit.

## Acceptance Criteria

### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| VAL-W00D-001 | The two tables and the EVD row are appended to the SPEC-0161 Task. Each hash is read again from its file. Each verdict row names its read scope and one owner. No `KEEP_VERIFIED` row rests on an unread file, and no requirement is lowered. No recorded row or cell is rewritten. The ledger is unchanged and its gate passes. The strict document validators give equal results before and after. |

### Evidence Requirements

- In PKG: `python3 -I tools/validate_package.py --root .`, and `sha256sum` of the named inputs.
- The four strict document validators and `python3 scripts/validate-work-residue-ledger.py --root .`, before and after; equal diagnostics.
- When a commit is requested: `python3 scripts/qa.py staged` and the commit hooks on the exact index.
- Limits: repository-static and read-only. No native hook, live cluster or hosted CI run is claimed.

## References

### Normative and Evidence

- [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md), [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), [ADR-0060](../../02.architecture/decisions/0060-work-residue-ledger-amendment.md), the [document lifecycle policy](../../../.agents/governance/document-lifecycle.md) and the [work residue ledger](../work-residue-ledger.json).
- PKG, read-only and git-ignored; it is identified by the hashes above.

### Historical and Navigation

- [SPEC-0161](../0161-w00-v14-7-delta-intake/spec.md) holds the earlier v14.7 and r1 records. SPEC-0213 (r1 intake) left the tree; Git history recovers it.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-W00D-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Ledger gate unchanged; appended tables read against their sources. |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-W00D-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Read scope and evidence lane recorded for each verdict row. |
