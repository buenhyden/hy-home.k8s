---
title: 'Documentation Architecture and SDLC Document Roles Reference'
type: content/reference
status: active
owner: platform
updated: 2026-08-07
---

# Documentation Architecture and SDLC Document Roles Reference

## Overview

This reference records two things that this repository previously kept
implicit. First, the Diátaxis documentation architecture: four user needs,
four corresponding documentation forms, the two axes that separate them, and
the compass that decides which form a piece of content belongs to. Second, the
role, purpose, prohibition, structure, and lifecycle rule of each SDLC document
type this repository routes, checked against primary sources on 2026-08-07 and
against the repository's own registry.

Diátaxis text was previously unavailable to this repository's research: the
published site returned HTTP 429 on every attempt on 2026-08-07. The quotations
below come instead from the framework's own reStructuredText sources on its
public authoring repository, fetched on 2026-08-07. That is a primary source
authored by the framework maintainer, not a secondary summary.

This is descriptive Stage 90 reference material. It does not change template
routing, frontmatter schema, status domains, stage ownership, or any validator.
Those remain with their canonical Stage 00 and Stage 99 owners.

### Purpose

- Record a source-backed statement of the Diátaxis map, compass, and quality
  distinction that later documentation work can cite.
- Record the purpose, exclusion, structure, and lifecycle rule of each SDLC
  document type from a primary source where one exists, and say plainly where
  none exists.
- Map Diátaxis modes onto this repository's actual routed document types and
  observed document counts, and name where the mapping is incomplete.
- Route every identified gap to the repository path that owns it, without
  making the change from this reference.

## Reference Type

- Type: durable-concept / external-standard-snapshot
- Source checked: `2026-08-07`
- Refresh trigger: Diátaxis framework revision; a change to
  `docs/99.templates/support/document-profiles.json` document-type routes,
  status domains, or heading contracts; a change to
  `docs/00.agent-governance/rules/stage-authoring-matrix.md`; or the first
  authored instance of a currently unused document type.

## Authority Boundary

- **Authoritative for**:
  - Source-attributed Diátaxis definitions checked on 2026-08-07, including the
    retrieval route used and the failure of the published site on that date.
  - Dated primary-source findings for ADR, incident, postmortem, runbook,
    changelog, and versioning document types.
  - The observed repository document-type inventory and counts recorded below.
  - The descriptive Diátaxis-to-repository mapping and the gap routing.
- **Not authoritative for**:
  - Template routing, profile identifiers, heading contracts, status domains,
    frontmatter schema, or validator behavior. Those belong to
    `docs/99.templates/support/` and `docs/00.agent-governance/`.
  - Any claim that this repository conforms to ISO/IEC/IEEE 42010 or
    ISO/IEC/IEEE 29148. Both catalog pages were unreachable or paywalled on
    2026-08-07 and their normative text was not observed.
  - Any decision to add, retire, or merge a document type. That is a
    documentation-owner decision, not a research output.
  - Live cluster, provider runtime, hosted CI, or remote evidence.

## Scope

### In Scope

- Diátaxis four modes, two axes, map table, compass table, and the functional
  versus deep quality distinction.
- Primary-source role and structure findings for PRD, ARD, ADR, guide, policy,
  runbook, incident, postmortem, and release documentation.
- The repository's routed document types, their status domains, and observed
  authored counts as of 2026-08-07.
- Gap identification with an owning repository path per gap.

### Out of Scope

- Changing any template, profile, route, status domain, or validator.
- Authoring any missing document type or creating any new stage folder.
- Quoting paywalled standard text that was not observed.
- Live, provider-runtime, hosted-CI, or remote verification.

## Definitions / Facts

### Diátaxis: Four Forms, Two Axes

Diátaxis "identifies four distinct needs, and four corresponding forms of
documentation - _tutorials_, _how-to guides_, _technical reference_ and
_explanation_. It places them in a systematic relationship, and proposes that
documentation should itself be organised around the structures of those needs."
It "solves problems related to documentation _content_ (what to write), _style_
(how to write it) and _architecture_ (how to organise it)."

The framework describes "a **two-dimensional structure**, rather than a _list_",
and states that a scheme must answer "how to arrange documentation _in general?_"
rather than mirroring product features.

The map table, quoted from the framework source:

