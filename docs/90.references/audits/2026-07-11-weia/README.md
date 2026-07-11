# 2026-07-11 Workspace Engineering Implementation Audit

## Overview

This dated Stage 90 pack will compare the Current
`docs/90.references/research/2026-07-07-wer/` benchmark with repository-backed
implementation evidence. It also records the approved design for integrating
the research and audit outputs requested on 2026-07-11.

The design uses targeted consolidation: strengthen the existing Current
research pack in place, create one new Current audit pack, and retain older
audits as historical or resolved baselines. The pack is descriptive and does
not redefine or modify active governance, templates, CI, agents, scripts,
manifests, credentials, or live operations.

## Audience

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Strengthen only the Current research pack and Stage 90 audit references.
- Compare external benchmarks with the workspace implementation at an exact
  repository commit.
- Cover governance, harness and loop engineering, Claude/Codex/Gemini,
  spec-driven development, the full document lifecycle and frontmatter,
  CI/CD, QA, formatting, linting, automation, pipelines, workflows,
  Kubernetes, infrastructure, security, AI agents, model routing,
  `agency-agents`, and vibe coding.
- Record missing, corrective, complementary, unnecessary, relocation,
  consolidation, and full-redesign options.
- Route active changes through follow-up PRD, ARD, ADR, Spec, Plan, or Task
  proposals with acceptance criteria.

### Out of Scope

- Changes to Stage 00 rules, Stage 99 templates, CI workflows, pre-commit
  configuration, agent adapters, provider settings, scripts, manifests, or
  operations documents.
- Live cluster, Argo CD, Vault, ESO, provider runtime, account, secret,
  deployment, or external-service validation.
- Push, pull request, or merge without separate approval.

## Design Decision

Three approaches were considered:

1. strengthen the Current research pack in place and create a new audit pack;
2. replace both research and audit packs with a new taxonomy; or
3. consolidate research into one monolithic benchmark.

Approach 1 was approved. It preserves the already hardened research evidence,
avoids duplicate Current research snapshots, and concentrates new work on the
known gaps: stale audits, frontmatter and lifecycle analysis, vibe coding,
AI-agent pre-commit obligations, implementation scoring, and one Current audit
pointer.

## Structure

```text
2026-07-11-weia/
├── README.md
├── implementation-plan.md
├── governance-harness-loop-providers.md
├── sdlc-document-lifecycle-frontmatter.md
├── ci-qa-automation-pipeline-workflow.md
├── kubernetes-infrastructure-security.md
├── ai-agents-model-routing-vibe-coding.md
└── remediation-roadmap.md
```

Until a report exists, its path remains a code literal rather than a broken
Markdown link.

The [implementation plan](implementation-plan.md) is the durable execution
ledger for this Stage 90-only integration. It does not authorize changes to
the active owners it audits.

## How to Work in This Area

1. Treat this README as the approved Stage 90 design and pack contract.
2. Use the Current research pack as benchmark context and the fixed audit
   commit as local implementation evidence.
3. Keep planned reports as code literals until their files exist.
4. Require content and evidence review for each logical unit.
5. Route every proposed active change to a canonical follow-up SDLC owner;
   never implement it from Stage 90.

## Link Basis

This README is located at
`docs/90.references/audits/2026-07-11-weia/`.

- Same-pack report links use `./` after the report exists.
- The parent audits index uses `../README.md`.
- Research pack links use `../../research/...`.
- Other documentation stages use `../../../<stage>/...`.
- Repository-root evidence uses `../../../../<path>`.
- Planned or conditional artifacts remain code literals.

## Repository Snapshot Contract

The initial inventory baseline is commit
`ab3556b8d5a9ae6f469a751057d9ad5ef261cdf7`, observed on `2026-07-11`.
This base SHA freezes the starting repository facts; it is distinct from the
final audit observation SHA, which the completed pack records separately after
all audit artifacts are present. Audit reports must say which SHA supports
each repository claim and must not silently substitute the evolving branch
HEAD for the initial baseline.

Counts use top-level frontmatter `status` values from authored documents.
Every `README.md` is an index surface and is excluded from the counts below.

