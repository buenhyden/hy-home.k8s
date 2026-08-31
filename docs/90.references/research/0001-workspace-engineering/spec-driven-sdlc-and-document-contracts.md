---
title: 'Reference: Spec-Driven SDLC and Document Contracts'
type: content/reference
status: active
owner: platform
updated: 2026-08-31
---

# Reference: Spec-Driven SDLC and Document Contracts

## Overview

This dated research reference maps a specification-led SDLC to the workspace's
typed document contracts. It separates external guidance from the repository's
actual authority: a current source can support a bounded practice claim, while
only a local profile, template, registry, and validator establish a local
document contract.

## Reference Type

Source-backed Stage 90 analysis; it is not a new lifecycle policy, release
approval, security control, or evidence of production operation.

## Authority Boundary

`docs/99.templates/registry.json` and its schema own typed
routes, frontmatter, status domains, required headings, templates, and
traceability relations. Stage routing and the stage-authoring matrix own human
timing and persona routing. This reference analyses those controls but cannot
change them or infer CI, approval, incident handling, deployment, or SSDF/ISO
conformance from their existence.

## Scope

It covers REQ-WERPC-007 and REQ-WERPC-010 through REQ-WERPC-019: SDD, the SDLC
state/authority/evidence chain, and PRD, ARD, ADR, Guide, Incident, Postmortem,
Policy, Release, and Runbook. It intentionally keeps the existing predecessor
provenance and canonical owner anchors in the source ledger.

## Definitions / Facts

### Spec-driven development baseline

GitHub Spec Kit describes a specification-led workflow in which an initial
idea is refined into a PRD/specification, then a plan and executable tasks;
its implementation guidance makes validation and operational feedback inputs
to later specification refinement. This supports a **state flow**, not a
mandated workspace taxonomy:

```text
intent / evidence
  -> PRD (product authority)
  -> ARD + ADR (architecture authority)
  -> Spec (implementation authority)
  -> Plan + Task (execution authority and evidence)
  -> validation / change evidence
  -> Guide | Policy | Runbook | Incident | Postmortem
  -> named follow-up to the affected PRD, ARD, ADR, or Spec
```

Each arrow requires a named local owner and evidence appropriate to the next
state. A link shows traceability, not truth: source files, review, test output,
or observed operational evidence must substantiate the linked claim. A rejected
or deferred change must retain its boundary rather than silently becoming an
accepted decision. ISO/IEC/IEEE 12207 describes a common life-cycle framework
but does not prescribe a single lifecycle model or document format; local
`draft`, `active`, `done`, `accepted`, and `archived` remain repository states.

NIST SSDF is compatible with this flow because its practices can be integrated
into an SDLC. It is not a document template or a conformance certificate:
security constraints, threat/risk evidence, verification results, and
vulnerability response need named controls and independently observable
evidence. Markdown presence alone proves none of those outcomes.

### Document-family contract matrix

“Implemented” means the checked profile/template/static route exists as of
2026-08-08. It does not assess the semantic accuracy of every authored document
or exercise a live process. Required links are the profile's active/draft
traceability relationship where one exists; “routing expectation” means the
stage matrix, not a machine-enforced link.

| Family     | Role, trigger, inputs -> outputs                                                                                                                                 | Owner / audience / lifecycle                                                                                                                                                          | Required links and quality or security rule                                                                                                                                       | Workspace As-Is -> gap -> target                                                                                                                                                                                                                                                                      |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PRD        | Product intent, scope, and measurable acceptance before design; problem and stakeholders -> numbered product requirement.                                        | Product Manager; product/engineering readers; `draft -> active -> done/archived`.                                                                                                     | Active/draft traceability maps requirement IDs and acceptance criteria to ARD or Spec; make scope/non-goals and assumptions explicit.                                             | `sdlc/prd` route/template/H2 contract exists. Preserve requirement-to-downstream reciprocity; do not claim product validation from a template pass.                                                                                                                                                   |
| ARD        | Architecture requirements and constraints after a PRD; upstream requirement -> quality, context, data, deployment boundaries.                                    | System Architect; engineers/operators; `draft -> active -> accepted/archived`.                                                                                                        | Links a PRD requirement to ADR or Spec; quality attributes and boundaries are mandatory. Security/reliability constraints need evidence, not labels.                              | `sdlc/ard` exists. Keep PRD reciprocity and make non-goals/quality trade-offs reviewable.                                                                                                                                                                                                             |
| ADR        | Significant architectural choice and alternatives; decision context -> accepted/superseded decision with consequences.                                           | System Architect; maintainers/reviewers; `draft -> active -> accepted/archived`.                                                                                                      | Decision lineage from ARD/ADR to affected Spec/helper profiles; preserve supersession rather than rewriting historical acceptance.                                                | `sdlc/adr` exists with context, decision, consequences, alternatives. AWS ADR guidance is a benchmark, not a local immutability rule.                                                                                                                                                                 |
| Spec       | Implementation-ready technical contract before build/change; PRD/ARD/ADR constraints -> testable design, interfaces, failure handling, verification plan.        | Engineering owner; implementers/testers; `draft -> active -> done/archived`.                                                                                                          | Traceability joins PRD requirements/criteria to verification methods; failure, escalation, and security boundaries must be explicit.                                              | `sdlc/spec` and helper profiles/templates exist. A valid spec is not proof implementation or tests succeeded.                                                                                                                                                                                         |
| Plan       | Ordered delivery and risk/validation/rollback design once a Spec is stable enough; Spec/ADR -> work packages and expected Tasks.                                 | Product/QA/tech lead; delivery reviewers; `draft -> active -> done/archived`.                                                                                                         | Traceability maps Spec criterion to work package and reciprocal Task. It must not be used as a live operating procedure.                                                          | `sdlc/plan` exists with execution-lineage validation. Planning evidence is not deployment approval.                                                                                                                                                                                                   |
| Task       | Execution record for assigned work, safety boundaries, review, and evidence; Plan/Spec -> dated evidence and handoff.                                            | Engineer/QA; implementers/reviewers; `draft -> active -> done/archived`.                                                                                                              | Traceability maps criterion/work item to result/evidence; program/standalone lineage constrains active records.                                                                   | `sdlc/task` exists with static lifecycle gates. A `done` document does not prove a remote or live action.                                                                                                                                                                                             |
| Guide      | Audience-facing learning or goal procedure once a surface is stable; stable promoted owner + audience need -> usable instructions and pitfalls.                  | Technical Writer; developers/operators/users; `draft -> active -> accepted/archived`.                                                                                                 | Promotes an eligible Spec/helper/Task; audience, prerequisites, steps, and pitfalls are required. Never turn an unverified command into a safe operational instruction.           | `sdlc/guide` exists. It is chiefly how-to-shaped; tutorial intent remains an untyped gap addressed in the Diátaxis reference.                                                                                                                                                                         |
| Incident   | Contemporaneous factual event record during response; observed impact/timeline -> response state, evidence, follow-up.                                           | Operations/Security; incident responders and later reviewers; `draft -> active -> accepted/archived`.                                                                                 | Traceability links timeline/action to a follow-up Task. Keep timestamps, source evidence, and later analysis distinct; no incident document authorizes production access.         | `sdlc/incident` exists at the incident-folder route. Static contract does not prove on-call response, evidence availability, or containment.                                                                                                                                                          |
| Postmortem | Blameless learning after incident closure; incident facts -> causal analysis, prevention, owned actions, feedback targets.                                       | Operations/Security; responders, engineering, leadership; `draft -> active -> accepted/archived`.                                                                                     | Links root cause/actions to Task and a feedback target. Google SRE supports timely blameless learning and follow-through; local action closure is not thereby proven.             | `sdlc/postmortem` exists as co-located `postmortem.md`. Target: retain explicit owner/due-state/evidence and route material learning to a canonical document.                                                                                                                                         |
| Policy     | Normative operational/release controls before a controlled release or control change; requirements/risk -> scope, controls, exceptions, verification, cadence.   | Operations Engineer; operators, reviewers, release stakeholders; `draft -> active -> accepted/archived`.                                                                              | Promotes eligible Spec/helper/Task. Controls need a responsible owner and verification surface; exceptions must remain bounded and reviewable.                                    | `sdlc/policy` exists. The stage matrix calls policy part of release control, but a profile does not demonstrate enforcement.                                                                                                                                                                          |
| Release    | A discrete, auditable version/change decision; approved policy, change set, validation, version decision -> release record, approval, rollout/rollback evidence. | No canonical local owner; intended readers include release/operations and consumers. A lifecycle must be approved before use (for example `draft -> approved -> released/withdrawn`). | Should link Policy, Plan/Task, validation results, deployment/runbook and, where public API exists, SemVer decision. Must not substitute a tag or workflow for approval evidence. | **Gap:** no `sdlc/release` profile, template, canonical path/index, status domain/lifecycle, or validator was found. Target requires a separately approved cross-stage owner, state model, retention/supersession rules, template, registry/schema projection, fixtures, and negative tests together. |
| Runbook    | Safe, repeatable operational procedure after a procedure is known; policy/observed procedure -> preconditions, steps, verification, observability, recovery.     | Operations Engineer; operators/responders; `draft -> active -> accepted/archived`.                                                                                                    | Promotes eligible policy/Spec/helper/Task; require verification, evidence sources, and safe rollback/recovery. A runbook is not an incident fact record or release approval.      | `sdlc/runbook` exists. Static validation cannot show a command is safe in a live environment.                                                                                                                                                                                                         |

