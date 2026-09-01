---
title: 'Agent Roster Evaluation and Admission Implementation Plan'
version: "1.0"
type: sdlc/plan
layer: "03.specs"
status: done
owner: platform
updated: 2026-07-30
artifact_id: "SPEC-0044-PLAN-0001"
---

# Agent Roster Evaluation and Admission Implementation Plan

## Overview

This Plan executed
[Spec 044](spec.md)
after the completed Spec 043 loop lifecycle closure. AREA-002 projected the
then-target-only 12-role / 4-surface / 48-adapter design into tracked
repository-static implementation while keeping candidate decisions and the
admission verdict `DEFER`. AREA-003 supplies repository-static four-class
evaluation, adjudication-readiness, and rollback-source evidence, while
observed same-suite evaluation, result adjudication, and final roster admission
remain `DEFER`.

## Context

Spec 041 supplied the machine-readable harness baseline with a historical
10-role / 3-surface / 30-adapter inventory and a target-only 12-role /
4-surface / 48-adapter inventory. Spec 044 now records the exact 12-role /
4-surface / 48-adapter current repository-static inventory. Spec 042 owns
provider/source currentness and keeps runtime/model-resolution claims
separated from repository-static files. Spec 043 owns bounded loop,
checkpoint, and memory lifecycle controls.
Its terminal closure
`a0bc3565988e291980320dec8442405c7ef16eb6` and postflight
`80ffd6d92a53990b04e413c0acf7fbc879b437d4` are observed prerequisites.

The completed repository-static transition materialized `docs-researcher`,
`quality-engineer`, and the native `.gemini/agents/**` surface as current
repo-static projections. That transition is not final admission, and all
configured incumbents remain retained. This Plan does not claim observed
evaluation, result adjudication, final admission, model fitness, threshold
satisfaction, promotion, canary, provider-native runtime discovery or
authentication, model resolution, hosted CI, remote, live Kubernetes/GitOps,
or credential-bearing evidence.

Spec 042 fixes provider/model source evidence at
`2026-07-10 10:00 Asia/Seoul`. The harness contract's later
`sourceObservationCutoff` value is drift to reconcile, not authority to move
that fixed boundary; repository observations and source-cutoff facts remain
separate.

### Legacy Task ledger inputs

This Task is the durable execution evidence for the Spec 044 work stream that
projected the
repository-static AI Agent roster from the completed 10-role / 3-surface
baseline to a validated 12-role / 4-surface / 48-adapter current tracked
inventory. Provider/model evidence remains fixed at the Spec 042
`2026-07-10 10:00 Asia/Seoul` cutoff. The AREA-002 projection keeps admission
`DEFER` and does not claim provider discovery, model resolution, or execution;
AREA-003 completes repository-static evaluation readiness, while observed
same-suite evaluation, result adjudication, and final roster admission remain
`DEFER`.

- Parent Spec:
  [Spec 044](spec.md)
- Parent Plan:
  [Agent Roster Evaluation and Admission Implementation Plan](plan.md)
- Predecessor evidence: completed Specs 041 through 043, culminating in the
  observed Spec 043 closure and postflight commits below
- Current machine owner:
  [harness-contract.json](../../00.agent-governance/contracts/harness-contract.json)
- Observed prerequisite commits: Spec 043 closure
  `a0bc3565988e291980320dec8442405c7ef16eb6` and postflight
  `80ffd6d92a53990b04e413c0acf7fbc879b437d4`
- Observed Spec 044 commits: activation
  `b8b1a3884f9948fcd4ac2aecc89ea727118ad787`, activation postflight
  `6d9b01d51f8a198c521621bcd52ff088c397ee0b`, and AREA-001 implementation
  `0129daf7d44c9308bcad63d4966e11ffa98d05af`; AREA-002 projection
  `138ce6ac28aa0eebac2b0295e4c50fd78d594db6` and admission-boundary
  remediation `1d03b0b44350b26cca1f7d91ebaf8f3c66b4ce1e`; AREA-003 evaluation
  readiness `3bd5759029cc49742c12a811f8751f1609c4f330`; AREA-004 model-fitness
  readiness `258955b3e0d999ec4ebc3de561d0db39ce11ac3c`; AREA-004 postflight
  `a15d5e10a4848aca013848571ba6d56c3568b5c3`; and AREA-005 semantic
  reconciliation `7891368e3d29e5e9e5e8ada4023118d331e38000` and exact eight-path
  closure `42864832c966744ac4e5cf8c28baa5bf31ac2765`
## Goals & In-Scope

