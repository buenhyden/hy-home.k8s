---
title: 'Reference: AI Agents Roster and Gap Analysis Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-10
---

# Reference: AI Agents Roster and Gap Analysis Research

## Overview

이 문서는 `hy-home.k8s`의 10개 역할과 Claude, Codex, `.agents` 로컬 어댑터
30개를 현재 리포지토리 증적으로 전수 감사하고, 외부
`msitarzewski/agency-agents` 카탈로그와 비교한다. 외부 카탈로그는 역할 발굴과
포맷 비교를 위한 비권위적 market scan이며 로컬 로스터나 모델 정책을 지배하지
않는다.

외부 소스 컷오프는 `2026-07-10 10:00 KST`다. `agency-agents`는 이 시각보다
앞선 마지막 `main` commit인
`9f3e401ccd09aa0ee0ef8e015226d0647908e01e`에 고정했다. 모델 라우팅은 같은
컷오프의 공식 공급자 문서와
[provider implementation reference](provider-implementation-status.md)를 사용한다.
이 문서는 활성 에이전트, 모델, 정책, validator 또는 provider 설정을 변경하지
않는다.

## Purpose

- 10개 로컬 역할과 세 어댑터의 model, tools, scope, guardrail, handoff,
  postflight, sandbox/effort 선언을 실제 파일 기준으로 기록한다.
- 파일 stem 일치와 provider-native 등록·권한·행동 동등성을 구분한다.
- 고정 revision의 외부 division, 파일 수, frontmatter, 변환·설치 표면을
  재현 가능한 방식으로 기록한다.
- 외부 역할 패턴을 `Closed`, `Adapt`, `Skip`, `Candidate`로 판정하고 모든
  권고를 canonical 후속 경로로 연결한다.
- 역할별 default/escalation/fallback 모델 가설과 eval gate를 기록하되 활성
  모델 정책이나 어댑터에는 적용하지 않는다.

## Reference Type

- Type: dated-implementation-audit / external-standard-snapshot
- Source checked: `2026-07-10 10:00 KST`
- Repo evidence checked: `2026-07-10`
- Upstream pin: `9f3e401ccd09aa0ee0ef8e015226d0647908e01e`
- Refresh trigger: local roster/adapter/model-policy/validator change, upstream
  revision/tag/release/format change, or official provider model/subagent lifecycle
  change.

## Authority Boundary

- **Authoritative for**: 이 checkout에서 확인한 10개 역할, 30개 파일, 선언 필드,
  validator 범위와 고정 upstream revision의 재현 가능한 snapshot.
- **Not authoritative for**: 활성 로스터·모델 정책, provider-native 등록 성공,
  모델 entitlement, inference 품질, hook/tool enforcement, live cluster 또는
  remote readiness.
- 활성 roster와 tier는
  [harness-catalog.md](../../../00.agent-governance/harness-catalog.md)와
  [model-policy.md](../../../00.agent-governance/model-policy.md)가 지배한다. 역할
  본문은 세 adapter set, 공통 위임 계약은
  [subagent-protocol.md](../../../00.agent-governance/subagent-protocol.md)가 지배한다.
- 공급자 기능과 모델 수명주기는 해당 공식 문서가 지배한다. upstream market
  scan과 이 문서의 라우팅 가설은 활성 owner를 덮어쓰지 않는다.

## Scope

- `.claude/agents/*.md`, `.codex/agents/*.toml`, `.agents/agents/*.md`의 10개
  공통 stem과 `scripts/validate-repo-quality-gates.sh`의 adapter 검사.
- `agency-agents`의 17개 division, Markdown inventory, lint contract,
  `tools.json`, `convert.sh`, license, tag/release 상태.
- Claude, Codex, Gemini의 공식 subagent/native path 및 같은 컷오프의 모델
  라우팅 사실.
- Historical `2026-07-04-wer`의 유효한 계약 비교와 gap lineage를 현재 증적으로
  재검증해 통합.
- 활성 agent, policy, model, provider config, script, template, CI, manifest,
  credential, live runtime, remote state 변경은 제외.

## Definitions / Facts

### Evidence Rules

