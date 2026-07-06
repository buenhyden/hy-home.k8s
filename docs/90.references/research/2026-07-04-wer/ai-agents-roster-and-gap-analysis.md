---
title: 'Reference: AI Agents Roster and Gap Analysis Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-06
---

# Reference: AI Agents Roster and Gap Analysis Research

## Overview

이 문서는 `hy-home.k8s` 워크스페이스에 구현된 AI Agent 로스터를 repo-backed
evidence 기준으로 정리하고, 외부 소스인 `msitarzewski/agency-agents` 저장소를
market-scan 수준에서 조사해 두 체계를 비교한다. 비교 결과로 기존 에이전트의
수정/보완 후보와 신규 에이전트 추가 후보를 gap-analysis 표로 제시한다.

This is durable reference material. It summarizes facts checked on 2026-07-06
and routes follow-up work to canonical owners; it does not change the runtime
roster, agent files, model policy, or governance.

## Purpose

- Record the current workspace AI agent roster and its provider adapter
  implementation as repo-backed facts.
- Capture a dated, source-attributed snapshot of the external
  `msitarzewski/agency-agents` catalog as non-authoritative market scan.
- Compare the two agent definition contracts so future adoption work does not
  import external agent files without adaptation.
- Provide a gap analysis: which existing workspace agents could be improved,
  and which new agents are candidates for addition, with canonical routing.

## Reference Type

- Type: dated-implementation-audit / external-standard-snapshot
- Source checked: 2026-07-06
- Refresh trigger: `docs/00.agent-governance/harness-catalog.md` roster
  changes, `docs/00.agent-governance/model-policy.md` tier changes,
  `.claude/agents/*.md` / `.agents/agents/*.md` / `.codex/agents/*.toml`
  adapter changes, or a major upstream `agency-agents` restructuring.

## Authority Boundary

- **Authoritative for**:
  - Repo-backed summary of the current workspace agent roster checked on
    2026-07-06.
  - Source-attributed external snapshot of `msitarzewski/agency-agents`
    checked on 2026-07-06, labeled non-authoritative market scan.
  - Checklist-level gap-analysis routing to canonical repository owners.
- **Not authoritative for**:
  - The runtime roster itself; `docs/00.agent-governance/harness-catalog.md`
    remains the canonical roster table.
  - Model tier vocabulary; `docs/00.agent-governance/model-policy.md` remains
    the canonical tier policy.
  - Agent behavior contracts; `.claude/agents/*.md`, `.agents/agents/*.md`,
    and `.codex/agents/*.toml` remain the provider-native role adapters.
  - Any agent addition, removal, or rewrite decision. Those route through
    Stage 03 specs and Stage 04 execution before adapter changes.
  - Market-scan conclusions as policy. External catalog facts inform
    candidates only; they cannot override governance or repo evidence.

## Scope

- Covers the eight local workspace agents, their three provider adapters, the
  two-tier model policy, and the local agent file contract.
- Covers the `agency-agents` division registry, agent counts, file format,
  multi-tool install tooling, and orchestration patterns as of 2026-07-06.
- Covers a format comparison and a gap analysis with adopt/adapt/skip
  recommendations bounded to this WSL2+k3d GitOps home-lab context.
- Excludes changes to governance, adapters, hooks, scripts, CI workflows,
  manifests, or secrets, and excludes live-runtime readiness claims.
- Excludes full per-agent review of the external catalog; only divisions
  relevant to this workspace were inventoried in detail.

## Definitions / Facts

### Workspace agent roster (repo-backed)

The canonical roster is `docs/00.agent-governance/harness-catalog.md`. As of
2026-07-06 the local roster is eight agents, each mirrored across three
provider adapters (`.claude/agents/*.md`, `.agents/agents/*.md` for Gemini,
`.codex/agents/*.toml` for GPT/Codex):

| Agent                | Role summary                                              | Tier     |
| -------------------- | --------------------------------------------------------- | -------- |
| `supervisor`         | Task routing, worker selection, runtime completion gates  | `top`    |
| `k8s-implementer`    | Kubernetes manifest authoring safe for GitOps review      | `worker` |
| `gitops-reviewer`    | GitOps structure, ArgoCD targeting, release safety review | `worker` |
| `code-reviewer`      | YAML, Helm, and shell quality/policy review               | `worker` |
| `security-auditor`   | RBAC, network isolation, secret-handling audit            | `worker` |
| `incident-responder` | Incident analysis, timeline, impact, remediation planning | `worker` |
| `doc-writer`         | Template-aligned documentation routing and drafting       | `worker` |
| `wiki-curator`       | LLM Wiki entrypoint and canonical-owner link curation     | `worker` |

