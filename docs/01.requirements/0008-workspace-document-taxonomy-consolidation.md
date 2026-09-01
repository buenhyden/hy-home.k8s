---
title: 'Workspace Document Taxonomy Consolidation Requirement Package'
version: "1.0"
type: sdlc/requirement-package
layer: "01.requirements"
status: active
owner: platform
updated: 2026-09-01
artifact_id: "REQ-0008"
supersedes: "[REQ-0005, REQ-0006]"
---

# Workspace Document Taxonomy Consolidation Requirement Package

## Overview

This program consolidates the repository's SDLC document topology, authoring
rules, templates, agent-governance controls, and validator orchestration into a
single traceable operating model. The human approved the target direction on
2026-08-09: co-locate each work unit's `spec.md`, `plan.md`, and append-only
`tasks/tsk-*.md` records under Stage 03; retain `docs/03.specs/` as that
authority; keep `docs/05.operations/` at its
stable path; and do not create a Release document family or releases folder.

On 2026-08-10 the human also approved the terminal artifact model recorded by
the pre-WORK-104 design package `WDTC-AMEND-001` in accepted
[ADR-0024](../02.architecture/decisions/0024-terminal-artifact-identity-and-archive-layout.md).
Those predecessor PRD/SRS/Interface, prefixed-AD, fixed Archive-census, and
fixed script-count decisions are historical only and are superseded by
[ADR-0030](../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md).
**Current terminal authority** is ADR-0030 together with
[Spec 0054](../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md).
The terminal current forms are a unified Requirement Package, prefix-free
Architecture Description (AD), and ADR. Every declared
`artifact_id` is globally unique; mandatory terminal outer profiles require
one, while excluded profiles prohibit the field. Stage 98 uses minimal
Migration and necessary Tombstone records backed by Git history. Accepted
ADR-0023 remains the transition predecessor. WORK-105 converted the complete
active/accepted ARD-0004 through ARD-0011 source census one-to-one to
AD-0004 through AD-0011, closed every live legacy ARD consumer, installed the
AD-0011 archive invariant, accepted ADR-0024, and
changed the PRD-0008 projection to ADR-0024 as one atomic gate. WORK-104 remains
the existing 82-move and destination Plan/Task rebaseline task.

WORK-105 retired the authored API Spec profile, Stage 03 route, template, and
relationships. Terminal solution-independent interface requirements are
package-scoped `REQ-####-IF-####` members in Stage 01. Native OpenAPI,
GraphQL, and Protobuf profiles/templates remain
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
is recorded in the [Spec-driven SDLC reference](../90.references/research/0001-workspace-engineering/m0004-spec-driven-sdlc-and-document-contracts.md).

REQ-0007 remains the product authority for repository delivery assurance, but
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

A new work unit is created at `docs/03.specs/<NNNN>-<slug>/`; its router,
Spec, Plan, and append-only Task records express one lifecycle without a separate execution
stage or date-based mutable identity.