| Evidence class | Meaning | Boundary |
| --- | --- | --- |
| Repo fact | Tracked adapter, governance owner, validator code, or deterministic file scan. | Declaration and static coverage only; not provider loading or behavior. |
| Fixed upstream fact | Content reachable at the pinned commit SHA. | Reproducible snapshot; not current `main` after the cutoff. |
| Official provider fact | Provider model/subagent documentation checked at the cutoff. | Product/API/CLI/account surfaces remain separate. |
| Interpretation | Explicit comparison of the above evidence. | Must not be promoted to active policy. |
| Recommendation | Non-mutating follow-up with an owner and eval gate. | Requires a separate approved Stage 03/04 change. |

### Local Roster and Shared Body Contract

The three directories each contain exactly ten files with the same stems:
`code-reviewer`, `doc-writer`, `gitops-reviewer`, `incident-responder`,
`k8s-implementer`, `network-reviewer`, `observability-reviewer`,
`security-auditor`, `supervisor`, and `wiki-curator`. This proves
`10 roles x 3 adapter surfaces = 30 files`.

All 30 bodies carry `Runtime Bootstrap`, `Role`, `When to Use`, `Inputs`,
`Outputs`, `Guardrails`, `Handoff / Escalation`, and `Postflight`; every role
routes postflight to `rules/postflight-checklist.md`. Scope imports are
architecture for code review, docs for doc/wiki, meta for supervisor, security
for the security auditor, ops plus infra for incident response, and infra for
GitOps/Kubernetes/network/observability. In particular, all three
`observability-reviewer` files import `scopes/infra.md`; there is no local
`scopes/observability.md` contract.

Stem and body parity are useful repository contracts, but they are not proof
that all three providers discover the files, interpret metadata identically,
enforce the same tools, or produce equivalent output.

### Provider-Native Adapter Status

