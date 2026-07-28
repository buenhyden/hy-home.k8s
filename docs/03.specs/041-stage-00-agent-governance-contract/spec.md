---
title: 'Stage 00 Agent Governance Contract Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-07-28
---

# Stage 00 Agent Governance Contract Specification

## Overview

This specification defines the foundation for the next workspace agent-governance
program: one provider-neutral machine contract, four provider/local projections,
an explicit four-class project-memory contract, and deterministic consumer
validation. Specs 038–040 are closed. Spec 040 terminal closure
`c5adc27b13893d7cbd1266c9225372cfb7df79e9` and postflight evidence update
`4335ea6076a68fe0bbed3526a21b92a39180faa7` satisfy this tranche's activation
prerequisite.

The external-source observation cutoff is **2026-07-26 Asia/Seoul**. Repository state,
not provider prose, remains runtime authority until each later evidence class
is implemented and observed. This Spec, its reciprocal Plan/Task, their
indexes, the shared progress entry, and the PRD-003 lineage relation form one
exact eight-path activation proposal; no future activation commit identity is
claimed.

## Strategic Boundaries & Non-goals

- **Owns**: the machine-contract shape, schema boundary, consumer migration
  order, provider projection invariants, evidence classes, and the activation
  gate for the PRD-003 / ARD-0006 / ADR-0019 program.
- **Consumes**: the current Stage 00 owner graph, `agent-role-semantics.json`,
  `validation-surfaces.json`, roster validators, provider adapters, and Specs
  038–040 closure evidence.
- **Does not own**: concrete provider installation/authentication, loop runtime,
  role admission, CI cutover, or terminal program closure; Specs 042–046 own
  those responsibilities in sequence.
- **Non-goals**: modifying active adapters during design, merging validation
  routing into the role contract, adding credentials, or deleting the old
  semantics contract before every consumer has migrated.

## Contracts

### Activation and lineage contract

1. Specs 038, 039, and 040 must be `done` with their closure evidence committed.
2. ADR-0019 remains `draft` and ADR-0013 remains the accepted current baseline
   until the new program is implemented.
3. At Spec 041 activation, the registry adds one PRD `003` / ARD `0006`
   program with Specs 041–046 as ordered tranches and accepted ADR `0013` as
   its governing decision. Draft ADR `0019` remains the proposed successor
   linked by PRD/ARD/Spec traceability and may replace that registry relation
   only with its Spec 046 acceptance evidence.
4. Only Spec 041 may own the first execution Plan/Task pair; later tranches
   remain blocked until their predecessor's tranche-owned criteria are `done`.
   Provider-runtime results recorded by Spec 042 may remain explicit
   `ABSENT`, `BLOCKED`, or `DEFER` readiness results without preventing
   repository-local Specs 043–046 from executing or closing. Such results
   cannot support a provider-runtime readiness claim.

### Machine-owner contract

- `docs/00.agent-governance/contracts/harness-contract.json` is the proposed
  single data owner for canonical roles, surface projections, permissions,
  stop conditions, handoff, evidence requirements, and model/eval references.
  It separates `currentInventory` from `targetInventory`: Spec 041 encodes the
  implemented 10-role/three-surface baseline exactly, while the 12-role/four-
  surface target remains pending until Specs 042 and 044 admit it.
- A colocated JSON Schema closes keys, enums, identifier formats, cardinality,
  version compatibility, and provider projection requirements.
- `docs/00.agent-governance/contracts/validation-surfaces.json` remains the
  independent path-to-validation routing owner. Role semantics must reference,
  not absorb, that contract.
- `agent-role-semantics.json` and its schema remain readable compatibility
  inputs until all named consumers select the new version. Spec 045 removes
  them only after a zero-consumer proof.
- The contract references
  `docs/00.agent-governance/memory/progress.md` as the only tracked shared
  project-memory ledger. Provider auto-memory and transient checkpoints cannot
  become current owners for repository facts or execution status.
- The contract declares exactly four memory classes:
  `working-short-term`, `durable-long-term`, `domain-scoped`, and
  `provider-local-auxiliary`. Each class identifies scope, authority role,
  owner, provenance, sensitivity, promotion target, and lifecycle-policy
  references. Provider-local memory is advisory; it cannot own repository
  facts, decisions, task status, or durable handoff evidence.
