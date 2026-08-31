---
title: 'Agent Governance CI and QA Cutover Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-08-01
artifact_id: "PLAN-0045"
---

# Agent Governance CI and QA Cutover Implementation Plan

## Overview

This Plan executes
[Spec 045](spec.md)
after the completed Spec 044 repository-static roster-readiness closure. It
adds a dedicated agent-governance CI selection/job/aggregate topology, closed
CI and legacy-cutover validators, consumer-first legacy removal, canonical
GitHub documentation routing, local QA inventory alignment, and synthetic
concurrent checkpoint and durable memory controls.

Spec 045 completion is repository-static and local QA evidence only. Spec 046
separately owns provider canaries, hosted CI observation, branch protection,
actual evaluation/admission/promotion, provider runtime/auth/model discovery,
remote execution, live evidence, and actual provider resume/handoff canaries.
Those lanes remain `DEFER` throughout this Plan unless a later separately
authorized Spec 046 record observes them.

## Context

Spec 039 supplies the always-start workflow, affected-surface selector,
full-SHA Action identity, least permissions, and `ci-summary` foundation. The
current workflow selects `pre-commit`, `repo-quality-static`, and
`manifest-static`; it does not yet expose a dedicated agent-governance output
or job.

Spec 044 closure
`42864832c966744ac4e5cf8c28baa5bf31ac2765` and postflight
`279f81032528dbf732acc3a1a8bc232d11d2c246` are observed prerequisites. They
preserve exact 12-role / 4-provider-surface / 48-tuple repository-static
readiness, mapping `PASS` 21 / `DEFER` 27, repository-static evaluation
readiness, and every configured incumbent without claiming observed
evaluation, final admission, fitness, promotion, canary, or runtime evidence.

The fixed provider/model/source cutoff is
`2026-07-10T10:00:00+09:00` / `2026-07-10T01:00:00Z`, as owned by
`provider-runtime-evidence.json`. The date `2026-07-30` is this activation
observation only and does not move that cutoff.

At activation, `scripts/validate-agent-governance-ci.py` and
`scripts/validate-agent-legacy-cutover.py` did not exist. The legacy
role-semantics contract/schema/validator/fixture remained readable
compatibility surfaces, the GitHub hub retained its pre-cutover name, and the
Spec 043 checkpoint/memory gates did not yet prove concurrent
provider-instance isolation. These were activation-time gaps, not completed
results.

### Legacy Task ledger inputs

This Task tracks the executable Spec 045 workstream that adds a dedicated
agent-governance repository-static CI/QA lane, closed CI and legacy-cutover
validation, consumer-first legacy removal, canonical GitHub hub routing, local
QA inventory alignment, and synthetic concurrent checkpoint and durable memory
policy.

The fixed provider/model/source cutoff remains
`2026-07-10T10:00:00+09:00` / `2026-07-10T01:00:00Z`. The date
`2026-07-30` is the activation observation only. AGQC-000 through AGQC-006 are
complete at the repository-static boundary. The closed
`validate-agent-governance-ci.py` and `validate-agent-legacy-cutover.py`
owners exist. The consumer-first cutover proves zero active consumers, retains
only closed superseding/archive evidence, removes legacy role-semantics
ownership, and establishes the canonical GitHub hub. The local QA contract now
owns the exact eight-step completion order, affected/staged runner separation,
plain staged and all-files pre-commit commands, both diff checks, formatter
rerun semantics, and current machine inventories.

Spec 045 completion remains repository-static. Hosted CI, branch protection,
provider runtime/auth/model discovery, actual evaluation/admission/promotion,
provider resume/handoff canaries, remote execution, and live evidence remain
`DEFER` and are reserved for Spec 046.

- Parent Spec:
  [Spec 045](spec.md)
- Parent Plan:
  [Agent Governance CI and QA Cutover Implementation Plan](plan.md)
- CI foundation: Spec 039
- Loop/checkpoint foundation: Spec 043
- Roster/evaluation predecessor: Spec 044
- Observed prerequisite commits: Spec 044 closure
  `42864832c966744ac4e5cf8c28baa5bf31ac2765` and postflight
  `279f81032528dbf732acc3a1a8bc232d11d2c246`
- Observed Spec 045 activation:
  `c677321d9c0afee2cce7a8485c58e23d4a3bf18c`
