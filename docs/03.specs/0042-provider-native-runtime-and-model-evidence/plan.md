---
title: 'Provider-Native Runtime and Model Evidence Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-29
artifact_id: "SPEC-0042-PLAN-0001"
---

# Provider-Native Runtime and Model Evidence Implementation Plan

## Overview

This Plan executed [Spec 042](spec.md)
after Spec 041 closure. It reconciles Claude, Codex, Gemini, and local adapter
claims against the **2026-07-10 10:00 Asia/Seoul** cutoff, records provider
model candidates without promoting unsupported IDs, and defines secret-free
runtime/canary evidence records. Repository-static validation may pass while
provider runtime readiness remains `ABSENT`, `BLOCKED`, or `DEFER`.

Spec 041 closure `1a3232ce73a653371634e99d773d71ab03f87967`,
postflight `6c35268793f09c1ba3f70cdbe3ece9293828ec16`, and terminal
evidence reconciliation `fdc3d457` are observed prerequisites. This Plan, its
Task, Spec 042 and its index, both Stage 04 indexes, the shared progress
handoff, and only the Spec 042 registry tranche form one exact eight-path
activation proposal. No future activation commit or provider-runtime result is
claimed before observation.

## Context

Spec 041 established one closed harness machine contract, the exact current
`10/3/30` inventory, target-only `12/4/48`, four non-transitive evidence
classes, and four memory classes. Spec 042 must now distinguish cutoff-backed
provider facts from observation-time docs and local runtime observations.

A prior user report recorded Codex CLI `0.145.0-alpha.27` present with Claude
and Gemini absent. Read-only executable re-observation on 2026-07-28 found
Claude Code `2.1.220 (Claude Code)` and Codex CLI `0.140.0` present while Gemini remained
absent. Preserve both observations with provenance; neither establishes
authentication, model resolution, subagent discovery, runtime readiness, or
provider support at the cutoff.

### Legacy Task ledger inputs

This Task is the durable evidence ledger for the
[Spec 042 Plan](plan.md).
It records cutoff source reconciliation, local version observations, provider
surface boundaries, model/effort candidate treatment, secret-free canary
records, QA, review, and closure.

Spec 041 terminal closure `1a3232ce73a653371634e99d773d71ab03f87967` and
postflight evidence update `6c35268793f09c1ba3f70cdbe3ece9293828ec16`
are observed prerequisites. Terminal evidence reconciliation `fdc3d457`
removes stale future-gate wording before this tranche activates.

