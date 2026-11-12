---
title: "Software Development Lifecycle"
version: "3.4.1"
type: "governance/contract"
status: "active"
owner: "platform"
updated: "2026-11-12"
---

# Software Development Lifecycle

## Overview

This document owns the human flow from durable requirements through
architecture, Spec-driven implementation, operations, and historical recovery.
Authors, agents and reviewers consume it to choose the responsible document
owner. It guarantees one owner per kind of knowledge; stage numbers express
ownership and navigation rather than a one-way approval waterfall.

## Authority Boundary

This flow selects the responsible document stage. Exact paths, profile IDs,
frontmatter, sections, relationships, status classes, and lifecycle edges come
only from the Stage 99 registry (`docs/99.templates/registry.json`). Provider and
agent-roster authority is outside Stage 99 and is not defined here.

This document is the one `governance/contract` member because it owns an
invariant that other owners consume rather than a procedure: each change kind
sets a minimum record set, check set and authoring approval (the change-kind
table under Current Contract).

## Governance Context

Work begins with repository evidence and a testable Requirement Package or a
directly approved package-local work unit. Architecture Descriptions record
current structure; ADRs record durable choices. A Stage 03 work unit owns its
Spec, Plan, and independently reviewable Tasks. Stable operating knowledge
moves to Stage 05, and reusable evidence to Stage 90; Git history owns
historical recovery, and Stage 98 is unvalidated history.

The common flow is Clarify → Spec → Plan → Tasks → cross-artifact analysis →
Implement → Verify → promote durable meaning → Complete or retire. GitHub
Spec Kit informs that flow without replacing this repository's per-Task
records. Diátaxis informs Operations reader intent, C4 and arc42 inform
proportional Architecture Description views, ADR practice preserves decision
lineage, and Google SRE informs factual incidents and blameless postmortems.

## Current Contract

1. Establish the problem, acceptance boundary, and complete requirement IDs.
2. Record structural views and durable decisions before implementation when
   the change affects system boundaries or important trade-offs.
3. Review the Stage 03 Spec's change and acceptance contract and the Plan's
   intended order, risks and verification before dependent execution. Their
   approval establishes current authority, not an implementation result.
   Implement through Task records in that package. Changed executable behavior
   uses a focused failing case followed by a passing case; narrative changes
   use selected document checks. The Task Table owns execution state and
   result, Task Evidence owns factual checks, and one Criterion Acceptance
   table owns each criterion verdict.
4. Promote stable operator controls to Guide, Policy, or Runbook owners and
   preserve incident learning in Incident and Postmortem records.
