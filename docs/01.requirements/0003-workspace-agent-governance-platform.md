---
title: "Workspace Agent and Document Governance Requirements"
version: "1.6.7"
type: "sdlc/requirement"
status: "active"
owner: "platform"
updated: "2026-09-26"
layer: "requirements"
artifact_id: "REQ-0003"
---

# Workspace Agent and Document Governance Requirements

## Overview

This document owns the current user requirements for agent execution and document governance. The
[common role registry](../../.agents/roles/registry.json) owns the machine truth of roles and skills,
[Common governance](../../.agents/README.md) owns the human execution rules, and
[Stage 99](../99.templates/README.md) owns document form. The current governance and common QA implementation is owned by
[ADR-0036](../02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md) and
[SPEC-0072](../03.specs/0072-agent-governance-and-quality-gate-consolidation/spec.md);
the wider document convergence and unfinished dispositions are owned by [Spec 0054](../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md).
This Requirement is not a copy of the implementation inventory, the provider roster, or a one-off migration plan.

## Vision

Operators must be able to judge a task's responsibility, allowed scope, current document authority, and actual evidence depth consistently,
and to resume a reviewable change safely.

## Problem Statement

Copying policy, machine contracts, and execution history into several documents splits the boundary between current support and unfinished work.
A static declaration must not be mistaken for runtime evidence, and past program counts must not be used as current admission criteria.

## Personas

- Maintainer: manages owners without duplication and changes that can be recovered.
- Agent operator and implementer: work within the approval, stop, and handoff boundaries.
- Reviewer and quality engineer: review contracts, failure meaning, and evidence depth with their roles kept separate.

## Key Use Cases

- A worker finds the role, skill, and approval owner in the current Registry and execution policy.
- A failed task stops and resumes safely after a checkpoint without sensitive data and a bounded retry.
- A document changer hands over current consumers and preserves decision history and sealed evidence.
- A reviewer separates local static results from external observation and links unfinished work to the next Task.

