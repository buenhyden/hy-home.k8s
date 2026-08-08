---
title: 'Reference: Spec-Driven SDLC and Document Contracts'
type: content/reference
status: active
owner: platform
updated: 2026-08-08
---

# Reference: Spec-Driven SDLC and Document Contracts

## Overview

Baseline routing for the documented software lifecycle and named document
families.

## Reference Type

Repository-static research baseline.

## Authority Boundary

Stage owners and document profiles own lifecycle and template contracts; this
reference is not a new process rule.

## Scope

It names the requested SDLC and document-family owners pending WERPC-003
source review.

## Definitions / Facts

### Spec-driven development baseline

`docs/03.specs/` is the current specification stage; completeness of a
spec-driven workflow is Unverified.

### SDLC baseline

The Stage 01 through Stage 05 documentation taxonomy is current repository
structure; its external benchmark alignment is Unverified.

### PRD baseline

`docs/01.requirements/` is the PRD-stage evidence path.

### ARD baseline

`docs/02.architecture/requirements/` is the ARD-stage evidence path.

### ADR baseline

`docs/02.architecture/decisions/` is the ADR-stage evidence path.

### Guide baseline

`docs/05.operations/guides/` is the guide evidence path.

### Incident baseline

`docs/05.operations/incidents/` is the incident evidence path; exercised
incident readiness is Unverified.

### Postmortem baseline

`docs/05.operations/postmortems/` is the postmortem evidence path; exercised
postmortem readiness is Unverified.

### Policy baseline

`docs/05.operations/policies/` is the policy evidence path.

### Release baseline

`.github/workflows/` is current release-adjacent evidence; a dedicated release
contract is Unverified.

### Runbook baseline

`docs/05.operations/runbooks/` is the runbook evidence path.

## Sources

No current external SDLC source was reviewed in WERPC-001; predecessor evidence
is retained only in the source ledger for later recheck.

## Review and Freshness

WERPC-003 adds source-backed document-family analysis. Refresh after profile
or stage-taxonomy changes.

## Related Documents

- [Documentation architecture](documentation-architecture-and-diataxis.md)
- [Pack coverage matrix](README.md#requirement-coverage-matrix)
- [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
