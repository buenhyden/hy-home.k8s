---
title: 'Reference: Local Harness Catalog'
type: reference
status: draft
owner: 'platform'
updated: 2026-05-24
---

# Reference: Local Harness Catalog

## Overview

This document is the canonical catalog for the local agent runtime used in `hy-home.k8s`.
It defines the supported agents, skills, model allocation, scope imports, and pattern families
that shape the runtime contract under `.claude/` and its Codex mirror under `.codex/`.

## Purpose

- Provide a single source of truth for the local runtime roster.
- Keep gateway files and runtime files in sync.
- Keep `.claude/agents/*.md` and `.codex/agents/*.toml` mirrors in sync.
- Record the model hierarchy for supervising and worker agents.
- Preserve pattern lineage without exposing source directory paths.

## Scope

- Covers local runtime agents, skills, scope imports, and model allocation.
- Does not duplicate rule text from `rules/`, `scopes/`, or `providers/`.
- Current remediation scope adds a `wiki-curator` runtime surface for LLM Wiki
  curation by explicit human request, while keeping all other new runtime
  surfaces out of scope unless this matrix records a concrete gap.

## Runtime Principles

- The local runtime is cluster-specific and GitOps-first.
- Supervising agents use `opus`.
- Task and worker agents use `sonnet`.
- Agent files are thin runtime bridges and must not duplicate governance policy.
- Codex mirror files are thin runtime bridges with the same contract as their `.claude` source.
- Skill files are either workflow contracts or reference-pattern contracts and
  must remain specific to this cluster.

## Readiness Evidence Boundary

`Ready` in this catalog means the repository surface exists, is wired into the local
governance/runtime contract, and is covered by repo-backed static gates where applicable.
It is not proof that GitHub CI, the full optional local toolchain, live k3d bootstrap,
ArgoCD health, or live cluster reconciliation completed in the current session.
Matrix validation is a regression and structure guard for catalog shape and required
fields. It is not semantic proof that every `Ready` claim was freshly revalidated.

Report readiness evidence in separate lanes:

- Repo/static readiness: local files, mirror contracts, command boundaries, and validation scripts.
- CI/toolchain readiness: GitHub Actions and optional tools such as `pre-commit`, `kube-linter`, `actionlint`, `zizmor`, `graphify`, and `rtk`.
- Live k3d readiness: human-approved bootstrap, ArgoCD reconciliation, Kubernetes API checks, and runtime health evidence.

## Matrix Status Contract

Matrix status values are limited to `Ready`, `Partial`, and `Missing`.

- `Ready` means repo/static surface readiness: the surface exists, is wired into
  governance/runtime contracts, and has no currently tracked concrete gap. A
  `Ready` row must use `Gap=None`.
- `Partial` means a surface exists but a concrete gap remains. The `Gap` field
  must name the incomplete behavior and `Remediation` must state how to close it.
- `Missing` means the required surface does not exist. The `Gap` field must name
  the missing surface and `Remediation` must state whether to create or defer it.

A `Ready` row is not semantic proof of agent behavior, GitHub CI, optional
toolchain availability, live k3d health, or ArgoCD reconciliation. When a human
explicitly requests a new runtime surface or future work discovers a concrete
gap, update this matrix first, then implement only the smallest surface needed
to close that gap.

## Readiness Matrix

