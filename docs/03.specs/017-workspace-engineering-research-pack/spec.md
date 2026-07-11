---
title: 'Workspace Engineering Research Pack Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-07-11
---

# Workspace Engineering Research Pack Technical Specification (Spec)

## Overview

This document defines the implementation contract for a dated, repo-first
research pack under
`docs/90.references/research/2026-07-04-wer/`.
The pack will synthesize the workspace purpose, roles, CI/CD, QA, formatting,
linting, automation, pipelines, workflows, operating contracts, templates,
scripts, integration guides, SDLC, governance, rules, Kubernetes,
infrastructure, and security.

The work is documentation-only. It must not mutate live Kubernetes, Argo CD,
Vault, cloud resources, GitHub remote state, credentials, or third-party
systems.

The brainstorming skill's default `docs/superpowers/specs/**` location is not
used because this repository's quality gate forbids `docs/superpowers` as a
top-level docs folder. Stage 03 is the repo-approved design/spec owner.

## Strategic Boundaries & Non-goals

In scope:

- Create a dated research pack folder under `docs/90.references/research/`.
- Move the four current flat research references into the dated pack folder.
- Refresh those four references with current repo evidence and verified
  official or primary external sources.
- Add two focused references for Kubernetes/infrastructure/security and
  automation/pipeline/workflow/QA.
- Update `docs/90.references/research/README.md` and parent reference indexes
  so the dated pack is discoverable and stale flat links are removed.
- Record source checked dates, freshness triggers, authority boundaries,
  market-scan limitations, and related documents.
- Track execution and validation through Stage 04 plan/task evidence and the
  progress ledger.

Out of scope:

- Live cluster, cloud, Vault, GitHub remote, or provider runtime mutation.
- Secret value inspection, credential regeneration, or certificate changes.
- Replacing current CI workflow architecture or installing external tools.
- Changing active governance policy except where a later implementation task
  explicitly routes documented drift to the canonical owner.
- Treating market scan material as authoritative.

## Related Inputs

- **PRD**: No separate PRD exists. The upstream requirement is the approved
  user request to build a dated workspace engineering research pack, move the
  existing four research documents into it, and include external source-backed
  analysis.
- **ARD**: No separate ARD exists. The architectural baseline is the current
  Stage 00 to Stage 99 documentation taxonomy and the existing
  `docs/90.references/**` reference contract.
- **Prior Specs**:
  - [Workspace Harness Research Pack](../009-workspace-harness-research-pack/spec.md)
  - [Workspace Harness Implementation Audit Pack](../010-workspace-harness-implementation-audit-pack/spec.md)
  - [Active Control Surface Governance Hardening](../016-active-control-surface-governance-hardening/spec.md)

Repository inputs:

- [90.references README](../../90.references/README.md)
- [Research README](../../90.references/research/README.md)
- [Reference Template](../../99.templates/templates/common/reference.template.md)
- [Agent Governance Hub](../../00.agent-governance/README.md)
- [Harness Catalog](../../00.agent-governance/harness-catalog.md)
- [Harness Implementation Map](../../00.agent-governance/harness-implementation-map.md)
- [Repository Quality Gate](../../../scripts/validate-repo-quality-gates.sh)
- [Harness Validation Wrapper](../../../scripts/validate-harness.sh)

## Contracts

- **Config Contract**:
  - No runtime configuration, provider adapter, workflow job, GitOps manifest,
    or secret file changes are required by this spec.
  - The research pack lives only under
    `docs/90.references/research/2026-07-04-wer/`.
  - The former flat research files are moved, not duplicated, so there is one
    current path for each moved reference.
- **Data / Interface Contract**:
  - Each authored reference uses `type: content/reference` frontmatter and the
    required reference sections from
    `docs/99.templates/templates/common/reference.template.md`.
  - `README.md` files remain folder entrypoints and do not copy the complete
    reference template.
  - Source claims include source checked dates and freshness triggers.
  - Market scan findings are labeled non-authoritative and cannot override
    official or repo-backed evidence.
- **Governance Contract**:
  - `docs/90.references/**` remains durable lookup material, not active
    policy, runbook, release gate, or runtime permission owner.
  - Active policy changes belong to Stage 00, Stage 05, workflows, scripts, or
    templates according to existing ownership.
  - External networked research is read-only. Posting, publishing, pushing,
    merging, credential mutation, or third-party state changes require separate
    human approval.

## Core Design

