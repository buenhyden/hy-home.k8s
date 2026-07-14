---
title: 'Agent Quality Standards (March 2026)'
type: governance/reference
status: active
owner: platform
updated: 2026-07-14
---

# Agent Quality Standards (March 2026)

## Overview

Quality gates for governance and execution alignment.

### Required Quality Dimensions

- Accuracy: policy text matches actual workspace behavior.
- Concision: avoid repetitive or generic instructions.
- Actionability: every rule implies a concrete action.
- Consistency: no conflicts across bootstrap, persona, scope, and provider docs.

## Authority Boundary

### Coverage Applicability

- Future testable application code should target at least 90% line and branch coverage where a language-specific test framework and coverage tool exist.
- Current Bash/YAML/Markdown infrastructure work uses validation-matrix coverage instead of fake numeric code coverage.
- The validation matrix for this repository includes repository quality gates, GitOps structure checks, Kubernetes manifest syntax, static infrastructure contracts, secret handling scans, shell syntax, CI workflow checks, README/template checks, and explicit live-check limitations.
- Repo-static, CI/toolchain, and live runtime readiness are separate evidence lanes. Do not present repository or CI validation as proof of live k3d, ArgoCD, Vault, ESO, deployment, or external-service health unless the matching live check was approved and run.
- CI/static validation and QA evidence must distinguish optional-tool skips from successful
  full coverage. A fallback path or skipped optional tool is not the same as
  complete tool coverage.
- GitHub Actions is the provider-agnostic remote QA gate for this repository; it
  is not live deployment CD and must not be used as evidence of live runtime
  readiness without an approved live check.
- Provider parity is validated as role parity plus evidence, not identical
  metadata keys. Claude, Gemini, and Codex adapters must preserve role, scope,
  guardrails, handoff, and postflight while using native metadata and
  permission surfaces.
- PR verification must state which coverage lane applies: 90% code coverage for future testable application code, or validation-matrix coverage for current infrastructure artifacts.

## Governance Context

The affected-surface contract selects repository validators; this rule owns the
meaning of their evidence and handoff vocabulary. Preflight defines expected
lanes, postflight confirms results, and provider adapters consume the same
terms without redefining them. CI, provider-runtime, and live evidence remain
separate authorities.

## Current Contract

### Validation Lane Contract

`docs/00.agent-governance/contracts/validation-surfaces.json` owns path-to-
validator and local/CI selection. This document owns how agents name and report
the resulting lanes:

- **affected**: validators selected for normalized changed paths during work.
  Evidence names the input path set and every selected validator. An empty path
  set or a validator with no applicable files is `SKIP`, not `PASS`.
- **staged**: standard file hooks evaluated against the actual Git index before
  commit. Evidence must identify the staged scope; an affected-path or
  working-tree run cannot stand in for this lane.
- **all-files**: all applicable file hooks plus the repository quality gate.
  This lane does not execute or prove `commit-msg` or explicit `manual` stages.
- **message/manual**: commit-message and explicit manual-stage checks. Report
  each applicable check separately; do not infer it from `--all-files`.
- **ci**: jobs deterministically selected from the affected-surface contract.
  Local selector, workflow syntax, and static Action checks are repo-static
  evidence only; a remote GitHub run needs its own check URL or run identity.
- **remote/live**: provider discovery/consumption, remote execution, and
  operator-approved Kubernetes, Argo CD, Vault, ESO, cloud, or deployment
  verification. Without direct authorized evidence this lane is `DEFER`.

### Result Vocabulary

- `PASS`: the named command or check ran over the stated scope and satisfied
  its acceptance condition.
- `SKIP`: the lane was selected but had no applicable files, or an explicitly
  optional tool was unavailable; record the reason and any independent
  fallback result.
- `FAIL`: the command ran or input validation stopped execution and the stated
  acceptance condition was not met.
- `DEFER`: the lane requires unavailable authority, environment, provider, or
  remote/live evidence. `DEFER` is a visible limitation, never a pass.

### Handoff Evidence Contract

Every repo-changing agent handoff records the following fields in the owning
Task or approved evidence record. A field may say `none` or `DEFER` with a
reason, but it must not be silently omitted:

- scope and changed paths;
- acceptance IDs;
- commands and tool/version;
- per-lane `PASS`, `SKIP`, `FAIL`, or `DEFER` results;
- limitations;
- reviewer identity and review disposition;
- rollback commit(s) or bounded rollback procedure;
- residual risk; and
- next owner.

Static gateway, hook, or role-adapter presence proves only tracked repository
configuration. It does not prove that Claude, Codex, Gemini, or another native
runtime discovered, loaded, or enforced that adapter.

## Validation and Refresh

### Minimum Verification for Governance Updates

- Structure parity with expected governance tree.
- English-only check under `docs/00.agent-governance/`.
- Root shim link checks for `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`.
- Affected-surface and provider-neutral role-semantic validators pass alongside
  provider-native metadata and roster-currentness checks.
- Checklist references remain valid (`preflight`, `postflight`, `stage-authoring-matrix`, `stage-checklists`).
- Diff check confirms no unintended edits outside the approved change scope.

## Related Documents

- [Validation Surface Contract](../contracts/validation-surfaces.json)
- [Harness Approval Boundaries](approval-boundaries.md)
- [Postflight Checklist](postflight-checklist.md)
- [Harness Implementation Map](../harness-implementation-map.md)