## Functional Requirements
- **REQ-0003-FR-0001**: Common Agent, Skill, Rule, Hook, Workflow, checkpoint, QA, and document policy must each have one current owner per responsibility.
- **REQ-0003-FR-0002**: Provider gateways and adapters must express only native syntax and capability differences, without copying common policy.
- **REQ-0003-FR-0003**: Skill provenance must distinguish repo-local, shared, provider-native, and explicitly requested external skills, and must not assume a missing skill is executable.
- **REQ-0003-FR-0004**: Work must link to the relevant process, branch, document, QA, DevOps, CI/CD, security, and Kubernetes scope and approval owner.
- **REQ-0003-FR-0005**: The Plan/Task handoff of a repository change must record the commands run, results, limits, remaining work, and approval boundaries.
- **REQ-0003-FR-0006**: A document's purpose and form must follow its repository form owner, and an external format must not be used as a substitute authority without separate approval.
- **REQ-0003-FR-0007**: Least privilege, secret non-disclosure, GitOps-first, and the explicit approval boundary for external, live, and destructive work must be preserved.
- **REQ-0003-FR-0008**: Projection must include only currently admitted provider surfaces, and a planned or absent surface must not count as current support.
- **REQ-0003-FR-0009**: Provider-native metadata must be kept distinct from repository document form, and static form conformance must not be promoted to evidence of discovery, authentication, or runtime enforcement.
- **REQ-0003-FR-0010**: The machine registry of roles and skills must define semantics, projection, permission, stop, handoff, and validation responsibility within one ownership boundary.
- **REQ-0003-FR-0011**: Repeated agent execution must provide bounded retry, a no-progress stop, safe checkpoint, compaction, and resume, and escalation; the loop contract must own the limits.
- **REQ-0003-FR-0012**: A single document machine owner must define document routes, profiles, metadata, form, and lifecycle edges, and prose policy must live only with its responsibility owner.
- **REQ-0003-FR-0013**: Each physical document form must map to exactly one profile, and its template and validator must agree.
- **REQ-0003-FR-0014**: Requirements, Architecture, Spec/Plan/Task, operations documents, References, and READMEs must each keep their purpose and must not copy execution detail or unobserved operational evidence into higher documents. Stage 05 keeps its position, and this convergence creates no Release family.
- **REQ-0003-FR-0015**: A document disposition must first hand over its unique current meaning and consumers, preserve observed facts and original Git recovery, and then proceed within a reviewed scope.
- **REQ-0003-FR-0016**: Affected-path, lane, and argv routing must have a single machine owner, and the failure meanings of validators that check independent contracts must not be merged.
- **REQ-0003-FR-0017**: CI must keep its intended independent evidence lanes, a complete aggregate verdict, least privilege, immutable external Action identifiers, and artifact retention boundaries. Local validation is not reported as a hosted run.
- **REQ-0003-FR-0018**: Changes must be delivered as logical commits with independent review, proportionate full validation, and reversible boundaries.
- **REQ-0003-FR-0019**: The package-local Plan/Task owns execution state and order, and must not distort the original tranche, follow-up, and succession history or copy it into a permanent central roster.
- **REQ-0003-FR-0020**: Completed packages, documents superseded by a successor, documents withdrawn without a successor, and closed incident records must be told apart by their actual lifecycle and kept with their whole body; a retired route or a moved scope must name its current owner without a body. Git history handles original recovery, with no second recovery ledger, and frozen sealed bodies and their provenance are not rewritten. The current evidential value of a retained copy is judged by an appraisal kept separate from the original text; only an approved unit whose retention need, consumers, and retention obligations are resolved is removed whole from the current tree, while its catalog identity and Git recovery remain. ADRs are no exception, and a retained copy cannot become current authority or input for reactivation.
- **REQ-0003-FR-0021**: Audit, research, data, generated output, and learning material must state their basis, observation time, and owner, and must not substitute for current policy or execution approval.
- **REQ-0003-FR-0022**: Scratch and checkpoints must stay bounded, secret-free temporary state, and durable execution evidence must be left in the Task. The removed shared progress ledger is not restored as a new current owner.
- **REQ-0003-FR-0023**: Stable document identities and semantic filenames must be kept, and the identity rules, uniqueness, and path correspondence of mandatory/excluded profiles must be validated. Identifiers in existing decision history are not reassigned.
- **REQ-0003-FR-0024**: A compatibility layer, wrapper, or script must be kept only while it has a real consumer and a unique rule or negative fixture, and must be removed after succession evidence and consumer-zero.
- **REQ-0003-FR-0025**: The agent system's risk, tool/data trust, oversight, stop, approval, trace, evaluation, and component provenance obligations must be implemented and validated in the current `.agents/roles/` Registry and `.agents/governance/` owners. A static declaration does not prove runtime enforcement.
- **REQ-0003-FR-0026**: Repository-declared, provider-runtime, hosted-CI, and approved remote/live evidence must be kept apart and must not be promoted into one another without observation.
- **REQ-0003-FR-0027**: Lifecycle validation must judge profile, state, and allowed edges, while ordinary body corrections and consumer succession are judged by semantic/link validation and reviewed Git recovery. Integrity checks of the sealed Archive stay separate.
- **REQ-0003-FR-0028**: Malformed input, a missing tool, fallbacks, risky paths, and forbidden actions must have deterministic direct negative tests, and a required-tool failure must not be hidden as a diagnostic SKIP.
- **REQ-0003-NFR-0001**: Roster and adapter counts must be derived from the current Registry, and role and surface admission and model fitness must be justified by local need, least privilege, and evaluation evidence.
- **REQ-0003-NFR-0002**: Targeted, affected, staged, full unit, all-files, and formatter/diff revalidation must check the same required contracts while recording each result and change snapshot.
- **REQ-0003-NFR-0003**: Document form and change decisions must be traceable to their primary basis, applicable scope, and validation evidence, and must not confuse an external standard with a repository convention.
- **REQ-0003-NFR-0004**: A discovered baseline defect is handled without weakening the contract, and a false-positive verdict, an environment limit, or an unresolved failure must not be hidden as success.
- **REQ-0003-IF-0001**: A migration must deliver the current owner switch, reciprocal links, and cleanup of stale claims and orphan consumers in the same review unit.
- **REQ-0003-IF-0002**: An external role catalog is only the provenance of an idea, never admission or policy authority.

