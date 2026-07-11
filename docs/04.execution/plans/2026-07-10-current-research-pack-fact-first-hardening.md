---
title: 'Current Research Pack Fact-First Hardening Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-10
---

# Current Research Pack Fact-First Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Audit all eight files in the Current workspace engineering research
pack, integrate still-valid earlier analysis, correct repo and external-source
drift, and add non-mutating follow-up routes.

**Architecture:** Each Current reference remains the single owner for one
research topic. Every task compares current repository evidence, earlier
related documents, and official external sources before changing one focused
artifact; pack-wide coverage and cross-document consistency are closed only
after all topic documents pass task-scoped review.

**Tech Stack:** Markdown, repository Stage 03/04/90/99 documentation contracts,
`rg`, Git, official web documentation, `apply_patch`, repository shell
validators, and Superpowers subagent task/review workflows.

## Global Constraints

- Audit `docs/90.references/research/2026-07-07-wer/README.md` and all seven
  Current references in place; do not create a new research pack or topic file.
- Preserve `docs/90.references/research/2026-07-04-wer/` unchanged as a
  Historical snapshot.
- Use `2026-07-10 10:00 KST` as the provider-model source cutoff.
- Investigate the current workspace implementation and the corresponding
  external benchmark for every requested topic.
- Integrate only still-valid descriptive analysis from earlier related
  research and audits; do not duplicate active policy or procedure.
- Local implementation claims require current repository evidence. External
  capability claims require official provider, standards-body, or upstream
  project evidence.
- Separate API availability, coding-agent product availability, CLI behavior,
  local adapter declarations, lifecycle state, and recommendation.
- Record active implementation gaps as severity, rationale, recommendation,
  and canonical follow-up route only.
- Do not change scripts, templates, CI workflows, provider agent adapters,
  model policy, runtime configuration, GitOps manifests, infrastructure
  configuration, live environments, credentials, secrets, or remote state.
- The approved isolated-worktree setup may add `.worktrees/` and
  `.superpowers/` to `.gitignore`; these entries protect the worktree and the
  durable SDD progress ledger and are not research implementation changes.
- Do not infer live Kubernetes, Argo CD, Vault, ESO, provider-runtime, or
  remote readiness from repo-static evidence.
- Use exact external URLs, source checked dates, refresh triggers, authority
  boundaries, and repo-fact/external-fact/interpretation/recommendation labels.
- Use a fresh implementer per task, task-scoped spec and quality review after
  each logical commit, and a whole-branch review before branch completion.
- Run `git diff --check`, `bash scripts/validate-harness.sh`, and
  `bash scripts/validate-repo-quality-gates.sh .`; record missing optional
  tools and fallback behavior honestly.
- Commit each independently reviewable logical unit separately.

---

## File Structure

| Path | Responsibility in this plan |
| --- | --- |
| `docs/04.execution/plans/2026-07-10-current-research-pack-fact-first-hardening.md` | Approved execution order, constraints, verification gates, and completion criteria. |
| `docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md` | Task status, baseline inventory, source/evidence ledger, command results, review outcomes, and handoff. |
| `docs/90.references/research/2026-07-07-wer/README.md` | Pack-wide coverage matrix, source cutoff, reading order, freshness, and cross-document ownership. |
| `docs/90.references/research/2026-07-07-wer/workspace-governance-baseline.md` | Workspace purpose, roles, operating contract, governance, templates, scripts, integration guides, and owner/authority mapping. |
| `docs/90.references/research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md` | Spec-driven development, SDLC document taxonomy, CI/CD, QA, formatting, linting, and syntax validation. |
| `docs/90.references/research/2026-07-07-wer/harness-and-loop-engineering.md` | Harness and loop elements, feedback, evaluation, termination, recovery, memory, and workspace application requirements. |
| `docs/90.references/research/2026-07-07-wer/provider-implementation-status.md` | Claude/Codex/Gemini capability, native surfaces, local implementation, current models, and surface-specific gaps. |
| `docs/90.references/research/2026-07-07-wer/automation-pipeline-workflow-qa.md` | Actual CI DAG, path filters, validation topology, automation/workflow/pipeline boundaries, and delivery evidence gaps. |
| `docs/90.references/research/2026-07-07-wer/kubernetes-infrastructure-security.md` | Kubernetes, GitOps, infrastructure, secrets, policy, network, supply-chain, and static/live security boundaries. |
| `docs/90.references/research/2026-07-07-wer/ai-agents-roster-and-gap-analysis.md` | Local agent roster, upstream `agency-agents`, role gaps, provider-native adapter differences, and task-model routing. |
| `docs/04.execution/plans/README.md` | Plan discovery and lifecycle status. |
| `docs/04.execution/tasks/README.md` | Task-record discovery and lifecycle status. |
| `docs/00.agent-governance/memory/progress.md` | Final durable result, evidence, limitations, and reusable lessons. |
| `.gitignore` | Ignore the approved `.worktrees/` isolation directory and `.superpowers/` SDD progress ledger. |

## Overview

This plan executes the approved 2026-07-10 addendum in the Workspace
Engineering Research Pack specification. It performs a surgical, evidence-first
hardening pass rather than creating another dated research snapshot or changing
the active workspace controls that the research evaluates.

## Context

The Current pack is structurally sound but is materially shorter than its
Historical predecessor and contains weak source ledgers, stale provider/model
claims, and several repo-fact mismatches. Read-only exploration already found
examples involving provider-native agent paths, Claude hook descriptions,
Codex model lifecycle, Gemini agent registration, GitHub Actions job topology,
GitOps ApplicationSet ownership, shell-syntax coverage, and task-model effort
mapping. The implementation must re-verify every finding before publication.

## Goals & In-Scope

- **Goals**:
  - Produce one evidence-backed Current reference per approved topic.
  - Restore relevant depth from prior documents without restoring stale facts.
  - Provide claim-level official sources and a 2026-07-10 model snapshot.
  - Give every implementation gap an actionable, non-mutating follow-up route.
  - Preserve pack-level discoverability and eliminate cross-document ownership
    ambiguity.
- **In Scope**:
  - Eight Current pack files, one new Stage 04 task record, Stage 04 indexes,
    the current plan lifecycle record, and final progress memory.
  - Read-only external research and repository-static validation.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Implement recommendations, promote model assignments, or redesign the
    active workspace harness.
  - Rewrite Historical research or active canonical policy.
- **Out of Scope**:
  - Live cluster, Vault, ESO, cloud, provider-runtime, remote GitHub, credential,
    secret-value, publish, push, merge, or third-party mutation.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| WERH-001 | Create execution evidence and baseline audit ledger | Stage 04 task record and task index | Addendum: Internal and External Research Contract | Task IDs, evidence lanes, baseline inventory, and limitations are explicit. |