A reviewer follows registry-owned reciprocal relations from a Requirement Package and AD to
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
| REQ-0008-FR-0001 | Co-locate each live work unit's Spec, Plan, router, and append-only Task records under `docs/03.specs/<NNNN>-<slug>/`. | Must | Every retained execution record maps to `spec.md`, `plan.md`, `README.md`, or `tasks/tsk-*.md` in one work unit, and no live Stage 04 execution route remains. |
| REQ-0008-FR-0002 | Use stable identifiers or semantic slugs for authored filenames and retain dates in frontmatter or observation metadata. Stage 90 packs exist only under `audits/####-<slug>/`, `data/####-<slug>/`, or `research/####-<slug>/`; their slugs are not dates. | Must | No current authored filename begins with a date; each Stage 90 pack uses a category-local four-digit identity and matching category template, while only real Incident/Postmortem routing may retain a year partition. |
| REQ-0008-FR-0003 | Keep `docs/05.operations/` and its guide, incident, policy, and runbook collections at the current stage number. | Must | No `docs/04.operations/` route or link is introduced and every current Stage 05 consumer remains resolvable. |
| REQ-0008-FR-0004 | Preserve existing lifecycle identifiers, slugs, and reviewed states through terminal form changes and use registry-owned reciprocal relationships for cross-stage lineage. | Must | The exact eight-record ARD-0004 through ARD-0011 source census converts one-to-one to AD-0004 through AD-0011 without renumbering, slug drift, or active/accepted state drift; every current lineage resolves with required reciprocal evidence. |
| REQ-0008-FR-0005 | Consolidate human authoring rules into disjoint Stage 00 and Stage 99 owners without duplicating machine-owned routes, headings, states, or schemas. | Must | Each rule family has one prose owner and the document-profile registry remains the sole machine contract. |
| REQ-0008-FR-0006 | Update template forms and support contracts for the approved SDLC, including Stage 03 Plan/Task placement and the date exception policy. | Must | Every physical form has one registry owner and current consumers pass template/profile parity checks. |
| REQ-0008-FR-0007 | Do not create a Release document type, Release template, releases folder, or release lifecycle in this program. | Must | Registry, templates, indexes, and live operations paths contain no new Release-family owner. |
| REQ-0008-FR-0008 | Classify retired material before disposition: retain distinct current authority, preserve observation facts, and delete duplicate, generated, superseded, or zero-consumer material after reviewed consumer and Git-recovery evidence. | Must | Every removed path has a named current owner or an explicit deletion decision in its Task/diff; Git is the default full-body recovery owner and no replacement document is created solely for retention. |
| REQ-0008-FR-0009 | Preserve the declared bytes of retained sealed Stage 98 evidence without making Stage 98 a current-document dependency or requiring parity with ordinary current files. | Must | Sealed records retain their declared integrity checks; current stages contain no Stage 98 links, and routine current moves/deletions recover from Git without a fixed Archive census. |
| REQ-0008-FR-0010 | Use route compatibility only for a bounded transition with a known consumer, then remove it at consumer-zero; do not retain body copies or redirects for routine moves. | Must | Negative fixtures reject ambiguous current ownership, while the terminal tree contains no obsolete compatibility owner or redirect-only document. |
| REQ-0008-FR-0011 | Consolidate validator orchestration and duplicate-purpose scripts without merging validators that enforce distinct contracts. | Must | `scripts/validation/registry.json` is the sole lane and argv owner; the aggregate invokes its `all-files` runner once without embedded validator commands; registry, Markdown, link/owner, security, CI, archive, and repository-wide contracts retain independent evidence where their semantics differ. |
| REQ-0008-FR-0012 | Retire a wrapper only after all consumers migrate, and retain focused validators or manual dispatchers while they own a distinct command or diagnostic contract. | Must | No deleted executable has a live consumer or unique negative fixture; retained wrappers add no rule semantics; the declared/executable graph agrees without a fixed file count. |
| REQ-0008-FR-0013 | Extend the existing harness contract, rather than creating a parallel governance registry, with system risk policy, tool/data trust, oversight, stop, approval/trace record shapes, evaluation, and component-provenance controls. | Must | Schema negative tests reject missing high-risk policy or evidence-reference fields and static evidence cannot satisfy runtime-enforcement fields. |
| REQ-0008-FR-0014 | Distinguish repository-declared, provider-runtime-enforced, hosted-CI, and authorized remote/live evidence states. | Must | No state transition or report promotes evidence across classes without a matching observed record. |
| REQ-0008-FR-0015 | Rotate the shared progress ledger and remove tracked stale generated graph output only after recoverability and consumer checks pass. | Should | Current memory is bounded, retained history is indexed, generated graph output is reproducible or ignored, and no consumer breaks. |
| REQ-0008-FR-0016 | Resolve the recorded pre-change validator failures without weakening the corresponding contracts. | Must | The final all-files gate passes with explicit false-positive adjudication and deterministic temporary-directory behavior. |
| REQ-0008-FR-0017 | Keep lifecycle validation focused on registry-classified profile, state, and allowed edge changes for retained authored documents. Terminal body maintenance, classification-only Reference/router creation, and consumer-zero deletion are governed by semantic/profile validation, link ownership, reviewed Task evidence, and Git recovery rather than ordinary-document byte pins. | Must | Illegal status/profile/edge changes and unproved sealed Archive mutations fail; ordinary current-body corrections and reviewed deletions do not require one Migration, Tombstone, or SHA row per file. |
| REQ-0008-NFR-0001 | Keep REQ-0007 Specs 047–051 suspended until the consolidated topology and validator owners are active, then provide a reviewed resumption route. | Must | No suspended tranche executes during migration and every path is valid at resumption. |
| REQ-0008-NFR-0002 | Keep platform desired state, remote services, credentials, provider runtime, and live cluster changes outside this program. | Must | Handoff reports these evidence classes as not performed or separately deferred. |
| REQ-0008-NFR-0003 | Use one flat Requirement Package profile, prefix-free Architecture Description paths, and ADR authority while preserving predecessor recovery evidence. | Must | Stage 01 has eight `REQ-####` packages; current AD filenames are `####-<slug>.md`; no PRD/SRS/Interface or prefixed-AD current route remains. |
| REQ-0008-NFR-0004 | Require exactly one globally unique, path-derived `artifact_id` on every mandatory terminal outer profile and prohibit the field on every excluded profile/surface. | Must | The closed active, operations, and Stage 98 grammars pass mandatory-presence, prohibited-presence, global uniqueness, canonical token, collision, and path/frontmatter equality fixtures without reallocating an existing numeric identity. |
| REQ-0008-NFR-0005 | Preserve removed current-authority bytes through reachable Git history; retain a bounded Migration only when it supplies unique mapping context not recoverable from the reviewed change itself. | Must | Recovery resolves the removed path from Git, while ordinary documents, working branches, current registries, templates, line numbers, and corpus snapshots are not permanent SHA-pinned inputs. |
| REQ-0008-NFR-0006 | Remove a script only after its consumers, unique rules, and negative fixtures have explicit successor evidence; no fixed script inventory is terminal authority. | Must | Declared consumers and executable inventory agree and no deleted executable retains a live consumer or unique test responsibility. |

