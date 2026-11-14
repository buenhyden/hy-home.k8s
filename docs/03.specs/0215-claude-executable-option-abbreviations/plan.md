---
title: "Claude Executable Option Abbreviations Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0215-PLAN-0001"
parent_ids: ["SPEC-0215"]
---

# Claude Executable Option Abbreviations Implementation Plan

## Global Constraints

This work order follows the [Spec](spec.md) and inherits all of its boundaries. It adds three constraints:

1. Only the five prefix rules are appended. No existing allow, ask or deny rule is removed, reordered or weakened.
2. No test runs a push, fetch, pull, clone or ls-remote with an executable-carrying option, and no probe is routed around the session's permission layer.
3. No Markdown line in the package carries a literal push command, so the repository quality check passes.

## Overview

Write the failing regressions and the new pin first, then append the five rules to the tracked settings. Then correct the provider-note sentence and add the Stage 03 README entry. [Task 0001](tasks/tsk-0001-claude-executable-option-abbreviations.md) owns execution and evidence.

## Context

Read at `83d3f5c1`:

- **Settings and pin.** `.claude/settings.json` holds 29 allow, 2 ask and 257 deny rules. The exact-name executable-option denies sit at lines 223-225. `scripts/validate-agent-governance.py` pins the deny list from line 134 by ordered equality.
- **Finding.** On 2026-11-14 an automated security review found that unique long-option abbreviations bypass the exact-name denies once push is allowed, and rated the gap HIGH.
- **Option lists.** Git 2.43 `--help-all` for push, fetch, pull, clone and ls-remote gives the shortest unique prefixes the Spec lists.
- **SPEC-0214.** It is finished and accepted. `LIFECYCLE-PACKAGE-EXIT` R4 refuses edits to its Spec or Plan, so this package carries the fix.
- **Architecture.** AD-0006 applies, and nothing departs from it. The interfaces are the deny list, the validator tuple and the test module. Migration: none. Rollback: revert the implementation commit.

## Goals & In-Scope

- The five appended deny rules, their validator pin and failing-first regressions, with the guards and the over-denial.
- The corrected provider-note sentence and the Stage 03 README entry.
- The derivation basis, the over-denials and the configured-program residual, recorded once in the Spec.

## Non-Goals & Out-of-Scope

- Any other permission rule; pull and clone, which keep the default prompt; the Codex side; hooks; workflows; remote settings; any registry.
- The SPEC-0214 package, which is closed.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-EXECOPT-001](spec.md#success-criteria--verification-plan) | Write the failing decision regressions and append the five rules to the validator tuple, show the whole validator failing on the old settings, then append the five rules to the settings. | Spec and Plan approval. | [Task 0001](tasks/tsk-0001-claude-executable-option-abbreviations.md) | Failing then passing decision test and validator; the two unittest modules; ruff. |
| WORK-002 | [VAL-EXECOPT-002](spec.md#success-criteria--verification-plan) | Correct the provider-note sentence, add the Stage 03 README entry, and run the document and exact-index checks. | WORK-001. | [Task 0001](tasks/tsk-0001-claude-executable-option-abbreviations.md) | Strict document validators, the repository quality check, staged lifecycle check, exact-index QA and commit hooks. |

## Verification Plan

- Failing-first order:
  1. Change the decision test and run it against the old settings. Each new deny expectation fails.
  2. Change the validator tuple. The whole validator fails with `AGENT-NATIVE-PERMISSION` on the old settings.
  3. Change the settings. Everything passes.
- Architecture compliance: the work stays within AD-0006 and adds no component, gate or diagnostic. A departure returns the Spec to `in-review`.
- Commit and merge order: in the SPEC-0214 pull request, after the Spec and Plan approval receipts. Record the risk class `high` (a permission change), and list each changed rule in the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor).

- **An executable-carrying option runs through a form no rule denies.** Unlikely, Severe: MEDIUM, mitigate and record. Owner: platform. The prefixes come from the full `--help-all` option lists. A configured receive-pack or upload-pack program and a quoted or variable option stay residual. Review cue: a remote or configuration change that names a program.
- **A future Git option shares a denied prefix.** Possible, Minor: LOW, monitor. A new over-denial or a new ambiguity appears. Rerun the derivation when Git changes version.
- **Agents meet over-denial.** Possible, Minor: LOW, accept. A branch containing `--e` is refused on push; the agent renames the branch.
- **The client matches rules differently from the model.** Possible, Moderate: MEDIUM, monitor. The evidence is labelled repository-static.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance. The Spec leaves `draft` only with its approval receipt. No runtime claim is made from repository-static checks.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