| WERH-002 | Harden workspace governance baseline | `workspace-governance-baseline.md` | Addendum: Artifact and Ownership Design | Repo facts, external benchmark, owner matrix, and follow-up routes are present. |
| WERH-003 | Harden spec-driven SDLC, CI, QA, and document taxonomy | `spec-sdlc-ci-qa-formatting.md` | Addendum: Coverage and Gap Classification | Every SDLC document family and QA lane has role, evidence, benchmark, and gap verdict. |
| WERH-004 | Harden harness and loop engineering | `harness-and-loop-engineering.md` | Addendum: Internal and External Research Contract | Harness/loop elements, termination, evaluation, recovery, and provider-neutral boundaries are source-backed. |
| WERH-005 | Harden provider implementation and current-model analysis | `provider-implementation-status.md` | Addendum: Provider and Model Freshness Design | Claude/Codex/Gemini API/product/CLI/local surfaces and model lifecycle states are separated. |
| WERH-006 | Harden automation, pipeline, workflow, and QA topology | `automation-pipeline-workflow-qa.md` | Addendum: Artifact and Ownership Design | Actual CI DAG, filters, GitOps boundary, feedback lanes, and delivery gaps match repo evidence. |
| WERH-007 | Harden Kubernetes, infrastructure, and security analysis | `kubernetes-infrastructure-security.md` | Addendum: Artifact and Ownership Design | Platform controls, external benchmarks, static/live limits, and prioritized gaps are explicit. |
| WERH-008 | Harden AI-agent roster, upstream comparison, and model routing | `ai-agents-roster-and-gap-analysis.md` | Addendum: Provider and Model Freshness Design | Local roster, current upstream evidence, native adapter gaps, and task-model recommendations are source-backed. |
| WERH-009 | Close pack coverage and cross-document integration | Current pack README and all Current references | Addendum: Coverage and Related-Document Integration Rules | Every requested topic has one primary owner; links, freshness, and repeated content are consistent. |
| WERH-010 | Run final validation and close execution records | Plan, task, indexes, progress memory | Addendum: Verification and Acceptance | Required static gates and final review pass; limitations and logical commits are recorded. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Diff | Reject whitespace and patch-format errors | `git diff --check` | Exit 0, no output. |
| VAL-PLN-002 | Harness | Validate provider/harness/document control contracts | `bash scripts/validate-harness.sh` | Exit 0 and `PASS harness repo-static validation`. |
| VAL-PLN-003 | Repository | Validate links, frontmatter, stage routing, scripts, manifests, secret handling, and policy fallbacks | `bash scripts/validate-repo-quality-gates.sh .` | Exit 0 and `[PASS] repository quality gates passed`. |
| VAL-PLN-004 | Coverage | Confirm all requested topic terms are represented in the Current pack | `rg -n 'purpose|role|CI/CD|QA|formatting|linting|syntax|automation|pipeline|workflow|operating contract|template|script|integration|SDLC|governance|security|Kubernetes|infrastructure|harness|loop|Claude|Codex|Gemini|PRD|ARD|ADR|incident|postmortem|policy|release|runbook|agency-agents|model' docs/90.references/research/2026-07-07-wer` | Every term family has at least one meaningful owner hit; Task evidence records the owner mapping. |
| VAL-PLN-005 | Freshness | Confirm cutoff, source metadata, and lifecycle vocabulary | `rg -n '2026-07-10 10:00 KST|Source checked|Last reviewed|Stable|GA|Preview|Limited|Deprecated|surface-specific' docs/90.references/research/2026-07-07-wer` | README and relevant provider/agent references contain the cutoff and lifecycle terms. |
| VAL-PLN-006 | Boundaries | Confirm implementation-gap text routes follow-up and does not claim active changes | `rg -n 'follow-up|canonical owner|recommendation|not authoritative|repo-static|live runtime' docs/90.references/research/2026-07-07-wer` | Each gap section includes non-mutating routing and evidence-boundary language. |
| VAL-PLN-007 | Completeness | Reject incomplete authored content | `rg -n '\b(T[B]D|T[O]DO|F[I]XME|implement[[:space:]]+later)\b' docs/90.references/research/2026-07-07-wer docs/04.execution/plans/2026-07-10-current-research-pack-fact-first-hardening.md docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md` | No incomplete authored-content marker matches. Historical command evidence outside the target files is irrelevant. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Provider pages change after the cutoff | High | Record the exact cutoff and page URL; distinguish cutoff facts from later observations. |
| API and coding-agent product model catalogs disagree | High | Preserve separate surface rows and do not infer availability across authentication or product surfaces. |
| Historical detail reintroduces stale facts | High | Re-verify every ported claim against current repo and official sources before use. |
| Research content becomes active policy | High | Keep authority boundaries, summarize canonical policy, and route changes to owner files without editing them. |
| Current documents duplicate one another | Medium | Assign one primary Current owner per concept in the pack coverage matrix and cross-link secondary references. |
| Optional local linters are unavailable | Medium | Run deterministic repository fallbacks; record optional-tool SKIP without claiming full tool coverage. |
| Large diffs hide isolated factual errors | Medium | Commit and review each topic document independently before pack-wide integration. |
| External source is inaccessible | Medium | Use another official first-party page for the same claim or classify the claim Unverified and omit it. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Every task must pass focused content assertions,
  `git diff --check`, and task-scoped source/repo fact review before commit.
- **Sandbox / Canary Rollout**: Documentation-only feature branch; no runtime
  rollout exists.
- **Human Approval Gate**: The design and written spec are approved. Any active
  CI, script, template, provider adapter, model policy, runtime, manifest,
  credential, secret, remote, or live change requires a separate task and new
  human approval.
- **Rollback Trigger**: A task reviewer finds unsupported facts, source-surface
  conflation, active-policy duplication, Historical edits, or unresolved
  required-gate failure. Revert or fix only that task commit before proceeding.
- **Prompt / Model Promotion Criteria**: Research may recommend model changes,
  but no model is promoted without task-specific eval evidence and a later
  canonical `model-policy.md`/adapter change task.

## Detailed Tasks

### Task 1: Establish Execution Evidence and Baseline Ledger

**Files:**

- Create: `docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md`
- Modify: `docs/04.execution/tasks/README.md`

**Interfaces:**

- Consumes: the approved addendum in
  `docs/03.specs/017-workspace-engineering-research-pack/spec.md` and this plan.
- Produces: task IDs `WERH-001` through `WERH-010`, baseline repo evidence,
  external-source lanes, limitations, and per-task review/commit fields used by
  all later tasks.

- [ ] **Step 1: Verify execution starts from the approved feature branch**

  Run:

  ```bash
  git status --short --branch
  git log -2 --oneline
  ```

  Expected: branch `codex/wer-current-pack-hardening`, no unrelated changes,
  and design commit `656b468` in history.

- [ ] **Step 2: Prove the task record is not already indexed**

  Run:

  ```bash
  rg -n '2026-07-10-current-research-pack-fact-first-hardening' docs/04.execution/tasks/README.md
  ```

  Expected: exit 1 before the task record and index row are added.

- [ ] **Step 3: Create the Stage 04 task record from the canonical task template**

  Use `apply_patch`. The authored record must contain these exact top-level
  sections and task rows:

  ```markdown
  ## Overview
  ## Inputs
  ## Working Rules
  ## Baseline Evidence
  ## Source and Claim Ledger
  ## Task Table
  ## Phase View
  ## Verification Summary
  ## Related Documents
  ```

  The Task Table must contain `WERH-001` through `WERH-010`, type `doc` except
  `WERH-010` type `eval`, owner `doc-writer` for research tasks,
  `supervisor` for WERH-001/WERH-009/WERH-010, and initial status `Todo`.
  Baseline Evidence must record the eight Current files, ten local agent stems
  across each of `.claude/agents`, `.agents/agents`, and `.codex/agents`, five
  GitHub workflow files, six CI jobs, the no-live/no-remote boundary, and the
  optional-tool limitations observed during baseline validation.

