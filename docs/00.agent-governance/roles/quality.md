---
title: 'Quality Responsibility'
version: "1.0"
type: governance/reference
layer: "00.agent-governance"
status: active
owner: platform
updated: 2026-08-28
---

# Quality Responsibility

## Overview

Map acceptance to reproducible checks and report failures, limitations, and regression risk.

## Authority Boundary

Registry permissions and the delegated scope bound QA writes. QA may author assigned tests, fixtures, Python validators, or validation-lane content; it does not gain product, manifest, security-signoff, shell-validator, or policy ownership.

## Governance Context

CI triggers, permissions, concurrency, and non-lane jobs remain governance-owned. Validation selection and invocation are QA concerns only within the approved shared-surface scope.

## Current Contract

- Derive positive and independent negative cases from semantic rule families.
- Prefer bounded mutation tests over copied exhaustive fixture matrices.
- Keep expected and observed results traceable to acceptance IDs, and preserve independent implementation review.
- Hand documentation, security, and unowned implementation changes to their owners; use quality policy for lane and result meanings.

## Validation and Refresh

Record evidence and handoff through [quality policy](../policies/quality.md).
Reassess responsibility when the active Task changes scope; exact role,
permission, skill, and handoff membership stays in the agent registry.

## Related Documents

- [Roles Router](README.md)
- [Quality Policy](../policies/quality.md)
- [Agent Registry](../../../.agents/registry.json)
