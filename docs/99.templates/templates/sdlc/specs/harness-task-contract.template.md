---
title: '<Harness Task Contract>'
type: task
status: draft
owner: platform
updated: YYYY-MM-DD
---

# Harness Task Contract

Use this contract for any change that touches a harness surface (governance,
GitOps, infrastructure, validation scripts, CI, secrets, or operations). It
binds the task to allowed paths, approval boundaries, and static-vs-live
evidence before editing. Remove guidance comments in the authored copy.

## Goal

-

## Non-goals

-

## Affected Surfaces

-

## Allowed Paths

-

## Forbidden Paths

-

## Approval Required

- Resolve each affected surface against the approval matrix in
  [`../../../../00.agent-governance/rules/approval-boundaries.md`](../../../../00.agent-governance/rules/approval-boundaries.md).

## GitOps Impact

-

## Kubernetes Impact

-

## Secret / Vault Handling

- Record only path, key, property, mount, and redacted evidence. Never include
  secret values, Vault tokens, private keys, or certificate material.

## Static Validation

- `bash scripts/validate-harness.sh`

## Live Validation

- Operator-approved only; record approval status and reason if skipped.

## Operations / Runbook Impact

-

## Rollback Plan

-

## Evidence Location

-

## Related Documents

- [Harness Implementation Map](../../../../00.agent-governance/harness-implementation-map.md)
- [Local Harness Catalog](../../../../00.agent-governance/harness-catalog.md)