- [ ] **Step 4: Add the Draft task record to the Stage 04 task index**

  Use `apply_patch` to add a row linking
  `./2026-07-10-current-research-pack-fact-first-hardening.md`, description
  `Current research pack fact-first audit, source refresh, related-document integration, and validation evidence.`, status `Draft`, and date
  `2026-07-10`.

- [ ] **Step 5: Validate the evidence scaffold**

  Run:

  ```bash
  rg -n 'WERH-00[1-9]|WERH-010|Baseline Evidence|Source and Claim Ledger|repo-static|live runtime' docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md
  git diff --check
  bash scripts/validate-repo-quality-gates.sh .
  ```

  Expected: all ten task IDs and evidence headings are found; both validation
  commands exit 0.

- [ ] **Step 6: Commit the execution scaffold**

  ```bash
  git add docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md docs/04.execution/tasks/README.md
  git commit -m 'docs(execution): scaffold current research hardening evidence'
  ```

### Task 2: Harden the Workspace Governance Baseline

**Files:**

- Modify: `docs/90.references/research/2026-07-07-wer/workspace-governance-baseline.md`
- Modify: `docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md`

**Interfaces:**

- Consumes: the Current and Historical governance references, Stage 00
  bootstrap/agentic/approval/persona/scope contracts, Stage 99 routing, root
  README, `.github/workflows/ci.yml`, and official OpenGitOps principles.
- Produces: the pack's canonical workspace purpose, operating contract,
  owner/authority matrix, enforcement/evidence map, and governance follow-up
  register. Task 9 links to these sections instead of duplicating them.

- [ ] **Step 1: Run failing content assertions for the missing governance depth**

  ```bash
  rg -n 'Owner and Authority Matrix|Enforcement and Evidence Map|Governance Gap Register|External Benchmark' docs/90.references/research/2026-07-07-wer/workspace-governance-baseline.md
  ```

  Expected: at least one required heading is absent before editing.

- [ ] **Step 2: Reconcile repo facts and earlier related analysis**

  Read the Current and Historical governance references plus:

  ```text
  README.md
  docs/00.agent-governance/rules/bootstrap.md
  docs/00.agent-governance/rules/agentic.md
  docs/00.agent-governance/rules/approval-boundaries.md
  docs/00.agent-governance/rules/persona.md
  docs/00.agent-governance/scopes/docs.md
  docs/00.agent-governance/harness-catalog.md
  docs/00.agent-governance/harness-implementation-map.md
  docs/99.templates/support/template-routing.md
  docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md
  scripts/README.md
  .github/workflows/ci.yml
  ```

  Re-verify workspace purpose, GitOps-first flow, role/persona ownership,
  provider-adapter ownership, Stage taxonomy, validation lanes, approval
  boundaries, and exact agent/workflow counts. Treat
  <https://opengitops.dev/> as external GitOps benchmark context, not local
  implementation proof.

- [ ] **Step 3: Add the exact governance analysis structure**

  Use `apply_patch` to add or normalize:

  ```markdown
  ### External Benchmark
  ### Owner and Authority Matrix
  ### Enforcement and Evidence Map
  ### Governance Gap Register
  ```

  Owner and Authority Matrix columns must be `Area`, `Canonical owner`,
  `Local implementation evidence`, `Authority boundary`, and `Current verdict`.
  Enforcement and Evidence Map columns must be `Contract`, `Instruction`,
  `Preventive control`, `Feedback evidence`, and `Knowledge store`.
  Governance Gap Register columns must be `Finding`, `Evidence`, `Risk`,
  `Recommendation`, and `Canonical follow-up route`.

  Include the observed lifecycle draft/done asymmetry, release-contract gap,
  duplicate lifecycle/route summaries, link-only lineage, audit-currentness
  drift, and stale Graphify snapshot as recommendations only after rechecking
  their current evidence.

- [ ] **Step 4: Replace weak or ambiguous source entries**

  Preserve repo-relative links and add exact official URLs with
  `Source checked: 2026-07-10`. Remove claims that cannot be tied to current
  repo evidence or a primary source. Set frontmatter `updated` and
  `Last reviewed` to `2026-07-10`.

- [ ] **Step 5: Run focused and repository validation**

  ```bash
  rg -n 'External Benchmark|Owner and Authority Matrix|Enforcement and Evidence Map|Governance Gap Register|2026-07-10' docs/90.references/research/2026-07-07-wer/workspace-governance-baseline.md
  git diff --check
  bash scripts/validate-repo-quality-gates.sh .
  ```

  Expected: all headings and date are found; validators exit 0.

- [ ] **Step 6: Record evidence and commit**

  Mark WERH-002 `Done` and add commands, source URLs, review outcome, and
  limitations to the task record. Record the resulting commit SHA during final
  closure from `git log`, after the commit exists. Then run:

  ```bash
  git add docs/90.references/research/2026-07-07-wer/workspace-governance-baseline.md docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md
  git commit -m 'docs(research): harden workspace governance baseline'
  ```

### Task 3: Harden Spec-Driven SDLC, CI, QA, and Document Taxonomy

**Files:**

- Modify: `docs/90.references/research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md`
- Modify: `docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md`

**Interfaces:**

- Consumes: Current/Historical SDLC research, Stage authoring/routing contracts,
  every Stage 99 SDLC template, `.editorconfig`, `.pre-commit-config.yaml`, CI,
  validators, and primary SDLC/security/format standards.
- Produces: canonical research treatment of spec-driven development, document
  purpose, lifecycle/traceability, and QA evidence lanes used by Tasks 6 and 9.

- [ ] **Step 1: Prove the Current document lacks the full approved structure**

  ```bash
  rg -n 'Lifecycle and Traceability Matrix|External SDLC Benchmark|QA Evidence Lane Matrix|Document Maturity Gap Register' docs/90.references/research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md
  ```

  Expected: at least one heading is absent before editing.

- [ ] **Step 2: Re-verify internal document and QA contracts**

  Inspect Stage 01-05 READMEs, `stage-authoring-matrix.md`,
  `document-stage-routing.md`, `sdlc-governance.md`, every template under
  `docs/99.templates/templates/sdlc/`, `.editorconfig`,
  `.pre-commit-config.yaml`, `.github/workflows/ci.yml`, and validation scripts.
  Record actual lifecycle states, missing release template, incident/postmortem
  steady-state inventory, and which command owns formatting, linting, syntax,
  structural, secret, policy, and live checks.

- [ ] **Step 3: Verify official and primary external benchmarks**

  Check and cite these exact sources:

  ```text
  https://github.com/github/spec-kit
  https://csrc.nist.gov/pubs/sp/800/218/final
  https://csrc.nist.gov/pubs/sp/800/61/r3/final
  https://sre.google/sre-book/postmortem-culture/
  https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
  https://docs.github.com/en/actions/reference/security/secure-use
  https://pre-commit.com/
  https://editorconfig.org/
  https://prettier.io/docs/
  https://spec.commonmark.org/0.31.2/
  https://yaml.org/spec/1.2.2/
  ```

  Label non-standard document families such as PRD and ARD as workspace/industry
  conventions rather than universal standards.

