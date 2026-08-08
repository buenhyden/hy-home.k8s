---
title: 'Workspace Document Taxonomy Consolidation Product Requirements'
type: sdlc/prd
status: active
owner: platform
updated: 2026-08-09
---

# Workspace Document Taxonomy Consolidation Product Requirements

## Overview

This program consolidates the repository's SDLC document topology, authoring
rules, templates, agent-governance controls, and validator orchestration into a
single traceable operating model. The human approved the target direction on
2026-08-09: co-locate each work unit's `spec.md`, `plan.md`, and `tasks.md`
under Stage 03; retire `docs/04.execution/`; keep `docs/05.operations/` at its
stable path; and do not create a Release document family or releases folder.

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

PRD-007 remains the product authority for repository delivery assurance, but
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

A reviewer follows registry-owned reciprocal relations from a PRD and ARD to
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
| REQ-WDTC-002 | Use stable identifiers or slugs for mutable authored filenames and retain dates in frontmatter; allow dates only when they are part of immutable observation or event identity. | Must | No mutable live PRD, ARD, ADR, Spec, Plan, Task, Guide, Policy, or Runbook filename begins with a date; Stage 90 snapshots, real incidents, postmortems, and Stage 98 mirrors are explicitly classified exceptions. |
| REQ-WDTC-003 | Keep `docs/05.operations/` and its guide, incident, policy, and runbook collections at the current stage number. | Must | No `docs/04.operations/` route or link is introduced and every current Stage 05 consumer remains resolvable. |
| REQ-WDTC-004 | Preserve existing PRD, ARD, ADR, and Spec identifiers and use registry-owned reciprocal relationships for cross-stage lineage. | Must | No identity is renumbered; every active lineage resolves with required reciprocal evidence. |
| REQ-WDTC-005 | Consolidate human authoring rules into disjoint Stage 00 and Stage 99 owners without duplicating machine-owned routes, headings, states, or schemas. | Must | Each rule family has one prose owner and the document-profile registry remains the sole machine contract. |
| REQ-WDTC-006 | Update template forms and support contracts for the approved SDLC, including Stage 03 Plan/Task placement and the date exception policy. | Must | Every physical form has one registry owner and current consumers pass template/profile parity checks. |
| REQ-WDTC-007 | Do not create a Release document type, Release template, releases folder, or release lifecycle in this program. | Must | Registry, templates, indexes, and live operations paths contain no new Release-family owner. |
| REQ-WDTC-008 | Classify retired material before disposition: archive unique history, preserve dated observations, and delete only duplicate, generated, superseded, or zero-consumer material with evidence. | Must | Every removed path has a reviewed archive, successor, provenance, or deletion disposition. |
| REQ-WDTC-009 | Preserve every existing Stage 98 envelope, payload, digest, and source reference; new archive records are append-only. | Must | Archive validation passes and existing archive-path diffs are zero. |
| REQ-WDTC-010 | Introduce old/new route compatibility before migration and remove old-route support only after an explicit zero-consumer cutover. | Must | Negative fixtures reject uncovered or ambiguous states in both transition and terminal modes. |
| REQ-WDTC-011 | Consolidate validator orchestration and duplicate-purpose scripts without merging validators that enforce distinct contracts. | Must | One declared lane owns selection/orchestration; registry, Markdown, link/owner, security, CI, and archive contracts retain independent evidence where their semantics differ. |
| REQ-WDTC-012 | Retire `validate-harness.sh` only after all consumers migrate, and retain active-corpus or lifecycle validators until rule, consumer, and fixture audits prove retirement safe. | Must | No deleted executable has a live consumer or unique negative fixture; the declared/executable inventory agrees. |
| REQ-WDTC-013 | Extend the existing harness contract, rather than creating a parallel governance registry, with system risk policy, tool/data trust, oversight, stop, approval/trace record shapes, evaluation, and component-provenance controls. | Must | Schema negative tests reject missing high-risk policy or evidence-reference fields and static evidence cannot satisfy runtime-enforcement fields. |
| REQ-WDTC-014 | Distinguish repository-declared, provider-runtime-enforced, hosted-CI, and authorized remote/live evidence states. | Must | No state transition or report promotes evidence across classes without a matching observed record. |
| REQ-WDTC-015 | Rotate the shared progress ledger and remove tracked stale generated graph output only after recoverability and consumer checks pass. | Should | Current memory is bounded, retained history is indexed, generated graph output is reproducible or ignored, and no consumer breaks. |
| REQ-WDTC-016 | Resolve the recorded pre-change validator failures without weakening the corresponding contracts. | Must | The final all-files gate passes with explicit false-positive adjudication and deterministic temporary-directory behavior. |
| REQ-WDTC-017 | Keep PRD-007 Specs 047–051 suspended until the consolidated topology and validator owners are active, then provide a reviewed resumption route. | Must | No suspended tranche executes during migration and every path is valid at resumption. |
| REQ-WDTC-018 | Keep platform desired state, remote services, credentials, provider runtime, and live cluster changes outside this program. | Must | Handoff reports these evidence classes as not performed or separately deferred. |

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
| ACC-WDTC-010 | PRD-007 has a valid consolidated resumption route and no remote or live action is implied. |

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
observations, modifying existing Stage 98 records, or collapsing semantically
distinct validators merely to reduce file count.

