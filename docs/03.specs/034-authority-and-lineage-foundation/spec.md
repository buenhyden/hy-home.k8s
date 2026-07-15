---
title: 'Authority and Lineage Foundation Technical Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-07-15
---

# Authority and Lineage Foundation Technical Specification (Spec)

## Overview

This Spec establishes the authority and lineage foundation for the document
lifecycle and evidence program. It reconciles completed Spec 033 with the
accepted seven-tranche decision, normalizes Current audit dispositions against
HEAD evidence, and removes hand-maintained lifecycle facts from non-owning
surfaces before schema and corpus migration begins.

## Strategic Boundaries & Non-goals

- **In scope**: Registry schema and lineage data, PRD-005 and PRD-006 program
  relations, current audit remediation overlay, Stage 00 lifecycle summaries,
  validator fixtures, and reciprocal program links.
- **Historical boundary**: ADR-0016, PRD-005, ARD-0008, completed Specs, Plans,
  Tasks, and observation-time audit facts are not rewritten.
- **Non-goals**: Archive payload conversion, Plan/Task movement, reference-tree
  consolidation, workflow behavior changes, or live validation.

## Contracts

- document-profiles.json remains the sole machine owner of program lineage.
- A program has one PRD, one ARD, an ordered original tranche set, and a
  separately ordered follow-up set.
- Spec 033 is a follow-up to the PRD-005 program; Specs 026-032 remain its
  original tranche set.
- Specs 034-040 are the original tranche set for PRD-006 and ARD-0009.
- Accepted and completed bodies are immutable. New decisions and registry
  relations express later facts.
- The Current audit register records post-observation closure only in its
  remediation overlay.

## Core Design

Registry v6 replaces the single specs array with explicit tranches and
followUps relations. Each relation identifies a Spec number, order, state,
reason, and governing decision. Schema validation rejects duplicate members,
overlap between the two sets, missing decisions, unknown paths, and a follow-up
that precedes its program.

The Current audit overlay gains normalized dispositions for findings whose
repository-static acceptance evidence now exists. Original tables remain
unchanged and live or remote evidence remains DEFER.

Stage 00 may describe lifecycle concepts and point to the registry, but an
exact state or route table outside Stage 99 must either be generated and
validated or reduced to non-authoritative prose.

## Data Modeling & Storage Strategy

The migration is backward-compatible for one tranche: the schema accepts the
legacy programLineage object only in a migration fixture while production data
moves atomically to the v6 shape. No relationship keys are added to document
frontmatter.

Program paths, Spec directories, and decision paths are validated from the
repository tree. Follow-up admission is a closed object rather than an
unstructured note.

## Interfaces & Data Structures

The registry interface exposes:

- program PRD and ARD identifiers;
- original tranches in execution order;
- follow-ups in approval order;
- governing ADR for each relation class;
- status and reciprocal-link validation targets.

Cross-document validation compares registry membership with mutable current
documents and treats immutable accepted/completed bodies as historical
evidence, not editable mirrors.

## Edge Cases & Error Handling

- A Spec cannot be both a tranche and a follow-up.
- A completed follow-up does not reopen the original program.
- A new follow-up without an accepted admission decision fails.
- A historical body mismatch is reported through a successor decision or
  overlay, never fixed by rewriting the body.
- A repo-static closure does not close a live or remote sub-finding.

## Failure Modes & Fallback / Human Escalation

- If v6 lineage cannot be introduced in a green commit, use a narrowly bounded
  compatibility reader and remove it in Spec 040.
- If an audit finding mixes repository-static and live acceptance, close only
  the repository-static portion and retain the live remainder.
- If another program has an undocumented numeric exception, leave it unchanged
  and record a separate follow-up rather than generalizing this decision.

## Verification Commands

- Run the registry self-test and strict route validation.
- Run cross-document owner and reciprocal-lineage validation.
- Run the Current-pack and remediation-overlay checks.
- Run Markdown profile validation and repository quality gates.
- Run pre-commit across all files before the logical commit.

## Success Criteria & Verification Plan

- **VAL-ALF-001**: Specs 026-032 are the only original PRD-005 tranches.
- **VAL-ALF-002**: Spec 033 is a completed follow-up and appears in no original
  tranche set.
- **VAL-ALF-003**: Specs 034-040 form the ordered PRD-006 tranche set.
- **VAL-ALF-004**: Duplicate, overlapping, decisionless, and unknown lineage
  fixtures fail.
- **VAL-ALF-005**: RMD-005, RMD-009, RMD-011, RMD-013, and RMD-032 receive
  evidence-backed overlay dispositions without editing observation facts.
- **VAL-ALF-006**: Stage 00 contains no unvalidated exact lifecycle owner table.

## Traceability

- **PRD**: [Workspace Document Lifecycle and Evidence Consolidation](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **ARD**: [Document Lifecycle and Evidence Operating Model](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- **Lineage decision**: [ADR-0017](../../02.architecture/decisions/0017-program-follow-up-lineage-semantics.md)
- **Current audit**: [2026-07-11 WEIA](../../90.references/audits/2026-07-11-weia/README.md)
- **Successor**: [Spec 035](../035-document-schema-and-lifecycle-contract/spec.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-WDLEC-001](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ALF-001 | Registry fixtures assert the original tranche set. |
| [REQ-WDLEC-002](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ALF-002 | Registry and reciprocal-link checks assert follow-up semantics. |
| [REQ-WDLEC-001](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ALF-003 | Program-lineage validation asserts the new tranche sequence. |
| [REQ-WDLEC-002](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ALF-004 | Independent negative mutations reject invalid membership. |
| [REQ-WDLEC-008](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ALF-005 | Current-pack overlay validation compares finding IDs with HEAD evidence. |
| [REQ-WDLEC-001](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ALF-006 | Duplicate-fact scans reject exact non-owner lifecycle tables. |