- [Provider-Native Runtime and Model Evidence Implementation Plan](plan.md)
- [Spec 042](spec.md)
- [PRD-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)
- [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
- [ADR-0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- [Harness machine contract](../../00.agent-governance/contracts/harness-contract.json)
- `docs/90.references/research/2026-07-07-wer/provider-implementation-status.md`; [current lookup](../../90.references/research/0001-workspace-engineering/provider-implementation-status.md)
- Spec 041 closure `1a3232ce73a653371634e99d773d71ab03f87967`,
  postflight `6c35268793f09c1ba3f70cdbe3ece9293828ec16`, and terminal
  evidence reconciliation `fdc3d457`
## Goals & In-Scope

- Reconcile official Claude, Codex, Gemini, and agency-agents sources against
  the exact cutoff without silently importing later claims.
- Separate source-backed model families from exact configured/observed IDs,
  provider fallback, runtime availability, and Spec 044 fitness admission.
- Define closed, synthetic, secret-free provider baseline and canary records
  with comparable verdicts and redaction rules.
- Validate current local, Claude, and Codex tracked surfaces while keeping
  Gemini native target-only until its admission criteria pass.
- Record `ABSENT`, `BLOCKED`, or `DEFER` without converting a repository-static
  PASS into provider-runtime readiness.

## Non-Goals & Out-of-Scope

- Installing or authenticating Claude or Gemini CLI, modifying user/home
  configuration, or dispatching a provider task without separate approval.
- Promoting a model/effort assignment, the target `12/4/48` roster, or a
  Gemini-native surface without the owning static/runtime/eval evidence.
- Reading or storing auth caches, account identities, credentials, tokens,
  prompt transcripts, provider response bodies, private endpoints, or private
  diagnostics.
- Adding unrelated CI jobs, changing GitHub settings, or mutating Kubernetes,
  GitOps, Vault, ESO, Argo CD, remote, cloud, or live state.

## Work Breakdown

| ID | Work package | Exit evidence |
| --- | --- | --- |
| PNME-000 | Activate reciprocal Plan/Task and Spec 042 lineage after Spec 041 postflight | Spec042 active; Plan/Task active; registry tranche active; predecessor closure cited |
| PNME-001 | Refresh the active provider source ledger while preserving the protected Current research snapshot | Claude/Codex/Gemini/agency-agents sources are recorded with dated applicability in the active evidence contract; the Current pack remains its fixed-cutoff reference basis |
| PNME-002 | Normalize provider model and effort policy | Candidate model/effort table distinguishes cutoff-backed family evidence, local observation, exact runtime resolution, fallback, and Spec044 fitness gate |
| PNME-003 | Define secret-free provider baseline and canary records | Records forbid credentials, auth files, account identity, prompt transcripts, provider response bodies, and secret-bearing diagnostics |
| PNME-004 | Validate tracked provider surfaces and MCP boundaries | Repo-static validators prove `.agents`, `.claude`, `.codex`, and target-only `.gemini` boundaries without runtime promotion |
| PNME-005 | Run QA/review and close the tranche | Focused/static/strict/aggregate/pre-commit/diff gates and independent reviews pass; external lanes remain explicit |

## Verification Plan

- `python3 scripts/validate-agent-harness-contract.py --root .`
- `python3 scripts/validate-agent-provider-config.py --root .`
- `python3 scripts/validate-agent-provider-canaries.py --root .`
- `python3 scripts/validate-markdown-profiles.py --root . --mode strict --body-contracts registry`
- `python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry`
- `bash scripts/validate-repo-quality-gates.sh .`
- `pre-commit run --all-files`
- `git diff --check`

Provider install/auth/run commands are not executed unless separately
authorized. If Claude or Gemini CLI is absent, record `ABSENT`; if auth is not
available, record `BLOCKED`; if a live action is out of scope, record `DEFER`.

### Legacy Task verification evidence

The activation proposal records only a repository-local lifecycle transition.
It does not claim provider discovery, authentication, runtime availability,
model resolution, Gemini-native admission, hosted CI, remote, credential, or
live PASS. The prior user report recorded Codex CLI `0.145.0-alpha.27` present
with Claude and Gemini absent. A read-only executable observation on 2026-07-28
instead found Claude Code `2.1.220 (Claude Code)` and Codex CLI `0.140.0` present while
Gemini remained absent. The two observations are retained separately; neither
is a provider-readiness result.

Initial staged validation exposed missing reciprocal Task body sections and
relationships. The repaired exact eight-path proposal then passed strict
registry, Markdown body-contract, cross-link/owner, staged lifecycle,
repository aggregate, all-files pre-commit, cached/unstaged diff, requirements
scope, and independent quality review. PNME-000 is complete without claiming
an unobserved result.

PNME-001 through PNME-004 have implementation evidence in
`9c4dcc7b7572bfe8f436d81ee87ede872707cc73`. The
provider contract fixes ten source identities, exact cutoff-day UTC handling,
four provider surfaces, eight candidate-only model records, seven MCP
boundaries, and twelve redacted canary records. Focused and repository-wide QA
passed and independent re-review returned requirements `COMPLIANT` plus
quality/security `APPROVED`. Implementation explicit-ref lifecycle and
clean-tree aggregate postflight passed. PNME-005 is complete with the exact
eight-path terminal proposal; the future closure SHA and its post-closure
evidence event are intentionally unclaimed.

Activation commit `1c3cc9bf32adae3033494ae7cb50eaaf1650b096`
has parent `fdc3d457a3806f86c288ea1bb923898a67294709` and changes
exactly the declared eight lifecycle paths. Parent-to-activation explicit-ref
lifecycle and the clean-tree repository aggregate passed after commit
creation. This evidence update does not identify or claim its own future
content-addressed SHA.
## Risks & Mitigations

| Risk | Mitigation | Owner |
| --- | --- | --- |
| Post-cutoff provider docs are mistaken for cutoff facts | Require dated release/tag evidence or label the claim observation-time/unresolved | platform |
| Parsed config is reported as runtime readiness | Preserve repo-static, native-discovery, and authenticated-run verdicts independently | platform |
| Model alias silently resolves to a different model | Record configured and observed IDs separately; silent fallback is FAIL | platform |
| Canary evidence captures sensitive content | Closed schema and synthetic negative fixtures reject secret/raw/private payloads | security-auditor |
| Absent provider blocks later repository-local work | Record owned `ABSENT`/`BLOCKED`/`DEFER` plus retry trigger; do not claim runtime PASS | platform |

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: Spec 042 and its reciprocal Plan/Task/index/progress
  lineage; the single Spec 042 program-registry relation; later Plan-owned
  provider contract/schema, focused validators, synthetic fixtures, provider
  notes, and Current research evidence.
- **Forbidden Paths**: Credentials, tokens, auth files/caches, account
  identities, environment dumps, shell history, private diagnostics, raw
  prompts/transcripts, provider response bodies, user/home configuration,
  provider installation/authentication/run, `.gemini/**` before native
  admission, current `12/4/48`, model promotion, unrelated CI, infrastructure,
  Kubernetes/GitOps, Vault, ESO, Argo CD, cloud, deployment, and release state.
- **Approval Required**: Push, merge, workflow dispatch, GitHub/provider
  settings, dependency installation, publication, networked provider
  execution, credentials, remote/live state, and scope expansion require
  separate explicit human approval.
- **Static Validation**: Focused provider contract/canary validators; document
  lifecycle self-test and staged/explicit-ref checks; strict registry,
  Markdown, links/owners; aggregate; all-files pre-commit; status and both diff
  checks.
- **Live Validation**: `DEFER`. Provider discovery/authenticated runs, hosted
  Actions, remote, Kubernetes, Vault, ESO, Argo CD, cloud, and deployment
  results are not authorized or inferred.
- **Secret / Vault Handling**: Do not open, print, copy, hash, store, or report
  secret values or sensitive local/provider artifacts. Use synthetic
  secret-like markers only in negative fixtures.
- **Rollback Plan**: Revert the newest logical PNME unit, rerun its focused
  checks and the aggregate, and revert activation last. Never reset, clean,
  rewrite shared history, or overwrite unrelated work.
- **Evidence Location**: This Task owns observed results; the Plan owns
  execution order; Spec 042 owns criteria; the harness contract owns current
  provider/evidence boundaries; Spec 044 owns role/model fitness promotion.
## Completion Criteria

- PNME-000 through PNME-005 have observed results in the reciprocal Task.
- Official-source claims are cutoff-classified with unsupported exact IDs
  unresolved rather than inferred.
- Provider baseline and canary schemas reject unknown, secret-bearing, raw, or
  cross-evidence-class payloads.
- Current tracked provider surfaces and any admitted target surface pass their
  repository-static validators without relabeling local/Antigravity evidence.
- Model/effort candidates retain parse, runtime-resolution, fallback, and Spec
  044 fitness gates.
- Focused, strict, lifecycle, aggregate, all-files, diff, and independent
  review gates pass before atomic closure.
- Provider runtime, hosted CI, remote, credential-bearing, and live outcomes
  remain their observed verdicts and are never inferred from static PASS.

Implementation commit `9c4dcc7b7572bfe8f436d81ee87ede872707cc73`
and its explicit-ref/clean-tree postflight satisfy PNME-001 through PNME-004
and the repository-static portion of PNME-005. The exact eight-path terminal
proposal closes this Plan without claiming its future closure SHA or
post-closure evidence event.

## Traceability

- **Spec**: [Provider-Native Runtime and Model Evidence](spec.md)
- **Task**: [Provider-Native Runtime and Model Evidence Task](README.md#task-records)

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-PNME-001](spec.md#success-criteria--verification-plan) | PNME-000, PNME-004 | [Activation and provider-path evidence](tasks/tsk-0001-pnme-000.md) |
| N/A — VAL-PNME-002 shares the Spec source above | PNME-001 | N/A — the reciprocal Task is linked in VAL-PNME-001 |
| N/A — VAL-PNME-003 shares the Spec source above | PNME-003, PNME-004 | N/A — the reciprocal Task is linked in VAL-PNME-001 |
| N/A — VAL-PNME-004 shares the Spec source above | PNME-002 | N/A — the reciprocal Task is linked in VAL-PNME-001 |
| N/A — VAL-PNME-005 through VAL-PNME-008 share the Spec source above | PNME-003 | N/A — the reciprocal Task is linked in VAL-PNME-001 |
| N/A — VAL-PNME-009 shares the Spec source above | PNME-005 | N/A — the reciprocal Task is linked in VAL-PNME-001 |

### Legacy Task traceability

- **Plan**: [Provider-Native Runtime and Model Evidence Implementation Plan](plan.md)
- **Spec**: [Provider-Native Runtime and Model Evidence](spec.md)

#### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [PNME-000](plan.md#work-breakdown) | PASS — exact eight-path activation and postflight satisfy their repository-static gates. | `fdc3d457` → `1c3cc9bf`; explicit-ref lifecycle and clean-tree aggregate passed; no provider-runtime claim. |
| [PNME-001](spec.md#success-criteria--verification-plan) | PASS — fixed cutoff source ledger implemented. | Exact ten-source set, UTC cutoff-day precision, prior/current observation separation, and protected Current snapshot preservation validate. |
| N/A — PNME-002 shares the Plan and Spec sources linked above | PASS — candidate model/effort policy implemented without assignment promotion. | Eight candidate-only records retain exact parse, runtime resolution, fallback, and Spec 044 fitness gates. |
| N/A — PNME-003 shares the Plan and Spec sources linked above | PASS — provider baseline/canary records implemented. | Twelve closed redacted records and eight canary mutations validate evidence-specific verdict behavior. |
| N/A — PNME-004 shares the Plan and Spec sources linked above | PASS — tracked surfaces and MCP boundaries reconciled. | Four surfaces, canonical repo-relative project paths, seven MCP servers, target-only absent Gemini, and seven-surface routing validate. |
| N/A — PNME-005 shares the Plan and Spec sources linked above | PASS — static QA, independent re-review, implementation commit/postflight, and exact eight-path terminal proposal are observed. | `9c4dcc7b`; unit/focused/strict/lifecycle/aggregate/all-files/diff PASS; requirements `COMPLIANT`; quality/security `APPROVED`; future closure SHA unclaimed; external/provider/live lanes remain `DEFER`. |
