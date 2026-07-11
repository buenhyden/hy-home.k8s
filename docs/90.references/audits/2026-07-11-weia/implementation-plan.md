---
title: Workspace Engineering Research and Implementation Audit Integration Plan
type: content/reference
status: active
owner: platform
updated: 2026-07-11
---

# Workspace Engineering Research and Implementation Audit Integration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strengthen the Current workspace-engineering research pack in place
and publish one evidence-scored Current implementation audit pack without
modifying active workspace controls.

**Architecture:** The Current `2026-07-07-wer` pack remains the benchmark
owner. The `2026-07-11-weia` pack compares that benchmark with a fixed
repository snapshot through five focused audits and one remediation roadmap.
All reports share one requirement map, maturity scale, confidence vocabulary,
source cutoff, and Current-pointer contract.

**Tech Stack:** Markdown, Git, `rg`, `pre-commit`, repository quality gates,
official provider and standards documentation, and repo-static evidence.

## Overview

This document is the detailed, checkbox-driven execution plan for the approved
Stage 90 research and audit integration design. It decomposes the work into
independently reviewable and testable documentation tasks.

## Purpose

Provide exact file ownership, evidence inputs, outputs, validation commands,
review gates, and logical commit boundaries for Subagent-Driven execution.

## Reference Type

Execution design and evidence ledger for a dated implementation audit pack.
It is descriptive metadata within Stage 90, not an active Plan or Task contract
for the workspace runtime.

## Authority Boundary

This plan authorizes changes only within the two approved Stage 90 roots. It
does not override Stage 00 governance, Stage 99 templates, provider-native
configuration, CI, hooks, scripts, manifests, or operations procedure. Any
recommended active change requires a separately approved canonical SDLC owner.

## Scope

The plan covers the in-place Current research refresh, five implementation
audits, the integrated remediation roadmap, index reconciliation, evidence
review, and final validation. Live operations and active-file remediation are
excluded.

## Definitions / Facts

- `Current research`: `docs/90.references/research/2026-07-07-wer/`.
- `Current audit candidate`: `docs/90.references/audits/2026-07-11-weia/`.
- `Base commit`: `ab3556b8d5a9ae6f469a751057d9ad5ef261cdf7`.
- `Provider/model cutoff`: `2026-07-10 10:00 KST`.
- `Repo-static`: tracked file or deterministic local validation evidence; it
  is not runtime proof.
- `Logical task`: one independently testable deliverable with its own two-stage
  review and commit.

## Sources

- [Approved pack design](README.md)
- [Current research pack](../../research/2026-07-07-wer/README.md)
- [Research index](../../research/README.md)
- [Audit index](../README.md)
- [Reference template](../../../99.templates/templates/common/reference.template.md)
- Official provider and standards sources already inventoried in the Current
  research pack and reverified by the source-owning task.

## Review and Freshness

- Written and self-reviewed: 2026-07-11
- Review trigger: approved scope/design change, Current research owner change,
  audit report taxonomy change, source-cutoff change, or execution finding that
  invalidates task boundaries.
- Completion trigger: every checkbox is resolved, whole-branch reviews pass,
  and the final path-boundary and validation evidence are recorded.

## Global Constraints

- Modify only `docs/90.references/research/` and
  `docs/90.references/audits/`.
- Record active-file gaps only as recommendations and follow-up PRD, ARD, ADR,
  Spec, Plan, or Task routes with measurable acceptance evidence.
- Keep `2026-07-07-wer` as the Current research pack and strengthen it in
  place; do not delete or relocate historical packs.
- Use `2026-07-10 10:00 KST` as the provider/model source cutoff.
- Use base commit `ab3556b8d5a9ae6f469a751057d9ad5ef261cdf7`
  for initial inventory and record the final audit observation SHA separately.
- Separate repository-static, CI-declared, optional-tool, and live-runtime
  evidence.
- Do not infer local model availability from API catalogs or declarations.
- Do not claim live Kubernetes, Argo CD, Vault, ESO, network-policy, secret,
  deployment, or provider-runtime readiness.
- Use logical-unit commits and two review gates per task: specification/content
  first, then evidence/quality.
- Keep facts, observations, recommendations, and inference distinguishable.
- Link only files that exist; planned artifacts remain code literals.

## Approved Stage 90 Governance Exception

The user explicitly approved a Stage 90-only implementation boundary for this
integration. Bootstrap `progress.md` is therefore not edited because its
canonical path is outside the two approved `docs/90.references/research/` and
`docs/90.references/audits/` roots. The checkboxes in this implementation plan
and the branch's logical-unit commit history are the scoped durable execution
ledger for this exception. Any later active follow-up PRD, ARD, ADR, Spec,
Plan, or Task must restore the normal bootstrap `progress.md` workflow.