| Aspect               | Tutorials                        | How-to guides                     | Reference                                | Explanation                           |
| -------------------- | -------------------------------- | --------------------------------- | ---------------------------------------- | ------------------------------------- |
| what they do         | introduce, educate, lead         | guide                             | state, describe, inform                  | explain, clarify, discuss             |
| answers the question | "Can you teach me to...?"        | "How do I...?"                    | "What is...?"                            | "Why...?"                             |
| oriented to          | learning                         | goals                             | information                              | understanding                         |
| purpose              | to provide a learning experience | to help achieve a particular goal | to describe the machinery                | to illuminate a topic                 |
| form                 | a lesson                         | a series of steps                 | dry description                          | discursive explanation                |
| analogy              | teaching a child how to cook     | a recipe in a cookery book        | information on the back of a food packet | an article on culinary social history |

The compass reduces the placement decision to two questions: "_action or
cognition?_ _acquisition or application?_" The framework defines the terms
flexibly as "_action_: practical steps, doing", "_cognition_: theoretical or
propositional knowledge, thinking", "_acquisition_: study", and
"_application_: work".

| If the content... | ...and serves the user's... | ...then it must belong to... |
| ----------------- | --------------------------- | ---------------------------- |
| informs action    | acquisition of skill        | a tutorial                   |
| informs action    | application of skill        | a how-to guide               |
| informs cognition | application of skill        | reference                    |
| informs cognition | acquisition of skill        | explanation                  |

Diátaxis names a failure mode it calls blur: "there is a kind of natural
affinity between each of the different forms of documentation and its
neighbours on the map, and a natural tendency to blur the distinctions". It
warns that "In the worst case there is a complete or partial collapse of
tutorials and how-to guides into each other, making it impossible to meet the
needs served by either."

Diátaxis separates **functional quality** from **deep quality**. Functional
quality is "_accuracy_, _completeness_, _consistency_, _usefulness_,
_precision_ and so on", and the framework states these "are all independent of
each other" and that documentation "can be accurate, complete, consistent and
also useless". Diátaxis addresses deep quality; it does not supply the
accuracy, completeness, and consistency controls that a governed repository
still needs from validators and review.

The framework also states its own lightness: "It doesn't impose implementation
constraints." Diátaxis therefore prescribes no status values, no ownership
model, no traceability requirement, and no lifecycle. Every such rule in this
repository is a local addition and must be sourced locally.

### SDLC Document Types

Source labels: `[S]` stated by the cited primary source, `[W]` a workspace rule
observed in this repository, `[I]` inference recorded as inference.

