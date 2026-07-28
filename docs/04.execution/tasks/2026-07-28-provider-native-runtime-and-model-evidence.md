---
title: 'Task: Provider-Native Runtime and Model Evidence'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-28
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
- [Provider evidence research](../../90.references/research/2026-07-07-wer/provider-implementation-status.md)
- Spec 041 closure `1a3232ce73a653371634e99d773d71ab03f87967`,
  postflight `6c35268793f09c1ba3f70cdbe3ece9293828ec16`, and terminal
  evidence reconciliation `fdc3d457`

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| PNME-000 | VAL-PNME-001 through VAL-PNME-009 | Activate reciprocal Spec/Plan/Task frontier after Spec 041 closure. | platform | Done | PASS — the exact eight-path activation and postflight satisfy lifecycle, strict document, aggregate, all-files, diff, and independent review gates. | Activation `1c3cc9bf32adae3033494ae7cb50eaaf1650b096`; parent `fdc3d457a3806f86c288ea1bb923898a67294709`; exact eight paths; explicit-ref lifecycle and clean-tree aggregate PASS; requirements compliant; quality approved; no provider-runtime or model-promotion claim. |
| PNME-001 | VAL-PNME-002, VAL-PNME-004 | Refresh official cutoff source ledger and unsupported model/runtime claims. | platform | Queued | Not executed. | Claude, Codex, Gemini, and agency-agents sources will be recorded with cutoff applicability. |
| PNME-002 | VAL-PNME-004 | Normalize provider model/effort candidates, exact-ID uncertainty, fallback behavior, and the Spec 044 fitness gate. | platform | Queued | Not executed. | No candidate becomes a current role assignment without parse, runtime resolution, and fitness evidence. |
| PNME-003 | VAL-PNME-005 through VAL-PNME-008 | Define secret-free provider baseline/canary records and provider verdict handling. | platform | Queued | Not executed. | `PASS`, `FAIL`, `BLOCKED`, `ABSENT`, and `DEFER` records must be redacted, comparable, and evidence-class specific. |
| PNME-004 | VAL-PNME-001 through VAL-PNME-003 | Validate tracked provider paths, native metadata, MCP/tool boundaries, and target-only Gemini admission. | platform | Queued | Not executed. | Repository-static validation must not promote provider discovery, authenticated-run, or Gemini-native readiness. |
| PNME-005 | VAL-PNME-001 through VAL-PNME-009 | Run focused/static/strict/aggregate/all-files QA, independent review, atomic closure, and postflight. | platform | Queued | Not executed. | Commands, reviewer verdicts, closure commits, rollback, and external limitations will be recorded here. |

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
live PASS. The user-reported local observation remains Codex CLI
`0.145.0-alpha.27` present with Claude and Gemini CLIs absent; it is not a
provider-readiness result.

Initial staged validation exposed missing reciprocal Task body sections and
relationships. The repaired exact eight-path proposal then passed strict
registry, Markdown body-contract, cross-link/owner, staged lifecycle,
repository aggregate, all-files pre-commit, cached/unstaged diff, requirements
scope, and independent quality review. PNME-000 is complete without claiming
an unobserved result.

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
| [PNME-001](../../03.specs/042-provider-native-runtime-and-model-evidence/spec.md#success-criteria--verification-plan) | Queued — cutoff source ledger not yet refreshed. | Official Claude, Codex, Gemini, and pinned agency-agents evidence required. |
| N/A — PNME-002 shares the Plan and Spec sources linked above | Queued — model/effort candidates are not assignments. | Exact configured/observed IDs, fallback, runtime resolution, and Spec 044 fitness remain required. |
| N/A — PNME-003 shares the Plan and Spec sources linked above | Queued — baseline/canary schemas not yet implemented. | Closed, synthetic, secret-free records with evidence-specific verdicts required. |
| N/A — PNME-004 shares the Plan and Spec sources linked above | Queued — tracked surfaces not yet reconciled. | Local/Antigravity, Claude, Codex, and target-only Gemini remain non-transitive evidence lanes. |
| N/A — PNME-005 shares the Plan and Spec sources linked above | Queued — terminal QA/review/closure not executed. | Focused, strict, lifecycle, aggregate, all-files, diff, and independent review evidence required. |