| Role | Claude | Codex | Gemini | Native/local distinction | Validation coverage | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `supervisor` | `.claude/agents/supervisor.md`; `opus 4.8`; `Read, Grep, Glob, Bash, Edit, Write, Task`; meta scope | `.codex/agents/supervisor.toml`; `gpt-5.5`; `xhigh`; no per-agent `tools`/`sandbox_mode` | `.agents/agents/supervisor.md`; `Gemini 3.1 Pro`; no `tools`/effort/sandbox field | Claude Markdown and Codex TOML use official project-agent paths. `.agents` is the Antigravity/local surface; Gemini CLI native path is `.gemini/agents/`. | Stem, Claude/Codex runtime phrases and scope parity, exact Claude model/tools and Codex model/effort. Gemini semantic fields are not compared. | Needs strengthening: file parity exists; native Gemini registration and current model resolution are unverified. |
| `code-reviewer` | `.claude/agents/code-reviewer.md`; `sonnet 4.6`; read-only tools; architecture scope | `.codex/agents/code-reviewer.toml`; `gpt-5.3-codex`; `high` | `.agents/agents/code-reviewer.md`; `Gemini 3.5 Flash` | Same native/local distinction; Claude `tools:` has no cross-provider equivalent in these files. | Stem, body phrases, Claude/Codex scope, and exact selected model/tool/effort fields; no Gemini semantic comparison. | Needs strengthening: contract-shaped parity, not native behavior parity. |
| `doc-writer` | `.claude/agents/doc-writer.md`; `sonnet 4.6`; write tools; docs scope | `.codex/agents/doc-writer.toml`; `gpt-5.3-codex`; `medium` | `.agents/agents/doc-writer.md`; `Gemini 3.5 Flash` | Same native/local distinction; editing authority remains task delegation, not the presence of write tools. | Stem, body phrases, Claude/Codex scope, exact selected fields, plus separate document-routing checks; no Gemini semantic comparison. | Needs strengthening: static contract is strong, native loading and behavioral parity are unverified. |
| `gitops-reviewer` | `.claude/agents/gitops-reviewer.md`; `sonnet 4.6`; read-only tools; infra scope | `.codex/agents/gitops-reviewer.toml`; `gpt-5.3-codex`; `high` | `.agents/agents/gitops-reviewer.md`; `Gemini 3.5 Flash` | Same native/local distinction; all bodies are review-only and GitOps-first. | Stem, body phrases, Claude/Codex scope, exact selected fields; no Gemini semantic comparison. | Needs strengthening: no provider inference or GitOps judgment eval ran. |
| `incident-responder` | `.claude/agents/incident-responder.md`; `sonnet 4.6`; read-only tools; ops+infra scopes | `.codex/agents/incident-responder.toml`; `gpt-5.3-codex`; `high` | `.agents/agents/incident-responder.md`; `Gemini 3.5 Flash` | Same native/local distinction; two scope imports are preserved in every file. | Stem, body phrases, exact Claude/Codex scopes and selected fields; no Gemini semantic comparison. | Needs strengthening: incident synthesis and escalation quality require role evals. |
| `k8s-implementer` | `.claude/agents/k8s-implementer.md`; `sonnet 4.6`; write tools; infra scope | `.codex/agents/k8s-implementer.toml`; `gpt-5.3-codex`; `high` | `.agents/agents/k8s-implementer.md`; `Gemini 3.5 Flash` | Same native/local distinction; write capability is bounded by GitOps-first guardrails and outer sandbox/approval. | Stem, body phrases, Claude/Codex scope and exact selected fields; no Gemini semantic comparison. | Needs strengthening: no native tool-boundary or manifest-generation eval ran. |
| `network-reviewer` | `.claude/agents/network-reviewer.md`; `sonnet 4.6`; read-only tools; infra scope | `.codex/agents/network-reviewer.toml`; `gpt-5.3-codex`; `high` | `.agents/agents/network-reviewer.md`; `Gemini 3.5 Flash` | Same native/local distinction; body explicitly forbids live probing. | Stem, body phrases, and Claude/Codex scope parity only. Validator expected-field maps omit this role; Gemini semantics are not compared. | Implementation gap: adapter exists, but exact model/tool/effort regression coverage is incomplete. |
| `observability-reviewer` | `.claude/agents/observability-reviewer.md`; `sonnet 4.6`; read-only tools; infra scope | `.codex/agents/observability-reviewer.toml`; `gpt-5.3-codex`; `high` | `.agents/agents/observability-reviewer.md`; `Gemini 3.5 Flash` | Same native/local distinction; body explicitly limits review to manifests and SLO docs. | Stem, body phrases, and Claude/Codex scope parity only. Validator expected-field maps omit this role; Gemini semantics are not compared. | Implementation gap: adapter exists, but exact model/tool/effort regression coverage is incomplete. |
| `security-auditor` | `.claude/agents/security-auditor.md`; `sonnet 4.6`; read-only tools; security scope | `.codex/agents/security-auditor.toml`; `gpt-5.3-codex`; `high` | `.agents/agents/security-auditor.md`; `Gemini 3.5 Flash` | Same native/local distinction; smaller-model output cannot authorize risky action. | Stem, body phrases, Claude/Codex scope and exact selected fields; no Gemini semantic comparison. | Needs strengthening: static shape cannot establish missed-critical rate or native enforcement. |
| `wiki-curator` | `.claude/agents/wiki-curator.md`; `sonnet 4.6`; write tools; docs scope | `.codex/agents/wiki-curator.toml`; `gpt-5.3-codex`; `medium` | `.agents/agents/wiki-curator.md`; `Gemini 3.5 Flash` | Same native/local distinction; canonical-owner and no-vector-store boundaries are explicit. | Stem, body phrases, Claude/Codex scope, exact selected fields, and special wiki guardrail phrases; no Gemini semantic comparison. | Needs strengthening: repository guardrails are validated more deeply than provider-native behavior. |

The validator enforces identical stem sets, required runtime phrases for Claude
and Codex, Claude/Codex scope equality, selected exact Claude model/tools and
Codex model/effort values, TOML parsing, and catalog registration. Its exact
model/tool/effort maps cover eight roles and omit `network-reviewer` and
`observability-reviewer`; it checks Gemini stem presence but does not parse or
semantically compare the `.agents` bodies/frontmatter. No native provider
agent-list, schema-load, model-resolution, tool-enforcement, or inference canary
ran.

### Upstream Snapshot — 2026-07-10