## Risks, Dependencies, and Assumptions

| ID | Risk, dependency, or assumption | Owner | Mitigation or validation |
| --- | --- | --- | --- |
| RISK-WDTC-001 | A broad path rewrite can silently corrupt links or create dual ownership. | Platform maintainer | Enumerated `git mv` map, transitional negative fixtures, zero-consumer cutoff, and affected/all-files validation. |
| RISK-WDTC-002 | Archived or dated observation content can be falsified by a global rewrite. | Governance steward | Exclude existing Stage 98 and observation bodies; permit only reviewed indexes, annotations, and append-only archive records. |
| RISK-WDTC-003 | Script reduction can delete a unique contract behind a similar filename. | Quality engineer | Consumer graph, rule comparison, negative-fixture comparison, and explicit retain/merge/retire disposition. |
| RISK-WDTC-004 | Contract consolidation can turn static declarations into false runtime-readiness claims. | AI agent operator | Separate evidence classes and enforcement availability; require observed provider or action records for promotion. |
| RISK-WDTC-005 | The design could be presented as standards conformance. | Governance steward | Cite only bounded external claims; record every path and filename rule as a local decision. |
| DEP-WDTC-001 | The document-profile registry and its validators are the migration control plane. | Quality engineer | Tests change before production routes and fail closed on zero or multiple profile matches. |
| DEP-WDTC-002 | Existing baseline gates are not fully green. | Quality engineer | Record failures before edits and close them as named implementation work rather than normalizing failure. |
| ASM-WDTC-001 | Existing identifiers are more valuable than a cosmetically contiguous stage sequence. | Platform maintainer | Human-approved direction A keeps Stage 05 stable and leaves the retired Stage 04 slot unused. |
| ASM-WDTC-002 | [ISO/IEC/IEEE 29148:2018](https://www.iso.org/cms/render/live/en/sites/isoorg/contents/data/standard/07/20/72089.html) supports requirements information but does not mandate this repository's folder names. | Governance steward | Keep requirements traceable and testable while treating physical routing as local architecture. |
| ASM-WDTC-003 | [NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final) practices can integrate with the local SDLC but do not make Markdown or a passing template a security outcome. | Security reviewer | Bind security claims to named controls and separately observable evidence. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-WDTC-001 | ACC-WDTC-001 | [ARD-0011](../02.architecture/requirements/0011-document-taxonomy-consolidation-architecture.md) and [Spec 052](../03.specs/052-document-taxonomy-consolidation/spec.md) own the target and migration contract; draft ADR-0023 records the human-approved target but does not yet own machine lineage. |
| REQ-WDTC-002 | ACC-WDTC-003 | N/A — the same ARD, ADR, and Spec own stable filenames and explicit date-identity exceptions. |
| REQ-WDTC-003 | ACC-WDTC-002 | N/A — draft ADR-0023 proposes the approved Stage 05 stability target for later lifecycle acceptance. |
| REQ-WDTC-004 | ACC-WDTC-004 | N/A — ARD-0011 owns identifier and registry-lineage boundaries. |
| REQ-WDTC-005 | ACC-WDTC-004 | N/A — Spec 052 owns prose and machine-authority consolidation. |
| REQ-WDTC-006 | ACC-WDTC-004 | N/A — Spec 052 owns template and current-consumer migration. |
| REQ-WDTC-007 | ACC-WDTC-002 | N/A — draft ADR-0023 records the explicit Release-family exclusion target. |
| REQ-WDTC-008 | ACC-WDTC-005 | N/A — Spec 052 owns disposition classification and evidence. |
| REQ-WDTC-009 | ACC-WDTC-008 | N/A — ARD-0011 owns archive inviolability and append-only boundaries. |
| REQ-WDTC-010 | ACC-WDTC-007 | N/A — Spec 052 owns transitional and terminal validator modes. |
| REQ-WDTC-011 | ACC-WDTC-005 | N/A — Spec 052 owns script and validator reconciliation. |
| REQ-WDTC-012 | ACC-WDTC-005 | N/A — Spec 052 owns consumer and fixture disposition gates. |
| REQ-WDTC-013 | ACC-WDTC-006 | N/A — ARD-0011 and Spec 052 own harness-contract extension. |
| REQ-WDTC-014 | ACC-WDTC-006 | N/A — draft ADR-0023 proposes the non-promotable evidence-depth decision. |
| REQ-WDTC-015 | ACC-WDTC-009 | N/A — Spec 052 owns memory and generated-output cleanup. |
| REQ-WDTC-016 | ACC-WDTC-007 | N/A — Spec 052 owns the named baseline remediation. |
| REQ-WDTC-017 | ACC-WDTC-010 | N/A — Spec 052 owns suspension and resumption evidence. |
| REQ-WDTC-018 | ACC-WDTC-010 | N/A — ARD-0011 owns the local-only system boundary. |