| Type          | Purpose                                                                                                                                                                                       | Must not                                                                                                                                                                  | Required structure                                                                                                                                                                                                 | Lifecycle rule                                                                                                                                                           | Primary source (checked 2026-08-07)                                                                                                                 |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| PRD           | Capture problem, stakeholders, scope, verifiable requirements, acceptance criteria `[W]`                                                                                                      | Carry architecture or task procedure `[W]`; reproduce paywalled standard text `[W]`                                                                                       | Overview, Vision, Problem Statement, Personas, Key Use Cases, Functional Requirements, Success and Acceptance Criteria, Scope and Non-goals, Risks, Traceability `[W]`                                             | `draft -> active -> done -> archived` `[W]`                                                                                                                              | None. "PRD" is industry practice, not a standardised artifact. The nearest formal standard is ISO/IEC/IEEE 29148:2018, whose text was not observed. |
| ARD           | Record stakeholders, concerns, boundaries, viewpoints, quality attributes, and keep architecture description separate from implementation `[W]`                                               | Claim ISO/IEC/IEEE 42010 conformance `[W]`; become a decision log `[I]`                                                                                                   | Overview, Boundaries and Non-goals, Quality Attributes, System Overview and Context, Data Architecture, Infrastructure and Deployment, Traceability `[W]`                                                          | `draft -> active -> accepted -> archived` `[W]`                                                                                                                          | ISO/IEC/IEEE 42010 catalog page returned HTTP 403 on 2026-08-07; normative text not observed.                                                       |
| ADR           | Record one architecturally significant decision with rationale, trade-offs, and consequences `[S]`                                                                                            | List only positive consequences `[S]`; be deleted or rewritten when reversed `[S]`; expand into a full architecture description `[W]`                                     | Title, Status, Context, Decision, Consequences `[S]`                                                                                                                                                               | Append-only; "If a decision is reversed, we will keep the old one around, but mark it as superseded" `[S]`; local domain `draft -> active -> accepted -> archived` `[W]` | <https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions>, <https://adr.github.io/>                                            |
| Guide         | Serve a reader outcome; Diátaxis separates the guided lesson from the goal-oriented recipe `[S]`                                                                                              | Write a how-to as a lesson or a tutorial as a recipe `[S]`; duplicate reference or policy detail `[W]`                                                                    | Overview, Guide Type, Target Audience, Prerequisites, Step-by-step Instructions, Common Pitfalls, Traceability `[W]`                                                                                               | `draft -> active -> accepted -> archived` `[W]`                                                                                                                          | Diátaxis sources, fetched 2026-08-07                                                                                                                |
| Policy        | State objectives and constraints, addressing "what" and "why" in technology-independent terms `[S]`                                                                                           | Contain executable procedure, which belongs in a runbook `[W]`                                                                                                            | Overview, Policy Scope, Applies To, Controls, Exceptions, Verification, Review Cadence, Traceability `[W]`                                                                                                         | `draft -> active -> accepted -> archived` `[W]`                                                                                                                          | <https://csrc.nist.gov/glossary/term/security_policy> (NIST SP 800-82r3 framing)                                                                    |
| Runbook       | Give "high-level instructions on how to respond to automated alerts", including severity, impact, debugging suggestions, and mitigation actions `[S]`                                         | Be "a deterministic list of commands that the on-call engineer runs every time a particular alert fires" — automate that instead `[S]`; merge policy into procedure `[W]` | Overview, Runbook Type, When to Use, Procedure or Checklist, Verification Steps, Observability and Evidence Sources, Safe Rollback or Recovery Procedure, Traceability `[W]`                                       | `draft -> active -> accepted -> archived` `[W]`; the source warns details "go out of date at the same rate as production environment changes" `[S]`                      | <https://sre.google/workbook/on-call/>                                                                                                              |
| Incident      | Maintain a living, multi-editable record during response that "proves invaluable for later postmortem analysis" `[S]`                                                                         | Contain speculative root cause `[W]`; delay declaration `[S]`                                                                                                             | Overview, Incident Metadata, Impact, Timeline, Response State, Evidence, Follow-up Actions, Traceability `[W]`; roles Incident Commander, Operations lead, Communication lead `[S]`                                | Declare early; the source names customer-visible outage, needing a second team, or one hour unresolved `[S]`                                                             | <https://sre.google/sre-book/managing-incidents/>, <https://sre.google/workbook/incident-response/>                                                 |
| Postmortem    | Produce "a written record of an incident, its impact, the actions taken to mitigate or resolve it, the root cause(s), and the follow-up actions to prevent the incident from recurring" `[S]` | Indict any individual or team `[S]`; omit contributing causes `[S]`                                                                                                       | Overview, Incident Link and Impact Summary, Root Cause Analysis, Contributing Factors, What Went Well, What Went Wrong, Action Items, Prevention and Verification, Documentation Feedback Loop, Traceability `[W]` | Triggers defined in advance; senior review, then broader sharing `[S]`                                                                                                   | <https://sre.google/sre-book/postmortem-culture/>                                                                                                   |
| Release notes | Provide "a curated, chronologically ordered list of notable changes for each version" written "_for humans_, not machines" `[S]`                                                              | Be a commit-log dump `[S]`; hide deprecations `[S]`; be partial `[S]`                                                                                                     | Per-version section, ISO 8601 date, grouped Added, Changed, Deprecated, Removed, Fixed, Security `[S]`                                                                                                             | Released versions are immutable; "Any modifications MUST be released as a new version" `[S]`                                                                             | <https://keepachangelog.com/en/1.1.0/>, <https://semver.org/>                                                                                       |

### Repository Document-Type Inventory

Observed on 2026-08-07 from `docs/99.templates/support/document-profiles.json`
(schemaVersion 8) and from frontmatter `type:` values across `docs/`, excluding
templates.

| Routed type         | Status domain                     | Authored count | Example path                                                                          |
| ------------------- | --------------------------------- | -------------- | ------------------------------------------------------------------------------------- |
| `sdlc/prd`          | draft, active, done, archived     | 7              | `docs/01.requirements/004-current-local-gitops-platform.md`                           |
| `sdlc/ard`          | draft, active, accepted, archived | 7              | `docs/02.architecture/requirements/0010-repository-delivery-evidence-architecture.md` |
| `sdlc/adr`          | draft, active, accepted, archived | 16             | `docs/02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md` |
| `sdlc/spec`         | draft, active, done, archived     | 47             | `docs/03.specs/046-agent-governance-program-closure/spec.md`                          |
| `sdlc/agent-design` | draft, active, done, archived     | 2              | `docs/03.specs/024-observability-and-network-review-agents/agent-design.md`           |
| `sdlc/api-spec`     | draft, active, done, archived     | 0              | none authored                                                                         |
| `sdlc/data-model`   | draft, active, done, archived     | 0              | none authored                                                                         |
| `sdlc/tests`        | draft, active, done, archived     | 0              | none authored                                                                         |
| `sdlc/plan`         | draft, active, done, archived     | 63             | `docs/04.execution/plans/2026-08-02-repository-assurance-integration-and-closure.md`  |
| `sdlc/task`         | draft, active, done, archived     | 65             | `docs/04.execution/tasks/2026-08-02-example-iac-and-validator-qa.md`                  |
| `sdlc/guide`        | draft, active, accepted, archived | 8              | `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md`                          |
| `sdlc/policy`       | draft, active, accepted, archived | 7              | `docs/05.operations/policies/0001-k8s-gitops-operations-policy.md`                    |
| `sdlc/runbook`      | draft, active, accepted, archived | 9              | `docs/05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md`               |
| `sdlc/incident`     | draft, active, accepted, archived | 0              | `docs/05.operations/incidents/` holds only `README.md`                                |
| `sdlc/postmortem`   | draft, active, accepted, archived | 0              | none authored                                                                         |
| release notes       | not routed                        | 0              | no profile exists                                                                     |

