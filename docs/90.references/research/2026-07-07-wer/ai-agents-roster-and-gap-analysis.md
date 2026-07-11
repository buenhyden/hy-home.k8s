---
title: 'Reference: AI Agents Roster and Gap Analysis Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-11
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

### Vibe-Coding Source and Authority Ledger

이 절은 용어의 기원과 안전 통제의 근거를 분리한다. Karpathy의 게시물은
`vibe coding`이라는 표현과 원래의 throwaway-project 맥락만 설명하는
비규범적 1차 발언이다. 아래의 risk, review, test, provenance, permission,
approval 통제는 NIST, OWASP와 공급자 공식 지침에서 가져온다. 모든 URL은
`2026-07-11`에 다시 열었고 provider/model 사실은 승인된
`2026-07-10 10:00 KST` 컷오프에서 동결했다. Living document의 컷오프 이후
기능 변경은 이 문서에 소급하지 않았다.

| Title | Publisher | URL | Source date | Check date | Authority class | Supported claim |
| --- | --- | --- | --- | --- | --- | --- |
| Original `vibe coding` post | Andrej Karpathy | <https://x.com/karpathy/status/1886192184808149383> | 2025-02-02 | 2026-07-11 | Contextual primary statement; non-normative | Prompt-led, low-attention coding was coined as a conversational style suitable in the post's throwaway/weekend-project context; it does not authorize production controls. |
| Secure Software Development Framework (SSDF) Version 1.1, SP 800-218 | NIST | <https://csrc.nist.gov/pubs/sp/800/218/final> | 2022-02-03 | 2026-07-11 | Government security guidance | Track requirements, risks, decisions and exceptions (PW.1.2); protect development environments (PO.5); review/analyze code (PW.7); scope, perform and record testing (PW.8); preserve release provenance (PS.3.2). |
| X03:2025 Inappropriate Trust in AI Generated Code (`Vibe Coding`) | OWASP Foundation | <https://owasp.org/Top10/2025/X01_2025-Next_Steps/#x032025-inappropriate-trust-in-ai-generated-code-vibe-coding> | 2025 edition | 2026-07-11 | OWASP project guidance; not a formal standard | The submitter remains responsible, should understand and review AI-assisted code with human and security-tool review, and should not use unattended vibe coding for complex or business-critical software. |
| LLM01:2025 Prompt Injection | OWASP Gen AI Security Project | <https://genai.owasp.org/llmrisk/llm01-prompt-injection/> | 2025 edition | 2026-07-11 | OWASP project guidance | External content can redirect an agent; constrain scope, validate expected output, apply least privilege, require approval for high-risk actions, and adversarially test. |
| LLM03:2025 Supply Chain | OWASP Gen AI Security Project | <https://genai.owasp.org/llmrisk/llm032025-supply-chain/> | 2025 edition | 2026-07-11 | OWASP project guidance | Verify suppliers and dependencies, keep inventories, preserve licensing and provenance, and use signing or hashes for externally supplied artifacts. |
| LLM05:2025 Improper Output Handling | OWASP Gen AI Security Project | <https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/> | 2025 edition | 2026-07-11 | OWASP project guidance | Treat model output as untrusted input and validate or sanitize it before shell, path, query, rendered-content, or downstream execution. |
| LLM06:2025 Excessive Agency | OWASP Gen AI Security Project | <https://genai.owasp.org/llmrisk/llm062025-excessive-agency/> | 2025 edition | 2026-07-11 | OWASP project guidance | Minimize tools, functionality, permissions and autonomy; mediate authorization outside the model and require human approval for high-impact actions. |
| Security | Anthropic, Claude Code Docs | <https://code.claude.com/docs/en/security> | Undated living document; available before cutoff | 2026-07-11 | Official product security guidance | Use permission boundaries and sandboxing, review commands and critical-file changes, verify trust for repositories/MCP, and protect sensitive code and credentials. |
| Best Practices for Claude Code | Anthropic, Claude Code Docs | <https://code.claude.com/docs/en/best-practices> | Undated living document; available before cutoff | 2026-07-11 | Official coding-agent workflow guidance | Explore before complex implementation, give executable verification criteria, run tests/linters, use independent review, and do not ship unverifiable work. |
| Running Codex safely at OpenAI | OpenAI | <https://openai.com/index/running-codex-safely/> | 2026-05-08 | 2026-07-11 | Official product security guidance | Combine sandbox and approval boundaries with constrained network/identity access, managed rules and agent-aware telemetry; stop higher-risk actions for review. |
| Trusted Folders | Google, Gemini CLI Docs | <https://geminicli.com/docs/cli/trusted-folders/> | Last updated 2026-04-23 | 2026-07-11 | Official product security guidance | Treat repository commands, hooks, skills, settings and MCP configuration as trust-bearing input; untrusted workspaces should operate with restricted capabilities. |
| Sandboxing in Gemini CLI | Google, Gemini CLI Docs | <https://geminicli.com/docs/cli/sandbox/> | Last updated 2026-04-27 | 2026-07-11 | Official product security guidance | Isolate shell/file actions, keep profiles restrictive, request explicit expansion, and do not treat a sandbox as eliminating all risk. |
| Models overview | Anthropic | <https://platform.claude.com/docs/en/about-claude/models/overview> | Living catalog; cutoff snapshot 2026-07-10 10:00 KST | 2026-07-11 | Official model catalog | Capability, latency, effort and lifecycle inform a candidate route; API publication does not prove local Claude Code access or entitlement. |
| Codex models | OpenAI | <https://developers.openai.com/codex/models> | Living catalog; cutoff snapshot 2026-07-10 10:00 KST | 2026-07-11 | Official model/product guidance | Coding-product model and effort guidance informs candidate routes; the local account and authentication surface still require a native canary. |
| Gemini API models | Google | <https://ai.google.dev/gemini-api/docs/models> | Living catalog; cutoff snapshot 2026-07-10 10:00 KST | 2026-07-11 | Official API model catalog | API model lifecycle informs candidate evaluation only; it does not prove Gemini CLI selection or local availability. |