---

### Task 1: Freeze Inventory and the Measurement Contract

**Files:**

- Modify: `docs/90.references/research/2026-07-07-wer/README.md`
- Modify: `docs/90.references/audits/2026-07-11-weia/README.md`
- Modify: `docs/90.references/audits/2026-07-11-weia/implementation-plan.md`

**Interfaces:**

- Consumes: approved design, base commit, current research/audit indexes, and
  route/frontmatter contracts.
- Produces: the snapshot, requirement map, scoring formula, evidence
  vocabulary, and topic ownership consumed by Tasks 2-13.

- [x] **Step 1: Record exact repository and document inventory**

Run the pinned-tree recipe; do not read inventory facts from the worktree:

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

Expected: every count names its path, status basis, observation SHA, and date;
README files are distinguished from authored documents. The checked
path/status stream output is
`253fcd638675527ddc6d1df59a04628f3dadfff47a55de1ac9893a927a7f17fd  -`.

- [x] **Step 2: Add the shared measurement contract**

Use these exact levels: `0 absent`, `1 documented/routed`,
`2 repository-static`, `3 deterministic local+CI enforcement`, and
`4 runtime/operational evidence`. Calculate
`sum(maturity) / (4 * applicable controls)`, disclose the arithmetic and N/A
exclusions, retain `Implemented/Partial/Gap/Not in scope`, and use
`Verified repo-static/Unverified live/Conditional` for confidence.

- [x] **Step 3: Close requirement ownership**

Give every row in the 48-row requirement matrix, and every requested
cross-cutting topic, one primary research owner and one planned audit owner.
This includes frontmatter keys/values, state transition, semantic lineage,
Release, incident/postmortem readiness, AI-agent all-files pre-commit, vibe
coding, agency-agents, and task-model routing.

- [x] **Step 4: Validate and commit**

Run:

```bash
git diff --check
rg -n 'maturity|confidence|frontmatter|vibe|pre-commit run --all-files|Release' \
  docs/90.references/research/2026-07-07-wer/README.md \
  docs/90.references/audits/2026-07-11-weia/README.md
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --files \
  docs/90.references/research/2026-07-07-wer/README.md \
  docs/90.references/audits/2026-07-11-weia/README.md \
  docs/90.references/audits/2026-07-11-weia/implementation-plan.md
git add docs/90.references/research/2026-07-07-wer/README.md \
  docs/90.references/audits/2026-07-11-weia/README.md \
  docs/90.references/audits/2026-07-11-weia/implementation-plan.md
git commit -m "docs(research): harden audit traceability evidence"
```

Expected: all requested topics have owners and all checks pass.

### Task 2: Strengthen SDLC, Lifecycle, and Frontmatter Research

**Files:**

- Modify: `docs/90.references/research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md`

**Interfaces:**

- Consumes: Task 1 inventory and Stage 00/99 routing, lifecycle, template, and
  frontmatter owners.
- Produces: the SDLC/frontmatter benchmark consumed by Task 8 and the primary
  AI-agent `pre-commit run --all-files` obligation benchmark consumed by
  Task 9.

- [x] **Step 1: Recount and cite the lifecycle**

Inspect the stage-authoring matrix, document routing, SDLC governance,
template routing, frontmatter schema, and repo-quality validator. Record counts
by family/status for PRD, ARD, ADR, Spec, agent-design, Plan, Task, Guide,
Policy, Runbook, Incident, Postmortem, Reference, and README. Preserve
`42/43 done` only as an explicitly labeled historical 2026-07-10 observation
and record `43/43 done` as the fixed-snapshot result.

- [x] **Step 2: Add document-role and necessity matrices**

For PRD, ARD, ADR, Spec, Plan, Task, Guide, Policy, Runbook, Incident,
Postmortem, Release, Reference, and README, state purpose, input, output,
owner, expected state path, retention, overlap risk, and criteria for keep,
consolidate, archive, or decline.

- [x] **Step 3: Define research candidate transitions and lineage**

Document, without changing policy:

```text
PRD: draft -> active -> done
ARD/ADR: draft -> active -> accepted
Spec: draft -> active -> done
Plan/Task: draft -> active -> done
Operations: draft -> active -> accepted
Archive: tombstone plus replacement or preservation reason
```

Cover approval evidence, reverse transitions, umbrella-number exceptions,
PRD requirement-to-Spec-to-Task-to-validation coverage, and draft-Spec versus
done-Task asymmetry.

- [x] **Step 4: Add the profile-specific frontmatter benchmark**

