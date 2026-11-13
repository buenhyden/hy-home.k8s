---
title: "W03 Remove the Layer Frontmatter Key"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0184"
---

# W03 Remove the Layer Frontmatter Key Technical Specification (Spec)

## Overview

This approved change contract closes handoff W03-H25 of the W03 stage of the external v14.7 execution package. The W03 task's metadata table lists `layer` among keys to adopt or remove after their real consumers and need are checked. `layer` repeats the stage folder of its document, and no script reads its value beyond the generic profile-constant check and the template parity rule; on 2026-11-13 the user decided to remove it, except on the accepted ADRs, which are never edited in place and keep it until a successor replaces each (W03-D22). Two freeze gates refuse the edit on frozen records: the package-exit rule R4 refuses any change to the Spec or Plan of a finished package (SPEC-0161), and `REFERENCE_PUBLISHED_REWRITE` refuses any change to a published Stage 90 member other than its status, version, updated and link destinations (13 members). On 2026-11-13 the user chose a one-use exemption in both gates for the `layer` line only, retired when this package closes (W03-D32). SPEC-0181 recorded the key and this migration in `frontmatter_keys`. The [Task](tasks/tsk-0001-w03-remove-layer-key.md) records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03, with W05 for validator code): the frontmatter `layer` line of every tracked Markdown document and template that carries it except accepted ADRs (82 files, this package's three included); `docs/99.templates/registry.json` (profile lists, order and constants, and the `frontmatter_keys` `layer` entry); `scripts/validate-markdown-profiles.py` (a status-conditional rule for `layer`); `scripts/validate-document-contract-registry.py` (the published-rewrite exemption and the `TEMPLATE_OMITTED_KEYS` comment) and `scripts/document_lifecycle.py` (the R4 exemption), each exemption with its retirement in this package's final source commit; the tests and fixtures that write or test `layer` (`tests/test_common_form_tree.py`, `tests/test_task_acceptance_contract.py`, `tests/test_task_execution_contract.py`, `tests/test_native_skill_envelope.py` where `layer:` is an insertion anchor, `tests/fixtures/completion-package.json`, `tests/test_frontmatter_key_contract.py`) and new tests; `.agents/governance/document-authoring.md` line 64, the `layer` mentions of `docs/99.templates/README.md` (the frontmatter list, order, key row with `{{LAYER}}` and template paragraph) and the lifecycle policy and `docs/90.references/AGENTS.md` sentences that state the one-use exemption until it is retired (`docs/03.specs/AGENTS.md` rule 7 names the package-exit check without its rules and needs no change); each edited document's frontmatter `version` and `updated`, except SPEC-0161's Spec and Plan; in the SPEC-0161 Task the W03-D32 row, evidence rows and the frontmatter `version` and `updated` (appended rows only); this package, the Stage 03 README and reviewed `.secrets.baseline` entries.
- Not in this package: the 34 accepted ADRs; ADR-0033, whose "Registry-fixed layer" sentence becomes a recorded stale reference; any body text other than the named policy sentences; other keys; Q-07 numbering (W03-D30); the wider accepted-ADR form exception of W03-D02 (W03-H02).
- No push, PR or merge without the user's approval, which is standing for this work (2026-11-13). Open question: none.

## Contracts

