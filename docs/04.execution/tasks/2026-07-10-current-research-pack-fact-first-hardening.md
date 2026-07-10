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
| WERH-002 | Harden workspace governance baseline. | doc | Addendum: Artifact and Ownership Design | Phase 2 | RED heading assertion exited 1 before editing; current repo counts (10 agent stems on each of three adapter surfaces, 5 workflows, 6 CI jobs), official OpenGitOps sources, owner/enforcement matrices, 7 evidence-backed follow-up rows, focused heading/date scan, Markdown lint, diff check, harness, and repo-quality results are recorded below. | doc-writer | Review findings corrected; independent re-review pending. | Pending WERH-010 closure from `git log` | Done |
| WERH-003 | Harden spec-driven SDLC, CI, QA, and document taxonomy. | doc | Addendum: Coverage and Gap Classification | Phase 2 | RED heading assertion exited 1; 19 SDLC templates, no Release route/template, zero Incident/Postmortem records, Spec/Task state asymmetry, all 14 document families, all 9 QA lanes, 11 primary sources, and 6 routed gap rows are recorded below. | doc-writer | Important review findings corrected; independent re-review pending. | Pending WERH-010 closure from `git log` | Done |
| WERH-004 | Harden harness and loop engineering. | doc | Addendum: Internal and External Research Contract | Phase 2 | RED heading assertion, exact six-column loop matrix, ownership/evidence boundaries, evaluation/recovery/termination design, 2025-11-25 MCP currentness, 8-category official MCP taxonomy, 7 routed findings, and focused/repository checks are recorded below. | doc-writer | Pending independent review | Pending WERH-010 closure from `git log` | Done |
| WERH-005 | Harden provider implementation and current-model analysis. | doc | Addendum: Provider and Model Freshness Design | Phase 2 | RED heading assertion exited 1; exact 10-role/30-path adapter matrix, three hook/settings JSON surfaces, 17 surface-specific model rows, 13 one-to-one model evaluation/migration rows, six task-routing rows, 21 official URLs, eight routed findings, focused assertions, Markdown lint, diff check, harness, and repo-quality results are recorded below. | doc-writer | Important review findings corrected; independent re-review pending. | Pending WERH-010 closure from `git log` | Done |
| WERH-006 | Harden automation, pipeline, workflow, and QA topology. | doc | Addendum: Artifact and Ownership Design | Phase 2 | RED heading assertion exited 1; 5 workflows, 6 CI jobs, 2 parallel roots, 3 `changes`-dependent conditional jobs, 8 official sources, 9 coverage rows, 7 routed gap rows, and the exact GitOps ownership boundary are recorded below. | doc-writer | Pending independent review | Pending WERH-010 closure from `git log` | Done |
| WERH-007 | Harden Kubernetes, infrastructure, and security analysis. | doc | Addendum: Artifact and Ownership Design | Phase 2 | RED heading assertion exited 1; 15 primary sources, 12 control rows, 6 evidence lanes, 14 routed security gaps, AppProject/GitOps/NetworkPolicy/ESO-Vault controls, and supply-chain boundaries are recorded below. | doc-writer | Pending independent review | Pending WERH-010 closure from `git log` | Done |
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
- [x] WERH-003 Harden spec-driven SDLC, CI, QA, and document taxonomy.
- [x] WERH-004 Harden harness and loop engineering.
- [x] WERH-005 Harden provider implementation and current-model analysis.
- [x] WERH-006 Harden automation, pipeline, workflow, and QA topology.
- [x] WERH-007 Harden Kubernetes, infrastructure, and security analysis.
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
  actual adapter parity is ten stems per provider while canonical
  `harness-catalog.md` readiness prose still says eight;
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
- **Review follow-up**: review found that the owner matrix reported a clean
  adapter inventory verdict while canonical `harness-catalog.md` prose still
  said eight. The reference now records the dual fact (ten actual stems per
  provider, stale canonical count), adds a seventh routed gap, and links all
  provider notes plus the maintenance runbook explicitly. Focused `rg`
  confirmed the three stale catalog phrases and ten files per provider;
  `git diff --check`, `markdownlint-cli2`, changed-file `pre-commit`, and
  `bash scripts/validate-repo-quality-gates.sh .` passed. Independent re-review
  remains pending.

