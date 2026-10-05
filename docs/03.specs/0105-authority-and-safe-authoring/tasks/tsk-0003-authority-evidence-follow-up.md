---
title: "Authority and Evidence Follow-up"
version: "0.2.0"
type: "sdlc/task"
status: "ready"
owner: "platform"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0105-TSK-0003"
parent_ids: ["SPEC-0105-PLAN-0001"]
---

# Task: Authority and Evidence Follow-up

## Overview

The current user's implementation request authorizes a bounded local follow-up
to completed [SPEC-0105](../spec.md). This Task owns the current investigation,
changes, actual check outcomes and handoff. The [Plan](../plan.md) assigns
WORK-006/007; the completed [original Task](tsk-0001-authority-and-authoring.md)
and [scanner follow-up](tsk-0002-quoted-secret-output.md) retain their results.
The work starts on `codex/p01-authority-evidence` in
`.worktrees/p01-authority-evidence` from clean `main` at
`9067729bf6679a0cd536362113be261056c32dd6`. The historical investigation
revision `2a03a5e03d6134542dc8c1d8eafc6b63e9f50fcb` is not a reset target.

## Inputs

- [Spec](../spec.md) VAL-P01-001/003/004/005/006 and [Plan](../plan.md)
  WORK-006/007. Current request: reconcile stale hosted guidance and P02
  closing evidence through local documentation changes, focused static checks,
  independent review and logical commits.
- `docs/03.specs/0106-stage99-lifecycle-normalization/` has completed
  Spec/Plan/Task records but its original EVD-P02-013 closing checks remain
  `NOT_RUN/pending`. A new current EVD-P02-014 must carry any actual recheck;
  the original outcome cannot be retrospectively promoted.
