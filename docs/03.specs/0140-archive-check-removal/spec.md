---
title: "Archive Check Removal"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-03"
layer: "specs"
artifact_id: "SPEC-0140"
---

# Archive Check Removal Technical Specification (Spec)

## Overview

On 2026-11-03 the operator asked to minimize and, where possible, delete
every CI/CD check of the files and entries in `docs/98.archive/`, together
with the migration checks, and then to delete the archived files and keep
only the README and directory structure. A further request on the same day
separates audiences: a README is for human readers and an `AGENTS.md` file is
for AI agents, reflected in the workspace governance and rules.
[ADR-0053](../../02.architecture/decisions/0053-unvalidated-archive.md)
records the decision. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-archive-check-removal.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - the archive and migration validators, their tests, the QA registry
    entries and the pre-commit and Markdown-lint exclusions;
  - the archive and migration branches of the document contract, link,
    lifecycle, Markdown-profile, language and agent-consumer validators;
  - the archive profiles, forms and retention keys of the Stage 99 registry
    and its schemas, and the `archive-cutover` skill;
  - the governance, provider and README text that described the removed
    model, REQ-0003, ADR-0040 and ADR-0053;
  - deleting the files under `docs/98.archive/` except its README, keeping
    the disposition directories, and repointing current links into them;
  - summarizing every deleted archive document in an `Archived Lineage`
    table of the current Stage 01 or Stage 02 document that owns its subject;
  - deleting legacy, deprecated and one-time QA and CI/CD code, tests and
    configuration, and retiring the completed SPEC-0105, SPEC-0106 and
    SPEC-0107 packages whose old Task form kept a legacy validator binding
    alive;
  - refusing the `superseded`, `retired` and `deprecated` states and older
    forms in Stage 01, 02 and 03 profiles, summarizing the documents that
    held them in their current owners, and deleting them;
  - deleting the completed Spec packages SPEC-0108 to SPEC-0139 after their
    durable contracts are promoted to current owners;
  - removing agent-directed text from READMEs, moving folder agent rules into
    folder `AGENTS.md` files, a registry profile for them, and the governance,
    provider and README text that states the split.
- Non-goals:
  - rewriting completed Task evidence or historical ADR and research text
    that describes the earlier model;
  - changing hosted CI, secret scanning, or lifecycle states of current
    documents.

## Contracts

- No registered validator reads `docs/98.archive/**`; a change there selects
  only `secret-handling`.
- No validator records, proves or requires a migration.
- A link into the archive is not checked, not even for existence.
- After deletion the archive tree holds its README and one `.gitkeep` per
  disposition directory.
- A README names no AI agent audience and holds no agent instruction. A folder
  `AGENTS.md` holds the agent rules for its subtree, is English with no
  frontmatter, and is classified by `common/folder-agents-guide`.

## Core Design

The document inventory excludes the archive path once, in
`scripts/document_contracts.py`. Every archive or migration branch that
depended on archive classification or proof is deleted rather than stubbed.

## Data Modeling & Storage Strategy

The Stage 99 registry loses the archive profiles and the retention,
citation, assessment, legacy and migration-admission keys.

## Interfaces & Data Structures

`scripts/validate-archive-integrity.py` and the `archive_*` modules are
removed; no public command replaces them.

## Edge Cases & Error Handling

- The comparison base still holds the old registry keys and archive files;
  the lifecycle gate must read that base without failing.
- A current link into a deleted archive file is turned into plain text where
  the document may change; a completed Task bound to its exact bytes keeps
  its link, which is no longer checked.

## Failure Modes & Fallback / Human Escalation

Recovery of any removed file or check is `git revert` of the change, or
`git show <commit>:<path>` for one file.

## Verification Commands

- `python3 scripts/qa.py staged` on each commit.
- `python3 scripts/run-contract-tests.py --root . --suite <suite>` for the
  document, document-lifecycle, validation-routing, agent-governance and
  tooling suites.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-ARC-001 | No registered validator or test reads or proves archive content or migrations, and the selected QA passes. |
| VAL-ARC-002 | `docs/98.archive/` holds only its README and directory structure, each deleted document is summarized in a current Stage 01 or Stage 02 owner, and the strict link check passes. |
| VAL-ARC-003 | An independent reviewer confirms the change, and the pull request's hosted checks pass. |
| VAL-ARC-005 | No QA, test or CI/CD path keeps a compatibility branch for an older format, generation or pinned historical commit, or checks only a finished one-time transition; no Stage 01, 02 or 03 profile admits a superseded, retired or deprecated state; no completed Spec package remains; and the selected QA passes. |
| VAL-ARC-004 | No README carries agent instructions or an AI agent audience, folder agent rules live in `AGENTS.md`, and the governance states the split. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARC-002 | Tree listing and link check |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARC-001 | Registry, test suites and QA |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARC-003 | Review and hosted checks |
| [REQ-0003-FR-0030](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARC-005 | Contract suites, validators and QA |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARC-004 | README search, registry and link checks |
