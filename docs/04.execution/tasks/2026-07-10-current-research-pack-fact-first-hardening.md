---
title: 'Task: Current Research Pack Fact-First Hardening'
type: sdlc/task
status: draft
owner: platform
updated: 2026-07-10
---

# Task: Current Research Pack Fact-First Hardening

## Overview

This document tracks the in-place, fact-first audit of the Current workspace
engineering research pack. It is the execution source of truth for baseline
inventory, claim provenance, task status, validation evidence, review outcomes,
and logical commits. The work is documentation-only and does not establish
live runtime or remote readiness.

## Inputs

- **Parent Spec**:
  [Workspace Engineering Research Pack specification and 2026-07-10 addendum](../../03.specs/017-workspace-engineering-research-pack/spec.md)
- **Parent Plan**:
  [Current Research Pack Fact-First Hardening Implementation Plan](../plans/2026-07-10-current-research-pack-fact-first-hardening.md)
- **Current Pack**:
  [2026-07-07 Workspace Engineering Research Pack](../../90.references/research/2026-07-07-wer/README.md)
- **Historical Context**:
  [2026-07-04 Workspace Engineering Research Pack](../../90.references/research/2026-07-04-wer/README.md)
- **Provider-model source cutoff**: `2026-07-10 10:00 KST`

## Working Rules

- Audit the Current pack README and all seven Current references in place.
- Preserve `docs/90.references/research/2026-07-04-wer/` unchanged as a
  Historical snapshot.
- Support local implementation claims with current repository evidence and
  external capability claims with official provider, standards-body, or
  upstream project evidence.
- Record exact external URLs, source checked dates, refresh triggers, and the
  distinction among repo fact, external fact, interpretation, recommendation,
  and unverified claims.
- Summarize active policy and link to its canonical owner; do not duplicate
  normative bodies in Stage 90 research.
- Record implementation gaps as non-mutating recommendations with severity,
  rationale, and canonical follow-up routes.
- Keep API, coding-agent product, CLI, local adapter, lifecycle, and
  recommendation claims surface-specific.
- Use repo-static validation as documentation evidence only. Do not infer live
  runtime, Kubernetes, Argo CD, Vault, ESO, provider, credential, secret, or
  deployment readiness.
- Do not perform live, remote, credential, secret, provider-runtime, publish,
  push, merge, or third-party mutation actions.
- Run focused assertions before and after each task, record deterministic
  validation, and capture task-scoped review and commit evidence.

## Baseline Evidence

### Current Pack Inventory

The Current pack contains exactly eight Markdown files:

| # | Current file | Primary responsibility |
| --- | --- | --- |
| 1 | `docs/90.references/research/2026-07-07-wer/README.md` | Pack coverage, cutoff, reading order, authority, and freshness. |
| 2 | `docs/90.references/research/2026-07-07-wer/workspace-governance-baseline.md` | Workspace governance and owner/authority baseline. |
| 3 | `docs/90.references/research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md` | SDLC, document taxonomy, CI, QA, and validation lanes. |
| 4 | `docs/90.references/research/2026-07-07-wer/harness-and-loop-engineering.md` | Harness and bounded-loop engineering. |
| 5 | `docs/90.references/research/2026-07-07-wer/provider-implementation-status.md` | Provider surfaces, local adapters, and model lifecycle. |
| 6 | `docs/90.references/research/2026-07-07-wer/automation-pipeline-workflow-qa.md` | Automation, pipeline, workflow, and QA topology. |
| 7 | `docs/90.references/research/2026-07-07-wer/kubernetes-infrastructure-security.md` | Kubernetes, infrastructure, and security boundaries. |
| 8 | `docs/90.references/research/2026-07-07-wer/ai-agents-roster-and-gap-analysis.md` | Local roster, upstream comparison, and task-model routing. |

### Local Agent Adapter Inventory

The same ten local agent stems exist across each provider/native adapter
surface: `.claude/agents/<stem>.md`, `.agents/agents/<stem>.md`, and
`.codex/agents/<stem>.toml`.