Assess the current five keys and automation-consumer candidates: common `id`,
`created`, `review_due`, `supersedes`; Reference `source_checked`; Incident
`incident_id`, `severity`, `incident_state`. Cover `owner: platform`, title and
date validity, placeholders, future dates, allowed states, approval location,
and body-versus-metadata ownership. Do not recommend universal expansion
without a consumer.

- [x] **Step 5: Add Release and exercise decision gates**

Treat Release as an ADR-first home-lab decision. Treat zero real incidents and
postmortems as neutral; identify missing tabletop/exercise evidence as the
readiness uncertainty.

Define the primary AI-agent QA obligation benchmark here: use changed-file and
affected-lane validation during iteration; require
`pre-commit run --all-files` before PR/merge and after hook, validator,
toolchain, or global-format changes; record unavailable/skipped tools; and
separate PostToolUse feedback from full-suite proof.

- [x] **Step 6: Validate and commit**

```bash
rg -n 'PRD|ARD|ADR|Release|frontmatter|state transition|lineage|exercise' \
  docs/90.references/research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --files \
  docs/90.references/research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md
git add docs/90.references/research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md
git commit -m "docs(research): deepen SDLC and frontmatter benchmark"
```

Expected: every document family and metadata class has a benchmark and all
checks pass.

### Task 3: Add Vibe-Coding and AI-Agent Verification Research

**Files:**

- Modify: `docs/90.references/research/2026-07-07-wer/ai-agents-roster-and-gap-analysis.md`

**Interfaces:**

- Consumes: fixed cutoff, pinned agency-agents snapshot, local 10-role/
  30-adapter inventory, Task 1 scoring contract, and Task 2's primary
  AI-agent QA obligation benchmark.
- Produces: the vibe-coding, role, and model-routing benchmark consumed by
  Task 11, plus secondary role/application implications linked to Task 2's
  primary QA benchmark.

- [x] **Step 1: Research vibe coding with source classes separated**

Use the coined/original discussion only as contextual definition. Use NIST
SSDF, relevant OWASP guidance, and official provider secure-use/coding-agent
guidance for controls. Record title, publisher, URL, date, check date,
authority class, and supported claim.

- [x] **Step 2: Define risk-bounded controls**

Cover prompt-led exploration, executable acceptance criteria, small diffs,
tests, static checks, independent review, provenance, secrets/permissions,
rollback, and stopping/escalation. Classify infrastructure, GitOps, identity,
secret, network, and security-policy changes as AI-assisted but evidence- and
approval-gated.

- [x] **Step 3: Record secondary AI-agent QA implications**

Describe how role instructions, provider adapters, and vibe-coding controls
apply Task 2's AI-agent QA obligation. Link to the SDLC research owner instead
of restating or redefining the primary benchmark, and record only secondary
role/application implications such as adapter feedback versus full-suite
proof.

- [x] **Step 4: Refresh role and model-routing criteria**

Keep active declaration, default, escalation, fallback, eval gate, and
availability confidence separate. Require telemetry and a non-overlap case
before recommending a new role such as FinOps.

- [x] **Step 5: Validate and commit**

```bash
rg -n 'vibe|pre-commit run --all-files|default|escalation|fallback|eval|FinOps' \
  docs/90.references/research/2026-07-07-wer/ai-agents-roster-and-gap-analysis.md
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --files \
  docs/90.references/research/2026-07-07-wer/ai-agents-roster-and-gap-analysis.md
git add docs/90.references/research/2026-07-07-wer/ai-agents-roster-and-gap-analysis.md
git commit -m "docs(research): add vibe coding and agent QA controls"
```

Expected: contextual claims and normative controls are distinct, each URL
supports its claim, and checks pass.

### Task 4: Refresh Harness, Loop, and Provider Research

**Files:**

- Modify: `docs/90.references/research/2026-07-07-wer/harness-and-loop-engineering.md`
- Modify: `docs/90.references/research/2026-07-07-wer/provider-implementation-status.md`

**Interfaces:**

- Consumes: the fixed official-source cutoff, local provider surfaces, Stage 00
  harness owners, and Task 1 evidence vocabulary.
- Produces: control IDs and provider comparisons consumed by Task 7.

- [x] **Step 1: Verify official claims at the cutoff**

Check official Anthropic, OpenAI, and Google documentation for agents,
subagents, hooks, permissions/sandbox, model lifecycle, and native paths.
Retain the fixed cutoff; label page changes after it as outside the snapshot.

- [x] **Step 2: Reconcile native and local surfaces**

For each provider, record native path, local adapter, tracked settings, model
declaration, hook wiring, project config, validator coverage, runtime evidence,
and confidence. State that `.agents/agents` is not native Gemini CLI
registration.

