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
map above. The following interfaces group those topics without changing that
row-level ownership. Report paths remain code literals until their files
exist; secondary reports link to the primary owner instead of copying volatile
facts.

| Planned report owner | Exclusive primary responsibility | Output interface |
| --- | --- | --- |
| `governance-harness-loop-providers.md` | Workspace purpose, roles, governance, rules, harness/loop controls, MCP, Claude, Codex, Gemini, shared provider layers, and provider implementation status. | Scored controls and routed governance/provider findings for `remediation-roadmap.md`. |
| `sdlc-document-lifecycle-frontmatter.md` | Templates and integration guides; PRD through Reference/README roles; lifecycle, states, numbering, lineage, frontmatter, Release, Incident, and Postmortem readiness. | Scored lifecycle/metadata controls and target-state findings for `remediation-roadmap.md`. |
| `ci-qa-automation-pipeline-workflow.md` | Scripts, CI/CD, QA, formatting, linting, syntax, automation, pipeline/workflow topology, and AI-agent all-files pre-commit obligations. | Scored delivery/quality controls and routed automation findings for `remediation-roadmap.md`. |
| `kubernetes-infrastructure-security.md` | Kubernetes, infrastructure, GitOps, security, Vault, ESO, network and policy controls, supply chain, and static-versus-live evidence. | Scored platform/security controls and reconciled SEC findings for `remediation-roadmap.md`. |
| `ai-agents-model-routing-vibe-coding.md` | Local AI-agent roster and adapters, `agency-agents`, task-model routing, provider availability boundaries, and vibe coding. | Scored role/model controls and routed agent findings for `remediation-roadmap.md`. |
| `remediation-roadmap.md` | Cross-report deduplication, dependency order, target-state choice, and integrated priority ordering only. | One follow-up register with canonical PRD, ARD, ADR, Spec, Plan, or Task routes and acceptance evidence. |

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
| `Priority` | One `P0`-`P3` value from the shared vocabulary below. |
| `Follow-up owner` | One canonical PRD, ARD, ADR, Spec, Plan, or Task route. |
| `Acceptance evidence` | Measurable proof required to close the recommendation. |

Rows may add notes outside the table, but must not rename, merge, or omit these
fields. `Not in scope` controls use `Maturity: N/A`, state the exclusion in
`Gap`, and remain outside the category denominator.

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
| Provider implementation and native/local parity | `governance-harness-loop-providers.md` | Link to the owner; keep model-routing recommendations separate. |
| CI job DAG, workflow counts, and QA wiring | `ci-qa-automation-pipeline-workflow.md` | Link to the owner; do not reconstruct the DAG elsewhere. |
| Kubernetes, GitOps, infrastructure, and security evidence | `kubernetes-infrastructure-security.md` | Link to the owner; preserve repo-static versus live distinctions. |
| Local and upstream agent roster facts | `ai-agents-model-routing-vibe-coding.md` | Link to the owner; upstream volume cannot redefine local need. |
| Model declarations, availability, and task routing | `ai-agents-model-routing-vibe-coding.md` | Link to the owner; provider report supplies implementation facts only. |
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