- [ ] **Step 4: Add the exact SDLC and QA structure**

  Use `apply_patch` to add or normalize:

  ```markdown
  ### External SDLC Benchmark
  ### Lifecycle and Traceability Matrix
  ### QA Evidence Lane Matrix
  ### Document Maturity Gap Register
  ```

  Lifecycle and Traceability Matrix must contain rows for PRD, ARD, ADR, Spec,
  Plan, Task, Guide, Policy, Runbook, Incident, Postmortem, Release artifact,
  Reference, and Archive Tombstone, with columns `Document`, `Purpose`,
  `Primary inputs`, `Decision/evidence owner`, `Lifecycle`, and `Local route`.
  QA Evidence Lane Matrix must separate formatting, linting, syntax/parse,
  repo-structural, manifest, secret, policy, artifact/release, and live runtime
  evidence. Document Maturity Gap Register must include the verified
  draft-spec/done-task asymmetry, release readiness/provenance gap, absence of
  incident exercise evidence, and traceability automation opportunity.

- [ ] **Step 5: Validate content and source precision**

  ```bash
  rg -n 'PRD|ARD|ADR|Guide|Incident|Postmortem|Policy|Release|Runbook|Lifecycle and Traceability Matrix|QA Evidence Lane Matrix|2026-07-10' docs/90.references/research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md
  git diff --check
  bash scripts/validate-repo-quality-gates.sh .
  ```

  Expected: every required document family and matrix is found; validators
  exit 0.

- [ ] **Step 6: Record evidence and commit**

  Update WERH-003 evidence and status, then:

  ```bash
  git add docs/90.references/research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md
  git commit -m 'docs(research): deepen spec driven SDLC and QA analysis'
  ```

### Task 4: Harden Harness and Loop Engineering

**Files:**

- Modify: `docs/90.references/research/2026-07-07-wer/harness-and-loop-engineering.md`
- Modify: `docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md`

**Interfaces:**

- Consumes: Current/Historical harness research, Stage 00 harness catalog and
  implementation map, provider baselines, shared hooks, official provider
  harness/agent-loop sources, and MCP specification/security guidance.
- Produces: provider-neutral harness/loop definitions, workspace application
  requirements, termination/evaluation/recovery design, and a follow-up gap
  register. Task 5 owns provider-specific implementation details.

- [ ] **Step 1: Run failing structure assertions**

  ```bash
  rg -n 'Evaluation and Recovery Loop|Harness Ownership Boundary|Provider-Neutral Control Loop Matrix|Harness and Loop Gap Register' docs/90.references/research/2026-07-07-wer/harness-and-loop-engineering.md
  ```

  Expected: at least one heading is absent before editing.

- [ ] **Step 2: Reconcile Current, Historical, and repo evidence**

  Re-read the Historical document's detailed source set and compare it with
  `harness-catalog.md`, `harness-implementation-map.md`, `subagent-protocol.md`,
  `model-policy.md`, shared hooks, memory/progress, and the provider runtime
  baselines. Correct any statement that assigns governance, memory, or Stage 99
  template ownership to `.agents/`; `.agents` owns shared skills, workflows,
  output styles, the Gemini baseline, and its local adapters, while canonical
  policy and templates remain with their owning stages.

- [ ] **Step 3: Verify official harness and loop sources**

  Check and cite:

  ```text
  https://openai.com/index/harness-engineering/
  https://openai.com/index/unrolling-the-codex-agent-loop/
  https://developers.openai.com/codex/subagents/
  https://code.claude.com/docs/en/sub-agents
  https://code.claude.com/docs/en/hooks
  https://geminicli.com/docs/core/subagents/
  https://geminicli.com/docs/reference/policy-engine/
  https://modelcontextprotocol.io/specification/2025-06-18
  https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices
  ```

  If MCP publishes a newer stable specification before the cutoff, record the
  newer version and explain the older source's historical status.

- [ ] **Step 4: Add the exact harness/loop analysis structure**

  Use `apply_patch` to add or normalize:

  ```markdown
  ### Harness Ownership Boundary
  ### Provider-Neutral Control Loop Matrix
  ### Evaluation and Recovery Loop
  ### Harness and Loop Gap Register
  ```

  Provider-Neutral Control Loop Matrix columns must be `Phase`, `Inputs`,
  `Allowed action`, `Feedback evidence`, `Termination condition`, and
  `Knowledge update`. Cover Observe, Plan, Act, Verify, Learn/Handoff, retry
  budget, failure escalation, compaction, and human approval. Keep MCP threat
  mitigations tied to the official security taxonomy.

- [ ] **Step 5: Validate and commit**

  ```bash
  rg -n 'Harness Ownership Boundary|Provider-Neutral Control Loop Matrix|Evaluation and Recovery Loop|Harness and Loop Gap Register|Observe|Plan|Act|Verify|Learn|2026-07-10' docs/90.references/research/2026-07-07-wer/harness-and-loop-engineering.md
  git diff --check
  bash scripts/validate-harness.sh
  bash scripts/validate-repo-quality-gates.sh .
  ```

  Expected: all structures and loop phases are found; validators exit 0.
  Update WERH-004 evidence/status and commit:

  ```bash
  git add docs/90.references/research/2026-07-07-wer/harness-and-loop-engineering.md docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md
  git commit -m 'docs(research): deepen harness and loop engineering'
  ```

### Task 5: Harden Provider Implementation and Current-Model Analysis

**Files:**

- Modify: `docs/90.references/research/2026-07-07-wer/provider-implementation-status.md`
- Modify: `docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md`

**Interfaces:**

- Consumes: local Claude/Codex/Gemini gateways, runtime baselines, hooks,
  adapters, model policy, harness catalog, and official provider docs checked
  at `2026-07-10 10:00 KST`.
- Produces: provider capability matrix, native-vs-local implementation matrix,
  current-model surface matrix, task-characteristic model recommendation, and
  non-mutating provider/model gap routes used by Task 8.

- [ ] **Step 1: Prove the Current document lacks the approved model surface detail**

  ```bash
  rg -n 'Native Surface and Local Adapter Matrix|Current Model Surface Matrix|Task-Characteristic Model Recommendation|Provider Gap Register|2026-07-10 10:00 KST' docs/90.references/research/2026-07-07-wer/provider-implementation-status.md
  ```

  Expected: at least one required heading or cutoff is absent before editing.

- [ ] **Step 2: Re-verify local provider implementation**

  Inspect gateway/runtime/provider files, `.claude/settings.json`,
  `.agents/hooks.json`, `.codex/hooks.json`, all 30 local adapters, and
  `validate-repo-quality-gates.sh`. Record exact adapter paths, imported scopes,
  declared model strings, tools, Codex effort, hook event wiring, tracked
  config presence/absence, and validator coverage.

  Explicitly recheck these preliminary findings before writing them:

  - `observability-reviewer` imports `scopes/infra.md`, not a nonexistent
    `scopes/observability.md`;
  - Claude settings bind shared lifecycle hook scripts rather than binding
    `validate-harness.sh` directly;
  - native `tools:` frontmatter is declared on Claude adapters, not uniformly
    on every provider adapter;
  - current Codex workers use high effort for implementation/review/security/
    incident roles and medium for docs/wiki roles;
  - Gemini CLI official project custom-agent path is `.gemini/agents/`, while
    the repository currently stores Gemini-oriented adapters in
    `.agents/agents/`; and
  - provider parity validation is stronger for file stems than for every
    provider-native field.

