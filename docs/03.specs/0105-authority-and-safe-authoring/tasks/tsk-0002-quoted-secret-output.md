---
title: "Quoted Secret Output Scanner Follow-up"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-10-04"
layer: "specs"
artifact_id: "SPEC-0105-TSK-0002"
---

# Task: Quoted Secret Output Scanner Follow-up

## Overview

The current user's explicit implementation request authorizes one bounded
follow-up to the completed SPEC-0105 implementation. Paired single- or
double-quoted `yaml`/`json` output values can miss the raw Secret command
scanner. This Task owns the follow-up state, observations and handoff; the
completed [prior Task](tsk-0001-authority-and-authoring.md) remains intact.

## Inputs

- [Spec](../spec.md) VAL-P01-002 and VAL-P01-006; [Plan](../plan.md) WP-002
  and WP-003.
- Intake snapshot: clean `codex/p01-authority-safety` at `d21f535`; current
  Secret rule in `scripts/validation/repository/quality.py` near line 2037 is
  consumed by the command scan near line 2139. Its inert-prohibition helper is
  also used by the direct-push scan. Existing focused regression owner is
  `tests/test_repository_quality_rules.py`.
- Independent read-only re-audit at that snapshot found this scanner gap.
  Approval and safety review found no new permission contradiction; the
  completed Spec/Plan may link a new authorized Task without reopening the
  completed prior Task. These findings identify work, not acceptance or
  authorization by the reviewers.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-004 | VAL-P01-002 | Reproduce and repair quoted Secret output matching in the shared rule; retain inert prose grammar | quality-engineer | Queued | Not executed | Source and consumer anchors in Inputs; focused failing/passing case pending |
| WORK-005 | VAL-P01-006 | Validate, obtain independent read-only review and commit local handoff | platform | Queued | Not executed | Exact-index, focused, affected, full and message checks pending |

## Approval and Safety Boundaries

- **Allowed Paths**: `scripts/validation/repository/quality.py`,
  `tests/test_repository_quality_rules.py`,
  `docs/03.specs/0105-authority-and-safe-authoring/spec.md`,
  `docs/03.specs/0105-authority-and-safe-authoring/plan.md` and
  `docs/03.specs/0105-authority-and-safe-authoring/tasks/tsk-0002-quoted-secret-output.md`
  only.
- **Forbidden Paths**: real Secret values, live state, remote repositories,
  native/provider trust settings, global configuration and frozen history.
- **Approval Required**: the user's current implementation request authorizes
  scoped reversible local authoring and logical commits. It grants no Secret
  read, live operation, remote push/PR/merge, archive disposition or destructive
  cleanup. The operator route in `.agents/governance/approval-and-safety.md`
  governs any separately protected action; none is planned here.
- **Static Validation**: demonstrate one failing quoted-output regression,
  then focused passing cases for `-o`/`--output` with space/equals and paired
  single/double quotes; retain raw-command rejection despite adjacent redaction,
  explicit inert Markdown prose allowance, runnable/comment denial, metadata
  jsonpath and ExternalSecret negatives. Run affected, exact-index staged and
  one final local full QA at the declared input snapshots. Validate each
  commit message through the current Commitizen contract.
- **Live Validation**: DEFER; no live command is authorized or needed.
- **Secret / Vault Handling**: synthetic command text only; no real Secret
  read, output or credential handling.
- **Rollback Plan**: forward corrective commit for the code/test change while
  preserving this Task and Git history; no reset or archive rewrite.
- **Evidence Location**: this Task alone owns actual commands, snapshots,
  results, review and residual limits.

## Verification Summary

Intake only. Root preflight observed Python 3.12.3, pre-commit 4.6.1, RTK and
CI-pinned Kustomize v5.8.1 still installed at `/usr/local/bin/kustomize`
with the digest recorded in the prior Task. The effective hooks path remains
`scripts/githooks`; the runner retains its existing bounded envelope.
The default shell sandbox failed to start with `bwrap: loopback: Failed
RTM_NEWADDR`; bounded supported escalation enabled read-only inspection.
Independent read-only intake reviewer `/root/approval_trace` found one LOW
path-clarity issue in Allowed Paths; the exact repository-relative paths above
resolve it, with no remaining intake finding reported. No focused regression,
implementation-diff review or commit has run for this follow-up at intake.
The superseded original-index staged QA was intentionally interrupted (exit
130) after the Task wording changed; it is not PASS evidence. The actual
`.git/COMMIT_EDITMSG` contains
`docs(governance): prepare quoted Secret output follow-up` and passed the
explicit pinned pre-commit Commitizen commit-msg check. Pre-commit stashed
and restored the unstaged Task without loss; its
observed hash matched. Final exact-index QA is pending. The planned order is
queued intake commit, in-progress implementation commit, completed closure
commit. Hosted CI, provider runtime and live behavior remain unobserved.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-004](../plan.md#work-breakdown) | Queued | VAL-P01-002 / WP-002; source and consumer anchors above |
| [WORK-005](../plan.md#work-breakdown) | Queued | VAL-P01-006 / WP-003; checks and review pending |