- [x] **Step 3: Complete the loop control model and gap register**

Ensure Observe/Plan/Act/Verify/Learn covers evidence, owner, output, failure,
retry budget, repeated-failure threshold, termination, eval trace, recoverable
compaction checkpoint, memory, approval, and MCP inventory/security. Preserve
or explicitly supersede HL-001 through HL-007 and retain stale `Eight/eight`,
native-consumption, model-currentness, and MCP gaps as routed findings.

- [x] **Step 4: Validate and commit**

```bash
rg -n 'Observe|Plan|Act|Verify|Learn|retry|compaction|MCP|Gemini CLI|Unverified' \
  docs/90.references/research/2026-07-07-wer/harness-and-loop-engineering.md \
  docs/90.references/research/2026-07-07-wer/provider-implementation-status.md
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --files \
  docs/90.references/research/2026-07-07-wer/harness-and-loop-engineering.md \
  docs/90.references/research/2026-07-07-wer/provider-implementation-status.md
git add docs/90.references/research/2026-07-07-wer/harness-and-loop-engineering.md \
  docs/90.references/research/2026-07-07-wer/provider-implementation-status.md
git commit -m "docs(research): refresh harness and provider controls"
```

Expected: native, local-static, and runtime evidence remain separate and all
checks pass.

### Task 5: Refresh Governance, Automation, Kubernetes, and Security Research

**Files:**

- Modify: `docs/90.references/research/2026-07-07-wer/workspace-governance-baseline.md`
- Modify: `docs/90.references/research/2026-07-07-wer/automation-pipeline-workflow-qa.md`
- Modify: `docs/90.references/research/2026-07-07-wer/kubernetes-infrastructure-security.md`

**Interfaces:**

- Consumes: Task 1 snapshot, current workflows/configs/manifests/scripts as
  read-only evidence, and existing governance/automation/security gap IDs.
- Produces: controls consumed by Tasks 7, 9, 10, and 12.

- [x] **Step 1: Refresh workspace owner and authority evidence**

Recheck purpose, roles, canonical owners, rules, enforcement, templates,
scripts, integrations, CI, operations, archive, and Stage 90 boundaries. Record
duplicated lifecycle summaries and Current drift as consolidation findings.

- [x] **Step 2: Recount automation and CI topology**

Inspect workflows, pre-commit, Prettier config/ignore, shared hooks, and
validators. Record workflow/job counts, actual DAG, path filters, specialist
lanes, aggregate gate, optional tools, GitOps CD boundary, Prettier wiring,
Action pinning, artifacts, supply-chain evidence, and DORA evidence.

- [x] **Step 3: Refresh Kubernetes and security evidence**

Recheck desired-state ownership, Kustomize, AppProjects, Vault, ESO, TLS,
secret transport and arguments, RBAC, NetworkPolicy, policy validation, image
and workflow supply chain, and static/live boundaries. Preserve SEC IDs or
record explicit supersession.

- [x] **Step 4: Compare restructuring options**

For Minimal, Consolidated, and Full redesign, state scope, benefit, cost,
blast radius, prerequisites, migration, rollback, and decision owner. Keep
Consolidated as the evidence-supported default unless findings disprove it.

- [x] **Step 5: Validate and commit**

```bash
rg -n 'Consolidated|Full redesign|Prettier|path filter|DORA|Vault|ESO|NetworkPolicy' \
  docs/90.references/research/2026-07-07-wer/workspace-governance-baseline.md \
  docs/90.references/research/2026-07-07-wer/automation-pipeline-workflow-qa.md \
  docs/90.references/research/2026-07-07-wer/kubernetes-infrastructure-security.md
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --files \
  docs/90.references/research/2026-07-07-wer/workspace-governance-baseline.md \
  docs/90.references/research/2026-07-07-wer/automation-pipeline-workflow-qa.md \
  docs/90.references/research/2026-07-07-wer/kubernetes-infrastructure-security.md
git add docs/90.references/research/2026-07-07-wer/workspace-governance-baseline.md \
  docs/90.references/research/2026-07-07-wer/automation-pipeline-workflow-qa.md \
  docs/90.references/research/2026-07-07-wer/kubernetes-infrastructure-security.md
git commit -m "docs(research): refresh governance delivery and platform evidence"
```

Expected: topology/counts match the snapshot, live claims are not inferred,
and checks pass.

### Task 6: Finalize the Audit Method and Report Interfaces

**Files:**

- Modify: `docs/90.references/audits/2026-07-11-weia/README.md`
- Modify: `docs/90.references/audits/2026-07-11-weia/implementation-plan.md`

**Interfaces:**

