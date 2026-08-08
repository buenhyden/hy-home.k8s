---
title: 'Reference: Source Coverage and Migration Ledger'
type: content/reference
status: active
owner: platform
updated: 2026-08-08
---

# Reference: Source Coverage and Migration Ledger

## Overview

This ledger preserves source, coverage, and predecessor-disposition evidence
for the consolidated WER pack. It establishes a lossless baseline; it does not
delete, rewrite, or revalidate the predecessor material.

## Reference Type

Repository-static migration and source-coverage baseline.

## Authority Boundary

The current topical reference and its canonical workspace owner retain authority
for each claim. This ledger records provenance and routing only. A predecessor
URL is dated evidence, not a 2026-08-08 checked source.

## Scope

The ledger covers the 25 tracked predecessor files, their current Git
provenance, section splits that cross new owners, and the source-register
interface for subsequent WERPC work.

## Definitions / Facts

### Source register

| Source ID | Owner topic | URL | Source class | Checked on | Adopted scope | Rejected scope | Refresh trigger |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC-WERPC-001 | 2026-07-04 predecessor pack | N/A — repository evidence | Dated predecessor evidence | 2026-07-04 | Historical claims and links preserved as provenance | No claim of current external verification | WERPC topical source review |
| SRC-WERPC-002 | 2026-07-07 predecessor pack | N/A — repository evidence | Dated predecessor evidence | 2026-07-07 | Historical claims and links preserved as provenance | No claim of current external verification | WERPC topical source review |
| SRC-WERPC-003 | 2026-08-07 predecessor pack | N/A — repository evidence | Dated predecessor evidence | 2026-08-07 | Historical claims and links preserved as provenance | No claim of current external verification | WERPC topical source review |
| SRC-WERPC-004 | Claude Code memory | [Official Anthropic memory documentation](https://code.claude.com/docs/en/memory) | Official provider primary documentation | 2026-08-08 | `CLAUDE.md`/auto-memory distinction, instruction context, `AGENTS.md` bridge, and scope/loading claims | Does not prove this repository's Claude runtime discovery, memory persistence, hook delivery, or authentication | Anthropic changes memory, instruction discovery, rules, imports, or auto-memory behavior |
| SRC-WERPC-005 | Claude Code settings and permissions | [Official Anthropic settings](https://code.claude.com/docs/en/settings) and [permission modes](https://code.claude.com/docs/en/iam) | Official provider primary documentation | 2026-08-08 | Layered settings, permissions, modes, and managed-policy boundary | Does not prove effective settings, account policy, or granted permission in this worktree | Anthropic changes settings precedence, permission modes, sandboxing, or managed policy |
| SRC-WERPC-006 | Claude Code hooks | [Official Anthropic hooks documentation](https://code.claude.com/docs/en/hooks) | Official provider primary documentation | 2026-08-08 | Hook lifecycle/event and enforcement boundary claims | Does not prove that a tracked hook was trusted, invoked, or blocked an action | Anthropic changes hook events, configuration, trust, exit, or enforcement semantics |
| SRC-WERPC-007 | Claude Code subagents | [Official Anthropic subagent documentation](https://code.claude.com/docs/en/sub-agents) | Official provider primary documentation | 2026-08-08 | Custom subagent configuration and scope claims | Does not prove local agent discovery, spawn, model, tool, or output behavior | Anthropic changes agent schema, delegation, isolation, permissions, or model behavior |
| SRC-WERPC-008 | Claude Code MCP | [Official Anthropic MCP documentation](https://code.claude.com/docs/en/mcp) | Official provider primary documentation | 2026-08-08 | MCP configuration/scoping and external-tool integration claims | Does not prove configured server availability, OAuth/key use, tool execution, or external data access | Anthropic changes MCP configuration, scope, authentication, or tool behavior |
| SRC-WERPC-009 | Codex instructions | [Official OpenAI AGENTS.md documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | Official provider primary documentation; first consulted from supplied Codex manual cache | 2026-08-08 | AGENTS discovery chain, precedence, project/global configuration guidance | Does not prove that this client/session loaded a specific local file | OpenAI changes instruction discovery, precedence, fallback filenames, or project configuration |
| SRC-WERPC-010 | Codex configuration, sandbox, approval, and models | [Official OpenAI configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), [sandbox documentation](https://learn.chatgpt.com/docs/sandboxing), and [models](https://learn.chatgpt.com/docs/models) | Official provider primary documentation; first consulted from supplied Codex manual cache | 2026-08-08 | Configuration/sandbox/approval distinction, model/reasoning configuration surface | Does not prove effective parsed config, approval result, authenticated model availability, or resolved model | OpenAI changes config keys, sandbox modes, approval policy, model/reasoning values, or availability rules |
| SRC-WERPC-011 | Codex subagents | [Official OpenAI subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Official provider primary documentation; first consulted from supplied Codex manual cache | 2026-08-08 | Delegation, custom-agent files, inheritance, and orchestration claims | Does not prove project agent discovery, spawned runtime, inherited tool availability, or result quality | OpenAI changes subagent defaults, agent schema, inheritance, concurrency, or orchestration |
| SRC-WERPC-012 | Codex hooks | [Official OpenAI hooks documentation](https://learn.chatgpt.com/docs/hooks) | Official provider primary documentation; first consulted from supplied Codex manual cache | 2026-08-08 | Hook discovery, trust, lifecycle events, and configuration shape claims | Does not prove that `.codex/hooks.json` was trusted, consumed, or enforced during a run | OpenAI changes hook event, trust, configuration, execution, or managed-hook semantics |
| SRC-WERPC-013 | Codex MCP | [Official OpenAI MCP documentation](https://learn.chatgpt.com/docs/extend/mcp) | Official provider primary documentation; first consulted from supplied Codex manual cache | 2026-08-08 | MCP as external tool/context configuration surface | Does not prove a server is installed, authenticated, available, or authorized for mutation | OpenAI changes MCP configuration, authentication, permission, or tool behavior |

WERPC-001 imported no external current source. WERPC-002 adds SRC-WERPC-004
through SRC-WERPC-013 after a 2026-08-08 primary-source review. Any other URL
inside predecessor content remains dated evidence until separately registered
with its predecessor date and an explicit current recheck.

### WERPC-002 claim register

| Claim ID | Owner | Claim / status | Supporting evidence | Boundary and uncertainty |
| --- | --- | --- | --- | --- |
| CLM-WERPC-002-01 | Harness | `Verified`: the workspace contract defines context, tools, guardrails, evaluation, recovery, and observability surfaces. | `.codex/CODEX.md`, `harness-catalog.md`, quality standards, loop contract; observed 2026-08-08. | Static implementation evidence only; component effectiveness/runtime delivery is not measured. |
| CLM-WERPC-002-02 | Loop | `Verified`: the machine contract declares `ready`, `running`, `validating`, `retry-assessment`, `completed`, `blocked`, `escalated`, and `aborted`, plus transitions and terminal states. | `contracts/agent-loop-lifecycle.json`; observed 2026-08-08. | Does not prove a provider emitted/obeyed each transition. |
| CLM-WERPC-002-03 | Loop | `Verified`: same-signature automatic retry limit is two and task recovery limit is three; identical no-progress second result escalates. | `contracts/agent-loop-lifecycle.json`; observed 2026-08-08. | Local policy, not an external provider behavior claim. |
| CLM-WERPC-002-04 | Workspace | `Verified`: root gateways and Stage 00 encode the JIT governance route and repository-wins durable memory design. | `AGENTS.md`, `CLAUDE.md`, bootstrap, runtime baselines, `memory/progress.md`; observed 2026-08-08. | Native client discovery and provider memory activity are `DEFER`. |
| CLM-WERPC-002-05 | Claude | `Verified`: Anthropic documents `CLAUDE.md` context, auto memory, and an `AGENTS.md` import/symlink bridge; it does not describe native AGENTS discovery. | SRC-WERPC-004, checked 2026-08-08. | Product claim only; this worktree's Claude discovery is `DEFER`. |
| CLM-WERPC-002-06 | Claude | `Verified`: native settings, hooks, subagents, permissions, and MCP have distinct official surfaces. | SRC-WERPC-005–008, checked 2026-08-08. | Tracked `.claude/**` proves only static configuration; trust, parse, authentication, and execution are `DEFER`. |
| CLM-WERPC-002-07 | Codex | `Verified`: OpenAI documents AGENTS discovery, configuration, hooks, custom agents/subagents, MCP, and separate sandbox/approval controls. | SRC-WERPC-009–013, checked 2026-08-08; official manual cache consulted first. | Product claim only. The worktree has no tracked `.codex/config.toml`; `.codex/CODEX.md` is a baseline, and native consumption/effective settings are `DEFER`. |
| CLM-WERPC-002-08 | Common system | `Partial`: the workspace has a provider-neutral static control plane and static role parity. | `harness-catalog.md`, provider notes, adapters, and contracts; observed 2026-08-08. | `Partial` because parity/discovery, effective permissions, model resolution, and runtime operation remain unobserved. |
| CLM-WERPC-002-09 | Provider runtime | `DEFER`: a client discovered the adapters, trusted hooks, authenticated, resolved models, and connected MCP servers. | No authorized non-secret runtime observation collected. | Requires scoped client/version/runtime evidence; static files and official docs cannot close it. |

### Tracked predecessor baseline

The following is the retained output of the required tracked-file enumeration:

```text
docs/90.references/research/2026-07-04-wer/README.md
docs/90.references/research/2026-07-04-wer/ai-agents-roster-and-gap-analysis.md
docs/90.references/research/2026-07-04-wer/automation-pipeline-workflow-qa.md
docs/90.references/research/2026-07-04-wer/harness-and-loop-engineering.md
docs/90.references/research/2026-07-04-wer/kubernetes-infrastructure-security.md
docs/90.references/research/2026-07-04-wer/provider-implementation-status.md
docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md
docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md
docs/90.references/research/2026-07-07-wer/README.md
docs/90.references/research/2026-07-07-wer/ai-agents-roster-and-gap-analysis.md
docs/90.references/research/2026-07-07-wer/automation-pipeline-workflow-qa.md
docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md
docs/90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md
docs/90.references/research/2026-07-07-wer/harness-and-loop-engineering.md
docs/90.references/research/2026-07-07-wer/kubernetes-infrastructure-security.md
docs/90.references/research/2026-07-07-wer/provider-implementation-status.md
docs/90.references/research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md
docs/90.references/research/2026-07-07-wer/workspace-governance-baseline.md
docs/90.references/research/2026-08-07-wer/README.md
docs/90.references/research/2026-08-07-wer/agent-memory-tiers-and-management.md
docs/90.references/research/2026-08-07-wer/agent-model-routing-and-configuration.md
docs/90.references/research/2026-08-07-wer/documentation-architecture-and-diataxis.md
docs/90.references/research/2026-08-07-wer/github-actions-and-ci-evidence.md
docs/90.references/research/2026-08-07-wer/llm-wiki-and-knowledge-routing.md
docs/90.references/research/2026-08-07-wer/research-consolidation-and-supersession-map.md
```

The enumeration count is 25: eight files under `2026-07-04-wer`, ten under
`2026-07-07-wer`, and seven under `2026-08-07-wer`.

### File-level disposition baseline

| Old path | Source commit | Topic or heading | Verification | New owner | Disposition | Reason and evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/90.references/research/2026-07-04-wer/README.md` | `147b27badd56e4ec10f8725c59e312a6d12c63f4` | Pack navigation | Tracked path and full Git provenance observed | `README.md` | Retain pending cutover gate | Snapshot profile and report index are represented by the new pack README. |
| `docs/90.references/research/2026-07-04-wer/ai-agents-roster-and-gap-analysis.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | AI agents | Tracked path and full Git provenance observed | `ai-agents-and-agency-agents.md` | Retain pending cutover gate | Agent roster and external-catalog material route to the AI-agent owner. |
| `docs/90.references/research/2026-07-04-wer/automation-pipeline-workflow-qa.md` | `2bce69fd6ddb850a94f886ef8906ce436a937cea` | Automation and QA | Tracked path and full Git provenance observed | `ci-cd-github-actions-and-qa.md` | Retain pending cutover gate | Automation, workflow, CI/CD, and QA route to one delivery owner. |
| `docs/90.references/research/2026-07-04-wer/harness-and-loop-engineering.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | Harness and loop | Tracked path and full Git provenance observed | `harness-and-loop-engineering.md` | Retain pending cutover gate | Harness and loop evidence has one focused owner. |
| `docs/90.references/research/2026-07-04-wer/kubernetes-infrastructure-security.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | Platform security | Tracked path and full Git provenance observed | `kubernetes-infrastructure-and-security.md` | Retain pending cutover gate | Kubernetes, infrastructure, and security route to one platform owner. |
| `docs/90.references/research/2026-07-04-wer/provider-implementation-status.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | Provider status | Tracked path and full Git provenance observed | `provider-implementation-status.md` | Retain pending cutover gate | Provider product and local-adapter separation routes to provider status. |
| `docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | SDLC and QA | Tracked path and full Git provenance observed | `spec-driven-sdlc-and-document-contracts.md` | Retain pending cutover gate | Primary SDLC material routes to the document-contract owner; delivery sections split below. |
| `docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | Workspace governance | Tracked path and full Git provenance observed | `workspace-governance-and-common-agent-environment.md` | Retain pending cutover gate | Shared environment material routes to workspace governance; cross-topic sections split below. |
| `docs/90.references/research/2026-07-07-wer/README.md` | `93bc9b6851de6f7f286fdad4a1ee83d4ba9e5f55` | Pack navigation and coverage | Tracked path and full Git provenance observed | `README.md` | Retain pending cutover gate | New README carries navigation and request-owner coverage. |
| `docs/90.references/research/2026-07-07-wer/ai-agents-roster-and-gap-analysis.md` | `93bc9b6851de6f7f286fdad4a1ee83d4ba9e5f55` | AI agents and routing | Tracked path and full Git provenance observed | `ai-agents-and-agency-agents.md` | Retain pending cutover gate | Agent-system evidence routes to AI agents; model portions split below. |
| `docs/90.references/research/2026-07-07-wer/automation-pipeline-workflow-qa.md` | `42360b3c95e7fffce1c43b52d890a40507eae403` | Automation and workflow | Tracked path and full Git provenance observed | `ci-cd-github-actions-and-qa.md` | Retain pending cutover gate | Delivery topology and QA evidence route to the delivery owner. |
| `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md` | `38a2fe6b90bad694d0a9a021c7edce8d800e03ea` | Migration evidence | Tracked path and full Git provenance observed | `source-coverage-and-migration-ledger.md` | Retain pending cutover gate | Provenance and migration facts route to this ledger. |
| `docs/90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md` | `787b28fe1f2b1fff16d59936ed2a411e04d25db5` | Document contract | Tracked path and full Git provenance observed | `spec-driven-sdlc-and-document-contracts.md` | Retain pending cutover gate | Document types route to SDLC contracts; Diátaxis portions split below. |
| `docs/90.references/research/2026-07-07-wer/harness-and-loop-engineering.md` | `42360b3c95e7fffce1c43b52d890a40507eae403` | Harness and loop | Tracked path and full Git provenance observed | `harness-and-loop-engineering.md` | Retain pending cutover gate | The newer harness/loop evidence routes to its focused owner. |
| `docs/90.references/research/2026-07-07-wer/kubernetes-infrastructure-security.md` | `42360b3c95e7fffce1c43b52d890a40507eae403` | Platform security | Tracked path and full Git provenance observed | `kubernetes-infrastructure-and-security.md` | Retain pending cutover gate | Platform security evidence routes to its focused owner. |
| `docs/90.references/research/2026-07-07-wer/provider-implementation-status.md` | `93bc9b6851de6f7f286fdad4a1ee83d4ba9e5f55` | Provider status and model routing | Tracked path and full Git provenance observed | `provider-implementation-status.md` | Retain pending cutover gate | Provider surface evidence routes to provider status; routing sections split below. |
| `docs/90.references/research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md` | `42360b3c95e7fffce1c43b52d890a40507eae403` | SDLC, CI/CD, and QA | Tracked path and full Git provenance observed | `spec-driven-sdlc-and-document-contracts.md` | Retain pending cutover gate | SDLC routes to document contracts; CI/CD and QA sections split below. |
| `docs/90.references/research/2026-07-07-wer/workspace-governance-baseline.md` | `42360b3c95e7fffce1c43b52d890a40507eae403` | Workspace governance | Tracked path and full Git provenance observed | `workspace-governance-and-common-agent-environment.md` | Retain pending cutover gate | Governance routing is owned by the common-environment reference. |
| `docs/90.references/research/2026-08-07-wer/README.md` | `39b34f93a65286113e00d21078a2f53d6282bf01` | Pack navigation | Tracked path and full Git provenance observed | `README.md` | Retain pending cutover gate | Pack boundary and navigation route to the successor README. |
| `docs/90.references/research/2026-08-07-wer/agent-memory-tiers-and-management.md` | `39b34f93a65286113e00d21078a2f53d6282bf01` | Memory tiers | Tracked path and full Git provenance observed | `agent-memory-tiers-and-management.md` | Retain pending cutover gate | Four-class memory material routes to the memory owner. |
| `docs/90.references/research/2026-08-07-wer/agent-model-routing-and-configuration.md` | `39b34f93a65286113e00d21078a2f53d6282bf01` | Model routing | Tracked path and full Git provenance observed | `agent-model-routing-and-configuration.md` | Retain pending cutover gate | Model selection and configuration route to the model owner. |
| `docs/90.references/research/2026-08-07-wer/documentation-architecture-and-diataxis.md` | `39b34f93a65286113e00d21078a2f53d6282bf01` | Documentation architecture | Tracked path and full Git provenance observed | `documentation-architecture-and-diataxis.md` | Retain pending cutover gate | Diátaxis and documentation architecture route to their focused owner. |
| `docs/90.references/research/2026-08-07-wer/github-actions-and-ci-evidence.md` | `39b34f93a65286113e00d21078a2f53d6282bf01` | Actions and CI evidence | Tracked path and full Git provenance observed | `ci-cd-github-actions-and-qa.md` | Retain pending cutover gate | Actions, CI/CD, and QA evidence route to the delivery owner. |
| `docs/90.references/research/2026-08-07-wer/llm-wiki-and-knowledge-routing.md` | `39b34f93a65286113e00d21078a2f53d6282bf01` | LLM-WIKI routing | Tracked path and full Git provenance observed | `llm-wiki-and-knowledge-routing.md` | Retain pending cutover gate | Knowledge routing routes to its focused owner. |
| `docs/90.references/research/2026-08-07-wer/research-consolidation-and-supersession-map.md` | `39b34f93a65286113e00d21078a2f53d6282bf01` | Consolidation evidence | Tracked path and full Git provenance observed | `source-coverage-and-migration-ledger.md` | Retain pending cutover gate | Consolidation and supersession facts route to the migration ledger. |

### Section-level split dispositions

| Old path | Source commit | Topic or heading | Verification | New owner | Disposition | Reason and evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/90.references/research/2026-07-04-wer/ai-agents-roster-and-gap-analysis.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | ### External catalog snapshot: `msitarzewski/agency-agents` (non-authoritative market scan) | H3 observed in required predecessor inventory | `ai-agents-and-agency-agents.md#agency-agents-baseline` | Route by section | The section is the dated predecessor basis for the agency-agents owner. |
| `docs/90.references/research/2026-07-04-wer/automation-pipeline-workflow-qa.md` | `2bce69fd6ddb850a94f886ef8906ce436a937cea` | `### QA evidence lanes` | H3 observed in required predecessor inventory | `ci-cd-github-actions-and-qa.md#qa-baseline` | Route by section | QA is a distinct requested topic owned by the delivery reference. |
| `docs/90.references/research/2026-07-04-wer/automation-pipeline-workflow-qa.md` | `2bce69fd6ddb850a94f886ef8906ce436a937cea` | `### Permissions, secrets, and token boundary` | H3 observed in required predecessor inventory | `kubernetes-infrastructure-and-security.md#security-baseline` | Route by section | Workflow permission and secret-boundary material is security evidence, while automation remains with the delivery owner. |
| `docs/90.references/research/2026-07-04-wer/harness-and-loop-engineering.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | `### Workspace Application Routing Notes` | H3 observed in required predecessor inventory | `workspace-governance-and-common-agent-environment.md#workspace-application-baseline` | Route by section | Workspace application is separately requested and has its own primary owner. |
| `docs/90.references/research/2026-07-04-wer/kubernetes-infrastructure-security.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | `### CI/CD and QA links` | H3 observed in required predecessor inventory | `ci-cd-github-actions-and-qa.md#qa-baseline` | Route by section | The platform file's delivery-validation links route to the delivery and QA owner. |
| `docs/90.references/research/2026-07-04-wer/provider-implementation-status.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | `### Common environment and rule system` | H3 observed in required predecessor inventory | `workspace-governance-and-common-agent-environment.md#common-system-baseline` | Route by section | Common-system material belongs to the common-environment owner. |
| `docs/90.references/research/2026-07-04-wer/provider-implementation-status.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | `### Shared MCP/tooling considerations` | H3 observed in required predecessor inventory | `harness-and-loop-engineering.md#harness-baseline` | Route by section | Shared tool-protocol and harness-boundary material routes to the harness owner. |
| `docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | `### CI/CD` | H3 observed in required predecessor inventory | `ci-cd-github-actions-and-qa.md#cicd-baseline` | Route by section | CI/CD has a separate requested topic and delivery owner. |
| `docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | `### Security and supply-chain findings` | H3 observed in required predecessor inventory | `kubernetes-infrastructure-and-security.md#security-baseline` | Route by section | Security and supply-chain material routes to the security owner rather than the SDLC owner. |
| `docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | `### QA and validation evidence` | H3 observed in required predecessor inventory | `ci-cd-github-actions-and-qa.md#qa-baseline` | Route by section | QA evidence has a distinct requested owner. |
| `docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | `### Formatting, linting, and pre-commit` | H3 observed in required predecessor inventory | `ci-cd-github-actions-and-qa.md#qa-baseline` | Route by section | Formatting and linting are delivery-quality evidence owned with QA. |
| `docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | `### Repo-local validation matrix` | H3 observed in required predecessor inventory | `ci-cd-github-actions-and-qa.md#qa-baseline` | Route by section | The repository validation matrix routes to the QA evidence owner. |
| `docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | `### roles and provider adapters` | H3 observed in required predecessor inventory | `provider-implementation-status.md#claude-baseline` | Route by section | Provider-adapter observations route to provider status; the shared governance contract remains with workspace governance. |
| `docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | `### CI/CD and QA evidence lanes` | H3 observed in required predecessor inventory | `ci-cd-github-actions-and-qa.md#qa-baseline` | Route by section | Delivery evidence is duplicated across governance and delivery material; delivery owns it. |
| `docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | `### formatting, linting, and syntax validation` | H3 observed in required predecessor inventory | `ci-cd-github-actions-and-qa.md#qa-baseline` | Route by section | Formatting and syntax-validation material routes to the QA owner. |
| `docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | `### automation, pipeline, and workflow` | H3 observed in required predecessor inventory | `ci-cd-github-actions-and-qa.md#cicd-baseline` | Route by section | Automation and pipeline material routes to the CI/CD owner. |
| `docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | `### templates and integration guides` | H3 observed in required predecessor inventory | `spec-driven-sdlc-and-document-contracts.md#guide-baseline` | Route by section | Template and guide-family material routes to the document-contract owner. |
| `docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | `### scripts and validation` | H3 observed in required predecessor inventory | `ci-cd-github-actions-and-qa.md#qa-baseline` | Route by section | Validation-script material routes to the QA evidence owner. |
| `docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | `### SDLC position` | H3 observed in required predecessor inventory | `spec-driven-sdlc-and-document-contracts.md#sdlc-baseline` | Route by section | SDLC-position material routes to the SDLC owner. |
| `docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md` | `8b4de80127463d9dd1c34bf8a12991d5ff0c3e92` | `### security boundary` | H3 observed in required predecessor inventory | `kubernetes-infrastructure-and-security.md#security-baseline` | Route by section | Security-boundary material routes to the security owner. |
| `docs/90.references/research/2026-07-07-wer/ai-agents-roster-and-gap-analysis.md` | `93bc9b6851de6f7f286fdad4a1ee83d4ba9e5f55` | `### Provider-Native Adapter Status` | H3 observed in required predecessor inventory | `provider-implementation-status.md#claude-baseline` | Route by section | Native-provider adapter observations route to provider status. |
| `docs/90.references/research/2026-07-07-wer/ai-agents-roster-and-gap-analysis.md` | `93bc9b6851de6f7f286fdad4a1ee83d4ba9e5f55` | `### Secondary AI-Agent QA Application` | H3 observed in required predecessor inventory | `ci-cd-github-actions-and-qa.md#qa-baseline` | Route by section | The secondary QA application routes to the QA evidence owner. |
| `docs/90.references/research/2026-07-07-wer/ai-agents-roster-and-gap-analysis.md` | `93bc9b6851de6f7f286fdad4a1ee83d4ba9e5f55` | `### Role and Model-Routing Decision Record` | H3 observed in required predecessor inventory | `agent-model-routing-and-configuration.md#model-routing-baseline` | Route by section | Model-routing material has a distinct primary owner. |
| `docs/90.references/research/2026-07-07-wer/automation-pipeline-workflow-qa.md` | `42360b3c95e7fffce1c43b52d890a40507eae403` | `### Permissions and Workflow Security Boundary` | H3 observed in required predecessor inventory | `kubernetes-infrastructure-and-security.md#security-baseline` | Route by section | Workflow security and permission evidence routes to the security owner. |
| `docs/90.references/research/2026-07-07-wer/automation-pipeline-workflow-qa.md` | `42360b3c95e7fffce1c43b52d890a40507eae403` | `### GitOps Delivery Boundary` | H3 observed in required predecessor inventory | `kubernetes-infrastructure-and-security.md#infrastructure-baseline` | Route by section | GitOps delivery-boundary material routes to the infrastructure owner. |
| `docs/90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md` | `787b28fe1f2b1fff16d59936ed2a411e04d25db5` | `### Decision Ledger` | H3 observed in required predecessor inventory | `documentation-architecture-and-diataxis.md#documentation-architecture-baseline` | Route by section | Documentation decision structure is routed to the documentation-architecture owner. |
| `docs/90.references/research/2026-07-07-wer/provider-implementation-status.md` | `93bc9b6851de6f7f286fdad4a1ee83d4ba9e5f55` | `### Current Model Surface Matrix — 2026-07-10 10:00 KST` | H3 observed in required predecessor inventory | `agent-model-routing-and-configuration.md#model-routing-baseline` | Route by section | Model-surface material routes to the model-routing owner. |
| `docs/90.references/research/2026-07-07-wer/provider-implementation-status.md` | `93bc9b6851de6f7f286fdad4a1ee83d4ba9e5f55` | `### Per-Model Evaluation and Migration Matrix` | H3 observed in required predecessor inventory | `agent-model-routing-and-configuration.md#model-routing-baseline` | Route by section | Model evaluation and migration material routes to the model-routing owner. |
| `docs/90.references/research/2026-07-07-wer/provider-implementation-status.md` | `93bc9b6851de6f7f286fdad4a1ee83d4ba9e5f55` | `### Task-Characteristic Model Recommendation` | H3 observed in required predecessor inventory | `agent-model-routing-and-configuration.md#model-routing-baseline` | Route by section | Model recommendation is separate from provider product surface analysis. |
| `docs/90.references/research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md` | `42360b3c95e7fffce1c43b52d890a40507eae403` | `### QA Evidence Lane Matrix` | H3 observed in required predecessor inventory | `ci-cd-github-actions-and-qa.md#qa-baseline` | Route by section | QA evidence is separately owned by the delivery reference. |
| `docs/90.references/research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md` | `42360b3c95e7fffce1c43b52d890a40507eae403` | `### Formatting, Linting, and Syntax Interpretation` | H3 observed in required predecessor inventory | `ci-cd-github-actions-and-qa.md#qa-baseline` | Route by section | Formatting and syntax material routes to the QA owner. |
| `docs/90.references/research/2026-07-07-wer/workspace-governance-baseline.md` | `42360b3c95e7fffce1c43b52d890a40507eae403` | `### Owner and Authority Matrix` | H3 observed in required predecessor inventory | `workspace-governance-and-common-agent-environment.md#common-system-baseline` | Route by section | Common ownership and governance remain with the workspace environment owner. |
| `docs/90.references/research/2026-08-07-wer/documentation-architecture-and-diataxis.md` | `39b34f93a65286113e00d21078a2f53d6282bf01` | `### SDLC Document Types` | H3 observed in required predecessor inventory | `spec-driven-sdlc-and-document-contracts.md#sdlc-baseline` | Route by section | The predecessor's SDLC document-family inventory routes to the SDLC contract owner. |
| `docs/90.references/research/2026-08-07-wer/research-consolidation-and-supersession-map.md` | `39b34f93a65286113e00d21078a2f53d6282bf01` | `### Supersession Map` | H3 observed in required predecessor inventory | `source-coverage-and-migration-ledger.md#file-level-disposition-baseline` | Route by section | The predecessor supersession relationship is preserved in the new migration ledger. |
| `docs/90.references/research/2026-08-07-wer/research-consolidation-and-supersession-map.md` | `39b34f93a65286113e00d21078a2f53d6282bf01` | `### Topic Ownership from 2026-08-07` | H3 observed in required predecessor inventory | `README.md#requirement-coverage-matrix` | Route by section | The predecessor topic-owner map routes to the successor coverage matrix. |

### Mutable-reference classification

No mutable consumer is migrated in WERPC-001. WERPC-007 owns occurrence
discovery and classification; WERPC-008 requires the completed classification
before cutover. This boundary prevents baseline inventory from asserting a
consumer migration that has not occurred.

## Sources

The source register above is the interface for later research. Its three
initial entries are explicitly dated predecessor evidence rather than current
external checks.

## Review and Freshness

Refresh source rows when WERPC-002 through WERPC-006 record a checked source.
Refresh provenance only if the predecessor path or its content-bearing Git
history changes before cutover.

## Related Documents

- [Pack README](README.md)
- [WERPC Task](../../../04.execution/tasks/2026-08-08-workspace-engineering-research-pack-consolidation.md)
- [WERPC Plan](../../../04.execution/plans/2026-08-08-workspace-engineering-research-pack-consolidation.md)