- [ ] **Step 3: Verify official provider and model sources at the cutoff**

  Check and cite:

  ```text
  https://platform.claude.com/docs/en/about-claude/models/overview
  https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions
  https://code.claude.com/docs/en/sub-agents
  https://developers.openai.com/codex/models
  https://developers.openai.com/codex/subagents
  https://developers.openai.com/api/docs/models
  https://developers.openai.com/api/docs/models/gpt-5.3-codex
  https://ai.google.dev/gemini-api/docs/models
  https://ai.google.dev/gemini-api/docs/changelog
  https://geminicli.com/docs/cli/model/
  https://geminicli.com/docs/core/subagents/
  ```

  Preserve the surface-specific conflict: Codex recommends GPT-5.6
  Sol/Terra/Luna, marks GPT-5.5 previous-generation, and deprecates
  `gpt-5.3-codex` for ChatGPT-sign-in Codex, while API availability is governed
  separately by the API model catalog.

- [ ] **Step 4: Add exact provider and model matrices**

  Use `apply_patch` to add or normalize:

  ```markdown
  ### Native Surface and Local Adapter Matrix
  ### Current Model Surface Matrix — 2026-07-10 10:00 KST
  ### Task-Characteristic Model Recommendation
  ### Provider Gap Register
  ```

  Native Surface columns: `Capability`, `Claude official surface`, `Codex official surface`, `Gemini official surface`, `Local implementation`, `Verdict`.
  Current Model Surface columns: `Provider`, `Surface`, `Model/ID`, `Lifecycle`, `Role fit`, `Local assignment`, `Verdict`, `Source`.
  Task-Characteristic columns: `Task profile`, `Claude default/escalation/fallback`, `Codex default/escalation/fallback`, `Gemini default/escalation/fallback`, `Effort/routing`, `Eval required`.
  Provider Gap Register columns: `Finding`, `Evidence`, `Risk`, `Recommendation`, `Canonical follow-up route`.

  Include Claude Fable 5, Opus 4.8, Sonnet 5, and Haiku 4.5; Codex GPT-5.6
  Sol/Terra/Luna, GPT-5.5, GPT-5.4 Mini, and `gpt-5.3-codex`; Gemini
  3.1 Pro Preview, 3.5 Flash Stable, and 3.1 Flash-Lite Stable. Do not recommend
  changing active adapter files in this task.

- [ ] **Step 5: Validate and commit**

  ```bash
  rg -n 'Native Surface and Local Adapter Matrix|Current Model Surface Matrix|Task-Characteristic Model Recommendation|Provider Gap Register|Fable 5|Opus 4.8|Sonnet 5|Haiku 4.5|GPT-5.6|GPT-5.5|gpt-5.3-codex|Gemini 3.1 Pro|Gemini 3.5 Flash|Gemini 3.1 Flash-Lite|2026-07-10 10:00 KST' docs/90.references/research/2026-07-07-wer/provider-implementation-status.md
  git diff --check
  bash scripts/validate-harness.sh
  bash scripts/validate-repo-quality-gates.sh .
  ```

  Expected: every matrix, model family, and cutoff is found; validators exit 0.
  Update WERH-005 evidence/status and commit:

  ```bash
  git add docs/90.references/research/2026-07-07-wer/provider-implementation-status.md docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md
  git commit -m 'docs(research): refresh provider and model analysis'
  ```

### Task 6: Harden Automation, Pipeline, Workflow, and QA Topology

**Files:**

- Modify: `docs/90.references/research/2026-07-07-wer/automation-pipeline-workflow-qa.md`
- Modify: `docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md`

**Interfaces:**

- Consumes: Current/Historical automation research, all GitHub workflow files,
  path filters, pre-commit, hooks, validators, GitOps root/ApplicationSet
  manifests, CI/QA guide, GitHub Actions official docs, DORA, and pre-commit.
- Produces: exact delivery topology, validation-coverage matrix, and automation
  gap register. Task 9 links to these sections for pipeline/workflow coverage.

- [ ] **Step 1: Run failing topology assertions**

  ```bash
  rg -n 'Actual CI Job DAG|Path Filter and Gate Coverage Matrix|GitOps Delivery Boundary|Automation Gap Register' docs/90.references/research/2026-07-07-wer/automation-pipeline-workflow-qa.md
  ```

  Expected: at least one heading is absent before editing.

- [ ] **Step 2: Re-derive repo facts from owning files**

  Inspect `.github/workflows/*.yml`, `.github/dependabot.yml`,
  `.pre-commit-config.yaml`, hook scripts/configs, validators,
  `gitops/clusters/local/root-application.yaml`,
  `gitops/clusters/local/applicationset-apps.yaml`, and
  `gitops/apps/root/kustomization.yaml`.

  Recheck that `branch-policy` and `changes` begin in parallel; downstream
  jobs are conditional on `changes`; `ci-summary` aggregates outcomes;
  `root-platform` owns platform applications under `gitops/apps/root`;
  `apps-generator` owns `gitops/workloads/*`; CI is a static QA gate rather
  than direct deployment CD; and shell syntax belongs to pre-commit/explicit
  `bash -n`, not an implied repo-quality-gate behavior unless the script proves
  otherwise.

- [ ] **Step 3: Verify exact external sources**

  ```text
  https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
  https://docs.github.com/en/actions/how-tos/monitor-workflows/use-the-visualization-graph
  https://docs.github.com/en/actions/reference/security/secure-use
  https://docs.github.com/en/actions/tutorials/authenticate-with-github_token
  https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency
  https://pre-commit.com/
  https://dora.dev/guides/dora-metrics/
  https://opengitops.dev/
  ```

- [ ] **Step 4: Add exact automation analysis sections**

  Use `apply_patch` to add or normalize:

  ```markdown
  ### Actual CI Job DAG
  ### Path Filter and Gate Coverage Matrix
  ### GitOps Delivery Boundary
  ### Automation Gap Register
  ```

  Actual CI Job DAG must show
  `branch-policy || changes -> pre-commit/repo-quality-static/manifest-static -> ci-summary`
  with the precise dependency/condition nuance in prose. Coverage Matrix
  columns: `Changed surface`, `Local hook/pre-commit`, `CI job`, `Validator`,
  `Optional dependency`, `Coverage verdict`. Gap Register must recheck path
  filter omissions, policy/hook coverage, warn-only live tests, immutable SHA
  pinning, supply-chain controls, regex-heavy static contracts, and absent DORA
  telemetry as recommendations only.

- [ ] **Step 5: Validate and commit**

  ```bash
  rg -n 'Actual CI Job DAG|branch-policy|changes|pre-commit|repo-quality-static|manifest-static|ci-summary|Path Filter and Gate Coverage Matrix|GitOps Delivery Boundary|Automation Gap Register|2026-07-10' docs/90.references/research/2026-07-07-wer/automation-pipeline-workflow-qa.md
  git diff --check
  bash scripts/validate-repo-quality-gates.sh .
  ```

  Expected: DAG jobs and all structures are found; validators exit 0. Update
  WERH-006 evidence/status and commit:

  ```bash
  git add docs/90.references/research/2026-07-07-wer/automation-pipeline-workflow-qa.md docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md
  git commit -m 'docs(research): correct automation and CI topology'
  ```

### Task 7: Harden Kubernetes, Infrastructure, and Security Analysis