- Observed Spec 045 postflight and implementation: activation postflight
  `46c8e6b64097cce1c403b8c22989b11226f21263` and AGQC-001
  `12c5578747ef37afb9a1e65afe41bee6aca0e473`; AGQC-001 postflight
  `25688ec6e321a0458437f83bdc914b339fe28c2d` and AGQC-002
  `be0a12ecd8d51b73f251004b34be6e8288159eb5`; AGQC-002 postflight
  `a3cf5836e46cb2e53f9ec5ddf4150559d2643d39` and AGQC-003
  `38a2fe6b90bad694d0a9a021c7edce8d800e03ea`; AGQC-003 postflight
  `dc7dccbfcb907ae38cc0f7c91b59b6556e4fe888` and AGQC-004
  `baf4df962cb70c55eefd20b5fe76ee07e7ff8be0`
- Observed AGQC-005 implementation: checkpoint isolation and memory lifecycle
  `781ebb82b64d2f63d6b9630b6b3e48115dc5a791`; closed static CI evidence
  ownership `4c7b87718aa41f680ef8f5e63c4396565b1c5e0b`
- Observed AGQC-006 terminal implementation and closure: baseline
  `a886e0616526eaf2905e9d90dc8d6be6a627b481`, hermetic test correction
  `ed89228546501dd11a7f4abad28e8ebb094fbd97`, and exact eight-file reciprocal
  closure `de9a88e4550b87542eb7221c5ae7416fe5075763` with sole parent
  `ed89228546501dd11a7f4abad28e8ebb094fbd97`
- Fixed cutoff owner:
  [provider-runtime-evidence.json](../../00.agent-governance/contracts/provider-runtime-evidence.json)
- Current machine owners:
  [harness-contract.json](../../00.agent-governance/contracts/harness-contract.json),
  [validation routing registry](../../../scripts/validation/registry.json),
  and
  [agent-loop-lifecycle.json](../../00.agent-governance/contracts/agent-loop-lifecycle.json)
## Goals & In-Scope

- Activate the reciprocal Spec/Plan/Task path and the single Spec 045
  program-lineage relation as one exact eight-file SDLC transition.
- Add a dedicated agent-governance selector output, static CI job, and
  `ci-summary` consumer without changing the always-start workflow boundary.
- Implement a closed agent-governance CI contract, schema, validator, fixture,
  focused tests, and routed local/CI invocation.
- Implement a consumer-first legacy-cutover validator and prove zero active
  consumers before deleting the legacy role-semantics contract, schema,
  validator, fixture, and legacy-specific test expectations.
- Establish `.github/README.md` as the canonical GitHub hub with its registry,
  quality-gate, fixture, inventory, and active-reference migration.
- Preserve targeted, affected, staged, tests, all-files, formatter review,
  rerun, and diff ordering across the quality, pre-commit, script, test, and
  documentation inventories.
- Add repository-static concurrent checkpoint namespace/provider identity and
  durable memory retention, compaction, replacement, archive/GC, conflict, and
  handoff policy fixtures without reading actual provider state.
- Reconcile semantic owners, complete independent requirements/quality/security
  reviews, run full local QA, and close/postflight only the Spec 045
  repository-static tranche.

## Non-Goals & Out-of-Scope

- No provider login, authenticated run, native agent/model discovery, provider
  resume/handoff canary, model resolution, or credential change.
- No hosted workflow dispatch or success claim, branch-protection/ruleset
  mutation, push, PR, merge, or remote required-check claim.
- No actual role evaluation, result adjudication, final admission, model
  fitness, threshold satisfaction, or promotion.
- No Kubernetes/GitOps, Vault/ESO, cloud, deployment, remote, or live mutation
  or readiness claim.
- No secret, auth file, shell history, private transcript, provider response,
  actual ignored checkpoint, or provider-local memory read.
- No Spec 046 activation or program-closure transition before Spec 045
  repository-static closure and postflight are observed.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| AGQC-000 | Activate the reciprocal Spec 045 execution path | Spec 044 closure `42864832` and postflight `279f8103` | Clean target worktree and observed predecessor identities | Exactly the Spec body/index, new Plan body/index, new Task body/index, program-lineage relation, and progress entry are `active`; no activation SHA is preclaimed |