5. Before a current document is deleted or moved, complete the manual
   consumer, preservation, hold and authority review in
   [document lifecycle](document-lifecycle.md#current-contract). A
   Git-history-only disposition also needs the exact recovery proof. Defer the
   affected disposition if any condition is unresolved. Replace or withdraw a
   Stage 01, 02 or 03 document by summarizing it in the owning current
   document's Archived Lineage table and deleting it; supersede
   or retire other documents only through registry-owned lifecycle edges and
   their reciprocal links.
6. Keep release procedure in a Runbook when one is needed, local execution
   evidence in Tasks and Git, the committed main `CHANGELOG.md` as release
   history, and tag, GitHub Release, hosted, provider or live evidence in its
   actually observed lane. Do not create a Release Record without a successor
   ADR, profile, lifecycle, template, and demonstrated audit consumer.

The terminal Stage 04 slot remains unused. This workspace carries no user
interface, so it has no design-system authority and no root design document; if
one is ever introduced it takes that authority and does not become a Stage 03
technical-design artifact.

### Ownership and placement

The meaning of each term below is owned by the
[Repository Vocabulary](../knowledge/glossary.md); this table owns only where
each artifact lives and the rules that govern it.

| Term | Owner and placement rule |
| --- | --- |
| Requirement | Stage 01. |
| Architecture Description / Architecture Decision Record | Stage 02. |
| Spec / Plan / Task | One Stage 03 package. Approval is not execution completion. |
| GitHub Issue / Project | Link to a Spec and Task by ID or URL; do not copy their full contract or evidence or synchronize status in both directions. Remote state requires observation. |
| Policy / rule / contract / control | Common behavior belongs to `.agents/governance/`, executable enforcement to scripts, document shape to Stage 99. These terms do not create parallel policy directories. The Stage 99 profile `governance/rule` names the shape those policy documents share, from the retired directory they once sat in; it is a stable identity rather than a claim that such a document carries one obligation. |
| Provider / Role / Agent | Native configuration is not evidence of runtime enforcement. |
| Skill | Lives under `.agents/skills/`; native discovery depends on the provider contract. A plain procedure reference is not a native registration. |
| Hook / Gate / validator / Fixture | A hook need not run QA, and a test fixture is never production policy input. |
| QA / CI / CD | This public repository runs repository-static QA locally. The hosted `ci-summary` job checks branch and commit metadata and `style-pr` runs only the selected style gate (plus the CI Python contract check when a lock changes); neither replays the rest of that QA. Argo CD reconciles declared GitOps state only under the operating boundary. |
| Deployment / release | Neither follows automatically from local validation or a commit. |
| Guide / Runbook | Stage 05. |
| Evidence / archive | Task and Git own change evidence; Git owns source recovery. Stage 98 is unvalidated history. |

### Proportional transitions

| Transition | Entry and output | Approval and evidence | Failure or rollback |
| --- | --- | --- | --- |
| Need to design | Requirement or direct scoped request; structural views or decision only when boundaries change | Request owner approves scope; design approval when required | Clarify an unresolved boundary before dependent implementation |
| Design to execution | Reviewed and approved change contract and ordered Plan; Task records work and checks | Reuse valid approval for the same scope; never infer approval from a checkbox or `ready` Task | Re-review affected authority when scope or evidence contradicts it; preserve unrelated work |
| Execution to handoff | Reviewed final bytes, resolved required checks, accepted criteria and Task handoff; scoped Git commit only when authorized | Local, index, hosted, provider, and live evidence remain distinct | Unresolved required checks block completion; missing external permission is DEFER |
| Handoff to operations or retention | Stable operating knowledge or terminal work record | Promote only durable meaning; apply the Stage 99 lifecycle contract; recover removed documents from Git history | Keep failures factual; use Git recovery rather than a second active owner |

### Change kinds

The kind of change sets the minimum records, checks and authoring approval.
A change that fits several rows takes the union. Push, pull request and merge
follow the [Git policy](git.md) for every row.

| Change kind | Minimum records | Checks | Authoring approval |
| --- | --- | --- | --- |
| Small correction: wording, link or typo | The current owner; no new package | Ordinary document selection in [quality](quality.md) | The operator's request |
| Document content: README, guide, reference | The current owner, or the Task of the package that changes it | Ordinary document selection | The operator's request |
| Executable behavior | A Stage 03 package; a failing case then a passing case in its Task | Focused regressions and affected purpose gates | Spec and Plan approval |
| Governance, provider, Stage 99 form, schema or registry | A Stage 03 package; durable meaning promoted to its owner | The contract-change selection in [quality](quality.md) | Spec and Plan approval |
| Architecture boundary or durable choice | An Architecture Description or ADR; a package when it is implemented | Document checks and forward links | The operator accepts the ADR |
| Live cluster change or incident fix | A Task, and an Incident record for an incident; Runbook steps | Observation in the approved live lane | The operator approves the live action; approved bootstrap and break-glass actions stay operator-bound under [approval and safety](approval-and-safety.md) |

Security checks follow their existing owners: [quality](quality.md) selects
the security unit regressions for continuing guarantees, and a reviewer who
finds secret exposure, RBAC risk or an isolation failure escalates to the
security auditor role. Operations learning that would change a need is
considered for an amended Requirement, which then follows that
Requirement's own review and approval.

A small correction reuses its current work owner and proportional checks. It
need not create a Requirement, ADR, or a new Spec package merely to edit a file.
An Issue can initiate work and a Project can display its progress without
becoming a second execution record; the active Task alone records actual work.

### Cross-artifact conformance

These rules apply to the Executable behavior and Governance, provider, Stage 99
rows, and to an Architecture row once it is implemented; a small correction or
document content change does not trigger them.

- Before a Spec leaves `draft`, its author reads the Requirement and the
  Architecture Descriptions and ADRs that own the affected boundary, and the
  Spec's Lifecycle Traceability `Architecture` column links the ones that
  constrain each criterion or states why none applies. The validator checks
  that the cell is present and non-empty; reviewers judge its content.
- An open question that changes an acceptance criterion keeps the Spec out of
  `approved`; a Plan is not approved against an unapproved Spec.
- A Spec or Plan that needs to depart from a current Architecture Description
  or ADR returns to `in-review` under the
  [lifecycle policy](document-lifecycle.md), and dependent work stops until a
  new or amended ADR is accepted or the departure is removed.
- When implementation and an approved Requirement, Architecture or Spec
  disagree, neither side is presumed correct. Record the divergence in the
  active Task, then either amend the owning document through its own review
  or correct the implementation. A requirement is never relaxed by editing a
  downstream document alone.

## Validation and Refresh

Run the registry, Markdown profile (`scripts/validate-markdown-profiles.py`),
link/owner, lifecycle (`scripts/validate-document-lifecycle.py`),
affected-surface, and repository quality gates selected by the changed paths. Treat repository
static results separately from hosted, provider-runtime, remote, or live
evidence. Review this flow when a stage, the change-kind table or the
lifecycle catalog in the Stage 99 registry changes.

## Related Documents

- [Common Agent Governance](../README.md)
- [Document Lifecycle Policy](document-lifecycle.md)
- [Document Authoring Policy](document-authoring.md)
- [Quality Policy](quality.md)
- [Git Policy](git.md)
- [Approval and Safety](approval-and-safety.md)
- Document Profile Registry (`docs/99.templates/registry.json`)
