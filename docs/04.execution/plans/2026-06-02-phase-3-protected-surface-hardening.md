---
title: 'Phase 3 Protected Surface Hardening Plan'
type: plan
status: done
owner: platform
updated: 2026-06-02
---

# Phase 3 Protected Surface Hardening Plan

## Overview

This document is the Phase 3 plan for executing approved protected-surface
changes based on the Phase 2 governance alignment plan. Phase 3 does not
redesign the Stage 00 canonical adapter model; it more clearly enforces the
repo-static versus live-runtime readiness boundary left as a deferred boundary
in Phase 1/2 across CI, hook runtime, template guidance, and governance
evidence.

## Context

The Phase 1 audit concluded that ADR-0013's Stage 00 canonical adapter model
should remain. Phase 2 fixed that conclusion and the deferred live-validation
boundary into Plan/Task traceability. The human operator then approved the
previously unapproved policy, runtime, CI, and template changes, and also
approved the CI topology, model policy, provider config, GitOps manifest, and
live validation scope. Within that approved scope, Phase 3 hardens only
protected surfaces with concrete drift and records protected surfaces with no
concrete drift as no-ops.

The narrow confirmed drift is that `.agents/**` is the shared asset SSoT but
was not explicitly included in the CI path filter and lifecycle/post-hook
repo-quality trigger surface. The work also strengthens template/runtime
wording so repo-static checks are not confused with live k3d, ArgoCD, Vault,
ESO, or deployment readiness.

## Goals & In-Scope

- **Goals**:
  - Ensure `.agents/**` shared asset changes trigger repository quality gates in CI and lifecycle/post hooks.
  - Include `.agents/hooks.json` in the provider hook JSON parse lane.
  - Describe SessionStart live probes as read-only runtime evidence and distinguish them from repo-static readiness.
  - Guide future Plan/Task templates to state the live runtime evidence boundary.
  - Run approved read-only live validation and record results or limitations.
  - Record Phase 3 implementation evidence in `docs/04.execution` and the progress ledger.
- **In Scope**:
  - `.github/workflows/ci.yml` path filter hardening.
  - Shared runtime hook scripts under `docs/00.agent-governance/hooks/`.
  - `scripts/validate-repo-quality-gates.sh` regression checks for the new trigger contract.
  - Non-structural `plan.template.md` and `task.template.md` guidance updates.
  - Governance/reference docs and README index updates required by the changed surfaces.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Reopen or replace ADR-0013.
  - Add new provider agents, model policy, provider TOML settings, GitOps manifests, or Kubernetes desired state without a concrete drift finding.
  - Promote HADS into the repository template contract.
  - Convert CI into deployment automation.
- **Out of Scope**:
  - Secret-value inspection, direct cluster mutation, external Vault mutation, deployment action, container publish, or commit push.
  - Private RTK database, credential, token, private key, or shell history inspection.

## Requirements & Acceptance Criteria