| AGQC-001 | Add dedicated agent-governance CI selector/job/`ci-summary` topology | AGQC-000, Spec 039 | Active reciprocal path and current selector/workflow baseline | Changed agent-governance owners select one required static job; `ci-summary` distinguishes selected PASS/FAIL from valid SKIP and rejects missing/cancelled results; full-SHA and least permissions remain intact |
| AGQC-002 | Implement the closed `validate-agent-governance-ci.py` contract/schema/fixture/tests | AGQC-001 | Topology and result vocabulary are explicit | Planned contract, adjacent schema, validator, deterministic fixture, focused tests, self-test, affected routing, aggregate owner, pre-commit/CI invocation, and inventories pass without provider credentials or hosted-runtime inference |
| AGQC-003 | Execute consumer-first legacy cutover and canonical GitHub hub rename | AGQC-002 | Harness semantics are current and the new CI gate fails closed | `validate-agent-legacy-cutover.py` proves zero active consumers before legacy role-semantics contract/schema/validator/fixture/test removal; stale claims are zero; `.github/README.md` and every route/reference/fixture/inventory adopt the canonical hub atomically |
| AGQC-004 | Align local QA ordering and repository inventories | AGQC-001, AGQC-002, AGQC-003 | New and retired command surfaces are known | Quality owner, affected/staged runner, `.pre-commit-config.yaml`, repository-quality gate, scripts/tests/GitHub/docs inventories, and formatter-rerun evidence express one targeted-to-diff order without dangling commands |
| AGQC-005 | Add repository-static concurrent checkpoint/provider identity and durable memory policy | AGQC-000, Spec 043 | Current loop/checkpoint/memory contracts and synthetic fixtures pass | Synthetic collisions and cross-worktree/task/provider resumes fail closed; durable retention, sensitivity, compaction replacement, archive/GC, conflict, and handoff policy validate; actual provider checkpoint/resume/handoff remains `DEFER` |
| AGQC-006 | Reconcile semantics, obtain independent reviews, run full QA, and close/postflight | AGQC-001 through AGQC-005 | Focused package gates pass and zero-consumer deletion is observed | Requirements are compliant, quality/security are approved, affected/staged/tests/all-files/formatter-rerun/diff gates pass, exact reciprocal closure/postflight are recorded, and every Spec 046 external/actual lane remains `DEFER` |

AGQC-000 through AGQC-006 are complete at the repository-static boundary.
Baseline `a886e061` passed Python `741`, aggregate, all-files,
formatter-review, worktree-diff, and cached-diff gates. Terminal test-only
HEAD `ed892285` passed `49` related tests, the nested-subreaper isolation
probe, file pre-commit, and independent requirements/quality/security review.
The combined coverage ended `COMPLIANT` / `APPROVED` / `APPROVED` with no
findings. The content-addressed closure SHA is recorded only after this
transition is committed and observed.

## Verification Plan

AGQC-000 uses only existing document controls:

```bash
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-document-lifecycle.py --root . --mode staged
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
python3 -m json.tool docs/99.templates/registry.json
git diff --check
```

The following focused commands are planned deliverables and cannot run until
AGQC-002 and AGQC-003 create them:

```bash
python3 scripts/validate-agent-governance-ci.py --root . --self-test
python3 scripts/validate-agent-governance-ci.py --root .
python3 -m unittest tests/test_validate_agent_governance_ci.py
python3 scripts/validate-agent-legacy-cutover.py --root . --self-test
python3 scripts/validate-agent-legacy-cutover.py --root .
python3 -m unittest tests/test_validate_agent_legacy_cutover.py
```

Later packages also run existing focused and completion gates:

```bash
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-agent-loop-lifecycle.py --root .
python3 scripts/validate-agent-checkpoint.py --root . --self-test
python3 scripts/validate-agent-roster-admission.py --root .
python3 scripts/validate-agent-evaluations.py --root .
python3 scripts/validate-agent-model-fitness.py --root .
python3 scripts/validate-affected-surfaces.py --root . --self-test
python3 scripts/validate-github-actions-security.py --root .
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
git diff --check
```

Hosted CI, branch protection, provider runtime/auth/model discovery, remote,
live, actual evaluation/admission/promotion, and provider resume/handoff
canaries are not completion commands for this Plan and remain `DEFER`.

### Legacy Task verification evidence

AGQC-000 through AGQC-004 are complete at activation `c677321d`, CI topology
implementation `12c55787`, closed CI contract implementation `be0a12ec`,
consumer-first cutover `38a2fe6b`, and local QA closure `baf4df96`.
The affected-surface contract owns four CI jobs and all required
agent-governance owner classes select `agent-governance-static`. The closed
validator enforces the exact job, step, environment, permissions, defaults,
command, pin, result, evidence, and delegated-check shapes; the summary
accepts only selected-success and unselected-skipped combinations and fails
closed otherwise.

