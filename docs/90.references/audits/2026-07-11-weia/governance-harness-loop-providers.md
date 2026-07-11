---
title: 'Audit: Governance, Harness, Loop, and Provider Parity'
type: content/reference
status: draft
owner: platform
updated: 2026-07-11
---

# Audit: Governance, Harness, Loop, and Provider Parity

## Overview

이 문서는 Current research의 governance, harness/loop, provider 구현 기준을
고정된 repository snapshot과 대조한 dated implementation audit다. 26개 통제를
governance, harness/loop, Claude, Codex, Gemini, common-system 범주로 분리해
채점하며, repository declaration과 provider-native runtime evidence를 같은 것으로
취급하지 않는다.

이 보고서는 provider/local declaration, native path와 registration surface,
settings/hooks/config, validator coverage, entitlement/runtime availability evidence의
canonical audit owner다. 역할별 model default, escalation, fallback, eval, adoption
recommendation은 후속 `ai-agents-model-routing-vibe-coding.md`가 소유한다.

## Purpose

- Audit workspace purpose, owners, rules, template/script/integration routing, and
  the bounded Observe/Plan/Act/Verify/Learn loop.
- Score Claude, Codex, Gemini, and the common repository layer independently.
- Reconcile `HL-001` through `HL-007` with actionable owners and measurable
  acceptance evidence.
- Preserve static, provider-runtime, live, and remote evidence boundaries while
  routing active changes out of Stage 90.

## Reference Type

- Type: dated-implementation-audit
- Audit observation SHA: `a85df194bbb8ebc61187b905afaef7f95215cc2f`
- Research cutoff: `2026-07-10 10:00 KST`
- Source checked: 2026-07-11
- Refresh trigger: Stage 00 governance/harness ownership, provider-native paths,
  settings/hooks/config, adapter inventory, model declarations, validator coverage,
  MCP configuration, provider canary evidence, or audit method changes.

## Authority Boundary

- **Authoritative for**:
  - The 26 scored controls and their repository evidence at the audit observation
    SHA.
  - Provider/local declarations, native loading/registration surfaces,
    settings/hooks/config facts, and entitlement/runtime availability evidence and
    confidence.
  - Routed governance, harness, MCP, provider-parity, and availability findings.
- **Not authoritative for**:
  - Active governance, provider configuration, permissions, hooks, model policy,
    templates, scripts, CI, or live operations.
  - Role-specific model default, escalation, fallback, eval, or adoption decisions.
  - Proof that a provider loaded a tracked file, invoked a hook, resolved a model,
    authenticated an account, or connected to MCP.

## Scope

- Includes workspace purpose, owner/authority routing, rules, template/script and
  integration-guide interfaces, security/approval boundaries, shared assets,
  duplicated summaries, Observe/Plan/Act/Verify/Learn, retry, recovery,
  termination, eval, compaction, memory, tools/MCP, hooks, canaries, provider
  declarations, native paths, settings/config, and availability evidence.
- Excludes active-owner edits, role-routing recommendations, credential or secret
  inspection, provider login/account inspection, native provider execution, MCP
  enablement, remote CI, and live Kubernetes/Argo CD/Vault/ESO checks.

## Definitions / Facts

### Evidence and Scoring Basis

All repository claims below are read from audit observation SHA
`a85df194bbb8ebc61187b905afaef7f95215cc2f`. Commands such as
`git show <SHA>:<path>` and `git ls-tree -r --name-only <SHA> -- <path>` fix the
evidence independently of the evolving audit branch. Static controls cannot receive
maturity 4. `Not in scope`/`N/A` rows would be excluded from denominators; this report
has no N/A rows.

