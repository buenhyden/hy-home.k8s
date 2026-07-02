---
title: 'Reference: Workspace Governance Baseline Research'
type: reference
status: draft
owner: platform
updated: 2026-07-02
---

# Reference: Workspace Governance Baseline Research

## Overview

이 문서는 `hy-home.k8s` 워크스페이스의 현재 governance baseline을 repo-backed evidence 기준으로 요약한다. 목적은 future agent와 maintainer가 workspace purpose, provider adapter model, QA/CI evidence lanes, template routing, scripts, hooks, approval boundaries를 빠르게 확인하도록 돕는 것이다.

This reference is descriptive. It summarizes canonical owners and current repository facts; it does not redefine active governance policy, CI enforcement, provider runtime behavior, or live-cluster procedure.

## Purpose

- Provide a durable baseline for the workspace harness research pack.
- Preserve a repo-first summary of the current governance, automation, validation, and documentation-routing model.
- Name canonical owners and follow-up routes so implementation checklists can point to the right source without changing policy here.

## Reference Type

- Type: durable-concept / external-standard-snapshot
- Source checked: 2026-07-02
- Refresh trigger: governance, CI, scripts, templates, provider adapter, or research pack structure changes.

## Authority Boundary

- **Authoritative for**:
  - Repo-backed summary of the current workspace governance baseline as checked on 2026-07-02.
  - Lookup-level mapping from governance concepts to canonical repository owners.
  - Research-pack implementation checklist items that name follow-up routes instead of changing policy.
- **Not authoritative for**:
  - Active governance rules, provider runtime policy, CI semantics, approval boundaries, or hook behavior.
  - Live k3d, ArgoCD, Vault, ESO, Kubernetes, cloud, deployment, or secret readiness.
  - New plans, tasks, operational runbooks, or implementation contracts.

## Scope

- Covers repo-backed workspace purpose, operating model, roles, adapters, QA/CI gates, hooks, templates, scripts, approval boundaries, and SDLC positioning.
- Excludes market-scan claims, provider product claims, external runtime capability claims, and live environment validation.
- Excludes any change to canonical governance, scripts, workflow jobs, provider adapters, manifests, secrets, or operations procedures.

## Definitions / Facts

### Workspace purpose and operating model

`hy-home.k8s` is a WSL2+k3d home-lab platform managed through ArgoCD GitOps. The default operating model is repo-backed desired state: agents plan and edit from repository evidence, run repo-static validation, and do not mutate the live cluster unless a human explicitly approves an emergency or operator path.

Canonical purpose and intake routing live in [AGENTS.md](../../../AGENTS.md), [.codex/CODEX.md](../../../.codex/CODEX.md), and [bootstrap.md](../../00.agent-governance/rules/bootstrap.md). Work should be planned from the active stage taxonomy, GitOps manifests, infrastructure files, scripts, tests, and current validators.

### Roles and provider adapters

The workspace uses a canonical-core plus provider-adapter model:

- Governance rules and execution checklists are owned by `docs/00.agent-governance/rules/**`.
- Runtime roster, model tiers, skills, mirror surfaces, and readiness language are cataloged in [harness-catalog.md](../../00.agent-governance/harness-catalog.md).
- Shared skills, workflows, and output styles come from `.agents/` as the shared SSoT, while `.claude/` and `.codex/` expose provider-native or symlinked adapter surfaces.
- Codex uses `.codex/CODEX.md`, `.codex/hooks.json`, and `.codex/agents/*.toml` as local runtime/adaptor surfaces; `.codex/hooks.json` is context and validation wiring, not a Claude-style permission gate.

Follow-up route: new or changed runtime surfaces should update the harness catalog, harness implementation map, and relevant approval-boundary owner in the same change set.

### CI/CD and QA

QA is split into separate evidence lanes:

- Repo/static readiness: local files, documentation contracts, validators, scripts, manifests, and task evidence.
- CI/toolchain readiness: GitHub Actions jobs and optional tools such as `pre-commit`, `kube-linter`, `conftest`, and other local tooling.
- Live runtime readiness: approved live checks only; it must not be inferred from repo-static or CI checks.