Model policy facts (`docs/00.agent-governance/model-policy.md`, checked
2026-07-06):

- Two tiers only: `top` (plan/supervisor) and `worker` (delegated subagent).
- Tier mapping: Claude `opus 4.8` / `sonnet 4.6` or `haiku 4.5`; Gemini
  `Gemini 3.1 Pro` / `Gemini 3.5 Flash`; Codex `gpt-5.5` / `gpt-5.3-codex`
  with mandatory `model_reasoning_effort` in agent TOML.
- `supervisor` is the only `top`-tier agent; escalation of a worker task to
  `top` is a routing decision, not a reclassification.

### Workspace agent file contract (repo-backed)

Each `.claude/agents/*.md` file uses Claude-native frontmatter plus a shared
body skeleton (verified against `supervisor.md` on 2026-07-06):

- Frontmatter: `name`, `description`, `model` (tier-mapped identifier), and
  least-privilege `tools:` list.
- Body: Runtime Bootstrap (JIT governance loading and an `@import` of one
  scope from `docs/00.agent-governance/scopes/`), Role, When to Use, Inputs,
  Outputs, Guardrails, Handoff / Escalation (routes through
  `docs/00.agent-governance/subagent-protocol.md`), and Postflight.
- Guardrails consistently forbid duplicating Stage 00 policy inline and bind
  agents to GitOps-first and no-plaintext-secrets boundaries.

### External catalog snapshot: `msitarzewski/agency-agents` (non-authoritative market scan)

Facts checked 2026-07-06 via the GitHub API and raw file fetches; this
subsection is market scan material and is not authoritative for any local
decision:

- MIT-licensed public repository, created 2025-10-13, still receiving pushes
  as of 2026-07-05; README claims 230+ agents.
- `divisions.json` is the division registry: 17 divisions (academic, design,
  engineering, finance, game-development, gis, healthcare, marketing,
  paid-media, product, project-management, sales, security,
  spatial-computing, specialized, support, testing). `integrations/`,
  `strategy/`, `examples/`, and `scripts/` are explicitly not divisions.
- Division sizes relevant here: engineering 34 files, security 10, testing 8,
  project-management 7.
- Agent file format: Markdown with frontmatter `name`, `description`,
  `color`, `emoji`, `vibe`, followed by persona-style sections (identity and
  memory, core mission, critical rules, domain frameworks, success metrics).
  There is no `model` tier field and no least-privilege `tools:` field.
- Distribution model: files are copied into `~/.claude/agents/` for Claude
  Code; the external repo's own convert and install helper scripts generate
  and install per-tool variants (Cursor, OpenCode, Copilot, Aider, Windsurf)
  using its `tools.json` as the tool-to-path/format map. These helpers live in
  the upstream repository, not in this workspace.
- Orchestration appears as catalog agents (`agents-orchestrator` in
  specialized, `studio-producer` in project-management) rather than as an
  enforced supervisor/worker tier model.

### Contract comparison

| Dimension       | `hy-home.k8s` local roster                       | `agency-agents` catalog               |
| --------------- | ------------------------------------------------ | ------------------------------------- |
| Roster size     | 8 role-scoped agents                             | 230+ persona agents in 17 divisions   |
| Model policy    | Mandatory two-tier mapping per provider          | None; no model field                  |
| Tool boundary   | Least-privilege `tools:` per agent               | None; format has no tools field       |
| Governance link | `@import` scope + subagent protocol + postflight | Self-contained persona text           |
| Multi-provider  | Hand-maintained triple adapters (md/md/toml)     | Script-generated per-tool conversions |
| Selection       | Supervisor routing + harness catalog             | User picks agent by name/division     |

Direct import of external agent files is therefore not contract-compliant
here: an imported file would lack tier mapping, least-privilege tools,
scope imports, and postflight wiring, and would bypass the harness catalog
roster. Any adoption is an adaptation task, not a copy task.

### Gap analysis: improvement candidates for existing agents

Non-binding candidates informed by the external scan; each change routes
through Stage 03 agent-design specs before adapter edits:

- `incident-responder`: the external SRE persona frames incidents around
  SLOs, error budgets, and burn-rate severity. A bounded improvement is to
  reference SLO/error-budget vocabulary in the analysis workflow, without
  claiming live observability that this repo cannot verify statically.
- `code-reviewer` / `gitops-reviewer`: external review personas carry
  explicit success-metrics sections. Adding measurable review-outcome
  expectations (e.g., evidence citations per finding) is a low-risk body
  improvement consistent with the current contract.
- `doc-writer` / `wiki-curator`: already stronger than external counterparts
  because they bind to templates and canonical owners; no adoption needed.