Every one of the 8 authored guides declares the same `## Guide Type` value,
`how-to`, although `docs/99.templates/templates/sdlc/operations/guide.template.md`
offers how-to, tutorial, or concept. The registry enforces the heading, not the
value.

### Diátaxis-to-Repository Mapping

| Diátaxis mode          | Compass position        | Repository owner                                                                                                                                 | Evidence                                                                                         | Assessment                                                                                                                                                                                                                     |
| ---------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Tutorial               | action + acquisition    | `sdlc/guide` with `Guide Type: tutorial`                                                                                                         | 0 of 8 guides use it                                                                             | Unoccupied. Learning material sits in `docs/90.references/learning/infrastructure-to-theory-roadmap.md`, which is routed as reference.                                                                                         |
| How-to guide           | action + application    | `sdlc/guide` (`how-to`) and `sdlc/runbook`                                                                                                       | 8 guides, 9 runbooks                                                                             | Occupied twice. The two profiles are separated by executability and rollback, not by Diátaxis, and at least two title-level near-duplicate pairs exist across `docs/05.operations/guides/` and `docs/05.operations/runbooks/`. |
| Reference              | cognition + application | `content/reference`, `governance/reference`, `governance/template-support`, native contract exceptions                                           | About 38 documents under `docs/90.references/**`                                                 | Occupied, but mixed. Stage 90 also holds dated audit and research narratives, which are closer to explanation than to reference.                                                                                               |
| Explanation            | cognition + acquisition | No routed type                                                                                                                                   | ADR `Context` and `Consequences`; ARD `Quality Attributes`; reference sub-type `durable-concept` | Unoccupied as a routed type. Explanation is absorbed into decision records and reference sub-types.                                                                                                                            |
| Not a Diátaxis concern | —                       | `sdlc/prd`, `sdlc/ard`, `sdlc/adr`, `sdlc/spec`, `sdlc/plan`, `sdlc/task`, `sdlc/incident`, `sdlc/postmortem`, `content/archive`, `governance/*` | Stages 01 through 04, Stage 98                                                                   | Correct by design. Diátaxis addresses documentation that serves a user's learning or work; it says nothing about lifecycle and evidence artifacts. Forcing these into four quadrants would be a category error.                |

### Gap Routing

| ID      | Gap                                                                                                                                                                                               | Owning path                                                                                                                                    |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| DOC-G1  | `Guide Type` is free text with no enum; all 8 guides say `how-to`, and one is titled "reference guide"                                                                                            | `docs/99.templates/support/document-profiles.json`, `docs/99.templates/templates/sdlc/operations/guide.template.md`                            |
| DOC-G2  | No tutorial-mode route exists; learning material is routed as Stage 90 reference                                                                                                                  | `docs/99.templates/support/sdlc-governance.md`, `docs/00.agent-governance/rules/stage-authoring-matrix.md`                                     |
| DOC-G3  | No explanation-mode route exists; explanation is implicit inside ADR, ARD, and reference sub-types                                                                                                | `docs/99.templates/support/common-documentation-governance.md`                                                                                 |
| DOC-G4  | The guide-versus-runbook boundary is prose-only, and the active-surface duplicate rule covers stages 01 through 04 only, so Stage 05 near-duplicates are not caught                               | `docs/99.templates/support/sdlc-governance.md`                                                                                                 |
| DOC-G5  | No release-notes or changelog document type exists, and the decision not to have one is undocumented                                                                                              | `docs/99.templates/support/document-profiles.json`, `docs/90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md` |
| DOC-G6  | Incident and postmortem contracts have zero authored instances, and no observable postmortem trigger threshold is defined, although the primary source requires triggers to be defined in advance | `docs/05.operations/incidents/README.md`, `docs/05.operations/policies/`                                                                       |
| DOC-G7  | `sdlc/api-spec`, `sdlc/data-model`, and `sdlc/tests` have full profiles, templates, and heading contracts but zero authored instances                                                             | `docs/99.templates/support/sdlc-governance.md`                                                                                                 |
| DOC-G8  | The ARD row of the format ledger cites ISO/IEC/IEEE 42010 without an observed-text boundary; the catalog page returned HTTP 403 on 2026-08-07                                                     | `docs/90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md`                                                     |
| DOC-G9  | The PRD row presents ISO/IEC/IEEE 29148 as grounding a form that no standard defines; the mapping is an unlabelled inference                                                                      | `docs/90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md`                                                     |
| DOC-G10 | The runbook contract requires a procedure section but records no counter-rule for the automation anti-pattern the primary source states                                                           | `docs/99.templates/templates/sdlc/operations/runbook.template.md`                                                                              |