### WERH-003 SDLC and QA Evidence

- **RED assertion**:
  `rg -n 'Lifecycle and Traceability Matrix|External SDLC Benchmark|QA Evidence Lane Matrix|Document Maturity Gap Register' docs/90.references/research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md`
  exited 1 with no matches before editing, proving the approved structure was
  absent.
- **Repo-fact inventory**: all Stage 01-05 READMEs, Stage 00 authoring/routing
  rules, Stage 99 SDLC support contracts, and all 19 files under
  `docs/99.templates/templates/sdlc/` were inspected. No Release structural
  template or route exists. `docs/05.operations/incidents/` contains only its
  README and zero tracked `sdlc/incident` or `sdlc/postmortem` artifacts.
- **Lifecycle and maturity recheck**: the canonical state contract ends
  PRD/Spec/Plan/Task with `done`, ARD/ADR/Operations with `accepted`, and
  Archive Tombstone with `archived`. Frontmatter scans found 20 Stage 03 parent
  Specs: 16 `draft`, 4 `active`, and 0 `done`; Stage 04 contains 43 Task
  records: 42 `done` and this current record `draft`.
- **QA ownership recheck**: `.editorconfig`, `.pre-commit-config.yaml`, both
  GitHub Actions workflows, the CI/CD QA guide, script inventory, repo-quality,
  GitOps, manifest, secret, policy, harness, and infrastructure static-contract
  validators were inspected. The reference now separates formatting, linting,
  syntax/parse, repo-structural, manifest, secret, policy, artifact/release,
  and live-runtime evidence into nine rows and records what each lane cannot
  prove. Follow-up review also confirmed root `.prettierrc.json` and
  `.prettierignore`, no Prettier pre-commit/CI execution wiring, and that
  `bash -n` is a CI/QA-guide manual single-file check rather than a
  repo-quality or harness command.
- **External sources**: the eleven required primary sources were checked
  read-only on 2026-07-10: GitHub Spec Kit; NIST SP 800-218 and SP 800-61 Rev.
  3; Google SRE postmortem culture; Nygard/Cognitect ADR; GitHub Actions secure
  use; pre-commit; EditorConfig; Prettier; CommonMark 0.31.2; and YAML 1.2.2.
  The reference explicitly treats PRD/ARD as workspace/industry conventions,
  ADR as a primary practice rather than a standard, and the remaining sources
  according to standards-body, official-tool, or primary-practice authority.
- **Focused validation**: the required term/date scan found every document
  family and all four approved headings. Exact row assertions returned 14
  lifecycle document rows and 9 QA evidence rows. An exact-URL scan found no
  missing required source. `markdownlint-cli2` reported 0 errors and
  `git diff --check` exited 0.
- **Link and repository validation**:
  `bash scripts/validate-repo-quality-gates.sh .` returned
  `[PASS] repository quality gates passed`, including its Markdown relative-link
  resolution and authored-document route checks.
- **Changed-file hooks**:
  `pre-commit run --files docs/90.references/research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md`
  passed every applicable file-hygiene, secret, and Markdown hook; non-applicable
  code/workflow/manifest hooks were skipped.
- **Harness validation**: `bash scripts/validate-harness.sh` returned
  `PASS harness repo-static validation`; repo quality, GitOps structure, 104
  YAML parses, kube-linter, secret scanning, built-in policy fallback, static
  infrastructure contracts, and diff hygiene passed. `conftest` was not
  installed, so its lane was skipped and is not reported as a Conftest pass.
- **Gap routing**: six non-mutating findings record severity, risk rationale,
  recommendation, and canonical follow-up for draft-Spec/done-Task asymmetry,
  release readiness/provenance, incident exercise evidence, traceability
  automation, immutable Action pinning, and configured-but-unwired Prettier.
- **Limitations**: no live Kubernetes/Argo CD/Vault/ESO, provider runtime,
  credential, secret-value, remote GitHub/CI/ruleset, release, publish, push,
  merge, or third-party mutation check ran. Repo-static PASS and external
  benchmark findings do not establish live or remote readiness.
- **Commit evidence**: the WERH-003 commit field intentionally remains pending
  until WERH-010 records the resulting SHA from `git log` after this commit
  exists. Important review findings for classification vocabulary, Prettier
  inventory/wiring, and manual shell syntax ownership were corrected;
  independent re-review remains pending.

