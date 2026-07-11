---
title: 'Codex Governance Harness Alignment Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-05-31
---

# Codex Governance Harness Alignment Plan

---

## Overview

This document is the implementation plan for aligning Stage 00 common agent
governance with the Codex/GPT harness. It defines the safe Phase 3 remediation
order and validation criteria for model-policy conflicts, Template Contract
drift, missing Codex TOML reasoning-effort fields, and operations policy
frontmatter drift found during Phase 1 investigation.

## Context

The attached work instructions required a three-phase pipeline.

- Phase 1: read-only investigation and analysis.
- Phase 2: plan document creation only.
- Phase 3: implementation of governance, template, config, and validation surfaces according to the approved plan.

The key facts confirmed in Phase 1 were:

- `docs/00.agent-governance/model-policy.md` described the Codex worker as `GPT-5.4-mini`, while `docs/00.agent-governance/harness-catalog.md` and `.codex/agents/*.toml` used `gpt-5.3-codex`.
- The user decided to keep `gpt-5.3-codex` as the Codex worker standard.
- `.codex/agents/*.toml` declared only `model` and did not declare `model_reasoning_effort`.
- The user decided to declare `model_reasoning_effort` in Codex TOML.
- `AGENTS.md` is actually used as a Codex/GPT provider shim.
- The user decided to clarify `AGENTS.md` as the Codex/GPT-specific shim.
- `docs/05.operations/policies/*.md` used `type: operation`, while `docs/99.templates/templates/sdlc/operations/policy.template.md` requires `type: sdlc/policy`.
- The user decided to normalize operations policy document frontmatter to `type: sdlc/policy`.
- Official OpenAI model docs currently document the `gpt-5.5`, `gpt-5.4-mini`, and `gpt-5.3-codex` model IDs and the supported reasoning effort range.

## Goals & In-Scope

- **Goals**:
  - Ensure Stage 00 has one shared governance surface, QA/CI/CD policy, Template Contract, and Model Policy.
  - Clarify that the Codex harness is an adapter implementing Stage 00, not a separate governance system.
  - Make the `model` and `model_reasoning_effort` fields in Codex agent TOML traceable through the Stage 00 Model Policy and validation scripts.
  - Align the type and path naming for the policy template, routing skill, edit hook, and authored policy documents.
  - Make Phase 3 changes and QA/CI/CD execution results traceable through Plan/Task documents.
- **In Scope**:
  - Align governance, provider, and hook-routing docs under `docs/00.agent-governance/**`.
  - Align the Codex harness in `.codex/CODEX.md`, `.codex/agents/*.toml`, and `AGENTS.md`.
  - Remediate policy template routing in `.agents/skills/docs-stage-routing/skill.md`.
  - Remediate authored-doc template hints in `docs/00.agent-governance/hooks/k8s-pre-edit.sh`.
  - Normalize `type` frontmatter in `docs/05.operations/policies/*.md`.
  - Add the required static validation to `scripts/validate-repo-quality-gates.sh`.
  - Record the Phase 3 task record and `docs/00.agent-governance/memory/progress.md` entry.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Changing Kubernetes manifests, ArgoCD applications, Vault, ESO, or live cluster state.
  - Adding new runtime agents, new skills, or new docs taxonomy stages.
  - Large content changes that rewrite the operational meaning of policy documents.
  - Changing GitHub Actions job topology.
- **Out of Scope**:
  - Directly running `kubectl apply`, `kubectl patch`, `argocd app sync`, or Vault writes.
  - Reading or outputting secret values.
  - Rewriting historical evidence in existing completed plans.

## Concept Alignment Plan

