# 2026-07-11 Workspace Engineering Implementation Audit

## Overview

This dated Stage 90 pack compares the Current
`docs/90.references/research/2026-07-07-wer/` benchmark with repository-backed
implementation evidence. It also records the approved design for integrating
the research and audit outputs requested on 2026-07-11.

The design uses targeted consolidation: strengthen the existing Current
research pack in place, create one new Current audit pack, and retain older
audits as historical or resolved baselines. The pack is descriptive and does
not redefine or modify active governance, templates, CI, agents, scripts,
manifests, credentials, or live operations.

## Snapshot Contract

- Pack role: Current.
- Snapshot date: 2026-07-11.
- Audit observation SHA: `a85df194bbb8ebc61187b905afaef7f95215cc2f`.
- Successor: none.
- Completion evidence: [Stage 04 Plan](../../../04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md)
  and [Stage 04 Task](../../../04.execution/tasks/2026-07-11-workspace-engineering-research-audit-integration.md).

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
├── governance-harness-loop-providers.md
├── sdlc-document-lifecycle-frontmatter.md
├── ci-qa-automation-pipeline-workflow.md
├── kubernetes-infrastructure-security.md
├── ai-agents-model-routing-vibe-coding.md
└── remediation-roadmap.md
```

The completed execution ledger now lives in the canonical
[Stage 04 Plan](../../../04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md),
with compact completion evidence in its paired
[Task](../../../04.execution/tasks/2026-07-11-workspace-engineering-research-audit-integration.md).
Neither document authorizes changes to the active owners audited here.

## Report Index

All five scored reports use the shared measurement contract below. The roadmap
normalizes their 80 actionable rows into 32 canonical findings; it does not
rescore or replace the source reports.

| Completed artifact | Scope | Applicable arithmetic | Actionable disposition |
| --- | --- | --- | --- |
| [Governance, Harness, Loop, and Provider Parity](governance-harness-loop-providers.md) | Governance, harness/loop, Claude, Codex, Gemini, and common system | `45/104` (43.3%); 26 applicable; no N/A | 17 Partial/Gap rows routed to the roadmap. |
| [SDLC, Document Lifecycle, and Frontmatter](sdlc-document-lifecycle-frontmatter.md) | Fourteen document families, lineage, transitions, and profile values | `56/108` (51.9%); 27 applicable; 4 N/A | 14 Partial/Gap rows routed; Release and consumer-free metadata remain excluded. |
| [CI, QA, Automation, Pipeline, and Workflow](ci-qa-automation-pipeline-workflow.md) | Delivery topology, QA/all-files obligations, and supply chain | `56/104` (53.8%); 26 applicable; 7 N/A | 8 Partial/Gap rows routed; consumer-free enterprise lanes remain excluded. |
| [Kubernetes Infrastructure and Security](kubernetes-infrastructure-security.md) | GitOps/platform foundations and `SEC-001` through `SEC-014` | `44/104` (42.3%); 26 applicable; no N/A | 15 Partial/Gap rows routed, including 2 P0 controls. |
| [AI Agents, Model Routing, Agency-Agents, and Vibe Coding](ai-agents-model-routing-vibe-coding.md) | Ten local roles, shared role system, upstream adoption, routing, and vibe coding | `51/116` (44.0%); 29 applicable; 2 N/A | 26 Partial/Gap rows routed; direct import and FinOps remain excluded. |
| [Integrated Remediation Roadmap](remediation-roadmap.md) | Deduplication, dependencies, target state, and canonical SDLC routes | 80 actionable source rows -> 32 canonical findings | Consolidated target selected; deferred/rejected lanes retain reopen triggers. |
| [Implementation Plan](../../../04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md) | Task-by-task execution and validation ledger | Tasks 1-13 complete | Both whole-branch reviews and final repository-static publication gates pass. |

## Successor or Resolution

Successor: none. This is the Current comparison owner until a separately
reviewed dated audit pack replaces the parent registry pointer.

## How to Work in This Area

1. Treat this README as the approved Stage 90 design and pack contract.
2. Use the Current research pack as benchmark context and the fixed audit
   commit as local implementation evidence.
3. Keep completed report links and score/disposition summaries synchronized.
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

## Repository Snapshot Details

The initial inventory baseline is commit
`ab3556b8d5a9ae6f469a751057d9ad5ef261cdf7`, observed on `2026-07-11`.
This base SHA freezes the starting document inventory and its checked digest.

The audit observation SHA is
`a85df194bbb8ebc61187b905afaef7f95215cc2f`, observed on `2026-07-11` after
Tasks 1-5 completed the Current research benchmark. Reports must read local
implementation evidence from that Git tree and label it `audit observation
SHA`; they must not substitute the evolving branch `HEAD`. Commits after this
SHA create audit outputs and do not become implementation evidence merely by
containing those outputs. The initial base remains the owner of the inventory
table below; the observation SHA owns implementation claims in Tasks 7-12.

Counts use top-level frontmatter `status` values from authored documents.
Every `README.md` is an index surface and is excluded from the counts below.

The checked recipe reads the pinned Git tree rather than the worktree and
limits `status` parsing to the first frontmatter block:

```bash
export LC_ALL=C
base=ab3556b8d5a9ae6f469a751057d9ad5ef261cdf7
git ls-tree -r --name-only "$base" -- \
  docs/01.requirements docs/02.architecture docs/03.specs \
  docs/04.execution docs/05.operations |
  awk '/\.md$/ && $0 !~ /\/README\.md$/ { print }' |
  sort |
  while IFS= read -r doc; do
    doc_status=$(git show "$base:$doc" |
      awk 'NR == 1 && $0 == "---" { fm=1; next }
        fm && $0 == "---" { exit }
        fm && /^status: / { sub(/^status: /, ""); print; exit }')
    printf '%s\t%s\n' "$doc" "${doc_status:-MISSING}"
  done |
  sha256sum
```

Observed output on `2026-07-11`:

```text
253fcd638675527ddc6d1df59a04628f3dadfff47a55de1ac9893a927a7f17fd  -
```

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

## Requirement Ownership Routing

The Current research pack
[owns the canonical requirement-to-research-to-audit map](../../research/2026-07-07-wer/README.md#canonical-requirement-to-research-to-audit-ownership-map).
Audit reports consume that map; this README owns only the snapshot, scoring,
and evidence contract.

## Completed Research Inputs

The completed [Current research pack](../../research/2026-07-07-wer/README.md)
is the benchmark input. Its topic owners are:

| Completed research owner | Benchmark responsibility |
| --- | --- |
| [Workspace Governance Baseline](../../research/2026-07-07-wer/workspace-governance-baseline.md) | Workspace purpose, governance, ownership, rules, and consolidation boundaries. |
| [Harness and Loop Engineering](../../research/2026-07-07-wer/harness-and-loop-engineering.md) | Harness, Observe/Plan/Act/Verify/Learn, retry, evaluation, recovery, compaction, MCP, and termination. |
| [Provider Implementation Status](../../research/2026-07-07-wer/provider-implementation-status.md) | Claude, Codex, Gemini, shared layers, model declarations, and runtime-evidence boundaries. |
| [Spec, SDLC, CI, QA, and Formatting](../../research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md) | Document families, lifecycle, lineage, frontmatter, release and incident readiness, and AI-agent QA obligations. |
| [Automation, Pipeline, Workflow, and QA](../../research/2026-07-07-wer/automation-pipeline-workflow-qa.md) | CI/CD topology, formatting, linting, automation, workflows, evidence artifacts, and delivery metrics. |
| [Kubernetes, Infrastructure, and Security](../../research/2026-07-07-wer/kubernetes-infrastructure-security.md) | Kubernetes, GitOps, Vault, ESO, network, policy, supply chain, and static-versus-live boundaries. |
| [AI Agents Roster and Gap Analysis](../../research/2026-07-07-wer/ai-agents-roster-and-gap-analysis.md) | Local agents, provider adapters, `agency-agents`, role gaps, model routing, and vibe-coding controls. |

## Report Interfaces and Topic Ownership

Each requested topic has exactly one primary audit owner through the canonical
map above. The following completed interfaces group those topics without
changing row-level ownership; secondary reports link to the primary owner
instead of copying volatile facts.

| Completed audit owner | Exclusive primary responsibility | Output interface |
| --- | --- | --- |
| [Governance/provider](governance-harness-loop-providers.md) | Workspace purpose, governance, rules, harness/loop controls, MCP, and provider implementation facts: adapter inventory and counts, provider/local declarations, native-provider semantics and loading/registration, settings/hooks/config, and entitlement/runtime availability evidence and confidence. It does not own role responsibilities, upstream roster comparison, role gaps, or adoption decisions. | Scored controls and canonical adapter/provider facts for the [agents/model/vibe audit](ai-agents-model-routing-vibe-coding.md), plus routed governance/provider findings for the [roadmap](remediation-roadmap.md). |
| [Lifecycle/frontmatter](sdlc-document-lifecycle-frontmatter.md) | Templates and integration guides; PRD through Reference/README roles; lifecycle, states, numbering, lineage, frontmatter, Release, Incident, and Postmortem readiness. | Scored lifecycle/metadata controls and target-state findings for the [roadmap](remediation-roadmap.md). |
| [CI/QA](ci-qa-automation-pipeline-workflow.md) | Scripts, CI/CD, QA, formatting, linting, syntax, automation, pipeline/workflow topology, and AI-agent all-files pre-commit obligations. | Scored delivery/quality controls and routed automation findings for the [roadmap](remediation-roadmap.md). |
| [Platform/security](kubernetes-infrastructure-security.md) | Kubernetes, infrastructure, GitOps, security, Vault, ESO, network and policy controls, supply chain, and static-versus-live evidence. | Scored platform/security controls and reconciled SEC findings for the [roadmap](remediation-roadmap.md). |
| [Agents/model/vibe](ai-agents-model-routing-vibe-coding.md) | Local role responsibilities, shared role bodies and instructions, upstream `agency-agents` roster/comparison, role gaps and adoption decisions, vibe coding, and role-specific default/escalation/fallback/eval recommendations. It consumes and links adapter inventory/count, provider metadata, native semantics/loading, and availability facts from the governance/provider report; it does not duplicate them. | Scored role and vibe-coding controls plus model-routing recommendations for the [roadmap](remediation-roadmap.md). |
| [Integrated roadmap](remediation-roadmap.md) | Cross-report deduplication, dependency order, target-state choice, and integrated priority ordering only. | One follow-up register with canonical PRD, ARD, ADR, Spec, Plan, or Task routes and acceptance evidence. |

## Audit Method

Every applicable control row uses these exact fields, in this order:

| Field | Required content |
| --- | --- |
| `ID` | Stable report-local control identifier. |
| `Benchmark` | External or Current-research benchmark and source. |
| `Expected control` | Testable repository or operating contract being assessed. |
| `Repository evidence` | Exact paths, commands, or observations fixed to the audit observation SHA. |
| `Maturity` | One shared maturity value below, or `N/A` with an exclusion reason. |
| `Verdict` | `Implemented`, `Partial`, `Gap`, or `Not in scope`. |
| `Confidence` | `Verified repo-static`, `Unverified live`, or `Conditional`. |
| `Gap` | Missing, corrective, complementary, unnecessary, or excluded element. |
| `Recommendation` | Bounded next action; Stage 90 does not implement it. |
| `Priority` | One `P0`-`P3` value from the shared vocabulary below for every `Partial`, `Gap`, or otherwise actionable finding; otherwise `N/A — no action`. |
| `Follow-up owner` | One canonical PRD, ARD, ADR, Spec, Plan, or Task route for every actionable finding; otherwise `N/A — no action`. |
| `Acceptance evidence` | Measurable proof required to close every actionable finding; otherwise `N/A — no action`. |

Rows may add notes outside the table, but must not rename, merge, or omit these
fields. Every `Partial`, `Gap`, or otherwise actionable finding must supply a
`P0`-`P3` priority, one canonical follow-up owner, and measurable acceptance
evidence. An `Implemented`, `Not in scope`, or `Maturity: N/A` control with no
action uses the exact value `N/A — no action` in all three fields; reports must
not invent remediation to populate them. `Not in scope` controls also state the
exclusion in `Gap` and remain outside the category denominator.

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

### Shared Priority Vocabulary

| Priority | Meaning |
| --- | --- |
| `P0 immediate safety` | Credible immediate risk to safety, secrets, access, data, or control integrity; stop or contain through the canonical owner before continuing affected work. |
| `P1 near-term integrity` | Material correctness, security, governance, or delivery-integrity gap that should be resolved before the next affected change or release. |
| `P2 planned improvement` | Bounded improvement with no demonstrated immediate integrity failure; schedule through the normal backlog and SDLC route. |
| `P3 optional/telemetry-gated` | Optional optimization or role/control expansion that proceeds only when telemetry, evaluation, or repeated demand justifies it. |

Priority never grants permission to mutate an active or live owner. Even a
`P0 immediate safety` finding is routed out of Stage 90 for separately approved
containment and remediation.

### Contradiction Ownership

| Contradiction topic | Sole audit owner | Secondary-report rule |
| --- | --- | --- |
| Document lifecycle, states, lineage, and frontmatter | `sdlc-document-lifecycle-frontmatter.md` | Link to the owner; do not restate counts or transitions. |
| Adapter inventory/count, provider/local declarations, native-provider semantics and loading/registration, settings/hooks/config, and entitlement/runtime availability evidence and confidence | `governance-harness-loop-providers.md` | Link to the owner; do not duplicate adapter counts, provider metadata, native semantics/loading, or availability facts. |
| CI job DAG, workflow counts, and QA wiring | `ci-qa-automation-pipeline-workflow.md` | Link to the owner; do not reconstruct the DAG elsewhere. |
| Kubernetes, GitOps, infrastructure, and security evidence | `kubernetes-infrastructure-security.md` | Link to the owner; preserve repo-static versus live distinctions. |
| Local role responsibilities, upstream `agency-agents` roster/comparison, role gaps, and adoption decisions | `ai-agents-model-routing-vibe-coding.md` | Link to the owner; consume Task 7 adapter inventory/count and native-provider facts, and do not let upstream volume redefine local need. |
| Role-specific model default, escalation, fallback, eval recommendations, and adoption decisions | `ai-agents-model-routing-vibe-coding.md` | Consume and link provider declarations and availability confidence from `governance-harness-loop-providers.md`; do not reopen those facts. |
| Integrated roadmap priority and dependency order | `remediation-roadmap.md` | Source reports retain row findings; the roadmap alone deduplicates and orders them. |

When a contradiction is found, its sole owner records both claims, their source
and cutoff or observation SHA, the winning fact, and the reason. A secondary
report links to that closure. It does not create a second truth owner.

## Evidence Boundary

- Repository claims are fixed to audit observation SHA
  `a85df194bbb8ebc61187b905afaef7f95215cc2f`.
- Provider and model research retains the approved
  `2026-07-10 10:00 KST` cutoff and prioritizes official sources.
- The `agency-agents` comparison uses a pinned upstream commit.
- Vibe-coding context is separated from authoritative controls such as secure
  development, review, test, provenance, and approval guidance.
- Static desired state never proves live Kubernetes, secret, policy, network,
  provider, or deployment enforcement.
- Facts, local observations, and inference are labeled separately.

Excluded live lanes are Kubernetes API and controller behavior; Argo CD sync,
health, drift, and reconciliation; Vault and ESO runtime, TLS, authentication,
secret values, rotation, and delivery; NetworkPolicy enforcement; provider
native loading, account/auth entitlement, permissions, model resolution, and
runtime behavior; remote GitHub Actions, rulesets, and CI results; credentials,
deployments, and external-service state. These lanes remain `Unverified live`
or `Conditional`; repository declarations and static PASS results cannot
promote them to maturity 4.

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

## Completion Evidence

The [completed Plan](../../../04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md)
preserves the thirteen-task ledger, logical publication boundaries, review
record, and validation commands. The paired
[Task](../../../04.execution/tasks/2026-07-11-workspace-engineering-research-audit-integration.md)
summarizes completed tasks, known publication commits, repository-static
validation, and the no-live/no-secret boundary. The final source correction is
commit `14198a7`; the Current pack publication is commit `184d13e`.

## Final Review and Freshness

- Final review status: specification/content PASS and evidence/quality PASS
  after review-fix commit `14198a7`.
- Review basis: complete branch diff from fixed base
  `ab3556b8d5a9ae6f469a751057d9ad5ef261cdf7` through the corrected review head.
- Last reviewed: 2026-07-11.
- Evidence boundary: Stage 90 documentation and repository-static validation
  only; no live cluster, provider runtime, remote CI/settings, credential,
  secret-value, publish, push, or merge operation was inspected or performed.
- Next review trigger: a Current research owner, audit owner, source cutoff,
  observation SHA, score/verdict, remediation disposition, canonical pointer,
  or linked active implementation owner changes.
- Refresh method: preserve this dated snapshot, choose a new observation SHA,
  rerun the 56-row ownership and 80-to-32 disposition checks, recalculate every
  report score/N/A distribution, revalidate sources and counts, then repeat both
  whole-branch reviews before changing Current pointers.

## Related Documents

- [Audits README](../README.md)
- [Current Workspace Engineering Research Pack](../../research/2026-07-07-wer/README.md)
- [Implementation Plan](../../../04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md)
- [Implementation Task](../../../04.execution/tasks/2026-07-11-workspace-engineering-research-audit-integration.md)
- [Governance, Harness, Loop, and Provider Parity](governance-harness-loop-providers.md)
- [SDLC, Document Lifecycle, and Frontmatter](sdlc-document-lifecycle-frontmatter.md)
- [CI, QA, Automation, Pipeline, and Workflow](ci-qa-automation-pipeline-workflow.md)
- [Kubernetes Infrastructure and Security](kubernetes-infrastructure-security.md)
- [AI Agents, Model Routing, Agency-Agents, and Vibe Coding](ai-agents-model-routing-vibe-coding.md)
- [Integrated Remediation Roadmap](remediation-roadmap.md)
- [Reference Template](../../../99.templates/templates/common/reference.template.md)
