---
title: 'Task: Provider-Native Runtime and Model Evidence'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-29
---

# Task: Provider-Native Runtime and Model Evidence

## Overview

This Task is the durable evidence ledger for the
[Spec 042 Plan](../plans/2026-07-28-provider-native-runtime-and-model-evidence.md).
It records cutoff source reconciliation, local version observations, provider
surface boundaries, model/effort candidate treatment, secret-free canary
records, QA, review, and closure.

Spec 041 terminal closure `1a3232ce73a653371634e99d773d71ab03f87967` and
postflight evidence update `6c35268793f09c1ba3f70cdbe3ece9293828ec16`
are observed prerequisites. Terminal evidence reconciliation `fdc3d457`
removes stale future-gate wording before this tranche activates.

## Inputs

- [Provider-Native Runtime and Model Evidence Implementation Plan](../plans/2026-07-28-provider-native-runtime-and-model-evidence.md)
- [Spec 042](../../03.specs/042-provider-native-runtime-and-model-evidence/spec.md)
- [PRD-003](../../01.requirements/003-workspace-agent-governance-platform.md)
- [ARD-0006](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md)
- [ADR-0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- [Harness machine contract](../../00.agent-governance/contracts/harness-contract.json)
- `docs/90.references/research/2026-07-07-wer/provider-implementation-status.md`; [current lookup](../../90.references/research/2026-08-08-wer/provider-implementation-status.md)
- Spec 041 closure `1a3232ce73a653371634e99d773d71ab03f87967`,
  postflight `6c35268793f09c1ba3f70cdbe3ece9293828ec16`, and terminal
  evidence reconciliation `fdc3d457`

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| PNME-000 | VAL-PNME-001 through VAL-PNME-009 | Activate reciprocal Spec/Plan/Task frontier after Spec 041 closure. | platform | Done | PASS — the exact eight-path activation and postflight satisfy lifecycle, strict document, aggregate, all-files, diff, and independent review gates. | Activation `1c3cc9bf32adae3033494ae7cb50eaaf1650b096`; parent `fdc3d457a3806f86c288ea1bb923898a67294709`; exact eight paths; explicit-ref lifecycle and clean-tree aggregate PASS; requirements compliant; quality approved; no provider-runtime or model-promotion claim. |
| PNME-001 | VAL-PNME-002, VAL-PNME-004 | Refresh official cutoff source ledger and unsupported model/runtime claims. | platform | Done | PASS — the fixed ten-source ledger records exact UTC publication time when known, requires precision for cutoff-day claims, and preserves the protected Current research snapshot. | Config validator production/self-test PASS with 13 closed mutations, including same-day-after-cutoff, source-set substitution/growth, invalid calendar date, and exact observed-version cases. |
| PNME-002 | VAL-PNME-004 | Normalize provider model/effort candidates, exact-ID uncertainty, fallback behavior, and the Spec 044 fitness gate. | platform | Done | PASS — eight provider/role model records remain candidate-only and require config parse, exact runtime resolution, no silent fallback, and Spec 044 fitness. | Provider contract/schema and config unit suite PASS; no candidate is promoted to a current assignment. |
| PNME-003 | VAL-PNME-005 through VAL-PNME-008 | Define secret-free provider baseline/canary records and provider verdict handling. | platform | Done | PASS — twelve provider/evidence-class canaries use closed redacted records and evidence-lane-specific verdicts. | Canary production/self-test PASS with eight negative mutations; credentials, raw prompts, provider bodies, mutation, missing ownership/retry trigger, and cross-lane promotion are rejected. |
| PNME-004 | VAL-PNME-001 through VAL-PNME-003 | Validate tracked provider paths, native metadata, MCP/tool boundaries, and target-only Gemini admission. | platform | Done | PASS — four provider surfaces, canonical repo-relative project paths, seven MCP servers, and target-only absent Gemini are validated without runtime promotion. | Affected-surface self/production, strict registry/Markdown/links, role audit, Current-pack RIA, and repository aggregate PASS. |
| PNME-005 | VAL-PNME-001 through VAL-PNME-009 | Run focused/static/strict/aggregate/all-files QA, independent review, atomic closure, and postflight. | platform | Done | PASS — focused/static/strict/aggregate/all-files/diff lanes, independent re-review, implementation postflight, and the exact eight-path terminal proposal are observed. The future closure SHA and post-closure evidence event are not preclaimed. | Implementation `9c4dcc7b7572bfe8f436d81ee87ede872707cc73`; provider unit `17/17`, config `13`, canary `8`, affected `21/21`, strict registry `455`, aggregate PASS, all applicable pre-commit hooks PASS; requirements `COMPLIANT`; quality/security `APPROVED`; provider discovery/authenticated run, hosted CI, remote, credential, and live lanes remain `DEFER`. |

## Approval and Safety Boundaries

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

## Verification Summary

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

## Traceability

- **Plan**: [Provider-Native Runtime and Model Evidence Implementation Plan](../plans/2026-07-28-provider-native-runtime-and-model-evidence.md)
- **Spec**: [Provider-Native Runtime and Model Evidence](../../03.specs/042-provider-native-runtime-and-model-evidence/spec.md)

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [PNME-000](../plans/2026-07-28-provider-native-runtime-and-model-evidence.md#work-breakdown) | PASS — exact eight-path activation and postflight satisfy their repository-static gates. | `fdc3d457` → `1c3cc9bf`; explicit-ref lifecycle and clean-tree aggregate passed; no provider-runtime claim. |
| [PNME-001](../../03.specs/042-provider-native-runtime-and-model-evidence/spec.md#success-criteria--verification-plan) | PASS — fixed cutoff source ledger implemented. | Exact ten-source set, UTC cutoff-day precision, prior/current observation separation, and protected Current snapshot preservation validate. |
| N/A — PNME-002 shares the Plan and Spec sources linked above | PASS — candidate model/effort policy implemented without assignment promotion. | Eight candidate-only records retain exact parse, runtime resolution, fallback, and Spec 044 fitness gates. |
| N/A — PNME-003 shares the Plan and Spec sources linked above | PASS — provider baseline/canary records implemented. | Twelve closed redacted records and eight canary mutations validate evidence-specific verdict behavior. |
| N/A — PNME-004 shares the Plan and Spec sources linked above | PASS — tracked surfaces and MCP boundaries reconciled. | Four surfaces, canonical repo-relative project paths, seven MCP servers, target-only absent Gemini, and seven-surface routing validate. |
| N/A — PNME-005 shares the Plan and Spec sources linked above | PASS — static QA, independent re-review, implementation commit/postflight, and exact eight-path terminal proposal are observed. | `9c4dcc7b`; unit/focused/strict/lifecycle/aggregate/all-files/diff PASS; requirements `COMPLIANT`; quality/security `APPROVED`; future closure SHA unclaimed; external/provider/live lanes remain `DEFER`. |