- Consumes: completed research benchmark from Tasks 1-5.
- Produces: report contracts, control ownership, scoring rules, snapshot, and
  priority vocabulary consumed by Tasks 7-12.

- [x] **Step 1: Record snapshot and report contracts**

Record base SHA, audit observation SHA, cutoff, excluded live lanes, report
responsibilities, and one owner per cross-cutting topic. Link completed
research and retain uncreated reports as code literals.

- [x] **Step 2: Define exact row fields and priorities**

Every control row contains `ID`, benchmark, expected control, repo evidence,
maturity, verdict, confidence, gap, recommendation, priority, follow-up owner,
and acceptance evidence. Priorities are `P0 immediate safety`, `P1 near-term
integrity`, `P2 planned improvement`, and `P3 optional/telemetry-gated`.

- [x] **Step 3: Define contradiction ownership**

Assign one report owner for lifecycle, provider implementation, CI DAG,
Kubernetes/security, agent roster, model routing, and roadmap priority.
Secondary reports link rather than duplicate volatile facts.

- [x] **Step 4: Validate and commit**

```bash
rg -n 'acceptance evidence|P0|P1|P2|P3|observation SHA|code literal' \
  docs/90.references/audits/2026-07-11-weia/README.md
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --files \
  docs/90.references/audits/2026-07-11-weia/README.md \
  docs/90.references/audits/2026-07-11-weia/implementation-plan.md
git add docs/90.references/audits/2026-07-11-weia/README.md \
  docs/90.references/audits/2026-07-11-weia/implementation-plan.md
git commit -m "docs(audit): finalize evidence and scoring contract"
```

Expected: the README is a complete audit entrypoint and checks pass.

### Task 7: Audit Governance, Harness, Loop, and Provider Parity

**Files:**

- Create: `docs/90.references/audits/2026-07-11-weia/governance-harness-loop-providers.md`

**Interfaces:**

- Consumes: Tasks 4-6 controls and method.
- Produces: governance/harness/provider scores and routed findings for Task
  12, plus canonical provider implementation and availability facts consumed
  by Task 11.

- [x] **Step 1: Build governance and harness matrices**

Cover purpose, roles, authority, contracts, owners, rules, templates, scripts,
integration guides, security boundary, shared assets, duplicated summaries,
Observe/Plan/Act/Verify/Learn, retry, termination, eval, recovery, compaction,
memory, approval, tools/MCP, hooks, canaries, and feedback evidence.

- [x] **Step 2: Build provider and common-system matrices**

Score Claude, Codex, and Gemini separately for provider/local declarations,
native loading and registration, settings/hooks/config, model declarations,
sandbox/permissions, validator semantics, and entitlement/runtime availability
evidence and confidence. Score the common stem/body/workflow/output-style/
memory/script layer without treating it as one native runtime. This task owns
those implementation facts; role-specific default, escalation, fallback, eval,
and adoption recommendations belong to Task 11.

- [x] **Step 3: Calculate scores and route gaps**

Show numerator, denominator, N/A rows, verdict/confidence distributions, and
never award maturity 4 to static controls. Each Partial/Gap states missing,
corrective, complementary, unnecessary, priority, follow-up document, and
acceptance evidence.

- [x] **Step 4: Validate and commit**

```bash
rg -n 'Claude|Codex|Gemini|Observe|retry|compaction|MCP|maturity|acceptance' \
  docs/90.references/audits/2026-07-11-weia/governance-harness-loop-providers.md
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --files \
  docs/90.references/audits/2026-07-11-weia/governance-harness-loop-providers.md
git add docs/90.references/audits/2026-07-11-weia/governance-harness-loop-providers.md
git commit -m "docs(audit): assess governance harness and provider parity"
```

Expected: provider/common scores are independently auditable and checks pass.

### Task 8: Audit SDLC, Document Lifecycle, and Frontmatter

**Files:**

- Create: `docs/90.references/audits/2026-07-11-weia/sdlc-document-lifecycle-frontmatter.md`

**Interfaces:**

- Consumes: Task 2 benchmark and Task 6 method.
- Produces: lifecycle, lineage, metadata, Release, and readiness findings for
  Task 12.

- [x] **Step 1: Audit flow and document families**

Score PRD, ARD, ADR, Spec, Plan, Task, Guide, Policy, Runbook, Incident,
Postmortem, Release, Reference, and README roles, routes, templates, states,
and evidence. Identify implemented, overlapping, unnecessary, missing, and
conditional families.

- [x] **Step 2: Audit numbering, lineage, and transitions**

Compare documented rules with actual paths/statuses. Measure PRD
requirement-to-Spec-to-Task-to-validation traceability, link versus semantic
lineage, numbering exceptions, upstream/downstream state mismatch, and
reverse-transition evidence.