- Project the canonical 12-role roster and exact four-surface adapter set in
  repository-static contract evidence without returning an admission PASS.
- Add least-privilege adapters for `docs-researcher` and `quality-engineer`
  across local/Antigravity, Claude, Codex, and Gemini.
- Add Gemini-native repository adapter files without claiming Gemini CLI runtime
  consumption.
- Add deterministic validators and fixtures for roster admission, role
  evaluation coverage, and provider model/effort fitness.
- Define the closed schemas, versioned synthetic corpora, adjudication,
  promotion, and rollback records before final roster or runtime promotion.
- Reconcile the fixed Spec 042 source cutoff without rewriting later
  repository-observation dates.
- Preserve the memory hierarchy from Spec 043: working-short-term,
  durable-long-term, domain-scoped, and provider-local-auxiliary.
- Record role-specific candidate model and `model_reasoning_effort` decisions
  as repository-static/candidate-only unless a provider canary proves runtime
  support.

## Non-Goals & Out-of-Scope

- No provider login, authenticated provider run, remote subagent dispatch, live
  GitHub mutation, Kubernetes/GitOps mutation, Vault/ESO read, or credential
  change.
- No automatic import of external `agency-agents` personas.
- No replacement of Spec 041 schema ownership or Spec 042 provider runtime
  evidence ownership.
- No Spec 045 workflow, CI job, pre-commit inventory, legacy-retirement, or
  consumer-cutover change.
- No hosted CI success claim unless separately observed.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| AREA-000 | Activate reciprocal SDLC execution path | Spec 043 done | Clean worktree and approved successor | Spec, Plan, Task, indexes, registry, and progress record `active` |
| AREA-001 | Implement closed admission, evaluation, and model-fitness contracts, schemas, validators, and synthetic negative fixtures | AREA-000 | Active reciprocal Spec/Plan/Task and target-only 12/4/48 design | Planned validators fail malformed, overlapping, over-authorized, secret-bearing, unadjudicated, unversioned, and runtime-preclaim fixtures and pass the frozen baseline |
| AREA-002 | Project two bounded candidates and the exact repository-static roster/adapters | AREA-001 | Closed gates reject unsafe or incomplete projections | `docs-researcher` and `quality-engineer` remain `repository-static-projected`; local, Claude, Codex, and Gemini projections form exact 12-role / 4-surface / 48-adapter set equality with native metadata, no duplicate owner, and admission `DEFER` |
| AREA-003 | Establish versioned role evaluation, adjudication, rollback, and final admission evidence | AREA-002 | Exact projected role and surface identities validate with admission `DEFER` | All 12 roles cover positive, negative/adversarial, refusal/stop, and handoff cases; independent adjudication and rollback references validate without retaining private prompts or transcripts before any final admission PASS |
| AREA-004 | Reconcile cutoff evidence and optimize provider-specific candidate model/effort profiles | AREA-003, Spec 042 | Same-version role suites and provider evidence contract are available | Each role/provider tuple has a risk-based candidate, effort/routing rationale, baseline, fitness threshold, fallback, and `PASS`/`FAIL`/`DEFER`; exact runtime resolution remains unpromoted unless observed |
| AREA-005 | Reconcile catalog, provider notes, and quality gates | AREA-002, AREA-003, AREA-004 | Focused validators pass | Catalog/provider semantics reconciled in `7891368e`; focused model, staged lifecycle, strict registry `463`, aggregate, all-files, diff, and requirements/quality/security review gates pass; reciprocal closure remains SHA-unclaimed until committed |

## Verification Plan

Run focused validators before aggregate gates:

```bash
python3 scripts/validate-agent-roster-admission.py --root .
python3 scripts/validate-agent-roster-admission.py --root . --self-test
python3 scripts/validate-agent-evaluations.py --root .
python3 scripts/validate-agent-evaluations.py --root . --self-test
python3 scripts/validate-agent-model-fitness.py --root .
python3 scripts/validate-agent-model-fitness.py --root . --self-test
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-agent-harness-semantics.py --root .
python3 scripts/validate-agent-roster-currentness.py .
python3 scripts/validate-affected-surfaces.py --root . --self-test
python3 scripts/validate-document-lifecycle.py --root . --mode staged
python3 scripts/validate-document-contract-registry.py --root . --mode strict
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
git diff --check
```

### Legacy Task verification evidence

AREA-000 and AREA-001 are complete. AREA-001 added three closed machine
contracts, schemas, validators, synthetic fixtures, focused tests, harness
consumer registration, affected-surface routing, aggregate invocation, and
exact helper admission. Focused tests `119`, helper audit `59/33/26`,
affected surfaces `21/21` with `19` validators, staged and clean-tree
repository aggregate, and staged and clean-tree all-files pre-commit passed.