The exact columns and maturity formula come from the [pack audit method](README.md#audit-method):
`sum(maturity) / (4 * applicable controls)`. Verdict and confidence remain separate
from maturity. Every actionable row names one priority, one canonical SDLC follow-up
route, and measurable acceptance evidence. No-action rows use the exact required
value in the final three fields.

### Governance Controls

| ID | Benchmark | Expected control | Repository evidence | Maturity | Verdict | Confidence | Gap | Recommendation | Priority | Follow-up owner | Acceptance evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GOV-001 | [Workspace Governance Baseline](../../research/2026-07-07-wer/workspace-governance-baseline.md) | Purpose, GitOps-first operating contract, repository/live boundary, and Stage 90 authority are explicit. | At the observation SHA, [root README](../../../../README.md), [bootstrap](../../../00.agent-governance/rules/bootstrap.md), [agentic rules](../../../00.agent-governance/rules/agentic.md), and this pack README define WSL2+k3d, repository-first work, approval, and descriptive-only Stage 90 scope. | 2 repository-static | Implemented | Verified repo-static | No missing element in the assessed repository contract; live reconciliation is outside this control. | Preserve the contract and evidence boundary. | N/A — no action | N/A — no action | N/A — no action |
| GOV-002 | Governance baseline; `HL-001` | Canonical owners, persona/roles, adapter ownership, and inventory statements agree without assigning Stage 00/04/99 assets to `.agents/`. | [Bootstrap](../../../00.agent-governance/rules/bootstrap.md), [persona](../../../00.agent-governance/rules/persona.md), [stage matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md), and [harness catalog](../../../00.agent-governance/harness-catalog.md) route owners; `git ls-tree` shows ten stems in each adapter directory, while three catalog statements still say `Eight`/`eight`. | 2 repository-static | Partial | Verified repo-static | Corrective: active catalog count prose is stale, and secondary ownership summaries can drift from canonical Stage 00/04/99 owners. | Correct the three count statements and replace duplicated ownership prose with tested canonical pointers. | P1 near-term integrity | New Stage 03 Spec: governance-owner-and-roster-currentness | A fixture-backed validator reports 10 shared stems/30 adapters, rejects stale numeric prose, and checks canonical owner links in the catalog. |
| GOV-003 | Governance baseline | Rules, checklists, approval boundaries, secrets, GitOps-first, and provider-specific enforcement differences are explicit. | [Preflight](../../../00.agent-governance/rules/preflight-checklist.md), [approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md), [postflight](../../../00.agent-governance/rules/postflight-checklist.md), Claude permissions, and repo-quality checks encode the static contract without calling Codex/Gemini hooks permission gates. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing element in the assessed rules/check boundary; provider runtime obedience remains separately scored. | Preserve provider-specific enforcement language and deterministic checks. | N/A — no action | N/A — no action | N/A — no action |
| GOV-004 | Governance baseline; template-routing benchmark | Authored paths route to the owning template and integration surface, while Stage 90 does not redefine template semantics. | [Template routing](../../../99.templates/support/template-routing.md), [reference template](../../../99.templates/templates/common/reference.template.md), [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md), and structural routes in `scripts/validate-repo-quality-gates.sh` are present at the observation SHA. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing routing control in Task 7 scope; lifecycle/frontmatter semantics belong to the lifecycle audit. | Keep this report linked to the canonical template and route detailed lifecycle findings to its sole audit owner. | N/A — no action | N/A — no action | N/A — no action |
| GOV-005 | Governance baseline | Scripts, hooks, CI/static validation, and evidence records integrate through named owners and bounded result semantics. | [Scripts inventory](../../../../scripts/README.md), [shared hooks](../../../00.agent-governance/hooks/), `.github/workflows/ci.yml`, and Stage 04 task records name commands and distinguish static results from runtime readiness. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing element for repository-static integration; remote CI execution is outside this control. | Preserve explicit commands and result boundaries when integrations change. | N/A — no action | N/A — no action | N/A — no action |
| GOV-006 | Governance baseline | Rules, templates, scripts, provider guides, and reference indexes have single owners and non-duplicated integration summaries. | [Harness catalog](../../../00.agent-governance/harness-catalog.md), provider notes, [reference maintenance runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md), and Stage 90 indexes exist; Current research records duplicated lifecycle/owner summaries and ambiguous older audit `Current` labels. | 2 repository-static | Partial | Verified repo-static | Complementary: canonical owners exist, but duplicated summaries and stale/current labels make integration guidance drift-prone. | Consolidate secondary summaries to pointers and enforce one Current audit target during the separately approved index reconciliation. | P2 planned improvement | New Stage 03 Spec: governance-reference-integration-consolidation | Link and owner fixtures prove one Current audit pointer, no conflicting owner prose, and resolved canonical integration links. |

### Harness and Loop Controls

| ID | Benchmark | Expected control | Repository evidence | Maturity | Verdict | Confidence | Gap | Recommendation | Priority | Follow-up owner | Acceptance evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HAR-001 | [Harness and Loop Engineering](../../research/2026-07-07-wer/harness-and-loop-engineering.md) | The four elements and Observe phase identify intent, evidence, constraints, feedback, and knowledge owners, and deterministic machine-readable task-state proof records completion. | [Harness catalog](../../../00.agent-governance/harness-catalog.md), [implementation map](../../../00.agent-governance/harness-implementation-map.md), bootstrap, preflight, memory, and provider baselines describe the four elements and evidence-first intake. | 2 repository-static | Partial | Verified repo-static | Complementary: the procedure is explicit, but no common machine-readable task state proves that every session completed Observe. | Define a minimal task-state/evidence schema only if a later harness Spec identifies a deterministic consumer. | P3 optional/telemetry-gated | New Stage 03 Spec: harness-task-state-contract | Representative task fixtures record source/evidence lane and owner, and a validator rejects a missing required Observe block without claiming provider execution. |
| HAR-002 | Harness research control-loop matrix | Plan and Act bind scope, approvals, tools, changed paths, rollback, and stop conditions to the owning task. | [Agentic rules](../../../00.agent-governance/rules/agentic.md), approval boundaries, Stage 04 plans/tasks, subagent protocol, and provider baselines document scoped planning/action and protected external/live boundaries. | 2 repository-static | Implemented | Verified repo-static | No missing element in the assessed documented Plan/Act contract; runtime compliance is not inferred. | Preserve task-scoped authorization and explicit stop conditions. | N/A — no action | N/A — no action | N/A — no action |
| HAR-003 | Harness research evaluation loop | Verify and Learn produce deterministic checks, review evidence, task handoff, and routed durable learning. | Repo-quality gates, pre-commit/CI definitions, postflight, lifecycle hook payload tests, Stage 04 evidence, and `memory/progress.md` implement repeatable static feedback and handoff paths. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing repository-static feedback control; static PASS is not provider or live readiness. | Preserve explicit PASS/SKIP/failure semantics and canonical learning owners. | N/A — no action | N/A — no action | N/A — no action |
| HAR-004 | Harness research `HL-002` | Retry/recovery changes the hypothesis, records attempts and failure classes, enforces a task budget/threshold, and terminates safely. | Research documents the desired state; active Stage 00 requires validation and escalation but has no common attempt schema, retry budget, repeated-failure threshold, or retry-counter enforcement. | 1 documented/routed | Gap | Verified repo-static | Missing: a bounded retry/escalation contract; identical retries can hide non-convergence and consume context. | Define task-instantiated retry units, failure classes, changed-hypothesis evidence, budget exhaustion, and safe termination without imposing an arbitrary global count. | P1 near-term integrity | New Stage 03 Spec: bounded-retry-and-termination-contract | Positive/negative task fixtures show attempt IDs, changed hypothesis, verifier reuse, configured budget/threshold, and deterministic rejection of an unchanged over-budget retry. |
| HAR-005 | Harness research `HL-003` | Eval evidence records capability criteria, trials, traces, graders/rubrics, failure classes, and attempt-to-attempt comparison. | Harness catalog and task records require commands/validators or approval, but there is no provider-neutral trial dataset, eval-trace schema, shared rubric, or behavioral regression grader. | 1 documented/routed | Partial | Verified repo-static | Complementary: deterministic completion evidence exists; behavioral and comparative eval records are not standardized. | Add an optional eval/evidence block after its consumers, privacy boundary, and validator semantics are specified. | P2 planned improvement | New Stage 03 Spec: provider-neutral-eval-evidence | Two representative task trials validate against the schema, preserve skipped lanes, identify rubric/graded judgment, and compare attempts without storing secrets or full private transcripts. |
| HAR-006 | Harness research `HL-004` | Compaction preserves goal, decisions, evidence, approvals, remaining budget, risks, and next verifier in a recoverable checkpoint. | [Lifecycle guard](../../../00.agent-governance/hooks/lifecycle-guard.sh) emits advisory PreCompact dirty-path and validation guidance; Stage 04 task evidence and Stage 00 memory exist, but no checkpoint is required or verified. | 2 repository-static | Partial | Verified repo-static | Missing: a recoverable compaction checkpoint contract; advisory output alone can lose active decision and approval state. | Define a compact handoff schema and keep blocking semantics provider-specific until canaries prove safe behavior. | P2 planned improvement | New Stage 03 Spec: recoverable-compaction-handoff | Payload fixtures include every required checkpoint field; recovery rehearsal reconstructs the next action and verifier; unsupported providers remain advisory. |
| HAR-007 | Harness research `HL-007`; MCP security guidance | Every enabled MCP server has an owner, command/endpoint, transport, tools, trust source, scopes, token audience, egress, logging, and disable/rollback evidence. | At the observation SHA, `git ls-tree` finds no tracked `.mcp.json`, `.codex/config.toml`, or `.gemini/settings.json`; no approved server inventory or runtime canary exists. | 0 absent | Gap | Verified repo-static | Missing: tracked MCP inventory/security evidence; upstream capability does not prove a safe enabled local server. | Keep MCP readiness unclaimed and require a separately approved provider/security inventory before enablement or scope elevation. | P1 near-term integrity | New Stage 03 Spec: provider-mcp-inventory-and-security | A redacted per-server inventory covers the official threat categories, least privilege, egress, approval, logs, disable/rollback, and one approved native connection canary per intended provider. |
| HAR-008 | Harness research `HL-005` and `HL-006` | Hooks, approvals, tools, canaries, and evidence lanes distinguish declared wiring, payload simulation, provider consumption, and live/remote readiness. | Three JSON files declare six Claude-shaped event groups and shared scripts; validators parse/simulate payloads. No provider version, config precedence, hook invocation, agent discovery, model resolution, MCP, or inference canary was recorded. | 2 repository-static | Partial | Conditional | Corrective: static hook and payload evidence can be overclaimed as Codex/Gemini consumption or live readiness. | Add read-only provider-native canaries only through approved tasks and keep all static/provider/live lanes separately labeled. | P1 near-term integrity | New Stage 04 Task: provider-native-readiness-canaries | Redacted canary records show version, config source, native agent discovery, hook event/result, permission boundary, resolved model, and explicit PASS/FAIL/SKIP without inspecting credentials. |

### Claude Controls

| ID | Benchmark | Expected control | Repository evidence | Maturity | Verdict | Confidence | Gap | Recommendation | Priority | Follow-up owner | Acceptance evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CLA-001 | [Provider Implementation Status](../../research/2026-07-07-wer/provider-implementation-status.md) | Claude has tracked local declarations at the documented native project agent path with ten registered candidates. | `git ls-tree` at the observation SHA finds ten `.claude/agents/*.md`; [Claude gateway](../../../../CLAUDE.md), local baseline, and [provider notes](../../../00.agent-governance/providers/claude.md) route loading. | 2 repository-static | Implemented | Verified repo-static | No missing repository declaration/native-path element; actual Claude discovery remains a runtime lane. | Preserve ten-file native-path inventory and gateway/provider routing. | N/A — no action | N/A — no action | N/A — no action |
| CLA-002 | Provider status: settings, hooks, permissions, sandbox, tools/MCP | Native settings define permissions/hooks, least-privilege tool boundaries, and project config without treating static parse as runtime enforcement. | `.claude/settings.json` declares permissions and six lifecycle event groups; shared scripts and validators check JSON, permission phrases, hook wiring, and payloads. No `.mcp.json` or hook/runtime canary exists. | 2 repository-static | Partial | Conditional | Complementary: strong tracked native settings exist, but actual settings precedence, hook invocation, sandbox behavior, and MCP availability are unverified. | Run an approved read-only Claude canary before claiming native enforcement or MCP readiness. | P2 planned improvement | New Stage 04 Task: claude-native-settings-canary | Record CLI version, effective project settings source, one allowed/denied boundary, agent discovery, one hook event, and MCP inventory status with secrets redacted. |
| CLA-003 | Provider status: model declarations, validator, entitlement/runtime | All ten roles use documented model syntax, semantic maps cover every role, and account/model resolution is evidenced separately from static declarations. | Supervisor declares `opus 4.8`; nine workers declare `sonnet 4.6`; expected model/tool maps cover 8/10 roles and omit `network-reviewer` and `observability-reviewer`; no account/model-resolution canary exists. | 1 documented/routed | Partial | Unverified live | Corrective: model strings/currentness are unverified, semantic coverage is 8/10, and entitlement/runtime availability is unknown. | Complete ten-role validation and canary supported alias/full-ID resolution before any separately owned model migration. | P1 near-term integrity | New Stage 04 Task: claude-declaration-and-availability-validation | Validator fixtures cover models/tools/scopes for 10/10 roles; a redacted native canary records auth surface, resolved model or explicit denial, and rollback evidence. |

### Codex Controls

| ID | Benchmark | Expected control | Repository evidence | Maturity | Verdict | Confidence | Gap | Recommendation | Priority | Follow-up owner | Acceptance evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| COD-001 | Provider implementation status | Codex has tracked declarations at the official project custom-agent path and explicit local loading guidance. | `git ls-tree` finds ten `.codex/agents/*.toml`; [AGENTS.md](../../../../AGENTS.md), [.codex/CODEX.md](../../../../.codex/CODEX.md), and [Codex provider notes](../../../00.agent-governance/providers/codex.md) route loading and preserve native TOML metadata. | 2 repository-static | Implemented | Verified repo-static | No missing element in the assessed repository declaration/native-path control; actual discovery remains part of HAR-008 provider-native consumption evidence. | Preserve ten-file native-path inventory and gateway/provider routing. | N/A — no action | N/A — no action | N/A — no action |
| COD-002 | Provider status: config, hooks, sandbox/approval, MCP | Project config and hook evidence distinguish hook validation from sandbox/approval and record effective config/MCP boundaries. | `.codex/hooks.json` declares six Claude-shaped events and passes static payload checks; no tracked `.codex/config.toml` exists, while provider notes correctly keep sandbox/approval separate from hooks. | 1 documented/routed | Partial | Conditional | Missing: reproducible project config and native consumption evidence; user/managed config, hook trust, sandbox, approvals, and MCP remain unknown. | Decide through a provider Spec whether tracked project defaults are required, then test hook/config precedence and sandbox/approval independently. | P2 planned improvement | New Stage 03 Spec: codex-project-config-boundary | Decision evidence names required project defaults or documents why none are needed; native fixtures/canary prove config precedence, hook handling, sandbox/approval separation, and MCP status. |
| COD-003 | Provider status: model declarations, validator, auth/availability | Ten roles have current, auth-surface-aware model/effort declarations and full semantic validation; runtime resolution is canaried. | Supervisor declares `gpt-5.5`/`xhigh`; nine workers use `gpt-5.3-codex`, with product deprecation dependent on ChatGPT sign-in; expected model/effort maps cover 8/10 roles; auth and model resolution were not inspected. | 1 documented/routed | Partial | Unverified live | Corrective: lifecycle depends on unknown auth surface, semantic coverage is 8/10, and entitlement/model resolution is unverified. | Inventory the non-secret auth surface, validate 10/10 declarations, and canary current resolution before the role-routing owner evaluates migrations. | P1 near-term integrity | New Stage 04 Task: codex-auth-and-availability-validation | Validator fixtures cover model/effort/scope for 10/10 roles; a redacted canary records product/API auth class, resolved/denied model, fallback behavior, and rollback. |

### Gemini Controls

| ID | Benchmark | Expected control | Repository evidence | Maturity | Verdict | Confidence | Gap | Recommendation | Priority | Follow-up owner | Acceptance evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GEM-001 | Provider implementation status | Gemini CLI project agents use the native `.gemini/agents/*.md` discovery path; local Antigravity adapters are labeled separately. | Ten `.agents/agents/*.md` local adapters exist, but no `.gemini/agents/` directory exists. The research and provider notes explicitly state that `.agents` is not Gemini CLI native registration. | 1 documented/routed | Gap | Conditional | Missing: Gemini CLI native declarations/registration; `.agents` file parity cannot establish native discovery. | Decide whether Gemini CLI is an intended runtime; if yes, design the smallest native adapter layer without moving the shared `.agents` SSoT. | P1 near-term integrity | New Stage 03 Spec: gemini-cli-native-adapter | The decision names the intended runtime; if adopted, native schema fixtures and a pinned CLI canary discover all approved agents while `.agents` remains explicitly local/shared. |
| GEM-002 | Provider status: native settings/hooks/policy/MCP | Gemini CLI uses `.gemini/settings.json`, native hook events, policy/approval semantics, and explicit MCP configuration. | No `.gemini/settings.json` exists; `.agents/hooks.json` uses Claude-shaped events and is local/Antigravity wiring, not Gemini CLI settings or a native permission gate. | 0 absent | Gap | Conditional | Missing: native Gemini settings, hook schema, policy/approval evidence, and MCP inventory. | Couple any intended native adapter with settings/policy design, negative fixtures, and provider-specific canaries; otherwise retain a documented non-runtime boundary. | P1 near-term integrity | New Stage 03 Spec: gemini-cli-settings-and-policy | Native JSON/schema validation covers intended events and policy rules, negative fixtures reject Claude-shaped substitution, and a canary records hook/policy/MCP behavior or a formal not-adopted decision. |
| GEM-003 | Provider status: model declaration, validator, entitlement/runtime | Native agent metadata uses exact lifecycle-aware model identifiers, all ten roles receive semantic validation, and account/CLI resolution is separately observed. | `.agents` declares supervisor display label `Gemini 3.1 Pro` and nine `Gemini 3.5 Flash`; validators check stems/phrases but do not semantically compare Gemini fields; no account/model/agent canary exists. | 1 documented/routed | Partial | Unverified live | Corrective: display labels do not prove exact CLI IDs/lifecycle, semantic validator coverage is absent, and entitlement/runtime availability is unknown. | After the native-runtime decision, validate exact native fields and canary account/CLI model resolution before role-routing recommendations consume availability. | P1 near-term integrity | New Stage 04 Task: gemini-native-availability-validation | A pinned CLI/account-class canary records agent discovery and resolved/denied exact model IDs; 10/10 native metadata fixtures pass and unsupported lifecycle claims fail. |

### Common-System Controls

| ID | Benchmark | Expected control | Repository evidence | Maturity | Verdict | Confidence | Gap | Recommendation | Priority | Follow-up owner | Acceptance evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| COM-001 | Governance, harness, and provider research; `HL-001` | Common stems, role-body contracts, skills, workflows, output styles, memory, and scripts have explicit owners without becoming one fictitious native runtime. | Ten stems match across 30 adapters; `.agents/{skills,workflows,output-styles}` is the shared SSoT with Claude/Codex symlink views; Stage 00 owns governance/memory, Stage 04 task evidence, Stage 99 templates, and shared scripts retain their owners. | 2 repository-static | Implemented | Verified repo-static | No missing owner boundary in the corrected benchmark; provider-native loading remains separately scored. | Preserve canonical-core plus provider-adapter language and do not describe `.agents` as a universal native runtime. | N/A — no action | N/A — no action | N/A — no action |
| COM-002 | Provider status semantic-parity finding | Parity validation covers all ten stems plus provider-required models, tools, effort, scopes, and equivalent body contracts without forcing identical metadata. | The validator checks 10-stem parity, required runtime phrases, scope imports, Claude/Codex parsing, and expected model/tool/effort for 8/10 roles; two roles are omitted and Gemini fields are not semantically compared. | 2 repository-static | Partial | Verified repo-static | Corrective: filename parity can pass while two roles or Gemini/provider-required fields drift semantically. | Extend field-aware fixtures to 10/10 roles and provider-native schemas while retaining explicit non-equivalence of permission/hook fields. | P1 near-term integrity | New Stage 04 Task: provider-adapter-semantic-parity | Positive and negative fixtures cover ten roles per provider, required fields and exact scopes; omitted-role, wrong-model/tool/effort, Gemini-schema, and body-contract drift each fail deterministically. |
| COM-003 | Harness research `HL-005`/`HL-006` | Shared hooks, validators, evidence records, and canaries preserve declared/static/provider/live boundaries across all providers. | Shared scripts and JSON payload simulations provide repository-static evidence; provider notes state Codex/Gemini wiring is not Claude permission parity; no three-provider native canary set exists. | 2 repository-static | Partial | Verified repo-static | Complementary: evidence-lane language is sound, but no comparable canary artifact demonstrates availability or detects runtime drift. | Define one redacted cross-provider canary result schema and keep every provider result independent; do not aggregate missing lanes into parity. | P2 planned improvement | New Stage 04 Task: cross-provider-canary-evidence | Three independent artifacts record version, native discovery, hook/config result, permission boundary, resolved model, MCP status, PASS/FAIL/SKIP, and timestamp without secrets; absent providers remain explicit SKIP. |

### Score and Distribution Summary

| Category | Applicable controls | Maturity numerator | Denominator | Implementation | Maturity distribution (`0/1/2/3/4`) | Verdict distribution (`Implemented/Partial/Gap/Not in scope`) | Confidence distribution (`Verified repo-static/Unverified live/Conditional`) | N/A exclusions |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| Governance | 6 | 15 | 24 | 62.5% | `0/0/3/3/0` | `4/2/0/0` | `6/0/0` | None |
| Harness and loop | 8 | 13 | 32 | 40.6% | `1/2/4/1/0` | `2/4/2/0` | `7/0/1` | None |
| Claude | 3 | 5 | 12 | 41.7% | `0/1/2/0/0` | `1/2/0/0` | `1/1/1` | None |
| Codex | 3 | 4 | 12 | 33.3% | `0/2/1/0/0` | `1/2/0/0` | `1/1/1` | None |
| Gemini | 3 | 2 | 12 | 16.7% | `1/2/0/0/0` | `0/1/2/0` | `0/1/2` | None |
| Common system | 3 | 6 | 12 | 50.0% | `0/0/3/0/0` | `1/2/0/0` | `3/0/0` | None |
| **Overall** | **26** | **45** | **104** | **43.3%** | **`2/7/13/4/0`** | **`9/13/4/0`** | **`18/3/5`** | **None** |

No maturity-4 score was awarded because no provider/native or operational canary
belongs to the fixed evidence set. The overall percentage is descriptive, not a
release or runtime readiness gate.

### `HL-001` through `HL-007` Closure Map

| Research finding | Audit controls | Audit disposition |
| --- | --- | --- |
| `HL-001` owner/inventory fact defect | GOV-002, COM-001 | Corrected research fact accepted; active catalog count and duplicate-summary repair remains P1. |
| `HL-002` retry/termination gap | HAR-004 | Gap, P1; bounded task-instantiated contract and negative fixtures required. |
| `HL-003` eval trace gap | HAR-005 | Partial, P2; optional provider-neutral evidence schema required before automation. |
| `HL-004` compaction recovery gap | HAR-006 | Partial, P2; recoverable checkpoint and rehearsal required. |
| `HL-005` provider consumption uncertainty | HAR-008, GEM-001, GEM-002 | Static declarations remain separate from native discovery/event evidence; HAR-008 owns the shared Claude/Codex/Gemini runtime-canary route. |
| `HL-006` live-readiness overclaim risk | HAR-008, COM-003 | Conditional/provider-live lanes remain independent; canaries cannot be replaced by static PASS. |
| `HL-007` MCP inventory/security gap | HAR-007 | Gap, P1; no readiness claim before approved per-server inventory and canary. |

## Comparison Analysis

- Governance and repository-static validation are the strongest categories, but
  duplicated owner summaries and stale role-count prose prevent clean currentness.
- The control loop is well documented through Verify/Learn, while retry budgets,
  attempt traces, behavioral evals, and recoverable compaction remain routed rather
  than enforced.
- Claude has the most complete tracked native settings surface. Codex has native
  agent files but no tracked project config. Gemini has local `.agents` adapters but
  no Gemini CLI native agent/settings layer.
- The common system is real as shared repository content and deterministic static
  checks. It is not a provider-neutral execution host, permission gate, MCP runtime,
  or availability proof.
- The validator proves 10-stem/30-file parity and selected Claude/Codex semantics,
  but its expected maps cover only 8 of 10 roles and it does not semantically compare
  Gemini metadata.

## Automation Opportunities

- Add fixture-backed 10/10 provider semantic validation after a scoped Stage 04
  task owns the change.
- Add retry/eval/compaction schemas only after a Stage 03 Spec identifies consumers,
  privacy boundaries, and failure semantics.
- Add redacted provider-native canary artifacts that preserve PASS/FAIL/SKIP and do
  not expose credentials or collapse providers into one parity result.
- Add an MCP inventory validator only after intended servers, owners, scopes, and
  rollback paths are approved.

## Residual Risks

- All provider entitlement, account, model resolution, agent discovery, hook
  consumption, permission behavior, MCP connection, and inference claims remain
  unverified unless a row explicitly says otherwise.
- User/managed provider settings can override or supplement tracked project files and
  were not inspected.
- Static validators can detect known structure and phrases but cannot prove that a
  model followed instructions or that remote CI/live systems are healthy.
- Model lifecycle and provider documentation can change after the fixed research
  cutoff; role-routing analysis must consume these facts without silently refreshing
  this snapshot.

## Sources

- [Audit pack README and method](README.md)
- [Workspace Governance Baseline](../../research/2026-07-07-wer/workspace-governance-baseline.md)
- [Harness and Loop Engineering](../../research/2026-07-07-wer/harness-and-loop-engineering.md)
- [Provider Implementation Status](../../research/2026-07-07-wer/provider-implementation-status.md)
- [Bootstrap Governance](../../../00.agent-governance/rules/bootstrap.md)
- [Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- [Harness Implementation Map](../../../00.agent-governance/harness-implementation-map.md)
- [Model Policy](../../../00.agent-governance/model-policy.md)
- [Claude Provider Notes](../../../00.agent-governance/providers/claude.md)
- [Codex Provider Notes](../../../00.agent-governance/providers/codex.md)
- [Gemini Provider Notes](../../../00.agent-governance/providers/gemini.md)
- [Reference Template](../../../99.templates/templates/common/reference.template.md)
- `scripts/validate-repo-quality-gates.sh` at the audit observation SHA

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-11
- Next review trigger: Stage 00 governance/harness, provider official path/schema,
  adapter inventory, native settings/config/hooks, model declaration, validator,
  MCP inventory, provider canary, audit method, or Current-pointer change.
- Refresh method: retain the old observation SHA, open a new dated audit or advance
  the snapshot explicitly, rerun static and native-canary lanes independently, and
  recalculate every numerator, denominator, distribution, and N/A exclusion.

## Related Documents

- **Audit pack**: [2026-07-11 WEIA README](README.md)
- **Implementation plan**: [WEIA implementation plan](../../../04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md)
- **Current research pack**: [2026-07-07 WER README](../../research/2026-07-07-wer/README.md)
- **Parent audits index**: [Audits README](../README.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