### WERH-004 Harness and Loop Evidence

- **RED assertion**:
  `rg -n 'Evaluation and Recovery Loop|Harness Ownership Boundary|Provider-Neutral Control Loop Matrix|Harness and Loop Gap Register' docs/90.references/research/2026-07-07-wer/harness-and-loop-engineering.md`
  exited 1 with no matches before editing, proving the approved structure was
  absent.
- **Repo-fact reconciliation**: the Current and Historical harness references,
  Stage 00 catalog/implementation map/subagent protocol/model policy/approval
  and agentic rules, all three provider notes and runtime baselines, shared
  hook scripts, three hook/settings JSON files, lifecycle payload validator,
  progress memory, related dated audits, Stage 99 route/template contracts,
  and reference-maintenance runbook were inspected. The reference now states
  that `.agents/` owns shared skills, workflows, output styles, the Gemini
  baseline, and local adapters only; Stage 00 retains governance/memory,
  Stage 04 retains task evidence, and Stage 99 retains templates.
- **Evidence boundary**: the reference separates declared JSON wiring,
  validator parse/payload-simulation evidence, native/runtime behavior, and
  live/remote readiness. Claude settings contain tracked native permissions;
  Codex/Gemini hook JSON remains declared context/validation wiring, and no
  provider-native consumption claim is made. No tracked `.mcp.json`,
  `.codex/config.toml`, or `.gemini/settings.json` was found.
- **External sources**: the nine required official pages were checked read-only
  on 2026-07-10:
  <https://openai.com/index/harness-engineering/>,
  <https://openai.com/index/unrolling-the-codex-agent-loop/>,
  <https://developers.openai.com/codex/subagents/>,
  <https://code.claude.com/docs/en/sub-agents>,
  <https://code.claude.com/docs/en/hooks>,
  <https://geminicli.com/docs/core/subagents/>,
  <https://geminicli.com/docs/reference/policy-engine/>,
  <https://modelcontextprotocol.io/specification/2025-06-18>, and
  <https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices>.
  MCP versioning and the latest specification were also checked at
  <https://modelcontextprotocol.io/docs/learn/versioning> and
  <https://modelcontextprotocol.io/specification/2025-11-25>.
- **MCP currentness and security**: official versioning marks `2025-11-25` as
  Current and ready for use, so `2025-06-18` is retained as a historical Final
  revision rather than the latest stable/current source. Threat/mitigation
  text uses only the official eight-category Security Best Practices taxonomy:
  Confused Deputy, Token Passthrough, SSRF, Session Hijacking, Local MCP Server
  Compromise, OAuth Authorization URL Validation, stdio Transport Security in
  Proxy Scenarios, and Scope Minimization.
- **Control-loop coverage**: the exact six-column matrix contains eight rows:
  Observe, Plan, Act, Verify, Learn/Handoff, retry budget/failure escalation,
  compaction, and human approval. The evaluation/recovery section adds
  capability and regression evals, traceability, calibrated judgment, evidence
  lanes, a recovery state machine, and six explicit termination modes.
- **Gap routing**: seven rows use only `Fact defect`, `Implementation gap`,
  `Needs strengthening`, or `Unverified` from the approved vocabulary. Each
  records severity, risk rationale, a non-mutating recommendation, and one
  canonical follow-up route. Provider-native implementation detail routes to
  WERH-005 rather than being duplicated here.
- **Focused and optional validation**: the required heading/phase/date scan
  found all four headings, all five named phases, and the checked date. An
  exact-header assertion found one matrix header with `Phase`, `Inputs`,
  `Allowed action`, `Feedback evidence`, `Termination condition`, and
  `Knowledge update`; the exact phase-row assertion found all five phase rows.
  `markdownlint-cli2` reported 0 errors and `git diff --check` exited 0.
- **Changed-file hooks**:
  `pre-commit run --files docs/90.references/research/2026-07-07-wer/harness-and-loop-engineering.md docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md`
  passed every applicable file-hygiene, secret, and Markdown hook;
  non-applicable code, workflow, manifest, and container hooks were skipped.