- **Component Boundary**:
  - `README.md`: pack purpose, reading order, file index, source priority,
    authority boundary, and market-scan warning.
  - `workspace-governance-baseline.md`: repo-first baseline for workspace
    purpose, roles, operating contract, templates, scripts, integration guides,
    SDLC, governance, system structure, rules, and current evidence lanes.
  - `harness-and-loop-engineering.md`: harness engineering and loop
    engineering definitions, elements, workspace application requirements,
    environment/rule needs, and implementation checklist items.
  - `provider-implementation-status.md`: Claude, Codex, and Gemini harness and
    loop capability comparison, including common environment, shared rules, and
    known differences between upstream capability and repo implementation.
  - `spec-sdlc-ci-qa-formatting.md`: spec-driven development, SDLC, CI/CD, QA,
    formatting, linting, syntax validation, and repo validation matrix mapping.
  - `kubernetes-infrastructure-security.md`: Kubernetes, infrastructure,
    GitOps, secrets, policy-as-code, supply-chain, and security source
    analysis.
  - `automation-pipeline-workflow-qa.md`: automation, pipeline, workflow, CI
    job graph, validation loops, QA evidence lanes, formatting/linting
    integration, and implementation checklist material.
- **Key Dependencies**:
  - Existing Stage 00 governance, Stage 90 references, Stage 99 templates,
    `.github`, scripts, GitOps, infrastructure, policy, tests, and Traefik
    evidence.
  - Official or primary external documentation verified during implementation.
  - Bounded market scan material labeled non-authoritative.
- **Tech Stack**:
  - Markdown, existing reference template, repository validation scripts,
    Git history, web research, and Stage 04 evidence records.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - The pack is a set of Markdown reference documents and README indexes.
  - The moved references retain their filenames and are updated in place after
    `git mv`.
  - New reference files use the same frontmatter keys as other current
    `content/reference` documents: `title`, `type`, `status`, `owner`, and
    `updated`.
- **Migration / Transition Plan**:
  - Create the dated pack folder.
  - Move the four current flat research references into it.
  - Update research and parent indexes.
  - Run stale-link focused scans.
  - Refresh content and add new references in later logical commits.

## Interfaces & Data Structures

### Research Pack Contract

```typescript
interface WorkspaceEngineeringResearchPack {
  root: "docs/90.references/research/2026-07-04-wer";
  references: [
    "workspace-governance-baseline.md",
    "harness-and-loop-engineering.md",
    "provider-implementation-status.md",
    "spec-sdlc-ci-qa-formatting.md",
    "kubernetes-infrastructure-security.md",
    "automation-pipeline-workflow-qa.md",
  ];
  requiredReferenceSections: [
    "Overview",
    "Purpose",
    "Reference Type",
    "Authority Boundary",
    "Scope",
    "Definitions / Facts",
    "Sources",
    "Review and Freshness",
    "Related Documents",
  ];
  sourcePriority: [
    "canonical repository owners",
    "official or primary external sources",
    "repo-backed evidence",
    "official issue trackers or release notes",
    "non-authoritative market scan material",
  ];
}
```

## API Contract (If Applicable)

No external API is introduced.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Documentation and governance researcher operating under the
  repo-local docs, meta, QA, infra, and security scopes.
- **Inputs**: User-approved design, repo evidence, existing research
  references, official external sources, market scan sources, templates, and
  validation output.
- **Outputs**: Dated research pack folder, moved/updated references, new
  references, updated indexes, Stage 04 evidence, and progress memory.
- **Success Definition**: The dated pack exists, stale flat paths are removed,
  required topics are covered, source authority is explicit, validation passes,
  and no live or external mutation occurs.

## Tools & Tool Contract (If Applicable)

- **Tool List**:
  - `rg` and shell readers for repo evidence.
  - Web research for current external source verification.
  - `git mv` for moving existing research references.
  - `apply_patch` for manual document edits.
  - Repository validation scripts.
- **Permission Boundary**:
  - Read-only external research is allowed.
  - Remote push, PR creation, merge, publishing, credential changes, paid jobs,
    third-party mutation, live Kubernetes, Vault, cloud, or GitHub settings
    changes are not allowed without separate approval.
- **Failure Handling**:
  - If external sources conflict, official or repo-backed sources outrank
    market scan material.
  - If validation fails, fix the owning reference, index, template route, or
    stale link before proceeding.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**:
  - Follow repo-first and official-source-first research order.
  - Keep market scan material non-authoritative.
  - Keep active policy out of `docs/90.references/**`.