**Files:**

- Modify: `docs/90.references/research/2026-07-07-wer/kubernetes-infrastructure-security.md`
- Modify: `docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md`

**Interfaces:**

- Consumes: Current/Historical security research, GitOps/infrastructure/policy
  sources, manifests, tests, security validators, Stage 05 operations docs, and
  official Kubernetes/GitOps/secrets/policy/supply-chain sources.
- Produces: platform control matrix, static/live evidence matrix, and prioritized
  non-mutating security gap register.

- [ ] **Step 1: Run failing security-depth assertions**

  ```bash
  rg -n 'Platform Security Control Matrix|Static and Live Evidence Boundary|Supply-Chain Security Analysis|Security Gap Register' docs/90.references/research/2026-07-07-wer/kubernetes-infrastructure-security.md
  ```

  Expected: at least one heading is absent before editing.

- [ ] **Step 2: Re-verify local controls and known gaps**

  Inspect GitOps AppProjects/root/ApplicationSet, Kustomize trees,
  NetworkPolicies, ESO/Vault samples, `bootstrap-local.sh`, infrastructure
  static/live tests, Conftest policy, kube-linter config, secret and policy
  validators, and operations policies/runbooks. Recheck minimum privilege,
  namespace/resource allow-lists, secret flow, network egress, policy fallback,
  image tag controls, bootstrap exceptions, and which live checks are warn-only.

- [ ] **Step 3: Verify exact primary external sources**

  ```text
  https://kubernetes.io/docs/concepts/configuration/secret/
  https://kubernetes.io/docs/concepts/services-networking/network-policies/
  https://kubernetes.io/docs/reference/access-authn-authz/rbac/
  https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/
  https://opengitops.dev/
  https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/
  https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/
  https://external-secrets.io/latest/provider/hashicorp-vault/
  https://developer.hashicorp.com/vault/docs/concepts/policies
  https://developer.hashicorp.com/vault/docs/auth/kubernetes
  https://www.openpolicyagent.org/docs/kubernetes
  https://www.conftest.dev/
  https://csrc.nist.gov/pubs/sp/800/204/d/final
  https://slsa.dev/spec/v1.2/
  https://scorecard.dev/
  ```

- [ ] **Step 4: Add exact security analysis sections**

  Use `apply_patch` to add or normalize:

  ```markdown
  ### Platform Security Control Matrix
  ### Static and Live Evidence Boundary
  ### Supply-Chain Security Analysis
  ### Security Gap Register
  ```

  Control Matrix columns: `Control domain`, `External expectation`, `Local
  implementation`, `Static evidence`, `Live evidence status`, `Verdict`.
  Security Gap Register columns: `Finding`, `Evidence`, `Risk`,
  `Recommendation`, `Canonical follow-up route`. Recheck CI path-filter gaps,
  hook policy coverage, warn-only health/TLS tests, action SHA pinning, absent
  CodeQL/dependency review/SBOM/attestation, Vault TLS default, process-argument
  secret exposure, and regex-heavy static contracts before including them.

- [ ] **Step 5: Validate and commit**

  ```bash
  rg -n 'Platform Security Control Matrix|Static and Live Evidence Boundary|Supply-Chain Security Analysis|Security Gap Register|Kubernetes|Argo CD|RBAC|NetworkPolicy|External Secrets|Vault|SLSA|2026-07-10' docs/90.references/research/2026-07-07-wer/kubernetes-infrastructure-security.md
  git diff --check
  bash scripts/validate-repo-quality-gates.sh .
  ```

  Expected: all required controls and sections are found; validators exit 0.
  Update WERH-007 evidence/status and commit:

  ```bash
  git add docs/90.references/research/2026-07-07-wer/kubernetes-infrastructure-security.md docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md
  git commit -m 'docs(research): deepen Kubernetes infrastructure security'
  ```

### Task 8: Harden AI-Agent Roster, Upstream Comparison, and Model Routing

**Files:**

- Modify: `docs/90.references/research/2026-07-07-wer/ai-agents-roster-and-gap-analysis.md`
- Modify: `docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md`

**Interfaces:**

- Consumes: local 30 adapter files, harness/model policy, Task 5 provider/model
  findings, the current upstream `agency-agents` repository, and official
  provider subagent/model sources.
- Produces: verified roster, upstream format/count snapshot, provider-native
  adapter verdict, Adopt/Adapt/Skip decisions, and role-level
  default/escalation/fallback model recommendations.

- [ ] **Step 1: Run failing AI-agent structure assertions**

  ```bash
  rg -n 'Provider-Native Adapter Status|Upstream Snapshot — 2026-07-10|Role and Coverage Gap Register|Default, Escalation, and Fallback Routing' docs/90.references/research/2026-07-07-wer/ai-agents-roster-and-gap-analysis.md
  ```

  Expected: at least one heading is absent before editing.

- [ ] **Step 2: Re-verify local roster and provider contracts**

  Count and compare stems in `.claude/agents`, `.agents/agents`, and
  `.codex/agents`. Inspect model, tools, scope import, guardrails, handoff,
  postflight, sandbox, and effort fields. Compare with Task 5's official native
  paths and runtime semantics. Do not treat stem parity as full native
  behavioral parity.

- [ ] **Step 3: Re-verify `agency-agents` from the upstream repository**

  Use read-only GitHub/web access to check:

  ```text
  https://github.com/msitarzewski/agency-agents
  https://raw.githubusercontent.com/msitarzewski/agency-agents/main/divisions.json
  https://raw.githubusercontent.com/msitarzewski/agency-agents/main/engineering/engineering-sre.md
  ```

  Record the exact repository revision or retrieval date, current division
  count, verifiable agent-file count, supported conversion targets, sample
  frontmatter, and whether README marketing counts match the tree. Do not keep
  `147+`, `230+`, or another estimate without current evidence and an explicit
  non-authoritative label.

- [ ] **Step 4: Add exact AI-agent analysis sections**

  Use `apply_patch` to add or normalize:

  ```markdown
  ### Provider-Native Adapter Status
  ### Upstream Snapshot — 2026-07-10
  ### Role and Coverage Gap Register
  ### Default, Escalation, and Fallback Routing
  ```

  Adapter Status columns: `Role`, `Claude`, `Codex`, `Gemini`, `Native/local
  distinction`, `Validation coverage`, `Verdict`.
  Upstream Snapshot columns: `Claim`, `Verified value`, `Evidence`, `Authority
  limitation`.
  Gap Register columns: `External pattern`, `Local coverage`, `Decision`,
  `Rationale`, `Canonical follow-up route` using only `Closed`, `Adapt`, or
  `Skip` unless current evidence justifies a new `Candidate`.
  Routing columns: `Local role`, `Task profile`, `Claude default/escalation/
  fallback`, `Codex default/escalation/fallback`, `Gemini default/escalation/
  fallback`, `Effort`, `Eval gate`.

- [ ] **Step 5: Validate and commit**

  ```bash
  rg -n 'Provider-Native Adapter Status|Upstream Snapshot|Role and Coverage Gap Register|Default, Escalation, and Fallback Routing|supervisor|observability-reviewer|network-reviewer|agency-agents|2026-07-10' docs/90.references/research/2026-07-07-wer/ai-agents-roster-and-gap-analysis.md
  git diff --check
  bash scripts/validate-harness.sh
  bash scripts/validate-repo-quality-gates.sh .
  ```

  Expected: all structures, newest roles, upstream reference, and date are
  found; validators exit 0. Update WERH-008 evidence/status and commit:

  ```bash
  git add docs/90.references/research/2026-07-07-wer/ai-agents-roster-and-gap-analysis.md docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md
  git commit -m 'docs(research): refresh AI agent roster and routing analysis'
  ```