- **Required validation**: `bash scripts/validate-harness.sh` returned
  `PASS harness repo-static validation`, including repository quality, GitOps
  structure, 104 YAML parses, kube-linter, secret handling, built-in policy
  fallback, static infrastructure contracts, and diff hygiene.
  `bash scripts/validate-repo-quality-gates.sh .` separately returned
  `[PASS] repository quality gates passed`, including Markdown link and route
  checks.
- **Tool limitations**: RTK 0.34.3 ran the commands but warned that project
  filters are untrusted, so filters were not applied. `rtk find` did not
  support the compound config-file predicate; the underlying read-only `find`
  command was used. `conftest` was not installed; the harness reported SKIP
  and the built-in policy fallback passed, which is not a Conftest pass.
- **Readiness limitations**: no provider-native canary, live
  Kubernetes/Argo CD/Vault/ESO, MCP connection, credential, secret-value,
  remote GitHub/CI/ruleset, publish, push, merge, or third-party mutation check
  ran. Repo-static PASS and official benchmarks do not establish live or
  remote readiness.
- **Review and commit evidence**: independent task-scoped review remains
  pending. The WERH-004 commit field intentionally remains pending until
  WERH-010 records the resulting SHA from `git log` after this commit exists.

### WERH-005 Provider and Model Evidence

- **RED assertion**:
  `rg -n 'Native Surface and Local Adapter Matrix|Current Model Surface Matrix|Task-Characteristic Model Recommendation|Provider Gap Register|2026-07-10 10:00 KST' docs/90.references/research/2026-07-07-wer/provider-implementation-status.md`
  exited 1 with no matches before editing, proving the approved structure and
  cutoff were absent.
- **Repo-fact inventory**: all root provider gateways, three local runtime
  baselines, provider notes, model policy, harness catalog/implementation map,
  `.claude/settings.json`, `.codex/hooks.json`, `.agents/hooks.json`, four
  shared hook scripts, all 30 provider adapter files, and the adapter/hook
  portions of `scripts/validate-repo-quality-gates.sh` were inspected. Exact
  counts are ten Claude Markdown, ten `.agents` Markdown, and ten Codex TOML
  adapters with identical stems.
- **Adapter-field reconciliation**: the provider reference now has ten exact
  role rows naming all 30 adapter paths, every imported scope, every model
  declaration, every Claude `tools:` allowlist, every Codex reasoning effort,
  and the `.agents` frontmatter fields absent from every local adapter. All
  observability adapters import `scopes/infra.md`; Claude settings binds the
  four shared scripts rather than `validate-harness.sh`; Claude `tools:` is a
  native field rather than a cross-provider parity requirement; and Codex
  declares `xhigh` for the supervisor, `high` for seven implementation/review/
  security/incident workers, and `medium` for docs/wiki. The validator proves
  stems and selected fields, but its expected maps omit network/observability
  and it does not semantically compare Gemini fields.
- **Native-path reconciliation**: official Gemini CLI project agents and
  settings/hooks live at `.gemini/agents/*.md` and `.gemini/settings.json`.
  The tracked `.agents/agents/*.md` and `.agents/hooks.json` are therefore
  documented as Antigravity/local adapters, not Gemini CLI native registration.
  Official Codex standalone `.codex/agents/*.toml` discovery does not require a
  tracked `.codex/config.toml`; its absence leaves documented agent defaults at
  six threads and depth one unless another config layer overrides them.
- **Model surface result**: the exact cutoff matrix has 17 surface rows. Codex
  product and OpenAI API catalog rows are separate for GPT-5.6 Sol, Terra, and
  Luna; ChatGPT-sign-in deprecation and the published API model page are
  separate rows for `gpt-5.3-codex`. Neither surface infers the other's
  lifecycle or availability. An adjacent 13-row evaluation/migration matrix
  provides one-to-one coverage for Claude Fable 5, Opus 4.8, Sonnet 5, Haiku
  4.5; GPT-5.6 Sol/Terra/Luna, GPT-5.5, GPT-5.4 Mini, GPT-5.3-Codex; and Gemini
  3.1 Pro Preview, 3.5 Flash, and 3.1 Flash-Lite. Each row names disposition,
  supported effort/routing facts or a surface-specific unknown, required eval,
  and an exact canonical non-mutating follow-up route.