- Spec 043 owns executable checkpoint promotion, refresh, expiry, archive/GC,
  conflict resolution, redaction, resume, and negative-fixture behavior. No
  provider transcript, full prompt, credential, token, or secret becomes a
  durable memory store.

### Evidence classes

Every result is classified as one of `repo-static`, `provider-runtime`,
`ci`, or `remote-live`. A PASS in one class never implies another class.

## Core Design

### Foundation-first migration

1. Inventory every current semantics consumer, producer, generated summary,
   validator, fixture, provider adapter, and governance reference.
2. Add failing fixtures for contract structure, unknown keys, duplicate roles,
   missing projections, invalid permissions, unbounded stop rules, and version
   incompatibility.
3. Introduce the new contract/schema without changing current runtime claims.
4. Migrate consumers one at a time and record selected contract version plus
   evidence class.
5. Require exact equality for the implemented 10-role/30-adapter baseline and
   reject orphan current members. Record the 12-role/48-adapter target as a
   non-current migration assertion rather than manufacturing missing adapters.
6. Hand the compatibility-removal ledger to Spec 045.

### Projection invariant

Each current canonical role has exactly one projection for each current
surface. A planned role or surface remains an explicit non-current target until
its owning tranche promotes it:

| Surface | Path family | Semantic boundary |
| --- | --- | --- |
| Local / Antigravity | `.agents/agents/*.md` | Local adapter and shared assets; never Gemini-native evidence |
| Claude | `.claude/agents/*.md` | Claude-native metadata and least-privilege tools |
| Codex | `.codex/agents/*.toml` | Codex-native instructions, model, and `model_reasoning_effort` |
| Gemini | `.gemini/agents/*.md` | Planned Gemini-native metadata and project settings consumption; Spec 042 owns admission |

The contract compares shared semantics while provider-specific schemas remain
provider-owned. Unsupported fields are rejected instead of emulated.

## Data Modeling & Storage Strategy

The proposed `harness-contract.json` contains:

- `schemaVersion`, `contractId`, source cutoff, and current owner;
- an ordered canonical role set;
- for each role: purpose, category, responsibilities, inputs, outputs,
  prohibited actions, permission class, stop conditions, handoff targets,
  required evidence, eval suite, and model-routing policy reference;
- an ordered surface set with native path, provider schema, evidence class,
  and per-role projection path, each marked `current` or `target`;
- consumer/version records and compatibility state;
- the canonical shared-memory path and transient checkpoint boundary;
- four explicit memory-class declarations with authority, owner, provenance,
  sensitivity, promotion target, and lifecycle-policy references;
- bounded cardinality assertions and redaction rules.

No credential, token, provider transcript, user configuration, or ignored
diagnostic payload belongs in the tracked contract.

## Interfaces & Data Structures

| Consumer | Required interface | Failure behavior |
| --- | --- | --- |
| Roster validator | Exact role and projection sets | Fail on missing, extra, duplicate, or orphan adapter |
| Semantic validator | Shared role fields and provider projection map | Fail on drift or unsupported provider claim |
| Harness catalog | Derived human-readable roster summary | Fail if prose disagrees with machine owner |
| Provider notes | Native path/schema and evidence boundary | Fail on relabeled local or unverified runtime evidence |
| Model/eval validator | Role policy and referenced eval decision | Fail on unknown model policy or missing fitness evidence |
| CI selector | Agent-governance affected paths | Route to Spec 045 static lane without credentials |

## Edge Cases & Error Handling

- A provider may support a field that another provider lacks; retain the shared
  semantic in the contract and project only schema-supported metadata.
- A new role must not be added to only one surface. Partial projection is a
  failing migration state, not temporary parity.
- A provider runtime can be absent while its tracked projection parses. Record
  repo-static PASS and provider-runtime ABSENT separately.
- A consumer that cannot select the new contract version blocks deletion of
  the compatibility contract but does not justify two current owners.
- A registry update attempted before Spec 040 closure fails the activation gate.

## Failure Modes & Fallback / Human Escalation

- **Current-program collision**: stop; complete Specs 038–040 before modifying
  program lineage or active adapter contracts.
- **Ambiguous owner**: keep the old contract readable, designate the new file
  as non-current, and escalate the ownership decision rather than dual-write.
- **Consumer regression**: revert the smallest consumer migration and retain
  its ledger row; do not weaken schema validation globally.
