---
title: "Provider README Language and QA Tool Diagnostics"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0110"
---

# Provider README Language and QA Tool Diagnostics Technical Specification (Spec)

## Overview

This package continues the v9 execution prompt after
[SPEC-0108](../0108-task-status-and-provider-boundaries/spec.md). It
translates the eight provider-root READMEs left pending (K-P2), makes a
missing local style tool report its cause instead of withholding it (K-P5),
and records the K-P0, K-P3 and K-P5 findings that current files already
satisfy. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-provider-readme-and-qa-diagnostics.md) records it.

## Strategic Boundaries & Non-goals

- In scope: Korean bodies for `.agents/README.md`, the three evaluation
  READMEs, the knowledge and prompts routers and the Claude and Codex
  READMEs; an empty language `pending_paths`; explicit missing-module
  diagnostics in the selected style and nonstyle validators; the
  `scripts/README.md` fallback sentence.
- Kept without change, with the reason recorded in the Task: F02 (AGENTS.md
  is the registered Codex gateway and Claude never reads it), F05, F18,
  F22, F39 and F21 (skipping `style-pr` on a title-only edit would let a
  skipped required check mask an earlier failure).
- Non-goals: the shared memory store and native memory disablement, which
  stay with [SPEC-0109](../0109-shared-workspace-memory/spec.md); any remote
  ruleset or workflow change.

## Contracts

- Every README under `.agents/`, `.claude/` and `.codex/` passes its
  Korean-first profile and no language path stays pending.
- When the invoking interpreter cannot import `pre_commit`, the selected
  style and nonstyle validators fail with a stable `STYLE-TOOL` or
  `NONSTYLE-TOOL` label, and the lane runner passes that label through
  instead of "details withheld". The result stays FAIL.

## Core Design

A preflight `importlib.util.find_spec("pre_commit")` runs before any hook
execution. The lane runner's failure snippet admits a line that starts with
a fixed `STYLE-` or `NONSTYLE-` rule label followed by a colon, so a fixed
diagnostic reaches the result line while free-form tool output stays
withheld.

## Data Modeling & Storage Strategy

No stored data changes.

## Interfaces & Data Structures

- `scripts/validate-selected-style.py` and
  `scripts/validate-selected-nonstyle.py`: exit 2 with
  `STYLE-TOOL: pre_commit module unavailable to the invoking interpreter`
  or the `NONSTYLE-TOOL` equivalent.
- `scripts/run-validation-lane.py` `failure_snippet`: accepts the fixed
  label form `^(STYLE|NONSTYLE)-[A-Z-]+:` followed by a space, in addition
  to hook ids.

## Edge Cases & Error Handling

A present module that fails at run time keeps its existing hook diagnostics.
A translated README that later regains untranslated prose fails
`LANG-KOREAN-FIRST`.

## Failure Modes & Fallback / Human Escalation

Rollback is a forward revert. The documented validation environment in
`scripts/README.md` remains the supported way to run the style gates.

## Verification Commands

- `python3 -m unittest` on the named style, nonstyle and lane-runner tests.
- `python3 scripts/validate-markdown-profiles.py`
- `"$VALIDATION_VENV/bin/python" scripts/qa.py staged` per logical commit.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-PRQA-001 | The profile validator passes all eight translated READMEs with an empty `pending_paths`, and links and headings are unchanged. |
| VAL-PRQA-002 | Focused tests show a missing `pre_commit` module yields the fixed tool label through the lane runner while the gate still fails, and the staged QA run with the documented validation environment passes the style gates. |
| VAL-PRQA-003 | The Task records the keep decision, source lines and reason for F02, F05, F18, F21, F22 and F39 without changing those surfaces. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PRQA-001 | README purpose and language; profile validator. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PRQA-002 | A missing required tool fails with its cause; focused tests and staged QA. |
| [REQ-0003-FR-0030](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PRQA-003 | Hosted surfaces traced to consumers and kept; source review recorded in the Task. |
