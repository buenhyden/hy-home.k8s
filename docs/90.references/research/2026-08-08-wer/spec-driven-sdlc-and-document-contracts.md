---
title: 'Reference: Spec-Driven SDLC and Document Contracts'
type: content/reference
status: active
owner: platform
updated: 2026-08-08
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

`docs/99.templates/support/document-profiles.json` and its schema own typed
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

| Family | Role, trigger, inputs -> outputs | Owner / audience / lifecycle | Required links and quality or security rule | Workspace As-Is -> gap -> target |
| --- | --- | --- | --- | --- |
| PRD | Product intent, scope, and measurable acceptance before design; problem and stakeholders -> numbered product requirement. | Product Manager; product/engineering readers; `draft -> active -> done/archived`. | Active/draft traceability maps requirement IDs and acceptance criteria to ARD or Spec; make scope/non-goals and assumptions explicit. | `sdlc/prd` route/template/H2 contract exists. Preserve requirement-to-downstream reciprocity; do not claim product validation from a template pass. |
| ARD | Architecture requirements and constraints after a PRD; upstream requirement -> quality, context, data, deployment boundaries. | System Architect; engineers/operators; `draft -> active -> accepted/archived`. | Links a PRD requirement to ADR or Spec; quality attributes and boundaries are mandatory. Security/reliability constraints need evidence, not labels. | `sdlc/ard` exists. Keep PRD reciprocity and make non-goals/quality trade-offs reviewable. |
| ADR | Significant architectural choice and alternatives; decision context -> accepted/superseded decision with consequences. | System Architect; maintainers/reviewers; `draft -> active -> accepted/archived`. | Decision lineage from ARD/ADR to affected Spec/helper profiles; preserve supersession rather than rewriting historical acceptance. | `sdlc/adr` exists with context, decision, consequences, alternatives. AWS ADR guidance is a benchmark, not a local immutability rule. |
| Spec | Implementation-ready technical contract before build/change; PRD/ARD/ADR constraints -> testable design, interfaces, failure handling, verification plan. | Engineering owner; implementers/testers; `draft -> active -> done/archived`. | Traceability joins PRD requirements/criteria to verification methods; failure, escalation, and security boundaries must be explicit. | `sdlc/spec` and helper profiles/templates exist. A valid spec is not proof implementation or tests succeeded. |
| Plan | Ordered delivery and risk/validation/rollback design once a Spec is stable enough; Spec/ADR -> work packages and expected Tasks. | Product/QA/tech lead; delivery reviewers; `draft -> active -> done/archived`. | Traceability maps Spec criterion to work package and reciprocal Task. It must not be used as a live operating procedure. | `sdlc/plan` exists with execution-lineage validation. Planning evidence is not deployment approval. |
| Task | Execution record for assigned work, safety boundaries, review, and evidence; Plan/Spec -> dated evidence and handoff. | Engineer/QA; implementers/reviewers; `draft -> active -> done/archived`. | Traceability maps criterion/work item to result/evidence; program/standalone lineage constrains active records. | `sdlc/task` exists with static lifecycle gates. A `done` document does not prove a remote or live action. |
| Guide | Audience-facing learning or goal procedure once a surface is stable; stable promoted owner + audience need -> usable instructions and pitfalls. | Technical Writer; developers/operators/users; `draft -> active -> accepted/archived`. | Promotes an eligible Spec/helper/Task; audience, prerequisites, steps, and pitfalls are required. Never turn an unverified command into a safe operational instruction. | `sdlc/guide` exists. It is chiefly how-to-shaped; tutorial intent remains an untyped gap addressed in the Diátaxis reference. |
| Incident | Contemporaneous factual event record during response; observed impact/timeline -> response state, evidence, follow-up. | Operations/Security; incident responders and later reviewers; `draft -> active -> accepted/archived`. | Traceability links timeline/action to a follow-up Task. Keep timestamps, source evidence, and later analysis distinct; no incident document authorizes production access. | `sdlc/incident` exists at the incident-folder route. Static contract does not prove on-call response, evidence availability, or containment. |
| Postmortem | Blameless learning after incident closure; incident facts -> causal analysis, prevention, owned actions, feedback targets. | Operations/Security; responders, engineering, leadership; `draft -> active -> accepted/archived`. | Links root cause/actions to Task and a feedback target. Google SRE supports timely blameless learning and follow-through; local action closure is not thereby proven. | `sdlc/postmortem` exists as co-located `postmortem.md`. Target: retain explicit owner/due-state/evidence and route material learning to a canonical document. |
| Policy | Normative operational/release controls before a controlled release or control change; requirements/risk -> scope, controls, exceptions, verification, cadence. | Operations Engineer; operators, reviewers, release stakeholders; `draft -> active -> accepted/archived`. | Promotes eligible Spec/helper/Task. Controls need a responsible owner and verification surface; exceptions must remain bounded and reviewable. | `sdlc/policy` exists. The stage matrix calls policy part of release control, but a profile does not demonstrate enforcement. |
| Release | A discrete, auditable version/change decision; approved policy, change set, validation, version decision -> release record, approval, rollout/rollback evidence. | No canonical local owner; intended readers include release/operations and consumers. A lifecycle must be approved before use (for example `draft -> approved -> released/withdrawn`). | Should link Policy, Plan/Task, validation results, deployment/runbook and, where public API exists, SemVer decision. Must not substitute a tag or workflow for approval evidence. | **Gap:** no `sdlc/release` profile, template, canonical path/index, status domain/lifecycle, or validator was found. Target requires a separately approved cross-stage owner, state model, retention/supersession rules, template, registry/schema projection, fixtures, and negative tests together. |
| Runbook | Safe, repeatable operational procedure after a procedure is known; policy/observed procedure -> preconditions, steps, verification, observability, recovery. | Operations Engineer; operators/responders; `draft -> active -> accepted/archived`. | Promotes eligible policy/Spec/helper/Task; require verification, evidence sources, and safe rollback/recovery. A runbook is not an incident fact record or release approval. | `sdlc/runbook` exists. Static validation cannot show a command is safe in a live environment. |