- **Documents.** Every document and template that carries `layer`, except an ADR whose status is `accepted`, loses that one frontmatter line; nothing else changes apart from `version` and `updated` where allowed. Published Stage 90 members change only by the `layer` line and the `version` and `updated` they may already change; SPEC-0161's Spec and Plan change only by the `layer` line.
- **Profiles.** No profile requires, orders or fixes `layer` except the architecture decision profile, where it becomes optional with its order and constant kept. A new rule (`FM-LAYER-ADR`) in the profile check refuses `layer` on any document whose status is not `accepted`; any other profile refuses it as an unlisted key (`FM-KEYSET`). The existing `forbidden` entries stay. `TEMPLATE_OMITTED_KEYS` keeps `layer`, so the ADR template without `layer` keeps parity with its source.
- **Schema.** `frontmatter.schema.json` is unchanged; it keeps the `layer` property that accepted ADRs need.
- **One-use exemptions (W03-D32).** The published-rewrite check also allows deleting the `layer` line, and R4 compares a finished package's Spec and Plan with the `layer` line set aside, nothing else; in both, the whole frontmatter `layer` line including its line ending is set aside, because the change deletes the line, and a body line is never exempted. A finished package's Spec and Plan therefore change by the `layer` line only, with no `version` or `updated` change. Every other change stays refused. Tests show a `layer`-only deletion passing, a naive blanking that leaves an empty line refused, and any other change refused. This package's final source commit, before the Task freezes, removes both exemptions, their tests and the policy sentences that state them, once no `layer` line remains outside accepted ADRs, and the Task records the gates refusing a `layer`-only change again, as the work lifecycle requires for one-use checks.
- **Open packages.** An open package's Spec and Plan change by the `layer` line in the implementation commit; each affected Task gets an appended evidence row with the before and after hashes and the reason (metadata only, no scope change, W03-D22). This package's own first-record receipt carries `layer`, as the profiles require at that time.
- **Key entry.** The `frontmatter_keys` `layer` entry describes it as retained only on accepted ADRs until replaced, with its condition, consumers, migration and tests updated.
- **Policy text.** The document authoring policy and the Stage 99 README no longer list `layer` as a document key and name the accepted-ADR exception; the lifecycle policy and `docs/90.references/AGENTS.md` state the one-use exemption until it is retired.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes and no ADR body changes. The accepted-ADR exception follows Stage 02 `AGENTS.md` rule 3 and W03-D02.

## Data Modeling & Storage Strategy

82 files lose one frontmatter line; 28 profiles stop requiring and 4 stop allowing `layer`, and the ADR profile moves it to optional.

## Interfaces & Data Structures

- `scripts/validate-markdown-profiles.py`: `FM-LAYER-ADR` beside `FM-CANCELLATION` and `INCIDENT-RESOLVED-AT`.
- `scripts/validate-document-contract-registry.py` and `scripts/document_lifecycle.py`: the two one-use exemptions.
- Tests: a non-ADR document with `layer` fails; a proposed or rejected ADR with `layer` fails; an accepted ADR with `layer` passes; a new ADR without it passes template parity; a `layer`-only change to a published member and to a finished package's Spec passes; any other change to either still fails.

## Edge Cases & Error Handling

- SPEC-0181 is implemented and merged before this package starts. If its package is still in the tree, its Spec and Plan change by the `layer` line: under the open-package rule while its Task is open, or under the R4 exemption once its Task is terminal, which works because the exemption lands first. If it has closed, its files have left the tree.
- `tests/test_native_skill_envelope.py` uses `layer:` as an insertion anchor; it is re-based on `updated:`.

## Failure Modes & Fallback / Human Escalation

If any change other than the `layer` line is needed in a frozen record, or any document gains a diagnostic, the author stops and asks the user. If an accepted ADR would need an edit, the author stops and asks the user.

## Verification Commands

- Before and after, record the four strict document validators; diagnostics after must equal those before.
- `git grep -n '^layer: '` lists only the 34 accepted ADRs after the change.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle`, `--suite agent-governance`, `--suite validation-routing`.
- `python3 scripts/validation/repository/quality.py --root .`; markdownlint over the edited Markdown; `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-LAYER-001 | Only the 34 accepted ADRs carry `layer`; the profiles, `FM-LAYER-ADR`, the key entry and the two one-use exemptions match the contract; the tests fail first and then pass. |
| VAL-LAYER-002 | The policy texts are updated, the affected Tasks record the metadata-only edits, validator diagnostics over the tree are unchanged, exact-index QA and the commit hooks pass, and the final source commit retires both exemptions. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LAYER-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Frontmatter and gate tests; the `layer` search. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LAYER-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; exact-index QA; closure retirement. |