The mandatory terminal outer profiles are Requirement Package, prefix-free AD,
ADR, Spec, Plan, append-only Task, Guide, Policy,
Runbook, Incident, Postmortem, Migration, and necessary Tombstone.
Change-local design belongs to Spec and Plan; executable tests remain with
their production module. Every declared `artifact_id` participates in one global uniqueness
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

Current interface requirements use the package-scoped `REQ-####-IF-####`
form, with `REQ-####` equal to the containing Package `artifact_id`. Stage 98
uses only the Spec 0054 minimal recovery topology: a bounded
`migrations/####-<slug>.md` record or a
`tombstones/<original-stage>/####-<slug>.md` lookup. It defines neither a
fixed archive-corpus count nor a separate `API-SPEC` tombstone category.

### Historical predecessor context

The following path-grammar and corpus/cardinality clauses preserve the
WORK-105 through WORK-108 predecessor transition evidence only. They are
non-authoritative for current authoring. ADR-0030, Spec 0054, and the Stage 99
registry own current paths and identities.

The predecessor path grammar was closed and deterministic:

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
distinct commit containing the old envelope. The completed predecessor ledger
snapshot recorded 93 `action=moved` rows, one source to one unique stable
record; that fixed count is historical evidence, not a current corpus claim.
Future `merged` or `replaced` rows retain a unique tombstone and non-null
replacement; `deleted` rows retain a unique tombstone and null replacement.
Many-to-one stable paths are forbidden.

The direct-link validator scans current registry-selected Markdown. Documents
under Stages 00, 01, 02, 03, 05, and 90 neither cite nor cross-link Stage 98;
historical recovery is named as Git history without an Archive path. Stage 98
may maintain bounded archive-internal navigation only.