The current GitHub CI workflow includes `branch-policy`, `changes`, `pre-commit`, `repo-quality-static`, `manifest-static`, and `ci-summary`. For docs/governance/script/runtime-surface changes, the local matching gate is `bash scripts/validate-repo-quality-gates.sh .`.

Follow-up route: CI workflow changes belong to `.github/workflows/**` and must preserve the static-vs-live evidence boundary documented in the CI/CD QA guide and harness implementation map.

### Automation and hooks

Shared hook behavior is implemented through scripts under `docs/00.agent-governance/hooks/*.sh` and provider wiring surfaces. Claude has native command permission and event wiring through `.claude/settings.json`; Codex and Gemini rely on hook wiring and behavioral compliance rather than an equivalent native permission gate.

Hooks and validators are feedback loops. They surface template routing, lifecycle validation, repository quality checks, manifest checks, and completion evidence requirements, but agents still need to run explicit validation before handoff.

Follow-up route: hook behavior changes belong in the shared hook scripts, provider wiring files, and repository quality gates, with evidence in a Stage 04 task and `memory/progress.md`.

### Templates and formatting

Authored documents under the active stage taxonomy must use the canonical template mapping in [docs/99.templates/README.md](../../99.templates/README.md) and routing rules in [document-stage-routing.md](../../00.agent-governance/rules/document-stage-routing.md). Reference documents under `docs/90.references/**` use [reference.template.md](../../99.templates/reference.template.md).

Language boundaries are stage-specific:

- Governance docs under `docs/00.agent-governance/**` are English-only.
- Human-facing README and overview text may use Korean.
- Reference metadata, source, freshness, authority boundary, generated-index contracts, and AI-agent routing notes should be English-first.

Follow-up route: template or routing drift should be fixed in `docs/99.templates/README.md`, the matching template, routing rules, README indexes, and validation scripts as needed.

### Scripts and validation

The current script inventory is maintained in [scripts/README.md](../../../scripts/README.md). It classifies validation scripts by retention tier and command contract. The core repo-quality gate validates documentation taxonomy, README `Link Basis` and `Related Documents`, structural template coverage, generated LLM Wiki freshness, script references, runtime mirror inventory, workflow contracts, and other repository-wide governance checks.

The manual harness wrapper `bash scripts/validate-harness.sh` bundles repo-static gates and does not add live checks. The requested Task 2 verification uses:

- `git diff --check`
- `bash scripts/validate-repo-quality-gates.sh .`

Follow-up route: script additions, removals, or semantic changes belong in `scripts/`, `scripts/README.md`, relevant CI/hook allowlists, task evidence, and progress memory.

### Operating contract and approval boundaries

The approval boundary matrix states the default: agents operate on repo-backed desired state, while live cluster mutation is not part of the default execution path. Protected surfaces include live cluster mutation, Vault/secret values, GitHub Actions permission expansion, GitOps sync/rollback, and operator-bound bootstrap or emergency actions.

External networked tools are read-only by default for research. Posting, publishing, pushing, merging, opening paid jobs, changing third-party resources, or modifying credentials requires explicit human approval.

Follow-up route: approval-boundary changes belong in [approval-boundaries.md](../../00.agent-governance/rules/approval-boundaries.md) and must preserve validation evidence and rollback ownership.

### Integration guides and SDLC position

The CI/CD QA guide positions local validation and GitHub Actions as complementary gates. Local `pre-commit` is the fast feedback path when available, while `repo-quality-static` and `manifest-static` are CI-backed lanes. Live runtime evidence belongs to approved operations procedures and runbook records.

The research pack itself sits in the SDLC as durable reference material: it supports later specs, plans, tasks, and operations docs, but it is not an implementation contract or runbook.

Follow-up route: if this baseline reveals a needed behavior change, create or update the owning Stage 00 rule, Stage 03 spec, Stage 04 plan/task, Stage 05 policy/runbook, script, or template rather than changing this reference into policy.

