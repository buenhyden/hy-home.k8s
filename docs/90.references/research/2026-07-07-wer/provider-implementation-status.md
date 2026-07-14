---
title: 'Reference: Provider Harness Implementation Status Research'
type: content/reference
status: accepted
owner: platform
updated: 2026-07-14
---

# Reference: Provider Harness Implementation Status Research

## Overview

이 문서는 Claude Code, Codex, Gemini CLI와 각 공급자의 API 모델 표면을
`hy-home.k8s`의 로컬 어댑터 선언과 비교한다. 공급자 기능, 제품/CLI 가용성,
API 모델 수명주기, 로컬 표시 문자열, 실행 권고를 하나의 상태로 합치지 않는다.

외부 소스 컷오프는 정확히 `2026-07-10 10:00 KST`다. 로컬 사실은 같은 시점의
tracked checkout을 정적으로 검사한 결과다. 이 스냅샷은 프로바이더 로그인,
계정별 entitlement, 설치된 CLI 버전, 실제 모델 해석, hook 소비, subagent 실행,
MCP 연결 또는 live inference를 검증하지 않았다.

### Purpose

- 세 공급자의 공식 agent/subagent, model, hook, permission, settings 표면을
  surface별로 비교한다.
- 10개 역할의 3개 로컬 어댑터, 모델 문자열, scope, tool/effort, hook wiring과
  validator coverage를 실제 파일에 맞춰 기록한다.
- 모델 선택을 default/escalation/fallback과 eval 조건으로 제안하되 활성
  `model-policy`, 어댑터 또는 런타임 설정은 변경하지 않는다.
- 구현 공백은 위험 근거와 canonical 후속 경로를 가진 권고로만 남긴다.

## Reference Type

- Type: durable-concept / external-standard-snapshot / dated-implementation-audit
- Source checked: `2026-07-10 10:00 KST`
- Repo evidence checked: `2026-07-10`
- Refresh trigger: provider model catalog, lifecycle/deprecation, coding-product
  authentication, CLI version/availability, native agent schema, hook semantics,
  local adapter/model policy, or validator coverage changes.

## Authority Boundary

- **Authoritative for**: 이 컷오프의 공식 문서와 현재 checkout을 연결한 설명,
  fact-defect 교정, 비교 및 비변경 권고.
- **Not authoritative for**: active model tier, provider credential/entitlement,
  CLI 설치 상태, native runtime registration, hook trust/consumption, MCP 연결,
  inference 결과, live cluster/remote readiness 또는 배포 승인.
- Local implementation claims are controlled by current repository evidence;
  upstream capability and lifecycle claims are controlled by the linked official
  surface. A label in an adapter is not proof that a provider accepted or ran it.
- Active owners remain
  [model-policy.md](../../../00.agent-governance/model-policy.md),
  [harness-catalog.md](../../../00.agent-governance/harness-catalog.md), provider
  notes/runtime files, provider-native settings, and repository validators. This
  Stage 90 reference does not override them.

## Scope

- Claude API/Claude Code, OpenAI API/Codex product and CLI, Gemini API/Gemini CLI.
- Instructions/settings, custom agents, tools, hooks, sandbox/permissions, model
  selection and local validation evidence.
- The 30 tracked local role adapters and three tracked hook/settings JSON files.
- No active script, hook, adapter, model policy, provider config, credential,
  manifest, CI workflow, runtime, or third-party resource change.

## Definitions / Facts

### Evidence and Surface Rules

| Evidence class | Meaning in this reference | It does not prove |
| --- | --- | --- |
| Official API catalog | Model ID and lifecycle shown by the provider API documentation at the cutoff. | Coding-product access, account entitlement, CLI routing, or local use. |
| Official coding-product/CLI documentation | Documented model selection, custom-agent, hook, config, sandbox, or command behavior for that product. | That the installed local version/account supports it or that this checkout activates it. |
| Repo declaration | Tracked gateway, adapter, hook/settings JSON, model label, scope, tools, effort, or validator code. | Native registration, runtime interpretation, hook execution, live inference, or semantic output parity. |
| Validator result | Parse, required phrase, stem, selected field, scope, and payload-simulation checks implemented by the current validator. | Complete provider schema conformance, every field's parity, provider consumption, or model availability. |
| Recommendation | A proposed default/escalation/fallback route requiring evaluation before an active-owner change. | Approval to edit active provider/model/runtime files. |

### Exact Cutoff Handling

The fixed cutoff is `2026-07-10 10:00 KST`. A provider/model fact is included
only when an official dated announcement predates that instant or the official
page was captured during the cutoff check. OpenAI's dated 2026-07-09 GPT-5.6
general-availability announcement is therefore eligible, but its stated gradual
rollout is not converted into local account availability. Later page
representations are not used as cutoff evidence. API publication, product
rollout, CLI resolution, account entitlement, and this workspace's local
assignment remain separate evidence lanes.

### Local Provider Inventory — 2026-07-10

The matrix below is the exact role-by-role inventory used by this audit. Scope
paths are imported by all three files named in the row. Claude `tools:` is a
Claude-native allowlist field; it is recorded as a local fact and is **not** a
cross-provider parity field. Codex has no `tools` or per-agent `sandbox_mode`
field in these files. Each `.agents` Markdown file has exactly the frontmatter
keys `name`, `description`, and `model`; none has `tools`, `effort`, or
`sandbox_mode`. Those `.agents` files are local/Antigravity adapters, not proof
of Gemini CLI native registration.