## Success / Acceptance Criteria

| Acceptance ID | Criterion |
| --- | --- |
| ACC-WDTC-001 | Stage 03 is the only live Spec/Plan/Task work-unit owner; every package has a thin router and package-local Task records, and retired Stage 04 has no live consumer. |
| ACC-WDTC-002 | `docs/05.operations/` remains stable and no Release-family surface is created. |
| ACC-WDTC-003 | Current authored filenames are date-free; Stage 90 pack roots use category-local, number-unique `####-<slug>` identities, contain a regular `README.md` using the matching Stage 99 category template, and dates remain metadata, while the Incident/Postmortem year partition is the only active event-route exception. |
| ACC-WDTC-004 | Registry-owned lineage, route, template, heading, and lifecycle contracts have no competing prose or machine owner. |
| ACC-WDTC-005 | Every removed document or script has a reviewed successor-or-delete decision, consumer-zero evidence, and Git recovery; a tracked Archive replacement is required only for distinct historical value. |
| ACC-WDTC-006 | Agent governance records risk, trust boundaries, tool-bound approval, oversight, provenance, and evidence depth without claiming provider enforcement from static files. |
| ACC-WDTC-007 | Baseline validator defects and migration regressions are closed; aggregate and all-files repository-static gates pass. |
| ACC-WDTC-008 | Retained sealed Archive payloads remain byte-stable and observation bodies preserve their historical meaning after semantic Stage 90 routing. |
| ACC-WDTC-009 | Logical-unit commits remain independently reviewable and revertible, with measured before/after inventories. |
| ACC-WDTC-010 | REQ-0007 has a valid consolidated resumption route and no remote or live action is implied. |
| ACC-WDTC-011 | Terminal active requirements and architecture expose one flat Requirement Package profile, package-scoped FR/NFR/IF members, prefix-free AD paths, and ADR decisions. The exact eight legacy-form records map to AD-0004 through AD-0011 with preserved slugs/states and zero live legacy consumers; native API contracts and classified history remain evidence. |
| ACC-WDTC-012 | After WORK-105's complete AD conversion, WORK-108 gives every mandatory terminal outer profile one globally unique, type-valid, path-derived `artifact_id`; every excluded profile, including the retired authored API Spec profile, prohibits it; positive API Spec coverage becomes retired-route negative coverage; native contract identity remains separate; and virtual `change_id` never enters the artifact namespace. |
| ACC-WDTC-013 | Every removed authority path is recoverable from Git; a minimal Migration/Tombstone exists only for unique lookup value, and no current-file parity, branch identity, or fixed Archive snapshot count is terminal policy. |
| ACC-WDTC-014 | Script inventory is derived from the closed owner/consumer graph; no fixed script count is terminal policy. |
| ACC-WDTC-015 | Lifecycle validation rejects illegal profile/state/edge changes and sealed-evidence mutation without freezing ordinary terminal bodies or blocking reviewed consumer-zero deletions and classification-only Reference/router creation. |