### 2026-08-10 gap-only source refresh

This refresh adds external meaning only for the five admitted document families.
It does not change a profile, template, lifecycle, route, or the accepted Spec
052 decisions. In particular, DOC-G5 still rejects a first-class release-notes
type; the broader release-record question remains a separate cross-stage design
decision.

| Family  | External question answered                                                          | Source-backed rule                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Workspace As-Is -> bounded target                                                                                                                                                                                                                                                                                             | Boundary                                                                                                                                                                                                                  |
| ------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PRD     | What evidence should connect stakeholder intent to requirements and acceptance?     | Requirements engineering turns stakeholder expectations into traceable requirements and information items, but ISO does not define a universal Product Requirements Document template ([SRC-WERPC-053](source-coverage.md#source-register)).                                                                                                                                                                                                                                                                                                              | The local PRD already owns vision, problem, personas, use cases, numbered requirements, acceptance, scope, risks, and downstream links. Keep that repository-defined contract; distinguish narrative intent from atomic technical requirements and never treat template conformance as stakeholder or product validation.     | ISO clauses beyond the public abstract were not consulted; NASA uses PRD to mean Project Requirements Document, so neither source owns the local family name or format.                                                   |
| ARD     | What makes an architecture description reviewable without prescribing one notation? | An architecture description is a work product about an architecture; purpose/environment, stakeholders and concerns, context, drivers, constraints, decisions/rationale, and concern-addressing views make it useful, while ISO 42010 does not mandate a method, tool, notation, format, or medium ([SRC-WERPC-054](source-coverage.md#source-register)).                                                                                                                                                                                                 | The local ARD already owns boundaries, quality attributes, context, data, deployment, and PRD-to-ADR/Spec traceability. Review material changes proportionally for unambiguous context, named drivers, decision rationale, and concern-to-view coverage; require a diagram only when it clarifies a real boundary or concern. | The ISO text consulted was public catalog/abstract material and the NASA outline is agency guidance; no ISO conformance or universal Markdown format is claimed.                                                          |
| Policy  | How is normative intent separated from implementation and assessment?               | Policy establishes accountable intent, scope, responsibilities, controls, exceptions, communication, review, and update triggers; procedures implement it and assessment evidence tests controls rather than treating the document as enforcement ([SRC-WERPC-055](source-coverage.md#source-register)).                                                                                                                                                                                                                                                  | `sdlc/policy` already requires scope, applies-to roles, controls, exceptions, verification, cadence, and traceability. Preserve Policy as the normative owner, keep commands in Runbooks, and bind each control to an enforcement surface and assessment evidence.                                                            | NIST's detailed model is cybersecurity/privacy-specific. Its accountability and policy/procedure/evidence separation are a bounded benchmark, not a universal operations-policy standard or proof of enforcement.         |
| Release | What is an auditable release record beyond version semantics or notes?              | Release engineering spans source, build, test, packaging, approval gates, deployment, audit trail, and rollback; immutable tag/commit/assets and provenance strengthen artifact identity but do not establish organizational release intent or approval ([SRC-WERPC-056](source-coverage.md#source-register); existing [SRC-WERPC-019](source-coverage.md#source-register), [SRC-WERPC-032](source-coverage.md#source-register), and [SRC-WERPC-040](source-coverage.md#source-register)). | No `sdlc/release` owner exists. A future decision must either map identity, approval, validation, provenance, rollout, rollback, outcome, retention, and supersession to existing Policy/Plan/Task/Runbook owners or approve a complete new contract atomically.                                                              | No public API, hosted release, immutable-release setting, attestation, rollout, or rollback was observed. A tag, workflow, GitHub Release, SemVer value, release notes, provenance, or attestation alone is insufficient. |
| Runbook | What makes an operational procedure safe, current, and improvable?                  | Current, known, practiced playbooks accelerate response; repeated deterministic command sequences should be evaluated for automation while preserving human judgment, escalation, and automation-failure recovery ([SRC-WERPC-057](source-coverage.md#source-register); existing [SRC-WERPC-018](source-coverage.md#source-register)).                                                                                                                                                                                               | `sdlc/runbook` already requires trigger, prerequisites, procedure, expected results, stop/escalation, verification, evidence, and recovery. Route the automation counter-rule through approved DOC-G10 and queued/not-executed WORK-013; record rehearsal/currentness as evidence without silently adding a required heading. | Google uses playbook/runbook contextually rather than as a formal document standard. Static structure cannot prove commands are current, rehearsed, authorized, or safe live.                                             |

The authoring consequence is a review checklist, not taxonomy expansion: keep
stable requirement and evidence identities; keep architecture views
proportional to concerns; keep policy intent separate from procedures; keep a
release record distinct from notes, versions, and provenance; and keep runbook
automation risk-based with a recoverable manual path.

### Current contract and evidence flow

The checked profiles use exact five-key SDLC frontmatter and closed status
domains. The registry, Markdown-profile validator, and strict links/owners
validator mechanically check route, required headings, relationship shape, and
index/link integrity. They are valuable **structural evidence**. They do not
validate business truth, change approval, test execution, source provenance,
secrets, runtime readiness, or a live deployment.

The required target is therefore a two-part rule: keep each authoritative fact
in its canonical family, and attach the smallest reproducible evidence needed
for the claim. Security-sensitive or production-changing instructions retain
an explicit approval boundary; an Incident, Runbook, or Release-shaped text
must never be interpreted as that approval.

### Gap-to-target sequence

1. Keep the registry/schema as the machine authority and Stage 00 routing as
   the human authority; do not duplicate lifecycle rules in research prose.
2. For existing families, retain route, owner, state, traceability and evidence
   in canonical records, and use negative validator tests before changing a
   deterministic rule.
3. Apply Diátaxis purpose during authoring and review before proposing new
   document profiles; a classification checklist is lower-risk than taxonomy
   expansion.
4. Resolve Release as a designed cross-stage contract, not an ad-hoc notes
   file: owner, audience, status transitions, approval, version scope,
   rollout/rollback, retention, supersession, links, fixtures, and validators
   must be decided together.
5. Treat SSDF, ISO, Google SRE, AWS ADR, and SemVer as bounded external
   benchmarks. Any conformance, incident-response, release, or production
   claim needs separately dated local evidence.

### 2026-08-17 full-corpus refresh

This increment is the fifth refresh cycle over this pack, executed under
Spec 058. Unlike the three preceding cycles it re-observed every owner row in
the pack rather than the twelve `Partial` rows, and it assigns each retained
`Partial` or `DEFER` row a blocking class recorded in the
[scope application index](scope-application-index.md). All observations are
dated **2026-08-17**. No live cluster, hosted CI run, provider runtime,
authenticated execution, or secret value was observed.

#### Re-observation of the fourteen document and lifecycle rows

All fourteen rows owned by this report were re-observed (`SRC-WERPC-080`). One
returned `changed` and thirteen returned `unchanged`. No status changed.

| Request ID    | External   | Workspace | Blocking class  |
| ------------- | ---------- | --------- | --------------- |
| REQ-WERPC-007 | unchanged  | confirmed | none            |
| REQ-WERPC-010 | unchanged  | confirmed | repo-static     |
| REQ-WERPC-011 | changed    | confirmed | none            |
| REQ-WERPC-012 | unchanged  | confirmed | none            |
| REQ-WERPC-013 | unchanged  | confirmed | none            |
| REQ-WERPC-014 | unchanged  | confirmed | human-judgement |
| REQ-WERPC-015 | unchanged  | confirmed | none            |
| REQ-WERPC-016 | unchanged  | confirmed | none            |
| REQ-WERPC-017 | unchanged  | confirmed | none            |
| REQ-WERPC-018 | unchanged  | absent    | human-judgement |
| REQ-WERPC-019 | unchanged  | confirmed | none            |
| REQ-WERPC-034 | unchanged  | confirmed | repo-static     |
| REQ-WERPC-035 | unchanged  | confirmed | repo-static     |
| REQ-WERPC-036 | unchanged  | confirmed | repo-static     |

#### REQ-WERPC-011 — the announced ISO 29148 revision entered ballot

**External result:** `changed` (`SRC-WERPC-088`). `ISO/IEC/IEEE 29148:2018` is
itself unchanged and was reconfirmed by its 2024 systematic review. What changed
is that a Draft International Standard, `ISO/IEC/IEEE DIS 29148`, is now visibly
in the ISO enquiry and ballot phase to replace it. This is the announced revision
that this report previously recorded as a future refresh trigger. The trigger has
fired in the sense that the revision is confirmed in progress, but the draft is
**not yet published**, so it does not supersede the 2018 edition.

**Status effect:** `no-change` (`CLM-WERPC-011-11`). `REQ-WERPC-011` keeps
`Verified`. A draft in ballot is not a published edition, and adopting it as
current basis would overstate the evidence.

**Blocking class:** `none`. Reopens when `DIS 29148` is published as the new
edition.

#### Structural contract re-verification

`REQ-WERPC-034`, `035`, and `036` were re-verified against
`docs/99.templates/registry.json` at the level this pack claims:
route regex, frontmatter key set and order, status domain, the closed
required-equals-allowed heading set, and the `bodyContract` reciprocity and
identifier rule. `sdlc/spec` still declares eleven closed headings with
`sourceLinkColumn` `PRD requirement`; `sdlc/plan` still declares nine with the
coupled `Spec criterion` identifier and `Expected Task` target column;
`sdlc/task` still declares six with the coupled `Criterion / work item`
identifier. All three remain `Verified` on structural contract with content,
implementation, and delivery effectiveness `DEFER`.

Instance tallies were not independently re-counted this cycle. The counts
recorded on 2026-08-14 are carried forward unchanged and are explicitly not
re-verified, because the package that owned these rows executed without a shell
tool. This is recorded as a bounded limitation rather than reported as a
confirmed count (`CLM-WERPC-011-34` through `CLM-WERPC-011-36`).

#### REQ-WERPC-018 — the decided Release gap is intact

A case-insensitive search across `document-profiles.json` returns zero matches
for a `release` profile: no `sdlc/release` identifier, route, template, or status
domain exists. `docs/03.specs/052-document-taxonomy-consolidation/spec.md:203`
still records `DOC-G5` as a decision. The workspace result is therefore `absent`
by design rather than drifted (`CLM-WERPC-011-18`). **Blocking class:**
`human-judgement` — creating a Release contract requires a separately approved
cross-stage design, which repository reading cannot supply.

#### REQ-WERPC-014 — Guide typing remains a queued decision

`sdlc/guide` still declares the `Guide Type` heading with no value constraint,
and `docs/03.specs/052-document-taxonomy-consolidation/spec.md:199` still records
`DOC-G1` as unenforced with the work queued rather than executed. The eight
tracked guides all still declare `how-to`. **Status effect:** `no-change`
(`CLM-WERPC-011-14`). **Blocking class:** `human-judgement`.

#### Retrieval caveat recorded for successors

`iso.org` returned HTTP 403 to direct retrieval for the ISO rows, and
`docs.aws.amazon.com` returned 403 once for the ADR row. Both were resolved
through a search-mediated fallback and are therefore recorded as observed rather
than `unreachable`. This is the same class of egress flakiness previously
documented for `diataxis.fr` HTTP 429, with a different host and status code.
Successor cycles re-checking ISO pages should expect 403 and prepare the
fallback.

## Sources

- [GitHub Spec Kit — Specification-Driven Development](https://github.com/github/spec-kit/blob/main/spec-driven.md) and [agentic SDD reference](https://github.com/github/spec-kit/blob/main/docs/reference/agentic-sdd.md), checked 2026-08-08: specification/plan/task flow and feedback framing; toolkit guidance only.
- [NIST SP 800-218 SSDF v1.1](https://csrc.nist.gov/pubs/sp/800/218/final), checked 2026-08-08: high-level secure-development practices integrable into an SDLC; no local implementation inference.
- [ISO/IEC/IEEE 12207:2026 abstract](https://www.iso.org/cms/render/live/en/sites/isoorg/contents/data/standard/09/02/90219.html), checked 2026-08-08: lifecycle-process framework boundary from the official abstract; paid clauses were not consulted.
- [AWS ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html), checked 2026-08-08: ADR context/consequence/supersession benchmark.
- [Google SRE incident management](https://sre.google/resources/practices-and-processes/incident-management-guide/) and [postmortem culture](https://sre.google/workbook/postmortem-culture/), checked 2026-08-08: response and learning/follow-through benchmark.
- [Semantic Versioning 2.0.0](https://semver.org/), checked 2026-08-08: public-API version meaning, not release governance.
- [ISO/IEC/IEEE 29148:2018 abstract](https://www.iso.org/standard/72089.html) and [NASA system-design processes](https://www.nasa.gov/reference/4-0-system-design-processes/), checked 2026-08-10: requirements-engineering information items and stakeholder-to-requirement practice; no universal Product Requirements Document format or conformance claim.
- [ISO/IEC/IEEE 42010:2022 abstract](https://www.iso.org/standard/74393.html) and [NASA software architecture description guidance](https://swehb.nasa.gov/spaces/SWEHBVB/pages/32604329/7.07%2B-%2BSoftware%2BArchitecture%2BDescription), checked 2026-08-10: architecture-description concepts and proportional review guidance; no fixed notation or format claim.
- [NIST CSF 2.0](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20), [SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final), and [SP 800-53A Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/a/r5/final), checked 2026-08-10: accountable policy, procedure, control, and assessment-evidence separation within the bounded cybersecurity/privacy context.
- [Google SRE release engineering](https://sre.google/sre-book/release-engineering/) and [GitHub immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases), checked 2026-08-10: release pipeline/audit and immutable artifact-identity boundaries; not a local release-document decision.
- [Google SRE eliminating toil](https://sre.google/workbook/eliminating-toil/), checked 2026-08-10: risk-aware automation of repeated operational procedures; no universal runbook standard or live-safety proof.

## Review and Freshness

Refresh on any Stage 01–05 taxonomy/profile/template/validator change, a
Release-family proposal, changes to traceability or retention rules, security
control ownership, incident/postmortem practice, or upstream revision of the
listed sources. Recheck before asserting ISO/SSDF conformance or operational
effectiveness. The original source set remains observed as of 2026-08-08; the
gap-only additions are observed as of 2026-08-10. Recheck when ISO 29148's
announced revision is published, NIST policy/control assessment guidance
changes, the Release-family decision advances, or DOC-G10/WORK-013 changes the
Runbook automation contract.

### 2026-08-11 Partial/DEFER incremental refresh

This bounded increment was executed and checked on **2026-08-12**; the heading
retains the approved package date. It addresses only REQ-WERPC-014 and does not
change the Guide profile, template, instances, taxonomy, Spec 052, or its
queued execution package.

#### REQ-WERPC-014 retained Guide disposition

**Typed/static contract:** The `sdlc/guide` profile still selects the numbered
Guide route, closed frontmatter and lifecycle domains, the seven required H2
sections, and active/draft lifecycle traceability. The template still prompts
authors to choose `how-to`, `tutorial`, or `concept`, but the profile has no
value constraint for the required `Guide Type` section. All eight current
numbered Guide instances declare `how-to` and pass the existing structural
profile contract. This preserves the source/claim-ledger distinction between
the verified static document contract in `CLM-WERPC-003-03` and the partial
classification/usefulness boundary in `CLM-WERPC-003-09`.

**Approved owner:** Spec 052 `DOC-G1` already requires the profile and template
enumeration, and `WORK-013` remains `Queued` / `Not executed`. PDRR-004 neither
implements that work nor changes the approved `DOC-G2`/`DOC-G3` route
decisions. Duplicate taxonomy or enforcement work is therefore excluded.

**Reader evidence:** A required heading, a declared `how-to` value, and a
profile PASS can establish only repository-static shape. They do not establish
that the classification matches a reader's need, that commands are safe in the
reader's environment, or that a reader can find, understand, and complete the
intended task. No reader test, accessibility study, task-completion observation,
or effectiveness measure was authorized or invented. Those outcomes remain
`DEFER` until a separately approved activity names the reader, task,
environment, method, acceptance threshold, and evidence owner.

**Final disposition:** `Partial`, retained as `exclude-duplicate`. No material
claim change exists and no claim proposal is created. Refresh when Spec 052 is
superseded, `WORK-013` changes Guide typing, a current Guide stops satisfying
the static contract, or a named reader-validation activity is approved.

### 2026-08-14 consistency and Partial re-observation

This bounded increment re-observed the workspace for `REQ-WERPC-014`, checked
on **2026-08-14**, and separately re-observed the Spec, Task, and Plan
document families named by Spec 057 amendment `C-WRCP-010` (`REQ-WERPC-034`,
`035`, `036`), which had no coverage-matrix owner row before this cycle. It
did not invoke a provider, query the GitHub remote, or inspect a cluster.

#### REQ-WERPC-014 Guide workspace consistency check

**Workspace delta:** `no-change`. `docs/05.operations/guides/` still holds
exactly eight numbered Guide instances, each declaring `` `how-to` ``. The
`sdlc/guide` profile object in `document-profiles.json` is unchanged (see the
key-level comparison recorded in the Diátaxis reference's matching section).
Spec 052 remains `active`, `DOC-G1` remains unenforced, and `WORK-013`
remains `Queued` / `Not executed`.

**External result:** not applicable this cycle. Consistent with the
2026-08-11 precedent, `REQ-WERPC-014` has no dedicated row in the source
register and continues to rely on repository-static evidence (Spec 052, the
`sdlc/guide` profile, and the eight Guide instances) only.

**As-Is:** Unchanged from the 2026-08-12 section: the static/typed document
contract remains `Verified`; classification usefulness for a named reader
remains `DEFER`.

**Gap and bounded target:** Unchanged. `DOC-G1` enum enforcement is queued
under `WORK-013` and does not enlarge this reference's scope.

**Missing evidence:** a named reader, task, environment, method, acceptance
threshold, and evidence owner for Guide classification usefulness.
**Owning authority:** Spec 052 for `DOC-G1`–`DOC-G3`; `WORK-013`'s owning
Plan for enum-enforcement execution. **Safe boundary:** a separately
approved, non-secret reader-validation activity, or the already-approved
`WORK-013` change executed by its own Plan; neither is authorized here.
**Refresh trigger:** Spec 052 is superseded, `WORK-013` executes, a current
Guide stops satisfying the static contract, or a named reader-validation
activity is approved.

**Final disposition:** `Partial`, retained as `exclude-duplicate`, unchanged
from the 2026-08-12 baseline. No promotion. New claim registered:
`CLM-WERPC-010-08`.

#### Spec, Task, and Plan document-family re-observation (`REQ-WERPC-034`, `035`, `036`)

Per `C-WRCP-010`, admitting these three families as coverage-matrix owner
rows neither raises nor lowers a status; Task 7 registers the rows, this
re-observation only supplies the dated evidence. This increment re-read the
three canonical paths, the `sdlc/spec`/`sdlc/task`/`sdlc/plan` profile
objects, the three templates, and `scripts/validate-markdown-profiles.py`
and `scripts/validate-links-and-owners.py`. It does not restate the
document-family contract matrix row above; it records only what this
re-observation adds or corrects.

**Enforced H2 profile (repository-static, matches each template exactly):**

| Family | Canonical path                            | Required H2 sections (in order)                                                                                                                                                                                                                                                              |
| ------ | ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Spec   | `docs/03.specs/[0-9]{3}-*/spec.md`        | Overview; Strategic Boundaries & Non-goals; Contracts; Core Design; Data Modeling & Storage Strategy; Interfaces & Data Structures; Edge Cases & Error Handling; Failure Modes & Fallback / Human Escalation; Verification Commands; Success Criteria & Verification Plan; Traceability (11) |
| Task   | `docs/04.execution/tasks/YYYY-MM-DD-*.md` | Overview; Inputs; Task Table; Approval and Safety Boundaries; Verification Summary; Traceability (6)                                                                                                                                                                                         |
| Plan   | `docs/04.execution/plans/YYYY-MM-DD-*.md` | Overview; Context; Goals & In-Scope; Non-Goals & Out-of-Scope; Work Breakdown; Verification Plan; Risks & Mitigations; Completion Criteria; Traceability (9)                                                                                                                                 |

**Lifecycle states the repository actually uses:** all three profiles
declare a four-value `statusDomain` (`draft`, `active`, `done`, `archived`),
but a frontmatter tally across every tracked instance on 2026-08-14 shows
zero `archived` use in any family: Spec is 5 `draft` / 6 `active` / 42
`done` / 0 `archived` of 53 files; Task is 5 `draft` / 2 `active` / 64
`done` / 0 `archived` of 71 files; Plan is 5 `draft` / 2 `active` / 62
`done` / 0 `archived` of 69 files. `archived` is a declared-but-unexercised
value for all three families, not a gap in the profile itself.

**Reciprocity rules the validator enforces:** the `bodyContract` on all
three requires a `### Lifecycle Traceability` table under `## Traceability`
and applies `reciprocalEvidence: true`, but the enforcement window is
`draft`/`active` only — `_body_contract_is_enforced` returns `status in
enforced_statuses` in the default `registry` body-contracts mode used by
`--mode strict` (`scripts/validate-links-and-owners.py:2871`,
`:636`), so a `done` or `archived` Spec/Task/Plan's own Traceability table is
no longer link/identifier-checked. That leaves 11 of 53 Spec files, 7 of 71
Task files, and 7 of 69 Plan files currently subject to the check.
`allowedSourceProfileIds`/`allowedTargetProfileIds` differ per family: Spec
links only from `sdlc/prd` (`targetLinkColumn` is `null`, so a Spec's
downstream side is never link-checked); Plan links from
`{sdlc/spec, sdlc/api-spec, sdlc/agent-design, sdlc/data-model, sdlc/tests}`
and to `sdlc/task`; Task links from
`{sdlc/plan, sdlc/spec, sdlc/api-spec, sdlc/agent-design, sdlc/data-model, sdlc/tests}`
with no target column, consistent with this cycle's own direct
Task-to-Spec/Plan standalone-execution links under ADR-0022.

A coupling exists only where a family's `identifierColumns` entry and its
`sourceLinkColumn`/`targetLinkColumn` name the **same** table column: Plan's
`Spec criterion` (kind `criterion`, pattern `^VAL-[A-Z0-9-]+-[0-9]{3}$`) is
also its `sourceLinkColumn`, and Task's `Criterion / work item` (kind
`work-item`, pattern `^[A-Z][A-Z0-9-]+-[0-9]{3}$`) is also its
`sourceLinkColumn`. For a coupled cell, `BODY-CONTRACT-IDENTIFIER`
(`scripts/validate-markdown-profiles.py:721-748`) and `BODY-LINK-SOURCE`
(`scripts/validate-links-and-owners.py:4503-4534`) both read the same
non-`N/A` value, and `_identifier_text` unwraps a full `[label](url)` link
to its label before pattern-matching. Verified directly against this
cycle's own authored documents rather than assumed: the reciprocal
[Plan](../../../03.specs/0058-workspace-research-consistency-and-partial-refresh/plan.md#traceability)'s
`Spec criterion` column (lines 843–855) renders every non-excluded row as
`[VAL-WRCP-0NN](../../../03.specs/0058-workspace-research-consistency-and-partial-refresh/spec.md)` —
a plain markdown link whose visible label is the bare `VAL-` identifier, no
backticks — and this
[package Task records](../../../03.specs/0058-workspace-research-consistency-and-partial-refresh/README.md#task-records), whose
`Criterion / work item` column (lines 210–219) follows the identical
pattern with `[WRCP-0NN](...#anchor)`. **This corrects, rather than
confirms, the brief's illustrative example**: `sdlc/spec` itself does not
carry this coupling, because its `sourceLinkColumn` is `PRD requirement`,
not `Spec criterion` — `Spec criterion` is identifier-checked only. Verified
against Spec 057's own Traceability table
(`docs/03.specs/0058-workspace-research-consistency-and-partial-refresh/spec.md`
lines 339–352): its `Spec criterion` column holds twelve plain bare values
(`VAL-WRCP-001` … `VAL-WRCP-012`, no backticks, no links, since that column
is never a link column for `sdlc/spec`), while its `PRD requirement` column
— the one that actually is `sdlc/spec`'s `sourceLinkColumn` — holds twelve
plain-text `N/A — direct human request for …` exclusions (no backticks
either), because Spec 057 is a direct-approval standalone execution under
ADR-0022 with no PRD to link. The coupled, both-constraints-on-one-cell
pattern the brief describes is real and verified, but it lives on Plan's
`Spec criterion` and Task's `Criterion / work item` columns, and its only
observed non-exclusion form in this repository is a plain markdown link
carrying the bare identifier as its label — not a backticked identifier.

**What the matrix row already claims, and what this adds:** the matrix row
states each profile/template exists and warns that a valid document does
not prove implementation, deployment, or live action succeeded; this
re-observation adds the exact heading counts and order, the exact lifecycle
distribution and its `archived`-declared-but-unused fact, the exact
enforcement window (`draft`/`active` only, `done`/`archived` exempt), the
exact allowed source/target profile sets, and the verified identifier/link
coupling behavior above. Nothing in the matrix row is restated or altered.

**Status, split by contract and effect (`C-WRCP-010`):** the admission of
`REQ-WERPC-034`/`035`/`036` neither raises nor lowers a status. For all
three families, the structural contract (route, frontmatter, status domain,
required H2 set, and `bodyContract` reciprocity/identifier rule) is
`Verified` by the strict-mode validators run this cycle (see Verification
below). Effectiveness — whether a Spec/Task/Plan's content is
implementation-ready, execution-safe, or delivery-approved — is unmeasured
and remains `DEFER`.

**Missing evidence (DEFER half):** authored-content correctness,
implementation success, execution safety, and delivery/deployment approval
for any individual Spec/Task/Plan instance. **Owning authority:** the
engineering owner named by each profile's matrix row (Engineering owner for
Spec; Engineer/QA for Task; Product/QA/tech lead for Plan); Stage 99 for the
registry/schema/template contract itself. **Safe boundary:** the existing
strict registry, Markdown-profile, and links/owners validators against the
exact tracked instance; no live build, deployment, or remote action is
authorized by this reference. **Refresh trigger:** a cited profile, template,
lifecycle, or validator rule changes, or a named Spec/Task/Plan instance is
separately authorized for content/effectiveness review.

**Final disposition:** Contract half `Verified`; effect half `DEFER` for all
three families. No claim is promoted beyond this split. New claims
registered: `CLM-WERPC-010-10` (`REQ-WERPC-034`), `CLM-WERPC-010-11`
(`REQ-WERPC-035`), `CLM-WERPC-010-12` (`REQ-WERPC-036`).

### 2026-08-20 full-corpus reverification

This increment consumes the reviewed SDLC/documentation report at workspace
baseline `8d8c8e5634fe939f8daaf041fbf5dfb444ed4a9c`. External and workspace
results remain independent. It appends current observations to this owner
without rewriting the legacy ARD history above, creating a universal document
standard, or treating public framework guidance as local conformance. The
allocation slice adds no source and assigns only
`CLM-WERPC-013-01..03` to the three current-form AD terminology corrections.

#### REQ-WERPC-007 Spec-driven development

- **Sources and result:** `unchanged` / `confirmed`, using
  `SRC-WERPC-014` and selector
  `spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline`.
- **As-Is / Gap / Target:** GitHub Spec Kit still places specification and
  refinement before planning and task execution; the workspace retains its
  bounded Spec/Plan/Task flow. Neither generated code nor a delivery outcome
  was observed. Keep the practice model and evidence outcomes separately.
- **Evidence / rejected inference:** public documentation only. The upstream
  workflow does not prove Spec Kit installation, generated-code correctness,
  provider execution, hosted CI, or local effectiveness.
- **Disposition / boundary:** `Verified`; blocking class `none`. No deeper
  outcome is promoted from the static observation.
- **Owner / safe follow-up / trigger:** Stage 03/04 lifecycle governance.
  Reopen if Spec Kit materially changes the cited flow or the local
  Spec/Plan/Task contract changes; evaluate outcomes only in a separately
  authorized execution.

#### REQ-WERPC-010 SDLC framework and evidence chain

- **Sources and result:** `unchanged` / `confirmed`, using
  `SRC-WERPC-015`, `SRC-WERPC-016`, and the same baseline selector.
- **As-Is / Gap / Target:** the repository retains its own lifecycle states,
  authorities, inputs, outputs, approvals, traceability, failure meanings, and
  evidence owners. ISO 12207:2026 and SSDF v1.1 remain bounded lifecycle and
  secure-development benchmarks; named control and result evidence is still
  needed before any conformance or effectiveness claim.
- **Evidence / rejected inference:** repository-static plus public catalog and
  publication evidence. The paid ISO clauses were not consulted, and neither
  source prescribes this taxonomy or proves a security control.
- **Disposition / boundary:** `Verified`; blocking class `repo-static`. The
  missing named lifecycle-control and effectiveness evidence remains `DEFER`.
- **Owner / safe follow-up / trigger:** Stage 00/03 lifecycle governance.
  Reopen on an ISO edition, SSDF revision, or local lifecycle-contract change;
  assess a named control only under its canonical owner.

#### REQ-WERPC-011 PRD contract

- **Sources and result:** `unchanged` / `drifted`, using
  `SRC-WERPC-053` and selector
  `spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix`.
- **As-Is / Gap / Target:** PRD owns product intent, stakeholders, scope,
  numbered requirements, and acceptance inputs, producing traceable product
  authority for AD or Spec review. The historical matrix still says ARD even
  though the terminal profile routes downstream architecture to
  Architecture Description (`sdlc/ad`). Preserve history and use AD in current
  references.
- **Evidence / rejected inference:** repository-static plus the public ISO
  catalog and NASA guidance. Public ISO evidence supports edition, status, and
  scope only; neither source defines a universal PRD form or proves stakeholder
  or product validation.
- **Disposition / correction:** `Verified gap`, blocking class `none`;
  `CLM-WERPC-013-01` records the current-form PRD downstream correction from
  legacy ARD to AD without rewriting historical text.
- **Owner / safe follow-up / trigger:** Product and Stage 99 profile owners.
  Reopen when ISO 29148 is published or superseded, NASA guidance changes, or
  the PRD-to-AD relationship changes.

#### REQ-WERPC-012 Architecture Description contract

- **Sources and result:** `unchanged` / `drifted`, using
  `SRC-WERPC-054` and the document-family selector.
- **As-Is / Gap / Target:** the terminal `sdlc/ad` contract turns upstream
  requirements and quality/context/data/deployment boundaries into an
  architecture description reviewed through AD-to-ADR/Spec traceability. The
  historical matrix retains the former ARD name and route; current references
  must use AD and `sdlc/ad` while legacy observations stay unchanged.
- **Evidence / rejected inference:** repository-static plus public ISO/IEEE
  catalog and NASA guidance. Paid normative clauses were not read, and the
  sources mandate neither a Markdown form nor a notation or proof of
  architecture effectiveness.
- **Disposition / correction:** `Verified gap`, blocking class `none`;
  `CLM-WERPC-013-02` records the current-form ARD-to-AD terminology, route, and
  lineage correction.
- **Owner / safe follow-up / trigger:** Architecture and Stage 99 profile
  owners. Reopen on a terminal AD/ADR relation or cited guidance change;
  review material architecture content separately and proportionally.

#### REQ-WERPC-013 ADR contract

- **Sources and result:** `unchanged` / `drifted`, using
  `SRC-WERPC-017` and the document-family selector.
- **As-Is / Gap / Target:** ADR still turns a significant decision context and
  alternatives into accepted consequences and supersession lineage. The
  active profile now accepts AD/ADR decision lineage, while historical prose
  says ARD/ADR; current records must use AD/ADR.
- **Evidence / rejected inference:** repository-static plus AWS guidance. The
  guidance is a benchmark for context, consequences, acceptance, immutability,
  and supersession; it does not define the exact local lifecycle or prove
  decision quality.
- **Disposition / correction:** `Verified gap`, blocking class `none`;
  `CLM-WERPC-013-03` records the current AD/ADR lineage wording correction.
- **Owner / safe follow-up / trigger:** Architecture and Stage 99 profile
  owners. Preserve accepted/superseded history and reopen if the AD/ADR
  relationship or upstream ADR guidance changes.

#### REQ-WERPC-014 Guide contract

- **Sources and result:** `unchanged` / `confirmed`, using
  `SRC-WERPC-020` and the document-family selector.
- **As-Is / Gap / Target:** Guide remains an audience-facing how-to-shaped
  family that consumes a stable promoted owner and produces prerequisites,
  steps, outcomes, and pitfalls. Its structural contract does not establish
  reader classification, accessibility, safe execution, or usability; retain
  `DOC-G1` and queued `WORK-013` ownership.
- **Evidence / rejected inference:** repository-static plus Diátaxis public
  guidance. A profile pass and a declared type do not prove a named reader can
  find, understand, or complete the task.
- **Disposition / boundary:** `Partial`; blocking class `human-judgement`.
  Reader validation and DOC-G1 implementation evidence remain `DEFER`.
- **Owner / safe follow-up / trigger:** Spec 052 and the WORK-013 owner. Reopen
  if they change, a Guide violates its static contract, or an approved activity
  names reader, task, environment, method, threshold, and evidence owner.

#### REQ-WERPC-015 Incident contract

- **Sources and result:** `unchanged` / `confirmed`, using
  `SRC-WERPC-018` and the document-family selector.
- **As-Is / Gap / Target:** Incident remains the contemporaneous factual owner
  for impact, timeline, response state, evidence, and follow-up Task during an
  end-to-end preparation/response/mitigation flow. No on-call response or
  exercise was observed; keep facts and later analysis distinct.
- **Evidence / rejected inference:** repository-static plus Google SRE
  guidance. A static route and heading contract do not prove containment,
  evidence availability, or response effectiveness.
- **Disposition / boundary:** `Verified`; blocking class `none`. No runtime
  incident-response result is inferred.
- **Owner / safe follow-up / trigger:** Operations/Security incident owners.
  Reopen on profile, response-model, or Google SRE guidance change; rehearse
  only under separately approved operational scope.

#### REQ-WERPC-016 Postmortem contract

- **Sources and result:** `unchanged` / `confirmed`, using
  `SRC-WERPC-018` and the document-family selector.
- **As-Is / Gap / Target:** Postmortem remains the blameless learning owner that
  consumes incident facts and produces causal analysis, owned/due actions,
  follow-up Tasks, and feedback targets. No action closure or reliability
  improvement outcome was observed.
- **Evidence / rejected inference:** repository-static plus Google SRE
  guidance. A template does not prove measurable follow-through or learning.
- **Disposition / boundary:** `Verified`; blocking class `none`; effectiveness
  is not promoted from structure.
- **Owner / safe follow-up / trigger:** Operations/Security postmortem owners.
  Reopen on contract or source change and evaluate action completion from
  named evidence only.

#### REQ-WERPC-017 Policy contract

- **Sources and result:** `unchanged` / `confirmed`, using
  `SRC-WERPC-055` and the document-family selector.
- **As-Is / Gap / Target:** Policy remains the normative owner for intent,
  applies-to scope, controls, exceptions, verification, and review cadence,
  with procedures and assessments kept separate. No enforcement, assessment,
  or compliance result was observed.
- **Evidence / rejected inference:** repository-static plus bounded NIST CSF,
  SP 800-53, and SP 800-53A guidance. Those cybersecurity/privacy sources do
  not prescribe a universal operations-policy format or prove local controls.
- **Disposition / boundary:** `Verified`; blocking class `none`. Keep control
  and assessment evidence independently observable.
- **Owner / safe follow-up / trigger:** Operations policy/control owners.
  Reopen on NIST revision or local policy/control/assessment contract change.

#### REQ-WERPC-018 Release contract gap

- **Sources and result:** `unchanged` / `absent`, using
  `SRC-WERPC-019`, `SRC-WERPC-056`, and the document-family selector.
- **As-Is / Gap / Target:** no `sdlc/release` profile, route, template,
  lifecycle, or validator exists; `DOC-G5` preserves that deliberate absence.
  An auditable Release family would need identity, approval, validation,
  rollout, rollback, outcome, retention, supersession, and links designed
  atomically rather than inferred from notes, tags, workflows, or SemVer.
- **Evidence / rejected inference:** repository-static plus Google SRE,
  GitHub, and SemVer guidance. These are release-engineering, immutable-identity,
  and versioning benchmarks, not a local approval or deployment record.
- **Disposition / boundary:** `Verified gap`; blocking class
  `human-judgement`. The approved cross-stage design is missing and remains
  `DEFER`; no empty family is created.
- **Owner / safe follow-up / trigger:** cross-stage lifecycle authority. Reopen
  only if DOC-G5 is superseded, a complete Release design is approved, or the
  upstream release/identity guidance changes.

#### REQ-WERPC-019 Runbook contract

- **Sources and result:** `unchanged` / `confirmed`, using
  `SRC-WERPC-018`, `SRC-WERPC-057`, and the document-family selector.
- **As-Is / Gap / Target:** Runbook remains the operational procedure owner
  consuming a known trigger/control and producing preconditions, steps,
  expected results, stop/escalation, verification, evidence, and recovery.
  Command currency, rehearsal, authorization, automation behavior, and live
  safety were not observed; preserve a recoverable manual path.
- **Evidence / rejected inference:** repository-static plus Google SRE
  guidance. A static procedure cannot prove commands are current, rehearsed,
  authorized, automated safely, or production-safe.
- **Disposition / boundary:** `Verified`; blocking class `none`. Live
  execution and automation outcome remain outside this increment.
- **Owner / safe follow-up / trigger:** Operations Runbook owner. Reopen on
  profile, DOC-G10/WORK-013, recurring procedure, or cited SRE guidance change;
  rehearse only with explicit environment and approval boundaries.

#### REQ-WERPC-034 Spec contract

- **Sources and result:** `unchanged` / `confirmed`, using
  `SRC-WERPC-014`, `SRC-WERPC-076`, and the document-family selector.
- **As-Is / Gap / Target:** Spec consumes approved upstream constraints and
  produces a testable implementation contract, interfaces, failure handling,
  and verification criteria. Route/frontmatter/lifecycle/headings/traceability
  remain structurally checked; individual content readiness is unassessed.
- **Evidence / rejected inference:** repository-static plus Spec Kit guidance.
  Structural validity does not prove implementation readiness or success.
- **Disposition / boundary:** `Verified`; blocking class `repo-static`.
  Instance content and effectiveness remain `DEFER`.
- **Owner / safe follow-up / trigger:** engineering and Stage 99 profile owners.
  Reopen on profile/template/body-contract/source change or authorize one named
  instance review.

#### REQ-WERPC-035 Task contract

- **Sources and result:** `unchanged` / `confirmed`, using
  `SRC-WERPC-014`, `SRC-WERPC-076`, and the document-family selector.
- **As-Is / Gap / Target:** Task consumes a Plan/Spec work item and produces an
  assigned, safety-bounded execution/result/evidence handoff. Structural
  lifecycle and criterion linkage remain checked; no individual delivery
  result was assessed.
- **Evidence / rejected inference:** repository-static plus Spec Kit guidance.
  A `done` state cannot prove work, remote action, or delivery occurred.
- **Disposition / boundary:** `Verified`; blocking class `repo-static`.
  Execution and outcome evidence remain `DEFER`.
- **Owner / safe follow-up / trigger:** engineering/QA and Stage 99 owners.
  Reopen on profile/template/body-contract/source change or a separately
  authorized instance review.

#### REQ-WERPC-036 Plan contract

- **Sources and result:** `unchanged` / `confirmed`, using
  `SRC-WERPC-014`, `SRC-WERPC-076`, and the document-family selector.
- **As-Is / Gap / Target:** Plan consumes a stable Spec/ADR boundary and
  produces ordered work packages, risk treatment, validation, rollback design,
  and reciprocal Tasks. Its structure remains checked; risk treatment,
  rollback readiness, approval, and delivery outcome are unassessed.
- **Evidence / rejected inference:** repository-static plus Spec Kit guidance.
  A structurally valid Plan does not prove safe execution or delivery success.
- **Disposition / boundary:** `Verified`; blocking class `repo-static`.
  Instance delivery effectiveness remains `DEFER`.
- **Owner / safe follow-up / trigger:** product/QA/technical lead and Stage 99
  owners. Reopen on profile/template/body-contract/source change or a named
  instance effectiveness review.

## Related Documents

- [Documentation architecture and Diátaxis](documentation-architecture-and-diataxis.md)
- [LLM-WIKI routing](llm-wiki-and-knowledge-routing.md)
- [Source coverage and migration ledger](source-coverage.md)
- [Document profiles](../../../99.templates/registry.json)
- [Document Authoring Policy](../../../00.agent-governance/policies/document-authoring.md)