### Risk-Bounded Vibe-Coding Control Matrix

여기서 `vibe coding`은 자연어 prompt로 빠르게 탐색하고 생성 결과를 반복하는
작업 방식이다. 빠른 feedback은 허용하지만 “결과가 그럴듯하다”는 완료 증거가
아니다. 모든 등급에서 AI output은 untrusted proposal이며, 위험이 올라갈수록
specification, deterministic evidence, independent review와 human approval을
추가한다.

| Control | R0 — disposable exploration | R1 — bounded repository change | R2 — protected control surface | R3 — live/high-impact action |
| --- | --- | --- | --- | --- |
| Allowed use | Time-boxed prompt-led spike with no production or durable-state claim. | AI-assisted implementation inside an explicit file and behavior scope. | AI-assisted analysis or patch proposal only for infrastructure, GitOps, identity, secret, network, security-policy, CI/hook or agent-governance changes. | Analysis, evidence collection and runbook draft only; not autonomous execution. |
| Executable acceptance | State a disposable question and observable result before generation. | Define testable acceptance criteria, affected lanes and completion command before edit. | Bind PRD/ARD/ADR/Spec/Plan/Task owner as applicable, risk/exception record, negative cases and approval gate. | Require operator-approved target, runbook, preconditions, stop criteria, rollback and post-action evidence. |
| Diff and iteration | Work in an isolated scratch/worktree and discard freely. | Keep diffs small, inspect every changed file and split unrelated work. | One logical control change at a time; flag lockfile, workflow, policy, credential path and out-of-scope edits. | No direct change by the coding agent; present the exact proposed action and blast radius to the operator. |
| Tests and static checks | Smoke check the claimed behavior; label unverified output. | Run changed-file and affected-lane tests, lint, type/schema/static checks, then the canonical completion gates. | Add adversarial/negative fixtures, secret/policy scans and domain-specific validators; passing tests written by the same agent are not independent assurance. | Use only approved preflight/live/postflight checks; static desired state never proves runtime success. |
| Review independence | Author self-review is enough only for discarded output. | Human or separately scoped reviewer checks the full diff and acceptance evidence. | Independent domain review is mandatory: GitOps/network/security/identity/secret owners cannot be replaced by the generating agent's summary. | Human operator owns approval and execution; peer/security approval follows the canonical operations boundary. |
| Provenance | Record prompt/source only if the spike is retained. | Cite input sources, agent/tool/model declaration, changed files, commands and PASS/SKIP/FAIL. | Preserve supplier/dependency identity, hashes or pins where applicable, risk decisions, approvals and artifact/rollback identity. | Preserve operator, target, timestamp, command/result, approval and recovery evidence without exposing secret values. |
| Secrets and permissions | No production credentials, external write tools or sensitive data. | Least-privilege workspace access; external content and model output remain untrusted. | No plaintext secret inspection or credential widening; sandbox, egress and tool scopes stay minimal and high-impact calls require human mediation. | No agent-held standing privilege; use approved operator identity and downstream authorization, never model judgment as authorization. |
| Rollback | Delete the spike or reset the isolated workspace. | Revert the logical commit or restore the documented pre-change state. | Prove config/data migration rollback and preserve the previous policy/manifest before approval. | Operator-owned recovery step and validation are prerequisites, not an afterthought. |
| Stop and escalate | Stop when the time box expires or the result cannot be observed. | Stop on scope drift, repeated failure, missing dependency, ambiguous acceptance or unverifiable claim. | Stop on missing owner/evidence, unexpected sensitive file, permission expansion, test weakening, validator bypass or Critical/High uncertainty; escalate to the canonical reviewer and human approver. | Stop on any target mismatch, stale approval, secret exposure, unexpected runtime state or rollback uncertainty and follow the incident/break-glass route. |

