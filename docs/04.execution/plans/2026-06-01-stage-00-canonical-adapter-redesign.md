---
title: 'Stage 00 Canonical Adapter Redesign Plan'
type: plan
status: done
owner: platform
updated: 2026-06-01
---

# Stage 00 Canonical Adapter Redesign Implementation Plan

---

## Overview

This document is the implementation plan for redesigning Stage 00 agent
governance as a canonical adapter model. It separates governance, provider
harness, hook, template, model policy, QA/CI, skill/workflow, and local runtime
drift found during Phase 1 investigation into change units, then defines the
Phase 3 remediation order and validation criteria.

Phase 2 deliverables are this plan and the Plan stage index update. Actual
governance, template, provider config, hook, and validator changes are
performed in Phase 3 after creating a separate task record.

## Context

Stage 00 already has common governance and provider-specific adapter structure,
but it does not explain in one canonical contract what is authoritative and
what is an adapter mirror. As a result, the same rules are repeated across
multiple documents, and some documents expose historical paths or
provider-specific wording as if they were active contracts.

### Upstream Traceability Overlay (2026-06-01)

When first written, this plan was a governance plan that directly used Phase 1
investigation results as input. Current upstream SDD traceability is owned by
[Workspace Agent Governance Platform PRD](../../01.requirements/2026-06-01-workspace-agent-governance-platform.md),
[Workspace Agent Governance Platform ARD](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md),
and [ADR-0013](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md).
This overlay only adds current requirement/architecture links and does not
retroactively rewrite existing Phase 2/Phase 3 evidence.

The core gaps confirmed during Phase 1 investigation were:

| Gap ID | Finding | Desired Direction |
| --- | --- | --- |
| GAP-001 | `common-governance.md`, `harness-catalog.md`, `model-policy.md`, and documentation rules repeat Stage 00 ownership explanations. | Create a Stage 00 canonical adapter ownership map and make each document responsibility non-overlapping. |
| GAP-002 | Template routing, documentation protocol, and hook guidance are repeated in different locations. | Separate the Template Contract source of truth from provider/hook adapter responsibilities. |
| GAP-003 | Actual shared hook scripts are `docs/00.agent-governance/hooks/*.sh`, but some docs referenced legacy provider-local hook script paths. | Clearly separate the shared hook path from provider event wiring. |
| GAP-004 | The actual role of `.agents/hooks.json` differs from placeholder/behavioral wording in docs. | Document Gemini/Antigravity adapter hook support from disk evidence. |
| GAP-005 | Subagent readiness is described differently in `common-governance.md` and `harness-catalog.md`. | Represent provider-specific native support, mirror support, and behavioral support as separate statuses. |
| GAP-006 | `.agents/skills` SSoT wording and `.claude/skills` symlink/mirror wording differ across docs. | Include shared asset SSoT and provider adapter mounts in the canonical schema. |
| GAP-007 | Model policy is duplicated across `model-policy.md`, `harness-catalog.md`, and provider config. | Separate the concrete model ID source of truth from provider config verification location. |
| GAP-008 | Model tier vocabulary mixes `top`, `supervisor`, `worker`, and review/security usage. | Fix tier vocabulary and exception rules in one location. |
| GAP-009 | `docs/00.agent-governance/README.md` omits hooks, model policy, common governance, and the Codex provider entry. | Harden the Stage 00 README as the canonical entry map. |
| GAP-010 | `.codex/rules/` is a placeholder, while shared rules live in `.agents/rules` and Stage 00. | Clarify how the Codex adapter loads shared rules. |
| GAP-011 | `.agents/workflows/qa-cicd-workflow.md` uses Gemini/Antigravity-centered wording but is also exposed to Codex. | Make the workflow body provider-neutral or state the adapter boundary. |
| GAP-012 | The `workspace-harness-audit` skill fits the current task, but catalog routing exposes only external skills. | Harden repo-local skill routing and the external skill availability ledger. |
| GAP-013 | pre-commit, post-validate, and CI guide wording do not fully follow the actual shared hook path and GitHub Actions job name. | Bind validator, pre-commit coverage, and CI documentation into the same QA contract. |
| GAP-014 | Template owner/status/lifecycle/headings partially drift from authored docs. | Align template defaults and lifecycle vocabulary by document stage. |
| GAP-015 | Branch completion workflow is not organized as a Stage 00 git/postflight strategy. | Integrate finishing-a-development-branch strategy into git/postflight workflow. |
| GAP-016 | `/home/hy/.local/bin/{node,npm,rtk}` exists, but `rtk` is not on PATH and `rtk gain` DB initialization fails. | Record reproducible checks for local runtime discovery, PATH, and RTK DB failure in the Codex/runtime baseline. |
| GAP-017 | 2026-05-30 active plans/tasks partially overlap with 2026-05-31/2026-06-01 completed follow-up work. | Reclassify change units through the new canonical adapter plan and decide close/supersede status for existing active plans in Phase 3. |