- [x] **Step 3: Audit frontmatter keys and values**

For every family, assess required keys, value domains, placeholder rejection,
date validity, ownership precision, allowed states, review freshness,
supersession, source freshness, and incident metadata. Keep body-owned
information out of metadata unless an automation consumer exists.

- [x] **Step 4: Compare target states and route findings**

Score Minimal, Consolidated, and Full redesign for benefit, cost, migration,
rollback, blast radius, and prerequisites. Show maturity arithmetic, N/A
exclusions, unnecessary controls, priority, owner, and acceptance evidence.

- [x] **Step 5: Validate and commit**

```bash
rg -n 'PRD|ARD|ADR|Incident|Postmortem|Release|frontmatter|lineage|Consolidated' \
  docs/90.references/audits/2026-07-11-weia/sdlc-document-lifecycle-frontmatter.md
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --files \
  docs/90.references/audits/2026-07-11-weia/sdlc-document-lifecycle-frontmatter.md
git add docs/90.references/audits/2026-07-11-weia/sdlc-document-lifecycle-frontmatter.md
git commit -m "docs(audit): assess SDLC lifecycle and frontmatter"
```

Expected: every family and baseline key/value class has a verdict and checks
pass.

### Task 9: Audit CI/CD, QA, Formatting, Linting, and Automation

**Files:**

- Create: `docs/90.references/audits/2026-07-11-weia/ci-qa-automation-pipeline-workflow.md`

**Interfaces:**

- Consumes: Task 2 SDLC and primary AI-agent QA obligation benchmark, Task 5
  automation benchmark, and Task 6 method.
- Produces: delivery and quality findings for Task 12.

- [x] **Step 1: Audit CI/CD topology and ownership**

Score triggers, permissions, concurrency, DAG roots, specialist jobs,
aggregate gates, path filters, caches/artifacts, reusable workflows, changelog,
deploy ownership, Argo CD pull/reconcile boundary, and DORA evidence.

- [x] **Step 2: Audit QA and AI-agent obligations**

Score formatting, linting, syntax/parser, Markdown, data formats, shell,
Actions, Dockerfile, Kubernetes, secrets, policy, artifact, and live lanes.
Separate configuration, local execution, CI enforcement, optional fallback,
and live proof. Compare agent gateways/bodies/postflight/workflows/guidance with
the risk-based all-files pre-commit rule.

- [x] **Step 3: Audit security and supply-chain automation**

Score Action pinning, CodeQL, dependency review, SBOM, provenance,
attestation, Scorecard, artifact retention, and secret scanning according to
repository relevance. Mark controls conditional or unnecessary when the
home-lab threat model does not justify them.

- [x] **Step 4: Calculate scores and route findings**

Show arithmetic, N/A reasons, confidence, priority, owner, and acceptance
evidence for every recommendation.

- [x] **Step 5: Validate and commit**

```bash
rg -n 'CI/CD|pre-commit run --all-files|Formatting|Linting|DORA|SBOM|provenance' \
  docs/90.references/audits/2026-07-11-weia/ci-qa-automation-pipeline-workflow.md
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --files \
  docs/90.references/audits/2026-07-11-weia/ci-qa-automation-pipeline-workflow.md
git add docs/90.references/audits/2026-07-11-weia/ci-qa-automation-pipeline-workflow.md
git commit -m "docs(audit): assess delivery quality and automation"
```

Expected: configured, executed, enforced, optional, and live lanes are
separate and checks pass.

### Task 10: Audit Kubernetes, Infrastructure, GitOps, and Security

**Files:**

- Create: `docs/90.references/audits/2026-07-11-weia/kubernetes-infrastructure-security.md`

**Interfaces:**

- Consumes: Task 5 platform/security benchmark and Task 6 method.
- Produces: platform/security findings for Task 12.

- [x] **Step 1: Audit desired state and GitOps ownership**

Score manifest/Kustomize structure, Application/AppProject ownership,
workload discovery, reconciliation declarations, health/sync assertions,
rollback, environment boundaries, and static/live evidence.

- [x] **Step 2: Audit identity, secret, transport, network, and policy**

Score RBAC, AppProject boundaries, Vault TLS/verification, ESO transport and
audience compatibility, secret exposure in arguments, rotation/reconciliation,
NetworkPolicy desired state/enforcement confidence, policy-as-code, manifest
linting, image identity, workflow pinning, and admin-equivalent boundaries.

- [x] **Step 3: Reconcile SEC findings and calculate scores**

