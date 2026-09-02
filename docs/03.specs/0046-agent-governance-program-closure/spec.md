---
title: 'Agent Governance Program Closure Technical Specification'
version: "1.0.0"
type: sdlc/spec
layer: "specs"
status: done
owner: platform
updated: 2026-08-01
artifact_id: "SPEC-0046"
---

# Agent Governance Program Closure Technical Specification (Spec)

## Overview

This Spec is the final repository-local integrator for the workspace
agent-governance program. It closes the PRD 003, AD 0006, ADR 0019, and Specs
041-045 chain by validating one machine-readable closure contract over the
current harness, loop, provider, roster, CI/QA, and legacy-cutover evidence.

Closure is evidence-lane aware. Repository-static contracts, fixtures,
validators, local tests, local QA, and independent reviews may close with PASS
when observed in this repository. Provider runtime/authentication, hosted
GitHub Actions, branch protection, remote execution, live Kubernetes/GitOps,
actual evaluation/admission/promotion, and actual model-fitness promotion stay
separate result lanes. They may be recorded as `ABSENT` or `DEFER` only with
an owner, limitation, and retry trigger; they must not be summarized as PASS.

The fixed provider/model/source observation cutoff remains
`2026-07-10T10:00:00+09:00` / `2026-07-10T01:00:00Z`, as owned by
`provider-runtime-evidence.json`. The Spec 046 activation date is not a new
provider or model freshness cutoff.

AGPC-004 closes this Spec and its reciprocal Plan and Task as terminal
repository documents, accepts ADR-0019 as the current decision, and keeps the
Spec 041 agent-design `active` as the current design owner. This transition
intentionally does not claim its own commit SHA. A separate AGPC-004 postflight
must observe that terminal commit. The AGPC-005 Task row is `Archived` because
local `main` integration and worktree/branch cleanup moved to the post-terminal
root finishing handoff; those actions remain planned and unexecuted. The `done`
document state does not promote any provider/runtime, hosted, actual-evaluation,
remote, or live lane.

## Strategic Boundaries & Non-goals

- **In scope**: predecessor closure matrix; canonical closure contract and
  schema; exact 12-role / 48-adapter repository-static parity; provider canary
  record classification; loop and memory recovery evidence; CI/QA and legacy
  cutover evidence; independent review; reciprocal Spec/Plan/Task closure; and
  a clean local branch handoff.
- **Protected boundaries**: no secret, token, auth cache, shell history,
  private transcript, provider response body, live cluster value, ignored
  checkpoint content, or provider-local memory value is read or retained.
- **Non-goals**: provider login, credential entry, hosted workflow dispatch,
  branch-protection mutation, push, PR creation, remote merge, release, live
  cluster mutation, deployment readiness, or promotion of unobserved runtime
  and evaluation lanes.

## Contracts

Spec 046 closure requires the following repository-local contract:

1. Specs 038-045 have allowed terminal states and committed evidence.
2. PRD 003, AD 0006, ADR 0019, and Specs 041-046 have reciprocal links and
   status/index/profile agreement.
3. One closure contract and one adjacent schema are the current machine owner
   for program closure result classification.
4. The closure contract contains one row per predecessor criterion and rejects
   missing, duplicate, stale, ownerless, or lane-collapsed evidence.
5. Current harness, provider, loop, roster, evaluation-readiness, CI/QA, and
   legacy-cutover contracts validate against their current schemas.
6. The canonical repository-static roster contains exactly 12 roles and four
   provider surfaces with exactly 48 adapter tuples.
7. Claude, Codex, and Gemini each have an independent classified canary record.
   Provider-runtime readiness requires a canary PASS; `ABSENT` and `DEFER`
   are accepted only as limitations with owner and retry trigger.
8. Evaluation readiness, model policy, and model/reasoning profile mapping may
   close only at the repository-static configured-evidence boundary. Actual
   model fitness, adjudication, admission, and promotion remain `DEFER` unless
   separately observed.
9. Local repository tests, affected/staged gates, all-files pre-commit,
   formatter rerun review, and both diff checks pass after the final change.
10. Independent requirements and quality/security reviewers approve the whole
    branch, and all findings are fixed and re-reviewed.
11. Worktree state and logical commit history are clean before local merge or
    cleanup.

## Core Design

### Closure Matrix

The closure matrix records each predecessor criterion with:

- owning document and criterion/work-package ID;
- implementation commit or exact commit range;
- validator or test command;
- result lane and result class;
- evidence digest or short human-readable summary;
- reviewer verdict where applicable;
- limitation, residual risk, owner, retry trigger, and rollback path.