| Layer | Implemented Surface | Status | Readiness Evidence |
| --- | --- | --- | --- |
| Gateway | `AGENTS.md`, root `CLAUDE.md`, root `GEMINI.md` | Ready | Thin routers point to governance docs and runtime baseline |
| Runtime baseline | `.claude/CLAUDE.md` | Ready | Defines loading order, GitOps-first boundary, roster pointers, and model hierarchy |
| Agents | `.claude/agents/*.md` | Ready | Eight local agents exist with frontmatter, scope imports, guardrails, handoff, and postflight |
| Codex mirrors | `.codex/agents/*.toml` | Ready | Mirror stems, imports, guardrails, and postflight are checked by `scripts/validate-repo-quality-gates.sh` |
| Skills | `.claude/skills/*/skill.md` | Ready | GitOps, validation, docs routing, docs stage conformance, deployment, incident, RCA, risk, security, and workspace harness audit workflows are local |
| Claude permissions/hooks | `.claude/settings.json`, `.claude/hooks/*.sh` | Ready | Claude runtime has allow/deny command policy plus SessionStart, PreToolUse, PostToolUse, Stop, SubagentStop, and PreCompact hooks; SessionStart live probes are opt-in with `HY_HOME_K8S_ENABLE_SESSION_LIVE_PROBES=1`; edit hooks warn on authored stage docs and run scoped auto-formatting, style validation, and documentation template enforcement; lifecycle hooks run objective repo-state validation and advise task-unit commit discipline for uncommitted tracked changes, while PreCompact remains advisory |
| Codex event hooks | `.codex/hooks.json` | Ready | Codex hook wiring reuses SessionStart, PreToolUse, PostToolUse, Stop, SubagentStop, PreCompact, graphify context, and authored-doc template enforcement where supported; SessionStart live probes remain opt-in through the shared hook script; Codex hooks are not a permission gate equivalent and remain context/validation wiring |
| Validation scripts | `scripts/*.sh`, `infrastructure/tests/*.sh` | Ready | Repo-backed gates cover quality, README `Link Basis` / `Related Documents`, structural template coverage, GitOps structure, manifests, contracts, secret handling, shell syntax, lifecycle hook payload simulation, authored-doc template enforcement, gateway thinness, language boundaries, Hookify local-rule shape, and hook-boundary clarity |
| Authored-doc command boundary | `scripts/validate-repo-quality-gates.sh`, staged docs | Ready | Risky command examples in authored docs require explicit human/operator boundary markers; authored docs block bare/main direct push and push examples without PR-flow context, while broader Markdown roots block bare/main direct push examples |
| Memory | `docs/00.agent-governance/memory/` | Ready | Agent progress and reusable memory have a local template-backed home; current runtime truth stays in this catalog and current script inventory stays in `scripts/README.md` |
| LLM Wiki curation | `.claude/agents/wiki-curator.md`, `.codex/agents/wiki-curator.toml`, `docs/90.references/llm-wiki/wiki-index.md`, `scripts/generate-llm-wiki-index.sh` | Ready | Runtime surface added for LLM Wiki curation with Markdown-only generated index and repo-quality freshness check |
| Escalation boundary | `subagent-protocol.md`, `rules/agentic.md` | Ready | Delegation, file ownership, direct mutation, and human approval boundaries are explicit |

## Harness Engineering Matrix

| Required Component | Current Surface | Status | Gap | Remediation |
| --- | --- | --- | --- | --- |
| Thin gateway | `AGENTS.md`, root `CLAUDE.md`, root `GEMINI.md` | Ready | None | Keep root files as routing shims and enforce line-count and pointer checks in `scripts/validate-repo-quality-gates.sh`. |
| Runtime baseline | `.claude/CLAUDE.md` | Ready | None | Keep loading order, GitOps-first boundary, roster pointers, and model hierarchy in the local baseline. |
| Agent roster | `.claude/agents/*.md` | Ready | None | Keep eight local agents thin, scope-imported, and aligned with this catalog. |
| Codex mirrors | `.codex/agents/*.toml` | Ready | None | Update the `.claude` source and Codex mirror in the same change set; keep mirror parity in the quality gate. |
| Skills | `.claude/skills/*/skill.md` | Ready | None | Keep cluster-specific workflows local and add new skills only when this matrix shows a concrete gap. |
| Claude permissions/hooks | `.claude/settings.json`, `.claude/hooks/*.sh` | Ready | None | Keep allow/deny command policy plus SessionStart, PreToolUse, PostToolUse, Stop, SubagentStop, and PreCompact hooks; keep SessionStart live probes opt-in with `HY_HOME_K8S_ENABLE_SESSION_LIVE_PROBES=1`; PostToolUse should run scoped auto-formatting and style validation before repository checks; Stop/SubagentStop may block objective repo-state failures and should advise task-unit commit discipline for uncommitted tracked changes, while PreCompact remains advisory. |
| Codex event hooks | `.codex/hooks.json` | Ready | None | Keep Codex hook scope limited to context and validation wiring; reuse the Claude hook scripts for authored-doc template enforcement and lifecycle validation; do not treat it as a Claude permission gate equivalent, and keep live startup probes opt-in through the shared hook script. |
| Validation scripts | `scripts/*.sh`, `infrastructure/tests/*.sh` | Ready | None | Keep repo-backed validation as the default completion evidence before handoff, including README section contracts, structural template coverage, lifecycle hook payload simulation, and local Hookify ignore/frontmatter checks. |
| Authored-doc command boundary | `scripts/validate-repo-quality-gates.sh`, staged docs | Ready | None | Keep `kubectl apply/patch`, `argocd app sync`, `vault kv put`, and push examples marked as human/operator-only or PR-flow work in authored docs, including operations policies; keep broader Markdown scans limited to bare/main direct push examples. |
| Memory | `docs/00.agent-governance/memory/` | Ready | None | Keep progress and reusable memory in `memory/progress.md`, while current runtime truth stays in this catalog. |
| LLM Wiki curation | `.claude/agents/wiki-curator.md`, `.codex/agents/wiki-curator.toml`, `docs/90.references/llm-wiki/wiki-index.md`, `scripts/generate-llm-wiki-index.sh` | Ready | None | Runtime surface added for LLM Wiki curation; keep it Markdown-only, generator-checked, and routed back to canonical owners. |
| Escalation boundary | `subagent-protocol.md`, `rules/agentic.md` | Ready | None | Keep delegation, destructive-action, live-mutation, and human-approval boundaries explicit. |

