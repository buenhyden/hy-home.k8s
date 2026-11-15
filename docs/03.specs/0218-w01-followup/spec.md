---
title: "W01 3.0.1 Follow-up"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0218"
---

# W01 3.0.1 Follow-up Technical Specification (Spec)

## Overview

### Intent

This Spec closes the gaps that a re-audit of the W01-CONTRACT prompt of the external workspace governance package 3.0.1 (`_workspace/governance/workspace_governance_3_0_1_20261115/`, called PKG below) found after SPEC-0217 merged. The consumers are the agents and the stage owners that read the governance policies, roles, workflows, skills, provider notes, the vocabulary form and the SPEC-0161 Task. The [Plan](plan.md) orders the work and the [Task](tasks/tsk-0001-w01-followup.md) records execution.

The re-audit on `main` at `c0af5a76` (2026-11-15) compared SPEC-0217's result with the W01 prompt and found the following:

- **Step 1 surfaces not audited.** SPEC-0217 audited only the ten governance policies. A read-only audit of roles, workflows, skills, provider notes and gateways found:
  - "skill invocation grants no authority", written in 17 skills and in `AGENTS.md`, with no canonical owner;
  - the progress-ledger prohibition, written in two workflows and four skills besides its owner (`context-and-memory.md` Objective);
  - the intake list, authored both in EXEC-R001 and in work-lifecycle Intake step 1;
  - three restatements in `.claude/provider.md`: line 21 (agent-execution Authority), line 30 (SAFE-R019) and lines 148 to 151 (SAFE-R018 shell confinement);
  - two role bodies that cite `.claude/provider.md` instead of SAFE-R018 for that rationale.
- **Step 3, docs99 machine owner.** The registry's vocabulary table (`docs/99.templates/registry.json` line 6685) and `vocabulary.template.md` define Policy Owner as a role with a backticked path. The glossary and D01 use a link, and only a link is mechanically checked: SPEC-0217 EVD-010 case C showed that the link validator refuses a missing owner path and that the knowledge validator does not check it.
- **Acceptance, "enforced or not".** SPEC-0217's rule fit was text-level. The checks named in the Rules tables were not run.
- **`UNVERIFIED` rows of the SPEC-0161 `W01 3.0.1 Rule Fit` table.**
  - SDLC-R016: the job names are confirmed in `ci.yml` lines 19 and 225, but its local-only QA content has the QUAL-R006 conflict.
  - AUTHOR-R017, AUTHOR-R022 and DOCLIFE-R007: `shared_contract` has five script consumers and `tests/test_shared_contract_binding.py`.
  - MODEL-R003: behavioural guidance with agents as its consumer.
- **Report items.** No actual latency comparison was made.

### Owning Requirements

PKG requirements GOV-06 (one canon, controlled projection), U12 (common governance apart from extensions), U13 (glossary owner) and R17 (policy revised with its consumers), all mapped to W01, and [REQ-0003-FR-0030](../../01.requirements/0003-workspace-agent-governance-platform.md). [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) and [ADR-0058](../../02.architecture/decisions/0058-repository-vocabulary-in-knowledge-surface.md) constrain the change. It conforms to both and amends neither.

## Scope

### In Scope

- `.agents/governance/agent-execution.md`:
  - EXEC-R005 states the canon: a role name or a skill invocation alone grants no write, delegation or approval.
  - EXEC-R001 points to work-lifecycle Intake step 1 instead of restating its list.
