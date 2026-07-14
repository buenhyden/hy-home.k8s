---
title: 'Control Surface and Cloud Example Documentation Normalization Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-14
---

# Control Surface and Cloud Example Documentation Normalization Implementation Plan

## Overview

This document defines the implementation plan for normalizing active
repository control-surface documentation and promoting AWS/Azure example docs
to an explicit example-local SDLC snapshot route.

> **2026-07-14 steady-state correction:** This Plan records the completed
> normalization tranche. Spec 030 later retired both `examples/*/docs/**`
> trees into `docs/90.references/cloud-examples/**`; the current registry has
> no authored/README route for those source paths and rejects tracked
> reintroduction. The route language below is historical execution evidence.

## Context

The repository already distinguishes README files, GitHub-native Markdown, and
Cloud Example Snapshot docs. The approved design keeps README and GitHub-native
files frontmatter-free while adding a routed example-local SDLC snapshot
profile for `examples/aws/docs/**` and `examples/azure/docs/**`.

## Goals & In-Scope

- **Goals**:
  - Align Stage 99 support contracts, Stage 00 governance, and validator
    behavior with the example-local SDLC snapshot route.
  - Keep control-surface README and GitHub-native Markdown files as
    frontmatter-free routing surfaces.
  - Normalize AWS/Azure example docs by document type without copying template
    placeholders.
  - Preserve snapshot boundaries and remove stale provider-latest claims.
  - Record deterministic validation evidence.
- **In Scope**:
  - `.github`, `examples`, `gitops`, `infrastructure`, `policy`, `scripts`,
    `secrets`, `tests`, and `traefik` documentation and validation surfaces.
  - Stage 00/03/04/99 documentation updates required by the route change.
  - Repository-static validation scripts.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Provider-latest refresh for AWS or Azure managed service guidance.
  - Live runtime validation.
  - Remote GitHub, cloud, credential, deploy, publish, or merge actions.
- **Out of Scope**:
  - Moving example-local docs into the main `docs/01` through `docs/05`
    lifecycle tree.
  - Secret value inspection.
  - Cosmetic file renames that do not support a contract or link fix.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Establish the spec, plan, task, README indexes, and progress memory. | `docs/03.specs/022-control-cloud-doc-normalization/spec.md`, this plan, task record, Stage 03/04 READMEs, progress ledger | VAL-CCDN-001 | Spec/plan/task exist, indexes link them, and `git diff --check` passes. |
| PLN-002 | Update route, frontmatter, and governance contracts for example-local SDLC snapshot docs. | `docs/99.templates/support/**`, `docs/00.agent-governance/rules/**`, `scripts/validate-repo-quality-gates.sh` | VAL-CCDN-001, VAL-CCDN-002 | README/GitHub-native exceptions and example-local SDLC routes are unambiguous and validated. |
| PLN-003 | Normalize active control-surface routing text. | `.github/*.md`, `examples/README.md`, `gitops/README.md`, `infrastructure/README.md`, `scripts/README.md`, `tests/README.md`, `traefik/README.md`, `policy/**`, `secrets/**` | VAL-CCDN-002, VAL-CCDN-004 | README and GitHub-native Markdown remain frontmatter-free and route to canonical owners. |
| PLN-004 | Normalize AWS example-local SDLC snapshot documents. | `examples/aws/docs/**` | VAL-CCDN-003, VAL-CCDN-004 | Non-README docs have valid frontmatter, type-appropriate sections, snapshot wording, and updated links. |
| PLN-005 | Normalize Azure example-local SDLC snapshot documents. | `examples/azure/docs/**` | VAL-CCDN-003, VAL-CCDN-004 | Non-README docs have valid frontmatter, type-appropriate sections, snapshot wording, and updated links. |
| PLN-006 | Close validation and evidence. | `scripts/validate-repo-quality-gates.sh`, task record, progress ledger | VAL-CCDN-005 | `git diff --check`, shell syntax, repo-quality, manifest, secret, and policy gates pass or accurately report optional skips. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Markdown whitespace and patch integrity. | `git diff --check` | No output. |
| VAL-PLN-002 | Static | Repository quality and route/frontmatter checks. | `bash scripts/validate-repo-quality-gates.sh .` | Prints repository quality gate pass. |
| VAL-PLN-003 | Static | Validator syntax. | `bash -n scripts/validate-repo-quality-gates.sh` | No output. |
| VAL-PLN-004 | Manifest | Manifest syntax and optional kube-linter coverage. | `bash scripts/validate-k8s-manifests.sh .` | Pass or explicit optional-tool skip only. |
| VAL-PLN-005 | Security | Plaintext secret scan. | `bash scripts/check-secret-handling.sh .` | No plaintext secret findings. |
| VAL-PLN-006 | Policy | OPA/Conftest or fallback policy gate. | `bash scripts/validate-policy-gates.sh .` | Pass or explicit optional-tool fallback pass. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Example docs become confused with production SDLC docs. | High | Keep them under `examples/<provider>/docs/**` and document the example-local snapshot boundary in contracts and validators. |
| README files accumulate policy bodies. | Medium | Keep README changes to routing, scope, structure, and matrices; move durable rules to Stage 00/99 or scripts. |
| Provider currentness claims become misleading. | High | Rewrite claims as dated snapshots unless a provider refresh spec is approved. |
| Bulk normalization breaks cross-links. | Medium | Use targeted `rg` searches after each rename or consolidation and update links in the same commit. |
| Validator overreaches and blocks GitHub-native files. | Medium | Keep explicit route exceptions for `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and `.github/SECURITY.md`. |

### Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Run repository-static validation after each logical
  batch.
- **Sandbox / Canary Rollout**: Not applicable; this is documentation and
  validation work.
- **Human Approval Gate**: Already granted for the design. Additional approval
  is required for live runtime, remote GitHub, cloud, credential, publish,
  merge, or destructive external action.
- **Rollback Trigger**: If validation cannot classify example-local docs
  deterministically, stop and restore the previous snapshot exception until a
  narrower route can be designed.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [x] Scoped work completed.
- [x] Example-local SDLC snapshot route documented and validated.
- [x] Control-surface README and GitHub-native Markdown frontmatter-free
  boundary preserved.
- [x] AWS and Azure example docs normalized or explicitly deferred with
  evidence.
- [x] Required validation passed.
- [x] Task record and progress memory updated.

## Traceability

- **Spec**: [../../03.specs/022-control-cloud-doc-normalization/spec.md](../../03.specs/022-control-cloud-doc-normalization/spec.md)
- **Tasks**: [../tasks/2026-07-06-control-cloud-doc-normalization.md](../tasks/2026-07-06-control-cloud-doc-normalization.md)
- **Template Routing**: [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
- **Frontmatter Schema**: [../../99.templates/support/frontmatter-schema.md](../../99.templates/support/frontmatter-schema.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