| Concept | Current State | Desired State | Planned Action |
| --- | --- | --- | --- |
| Agent | `.agents/` SSoT wording and `.claude/agents` primary wording are mixed. | Describe `.agents/` as the shared content SSoT and provider agent files as runtime mirrors. | Clean up terminology in `common-governance.md`, `harness-catalog.md`, and `subagent-protocol.md`. |
| Skill | `.codex/skills` symlink wording and `.claude/skills` references are mixed, and docs-stage-routing points to `deprecated operations-template route`. | Clarify the `.agents/skills` SSoT and provider symlink relationship, and standardize on `policy.template.md`. | Remediate `.agents/skills/docs-stage-routing/skill.md` and catalog routing wording. |
| Rule | JIT, GitOps-first, and Template-first rules exist, but AGENTS gateway wording conflicts with provider scope. | Keep common rules in Stage 00 and keep `AGENTS.md` as only the Codex/GPT shim. | Clean up pointers in `providers/agents-md.md`, `providers/codex.md`, and `AGENTS.md`. |
| Hook | `.codex/hooks.json` calls `docs/00.agent-governance/hooks/*.sh`, but some docs described legacy provider-local hook script paths. | Describe shared hook scripts as `docs/00.agent-governance/hooks/*.sh` and provider configs as event wiring. | Remediate `.codex/CODEX.md`, provider docs, and hook boundary text. |
| Sub-agent | Codex TOML mirrors exist, but no explicit reasoning-effort policy exists. | `supervisor` and workers declare model and reasoning effort according to Model Policy. | Update `.codex/agents/*.toml` and the validator. |
| Output Style | Common governance says fully supported; catalog says Codex/Gemini are tone-only. | Separate native support from behavioral/tone-only support. | Align the support matrix in `common-governance.md` and `harness-catalog.md`. |
| Workflow | QA/CI/CD workflow exists, but model/config drift is not fully checked. | Phase 3 workflow includes static gates for model and template drift. | Add checks to `scripts/validate-repo-quality-gates.sh`. |
| Memory | `progress.md` ledger exists and is required for repo-changing work. | Phase 3 implementation writes a concise progress entry with evidence. | Include the `progress.md` update in task implementation. |
| QA | Repo quality gate passes, but semantic drift is not fully covered. | Validator catches Codex model effort, policy type, and template route drift. | Add focused static checks in quality gate. |
| CI/CD | GitHub Actions runs repo gates; no topology change is needed. | Existing CI inherits strengthened repo quality gate. | No workflow topology change; rely on script hardening. |
| Model Policy | `model-policy.md` conflicts with `harness-catalog.md`. | Top: `gpt-5.5`; Codex worker: `gpt-5.3-codex`; allowed efforts documented. | Update model policy and catalog as one source-aligned pair. |
| Template Contract | `deprecated operations-template route` references remain, while actual template is `policy.template.md`. | Policy docs and routing use `policy.template.md` and `type: sdlc/policy`. | Update routing skill, hook hint, policy docs, and validator. |

## Codex Model and Reasoning-Effort Assignment