| Role and exact imported scope | Claude adapter, model, native `tools:` | Codex adapter, model, reasoning effort | `.agents` local adapter, model, absent fields |
| --- | --- | --- | --- |
| `code-reviewer`; `docs/00.agent-governance/scopes/architecture.md` | `.claude/agents/code-reviewer.md`; `sonnet 4.6`; `Read, Grep, Glob, Bash` | `.codex/agents/code-reviewer.toml`; `gpt-5.3-codex`; `high` | `.agents/agents/code-reviewer.md`; `Gemini 3.5 Flash`; no `tools`/`effort`/`sandbox_mode` |
| `doc-writer`; `docs/00.agent-governance/scopes/docs.md` | `.claude/agents/doc-writer.md`; `sonnet 4.6`; `Read, Write, Edit, Grep, Glob, Bash` | `.codex/agents/doc-writer.toml`; `gpt-5.3-codex`; `medium` | `.agents/agents/doc-writer.md`; `Gemini 3.5 Flash`; no `tools`/`effort`/`sandbox_mode` |
| `gitops-reviewer`; `docs/00.agent-governance/scopes/infra.md` | `.claude/agents/gitops-reviewer.md`; `sonnet 4.6`; `Read, Grep, Glob, Bash` | `.codex/agents/gitops-reviewer.toml`; `gpt-5.3-codex`; `high` | `.agents/agents/gitops-reviewer.md`; `Gemini 3.5 Flash`; no `tools`/`effort`/`sandbox_mode` |
| `incident-responder`; `docs/00.agent-governance/scopes/ops.md` and `docs/00.agent-governance/scopes/infra.md` | `.claude/agents/incident-responder.md`; `sonnet 4.6`; `Read, Grep, Glob, Bash` | `.codex/agents/incident-responder.toml`; `gpt-5.3-codex`; `high` | `.agents/agents/incident-responder.md`; `Gemini 3.5 Flash`; no `tools`/`effort`/`sandbox_mode` |
| `k8s-implementer`; `docs/00.agent-governance/scopes/infra.md` | `.claude/agents/k8s-implementer.md`; `sonnet 4.6`; `Read, Write, Edit, Grep, Glob, Bash` | `.codex/agents/k8s-implementer.toml`; `gpt-5.3-codex`; `high` | `.agents/agents/k8s-implementer.md`; `Gemini 3.5 Flash`; no `tools`/`effort`/`sandbox_mode` |
| `network-reviewer`; `docs/00.agent-governance/scopes/infra.md` | `.claude/agents/network-reviewer.md`; `sonnet 4.6`; `Read, Grep, Glob, Bash` | `.codex/agents/network-reviewer.toml`; `gpt-5.3-codex`; `high` | `.agents/agents/network-reviewer.md`; `Gemini 3.5 Flash`; no `tools`/`effort`/`sandbox_mode` |
| `observability-reviewer`; `docs/00.agent-governance/scopes/infra.md` | `.claude/agents/observability-reviewer.md`; `sonnet 4.6`; `Read, Grep, Glob, Bash` | `.codex/agents/observability-reviewer.toml`; `gpt-5.3-codex`; `high` | `.agents/agents/observability-reviewer.md`; `Gemini 3.5 Flash`; no `tools`/`effort`/`sandbox_mode` |
| `security-auditor`; `docs/00.agent-governance/scopes/security.md` | `.claude/agents/security-auditor.md`; `sonnet 4.6`; `Read, Grep, Glob, Bash` | `.codex/agents/security-auditor.toml`; `gpt-5.3-codex`; `high` | `.agents/agents/security-auditor.md`; `Gemini 3.5 Flash`; no `tools`/`effort`/`sandbox_mode` |
| `supervisor`; `docs/00.agent-governance/scopes/meta.md` | `.claude/agents/supervisor.md`; `opus 4.8`; `Read, Grep, Glob, Bash, Edit, Write, Task` | `.codex/agents/supervisor.toml`; `gpt-5.5`; `xhigh` | `.agents/agents/supervisor.md`; `Gemini 3.1 Pro`; no `tools`/`effort`/`sandbox_mode` |
| `wiki-curator`; `docs/00.agent-governance/scopes/docs.md` | `.claude/agents/wiki-curator.md`; `sonnet 4.6`; `Read, Write, Edit, Grep, Glob, Bash` | `.codex/agents/wiki-curator.toml`; `gpt-5.3-codex`; `medium` | `.agents/agents/wiki-curator.md`; `Gemini 3.5 Flash`; no `tools`/`effort`/`sandbox_mode` |

The matrix proves 30 concrete files and exact declared values. It also proves
that every `observability-reviewer` imports `scopes/infra.md`, not a nonexistent
`scopes/observability.md`; it does not prove provider loading or behavior.

- `.claude/settings.json`, `.codex/hooks.json`, and `.agents/hooks.json` are
  tracked. `.codex/config.toml`, `.gemini/settings.json`, and `.mcp.json` are not
  tracked in this checkout. The absence of `.codex/config.toml` does not prevent
  official standalone `.codex/agents/*.toml` discovery; it leaves global agent
  limits at documented defaults (`max_threads=6`, `max_depth=1`) unless another
  active config layer overrides them.
- `.claude/settings.json` binds shared `session-start.sh`, `k8s-pre-edit.sh`,
  `post-validate.sh`, and `lifecycle-guard.sh`; it does not bind
  `scripts/validate-harness.sh` directly. The Codex and `.agents` JSON files
  reference the same shared scripts using provider-specific project-directory
  fallbacks.
- `scripts/validate-repo-quality-gates.sh` proves exact file-stem parity. It
  validates selected Claude model/tools and Codex model/effort fields, compares
  Claude/Codex scope imports, and parses all three JSON files. Its expected-field
  maps omit `network-reviewer` and `observability-reviewer`, and it does not
  semantically compare Gemini fields to the other adapters. Stem parity is
  therefore stronger than complete provider-native field or behavior parity.

### Provider Evidence Ledger

This ledger reconciles the exact fields required for implementation review.
`Verified repo-static` applies only to tracked files and deterministic validator
behavior; every provider runtime remains `Unverified live`.