The AGQC-003 legacy-cutover contract, schema, fixture, tests, and validator
prove zero active consumers before the atomic legacy deletion and GitHub hub
rename. The AGQC-006K successor boundary derives candidates only from the Git
index through a closed absolute Git runner; ignored and non-ignored untracked
paths are never opened or counted, while a staged consumer is enforceable. One
root-dirfd no-follow reader owns every content route and rejects parent/final
swap, symlink/type, oversized-file, and mid-read growth drift. Closed limits
cover Git time and cleanup, stdout/stderr, candidate count/path bytes,
regular-file bytes, and bounded escaped single-line diagnostics. Protected
historical snapshots are accepted only through exact digest, lifecycle,
source, retired-reference count, and superseding-replacement evidence. Missing
evidence and retired-reference removal fail closed.

The historical AGQC-002 exact staged path set, staged-runner result, and plain
staged pre-commit result are unavailable in canonical records; that historical
staged sub-lane is therefore `DEFER`. The `811`-path affected-surface corpus is
affected evidence only and cannot be used to infer staged completion. This
does not change the recorded AGQC-002 implementation result. AGQC-006K closure
instead uses newly observed HEAD evidence: affected-surface self-test and
production passed `22/22` over `815` tracked paths with `0/0`
uncovered/ambiguous; the exact 11-path affected and staged runners passed all
18 selected validators; focused/closed legacy and governance-CI suites, strict
registry/Markdown/links, and the RIA digest-pin test passed; and plain staged
pre-commit passed every applicable hook with no formatter mutation. The scoped
successor report records the final reruns and diff evidence without
retroactively changing the historical AGQC-002 result.

AGQC-004 adds `staged` to the closed local runner, propagates exact staged
Markdown paths to every selected document validator, and makes
`quality-standards.md` the sole eight-step local completion owner. The closed
CI contract now validates `6` truth cases, `43` mutations, `16` delegated
checks, `1` deferred owner solely for Spec 046, `10` QA surfaces, the separate plain staged and
all-files pre-commit commands, and both worktree and cached diff checks.
AGQC-005 closes repository-static concurrent checkpoint/provider identity and
the working short-term, durable long-term, domain scoped, and provider-local
auxiliary memory lifecycle policy. Checkpoint evidence reports `20` focused
tests and `110` negative mutations; loop evidence reports `22` focused tests
and `66` self-test cases. Independent review approved the implementation.

AGQC-006 completes through terminal implementation HEAD
`ed89228546501dd11a7f4abad28e8ebb094fbd97`. At baseline `a886e061`, the
terminal Python discovery suite passed `741` tests in `557.634s`;
`scripts/validate-repo-quality-gates.sh .` and `pre-commit run --all-files`
passed, no formatter mutation remained, and both worktree and cached diff
checks were clean. The test-only terminal delta passed all `49` related tests,
the nested-subreaper isolation probe, file pre-commit, and three independent
reviews. Requirements review is
complete through the terminal whole-branch review plus the contiguous
`24ddb1a0..cbe059d2`, `cbe059d2..8e52d52c`, `8e52d52c..eb064108`, and
`eb064108..a886e061` remediation reviews plus the `ed892285` delta review; its
terminal disposition is `COMPLIANT`. Quality and security are `APPROVED`
through the same terminal delta. Every review reports Critical `0`, Important
`0`, and Minor `0` after remediation.

Exact eight-file reciprocal closure
`de9a88e4550b87542eb7221c5ae7416fe5075763` is observed with sole parent
`ed89228546501dd11a7f4abad28e8ebb094fbd97`. Explicit-ref lifecycle validation
for that edge, clean-tree repository aggregate, post-closure all-files
pre-commit, and exact-range diff checks passed. This postflight evidence update
does not preclaim its own content-addressed commit SHA.

