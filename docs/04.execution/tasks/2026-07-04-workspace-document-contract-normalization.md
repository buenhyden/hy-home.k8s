---
title: 'Task: Workspace Document Contract Normalization'
type: sdlc/task
status: draft
owner: platform
updated: 2026-07-04
---

# Task: Workspace Document Contract Normalization

## Overview

This document tracks implementation and verification work for workspace
document contract normalization. It keeps audit, contract, active document,
historical evidence, reference, CI/QA, validator, and final review work
traceable to the parent Spec and Plan.

## Inputs

- **Parent Spec**:
  [Workspace Document Contract Normalization Spec](../../03.specs/014-workspace-document-contract-normalization/spec.md)
- **Parent Plan**:
  [Workspace Document Contract Normalization Plan](../plans/2026-07-04-workspace-document-contract-normalization.md)

## Working Rules

- Use subagent-driven development for implementation.
- Each task gets one logical commit.
- Each task receives spec compliance review before code quality review.
- Documentation-only work still requires validation evidence.
- Historical evidence is in scope for normalization, but old facts must remain
  distinguishable from current operating guidance.
- Repo-static validation must not be reported as live runtime readiness unless
  a separate live check is approved and run.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Audit and inventory document contract drift. | doc | VAL-SPC-001, VAL-SPC-006 | PLN-001 | Audit report, drift scans, repo gate | platform | Done |
| T-002 | Normalize support contracts and template forms. | doc | Contracts, Core Design | PLN-002 | Route/profile parity scans, repo gate | platform | Done |
| T-003 | Apply active SDLC document profiles. | doc | VAL-SPC-002 | PLN-003 | Active docs scans, README checks, repo gate | platform | Todo |
| T-004 | Normalize historical evidence contracts. | doc | VAL-SPC-003 | PLN-004 | Historical evidence scans, archive/progress checks, repo gate | platform | Todo |
| T-005 | Align references, CI/QA, and formatting contracts. | doc | VAL-SPC-004, VAL-SPC-005 | PLN-005 | Official source review, workflow/doc comparison, repo gate | platform | Todo |
| T-006 | Reconcile final validator and governance gates. | test | VAL-SPC-006, VAL-SPC-007 | PLN-006 | Full validation bundle and final review | platform | Todo |

## Suggested Types

- `doc`
- `test`
- `guardrail`
- `ops`

## Phase View

### Phase 1: Audit

- [x] T-001 Audit and inventory document contract drift.

### Phase 2: Contract Sources

- [x] T-002 Normalize support contracts and template forms.

### Phase 3: Active Documents

- [ ] T-003 Apply active SDLC document profiles.

### Phase 4: Historical Evidence

- [ ] T-004 Normalize historical evidence contracts.

### Phase 5: References and CI/QA

- [ ] T-005 Align references, CI/QA, and formatting contracts.

### Phase 6: Final Validation

- [ ] T-006 Reconcile final validator and governance gates.

## Verification Summary

- **Required Commands**:
  - `git diff --check`
  - `bash -n scripts/validate-repo-quality-gates.sh`
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `bash scripts/validate-harness.sh`
- **Conditional Commands**:
  - `bash infrastructure/tests/verify-contracts-static.sh`
  - `bash scripts/validate-gitops-structure.sh`
  - `bash scripts/validate-k8s-manifests.sh .`
  - `bash scripts/check-secret-handling.sh .`
  - `bash scripts/validate-policy-gates.sh .`
- **Review Evidence**:
  - Spec compliance reviewer result after each task.
  - Code quality reviewer result after each task.
  - Final independent reviewer result for the full branch.

## Execution Evidence

### T-001 Audit and Inventory Document Contract Drift

Status: Done.

Evidence:

- Added the dated audit report:
  [Workspace Document Contract Normalization Audit](../../90.references/audits/2026-07-04-workspace-document-contract-normalization-audit.md).
- Updated the audit report index in
  [Audit References README](../../90.references/audits/README.md).
- Focused docs Markdown inventory counted 206 Markdown files, 181 authored
  frontmatter documents, 23 README files, 2 intentional common-template
  frontmatter-free exceptions, and 32 archive Tombstones.
- `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and
  `.github/SECURITY.md` were recorded as active frontmatter-free repository
  surfaces that need explicit contract treatment in T-002 or T-005.
- Read-only subagent cross-check found no validator-blocking drift and added
  three follow-up routes: scripts README count drift, coverage wording
  boundary drift, and resolved prior-audit findings that need historical
  framing.

Validation:

- `git diff --check` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.

### T-002 Normalize Support Contracts and Template Forms

Status: Done.

Evidence:

- Clarified `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and
  `.github/SECURITY.md` as frontmatter-free GitHub-native control Markdown in
  template support contracts, Stage 00 routing rules, and the repository
  quality gate.
- Extended reference template/support vocabulary with
  `dated-implementation-audit`, `data-catalog`, and `source-ledger` so new
  Stage 90 reference documents match observed repository usage.
- Clarified incident record routing: the incident file must live under
  `docs/05.operations/incidents/YYYY/INC-###-<title>/` and its filename must
  match the incident folder; `postmortem.md` remains in the same folder.
- Clarified that `docs/00.agent-governance/memory/<topic>.md` excludes the
  reserved `progress.md` route.
- Documented the required-heading extraction algorithm: literal `## `
  template headings are required unless they contain placeholders or are
  marked optional or if-applicable.
- Updated `docs/00.agent-governance/hooks/k8s-pre-edit.sh` so mismatched
  incident folder/file IDs produce an early route note instead of a misleading
  incident-template classification.
- Added official GitHub source links for PR template and security policy
  GitHub-native Markdown behavior.

Validation:

- `git diff --check` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash -n docs/00.agent-governance/hooks/k8s-pre-edit.sh` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- Pre-edit hook simulation for
  `docs/05.operations/incidents/2026/INC-001-demo/INC-002-other.md` emitted a
  route note that the incident filename must match the folder.
- Focused flat-template route scan — PASS.
- Focused support stale migration wording scan — PASS.
- Broad legacy residue scan found only historical Stage 04/progress evidence
  and template starter markers, not current support-contract drift.

### T-003 Apply Active SDLC Document Profiles

Status: Todo.

### T-004 Normalize Historical Evidence Contracts

Status: Todo.

### T-005 Align References, CI/QA, and Formatting Contracts

Status: Todo.

### T-006 Reconcile Final Validator and Governance Gates

Status: Todo.

## Related Documents

- **Spec**:
  [Workspace Document Contract Normalization Spec](../../03.specs/014-workspace-document-contract-normalization/spec.md)
- **Plan**:
  [Workspace Document Contract Normalization Plan](../plans/2026-07-04-workspace-document-contract-normalization.md)
- **Template Routing Contract**:
  [Template Routing](../../99.templates/support/template-routing.md)
- **Frontmatter Schema**:
  [Frontmatter Schema](../../99.templates/support/frontmatter-schema.md)
