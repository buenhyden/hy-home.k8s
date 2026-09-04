---
title: "Task: Stage 90 disposition ledger"
version: "1.0.0"
type: "sdlc/task"
status: "done"
owner: "platform"
updated: "2026-08-31"
layer: "specs"
artifact_id: "SPEC-0054-TSK-0007"
---

# Task: Stage 90 disposition ledger

## Overview

This is the completed Spec 0054 Task record for WP-007. The state-only handoff
to SPEC-0054-TSK-0008 is recorded with this terminal state.

## Inputs

- [Common execution contract](../plan.md#common-execution-contract)
- [Spec 0054](../spec.md)
- [Plan 0054](../plan.md)
- [WP-007 execution boundary](../plan.md#wp-007--stage-90-disposition-ledger)

## Task Table

**Plan label:** WP-007

**Depends on:** WP-003

**Current state:** `done`

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-054-007 | VAL-SDLC-008, VAL-SDLC-011, VAL-SDLC-012 | Record the reviewed Stage 90 semantic destinations without mutating evidence or creating a permanent census. | platform | Done | The latest external-research pack is the preservation boundary; every other existing Stage 90 family has a reviewed consumer-first removal disposition. Audit, Research, and Data remain valid Stage 90 roles when a future document has distinct provenance, freshness, and non-authoritative purpose. | `research/0001-workspace-engineering/`: 14 pack files; collection router: one file; `audits/`: 34 files; `data/`: seven files; reference-focused baseline: 122 tests PASS; document/link/quality gates PASS; disposition commit `16a8038`; research commits `5b35d207`, `ab117c49`, `4f2aceb3` |

## Approval and Safety Boundaries

The [common execution contract](../plan.md#common-execution-contract) applies
without exception. WP-007's no-evidence-mutation scope, candidate disposition,
reviews, rollback, and logical commit are owned by its linked Plan section.

## Verification Summary

WP-007 completed after the atomic handoff from WP-003. Direct user approval on
2026-08-31 requires the latest externally researched material under
`docs/90.references/research/0001-workspace-engineering/` to be preserved. Later commit
`e8bb8319` is a mechanical governance cutover and does not supersede the latest
external-research commits `5b35d207`, `ab117c49`, and `4f2aceb3` for recency.
The current tree contains no second research pack. Audit and Data files may be
removed only after active consumers route to canonical owners or direct
repository sources; Git is the default full-body recovery owner and no
redirect or full-body Stage 98 copy is authorized.

The reviewed point-in-time dispositions are:

| Existing family | Disposition | Required consumer cutover |
| --- | --- | --- |
| Stage router, Research router, and `research/0001-workspace-engineering/` | Preserve at the current paths while Spec 0062 consumes the pack. Do not rewrite its external-research bodies during the Audit/Data cutover. | Keep current Spec 0062 provenance links; remove obsolete RIA/llm-wiki validation dependencies separately. |
| `audits/` | Remove the 34 existing bodies after consumer-zero. This does not ban future distinct Audit evidence. | Route current normative claims to Stage 00-05 owners; Requirement `0005` and Architecture Description `0008` are already WP-013 removal candidates after unique-content transfer. |
| `data/` | Remove the seven existing snapshot/control-plane bodies after consumer-zero. This does not ban future distinct Data evidence. | Route ADR and README consumers to current ADR/Architecture/Requirement owners, direct manifests/configuration, or official upstream sources; remove RIA registry/schema pins. |
| `cloud-examples/` | Remove the five snapshot/example bodies after consumer-zero; no replacement Research pack is justified. | Replace navigation and validator path assumptions with direct canonical sources. |
| `learning/` | Remove the two roadmap bodies after consumer-zero. They are neither current external research nor operational procedure. | Do not route them to Stage 05 Guide `0010`, which already owns CI/CD QA reference operations. |
| `llm-wiki/` | Remove both generated projections with the generator and exclusive gates. | Cut over Guide `0009`, Runbook `0011`, Spec 0062 commands, hooks, registry entries, fixtures, and script documentation. |
| Reference information architecture | Remove the module, CLI, schema/current-pack registry, exclusive fixtures, SHA/FSM/census rules, and aggregate overlap. | Preserve only focused semantic checks still needed by the current Research pack, using canonical document/link validators rather than a parallel control plane. |

Read-only baseline verification on 2026-08-31 ran
`python3 -m unittest discover -s tests -p 'test_*reference*.py'`: 122 tests
passed with no Stage 90 evidence mutation. This is pre-cutover regression
evidence, not proof that the obsolete RIA behavior should be retained.

The user-confirmed stage boundary assigns AI-agent governance, roles, and
skills to Stage 00; Requirements, Architecture, and Specs to the coherent SDLC
chain; operational Guides, Incidents, Postmortems, and Runbooks to Stage 05;
workspace Audit, external Research, and Data to Stage 90; historical archive
material to Stage 98; and reusable document forms to Stage 99. A repository
preflight found 794 direct Archive-link-pattern matches across 434 active-stage
files. Those inbound historical dependencies are outside WP-007/WP-008's
Stage 90 mutation scope and are scheduled for current-corpus cutover before
Stage 98 minimization. No active Stage 00/01/02/03/05/90 document may retain or
replace such a link with another Stage 98 citation.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-054-007](../plan.md#wp-007--stage-90-disposition-ledger) | Done. | The preservation boundary, per-family disposition, consumer destinations, and 122-test read-only baseline are recorded. Strict registry, Markdown, link/owner, repository-quality, and diff checks passed; direct human boundary review and execution-owner diff review found no unresolved issue. |