### Task 9: Close Pack Coverage and Cross-Document Integration

**Files:**

- Modify: `docs/90.references/research/2026-07-07-wer/README.md`
- Modify: all seven Current reference documents only when cross-link,
  ownership, source-date, or contradiction repair is required
- Modify: `docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md`

**Interfaces:**

- Consumes: approved and reviewed outputs from Tasks 2-8.
- Produces: one primary owner for every requested topic, pack-wide source and
  freshness rules, changed-document summary, and resolved cross-document
  contradictions.

- [ ] **Step 1: Prove the pack README lacks the final coverage contract**

  ```bash
  rg -n 'Requirement Coverage Matrix|Audit Outcome Summary|Model Source Cutoff|Primary Current Owner' docs/90.references/research/2026-07-07-wer/README.md
  ```

  Expected: at least one heading is absent before editing.

- [ ] **Step 2: Build the complete requirement-owner mapping**

  Use `apply_patch` to add:

  ```markdown
  ## Model Source Cutoff
  ## Requirement Coverage Matrix
  ## Audit Outcome Summary
  ```

  Requirement Coverage Matrix columns must be `Requirement`, `Primary Current
  owner`, `Workspace evidence`, `External benchmark`, `Audit status`, and
  `Follow-up route`. Include separate rows for workspace purpose, roles,
  overview, operating contract, governance, system, rules, templates, scripts,
  integration guides, SDLC, PRD, ARD, ADR, guide, incident, postmortem, policy,
  release, runbook, security, Kubernetes, infrastructure, CI/CD, QA,
  formatting, linting, syntax validation, automation, pipeline, workflow,
  harness engineering, loop engineering, Claude, Codex, Gemini, shared
  provider environment/rules, AI agents, `agency-agents`, and task-model
  routing.

- [ ] **Step 3: Run cross-document contradiction and source checks**

  Search all Current files for agent counts, workflow/job counts, model IDs,
  source dates, `.gemini/agents`, `.agents/agents`, ApplicationSet ownership,
  hook names, and static/live language. Resolve contradictions in the primary
  owner and replace secondary duplicated analysis with a concise relative
  link. Preserve each reference's Authority Boundary and update README
  `Last reviewed` to `2026-07-10`.

- [ ] **Step 4: Run pack-wide coverage and quality gates**

  ```bash
  rg -n 'Requirement Coverage Matrix|Model Source Cutoff|Audit Outcome Summary|2026-07-10 10:00 KST' docs/90.references/research/2026-07-07-wer/README.md
  rg -n 'purpose|role|CI/CD|QA|formatting|linting|syntax|automation|pipeline|workflow|operating contract|template|script|integration|SDLC|governance|security|Kubernetes|infrastructure|harness|loop|Claude|Codex|Gemini|PRD|ARD|ADR|incident|postmortem|policy|release|runbook|agency-agents|model' docs/90.references/research/2026-07-07-wer
  git diff --check
  bash scripts/validate-harness.sh
  bash scripts/validate-repo-quality-gates.sh .
  ```

  Expected: coverage headings and all topic families are found; validators exit
  0. Update WERH-009 evidence/status and commit:

  ```bash
  git add docs/90.references/research/2026-07-07-wer docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md
  git commit -m 'docs(research): close current pack coverage and integration'
  ```

### Task 10: Run Final Validation and Close Execution Records

**Files:**