The validator rejects a row when required repository-local evidence is not
PASS, when a provider/hosted/remote/live lane is collapsed into repository
PASS, or when a non-PASS limitation lacks owner and retry trigger.

### Provider Canary Classification

Each provider record is independent and secret-free:

- `claude`: repository-static adapter/config evidence exists; native runtime
  execution is `ABSENT` or `DEFER` unless the CLI/authenticated canary is
  separately observed.
- `codex`: repository-static adapter/config evidence exists; local Codex CLI
  availability may be recorded as an environment observation, but provider
  runtime/auth/model discovery remains a separate canary lane.
- `gemini`: repository-static project surface and adapter evidence exist;
  Gemini CLI/native runtime execution is `ABSENT` or `DEFER` unless separately
  installed, authenticated, and observed.

The canary set records provider, observation timestamp, source cutoff,
config/instruction source, discovered role surface, configured model and
reasoning-effort value or provider-native equivalent, auth class, MCP/policy
summary, result, limitation, owner, retry trigger, and rollback/cleanup note.

### Model And Reasoning Profiles

Spec 046 validates that provider-specific agent records point to the current
approved model-policy and that each role has an explicit configured
`model`/`model_reasoning_effort` or provider-native equivalent. The validator
checks configuration completeness and policy alignment only. It does not claim
that the configured models have passed live fitness, admission, or promotion.

### Memory Layers

Closure covers the four repository-local memory layers introduced by the
program:

- working short-term task memory;
- durable long-term progress memory;
- domain-scoped memory for role and area knowledge; and
- provider-local auxiliary memory.

The closure contract validates owner, sensitivity, promotion path,
retention/expiry, compaction source and replacement, archive/GC disposition,
conflict handling, and handoff rules. It does not read provider-local memory
values or ignored checkpoint contents.

## Data Modeling & Storage Strategy

The durable closure record is stored in
`docs/00.agent-governance/contracts/agent-governance-closure.json` with schema
`docs/00.agent-governance/contracts/agent-governance-closure.schema.json`.
The canonical execution evidence remains in the reciprocal Stage 04 Task and
the durable progress ledger.

The contract uses explicit result lanes:

- `repository_static`
- `local_validation`
- `local_review`
- `provider_runtime`
- `hosted_ci`
- `remote_action`
- `live_platform`
- `actual_evaluation`

Allowed result classes are `PASS`, `FAIL`, `ABSENT`, and `DEFER`. `PASS` is
valid only for an observed lane. `ABSENT` and `DEFER` require owner,
limitation, and retry trigger. `FAIL` requires remediation or a successor
owner and cannot support closure of required repository-local criteria.

## Interfaces & Data Structures

- **Closure contract**: program ID, cutoff, activation predecessor, predecessor
  criteria, lane results, provider records, model profile summary, memory
  layer summary, QA evidence, review evidence, limitations, and handoff.
- **Validator**:
  `python3 scripts/validate-agent-governance-closure.py --root .`.
- **Fixture**:
  `tests/fixtures/agent-governance-closure.json` carries a positive closure
  example plus self-test mutation coverage.
- **Consumer routing**: repository-quality, pre-commit, GitHub workflow,
  validation-surfaces contract, implementation map, and provider governance
  docs list the closure validator without making it a provider-runtime gate.

## Edge Cases & Error Handling

- A present adapter file does not prove provider runtime discovery.
- A local CLI version does not prove authenticated provider canary PASS.
- A repository-static mapping PASS does not prove actual model fitness or
  promotion.
- Two provider canary PASS results do not imply the third provider is ready.
- Hosted workflow YAML validation does not imply a current hosted run PASS.
- Live Kubernetes/GitOps desired state does not imply live readiness.
- Any `DEFER` or `ABSENT` without owner and retry trigger is invalid.
- Any formatter mutation after QA requires review, staging, and rerun before
  closure.

## Failure Modes & Fallback / Human Escalation

- Stop closure when any required repository-local predecessor, contract,
  validator, local QA, or independent review result fails.
- Escalate to the platform/security owner for provider login, credential
  renewal, paid action, branch-protection mutation, remote workflow dispatch,
  live cluster mutation, push, PR, merge, or release.
- If live/provider/hosted evidence is unavailable, record it as `ABSENT` or
  `DEFER` with owner and retry trigger rather than weakening the contract.
- If a review finding requires changing the requirement, update PRD, AD, ADR,
  or the owning Spec first, then revalidate.

## Verification Commands

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