- **External sources**: 21 official URLs were checked read-only at exactly
  `2026-07-10 10:00 KST`: six Anthropic/Claude model, configuration, and
  subagent pages; six OpenAI API/Codex model, subagent, config, and hook pages;
  and nine Gemini API/CLI model, release, subagent, hook, and settings pages.
  OpenAI developer URLs redirect to ChatGPT Learn, so the stable developer URLs
  and redirect caveat are retained. Gemini API stability is not used to infer
  CLI account/version availability.
- **Gap routing**: eight rows use approved `Fact defect`, `Implementation gap`,
  `Needs strengthening`, or `Unverified` classifications. They route stale
  Current facts, Claude syntax/currentness, Codex auth/lifecycle drift, Gemini
  native adapter/settings mismatch, Gemini lifecycle labels, semantic parity
  coverage, implicit Codex agent limits, and missing native canary evidence to
  canonical follow-up owners without modifying active files.
- **Task-characteristic routing**: six rows express default, escalation, and
  fallback for architecture, routine implementation/review, security/incident,
  documentation/research, high-volume deterministic work, and an eventual
  model migration. Every route names eval criteria; `max` is recorded only as
  additional single-model reasoning effort, never as subagent orchestration.
  None reconfigures active model policy or provider adapters.
- **Focused and optional validation**: the required heading/model/cutoff scan
  found all four headings and every required model including GPT-5.4 Mini. An
  exact-header scan found the four headings once; an exact required-URL loop
  reported no missing source. `markdownlint-cli2` reported 0 errors and
  `git diff --check` exited 0.
- **Required validation**: `bash scripts/validate-harness.sh` returned
  `PASS harness repo-static validation`, including repository quality, GitOps
  structure, 104 YAML parses, kube-linter, secret handling, built-in policy
  fallback, static infrastructure contracts, and diff hygiene.
  `bash scripts/validate-repo-quality-gates.sh .` returned
  `[PASS] repository quality gates passed`.
- **Limitations**: `conftest` was not installed, so the harness reported SKIP
  and the built-in policy fallback passed; this is not a Conftest pass. No
  provider CLI version, login/account entitlement, auth credential, agent
  registry, model picker, resolved model, hook trust/consumption, inference,
  MCP connection, live Kubernetes/Argo CD/Vault/ESO, secret-value, remote
  GitHub/CI, publish, push, merge, or third-party mutation check ran.
- **Review and commit evidence**: task review found Important issues in exact
  adapter-field proof, one-to-one model evaluation coverage, OpenAI
  product/API separation, and effort/orchestration wording. These findings were
  corrected; independent re-review remains pending. The WERH-005 commit field
  intentionally remains pending until WERH-010 records the actual SHA from
  `git log` after the follow-up commit exists.

### WERH-006 Automation, Pipeline, Workflow, and QA Evidence

- **RED assertion**:
  `rg -n 'Actual CI Job DAG|Path Filter and Gate Coverage Matrix|GitOps Delivery Boundary|Automation Gap Register' docs/90.references/research/2026-07-07-wer/automation-pipeline-workflow-qa.md`
  exited 1 with no matches before editing, proving that the approved topology
  structures were absent.
- **Workflow and DAG re-derivation**: all five workflow YAML files and their
  owning `.github` configs were inspected. `ci.yml` has six jobs.
  `branch-policy` and `changes` have no `needs` and are parallel roots;
  `branch-policy` is PR-only. `pre-commit`, `repo-quality-static`, and
  `manifest-static` each need only `changes` and use one corresponding filter
  output. `ci-summary` directly needs all five jobs, runs with `always()`, and
  fails for a needed `failure` or `cancelled` result while accepting a
  conditional `skipped` result. This corrects the prior serial-DAG fact defect.
- **Filter and validator evidence**: `precommit: '**'` selects the pre-commit
  job for an observed changed path. The `repo_quality` list includes docs,
  `.github`, all three adapter roots, scripts, tests, examples, and
  `gitops/apps/root/**`; the broader `manifests` list includes `gitops/**`,
  infrastructure YAML/tests, examples, policy, Traefik, Kube-linter config,
  and the four manifest/policy validator scripts. The exact six-column matrix
  contains nine surface rows and distinguishes direct CI commands, provider
  hooks, pre-commit, and optional-tool behavior.