| Provider | Official native path at cutoff | Local adapter inventory | Tracked settings / hook wiring | Model declaration | Project config | Validator coverage | Runtime evidence | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Claude Code | Project agents: `.claude/agents/*.md`; project settings and hooks: `.claude/settings.json` | Ten `.claude/agents/*.md` files | `.claude/settings.json` declares permissions and six Claude lifecycle event groups pointing to shared scripts | Supervisor `opus 4.8`; nine workers `sonnet 4.6`; declarations are not documented alias/full-ID syntax | Tracked native project settings exist | JSON/permission rules, hook phrases/payloads, stem/scope parity, and model/tools for 8 of 10 roles; `network-reviewer` and `observability-reviewer` are omitted from expected-field maps | No CLI version, settings load, agent discovery, hook invocation, model resolution, or inference canary | `Verified repo-static`; `Unverified live` |
| Codex | Project custom agents: `.codex/agents/*.toml`; layered project/user/managed configuration is `config.toml`; project hooks use `.codex/hooks.json` where supported/trusted | Ten `.codex/agents/*.toml` files | `.codex/hooks.json` declares six Claude-shaped event groups and shared-script commands; consumption is not observed | Supervisor `gpt-5.5`/`xhigh`; nine workers `gpt-5.3-codex` with `high` or `medium` | No tracked `.codex/config.toml`; user/managed overrides are not inspected | JSON/event/script checks, payload simulations, stem/scope parity, and model/effort for 8 of 10 roles; no provider load test | No CLI version, config precedence, hook trust/consumption, auth surface, resolved model, agent run, or inference canary | `Verified repo-static`; `Unverified live` |
| Gemini CLI | Project custom agents: `.gemini/agents/*.md`; workspace settings/hooks: `.gemini/settings.json` with Gemini events such as `BeforeTool`, `AfterTool`, `AfterAgent`, and `PreCompress` | Ten `.agents/agents/*.md` local/Antigravity reference adapters; **`.agents/agents` is not native Gemini CLI registration** | `.agents/hooks.json` uses Claude-style events; no tracked native `.gemini/settings.json` exists | Supervisor display label `Gemini 3.1 Pro`; nine workers `Gemini 3.5 Flash`; labels are not native resolution evidence | No tracked `.gemini/settings.json` or `.gemini/agents/` | JSON/event/script presence and 10-stem parity only; no Gemini metadata semantic comparison, native event/schema validation, or provider load test | No CLI version, native registry, policy/settings load, hook invocation, account/model resolution, subagent run, or inference canary | `Verified repo-static` for local adapters only; `Unverified live` and `Conditional` on a future native adapter |

### Native Surface and Local Adapter Matrix

| Capability | Claude official surface | Codex official surface | Gemini official surface | Local implementation | Verdict |
| --- | --- | --- | --- | --- | --- |
| Instruction/settings | Team settings use `.claude/settings.json`; `~/.claude.json` is separate global/session/MCP state. | `AGENTS.md` and layered `config.toml`; project layers require trust. | `GEMINI.md` plus workspace `.gemini/settings.json`. | Thin root gateways route to Stage 00 and provider runtime baselines. Claude settings is tracked; Codex config and Gemini settings are absent. | **Needs strengthening**: gateway declarations exist, but native config coverage differs. |
| Custom agents | Project agents are `.claude/agents/*.md`; YAML frontmatter supports model, tools, permission, MCP, hooks, effort, memory, and isolation. | Project agents are standalone `.codex/agents/*.toml`; model, effort, sandbox, MCP, and skills are supported. | Project agents are `.gemini/agents/*.md`, managed with `/agents` and `.gemini/settings.json`. | Ten Claude-native files, ten Codex-native files, and ten `.agents/agents/*.md` Antigravity/local adapters exist. No `.gemini/agents/` exists. | **Implementation gap** for Gemini CLI native registration; 30-file local stem parity is not three-runtime parity. |
| Model selection | Alias (`fable`, `opus`, `sonnet`, `haiku`) or full ID; availability varies by provider, version, account, and allowlist. | `/model`, `--model`, config, or per-agent model/effort; product and API availability are separate. | CLI `/model` Auto/manual selection; API model IDs and lifecycle are a separate catalog. | Local labels/IDs are declarations. Claude strings with spaces and Gemini display labels are not the documented concrete IDs; Codex IDs are concrete but lifecycle-drifted. | **Fact defect corrected**: no local label is promoted to verified provider resolution. |
| Tools and execution boundary | Agent `tools:` is an allowlist; project permissions and sandbox live in Claude settings. | Per-agent sandbox is supported; session sandbox/approval/config remains a separate control layer from hooks. | Agent `tools`/MCP fields and policy engine are native; settings govern approvals. | Claude has explicit tools and allow/deny rules. Codex relies on runtime sandbox outside the local agent TOML. `.agents` adapters omit native Gemini tools/policy fields. | **Needs strengthening**: shared prose is not identical least-privilege enforcement. |
| Hooks | Project hooks are in Claude settings and can block supported lifecycle events. | Trusted `.codex/hooks.json`/config hooks can block supported events, while sandbox and approval remain independent controls. | Native hooks are in `.gemini/settings.json` and use events such as `BeforeTool`/`AfterTool`; exit 2 can block. | Three tracked JSON surfaces name six Claude-style events and shared scripts. `.agents/hooks.json` is not the Gemini CLI native location or event schema. | **Implementation gap** for Gemini CLI; Codex local contract intentionally treats hooks as validation wiring, not a sandbox substitute. |
| Shared assets/MCP | Claude supports MCP and scoped subagent MCP; project servers use `.mcp.json`. | Codex supports per-agent and config-layer MCP. | Gemini agents support inline MCP and CLI MCP configuration. | `.agents/{skills,workflows,output-styles}` is the repo SSoT with Claude/Codex symlink views; no tracked `.mcp.json` or `.codex/config.toml`. | **Unverified** for active MCP connections; shared files prove repository reuse only. |
| Validation/evaluation | Native surfaces expose configuration, but repository-specific completion evidence remains local. | Model docs advise task-based reasoning; subagents add parallelism and cost. | API/CLI lifecycle and routing differ; Preview must be handled explicitly. | Repo-quality checks stems and selected fields; harness/static gates run outside provider inference. | **Needs strengthening**: add task evals and native canaries before any active migration. |

### Current Model Surface Matrix — 2026-07-10 10:00 KST

The `Lifecycle` column is surface-specific. Codex product recommendations and
deprecations are separate from OpenAI API catalog publication and endpoint
support; neither surface is used to infer the other. The required column
contract remains unchanged.