### 2026-08-10 gap-only source refresh

This refresh adds external meaning only for the five admitted document families.
It does not change a profile, template, lifecycle, route, or the accepted Spec
052 decisions. In particular, DOC-G5 still rejects a first-class release-notes
type; the broader release-record question remains a separate cross-stage design
decision.

| Family | External question answered | Source-backed rule | Workspace As-Is -> bounded target | Boundary |
| --- | --- | --- | --- | --- |
| PRD | What evidence should connect stakeholder intent to requirements and acceptance? | Requirements engineering turns stakeholder expectations into traceable requirements and information items, but ISO does not define a universal Product Requirements Document template ([SRC-WERPC-053](source-coverage-and-migration-ledger.md#source-register)). | The local PRD already owns vision, problem, personas, use cases, numbered requirements, acceptance, scope, risks, and downstream links. Keep that repository-defined contract; distinguish narrative intent from atomic technical requirements and never treat template conformance as stakeholder or product validation. | ISO clauses beyond the public abstract were not consulted; NASA uses PRD to mean Project Requirements Document, so neither source owns the local family name or format. |
| ARD | What makes an architecture description reviewable without prescribing one notation? | An architecture description is a work product about an architecture; purpose/environment, stakeholders and concerns, context, drivers, constraints, decisions/rationale, and concern-addressing views make it useful, while ISO 42010 does not mandate a method, tool, notation, format, or medium ([SRC-WERPC-054](source-coverage-and-migration-ledger.md#source-register)). | The local ARD already owns boundaries, quality attributes, context, data, deployment, and PRD-to-ADR/Spec traceability. Review material changes proportionally for unambiguous context, named drivers, decision rationale, and concern-to-view coverage; require a diagram only when it clarifies a real boundary or concern. | The ISO text consulted was public catalog/abstract material and the NASA outline is agency guidance; no ISO conformance or universal Markdown format is claimed. |
| Policy | How is normative intent separated from implementation and assessment? | Policy establishes accountable intent, scope, responsibilities, controls, exceptions, communication, review, and update triggers; procedures implement it and assessment evidence tests controls rather than treating the document as enforcement ([SRC-WERPC-055](source-coverage-and-migration-ledger.md#source-register)). | `sdlc/policy` already requires scope, applies-to roles, controls, exceptions, verification, cadence, and traceability. Preserve Policy as the normative owner, keep commands in Runbooks, and bind each control to an enforcement surface and assessment evidence. | NIST's detailed model is cybersecurity/privacy-specific. Its accountability and policy/procedure/evidence separation are a bounded benchmark, not a universal operations-policy standard or proof of enforcement. |
| Release | What is an auditable release record beyond version semantics or notes? | Release engineering spans source, build, test, packaging, approval gates, deployment, audit trail, and rollback; immutable tag/commit/assets and provenance strengthen artifact identity but do not establish organizational release intent or approval ([SRC-WERPC-056](source-coverage-and-migration-ledger.md#source-register); existing [SRC-WERPC-019](source-coverage-and-migration-ledger.md#source-register), [SRC-WERPC-032](source-coverage-and-migration-ledger.md#source-register), and [SRC-WERPC-040](source-coverage-and-migration-ledger.md#source-register)). | No `sdlc/release` owner exists. A future decision must either map identity, approval, validation, provenance, rollout, rollback, outcome, retention, and supersession to existing Policy/Plan/Task/Runbook owners or approve a complete new contract atomically. | No public API, hosted release, immutable-release setting, attestation, rollout, or rollback was observed. A tag, workflow, GitHub Release, SemVer value, release notes, provenance, or attestation alone is insufficient. |
| Runbook | What makes an operational procedure safe, current, and improvable? | Current, known, practiced playbooks accelerate response; repeated deterministic command sequences should be evaluated for automation while preserving human judgment, escalation, and automation-failure recovery ([SRC-WERPC-057](source-coverage-and-migration-ledger.md#source-register); existing [SRC-WERPC-018](source-coverage-and-migration-ledger.md#source-register)). | `sdlc/runbook` already requires trigger, prerequisites, procedure, expected results, stop/escalation, verification, evidence, and recovery. Route the automation counter-rule through approved DOC-G10 and queued/not-executed WORK-013; record rehearsal/currentness as evidence without silently adding a required heading. | Google uses playbook/runbook contextually rather than as a formal document standard. Static structure cannot prove commands are current, rehearsed, authorized, or safe live. |

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

## Related Documents

- [Documentation architecture and Diátaxis](documentation-architecture-and-diataxis.md)
- [LLM-WIKI routing](llm-wiki-and-knowledge-routing.md)
- [Source coverage and migration ledger](source-coverage-and-migration-ledger.md)
- [Document profiles](../../../99.templates/support/document-profiles.json)
- [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