- **Shell and hook boundary**: dedicated `bash -n` evidence is limited to the
  shared PostToolUse/lifecycle hook scripts after a matching edit and explicit
  manual commands in the CI/CD QA guide. CI uses pre-commit ShellCheck/shfmt;
  `validate-repo-quality-gates.sh` is not reported as a general shell-syntax
  gate. Post-edit/lifecycle manifest routing runs manifest syntax and secret
  handling but not the full CI static-contract/GitOps-structure/policy bundle.
- **GitOps delivery boundary**: `root-platform` points to
  `gitops/apps/root`, whose kustomization lists 18 platform Application
  manifests. `apps-generator` discovers `gitops/workloads/*` under the `apps`
  project. Both tracked controllers declare automated prune/self-heal intent.
  The CI workflow contains no deploy/live mutation job, so it is documented as
  static QA rather than deployment CD; live pull, generated Applications,
  health, sync, and convergence remain Unverified.
- **External sources**: the eight required official/primary sources were
  opened read-only on 2026-07-10: GitHub workflow syntax, visualization graph,
  secure use, `GITHUB_TOKEN`, and concurrency; pre-commit; DORA metrics; and
  OpenGitOps. External behavior and benchmarks are kept separate from local
  implementation evidence.
- **Gap rechecks**: seven non-mutating rows use the approved classification
  vocabulary and record severity, current evidence, risk rationale,
  recommendation, and canonical follow-up route. They cover path-filter
  dependencies, local policy/hook coverage, warn-only Headlamp/Kiali live TLS
  assertions, immutable Action SHA pinning, absent supply-chain evidence,
  regex-heavy static contracts, and absent DORA telemetry.
- **Focused and optional validation**: the four exact headings were each found
  once; the exact coverage header was found; all eight required URLs were
  present; the DAG/job/date scan found every required term; and
  `markdownlint-cli2` reported 0 errors.
- **Required validation**: `git diff --check` exited 0; changed-file
  `pre-commit run --files` passed every applicable file-hygiene, secret, and
  Markdown hook; and non-applicable workflow/shell/manifest hooks were skipped.
  `bash scripts/validate-repo-quality-gates.sh .` returned
  `[PASS] repository quality gates passed`. `bash scripts/validate-harness.sh`
  returned `PASS harness repo-static validation`, including GitOps ownership,
  104 YAML parses, Kube-linter, secret handling, built-in policy fallback,
  static infrastructure contracts, and diff hygiene.
- **Limitations**: no live Kubernetes/Argo CD/Vault/ESO, provider runtime,
  credential, secret-value, remote GitHub Actions/ruleset/required-check,
  workflow dispatch, release, publish, push, merge, or third-party mutation
  check ran. `conftest` was not installed, so the harness reported SKIP and the
  built-in policy fallback passed; this is not a Conftest pass. Kube-linter was
  available and reported no lint errors for the harness manifest targets.
- **Review and commit evidence**: independent task-scoped review remains
  pending. The WERH-006 commit field intentionally remains pending until
  WERH-010 records the resulting SHA from `git log` after this commit exists.

### WERH-007 Kubernetes, Infrastructure, and Security Evidence

- **RED assertion**:
  `rg -n 'Platform Security Control Matrix|Static and Live Evidence Boundary|Supply-Chain Security Analysis|Security Gap Register' docs/90.references/research/2026-07-07-wer/kubernetes-infrastructure-security.md`
  exited 1 with no matches before editing, proving the approved security-depth
  structure was absent.
- **GitOps and authorization recheck**: the root Application points to
  `gitops/apps/root`; its Kustomize file lists 18 platform Applications. The
  separate `apps-generator` ApplicationSet discovers `gitops/workloads/*` in
  the `apps` project. The `apps` AppProject denies cluster kinds and allows
  exactly eight namespaced kinds; the `platform` project enumerates sources,
  destinations, and resource kinds without wildcards. Its `argocd`
  destination is documented as the admin-equivalent high-trust boundary from
  upstream guidance, while remote source write access and live RBAC remain
  Unverified.
- **Secrets, RBAC, and network recheck**: the ESO store names the Kubernetes
  auth role, ServiceAccount, and namespace; the ServiceAccount has the
  `system:auth-delegator` TokenReview binding; and the Vault HCL grants only
  read/list on the data/metadata paths for three logical platform secrets.
  Six egress NetworkPolicies cover six namespace/use-case surfaces with exact
  service destinations where applicable. CNI packet enforcement, ingress
  isolation, Vault role attachment, ESO sync, Secret RBAC, etcd encryption,
  and version-sensitive Vault audience compatibility were not inferred.