| Claim | Verified value | Evidence | Authority limitation |
| --- | --- | --- | --- |
| Revision at cutoff | `9f3e401ccd09aa0ee0ef8e015226d0647908e01e`, committed `2026-07-10 05:32:59 KST`; last `main` commit before the cutoff | [Pinned commit](https://github.com/msitarzewski/agency-agents/commit/9f3e401ccd09aa0ee0ef8e015226d0647908e01e) | Later `main` changes are outside this snapshot. |
| License and releases | MIT; repository tags `0`, releases `0` at check time | [Pinned LICENSE](https://raw.githubusercontent.com/msitarzewski/agency-agents/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/LICENSE), GitHub tag/release APIs | No version tag exists to use as a semantic release baseline. |
| Division registry | 17: academic, design, engineering, finance, game-development, gis, healthcare, marketing, paid-media, product, project-management, sales, security, spatial-computing, specialized, support, testing | [Pinned `divisions.json`](https://raw.githubusercontent.com/msitarzewski/agency-agents/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/divisions.json) | Top-level integrations, strategy, examples, and scripts are not divisions. |
| Agent Markdown inventory | Recursive division count `254`; direct-child-only count `239`; 15 nested game-development files explain the difference | [Pinned recursive tree](https://api.github.com/repos/msitarzewski/agency-agents/git/trees/9f3e401ccd09aa0ee0ef8e015226d0647908e01e?recursive=1) | Counts include `.md` blobs only under the 17 registered divisions. The Git tree response was not truncated. |
| Division counts | academic 6; design 9; engineering 49; finance 5; game-development 20; gis 13; healthcare 3; marketing 36; paid-media 7; product 5; project-management 7; sales 9; security 10; spatial-computing 6; specialized 54; support 6; testing 9 | Same pinned recursive tree grouped by the first path segment | A future tree or registry change requires a recount. |
| README count | `230+` is upstream self-description; the fixed-SHA recursive count is 254. The old Current value `147+` is replaced. | [Pinned README](https://raw.githubusercontent.com/msitarzewski/agency-agents/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/README.md) and pinned tree | Marketing text is non-authoritative for inventory; do not use it as the reproducible count. |
| Required source frontmatter | `name`, `description`, `color` are required errors; `emoji` and `vibe` are optional source extensions | [Pinned linter](https://raw.githubusercontent.com/msitarzewski/agency-agents/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/scripts%2Flint-agents.sh), [pinned SRE sample](https://raw.githubusercontent.com/msitarzewski/agency-agents/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/engineering/engineering-sre.md) | Recommended persona sections are warnings, not the local governance contract. |
| Common model/tool contract | No required common `model`, reasoning/effort, scope, guardrail, handoff, postflight, or minimum-tool contract. Optional source `tools` is consumed only by Qwen conversion. | Pinned linter and [pinned converter](https://raw.githubusercontent.com/msitarzewski/agency-agents/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/scripts%2Fconvert.sh) | Absence is a format fact, not evidence that upstream agents can execute arbitrary tools in every host. Host policy remains separate. |
| Install targets | `tools.json` registers 15: 12 per-agent targets, two roster targets, and one plugin target | [Pinned `tools.json`](https://raw.githubusercontent.com/msitarzewski/agency-agents/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/tools.json) | Target registration does not prove every installed host/version works. |
| Conversion targets | `convert.sh --tool all` generates 13 targets. Claude Code and Copilot are `identity` copy targets in `tools.json` and need no generated conversion. | Pinned converter and `tools.json` | Conversion shape is not semantic equivalence across providers. |
| Codex/Gemini conversion output | Codex output has only `name`, `description`, `developer_instructions`; Gemini CLI output has only `name`, `description`, body under `.gemini/agents/*.md` | Pinned converter | Neither output injects local model, Codex effort/sandbox, Gemini tools/MCP, Stage 00 scope, guardrails, handoff, or postflight. |
| Gemini path distinction | Upstream Gemini CLI target is `.gemini/agents/*.md`; local role adapters are `.agents/agents/*.md` | Pinned `tools.json`, [official Gemini subagents](https://geminicli.com/docs/core/subagents/), and repo paths | Similar Markdown bodies do not make `.agents` a Gemini CLI native registry. |

Reproduction method: take the keys of pinned `divisions.json`, select recursive
tree blobs matching `<division>/**/*.md`, and count them (`254`). Restricting to
exactly one slash produces `239`; the 15-file difference is the nested
`game-development/{blender,godot,roblox-studio,unity}/` inventory. This method
avoids README marketing totals and unrelated top-level Markdown.

The unpinned [current repository page](https://github.com/msitarzewski/agency-agents)
is retained only for discovery and as a refresh trigger. It is not evidence for
this cutoff snapshot.

### Contract Comparison

| Dimension | Local workspace contract | Pinned `agency-agents` contract | Analysis |
| --- | --- | --- | --- |
| Selection | Ten bounded roles, supervisor routing, canonical catalog | 254 persona files organized by division | External breadth is a discovery lens, not a reason to expand the local roster. |
| Model/routing | Two local tiers, per-provider declarations, role/risk escalation | No required model or effort field | Direct copy cannot satisfy local routing policy. |
| Tool/permission | Claude per-agent allowlist plus outer provider permissions/sandbox; Codex/Gemini differ | No common minimum or allowlist requirement; host-specific conversion is thin | Host enforcement and conversion output must not be conflated. |
| Governance | JIT scope import, guardrails, handoff, postflight, durable memory owner | Self-contained persona, identity/memory, frameworks, delivery style | Persona-memory blocks conflict with the local canonical knowledge-store rule. |
| Provider packaging | Three hand-maintained role adapters with partial static parity checks | 15 install targets and 13 generated conversions | File conversion offers reach, not native behavioral parity. |
| Evaluation | Repo gates plus recommended task-specific agent evals | Source linter checks required metadata and warns on sections | Neither source lint nor local static shape proves output quality. |

### Role and Coverage Gap Register

`Candidate` requires repeated local work plus a distinct scope, tools,
deliverable, acceptance criteria, handoff, and postflight that cannot be safely
absorbed by an existing role. No newly scanned upstream role meets that bar at
this cutoff.

| External pattern | Local coverage | Decision | Rationale | Canonical follow-up route |
| --- | --- | --- | --- | --- |
| `engineering-sre` / observability | `observability-reviewer` now owns manifest/SLO review | Closed | The 2026-07-04 candidate was implemented across all three local surfaces on 2026-07-06. It remains manifest-static, not live SRE automation. | Preserve in [harness catalog](../../../00.agent-governance/harness-catalog.md); future behavior change requires an agent-design spec/task. |
| `engineering-network-engineer` | `network-reviewer` owns ingress, Traefik, NetworkPolicy, DNS, and TLS manifest review | Closed | The earlier candidate was implemented across all three local surfaces. Native semantic field validation remains a separate gap. | Stage 00 validator owner via a bounded Stage 04 parity task. |
| `engineering-sre` incident vocabulary | `incident-responder` plus `observability-reviewer` | Adapt | SLO, error-budget, and burn-rate framing can improve evidence and severity without granting live monitoring authority. | New Stage 03 agent-body spec, then coordinated three-adapter task and role eval. |
| `engineering-code-reviewer` success metrics | `code-reviewer` and `gitops-reviewer` | Adapt | Evidence citations, finding precision, and false-negative targets are measurable improvements; a duplicate reviewer is not justified. | Agent-body/eval spec routed through catalog, adapter owners, and repo QA evidence. |
| `engineering-devops-automator` | `supervisor`, `k8s-implementer`, `gitops-reviewer`, workflows, validators | Adapt | Automation responsibility is already separated by write/review/static-gate boundaries. A general mutation-capable agent would blur ownership. | Existing role scopes and [automation reference](automation-pipeline-workflow-qa.md); new task only for a repeated concrete gap. |
| testing QA personas | `code-reviewer`, role-specific reviewers, pre-commit, CI/static validators | Adapt | Agent-output eval design is useful, but validation remains deterministic and role-specific; a broad QA persona has no distinct write surface yet. | Evaluation design under Stage 03/04; keep deterministic owners in scripts/CI. |
| identity/access and compliance personas | `security-auditor`, security scope, Kubernetes/static policy gates | Adapt | IAM/compliance lenses fit the current security audit boundary; no repeated distinct deliverable or tool boundary proves a second role. | Security agent-body/eval spec plus [security reference](kubernetes-infrastructure-security.md). |
| `engineering-finops-engineer` | No dedicated local cost telemetry or FinOps evidence loop | Skip | The upstream role is relevant in general, but the repo has no repeated local work, scoped data/tool access, or acceptance contract to justify an agent now. | Reconsider only after an approved cost-observability requirement and evidence pipeline exist. |
| `engineering-technical-writer` | `doc-writer` plus Stage 99 templates | Skip | Local taxonomy/template routing is more specific and already owned. | Existing `doc-writer`; no roster change. |
| `engineering-codebase-onboarding-engineer` | `wiki-curator`, README indexes, LLM Wiki/graph outputs | Skip | A new persona would duplicate canonical-owner curation. | Existing `wiki-curator`; freshness gaps route to a documentation task. |
| `agents-orchestrator` / multi-agent architect / studio producer | `supervisor`, subagent protocol, harness/loop contract | Skip | The local supervisor and explicit protocol own orchestration; an additional catalog persona would duplicate authority. | [Subagent Protocol](../../../00.agent-governance/subagent-protocol.md) and harness reference. |
| Persona identity and memory blocks | Shared bodies plus tracked governance memory | Skip | Per-persona memory would compete with the canonical project ledger and weaken provenance. | [Memory progress](../../../00.agent-governance/memory/progress.md) and Stage 00 memory templates only. |
| Thin Codex/Gemini conversions | Hand-maintained local provider adapters | Adapt | Upstream conversion omits required local scope, guardrail, handoff, postflight, model, effort/tool boundaries. Direct import is non-compliant. | Separate adapter-generation design only after schema/native canaries; preserve hand-maintained files meanwhile. |

The canonical catalog still contains three stale prose statements saying
“Eight”/“eight” adapters even though its roster table and disk contain ten.
This is a Stage 00 documentation/validator follow-up only; the active catalog is
read-only in this research workstream. Likewise, extending exact validator maps
to network/observability and adding Gemini native-schema checks are recorded as
future Stage 04 work, not applied here.

### Default, Escalation, and Fallback Routing

This matrix is an evaluation hypothesis, not active assignment. Current local
declarations remain `opus 4.8` / `sonnet 4.6`, `gpt-5.5` /
`gpt-5.3-codex`, and `Gemini 3.1 Pro` / `Gemini 3.5 Flash`. Claude spaced
labels and Gemini display labels are not documented exact IDs; Codex worker
lifecycle depends on the authentication surface. Every proposed route requires
native availability, exact-ID, role-task, tool, quality, latency/cost, and
rollback evidence before an active owner changes.

| Local role | Task profile | Claude default/escalation/fallback | Codex default/escalation/fallback | Gemini default/escalation/fallback | Effort | Eval gate |
| --- | --- | --- | --- | --- | --- | --- |
| `supervisor` | Ambiguous planning, decomposition, multi-agent synthesis, completion judgment | Opus 4.8 / Fable 5 / Sonnet 5 | Sol medium / Sol high or `max` / Terra | 3.5 Flash Stable / 3.1 Pro Preview with explicit acceptance / 3.1 Flash-Lite for bounded preprocessing only | Current Codex `xhigh`; proposed Sol effort starts medium and increases only on eval evidence. `max` is single-model reasoning, not orchestration. | Golden plans, delegation correctness, cross-agent synthesis, tool use, long-context retention, termination, cost/latency, rollback. |
| `code-reviewer` | YAML/Helm/shell correctness and policy review | Sonnet 5 / Opus 4.8 / Haiku 4.5 for bounded scans | Terra / Sol / 5.4 Mini or Luna only if thresholds hold | 3.5 Flash / 3.1 Pro Preview / 3.1 Flash-Lite for bounded scans | Current Codex `high`; candidate uses lowest effort meeting false-negative threshold. | Seeded defects, false negatives/positives, evidence citations, severity calibration, no unauthorized edits, repo gates. |
| `doc-writer` | Template routing, drafting, taxonomy and source synthesis | Sonnet 5 / Opus 4.8 / Haiku 4.5 | Terra / Sol / Luna or 5.4 Mini | 3.5 Flash / 3.1 Pro Preview / 3.1 Flash-Lite | Current Codex `medium`; candidate default/medium, escalate for conflicting sources or architecture. | Template/path correctness, unsupported-claim rate, link accuracy, Korean clarity, minimal duplication, cost. |
| `gitops-reviewer` | Argo CD targeting, Kustomize structure, release risk | Sonnet 5 / Opus 4.8 / Haiku only for deterministic inventory | Terra / Sol / 5.4 Mini for bounded inventory | 3.5 Flash / 3.1 Pro Preview / Flash-Lite for inventory only | Current Codex `high`; retain high-risk review depth until comparative eval passes. | Seeded ownership/sync defects, missed-high-risk rate, file evidence, no live mutation, independent reviewer agreement. |
| `incident-responder` | Timeline, impact, RCA hypothesis, remediation handoff | Opus 4.8 / Fable 5 / Sonnet 5 | Sol high / Sol `max` plus independent review / Terra as evidence collector | 3.5 Flash / 3.1 Pro Preview with lifecycle acceptance / Flash-Lite extraction only | Current Codex `high`; smaller fallback never signs off severity or recovery. | Timeline fidelity, causal uncertainty, severity calibration, evidence provenance, unsafe-action refusal, human approval. |
| `k8s-implementer` | Bounded GitOps manifest authoring and validation repair | Sonnet 5 / Opus 4.8 / Haiku only for mechanical transforms | Terra / Sol / 5.4 Mini or Luna only for schema-bounded transforms | 3.5 Flash / 3.1 Pro Preview / Flash-Lite only for bounded transforms | Current Codex `high`; lower candidate effort must still pass write/review separation and all repo gates. | Patch correctness, schema/Kustomize validity, secret safety, minimal diff, tool boundary, independent GitOps/security review. |
| `network-reviewer` | Ingress, Traefik, NetworkPolicy, DNS/TLS static review | Sonnet 5 / Opus 4.8 / Haiku only for inventory | Terra / Sol / 5.4 Mini for bounded inventory | 3.5 Flash / 3.1 Pro Preview / Flash-Lite inventory only | Current Codex `high`; exact-field validator coverage must be added before routing migration. | Seeded routing/isolation/TLS errors, scope separation from security, evidence lines, no live probes, false-negative threshold. |
| `observability-reviewer` | Monitoring manifest and SLO-document review | Sonnet 5 / Opus 4.8 / Haiku only for inventory | Terra / Sol / 5.4 Mini for bounded inventory | 3.5 Flash / 3.1 Pro Preview / Flash-Lite inventory only | Current Codex `high`; exact-field validator coverage must be added before routing migration. | Seeded scrape/alert/SLO defects, no live-query claim, evidence lines, role handoff, false-negative threshold. |
| `security-auditor` | RBAC, network isolation, secret and governance risk judgment | Opus 4.8 / Fable 5 where access permits / Sonnet 5 second pass | Sol high / Sol `max` plus independent review / Terra as evidence collector | 3.5 Flash / 3.1 Pro Preview with lifecycle acceptance / Flash-Lite extraction only | Current Codex `high`; fallback output cannot approve or downgrade a critical finding. | Missed-critical rate, severity consistency, evidence citations, refusal, secret non-disclosure, independent/human approval. |
| `wiki-curator` | Canonical-owner maps, stale-link and generated-index curation | Sonnet 5 / Opus 4.8 / Haiku 4.5 | Terra / Sol / Luna or 5.4 Mini | 3.5 Flash / 3.1 Pro Preview / 3.1 Flash-Lite | Current Codex `medium`; default/medium, deterministic validators before escalation. | Link/owner accuracy, no policy duplication, no vector-store creation, generator idempotence, cost and rollback. |

Provider model facts behind these hypotheses are maintained in the adjacent
[provider implementation reference](provider-implementation-status.md): Claude
Fable 5, Opus 4.8, Sonnet 5, and Haiku 4.5; Codex-product GPT-5.6 Sol/Terra/Luna,
previous-generation GPT-5.5, GPT-5.4 Mini, and authentication-specific
GPT-5.3-Codex lifecycle; Gemini API `gemini-3.1-pro-preview`, stable
`gemini-3.5-flash`, and stable `gemini-3.1-flash-lite`. API publication does
not prove coding-product/CLI or local account availability.

## Interpretation

The local system has a coherent role/body contract and exact 30-file stem
parity, but only Claude and Codex are on their documented native project-agent
paths. `.agents/agents` is a local Antigravity adapter surface, while official
Gemini CLI custom agents use `.gemini/agents`. Static checks also cover only a
subset of provider-specific semantics. Therefore “three adapters exist” is the
accurate claim; “three native runtimes are behaviorally equivalent” is not.

`agency-agents` is valuable for persona vocabulary, role discovery, and
multi-target packaging. Its 254-file breadth and 15-target installer are not a
replacement for the local least-privilege, scope, handoff, postflight, model,
eval, and canonical-owner contracts. Safe reuse is adaptation: select a proven
local gap, strip conflicting persona memory, add local governance and provider
metadata, validate all adapters, run role-specific evals, and preserve rollback.

## Sources

All external sources were checked read-only at `2026-07-10 10:00 KST`.

### Pinned Agency-Agents Sources

- Pinned commit: <https://github.com/msitarzewski/agency-agents/commit/9f3e401ccd09aa0ee0ef8e015226d0647908e01e>
- Pinned tree: <https://github.com/msitarzewski/agency-agents/tree/9f3e401ccd09aa0ee0ef8e015226d0647908e01e>
- Recursive Git tree API: <https://api.github.com/repos/msitarzewski/agency-agents/git/trees/9f3e401ccd09aa0ee0ef8e015226d0647908e01e?recursive=1>
- Division registry: <https://raw.githubusercontent.com/msitarzewski/agency-agents/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/divisions.json>
- Agent linter: <https://raw.githubusercontent.com/msitarzewski/agency-agents/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/scripts%2Flint-agents.sh>
- Conversion script: <https://raw.githubusercontent.com/msitarzewski/agency-agents/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/scripts%2Fconvert.sh>
- Install-target registry: <https://raw.githubusercontent.com/msitarzewski/agency-agents/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/tools.json>
- SRE sample: <https://raw.githubusercontent.com/msitarzewski/agency-agents/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/engineering/engineering-sre.md>
- README self-description: <https://raw.githubusercontent.com/msitarzewski/agency-agents/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/README.md>
- MIT license: <https://raw.githubusercontent.com/msitarzewski/agency-agents/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/LICENSE>
- Unpinned discovery page, not snapshot authority:
  <https://github.com/msitarzewski/agency-agents>

### Official Provider Sources

- Claude Code subagents: <https://code.claude.com/docs/en/sub-agents>
- Claude models: <https://platform.claude.com/docs/en/about-claude/models/overview>
- Codex subagents: <https://developers.openai.com/codex/subagents>
- Codex models: <https://developers.openai.com/codex/models>
- OpenAI API models: <https://developers.openai.com/api/docs/models>
- Gemini CLI subagents: <https://geminicli.com/docs/core/subagents/>
- Gemini CLI model selection: <https://geminicli.com/docs/cli/model/>
- Gemini API models: <https://ai.google.dev/gemini-api/docs/models>

### Repository Sources

- Canonical roster: [Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- Tier vocabulary: [Model Policy](../../../00.agent-governance/model-policy.md)
- Delegation: [Subagent Protocol](../../../00.agent-governance/subagent-protocol.md)
- Provider notes: [Claude](../../../00.agent-governance/providers/claude.md),
  [Codex](../../../00.agent-governance/providers/codex.md), and
  [Gemini](../../../00.agent-governance/providers/gemini.md)
- Adapter sets: `.claude/agents/*.md`, `.codex/agents/*.toml`, and
  `.agents/agents/*.md`
- Static parity owner: `scripts/validate-repo-quality-gates.sh`
- Earlier analysis integrated after current re-verification:
  [2026-07-04 agent reference](../2026-07-04-wer/ai-agents-roster-and-gap-analysis.md)

## Review and Freshness

- Review cadence: on roster/adapter/model-policy/validator or upstream/provider
  source change.
- Last reviewed: `2026-07-10 10:00 KST`
- Next review trigger: any change to the 30 adapters, harness catalog, model
  policy, adapter validator, official native-agent paths/model lifecycle, or
  pinned upstream registry/conversion format.
- Refresh method: select the last upstream commit before the new cutoff, pin the
  SHA, recount registered-division Markdown recursively, re-read linter/tools/
  converter contracts, recount and parse local adapters, and run static and
  provider-native canary evidence in separate lanes.
- Limitations: no provider CLI, agent registry, model resolution, entitlement,
  inference, hook/tool enforcement, live cluster, credential, secret-value,
  remote CI, publish, push, merge, or third-party mutation was checked.

## Related Documents

- **Parent research README**: [README.md](README.md)
- **Provider and model reference**: [provider-implementation-status.md](provider-implementation-status.md)
- **Harness and loop reference**: [harness-and-loop-engineering.md](harness-and-loop-engineering.md)
- **Automation and QA reference**: [automation-pipeline-workflow-qa.md](automation-pipeline-workflow-qa.md)
- **Kubernetes and security reference**: [kubernetes-infrastructure-security.md](kubernetes-infrastructure-security.md)
- **Workspace baseline**: [workspace-governance-baseline.md](workspace-governance-baseline.md)
- **Current hardening task**:
  [Task record](../../../04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md)