| Family and path basis | Authored inventory | Status at initial baseline |
| --- | --- | --- |
| PRD — `docs/01.requirements/*.md` | 4 | 4 `active` |
| ARD — `docs/02.architecture/requirements/*.md` | 4 | 4 `active` |
| ADR — `docs/02.architecture/decisions/*.md` | 9 | 9 `accepted` |
| Spec — `docs/03.specs/*/spec.md` | 20 | 16 `draft`; 4 `active` |
| Agent design — `docs/03.specs/*/agent-design.md` | 1 | 1 `draft` |
| Plan — `docs/04.execution/plans/*.md` | 41 | 41 `done` |
| Task — `docs/04.execution/tasks/*.md` | 43 | 43 `done` |
| Guide — `docs/05.operations/guides/*.md` | 8 | 8 `active` |
| Policy — `docs/05.operations/policies/*.md` | 7 | 7 `active` |
| Runbook — `docs/05.operations/runbooks/*.md` | 9 | 9 `active` |
| Incident — `docs/05.operations/incidents/*.md` | 0 | No authored record; `README.md` is index-only. |
| Postmortem — `docs/05.operations/incidents/` postmortem records | 0 | No authored record. |

## Research Ownership

| Current research owner | Approved strengthening responsibility |
| --- | --- |
| `README.md` | Requirement-to-research-to-audit traceability, source cutoff, Current pointer, and contradiction closure. |
| `workspace-governance-baseline.md` | Workspace purpose, roles, rules, environment, ownership, and consolidation boundaries. |
| `harness-and-loop-engineering.md` | Observe/Plan/Act/Verify/Learn loop, retry, evaluation, recovery, compaction, MCP, and termination controls. |
| `provider-implementation-status.md` | Claude, Codex, Gemini native/local surfaces, common contracts, model declaration, and runtime-evidence boundaries. |
| `spec-sdlc-ci-qa-formatting.md` | Document roles, 01-to-05 flow, numbering, state transitions, lineage, frontmatter, release, incident, postmortem, and AI-agent pre-commit obligations. |
| `kubernetes-infrastructure-security.md` | Kubernetes, GitOps, Vault, ESO, policy, network, supply-chain, and static-versus-live evidence. |
| `automation-pipeline-workflow-qa.md` | CI/CD, QA, formatting, linting, syntax, automation, pipeline, workflow, evidence artifacts, and delivery metrics. |
| `ai-agents-roster-and-gap-analysis.md` | Local roster, provider adapters, `agency-agents`, role gaps, model routing, instructions, and vibe-coding controls. |

### Research-to-Audit Topic Ownership

The following map closes research-to-audit ownership for every requested
cross-cutting topic. Each row has one primary research owner and one planned
audit owner; planned paths remain code literals until their reports exist.

| Requested topic | Primary Current research owner | Planned audit owner |
| --- | --- | --- |
| Frontmatter keys and values | `spec-sdlc-ci-qa-formatting.md` | `sdlc-document-lifecycle-frontmatter.md` |
| Document state transitions | `spec-sdlc-ci-qa-formatting.md` | `sdlc-document-lifecycle-frontmatter.md` |
| Semantic lineage | `spec-sdlc-ci-qa-formatting.md` | `sdlc-document-lifecycle-frontmatter.md` |
| Release readiness | `spec-sdlc-ci-qa-formatting.md` | `sdlc-document-lifecycle-frontmatter.md` |
| Incident readiness | `spec-sdlc-ci-qa-formatting.md` | `sdlc-document-lifecycle-frontmatter.md` |
| Postmortem readiness | `spec-sdlc-ci-qa-formatting.md` | `sdlc-document-lifecycle-frontmatter.md` |
| AI-agent `pre-commit run --all-files` obligation | `spec-sdlc-ci-qa-formatting.md` | `ci-qa-automation-pipeline-workflow.md` |
| Vibe coding | `ai-agents-roster-and-gap-analysis.md` | `ai-agents-model-routing-vibe-coding.md` |
| `agency-agents` comparison | `ai-agents-roster-and-gap-analysis.md` | `ai-agents-model-routing-vibe-coding.md` |
| Task-model routing | `ai-agents-roster-and-gap-analysis.md` | `ai-agents-model-routing-vibe-coding.md` |

## Audit Method

Every applicable control will record:

1. external benchmark and source;
2. expected control or operating contract;
3. current repository evidence;
4. implementation maturity and evidence confidence;
5. missing, corrective, complementary, or unnecessary elements;
6. recommendation and priority; and
7. follow-up SDLC owner and acceptance criteria.

### Shared Maturity, Confidence, and Verdict Contract