- **Policy Constraints**:
  - Respect approval boundaries for live mutation and external state changes.
  - Preserve one current path per moved research reference.
- **Versioning Rule**:
  - Use the dated pack folder as the version boundary for this refresh.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**:
  - Stage 04 plan and task records own execution order, evidence, and status.
- **Long-term Memory**:
  - `docs/00.agent-governance/memory/progress.md` records completion evidence
    and reusable routing lessons.
- **Retrieval Boundary**:
  - The research pack provides lookup context only. It does not become an
    execution rule source.

## Guardrails (If Applicable)

- **Input Guardrails**:
  - Verify external claims with web research before updating current source
    statements.
  - Treat missing or changed provider behavior as unknown until primary source
    evidence exists.
- **Output Guardrails**:
  - Every reference has authority boundary, sources, and freshness metadata.
  - Market scan text is labeled non-authoritative.
  - README files remain entrypoints, not policy bodies.
- **Blocked Conditions**:
  - Required source cannot be verified.
  - Moving references would leave unresolved stale links that cannot be fixed.
  - Repo quality gate fails repeatedly with unresolved ownership.
- **Escalation Rule**:
  - Stop and ask for clarification if a required source, canonical owner, or
    scope boundary is ambiguous enough to change the pack structure.

## Evaluation (If Applicable)

- **Eval Types**:
  - Structural validation, stale-link scans, source-authority review, and
    repo-static validation.
- **Metrics**:
  - All approved output files exist in the dated pack.
  - No current index points to removed flat research paths.
  - Required reference sections are present.
  - Repository quality gates pass.
- **Datasets / Fixtures**:
  - Existing Stage 90 research references, Stage 00 governance, Stage 99
    templates, scripts, workflow files, GitOps manifests, infrastructure
    docs, policy files, and official external documentation.
- **How to Run**:
  - Use the verification commands in this spec and the later Stage 04 plan.

## Edge Cases & Error Handling

- **Existing links to flat references**:
  - Update links to the dated pack path in the same move commit or an adjacent
    index commit.
- **Source drift during writing**:
  - Record the checked date and keep claims narrowly tied to the verified
    source.
- **Provider capability mismatch**:
  - Distinguish upstream provider capability from repo implementation status.
- **Optional tool absence**:
  - Report optional lint/policy tool absence as SKIP or fallback evidence, not
    as full coverage.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: `docs/superpowers/**` or another non-canonical path is
  introduced.
  - **Fallback**: Move design and execution artifacts into the repo-approved
    Stage 03/04 taxonomy.
  - **Human Escalation**: Only needed if the user requires a path forbidden by
    the repository quality gate.
- **Failure Mode**: External source claims cannot be verified.
  - **Fallback**: Mark the claim as unknown or remove it.
  - **Human Escalation**: Ask before using non-primary sources for a material
    conclusion.
- **Failure Mode**: Validation fails because of stale links after moving files.
  - **Fallback**: Fix links and indexes before content refresh work continues.
  - **Human Escalation**: Ask only if multiple canonical paths are possible.

## Verification Commands

Required:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Recommended when the implementation touches validation-sensitive surfaces:

```bash
bash scripts/validate-harness.sh
```

Focused scans:

