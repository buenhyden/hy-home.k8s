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

### Shared terminology and ownership

| Term | Meaning and owner |
| --- | --- |
| Requirement | Durable need and acceptance boundary; Stage 01. |
| Architecture Description / Architecture Decision Record | Current structural view / durable choice and rationale; Stage 02. |
| Spec / Plan / Task | Change contract / execution order and risk / work, verification, and handoff evidence; one Stage 03 package. |
| Policy / rule / contract / control | A policy owns normative meaning; a rule is one obligation; a contract specifies an interface or invariant; a control enforces it. Common behavior belongs to Stage 00 policies, executable enforcement to scripts, document shape to Stage 99. These terms do not create parallel policy directories. |
| Provider / Role / Agent | Runtime-specific adapter contract / neutral responsibility and allowed scope / an executing instance of a role. Native configuration is not evidence of runtime enforcement. |
| Skill | Reusable procedure under Stage 00 skills; native discovery depends on the provider contract. A plain procedure reference is not a native registration. |
| Hook / Gate / validator / Fixture | Native event callback / blocking quality decision / executable check implementing that decision / independent bounded test input. A hook need not run QA, and a test fixture is never production policy input. |
| QA / CI / CD | Quality checks / hosted validation of a checkout / delivery and reconciliation. Local and CI static QA share one execution contract; Argo CD reconciles the declared GitOps state under the operating boundary. |
| Deployment / release | Applying a declared version to an environment / identifying and publishing a deliverable. Neither follows automatically from local validation or a commit. |
| Guide / Runbook | Explanatory operating knowledge / triggered operational steps with rollback and verification; Stage 05. |
| Evidence / archive | Observed result with input, environment, and limits / non-authoritative historical retention. Task and Git own change evidence; Stage 98 owns retained recovery records. |

### Proportional transitions

| Transition | Entry and output | Approval and evidence | Failure or rollback |
| --- | --- | --- | --- |
| Need to design | Requirement or direct scoped request; structural views or decision only when boundaries change | Request owner approves scope; design approval when required | Clarify an unresolved boundary before dependent implementation |
| Design to execution | Accepted change contract and ordered Plan; Task records work and checks | Reuse valid approval for the same scope; never infer approval from a checkbox | Revise the Plan when evidence contradicts it; preserve unrelated work |
| Execution to handoff | Reviewed final bytes and required checks; scoped Git commit and Task result | Local, index, hosted, provider, and live evidence remain distinct | Failed required checks block completion; missing external permission is DEFER |
| Handoff to operations or retention | Stable operating knowledge or terminal work record | Promote only durable meaning; apply Stage 99 lifecycle and recovery contracts | Keep failures factual; use Git recovery rather than a second active owner |

A small correction reuses its current work owner and proportional checks. It
need not create a Requirement, ADR, or a new Spec package merely to edit a file.

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
