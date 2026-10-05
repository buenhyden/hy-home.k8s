---
title: "Current Registry Fixture Consumers"
version: "1.0.1"
type: "sdlc/task"
status: "ready"
owner: "platform"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0005"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Current Registry Fixture Consumers

## Overview

This bounded follow-up owns [VAL-P02-005](../spec.md#success-criteria--verification-plan)
and [WORK-005](../plan.md#work-breakdown). The existing hosted complement
failed unit tests because three current fixtures still expect retired
profile/domain declarations. This work follows completed Task0004 and
preserves its narrow validator correction and all completed evidence.

## Inputs

- The user's normal unit-commit, push and merge instruction authorizes the
  necessary scoped fixture repair. The root explicitly assigned these six
  paths to one repo-tooling-engineer writer; quality and review are separate.
- [Plan](../plan.md), [registered Task form](../../../99.templates/templates/specs/task.template.md)
  and [quality policy](../../../../.agents/governance/quality.md).
- Clean Task0004 closing commit `961e6b21277b86f4c9238728e8ca3663d27b0ae1`.
- Existing automatic run `37294064121`, published P01 head `d0f358e8…`,
  complement job `111711030852`; no retry or cancel. Only the observed
  `unit-tests` complement gate failed; pre-commit and other gates passed.
  The clipped output identified five named failures, not a total failure count.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-005 | [VAL-P02-005](../spec.md#success-criteria--verification-plan) | Align current Registry fixture consumers while preserving identity, lifecycle and provenance refusals | repo-tooling-engineer | frontmatter | NOT_RUN | pending | [Observed intake](#observed-intake) |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-040 | [VAL-P02-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Existing hosted failure and bounded named reproduction | Unchanged published Registry and three test consumers | FAIL | [Observed intake](#observed-intake) | pending |
| EVD-P02-041 | [VAL-P02-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Changed-input named GREEN and related controls | Pending implementation bytes | NOT_RUN | [Planned repair](#planned-repair) | pending |
| EVD-P02-042 | [VAL-P02-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Observed draft actual-index staged/message and independent review | Draft tree `2c433586…` | PASS | [Ready prerequisites](#ready-prerequisites) | accepted |
| EVD-P02-043 | [VAL-P02-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Terminal completion and separate review | Pending terminal candidate | NOT_RUN | [Validation boundaries](#validation-boundaries) | pending |

## Approval and Safety Boundaries

- **Allowed Paths**: This Spec, Plan and Task; `tests/test_document_artifact_identity.py`, `tests/test_document_lifecycle_archive_cutover.py` and `tests/test_document_lifecycle_migration.py`. One writer owns these six paths.
- **Forbidden Paths**: Production validators, schemas, Registry, published profiles/domains, validation lanes, hosted configuration, frozen Archive, completed Tasks/evidence, provider/native state, private values and unrelated files.
- **Approval Required**: The existing explicit user commit/push/normal-merge authority and root's bounded necessary fixture delegation apply. The user's conditional terminal-candidate reflection authorization persists: fresh actual checks and separate review must pass before commit. No authentication or native runtime enforcement is claimed.
- **Static Validation**: Existing observed RED is preserved without identical retries. Changed-input named GREEN and meaningful related negatives, scoped pinned hooks, every actual index's canonical staged/message and independent review are required. Prospective completion/review precedes reflected source's fresh staged/completion/message/review. Local full and affected execution remain NOT_RUN under the current exclusion.
- **Live Validation**: DEFER — no cluster or runtime operation requested.
- **Secret / Vault Handling**: Safe path, rule and exception metadata only; no private values or raw sensitive CI output.
- **Rollback Plan**: Reviewed forward correction or revert; no force, rebase, branch deletion, cleanup or local main mutation.
- **Evidence Location**: This Task and external safe receipts; operational absolute argv/cwd stay outside tracked source.

## Verification Summary

### Observed intake

Five exact methods reproduced the observed failures on unchanged inputs,
each under a 60-second bound, without discovery. The identity method
`PathArtifactIdentityTest.test_wrong_but_pattern_valid_ids_fail_for_each_numbered_profile`
raises `KeyError('archive/route-tombstone')`; the published profile is
`archive/route`. Both `DocumentAuthorityLifecycleTests` methods
`test_real_registry_edge_list_accepts_legal_and_rejects_illegal` and
`test_loaded_registry_types_terminal_domains_and_owns_transition_projection`
raise `StopIteration` for retired `requirement-architecture`.
Both `MigrationLifecycleTest` methods
`test_canonical_policy_guard_precedes_pattern_compilation` and
`test_canonical_default_api_and_schema_null_semantics_are_preserved`
raise `StopIteration` in shared setup for retired
`governance-guide-policy-runbook`. That family differs from the authority
failure; the earlier same-family shorthand is corrected here.

Safe reproduction stderr SHA-256 values are
`c6dbb6debfb3f6a9c276a3724fb3fe48b18914e018678a9707998d0c43e2b3a8`
(identity),
`6a9b778a09a98716adeaf873b99f28e0b17c894d17c86856584d745775b505bc`
(authority), and
`7365f561553e9af4e8f5dbf8d9535cf63f721780357b963c08ab799af6587c0b`
(migration). These historical FAIL observations do not revoke completed
Task0003/0004 local acceptance or establish repaired hosted acceptance.

### Planned repair

Use the published `archive/route` key consistently in identity cases and
their exclusion set while preserving wrong-ID refusals. Authority cases
follow current `requirement` review-to-approved and separate
`architecture-description` review-to-active semantics; illegal edges remain
refused. Migration setup already inherits the complete current graph and
declared assets. Adjust its existing governance route for the finite test
paths; retain current membership and remove duplicate declaration additions.
Two pattern/route matrices must look up current `archive/scope-migration`,
while document type mutations retain `archive/migration`. The existing
unmapped-state negative must render its quoted header's actual requested
active or retired state; otherwise its retired case does not mutate bytes.
Preserve policy-before-pattern, default/null, source Git/digest, disposition,
consumer, recovery and negative proof checks. No retired declaration returns.

### Validation boundaries

At draft authoring, implementation, named GREEN, scoped hooks and all current
index outcomes remain unobserved. Quality owns explicitly named identity and
authority controls plus all 25 affected migration setup methods. Independent
review reads each full candidate and actual receipts. Canonical staged runs
retain the existing runner limits and every actually selected gate; manual
named tests use separate bounded invocations. Existing Conftest preparation
and pinned tools are reused without configuration changes.

### Ready prerequisites

Draft commit `9d6fc142227bcc4659c7aae878edc866bdff178c` has tree
`2c4335864b7ae7e67f399bc21bd53419910b99ce`. Its six actual canonical staged
gates, configured message and separate candidate/evidence review passed.
Safe staged stdout SHA-256 is
`9e6d1541834095bbf0cd260709e759d1e92a2a21f0a23706a415337e881891bb`;
outer stderr was empty and all children reported complete output/cleanup.
The actual message fixture SHA-256 is
`032ff0e200d39e52b5b5975cde3c9e9e4c818b7f8eaf5bfd5acfe692ec2c99b2`.
This accepts only that prior draft; the ready index receives fresh checks.

Selection-only canonical preflight of the exact six allowed paths reported
no unmatched path and seven validators: agent-governance,
archive-contract-tests, document-contract-registry, document-lifecycle,
links-and-owners, markdown-profiles and repository-quality. No affected
execution occurred. Existing tools/configuration and runner limits are
unchanged; the selected gates retain their existing prerequisites.
The explicit focused manifest under `.worktrees/proposal/` names four
identity methods, two authority methods and all 25 shared migration setup
methods. These changed-input checks retain the five observed failure cases
and directly affected positive/negative contracts; they are not discovery.
Each named invocation is separately bounded. At this ready transition,
implementation, focused GREEN and required hosted outcomes remain pending.

Normal required exact-head hosted checks precede merge, and automatic
integrated-main checks precede integration acceptance. Remote push waits for
both local follow-ups to finish. The later known-path real-Git cumulative
probe is a private history-proof lane, not full CI or explicit-ref acceptance.