```bash
rg -n "docs/90.references/research/(workspace-governance-baseline|harness-and-loop-engineering|provider-implementation-status|spec-sdlc-ci-qa-formatting)\\.md" docs .github AGENTS.md CLAUDE.md GEMINI.md README.md scripts
rg -n "non-authoritative|market scan|Source checked|Review and Freshness" docs/90.references/research/2026-07-04-wer
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: The dated pack folder exists and contains one README, four
  moved references, and two new references.
- **VAL-SPC-002**: Root and parent reference indexes route to the dated pack
  and do not present removed flat research files as current direct paths.
- **VAL-SPC-003**: Each authored reference has required reference sections,
  source checked metadata, freshness triggers, and authority boundaries.
- **VAL-SPC-004**: The required topics are covered: workspace purpose, roles,
  CI/CD, QA, formatting, linting, syntax validation, automation, pipeline,
  workflow, operating contract, templates, scripts, integration guides, SDLC,
  governance, system/rules, security, Kubernetes, infrastructure, harness
  engineering, loop engineering, provider status, and spec-driven development.
- **VAL-SPC-005**: External-source claims are checked with official or primary
  sources where possible, and market scan material is labeled
  non-authoritative.
- **VAL-SPC-006**: Required validation commands pass, and Stage 04 task
  evidence records executed commands and limitations.
- **VAL-SPC-007**: No live Kubernetes, Argo CD, Vault, cloud, GitHub remote,
  provider runtime, credential, or third-party mutation occurs.

## 2026-07-10 Current Pack Fact-First Hardening Addendum

### Purpose and Approved Scope

This addendum defines the approved maintenance design for an in-place,
fact-first audit of the Current research pack at
`docs/90.references/research/2026-07-07-wer/`. It supplements the original
dated-pack creation contract above without rewriting the historical work that
contract describes.

The maintenance pass must:

- audit the Current pack README and all seven Current reference documents;
- investigate the current workspace implementation and the corresponding
  external benchmark for every requested topic;
- correct factual drift, restore still-valid analysis lost during earlier
  condensation, deepen weak source attribution, and add actionable follow-up
  routes;
- use `2026-07-10 10:00 KST` as the explicit provider-model source cutoff;
- integrate still-valid content from earlier related research, audit, and
  canonical owner documents into the matching Current reference;
- preserve the `2026-07-04-wer` Historical pack as an unchanged dated
  snapshot; and
- record implementation gaps as recommendations only.

The maintenance pass must not change active scripts, templates, CI workflows,
provider agent adapters, model policy, runtime configuration, GitOps
manifests, infrastructure configuration, live environments, credentials,
secrets, or remote state.

### Artifact and Ownership Design

No new research-pack directory or additional topic reference is introduced.
The Current pack retains this component boundary:

| Current artifact | Maintenance responsibility |
| --- | --- |
| `README.md` | Coverage matrix, source cutoff, reading order, changed-document summary, authority boundary, and pack-wide freshness. |
| `workspace-governance-baseline.md` | Workspace purpose, roles, overview, operating contract, governance, rules, templates, scripts, integration guides, owner/authority matrix, and follow-up routes. |
| `harness-and-loop-engineering.md` | Four-element harness, Observe/Plan/Act/Verify/Learn loop, evaluation, recovery, termination, memory, and the workspace system/environment/rule requirements. |
| `provider-implementation-status.md` | Claude, Codex, and Gemini upstream capabilities, native runtime surfaces, local adapters, hooks, permissions, subagents, model lifecycle, and local-currentness comparison. |
| `spec-sdlc-ci-qa-formatting.md` | Spec-driven development, full SDLC, PRD/ARD/ADR/guide/incident/postmortem/policy/release/runbook roles, formatting, linting, syntax validation, and QA evidence lanes. |
| `automation-pipeline-workflow-qa.md` | Actual GitHub Actions DAG, path filtering, pre-commit/hooks/CI/GitOps feedback topology, automation/pipeline/workflow distinction, and delivery measurement gaps. |
| `kubernetes-infrastructure-security.md` | Kubernetes, Argo CD, infrastructure, RBAC, NetworkPolicy, ESO/Vault, policy-as-code, supply-chain security, and static/live evidence boundaries. |
| `ai-agents-roster-and-gap-analysis.md` | Local agent roster, current `agency-agents` upstream evidence, Adopt/Adapt/Skip analysis, missing or overlapping roles, and task-characteristic model routing. |

The design record stays in this existing Stage 03 spec. A new dated Stage 04
plan and task record will own execution and validation evidence after the
written spec is approved. `docs/00.agent-governance/memory/progress.md` will
receive the final durable completion entry. These evidence records do not
broaden the content-edit scope beyond the Current research pack.

### Internal and External Research Contract

Every material topic must use a three-part evidence record:

1. **Workspace implementation**: current repository documents, configs,
   scripts, workflows, manifests, adapters, templates, Git history, and
   deterministic static validation output.
2. **External benchmark**: official provider documentation, standards bodies,
   and upstream project sources checked read-only.
3. **Comparison**: external expectation, local implementation, evidence,
   gap/risk, recommendation, and canonical follow-up owner.

Local implementation claims are controlled by repository evidence. External
product and model claims are controlled by the applicable official provider or
upstream source. Market scans cannot establish local implementation or override
official sources.

External research must prioritize:

1. OpenAI, Anthropic, Google/Gemini CLI, and MCP official documentation for
   harness, loop, agent, subagent, model, tool, hook, permission, and runtime
   claims.
2. NIST, CISA, SLSA, and other primary standards sources for SDLC and security
   benchmarks.
3. Kubernetes, Argo CD, External Secrets Operator, HashiCorp Vault, OPA, and
   tool-owner documentation for platform, GitOps, secret, policy, formatting,
   linting, and validation claims.
4. The `msitarzewski/agency-agents` repository itself for its roster, division,
   conversion, and persona-format claims.

Each Current reference must include exact URLs where practical, a source
checked timestamp or date, a refresh trigger, and a clear distinction between
repo fact, external fact, interpretation, and recommendation.

### Coverage and Gap Classification

The Current pack README must map every user-requested topic to one primary
Current reference. The coverage set includes workspace purpose, roles,
overview, operating contract, governance, system, rules, templates, scripts,
integration guides, SDLC, security, Kubernetes, infrastructure, CI/CD, QA,
formatting, linting, syntax validation, automation, pipeline, workflow,
harness engineering, loop engineering, provider implementation, common
provider environment, AI agents, `agency-agents`, task-characteristic model
routing, and the role of each required SDLC document family.

Each coverage row or corresponding document section must be classified as one
of:

- **Sufficient**: current content is accurate and adequately sourced;
- **Needs strengthening**: accurate but shallow, weakly sourced, or missing
  analysis;
- **Fact defect**: contradicted by current repo or official evidence;
- **Implementation gap**: missing or partial active behavior, recorded as a
  recommendation and follow-up route only; or
- **Unverified**: evidence is unavailable or ambiguous, so no implementation or
  capability claim is made.

### Related-Document Integration Rules

Earlier related material includes the Historical `2026-07-04-wer` pack,
workspace engineering audit packs, Stage 00 governance and provider references,
Stage 03/04 execution records, Stage 05 guides/policies/runbooks, and Stage 99
templates.

Integration must follow these rules:

- port only still-valid descriptive analysis into the matching Current
  reference;
- reconcile ported content against current repository evidence and current
  official sources before use;
- omit or correct stale facts rather than preserving them for completeness;
- preserve Historical files unchanged and link to them only as dated context;
- summarize active policy or procedure and link to its canonical owner instead
  of copying normative bodies into Stage 90;
- assign one Current reference as the primary owner of each repeated concept
  and replace secondary duplication with a concise cross-link; and
- retain source provenance so readers can distinguish original evidence,
  current synthesis, and recommendations.

### Provider and Model Freshness Design

The provider comparison must not collapse API availability, coding-agent
product availability, CLI configuration, and local adapter declarations into a
single model status. Each model record must carry:

- provider and product surface;
- display name and exact model ID or supported alias;
- lifecycle state such as Stable/GA, Preview, Limited, Deprecated, or
  surface-specific;
- role fit for supervisor, implementation, exploration, review/security,
  documentation, and high-volume deterministic work;
- default, escalation, and cost/latency fallback recommendation;
- reasoning, effort, or routing controls supported by that surface;
- current local assignment; and
- audit verdict plus eval and canonical migration route.

The source snapshot established during design, to be rechecked during
implementation, is:

| Provider | Official current-source baseline at the cutoff | Local audit question |
| --- | --- | --- |
| Claude | Claude Fable 5 is the highest-capability widely released model; Claude Opus 4.8 is recommended for complex agentic coding; Claude Sonnet 5 is the balanced coding/agent model; Claude Haiku 4.5 is the fastest current tier. | Determine whether local Opus 4.8 remains appropriate for supervision, whether Sonnet 4.6 worker assignments should be recommended for later migration to Sonnet 5, and whether local frontmatter uses supported aliases or full IDs. |
| Codex | The Codex product model page recommends GPT-5.6 Sol, Terra, and Luna; describes GPT-5.5 as previous-generation; and marks `gpt-5.3-codex` deprecated for ChatGPT-sign-in Codex while the API catalog may still expose it. | Separate Codex product and API availability, classify local `gpt-5.5` and `gpt-5.3-codex` declarations by authentication surface, and recommend Sol/Terra/Luna or other current mappings only after task-specific evaluation. |
| Gemini | Gemini 3.1 Pro is Preview; Gemini 3.5 Flash and Gemini 3.1 Flash-Lite are Stable. Gemini CLI documents native custom agents under `.gemini/agents/` and separate model-routing behavior. | Distinguish display labels from concrete IDs, record Preview risk for the supervisor tier, verify whether `.agents/agents/` is native or only a repository adapter, and compare stable worker/fallback options. |

Primary provider sources for this snapshot include:

- <https://platform.claude.com/docs/en/about-claude/models/overview>
- <https://code.claude.com/docs/en/sub-agents>
- <https://developers.openai.com/codex/models>
- <https://developers.openai.com/codex/subagents>
- <https://developers.openai.com/api/docs/models>
- <https://ai.google.dev/gemini-api/docs/models>
- <https://geminicli.com/docs/core/subagents/>
- <https://geminicli.com/docs/cli/model/>

The research documents may recommend later model-policy and adapter changes,
but this maintenance pass must not apply those changes.

### Data Flow, Conflict Handling, and Failure Semantics

The audit data flow is:

```text
earlier research/audits + current repo evidence + official external sources
                                |
                                v
                      claim and coverage ledger
                                |
                                v
             fact correction + valid-content integration + gap verdict
                                |
                                v
                    eight Current pack documents
                                |
                                v
             cross-document consistency and repo-static validation