| Maturity | Meaning |
| --- | --- |
| `0 absent` | Control is absent. |
| `1 documented/routed` | Control is documented or routed only. |
| `2 repository-static` | Control is present as repository-static evidence. |
| `3 deterministic local+CI enforcement` | Control is deterministically enforced in local validation and CI. |
| `4 runtime/operational evidence` | Control is supported by runtime or operational evidence. |

Category implementation is
`sum(maturity) / (4 * applicable controls)`. The report must disclose the
numerator, denominator, and every N/A exclusion. Human verdicts remain
`Implemented`, `Partial`, `Gap`, or `Not in scope`. Evidence confidence is
`Verified repo-static`, `Unverified live`, or `Conditional`. Maturity,
confidence, and verdict are separate fields: a score does not imply stronger
confidence or a different human verdict.

## Evidence Boundary

- Repository claims are fixed to the implementation audit commit recorded by
  the completed pack.
- Provider and model research retains the approved
  `2026-07-10 10:00 KST` cutoff and prioritizes official sources.
- The `agency-agents` comparison uses a pinned upstream commit.
- Vibe-coding context is separated from authoritative controls such as secure
  development, review, test, provenance, and approval guidance.
- Static desired state never proves live Kubernetes, secret, policy, network,
  provider, or deployment enforcement.
- Facts, local observations, and inference are labeled separately.

## SDLC and Frontmatter Design

The audit compares three target states:

- `Minimal`: preserve the tree and repair only currentness, state, and links;
- `Consolidated`: centralize duplicated lifecycle summaries and add deliberate
  semantic traceability; and
- `Full redesign`: migrate to document identifiers and lineage-led contracts.

`Consolidated` is the default recommendation unless evidence supports a larger
change. Full redesign must state blast radius, prerequisites, migration,
rollback, and follow-up decision owners.

Frontmatter analysis begins with the current five-key contract and recommends
profile-specific metadata only when an actual automation consumer is defined.
It will examine ownership, family-specific states and transitions, lineage,
supersession, review freshness, reference source checks, incident identity and
severity, placeholder rejection, and date validity without moving all body
content into metadata.

## Cross-Category Decision Rules

- File-count parity is not provider runtime or behavioral parity.
- `.agents` is not described as a native Gemini CLI implementation.
- API model catalogs do not prove local CLI or account availability.
- A tracked formatter configuration does not prove execution or CI
  enforcement.
- Optional static tools do not prove deterministic CI coverage.
- Unchecked Vault, ESO, NetworkPolicy, Argo CD, and Kubernetes behavior remains
  live-Unverified.
- Upstream agent volume does not justify local role proliferation.
- Vibe coding is limited to bounded exploration; infrastructure and security
  changes remain specification-, evidence-, review-, and approval-gated.
- `pre-commit run --all-files` is evaluated as a risk-based pre-PR/pre-merge
  obligation and a mandatory check for hook, toolchain, global formatting, or
  validation-contract changes, not as an after-every-edit requirement.

## Planned Logical Commits

1. approved design and audit-pack contract;
2. Current research index and traceability;
3. SDLC, document lifecycle, and frontmatter research;
4. AI agents, model routing, and vibe-coding research;
5. remaining research fact and source refresh;
6. audit method and pack index;
7. governance, harness, loop, and provider audit;
8. SDLC, lifecycle, and frontmatter audit;
9. CI/CD, QA, automation, pipeline, and workflow audit;
10. Kubernetes, infrastructure, and security audit;
11. AI agents, model routing, `agency-agents`, and vibe-coding audit;
12. remediation roadmap and follow-up SDLC routes; and
13. Current pointer reconciliation and final verification corrections.

## Execution and Review

- Work is isolated under `.worktrees/` on a `codex/` branch.
- Subagent-driven implementation assigns non-overlapping file ownership.
- Each logical unit receives content and evidence review before acceptance.
- A whole-branch review checks contradictions and coverage at the end.
- Validation includes repository quality gates, changed-file pre-commit,
  final all-files pre-commit, link/frontmatter/routing checks, source and count
  verification, requirement coverage, and a path guard proving active files
  were not changed.

## Approval Record

The user approved the Stage 90-only scope, approach 1, artifact ownership,
audit method, maturity model, evidence boundary, SDLC/frontmatter design,
cross-category comparison rules, and execution strategy on 2026-07-11.

## Related Documents

- [Audits README](../README.md)
- [Current Workspace Engineering Research Pack](../../research/2026-07-07-wer/README.md)
- [Reference Template](../../../99.templates/templates/common/reference.template.md)