## Agent-first Engineering Matrix

| Required Component | Current Surface | Status | Gap | Remediation |
| --- | --- | --- | --- | --- |
| Evidence-first intake | `rules/bootstrap.md`, `rules/preflight-checklist.md`, `rules/agentic.md` | Ready | None | Plan from repo evidence, current diffs, validators, and scoped source files before editing. |
| Context hierarchy | `AGENTS.md`, `.claude/CLAUDE.md`, `docs/00.agent-governance/**` | Ready | None | Keep root context minimal, load governance just in time, and select task-specific docs instead of loading everything. |
| JIT loading | `rules/bootstrap.md`, `.claude/CLAUDE.md` | Ready | None | Keep the bootstrap -> preflight -> persona -> scope -> provider -> progress -> postflight sequence canonical. |
| Scope and persona routing | `rules/persona.md`, `scopes/*.md` | Ready | None | Resolve one primary layer before edits and transition explicitly when scope changes. |
| GitOps-first execution | `rules/agentic.md`, `.claude/settings.json`, GitOps docs and validators | Ready | None | Keep infrastructure changes repo-backed and prevent direct cluster mutation by default. |
| Documentation routing | `rules/document-stage-routing.md`, `rules/documentation-protocol.md`, `.claude/skills/docs-stage-routing/skill.md`, `.claude/hooks/*.sh`, `.codex/hooks.json` | Ready | None | Keep generated docs in the canonical stage tree, use templates before authoring, and keep Claude/Codex edit hooks enforcing the template contract. |
| LLM Wiki curation | `.claude/agents/wiki-curator.md`, `.codex/agents/wiki-curator.toml`, `docs/90.references/llm-wiki/wiki-index.md`, `scripts/generate-llm-wiki-index.sh` | Ready | None | Runtime surface added for LLM Wiki curation by explicit human request; route policy and procedure changes to canonical owners instead of the generated index. |
| Authored-doc command boundaries | `scripts/validate-repo-quality-gates.sh`, `docs/02.architecture/decisions`, `docs/03.specs`, `docs/05.operations/guides`, `docs/05.operations/policies`, `docs/05.operations/runbooks` | Ready | None | Keep risky command examples framed as human/operator-approved bootstrap, break-glass, external secret, or PR-flow work. |
| Validation before completion | `scripts/*.sh`, `infrastructure/tests/*.sh`, `.github/workflows/ci.yml`, `.claude/hooks/lifecycle-guard.sh` | Ready | None | Define validation evidence before editing, keep lifecycle hook payload simulation in the quality gate, and report skipped or unavailable local tools honestly. |
| Postflight and handoff | `rules/postflight-checklist.md`, `subagent-protocol.md`, `.claude/hooks/lifecycle-guard.sh` | Ready | None | Complete postflight checks, preserve handoff evidence before final response, and treat lifecycle hooks as a final repo-state guard rather than a replacement for human-readable evidence. |

