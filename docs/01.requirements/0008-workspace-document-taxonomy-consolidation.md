---
title: 'Workspace Document Taxonomy Consolidation Product Requirements'
type: sdlc/prd
status: active
owner: platform
updated: 2026-08-11
artifact_id: "PRD-0008"
---

# Workspace Document Taxonomy Consolidation Product Requirements

## Overview

This program consolidates the repository's SDLC document topology, authoring
rules, templates, agent-governance controls, and validator orchestration into a
single traceable operating model. The human approved the target direction on
2026-08-09: co-locate each work unit's `spec.md`, `plan.md`, and `tasks.md`
under Stage 03; retire `docs/04.execution/`; keep `docs/05.operations/` at its
stable path; and do not create a Release document family or releases folder.

On 2026-08-10 the human also approved the terminal artifact model recorded by
the pre-WORK-104 design package `WDTC-AMEND-001` in accepted
[ADR-0024](../02.architecture/decisions/0024-terminal-artifact-identity-and-archive-layout.md).
The terminal active forms are PRD, optional SRS, optional Interface
Requirement, Architecture Description (AD), and ADR. Every declared
`artifact_id` is globally unique; mandatory terminal outer profiles require
one, while excluded profiles prohibit the field. Stage 98 uses stable change,
tombstone, and migration records instead of dated mirror paths. Accepted
ADR-0023 remains the transition predecessor. WORK-105 converted the complete
active/accepted ARD-0004 through ARD-0011 source census one-to-one to
AD-0004 through AD-0011, closed every live legacy ARD consumer, installed the
AD-0011 archive invariant, accepted ADR-0024, and
changed the PRD-0008 projection to ADR-0024 as one atomic gate. WORK-104 remains
the existing 82-move and destination Plan/Task rebaseline task.

WORK-105 retired the authored API Spec profile, Stage 03 route, template, and
relationships. Terminal human-authored interface
requirements use only Stage 01 `sdlc/interface` and the `IFC-###-<SLUG-TOKEN>`
grammar. Native OpenAPI, GraphQL, and Protobuf profiles/templates remain
machine-readable Interface evidence under separate native identity contracts;
they are not authored API Spec records or mandatory human artifact IDs.

