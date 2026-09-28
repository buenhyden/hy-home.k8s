---
title: "Archive Lifecycle Standardization"
version: "0.1.1"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-09-28"
layer: "specs"
artifact_id: "SPEC-0100"
---

# Archive Lifecycle Standardization Technical Specification (Spec)

## Overview

Align the current Archive lifecycle explanation, template, routing and existing validators with the accepted [ADR-0040](../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md). The original implementation request dated 2026-09-28 authorized non-destructive repository changes and local verification. Its observed base was `d2296de9ea66ea80c27fcc965c21d552febb057d`; publication is recorded separately in the [Task](tasks/tsk-0001-standardize-archive-lifecycle.md). The common 3.0.0 proposal is an input to assess, not an accepted local decision.

## Strategic Boundaries & Non-goals

This package owns change-specific acceptance and evidence. Durable Archive meaning remains with [document lifecycle](../../../.agents/governance/document-lifecycle.md), machine fields and state transitions with the [Stage 99 registry](../../99.templates/registry.json), and history with Git. Preserve every frozen body and sealed catalog capture row. The original implementation scope did not authorize actual Archive removal, history rewrite, ADR acceptance, incident closure, cluster/service/secret access, remote push or merge; the later publication is recorded in the Task. No new validation engine, duplicate registry, or research pack is needed.

The user approved changing the current Spec/Plan/Task terminal spelling from `done` to `completed` on 2026-09-28. This preserves the terminal meaning and existing transitions; it does not approve a new state, Incident semantics or Archive disposition. Migrate current profiles, transition consumers and live frontmatter together. Admit historical `done` only in explicitly historical validation, and preserve frozen Stage 98 bodies and original Task evidence. `closed` remains a permitted Incident state.

## Contracts

- Recheck accepted ADR-0040's six dispositions, exact whole-unit retention, hold and assessment, one catalog envelope, default-branch source reachability and ordered citation decision at each existing caller. Retain the precedence that denies withdrawn, invalidated or unavailable sources before an Incident evidence exception.
- A terminal unit waits in its current stage until disposition is separately approved. Its members must meet their own terminal criteria; no terminal state grants execution or removal authority.
- Current READMEs route readers to one owner and describe residual obligations with evidence. A historical completed package is evidence, not a current work queue. The current Incident form derives its Current state from frontmatter `status` and points to the registry for allowed values.
- Run relevant repository-static checks and record the exact snapshot, scope, result, skipped or unavailable checks, review disposition and next owner in the [Task](tasks/tsk-0001-standardize-archive-lifecycle.md). Static PASS does not establish provider, hosted CI or live behavior.

### Approved terminal spelling and separate proposals

| Profile family | Current → target | Meaning and transition boundary | Frozen generation and consumers | Decision |
| --- | --- | --- | --- | --- |
| `spec-plan` | `done` → `completed` | Keep terminal acceptance meaning; replace the `active` → `done` edge with `active` → `completed` and retain all other edges and disposition approval | Preserve archived `done` bytes; update current Registry, validators, guidance and live instances together | User approved 2026-09-28; verify migration |
| `task` | `done` → `completed` | Keep Task execution completion distinct from Spec acceptance and cancellation; replace `in-progress` → `done` with `in-progress` → `completed` | Preserve archived Task bytes and original Commit Ledgers; historical Task table results are separate evidence | User approved 2026-09-28; verify migration |
| `incident` | `closed` retained or mapped after review | `resolved` is currently nonterminal and `closed` terminal; they are not synonyms. Decide closure evidence and bundle disposition before any map | Preserve resolved bundles and Postmortems; update incident profile, form, bundle validator and consumers only if decision changes semantics | Deferred to a new accepted ADR |
| `governance-guide-policy-runbook` | `active`, `superseded`, `retired` unchanged | `active` is a current publication state, not an execution phase | No rewrite to sealed governance history | No change proposed |
| Archive assessment | `withdrawn` unchanged | Evidential judgment differs from document lifecycle `withdrawn` | Assessment rows and citation decision remain independent | No change proposed |

The migration inventory found 11 live frontmatter `done` values and 492 frozen Stage 98 values. Only the live values change. Historical validators may normalize `done` for a frozen body or prior Git generation, while a current `done` must fail. ADR-0040 already decides Archive disposition semantics; Incident state mapping and new conditional metadata are not adopted without a demonstrated need.

## Core Design

Reuse the existing Archive disposition, document lifecycle, links/owners and QA gates. Reproduce an actual discrepancy before a scoped code repair, then exercise the smallest regression case. Update current explanations, the single Incident form and affected navigation together. Do not change an accepted architecture meaning through a validator-only edit. The [Plan](plan.md) orders inspection, scoped repair, current-document edits and final verification.

## Data Modeling & Storage Strategy

Keep the current Stage 98 Retention Catalog and Assessment as the only per-unit management records. A row absent from Assessment retains the registry's `unreviewed`/`retained` defaults; a row present retains its evidence and Hold. Source Git objects and the envelope commit, path and mode are verified under the accepted contract. This change adds no persistent state store or historical catalog row.

## Interfaces & Data Structures

