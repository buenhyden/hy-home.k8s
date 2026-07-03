---
title: 'Task: Workspace Document Governance Hardening'
type: sdlc/task
status: draft
owner: platform
updated: 2026-07-03
---

# Task: Workspace Document Governance Hardening

## Overview

This document tracks implementation and verification work for workspace
document governance hardening. It keeps the audit, contract, provider,
workspace application, and final validation work traceable to the parent Spec
and Plan.

## Inputs

- **Parent Spec**: [Workspace Document Governance Hardening Spec](../../03.specs/013-workspace-document-governance-hardening/spec.md)
- **Parent Plan**: [Workspace Document Governance Hardening Plan](../plans/2026-07-03-workspace-document-governance-hardening.md)

## Working Rules

- Work audit-first and keep the current passing repository quality gate as the
  baseline.
- Every logical task must update this evidence file before commit.
- Documentation-only changes still require `git diff --check` and
  `bash scripts/validate-repo-quality-gates.sh .`.
- Repo-static validation must not be reported as live runtime readiness.
- Do not inspect secret values or mutate live Kubernetes, Argo CD, Vault,
  cloud, or publishing surfaces.
- Use sub-agent review for each major implementation unit when executing the
  plan.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Capture baseline document/provider/CI-QA audit inventory. | doc | Spec / Evaluation | Task 1 | Baseline scans, audit report decision, gate evidence | platform | Open |
| T-002 | Harden core template, frontmatter, routing, Stage 00, and validator contracts. | doc | Spec / Contracts | Task 2 | Route/profile scans and validator pass | platform | Open |
| T-003 | Harden provider entrypoint contracts for AGENTS, Claude, Codex, and Gemini surfaces. | doc | Spec / Agent Role & IO Contract | Task 3 | Provider topology scans and validator pass | platform | Open |
| T-004 | Apply document governance profiles to workspace README and authored documents. | doc | Spec / Guardrails | Task 4 | README/frontmatter/residue scans and validator pass | platform | Open |
| T-005 | Finalize deterministic validator checks, CI/QA evidence, and final review. | test | Spec / Success Criteria | Task 5 | Full local validation and final sub-agent READY | platform | Open |

## Suggested Types

- `doc`
- `test`
- `eval`
- `ops`
- `guardrail`

## Phase View

### Phase 1: Audit Inventory

- [ ] T-001 Capture baseline document/provider/CI-QA audit inventory.

### Phase 2: Core Contracts

- [ ] T-002 Harden core template, frontmatter, routing, Stage 00, and validator
  contracts.

### Phase 3: Provider Entrypoints

- [ ] T-003 Harden provider entrypoint contracts for AGENTS, Claude, Codex, and
  Gemini surfaces.

### Phase 4: Workspace Application

- [ ] T-004 Apply document governance profiles to workspace README and authored
  documents.

### Phase 5: Final Validation

- [ ] T-005 Finalize deterministic validator checks, CI/QA evidence, and final
  review.

## Verification Summary

- **Test Commands**:
  - `git diff --check`
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `bash scripts/validate-harness.sh`
- **Conditional Manifest Commands**:
  - `bash infrastructure/tests/verify-contracts-static.sh`
  - `bash scripts/validate-gitops-structure.sh`
  - `bash scripts/validate-k8s-manifests.sh .`
  - `bash scripts/check-secret-handling.sh .`
  - `bash scripts/validate-policy-gates.sh .`
- **Logs / Evidence Location**:
  - This task record.
  - `docs/00.agent-governance/memory/progress.md`.
  - `docs/90.references/audits/2026-07-03-workspace-document-governance-hardening-audit.md`
    if durable audit findings justify a separate Stage 90 report.

## Current Evidence

- Stage 03 Spec approved by user and committed in
  `ce5f6e2 docs(spec): Define workspace document governance hardening`.
- Stage 04 Plan and Task created from the approved Spec.

## Related Documents

- [Spec](../../03.specs/013-workspace-document-governance-hardening/spec.md)
- [Plan](../plans/2026-07-03-workspace-document-governance-hardening.md)
- [Template Documentation Contract](../../99.templates/support/documentation-contract.md)
- [Template Frontmatter Schema](../../99.templates/support/frontmatter-schema.md)
- [Template Routing Contract](../../99.templates/support/template-routing.md)
- [Agent Governance Hub](../../00.agent-governance/README.md)
- [CI/CD & QA Reference Guide](../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