Direct cluster mutation is not part of the default Agent-first execution path.
Any `kubectl apply`, `kubectl patch`, external secret change, or live-cluster mutation
belongs to a human-approved bootstrap or break-glass path with explicit evidence.

## Agents

| File                                   | Role                                   | Model    | Scope Imports  | Responsibility                                                          | Lineage Family                               |
| -------------------------------------- | -------------------------------------- | -------- | -------------- | ----------------------------------------------------------------------- | -------------------------------------------- |
| `.claude/agents/supervisor.md`         | Task routing and orchestration control | `opus`   | `meta`         | Select agents, enforce completion gates, synthesize outcomes            | orchestration                                |
| `.claude/agents/k8s-implementer.md`    | Kubernetes manifest authoring          | `sonnet` | `infra`        | Author GitOps-safe manifest changes and prepare validation-ready output | cicd-pipeline, infra-as-code, security-audit |
| `.claude/agents/gitops-reviewer.md`    | GitOps pipeline and ArgoCD review      | `sonnet` | `infra`        | Review sync targets, Kustomize structure, and GitOps release safety     | cicd-pipeline, infra-as-code, security-audit |
| `.claude/agents/security-auditor.md`   | Kubernetes security review             | `sonnet` | `security`     | Review RBAC, network isolation, and secret handling                     | security-audit                               |
| `.claude/agents/incident-responder.md` | Cluster incident analysis              | `sonnet` | `ops`, `infra` | Reconstruct timelines, assess impact, and define remediation            | incident-postmortem                          |
| `.claude/agents/code-reviewer.md`      | YAML, Helm, and shell quality review   | `sonnet` | `architecture` | Review correctness, maintainability, and policy alignment               | code-reviewer                                |
| `.claude/agents/doc-writer.md`         | Documentation routing and delegated drafting | `sonnet` | `docs`         | Support template/routing alignment and delegated stage document updates | technical-writer                             |
| `.claude/agents/wiki-curator.md`       | LLM Wiki curation                      | `sonnet` | `docs`         | Maintain generated canonical-owner link maps and route stale links      | technical-writer, governance                 |

## Codex Mirrors

`.codex/agents/*.toml` mirrors the corresponding `.claude/agents/*.md` worker
contracts for Codex execution. Mirror files must keep the same name, role,
scope imports, guardrails, and postflight requirements. Update the `.claude`
source and Codex mirror in the same change set.

Mirror consistency is a quality-gate contract. `scripts/validate-repo-quality-gates.sh`
must be able to verify matching file stems, matching scope imports, Runtime
Bootstrap text, Guardrails, Handoff / Escalation, and Postflight requirements
across the `.claude` source and `.codex` mirror.

## Skills