| Codex Agent | Model | Planned `model_reasoning_effort` | Rationale |
| --- | --- | --- | --- |
| `supervisor` | `gpt-5.5` | `xhigh` | Governance routing and multi-agent orchestration are high-risk planning tasks. |
| `code-reviewer` | `gpt-5.3-codex` | `high` | Review findings can block merge and need strong reasoning. |
| `gitops-reviewer` | `gpt-5.3-codex` | `high` | GitOps structure and release safety are cluster-affecting. |
| `k8s-implementer` | `gpt-5.3-codex` | `high` | Kubernetes manifest authoring has operational blast radius. |
| `security-auditor` | `gpt-5.3-codex` | `high` | RBAC, secrets, and network findings are security-sensitive. |
| `incident-responder` | `gpt-5.3-codex` | `high` | Incident reconstruction needs careful causal reasoning. |
| `doc-writer` | `gpt-5.3-codex` | `medium` | Template-aligned documentation is bounded by repo validators. |
| `wiki-curator` | `gpt-5.3-codex` | `medium` | LLM Wiki curation is link-map and reference maintenance work. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Create Phase 3 task record before implementation | `docs/04.execution/tasks/2026-05-31-codex-governance-harness-alignment.md` | G2, Traceability | Task uses `task.template.md`, links this plan, and defines evidence. |
| PLN-002 | Align Stage 00 model policy | `docs/00.agent-governance/model-policy.md`, `docs/00.agent-governance/harness-catalog.md` | G3, Model Policy | Codex worker is `gpt-5.3-codex`; allowed reasoning efforts are documented. |
| PLN-003 | Align Codex harness model config | `.codex/agents/*.toml`, `.codex/CODEX.md` | G3, Codex config correctness | Every TOML declares allowed `model` and `model_reasoning_effort`. |
| PLN-004 | Clarify `AGENTS.md` provider role | `AGENTS.md`, `docs/00.agent-governance/providers/agents-md.md`, `docs/00.agent-governance/providers/codex.md` | G3, Single governance | `AGENTS.md` is Codex/GPT shim and points to shared Stage 00 without duplicating policy. |
| PLN-005 | Normalize hook and provider script references | `.codex/CODEX.md`, `docs/00.agent-governance/providers/*.md`, `docs/00.agent-governance/common-governance.md`, `docs/00.agent-governance/harness-catalog.md` | G3, Hook boundary | Docs consistently describe shared scripts under `docs/00.agent-governance/hooks/*.sh`. |
| PLN-006 | Normalize Template Contract policy naming | `.agents/skills/docs-stage-routing/skill.md`, `docs/00.agent-governance/hooks/k8s-pre-edit.sh`, `docs/00.agent-governance/rules/document-stage-routing.md` | G3, Template Contract | Policy routing uses `docs/99.templates/templates/sdlc/operations/policy.template.md`; no `deprecated operations-template route` references remain in active routing. |
| PLN-007 | Normalize authored policy frontmatter | `docs/05.operations/policies/*.md` | G3, Template compliance | All policy docs use `type: sdlc/policy`; no `^type: operation$` remains under policies. |
| PLN-008 | Strengthen repo quality gates for recurring drift | `scripts/validate-repo-quality-gates.sh` | G3, QA and CI/CD | Gate fails on Codex TOML model/effort drift, policy type drift, and active `deprecated operations-template route` routing drift. |
| PLN-009 | Update required indexes and memory | `docs/04.execution/plans/README.md`, `docs/04.execution/tasks/README.md`, `docs/00.agent-governance/memory/progress.md` | Traceability | README indexes are current and progress entry records files changed and verification evidence. |
| PLN-010 | Run validation and record limitations | validation commands below | QA and CI/CD | Required repo-static checks pass or limitations are documented. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Repository quality gate | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | Docs index | LLM Wiki generated index freshness if docs references change | `bash scripts/generate-llm-wiki-index.sh --check` | PASS or not affected with rationale |
| VAL-PLN-003 | Targeted model | Codex worker model remains canonical | `rg -n "GPT-5.4-mini\|gpt-5.4-mini" docs/00.agent-governance .codex AGENTS.md -g '!docs/00.agent-governance/memory/**'` | No active policy/config reference |
| VAL-PLN-004 | Targeted effort | Codex TOML effort fields exist | `rg -n "model_reasoning_effort" .codex/agents` | Eight agent TOMLs report explicit values |
| VAL-PLN-005 | Targeted policy type | Policy docs use policy type | `rg -n "^type: operation$" docs/05.operations/policies` | No output |
| VAL-PLN-006 | Targeted template route | Active routing uses `policy.template.md` | `rg -n "operation\\.template\\.md" .agents docs/00.agent-governance .codex` | No active routing or hook references remain |
| VAL-PLN-007 | Shell syntax | Hook and validator syntax | `bash -n docs/00.agent-governance/hooks/k8s-pre-edit.sh scripts/validate-repo-quality-gates.sh` | PASS |
| VAL-PLN-008 | Diff hygiene | Whitespace and accidental churn | `git diff --check` | PASS |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Model policy wording drifts again between `model-policy.md` and `harness-catalog.md` | High | Make one table authoritative for concrete IDs and add validator coverage for `.codex/agents/*.toml`. |
| `model_reasoning_effort` is not accepted by future Codex TOML schema | Medium | Keep the value explicit only after local TOML parsing and quality gate pass; document as Codex mirror metadata if runtime-native support is behavioral. |
| README sync expands the diff beyond the model/template fix | Medium | Limit README changes to index rows required by file additions or changed document status. |
| Policy frontmatter type change is semantically misread as policy content rewrite | Low | Change only the frontmatter `type`; do not alter policy body semantics. |
| Hook template hint changes affect authored-doc edit warnings | Medium | Run shell syntax and repository hook payload simulation through the quality gate. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repo-static validators and targeted `rg` checks must pass before handoff.
- **Sandbox / Canary Rollout**: not applicable; this is repository governance/config documentation work.
- **Human Approval Gate**: required before Phase 3 implementation begins, because governance and Codex config will change.
- **Rollback Trigger**: any failing quality gate that cannot be fixed within the approved scope rolls back the affected Phase 3 file set.
- **Prompt / Model Promotion Criteria**: Codex worker remains `gpt-5.3-codex`; `supervisor` remains `gpt-5.5`; reasoning-effort values must be one of the documented allowed values for each model.

## Completion Criteria

- [x] Phase 3 task record exists and links this plan.
- [x] Stage 00 model policy and harness catalog agree on Codex model tiers.
- [x] `.codex/agents/*.toml` declares allowed model and `model_reasoning_effort`.
- [x] `AGENTS.md` is a Codex/GPT shim and does not duplicate shared governance.
- [x] Template routing uses `policy.template.md` for operations policy documents.
- [x] Policy authored docs use `type: sdlc/policy`.
- [x] Validator covers the recurring drift points.
- [x] Required README and memory updates are complete.
- [x] Verification commands pass or limitations are recorded.

## Related Documents

- Parent Spec: N/A — pre-Spec execution record.
- [Governance Hub](../../00.agent-governance/README.md)
- [Model Policy](../../00.agent-governance/model-policy.md)
- [Harness Catalog](../../00.agent-governance/harness-catalog.md)
- [Codex Provider Notes](../../00.agent-governance/providers/codex.md)
- [Codex Runtime Baseline](../../../.codex/CODEX.md)
- [Template README](../../99.templates/README.md)
- [Plan Template](../../99.templates/templates/sdlc/execution/plan.template.md)
- [OpenAI Models](https://developers.openai.com/api/docs/models)
- [GPT-5.5 Model](https://developers.openai.com/api/docs/models/gpt-5.5)
- [GPT-5.3-Codex Model](https://developers.openai.com/api/docs/models/gpt-5.3-codex)
- [Phase 3 Task Record](../tasks/2026-05-31-codex-governance-harness-alignment.md)