| # | Agent stem | Claude | Shared | Codex |
| --- | --- | --- | --- | --- |
| 1 | `code-reviewer` | Present | Present | Present |
| 2 | `doc-writer` | Present | Present | Present |
| 3 | `gitops-reviewer` | Present | Present | Present |
| 4 | `incident-responder` | Present | Present | Present |
| 5 | `k8s-implementer` | Present | Present | Present |
| 6 | `network-reviewer` | Present | Present | Present |
| 7 | `observability-reviewer` | Present | Present | Present |
| 8 | `security-auditor` | Present | Present | Present |
| 9 | `supervisor` | Present | Present | Present |
| 10 | `wiki-curator` | Present | Present | Present |

This inventory proves file-stem parity only; it does not prove provider-native
registration, runtime loading, permission enforcement, or live behavior.

### GitHub Workflow and CI Job Inventory

Five workflow files are present:

| # | Workflow file |
| --- | --- |
| 1 | `.github/workflows/ci.yml` |
| 2 | `.github/workflows/generate-changelog.yml` |
| 3 | `.github/workflows/greetings.yml` |
| 4 | `.github/workflows/labeler.yml` |
| 5 | `.github/workflows/stale.yml` |

The repository CI workflow declares six jobs:
`branch-policy`, `changes`, `pre-commit`, `repo-quality-static`,
`manifest-static`, and `ci-summary`. This is repo-static workflow evidence;
no remote GitHub Actions run or branch-protection state was inspected.

### Evidence Boundary and Optional Tools

- Baseline repository validation:
  `bash scripts/validate-repo-quality-gates.sh .` exited 0 with
  `[PASS] repository quality gates passed`.
- `rtk 0.34.3` is available at `/home/hy/.local/bin/rtk`, but `rtk gain`
  cannot initialize its tracking database (`Error code 14`). Required commands
  therefore run directly; RTK tracking is recorded as unavailable rather than
  passed, and no private runtime database is inspected.
- `pre-commit` and `markdownlint-cli2` are locally available for task-scoped
  optional checks. Their results belong in the verification evidence for the
  task on which they run.
- `conftest` is not installed. Harness validation reports this optional lane as
  `SKIP` and runs the built-in policy fallback, which passed; this fallback is
  repo-static evidence and is not equivalent to a `conftest` pass.
- Live runtime, remote GitHub, provider-runtime, credential, secret-value,
  publish, push, merge, and third-party checks are prohibited for this plan and
  remain not run. Repo-static PASS does not promote those lanes to ready.

## Source and Claim Ledger

| Claim lane | Evidence required | Approved source priority | Recording rule | Failure handling |
| --- | --- | --- | --- | --- |
| Repo fact | Current tracked file, config, script, workflow, manifest, adapter, template, Git history, or deterministic static output. | Canonical repository owner first; related historical material is context only. | Record the exact path, command, or commit and the observation date. | Classify contradicted content as `Fact defect`; do not preserve it for completeness. |
| External fact | Current official provider documentation, standards body, or upstream project source. | Official provider/project page, then a primary standards source; market scans are non-authoritative. | Record the exact URL, surface, and `Source checked` date or cutoff. | Use another first-party source or classify the claim `Unverified` and omit unsupported capability text. |
| Interpretation | Explicit comparison between repo evidence and external benchmark. | The paired repo-fact and external-fact entries. | State the inference and keep it separate from sourced facts. | Downgrade to `Unverified` when either side is missing or ambiguous. |
| Recommendation | Evidence-backed gap with severity, rationale, and canonical follow-up owner. | Confirmed repo fact plus applicable external fact or explicit local contract. | Keep recommendations non-mutating and outside active implementation claims. | Do not apply active-file, runtime, model-policy, adapter, CI, or manifest changes in this workstream. |
| Unverified | Evidence is inaccessible, ambiguous, stale, or surface-conflicted. | None until sufficient primary evidence is available. | Mark `Unverified` or remove the claim; never substitute recollection. | Record the limitation and refresh trigger. |