R0 결과가 durable branch로 승격되는 순간 R1 이상을 처음부터 적용한다. 특히
R2에 나열한 표면은 “vibe로 완성”할 수 있는 대상이 아니라 AI-assisted draft를
evidence- and approval-gated SDLC로 넘기는 대상이다. 이 연구는 live mutation
권한, secret 접근 권한 또는 active policy 예외를 만들지 않는다.

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

### Secondary AI-Agent QA Application

AI-agent QA 의무의 primary benchmark는
[SDLC, CI, QA and Formatting Research](spec-sdlc-ci-qa-formatting.md#ai-agent-qa-benchmark-summary)가
소유한다. 그 문서는 iteration 중 changed-file/affected-lane feedback, PR/merge
전과 hook·validator·toolchain·global-format contract 변경 후의
`pre-commit run --all-files`, 그리고 PASS/SKIP/FAIL 및 unavailable evidence
기록을 정의한다. 이 절은 그 기준을 다시 정의하지 않고 로컬 역할과 adapter에
적용할 때 생기는 2차 의미만 기록한다.

| Application surface | Secondary role/application implication | Evidence boundary |
| --- | --- | --- |
| `supervisor` | Task 시작 전에 affected lane과 완료 gate를 배정하고, handoff에서 primary benchmark의 명령 결과와 skipped limitation이 있는지 확인한다. | Supervisor의 완료 판단은 명령 출력이나 승인 기록을 소비할 뿐, 자체 요약으로 full-suite PASS를 만들지 못한다. |
| Authoring roles: `k8s-implementer`, `doc-writer`, `wiki-curator` | 작은 logical diff마다 changed-file/affected-lane feedback을 실행하고, 결과와 미실행 사유를 reviewer에게 넘긴다. | 생성 agent가 작성한 test와 self-review는 독립 검토가 아니며 protected surface sign-off가 아니다. |
| Review roles: `code-reviewer`, `gitops-reviewer`, `network-reviewer`, `observability-reviewer`, `security-auditor`, `incident-responder` | 전체 changed-file inventory와 acceptance evidence를 검사하고 out-of-scope edit, 약화된 test, skipped hook, secret/permission drift를 finding으로 올린다. | Read-only review는 실행되지 않은 full suite, provider permission enforcement 또는 live state를 PASS로 승격하지 않는다. |
| Provider adapters | Claude `tools`, Codex effort/sandbox outer boundary, `.agents` guardrail처럼 native metadata가 달라도 같은 QA handoff 문구와 scope를 유지해야 한다. | Adapter field와 stem parity는 선언 증거다. 실제 host가 adapter와 hook wiring을 소비했는지는 native canary 없이는 `Unverified`. |
| PostToolUse and lifecycle hooks | 빠른 formatter/style/repo feedback으로 iteration을 줄이고 objective failure를 조기에 드러낸다. | PostToolUse 결과는 primary benchmark가 명시한 `pre-commit run --all-files` 또는 explicit completion command의 대체물이 아니다. |
| R2 protected surfaces | 생성 역할과 domain reviewer를 분리하고, human approval 전에 deterministic repo evidence와 rollback을 함께 제시한다. | infrastructure, GitOps, identity, secret, network, security-policy 변경은 adapter feedback만으로 승인되지 않는다. |

따라서 agent body 또는 adapter를 후속 변경할 때는 QA 명령을 중복 복사하기보다
primary benchmark를 link하고, 역할에는 affected-lane 선택, evidence handoff,
independent review와 stop/escalation 책임만 둔다. 이 구조는 primary owner가
명령 계약을 바꿀 때 30개 adapter가 서로 다른 오래된 문구를 갖는 것을 막는다.

### Upstream Snapshot — 2026-07-10

| Claim | Verified value | Evidence | Authority limitation |
| --- | --- | --- | --- |
| Revision at cutoff | `9f3e401ccd09aa0ee0ef8e015226d0647908e01e`, committed `2026-07-10 05:32:59 KST`; last `main` commit before the cutoff | [Cutoff commit query](https://api.github.com/repos/msitarzewski/agency-agents/commits?sha=main&until=2026-07-10T01%3A00%3A00Z&per_page=1), [pinned commit](https://github.com/msitarzewski/agency-agents/commit/9f3e401ccd09aa0ee0ef8e015226d0647908e01e) | The query cutoff is `2026-07-10 01:00:00Z`, equivalent to `10:00 KST`; later `main` changes are outside this snapshot. |
| License and releases | MIT; repository tags `0`, releases `0` at check time | [Pinned LICENSE](https://raw.githubusercontent.com/msitarzewski/agency-agents/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/LICENSE), [tags API](https://api.github.com/repos/msitarzewski/agency-agents/tags?per_page=100), [releases API](https://api.github.com/repos/msitarzewski/agency-agents/releases?per_page=100) | The APIs returned empty arrays at the cutoff check; no version tag exists to use as a semantic release baseline. |
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

### Pinned Upstream Role-Overlap Classification

The classifications below compare the local role contract with standalone
persona files present in the pinned recursive tree. `Direct overlap` means a
standalone upstream persona has materially the same primary function; it does
not mean identical name, tools, authority, or behavior. `Near/functional
overlap` means one or more personas offer useful patterns but no single one
matches the local contract. `No exact standalone upstream role` means the
pinned tree has no dedicated persona for that local role even though adjacent
personas may provide partial patterns. None of these labels establishes a
local implementation gap or provider parity.

| Local role | Upstream-overlap classification | Pinned upstream evidence | Contract boundary |
| --- | --- | --- | --- |
| `supervisor` | Direct overlap | `specialized/agents-orchestrator.md` | Both own decomposition and multi-agent coordination; the local role additionally owns repository governance, completion evidence, and bounded-loop termination. |
| `code-reviewer` | Direct overlap | `engineering/engineering-code-reviewer.md` | Both center on code-review findings; the local role is constrained to repository evidence, read-only review, and local postflight. |
| `doc-writer` | Near/functional overlap | `engineering/engineering-technical-writer.md`; `specialized/specialized-document-generator.md` | Upstream writing patterns are relevant, but neither standalone persona owns the local Stage taxonomy, templates, canonical links, and source ledger together. |
| `gitops-reviewer` | No exact standalone upstream role | Nearby: `engineering/engineering-devops-automator.md`; `engineering/engineering-code-reviewer.md` | Automation and review patterns are partial; no pinned standalone persona owns Argo CD targeting, Kustomize structure, sync risk, and review-only GitOps evidence. |
| `incident-responder` | Direct overlap | `security/security-incident-responder.md`; `engineering/engineering-incident-response-commander.md` | Incident triage and response overlap directly; the local role remains read-only and routes recovery or live action through explicit approval and handoff. |
| `k8s-implementer` | No exact standalone upstream role | Nearby: `engineering/engineering-devops-automator.md`; `engineering/engineering-sre.md` | No pinned standalone Kubernetes implementer exists; DevOps/SRE provide partial operational patterns but not the local GitOps-only manifest-authoring contract. |
| `network-reviewer` | Direct overlap | `engineering/engineering-network-engineer.md` | Network design and diagnostics overlap directly; the local role is narrower, review-only, manifest-static, and explicitly forbids live probes. |
| `observability-reviewer` | No exact standalone upstream role | Nearby: `engineering/engineering-sre.md` | No pinned standalone observability reviewer exists; SRE supplies SLO/monitoring vocabulary but also carries broader operational responsibilities absent from the local static-review role. |
| `security-auditor` | Near/functional overlap | `security/security-compliance-auditor.md`; `security/security-appsec-engineer.md`; `security/security-cloud-security-architect.md` | Several narrower security personas contribute patterns, but no single pinned persona matches the local cross-cutting RBAC, NetworkPolicy, secrets, and governance audit contract. |
| `wiki-curator` | No exact standalone upstream role | Nearby: `engineering/engineering-codebase-onboarding-engineer.md`; `engineering/engineering-technical-writer.md` | No pinned standalone wiki curator exists; onboarding and technical-writing personas only partially cover canonical-owner, stale-link, and generated-index curation. |

### Role and Coverage Gap Register

`Candidate` requires repeated local work plus a distinct scope, tools,
deliverable, acceptance criteria, handoff, and postflight that cannot be safely
absorbed by an existing role. No newly scanned upstream role meets that bar at
this cutoff. In this register, `Closed` means the previously identified **local
coverage gap** has an implemented local owner. It never means that the local
role has an exact upstream standalone counterpart or that provider behavior is
at parity.

| External pattern | Local coverage | Decision | Rationale | Canonical follow-up route |
| --- | --- | --- | --- | --- |
| `engineering-sre` / observability | `observability-reviewer` now owns manifest/SLO review | Closed | The earlier **local coverage gap** was closed across all three local surfaces on 2026-07-06. This does not assert an exact upstream observability-reviewer role: pinned `engineering-sre` is only a near/functional pattern, and local coverage remains manifest-static rather than live SRE automation. | Preserve in [harness catalog](../../../00.agent-governance/harness-catalog.md); future behavior change requires an agent-design spec/task. |
| `engineering-network-engineer` | `network-reviewer` owns ingress, Traefik, NetworkPolicy, DNS, and TLS manifest review | Closed | The earlier **local coverage gap** was closed across all three local surfaces. The upstream network engineer directly overlaps functionally, but native semantic-field validation and behavioral parity remain separate gaps. | Stage 00 validator owner via a bounded Stage 04 parity task. |
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

### Role and Model-Routing Decision Record

This matrix is an evaluation hypothesis, not active assignment. It separates
six fields that must never be collapsed into “best model”: active declaration,
research default, escalation, fallback, eval gate, and availability confidence.
Current declarations remain owned by the adapter files and canonical catalog;
candidate facts remain frozen at `2026-07-10 10:00 KST` in the adjacent
[provider implementation reference](provider-implementation-status.md).

`C / O / G` below means Claude / OpenAI Codex / Gemini. A candidate catalog
entry is not an entitlement. `Verified repo-static declaration` means only that
the tracked adapter names a model; every candidate route remains `Conditional`
until the exact product surface resolves the ID, the account can invoke it, the
role eval passes, and rollback to the incumbent is demonstrated.

| Local role | Active declaration — repo-static only | Research default candidate | Escalation trigger and candidate | Fallback boundary and candidate | Eval gate | Availability confidence |
| --- | --- | --- | --- | --- | --- | --- |
| `supervisor` | C `opus 4.8`; O `gpt-5.5`/`xhigh`; G `Gemini 3.1 Pro` | C Opus 4.8; O Sol/medium; G 3.5 Flash Stable | Ambiguous/high-risk planning or failed synthesis: C Fable 5; O Sol/high then `max`; G 3.1 Pro Preview only with lifecycle acceptance | C Sonnet 5; O Terra; G Flash-Lite only for bounded preprocessing, never completion judgment | Golden plans, delegation/synthesis correctness, tool use, termination, long-context retention, cost/latency, rollback | Active declaration `Verified repo-static`; every candidate `Conditional`; no native resolution, entitlement or inference canary. |
| `code-reviewer` | C `sonnet 4.6`; O `gpt-5.3-codex`/`high`; G `Gemini 3.5 Flash` | C Sonnet 5; O Terra; G 3.5 Flash | High missed-defect risk or conflicting evidence: C Opus 4.8; O Sol; G 3.1 Pro Preview | C Haiku 4.5; O 5.4 Mini/Luna; G Flash-Lite for deterministic inventory only | Seeded defects, false negative/positive rate, citations, severity, no unauthorized edits, repo gates | Active declaration `Verified repo-static`; candidate product/account availability and comparative quality `Conditional`. |
| `doc-writer` | C `sonnet 4.6`; O `gpt-5.3-codex`/`medium`; G `Gemini 3.5 Flash` | C Sonnet 5; O Terra; G 3.5 Flash | Conflicting sources or architecture synthesis: C Opus 4.8; O Sol; G 3.1 Pro Preview | C Haiku 4.5; O Luna/5.4 Mini; G Flash-Lite for bounded format work | Template/path correctness, unsupported claims, links, Korean clarity, duplication and cost | Active declaration `Verified repo-static`; candidate availability and native adapter consumption `Conditional`. |
| `gitops-reviewer` | C `sonnet 4.6`; O `gpt-5.3-codex`/`high`; G `Gemini 3.5 Flash` | C Sonnet 5; O Terra; G 3.5 Flash | Sync/ownership/release-risk ambiguity: C Opus 4.8; O Sol; G 3.1 Pro Preview | Smaller models only for deterministic inventory; never risk sign-off | Seeded ownership/sync defects, missed-high-risk rate, file evidence, no live mutation, reviewer agreement | Active declaration `Verified repo-static`; candidates `Conditional`; no GitOps judgment inference canary. |
| `incident-responder` | C `sonnet 4.6`; O `gpt-5.3-codex`/`high`; G `Gemini 3.5 Flash` | C Opus 4.8; O Sol/high; G 3.5 Flash | Severe/ambiguous causality: C Fable 5; O Sol/`max` plus independent review; G 3.1 Pro Preview with lifecycle acceptance | C Sonnet 5; O Terra; G Flash-Lite as evidence extractor only, never severity/recovery sign-off | Timeline fidelity, causal uncertainty, severity, provenance, unsafe-action refusal and human approval | Active declaration `Verified repo-static`; candidate availability `Conditional`; live response remains `Unverified live`. |
| `k8s-implementer` | C `sonnet 4.6`; O `gpt-5.3-codex`/`high`; G `Gemini 3.5 Flash` | C Sonnet 5; O Terra; G 3.5 Flash | Cross-resource/security ambiguity: C Opus 4.8; O Sol; G 3.1 Pro Preview | Smaller model only for schema-bounded mechanical transform; independent review still required | Patch/schema/Kustomize correctness, secret safety, minimal diff, tool boundary, GitOps/security review | Active declaration `Verified repo-static`; candidate availability `Conditional`; local declaration does not prove cluster access or readiness. |
| `network-reviewer` | C `sonnet 4.6`; O `gpt-5.3-codex`/`high`; G `Gemini 3.5 Flash` | C Sonnet 5; O Terra; G 3.5 Flash | Routing/isolation/TLS ambiguity: C Opus 4.8; O Sol; G 3.1 Pro Preview | Smaller model for inventory only, never isolation/TLS sign-off | Seeded routing/isolation/TLS errors, evidence lines, no live probes, false-negative threshold | Active declaration `Verified repo-static`; candidate availability `Conditional`; exact-field validator coverage is prerequisite to migration. |
| `observability-reviewer` | C `sonnet 4.6`; O `gpt-5.3-codex`/`high`; G `Gemini 3.5 Flash` | C Sonnet 5; O Terra; G 3.5 Flash | Alert/SLO interpretation ambiguity: C Opus 4.8; O Sol; G 3.1 Pro Preview | Smaller model for inventory only, never live-state or SLO sign-off | Seeded scrape/alert/SLO defects, no live-query claim, evidence and handoff accuracy | Active declaration `Verified repo-static`; candidate availability `Conditional`; exact-field validator coverage is prerequisite to migration. |
| `security-auditor` | C `sonnet 4.6`; O `gpt-5.3-codex`/`high`; G `Gemini 3.5 Flash` | C Opus 4.8; O Sol/high; G 3.5 Flash | Critical-risk uncertainty: C Fable 5 where entitled; O Sol/`max` plus independent review; G 3.1 Pro Preview with lifecycle acceptance | C Sonnet 5; O Terra; G Flash-Lite as evidence collector only; fallback cannot approve or downgrade findings | Missed-critical rate, severity consistency, citations, refusal, secret non-disclosure, independent/human approval | Active declaration `Verified repo-static`; candidate availability `Conditional`; security sign-off is never inferred from catalog publication. |
| `wiki-curator` | C `sonnet 4.6`; O `gpt-5.3-codex`/`medium`; G `Gemini 3.5 Flash` | C Sonnet 5; O Terra; G 3.5 Flash | Conflicting canonical owners or large synthesis: C Opus 4.8; O Sol; G 3.1 Pro Preview | C Haiku 4.5; O Luna/5.4 Mini; G Flash-Lite for bounded curation | Link/owner accuracy, no policy duplication/vector store, generator idempotence, cost and rollback | Active declaration `Verified repo-static`; candidate availability and provider-native behavior `Conditional`. |

The active declaration column is descriptive, not a claim that the named model
resolved in the current CLI or account. Default promotion requires the role eval
to beat or match the incumbent at an approved cost/latency bound. Escalation is
triggered by risk or failed evidence, not prestige. Fallback must reduce scope
and authority rather than silently accept lower quality. If a native canary
fails, the route stays on the incumbent and the failure is recorded; it is not
papered over with an API catalog entry.

### New-Role Admission Gate

Upstream catalog breadth does not create a local role. A proposed role must
provide all of: repeated repo-backed demand; a distinct canonical scope and
deliverable; a written non-overlap case against all ten existing roles; least-
privilege tool and data access; measurable eval thresholds; handoff/postflight;
and rollback. A telemetry-dependent role must also identify the approved data
source, access owner, freshness, retention and evidence-quality checks before an
adapter is proposed.

`FinOps` therefore remains `Skip`: there is no approved local cost telemetry
pipeline, no repeated cost-optimization task evidence, and no demonstrated
non-overlap case showing that `supervisor`, `observability-reviewer` and existing
reporting workflows cannot absorb the bounded work. Only a future cost-
observability requirement with those telemetry and non-overlap gates may reopen
the Stage 03 agent-design decision.

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

Provider/model facts are frozen at `2026-07-10 10:00 KST`. All URLs below and
in the source ledger were re-opened read-only on `2026-07-11`; no post-cutoff
provider/model release, lifecycle or availability fact was added.

### Vibe-Coding and Secure-Use Sources

- Original contextual post, non-normative:
  <https://x.com/karpathy/status/1886192184808149383>
- NIST SP 800-218 SSDF Version 1.1:
  <https://csrc.nist.gov/pubs/sp/800/218/final>
- OWASP Top 10:2025 X03, Inappropriate Trust in AI Generated Code:
  <https://owasp.org/Top10/2025/X01_2025-Next_Steps/#x032025-inappropriate-trust-in-ai-generated-code-vibe-coding>
- OWASP Gen AI LLM01, LLM03, LLM05 and LLM06:
  <https://genai.owasp.org/llmrisk/llm01-prompt-injection/>,
  <https://genai.owasp.org/llmrisk/llm032025-supply-chain/>,
  <https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/>, and
  <https://genai.owasp.org/llmrisk/llm062025-excessive-agency/>
- Anthropic Claude Code security and best practices:
  <https://code.claude.com/docs/en/security> and
  <https://code.claude.com/docs/en/best-practices>
- OpenAI, Running Codex safely at OpenAI:
  <https://openai.com/index/running-codex-safely/>
- Google Gemini CLI trusted folders and sandbox:
  <https://geminicli.com/docs/cli/trusted-folders/> and
  <https://geminicli.com/docs/cli/sandbox/>

### Pinned Agency-Agents Sources

- Pinned commit: <https://github.com/msitarzewski/agency-agents/commit/9f3e401ccd09aa0ee0ef8e015226d0647908e01e>
- Pinned tree: <https://github.com/msitarzewski/agency-agents/tree/9f3e401ccd09aa0ee0ef8e015226d0647908e01e>
- Cutoff commit query API:
  <https://api.github.com/repos/msitarzewski/agency-agents/commits?sha=main&until=2026-07-10T01%3A00%3A00Z&per_page=1>
- Tags API:
  <https://api.github.com/repos/msitarzewski/agency-agents/tags?per_page=100>
- Releases API:
  <https://api.github.com/repos/msitarzewski/agency-agents/releases?per_page=100>
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
- Last reviewed: `2026-07-11`; provider/model fact cutoff remains
  `2026-07-10 10:00 KST`.
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

- **Current pack README**: [README.md](README.md)
- **Provider and model reference**: [provider-implementation-status.md](provider-implementation-status.md)
- **Harness and loop reference**: [harness-and-loop-engineering.md](harness-and-loop-engineering.md)
- **Automation and QA reference**: [automation-pipeline-workflow-qa.md](automation-pipeline-workflow-qa.md)
- **Kubernetes and security reference**: [kubernetes-infrastructure-security.md](kubernetes-infrastructure-security.md)
- **Workspace baseline**: [workspace-governance-baseline.md](workspace-governance-baseline.md)
- **Current hardening task**:
  [Task record](../../../04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md)