- Modify: `docs/04.execution/plans/2026-07-10-current-research-pack-fact-first-hardening.md`
- Modify: `docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: all reviewed task commits and review results.
- Produces: a substantively reviewed branch, independently reviewed closure
  evidence, complete lifecycle status, durable memory, and a clean branch.

- [ ] **Step 1: Verify only approved paths changed from the pinned branch base**

  The feature branch originated from `main` at immutable base
  `a70326b6443ffe6eb5cc6d1a8f4c48f425a0c4c4`. Use that SHA, not a moving
  branch name, for every whole-branch comparison and review package.

  ```bash
  git diff --name-only a70326b6443ffe6eb5cc6d1a8f4c48f425a0c4c4...HEAD
  git log --oneline a70326b6443ffe6eb5cc6d1a8f4c48f425a0c4c4..HEAD
  ```

  Expected: changes are limited to the approved Spec 017 addendum, Stage 04
  plan/task/index evidence, Current pack files, progress memory, and the
  `.gitignore` entries required by the approved worktree/SDD setup; commits are
  separated by the logical units in this plan.

- [ ] **Step 2: Run the pre-review deterministic validation bundle**

  ```bash
  git diff --check a70326b6443ffe6eb5cc6d1a8f4c48f425a0c4c4...HEAD
  bash scripts/validate-harness.sh
  bash scripts/validate-repo-quality-gates.sh .
  rg -n '\b(T[B]D|T[O]DO|F[I]XME|implement[[:space:]]+later)\b' docs/90.references/research/2026-07-07-wer docs/04.execution/plans/2026-07-10-current-research-pack-fact-first-hardening.md docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md
  ```

  Expected: both validators exit 0; incomplete-marker scan exits 1 with no
  matches. If `pre-commit` is installed, also run
  `pre-commit run --all-files` and record its exact result. Do not install
  missing optional tools in this task.

- [ ] **Step 3: Complete substantive whole-branch review and remediation**

  Generate the Superpowers whole-branch review package for
  `a70326b6443ffe6eb5cc6d1a8f4c48f425a0c4c4...HEAD`, dispatch an independent
  reviewer, and record the exact package boundary and verdict. Fix every
  Critical and Important finding in a logical reviewed fix wave, regenerate
  the package from the same pinned base, and repeat review until no Critical or
  Important finding remains. Re-run Step 2 after the last remediation commit.

  Do not mark WERH-010, the final Phase View item, plan/task lifecycle, index
  lifecycle, memory handoff, or whole-branch-review completion as final before
  this substantive review passes.

- [ ] **Step 4: Prepare and commit a provisional closure record**

  Use `apply_patch` to:

  - mark WERH-001 through WERH-009 `Done`, but keep WERH-010
    `Review Pending` and its Phase View checkbox unchecked;
  - record every validation command, output summary, task commit, substantive
    review verdict, optional-tool SKIP, and no-live/no-remote limitation without
    claiming that the closure-only review has occurred;
  - set plan/task frontmatter to `status: active` and keep the corresponding
    plan/task README rows `Active`;
  - leave the final-promotion Completion Criteria unchecked;
  - append a provisional progress-memory entry with Metadata, Progress, Memory,
    Evidence, and Handoff sections that explicitly says closure review is
    pending; and
  - keep the closure diff limited to the five files listed for Task 10.

  Validate the provisional closure files before commit:

  ```bash
  git diff --check
  bash scripts/validate-harness.sh
  bash scripts/validate-repo-quality-gates.sh .
  git status --short --branch
  ```

  Expected: validators exit 0; status shows only the five expected closure
  files. Commit the provisional, review-pending record:

  ```bash
  git add docs/04.execution/plans/2026-07-10-current-research-pack-fact-first-hardening.md docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md docs/04.execution/plans/README.md docs/04.execution/tasks/README.md docs/00.agent-governance/memory/progress.md
  git commit -m 'docs(execution): record provisional current research closure'
  ```

- [ ] **Step 5: Independently review the closure-only diff**

  Record the resulting immutable provisional commit as
  `<PROVISIONAL_CLOSURE_SHA>`. Build a focused review package for exactly
  `<PROVISIONAL_CLOSURE_SHA>^..<PROVISIONAL_CLOSURE_SHA>` and dispatch a fresh
  independent reviewer. The review must verify that the five-file closure
  evidence matches the already-approved substantive branch review and does not
  make premature, unsupported, live-runtime, or remote-readiness claims.

  Fix Critical and Important findings in another provisional closure commit
  and repeat the focused review against the exact immutable closure commit or
  commit range. Do not perform final lifecycle promotion until the focused
  reviewer returns a clean verdict.

- [ ] **Step 6: Validate and commit the final lifecycle promotion**

  Only after Step 5 passes, use `apply_patch` on the same five closure files to:

  - mark WERH-010 `Done` and check its Phase View item;
  - set plan/task frontmatter to `status: done` and set the corresponding
    plan/task README rows to `Done`;
  - check each Completion Criteria item whose evidence now exists;
  - record the closure-only review package boundary and clean verdict; and
  - finalize the progress-memory Handoff as complete without changing the
    no-live/no-remote evidence boundary.

  With those final promotion edits still pending, run the deterministic bundle
  against the complete working-tree state from the pinned base. Run the
  `pre-commit` command when installed; otherwise omit it and record an exact
  optional-tool SKIP:

  ```bash
  git diff --check a70326b6443ffe6eb5cc6d1a8f4c48f425a0c4c4
  git diff --name-only a70326b6443ffe6eb5cc6d1a8f4c48f425a0c4c4
  git log --oneline a70326b6443ffe6eb5cc6d1a8f4c48f425a0c4c4..HEAD
  pre-commit run --files docs/04.execution/plans/2026-07-10-current-research-pack-fact-first-hardening.md docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md docs/04.execution/plans/README.md docs/04.execution/tasks/README.md docs/00.agent-governance/memory/progress.md
  bash scripts/validate-harness.sh
  bash scripts/validate-repo-quality-gates.sh .
  rg -n '\b(T[B]D|T[O]DO|F[I]XME|implement[[:space:]]+later)\b' docs/90.references/research/2026-07-07-wer docs/04.execution/plans/2026-07-10-current-research-pack-fact-first-hardening.md docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md
  ```

  Expected: both validators pass, the incomplete-marker scan exits 1 with no
  matches, and the pinned-base path and commit inventory matches the approved
  scope. Record the exact command results, optional-tool limitations, pinned
  base, and no-live/no-remote boundary in the still-pending Task and progress
  memory. Do not claim post-commit verification at this point.

  After recording that evidence, run the final-state gates again so the
  recorded evidence itself is covered. This second pass is a commit gate, not
  another result to write back. If `pre-commit` is unavailable, preserve the
  recorded SKIP from the first pass and omit only that command:

  ```bash
  pre-commit run --files docs/04.execution/plans/2026-07-10-current-research-pack-fact-first-hardening.md docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md docs/04.execution/plans/README.md docs/04.execution/tasks/README.md docs/00.agent-governance/memory/progress.md
  git diff --check a70326b6443ffe6eb5cc6d1a8f4c48f425a0c4c4
  bash scripts/validate-harness.sh
  bash scripts/validate-repo-quality-gates.sh .
  git add docs/04.execution/plans/2026-07-10-current-research-pack-fact-first-hardening.md docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md docs/04.execution/plans/README.md docs/04.execution/tasks/README.md docs/00.agent-governance/memory/progress.md
  git diff --cached --check
  git diff --cached --name-only
  git diff --name-only
  git status --short --branch
  ```

  Expected: all final-state gates pass; the staged diff contains exactly the
  five closure files; no unstaged path remains; and the status contains only
  those five staged files. Commit the already-recorded, reviewed, and validated
  final evidence without another writeback:

  ```bash
  git commit -m 'docs(execution): close current research hardening evidence'
  ```

- [ ] **Step 7: Verify the committed branch and hand off without writeback**

  ```bash
  git diff --check a70326b6443ffe6eb5cc6d1a8f4c48f425a0c4c4...HEAD
  git diff --name-only a70326b6443ffe6eb5cc6d1a8f4c48f425a0c4c4...HEAD
  git log --oneline a70326b6443ffe6eb5cc6d1a8f4c48f425a0c4c4..HEAD
  bash scripts/validate-harness.sh
  bash scripts/validate-repo-quality-gates.sh .
  rg -n '\b(T[B]D|T[O]DO|F[I]XME|implement[[:space:]]+later)\b' docs/90.references/research/2026-07-07-wer docs/04.execution/plans/2026-07-10-current-research-pack-fact-first-hardening.md docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md
  git status --short --branch
  ```

  Expected: the committed branch remains valid, the incomplete-marker scan
  exits 1 with no matches, the full-branch paths and logical commits match the
  approved scope, and the worktree is clean. Report this post-commit result
  externally in the handoff; do not modify the completed plan, task, indexes,
  or memory to self-record it. If any check fails, reopen the lifecycle, make a
  reviewed fix, and repeat Steps 6 and 7 rather than leaving uncommitted
  evidence. On success, invoke `superpowers:finishing-a-development-branch`.

## Completion Criteria

- [x] All eight Current pack documents audited
- [x] Every requested topic mapped to one primary Current owner
- [x] Internal and external evidence recorded for every material comparison
- [x] Earlier related content integrated without Historical changes or active-policy duplication
- [x] Provider/model matrix reflects `2026-07-10 10:00 KST` and surface-specific lifecycle
- [x] Fact defects corrected and implementation gaps routed without active changes
- [x] Task-scoped reviews and substantive whole-branch review approved from pinned base `a70326b6443ffe6eb5cc6d1a8f4c48f425a0c4c4`
- [x] Provisional closure remains review-pending until its exact immutable closure diff is independently approved
- [x] WERH-010, Phase View, frontmatter, indexes, and memory promoted to final `Done` only after closure-only review approval
- [x] Required repo-static validation passed with limitations recorded
- [x] Pre-commit final-state validation passed from pinned base `a70326b6443ffe6eb5cc6d1a8f4c48f425a0c4c4` and its results are durable; post-commit clean verification is externally reported handoff evidence without writeback
- [x] Logical commits preserved

## Related Documents

- **Spec**: [Workspace Engineering Research Pack Specification](../../03.specs/017-workspace-engineering-research-pack/spec.md)
- **Tasks**: `../tasks/2026-07-10-current-research-pack-fact-first-hardening.md`
- **Current Research Pack**: [2026-07-07 Current WER Pack](../../90.references/research/2026-07-07-wer/README.md)
- **Historical Research Pack**: [2026-07-04 Historical WER Pack](../../90.references/research/2026-07-04-wer/README.md)
- **Reference Template**: [Reference Template](../../99.templates/templates/common/reference.template.md)
- **Task Template**: [Task Template](../../99.templates/templates/sdlc/execution/task.template.md)