## Goals & In-Scope

- **Goals**:
  - Redefine Stage 00 as a `canonical core + provider adapter + validation evidence` model.
  - Separate the source-of-truth locations for common rules, Template Contract, Model Policy, skill/workflow routing, and hook/QA contract.
  - State adapter responsibilities so Claude, Codex/GPT, and Gemini/Antigravity implement the same Stage 00 contract according to each runtime's characteristics.
  - Split Phase 1 gaps into change units that define Phase 3 implementation order and validation criteria.
  - Do not rewrite existing active/stale plans and tasks without approval; leave supersede/close decisions as Phase 3 task evidence.
- **In Scope**:
  - Planning alignment for canonical ownership, provider notes, rules, hooks, models, and catalog docs under `docs/00.agent-governance/**`.
  - Planning alignment for adapter boundaries in `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.codex/CODEX.md`, `.claude/CLAUDE.md`, and `.agents/GEMINI.md`.
  - Planning cleanup for SSoT/mirror relationships across `.agents/skills`, `.agents/workflows`, and provider skill/workflow mirrors.
  - Planning hardening for `docs/99.templates/**` template lifecycle, owner/status, and heading contracts.
  - Planning static validation hardening for `scripts/validate-repo-quality-gates.sh`, `.pre-commit-config.yaml`, hook scripts, and CI docs.
  - Planning investigation for `/home/hy/.local/bin` runtime tool discovery and the `rtk` availability failure.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not directly modify governance, templates, provider config, hooks, or validation scripts in Phase 2.
  - Do not add new docs taxonomy stages, new runtime providers, or new agent roles.
  - Do not retroactively edit existing historical plan/task evidence.
  - Do not update model policy from unofficial assumptions.
- **Out of Scope**:
  - Changing Kubernetes manifests, ArgoCD applications, Vault, External Secrets, or live cluster state.
  - Reading, outputting, committing, or including secret values in PR descriptions.
  - Changing GitHub Actions topology or deployment/publish actions.
  - Destructive Git operations, rebase, reset, force-push, or merge before Phase 3 approval.

## Canonical Adapter Model

