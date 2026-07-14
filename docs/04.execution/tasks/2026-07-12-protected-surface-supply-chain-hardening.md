---
title: 'Task: Protected Surface and Supply Chain Hardening'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-12
---

# Task: Protected Surface and Supply Chain Hardening

## Overview

This Task tracks six bounded changes that harden protected repository surfaces
without claiming remote or live-system readiness. PSH-001 establishes the
reciprocal Spec, Plan, Task, and Stage-index chain. PSH-002 through PSH-006 add
fixture-tested Action, GitOps, Vault/ESO, bootstrap, secret-handling, and
repository-static closure evidence in dependency order.

## Inputs

- **Parent Spec**: [Protected Surface and Supply Chain Hardening Technical Specification](../../03.specs/032-protected-surface-supply-chain-hardening/spec.md)
- **Parent Plan**: [Protected Surface and Supply Chain Hardening Implementation Plan](../plans/2026-07-12-protected-surface-supply-chain-hardening.md)
- **QA Baseline**: Completed Spec 031 owns affected-surface selection, local/CI
  parity, cross-provider role semantics, and the Stage 00 QA handoff.
- **Security Baseline**: Official GitHub Actions, OpenGitOps, External Secrets,
  Vault, and Kubernetes guidance referenced by the parent Spec defines the
  reviewed repository-static boundaries.

## Task Table

| Task ID | Description | Type | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| PSH-001 | Start reciprocal execution evidence | doc | Reciprocal-link assertion | platform | Done |
| PSH-002 | Add Action identity and permission validator | guardrail | Action fixture self-test | platform | Pending |
| PSH-003 | Pin nine Action identities and minimize workflow permissions | ci | Action validator, actionlint, zizmor | platform | Pending |
| PSH-004 | Add GitOps identity and deletion change-set review | guardrail | GitOps fixture self-test | platform | Pending |
| PSH-005 | Harden local Vault/ESO and bootstrap secret handling | security | Vault fixture, static contracts, secret scan | platform | Pending |
| PSH-006 | Close repository-static evidence and lifecycle | doc | Full QA bundle and independent review | platform | Pending |

## Approval and Safety Boundaries

- **Allowed Paths**: Each logical unit is limited to the exact `Files` list in
  the parent Plan. PSH-001 changes only this Task, its parent Spec and Plan, and
  their three Stage indexes plus the Task's one durable-ledger row.
- **Forbidden Paths**: Provider credentials, authentication state, ignored
  certificates or local settings, secret values, kubeconfigs, generated local
  output, and paths outside the active Plan unit are excluded.
- **Approval Required**: Human approval is required before push, merge, remote
  workflow execution, certificate or credential change, GitOps reconciliation,
  Kubernetes apply, Vault request, or other live operator action.
- **Static Validation**: Run the exact RED/GREEN fixture or assertion for the
  active PSH row, its focused validator commands, repository quality gates,
  pre-commit, diff checks, exact staged-path proof, and independent review where
  required by the parent Plan.
- **Live Validation**: DEFER. Repository-static checks do not prove GitHub
  remote behavior, Argo CD prune or reconciliation, ESO authentication, Vault
  TLS/runtime behavior, or Kubernetes authorization.
- **Secret / Vault Handling**: Do not read, print, decode, enumerate, move, or
  modify secret values, tokens, certificates, Vault data, provider auth files,
  shell history, or ignored local state.
- **Rollback Plan**: Revert completed PSH logical commits newest-first. Keep
  validators and their consumers in the same owning unit or revert consumers
  before their contracts.
- **Evidence Location**: This Task, its parent Spec and Plan, logical commits,
  repository-static validator output, and ignored `.superpowers/sdd/psh*-report.md`
  review packages.
- **GitOps Impact**: PSH-004 reviews rendered identity and deletion candidates
  only; it does not apply, prune, or reconcile desired state.
- **Kubernetes Impact**: No live cluster mutation is authorized.
- **Operations / Runbook Impact**: PSH-005 may align tracked local-only security
  contracts and runbook evidence only within its exact Plan boundary.

## Verification Summary

PSH-001 began from the expected RED state: the canonical Task path did not
exist, so the reciprocal-lineage assertion exited 1 before inspecting links.
GREEN requires the Spec, Plan, and Task to name one another, one Active index
row dated 2026-07-12 for each document, the exact PSH-001 through PSH-006 table,
one exact fourteen-column durable-ledger row, strict document conformance, the
full repository quality gate, focused pre-commit, and exactly seven staged
paths with no unstaged tracked changes. This evidence is repository-static;
remote and live lanes remain DEFER.

## Traceability

- [Protected Surface and Supply Chain Hardening Spec](../../03.specs/032-protected-surface-supply-chain-hardening/spec.md)
- [Protected Surface and Supply Chain Hardening Plan](../plans/2026-07-12-protected-surface-supply-chain-hardening.md)
- [Affected Surface and Agent QA Spec](../../03.specs/031-affected-surface-agent-qa/spec.md)
- [Workspace Document Assurance PRD](../../01.requirements/005-workspace-document-assurance-modernization.md)
- [Workspace Document Assurance ARD](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- [Current Remediation Roadmap](../../90.references/audits/2026-07-11-weia/remediation-roadmap.md)