Task-level source URLs, repo paths, checked dates, claim classifications, review
outcomes, and commit SHAs are added to the corresponding row or linked evidence
as each task completes.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Review outcome | Commit | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WERH-001 | Create execution evidence and baseline audit ledger. | doc | Addendum: Internal and External Research Contract | Phase 1 | Task IDs, evidence lanes, inventories, boundaries, and limitations are explicit. | supervisor | Pending | Pending | Todo |
| WERH-002 | Harden workspace governance baseline. | doc | Addendum: Artifact and Ownership Design | Phase 2 | RED heading assertion exited 1 before editing; current repo counts (10 agent stems on each of three adapter surfaces, 5 workflows, 6 CI jobs), official OpenGitOps sources, owner/enforcement matrices, 6 evidence-backed follow-up rows, focused heading/date scan, Markdown lint, diff check, harness, and repo-quality results are recorded below. | doc-writer | Implementer self-review passed; independent task review pending. | Pending WERH-010 closure from `git log` | Done |
| WERH-003 | Harden spec-driven SDLC, CI, QA, and document taxonomy. | doc | Addendum: Coverage and Gap Classification | Phase 2 | Every SDLC document family and QA lane has a role, evidence, benchmark, and gap verdict. | doc-writer | Pending | Pending | Todo |
| WERH-004 | Harden harness and loop engineering. | doc | Addendum: Internal and External Research Contract | Phase 2 | Harness/loop elements, termination, evaluation, recovery, and provider-neutral boundaries are source-backed. | doc-writer | Pending | Pending | Todo |
| WERH-005 | Harden provider implementation and current-model analysis. | doc | Addendum: Provider and Model Freshness Design | Phase 2 | Provider/API/product/CLI/local surfaces and model lifecycle states are separated. | doc-writer | Pending | Pending | Todo |
| WERH-006 | Harden automation, pipeline, workflow, and QA topology. | doc | Addendum: Artifact and Ownership Design | Phase 2 | CI DAG, filters, GitOps boundary, feedback lanes, and delivery gaps match repo evidence. | doc-writer | Pending | Pending | Todo |
| WERH-007 | Harden Kubernetes, infrastructure, and security analysis. | doc | Addendum: Artifact and Ownership Design | Phase 2 | Platform controls, external benchmarks, static/live limits, and prioritized gaps are explicit. | doc-writer | Pending | Pending | Todo |
| WERH-008 | Harden AI-agent roster, upstream comparison, and model routing. | doc | Addendum: Provider and Model Freshness Design | Phase 2 | Local roster, current upstream evidence, native adapter gaps, and task-model recommendations are source-backed. | doc-writer | Pending | Pending | Todo |
| WERH-009 | Close pack coverage and cross-document integration. | doc | Addendum: Coverage and Related-Document Integration Rules | Phase 3 | Every requested topic has one primary owner; links, freshness, and repeated content are consistent. | supervisor | Pending | Pending | Todo |
| WERH-010 | Run final validation and close execution records. | eval | Addendum: Verification and Acceptance | Phase 4 | Required static gates and final review pass; limitations and logical commits are recorded. | supervisor | Pending | Pending | Todo |

## Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`

## Phase View

### Phase 1: Evidence Scaffold

- [ ] WERH-001 Create execution evidence and baseline audit ledger.

### Phase 2: Topic Hardening

- [x] WERH-002 Harden workspace governance baseline.
- [ ] WERH-003 Harden spec-driven SDLC, CI, QA, and document taxonomy.
- [ ] WERH-004 Harden harness and loop engineering.
- [ ] WERH-005 Harden provider implementation and current-model analysis.
- [ ] WERH-006 Harden automation, pipeline, workflow, and QA topology.
- [ ] WERH-007 Harden Kubernetes, infrastructure, and security analysis.
- [ ] WERH-008 Harden AI-agent roster, upstream comparison, and model routing.

### Phase 3: Pack Integration

- [ ] WERH-009 Close pack coverage and cross-document integration.

### Phase 4: Validation Closure

- [ ] WERH-010 Run final validation and close execution records.

## Verification Summary

### WERH-002 Governance Baseline Evidence

- **RED assertion**:
  `rg -n 'Owner and Authority Matrix|Enforcement and Evidence Map|Governance Gap Register|External Benchmark' docs/90.references/research/2026-07-07-wer/workspace-governance-baseline.md`
  exited 1 with no matches before the edit.
- **Repo-fact inventory**: `find` counts confirmed ten agent files under each
  of `.claude/agents`, `.agents/agents`, and `.codex/agents`; five workflow
  files under `.github/workflows`; and a job-ID scan of `ci.yml` found six jobs.
  A lifecycle scan found 20 active `spec.md` files, 16 with `status: draft`
  and none with `status: done`; the completed 021 lifecycle plan/task remain a
  concrete draft/done asymmetry example.