| Layer | Canonical Responsibility | Adapter Responsibility | Evidence / Validation |
| --- | --- | --- | --- |
| Stage 00 Core | Governance principles, scope rules, template routing, model/tier policy, QA contract. | Provider docs import the core and state only runtime-specific differences. | `docs/00.agent-governance/**`, repo quality gate. |
| Shared Assets | Shared agents/skills/rules/workflows/output-styles ownership and lifecycle. | `.claude`, `.codex`, `.agents` expose native files, symlinks, or behavioral mirrors. | Harness catalog, subagent protocol, provider configs. |
| Provider Adapter | Runtime-specific loading order, model config, tool permissions, hook/event wiring. | Claude, Codex/GPT, Gemini/Antigravity each document native support vs mirror support. | Provider notes, runtime baseline files, static drift checks. |
| Template Contract | Stage-to-template mapping, required headings, owner/status vocabulary, link basis. | Doc-writer agents and hooks use the same routing without redefining it. | `docs/99.templates/**`, stage routing skill, hook hint checks. |
| QA/CI Contract | Local static checks, pre-commit coverage, CI job naming, postflight expectations. | Provider postflight instructions call the same smallest relevant gates. | `scripts/validate-repo-quality-gates.sh`, CI docs, task evidence. |
| Completion Strategy | Branch finishing, PR readiness, cleanup boundaries, explicit discard confirmation. | Provider-specific handoff text follows the common postflight/git strategy. | `rules/git-workflow.md`, `rules/postflight-checklist.md`, task record. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Create Phase 3 task record and freeze implementation scope before edits | `docs/04.execution/tasks/2026-06-01-stage-00-canonical-adapter-redesign.md`, `docs/04.execution/tasks/README.md` | REQ-CAN-001 | Task uses `task.template.md`, links this plan, and states Phase 3 approval/scope boundaries. |
| PLN-002 | Define Stage 00 canonical ownership map | `docs/00.agent-governance/README.md`, `docs/00.agent-governance/common-governance.md`, `docs/00.agent-governance/harness-catalog.md` | REQ-CAN-002 | README lists hooks, model policy, common governance, Codex provider notes, and each doc has a non-overlapping responsibility. |
| PLN-003 | Consolidate Template Contract routing | `docs/00.agent-governance/rules/document-stage-routing.md`, `docs/00.agent-governance/rules/documentation-protocol.md`, `docs/99.templates/README.md`, `.agents/skills/docs-stage-routing/skill.md` | REQ-CAN-003 | One active mapping exists for each stage; provider/hook docs link to it instead of duplicating rules. |
| PLN-004 | Normalize provider gateway and adapter loading semantics | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.codex/CODEX.md`, `.claude/CLAUDE.md`, `.agents/GEMINI.md`, `docs/00.agent-governance/providers/*.md` | REQ-CAN-004 | Root gateways stay thin; provider files describe native support, mirror support, hook support, and limitations consistently. |
| PLN-005 | Reconcile hook path and event wiring drift | `docs/00.agent-governance/hooks/*.sh`, `.codex/hooks.json`, `.agents/hooks.json`, provider docs, `docs/00.agent-governance/rules/postflight-checklist.md` | REQ-CAN-005 | Active docs refer to shared hook scripts under `docs/00.agent-governance/hooks/*.sh`; provider configs are described as event wiring. |
| PLN-006 | Reconcile subagent, skill, workflow, and output-style status vocabulary | `docs/00.agent-governance/common-governance.md`, `docs/00.agent-governance/harness-catalog.md`, `docs/00.agent-governance/subagent-protocol.md`, `.agents/skills`, `.agents/workflows`, `.codex/skills`, `.claude/skills` | REQ-CAN-006 | Matrices distinguish native, mirror/symlink, behavioral, partial, and missing support without contradiction. |
| PLN-007 | Normalize model policy and tier vocabulary after official verification | `docs/00.agent-governance/model-policy.md`, `docs/00.agent-governance/harness-catalog.md`, provider agent configs | REQ-CAN-007 | Concrete model IDs and allowed effort/tier vocabulary match official provider docs and local configs. |
| PLN-008 | Harden QA/CI static gates for canonical adapter drift | `scripts/validate-repo-quality-gates.sh`, `.pre-commit-config.yaml`, `docs/00.agent-governance/hooks/post-validate.sh`, `.github/ABOUT.md`, `.github/workflows/ci.yml` | REQ-CAN-008 | Shared hook path, pre-commit file coverage, CI job names, model/config drift, and template routing drift are checked or explicitly documented. |
| PLN-009 | Update template lifecycle and required metadata contract | `docs/99.templates/*.template.md`, `docs/99.templates/README.md`, `docs/00.agent-governance/rules/stage-checklists.md`, `docs/00.agent-governance/rules/stage-authoring-matrix.md` | REQ-CAN-009 | Templates use consistent owner/status vocabulary and each stage documents required vs optional headings. |
| PLN-010 | Integrate branch completion strategy into Stage 00 workflow | `docs/00.agent-governance/rules/git-workflow.md`, `docs/00.agent-governance/rules/postflight-checklist.md`, provider docs, relevant local skills/workflows if needed | REQ-CAN-010 | Completion flow includes verification, base branch detection, PR/merge/keep/discard options, cleanup boundaries, and typed destructive confirmation. |
| PLN-011 | Investigate local runtime PATH and RTK availability | `.codex/CODEX.md`, `RTK.md`, provider runtime docs, task evidence | REQ-CAN-011 | Phase 3 records `command -v rtk`, `/home/hy/.local/bin/rtk --version`, PATH expectations, and the `rtk gain` DB failure cause or limitation. |
| PLN-012 | Reconcile active/stale plans and tasks without rewriting old bodies | `docs/98.archive/README.md`, README indexes | REQ-CAN-012 | Old superseded items are discoverable through the central archive index; active items keep clear remaining scope or dated completion evidence. |
| PLN-013 | Update traceability records after implementation | `docs/04.execution/plans/README.md`, `docs/04.execution/tasks/README.md`, `docs/00.agent-governance/memory/progress.md` | REQ-CAN-013 | README indexes and progress ledger identify files changed, checks run, limitations, and no-live-cluster boundary. |

## Change Unit Split

| Change Unit | Scope | Depends On | Phase 3 Commit Boundary |
| --- | --- | --- | --- |
| CU-001 Canonical Ownership | Stage 00 README, common governance, harness catalog responsibility map. | PLN-001 | One docs-only commit. |
| CU-002 Template Contract | Stage routing, documentation protocol, template README, routing skill. | CU-001 | One docs/skill commit with template validation. |
| CU-003 Provider Adapter Gateways | Root shims, provider notes, runtime baselines. | CU-001, CU-002 | One adapter docs commit. |
| CU-004 Hook and QA Contract | Shared hook path docs, post-validate coverage, pre-commit coverage, CI guide naming. | CU-003 | One validator/config/docs commit. |
| CU-005 Model Policy | Model policy, tier vocabulary, provider config verification. | CU-001 | One model-policy commit after official docs check. |
| CU-006 Skills and Workflows | Skill routing, external path availability, provider-neutral workflow wording. | CU-001 | One docs/asset catalog commit. |
| CU-007 Template Lifecycle | Owner/status defaults and stage heading requirements. | CU-002 | One template contract commit. |
| CU-008 Branch Completion | Git workflow and postflight completion strategy. | CU-003 | One workflow docs commit. |
| CU-009 Local Toolchain | `/home/hy/.local/bin` PATH and RTK DB investigation. | PLN-001 | One runtime baseline/task evidence commit, only if docs changes are needed. |
| CU-010 Plan/Task Reconciliation | Supersede/close overlapping 2026-05-30 records where evidence supports it. | CU-001-CU-009 | One traceability commit. |
| CU-011 Validation Evidence | README indexes, progress ledger, final quality gate evidence. | All prior CUs | Final traceability commit. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Phase 2 plan and README index pass repository governance checks | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | Diff hygiene | No whitespace or conflict marker issues | `git diff --check` | PASS |
| VAL-PLN-003 | Plan routing | New plan is discoverable from Plan README | `rg -n "stage-00-canonical-adapter-redesign" docs/04.execution/plans/README.md docs/04.execution/plans/2026-06-01-stage-00-canonical-adapter-redesign.md` | Both README and plan file are reported. |
| VAL-PLN-004 | Wiki index | LLM Wiki generated index remains fresh if doc references require it | `bash scripts/generate-llm-wiki-index.sh --check` | PASS or documented as not affected. |
| VAL-CAN-001 | Official model source | Provider model IDs and effort/tier claims are verified before Phase 3 edits | Official provider docs review plus local config scan | No model policy change is made from stale memory alone. |
| VAL-CAN-002 | Hook path drift | Shared hook path is the only active script path in docs/config after Phase 3 | `rg -n "docs/00.agent-governance/hooks" docs .codex .agents .claude` | Active docs/config expose the shared hook path. |
| VAL-CAN-003 | Template drift | Active routing has one template target per stage | `rg -n "operation\\.template\\.md\|policy\\.template\\.md\|plan\\.template\\.md" docs/00.agent-governance .agents .codex .claude docs/99.templates` | No stale active routing target remains. |
| VAL-CAN-004 | QA/CI drift | Local static gates cover shared hooks and CI docs match actual job names | `bash scripts/validate-repo-quality-gates.sh .` | Gate catches path/job drift or docs explain intentional exceptions. |
| VAL-CAN-005 | Local runtime | RTK and local toolchain availability are reproducibly documented | `command -v rtk`; `/home/hy/.local/bin/rtk --version`; `/home/hy/.local/bin/rtk gain` | PATH status, version, and DB result are recorded without exposing secrets. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Canonical adapter rewrite becomes a broad style refactor | High | Keep Phase 3 commits by CU boundary and require each changed line to map to a gap or validation rule. |
| Existing active plans are rewritten as if their historical evidence were wrong | Medium | Preserve historical content; add dated supersede/closure notes only when current evidence supports it. |
| Provider-specific native behavior is collapsed into a false common denominator | High | Matrices must distinguish native, mirror/symlink, behavioral, partial, and missing support. |
| Model policy is updated from stale assumptions | High | Verify current official provider documentation immediately before Phase 3 model-policy edits. |
| Validator hardening blocks unrelated work due to over-broad checks | Medium | Prefer targeted checks for documented drift classes; add explicit exceptions only with rationale. |
| RTK investigation touches credentials or private runtime state | High | Do not read auth files, shell history, tokens, or private DB contents; record only command availability and error class. |
| Branch completion guidance encourages destructive cleanup | High | Require explicit user approval and typed confirmation for discard/reset/delete actions. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Phase 3 starts with a task record and ends each CU with targeted `rg` checks plus `bash scripts/validate-repo-quality-gates.sh .`.
- **Sandbox / Canary Rollout**: Not applicable for live infrastructure. This plan affects repository governance, templates, adapter docs, hooks, and validators only.
- **Human Approval Gate**: Required before Phase 3 implementation, before external network verification beyond official docs, and before any destructive git or filesystem action.
- **Rollback Trigger**: If a CU introduces contradictory provider support claims, stale model IDs, broken template routing, or failing quality gates that cannot be fixed in scope, revert only that CU's files and keep the gap open in the task record.
- **Prompt / Model Promotion Criteria**: Model/tier changes require official provider documentation evidence, local config parity, and validator coverage; no promotion is accepted from memory or preference alone.
- **Branch Completion Gate**: Before PR/merge handoff, verify status, base branch, relevant tests, branch diff, and present explicit keep/PR/merge/discard options. Destructive discard requires typed confirmation.

## Completion Criteria

- [x] Phase 3 task record exists and links this plan.
- [x] Stage 00 canonical ownership map is documented and indexed.
- [x] Provider gateway files are thin adapters and do not duplicate common governance.
- [x] Hook path, event wiring, skill/workflow, and output-style support states are consistent across docs.
- [x] Model policy, harness catalog, and provider configs agree after official source verification.
- [x] Template owner/status/lifecycle and required heading contracts are consistent across `docs/99.templates`.
- [x] QA/CI gates cover the recurring drift classes found in Phase 1.
- [x] Local RTK/PATH limitation is recorded with a concrete follow-up boundary.
- [x] Overlapping 2026-05-30 plans/tasks have a dated superseded status rationale.
- [x] Required README indexes, task evidence, and progress ledger are updated.
- [x] No live cluster, secret, deployment, or destructive git action was performed without explicit approval.

## Related Documents

- **PRD**: [../../01.requirements/2026-06-01-workspace-agent-governance-platform.md](../../01.requirements/2026-06-01-workspace-agent-governance-platform.md)
- **ARD**: [../../02.architecture/requirements/0006-workspace-agent-governance-platform.md](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md)
- **ADR**: [../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
- **Task**: [../tasks/2026-06-01-stage-00-canonical-adapter-redesign.md](../tasks/2026-06-01-stage-00-canonical-adapter-redesign.md)
- **Prior Archive Index**: [../../98.archive/README.md](../../98.archive/README.md)
- **Codex Follow-up Plan**: [./2026-05-31-codex-governance-harness-alignment.md](./2026-05-31-codex-governance-harness-alignment.md)
- **Claude Surface Plan**: [./2026-06-01-claude-agent-surface-restoration.md](./2026-06-01-claude-agent-surface-restoration.md)
- **Governance Hub**: [../../00.agent-governance/README.md](../../00.agent-governance/README.md)
- **Common Governance**: [../../00.agent-governance/common-governance.md](../../00.agent-governance/common-governance.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Model Policy**: [../../00.agent-governance/model-policy.md](../../00.agent-governance/model-policy.md)
- **Document Stage Routing**: [../../00.agent-governance/rules/document-stage-routing.md](../../00.agent-governance/rules/document-stage-routing.md)
- **Postflight Checklist**: [../../00.agent-governance/rules/postflight-checklist.md](../../00.agent-governance/rules/postflight-checklist.md)
- **Git Workflow**: [../../00.agent-governance/rules/git-workflow.md](../../00.agent-governance/rules/git-workflow.md)
- **Template README**: [../../99.templates/README.md](../../99.templates/README.md)
- **Plan Template**: [../../99.templates/templates/sdlc/execution/plan.template.md](../../99.templates/templates/sdlc/execution/plan.template.md)
- **RTK Runtime Notes**: [../../../RTK.md](../../../RTK.md)
- **Codex Runtime Baseline**: [../../../.codex/CODEX.md](../../../.codex/CODEX.md)
- **OpenAI Models**: [https://developers.openai.com/api/docs/models](https://developers.openai.com/api/docs/models)
- **OpenAI Reasoning Guide**: [https://developers.openai.com/api/docs/guides/reasoning](https://developers.openai.com/api/docs/guides/reasoning)
- **GPT-5.3-Codex Model**: [https://developers.openai.com/api/docs/models/gpt-5.3-codex](https://developers.openai.com/api/docs/models/gpt-5.3-codex)