```

Conflict and error handling rules:

- repo evidence controls claims about the local workspace;
- current official provider documentation controls current provider behavior;
- product-surface conflicts are preserved as separate surface-specific facts;
- Preview or limited-access capability is not presented as a stable default;
- inaccessible primary sources are not replaced by uncited recollection;
- unresolved claims are marked Unverified or removed;
- optional-tool absence is reported as SKIP or fallback evidence, not PASS;
- static evidence must not be promoted to live/runtime readiness; and
- a finding that requires an active-file change is recorded with severity,
  rationale, canonical owner, and proposed follow-up only.

### Execution, Commit, and Review Design

Execution occurs on a dedicated feature branch. Logical commit units are:

1. this approved design addendum;
2. Stage 04 plan and task evidence scaffold;
3. governance and SDLC research hardening;
4. harness, loop, provider, and current-model hardening;
5. CI/CD, QA, automation, pipeline, and workflow hardening;
6. Kubernetes, infrastructure, and security hardening;
7. AI agent, `agency-agents`, and task-model-routing hardening; and
8. pack index, coverage matrix, progress memory, and final validation evidence.

After the Stage 04 plan is approved, execution uses fresh implementer
subagents per independent task, a task-scoped spec and quality review after
each logical unit, and a whole-branch review before branch completion. The
subagent-driven workflow supersedes the separate-session executing-plans path
because subagents are available in the current session.

### Verification and Acceptance

Required deterministic checks:

```bash
git diff --check
bash scripts/validate-harness.sh
bash scripts/validate-repo-quality-gates.sh .
```

Run pre-commit and Markdown-specific checks when installed. Record missing
optional tools and fallback behavior. Do not run live cluster, secret-value,
provider-runtime, credential, or remote-state checks.

This maintenance addendum is complete only when:

- all eight Current pack documents have been audited;
- the README coverage matrix maps every requested topic to a primary owner;
- internal and external evidence exist for each material comparison;
- related earlier content has been reconciled and integrated without changing
  Historical snapshots or duplicating active policy;
- the provider/model matrix reflects the `2026-07-10 10:00 KST` cutoff and
  distinguishes API, coding-agent product, CLI, and local adapter surfaces;
- factual defects are corrected and implementation gaps have actionable but
  non-mutating follow-up routes;
- cross-document links, authority boundaries, freshness metadata, and source
  ledgers are consistent;
- every logical task passes task-scoped review and the whole pack passes final
  review; and
- required repository validation passes with limitations recorded honestly.

## Related Documents

- **Prior Spec**: [Workspace Harness Research Pack](../009-workspace-harness-research-pack/spec.md)
- **Prior Spec**: [Workspace Harness Implementation Audit Pack](../010-workspace-harness-implementation-audit-pack/spec.md)
- **Prior Spec**: [Active Control Surface Governance Hardening](../016-active-control-surface-governance-hardening/spec.md)
- **Historical/original Plan (2026-07-04)**:
  [Workspace Engineering Research Pack Plan](../../04.execution/plans/2026-07-04-workspace-engineering-research-pack.md)
- **Historical/original Task (2026-07-04)**:
  [Workspace Engineering Research Pack Task](../../04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md)
- **Current execution Plan (2026-07-10)**:
  [Current Research Pack Fact-First Hardening Plan](../../04.execution/plans/2026-07-10-current-research-pack-fact-first-hardening.md)
- **Current execution Task (2026-07-10)**:
  [Current Research Pack Fact-First Hardening Task](../../04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md)
- **Research README**: [../../90.references/research/README.md](../../90.references/research/README.md)
- **Reference Template**: [../../99.templates/templates/common/reference.template.md](../../99.templates/templates/common/reference.template.md)
- **Reference Maintenance Runbook**: [../../05.operations/runbooks/0011-reference-maintenance-runbook.md](../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