The first three commands are Spec 046 deliverables. They are not claimed to
exist until AGPC-001 creates the contract, schema, fixture, validator, and
tests.

## Success Criteria & Verification Plan

- **VAL-AGPC-001**: Specs 038-045 and upstream PRD/AD/ADR lineage have
  committed, reciprocal, current-state evidence.
- **VAL-AGPC-002**: The closure contract/schema/validator/fixture/tests are
  closed and reject lane collapse, missing rows, stale owners, and ownerless
  limitations.
- **VAL-AGPC-003**: Harness, provider, loop, roster, evaluation-readiness,
  model-policy, CI/QA, and legacy-cutover contracts validate at their
  repository-static boundary.
- **VAL-AGPC-004**: The current roster is exactly 12 roles and 48 adapter
  tuples across four surfaces.
- **VAL-AGPC-005**: Claude, Codex, and Gemini canary records are independently
  classified and keep provider-runtime readiness separate from repository
  PASS.
- **VAL-AGPC-006**: Model and reasoning-effort settings are complete and
  policy-aligned for provider-specific agents without claiming actual
  promotion.
- **VAL-AGPC-007**: Four memory layers validate owner, sensitivity, promotion,
  retention, compaction, archive/GC, conflict, and handoff rules without
  reading private state.
- **VAL-AGPC-008**: Local tests, affected/staged gates, repository aggregate,
  all-files pre-commit, formatter rerun, and diff checks pass.
- **VAL-AGPC-009**: Whole-branch requirements and quality/security review are
  approved with no open findings.
- **VAL-AGPC-010**: AGPC-004 owns reciprocal terminal documents and the
  separate observed postflight. The AGPC-005 Task row archives local `main`
  integration plus worktree/branch cleanup into the post-terminal root
  finishing handoff. The terminal document portion is complete without a
  self-SHA preclaim, while commit observation and the planned local finishing
  actions remain unexecuted; no remote action is authorized.

## Traceability

- **PRD**: [PRD 003](../../01.requirements/0003-workspace-agent-governance-platform.md)
- **AD**: [AD 0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
- **Decision**: [ADR 0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **Document-lifecycle prerequisites**: [Spec 038](../0038-reference-information-architecture/spec.md),
  [Spec 039](../0039-github-ci-qa-evidence/spec.md), and
  [Spec 040](../0040-contract-cutover-and-program-closure/spec.md)
- **Agent-governance predecessors**: [Spec 041](../0041-stage-00-agent-governance-contract/spec.md),
  [Spec 042](../0042-provider-native-runtime-and-model-evidence/spec.md),
  [Spec 043](../0043-agent-harness-loop-lifecycle/spec.md),
  [Spec 044](../0044-agent-roster-evaluation-and-admission/spec.md), and
  [Spec 045](../0045-agent-governance-ci-qa-cutover/spec.md)
- **Plan**:
  [Agent Governance Program Closure Implementation Plan](plan.md)
- **Task**:
  [Task: Agent Governance Program Closure](plan.md)

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — [Acceptance criterion 02](../../01.requirements/0003-workspace-agent-governance-platform.md#success--acceptance-criteria) remains package-owned | VAL-AGPC-001 | Predecessor and lineage validation proves the reciprocal program chain. |
| N/A — shared PRD 003 source above | VAL-AGPC-002 | Closure contract/schema/validator reject incomplete or lane-collapsed evidence. |
| N/A — shared PRD 003 source above | VAL-AGPC-003 | Current machine contracts validate at the repository-static boundary. |
| N/A — shared PRD 003 source above | VAL-AGPC-004 | Roster validation proves exact 12/48 repository-static parity. |
| N/A — shared PRD 003 source above | VAL-AGPC-005 | Provider canary validation keeps Claude, Codex, and Gemini lanes independent. |
| N/A — shared PRD 003 source above | VAL-AGPC-006 | Model-policy validation proves configured model and reasoning-effort completeness. |
| N/A — shared PRD 003 source above | VAL-AGPC-007 | Memory lifecycle validation proves four-class ownership and handoff rules. |
| N/A — shared PRD 003 source above | VAL-AGPC-008 | Local QA commands prove repository-static completion gates. |
| N/A — shared PRD 003 source above | VAL-AGPC-009 | Independent whole-branch review prevents waiver or catalog-only closure. |
| N/A — local completion constraint | VAL-AGPC-010 | AGPC-004 terminal documents are complete; separate commit observation and the archived-to-handoff local merge/worktree cleanup remain planned and unexecuted. |
