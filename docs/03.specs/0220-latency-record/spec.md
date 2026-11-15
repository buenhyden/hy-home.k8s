---
title: "QA Latency Record"
version: "0.1.0"
type: "sdlc/spec"
status: "in-review"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0220"
---

# QA Latency Record Technical Specification (Spec)

## Overview

### Intent

This Spec records the actual latency comparison that the result section of every PKG 3.0.1 stage prompt (`_workspace/governance/workspace_governance_3_0_1_20261115/`, called PKG below) asks for. It also records the deletion of the session scratch clones that the SPEC-0161 `Q07 Target Preparation` table still lists. The consumer is W05-GATES, which owns the document-check bottleneck work (U27), and every reader of the SPEC-0161 Task. The [Plan](plan.md) orders the work and the [Task](tasks/tsk-0001-latency-record.md) records execution.

Measured on 2026-11-15, on this host, in a clone of `main` `e879e58e`, with the pinned `hyhome-validation` environment. Each case staged a one-sentence change to one file and timed `scripts/qa.py staged`:

| Case | Selected gates | Seconds | Result |
| --- | --- | --- | --- |
| Nothing staged | 0 | 13.8 | n/a |
| Ordinary document (`docs/90.references/README.md`) | 6 | 64.4 | PASS |
| Governance policy (`.agents/governance/model-selection.md`) | 9 | 69.3 | PASS |
| Stage 03 Task record (the SPEC-0161 Task) | 7 | 69.9 | PASS |

The full run is the one-time run of 16 registered checks recorded in the SPEC-0161 `W01 Follow-up Record`: about 1,198 s, 15 rc 0 and 1 rc 1. The scratch clones `negA`, `negB`, `negC` and `latency` were deleted by the user on 2026-11-15, and their absence was confirmed afterwards.

### Owning Requirements

[REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) (the record held by the Task) and REQ-0003-NFR-0002 (selected checks with their input and mode, without a blanket full sweep). [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view. This change conforms and amends neither.

## Scope

### In Scope

- In the SPEC-0161 Task:
  - an appended `QA Latency Record` table with three parts: the per-commit QA, the full run and the limits;
  - one correction row for target 6 of the `Q07 Target Preparation` table;
  - one EVD row;
  - the frontmatter `version` and `updated`.
- This package and the Stage 03 README entry.

Decision. On 2026-11-15 the user asked to record the commit QA, full run and limits content and to commit, push, open a PR and merge. Open question: none.

### Non-goals

- No change to code, tests, policy, the registry or the ledger. Reducing the measured latency is W05-GATES's (U27).
- No new measurement beyond the four cases above.

## Behavior Contract

### Normal Behavior

- **Commit QA.** The four cases above, with the gates each selected.
  - About 14 s of each run is fixed cost with nothing staged.
  - Three more gates (6 to 9) added about 5 s.
- **Full run.** About 1,198 s, 17 to 19 times one commit run.
  - The `document` suite (774.9 s) and the `qa-runner` suite (316.7 s) are 91 percent of it, and none of the three commit cases selected them.
  - This is the observed basis for not running the full suite on every Git event.
- **Limits.**
  - One run per case on one host, with no warm-up control and no hosted CI timing.
  - Changes under `scripts/` or `tests/` were not measured; they may select the contract suites.
  - The last eight checks of the full run may have read a tree in mid-edit, as the `W01 Follow-up Record` states.
- **Correction.** Target 6 (session scratch clones): `negA`, `negB` and `negC`, and the later `latency` clone, are deleted; none remains.

### Failure and Edge Cases

- A table copies a span of a governance policy: not expected, because it holds measurements only.
- Rollback before merge is deleting the branch; after merge, reverting the merge commit.

## Acceptance Criteria

### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| VAL-LAT-001 | The SPEC-0161 Task holds the `QA Latency Record` (commit QA, full run, limits), the target 6 correction and one EVD row. The four strict document validators and the ledger gate (41 entries) pass. |

### Evidence Requirements

- The four strict document validators, the ledger gate, and `python3 scripts/qa.py staged` through the hooks.
- Risk class `low` (records only): focused checks and the author's self-check (Q08).

## References

### Normative and Evidence

- [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md), [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) and the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md).

### Historical and Navigation

- SPEC-0218 and SPEC-0219 (exited) recorded the full run and the cutover targets.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LAT-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators and ledger gate; record read against the measurement. |
