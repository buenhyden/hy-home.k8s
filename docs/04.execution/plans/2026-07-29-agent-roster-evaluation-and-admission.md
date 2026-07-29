---
title: 'Agent Roster Evaluation and Admission Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-07-29
---

# Agent Roster Evaluation and Admission Implementation Plan

## Overview

This Plan executes
[Spec 044](../../03.specs/044-agent-roster-evaluation-and-admission/spec.md)
after the completed Spec 043 loop lifecycle closure. AREA-002 projects the
target-only 12-role / 4-surface / 48-adapter design into tracked
repository-static implementation while keeping candidate decisions and the
admission verdict `DEFER`. AREA-003 separately owns the four-class evaluation,
independent adjudication, and rollback evidence required for final roster
admission.

## Context

Spec 041 currently owns the machine-readable harness contract with a current
10-role / 3-surface / 30-adapter inventory and a target-only 12-role /
4-surface / 48-adapter inventory. Spec 042 owns provider/source currentness and
keeps runtime/model-resolution claims separated from repository-static files.
Spec 043 owns bounded loop, checkpoint, and memory lifecycle controls.
Its terminal closure
`a0bc3565988e291980320dec8442405c7ef16eb6` and postflight
`80ffd6d92a53990b04e413c0acf7fbc879b437d4` are observed prerequisites.

The active transition first materializes `docs-researcher`,
`quality-engineer`, and the native `.gemini/agents/**` surface as current
repo-static projections. That transition is not final admission. This Plan
does not claim provider-native runtime discovery, authenticated execution,
hosted CI, remote, live Kubernetes/GitOps, or credential-bearing evidence.

Spec 042 fixes provider/model source evidence at
`2026-07-10 10:00 Asia/Seoul`. The harness contract's later
`sourceObservationCutoff` value is drift to reconcile, not authority to move
that fixed boundary; repository observations and source-cutoff facts remain
separate.

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
| AREA-005 | Reconcile catalog, provider notes, and quality gates | AREA-002, AREA-003, AREA-004 | Focused validators pass | aggregate, all-files pre-commit, review, and closure evidence |

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
python3 scripts/validate-agent-role-semantics.py --root .
python3 scripts/validate-agent-roster-currentness.py .
python3 scripts/validate-affected-surfaces.py --root . --self-test
python3 scripts/validate-document-lifecycle.py --root . --mode staged
python3 scripts/validate-document-contract-registry.py --root . --mode strict
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
git diff --check
```

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

## Completion Criteria

- Spec 044 status, reciprocal Plan/Task status, indexes, and program lineage
  close as `done` after implementation and review.
- The harness contract reports current 12/4/48 repository-static inventory.
- All four adapter surfaces contain exactly one file per canonical role.
- AREA-002 records `repository-static-projected` / `DEFER`; it does not satisfy
  final roster admission by itself.
- New admission, evaluation, and model-fitness validators pass self-tests and
  repository checks.
- All 12 roles have versioned four-class evaluation coverage, adjudication, and
  rollback evidence; the two new roles have distinct deliverable ownership and
  least-privilege stop/handoff behavior.
- Provider-specific role model/effort profiles are optimized as candidate-only
  repository mappings with explicit baselines, thresholds, fallback, cutoff,
  and `DEFER` runtime-resolution verdicts unless an authorized canary was
  actually observed.
- Existing aggregate, lifecycle, registry, Markdown, link/owner, affected
  surface, and all-files pre-commit gates pass.
- Independent requirements, quality, and security reviews accept the bounded
  repository-static claims and residual `DEFER` lanes.

## Traceability

- **Spec**: [Agent Roster Evaluation and Admission](../../03.specs/044-agent-roster-evaluation-and-admission/spec.md)
- **Task**: [Agent Roster Evaluation and Admission Task](../tasks/2026-07-29-agent-roster-evaluation-and-admission.md)
- **Program**: [PRD-003](../../01.requirements/003-workspace-agent-governance-platform.md) and [ARD-0006](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md)
- **Governing decision**: [ADR-0013](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
- **Proposed successor decision**: [ADR-0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **Prerequisite**: Spec 043 closure `a0bc3565` and postflight `80ffd6d9`

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-AREA-001](../../03.specs/044-agent-roster-evaluation-and-admission/spec.md#success-criteria--verification-plan) | AREA-000, AREA-001, AREA-002 | [Activation and roster evidence](../tasks/2026-07-29-agent-roster-evaluation-and-admission.md#task-table) |
| N/A — VAL-AREA-002 shares the Spec source above | AREA-001, AREA-002 | N/A — the reciprocal Task is linked in VAL-AREA-001 |
| N/A — VAL-AREA-003 and VAL-AREA-004 share the Spec source above | AREA-001, AREA-002 | N/A — the reciprocal Task is linked in VAL-AREA-001 |
| N/A — VAL-AREA-005 and VAL-AREA-006 share the Spec source above | AREA-001, AREA-003, AREA-004 | N/A — the reciprocal Task is linked in VAL-AREA-001 |
| N/A — VAL-AREA-007 shares the Spec source above | AREA-004 | N/A — the reciprocal Task is linked in VAL-AREA-001 |
| N/A — VAL-AREA-008 shares the Spec source above | AREA-004, AREA-005 | N/A — the reciprocal Task is linked in VAL-AREA-001 |