The provider/model/source cutoff remains the fixed 2026-07-10 timestamp.
Hosted CI, branch protection, provider runtime/auth/model discovery, actual
evaluation/admission/promotion, provider resume/handoff canaries, remote, and
live evidence are `DEFER`. Independent implementation reviewers are assigned
only in AGQC-006.
## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Repository-static CI topology is reported as a hosted run | Record selector, workflow, security, and aggregate results as repo-static only; leave hosted run identity and branch protection to Spec 046. |
| Planned validator names are mistaken for existing controls | Keep AGQC-002/003 queued until the files, schemas/fixtures/tests, self-tests, and production checks are observed together. |
| Legacy files are deleted while a hidden consumer remains | Make zero-consumer proof a blocking precondition and update harness, aggregate, affected, pre-commit, docs, test, and inventory consumers before deletion. |
| The `.github` rename leaves a stale owner or broken route | Move the file with registry, quality-gate, routing, fixture, inventory, and broad active-reference updates in one tested unit. |
| Concurrent provider sessions overwrite or resume another task | Validate deterministic non-secret repository/worktree/task/provider/instance identity and reject duplicate writers or mismatched bases in synthetic fixtures. |
| Compaction or archive policy retains sensitive/raw context | Require canonical owner, sensitivity, replacement provenance, retention/expiry, archive/GC disposition, and value-free diagnostics; reject raw prompts, transcripts, auth, and secrets. |
| Spec 045 absorbs Spec 046 provider or promotion evidence | Keep actual canaries, hosted observation, branch protection, evaluation/admission/promotion, runtime/auth/model discovery, remote, and live lanes explicitly successor-owned and `DEFER`. |
| Formatter output expands scope | Review every formatter diff, restore the approved package boundary, and rerun affected plus all-files before a logical commit. |

### Legacy Task approval and rollback boundaries

- **Recorded AGQC-000 Activation Paths**:
  `docs/03.specs/0045-agent-governance-ci-qa-cutover/spec.md`,
  `docs/03.specs/0045-agent-governance-ci-qa-cutover/plan.md`,
  `docs/03.specs/0045-agent-governance-ci-qa-cutover/README.md#task-records`,
  `docs/03.specs/README.md`, `docs/03.specs/0045-agent-governance-ci-qa-cutover/plan.md`,
  `docs/03.specs/0045-agent-governance-ci-qa-cutover/README.md#task-records`,
  `docs/99.templates/registry.json`, and
  `docs/00.agent-governance/memory/progress.md`
- **Later Planned Paths**: `.github/**`, `.pre-commit-config.yaml`,
  root provider shims, `.agents/**`, `.claude/**`, `.codex/**`, `.gemini/**`,
  `docs/00.agent-governance/**`, the reciprocal Spec/Plan/Task/index owners,
  `docs/99.templates/registry.json`, `scripts/**`, and
  `tests/**`; each later package requires its own bounded implementation scope
- **Forbidden Paths**: credentials, auth caches/files, shell history, provider
  response bodies, private prompts/transcripts, Vault/ESO values, live
  Kubernetes/GitOps state, provider account state, actual provider-local
  memory, and actual `.agent-work/**` checkpoint content
- **Approval Required**: provider login/authenticated run, hosted workflow
  dispatch or remote GitHub mutation, branch-protection change, push/PR/merge,
  paid or credential-bearing action, provider resume/handoff canary, live
  cluster mutation, or credential change
- **Static Validation**: AGQC-000 used the existing strict registry, isolated
  proposed-index lifecycle, Markdown/frontmatter, link/owner, JSON, and
  diff/scope checks. AGQC-001 and AGQC-002 now add affected-surface topology
  and the closed agent-governance CI contract; each later validator runs only
  after its contract, schema, fixture, tests, and implementation exist
- **Live Validation**: `DEFER`; no hosted, provider-runtime, remote, or live
  operation is authorized
- **Secret / Vault Handling**: no secret reads or prints, no auth inspection,
  no credential fixture values, and synthetic/redacted fixtures only
- **Rollback Plan**: discard or revert only the exact AGQC unit in reverse
  dependency order; restore the legacy owner and former GitHub hub name
  together if zero-consumer or rename validation fails; revert AGQC-000 last
  without reset, clean, or overwrite of unrelated work
- **Evidence Location**: this Task and
  `../../00.agent-governance/memory/progress.md`
## Completion Criteria

- Spec 045, its reciprocal Plan and Task, three indexes, program-lineage
  relation, and progress owner close together only after AGQC-001 through
  AGQC-006 are reviewed and complete.
- The dedicated agent-governance selector/job/`ci-summary` topology and closed
  CI contract/schema/validator/fixture/tests pass repository-static checks.
- `validate-agent-legacy-cutover.py` proves zero active consumers before all
  legacy role-semantics ownership surfaces and legacy-specific tests are
  removed.
- `.github/README.md` is the sole canonical GitHub hub; the retired predecessor
  path and active references to it are zero.
- Local QA, repository-quality, pre-commit, script, test, GitHub, and
  documentation inventories agree on the new and retired surfaces and the
  canonical completion order.
- Synthetic concurrent checkpoint/provider identity and durable memory
  retention/compaction/archive controls pass without reading actual provider
  or ignored checkpoint state.