- **Protected-surface expansion**: require explicit human approval before
  changing permissions, credentials, remote state, or live provider resources.

## Verification Commands

The implementation tranche must introduce and run the focused contract command
before the existing aggregate gates:

```bash
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-agent-role-semantics.py --root .
python3 scripts/validate-agent-roster-currentness.py .
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
bash scripts/validate-repo-quality-gates.sh .
git diff --check
```

`validate-agent-harness-contract.py` is a planned Spec 041 deliverable and is
not claimed to exist in this draft.

## Success Criteria & Verification Plan

- **VAL-SAGC-001**: Specs 038–040 are done before the PRD-003 program is
  enrolled or Spec 041 is activated.
- **VAL-SAGC-002**: The new contract and schema reject unknown keys, invalid
  enums, duplicate roles, missing projections, and unsupported versions.
- **VAL-SAGC-003**: `validation-surfaces.json` remains an independent current
  owner with no duplicated path-routing rules in the harness contract.
- **VAL-SAGC-004**: Every current consumer selects exactly one contract version
  and records deterministic migration evidence.
- **VAL-SAGC-005**: The current inventory is exactly the implemented 10 roles
  and 30 adapters, with no missing, extra, duplicate, or orphan current member;
  the proposed 12/48 inventory is present only as a non-current target.
- **VAL-SAGC-006**: Repo-static, provider-runtime, CI, and remote-live results
  remain separate evidence classes.
- **VAL-SAGC-007**: No credential, token, user config, or raw transcript enters
  the tracked contract or fixtures.
- **VAL-SAGC-008**: Focused validation, strict document checks, repository
  quality gate, and diff checks PASS before tranche handoff.
- **VAL-SAGC-009**: The machine contract declares the four memory classes and
  their authority/provenance/sensitivity/promotion boundaries, while executable
  checkpoint lifecycle behavior remains owned by Spec 043 and sensitive or raw
  transcript content is rejected.

## Traceability

- **Program requirement**: [PRD 003](../../01.requirements/003-workspace-agent-governance-platform.md)
- **Architecture**: [ARD 0006](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md)
- **Proposed decision**: [ADR 0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **Current-program prerequisite**: [Spec 040](../040-contract-cutover-and-program-closure/spec.md)
- **Agent design**: [Agent Design](./agent-design.md)
- **Execution Plan**: [Stage 00 Agent Governance Contract Implementation Plan](../../04.execution/plans/2026-07-28-stage-00-agent-governance-contract.md)
- **Task evidence**: [Stage 00 Agent Governance Contract Task](../../04.execution/tasks/2026-07-28-stage-00-agent-governance-contract.md)
- **Successor**: [Spec 042](../042-provider-native-runtime-and-model-evidence/spec.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-PRD-FUN-10](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-SAGC-002 | Contract/schema negative fixtures prove the closed machine contract. |
| N/A — VAL-SAGC-003 shares the PRD-003 source linked in VAL-SAGC-002 | VAL-SAGC-003 | Routing-owner comparison proves validation routing remains separate. |
| N/A — VAL-SAGC-004 shares the PRD-003 source linked in VAL-SAGC-002 | VAL-SAGC-004 | Consumer migration ledger proves one selected machine owner. |
| N/A — VAL-SAGC-005 shares the PRD-003 source linked in VAL-SAGC-002 | VAL-SAGC-005 | Exact-set validation proves canonical role/projection parity. |
| N/A — VAL-SAGC-006 shares the PRD-003 source linked in VAL-SAGC-002 | VAL-SAGC-006 | Evidence fixtures prove result-class separation. |
| N/A — VAL-SAGC-001 shares the PRD-003 source linked in VAL-SAGC-002 | VAL-SAGC-001 | Dependency validation proves safe program activation. |
| N/A — VAL-SAGC-007 shares the PRD-003 source linked in VAL-SAGC-002 | VAL-SAGC-007 | Redaction fixtures prove sensitive data exclusion. |
| N/A — VAL-SAGC-008 shares the PRD-003 source linked in VAL-SAGC-002 | VAL-SAGC-008 | Focused and aggregate QA prove reviewable handoff. |
| N/A — VAL-SAGC-009 shares the PRD-003 source linked in VAL-SAGC-002 | VAL-SAGC-009 | Contract/schema fixtures prove explicit memory classes, authority boundaries, and the Spec 041/043 ownership split. |
