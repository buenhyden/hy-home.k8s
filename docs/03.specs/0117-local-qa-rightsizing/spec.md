---
title: "Local QA Rightsizing"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0117"
---

# Local QA Rightsizing Technical Specification (Spec)

## Overview

On 2026-10-16 the operator asked for a review of the local full test surface
for checks that are over-applied, duplicated, conflicting or out of step with
the current repository, and for their repair. The audit found eight phase-one
items and one new defect: three focused test modules fail on `main`
`f062294c`, and no selected lane runs them. This Spec owns the phase-one
repairs. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-local-qa-rightsizing.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - the three failing modules `tests/test_completed_state_migration.py`,
    `tests/test_generic_migration_recovery.py` and
    `tests/test_document_lifecycle_cumulative_history.py`;
  - exact version and commit constants in
    `scripts/validate-ci-python-contract.py` that copy the lock file,
    `.pre-commit-config.yaml` and the workflow action references;
  - chart version arguments in `scripts/validation/platform/ingress.py`;
  - prose phrase lists, retired-path denylists and the CODEOWNERS requirement
    in `scripts/validation/repository/quality.py`;
  - registry surfaces for paths that no longer exist and unused lanes or enum
    values in `scripts/validation/registry.json`, with their fixtures;
  - the delivery procedure in `.agents/governance/quality.md`,
    `.agents/governance/git.md` and `.github/repository-surface.md`, which
    omits the required `independent-review` check, and the root README
    description of `.github/`.
- Non-goals:
  - narrowing broad affected-path surfaces and merging duplicate workflow
    security checks (phase two);
  - historical-commit replay tests, the result-reuse mechanism, PR metadata
    byte copies, nginx-specific validators and LAN address pins (separate
    Specs);
  - any change to `.github/workflows/**`, remote protection or credentials.

## Contracts

- A validator checks the shape and consistency of a pinned input, not a
  second copy of its value. Direct requirements must be exact `==` pins that
  agree with the hash lock; every lock entry carries SHA-256 hashes; every
  non-local pre-commit `rev` is a full commit with a `# frozen: <tag>`
  comment; workflow actions are referenced by full commit. Changing a pinned
  value in its own file needs no validator edit.
- Platform validators check the declared structure (repository, chart name,
  namespace, routing values), not the chart version.
- Repository quality checks assert structure. They do not require exact
  sentences of other documents, templates or scripts, and they do not keep
  denylists for paths or phrases that were retired and no longer exist.
- Registry surfaces, lanes and enum values exist only for paths and consumers
  that exist.
- The documented delivery sequence names all three required `main` checks:
  `ci-summary`, `style-pr` and `independent-review`.
- Every focused test module in `tests/` passes on the delivered head.

## Core Design

Each repair removes a duplicate or stale assertion and keeps the protection it
stood for in its single owner: the lock and config files for versions,
`validate-github-actions-security.py` and hosted SHA pinning for action
identity, main protection for review, and the Stage 99 registry for document
form. A failing test is either aligned with the current contract or, when the
behavior it protected was retired, removed with its consumer per
[work lifecycle](../../../.agents/workflows/work-lifecycle.md).

## Data Modeling & Storage Strategy

No new data. Registry and fixture entries are removed, not added.

## Interfaces & Data Structures

Validator command lines and rule IDs stay unchanged; only the failure set
narrows.

## Edge Cases & Error Handling

- A Dependabot or manual bump of a pin: passes when the pin keeps its format
  and the direct and lock files agree.
- A direct pin that disagrees with the lock, a lock entry without a hash, a
  short `rev` or a tag-based action reference: still fails with the existing
  rule ID.

## Failure Modes & Fallback / Human Escalation

Removing an assertion can hide a real regression if its owner does not hold
it. Each removal names the remaining owner in the Task; if none exists, the
item is deferred instead of removed.

## Verification Commands

- `python -m unittest` on each changed or previously failing test module.
- `python3 scripts/qa.py staged` on the exact index of each commit.
- An independent read-only review of the branch.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-QR-001 | The three previously failing modules pass, with each failure classified as a stale test or a product regression and repaired at its root. |
| VAL-QR-002 | `validate-ci-python-contract.py` holds no copied version, commit or action constant; tests show a pin bump passes and malformed pins still fail. |
| VAL-QR-003 | `ingress.py` takes no chart version; tests show a version bump passes and structural drift still fails. |
| VAL-QR-004 | `quality.py` and the registry hold no exact-prose lists, retired denylists, CODEOWNERS requirement, nonexistent surfaces or unused lanes; affected tests pass. |
| VAL-QR-005 | The delivery procedure documents name `independent-review`, and the root README describes `.github/` as it is; selected document checks and review pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QR-001 | Focused tests and staged QA |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QR-002 | Focused tests and staged QA |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QR-003 | Focused tests and staged QA |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QR-004 | Focused tests and staged QA |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QR-005 | Document checks and independent review |