- Independent requirements, quality, and security reviews approve the bounded
  repository-static claims; focused, affected, staged, tests, all-files,
  formatter-review/rerun, strict document, and diff gates pass.
- Hosted CI, branch protection, provider runtime/auth/model discovery, actual
  evaluation/admission/promotion, provider resume/handoff canaries, remote,
  and live evidence remain explicitly `DEFER` for Spec 046.

## Traceability

- **Spec**: [Agent Governance CI and QA Cutover](spec.md)
- **Task**: [Agent Governance CI and QA Cutover Task](README.md#task-records)
- **Program**: [PRD-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) and [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
- **Governing decision**: [ADR-0013](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
- **Active successor decision**: [ADR-0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **CI foundation**: Spec 039
- **Loop foundation**: Spec 043
- **Observed prerequisite**: Spec 044 closure `42864832` and postflight
  `279f8103`
- **Successor**: Spec 046

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-AGQC-001](spec.md#success-criteria--verification-plan) | AGQC-000, AGQC-001, AGQC-002 | [Activation, topology, and CI contract evidence](tasks/tsk-0001-agqc-000.md) |
| N/A — VAL-AGQC-002 through VAL-AGQC-004 share the Spec source above | AGQC-001, AGQC-002 | N/A — the reciprocal Task is linked in VAL-AGQC-001 |
| N/A — VAL-AGQC-005 and VAL-AGQC-006 share the Spec source above | AGQC-004 | N/A — the reciprocal Task is linked in VAL-AGQC-001 |
| N/A — VAL-AGQC-007 and VAL-AGQC-008 share the Spec source above | AGQC-003 | N/A — the reciprocal Task is linked in VAL-AGQC-001 |
| N/A — VAL-AGQC-009 shares the Spec source above | AGQC-005 | N/A — the reciprocal Task is linked in VAL-AGQC-001 |
| N/A — VAL-AGQC-010 shares the Spec source above | AGQC-000, AGQC-006 | N/A — the reciprocal Task is linked in VAL-AGQC-001 |

### Legacy Task traceability

- **Successor**: Spec 046

#### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [AGQC-000](plan.md#work-breakdown) | Done | Activation `c677321d`; lifecycle, strict registry `465` with `0/0` uncovered/ambiguous, Markdown, link/owner, JSON, aggregate, all-files pre-commit, diff, and final independent review PASS. |
| [AGQC-001](spec.md#success-criteria--verification-plan) | Done | `12c55787`; affected `22/22`, `19` selections, `6` CI ranges, `37` mutations, `806` paths, `4` jobs, `0/0`; CI Python/GitHub security/aggregate/all-files/final review PASS. |
| N/A — AGQC-002 shares the Plan and Spec sources above | Done | `be0a12ec`; `22` focused tests, self-test `6` truth/`38` mutation cases, production `12` route classes/`13` delegated checks, affected `22/22` with an `811`-path affected-surface tracked/candidate corpus and `0/0`, aggregate/all-files/diff/final review PASS. |
| N/A — AGQC-003 shares the Plan and Spec sources above | Done | `38a2fe6b`; `20` focused tests, self-test `3/22`, production `810` scanned files/`43` evidence references/`0` active consumers, RIA `87`, aggregate/all-files/diff/final requirements/security/integration review PASS. |
| N/A — AGQC-004 shares the Plan and Spec sources above | Done | `baf4df96`; runner `22`, CI `24`, self-test `6/43`, production `12/16/6/2/10`, legacy `3/22` and `810/43/0`, affected/staged `15` paths, aggregate/plain pre-commit/all-files/diff/final review PASS, formatter mutation `0`. |
| N/A — AGQC-005 shares the Plan and Spec sources above | Done | `781ebb82`; checkpoint `20` focused tests/`110` negative mutations/four memory classes. `4c7b8771`; loop `22` focused tests/`66` self-test cases, deterministic identity isolation and four-class sensitivity, retention/expiry, compaction source/replacement, archive/GC, conflict, and handoff; independent review approved. |
| N/A — AGQC-006 shares the Plan and Spec sources above | Done | Baseline `a886e061`: Python `741`, aggregate, all-files, formatter review and both diff checks PASS. Terminal test-only `ed892285`: related `49`, nested-subreaper isolation, file pre-commit and three independent reviews PASS, all `0/0/0`. Reciprocal closure `de9a88e4` has sole parent `ed892285`; explicit-ref, clean aggregate/all-files/diff PASS. Hosted/provider/actual/remote/live lanes remain Spec 046 `DEFER`. |