| Path                                             | Contract Type | Purpose                                                                                                                          | Supported Workflows                                                                 | Lineage Family                               |
| ------------------------------------------------ | ------------- | -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------- |
| `.claude/skills/gitops-workflow/skill.md`        | workflow      | Define the approved GitOps workflow for onboarding, updating, and diagnosing workloads                                           | onboarding, change review, sync diagnosis                                           | cicd-pipeline, infra-as-code, security-audit |
| `.claude/skills/docs-stage-routing/skill.md`     | workflow      | Route generated documentation into the canonical stage tree and block parallel doc hierarchies                                   | doc routing, template selection, stage mapping, superpowers rerouting                | governance, technical-writer                  |
| `.claude/skills/docs-stage-conformance/skill.md` | workflow      | Audit and fix authored docs, README indexes, template conformance, links, headings, and validation evidence without semantic rewrites | docs cleanup, template conformance, README/index drift, duplicate-H1 cleanup         | governance, technical-writer                  |
| `.claude/skills/k8s-validate/skill.md`           | workflow      | Define the manifest validation pipeline for YAML, GitOps structure, and secret scanning                                          | validation, pre-PR checks, failure triage                                           | cicd-pipeline, infra-as-code, security-audit |
| `.claude/skills/risk-report/skill.md`            | workflow      | Define the cluster risk register workflow and output shape                                                                       | risk identification, risk tracking, review cadence                                  | risk-register                                |
| `.claude/skills/workspace-harness-audit/skill.md` | workflow      | Define the workspace-wide Gap analysis workflow for broad WSL2/k3d/ArgoCD GitOps, SDD lifecycle, QA, CI/CD, and governance prompts | workspace gap analysis, full target inventory, skill path checks, implementation planning | supervisor, doc-writer, gitops-reviewer      |
| `.claude/skills/deployment-strategies/skill.md`  | reference-pattern | Kubernetes and ArgoCD deployment strategy catalog with YAML patterns, health check probes, rollback procedures, and DORA metrics | deployment planning, strategy selection, rollback, DORA measurement                 | cicd-pipeline                                |
| `.claude/skills/incident-postmortem/skill.md`    | workflow      | Full pipeline for cluster incident post-analysis: timeline -> RCA -> impact -> remediation -> postmortem report                  | postmortem authoring, incident review, RCA, remediation planning                    | incident-postmortem                          |
| `.claude/skills/rca-methodology/skill.md`        | reference-pattern | Structured RCA technique reference: 5 Whys, Fishbone, Fault Tree Analysis, Change Analysis, and cognitive bias prevention        | root cause analysis, 5 Whys, fishbone, FTA, change analysis                         | incident-postmortem                          |
| `.claude/skills/k8s-security-audit/skill.md`     | workflow      | Structured security audit workflow: RBAC, NetworkPolicy, Secret handling, container security context, and image supply chain     | security audit, RBAC review, network policy audit, secret scanning, CIS benchmark   | security-audit                               |
| `.claude/skills/vulnerability-patterns/skill.md` | reference-pattern | Kubernetes manifest and Helm chart vulnerability pattern catalog with vulnerable/safe YAML examples and CIS benchmark mappings   | manifest hardening, YAML security review, Helm security, misconfiguration detection | security-audit, code-reviewer                |

Workflow skills define ordered execution behavior and expected outputs.
Reference-pattern skills provide reusable judgment catalogs, examples, and
review heuristics. Do not require every reference-pattern skill to carry the
same checklist shape as a workflow skill; instead, keep its trigger,
applicable review surface, and failure boundaries clear.

## Task-to-Skill Routing

Use the repo-local `.claude/skills/**` roster first for cluster-specific work.
When a user prompt explicitly requires external `SKILL.md` paths, treat those
paths as external requested skills for that task only. Missing external paths
must be recorded as a Gap rather than silently replaced by a similar local
skill.