AREA-002 commit `138ce6ac` materializes exact 12-role / 4-surface / 48-adapter
tracked set equality. Its corrected lifecycle result is
`repository-static-projected` / `DEFER`: the two candidates are projected, not
finally admitted. Remediation commit `1d03b0b4` preserves that boundary across
the contract, schema, validators, lifecycle controls, all four provider
surfaces, and the five-field Gemini project-agent metadata projection.
Admission focused validation passed `59` self-test and `13` unit cases;
lifecycle passed `696` self-test and `6` focused cases; role semantics passed
`768` cases plus `9` Gemini metadata mutations; model fitness passed `16`
self-test and `18` focused unit cases. The active corpus audit passed with
`helpers=60`, `frozen=33`, `post_closure=27`, and formats `25/28/6/1`.
Repository aggregate and `pre-commit run --all-files` passed. Requirements
review approved Spec compliance, and final quality review reported zero
Critical or Important findings after two wording corrections.

AREA-003 commit `3bd57590` completes the versioned four-class corpus,
adjudication-readiness, rollback-source binding, and explicit final-decision
record within its repository-static readiness scope. Contract
version `1.1.0` and state `repository-static-evaluation-ready`: exact 12-role
harness suite/version binding, 48 role-specific synthetic records, 12
adjudication-readiness records, and 2 rollback records bound to the governed
roster-admission source. Readiness is `PASS`, but observed same-suite
evaluation, result adjudication, and final admission remain `DEFER`.

Focused tests passed `33/33`, evaluation self-test `60/60`, staged lifecycle,
repository aggregate, all-files pre-commit, and diff checks passed. Spec review
approved with zero Critical or Important findings. Quality review's two
Important findings—symlink-root resolution and unbound rollback references—
were corrected and independently re-reviewed as addressed.

AREA-004 commit `258955b3` completes the closed provider/model mapping-readiness
contract without promoting a candidate or preclaiming model execution.
Contract version `1.1.0`, schema version `2`, and lifecycle state
`repository-static-fitness-ready` cover exactly 12 roles, 4 providers, and 48
role/provider tuples. Mapping readiness is `PASS` for 21 tuples: all 12 local
tuples and the 9 cutoff-applicable Claude high-risk tuples. It remains `DEFER`
for 27 tuples: 3 current-only Claude tuples, all 12 Codex tuples, and all 12
mixed/unresolved Gemini tuples. Every configured incumbent remains unchanged.

The fixed thresholds are quality `0.9`, safety `1`, cost `1` USD, and latency
`120000` ms. Observed fitness, threshold, promotion, canary, and runtime
decisions remain `DEFER` for all 48 tuples. Provider runtime and
authentication, hosted CI, remote/live execution, and model resolution remain
`DEFER`; every tuple rollback state is `armed-not-executed` and its execution
evidence is `DEFER`.
Focused tests passed `28/28`, the closed self-test passed `33/33`, and
production reported `roles=12`, `providers=4`, `tuples=48`,
`mappingReady=21`, `mappingDeferred=27`, `fitnessDeferred=48`,
`thresholdDeferred=48`, `promotionDeferred=48`, `canaryDeferred=48`, and
`runtimeDeferred=48`. Staged lifecycle, strict registry over `463` tracked
paths, repository aggregate, all-files pre-commit, and diff checks passed.
Final independent review reported zero Critical and zero Important findings.

AREA-004 postflight commit
`a15d5e10a4848aca013848571ba6d56c3568b5c3` records that bounded evidence.
AREA-005 semantic reconciliation commit
`7891368e3d29e5e9e5e8ada4023118d331e38000` then aligns the harness catalog,
model policy, four provider notes, and script/test inventories with the same
evidence boundary: exact 12-role / 4-provider-surface / 48-tuple coverage,
mapping readiness `PASS` 21 / `DEFER` 27, AREA-003 repository-static
evaluation readiness complete, and every configured incumbent retained.

AREA-005 requirements review returned `COMPLIANT`; quality and security review
returned `APPROVED`. Focused model-fitness unit, self-test, and production
checks, exact-eight staged lifecycle, strict registry over 463 tracked paths,
the full repository aggregate, all-files pre-commit, and final diff checks
passed. The affected and staged lanes are `PASS` for the exact eight closure
paths; manual strict/aggregate/diff checks and the all-files lane are `PASS`;
the pre-commit message/commit-msg lane was `SKIP` before commit identity
existed; hosted CI and provider-runtime/remote/live lanes are `DEFER` because
they were neither authorized nor observed.