The design is a local architecture choice, not an ISO, NIST, or tool-vendor
conformance claim. [ISO/IEC/IEEE 12207:2026](https://www.iso.org/cms/render/live/en/sites/isoorg/contents/data/standard/09/02/90219.html)
provides a common lifecycle-process framework without prescribing one lifecycle
model or document format, while
[ISO/IEC/IEEE 15289:2019](https://www.iso.org/cms/render/live/en/sites/isoorg/contents/data/standard/07/49/74909.html)
allows lifecycle information items to be combined or split for the selected
model. [GitHub Spec Kit](https://github.com/github/spec-kit/blob/main/docs/index.md)
and [OpenSpec](https://github.com/Fission-AI/OpenSpec/blob/main/docs/overview.md)
provide bounded implementation examples in which specification, design or
plan, and tasks are organized around one change. The local research boundary
is recorded in the [Spec-driven SDLC reference](../90.references/research/2026-08-08-wer/spec-driven-sdlc-and-document-contracts.md).

PRD-0007 remains the product authority for repository delivery assurance, but
its Specs 047 through 051 stay suspended while this program changes their
document and validator paths. Completed Spec 053 remains the authority for the
already-finished research-pack consolidation and is not reopened.

## Vision

A maintainer or AI agent can start from one stable work-unit folder, follow
requirements and decisions to implementation evidence, and identify exactly
one human rule owner and one machine enforcement owner for every governed
behavior. The current operating topology stays legible, historical evidence
stays recoverable, and repository-static readiness is never confused with
provider-runtime enforcement.

## Problem Statement

The clean pre-change 2026-08-09 repository audit found 458 tracked files under
`docs/`: 52 in Stage 03,
135 in Stage 04, 29 in Stage 05, 58 in Stage 90, 44 in Stage 98, and 41 in
Stage 99. Stage 03 contains 49 specifications, while Stage 04 contains 65 Plan
and 67 Task documents plus three indexes. Most execution pairs duplicate the
same work-unit slug but live in separate trees and carry a date-based filename
identity unrelated to their stable Spec identifier.

The active contracts also disagree with current implementation. Spec 052 and
its upstream design still require `05.operations` to become `04.operations`,
although the approved direction keeps Stage 05 stable. They assume one-shot
active-corpus data and validators can be deleted wholesale, while the current
script audit found distinct remaining contracts that require consumer and
negative-fixture proof before retirement. The document-profile registry is the
declared machine authority, yet Stage 00 and Stage 99 prose still restate
heading, route, and lifecycle ownership in several places.

The agent harness has strong repository-static role and adapter coverage, but
its static `current` or `ready` states can be mistaken for provider-enforced
behavior. It does not yet bind actual action approval to the target and
arguments, classify untrusted context and tool output, record system-level risk
and oversight, or preserve provenance and trace availability for admitted
agent components. NIST AI RMF, NIST AI 600-1, OWASP agentic guidance, OpenAI
tool/HITL/tracing guidance, Anthropic agent-evaluation guidance, and SLSA
provenance support those control objectives without proving local enforcement.

Finally, the clean pre-change worktree does not have a green all-files
baseline. The observed failures are a registry self-test temporary-memory
allocation error, three detect-secrets false positives or baseline drifts, and
one Markdown heading defect. These are recorded baseline defects and must be
closed by the program; they may not be hidden by weakening a gate.

## Personas

| Persona | Goal | Constraint or authority boundary |
| --- | --- | --- |
| Governance steward | Maintain one coherent SDLC and agent-governance rule system. | May consolidate owners but may not weaken approval, archive, or evidence boundaries. |
| Platform maintainer | Locate and evolve one work unit through a stable folder and lineage. | Approves protected local changes; does not implicitly authorize remote or live mutation. |
| Quality engineer | Preserve deterministic gates while removing redundant orchestration. | May retire a validator only after consumer, rule, and negative-fixture disposition. |
| Technical writer | Select one template and author to one current document contract. | Must preserve historical observation meaning and documented exceptions. |
| AI agent operator | Route each provider-specific agent through shared workspace governance. | Static configuration is not evidence of provider enforcement or runtime execution. |
| Auditor | Recover decisions, retired evidence, approvals, and validation results. | Existing archive payloads and digests are immutable. |

## Key Use Cases

A new work unit is created at `docs/03.specs/<NNN>-<slug>/`; its fixed-name
Spec, Plan, and Task files express one lifecycle without a separate execution
stage or date-based mutable identity.

A reviewer follows registry-owned reciprocal relations from a PRD and AD to
an accepted ADR, Spec criteria, Plan work packages, Task results, and
operations feedback. A link establishes traceability, while the named test or
review evidence establishes the claim.

A governance steward changes an authoring or lifecycle rule at one canonical
owner. Template forms and provider adapters project that owner, and validators
fail when a projection drifts.

A quality engineer migrates old and new routes through an explicit transition
window. The gate accepts only the declared transition state, rejects ambiguous
dual ownership, and removes old-route support only after the live inventory is
zero.

An AI agent requests an external or destructive action. The approval evidence
binds the action fingerprint, target, argument digest, approver, expiry,
decision, and execution result instead of treating a general conversation
approval as reusable authority.

An auditor distinguishes a unique historical record that requires a new
ArchiveEnvelope from duplicate, generated, or zero-consumer material that can
be deleted with provenance and disposition evidence.

## Functional Requirements

| Requirement ID | Requirement | Priority | Verification intent |
| --- | --- | --- | --- |
| REQ-WDTC-001 | Co-locate each live work unit's Spec, Plan, and Task under `docs/03.specs/<NNN>-<slug>/` and retire `docs/04.execution/`. | Must | Every retained execution record maps to `spec.md`, `plan.md`, or `tasks.md` in one work unit, and no live Stage 04 execution route remains. |
| REQ-WDTC-002 | Use stable identifiers or slugs for mutable authored filenames and retain dates in frontmatter; allow dates only when they are part of immutable observation or event identity. | Must | No mutable live PRD, SRS, Interface Requirement, AD, ADR, Spec, Plan, Task, Guide, Policy, or Runbook filename begins with a date; only Stage 90 snapshots and real incidents/postmortems are classified date-identity exceptions, and terminal Stage 98 paths contain no date or year component. |
| REQ-WDTC-003 | Keep `docs/05.operations/` and its guide, incident, policy, and runbook collections at the current stage number. | Must | No `docs/04.operations/` route or link is introduced and every current Stage 05 consumer remains resolvable. |
| REQ-WDTC-004 | Preserve existing lifecycle identifiers, slugs, and reviewed states through terminal form changes and use registry-owned reciprocal relationships for cross-stage lineage. | Must | The exact eight-record ARD-0004 through ARD-0011 source census converts one-to-one to AD-0004 through AD-0011 without renumbering, slug drift, or active/accepted state drift; every current lineage resolves with required reciprocal evidence. |
| REQ-WDTC-005 | Consolidate human authoring rules into disjoint Stage 00 and Stage 99 owners without duplicating machine-owned routes, headings, states, or schemas. | Must | Each rule family has one prose owner and the document-profile registry remains the sole machine contract. |
| REQ-WDTC-006 | Update template forms and support contracts for the approved SDLC, including Stage 03 Plan/Task placement and the date exception policy. | Must | Every physical form has one registry owner and current consumers pass template/profile parity checks. |
| REQ-WDTC-007 | Do not create a Release document type, Release template, releases folder, or release lifecycle in this program. | Must | Registry, templates, indexes, and live operations paths contain no new Release-family owner. |
| REQ-WDTC-008 | Classify retired material before disposition: archive unique history, preserve dated observations, and delete only duplicate, generated, superseded, or zero-consumer material with evidence. | Must | Every removed path has a reviewed archive, successor, provenance, or deletion disposition. |
| REQ-WDTC-009 | Preserve every existing Stage 98 payload byte, digest, original `source_commit`, `source_blob`, and the old ArchiveEnvelope commit/blob while permitting only the reviewed terminal wrapper/path cutover. | Must | The schema-versioned migration ledger distinguishes original-source provenance from `legacy_archive_commit`/`legacy_envelope_blob`, proves a recoverable 93-row bijection, and resolves every path transformation to both evidence sources. |
| REQ-WDTC-010 | Introduce old/new route compatibility before migration and remove old-route support only after an explicit zero-consumer cutover. | Must | Negative fixtures reject uncovered or ambiguous states in both transition and terminal modes. |
| REQ-WDTC-011 | Consolidate validator orchestration and duplicate-purpose scripts without merging validators that enforce distinct contracts. | Must | One declared lane owns selection/orchestration; registry, Markdown, link/owner, security, CI, and archive contracts retain independent evidence where their semantics differ. |
| REQ-WDTC-012 | Retire `validate-harness.sh` only after all consumers migrate, and retain active-corpus or lifecycle validators until rule, consumer, and fixture audits prove retirement safe. | Must | No deleted executable has a live consumer or unique negative fixture; the declared/executable inventory agrees. |
| REQ-WDTC-013 | Extend the existing harness contract, rather than creating a parallel governance registry, with system risk policy, tool/data trust, oversight, stop, approval/trace record shapes, evaluation, and component-provenance controls. | Must | Schema negative tests reject missing high-risk policy or evidence-reference fields and static evidence cannot satisfy runtime-enforcement fields. |
| REQ-WDTC-014 | Distinguish repository-declared, provider-runtime-enforced, hosted-CI, and authorized remote/live evidence states. | Must | No state transition or report promotes evidence across classes without a matching observed record. |
| REQ-WDTC-015 | Rotate the shared progress ledger and remove tracked stale generated graph output only after recoverability and consumer checks pass. | Should | Current memory is bounded, retained history is indexed, generated graph output is reproducible or ignored, and no consumer breaks. |
| REQ-WDTC-016 | Resolve the recorded pre-change validator failures without weakening the corresponding contracts. | Must | The final all-files gate passes with explicit false-positive adjudication and deterministic temporary-directory behavior. |
| REQ-WDTC-017 | Keep PRD-0007 Specs 047–051 suspended until the consolidated topology and validator owners are active, then provide a reviewed resumption route. | Must | No suspended tranche executes during migration and every path is valid at resumption. |
| REQ-WDTC-018 | Keep platform desired state, remote services, credentials, provider runtime, and live cluster changes outside this program. | Must | Handoff reports these evidence classes as not performed or separately deferred. |
| REQ-WDTC-019 | Make PRD, optional SRS, and optional Interface Requirement the terminal active requirement forms and Architecture Description (`sdlc/ad`) plus ADR the terminal active architecture forms; retire ARD and the authored API Spec form while preserving reviewed history and native API-contract evidence. | Must | `docs/02.architecture/descriptions/ad-<id>-<slug>.md` is the only active AD route; WORK-105 converts the exact eight source ARDs one-to-one, leaves zero unconverted current ARDs and zero live/unclassified legacy ARD consumers, separately gates AD-0011 invariant replacement with ADR-0024 acceptance/projection, and proves both zero authored API Spec instances and complete consumer disposition before API Spec retirement. ARD/RFC and authored API Spec then have no active terminal profile, template, route, relationship, or navigation. |
| REQ-WDTC-020 | Require exactly one globally unique, path-derived `artifact_id` on every mandatory terminal outer profile and prohibit the field on every excluded profile/surface. | Must | The closed active, operations, and Stage 98 grammars pass mandatory-presence, prohibited-presence, global uniqueness, canonical token, collision, and path/frontmatter equality fixtures without reallocating an existing numeric identity. |
| REQ-WDTC-021 | Cut the 93 historical Stage 98 records over to stable change and tombstone paths through a schema-versioned migration ledger, while counting migration documents separately. | Must | The current cutover is 93-to-93 with every action `moved`; 76 execution records map to 41 `chg-####` directories and 17 other records map to unique tombstones in the exact `3/8/4/2` split, with no shared stable path. |
| REQ-WDTC-022 | Close the tracked `scripts/` inventory from the current 50 assets to exactly 47 through the reviewed three-asset deletion set only. | Must | WORK-112 removes only `validate-harness.sh` after consumer migration and leaves 49 assets; WORK-114 removes only the transition manifest/tool and leaves 39 Python, seven shell, and one README asset. |

The mandatory terminal outer profiles are PRD, SRS, Interface Requirement,
AD, ADR, Spec, Agent Design, Data Model, Tests, Plan, Task, Guide, Policy,
Runbook, Incident, Postmortem, and Stage 98 Plan, Task, Tombstone, and
Migration. Every declared `artifact_id` participates in one global uniqueness
check. Stage 00 governance/reference, Stage 90 content/reference/observations,
governance memory/progress, Stage 99 support, README, template, fixture,
native/generated, the retired authored API Spec surface, virtual change
aggregate, and embedded archive payload surfaces MUST NOT declare
`artifact_id`; its retired authored template is also outside the terminal
surface. Embedded `original_artifact_id` is provenance
outside the outer namespace. Native OpenAPI/GraphQL/Protobuf identity remains
owned by its separate machine-readable contract and is not a mandatory human
artifact ID.

Authored API Spec retirement has two independent evidence conditions. First,
the tracked authored API Spec instance census must be zero. Second, a
full-repository `git grep` classifier must disposition every
authored-profile reference and leave zero live or unclassified consumers.
Instance zero does not satisfy the consumer condition.

The classifier includes profile/template and relationship surfaces; the
positive Markdown fixture; lifecycle transitions and implementation; registry
allowlists, mappings, and self-tests; the authoring hook and template routing;
current Stage 00 and Stage 03 navigation prose; and validators, tests,
documentation, and fixtures. Each match must migrate to Stage 01 Interface or
a native contract, convert positive API Spec coverage into a terminal
retired-route negative fixture, or be marked `retain-history` / `retain-native`
for immutable history or native evidence. A literal repository-wide match
count may remain nonzero; terminal acceptance requires zero live or
unclassified consumers after the complete classifier.

The former architecture-requirement form retirement is independently closed
over the complete current census
re-authorized after the WORK-104 link-only body updates at review base
`a6fa1806`: active ARD-0004, ARD-0005, ARD-0006, ARD-0007, ARD-0010, and
ARD-0011 plus accepted ARD-0008 and ARD-0009. The numeric-preserving mapping
is exactly ARD-0004 through ARD-0011 to AD-0004 through AD-0011, in order, with
each source filename slug and active/accepted state preserved; ADR-0024 owns
the exact source/target path table. WORK-105 classified every tracked legacy-form
profile/template/route/relationship, lifecycle, registry, navigation,
authoring, validation, test, fixture, skill, issue-form, execution,
operations, and generated-current reference as `migrate-current` or, only for
immutable/explicit history, `retain-history`. Acceptance requires zero
unconverted current legacy-form records and zero live or unclassified legacy-form consumers; literal
historical matches may remain only with reviewed `retain-history` evidence.

The AD-0011 target's archive-invariant replacement, ADR-0024 acceptance, and
PRD-0008 projection change passed as one separate atomic authority gate after
the full eight-record corpus and consumer closure. WORK-108 performs
`artifact_id` backfill only after the
full WORK-105 conversion, so this form migration does not move the identity
backfill earlier in the closed schedule.

The current 93 Stage 98 records need no `API-SPEC` tombstone type. A
later-discovered historical API Spec must be mapped through the reviewed
ledger to a Stage 01 Interface record or an `IFC` tombstone before terminal
acceptance.

The path grammar is closed and deterministic:

| Form | Path-derived identity |
| --- | --- |
| PRD / SRS | `docs/01.requirements/###-<slug>.md` / `srs-###-<slug>.md` maps one record per three-digit typed ID to `PRD-###` / `SRS-###`. |
| Interface Requirement | The complete suffix of `ifc-###-<slug-token>.md` maps to `IFC-###-<SLUG-TOKEN>`; the uppercase token matches `[A-Z0-9]+(?:-[A-Z0-9]+)*`. |
| AD / ADR | Four-digit `ad-####` / decision `####` token maps to `AD-####` / `ADR-####`. |
| Stage 03 | Parent work-unit `###` plus fixed leaf maps to `SPEC-###`, `AGENT-DESIGN-###`, `DATA-MODEL-###`, `TESTS-###`, `PLAN-###`, or `TASK-###`. |
| Guide / Policy / Runbook | Stage 05 four-digit filename token maps to `GUIDE-####`, `POLICY-####`, or `RUNBOOK-####`. |
| Incident / Postmortem | Incident year and three-digit number map to `INC-YYYY-NNN` / `POSTMORTEM-YYYY-NNN`. |
| Stage 98 change leaves | `changes/chg-####-<slug>/plan.md` and `task.md` map to `PLAN-CHG-####` / `TASK-CHG-####`; both leaves carry the parent-derived `change_id=CHG-####`. |
| Stage 98 migration | `mig-####-<slug>.md` maps to `MIG-####` and equal `migration_id`. |
| Stage 98 tombstone | `tmb-<type>-<stable-token>.md` maps to `TMB-<TYPE>-<STABLE-TOKEN>` under the closed stage/type map and token rule. |

The `chg-####` directory has no frontmatter or `artifact_id`; `CHG-####` is a
virtual/path-derived grouping ID. Every present Plan/Task leaf MUST carry that
same parent-derived `change_id`; sibling leaves MUST agree, while each leaf
retains its own globally unique `artifact_id`. The tombstone map is
`01.requirements/{PRD,SRS,IFC}`,
`02.architecture/{AD,ADR}`,
`03.specs/{SPEC,AGENT-DESIGN,DATA-MODEL,TESTS,PLAN,TASK}`, and
`05.operations/{GUIDE,POLICY,RUNBOOK,INCIDENT,POSTMORTEM}`. When embedded
`original_artifact_id` exists, the tombstone stable token is its suffix. When
it is null, the token is
`LEGACY-<SHA256(canonical legacy_path + NUL + source_blob)>` using the full
uppercase digest; the path uses its exact lowercase form.

Canonical comparison ASCII-lowercases the path-derived typed ID and compares
the full token sequence to frontmatter. Validators reject aliases, collisions,
non-canonical case, leading/trailing/double hyphens, a noncanonical repository-
relative POSIX legacy path, or a truncated fallback digest.

Each Stage 98 ledger row requires the seven user fields `legacy_path`,
`stable_path`, `artifact_id`, `action`, `replacement`, `source_commit`, and
`reason`, plus `schema_version`, `migration_id`, `legacy_archive_commit`,
`legacy_envelope_blob`, `source_blob`, `content_sha256`, and `record_kind`.
The seven named fields are required but are not an exclusive field set.
`source_commit` is original-source provenance; `legacy_archive_commit` is the
distinct commit containing the old envelope. The current 93 rows all use
`action=moved`, one source to one unique stable record. Future `merged` or
`replaced` rows retain a unique tombstone and non-null replacement; `deleted`
rows retain a unique tombstone and null replacement. Many-to-one stable paths
are forbidden.

The direct-link validator scans mutable/current registry-selected Markdown
outside Stage 98 and excludes historical observation profiles and embedded
immutable archive payloads. Stage 98's README and migration ledger may link to
individual stable records for index/provenance. Every other current document
may link only to the Stage 98 collection README.

## Success / Acceptance Criteria

| Acceptance ID | Criterion |
| --- | --- |
| ACC-WDTC-001 | Stage 03 is the only live Spec/Plan/Task work-unit owner and `docs/04.execution/` is absent. |
| ACC-WDTC-002 | `docs/05.operations/` remains stable and no Release-family surface is created. |
| ACC-WDTC-003 | Mutable active filenames are date-free, while every date-identity exception is explicit and validated. |
| ACC-WDTC-004 | Registry-owned lineage, route, template, heading, and lifecycle contracts have no competing prose or machine owner. |
| ACC-WDTC-005 | Every removed document or script has a reviewed archive, successor, provenance, consumer, and fixture disposition. |
| ACC-WDTC-006 | Agent governance records risk, trust boundaries, tool-bound approval, oversight, provenance, and evidence depth without claiming provider enforcement from static files. |
| ACC-WDTC-007 | Baseline validator defects and migration regressions are closed; aggregate and all-files repository-static gates pass. |
| ACC-WDTC-008 | Existing archive payloads remain byte-stable and dated observation bodies preserve their historical meaning. |
| ACC-WDTC-009 | Logical-unit commits remain independently reviewable and revertible, with measured before/after inventories. |
| ACC-WDTC-010 | PRD-0007 has a valid consolidated resumption route and no remote or live action is implied. |
| ACC-WDTC-011 | Terminal active requirements and architecture expose only PRD/SRS/Interface Requirement and AD/ADR. The exact eight legacy-form records map to AD-0004 through AD-0011 with preserved slugs/states, zero unconverted current records, and zero live/unclassified legacy-form consumers; the AD-0011 authority gate is atomic. Authored API Spec is retired only after independent zero-instance and complete-consumer-disposition proof, while native API contracts and classified history remain evidence. |
| ACC-WDTC-012 | After WORK-105's complete AD conversion, WORK-108 gives every mandatory terminal outer profile one globally unique, type-valid, path-derived `artifact_id`; every excluded profile, including the retired authored API Spec profile, prohibits it; positive API Spec coverage becomes retired-route negative coverage; native contract identity remains separate; and virtual `change_id` never enters the artifact namespace. |
| ACC-WDTC-013 | All 93 historical Stage 98 records have unique recoverable terminal records under the 14-field ledger contract, immutable payload/provenance, and no terminal date/year path. |
| ACC-WDTC-014 | The exact script sequence is `50 -> 49 -> 47`; all other 47 assets retain their distinct contract, diagnostic, fixture, evidence, or recovery responsibility. |

## Scope and Non-goals

In scope are `docs/**`, the document-profile registry and templates, Stage 00
agent-governance prose and machine contracts, repository-local validation and
orchestration scripts, their tests and fixtures, the shared progress ledger,
tracked generated documentation artifacts, and all affected cross-links and
indexes.

Out of scope are platform behavior and manifests under `gitops/`,
`infrastructure/`, `traefik/`, or `policy/`; provider authentication or
runtime execution; hosted CI settings; credentials or secret values; remote
publication; live cluster mutation; and public release management.

Explicit non-goals are renumbering `05.operations`, removing the numbered
stage-prefix taxonomy, inventing Release/tutorial/explanation families,
renumbering existing lifecycle records, rewriting historical Stage 90
observations, mutating any Stage 98 payload or provenance, moving an existing
Stage 98 path outside the reviewed schema-versioned ledger, or collapsing
semantically distinct validators merely to reduce file count. Legacy architecture-requirement and RFC terminology may
remain as literal historical payload text but have no terminal active document
surface.

## Risks, Dependencies, and Assumptions

| ID | Risk, dependency, or assumption | Owner | Mitigation or validation |
| --- | --- | --- | --- |
| RISK-WDTC-001 | A broad path rewrite can silently corrupt links or create dual ownership. | Platform maintainer | Enumerated `git mv` map, transitional negative fixtures, zero-consumer cutoff, and affected/all-files validation. |
| RISK-WDTC-002 | Archived or dated observation content can be falsified by a global rewrite. | Governance steward | Keep Stage 90 observation bodies and Stage 98 payload/provenance immutable; permit a Stage 98 outer-wrapper/path change only through the reviewed schema-versioned ledger and recovery proof. |
| RISK-WDTC-003 | Script reduction can delete a unique contract behind a similar filename. | Quality engineer | Consumer graph, rule comparison, negative-fixture comparison, and explicit retain/merge/retire disposition. |
| RISK-WDTC-004 | Contract consolidation can turn static declarations into false runtime-readiness claims. | AI agent operator | Separate evidence classes and enforcement availability; require observed provider or action records for promotion. |
| RISK-WDTC-005 | The design could be presented as standards conformance. | Governance steward | Cite only bounded external claims; record every path and filename rule as a local decision. |
| RISK-WDTC-006 | A terminal Stage 98 wrapper/path rewrite could break recovery or silently merge identities. | Governance steward | Require the 93-row bijection, old ArchiveEnvelope Git blob, exact payload/provenance fields, closed ledger actions, and migration/tombstone evidence before cutover. |
| RISK-WDTC-007 | Converting only AD-0011 could strand seven legacy-form records or leave live legacy profile/relationship/navigation consumers. | System architect | Gate WORK-105 on the exact eight-row mapping, complete full-grep classifier, zero unconverted current records, and zero live/unclassified legacy-form consumers; keep the AD-0011 authority gate separately atomic. |
| DEP-WDTC-001 | The document-profile registry and its validators are the migration control plane. | Quality engineer | Tests change before production routes and fail closed on zero or multiple profile matches. |
| DEP-WDTC-002 | Existing baseline gates are not fully green. | Quality engineer | Record failures before edits and close them as named implementation work rather than normalizing failure. |
| ASM-WDTC-001 | Existing identifiers are more valuable than a cosmetically contiguous stage sequence. | Platform maintainer | Human-approved direction A keeps Stage 05 stable and leaves the retired Stage 04 slot unused. |
| ASM-WDTC-002 | [ISO/IEC/IEEE 29148:2018](https://www.iso.org/cms/render/live/en/sites/isoorg/contents/data/standard/07/20/72089.html) supports requirements information but does not mandate this repository's folder names. | Governance steward | Keep requirements traceable and testable while treating physical routing as local architecture. |
| ASM-WDTC-003 | [NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final) practices can integrate with the local SDLC but do not make Markdown or a passing template a security outcome. | Security reviewer | Bind security claims to named controls and separately observable evidence. |
| ASM-WDTC-004 | [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) defines Architecture Description structure/expression and distinguishes architecture from its AD, but does not prescribe recording format or media. | Governance steward | Use Architecture Description as the local term while treating `sdlc/ad`, its route, filename, and ID rules as local decisions. |
| ASM-WDTC-005 | [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) covers requirements-engineering processes and information items without requiring the local PRD/SRS/Interface split. | Governance steward | Keep the three-form split optional where specified and do not claim the folder model is standards-mandated. |
| ASM-WDTC-006 | [ISO/IEC/IEEE 15289:2019](https://www.iso.org/standard/74909.html) supports selecting an organization-appropriate information-item presentation/repository model. | Governance steward | Treat the terminal tree, stable IDs, pairing, and script disposition as human-approved local architecture rather than ISO conformance. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-WDTC-001 | ACC-WDTC-001 | [AD-0011](../02.architecture/descriptions/ad-0011-document-taxonomy-consolidation-architecture.md) and [Spec 052](../03.specs/0052-document-taxonomy-consolidation/spec.md) own the target and migration contract; accepted ADR-0023 remains the transition predecessor and accepted ADR-0024 is the registry projection. |
| REQ-WDTC-002 | ACC-WDTC-003 | N/A — ADR-0024 and Spec 052 own stable filenames and the terminal removal of the Stage 98 date exception. |
| REQ-WDTC-003 | ACC-WDTC-002 | N/A — accepted ADR-0023 records the approved Stage 05 stability target and remains unchanged by the active successor. |
| REQ-WDTC-004 | ACC-WDTC-004 | N/A — ADR-0024 and Spec 052 own the exact eight-record ARD-to-AD mapping and stable registry-lineage boundaries. |
| REQ-WDTC-005 | ACC-WDTC-004 | N/A — Spec 052 owns prose and machine-authority consolidation. |
| REQ-WDTC-006 | ACC-WDTC-004 | N/A — Spec 052 owns template and current-consumer migration. |
| REQ-WDTC-007 | ACC-WDTC-002 | N/A — accepted ADR-0023 records the explicit Release-family exclusion target. |
| REQ-WDTC-008 | ACC-WDTC-005 | N/A — Spec 052 owns disposition classification and evidence. |
| REQ-WDTC-009 | ACC-WDTC-008 | N/A — accepted ADR-0024 and Spec 052 own the bounded wrapper/path supersession while retaining payload/provenance invariants. |
| REQ-WDTC-010 | ACC-WDTC-007 | N/A — Spec 052 owns transitional and terminal validator modes. |
| REQ-WDTC-011 | ACC-WDTC-005 | N/A — Spec 052 owns script and validator reconciliation. |
| REQ-WDTC-012 | ACC-WDTC-005 | N/A — Spec 052 owns consumer and fixture disposition gates. |
| REQ-WDTC-013 | ACC-WDTC-006 | N/A — AD-0011 and Spec 052 own harness-contract extension. |
| REQ-WDTC-014 | ACC-WDTC-006 | N/A — accepted ADR-0023 records the non-promotable evidence-depth decision. |
| REQ-WDTC-015 | ACC-WDTC-009 | N/A — Spec 052 owns memory and generated-output cleanup. |
| REQ-WDTC-016 | ACC-WDTC-007 | N/A — Spec 052 owns the named baseline remediation. |
| REQ-WDTC-017 | ACC-WDTC-010 | N/A — Spec 052 owns suspension and resumption evidence. |
| REQ-WDTC-018 | ACC-WDTC-010 | N/A — AD-0011 owns the local-only system boundary. |
| REQ-WDTC-019 | ACC-WDTC-011 | [Spec 052](../03.specs/0052-document-taxonomy-consolidation/spec.md) owns the exact eight-record AD conversion, complete consumer closure, terminal PRD/SRS/Interface Requirement and AD/ADR form contract, authored API Spec retirement, and native API evidence preservation; accepted ADR-0024 is the registry projection after the atomic AD-0011 invariant gate. |
| REQ-WDTC-020 | ACC-WDTC-012 | N/A — accepted ADR-0024 and Spec 052 own global artifact identity, authored API Spec prohibition, native-contract separation, numeric preservation, and WORK-108 backfill after WORK-105's full AD conversion. |
| REQ-WDTC-021 | ACC-WDTC-013 | N/A — accepted ADR-0024 and Spec 052 own the stable Stage 98 topology and exact 93-row ledger cutover. |
| REQ-WDTC-022 | ACC-WDTC-014 | N/A — Spec 052 owns the reviewed WORK-112/WORK-114 `50 -> 49 -> 47` script disposition. |