The current implementation uses `scripts/validation/registry.json` for route,
lane, and argv selection. The orchestration-only
`validate-repo-quality-gates.sh` invokes its bounded `all-files` runner once;
focused production validators plus `validation/repository/quality.py` own
distinct and residual rules. Independent top-level tests own synthetic
mutations and fixtures, while production modules neither import nor read them.
Tracked path input, Git output, subprocess output, and execution time are
bounded and fail closed. Transitional Agent wrappers have no current consumer,
and the externally required `agent-governance-static` job name remains stable.
Stage 90 currently retains only the latest external research pack at
`research/0001-workspace-engineering/`; topology tests reject date-based or
loose entries, duplicate category-local numbers, missing pack README files,
non-regular members, and category-template mismatch.

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
| RISK-WDTC-002 | Archived or observation-dated content can be falsified by a global rewrite. | Governance steward | Keep retained sealed Stage 98 payload/provenance immutable; preserve Stage 90 claims and source dates while allowing reviewed semantic pack routing and current-link correction. |
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
| REQ-0008-FR-0001 | ACC-WDTC-001 | [AD-0011](../02.architecture/descriptions/0011-document-taxonomy-consolidation-architecture.md) owns the current Architecture Description; [Spec 052](../03.specs/0052-document-taxonomy-consolidation/spec.md) remains reciprocal predecessor migration evidence. |
| REQ-0008-FR-0002 | ACC-WDTC-003 | N/A — ADR-0024 and Spec 052 own stable filenames and the terminal removal of the Stage 98 date exception. |
| REQ-0008-FR-0003 | ACC-WDTC-002 | N/A — accepted ADR-0023 records the approved Stage 05 stability target and remains unchanged by the active successor. |
| REQ-0008-FR-0004 | ACC-WDTC-004 | N/A — ADR-0024 and Spec 052 own the exact eight-record ARD-to-AD mapping and stable registry-lineage boundaries. |
| REQ-0008-FR-0005 | ACC-WDTC-004 | N/A — Spec 052 owns prose and machine-authority consolidation. |
| REQ-0008-FR-0006 | ACC-WDTC-004 | N/A — Spec 052 owns template and current-consumer migration. |
| REQ-0008-FR-0007 | ACC-WDTC-002 | N/A — accepted ADR-0023 records the explicit Release-family exclusion target. |
| REQ-0008-FR-0008 | ACC-WDTC-005 | N/A — Spec 052 owns disposition classification and evidence. |
| REQ-0008-FR-0009 | ACC-WDTC-008 | N/A — ADR-0030 and Spec 0054 own bounded Git recovery while predecessor payload/provenance invariants remain historical evidence. |
| REQ-0008-FR-0010 | ACC-WDTC-007 | N/A — Spec 052 owns transitional and terminal validator modes. |
| REQ-0008-FR-0011 | ACC-WDTC-005 | N/A — Spec 052 owns script and validator reconciliation. |
| REQ-0008-FR-0012 | ACC-WDTC-005 | N/A — Spec 052 owns consumer and fixture disposition gates. |
| REQ-0008-FR-0013 | ACC-WDTC-006 | N/A — AD-0011 and Spec 052 own harness-contract extension. |
| REQ-0008-FR-0014 | ACC-WDTC-006 | N/A — accepted ADR-0023 records the non-promotable evidence-depth decision. |
| REQ-0008-FR-0015 | ACC-WDTC-009 | N/A — Spec 052 owns memory and generated-output cleanup. |
| REQ-0008-FR-0016 | ACC-WDTC-007 | N/A — Spec 052 owns the named baseline remediation. |
| REQ-0008-FR-0017 | ACC-WDTC-015 | [AD-0011](../02.architecture/descriptions/0011-document-taxonomy-consolidation-architecture.md) owns lifecycle, consumer, and Git-recovery responsibility separation. |
| REQ-0008-NFR-0001 | ACC-WDTC-010 | N/A — Spec 052 owns suspension and resumption evidence. |
| REQ-0008-NFR-0002 | ACC-WDTC-010 | N/A — AD-0011 owns the local-only system boundary. |
| REQ-0008-NFR-0003 | ACC-WDTC-011 | [AD-0011](../02.architecture/descriptions/0011-document-taxonomy-consolidation-architecture.md) describes Requirement Package, prefix-free Architecture, and package-local Task topology under the current authority named above. |
| REQ-0008-NFR-0004 | ACC-WDTC-012 | N/A — ADR-0030, Spec 0054, and the Stage 99 registry own global artifact identity and path/profile parity. |
| REQ-0008-NFR-0005 | ACC-WDTC-013 | N/A — ADR-0030 and Spec 0054 own minimal Git-backed recovery without fixed Archive cardinality. |
| REQ-0008-NFR-0006 | ACC-WDTC-014 | N/A — ADR-0030 and Spec 0054 own consumer-derived script reconciliation without a fixed count. |