| Provider | Surface | Model/ID | Lifecycle | Role fit | Local assignment | Verdict | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude | Claude API + Claude Code | Claude Fable 5 / `claude-fable-5`; Code alias `fable`/`best` when available | Most capable widely released; API GA since 2026-06-09; Code requires supported version/access and has domain/account fallback caveats | Long-running, ambiguous, highest-value investigation or architecture escalation | None | **Unverified locally**: official capability is documented, but local availability and resolution were not tested. Use only as evaluated escalation. | [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview), [Claude Code model config](https://code.claude.com/docs/en/model-config) |
| Claude | Claude API + Claude Code | Claude Opus 4.8 / `claude-opus-4-8`; Code alias `opus` | Current widely released; official starting point for complex agentic coding | Supervisor, complex implementation, security/incident decision | Supervisor declares `opus 4.8` | **Implementation gap**: role fit remains sound, but the local spaced string is neither documented alias nor full ID. Evaluate supported syntax before migration. | [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview), [Subagents](https://code.claude.com/docs/en/sub-agents) |
| Claude | Claude API + Claude Code | Claude Sonnet 5 / `claude-sonnet-5`; Code alias `sonnet` | Current widely released; balanced speed/intelligence | Default worker for coding, review, docs, and tool use | Nine workers declare `sonnet 4.6` | **Implementation gap**: local worker generation trails the current model. Benchmark Sonnet 5 before changing the active owner. | [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview), [Model IDs](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions) |
| Claude | Claude API + Claude Code | Claude Haiku 4.5 / `claude-haiku-4-5-20251001`; alias `claude-haiku-4-5`/Code `haiku` | Current fastest tier | Simple/high-volume fallback and low-risk extraction | Allowed by model policy/catalog but assigned to no tracked adapter | **Needs strengthening**: fallback is policy text, not an exercised local assignment. | [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) |
| OpenAI | Codex product (ChatGPT desktop/web, CLI, IDE) | GPT-5.6 Sol / `gpt-5.6-sol` | General availability announced 2026-07-09 with a gradual global rollout; the announcement names Codex availability | Complex, open-ended coding, computer use, research, and cybersecurity | None | **Unverified locally**: the dated release is within the cutoff, but local version/account/model resolution was not tested. | [2026-07-09 launch announcement](https://openai.com/index/gpt-5-6/) |
| OpenAI | OpenAI API | GPT-5.6 Sol / `gpt-5.6-sol`; family alias behavior not assumed | General availability announced 2026-07-09; the announcement names API availability and gradual rollout | Complex professional reasoning/coding via API | None | **Unverified locally**: an official release announcement does not prove local API authentication, entitlement, endpoint resolution, or Codex product access. | [2026-07-09 launch announcement](https://openai.com/index/gpt-5-6/) |
| OpenAI | Codex product (ChatGPT desktop/web, CLI, IDE) | GPT-5.6 Terra / `gpt-5.6-terra` | General availability announced 2026-07-09 with Codex plan-dependent access and gradual rollout | Everyday work and migration evaluation candidate for prior GPT-5.5 tasks | None | **Unverified locally**: announced product availability is not active local state. | [2026-07-09 launch announcement](https://openai.com/index/gpt-5-6/) |
| OpenAI | OpenAI API | GPT-5.6 Terra / `gpt-5.6-terra` | General availability announced 2026-07-09; the announcement names API availability and gradual rollout | Intelligence/cost-balanced API workloads | None | **Unverified locally**: API authentication, entitlement, and model resolution were not canaried. | [2026-07-09 launch announcement](https://openai.com/index/gpt-5-6/) |
| OpenAI | Codex product (ChatGPT desktop/web, CLI, IDE) | GPT-5.6 Luna / `gpt-5.6-luna` | General availability announced 2026-07-09 with Codex plan-dependent access and gradual rollout | Clear, repeatable, high-volume extraction, classification, transformation, and structured summaries | None | **Unverified locally**: announced product availability requires local thresholds and a native canary. | [2026-07-09 launch announcement](https://openai.com/index/gpt-5-6/) |
| OpenAI | OpenAI API | GPT-5.6 Luna / `gpt-5.6-luna` | General availability announced 2026-07-09; the announcement names API availability and gradual rollout | Cost-sensitive, high-volume API workloads | None | **Unverified locally**: API authentication, entitlement, and model resolution were not canaried. | [2026-07-09 launch announcement](https://openai.com/index/gpt-5-6/) |
| OpenAI | Codex product | GPT-5.5 / `gpt-5.5` | Previous-generation | Existing supervisor; legacy complex work | Supervisor, `xhigh` | **Implementation gap**: locally coherent but no longer current recommended generation. Evaluate Sol before active migration. | [Codex models](https://developers.openai.com/codex/models) |
| OpenAI | Codex product | GPT-5.4 Mini / `gpt-5.4-mini` | Other current model; not listed as deprecated | Responsive coding tasks and subagents | None | **Needs strengthening**: viable focused-worker candidate, but not the current local policy and not a replacement without eval. | [Codex models](https://developers.openai.com/codex/models), [Subagents](https://developers.openai.com/codex/subagents) |
| OpenAI | Codex product with ChatGPT sign-in | GPT-5.3-Codex / `gpt-5.3-codex` | Deprecated on this authentication surface | Legacy agentic coding route; official page directs references to a latest listed model | Nine workers; `high` on seven implementation/review/security/incident roles and `medium` on docs/wiki | **Implementation gap, high risk**: if local Codex uses ChatGPT sign-in, the declared worker model is deprecated; auth mode remains unverified. | [Codex models](https://developers.openai.com/codex/models) |
| OpenAI | OpenAI API model page | GPT-5.3-Codex / `gpt-5.3-codex` | Dedicated API page is published and documents Responses/Chat Completions endpoints; the page does not label the API model deprecated | Agentic coding via an API-key workflow while the API page remains available | Same nine declarations; no adapter records authentication surface | **Unverified locally**: API publication is not Codex product support, and local API use was not tested. Preserve only as an auth-specific migration baseline. | [GPT-5.3-Codex API model](https://developers.openai.com/api/docs/models/gpt-5.3-codex) |
| Gemini | Gemini API | Gemini 3.1 Pro Preview / `gemini-3.1-pro-preview` | Preview | Complex reasoning, software engineering, precise multi-step/tool-use escalation | Supervisor declares `Gemini 3.1 Pro` | **Implementation gap**: local display label omits exact ID/lifecycle and Preview is not a stable default claim. CLI access is unverified. | [Model page](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview), [API models](https://ai.google.dev/gemini-api/docs/models) |
| Gemini | Gemini API | Gemini 3.5 Flash / `gemini-3.5-flash` | Stable/GA since 2026-05-19 | Sustained agentic/coding loops, default worker, everyday stable route | Nine workers declare `Gemini 3.5 Flash` | **Needs strengthening**: external role/lifecycle align, but local string and `.agents` adapter do not prove Gemini CLI resolution or registration. | [Model page](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash), [Release notes](https://ai.google.dev/gemini-api/docs/changelog) |
| Gemini | Gemini API | Gemini 3.1 Flash-Lite / `gemini-3.1-flash-lite` | Stable/GA since 2026-05-07 | Low-latency, high-volume extraction, classification, routing, and summarization fallback | None | **Needs strengthening**: evaluated fallback candidate only; no tracked adapter assignment or CLI availability evidence. | [Model page](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-lite), [Release notes](https://ai.google.dev/gemini-api/docs/changelog) |

### Per-Model Evaluation and Migration Matrix

This companion matrix has one row for each of the 13 required model families.
Disposition describes a proposed role in an evaluation, not an approved active
assignment. “Current baseline” means retain for comparison/rollback only while
its exact product or API surface remains supported; it is not a current-model
endorsement.

| Model | Default/escalation/fallback disposition | Supported effort or routing fact | Required evaluation | Exact canonical migration/follow-up route |
| --- | --- | --- | --- | --- |
| Claude Fable 5 | Escalation only for highest-value, ambiguous, long-running work; not local default or fallback. | Claude Code documents `fable`/`best` routing when available; the model overview says adaptive thinking is always on and does not publish a per-model effort range used by this audit. | Native alias/full-ID resolution, account/version availability, long-context/tool correctness, cost/latency, and fallback to Sonnet 5. | [Model Policy](../../../00.agent-governance/model-policy.md) → Claude provider/runtime owners → new Stage 03/04 model-migration spec/task with provider canary evidence. |
| Claude Opus 4.8 | Default candidate for supervisor/high-risk decisions; escalation from routine work; Sonnet 5 is the proposed lower-cost fallback. | Claude Code alias `opus` or full ID; official overview says `effort` defaults to `high` on the API, Claude Code, and claude.ai and may be set explicitly. | Exact local syntax load, complex coding/security/incident golden tasks, effort sweep, tool-call correctness, independent review, cost/latency, and rollback. | [Model Policy](../../../00.agent-governance/model-policy.md) → [Harness Catalog](../../../00.agent-governance/harness-catalog.md) → Claude provider/runtime owners → new Stage 03/04 migration spec/task. |
| Claude Sonnet 5 | Proposed default worker and fallback from Opus/Fable; not the highest-risk escalation. | Claude Code alias `sonnet` or full ID; official overview says `effort` defaults to `high` on the API and Claude Code and may be set explicitly. | Compare against all nine `sonnet 4.6` worker roles for patch/review quality, effort sweep, source fidelity, tool use, latency/cost, and rollback. | [Model Policy](../../../00.agent-governance/model-policy.md) → Claude provider/runtime owners → coordinated adapter/validator migration task. |
| Claude Haiku 4.5 | Fallback for bounded, low-risk, high-volume work; never an approval route for security/incident decisions. | Claude Code alias `haiku` or full ID; model overview lists extended thinking support and no adaptive thinking, but does not state a per-model effort range used here. | Extraction/classification exactness, schema validity, false-negative ceiling, escalation trigger to Sonnet 5, throughput, and cost. | [Model Policy](../../../00.agent-governance/model-policy.md) → Claude provider/runtime owners → WERH-008 routing analysis → separately approved fallback canary task. |
| GPT-5.6 Sol | Proposed default for ambiguous/high-value Codex work and escalation from Terra; Terra is fallback when its quality threshold passes. | The dated launch announcement documents selectable effort and a `max` setting in Codex. Exact per-surface enums and local availability are not inferred. | Product and API canaries separately; local auth/version/model resolution; complex task quality; effort sweep; cost/latency; rollback from GPT-5.5. | [Model Policy](../../../00.agent-governance/model-policy.md) → Codex provider/runtime owners → new Stage 03/04 auth-surface-specific migration spec/task. |
| GPT-5.6 Terra | Proposed default for routine implementation/review and fallback from Sol; escalation to Sol. | The dated launch announcement describes Terra as a balanced lower-cost route and documents selectable effort in Codex; no exact GPT-5.5 mapping is assumed. | Compare representative supervisor/worker tasks against GPT-5.5 and GPT-5.3-Codex; effort sweep, false-negative review rate, cost/latency, and rollback. | [Model Policy](../../../00.agent-governance/model-policy.md) → Codex provider/runtime owners → coordinated adapter/validator migration task after auth inventory. |
| GPT-5.6 Luna | Fallback/default only for clear, repeatable, high-volume work; escalate to Terra or Sol when thresholds fail. | The dated launch announcement describes Luna as the fastest/lowest-cost family route and documents selectable effort in Codex; local route resolution is Unverified. | Exact-match/schema validity, sampled precision/recall, retry/escalation rate, tool correctness, throughput, and cost ceiling. | [Model Policy](../../../00.agent-governance/model-policy.md) → Codex provider/runtime owners → WERH-008 routing analysis → bounded-worker canary task. |
| GPT-5.5 | Current local supervisor baseline and rollback candidate only; proposed migration escalation is Sol and routine fallback candidate is Terra. | Local adapter declares `xhigh`; Codex product calls GPT-5.5 previous-generation and gives no exact GPT-5.5-to-GPT-5.6 effort mapping. | Re-run supervisor golden tasks against Sol/Terra at several efforts; compare judgment, tools, latency/cost, and verify rollback. | [Model Policy](../../../00.agent-governance/model-policy.md) → Codex provider/runtime owners → new supervisor migration spec/task. |
| GPT-5.4 Mini | Proposed focused-subagent or responsive-work fallback; not default for high-risk judgment; escalate to Terra/Sol. | Codex product documents the model route for responsive coding/subagents; a per-model supported-effort range is not published on that cited row, so it remains unknown here. | Focused implementation/review quality, tool behavior, false-negative rate, parallel-worker economics, escalation trigger, and rollback. | [Model Policy](../../../00.agent-governance/model-policy.md) → [Subagent Protocol](../../../00.agent-governance/subagent-protocol.md) → Codex provider/runtime owners → bounded-subagent canary task. |
| GPT-5.3-Codex | Current worker baseline only. ChatGPT-sign-in Codex must migrate; an API-key fallback is considered only if API availability and auth intent are proven. | API page supports `low`, `medium`, `high`, `xhigh`; Codex product deprecates this ID for ChatGPT sign-in. No lifecycle inference crosses those surfaces. | Non-secret auth-surface inventory; product/API canaries separately; compare seven `high` and two `medium` roles against Terra/Sol/5.4 Mini; rollback on a supported surface only. | [Model Policy](../../../00.agent-governance/model-policy.md) → Codex provider/runtime owners → new Stage 03/04 auth inventory and migration spec/task; evidence in a Stage 04 provider canary. |
| Gemini 3.1 Pro Preview | Escalation only for complex reasoning/tool work; not stable default or fallback. | Gemini API lifecycle is Preview; no provider-equivalent reasoning-effort range is published on the cited model page, and Gemini CLI routing remains a separate unknown surface. | Preview acceptance, exact API ID, CLI/account resolution separately, complex-task gain over 3.5 Flash, tool correctness, quota/latency, fallback. | [Model Policy](../../../00.agent-governance/model-policy.md) → [Gemini provider notes](../../../00.agent-governance/providers/gemini.md) → WERH-008 routing analysis → native canary task. |
| Gemini 3.5 Flash | Proposed stable default worker and fallback from Pro Preview; escalate to Pro Preview only with explicit lifecycle acceptance. | Gemini API marks the ID Stable; no cross-surface CLI availability or reasoning-effort range is inferred. | All nine worker-role golden tasks, exact-ID and native-agent discovery, source/tool quality, cost/latency, and rollback. | [Model Policy](../../../00.agent-governance/model-policy.md) → Gemini provider/runtime owners → WERH-008 routing analysis → native adapter/model canary task. |
| Gemini 3.1 Flash-Lite | Fallback/default only for bounded extraction, classification, routing, and summaries; escalate to 3.5 Flash on threshold failure. | Gemini API marks the ID Stable; no Gemini CLI route or reasoning-effort analogue is claimed. | Exact-match/schema validity, sampled precision/recall, escalation/termination behavior, quota/latency, and cost ceiling. | [Model Policy](../../../00.agent-governance/model-policy.md) → Gemini provider/runtime owners → WERH-008 routing analysis → bounded-fallback canary task. |

The official Gemini CLI model page still lists its Auto (Gemini 3) pool as
`gemini-3-pro-preview` and `gemini-3-flash-preview`, while the API catalog at
the cutoff lists newer lifecycle states. The CLI page also carries an
account-tier notice that unpaid-tier and Google One users were scheduled to move
to Antigravity CLI on 2026-06-18. This documentation divergence is why API
stability is not used to claim a particular CLI/account model route; an approved
native canary must record the installed version, auth/account surface without
secrets, and the model actually resolved.

### Task-Characteristic Model Recommendation

These are migration hypotheses, not active assignments. “Fallback” may mean a
smaller model or deterministic tooling when correctness is better protected by
schema/validator execution. Every route requires provider-auth/version checks and
task-specific eval before changing Stage 00 owners or adapters.

| Task profile | Claude default/escalation/fallback | Codex default/escalation/fallback | Gemini default/escalation/fallback | Effort/routing | Eval required |
| --- | --- | --- | --- | --- | --- |
| Ambiguous architecture or long-running multi-agent work | Opus 4.8 / Fable 5 / Sonnet 5 | Sol medium / Sol high or max / Terra | Stable 3.5 Flash / 3.1 Pro Preview / 3.1 Flash-Lite for bounded preprocessing only | Begin at the provider default or medium for planning; increase Sol effort only when eval evidence justifies the cost. `max` is a single-model effort setting, not agent orchestration. | Golden architecture decisions, long-context retention, tool-call correctness, cost/latency, and fallback behavior. |
| Routine implementation and code/GitOps review | Sonnet 5 / Opus 4.8 / Haiku 4.5 for simple scans | Terra / Sol / GPT-5.4 Mini or Luna by quality threshold | 3.5 Flash / 3.1 Pro Preview / 3.1 Flash-Lite | Use the lowest effort that passes build/static/review acceptance; separate write and independent review roles. | Representative edit/review tasks, false-negative review rate, patch correctness, token/time budget, and repo gates. |
| Security, incident, or high-risk governance judgment | Opus 4.8 / Fable 5 where domain access permits / Sonnet 5 as second-pass worker | Sol high / Sol max plus independent reviewer / Terra as evidence collector | 3.5 Flash stable / 3.1 Pro Preview with explicit lifecycle acceptance / Flash-Lite only for extraction | Never treat smaller fallback output as approval; `max` adds single-model reasoning time, while independent review remains a separate control. | Severity calibration, missed-critical findings, evidence citation, refusal/fallback behavior, and human approval outcome. |
| Documentation, research, taxonomy, and synthesis | Sonnet 5 / Opus 4.8 / Haiku 4.5 | Terra / Sol / Luna or GPT-5.4 Mini | 3.5 Flash / 3.1 Pro Preview / 3.1 Flash-Lite | Medium/default effort; escalate for conflicting sources or cross-document architecture, not volume alone. | Source fidelity, unsupported-claim rate, link accuracy, template conformance, Korean clarity, and cost. |
| High-volume deterministic extraction/classification | Haiku 4.5 / Sonnet 5 / deterministic parser | Luna or GPT-5.4 Mini / Terra / deterministic parser | 3.1 Flash-Lite / 3.5 Flash / deterministic parser | Prefer schema-constrained output and validators; retry budget and human sample review must be explicit. | Exact-match/schema validity, sampled precision/recall, retry/termination rate, throughput, and cost ceiling. |
| Active model-policy or adapter migration | Current active assignment / one evaluated candidate / rollback to current assignment | Current active assignment / one evaluated candidate / rollback to current assignment | Current active assignment / one exact-ID candidate / rollback to current assignment | Change canonical policy first, then all affected adapters/validators in one separately approved task; preserve auth-surface distinctions. | Native canary on supported CLI/account, adapter parse/load, representative tasks, regression comparison, rollback rehearsal, and reviewer approval. |

### Provider Gap Register

| Finding | Evidence | Risk | Recommendation | Canonical follow-up route |
| --- | --- | --- | --- | --- |
| **Fact defect — stale Current provider claims** | The prior Current text used `.claude.json` for project settings, reduced Gemini CLI to scripted delegation, named `.agents/hooks.json` as native Gemini wiring, claimed an observability scope that does not exist, and said Claude binds `validate-harness.sh` directly. The active harness catalog also says `Eight`/`eight` although ten role stems exist. | **High**: readers could edit the wrong surface, infer controls that are absent, or undercount the roster. This reference corrects the facts; active files remain unchanged. | Preserve the corrected native/local split and 10-role/30-adapter count; route active catalog wording through a separate Stage 00 change. | WERH-009 pack integration, [harness-catalog.md](../../../00.agent-governance/harness-catalog.md), and the [reference maintenance runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md). |
| **Implementation gap — Claude adapter model syntax/currentness** | Official agent frontmatter accepts aliases or full IDs; local files use `opus 4.8`/`sonnet 4.6`. Sonnet 5 is current and Opus 4.8 remains recommended for complex agentic coding. | **High**: direct Claude Code resolution is unverified, and worker currentness has drifted. | In a separate approved model migration, canary exact alias/ID syntax and benchmark Sonnet 5 before changing policy and all adapters. | [model-policy.md](../../../00.agent-governance/model-policy.md), [harness-catalog.md](../../../00.agent-governance/harness-catalog.md), Claude provider/runtime owners. |
| **Implementation gap — Codex lifecycle and auth-surface drift** | Local supervisor uses previous-generation GPT-5.5; all workers use `gpt-5.3-codex`, deprecated for ChatGPT-sign-in Codex but still exposed by the API page. | **High**: auth-dependent failure or silent fallback can invalidate routing and eval assumptions. | Inventory the intended authentication surface without reading credentials, then evaluate Sol/Terra/Luna and GPT-5.4 Mini per role before a coordinated migration. | [model-policy.md](../../../00.agent-governance/model-policy.md), Codex provider/runtime owners, and a new Stage 03/04 migration spec/task. |
| **Implementation gap — Gemini CLI native adapter/settings mismatch** | Official custom agents live in `.gemini/agents/*.md`; native hooks/settings live in `.gemini/settings.json` with Gemini event names. The repo has `.agents/agents/*.md` and `.agents/hooks.json` only. | **High**: Antigravity/local files may be mistaken for Gemini CLI registration and blocking enforcement. | Decide whether Gemini CLI is an intended runtime; if yes, design the smallest native adapter/settings layer and native-schema validator in a separate approved task. | Gemini provider/runtime owners, [harness-catalog.md](../../../00.agent-governance/harness-catalog.md), and a new Stage 03/04 adapter spec/task. |
| **Needs strengthening — Gemini model lifecycle declarations** | Local `Gemini 3.1 Pro` and `Gemini 3.5 Flash` omit exact IDs and Preview/Stable states; no Flash-Lite assignment exists. CLI model docs and API catalog are not lifecycle-identical. | **High** for a Preview supervisor default; account/version routing may differ from the API. | Keep 3.5 Flash as the stable evaluation baseline, treat 3.1 Pro Preview as explicit escalation, and test Flash-Lite as a bounded fallback. | [model-policy.md](../../../00.agent-governance/model-policy.md), Gemini provider notes, and Task 8 routing analysis. |
| **Needs strengthening — semantic parity validator coverage** | Stem sets are exact, but expected model/tool maps omit two roles, Gemini fields are not semantically compared, and no native schema/load test runs. | **Medium-High**: field drift can pass while all 30 filenames remain present. | Extend coverage only in a separately approved validator task: all ten roles, provider-native required fields, exact scopes, and native canary evidence separated from static checks. | `scripts/validate-repo-quality-gates.sh`, [harness-catalog.md](../../../00.agent-governance/harness-catalog.md), and a Stage 04 validator task. |
| **Needs strengthening — Codex global agent defaults are implicit** | Standalone `.codex/agents/*.toml` is official; tracked `.codex/config.toml` is absent, so documented defaults are 6 threads and depth 1 unless another layer overrides them. | **Medium**: concurrency/depth can vary via user/managed config and is not reproducible from the repo alone. | Record desired project limits only if a separate design finds reproducibility necessary; do not add config in this research task. | Codex provider/runtime owners and [subagent protocol](../../../00.agent-governance/subagent-protocol.md). |
| **Unverified — native/runtime/account behavior** | No provider CLI version, login/account entitlement, hook trust panel, agent registry, model picker, inference, or MCP connection was inspected. | **Medium-High**: repo-static PASS cannot establish provider readiness or model execution. | Before any migration, run approved read-only native canaries that record version, auth mode without secrets, resolved model, agent discovery, hook trust/consumption, and rollback evidence. | A new Stage 04 provider canary task; evidence belongs in the task, not this reference. |

### Interpretation

The common environment is real at the repository contract level: thin gateways,
Stage 00 governance, a shared `.agents` asset SSoT, shared hook scripts, task
evidence, and repo-static validators. It is not a single provider-native runtime.
Claude, Codex, and Gemini each require their own exact agent/settings schema,
permission boundary, trust model, lifecycle interpretation, and canary evidence.

The safe migration order is evidence-first: select representative task evals,
verify the intended product/auth/account/CLI surface, test one candidate against
the current assignment, update canonical model policy, update every affected
adapter and validator together, then retain a rollback route. A new model name in
an API catalog alone is insufficient migration evidence.

## Sources

All external sources below were checked read-only at `2026-07-10 10:00 KST`.
Later page changes require a new, explicitly dated snapshot and are not silently
inserted into this one.

### Official Provider Sources

Claude/Anthropic:

- Models overview: <https://platform.claude.com/docs/en/about-claude/models/overview>
- Model IDs and versioning: <https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions>
- Model deprecations: <https://platform.claude.com/docs/en/about-claude/model-deprecations>
- Claude Code model configuration: <https://code.claude.com/docs/en/model-config>
- Claude Code subagents: <https://code.claude.com/docs/en/sub-agents>
- Claude Code hooks: <https://code.claude.com/docs/en/hooks>
- Claude Code permissions: <https://code.claude.com/docs/en/permissions>
- Claude Code sandboxing: <https://code.claude.com/docs/en/sandboxing>
- Claude Code settings: <https://code.claude.com/docs/en/configuration>

OpenAI/Codex:

- GPT-5.6 preview announcement (2026-06-26): <https://openai.com/index/previewing-gpt-5-6-sol/>
- GPT-5.6 general-availability announcement (2026-07-09): <https://openai.com/index/gpt-5-6/>
- Codex models: <https://developers.openai.com/codex/models>
- Codex subagents: <https://developers.openai.com/codex/subagents>
- Codex configuration reference: <https://developers.openai.com/codex/config-reference>
- Codex hooks: <https://developers.openai.com/codex/hooks>
- OpenAI API models: <https://developers.openai.com/api/docs/models>
- GPT-5.3-Codex API model page: <https://developers.openai.com/api/docs/models/gpt-5.3-codex>

Google/Gemini:

- Gemini API models: <https://ai.google.dev/gemini-api/docs/models>
- Gemini API release notes: <https://ai.google.dev/gemini-api/docs/changelog>
- Gemini 3.1 Pro Preview: <https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview>
- Gemini 3.5 Flash: <https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash>
- Gemini 3.1 Flash-Lite: <https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-lite>
- Gemini CLI model selection: <https://geminicli.com/docs/cli/model/>
- Gemini CLI subagents: <https://geminicli.com/docs/core/subagents/>
- Gemini CLI hooks: <https://geminicli.com/docs/hooks/>
- Gemini CLI policy engine: <https://geminicli.com/docs/reference/policy-engine/>
- Gemini CLI settings: <https://geminicli.com/docs/cli/settings/>

### Repo Sources

- Root gateways: [AGENTS.md](../../../../AGENTS.md),
  [CLAUDE.md](../../../../CLAUDE.md), and [GEMINI.md](../../../../GEMINI.md)
- Runtime baselines: [Claude](../../../../.claude/CLAUDE.md),
  [Codex](../../../../.codex/CODEX.md), and
  [Gemini/Antigravity](../../../../.agents/GEMINI.md)
- Provider notes: [Claude](../../../00.agent-governance/providers/claude.md),
  [Codex](../../../00.agent-governance/providers/codex.md), and
  [Gemini](../../../00.agent-governance/providers/gemini.md)
- Active owners: [Model Policy](../../../00.agent-governance/model-policy.md),
  [Harness Catalog](../../../00.agent-governance/harness-catalog.md), and
  [Harness Implementation Map](../../../00.agent-governance/harness-implementation-map.md)
- Tracked settings/hook wiring:
  [.claude/settings.json](../../../../.claude/settings.json),
  [.codex/hooks.json](../../../../.codex/hooks.json), and
  [.agents/hooks.json](../../../../.agents/hooks.json)
- Adapter sets: `.claude/agents/*.md`, `.codex/agents/*.toml`, and
  `.agents/agents/*.md`
- Validator: `scripts/validate-repo-quality-gates.sh`
- Earlier dated synthesis integrated after re-verification:
  [2026-07-04 provider reference](../2026-07-04-wer/provider-implementation-status.md)

Market scan: none used as authority for provider capability, model lifecycle, or
local implementation in this document.

## Review and Freshness

- Review cadence: on provider model/lifecycle, coding-product auth, CLI/schema,
  hook semantics, local adapter/model-policy, or validator change.
- Last reviewed: `2026-07-10 10:00 KST`
- Next review trigger: any official model catalog/deprecation update; Claude Code,
  Codex, or Gemini CLI release affecting agent/model/hook/settings behavior; an
  account/auth surface change; or any edit to the 30 adapters, three hook/settings
  JSON files, model policy, harness catalog, or validator.
- Refresh method: re-open the exact official URLs, record the new timestamp,
  re-count and parse local files, preserve API/product/CLI/local separation, and
  rerun approved static plus native-canary evidence lanes independently.

## Related Documents

- **Current pack README**: [README.md](README.md)
- **References README**: [../../README.md](../../README.md)
- **Workspace baseline**: [workspace-governance-baseline.md](workspace-governance-baseline.md)
- **Harness reference**: [harness-and-loop-engineering.md](harness-and-loop-engineering.md)
- **AI agent routing**: [ai-agents-roster-and-gap-analysis.md](ai-agents-roster-and-gap-analysis.md)
- **Model Policy**: [../../../00.agent-governance/model-policy.md](../../../00.agent-governance/model-policy.md)
- **Harness Catalog**: [../../../00.agent-governance/harness-catalog.md](../../../00.agent-governance/harness-catalog.md)
- **Current hardening task**: [../../../04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md](../../../04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md)