## Success / Acceptance Criteria

Each member of the Lifecycle Traceability below is judged by the validation of its linked Architecture and implementation owner.
The current role/skill projection, document routes, identity, and lifecycle, consumer ownership, the bounded loop, and
the protected QA contracts are validated with positive/negative fixtures. Provider-runtime and hosted/live results
are not reported as PASS without their observation, and each limitation has an owner and a retry condition.

- **Acceptance criterion 01**: The owner graph of common policy, machine contracts, and execution evidence is connected.
- **Acceptance criterion 02**: The trace across REQ-0003, AD-0006, the current ADRs, and approved Spec/Plan/Task is kept.
- **Acceptance criterion 03**: Gateways are thin projections and keep native, static, and runtime evidence distinct.
- **Acceptance criterion 04**: The relevant repository static quality gate passes after the change.
- **Acceptance criterion 05**: No unapproved external format replaces the repository form owner.
- **Acceptance criterion 06**: The role and surface projections derived from the current Registry agree.
- **Acceptance criterion 07**: Provider readiness is judged only by its secret-free canary PASS, and ABSENT/DEFER carries a limit, an owner, and a retry trigger.
- **Acceptance criterion 08**: Consistency of the machine schema, metadata, and projections is validated.
- **Acceptance criterion 09**: Recovery fixtures validate retry, stop, checkpoint, compaction, and resume, and the exclusion of sensitive data.
- **Acceptance criterion 10**: Evidence exists for each role's input/output, permission, stop, handoff, eval, and model fitness.
- **Acceptance criterion 11**: Results of the required local/CI lanes, full QA, and formatter/diff revalidation are traceable.
- **Acceptance criterion 12**: Current surfaces carry no duplicate authority, stale claim, or orphan consumer, and actual runtime limits are preserved.

## Scope and Non-goals

In scope: current owner boundaries, approval, document lifecycle, validation responsibility, and execution handoff.
Out of scope: new provider admission, vendoring an external role catalog, collecting secrets, live changes, or creating a Release family.
The removed shared progress ledger and the past proposal's `agentSystems`/`evidenceOwnerPolicies` are not
claimed as current implementation or restored as a new parallel registry. FR-0025's ongoing obligations are validated at their current owners.

## Risks, Dependencies, and Assumptions
The relevant owners update concrete provider/model availability and authentication evidence. A static file is not runtime discovery.
This document does not separately pin the number of roles or providers, retry constants, or validator argv.
It follows the current boundaries of [ADR-0030](../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md),
[ADR-0031](../02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md), and
[ADR-0040](../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md).
- Model availability, effort enums, CLI schemas, and authentication change. A concrete value must be proven together by the
  official source at the reference time and an authenticated canary; inferring from names is forbidden.
- Native Claude/Codex format support is not equated with an account's actual execution permission.
- Provider credentials are not placed in GitHub-hosted CI. The authenticated canary runs in a local/manual
  evidence lane and records only secret-free results.
- The Task and Git own work, validation, and handoff. No separate automatic checkpoint file is made mandatory,
  and credentials or full transcripts are not stored.
- ADR-0019 and ADR-0013 are superseded historical decisions that preserve predecessor execution and the
  external-lane limitation. ADR-0036 and SPEC-0072 own the current governance location and the QA/CD boundary. ADR-0034 is a superseded decision that passed that boundary to ADR-0035, and ADR-0035 passed it to ADR-0036.

### Agent execution and approval requirements

- **Allowed Actions**: Inspect current owners, edit approved repository scope, and run non-destructive local validation.
- **Disallowed Actions**: Read secret values, invent runtime evidence, restore obsolete governance owners, or mutate external/live systems without approval.
- **Human-in-the-loop Requirement**: Obtain approval for destructive Git, external actions, provider authentication, deployment, or secret handling.
- **Evaluation Expectation**: Preserve independent review, stable-snapshot validation results, failure limitations, and package-local unfinished ownership.

### Unfinished execution and original lineage