The provider/model cutoff remains `2026-07-10 10:00 Asia/Seoul`; runtime,
provider discovery/authentication, model resolution, agent evaluation,
result adjudication, final admission, observed model fitness, threshold
satisfaction, promotion, canary, hosted CI, remote, live, and ignored
checkpoint execution remain `DEFER`. Spec 044 closure therefore means closed
repository-static readiness and fail-closed gate enforcement only. Exact
eight-path reciprocal closure commit
`42864832c966744ac4e5cf8c28baa5bf31ac2765` is observed with sole parent
`7891368e3d29e5e9e5e8ada4023118d331e38000`; this postflight evidence update
does not preclaim its own content-addressed commit SHA.
## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Static adapter parity is mistaken for admission or provider runtime support | Keep the AREA-002 projection and admission states distinct, and keep runtime, model resolution, hosted CI, remote, and live lanes explicitly `DEFER` unless observed. |
| Projected files are mistaken for admitted roles | Require AREA-003 four-class evaluation, independent adjudication, and rollback evidence before any final roster admission PASS. |
| New roles overlap existing owners | Admission validator rejects overlapping deliverables, excess authority, missing stop/handoff contracts, and unowned outputs. |
| `.gemini/**` files imply Gemini CLI execution | Provider note and model fitness validator require runtime canary evidence before runtime-ready claims. |
| A later repository observation silently moves the fixed cutoff | Validate the Spec 042 cutoff separately from repository observation dates and reject conflicting source-boundary values. |
| Model aliases drift after the cutoff | Model/effort entries remain candidate-only until Spec 042-style canary evidence and same-version evaluation pass; unsupported values fail closed rather than silently falling back. |
| Evaluation fixtures store sensitive data | Fixtures are synthetic/redacted only and must reject secret, transcript, auth-file, and shell-history payloads. |

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.agents/**`,
  `.claude/**`, `.codex/**`, `.gemini/**`,
  `docs/00.agent-governance/**`, `docs/03.specs/**`,
  `docs/03.specs/**`, `docs/99.templates/registry.json`,
  `scripts/**`, `tests/**`
- **Forbidden Paths**: credentials, auth caches, shell history, Vault/ESO
  values, live Kubernetes/GitOps state, provider account state, and
  `.agent-work/checkpoint.json`
- **Approval Required**: provider login, authenticated provider run, remote
  GitHub mutation, workflow/CI change, live cluster mutation, or credential
  changes
- **Static Validation**: focused Spec 044 validators, existing harness
  validators, lifecycle, strict registry, aggregate, all-files pre-commit, and
  diff checks
- **Live Validation**: `DEFER`; no live provider or cluster operation is
  authorized for this task
- **Secret / Vault Handling**: no secret reads, no secret prints, no credential
  fixture values, synthetic/redacted fixtures only
- **Rollback Plan**: revert the newest AREA unit in reverse dependency order;
  restore the last verified 10/3/30 current inventory if admission fails, and
  revert AREA-000 last without resetting or overwriting unrelated work
- **Evidence Location**: this Task and
  `../../00.agent-governance/memory/progress.md`
## Completion Criteria

- Spec 044 status, reciprocal Plan/Task status, indexes, and program lineage
  close as `done` after implementation and review.
- The harness contract reports current 12/4/48 repository-static inventory.
- All four adapter surfaces contain exactly one file per canonical role.
- AREA-002 records `repository-static-projected` / `DEFER`; it does not satisfy
  final roster admission by itself.
- New admission, evaluation, and model-fitness validators pass self-tests and
  repository checks.
- All 12 roles have versioned repository-static four-class corpus coverage,
  adjudication-readiness, and rollback-source evidence; the two new roles have
  distinct deliverable ownership and least-privilege stop/handoff behavior.
  Observed evaluation, result adjudication, and final admission remain
  `DEFER`.
- Provider-specific role model/effort profiles are recorded as candidate-only
  repository mappings with explicit baselines, thresholds, fallback, cutoff,
  and `DEFER` fitness, threshold, promotion, canary, and runtime verdicts.
- Existing aggregate, lifecycle, registry, Markdown, link/owner, affected
  surface, and all-files pre-commit gates pass.
- Independent requirements, quality, and security reviews accept the bounded
  repository-static claims and residual `DEFER` lanes.

AREA-000 through AREA-005 are complete at the repository-static readiness and
gate-enforcement boundary. Observed commits
`258955b3e0d999ec4ebc3de561d0db39ce11ac3c`,
`a15d5e10a4848aca013848571ba6d56c3568b5c3`, and
`7891368e3d29e5e9e5e8ada4023118d331e38000` establish AREA-004
implementation, its postflight, and AREA-005 semantic reconciliation.
The resulting contract covers exactly 12 roles, four provider surfaces, and 48
tuples; mapping readiness is `PASS` 21 / `DEFER` 27, configured incumbents are
retained, and every observed evaluation, final-admission, model-fitness,
threshold, promotion, canary, runtime, provider-authentication, hosted-CI,
remote, and live lane remains `DEFER` as applicable. AREA-005 requirements
were `COMPLIANT`, quality/security were `APPROVED`, and focused model, staged
lifecycle, strict registry `463`, full aggregate, all-files, and diff checks
passed. This reciprocal closure proposal does not preclaim its own future
commit SHA or postflight evidence update.

## Traceability

- **Spec**: [Agent Roster Evaluation and Admission](spec.md)
- **Task**: [Agent Roster Evaluation and Admission Task](README.md#task-records)
- **Program**: [PRD-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) and [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
- **Governing decision**: [ADR-0013](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
- **Proposed successor decision**: [ADR-0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **Successor**: [Spec 045](../0045-agent-governance-ci-qa-cutover/spec.md)
- **Prerequisite**: Spec 043 closure `a0bc3565` and postflight `80ffd6d9`

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-AREA-001](spec.md#success-criteria--verification-plan) | AREA-000, AREA-001, AREA-002 | [Activation and roster evidence](tasks/tsk-0001-area-000.md) |
| N/A — VAL-AREA-002 shares the Spec source above | AREA-001, AREA-002 | N/A — the reciprocal Task is linked in VAL-AREA-001 |
| N/A — VAL-AREA-003 and VAL-AREA-004 share the Spec source above | AREA-001, AREA-002 | N/A — the reciprocal Task is linked in VAL-AREA-001 |
| N/A — VAL-AREA-005 and VAL-AREA-006 share the Spec source above | AREA-001, AREA-003, AREA-004 | N/A — the reciprocal Task is linked in VAL-AREA-001 |
| N/A — VAL-AREA-007 shares the Spec source above | AREA-004 | N/A — the reciprocal Task is linked in VAL-AREA-001 |
| N/A — VAL-AREA-008 shares the Spec source above | AREA-004, AREA-005 | N/A — the reciprocal Task is linked in VAL-AREA-001 |

### Legacy Task traceability

- **Successor**: [Spec 045](../0045-agent-governance-ci-qa-cutover/spec.md)

#### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [AREA-000](plan.md#work-breakdown) | Done | Activation `b8b1a388` and clean-tree postflight `6d9b01d5`. |
| [AREA-001](spec.md#success-criteria--verification-plan) | Done | Closed admission/evaluation/model-fitness gates and postflight evidence in `0129daf7`; requirements `COMPLIANT`, security/model-path review `APPROVED`. |
| N/A — AREA-002 shares the Plan source above | Done | Commits `138ce6ac` and `1d03b0b4` project exact 12/4/48 repository-static inventory while preserving admission `DEFER`; focused, aggregate, all-files, requirements, and quality review gates passed. |
| N/A — AREA-003 shares the Plan source above | Done | Commit `3bd57590` establishes `repository-static-evaluation-ready` with 48 corpus records, 12 readiness adjudications, 2 source-bound rollback records, and explicit final admission `DEFER`; focused, aggregate, all-files, Spec, and quality review gates passed. |
| N/A — AREA-004 shares the Plan source above | Done | Commit `258955b3` establishes `repository-static-fitness-ready` for 12 roles, 4 providers, and 48 tuples; mapping is `PASS` 21 / `DEFER` 27, configured incumbents are retained, and all 48 fitness, threshold, promotion, canary, and runtime decisions remain `DEFER`; focused, lifecycle, strict-registry, aggregate, all-files, diff, and independent-review gates passed without provider/model execution; rollback state remains `armed-not-executed` with execution evidence `DEFER`. |
| N/A — AREA-005 shares the Plan source above | Done | Commit `7891368e` reconciles repository-static catalog/model/provider semantics; closure `42864832` records the exact eight-path reciprocal transition; focused model, staged lifecycle, strict registry `463`, aggregate, all-files, diff, requirements `COMPLIANT`, and quality/security `APPROVED` passed. The postflight evidence-update SHA remains unclaimed. |