Map SEC-001 through SEC-014 to evidence, verdict, maturity, confidence,
priority, follow-up owner, and acceptance evidence; explicitly supersede
findings whose evidence changed. Disclose arithmetic and N/A exclusions.

- [x] **Step 4: Validate and commit**

```bash
rg -n 'GitOps|Vault|ESO|TLS|NetworkPolicy|SEC-0|Unverified live|acceptance' \
  docs/90.references/audits/2026-07-11-weia/kubernetes-infrastructure-security.md
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --files \
  docs/90.references/audits/2026-07-11-weia/kubernetes-infrastructure-security.md
git add docs/90.references/audits/2026-07-11-weia/kubernetes-infrastructure-security.md
git commit -m "docs(audit): assess Kubernetes infrastructure and security"
```

Expected: desired state and live enforcement are distinct, retained SEC
findings have current evidence, and checks pass.

### Task 11: Audit AI Agents, Models, Agency-Agents, and Vibe Coding

**Files:**

- Create: `docs/90.references/audits/2026-07-11-weia/ai-agents-model-routing-vibe-coding.md`

**Interfaces:**

- Consumes: Tasks 3 and 6 plus Task 7's canonical provider/local declaration,
  native-loading/registration, settings/hooks/config, and entitlement/runtime
  availability evidence and confidence. Task 7 already consumes Task 4.
- Produces: role, instruction, upstream, vibe-coding, and role-specific model
  default/escalation/fallback/eval recommendations and adoption decisions for
  Task 12.

- [ ] **Step 1: Audit the local role and adapter system**

Score ten roles, shared bodies, instructions, tools, permissions, outputs,
handoff, eval, and semantic validator depth. Use Task 7's thirty-adapter and
provider implementation facts by link; do not duplicate or rescore provider
metadata, declarations, native loading/registration, settings/hooks/config, or
entitlement/runtime availability evidence. Treat stem parity as inventory
evidence only.

- [ ] **Step 2: Compare pinned agency-agents patterns**

Compare responsibilities and reusable content rather than raw count. Classify
each relevant pattern as `Adapt`, `Already covered`, `Skip`, or
`Telemetry-gated`; improve existing roles before proposing new ones.

- [ ] **Step 3: Audit model routing and vibe controls**

For each role, consume Task 7's active declaration, auth/entitlement surface,
runtime availability evidence, and confidence as fixed inputs. Own only the
role-specific default, escalation, fallback, eval gate, lifecycle risk,
context/tool need, cost/latency recommendation, and adoption decision; link
back to Task 7 instead of restating provider facts. Score spec, acceptance
criteria, diff size, tests, static gates, independent review, provenance,
secrets/permissions, rollback, and stopping rules for vibe coding.

- [ ] **Step 4: Calculate scores and route findings**

Show arithmetic, N/A exclusions, confidence, priority, unnecessary role
proposals, existing-role modifications, new-role threshold, follow-up owner,
and acceptance evidence.

- [ ] **Step 5: Validate and commit**

```bash
rg -n 'agency-agents|vibe|default|escalation|fallback|availability|Adapt|Skip' \
  docs/90.references/audits/2026-07-11-weia/ai-agents-model-routing-vibe-coding.md
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --files \
  docs/90.references/audits/2026-07-11-weia/ai-agents-model-routing-vibe-coding.md
git add docs/90.references/audits/2026-07-11-weia/ai-agents-model-routing-vibe-coding.md
git commit -m "docs(audit): assess agents models and vibe coding"
```

Expected: Task 7 owns provider implementation and runtime-availability facts;
Task 11 links those inputs and owns role-specific routing/adoption decisions,
upstream discovery, and vibe-coding findings. Checks pass.

### Task 12: Build the Integrated Remediation Roadmap

**Files:**

- Create: `docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md`

**Interfaces:**

- Consumes: findings and scores from Tasks 7-11.
- Produces: de-duplicated priority, dependency, target-state, and follow-up map
  consumed by Task 13 and future approved SDLC work.

- [ ] **Step 1: Normalize findings**

Assign one ID, owner report, evidence, root cause, dependency, priority, and
superseded historical finding to each gap. Secondary reports link to the owner.

- [ ] **Step 2: Build the target operating model and options**

Describe governance, lifecycle, harness, provider, agent, delivery, platform,
security, evidence, and review responsibilities. Compare Minimal,
Consolidated, and Full redesign with cost, benefit, blast radius, migration,
rollback, and prerequisites.

- [ ] **Step 3: Build phased follow-up routes**

Create phases for safety/integrity, lifecycle traceability, provider/harness
verification, delivery/supply-chain evidence, and optional optimization. For
each phase, name the first PRD/ARD/ADR/Spec/Plan/Task/Guide/Policy/Runbook
owner and exact acceptance evidence.