- The 17 `.agents/skills/*/SKILL.md` and root `AGENTS.md`: the skill-authority sentence links to EXEC-R005.
- `.agents/workflows/work-lifecycle.md` (lines 54 and 125), `.agents/workflows/delegated-development.md` (line 60), and the skills `docs-stage-conformance`, `execution-plan`, `task-breakdown` and `knowledge-map`: each progress-ledger prohibition links to [context and memory](../../../.agents/governance/context-and-memory.md#objective) instead of restating it.
- `.claude/provider.md`: lines 21, 30 and 148 to 151 keep only native facts and link to agent-execution Authority, SAFE-R019 and SAFE-R018.
- `.agents/roles/incident-responder.md` and `.agents/roles/observability-reviewer.md`: the rationale link points to SAFE-R018.
- `docs/99.templates/registry.json`: the vocabulary Policy Owner column meaning becomes "the owner role, linked with a relative Markdown link to its existing owner file".
- `docs/99.templates/templates/governance/vocabulary.template.md`: its author prompt and example row take the link form.
- The SPEC-0161 Task: an appended `W01 Follow-up Record` table, one EVD row, and its frontmatter `version` and `updated`. The table records:
  - four rule-fit corrections: SDLC-R016 to `CHANGE` (W06); AUTHOR-R017, AUTHOR-R022, DOCLIFE-R007 and MODEL-R003 to `KEEP_VERIFIED`;
  - the surface audit;
  - the executed evidence checks with exit codes and durations;
  - the latency comparison.
- This package, the Stage 03 README entry, reviewed `.secrets.baseline` entries, and the frontmatter versions of every edited file.

Decisions applied, not asked again: PKG `decisions.json` and the user's SPEC-0217 answers. W01-H02 stays open (user's choice of 2026-11-15). Open question: none.

### Non-goals

- No change to a rule's meaning beyond the EXEC-R005 canon sentence; no change to items owned by later stages.
- No validator, test or schema change; no ledger entry change.
- No write to `_workspace/`.

## Behavior Contract

### Normal Behavior

- **One canon.** Each named rule has one author.
  - A skill, workflow, role or provider note keeps a one-line, contextual reminder only as a link to the canon. This is the controlled reflection that GOV-06 allows for self-contained agent text.
  - Native facts (bindings, SPEC-0098, hook behaviour) stay in the provider note.
- **Vocabulary form.** The registry meaning and the template match the glossary's link form, and the link validator checks the owner path.
- **Executed evidence.** Each named check that is runnable locally runs once:
  - It is recorded with its registered command, exit code and duration, and the rules it backs move from "text-level" to "executed" for their mechanical part.
  - The `staged-qa`, `selected-style`, `commitizen` and `commit-message-exceptions` hooks are evidenced by this session's commit runs.
  - `Semantic review` rules stay not mechanically enforced, and the record says so.
- **Latency comparison.** Two cases are measured and recorded, with the limits of the comparison: the durations of the individual named checks, and the per-commit staged QA in the hooks.

### Failure and Edge Cases

- A projection or validator pins a sentence being edited: the governance or profile validator refuses it, and the edit takes the pinned form or the projection is regenerated by its owner.
- A link anchor is wrong: the link validator refuses it.
- A named check fails: the failure is recorded as is, and nothing in the Rules tables is marked executed for that check.
- Rollback before merge is deleting the branch; after merge, reverting the merge commit.

## Acceptance Criteria

### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| VAL-W01F-001 | The skill-authority, progress-ledger and intake rules each have one author. The other places link to it, and the provider note and two role bodies link to their canon. The governance, profile and link validators pass. |
| VAL-W01F-002 | The registry vocabulary meaning and the template use the link form. The contract registry, contract tests and links validators pass. |
| VAL-W01F-003 | The SPEC-0161 Task records the four corrections, the surface audit, the executed checks with exit codes and durations, and the latency comparison. The ledger gate passes at 57 entries. |

### Evidence Requirements

- The governance, knowledge, four strict document, ledger and document contract-test checks, before and after.
- `python3 scripts/qa.py staged` through the hooks on the exact index.
- An independent review, because the risk class is `high` (governance, provider note and registry).
- Limits: repository-static only.

## References

### Normative and Evidence

- [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md), [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), [ADR-0058](../../02.architecture/decisions/0058-repository-vocabulary-in-knowledge-surface.md) and the [glossary](../../../.agents/knowledge/glossary.md).
- PKG W01 prompt `prompts/W01-CONTRACT.md` (`091ed4dc…`), D01 (`3141a458…`) and `coverage.json`.

### Historical and Navigation

- SPEC-0217 (exited; summarized in REQ-0003 Archived Lineage) and the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md) `W01 3.0.1 Rule Fit` table.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0030](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-W01F-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Governance, profile and link validators. |
| [REQ-0003-FR-0032](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-W01F-002 | [ADR-0058](../../02.architecture/decisions/0058-repository-vocabulary-in-knowledge-surface.md) | Contract registry, contract tests and link validators. |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-W01F-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Ledger gate; record read against the run log. |
