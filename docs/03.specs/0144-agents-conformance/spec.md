---
title: "Agent Surface Conformance"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0144"
---

# Agent Surface Conformance Technical Specification (Spec)

## Overview

On 2026-11-06 the operator asked to check every file under `.agents/`
against its governance, its Stage 99 profile and form, and the current
workspace, and to correct conflicts with the implementation, contradictions
and duplication inside each file. Four read-only audits found about 110
items. The operator chose the correctness-and-code scope: fix conflicts,
contradictions and duplication, and the small code and registry defects with
tests; bind `ops-runbook` to `doc-writer`; remove only the unread registry
schema field. Governance, registry and schema changes need this package. The
[Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-agents-conformance.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - `.agents/governance/`: statements that name a writer, signature,
    checkpoint, coverage target or job that does not exist; the missing PR
    branch-prefix rule; the `kube-linter`, `style-pr` and pre-commit
    exclusion facts; intra-file contradictions; repeated statements of one
    rule inside a file.
  - `.agents/roles/`: the README's draft-to-active path, QA shell-validator
    ownership and plain-text links; stale generated-index wording; provider
    detail inside neutral bodies; duplicated sentences; the supervisor's
    source-of-truth and write-tool wording; missing `supervisor` escalation
    in reviewer handoffs.
  - `.agents/skills/`: wrong commands, paths, headings, tool facts and
    retired names (Vault, Nginx, production); contradictory severity and
    disposition vocabularies; embedded forms that contradict the Stage 99
    profiles; stale metadata; read-only roles told to write.
  - `.agents/README.md`, `knowledge/`, `prompts/`, `workflows/`,
    `evaluations/`: wrong sidecar description, invented Task fields,
    deleted-Task references, missing `_workspace/` row, prompt allowlist and
    Conventional Commit type rules, duplicated handoff detail, missing
    template tables and links.
  - Code and registry: `scripts/prompt-input.py` treats the whitespace
    check's findings as a failure; the `doc-update` owner-candidate pathspec
    misses root routers; `ops-runbook` has no binding role; the schema field
    `permissionClass.external_writes_require_approval` has no reader.
- Non-goals:
  - per-role rewrites of the shared Authority Boundary, Validation and
    Refresh, and Related Documents sections of the 17 role bodies;
  - new Item Index tables in READMEs that the validators accept today;
  - the derived constant fields `supported_providers`, `projections` and
    `providers` in the registry schema;
  - retyping `sdlc.md` from `governance/contract`;
  - CIS benchmark renumbering that needs the external source;
  - any live, hosted or provider-runtime change.

## Contracts

- No `.agents/` statement names a script, command, field, job, writer or
  path that does not exist, or describes a tool's behavior differently from
  its code.
- Each file states each rule once and holds no two statements that
  contradict each other.
- `prompt-input.py` keeps refusing commands outside its allowlist and still
  fails a declared input on an unexpected exit code; the whitespace check's
  findings become draft input instead of an abort.
- The `doc-update` owner-candidate input lists `docs/README.md` and
  `.agents/README.md` as well as nested routers.
- `doc-writer` binds `ops-runbook`, and both provider projections agree with
  the registry.
- The registry schema and registry no longer carry
  `external_writes_require_approval`; approval stays owned by
  `approval-and-safety.md`.
- Every current document still passes the strict document checks.

## Core Design

Correct prose at its owner and keep one statement per rule; where two files
state the same rule, the owner keeps it and the other links. Code changes are
the smallest edits that make the stated contract true, each with a failing
test first.

## Data Modeling & Storage Strategy

`registry.schema.json` loses one property and its `required` entry;
`registry.json` loses its four values and gains one `skill_refs` entry. No
document schema changes.

## Interfaces & Data Structures

`prompt-input.py` gains a per-input set of accepted exit codes for the
whitespace check; its command-line interface is unchanged. The allowlist
gains the two root-router pathspecs for `doc-update`.

## Edge Cases & Error Handling

- Normal: a clean diff yields an empty whitespace section; a diff with
  whitespace errors yields their listing in the draft.
- Error: any other non-zero exit, and any command outside the allowlist, is
  still refused.
- Boundary: a projection that still lacks `ops-runbook` after the registry
  change fails the agent-governance validator.

## Failure Modes & Fallback / Human Escalation

A failing check after a change means a consumer relied on the old text or
value; revert that commit and reopen the item.

## Verification Commands

- `python3 scripts/run-contract-tests.py --root . --suite document`
- the agent-governance and prompt-input unit tests
- `python3 scripts/validate-agent-governance.py --root .`
- the strict registry, Markdown-profile, link and lifecycle checks
- `python3 scripts/qa.py staged` on each commit

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-AGC-001 | The `.agents/governance/` items in scope are corrected; strict document checks PASS |
| VAL-AGC-002 | The `.agents/roles/` and `.agents/skills/` prose items in scope are corrected; strict document checks PASS |
| VAL-AGC-003 | The `.agents/README.md`, `knowledge/`, `prompts/`, `workflows/` and `evaluations/` items in scope are corrected; strict document checks PASS |
| VAL-AGC-004 | Regression tests fail before and pass after the `prompt-input.py`, `ops-runbook` binding and schema-field changes; the agent-governance validator and unit tests PASS |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGC-001 | Strict document checks and independent review |
| [REQ-0003-FR-0010](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGC-002 | Strict document checks, agent-governance validator |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGC-003 | Strict document checks and independent review |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGC-004 | Regression tests red then green |