The existing [frontmatter schema](../../99.templates/contracts/frontmatter.schema.json), registry profiles and validation runner remain the machine interfaces. Current Spec/Plan/Task initial statuses are `draft`/`draft`/`queued`; their approved terminal spelling is `completed` after the coordinated migration. Incident metadata's human Current state points to frontmatter `status`; there is no separately authored state value. Permitted values come from `operation/incident` in the registry. The Archive citation table remains the single ordered admission decision.

## Edge Cases & Error Handling

Treat a missing source object, shallow history, unreachable default-branch source, changed index, a removed unit and catalog row hidden in a target-reachable ancestor (including merge ancestry), partial package, zero tested units, absent required tool and contradictory assessment as failures or explicit DEFER according to the owning gate. An unrelated branch is not an ancestor and cannot supply a phantom baseline. A valid approved `git-history-only` whole-unit removal remains admitted, without restoring the payload. A withdrawn, invalidated or history-only unit stays uncitable even for an Incident. Do not infer current authority from retained evidence, and do not count a past Task's PASS as this run's PASS.

## Failure Modes & Fallback / Human Escalation

If a desired change needs a new state meaning, a removal approval or a protected action, leave that contract intact and hand the exact proposed diff, decision and verification need to the responsible owner. Failed full QA keeps acceptance open. Roll back only the reviewed current files by a forward correction; do not reset or alter frozen history.

## Verification Commands

Use `python3 scripts/qa.py quick --root . --base-ref HEAD` for the affected working tree and `python3 scripts/qa.py full --root . --base-ref HEAD` for the final full tree. Run targeted existing tests for any changed validator and `git diff --check`; if a logical commit is authorized, staged QA checks the exact index separately. Command results, counts and tool limits belong in the Task after execution, not in this goal contract.

## Success Criteria & Verification Plan

| ID | Acceptance contract | Evidence |
| --- | --- | --- |
| VAL-ARC-001 | Current policy, registry, schema and each existing caller agree with ADR-0040 without changing accepted meaning | Bounded source/consumer map and focused regression results |
| VAL-ARC-002 | Current incident form and README routing have one status/list owner and preserve unresolved obligations | Profile, links/owners and reviewer check |
| VAL-ARC-003 | Frozen generations and catalog capture rows remain unchanged; source and whole-unit checks remain strict | Git diff, lifecycle/archive cutover and fixture evidence |
| VAL-ARC-004 | Common S01–S16 and V01–V40 are dispositioned against actual repository owners and executed tests, with exclusions explained | Task evidence and explicit decision handoff |
| VAL-ARC-005 | Ordered targeted, quick and full repository QA and independent review report exact PASS/FAIL/SKIP/DEFER | Task command and snapshot record |
| VAL-ARC-006 | Approved Spec/Plan/Task `completed` spelling is implemented across current profiles, transitions, validators and instances; frozen `done` and historical evidence remain valid and unchanged; other state and field proposals stay separate | Consumer inventory, focused current/historical fixtures, profile and lifecycle checks, frozen-path diff |

### Document impact

| Owner or document family | Disposition | Reason and Task owner | Acceptance |
| --- | --- | --- | --- |
| REQ-0003 and AD-0006 current text | Change only stale SPEC-0054 unfinished wording | This Task; preserve narrowed open REQ-0004 obligations | VAL-ARC-002 |
| ADR-0040 and document lifecycle policy | Keep accepted Archive meaning; state the approved terminal spelling at the current policy owner | This Task; architect owns any new semantic decision | VAL-ARC-001, VAL-ARC-006 |
| Stage 99 registry, schema and validators | Migrate current terminal spelling and historical compatibility at existing owners; repair reproduced enforcement defects | This Task and tooling owner | VAL-ARC-001, VAL-ARC-003, VAL-ARC-006 |
| Incident template and current stage/AD READMEs | Change duplicate or stale current guidance | This Task; wiki-curator owns navigation | VAL-ARC-002 |
| REQ and ADR decision READMEs | Change stale SPEC-0054 work pointer and duplicate ADR navigation | Wiki-curator; retain narrowed open REQ-0004 obligations | VAL-ARC-002 |
| Stage 98 frozen units and sealed catalog capture rows | Keep byte-for-byte | No removal approval exists | VAL-ARC-003 |
| Research pack 0002 and SPEC-0099 | Keep separate owners | Existing Archive research and workspace engineering refresh already own their topics | VAL-ARC-004 |
| SPEC-0095–0098 provider/retention work | Keep historical scope and evidence | Their closed or active contracts do not authorize this state migration | VAL-ARC-004 |

## Traceability

This directly requested conformance work adds no solution-independent requirement or structural decision. [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md), [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) and ADR-0040 are current upstream context; the [Plan](plan.md) and [Task](tasks/tsk-0001-standardize-archive-lifecycle.md) own execution order and observed evidence.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARC-001 | Existing Archive retention/citation gates and reviewed source map |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARC-003 | Exact retention and whole-unit regression |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARC-004 | S/V disposition and Task evidence |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARC-005 | QA registry lanes and Task evidence |
| N/A — direct scoped request of 2026-09-28; no new Requirement Package | VAL-ARC-002 | Template/profile review |
| N/A — direct scoped request and state approval of 2026-09-28; no new Requirement Package | VAL-ARC-006 | Current and historical migration checks |
