---
title: "Repository Vocabulary"
version: "1.0.1"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0163"
---

# Repository Vocabulary Technical Specification (Spec)

## Overview

This approved change contract creates the Repository Vocabulary that requirements GOV-01, R45-08 and R147-09 of the external v14.7 execution package ask for: `.agents/knowledge/glossary.md` becomes the single owner of shared term meanings, while each policy keeps its operating rules. The package's `REPOSITORY-VOCABULARY` contract (`repository-vocabulary` v14.5) supplies the 33 common terms and the form. Today the meanings sit in the `Shared terminology and ownership` table of the [SDLC contract](../../../.agents/governance/sdlc.md), and [ADR-0036](../../02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md), the context-and-memory policy, the wiki-curator role, the knowledge-map skill and the knowledge validator all declare `.agents/knowledge/` a pointer-only surface. The user ruled on 2026-11-12 that current v14.7 requirements prevail over conflicting rules ([SPEC-0161](../0161-w00-v14-7-delta-intake/spec.md) Task, EVD-018), so this change amends that pointer-only rule for exactly one file. [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) gains the requirement. The [Plan](plan.md) orders the work; [Task 0001](tasks/tsk-0001-repository-vocabulary.md) records evidence and acceptance.

## Strategic Boundaries & Non-goals

- In scope, by writer:
  - W01: `.agents/knowledge/glossary.md` (new); REQ-0003 new FR-0032, its Traceability row and a back-link; the `.agents/governance/sdlc.md` table; `.agents/governance/context-and-memory.md` pointer-surface sentence; `.agents/knowledge/README.md`; new ADR-0058 amending ADR-0036 Decision 3 and the decision index `docs/02.architecture/decisions/README.md`.
  - W03: `docs/99.templates/registry.json` (profiles `governance/vocabulary` and `common/template-governance-vocabulary`, both in the `governance-operations` lifecycle domain; `governance/knowledge` excludes `glossary.md`); template `docs/99.templates/templates/governance/vocabulary.template.md`; `docs/99.templates/README.md` and `docs/99.templates/templates/README.md`.
  - W05: `scripts/validate-knowledge-surface.py`, `tests/test_validate_knowledge_surface.py`, `scripts/README.md` row.
  - W07: `.agents/roles/wiki-curator.md` authority sentence and `.agents/skills/knowledge-map/SKILL.md` step 2.
  - This package, the Stage 03 README and reviewed `.secrets.baseline` digests.
- Out of scope: the common H2/H3 forms of other roles, DOC-09, CI-SCOPE and DOC-12.
- The glossary defines terms and names the role and path that own each rule; it restates no approval step, command, transition or check algorithm. Rows of the SDLC table that carry rules keep them in `sdlc.md`; only neutral meanings move.
- ADR-0036 keeps its body; ADR-0058 amends only the knowledge clause of Decision 3. ADR-0058 needs the user's acceptance, which Spec approval does not give.
- No push, PR or merge without separate approval.
- Open question: none.

## Contracts

- The glossary is English, with H1 `Repository Vocabulary` and the H2s `Purpose`, `Scope`, `Normative Language`, `Repository Vocabulary`, `Local Extensions`, `Maintenance` and `References`, in that order. `Normative Language` declares the RFC 2119 and RFC 8174 reading of capitalized MUST, MUST NOT, SHOULD and MAY and says the words grant no authority.
- The `Repository Vocabulary` table has the columns `Term ID | Term | Korean | Definition | Not to Confuse | Policy Owner | Contract Version`. It holds the 33 common terms with the package IDs, terms, Korean names and meanings translated without change of sense. Policy Owner keeps the package owner role and adds the local path in backticks. Contract Version is `repository-vocabulary v14.5`.
- `Local Extensions` uses the same columns for repository terms, including the neutral meanings moved from the SDLC table; it never reuses a common Term ID.
- The knowledge validator routes `.agents/knowledge/glossary.md` by file name to a vocabulary check instead of the pointer check. It reads both tables and refuses a missing common table (`KNOWLEDGE-VOCABULARY-EMPTY`), a Term ID not matching `TERM-[A-Z0-9-]+` (`KNOWLEDGE-TERM-ID`), a repeated Term ID across both tables (`KNOWLEDGE-TERM-DUPLICATE`), a named path that does not exist (`KNOWLEDGE-PATH-MISSING`) and a twelve-word span copied from a named owner (`KNOWLEDGE-DUPLICATED-SPAN`). Word matching counts Hangul as well as Latin letters, so Korean text is compared too.
- That all 33 common IDs are present is checked once in the Task against the package contract, not by the validator, so the validator carries no copy of the contract's ID list.
- ADR-0058 states that `.agents/knowledge/` holds pointer documents and exactly one vocabulary document, which defines meanings and states no rule.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view and is unchanged. ADR-0058 amends ADR-0036 the way ADR-0057 amended ADR-0056. The glossary is a governed knowledge document with its own profile because its required headings differ from the pointer form. Wiki-curator keeps owner maps; doc-writer writes the glossary.

## Data Modeling & Storage Strategy

The glossary is Markdown with the six-key governance front matter and `type: governance/vocabulary`. No data store.

## Interfaces & Data Structures

Registry profiles `governance/vocabulary` (path `^\.agents/knowledge/glossary\.md$`, template `docs/99.templates/templates/governance/vocabulary.template.md`) and `common/template-governance-vocabulary` (that template path). REQ-0003-FR-0032: a single Repository Vocabulary owns the meaning of shared governance terms under stable term IDs, each linked to the policy that owns its rules, and policies do not redefine those terms.

## Edge Cases & Error Handling

- A term whose package owner role has no current file keeps the nearest current owner path and says so; no file name is invented.
- Pointer documents keep their current checks; the Hangul word change can surface a new copied span in them, which is then fixed in that document.
- A Local Extension that reuses a common Term ID is a duplicate.

## Failure Modes & Fallback / Human Escalation

If a definition cannot avoid a twelve-word span from its owner, the definition is reworded, never the owner. If the user does not accept ADR-0058, the glossary and its profile are not committed and the package stops with that decision recorded.

## Verification Commands

- `python3 scripts/run-contract-tests.py --root . --suite <suite holding tests/test_validate_knowledge_surface.py>`, with the new tests shown failing before the validator change.
- `python3 scripts/validate-knowledge-surface.py --root .` on the tree.
- An inline check that the glossary's common IDs equal the package contract's 33 IDs.
- The strict document validators, the staged lifecycle check and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-VOCAB-001 | The glossary has the required headings and columns, the 33 common IDs equal the contract set, every owner path resolves, and the knowledge validator passes on the tree. |
| VAL-VOCAB-002 | New tests fail before and pass after the validator change for a missing table, a bad Term ID, a duplicate Term ID, a missing owner path and a copied span in Latin and in Hangul; existing knowledge tests still pass. |
| VAL-VOCAB-003 | ADR-0058 is accepted; the SDLC table keeps every rule and links the glossary; the registry routes the glossary to the new profile; the pointer-only owners name the vocabulary exception; the strict document checks and commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0032](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-VOCAB-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), [ADR-0036](../../02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md), [ADR-0058](../../02.architecture/decisions/0058-repository-vocabulary-in-knowledge-surface.md) | Knowledge validator and inline ID check. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-VOCAB-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Direct negative tests in the contract suite. |
| [REQ-0003-FR-0032](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-VOCAB-003 | [ADR-0036](../../02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md), [ADR-0058](../../02.architecture/decisions/0058-repository-vocabulary-in-knowledge-surface.md) | ADR acceptance, strict document checks and commit hooks. |