| Requirement | Acceptance Criteria |
| --- | --- |
| REQ-P3-001 | CI `repo_quality` path filter includes `.agents/**`. |
| REQ-P3-002 | `post-validate.sh` and `lifecycle-guard.sh` run repo-quality gates for `.agents/**` shared asset changes. |
| REQ-P3-003 | Runtime JSON parse checks include `.agents/hooks.json` with `.claude/settings.json` and `.codex/hooks.json`. |
| REQ-P3-004 | SessionStart output distinguishes skipped/read-only live probes from repo-static readiness evidence. |
| REQ-P3-005 | Future Plan/Task template guidance records live runtime evidence and human approval boundaries without adding new required headings. |
| REQ-P3-006 | Repository quality gate enforces the new `.agents/**` trigger contract. |
| REQ-P3-007 | Phase 3 Plan/Task, README indexes, Phase 2 downstream links, and progress ledger are updated. |
| REQ-P3-008 | Approved read-only live validation is run, or any live validation limitation is recorded without claiming runtime readiness. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Harden CI shared asset trigger | `.github/workflows/ci.yml`, `scripts/validate-repo-quality-gates.sh` | REQ-P3-001, REQ-P3-006 | Quality gate fails if `.agents/**` is absent from the CI repo-quality filter. |
| PLN-002 | Harden runtime hook trigger and JSON parse lanes | `docs/00.agent-governance/hooks/post-validate.sh`, `docs/00.agent-governance/hooks/lifecycle-guard.sh` | REQ-P3-002, REQ-P3-003 | Hooks include `.agents/*` repo-quality matching and parse `.agents/hooks.json`. |
| PLN-003 | Clarify SessionStart live-readiness boundary | `docs/00.agent-governance/hooks/session-start.sh` | REQ-P3-004 | SessionStart states live probes are read-only and not repo-static readiness proof. |
| PLN-004 | Update template and governance guidance | `docs/99.templates/templates/sdlc/execution/plan.template.md`, `docs/99.templates/templates/sdlc/execution/task.template.md`, governance/reference docs | REQ-P3-005 | Template guidance changes do not add required headings and quality gates pass. |
| PLN-005 | Record Phase 3 execution evidence | Phase 3 Plan/Task, README indexes, Phase 2 links, progress ledger | REQ-P3-007 | Artifacts are indexed and linked with `status: done`, `owner: platform`, and related docs. |
| PLN-006 | Run approved read-only live validation | `docs/00.agent-governance/hooks/session-start.sh`, `infrastructure/tests/run-all.sh` | REQ-P3-008 | Live checks pass, or blockers are recorded as live validation limitations. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-P3-001 | Syntax | Check changed shell scripts | `bash -n docs/00.agent-governance/hooks/post-validate.sh docs/00.agent-governance/hooks/lifecycle-guard.sh docs/00.agent-governance/hooks/session-start.sh scripts/validate-repo-quality-gates.sh` | Exit 0. |
| VAL-P3-002 | Diff hygiene | Check whitespace and conflict marker issues | `git diff --check` | Exit 0. |
| VAL-P3-003 | Wiki index | Confirm generated LLM Wiki index remains current | `bash scripts/generate-llm-wiki-index.sh --check` | PASS. |
| VAL-P3-004 | Repository quality | Run repository governance, template, hook, CI, and static quality gates | `bash scripts/validate-repo-quality-gates.sh .` | PASS. |
| VAL-P3-005 | Shared asset trigger scan | Confirm `.agents/**` and `.agents/hooks.json` hardening appears in CI/hooks/validator | `rg -n "\\.agents/\\*\\*\|\\.agents/\\*\|\\.agents/hooks\\.json" .github/workflows/ci.yml docs/00.agent-governance/hooks/post-validate.sh docs/00.agent-governance/hooks/lifecycle-guard.sh scripts/validate-repo-quality-gates.sh` | Matches exist in all expected surfaces. |
| VAL-P3-006 | Phase 3 index scan | Confirm Phase 3 artifacts are indexed and linked | `rg -n "phase-3-protected-surface-hardening" docs/04.execution/plans/README.md docs/04.execution/tasks/README.md docs/04.execution/plans/2026-06-02-phase-2-governance-alignment.md docs/04.execution/tasks/2026-06-02-phase-2-governance-alignment.md` | README and Phase 2 downstream links report matches. |
| VAL-P3-007 | Approved live validation | Run read-only session and runtime probes | `HY_HOME_K8S_ENABLE_SESSION_LIVE_PROBES=1 bash docs/00.agent-governance/hooks/session-start.sh`; `bash infrastructure/tests/run-all.sh` | Commands pass, or live blockers are recorded without mutating the cluster. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Phase 3 expands into a new Stage 00 redesign | High | Keep ADR-0013 unchanged and modify only proven trigger/readiness-boundary surfaces. |
| Template changes force broad historical doc rewrites | High | Do not add new required H2 headings; add guidance inside existing template sections only. |
| CI/hook hardening is mistaken for live runtime proof | Medium | SessionStart and docs state repo-static, CI/toolchain, and live runtime evidence are separate lanes. |
| Runtime hook changes break JSON or shell parsing | Medium | Run shell syntax checks, JSON checks through quality gates, and hook payload simulations. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Shell syntax, diff hygiene, LLM Wiki freshness, repository quality gates, and targeted `.agents/**` trigger scans.
- **Sandbox / Canary Rollout**: Approved read-only live validation may run against the local k3d/Kubernetes/ArgoCD/Vault/ESO surfaces. Mutation remains out of scope.
- **Human Approval Gate**: Satisfied for policy, runtime hook, CI, template, CI topology, model policy, provider config, GitOps manifest, and live validation by the 2026-06-02 user requests. Model policy, provider config, and GitOps manifest are no-op in this implementation because no concrete drift was found. Live cluster mutation, secret-value inspection, deployment, external Vault mutation, and publish actions remain out of scope.
- **Rollback Trigger**: If hook payload simulation, CI YAML parsing, or repository quality gates fail, revert only Phase 3 CI/hook/template/docs changes.
- **Prompt / Model Promotion Criteria**: Not applicable. No prompt, model, or provider agent model policy is changed.

## Completion Criteria

- [x] CI repo-quality filter includes `.agents/**`.
- [x] Post-validate and lifecycle hooks include `.agents/*` repo-quality trigger matching.
- [x] Post-validate and lifecycle hooks parse `.agents/hooks.json`.
- [x] SessionStart output distinguishes read-only live probes from repo-static readiness.
- [x] Templates contain non-structural live-readiness boundary guidance.
- [x] Phase 3 Plan/Task are indexed and linked from Phase 2.
- [x] Static verification commands pass or limitations are recorded.
- [x] Approved read-only live validation passes or limitations are recorded.

## Rollback

- Remove `.agents/**` from the CI repo-quality path filter.
- Remove `.agents/*` and `.agents/hooks.json` handling from post-validate and lifecycle hooks.
- Restore the prior SessionStart wording.
- Revert Phase 3 template guidance additions.
- Remove Phase 3 Plan/Task files, README rows, Phase 2 related links, and the progress ledger entry.

## Related Documents

- **ADR**: [../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
- **Phase 1 Audit Task**: [../tasks/2026-06-02-phase-1-governance-alignment-audit.md](../tasks/2026-06-02-phase-1-governance-alignment-audit.md)
- **Phase 2 Plan**: [./2026-06-02-phase-2-governance-alignment.md](./2026-06-02-phase-2-governance-alignment.md)
- **Phase 2 Task**: [../tasks/2026-06-02-phase-2-governance-alignment.md](../tasks/2026-06-02-phase-2-governance-alignment.md)
- **Tasks**: [../tasks/2026-06-02-phase-3-protected-surface-hardening.md](../tasks/2026-06-02-phase-3-protected-surface-hardening.md)
- **Phase 4 Plan**: [./2026-06-02-phase-4-eso-vault-runtime-diagnosis.md](./2026-06-02-phase-4-eso-vault-runtime-diagnosis.md)
- **Phase 4 Task**: [../tasks/2026-06-02-phase-4-eso-vault-runtime-diagnosis.md](../tasks/2026-06-02-phase-4-eso-vault-runtime-diagnosis.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Plan Template**: [../../99.templates/templates/sdlc/execution/plan.template.md](../../99.templates/templates/sdlc/execution/plan.template.md)
