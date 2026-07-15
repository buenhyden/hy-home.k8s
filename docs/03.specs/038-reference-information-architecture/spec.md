---
title: 'Reference Information Architecture Technical Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-07-15
---

# Reference Information Architecture Technical Specification (Spec)

## Overview

This Spec consolidates the authority, currentness, generation, freshness, and
duplicate rules for docs/90.references. It keeps audits, research, data,
generated LLM navigation, learning material, and historical archive records
distinct while preventing any of them from becoming an accidental policy,
plan, runbook, or runtime owner.

## Strategic Boundaries & Non-goals

- **In scope**: docs/90.references and subdirectories, Current-pack pointers,
  remediation overlays, source/freshness metadata, generated-output ownership,
  category indexes, duplicate detection, cross-links, and directly affected
  templates/support rules.
- **Non-goals**: Rewriting dated observation facts, merging snapshots solely
  because topics overlap, defining active governance in references, or
  creating a retrieval/vector runtime.

## Contracts

- Audits own dated implementation observations and a separately maintained
  remediation overlay; exactly one pack is Current.
- Research owns dated external-source synthesis and source ledgers; exactly one
  current research pack may be selected for a program.
- Data owns repo-backed facts, source checks, and refresh triggers.
- llm-wiki owns only deterministic generated canonical-owner navigation.
- Learning owns non-authoritative study roadmaps.
- Archive owns immutable non-current records and is not a reference-policy
  substitute.
- A dated snapshot is not a duplicate merely because a later snapshot exists.

## Core Design

Registry current-pack entries, folder indexes, and generated-output checks
provide one discoverable currentness path. Historical and Resolved packs keep
their bodies and observation SHAs. Current closure changes only remediation
overlays.

Duplicate analysis compares normalized scope, authority claim, source coverage,
generation owner, and current state. It consolidates only duplicate current
owners, generated/manual pairs, and policy text copied into references.

Generated wiki output is accepted only when its tracked file equals generator
output. Manual edits and stale canonical-owner paths fail.

## Data Modeling & Storage Strategy

Reference profiles record role-specific allowed states and body evidence
without adding a universal frontmatter expansion. Source check, observation
date, authority boundary, and refresh trigger remain semantic body contracts
where the profile requires them.

Generated ownership is a registry relation between generator, output, inputs,
and validation command. Data freshness uses explicit triggers rather than an
arbitrary universal expiration date.

## Interfaces & Data Structures

- Current-pack validator: profile, pack ID, members, states, observation SHA,
  index row, and unique Current pointer.
- Source-ledger validator: source URL, checked date, adopted/rejected scope, and
  refresh trigger.
- Generated-output validator: generator path, input roots, output path, and
  no-diff result.
- Duplicate-owner validator: normalized role, scope, lineage, current state,
  and canonical replacement.

## Edge Cases & Error Handling

- A Historical pack containing the word Open does not reopen a finding.
- A Current audit can contain DEFER for live evidence without losing Current
  status.
- A research conclusion that becomes policy must be promoted to its owner and
  linked; the reference remains evidence, not the policy source.
- Generated output missing its tool is SKIP or DEFER according to the owning
  contract, never PASS.
- Learning content may overlap a technical topic but cannot own operational
  instructions.

## Failure Modes & Fallback / Human Escalation

- If two documents claim the same Current scope, stop consolidation until the
  owner and preservation disposition are approved.
- If source currentness cannot be verified, preserve the dated snapshot and
  mark its currentness limitation.
- If a generator is unavailable, validate the tracked contract statically and
  record the missing execution separately.

## Verification Commands

- Run Current-pack, member, index, and observation-SHA checks.
- Run reference profile, source/freshness, and duplicate-owner validation.
- Regenerate llm-wiki and require no diff.
- Run link, repository quality, Markdown, and all-files pre-commit checks.

## Success Criteria & Verification Plan

- **VAL-RIA-001**: Audit and research Current pointers are unique and complete.
- **VAL-RIA-002**: Historical and Resolved observation bodies remain unchanged.
- **VAL-RIA-003**: HEAD closure updates only the remediation overlay and
  affected indexes.
- **VAL-RIA-004**: Data references name source evidence and refresh triggers.
- **VAL-RIA-005**: Generated wiki output has one generator and zero drift.
- **VAL-RIA-006**: Duplicate Current owners, generated/manual duplicates, and
  active-policy copies under references are zero.

## Traceability

- **Foundation**: [Spec 035](../035-document-schema-and-lifecycle-contract/spec.md)
- **Final integrator**: [Spec 040](../040-contract-cutover-and-program-closure/spec.md)
- **Current audit**: [2026-07-11 WEIA](../../90.references/audits/2026-07-11-weia/README.md)
- **PRD**: [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **ARD**: [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-WDLEC-008](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-RIA-001 | Registry and index checks enforce unique Current packs. |
| [REQ-WDLEC-008](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-RIA-002 | Historical-body guard compares observation snapshots with baseline. |
| [REQ-WDLEC-008](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-RIA-003 | Finding-disposition fixtures restrict mutable overlay paths. |
| [REQ-WDLEC-008](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-RIA-004 | Reference body-contract checks verify source and freshness fields. |
| [REQ-WDLEC-008](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-RIA-005 | Generator no-diff validation protects the wiki index. |
| [REQ-WDLEC-008](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-RIA-006 | Duplicate and policy-residue fixtures fail. |
