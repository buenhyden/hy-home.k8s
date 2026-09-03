---
title: 'Agent Governance Program Closure Implementation Plan'
version: "1.0.0"
type: sdlc/plan
layer: "specs"
status: done
owner: platform
updated: 2026-08-01
artifact_id: "SPEC-0046-PLAN-0001"
---

# Agent Governance Program Closure Implementation Plan

## Overview

This Plan executes
[Spec 046](./spec.md) as the
final repository-local closure tranche. It activated the reciprocal execution
path, implemented one closed closure contract, routed it through local QA/CI,
ran independent whole-branch review, and closed the reciprocal terminal
documents through AGPC-004. The terminal commit observation remains a separate
AGPC-004 postflight. The AGPC-005 Task row archives local `main` integration
and isolated-worktree cleanup into the post-terminal root finishing handoff;
those actions remain planned and unexecuted.

## Context

Spec 045 closed at
`de9a88e4550b87542eb7221c5ae7416fe5075763` with sole parent
`ed89228546501dd11a7f4abad28e8ebb094fbd97`; postflight
`060396112abaddbbcf79a33c8a04ae775cce66a1` observed that edge. The fixed
provider/model/source cutoff remains `2026-07-10T10:00:00+09:00` /
`2026-07-10T01:00:00Z`.

Specs 041-045 closed repository-static harness, provider-source, loop/memory,
12-role/48-adapter readiness, and CI/QA controls. They did not observe provider
runtime/auth/model discovery, current hosted CI or branch protection, actual
evaluation/admission/promotion, remote execution, or live platform state.

### Legacy Task ledger inputs

This Task is the canonical execution-evidence owner for Spec 046 activation,
closure-contract implementation, QA routing, final independent review,
reciprocal closure/postflight, local `main` merge, and isolated-worktree
cleanup.

AGPC-004 completed the terminal document transition in observed commit
`0a9e10324b552079fdd212683570e08a19878376`, whose sole parent is
`e84393af5d6196ec352307b3af21b3790e108794`. This separate postflight binds
that observation without inventing the postflight commit's own SHA. The
AGPC-005 row is `Archived`: it transfers still-unexecuted local `main`
integration and worktree/branch cleanup to the post-terminal root finishing
handoff. Accordingly, those actions remain planned operational evidence rather
than completed evidence in this terminal Task.

Provider runtime/auth/model discovery, hosted CI, branch protection, remote
execution, live platform state, actual evaluation/admission/promotion, and
actual model fitness remain separate `DEFER` or `ABSENT` lanes unless a later
approved action observes them.