| Task Area | Repo-local or External Requested Skill Paths | Routing Notes |
| --- | --- | --- |
| Workspace investigation and analysis | external requested: `/home/hy/.agents/skills/grill-with-docs/SKILL.md` | Use with architecture, DevOps, QA, Kubernetes, and documentation review skills when a prompt requests full-workspace analysis. |
| Documentation writing | repo-local: `.claude/skills/docs-stage-routing/skill.md`, `.claude/skills/docs-stage-conformance/skill.md`; external requested: `/home/hy/.agents/skills/documentation-writer/SKILL.md`; `/home/hy/.agents/skills/humanizer/SKILL.md`; `/home/hy/gstack/.agents/skills/gstack-document-release/SKILL.md`; `/home/hy/.agents/skills/technical-blog-writing/SKILL.md` | Use docs-stage routing for new canonical artifacts and docs-stage conformance for narrow in-place cleanup, template, README, link, and heading drift. |
| Documentation co-authoring and release | external requested: `/home/hy/.agents/skills/doc-coauthoring/SKILL.md`; `/home/hy/gstack/.agents/skills/gstack-document-release/SKILL.md`; `/home/hy/.agents/skills/humanizer/SKILL.md` | Use for review/release workflow, not for replacing template contracts. |
| Repeated workflow and instruction skills | external requested: `/home/hy/.codex/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/writing-skills/SKILL.md`; `/home/hy/.codex/trailofbits-skills/plugins/skill-improver/skills/skill-improver/SKILL.md`; `/home/hy/.agents/skills/skill-creator/SKILL.md`; `/home/hy/.agents/skills/write-a-skill/SKILL.md` | Prefer updating existing repo-local skills or catalog entries before adding new surfaces. |
| Subagent creation and subagent-driven work | external requested: `/home/hy/.codex/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/subagent-driven-development/SKILL.md` | Use only after an implementation plan has independent tasks and local subagent protocol constraints are satisfied. |
| Hook work | external requested: `/home/hy/.agents/skills/hook-development/SKILL.md`; `/home/hy/.codex/plugins/cache/claude-plugins-official/hookify/local/skills/writing-rules/SKILL.md` | Keep shared enforcement in tracked hooks, settings, Codex hook wiring, and validators. |
| Native instruction files and runtime governance | external requested: `/home/hy/.codex/plugins/cache/claude-plugins-official/claude-md-management/1.0.0/skills/claude-md-improver/SKILL.md`; `/home/hy/.agents/skills/claude-md-improver/SKILL.md`; `/home/hy/.agents/skills/agent-md-refactor/SKILL.md` | Keep `AGENTS.md`, root `CLAUDE.md`, and `GEMINI.md` as thin gateways. |
| Scripts | external requested: `/home/hy/.agents/skills/bash-scripting/SKILL.md` | Keep scripts single-purpose, deterministic, and static unless a human approves live operations. |
| Kubernetes and infrastructure | repo-local: `.claude/skills/gitops-workflow/skill.md`, `.claude/skills/k8s-validate/skill.md`; external requested: `/home/hy/.agents/skills/senior-devops/SKILL.md`; `/home/hy/.agents/skills/senior-architect/SKILL.md`; `/home/hy/.agents/skills/architect-review/SKILL.md`; `/home/hy/.agents/skills/architecture/SKILL.md`; `/home/hy/.agents/skills/kubernetes-specialist/SKILL.md`; `/home/hy/.agents/skills/kubernetes-architect/SKILL.md`; `/home/hy/.agents/skills/kubernetes-deployment/SKILL.md` | GitOps-first and no direct live mutation remain mandatory. |
| QA | external requested: `/home/hy/.agents/skills/senior-qa/SKILL.md`; `/home/hy/.agents/skills/testing-qa/SKILL.md`; `/home/hy/.codex/trailofbits-skills/plugins/testing-handbook-skills/skills/coverage-analysis/SKILL.md` | Use repo-static validation first; live QA requires approved runtime context. |
| CI/CD | external requested: `/home/hy/.agents/skills/senior-devops/SKILL.md`; `/home/hy/.agents/skills/devops-engineer/SKILL.md`; `/home/hy/.agents/skills/devops-troubleshooter/SKILL.md` | CI structure changes require separate review if they alter gates or dependencies. |

Workspace-local `.agents/skills/**` files are ignored convenience mirrors, not
repo-backed runtime truth. If a local `.agents/skills/<name>/skill.md` mirrors a
tracked `.claude/skills/<name>/skill.md`, the local copy must stay byte-for-byte
aligned or be removed locally. The repository quality gate checks this only when
the ignored `.agents/` directory exists in the local worktree.

Workspace-local `.claude/*.local.md` files are ignored local warning layers.
Hookify `.local.md` rules may guide an operator during local sessions, but shared
enforcement must remain in tracked hooks, runtime settings, Codex hook wiring,
and `scripts/validate-repo-quality-gates.sh`. Local Hookify rules must stay
untracked, ignored, and frontmatter-shaped when they exist.

## Consistency Rules

- `AGENTS.md` must route to this catalog instead of embedding a duplicate agent table.
- Root `CLAUDE.md` and `GEMINI.md` must point to this catalog when describing runtime agents.
- `.claude/CLAUDE.md` must remain the runtime baseline for local agent execution.
- `.codex/agents/*.toml` mirrors must stay aligned with `.claude/agents/*.md` and pass the mirror checks in `scripts/validate-repo-quality-gates.sh`.
- `.claude/*.local.md` files must stay ignored and untracked; Hookify local rules are advisory only and must not replace tracked validators.
- Document-generation workflows must use `.claude/skills/docs-stage-routing/skill.md` before proposing new authored-document paths.
- Any new local agent or skill must be added here in the same change set.

## Related Documents

- [AGENTS.md](../../AGENTS.md)
- [Runtime Baseline](../../.claude/CLAUDE.md)
- [Subagent Protocol](./subagent-protocol.md)
- [Claude Provider Notes](./providers/claude.md)
