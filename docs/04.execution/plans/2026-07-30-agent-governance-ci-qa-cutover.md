---
title: 'Agent Governance CI and QA Cutover Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-08-01
---

# Agent Governance CI and QA Cutover Implementation Plan

## Overview

This Plan executes
[Spec 045](../../03.specs/045-agent-governance-ci-qa-cutover/spec.md)
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
python3 -m json.tool docs/99.templates/support/document-profiles.json
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

- **Spec**: [Agent Governance CI and QA Cutover](../../03.specs/045-agent-governance-ci-qa-cutover/spec.md)
- **Task**: [Agent Governance CI and QA Cutover Task](../tasks/2026-07-30-agent-governance-ci-qa-cutover.md)
- **Program**: [PRD-003](../../01.requirements/003-workspace-agent-governance-platform.md) and [ARD-0006](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md)
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
| [VAL-AGQC-001](../../03.specs/045-agent-governance-ci-qa-cutover/spec.md#success-criteria--verification-plan) | AGQC-000, AGQC-001, AGQC-002 | [Activation, topology, and CI contract evidence](../tasks/2026-07-30-agent-governance-ci-qa-cutover.md#task-table) |
| N/A — VAL-AGQC-002 through VAL-AGQC-004 share the Spec source above | AGQC-001, AGQC-002 | N/A — the reciprocal Task is linked in VAL-AGQC-001 |
| N/A — VAL-AGQC-005 and VAL-AGQC-006 share the Spec source above | AGQC-004 | N/A — the reciprocal Task is linked in VAL-AGQC-001 |
| N/A — VAL-AGQC-007 and VAL-AGQC-008 share the Spec source above | AGQC-003 | N/A — the reciprocal Task is linked in VAL-AGQC-001 |
| N/A — VAL-AGQC-009 shares the Spec source above | AGQC-005 | N/A — the reciprocal Task is linked in VAL-AGQC-001 |
| N/A — VAL-AGQC-010 shares the Spec source above | AGQC-000, AGQC-006 | N/A — the reciprocal Task is linked in VAL-AGQC-001 |