Spec 0054 closed as `done` through WP-013 and TSK-0013 and is kept in `98.archive/completed/`.
Spec 0049 depended on the retired Spec 0048 and the Traefik lane and was withdrawn on 2026-09-25 ([SPEC-0089](../03.specs/0089-deferred-conflict-resolution/spec.md)); it is kept in `98.archive/retired/` and not cited ([SPEC-0090](../03.specs/0090-spec0049-retirement/spec.md)). Its unimplemented scope (render, schema, policy, secret, shell fixture, image, and tool evidence lanes) remains an ownerless gap of REQ-0004-FR-0008 and FR-0010; the next owner is the request owner who plans a new package under current authority.
Specs 0047, 0048, 0050, and 0051 were withdrawn without successors, are kept in `98.archive/retired/`, and are not cited
([SPEC-0087](../03.specs/0087-stage03-terminal-package-retention/spec.md)).
[REQ-0004](./0004-current-local-gitops-platform.md) co-owns the platform-specific obligations.

The original REQ-0005/0006 were superseded by REQ-0008. Their current meaning passes back to this document,
but that does not mean the original decisions were written for REQ-0003. Past fixed tranche/corpus counts,
Spec 033's follow-up distinction, and the ARD→AD identity conversion are history, not current roster rules.
REQ-0006's Plan/Task-only retention and REQ-0008's ban on every Stage 98 link are superseded by ADR-0038's dispositions and ADR-0039's ordered citation table. Sealed records remain outside current authority.

Current governance and QA implementation is owned by
[SPEC-0072](../03.specs/0072-agent-governance-and-quality-gate-consolidation/spec.md).
Provider-native execution scope, capability-to-model binding, and write-path
guard parity are owned by
[SPEC-0073](../98.archive/completed/03.specs/0073-provider-native-enforcement-parity/spec.md).
Shared write-guard ownership, patch-envelope parsing, and enforcement
honesty are owned by
[SPEC-0074](../98.archive/completed/03.specs/0074-provider-write-guard-ownership-and-enforcement-honesty/spec.md).
Common knowledge and prompt surfaces and their document contracts are
owned by
[SPEC-0075](../98.archive/completed/03.specs/0075-common-knowledge-and-prompt-surfaces/spec.md).
Responsibility-boundary coverage, the roles that close it, and routing
completeness are owned by
[SPEC-0076](../98.archive/completed/03.specs/0076-agent-role-coverage-and-contract-completion/spec.md).
Retirement of unreachable validation code, absent-subject assertions, and
same-snapshot duplicate gate execution is owned by
[SPEC-0077](../98.archive/completed/03.specs/0077-dead-contract-and-duplicate-execution-retirement/spec.md).
Reconciliation of document statements that drifted from the implementation,
and of Stage 03 lifecycle state that lagged completed work, is owned by
[SPEC-0078](../98.archive/completed/03.specs/0078-document-currency-reconciliation/spec.md).
The six-disposition Archive stage, its derived citation rule, and the move of
the registry routes, archive forms, and validators to that model are owned by
[SPEC-0079](../98.archive/completed/03.specs/0079-six-disposition-archive-stage/spec.md).
The first disposition under that model, which retains ADR-0032 and resolves
frozen Stage 98 links to a retained source, is owned by
[SPEC-0080](../98.archive/completed/03.specs/0080-adr-0032-retention-pilot/spec.md).
Retaining the fifteen remaining superseded decisions is owned by
[SPEC-0081](../98.archive/completed/03.specs/0081-superseded-decision-retention/spec.md).
The unit archive retention contract that ADR-0039 adopts, its cutover, and the
first exact disposition are owned by
[SPEC-0082](../98.archive/completed/03.specs/0082-unit-archive-retention-contract/spec.md).
Retaining the ten finished Stage 03 packages under that contract, and
recording why the two superseded proposals cannot follow, is owned by
[SPEC-0083](../98.archive/completed/03.specs/0083-finished-package-retention/spec.md).
Closing the Stage 03 backlog those rounds left, including the two registry gaps
that blocked two of its dispositions, is owned by
[SPEC-0084](../98.archive/completed/03.specs/0084-stage03-backlog-closeout/spec.md).
The archive reappraisal and verifiable-source contract that ADR-0040 proposes,
its cutover, the index navigation corrections, and the ordered lifecycle and
result vocabulary work are owned by
[SPEC-0085](../03.specs/0085-archive-reappraisal-and-document-standards/spec.md).
The operator-authorized native-runtime observation of Claude and Codex that
SPEC-0072 left open is owned by
[SPEC-0086](../03.specs/0086-provider-native-runtime-observation/spec.md).
Retaining the seven terminal Stage 03 packages that SPEC-0084 left in place is
owned by
[SPEC-0087](../03.specs/0087-stage03-terminal-package-retention/spec.md).
Converging Operations document ownership, disposing of Stage 98 Operations
residue, and removing dead or duplicate validation logic is owned by
[SPEC-0088](../03.specs/0088-operations-corpus-convergence/spec.md).
Resolving the conflicts SPEC-0088 deferred and withdrawing open packages that
contradict current authority is owned by
[SPEC-0089](../03.specs/0089-deferred-conflict-resolution/spec.md).
Retaining the withdrawn SPEC-0049 package in `retired/` is owned by
[SPEC-0090](../03.specs/0090-spec0049-retirement/spec.md).
Constraining every README to its direct children under one registry
navigation contract is owned by
[SPEC-0091](../03.specs/0091-readme-navigation-contract/spec.md).
Stating each document's language in one registry contract is owned by
[SPEC-0093](../03.specs/0093-document-language-contract/spec.md).

