---
title: "Authority and Evidence Follow-up"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
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
| WORK-006 | [VAL-P01-001](../spec.md#success-criteria--verification-plan), [VAL-P01-003](../spec.md#success-criteria--verification-plan), [VAL-P01-004](../spec.md#success-criteria--verification-plan), [VAL-P01-005](../spec.md#success-criteria--verification-plan) | Reconcile dated hosted evidence, current guide and P02 closing claims without changing approval or runtime authority | platform | completed | PASS | accepted | [Historical P02 candidate recheck](#historical-p02-candidate-recheck) and EVD-P01-006 below |
| WORK-007 | [VAL-P01-006](../spec.md#success-criteria--verification-plan) | Verify local delivery inputs and record lifecycle handoff | platform | completed | PASS | accepted | [Local handoff evidence](#local-handoff-evidence) and EVD-P01-007 below |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P01-006 | [VAL-P01-001](../spec.md#success-criteria--verification-plan), [VAL-P01-003](../spec.md#success-criteria--verification-plan), [VAL-P01-004](../spec.md#success-criteria--verification-plan), [VAL-P01-005](../spec.md#success-criteria--verification-plan) | WORK-006 | Dated source, consumer and authority comparison | Base `9067729b`; SPEC-0103 hosted record; SPEC-0106 EVD-P02-014 and phase3 tree `7aea4f72807765619de08f83efc9d8b459cd9702` | PASS | [Historical P02 candidate recheck](#historical-p02-candidate-recheck) | accepted |
| EVD-P01-007 | [VAL-P01-006](../spec.md#success-criteria--verification-plan) | WORK-007 | Local exact-index, completion, message and independent review | Draft tree `ad6d5170…`, ready tree `60ef9139…`, phase3 tree `7aea4f72…`, P02 prose tree `6771b01e…`, intermediate tree `1cabc737…` | PASS | [Local handoff evidence](#local-handoff-evidence) | accepted |

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
  review. The owner subsequently clarified that at least four local logical
  commits may be used to traverse the new Task's legal `draft` → `ready` →
  `in-progress` → `completed` lifecycle. A fifth local commit is needed after
  the observed row-edge refusal, because WORK-007 must also pass through a
  committed `in-progress` row. It grants no current hosted-state lookup,
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

The repaired Task-only ready index `60ef913901dfa9addb85e373ef18e006ae034546`
passed all six canonical staged gates in 194.290 seconds; its unchanged
Commitizen message remained valid. Independent read-only reviewer
`/root/qa_release_survey` inspected the repaired Task SHA-256
`945ccae3201195b68eebf9df229eb39c822c94da541c95cd0a30dabbf67ffc46`
and reported no remaining finding. Normal Git commit created
`1952642af8be9cc84353ea978d44cd897d11cba9` from that exact tree.
This ready-only result establishes neither final P01 acceptance nor current
P02 closing validation.

### Historical P02 candidate recheck

The historical three-document recheck, its initial scratch setup failure,
the repaired staged PASS, explicit-ref PASS, retrospective message PASS and
affected selection belong to
[SPEC-0106 EVD-P02-014](../../0106-stage99-lifecycle-normalization/tasks/tsk-0001-lifecycle-normalization.md#p01-follow-up-recheck).
This P01 Task consumes that source evidence for WORK-006; it does not turn
the prior EVD-P02-013 into a past PASS. Current changed-index completion and
final read-only review were subsequently performed on the phase3 index above:
six staged gates passed, SPEC-0106-only lifecycle completion passed, the
actual message passed pinned Commitizen, and independent read-only reviewer
`/root/qa_release_survey` reported no blocking finding on those exact bytes.
Normal local commit `e85d6557b71e84adaefa9dfc4ac5ad0b553fec54`
recorded the correction. The P02 Task owns the commands, hashes and limits.
This accepts WORK-006 and EVD-P01-006 for the dated source and current local
P02 evidence only. Current remote state, authenticated operator approval and
native/runtime activation remain `DEFER` to their existing owners. WORK-007
and EVD-P01-007 still await final local handoff checks and review.

The subsequent P02 acceptance-prose index
`6771b01e58fdf02b263c64c1481ec990ccf15374` passed six of six staged
gates in 196.226 seconds. SPEC-0106-only completion returned PASS with
`INDEX-SNAPSHOT` SHA-256
`e65c32e3d74cc875eab4895c51bb50c0299ee391502a1ac5951ac4f086bbf719`.
The final intended message
`docs(governance): complete P01 evidence follow-up` passed pinned Commitizen;
its file SHA-256 is
`dd69367b7785b4fa37c0a4ba8a188af86693a61e9fe45b7fa4f0a0f784441dd1`.
The independent reviewer identified the need to verify changed P02 prose on
its own index, and the P02 Task owns that result. WORK-007 remains
`in-progress/NOT_RUN/pending` until its terminal index and review are observed.

An isolated prospective terminal index at branch HEAD
`e85d6557b71e84adaefa9dfc4ac5ad0b553fec54` and tree
`514d0e53b1311db6c0ba54012ab5c08338d7ea13` failed the registered
staged lane after 198.296 seconds: five
of six gates passed, while `document-lifecycle` rejected
`TASK-ITEM-EDGE WORK-007: ready -> completed`. The source row in committed
HEAD was `ready`; the later uncommitted `in-progress` row could not supply a
historical transition. This is a real required-gate FAIL for that abandoned
proposal, not a PASS for the current source. Its stdout SHA-256 is
`97e08e0751812d52fcc00eb704c1245e4a2488330a686d1be25cbfec7d5d7107`
at `/tmp/hy-p01-final-proposal-OIXvGSSq/staged.stdout`.
The Task remains in-progress.
The next local index records the intermediate WORK-007 row and preserves
EVD-P01-007 as `NOT_RUN/pending`. No Registry edge, validator or history is
changed to evade the result.

The intermediate legal row-state index
`1cabc737e5e0e43cf00a8654a3815b3118650c80` passed all six canonical
staged gates in 201.874 seconds, stdout SHA-256
`5c4a7192d6dd0a22348eb80301baa854040813939aa2cb4bd4c34bcdf3264fec`.
SPEC-0106-only completion on that same input returned PASS with
`INDEX-SNAPSHOT` SHA-256
`acef3cb95b7de576669849c830fde7d774d193f2578d5bbc39d46b275ea1bf2c`.
The actual message `docs(governance): advance P01 handoff verification`
passed pinned Commitizen; independent read-only reviewer
`/root/qa_release_survey` reported PASS with no blocking finding. Normal
local commit `eb2de6c666f543e844eda13ddf4c713a9c196fbd` preserved the
WORK-007 `in-progress` row. The terminal Task source bytes require their own
exact-index checks and independent review before local commit; no later
result or commit OID is asserted in this Task.

### Local handoff evidence

The authorized Task states followed direct Registry edges: draft in
`0625dfbeab0d751d347ca9e6e162740774c94410`, ready in
`1952642af8be9cc84353ea978d44cd897d11cba9`, and in-progress in
`e85d6557b71e84adaefa9dfc4ac5ad0b553fec54` and
`eb2de6c666f543e844eda13ddf4c713a9c196fbd`. This terminal Task state
records acceptance of the observed local source and handoff inputs. The
first ready-only index FAIL and repaired PASS, initial scratch setup FAIL and
corrected P02 PASS, and prospective illegal row-edge FAIL remain documented
above and in the P02 Task. The phase3, P02 acceptance-prose and intermediate
index checks passed as individually recorded. The intended terminal message
`docs(governance): complete P01 evidence follow-up` passed its separate
pinned Commitizen check on unchanged bytes.

Affected execution and local full QA remain `NOT_RUN` by the scoped request;
the selected affected gates were recorded without executing that lane.
No remote settings or hosted runs were re-read, so current hosted activation
is `DEFER` to the repository operator. Native provider delivery, actual
approval authentication, cluster, cloud, Vault and external runtime remain
unobserved; their existing owners retain those actions. No archive
disposition, push, PR, main integration or worktree cleanup is claimed.
The configured `scripts/githooks` chain was preserved, but the delegated
workspace pre-commit and commit-msg hooks were absent; their execution is
not claimed. Rollback is a reviewed forward corrective commit on this
retained feature branch, preserving historical Task results and the
five-commit lifecycle.