- [ ] **Step 4: Record adoption and rejection decisions**

Identify controls/document families that are unnecessary, telemetry-gated, or
ADR-first. Do not convert every external practice into a local requirement.

- [ ] **Step 5: Validate and commit**

```bash
rg -n 'P0|P1|P2|P3|Minimal|Consolidated|Full redesign|PRD|ARD|ADR|Spec|acceptance' \
  docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --files \
  docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md
git add docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md
git commit -m "docs(audit): route integrated remediation roadmap"
```

Expected: every non-implemented finding has one owner and one disposition and
checks pass.

### Task 13: Reconcile Current Pointers and Verify the Whole Pack

**Files:**

- Modify: `docs/90.references/research/README.md`
- Modify: `docs/90.references/research/2026-07-07-wer/README.md`
- Modify: `docs/90.references/audits/README.md`
- Modify: `docs/90.references/audits/2026-07-11-weia/README.md`
- Modify: `docs/90.references/audits/2026-07-11-weia/implementation-plan.md`
- Correct only review-proven errors in reports changed by Tasks 2-12.

**Interfaces:**

- Consumes: complete research/audit packs and all task reviews.
- Produces: one Current research pointer, one Current audit pointer, historical
  status for replaced snapshots, complete links, and final evidence.

- [ ] **Step 1: Resolve indexes and historical status**

Make `2026-07-07-wer` the only Current research pack and `2026-07-11-weia` the
only Current implementation audit pack. Mark older audit entries Historical or
Resolved without deleting, moving, or rewriting snapshot bodies. Link every
completed report from its pack README and parent index.

- [ ] **Step 2: Close requirement coverage**

For every request, verify one research owner, one audit owner, one score/
verdict, and one follow-up disposition. Explicitly cover frontmatter values,
state transitions, Release, incidents/postmortems, all-files pre-commit, vibe
coding, provider/common harness, agency-agents, and model routing.

- [ ] **Step 3: Recheck arithmetic, counts, sources, and contradictions**

Recompute scores and N/A denominators; rerun counts; verify URLs and cutoff;
search for the former unlabeled Task-count wording while preserving explicitly
labeled historical 2026-07-10 observations, duplicate Current labels,
conflicting role/workflow/job counts, native Gemini mislabeling, and
live-readiness overclaims.

- [ ] **Step 4: Enforce the path boundary**

```bash
git diff --name-only ab3556b8d5a9ae6f469a751057d9ad5ef261cdf7...HEAD
git diff --name-only ab3556b8d5a9ae6f469a751057d9ad5ef261cdf7...HEAD | \
  awk '!/^docs\/90\.references\/(research|audits)\// { print; bad=1 } END { exit bad }'
rg -n '42/43 [T]asks were done at audit time|\.agents/agents[^|.]*is [Nn]ative Gemini|live readiness.*[I]mplemented' \
  docs/90.references/research/2026-07-07-wer \
  docs/90.references/audits/2026-07-11-weia
```

Expected: every changed path is under the two approved roots and stale or
overclaim searches have no unresolved matches.

- [ ] **Step 5: Run full validation**

```bash
git diff --check ab3556b8d5a9ae6f469a751057d9ad5ef261cdf7...HEAD
bash scripts/validate-repo-quality-gates.sh .
bash docs/00.agent-governance/scripts/validate-harness.sh
pre-commit run --all-files
git status --short --branch
```

Expected: all commands pass before final integration metadata is committed.

- [ ] **Step 6: Run whole-branch reviews and correct findings**

Require one specification/content review and one evidence/quality review over
the complete diff. Correct every accepted finding in its owning commit or one
clearly labeled final review-fix commit, then rerun Step 5.

- [ ] **Step 7: Commit final integration metadata**

```bash
git add docs/90.references/research/README.md \
  docs/90.references/research/2026-07-07-wer/README.md \
  docs/90.references/audits/README.md \
  docs/90.references/audits/2026-07-11-weia/README.md \
  docs/90.references/audits/2026-07-11-weia/implementation-plan.md
git commit -m "docs(audit): publish Current implementation audit pack"
```

Expected: indexes, metadata, and the execution ledger describe the reviewed
final state and the worktree is clean.

## Execution Choice

The approved mode is Subagent-Driven Development: use a fresh implementer for
each task, then run specification/content and evidence/quality reviews before
advancing. This checklist is the durable execution ledger.

## Related Documents

- [Approved Audit Pack Design](README.md)
- [Current Research Pack](../../research/2026-07-07-wer/README.md)
- [Audits Index](../README.md)
- [Research Index](../../research/README.md)