- The archived [SPEC-0103-TSK-0006](../../../98.archive/completed/03.specs/0103-qa-evidence-reuse/tasks/tsk-0006-integration.md#final-protected-host-disposition-2026-10-02)
  records hosted verifier/publisher success on 2026-10-02 at run
  `36967966896` over main SHA
  `997aa67d4a7ddb5dcdecf7048a68900155178231`; current remote settings and
  runs are outside this request. The [Archive Retention Catalog](../../../98.archive/README.md)
  routes that retained package. A repository
  workflow file or provider projection does not prove current hosted or native
  runtime state.
- The Stage 99 `sdlc/task` profile selects
  `docs/99.templates/templates/specs/task.template.md`. This Task is the
  canonical execution record; no new Spec, approval ledger or progress file is
  required. The owning Stage 03 README already routes to the SPEC-0105 package.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-006 | [VAL-P01-001](../spec.md#success-criteria--verification-plan), [VAL-P01-003](../spec.md#success-criteria--verification-plan), [VAL-P01-004](../spec.md#success-criteria--verification-plan), [VAL-P01-005](../spec.md#success-criteria--verification-plan) | Reconcile dated hosted evidence, current guide and P02 closing claims without changing approval or runtime authority | platform | ready | NOT_RUN | pending | Source comparison and EVD-P01-006 below |
| WORK-007 | [VAL-P01-006](../spec.md#success-criteria--verification-plan) | Validate the four authorized Task-lifecycle commits and obtain independent read-only review | platform | ready | NOT_RUN | pending | EVD-P01-007 and handoff below |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P01-006 | [VAL-P01-001](../spec.md#success-criteria--verification-plan), [VAL-P01-003](../spec.md#success-criteria--verification-plan), [VAL-P01-004](../spec.md#success-criteria--verification-plan), [VAL-P01-005](../spec.md#success-criteria--verification-plan) | WORK-006 | Dated source, consumer and authority comparison | Clean main `9067729b`; historical SPEC-0103 and current P02 records | NOT_RUN | [Verification Summary](#verification-summary) | pending |
| EVD-P01-007 | [VAL-P01-006](../spec.md#success-criteria--verification-plan) | WORK-007 | Exact index, completion, message and independent review | Pending logical index snapshots | NOT_RUN | [Verification Summary](#verification-summary) | pending |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/0105-authority-and-safe-authoring/spec.md`,
  `plan.md`, this Task;
  `docs/03.specs/0106-stage99-lifecycle-normalization/spec.md`, `plan.md`,
  its existing `tasks/tsk-0001-lifecycle-normalization.md`; and
  `.github/repository-surface.md`. The separately delegated doc-writer owns
  the Stage 03 records; wiki-curator owns the GitHub navigation update.
- **Forbidden Paths**: frozen Stage 98 bodies, shared governance rules,
  provider trust/native configuration, validators, schemas, workload manifests,
  secrets and private runtime state.
- **Approval Required**: the current user request authorizes these scoped
  reversible document changes, one local worktree, and read-only independent
  review. The owner subsequently clarified that four local logical commits
  may be used to traverse the new Task's legal `draft` → `ready` →
  `in-progress` → `completed` lifecycle. It grants no current hosted-state lookup,
  remote push/PR/merge, archive disposition, live action, secret access,
  destructive cleanup or worktree removal. An actual protected action requires
  the separate operator route in `.agents/governance/approval-and-safety.md`;
  a structural record, reviewer verdict or past hosted success cannot supply
  that authentication. Existing valid scoped authorization is reused.
- **Static Validation**: preflight selected tools and time/output limits;
  reconstruct the immutable P02 transition in isolated `/tmp` material;
  execute its exact three-path staged gates once and explicit-ref history
  check. Select affected gates but do not execute the affected lane. For each
  new logical index, inspect and run canonical exact-index staged checks,
  lifecycle `completion` on the final current Spec-anchor candidate only,
  actual commit-message validation and normal hooks. Earlier draft, ready
  and in-progress index states are not completion evidence. Obtain a distinct read-only review on the
  final diff. Prose changes need no invented RED/GREEN regression.
- **Live Validation**: DEFER; no remote or live observation is in scope.
- **Secret / Vault Handling**: no secret reads or output; use only redacted
  metadata and source paths.
- **Rollback Plan**: use a reviewed forward corrective commit on this branch
  if a documented claim needs repair; preserve existing Task and Git history.
- **Evidence Location**: this Task for P01 execution, and EVD-P02-014 in the
  current SPEC-0106 Task for its closing re-verification.

## Verification Summary

Initial source comparison, before editing, classifies the current concerns:

| Finding and class | Current owner and consumer | Source revision / lane | Authorization and disposition | Remaining / next owner |
| --- | --- | --- | --- | --- |
| Hosted activation `DEFER` wording is a stale fact after dated success | `.github/repository-surface.md` guides GitHub surface readers; SPEC-0103 Task holds original hosted evidence | SPEC-0103 at run `36967966896`, SHA `997aa67d…`; historical hosted lane | Update the guide to distinguish dated success from unobserved current remote state; static edit is authorized | Current remote state DEFER; repository operator if later needed |
| P02 closing language is an evidence gap, not a failed implementation | SPEC-0106 Task owns EVD-P02-013 and new EVD-P02-014; its Spec/Plan consume the current closing disposition | `9067729b` recorded prior handoff; new exact staged/index and review evidence pending | Preserve EVD-P02-013 `NOT_RUN/pending`; promote current prose only after new observed checks and review | doc-writer and quality-engineer, then read-only reviewer |
| Structural approval and provider projections may be mistaken for authenticated actor or runtime | `.agents/governance/approval-and-safety.md` and agent execution remain current owners; P01 Task records application | Current repository-static policy and current request; protected/live lane DEFER | Maintain distinct authoring, approval and native boundaries without changing shared policy | Operator for any protected action; provider owner for native observation |
| GitOps desired state, bootstrap assets, AWS/Azure examples and external runtime describe different scopes | Root README and their current repository owners; no contradictory consumer identified | `9067729b` repository-static inspection | Maintain existing separation; no live inference or unrelated edits | Corresponding runtime operator only if live verification is requested |

Commands, exact changed paths, tool identities, gate selections, outputs,
reviewer identity/findings, commit hashes, rollback and residual risks will be
appended only after observation. At intake the historical recheck, current
staged/completion/message checks and independent review are `NOT_RUN/pending`.
Affected execution and local full QA are `NOT_RUN` by the current scoped
request; they are not PASS evidence. Current remote and live state are `DEFER`
to the relevant operator. The initial draft claimed no delivery or acceptance.

### Readiness after the draft commit

The first authorized logical commit
`0625dfbeab0d751d347ca9e6e162740774c94410` has tree
`ad6d5170d129081174ec2e38a2f29da1811dcb6f` and four paths: this Task,
its Spec and Plan, and `.github/repository-surface.md`. The reviewed file
SHA-256 values in that order are
`6e9d43445000d5c9b02d1b6a15bfdba8d91ab214832c8afac186248916f6ec3c`,
`2ca18743f7a43dea01ed8193113dacae762940567c0a1add8824192b410bc558`,
`a887a468e6f997f99c71c302d6a4e62377000a55eb75e714bf2e0f036acb3354`,
and `c26f44bd31171dfb4dc6bb516c84d7137a7e972fb3901adde5f033f0c96f6aee`.
The independent read-only code-reviewer `/root/qa_release_survey` inspected
those exact files and the source contracts, reported PASS with no remaining
finding for the intake diff. This is intake review, not final acceptance.
The bounded runner invoked `/usr/bin/python3 -B scripts/qa.py staged
--base-ref HEAD --root <P01_WORKTREE>` on that exact index, where
`<P01_WORKTREE>` denotes the isolated P01 worktree in this tracked summary;
the scratch result retains the resolved command. It returned zero with six
of six selected gates PASS
(193.708 seconds, raw result in
`/tmp/hy-p01-phase1-qa-qlu1f8n_/staged.json`).
`git diff --cached --check` returned zero. The actual first message
`docs(governance): clarify authority evidence follow-up scope` passed pinned
Commitizen validation; normal `git commit -F` returned zero. These claims
describe only the draft index and first commit.

Readiness tool preflight at the new branch HEAD observed Python 3.12.3,
pre-commit 4.6.1 and Git 2.43.0. Repository `core.hooksPath` points to
`scripts/githooks`; its executable pre-commit/commit-msg entries delegate to
global and workspace hooks. Neither delegated workspace hook exists in the
common `.git/hooks`, and the global commit-msg hook is absent, so the first
commit's normal hook invocation is not evidence that the workspace
pre-commit or Commitizen hook executed. Explicit pinned message validation
and exact-index QA supply the corresponding local evidence. No hook,
trust or user configuration was changed. Resource and tool limits remain
those of the registered validation runner; no broad discovery or full QA is
scheduled. The separately observed P02 historical recheck awaits its current
Task evidence disposition; current completion and final review remain pending.

The first ready-only index `9af794945da425bd8f8aa5304ce87dd44ea880a4`
failed canonical staged QA after 196.005 seconds: five of six selected gates
passed, while `repository-quality` rejected an absolute local checkout path
written into this Task's command evidence. The result is FAIL for that
superseded index, not a reason to weaken the path rule. This revision writes
the command with a worktree placeholder and requires fresh exact-index QA
before a ready-state commit. The unchanged commit message already passed the
separate pinned Commitizen check, which does not validate document content.
