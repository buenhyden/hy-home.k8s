---
title: 'Stage 00 Agent Governance Contract Specification'
type: sdlc/spec
status: draft
owner: platform
updated: 2026-07-22
---

# Stage 00 Agent Governance Contract Specification

## Overview

This specification defines the foundation for the next workspace agent-governance
program: one provider-neutral machine contract, four provider/local projections,
and deterministic consumer validation. It is a design record only while Specs
038–040 remain active. Spec 041 may be promoted and enrolled in `programLineage`
only after Spec 040 closes the current PRD-006 program.

The external-fact cutoff is **2026-07-10 10:00 Asia/Seoul**. Repository state,
not this draft, remains the current runtime authority until the tranche is
implemented and reviewed.

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
   program with Specs 041–046 as ordered tranches and ADR `0019` as the
   decision relation.
4. Only Spec 041 may own the first execution Plan/Task pair; later tranches
   remain blocked until their predecessor's tranche-owned criteria are `done`.
   Provider-runtime results recorded by Spec 042 may remain explicit closure
   blockers without preventing repository-local Specs 043–045 from executing.

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

## Traceability

- **Program requirement**: [PRD 003](../../01.requirements/003-workspace-agent-governance-platform.md)
- **Architecture**: [ARD 0006](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md)
- **Proposed decision**: [ADR 0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **Current-program prerequisite**: [Spec 040](../040-contract-cutover-and-program-closure/spec.md)
- **Agent design**: [Agent Design](./agent-design.md)
- **Successor**: [Spec 042](../042-provider-native-runtime-and-model-evidence/spec.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-PRD-FUN-10](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-SAGC-002 | Contract/schema negative fixtures prove the closed machine contract. |
| [REQ-PRD-FUN-10](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-SAGC-003 | Routing-owner comparison proves validation routing remains separate. |
| [REQ-PRD-FUN-10](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-SAGC-004 | Consumer migration ledger proves one selected machine owner. |
| [REQ-PRD-MET-08](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-SAGC-005 | Exact-set validation proves canonical role/projection parity. |
| [REQ-PRD-MET-08](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-SAGC-006 | Evidence fixtures prove result-class separation. |
| [REQ-PRD-FUN-07](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-SAGC-001 | Dependency validation proves safe program activation. |
| [REQ-PRD-FUN-07](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-SAGC-007 | Redaction fixtures prove sensitive data exclusion. |
| [REQ-PRD-FUN-07](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-SAGC-008 | Focused and aggregate QA prove reviewable handoff. |