- **Validator and runtime-boundary recheck**: the CI `manifest-static` lane
  declares five explicit scripts and installs PyYAML only. The policy script
  runs Conftest when available and always runs its four-category Python
  fallback; the manifest script skips kube-linter when unavailable.
  `verify-contracts-static.sh` is regex-heavy; Kustomize structure validation
  parses YAML and checks sibling references but does not fully render and
  schema-validate every root. `verify-gitops.sh` accepts nonempty health and
  does not assert sync. `verify-ingress-tls.sh` uses `curl -k`, makes Traefik
  443 opt-in, and leaves Headlamp/Kiali mismatches warn-only.
- **Transport and bootstrap recheck**: bootstrap defaults external Vault HTTPS
  to skip certificate verification and expands a Vault token header and
  `kubectl --from-literal` password into process arguments. The in-cluster ESO
  store uses HTTP. These are recorded as recommendations only; no script,
  manifest, credential, secret, or runtime changed.
- **Supply-chain recheck**: the repository has scoped workflow permissions,
  `persist-credentials: false` where checkout is used, weekly GitHub Actions
  Dependabot updates, secret scanning, actionlint, Zizmor, and non-`latest`
  policy. All checked Action references use version tags and Zizmor disables
  `unpinned-uses`. No active tracked workflow provides CodeQL, dependency
  review, SBOM, provenance/attestation, signature verification, or Scorecard.
  No SLSA level is claimed.
- **External sources**: the exact 15 required primary URLs were opened
  read-only on 2026-07-10: four Kubernetes pages; OpenGitOps; two Argo CD
  pages; ESO Vault provider; Vault policies and Kubernetes auth; OPA for
  Kubernetes; Conftest; NIST SP 800-204D; SLSA v1.2; and OpenSSF Scorecard.
  Argo CD `stable` and ESO `latest` are recorded as rolling URLs; the ESO page
  displayed currentness/version ambiguity, so the exact checked URL, date,
  and Vault-version-dependent audience wording are preserved without a fixed
  release claim.
- **Control and gap coverage**: the exact six-column control matrix has 12
  rows; the static/live boundary has six distinct lanes; and the exact
  five-column gap register has 14 findings. Each finding uses an approved
  classification, includes severity and risk rationale, recommends no active
  change in this workstream, and names one canonical follow-up route.
- **Focused validation**: the required term/date scan found all four exact
  headings and Kubernetes, Argo CD, RBAC, NetworkPolicy, External Secrets,
  Vault, and SLSA coverage. Each exact heading appears once; all 15 required
  URLs are present; exact row assertions found 12 control rows, six evidence
  lanes, and 14 gap rows. `markdownlint-cli2` reported 0 errors and
  `git diff --check` exited 0.
- **Changed-file hooks**:
  `pre-commit run --files docs/90.references/research/2026-07-07-wer/kubernetes-infrastructure-security.md docs/04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md`
  passed every applicable file-hygiene, secret, and Markdown hook;
  non-applicable workflow, shell, and manifest hooks were skipped.
- **Required repository validation**:
  `bash scripts/validate-repo-quality-gates.sh .` returned
  `[PASS] repository quality gates passed`. `bash scripts/validate-harness.sh`
  returned `PASS harness repo-static validation`, including the 18-app GitOps
  hierarchy, 104 YAML parses, Kube-linter with no lint errors, 100-file secret
  scan, built-in policy fallback, static infrastructure contracts, and diff
  hygiene.
- **Limitations**: no live Kubernetes, Argo CD, Vault, ESO, CNI, endpoint,
  ingress/TLS, secret-value, credential, remote GitHub Actions/ruleset/
  required-check, artifact, release, publish, push, merge, or third-party
  mutation check ran. `conftest` was not installed, so the harness reported
  SKIP and the built-in policy fallback passed; this is not a Conftest pass.
  Repo-static and external benchmark evidence do not prove enforcement or
  readiness.
- **Review and commit evidence**: independent task-scoped review remains
  pending. The WERH-007 commit field intentionally remains pending until
  WERH-010 records the resulting SHA from `git log` after this commit exists.

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