- Parent [Spec 046](./spec.md)
- Parent [Implementation Plan](./plan.md)
- [PRD 003](../../../../01.requirements/0003-workspace-agent-governance-platform.md),
  [AD 0006](../../../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md),
  and [ADR 0019](../../../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- Spec 045 closure `de9a88e4550b87542eb7221c5ae7416fe5075763`,
  sole parent `ed89228546501dd11a7f4abad28e8ebb094fbd97`, and observed
  postflight `060396112abaddbbcf79a33c8a04ae775cce66a1`
- Fixed cutoff `2026-07-10T10:00:00+09:00` /
  `2026-07-10T01:00:00Z`
- Observed Spec 046 activation
  `c6bae0227acd3e4f57b591c14a88e31b6f2e553f` with sole parent
  `060396112abaddbbcf79a33c8a04ae775cce66a1`
- Observed ADR-0019 and program-design activation
  `ff66dd933e00def085b4c0319a67c6651356b116`
- Observed AGPC-003 evidence commit
  `666e814a65303fe297cf07fab4112720bea62f0a`
- Observed AGPC-004 terminal commit
  `0a9e10324b552079fdd212683570e08a19878376` with sole parent
  `e84393af5d6196ec352307b3af21b3790e108794`
## Goals & In-Scope

- Activate reciprocal Spec 046, Plan, Task, indexes, lineage, and progress.
- Add the closure contract, schema, positive fixture, validator, self-test, and
  focused unit tests.
- Keep repository-static/local PASS non-transitive across external lanes.
- Reconcile 12/48 roster, provider canaries, model/reasoning configuration, and
  the four memory classes without reading private state.
- Route one closure owner through validation surfaces, pre-commit, CI, and
  script/test documentation.
- Complete local QA and independent review, close reciprocal terminal
  documents, then hand terminal-commit observation to the separate AGPC-004
  postflight and archive local merge/cleanup into the post-terminal root
  finishing handoff.

## Non-Goals & Out-of-Scope

- No provider login, credential inspection/change, authenticated canary, or
  provider-local memory read.
- No hosted workflow dispatch, branch-protection mutation, push, PR, remote
  merge, release, paid action, or live cluster mutation.
- No actual evaluation, admission, model-fitness, threshold, or promotion PASS
  claim without separately observed evidence.
- No reading ignored checkpoint content, auth files, tokens, shell history,
  transcripts, provider response bodies, or secret values.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| AGPC-000 | Activate reciprocal Spec 046 execution path | Spec 045 closure/postflight | Clean branch worktree | Exact eight-file Spec/Plan/Task/index/profile/progress activation is active and validated |
| AGPC-001 | Implement closure contract package | AGPC-000 | Current contract/schema/test patterns are reviewed | Contract, schema, fixture, self-test, validator, and focused tests pass |
| AGPC-002 | Route the gate and reconcile evidence owners | AGPC-001 | Closure validator passes | Validation surfaces, CI/QA, inventories, implementation map, catalog, and provider notes point to one owner |
| AGPC-003 | Run final QA and independent reviews | AGPC-002 | Focused and routed gates pass | Affected/staged/all-files/aggregate/diff gates pass and reviewers approve |
| AGPC-004 | Close reciprocal documents and hand off observed postflight | AGPC-003 | No open findings or formatter mutation | Terminal document work is complete without self-SHA preclaim; a separate postflight observes the commit |
| AGPC-005 | Transfer local branch finish to the post-terminal root handoff | AGPC-004 | Terminal Task must contain no pending row | Task row is archived with explicit planned/unexecuted local merge and cleanup evidence |

## Verification Plan

```bash
python3 scripts/validate-agent-governance-closure.py --root . --self-test
python3 scripts/validate-agent-governance-closure.py --root .
python3 -m unittest tests/test_validate_agent_governance_closure.py
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-agent-provider-canaries.py --root .
python3 scripts/validate-agent-loop-lifecycle.py --root .
python3 scripts/validate-agent-roster-admission.py --root .
python3 scripts/validate-agent-evaluations.py --root .
python3 scripts/validate-agent-model-fitness.py --root .
python3 scripts/validate-agent-governance-ci.py --root .
python3 scripts/validate-agent-legacy-cutover.py --root .
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
git diff --check
```

AGPC-001 owns the first three commands. Other commands retain their existing
repository-static or local-validation evidence class and cannot establish an
external/runtime PASS.

### Legacy Task verification evidence

AGPC-000 activation `c6bae0227acd3e4f57b591c14a88e31b6f2e553f`
has sole parent `060396112abaddbbcf79a33c8a04ae775cce66a1` and exactly eight
paths. Staged lifecycle, strict registry/Markdown/links, the exact-path staged
runner, plain staged pre-commit, repository-wide all-files pre-commit, and both
diff checks passed without formatter mutation. The activation content did not
preclaim its own SHA.

AGPC-001 implementation `c4457fa01ae41013ba56db3d3591da845529cf2b`
adds the closure contract, closed schema, production validator, duplicate-safe
fixture, focused tests, corpus-role registration, and narrowly scoped
secret-scanner exclusions for integrity metadata. The package binds actual
predecessor files and provider/model evidence by descriptor-relative reads and
SHA-256, keeps every non-repository lane `ABSENT` or `DEFER`, and rejects
secret-like durable keys or values without echoing them. The 28 focused tests,
exact ten-path staged lane, full pre-commit suite, Ruff, both diff checks, and
independent requirements and quality reviews passed. At that observation,
AGPC-002 through AGPC-005 remained pending.

AGPC-002 implementation `4fdea6a068aec6c65681bae32c44b67a5e95f09e`
routes closure self-test and production validation through the existing single
`agent-governance-static` job and through pre-commit before affected-surface
and repository-quality aggregation. The synchronized CI contract is `1.3.0`
with 18 delegated checks. Validation remains 22 surfaces and increases to 22
validators, with closure selected by exactly the 12 existing agent-governance
route classes. The implementation map, catalog, four provider notes, and
GitHub hub now route to one program result-classification owner while retaining
provider, hosted, actual-evaluation, remote, and live separation.

Focused CI and affected-surface tests first passed, then the repository
aggregate identified stale runner and provider-hook expected sets. Those
expectations were corrected, the affected 49 and 3 tests passed, and the full
aggregate, exact 20-path staged lane, full pre-commit, Ruff, diff checks, and
final requirements plus quality/security re-reviews passed. AGPC-003 through
AGPC-005 remain pending.

AGPC-003 final QA/review fix `1e2bd0744b5213d5004c34aac028b9642cc60028`
passed the full Python suite (774 tests with zero failures or errors), all 15
explicit Spec 046 validator commands, and affected-surface production (822
paths, 22/22 surfaces, 22 validators). The exact 12-path staged and affected
lanes passed, as did the repository aggregate with its unique PASS marker,
staged and all-files pre-commit without formatter mutation, and both diff
checks. Scoped Ruff was clean for every amended Python file; four E702
findings remain only in unchanged
`scripts/validate-active-corpus-eligibility.py` and were independently
adjudicated non-blocking for this fix diff. Initial whole-branch requirements
review found one current-owner issue, initial quality review found one
pathname-reopen TOCTOU issue, and independent security review found no blocking
issue. The final fix resolved those findings and two branch-introduced Ruff
findings; one scoped re-review approved all three original findings as resolved
with no new blocking finding. Provider/runtime, hosted, actual-evaluation,
remote, and live results remain `DEFER` or `ABSENT`; AGPC-004 and AGPC-005
remain pending.

Observed AGPC-003 evidence commit `666e814a65303fe297cf07fab4112720bea62f0a`
records the final fix `1e2bd0744b5213d5004c34aac028b9642cc60028` and a
scoped review with `SPEC PASS`, `QUALITY PASS`, and no findings. This
postflight records only that observed evidence; it does not preclaim the
postflight's own commit SHA, ADR acceptance, terminal document closure, local
merge, worktree cleanup, or external-lane evidence. AGPC-004 and AGPC-005
remain pending.

Decision-readiness activation `ff66dd933e00def085b4c0319a67c6651356b116`
used the governed `draft -> active` edge for ADR-0019 and the program
agent-design while retaining accepted ADR-0013 as the current decision. It
reconciled the fixed `2026-07-10T10:00:00+09:00` /
`2026-07-10T01:00:00Z` source cutoff across current program authorities and
updated five source-bound predecessor digests. The exact 14-path unit passed
closure 28/28, staged lifecycle, strict documents, affected 22/22, the full
repository aggregate, staged pre-commit, Ruff, both diff checks, independent
requirements `COMPLIANT`, and quality/security `APPROVED`. This postflight
records the observed activation SHA; it does not accept ADR-0019 or make it the
current decision.

AGPC-004 terminal document commit
`0a9e10324b552079fdd212683570e08a19878376`, with sole parent
`e84393af5d6196ec352307b3af21b3790e108794`, accepts ADR-0019 as the current
decision, keeps the Spec 041 agent-design active as current design owner,
closes the reciprocal Spec 046/Plan/Task documents, and reconciles
current-owner indexes and profile lineage. This postflight advances the closure
contract package to `1.2.1` and binds ADR-0019's implementation reference to
that observed terminal commit while preserving its source digest and ADR-0013
as accepted historical predecessor evidence.

The terminal commit contains exactly these 21 paths:

- `docs/00.agent-governance/contracts/agent-governance-closure.json`
- `docs/00.agent-governance/contracts/agent-governance-closure.schema.json`
- `docs/00.agent-governance/memory/progress.md`
- `docs/01.requirements/0003-workspace-agent-governance-platform.md`
- `docs/01.requirements/README.md`
- `docs/02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md`
- `docs/02.architecture/decisions/README.md`
- `docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md`
- `docs/02.architecture/descriptions/README.md`
- `docs/03.specs/0041-stage-00-agent-governance-contract/agent-design.md`
- `docs/03.specs/0041-stage-00-agent-governance-contract/spec.md`
- `docs/03.specs/0046-agent-governance-program-closure/spec.md`
- `docs/03.specs/README.md`
- `docs/03.specs/0046-agent-governance-program-closure/plan.md`
- `docs/03.specs/0046-agent-governance-program-closure/plan.md`
- `docs/03.specs/0046-agent-governance-program-closure/README.md#task-records`
- `docs/03.specs/0046-agent-governance-program-closure/README.md#task-records`
- `docs/99.templates/registry.json`
- `scripts/validate-agent-governance-closure.py`
- `tests/fixtures/agent-governance-closure.json`
- `tests/test_validate_agent_governance_closure.py`

The final v4 review package was 86,731 bytes with SHA-256
`806a76eb7587f764c996412cee1290e138934d898ad2c209f5ec2d0ad5b0e8ab`;
independent requirements review returned `COMPLIANT` and independent
quality/security review returned `APPROVED`. Explicit-ref lifecycle validation
over the sole-parent edge passed, and the clean-tree repository quality
aggregate passed. The focused 29-test suite, closure self-test/production,
strict 467-path document registry, strict Markdown profile, strict
link/body-contract checks, and `git diff --check` also passed.

AGPC-003 remains the owner of its previously observed affected, staged,
aggregate, all-files, formatter, and independent-review evidence; AGPC-004
does not reclassify those observations. This postflight does not preclaim its
own commit SHA. The AGPC-005 row continues to archive local `main` integration
and worktree/branch cleanup into the post-terminal root finishing handoff; both
remain planned and unexecuted. External lanes remain `DEFER` or `ABSENT`.

The closure design preserves working short-term, durable long-term,
domain-scoped, and provider-local auxiliary memory as the four classes. It
also distinguishes configured provider model/reasoning completeness from
actual evaluation, fitness, admission, and promotion.
## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Static PASS becomes provider/hosted/live PASS | Require explicit lane classification and prohibit cross-lane promotion. |
| Configured model/effort is called observed fitness | Validate configuration completeness only; retain actual evaluation and promotion as `DEFER`. |
| Memory prose becomes a duplicate authority | Reference the existing four-class machine owner and validate lifecycle fields rather than redefine it. |
| Closure duplicates predecessor evidence | Store concise unique criterion rows and canonical evidence links, not raw logs. |
| Final QA changes files after review | Review formatter output and rerun affected, staged, all-files, diff, and impacted reviews. |
| Dirty `main` contains unrelated user work | Inspect and preserve it; use a safe integration route or stop if overlap prevents local merge. |

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: Spec 046 reciprocal documents/indexes, agent-governance
  contracts/docs, `.github/**`, `.pre-commit-config.yaml`, scripts, tests, and
  provider shims/adapters required by the closure route.
- **Forbidden Paths**: actual `.agent-work/checkpoint.json`, ignored/private
  provider state, auth caches/files, credentials, tokens, shell history,
  private transcripts, provider response bodies, secret values, and live
  Kubernetes/GitOps state.
- **Approval Required**: provider login/authenticated run, provider-native
  runtime discovery, hosted workflow dispatch, remote GitHub mutation, push,
  PR, remote merge, release, paid action, credential change, or live mutation.
- **Static Validation**: focused contract tests, affected/staged runners,
  strict document checks, repository aggregate, all-files pre-commit, and both
  diff checks.
- **Live Validation**: `DEFER`; every external lane requires a separate owner,
  limitation, retry trigger, approval, and observation.
- **Secret / Vault Handling**: no secret reads or prints and only synthetic or
  redacted tracked fixtures.
- **Rollback Plan**: revert only the current AGPC unit in reverse dependency
  order and preserve unrelated user work; revert activation last.
- **Evidence Location**: this Task and
  `../../00.agent-governance/memory/progress.md`.
## Completion Criteria

- Spec 046 activated and its reciprocal documents reached terminal lifecycle
  states through AGPC-004 without a self-commit SHA claim.
- The closure contract package rejects missing, duplicate, stale, ownerless,
  and cross-lane-promoted evidence.
- Provider, hosted, remote, live, and actual-evaluation results stay honestly
  classified.
- Four memory classes and provider model/reasoning configuration validate at
  their repository-static boundary.
- Final reviews approved. A separate AGPC-004 postflight still must observe the
  terminal commit. The AGPC-005 Task row is archived into the post-terminal
  root handoff; local `main` integration and safe isolated-worktree/
  finished-branch cleanup remain planned and unexecuted, and no push is
  authorized.
- This Plan's `done` state records terminal document closure only and does not
  claim the remaining portion of VAL-AGPC-010 as observed.

## Traceability

- **Spec**: [Agent Governance Program Closure](./spec.md)
- **Task**: [Task: Agent Governance Program Closure](./plan.md)
- **Predecessor**: Spec 045 closure `de9a88e4` and postflight `06039611`
- **Program**: [PRD 003](../../../../01.requirements/0003-workspace-agent-governance-platform.md),
  [AD 0006](../../../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md),
  and [ADR 0019](../../../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-AGPC-001](./spec.md#success-criteria--verification-plan) | AGPC-000 | [Activation evidence](./tasks/tsk-0001-agpc-000.md) |
| N/A — VAL-AGPC-002 shares the Spec source above | AGPC-001 | N/A — reciprocal Task is linked in VAL-AGPC-001 |
| N/A — VAL-AGPC-003 through VAL-AGPC-007 share the Spec source above | AGPC-002 | N/A — reciprocal Task is linked in VAL-AGPC-001 |
| N/A — VAL-AGPC-008 and VAL-AGPC-009 share the Spec source above | AGPC-003 | N/A — reciprocal Task is linked in VAL-AGPC-001 |
| N/A — VAL-AGPC-010 shares the Spec source above | AGPC-004 | N/A — terminal documents are complete; reciprocal Task records the pending observed postflight |
| N/A — remaining VAL-AGPC-010 operational handoff | AGPC-005 | N/A — reciprocal Task archives planned local integration and cleanup into the post-terminal root handoff |

### Legacy Task traceability

- **Spec**: Agent Governance Program Closure
- **Plan**: Agent Governance Program Closure Implementation Plan
- **Successor state**: the post-terminal root handoff performs the still-planned
  local merge and worktree/branch cleanup

#### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [AGPC-000](./plan.md#work-breakdown) | Done | Activation `c6bae022`; exact eight paths, sole parent `06039611`, staged lifecycle/runner, strict docs, staged/all-files pre-commit, and diff PASS. |
| [AGPC-001](./spec.md#success-criteria--verification-plan) | Done | Implementation `c4457fa0`; closed contract/schema/fixture/validator/tests, exact ten-path staged lane, full pre-commit, focused 28/28, Ruff, diff, and both independent reviews PASS. |
| N/A — AGPC-002 shares the Plan and Spec sources above | Done | Implementation `4fdea6a0`; one CI job, 18 delegated checks, 22/22 surface-validator inventory, exact 12 closure routes, 20-path staged/aggregate/pre-commit PASS, and final reviews approved. |
| N/A — AGPC-003 shares the Plan and Spec sources above | Done | Final fix `1e2bd0744b5213d5004c34aac028b9642cc60028`; observed evidence `666e814a65303fe297cf07fab4112720bea62f0a` with scoped review `SPEC PASS`, `QUALITY PASS`, and no findings; 774-test suite, 15 Spec 046 validators, affected/staged/aggregate/all-files/Ruff/diff PASS, and scoped re-review approval with no blocking finding. |
| N/A — AGPC-004 shares the Plan and Spec sources above | Done | Observed terminal commit `0a9e10324b552079fdd212683570e08a19878376` with sole parent `e84393af5d6196ec352307b3af21b3790e108794`; exact 21 paths, v4 requirements `COMPLIANT`, quality/security `APPROVED`, explicit-ref lifecycle PASS, and clean-tree aggregate PASS. This postflight does not claim its own SHA. |
| N/A — AGPC-005 shares the Plan and Spec sources above | Archived | Planned local merge and cleanup transferred to the post-terminal root finishing handoff without an execution claim. |