## Traceability

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-0003-FR-0012 | A single document machine owner must define document routes, profiles, metadata, form, and lifecycle edges, and prose policy must live only with its responsibility owner. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0013 | Each physical document form must map to exactly one profile, and its template and validator must agree. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0014 | Requirements, Architecture, Spec/Plan/Task, operations documents, References, and READMEs must each keep their purpose and must not copy execution detail or unobserved operational evidence into higher documents. Stage 05 keeps its position, and this convergence creates no Release family. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0015 | A document disposition must first hand over its unique current meaning and consumers, preserve observed facts and original Git recovery, and then proceed within a reviewed scope. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0016 | Affected-path, lane, and argv routing must have a single machine owner, and the failure meanings of validators that check independent contracts must not be merged. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0017 | CI must keep its intended independent evidence lanes, a complete aggregate verdict, least privilege, immutable external Action identifiers, and artifact retention boundaries. Local validation is not reported as a hosted run. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0018 | Changes must be delivered as logical commits with independent review, proportionate full validation, and reversible boundaries. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0019 | The package-local Plan/Task owns execution state and order, and must not distort the original tranche, follow-up, and succession history or copy it into a permanent central roster. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0020 | Completed packages, documents superseded by a successor, documents withdrawn without a successor, and closed incident records must be told apart by their actual lifecycle and kept with their whole body; a retired route or a moved scope must name its current owner without a body. Git history handles original recovery, with no second recovery ledger, and frozen sealed bodies and their provenance are not rewritten. The current evidential value of a retained copy is judged by an appraisal kept separate from the original text; only an approved unit whose retention need, consumers, and retention obligations are resolved is removed whole from the current tree, while its catalog identity and Git recovery remain. ADRs are no exception, and a retained copy cannot become current authority or input for reactivation. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0021 | Audit, research, data, generated output, and learning material must state their basis, observation time, and owner, and must not substitute for current policy or execution approval. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0022 | Scratch and checkpoints must stay bounded, secret-free temporary state, and durable execution evidence must be left in the Task. The removed shared progress ledger is not restored as a new current owner. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0023 | Stable document identities and semantic filenames must be kept, and the identity rules, uniqueness, and path correspondence of mandatory/excluded profiles must be validated. Identifiers in existing decision history are not reassigned. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0024 | A compatibility layer, wrapper, or script must be kept only while it has a real consumer and a unique rule or negative fixture, and must be removed after succession evidence and consumer-zero. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0025 | The agent system's risk, tool/data trust, oversight, stop, approval, trace, evaluation, and component provenance obligations must be implemented and validated in the current `.agents/roles/` Registry and `.agents/governance/` owners. A static declaration does not prove runtime enforcement. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0026 | Repository-declared, provider-runtime, hosted-CI, and approved remote/live evidence must be kept apart and must not be promoted into one another without observation. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0027 | Lifecycle validation must judge profile, state, and allowed edges, while ordinary body corrections and consumer succession are judged by semantic/link validation and reviewed Git recovery. Integrity checks of the sealed Archive stay separate. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0028 | Malformed input, a missing tool, fallbacks, risky paths, and forbidden actions must have deterministic direct negative tests, and a required-tool failure must not be hidden as a diagnostic SKIP. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0001 | The common governance and owner graph validate as a single current source. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0002 | Provider gateways keep the thin adapter boundary. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0003 | Skill provenance and missing gaps are machine-validated. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0004 | Every strategy axis and scope owner can be found. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0005 | A repo-changing handoff leaves its evidence and limitations. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0006 | Template, profile, and cross-link checks pass. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0007 | No GitOps, secret, privilege, or external-action guardrail is violated. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0008 | Registry-admitted surfaces carry native claims separate from the common semantics. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0009 | Schema, model, effort, MCP, and each admitted provider's independent canary record are validated. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0010 | The machine harness contract/schema validates every role and adapter. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0011 | The bounded runner's timeout, output, child cleanup, and no-progress handoff are validated by Task evidence. | [SPEC-0072](../03.specs/0072-agent-governance-and-quality-gate-consolidation/spec.md) |
| REQ-0003-NFR-0001 | Registry-derived role/adapter parity and eval/model fitness are validated. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-NFR-0002 | Quick, staged-index, final-tree, and CI common QA keep their input boundaries and failure propagation distinct. | [SPEC-0072](../03.specs/0072-agent-governance-and-quality-gate-consolidation/spec.md) |
| REQ-0003-IF-0001 | No legacy or orphan current owner remains on an active surface. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-IF-0002 | An external role idea is admitted only after it passes a local gap and an eval. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 01 remains acceptance-only | The common `.agents/` owner graph links without contradiction. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 02 remains acceptance-only | A reciprocal Requirement Package→AD→ADR→Spec→Plan/Task chain exists. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 03 remains acceptance-only | Gateways do not copy policy and keep evidence classes distinct. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 04 remains acceptance-only | The repository static quality gate PASSes. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 05 remains acceptance-only | The repository template contract stays the only form authority. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 06 remains acceptance-only | Registry-derived roles and admitted adapters are at parity. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 07 remains acceptance-only | Each admitted provider's canary record and runtime-readiness boundary are validated. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 08 remains acceptance-only | Contract, schema, and provider metadata parity PASSes. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 09 remains acceptance-only | Bounded failure handling and safe handoff | [SPEC-0072](../03.specs/0072-agent-governance-and-quality-gate-consolidation/spec.md) |
| N/A — Acceptance criterion 10 remains acceptance-only | Per-role eval and model fitness evidence exists. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 11 remains acceptance-only | Shared QA and distinct index evidence | [SPEC-0072](../03.specs/0072-agent-governance-and-quality-gate-consolidation/spec.md) |
| N/A — Acceptance criterion 12 remains acceptance-only | There are zero stale legacy and orphan references. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |

### Reviewed member-ID transfer

The table below records the succession of current meaning. Earlier member IDs are historical identifiers of the original decisions and program and are not reassigned.

| Original member ID | Current semantic owner |
| --- | --- |
| REQ-0005-FR-0001 | REQ-0003-FR-0012 |
| REQ-0005-FR-0002 | REQ-0003-FR-0013 |
| REQ-0005-FR-0003 | REQ-0003-FR-0014 |
| REQ-0005-FR-0004 | REQ-0003-FR-0012 |
| REQ-0005-FR-0005 | REQ-0003-FR-0015 |
| REQ-0005-FR-0006 | REQ-0004-FR-0009 |
| REQ-0005-FR-0007 | REQ-0003-FR-0016 |
| REQ-0005-FR-0008 | REQ-0003-FR-0017 |
| REQ-0005-FR-0009 | REQ-0003-FR-0009 |
| REQ-0005-FR-0010 | REQ-0003-FR-0018 |
| REQ-0005-NFR-0001 | REQ-0003-NFR-0003 |
| REQ-0005-NFR-0002 | REQ-0003-FR-0015 |
| REQ-0006-FR-0001 | REQ-0003-FR-0012 |
| REQ-0006-FR-0002 | REQ-0003-FR-0019 |
| REQ-0006-FR-0003 | REQ-0003-FR-0012 |
| REQ-0006-FR-0004 | REQ-0003-FR-0020 |
| REQ-0006-FR-0005 | REQ-0003-FR-0020 |
| REQ-0006-FR-0006 | REQ-0003-FR-0020 |
| REQ-0006-FR-0007 | REQ-0003-FR-0019 |
| REQ-0006-FR-0008 | REQ-0003-FR-0021 |
| REQ-0006-FR-0009 | REQ-0003-FR-0022 |
| REQ-0006-FR-0010 | REQ-0003-FR-0017 |
| REQ-0006-FR-0011 | REQ-0003-FR-0018 |
| REQ-0006-NFR-0001 | REQ-0003-FR-0007 |
| REQ-0006-NFR-0002 | REQ-0003-FR-0014 |
| REQ-0008-FR-0001 | REQ-0003-FR-0019 |
| REQ-0008-FR-0002 | REQ-0003-FR-0023 |
| REQ-0008-FR-0003 | REQ-0003-FR-0014 |
| REQ-0008-FR-0004 | REQ-0003-FR-0023 |
| REQ-0008-FR-0005 | REQ-0003-FR-0012 |
| REQ-0008-FR-0006 | REQ-0003-FR-0013 |
| REQ-0008-FR-0007 | REQ-0003-FR-0014 |
| REQ-0008-FR-0008 | REQ-0003-FR-0015 |
| REQ-0008-FR-0009 | REQ-0003-FR-0020 |
| REQ-0008-FR-0010 | REQ-0003-FR-0024 |
| REQ-0008-FR-0011 | REQ-0003-FR-0016 |
| REQ-0008-FR-0012 | REQ-0003-FR-0024 |
| REQ-0008-FR-0013 | REQ-0003-FR-0025 |
| REQ-0008-FR-0014 | REQ-0003-FR-0026 |
| REQ-0008-FR-0015 | REQ-0003-FR-0022 |
| REQ-0008-FR-0016 | REQ-0003-NFR-0004 |
| REQ-0008-FR-0017 | REQ-0003-FR-0027 |
| REQ-0008-NFR-0001 | REQ-0003-FR-0019 |
| REQ-0008-NFR-0002 | REQ-0003-FR-0007 |
| REQ-0008-NFR-0003 | REQ-0003-FR-0012 / REQ-0003-FR-0023 |
| REQ-0008-NFR-0004 | REQ-0003-FR-0023 |
| REQ-0008-NFR-0005 | REQ-0003-FR-0020 / REQ-0003-FR-0015 |
| REQ-0008-NFR-0006 | REQ-0003-FR-0024 |
| REQ-0007-FR-0001 | REQ-0004-FR-0005 |
| REQ-0007-FR-0002 | REQ-0004-FR-0006 |
| REQ-0007-FR-0003 | REQ-0004-FR-0007 / REQ-0003-FR-0016 |
| REQ-0007-FR-0004 | REQ-0003-FR-0017 |
| REQ-0007-FR-0005 | REQ-0004-FR-0008 |
| REQ-0007-FR-0006 | REQ-0004-FR-0010 |
| REQ-0007-FR-0007 | REQ-0004-FR-0009 |
| REQ-0007-FR-0008 | REQ-0003-FR-0028 |
| REQ-0007-FR-0009 | REQ-0003-FR-0007 |
| REQ-0007-FR-0010 | REQ-0004-FR-0011 / REQ-0003-FR-0018 / REQ-0003-FR-0019 |
| REQ-0007-FR-0011 | REQ-0004-FR-0012 |
| REQ-0007-FR-0012 | REQ-0004-FR-0013 |
| REQ-0007-FR-0013 | REQ-0004-FR-0014 |
| REQ-0007-NFR-0001 | REQ-0004-NFR-0003 |
| REQ-0007-NFR-0002 | REQ-0003-FR-0014 |

- Current architecture: [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md).
- Current integration: [Spec 0054](../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) and its package-local Plan/Tasks.
- Original decision bodies remain in the [decision log](../02.architecture/decisions/README.md); recovery is indexed in [Stage 98](../98.archive/README.md).
