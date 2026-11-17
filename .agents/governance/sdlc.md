---
title: "Software Development Lifecycle"
version: "4.1.2"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-11-17"
---

# Software Development Lifecycle

## Purpose and Scope

### Objective

This document owns the human flow from durable requirements through
architecture, Spec-driven implementation, operations, and historical recovery.
Authors, agents and reviewers consume it to choose the responsible document
owner. It guarantees one owner per kind of knowledge; stage numbers express
ownership and navigation rather than a one-way approval waterfall.

### Applies To

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

[Common Agent Governance](../README.md) is the common agent governance entry point.

#### Exclusions

Provider and agent-roster authority is excluded and stated under Owner; if another subject is excluded, name it and its owner here.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| SDLC-R001 | Always | Establish the problem, acceptance boundary, and complete requirement IDs. | Semantic review | none |
| SDLC-R002 | When the change affects system boundaries or important trade-offs | Record structural views and durable decisions before implementation when the change affects system boundaries or important trade-offs. | Semantic review | none |
| SDLC-R003 | Before dependent execution | Review the Stage 03 Spec's change and acceptance contract and the Plan's intended order, risks and verification before dependent execution. Their approval establishes current authority, not an implementation result. Implement through Task records in that package. Changed executable behavior uses a focused failing case followed by a passing case; narrative changes use selected document checks. The Task's Lifecycle Traceability table owns execution state and result, its Results table owns factual checks, and one Criterion Decisions table owns each criterion verdict. | `document-lifecycle` | none |
| SDLC-R004 | Always | Promote stable operator controls to Guide, Policy, or Runbook owners and preserve incident learning in Incident and Postmortem records. | Semantic review | none |
| SDLC-R005 | Before a current document is deleted or moved | Before a current document is deleted or moved, complete the manual consumer, preservation, hold and authority review in [document lifecycle](document-lifecycle.md#requirements). A Git-history-only disposition also needs the exact recovery proof. Defer the affected disposition if any condition is unresolved. Replace or withdraw a Stage 01, 02 or 03 document by summarizing it in the owning current document's Archived Lineage table and deleting it; supersede or retire other documents only through registry-owned lifecycle edges and their reciprocal links. | Semantic review | none |
| SDLC-R006 | Always | Keep release procedure in a Runbook when one is needed, local execution evidence in Tasks and Git, the committed main `CHANGELOG.md` as release history, and tag, GitHub Release, hosted, provider or live evidence in its actually observed lane. Use these owners for all release documentation. | Semantic review | none |
| SDLC-R007 | Always | The terminal Stage 04 slot remains unused. This workspace carries no user interface, so it has no design-system authority and no root design document; if one is ever introduced it takes that authority and does not become a Stage 03 technical-design artifact. | Semantic review | none |
| SDLC-R008 | Always | Requirement | `markdown-profiles` | none |
| SDLC-R009 | Always | Architecture Description / Architecture Decision Record | `markdown-profiles` | none |
| SDLC-R010 | Always | Spec / Plan / Task | `document-lifecycle` | none |
| SDLC-R011 | Always | GitHub Issue / Project | Semantic review | none |
| SDLC-R012 | Always | Policy / rule / contract / control | `document-contract-registry` | none |
| SDLC-R013 | Always | Provider / Role / Agent | `agent-governance` | none |
| SDLC-R014 | Always | Skill | `agent-governance` | none |
| SDLC-R015 | Always | Hook / Gate / validator / Fixture | Semantic review | none |
| SDLC-R016 | Always | QA / CI / CD | `ci-python-contract` | none |
| SDLC-R017 | Always | Deployment / release | Semantic review | none |
| SDLC-R018 | Always | Guide / Runbook | `markdown-profiles` | none |
| SDLC-R019 | Always | Evidence / archive | Semantic review | none |
| SDLC-R020 | At the Need to design transition | Need to design | Semantic review | none |
| SDLC-R021 | At the Design to execution transition | Design to execution | `document-lifecycle` | none |
| SDLC-R022 | At the Execution to handoff transition | Execution to handoff | `document-lifecycle` | none |
| SDLC-R023 | At the Handoff to operations or retention transition | Handoff to operations or retention | `document-lifecycle` | none |
| SDLC-R024 | Always | The kind of change sets the minimum records, checks and authoring approval. A change that fits several rows takes the union. Push, pull request and merge follow the [Git policy](git.md) for every row. | Semantic review | none |
| SDLC-R025 | For a small correction | Small correction: wording, link or typo | `document-contract-tests` | none |
| SDLC-R026 | For a document content change | Document content: README, guide, reference | `document-contract-tests` | none |
| SDLC-R027 | For an executable behavior change | Executable behavior | Semantic review | none |
| SDLC-R028 | For a governance, provider, Stage 99 form, schema or registry change | Governance, provider, Stage 99 form, schema or registry | `document-lifecycle` | none |
| SDLC-R029 | For an architecture boundary or durable choice | Architecture boundary or durable choice | Semantic review | none |
| SDLC-R030 | For a live cluster change or incident fix | Live cluster change or incident fix | Semantic review | none |
| SDLC-R031 | Before a Spec leaves draft | Before a Spec leaves `draft`, its author reads the Requirement and the Architecture Descriptions and ADRs that own the affected boundary, and the Spec's Lifecycle Traceability `Architecture` column links the ones that constrain each criterion or states why none applies. The validator checks that the cell is present and non-empty; reviewers judge its content. | `markdown-profiles` | none |
| SDLC-R032 | When an open question changes an acceptance criterion | An open question that changes an acceptance criterion keeps the Spec out of `approved`; a Plan is not approved against an unapproved Spec. | Semantic review | none |
| SDLC-R033 | When a Spec or Plan needs to depart from a current Architecture Description or ADR | A Spec or Plan that needs to depart from a current Architecture Description or ADR returns to `in-review` under the [lifecycle policy](document-lifecycle.md), and dependent work stops until a new or amended ADR is accepted or the departure is removed. | `document-lifecycle` | none |
| SDLC-R034 | When implementation and an approved Requirement, Architecture or Spec disagree | When implementation and an approved Requirement, Architecture or Spec disagree, resolve in the order current user requirement, approved contract, implementation and tests. Record the divergence in the active Task, then either amend the owning document through its own review or correct the implementation, changing producer, reader, schema, current guidance and tests in one change set. An unapproved test expectation never becomes policy, a test is never edited alone to make a violation pass, and a requirement is never relaxed by editing a downstream document alone. This order never authorizes a protected action: [approval and safety](approval-and-safety.md) still binds, and no package or agent message counts as user approval. | Semantic review | none |
| SDLC-R035 | Always | Three separate axes describe where work stands, and one never implies another. The document STAGE (Stage 01 to 99) names the owner and place of a document. The SDLC phase (Clarify to Complete above) names the work step. The Git point names before, during or after commit, push, pull request or merge. Status, acceptance, promotion and exit per document role follow the [lifecycle policy](document-lifecycle.md). | Semantic review | none |

| Rule ID | Level | Status |
| --- | --- | --- |
| SDLC-R001 | required | active |
| SDLC-R002 | required | active |
| SDLC-R003 | required | active |
| SDLC-R004 | required | active |
| SDLC-R005 | required | active |
| SDLC-R006 | required | active |
| SDLC-R007 | required | active |
| SDLC-R008 | required | active |
| SDLC-R009 | required | active |
| SDLC-R010 | required | active |
| SDLC-R011 | required | active |
| SDLC-R012 | required | active |
| SDLC-R013 | required | active |
| SDLC-R014 | required | active |
| SDLC-R015 | required | active |
| SDLC-R016 | required | active |
| SDLC-R017 | required | active |
| SDLC-R018 | required | active |
| SDLC-R019 | required | active |
| SDLC-R020 | required | active |
| SDLC-R021 | required | active |
| SDLC-R022 | required | active |
| SDLC-R023 | required | active |
| SDLC-R024 | required | active |
| SDLC-R025 | required | active |
| SDLC-R026 | required | active |
| SDLC-R027 | required | active |
| SDLC-R028 | required | active |
| SDLC-R029 | required | active |
| SDLC-R030 | required | active |
| SDLC-R031 | required | active |
| SDLC-R032 | required | active |
| SDLC-R033 | required | active |
| SDLC-R034 | required | active |
| SDLC-R035 | required | active |

#### Stage 04 slot

`SDLC-R007`

#### Ownership and placement

The meaning of each term below is owned by the
[Repository Vocabulary](../knowledge/glossary.md); this table owns only where
each artifact lives and the rules that govern it.

| Rule ID | Owner and placement rule |
| --- | --- |
| SDLC-R008 | Stage 01. |
| SDLC-R009 | Stage 02. |
| SDLC-R010 | One Stage 03 package. Approval is not execution completion. |
| SDLC-R011 | Link to a Spec and Task by ID or URL; do not copy their full contract or evidence or synchronize status in both directions. Remote state requires observation. |
| SDLC-R012 | Common behavior belongs to `.agents/governance/`, executable enforcement to scripts, document shape to Stage 99. These terms do not create parallel policy directories. The Stage 99 profile `governance/rule` names the shape those policy documents share, from the retired directory they once sat in; it is a stable identity rather than a claim that such a document carries one obligation. Policy is one document role with one common form, placed as `governance/rule` under `.agents/governance/` or `operation/policy` in Stage 05; a Rule is a normative unit with a stable ID inside a Policy, not a document role. |
| SDLC-R013 | Native configuration is not evidence of runtime enforcement. |
| SDLC-R014 | Lives under `.agents/skills/`; native discovery depends on the provider contract. A plain procedure reference is not a native registration. |
| SDLC-R015 | A hook need not run QA, and a test fixture is never production policy input. |
| SDLC-R016 | This public repository runs repository-static QA locally. The hosted `ci-summary` job checks branch and commit metadata. `style-pr` runs the selected style gate, the CI Python contract check when a lock changes, and the static GitOps identity check when GitOps data changes; its adoption awaits ADR-0063 acceptance. Neither job replays the rest of that QA. Argo CD reconciles declared GitOps state only under the operating boundary. |
| SDLC-R017 | Neither follows automatically from local validation or a commit. |
| SDLC-R018 | Stage 05. |
| SDLC-R019 | Task and Git own change evidence; Git owns source recovery. Stage 98 is unvalidated history. |

#### Proportional transitions

| Rule ID | Entry and output | Approval and evidence | Failure or rollback |
| --- | --- | --- | --- |
| SDLC-R020 | Requirement or direct scoped request; structural views or decision only when boundaries change | Request owner approves scope; design approval when required | Clarify an unresolved boundary before dependent implementation |
| SDLC-R021 | Current approved change contract and ordered Plan, or separately verified scoped user authorization; Task records work and checks | Bind approval to the reviewed inputs and current request revision; draft authoring and focused document checks remain within writing scope | Re-review affected authority when scope or evidence contradicts it; preserve unrelated work |
| SDLC-R022 | Reviewed final bytes, resolved required checks, accepted criteria and Task handoff; scoped Git commit only when authorized | Local, index, hosted, provider, and live evidence remain distinct | Unresolved required checks block completion; missing external permission is DEFER |
| SDLC-R023 | Stable operating knowledge or terminal work record | Promote only durable meaning; apply the Stage 99 lifecycle contract; recover removed documents from Git history | Keep failures factual; use Git recovery rather than a second active owner |

#### Change kinds

`SDLC-R024`

| Rule ID | Minimum records | Checks | Authoring approval |
| --- | --- | --- | --- |
| SDLC-R025 | The current owner; no new package | Ordinary document selection in [quality](quality.md) | The operator's request |
| SDLC-R026 | The current owner, or the Task of the package that changes it | Ordinary document selection | The operator's request |
| SDLC-R027 | A Stage 03 package; a failing case then a passing case in its Task | Focused regressions and affected purpose gates | Spec and Plan approval |
| SDLC-R028 | A Stage 03 package; durable meaning promoted to its owner | The contract-change selection in [quality](quality.md) | Spec and Plan approval |
| SDLC-R029 | An Architecture Description or ADR; a package when it is implemented | Document checks and forward links | The operator approves the ADR, whose status becomes `accepted` |
| SDLC-R030 | A Task, and an Incident record for an incident; Runbook steps | Observation in the approved live lane | The operator approves the live action; approved bootstrap and break-glass actions stay operator-bound under [approval and safety](approval-and-safety.md) |

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

#### Cross-artifact conformance

These rules apply to the Executable behavior and Governance, provider, Stage 99
rows, and to an Architecture row once it is implemented; a small correction or
document content change does not trigger them.

#### Three axes

`SDLC-R035`

### Exceptions

This policy defines no exception condition of its own; exceptions follow the approval and safety policy's operator approval route. If this policy needs its own, state it here.

#### Approval and Review

This policy defines no exception approval or review step of its own; the approval and safety policy's operator approval route applies. If it needs its own, state it here.

## Enforcement

### Mechanisms

Run the registry, Markdown profile (`scripts/validate-markdown-profiles.py`),
link/owner, lifecycle (`scripts/validate-document-lifecycle.py`),
affected-surface, and repository quality gates selected by the changed paths. Treat repository
static results separately from hosted, provider-runtime, remote, or live
evidence. Review this flow when a stage, the change-kind table or the
lifecycle catalog in the Stage 99 registry changes.

The checks are owned by the [Quality Policy](quality.md), the [Git Policy](git.md) and the Document Profile Registry (docs/99.templates/registry.json).

### Limits

Repository static results are kept separate from hosted, provider-runtime, remote or live evidence. Native provider configuration is not evidence of runtime enforcement (SDLC-R013), and remote GitHub Issue or Project state requires observation rather than being inferred (SDLC-R011).

## Ownership

### Owner

This flow selects the responsible document stage. Exact paths, profile IDs,
frontmatter, sections, relationships, status classes, and lifecycle edges come
only from the Stage 99 registry (`docs/99.templates/registry.json`). Provider and
agent-roster authority is outside Stage 99 and is not defined here.

This document is a Policy on the `governance/rule` profile because it owns an
invariant that other owners consume rather than a procedure: each change kind
sets a minimum record set, check set and authoring approval (the change-kind
table under Requirements).

- [Document Lifecycle Policy](document-lifecycle.md)
- [Document Authoring Policy](document-authoring.md)
- [Approval and Safety](approval-and-safety.md)

#### Responsibilities

The [Ownership and placement](#ownership-and-placement) table states the owner and placement rule of each artifact.

### Review Triggers

This policy changes as a governed-document change under the work lifecycle and the document lifecycle policy, with no adoption step of its own; if it needs one, state it here.