- All workers: the external catalog's persona-memory sections conflict with
  this repo's knowledge-store rule (durable lessons live in
  `docs/00.agent-governance/memory/progress.md`, not inside agent files); do
  not import identity-memory blocks.

### Gap analysis: addition candidates

Candidates bounded to the WSL2+k3d ArgoCD GitOps platform purpose. `Adopt`
means a new local agent is plausibly justified; `Adapt` means fold the idea
into an existing agent; `Skip` means out of workspace scope:

| External pattern                                        | Verdict           | Rationale and routing                                                                                                                                                               |
| ------------------------------------------------------- | ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `engineering-devops-automator`                          | Adapt             | CI/pipeline upkeep is already split across `supervisor`, `k8s-implementer`, and validators; fold pipeline-maintenance prompts into existing scopes.                                 |
| `engineering-sre` (SLO/observability)                   | Adopt (candidate) | An `observability` worker for Prometheus/Grafana manifest review and SLO doc upkeep is a plausible future addition once observability manifests land; requires Stage 03 spec first. |
| `engineering-network-engineer`                          | Adopt (candidate) | Traefik/DNS/ingress review has no dedicated owner; today it falls to `k8s-implementer` + `security-auditor`. Justified only if network change volume grows.                         |
| `security-compliance-auditor`                           | Adapt             | Compliance-checklist framing can extend `security-auditor` guardrails; a second security agent is not warranted at this roster size.                                                |
| `testing-api-tester`, `testing-performance-benchmarker` | Skip              | No application API surface in this platform repo; tests are repo-static and shell-based.                                                                                            |
| `engineering-technical-writer`                          | Skip              | `doc-writer` plus the Stage 99 template contract already covers this with stronger routing.                                                                                         |
| `engineering-codebase-onboarding-engineer`              | Skip              | `wiki-curator` plus graphify output owns onboarding surfaces.                                                                                                                       |
| `agents-orchestrator` / `studio-producer`               | Skip              | Supervisor tier plus `harness-catalog.md` already own orchestration; catalog-agent orchestration would duplicate governance.                                                        |

### Implementation routing checklist

- [ ] Roster or tier changes: update `docs/00.agent-governance/model-policy.md`
      and `docs/00.agent-governance/harness-catalog.md` first, then adapters.
- [ ] New agent proposals: author an agent-design spec under
      `docs/03.specs/` and a Stage 04 task before creating adapter files.
- [ ] Adapter edits: keep `.claude/agents/*.md`, `.agents/agents/*.md`, and
      `.codex/agents/*.toml` aligned in the same change.
- [ ] Any external import: strip persona-memory blocks, add tier `model`,
      least-privilege `tools:`, scope `@import`, guardrails, and postflight.
- [ ] Record adoption or rejection decisions in
      `docs/00.agent-governance/memory/progress.md`.

## Sources

- `docs/00.agent-governance/harness-catalog.md` (checked 2026-07-06)
- `docs/00.agent-governance/model-policy.md` (checked 2026-07-06)
- `.claude/agents/` / `.agents/agents/` / `.codex/agents/` listings and
  `.claude/agents/supervisor.md` (checked 2026-07-06)
- <https://github.com/msitarzewski/agency-agents> repository metadata via
  GitHub API (checked 2026-07-06)
- <https://raw.githubusercontent.com/msitarzewski/agency-agents/main/divisions.json>
  (checked 2026-07-06)
- `agency-agents` `engineering/`, `security/`, `testing/`, and
  `project-management/` directory listings via GitHub API (checked 2026-07-06)
- <https://raw.githubusercontent.com/msitarzewski/agency-agents/main/engineering/engineering-sre.md>
  frontmatter/body sample (checked 2026-07-06)
- `agency-agents` `README.md` install/format/orchestration claims
  (checked 2026-07-06; README body claims are market scan material)

## Review and Freshness

- Review cadence: on source or roster change
- Last reviewed: 2026-07-06
- Next review trigger: local roster/adapter/model-policy changes, a decision
  to adopt any addition candidate, or major upstream catalog restructuring.

## Related Documents

- [Pack README](README.md)
- [Provider Harness Implementation Status Research](provider-implementation-status.md)
- [Harness and Loop Engineering Research](harness-and-loop-engineering.md)
- [Workspace Governance Baseline](workspace-governance-baseline.md)
- Canonical roster: `../../../00.agent-governance/harness-catalog.md`
- Canonical tier policy: `../../../00.agent-governance/model-policy.md`
- Subagent protocol: `../../../00.agent-governance/subagent-protocol.md`
- [Reference Template](../../../99.templates/templates/common/reference.template.md)
- [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