- **Gap rechecks**: Stage 99 contains no release template; lifecycle and route
  summaries repeat across `sdlc-governance.md`, `stage-authoring-matrix.md`,
  and `document-stage-routing.md`; semantic lineage remains link/review based;
  the audit index has multiple `Current` dated snapshots; and
  `graphify-out/GRAPH_REPORT.md` was built from `e8a99671`, 199 commits behind
  the pre-edit `HEAD` according to `git rev-list --count e8a99671..HEAD`.
- **External sources**: official OpenGitOps benchmark context was checked
  read-only on 2026-07-10 at <https://opengitops.dev/> and
  <https://github.com/open-gitops/documents/blob/main/PRINCIPLES.md>.
- **Focused and optional validation**:
  `rg -n 'External Benchmark|Owner and Authority Matrix|Enforcement and Evidence Map|Governance Gap Register|2026-07-10' docs/90.references/research/2026-07-07-wer/workspace-governance-baseline.md`
  found every required heading/date; `markdownlint-cli2` reported 0 errors;
  and `pre-commit run --files` passed every applicable hook for both changed
  files.
- **Required validation**: `git diff --check` exited 0;
  `bash scripts/validate-repo-quality-gates.sh .` returned
  `[PASS] repository quality gates passed`; and
  `bash scripts/validate-harness.sh` returned
  `PASS harness repo-static validation`.
- **Limitations**: the harness ran repo-static checks only. `conftest` was not
  installed, so the built-in policy fallback passed and is not reported as a
  Conftest pass. No live Kubernetes/Argo CD/Vault/ESO, provider runtime,
  secret-value, credential, remote GitHub/CI/ruleset, publish, push, merge, or
  third-party mutation check ran. OpenGitOps is benchmark context only, never
  local implementation proof.
- **Commit evidence**: the WERH-002 commit field intentionally remains pending
  until WERH-010 records the resulting SHA from `git log` after this commit
  exists.

- **RED command**:
  `rg -n '2026-07-10-current-research-pack-fact-first-hardening' docs/04.execution/tasks/README.md`
  exited 1 with no output before the task record and index row existed.
- **Baseline command**: `bash scripts/validate-repo-quality-gates.sh .`
  exited 0 with `[PASS] repository quality gates passed`.
- **Focused scaffold command**:
  `rg -n 'WERH-00[1-9]|WERH-010|Baseline Evidence|Source and Claim Ledger|repo-static|live runtime' docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md`
  found all ten task IDs, both evidence headings, and both evidence-boundary
  terms.
- **Required repository checks**: `git diff --check` exited 0 with no output;
  `bash scripts/validate-repo-quality-gates.sh .` exited 0 with
  `[PASS] repository quality gates passed` after canonical template-heading
  alignment.
- **Task-scoped optional checks**: `markdownlint-cli2` reported 0 errors, and
  `pre-commit run --files ...` passed every applicable hook.
- **Harness check**: `bash scripts/validate-harness.sh` exited 0 with
  `PASS harness repo-static validation`; optional `conftest` was skipped and
  the built-in policy fallback passed.
- **Final workstream checks**: focused coverage/freshness/boundary/completeness
  scans from the parent plan and task-scoped source/repo-fact review remain
  assigned to WERH-010.
- **Evidence location**: this task record, per-task logical commits, and the
  final progress-memory entry created during WERH-010.

## Related Documents

- **Spec**:
  [Workspace Engineering Research Pack](../../03.specs/017-workspace-engineering-research-pack/spec.md)
- **Plan**:
  [Current Research Pack Fact-First Hardening Implementation Plan](../plans/2026-07-10-current-research-pack-fact-first-hardening.md)
- **Current Research Pack**:
  [2026-07-07 WER](../../90.references/research/2026-07-07-wer/README.md)
- **Historical Research Pack**:
  [2026-07-04 WER](../../90.references/research/2026-07-04-wer/README.md)
- **Task Template**:
  [Stage 04 Task Template](../../99.templates/templates/sdlc/execution/task.template.md)
- **Task Index**: [Stage 04 Tasks](./README.md)
