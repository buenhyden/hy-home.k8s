---
title: "Dead Profile Mode Cleanup"
version: "0.1.1"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0143"
---

# Dead Profile Mode Cleanup Technical Specification (Spec)

## Overview

On 2026-11-06 the operator asked to clean up the dead modes that SPEC-0142
left as a follow-up. The document loader still types two profile modes and
one frontmatter mode that no registry value can produce, and three validators
keep branches that only those modes reach. A validator code change is
executable behavior, so this package owns it. The [Plan](plan.md) orders the
work and [Task 0001](tasks/tsk-0001-dead-profile-mode-cleanup.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - the profile modes `frontmatter-free` and `classification-only` in the
    `DocumentProfile.mode` type of `scripts/document_contracts.py`;
  - the frontmatter mode `not-applicable` in `FrontmatterContract.mode`,
    which the loader never produces: it maps the registry's `required` to
    `required` and every other value to `forbidden`;
  - the branches that test those values in
    `scripts/validate-markdown-profiles.py` and
    `scripts/validation/repository/quality.py`, and the helper code that only
    they used.
- Non-goals:
  - the schema and registry, which already allow only the five current
    profile modes;
  - other uses of the word `not-applicable` (validation-lane fallbacks,
    platform assurance, lifecycle messages), which are separate domains;
  - accepted ADR text that mentions frontmatter-free READMEs.

## Contracts

- The typed profile modes equal the schema's `mode` enum: `authored`,
  `router`, `template`, `native` and `non-target`.
- The typed frontmatter modes are `required` and `forbidden`, the two values
  the loader produces.
- GitHub-native YAML under `.github/ISSUE_TEMPLATE/` and `.github/workflows/`
  is still refused when it starts with the five-key SDLC frontmatter.
- Every current document still passes the strict document checks.

## Core Design

Remove only values and branches that no registry input reaches. Each removed
branch is guarded by a condition that is always false, so the remaining code
paths and their diagnostics stay the same.

## Data Modeling & Storage Strategy

No data, schema or registry change.

## Interfaces & Data Structures

No command-line interface changes. Two `Literal` types narrow; the private
helper `_is_native_candidate_path` drops its unused `registry` parameter.

## Edge Cases & Error Handling

- Normal: every current document and form validates as before.
- Error: a GitHub-native YAML file with an SDLC envelope is still refused
  with `FM-FORBIDDEN`.
- Boundary: a future profile mode must be added to the schema and the type
  together, or the new regression test fails.

## Failure Modes & Fallback / Human Escalation

A failing document check after the change means a path relied on a removed
branch; revert the implementing commit and reopen the scope.

## Verification Commands

- `python3 scripts/run-contract-tests.py --root . --suite document`
- the strict registry, Markdown-profile, link and lifecycle checks
- `python3 scripts/validation/repository/quality.py`
- `python3 scripts/qa.py staged` on each commit

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-DPM-001 | A regression test shows the typed profile and frontmatter modes differ from the schema and loader before the change and match after it |
| VAL-DPM-002 | No `frontmatter-free`, `classification-only` or frontmatter `not-applicable` branch remains in the scripts; the document suite, strict document checks and repository quality check PASS |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DPM-001 | Type regression test |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DPM-002 | Code search, document suite and strict document checks |