## Sources

- Diátaxis framework source, `source/index.rst`, `source/map.rst`,
  `source/compass.rst`, `source/quality.rst`, retrieved from
  <https://github.com/evildmp/diataxis-documentation-framework> on 2026-08-07.
  Adopted: the four forms, the map table, the compass table, the blur failure
  mode, and the functional-versus-deep-quality distinction. Rejected: any
  lifecycle, status, ownership, or traceability rule; Diátaxis states it "doesn't
  impose implementation constraints".
- <https://diataxis.fr/> — returned HTTP 429 Too Many Requests on 2026-08-07 on
  every attempt, including `/start-here/`. Recorded as unreachable; the
  authoring repository above was used instead.
- <https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions>
  checked 2026-08-07. Adopted: ADR sections, status values, and the
  supersede-not-delete rule. Rejected: file naming, tooling, review workflow.
- <https://adr.github.io/> checked 2026-08-07. Adopted: the architecturally
  significant requirement and decision-log definitions. Rejected: any single
  normative ADR template.
- <https://sre.google/sre-book/postmortem-culture/> checked 2026-08-07.
  Adopted: the postmortem definition, blameless framing, and the
  triggers-defined-in-advance rule. Rejected: any heading contract.
- <https://sre.google/sre-book/managing-incidents/> and
  <https://sre.google/workbook/incident-response/> checked 2026-08-07.
  Adopted: incident roles and the living-document practice. Rejected: severity
  taxonomies and file formats.
- <https://sre.google/workbook/on-call/> checked 2026-08-07. Adopted: the
  playbook definition, the staleness warning, and the automation anti-pattern.
  Rejected: any runbook heading contract.
- <https://keepachangelog.com/en/1.1.0/> and <https://semver.org/> checked
  2026-08-07. Adopted: changelog purpose, the six change types, and release
  immutability. Rejected: applicability to a repository that declares no public
  API.
- <https://csrc.nist.gov/glossary/term/security_policy> checked 2026-08-07.
  Adopted: the technology-independent "what and why" policy framing. Rejected:
  any policy heading set.
- <https://www.iso.org/standard/74393.html> returned HTTP 403 on 2026-08-07 and
  <https://www.iso.org/standard/72089.html> is paywalled. Neither normative text
  was observed; no conformance claim is made from either.
- Repository evidence observed 2026-08-07:
  `docs/99.templates/support/document-profiles.json`,
  `docs/99.templates/support/sdlc-governance.md`,
  `docs/99.templates/support/common-documentation-governance.md`,
  `docs/00.agent-governance/rules/stage-authoring-matrix.md`, and the authored
  document sets under `docs/01.requirements/` through `docs/05.operations/`.

## Review and Freshness

- Review when the Diátaxis framework publishes a revision, when
  `document-profiles.json` changes a document-type route, status domain, or
  heading contract, or when a currently unused type gains its first instance.
- The counts in this reference are a dated observation. They drift with every
  authored document and must be re-observed rather than reused.
- Current truth for routing and enforcement stays with
  `docs/99.templates/support/` and `docs/00.agent-governance/`. Nothing here
  overrides them.
- ISO/IEC/IEEE 42010 and 29148 remain unobserved. Any future conformance claim
  requires observed normative text, not this reference.

## Related Documents

- [Research Pack Index](README.md)
- [Document Type Format and Evidence Contract](../research/2026-07-07-wer/document-type-format-and-evidence-contract.md)
- [Spec, SDLC, CI, QA, and Formatting Reference](../research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md)
- [Stage Authoring Matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [SDLC Governance](../../99.templates/support/sdlc-governance.md)
