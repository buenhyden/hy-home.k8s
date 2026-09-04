---
title: "Software Development Lifecycle"
version: "1.1.0"
type: "governance/contract"
status: "active"
owner: "platform"
updated: "2026-09-04"
---

# Software Development Lifecycle

## Overview

This document owns the human flow from durable requirements through
architecture, Spec-driven implementation, operations, and historical recovery.
Stage numbers express ownership and navigation rather than a one-way approval
waterfall.

## Authority Boundary

This flow selects the responsible document stage. Exact paths, profile IDs,
frontmatter, sections, relationships, status classes, and lifecycle edges come
only from the [Stage 99 registry](../99.templates/registry.json). Provider and
agent-roster authority is outside Stage 99 and is not defined here.

## Governance Context

Work begins with repository evidence and a testable Requirement Package or a
directly approved package-local work unit. Architecture Descriptions record
current structure; ADRs record durable choices. A Stage 03 work unit owns its
Spec, Plan, and independently reviewable Tasks. Stable operating knowledge
moves to Stage 05, reusable evidence to Stage 90, and historical recovery
evidence to Stage 98.

The common flow is Clarify → Spec → Plan → Tasks → cross-artifact analysis →
Implement → Verify → promote durable meaning → Complete or Archive. GitHub
Spec Kit informs that flow without replacing this repository's per-Task
records. Diátaxis informs Operations reader intent, C4 and arc42 inform
proportional Architecture Description views, ADR practice preserves decision
lineage, and Google SRE informs factual incidents and blameless postmortems.

## Current Contract

1. Establish the problem, acceptance boundary, and complete requirement IDs.
2. Record structural views and durable decisions before implementation when
   the change affects system boundaries or important trade-offs.
3. Implement through one Stage 03 Spec package with ordered Plan and Task
   evidence, using RED then GREEN validation.
4. Promote stable operator controls to Guide, Policy, or Runbook owners and
   preserve incident learning in Incident and Postmortem records.
5. Supersede, retire, withdraw, or seal documents only through registry-owned
   lifecycle edges and the applicable reciprocal or recovery evidence.
6. Keep release procedure in a Runbook when one is needed, local execution
   evidence in Tasks and Git, and tag, hosted CI, provider, or live release
   evidence external. Do not create a Release Record without a successor ADR,
   profile, lifecycle, template, and demonstrated audit consumer.

The terminal Stage 04 slot remains unused. Root `DESIGN.md` remains the UI and
design-system authority, not a Stage 03 technical-design artifact.

## Validation and Refresh

Run the registry, Markdown profile, link/owner, lifecycle, affected-surface,
and repository quality gates selected by the changed paths. Treat repository
static results separately from hosted, provider-runtime, remote, or live
evidence.

## Related Documents

- [Governance Hub](README.md)
- [Document Lifecycle Policy](policies/document-lifecycle.md)
- [Document Authoring Policy](policies/document-authoring.md)
- [Document Profile Registry](../99.templates/registry.json)