### Governance system and rules

The current governance system uses:

- Thin gateway files that route to Stage 00 and provider baselines.
- JIT loading through bootstrap, preflight, persona/scope, provider notes, memory, and postflight.
- Stage routing through the document-stage routing rules and templates README.
- Four-element harness framing: instruction/settings documents, architecture constraints, feedback loops, and knowledge stores.
- Evidence stores in Stage 04 task records and `docs/00.agent-governance/memory/progress.md`.

Follow-up route: repeated code, document, or structure drift should update the smallest durable harness surface that would have prevented recurrence: rule, skill/prompt, hook, validator, template, README index, archive Tombstone, or memory entry.

### Implementation checklist

- Confirm the target stage and template before authoring. Canonical owners: `docs/99.templates/README.md`, `reference.template.md`, and `document-stage-routing.md`.
- Keep research-pack references descriptive. Canonical owner for active governance remains `docs/00.agent-governance/**`.
- Keep README indexes current when adding or changing research references. Canonical owners: `docs/90.references/README.md` and `docs/90.references/research/README.md`.
- Record task status and validation evidence in the Stage 04 task. Canonical owner: `docs/04.execution/tasks/2026-07-02-workspace-harness-research-pack.md`.
- Append concise progress and reusable memory for repo-changing work. Canonical owner: `docs/00.agent-governance/memory/progress.md`.
- Run `git diff --check` and `bash scripts/validate-repo-quality-gates.sh .` before handoff. Canonical owners: `scripts/README.md` and `.github/workflows/ci.yml`.
- Route any CI semantic change to `.github/workflows/ci.yml` plus the CI/CD QA guide, not this reference.
- Route any approval-boundary change to `rules/approval-boundaries.md` and record rollback/evidence ownership.
- Route any provider-adapter or runtime-roster change to `harness-catalog.md`, `harness-implementation-map.md`, and the relevant provider baseline.
- Do not treat repo-static validation as live k3d, ArgoCD, Vault, ESO, Kubernetes, deployment, or secret readiness.

## Sources

- [AGENTS.md](../../../AGENTS.md)
- [.codex/CODEX.md](../../../.codex/CODEX.md)
- [Bootstrap Governance](../../00.agent-governance/rules/bootstrap.md)
- [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Document Stage Routing Rules](../../00.agent-governance/rules/document-stage-routing.md)
- [Agent Quality Standards](../../00.agent-governance/rules/quality-standards.md)
- [Harness Approval Boundaries](../../00.agent-governance/rules/approval-boundaries.md)
- [Local Harness Catalog](../../00.agent-governance/harness-catalog.md)
- [Harness Implementation Map](../../00.agent-governance/harness-implementation-map.md)
- [Common Governance & Mappings](../../00.agent-governance/common-governance.md)
- [CI/CD & QA Reference Guide](../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- [Scripts README](../../../scripts/README.md)
- [GitHub CI Workflow](../../../.github/workflows/ci.yml)
- [Reference Template](../../99.templates/reference.template.md)

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-02
- Next review trigger: governance, CI, scripts, templates, provider adapter, approval-boundary, harness catalog, implementation-map, or research pack structure changes.

## Related Documents

- **Parent research README**: [README.md](./README.md)
- **Parent references README**: [90.references README](../README.md)
- **Spec**: [Workspace Harness Research Pack Spec](../../03.specs/009-workspace-harness-research-pack/spec.md)
- **Plan**: [Workspace Harness Research Pack Plan](../../04.execution/plans/2026-07-02-workspace-harness-research-pack.md)
- **Task**: [Workspace Harness Research Pack Task](../../04.execution/tasks/2026-07-02-workspace-harness-research-pack.md)
- **Harness catalog**: [Local Harness Catalog](../../00.agent-governance/harness-catalog.md)
- **Implementation map**: [Harness Implementation Map](../../00.agent-governance/harness-implementation-map.md)
- **CI/CD QA guide**: [CI/CD & QA Reference Guide](../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- **Scripts README**: [Scripts README](../../../scripts/README.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
