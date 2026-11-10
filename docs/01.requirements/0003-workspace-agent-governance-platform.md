---
title: "Workspace Agent and Document Governance Requirements"
version: "3.0.1"
type: "sdlc/requirement"
status: "approved"
owner: "platform"
updated: "2026-11-11"
layer: "requirements"
artifact_id: "REQ-0003"
---

# Workspace Agent and Document Governance Requirements

## Overview

This package states the user requirements for agent execution and document governance; the operator approved it on 2026-11-05 as current requirement authority. The
[common role registry](../../.agents/roles/registry.json) owns the machine truth of roles and skills,
[Common governance](../../.agents/README.md) owns the human execution rules, and
[Stage 99](../99.templates/README.md) owns document form. Common governance and
the [validation registry](../../scripts/validation/registry.json) own current
execution and QA contracts. [ADR-0036](../02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md)
records the durable governance decisions. The earlier Spec packages are deleted; the Archived Lineage table below summarizes them and Git history recovers them.
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
- A document changer hands over current consumers and preserves decision history.
- A reviewer separates local static results from external observation and links unfinished work to the next Task.

## Functional Requirements

Acceptance criteria are abbreviated `AC##` in the Verification intent column.

| Requirement ID | Requirement | Priority | Verification intent |
| --- | --- | --- | --- |
| REQ-0003-FR-0001 | Common Agent, Skill, Rule, Hook, Workflow, checkpoint, QA, and document policy must each have one current owner per responsibility. | Must | AC01: the owner graph links without contradiction. |
| REQ-0003-FR-0002 | Provider gateways and adapters must express only native syntax and capability differences, without copying common policy. | Must | AC03: gateways copy no common policy. |
| REQ-0003-FR-0003 | Skill provenance must distinguish repo-local, shared, provider-native, and explicitly requested external skills, and must not assume a missing skill is executable. | Must | AC06: Registry skill membership and paths validate. |
| REQ-0003-FR-0004 | Work must link to the relevant process, branch, document, QA, DevOps, CI/CD, security, and Kubernetes scope and approval owner. | Must | AC01: each scope axis routes to an owner. |
| REQ-0003-FR-0005 | The Plan/Task handoff of a repository change must record the commands run, results, limits, remaining work, and approval boundaries. | Must | Task handoff fields carry commands, results, limits and next owner. |
| REQ-0003-FR-0006 | A document's purpose and form must follow its repository form owner, and an external format must not be used as a substitute authority without separate approval. | Must | AC05: template and profile checks PASS. |
| REQ-0003-FR-0007 | Least privilege, secret non-disclosure, GitOps-first, and the explicit approval boundary for external, live, and destructive work must be preserved. | Must | Registry permissions and guard checks cover the protected actions; runtime enforcement is observed separately. |
| REQ-0003-FR-0008 | Projection must include only currently admitted provider surfaces, and a planned or absent surface must not count as current support. | Must | AC06: projections match the admitted Registry surfaces. |
| REQ-0003-FR-0009 | Provider-native metadata must be kept distinct from repository document form, and static form conformance must not be promoted to evidence of discovery, authentication, or runtime enforcement. | Must | AC08: metadata parity validates without runtime claims. |
| REQ-0003-FR-0010 | The machine registry of roles and skills must define semantics, projection, permission, stop, handoff, and validation responsibility within one ownership boundary. | Must | AC08: the Registry schema validates every role. |
| REQ-0003-FR-0011 | Repeated agent execution must provide bounded retry, a no-progress stop, safe checkpoint, compaction, and resume, and escalation; the loop contract must own the limits. | Must | AC09: runner limit fixtures and Task handoff. |
| REQ-0003-FR-0012 | A single document machine owner must define document routes, profiles, metadata, form, and lifecycle edges, and prose policy must live only with its responsibility owner. | Must | Document contract registry check PASS. |
| REQ-0003-FR-0013 | Each physical document form must map to exactly one profile, and its template and validator must agree. | Must | Markdown profile check PASS. |
| REQ-0003-FR-0014 | Requirements, Architecture, Spec/Plan/Task, operations documents, References, and READMEs must each keep their purpose and must not copy execution detail or unobserved operational evidence into higher documents. Stage 05 keeps its position, and this convergence creates no Release family. | Must | Profile and link checks PASS per stage. |
| REQ-0003-FR-0015 | Before disposing of a current document, the owner must hand over its unique current meaning and assess current, historical, audit and recovery consumers, preservation value, holds and disposition authority. Existing factual records remain intact. Unresolved conditions defer that disposition. | Must | Reviewed Task evidence names each assessment and owner; link and owner checks find no orphan current consumer. |
| REQ-0003-FR-0016 | Affected-path, lane, and argv routing must have one machine owner. A logical check executes once per identical bytes, configuration, tool identity, scope, mode and trust; validators with distinct failure meanings remain separate, and stages select rather than duplicate those checks. | Must | Validation registry routing tests PASS. |
| REQ-0003-FR-0017 | This public repository performs purpose, unit and document-content QA locally. Hosted CI checks branch and delivery metadata with a fail-closed verdict and runs only the selected shared style rule as a distinct PR final defense on its own merge SHA/run, plus, when a PR changes `.github/requirements/`, the reviewed base's CI lock contract on the PR files, because a bot-authored lock update never passes local staged QA; it does not rerun or certify local purpose QA. Hosted jobs use least privilege and immutable external Action identifiers and produce no artifact under the current contract. A future artifact uploader must define its purpose, inputs, trust boundary, retention budget and validation owner in its introduction contract, with validation of those declared constraints. Local validation is never reported as a hosted result; historical unrun hosted full QA remains `NOT_RUN` evidence, not a current gate. A deployment style check requires an actual deployment workflow and observed run. | Must | AC11: hosted runs have their own SHA/run evidence. |
| REQ-0003-FR-0018 | Changes must be delivered as logical commits with independent review, exact-index validation, required lint and format on the final local index immediately before commit, and reversible boundaries. Select affected purpose gates and named behavior and security unit regressions after tool and budget preflight. Retire the long local full/ci sweep and blanket unit discovery from completion, including global QA changes; an explicit audit selects bounded named checks for its purpose rather than reintroducing the sweep. | Must | AC11: commit-time lint/format and selected checks recorded. |
| REQ-0003-FR-0019 | The package-local Plan/Task owns execution state and order, and must not distort the original tranche, follow-up, and succession history or copy it into a permanent central roster. | Must | Plan/Task review shows package-local state. |
| REQ-0003-FR-0020 | A non-current document leaves its active stage only after its disposition conditions are met. Git-history-only disposition requires a reachable exact source `commit:path` whose bytes match the source being disposed of and a byte-identical temporary restoration. The existing Task carries disposition and recovery evidence; Stage 01–03 use the current owner's Archived Lineage, while other types use their existing relationships or disposition record. No recovery ledger, catalog or migration record is added. `docs/98.archive/` remains unvalidated and non-authoritative; it currently holds only its README and directory structure. | Must | Reviewed Task evidence includes source identity and restoration result; lifecycle and link checks PASS for the changed current documents. |
| REQ-0003-FR-0021 | Audit, research, data, generated output, and learning material must state their basis, observation time, and owner, and must not substitute for current policy or execution approval. | Must | Reference profiles carry basis, date and owner. |
| REQ-0003-FR-0022 | Scratch and checkpoints must stay bounded, secret-free temporary state, and durable execution evidence must be left in the Task. The removed shared progress ledger is not restored as a new current owner. The shared workspace memory store (`scripts/workspace_memory.py`) may retain revised decision context across sessions and providers; it is never Task status, evidence, approval or acceptance, and it is not that ledger. | Must | No ledger file exists; memory entries carry no Task status. |
| REQ-0003-FR-0023 | Stable document identities and semantic filenames must be kept, and the identity rules, uniqueness, and path correspondence of mandatory/excluded profiles must be validated. Identifiers in existing decision history are not reassigned. | Must | Identity and path checks PASS. |
| REQ-0003-FR-0024 | A compatibility layer, wrapper, or script must be kept only while it has a real consumer and a unique rule or negative fixture, and must be removed after succession evidence and consumer-zero. | Must | AC12: no wrapper without a consumer. |
| REQ-0003-FR-0025 | The agent system's risk, tool/data trust, oversight, stop, approval, trace, evaluation, and component provenance obligations must be implemented and validated in the current `.agents/roles/` Registry and `.agents/governance/` owners. A static declaration does not prove runtime enforcement. | Must | Governance validator PASS at the current owners. |
| REQ-0003-FR-0026 | Repository-declared, provider-runtime, hosted-CI, and approved remote/live evidence must be kept apart and must not be promoted into one another without observation. | Must | AC03: evidence classes stay distinct in Task records. |
| REQ-0003-FR-0027 | Lifecycle validation must judge profile, state, and allowed edges, while ordinary body corrections and consumer succession are judged by semantic/link validation and reviewed Git recovery. | Must | Lifecycle check judges state edges only. |
| REQ-0003-FR-0028 | Malformed input, a missing tool, fallbacks, risky paths, and forbidden actions must have deterministic direct negative tests, and a required-tool failure must not be hidden as a diagnostic SKIP. | Must | Negative fixtures fail closed in the unit suite. |
| REQ-0003-FR-0029 | One producer must prepare a SemVer GitHub Release and tag from a reviewed main release-preparation PR whose canonical `CHANGELOG.md` entry describes integrated changes. A released public compatibility contract covers supported CLI/options, JSON schemas, document profiles/frontmatter, GitOps desired state and external-service interfaces; breaking, additive compatible and compatible corrective changes advance major, minor and patch respectively after 1.0. For an initial 0.y release, the operator selects and records the first version and its compatibility promise. Retries never move a tag, a development push creates no release, an unsuccessful validation cannot publish, and publication repeats no QA. Existing `main-<full commit SHA>` tags remain untouched as history. If immutable Releases are enabled, required assets are attached to the draft before publication. A release is repository contract history, not runtime certification. | Must | AC13: release refusal checks PASS. |
| REQ-0003-FR-0030 | CI/QA/validation scripts, invoked or discovered tests, and `.github/` surfaces must be traced to active consumers, unique rules, triggers, permissions and current repository purpose. Proven one-off, legacy, deprecated, duplicate, conflicting or excessive execution is retired only after ongoing coverage transfers, callers and registration are removed, dedicated helpers/fixtures/tests lose their consumers, and necessary results remain at the existing evidence owner. Distinct security, document and GitOps failure meanings stay covered. Small changes must not trigger broad repeat work at later delivery stages. | Must | AC14: no proven one-off caller remains. |
| REQ-0003-FR-0031 | Skill evaluation must retain the same task and conditions, actual outputs without and with the Skill, scoring criteria, scores and one representative aggregate owner. Scores must identify evidence granularity, trial count, result signals, grader and criterion IDs, partial-score rationale and human-calibration state. Only actual evaluation cycles update outputs, scores and aggregates; an aggregate requires its task, complete paired outputs and score. Preserve original observed bytes and distinguish incomplete evidence from measured results. Representative evaluations establish only their declared scope, not the full Skill roster, native selection, command execution, approval or runtime enforcement. Retiring a recurring grader must preserve this evidence capacity and its canonical forms without making grading a recurring repository QA requirement. | Must | AC10: evaluation forms keep paired evidence. |
| REQ-0003-NFR-0001 | Roster and adapter counts must be derived from the current Registry, and role and surface admission and model fitness must be justified by local need, least privilege, and evaluation evidence. | Must | AC06: counts derive from the Registry. |
| REQ-0003-NFR-0002 | Targeted named unit and purpose checks, affected, staged and formatter/diff validation must cover applicable contracts at their appropriate input and stage without a blanket discovery or retired full/ci sweep. Record each result, input snapshot, tool and mode; reuse is admitted only for proven identical inputs and never across local, hosted or live trust lanes. | Must | AC11: results record input, tool and mode. |
| REQ-0003-NFR-0003 | Document form and QA/release decisions must trace a dated official primary source to its exact claim, applicable scope, local decision and validation evidence. An external standard is guidance or convention until the repository's current owner adopts a rule; it never establishes certification or remote state. | Must | Source citations name date, claim and scope. |
| REQ-0003-NFR-0004 | A discovered baseline defect is handled without weakening the contract, and a false-positive verdict, an environment limit, or an unresolved failure must not be hidden as success. | Must | Review finds no hidden failure or weakened gate. |
| REQ-0003-IF-0001 | A migration must deliver the current owner switch, reciprocal links, and cleanup of stale claims and orphan consumers in the same review unit. | Must | AC12: the migration review unit leaves no stale claim. |
| REQ-0003-IF-0002 | An external role catalog is only the provenance of an idea, never admission or policy authority. | Must | No external catalog is cited as admission authority. |

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
- **Acceptance criterion 07**: Provider readiness is reported only from an observed, secret-free remote/live session recorded in a Task, and ABSENT/DEFER carries a limit, an owner, and a retry trigger.
- **Acceptance criterion 08**: Consistency of the machine schema, metadata, and projections is validated.
- **Acceptance criterion 09**: Runner fixtures validate timeout, output limits and child cleanup, Task evidence records the no-progress stop and handoff, and compaction and resume follow the context policy without sensitive data.
- **Acceptance criterion 10**: Evidence for role input/output, permission, stop, handoff, evaluation and model fitness names its observed scope and gaps. A representative paired Skill evaluation retains task, both outputs, score and aggregate relationships without claiming coverage of unmeasured roles, Skills or runtime behavior.
- **Acceptance criterion 11**: Results of applicable focused named behavior/security, affected, exact-index and formatter/diff checks are traceable by actual input; hosted branch metadata and selected PR style have distinct SHA/run results, and historical unrun full QA remains separate. The same leaf is not repeated through commit, push, merge and postmerge solely because the delivery stage changed.
- **Acceptance criterion 12**: Current surfaces carry no duplicate authority, stale claim, or orphan consumer, and actual runtime limits are preserved.
- **Acceptance criterion 13**: A main release-preparation PR supplies a reviewed `CHANGELOG.md` entry and one SemVer tag/Release producer; development pushes create none, existing SHA tags are preserved, duplicate notifications do not move a tag, and failed checks do not publish.
- **Acceptance criterion 14**: The active script, test and `.github/` graph has no proven one-off or duplicate execution after consumer succession, while distinct security, document and repository-purpose checks remain covered. Issues express requests, the Spec contract, Task execution and Project a view without copied or bidirectionally overwritten state.

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
[ADR-0053](../02.architecture/decisions/0053-unvalidated-archive.md).
- Model availability, effort enums, CLI schemas, and authentication change. A concrete value must be proven together by the
  official source at the reference time and an observed authenticated session; inferring from names is forbidden.
- Native Claude/Codex format support is not equated with an account's actual execution permission.
- Provider credentials are not placed in GitHub-hosted CI. Authenticated provider observation is remote/live
  evidence recorded in a Task with secret-free results only.
- The Task and Git own work, validation, and handoff. No separate automatic checkpoint file is made mandatory,
  and credentials or full transcripts are not stored.
- ADR-0036 and `scripts/validation/registry.json` own the current governance location and the QA/CD boundary. Earlier ADRs are summarized in the AD-0006 [Archived Lineage](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md#archived-lineage).

### Agent execution and approval requirements

- **Allowed Actions**: Inspect current owners, edit approved repository scope, and run non-destructive local validation.
- **Disallowed Actions**: Read secret values, invent runtime evidence, restore obsolete governance owners, or mutate external/live systems without approval.
- **Human-in-the-loop Requirement**: Obtain approval for destructive Git, external actions, provider authentication, deployment, or secret handling.
- **Evaluation Expectation**: Preserve independent review, stable-snapshot validation results, failure limitations, and package-local unfinished ownership.

### Unfinished execution and original lineage

Withdrawn, completed and superseded packages through SPEC-0140 were deleted. Git history recovers each from the commit its Archived Lineage row names (default `git show 69445fca:<path>`), and the [Archived Lineage](#archived-lineage) table summarizes them. Their retired designs are not current authority, and withdrawn work is not declared complete. REQ-0005, REQ-0006 and REQ-0008 were merged into this document; the [Reviewed member-ID transfer](#reviewed-member-id-transfer) table maps their member IDs. Custom CRD schema, generated output and live observations remain explicit DEFER under the owners in [REQ-0004](./0004-current-local-gitops-platform.md), which co-owns the platform-specific obligations.

## Traceability

SPEC-0152 completed the current manual disposition policy change; its exact completed source and recovery proof are in [Archived Lineage](#archived-lineage). Earlier completed packages, including SPEC-0151 and SPEC-0150, are summarized there and recovered from Git history. The seven-stage W00–W11 follow-up roadmap remains future work in `git show 4033d38e:docs/03.specs/0152-manual-document-disposition-policy/plan.md` under `Deferred Roadmap`; this closure does not complete those stages. The approved [SPEC-0153](../03.specs/0153-cumulative-lifecycle-history-validation/spec.md) addresses the separately observed broad-history ADR and Task validation failures; its implementation is locally committed and source-history checks passed, while Task criterion acceptance remains pending. It does not revise SPEC-0152's completed evidence.

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-0003-FR-0001 | The common governance and owner graph validate as a single current source. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0002 | Provider gateways keep the thin adapter boundary. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0003 | Registry skill membership and path existence are machine-validated; provenance classes are policy-reviewed. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0004 | Every strategy axis and scope owner can be found. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0005 | A repo-changing handoff leaves its evidence and limitations. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0006 | Template, profile, and cross-link checks pass. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0007 | No GitOps, secret, privilege, or external-action guardrail is violated. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0008 | Registry-admitted surfaces carry native claims separate from the common semantics. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0009 | Registry schema, model and effort bindings validate statically; provider-runtime observation stays separate remote/live evidence, and no MCP server is admitted. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0010 | The machine harness contract/schema validates every role and adapter. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0011 | The bounded runner's timeout, output, child cleanup, and no-progress handoff are validated by Task evidence. | N/A — SPEC-0072 left the tree; Git history recovers it |
| REQ-0003-FR-0012 | The document contract registry alone defines routes, profiles, metadata, form and lifecycle edges. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), SPEC-0140 (left the tree; Git history recovers it) |
| REQ-0003-FR-0013 | Every physical form maps to one profile, and template and validator agree. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0014 | Each stage keeps its purpose and copies no execution detail upward. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0015 | A disposition transfers current meaning and reviews all consumer and preservation obligations before removal. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0016 | One machine route selects each applicable leaf once per identical input, configuration, tool, mode and trust while independent validator failure meanings remain distinct. | N/A — SPEC-0117, SPEC-0118, SPEC-0120 left the tree; Git history recovers them |
| REQ-0003-FR-0017 | Public-repository purpose QA runs locally; hosted branch metadata and PR style have distinct observed inputs and never certify local QA. | N/A — SPEC-0113, SPEC-0115, SPEC-0123 left the tree; Git history recovers them |
| REQ-0003-FR-0018 | Logical commits get independent review, exact-index and pre-commit style checks; named purpose/unit gates replace retired full/ci and blanket discovery. | N/A — SPEC-0140 left the tree; Git history recovers it |
| REQ-0003-FR-0019 | Execution state lives only in the package-local Plan/Task. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0020 | Eligible non-current documents leave their stage after manual source restoration review; `docs/98.archive/` remains unvalidated. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), ADR-0056, SPEC-0152 and SPEC-0140 (left the tree; Git history recovers them) |
| REQ-0003-FR-0021 | Each reference, audit or generated artifact names basis, observation time and owner. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0022 | No shared progress ledger exists, and memory entries are never Task status or evidence. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0023 | Identity, uniqueness and path correspondence checks PASS. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0024 | No compatibility layer remains without a consumer and a unique rule. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0025 | The governance validator checks these obligations at the current Registry and governance owners. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0026 | Each evidence class is reported separately and never promoted without observation. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0027 | Lifecycle validation judges profile, state and edges; body corrections pass semantic and link checks. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), [SPEC-0153](../03.specs/0153-cumulative-lifecycle-history-validation/spec.md), SPEC-0140 (left the tree; Git history recovers it) |
| REQ-0003-FR-0028 | Each failure class has a direct negative test, and a missing required tool fails. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0029 | A reviewed main release-preparation PR controls canonical changelog and a single SemVer tag/Release producer; historical SHA tags are preserved. Actual publication needs separate observation. | N/A — SPEC-0136, SPEC-0137 left the tree; Git history recovers them |
| REQ-0003-FR-0030 | Active scripts, tests and hosted surfaces are retired only after ongoing coverage and consumers transfer, with distinct failure meanings preserved. | N/A — SPEC-0140 left the tree; Git history recovers it |
| REQ-0003-FR-0031 | Representative Skill comparisons retain actual paired outputs, scoped scoring and one aggregate owner; canonical evidence forms neither rerun grading nor establish native behavior. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-NFR-0001 | Role/adapter counts derive from the Registry; eval and model fitness remain reported gaps until observed. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-NFR-0002 | Local selected checks retain exact input/mode boundaries and hosted evidence remains separate. | N/A — SPEC-0107 left the tree; Git history recovers it |
| REQ-0003-NFR-0003 | Dated primary sources are mapped to claims, applicable scope, local decisions and Task evidence. | N/A — SPEC-0107 left the tree; Git history recovers it |
| REQ-0003-NFR-0004 | A baseline defect is fixed without weakening a contract, and no false positive, environment limit or unresolved failure is reported as success. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-IF-0001 | No legacy or orphan current owner remains on an active surface. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-IF-0002 | An external role idea is admitted only after it passes a local gap and an eval. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 01 remains acceptance-only | The common `.agents/` owner graph links without contradiction. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 02 remains acceptance-only | Requirement Package→AD→ADR links are reciprocal; Spec/Plan/Task links are added when a package exists. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 03 remains acceptance-only | Gateways do not copy policy and keep evidence classes distinct. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 04 remains acceptance-only | The repository static quality gate PASSes. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 05 remains acceptance-only | The repository template contract stays the only form authority. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 06 remains acceptance-only | Registry-derived roles and admitted adapters are at parity. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 07 remains acceptance-only | Provider runtime readiness stays remote/live evidence recorded in a Task; no static check claims it. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 08 remains acceptance-only | Contract, schema, and provider metadata parity PASSes. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 09 remains acceptance-only | Bounded failure handling and safe handoff | N/A — SPEC-0072 left the tree; Git history recovers it |
| N/A — Acceptance criterion 10 remains acceptance-only | Evaluation capacity exists; observed pairs and model fitness remain unmeasured and are reported as gaps. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 11 remains acceptance-only | Applicable local stage checks retain distinct inputs without repeating a successful identical leaf. | N/A — SPEC-0107 left the tree; Git history recovers it |
| N/A — Acceptance criterion 12 remains acceptance-only | There are zero stale legacy and orphan references. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 13 remains acceptance-only | Canonical main changelog and one SemVer tag/Release producer pass local refusal checks; publication is observed separately. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md); release decision ADR-0048 and RUN-0012 |
| N/A — Acceptance criterion 14 remains acceptance-only | Proven obsolete callers are retired after ongoing coverage transfer; Issues, Spec, Task and Project retain distinct ownership. | N/A — SPEC-0107 left the tree; Git history recovers it |

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
- Current integration: none. SPEC-0140 left the tree; Git history recovers it.
- Original decision bodies remain in the [decision log](../02.architecture/decisions/README.md); recovery is by Git history (`git show <commit>:<path>`), with summaries in [Archived Lineage](#archived-lineage).

### Archived Lineage

These documents were deleted from `docs/98.archive/` or `docs/03.specs/` under SPEC-0140. Unless a row names its own recovery commit, recover one with `git show 69445fca:<path>`; the paths below are the paths at the recovery commit. A completed Spec path is its package directory (`spec.md`, `plan.md`, `tasks/`).

| Source | Kind | Summary | Original path |
| --- | --- | --- | --- |
| REQ-0005 (superseded) | superseded requirement | Document assurance modernization: profile-specific, machine-verifiable contracts for document type, ownership, lifecycle, templates and validation. Superseded by REQ-0008 (2026-09-05); current meaning passed to this document. | `docs/98.archive/superseded/01.requirements/0005-workspace-document-assurance-modernization.md` |
| REQ-0006 (superseded) | superseded requirement | Completed lifecycle and evidence consolidation program (Specs 034-040) closed at commit `c5adc27b13893d7cbd1266c9225372cfb7df79e9`. Superseded by REQ-0008 (2026-09-05); current meaning passed to this document. | `docs/98.archive/superseded/01.requirements/0006-workspace-document-lifecycle-and-evidence-consolidation.md` |
| REQ-0008 (superseded) | superseded requirement | Document taxonomy consolidation: co-located spec, plan and tasks under Stage 03, one authoring model, agent-governance controls and validator orchestration; superseded REQ-0005 and REQ-0006. Archived 2026-09-05 with this document as replacement. | `docs/98.archive/superseded/01.requirements/0008-workspace-document-taxonomy-consolidation.md` |
| SPEC-0007 (superseded) | superseded spec | Documentation governance consistency spec: `docs/99.templates/` as SSoT, template compliance, legacy file removal and CI policy-gate scope. Replaced by a 2026-06-02 execution plan (`docs/04.execution/plans/2026-06-02-docs-01-05-current-implementation-alignment.md`). | `docs/98.archive/superseded/03.specs/0007-docs-governance-consistency.md` |
| SPEC-0009 | completed spec | Documentation-only research pack under `docs/90.references/research/` comparing the repo's governance, CI/CD, QA and SDLC contract with external sources. Completed. | `docs/98.archive/completed/03.specs/0009-workspace-harness-research-pack/` |
| SPEC-0010 | completed spec | Documentation-only four-report implementation audit pack under `docs/90.references/audits/` measuring the research pack's categories against repo evidence. Completed. | `docs/98.archive/completed/03.specs/0010-workspace-harness-implementation-audit-pack/` |
| SPEC-0011 | completed spec | Destructive four-phase restructuring of `docs/99.templates/` into template forms, support contracts and governance rules, removing legacy flat paths and duplicated README governance. Completed. | `docs/98.archive/completed/03.specs/0011-template-contract-governance-migration/` |
| SPEC-0012 | completed spec | Audit-first follow-up and selective enhancement of `docs/99.templates/**`, support contracts, Stage 00 references and validation after the template migration. Completed. | `docs/98.archive/completed/03.specs/0012-template-governance-audit-enhancement/` |
| SPEC-0013 | completed spec | Hardened document type contracts, frontmatter profiles, template governance, provider entrypoints and repository documentation quality gates. Completed. | `docs/98.archive/completed/03.specs/0013-workspace-document-governance-hardening/` |
| SPEC-0014 | completed spec | Second workspace-wide normalization of active and historical documents, templates, README profiles and CI/QA docs around one frontmatter, section and routing model, keeping past facts in explicit historical sections. Completed. | `docs/98.archive/completed/03.specs/0014-workspace-document-contract-normalization/` |
| SPEC-0015 | completed spec | Normalized AI-agent governance, provider shims, Claude and Codex role files, local baselines and validation surfaces, with Stage 00 as owner of durable agent governance. Completed. | `docs/98.archive/completed/03.specs/0015-agent-governance-contract-normalization/` |
| SPEC-0016 | completed spec | Hardened active control surfaces (`.github`, validators, GitOps, infrastructure, policy, tests, Traefik local routes, sample-app template) while keeping cloud examples as dated snapshots. Completed. | `docs/98.archive/completed/03.specs/0016-active-control-surface-governance-hardening/` |
| SPEC-0017 | completed spec | Documentation-only dated research pack `2026-07-04-wer` covering workspace purpose, roles, CI/CD, QA, templates, scripts, SDLC, Kubernetes, infrastructure and security. Completed; later consolidated by SPEC-0053. | `docs/98.archive/completed/03.specs/0017-workspace-engineering-research-pack/` |
| SPEC-0018 | completed spec | Dated audit pack `2026-07-05-wea` comparing the research pack with repo evidence, and moved existing audit files into dated folders. Completed. | `docs/98.archive/completed/03.specs/0018-workspace-engineering-implementation-audit-pack/` |
| SPEC-0019 | completed spec | Normalized Stage 01 PRD and Stage 03 Spec template routing, converting date-based PRD filenames to stable numeric names across templates, governance references, READMEs and validators. Completed. | `docs/98.archive/completed/03.specs/0019-template-path-numbering-contract/` |
| SPEC-0020 | completed spec | Staged documentation and governance normalization that defined `_workspace` as isolated temporary repo-support staging and ran a repository-wide frontmatter, section, template and contract pass. Completed. | `docs/98.archive/completed/03.specs/0020-workspace-contract-governance-normalization/` |
| SPEC-0021 | completed spec | Repository contract for SDLC lifecycle routing, stage handoff, numeric lineage, archive preservation metadata, active-surface limits and `_workspace` boundaries. Completed. | `docs/98.archive/completed/03.specs/0021-sdlc-lifecycle-contract/` |
| SPEC-0022 | completed spec | Documentation and validation contract for control-surface READMEs (kept frontmatter-free) and promotion of AWS and Azure example documents to an example-local SDLC snapshot profile. Completed. | `docs/98.archive/completed/03.specs/0022-control-cloud-doc-normalization/` |
| SPEC-0023 | completed spec | Repo-static gap closure over Stage 03/04 documents, separating operator-only and live follow-ups from completed implementation; first gap was the research-pack stream. Completed. | `docs/98.archive/completed/03.specs/0023-stage03-04-repo-static-gap-closure/` |
| SPEC-0024 | completed spec | Added two review-only worker agents, `observability-reviewer` and `network-reviewer`, closing roster gaps for observability manifests and the network surface. Completed. | `docs/98.archive/completed/03.specs/0024-observability-and-network-review-agents/` |
| SPEC-0025 | completed spec | One normalization cycle: a single Current audit pack, reconciled Stage 03 Specs and Stage 04 Plans, and a canonical Spec for the ten-role, thirty-adapter roster. Completed. | `docs/98.archive/completed/03.specs/0025-governance-owner-and-roster-currentness/` |
| SPEC-0026 | completed spec | Single machine-readable document registry for routes, frontmatter profiles, lifecycle states, section profiles, template ownership and README profiles; foundation for Specs 027 to 032. Completed. | `docs/98.archive/completed/03.specs/0026-document-contract-registry/` |
| SPEC-0027 | completed spec | Aligned Stage 99 support contracts and template forms to the registry, removing duplicate route and lifecycle ownership and legacy forms. Completed. | `docs/98.archive/completed/03.specs/0027-template-contract-consolidation/` |
| SPEC-0028 | completed spec | Replaced the monolithic README snippet library and universal seven-heading rule with path-specific README profiles; kept `_workspace` temporary, ignored and non-secret. Completed. | `docs/98.archive/completed/03.specs/0028-readme-workspace-profiles/` |
| SPEC-0029 | completed spec | Registry-driven document validation with positive and negative fixtures, compatibility and strict modes and stable diagnostics. Completed. | `docs/98.archive/completed/03.specs/0029-semantic-document-validation/` |
| SPEC-0030 | completed spec | Migrated the tracked document population to the approved profiles, consolidated duplicate ownership, removed template residue, repaired links and moved AWS and Azure SDLC prose into dated provider snapshots. Completed. | `docs/98.archive/completed/03.specs/0030-authored-document-migration/` |
| SPEC-0031 | completed spec | One affected-surface-to-validator contract aligning local hooks, pre-commit, agent obligations, provider gateways and CI selectors. Completed. | `docs/98.archive/completed/03.specs/0031-affected-surface-agent-qa/` |
| SPEC-0032 | completed spec | Final tranche hardening workflow identity, GitOps change assurance, Vault and ESO boundaries, secret handling and policy evidence. Completed. | `docs/98.archive/completed/03.specs/0032-protected-surface-supply-chain-hardening/` |
| SPEC-0033 | completed spec | Follow-up normalization of Stage 99: forms separated from governance and machine contracts, five-key frontmatter baseline kept, registry-owned body traceability added. All eight work packages completed. Served the then-current REQ-0005, later superseded. | `docs/98.archive/completed/03.specs/0033-template-lifecycle-contract-normalization/` |
| SPEC-0034 | completed spec | Authority and lineage foundation for the lifecycle program (then REQ-0006): reconciled Spec 033, normalized Current audit dispositions and removed hand-maintained lifecycle facts from non-owning surfaces. Completed. | `docs/98.archive/completed/03.specs/0034-authority-and-lineage-foundation/` |
| SPEC-0035 | completed spec | Closed, profile-specific registry schema for frontmatter, ordering, lifecycle states, admission, transitions, transition evidence and template parity (then REQ-0006). Completed. | `docs/98.archive/completed/03.specs/0035-document-schema-and-lifecycle-contract/` |
| SPEC-0036 | completed spec | Implemented ADR-0018: replaced 31 metadata-only tombstones with full-body archive records and aligned the archive index, validators, historical-link resolution and `_workspace` boundary (then REQ-0006). Completed. | `docs/98.archive/completed/03.specs/0036-archive-record-and-workspace-boundary/` |
| SPEC-0037 | completed spec | Applied lifecycle-based accumulation limits to Stages 01-04, audited Stage 05 and moved eligible completed Plans and Tasks of closed lineages into full-body archive records (then REQ-0006). Completed. | `docs/98.archive/completed/03.specs/0037-active-corpus-and-execution-retention/` |
| SPEC-0038 | completed spec | Consolidated authority, currentness, generation, freshness and duplicate rules for `docs/90.references` (then REQ-0006). Completed. | `docs/98.archive/completed/03.specs/0038-reference-information-architecture/` |
| SPEC-0039 | completed spec | Aligned `.github` automation, pre-commit, validators, artifact retention and protected-surface evidence with the lifecycle and archive contracts, and fixed a portability defect in the GitOps change-set self-test (then REQ-0006). Completed. | `docs/98.archive/completed/03.specs/0039-github-ci-qa-evidence/` |
| SPEC-0040 | completed spec | Removed temporary compatibility, proved the integrated contract, ran whole-branch review and closed the lifecycle program without claiming unobserved remote or live results (then REQ-0006). Completed. | `docs/98.archive/completed/03.specs/0040-contract-cutover-and-program-closure/` |
| SPEC-0041 | completed spec | Foundation of the agent-governance program: one provider-neutral machine contract, four provider and local projections, a four-class project-memory contract and deterministic consumer validation. Completed. | `docs/98.archive/completed/03.specs/0041-stage-00-agent-governance-contract/` |
| SPEC-0042 | completed spec | Provider-native project surfaces, model and effort selection, MCP and tool boundaries and comparable runtime evidence for Claude, Codex and Gemini. Completed. | `docs/98.archive/completed/03.specs/0042-provider-native-runtime-and-model-evidence/` |
| SPEC-0043 | completed spec | Bounded, observable and recoverable execution loop shared by the provider projections, turning repeated failures into stop, escalation or evaluation input. Completed. | `docs/98.archive/completed/03.specs/0043-agent-harness-loop-lifecycle/` |
| SPEC-0044 | completed spec | Canonical 12-role roster and 48-adapter contract (adds `docs-researcher` and `quality-engineer`) with an admission gate. Closed at repository-static readiness; observed evaluation and final admission were not claimed. | `docs/98.archive/completed/03.specs/0044-agent-roster-evaluation-and-admission/` |
| SPEC-0045 | completed spec | Agent-governance validation lane on top of the always-start CI: 12 roles, 4 surfaces, 48 tuples, legacy cutover, local QA ordering and checkpoint isolation. Completed. | `docs/98.archive/completed/03.specs/0045-agent-governance-ci-qa-cutover/` |
| SPEC-0046 | completed spec | Final repository-local integrator closing PRD 003, AD 0006, ADR 0019 and Specs 041-045 through one machine-readable closure contract; hosted and provider-runtime lanes were not claimed. Completed. | `docs/98.archive/completed/03.specs/0046-agent-governance-program-closure/` |
| SPEC-0052 | completed spec | Document taxonomy consolidation (architecture-requirement corpus to AD, retirement of the human-authored API Spec profile, closure of legacy-form consumers); its transferred responsibilities moved to SPEC-0054. Served the then-current REQ-0008 and cites REQ-0003 and REQ-0004 as current authority. Completed. | `docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/` |
| SPEC-0053 | completed spec | New dated research pack `0001-workspace-engineering` re-researched from current sources and integrating all 25 files of three predecessor packs, which were then removed. Completed. | `docs/98.archive/completed/03.specs/0053-workspace-engineering-research-pack-consolidation/` |
| SPEC-0054 | completed spec | B-scope consolidation of SDLC documents, spec-driven workflow, agent governance, templates, validators, scripts, operations material and Stage 90/98 retention. Its governance continuation passed to SPEC-0072 and ADR-0035 on 2026-09-06. Completed. | `docs/98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/` |
| SPEC-0055 | completed spec | Current-state governance audit pack `2026-08-09-wgia` covering the repo's purpose, SDLC, CI/CD, QA, security, memory, harness and every agent role, with blockers and remediation. Completed. | `docs/98.archive/completed/03.specs/0055-workspace-governance-audit-and-remediation/` |
| SPEC-0056 | completed spec | Gap-only external-source refresh of the `0001-workspace-engineering` research pack for questions with no or `Partial` external treatment. Completed. | `docs/98.archive/completed/03.specs/0056-workspace-engineering-gap-only-refresh/` |
| SPEC-0057 | completed spec | Closed-ledger incremental refresh of the same pack targeting unresolved `Partial` and qualified `DEFER` evidence. Completed. | `docs/98.archive/completed/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/` |
| SPEC-0058 | completed spec | Combined cycle: a constraint-consistency pass (scope projection, one-off artifact cleanup, link integrity) and re-observation of twelve `Partial` requirement rows. Completed. | `docs/98.archive/completed/03.specs/0058-workspace-research-consistency-and-partial-refresh/` |
| SPEC-0059 | completed spec | Fifth full-corpus refresh of the research pack across 23 requested topics mapped onto 36 existing owner rows. Completed. | `docs/98.archive/completed/03.specs/0059-workspace-research-full-corpus-refresh/` |
| SPEC-0063 | completed spec | Consolidated governance invariants: retired validators bound to completed migrations (141 constants, 49 commit, blob or digest pins) while keeping rules that examine live state. Completed under the 2026-08-29 approval. | `docs/98.archive/completed/03.specs/0063-governance-invariant-consolidation/` |
| SPEC-0064 | completed spec | Consolidated the agent-governance surfaces (`docs/00.agent-governance/`, `.agents/`, `.claude/`, `.codex/`; 98 files audited): three defects fixed, eight candidates rejected, the progress ledger reduced to a minimal tombstone. Completed under the 2026-08-30 approval. | `docs/98.archive/completed/03.specs/0064-agent-governance-surface-consolidation/` |
| SPEC-0065 | completed spec | Retired the three transition residuals left by SPEC-0054 WP-012, including the progress and memory template routes tied to sealed `MIG-0004` and the retired ledger. Completed under the 2026-08-30 approval. | `docs/98.archive/completed/03.specs/0065-transition-residue-retirement/` |
| SPEC-0066 | completed spec | Delegated owner of SPEC-0054 WP-010 and WP-011: the validation-tooling ownership transition under ADR-0031. Completed. | `docs/98.archive/completed/03.specs/0066-validation-tooling-ownership/` |
| SPEC-0067 | completed spec | Artifact identity and filename normalization: every governed identity names its type and parent and numbered leaf filenames start with their number; declaration and naming only. Completed. | `docs/98.archive/completed/03.specs/0067-artifact-identity-and-filename-normalization/` |
| SPEC-0072 | completed spec | Agent-governance and quality-gate consolidation: common authority and QA migration, then the 2026-09-08 and 2026-09-09 corrections of gate coverage, formatter behavior, commit validation, redundant execution and evaluation-input containment. ADR-0036 succeeds ADR-0034/0035 for current authority. Completed. | `docs/98.archive/completed/03.specs/0072-agent-governance-and-quality-gate-consolidation/` |
| SPEC-0103 | completed spec | QA evidence reuse across commit, push, PR, merge and post-merge main: each gate runs once per proven-equivalent input, with one immutable commit tag on successful main updates. Completed; hosted trials and some provider limits stayed separate evidence. | `docs/98.archive/completed/03.specs/0103-qa-evidence-reuse/` |
| SPEC-0105 | completed spec | Common authority and safe authoring (P01): repaired approval and execution contracts so explicitly scoped local authoring proceeds without weakening protected execution boundaries. Its durable contract lives in the current approval-and-safety, agent-execution and quality governance. Recoverable at `69445fca`. | `docs/03.specs/0105-authority-and-safe-authoring/` |
| SPEC-0106 | completed spec | Stage 99 lifecycle normalization (P02): made the Stage 99 document contract describe lifecycle and execution traceability consistently across registry, forms, validators and consumers, with Plan-to-Spec and Task-to-Plan `parent_ids`. Its durable contract lives in the current Stage 99 registry and forms. Recoverable at `69445fca`. | `docs/03.specs/0106-stage99-lifecycle-normalization/` |
| SPEC-0107 | completed spec | Local quality and release lifecycle: local QA selection, logical commit delivery and a reviewed main release-preparation route with one SemVer tag/Release producer. Its durable decision lives in ADR-0048 and its structure in AD-0006. Recoverable at `69445fca`. | `docs/03.specs/0107-local-qa-and-release/` |
| SPEC-0108 | completed spec | Stopped a multi-row Task carrying a hand-synchronized frontmatter summary (status derives from its rows), moved provider-root READMEs to the Korean-first navigation profile and changed requested push, merge and pull-request commands from a blanket Claude denial to a per-call prompt. No Plan Promotion table; the result lives in the Stage 99 Registry, the validators and the provider notes. | `docs/03.specs/0108-task-status-and-provider-boundaries/` |
| SPEC-0109 | completed spec | Designed and implemented one workspace memory store that Claude and Codex sessions both read and write, retained across task completion and session end. Its durable contract lives in the context and memory policy (`.agents/governance/context-and-memory.md`). | `docs/03.specs/0109-shared-workspace-memory/` |
| SPEC-0110 | completed spec | Translated the eight provider-root READMEs, made a missing local style tool report its cause instead of withholding it, and recorded the v9 findings that current files already satisfied. No Plan Promotion table. | `docs/03.specs/0110-provider-readme-and-qa-diagnostics/` |
| SPEC-0111 | completed spec | Repaired five lifecycle and acceptance tests whose fixtures had drifted after documentation-only commits, so the tests no longer read inputs that later Tasks legitimately changed. No durable contract beyond the tests. | `docs/03.specs/0111-historical-fixture-drift/` |
| SPEC-0112 | completed spec | Pinned the three remaining tests that read completed package documents from the working tree, so editing or archiving a package no longer breaks them. No durable contract beyond the tests. | `docs/03.specs/0112-pinned-package-fixtures/` |
| SPEC-0113 | completed spec | Synchronized requirements, architecture and Spec documents after SPEC-0108 to SPEC-0112 and closed the narrow v9 prompt gaps left by the earlier keep decisions. No Plan Promotion table. | `docs/03.specs/0113-sdlc-sync-and-v9-gaps/` |
| SPEC-0114 | completed spec | Hardened Claude permission rules and hooks and Codex config: every push stays at ask, pull request creation and merge are allowed with `--admin` merges denied, executable-carrying Git options are denied and the Codex workspace network is off. The current contract is stated in `.claude/provider.md` and `.codex/provider.md`. | `docs/03.specs/0114-provider-permission-hardening/` |
| SPEC-0115 | completed spec | Evidence-led review and scoped repair of the local governance, document, validation, delivery and Kubernetes assurance surfaces requested on 2026-10-15. Promoted to the document authoring, document lifecycle and quality policies under `.agents/governance/`. | `docs/03.specs/0115-r10-local-remediation/` |
| SPEC-0116 | completed spec | Added local independent review published as the review App's required `independent-review` check, addressing the HIGH risk that a pull request could rewrite the workflow-defined required checks. Its runbook later left the tree, and the `independent-review` check was removed from the remote setting on 2026-11-03 at the operator's request (see `.github/rulesets/main-protection.md`). | `docs/03.specs/0116-independent-review-gate/` |
| SPEC-0117 | completed spec | Phase one of the 2026-10-16 local QA review: repaired eight over-applied, duplicated or stale checks and fixed three focused test modules that no selected lane ran. No durable contract introduced. | `docs/03.specs/0117-local-qa-rightsizing/` |
| SPEC-0118 | completed spec | Phase two of the local QA review: registered test modules that no lane ran and narrowed the `scripts` and `tests` catch-all surfaces so they select only gates their paths can affect. No durable contract introduced. | `docs/03.specs/0118-qa-phase-two/` |
| SPEC-0120 | completed spec | Gave every test module a named purpose gate that runs when its product or its own file changes, after SPEC-0118 left 63 of 76 modules ungated. No durable contract introduced. | `docs/03.specs/0120-test-purpose-gates/` |
| SPEC-0122 | completed spec | First use of the ADR-0040 whole-unit removal path: removed the seven Retention Catalog units that had no consumer outside Stage 98. No durable contract introduced. | `docs/03.specs/0122-archive-unit-disposition/` |
| SPEC-0123 | completed spec | Added the CI Python lock check (one `--only-binary :all:` directive, wheel-only hashes) to the hosted `style-pr` job after two Dependabot locks dropped the directive and still showed green. Promoted to the quality policy, hosted lane. | `docs/03.specs/0123-hosted-lock-check/` |
| SPEC-0124 | completed spec | Observed the ten required survey sources directly against six perspectives and recorded the result in the m0012 source-coverage register. No durable contract introduced. | `docs/03.specs/0124-required-source-coverage/` |
| SPEC-0125 | completed spec | Classified all 148 survey requirements (CR-01.01 to CR-21.05) from evidence in an existing Task and closed the small local gaps. Promoted the handoff candidate, verified and delivered commit fields to the quality policy and the memory restore procedure to the context and memory policy. | `docs/03.specs/0125-survey-status-and-local-gaps/` |
| SPEC-0126 | completed spec | Added a C4 context view, a container view with element table, a deployment mapping and an arc42 coverage table to AD-0007, plus one optional template prompt. Promoted to AD-0007. | `docs/03.specs/0126-architecture-views/` |
| SPEC-0127 | completed spec | Rejected mutually superseding ADRs in the lifecycle validator, added decision-maker and confirmation prompts to the decision template and recorded that ADR numbers are never reused and why `main` is the only long-lived branch. Promoted to the Git policy and ADR-0030. | `docs/03.specs/0127-adr-lineage-and-branch-strategy/` |
| SPEC-0128 | completed spec | Added a change-kinds table with security touchpoints and the return of operations learning to requirements, and Spec, Plan and Task template prompts for scenarios, interfaces, migration and rollback, and command evidence. Promoted to the SDLC policy (Change kinds). | `docs/03.specs/0128-change-kinds-and-authoring-prompts/` |
| SPEC-0129 | completed spec | Recorded a classified inventory of tracked files, an operations-document repetition survey and reproducible QA timing figures, and made the two operations edits the survey supported. No durable contract introduced. | `docs/03.specs/0129-inventory-operations-and-qa-baseline/` |
| SPEC-0130 | completed spec | Turned history links to twelve Archive units in two Requirements and one architecture description into plain identifiers, then removed those units as `git-history-only`. No durable contract introduced. | `docs/03.specs/0130-archive-history-link-migration/` |
| SPEC-0131 | completed spec | Moved the consumers of ten further Archive units to plain identifiers and a Git recovery route and corrected sentences that still said removed Specs are kept in the archive. No durable contract introduced. | `docs/03.specs/0131-archive-evidence-owner-migration/` |
| SPEC-0132 | completed spec | Removed 34 retained Archive units after a scratch-worktree trial showed the registry, validators and tests did not read their bodies, leaving SPEC-0104. No durable contract introduced. | `docs/03.specs/0132-archive-registry-and-test-consumers/` |
| SPEC-0133 | completed spec | Recorded the operator's decisions on the m0012 `DERIVED_PROPOSAL` cells and the eight `EXTERNAL` survey items, adopted the C4 diagram checks in the architecture-description author prompt and recorded the read-only evidence for CR-12.01. No durable contract introduced. | `docs/03.specs/0133-review-decisions-and-c4-prompt/` |
| SPEC-0134 | completed spec | Moved SPEC-0080 to Git history and recorded a `usable` assessment with a reason for each of the other eight retained Archive units. No durable contract introduced. | `docs/03.specs/0134-archive-final-units/` |
| SPEC-0135 | completed spec | Recorded the operator's actions on five `EXTERNAL` survey items (CR-01.02, CR-12.01, CR-18.06, CR-08.01, CR-14.03). No durable contract introduced. | `docs/03.specs/0135-external-item-decisions/` |
| SPEC-0136 | completed spec | Prepared the first SemVer release `v0.1.0` under RUN-0012 and the SPEC-0107 release contract. No durable contract introduced. | `docs/03.specs/0136-first-semver-release/` |
| SPEC-0137 | completed spec | Kept the full changelog and limited the GitHub Release body to the 125,000-character limit after the `0.1.0` section (143,352 characters) would have failed publication. Promoted to RUN-0012, Verification. | `docs/03.specs/0137-release-body-limit/` |
| SPEC-0138 | completed spec | Recorded the operator's remaining survey decisions: four independent repositories (CR-03.06, CR-03.07, CR-08.01), no GitHub Projects for status (CR-14.03), SPEC-0103 `usable` for good and a read-only live check for CR-09.04. No durable contract introduced. | `docs/03.specs/0138-remaining-decisions-closeout/` |
| SPEC-0139 | completed spec | Recorded the root cause, recovery and a fresh live observation of the `vault-backend` ClusterSecretStore failure, closing CR-09.04. No durable contract introduced. | `docs/03.specs/0139-cr-09-04-recovery/` |
| SPEC-0140 | completed spec | Removed every archive and migration check and the archived files (ADR-0053), deleted legacy and one-time QA code and completed packages SPEC-0105 to SPEC-0139, refused superseded, retired and deprecated states in Stages 01 to 03, and split README (human) from folder AGENTS.md (agent). All five criteria accepted on 2026-11-03; durable contracts promoted to document lifecycle and document authoring policy. Recover with `git show a9e3a87b:<path>`. | `docs/03.specs/0140-archive-check-removal/` |
| SPEC-0142 | completed spec | Removed stale Stage 99 contract entries: the retired Stage 00 Plan promotion owner, the ADR form's self-ID supersession cell, the unused profile modes `evidence` and `generated`, the unreferenced `requirementMemberId` definition and the unused `Agent Harness Requirements` language entry, and corrected the Stage 99 README and AGENTS prose. All four criteria accepted on 2026-11-06; the durable contract is in document lifecycle policy. Recover with `git show b712372b:<path>`. | `docs/03.specs/0142-stage99-contract-cleanup/` |
| SPEC-0143 | completed spec | Removed the profile modes `frontmatter-free` and `classification-only` and the frontmatter mode `not-applicable`, which the schema and loader never produce, with the validator branches only they reached, and added a regression test that ties the typed modes to the schema enum. Both criteria accepted on 2026-11-06; no durable contract introduced. Recover with `git show 0dde6158:<path>`. | `docs/03.specs/0143-dead-profile-mode-cleanup/` |
| SPEC-0144 | completed spec | Aligned `.agents/` with the current workspace after four read-only audits: corrected statements naming nonexistent writers, jobs, fields and tools, resolved intra-file contradictions (including a circular security severity deferral) and duplicated rules across governance, roles, skills, prompts, workflows, knowledge and evaluations; fixed `prompt-input.py` aborting on `git diff --check` findings and missing root routers, bound `ops-runbook` to `doc-writer`, and removed the unread `external_writes_require_approval` schema field, each with a regression test. All four criteria accepted on 2026-11-06; no durable contract introduced. Recover with `git show 22ed5caf:<path>`. | `docs/03.specs/0144-agents-conformance/` |
| SPEC-0145 | completed spec | Resolved the items SPEC-0144 deferred: role-specific Authority Boundary, Validation and Refresh, and Related Documents in the 17 role bodies; Item Index and Add and Find in the `.agents/` collection READMEs; per-role `supported_providers` and `projections` removed from the agent registry and derived in `validate-agent-governance.py` (regression test first); the `sdlc.md` contract invariant stated; CIS references renumbered to CIS Kubernetes Benchmark v1.9; the `hy-home.docker` revision pin rechecked. All four criteria accepted on 2026-11-06; no durable contract introduced. Recover with `git show 1ea51238:<path>`. | `docs/03.specs/0145-agents-deferred-conformance/` |
| SPEC-0146 | completed spec | After the AUD-0001 SDLC governance audit, added the `Cross-artifact conformance` rules to `sdlc.md` (a Spec links its constraining AD and ADRs or says none apply; an open question that changes a criterion blocks approval; an architecture departure waits for an accepted ADR; an implementation-versus-document divergence is resolved at its owner) and the matching Spec, Plan and ADR template prompts. All three criteria accepted on 2026-11-06; the durable rules were promoted to `sdlc.md`. Recover with `git show ca3ead4c:<path>`. | `docs/03.specs/0146-sdlc-cross-artifact-conformance/` |
| SPEC-0147 | completed spec | Resolved AUD-0001 decision D-1: the `sdlc/spec` Lifecycle Traceability table and its template profile require an `Architecture` column (constraining AD or ADR link, or why none applies), enforced by the existing header and non-empty-cell checks without link-target or reciprocal checks; focused test red then green; Spec fixtures updated; `sdlc.md` 3.2.0 names the column. Both criteria accepted on 2026-11-06; the durable rule was promoted to `sdlc.md`. Recover with `git show 2b1ac507:<path>`. | `docs/03.specs/0147-spec-architecture-column/` |
| SPEC-0148 | completed spec | Fixed AUD-0001 finding F-07: `validate-markdown-profiles.py` padded or truncated body-contract rows to the header width silently, which let one nine-cell evidence row disable the Task contract check; it now refuses such rows with `BODY-CONTRACT-ROW-WIDTH`. Focused test red then green; the fixed validator flags the three rows of the original `7aff341c` defect. Both criteria accepted on 2026-11-06; no durable contract introduced. Recover with `git show ef3a6398:<path>`. | `docs/03.specs/0148-task-table-row-width/` |
| SPEC-0149 | completed spec | Fixed AUD-0001 F-08 and F-09: the shared pre-action guard `scripts/provider_write_guard.py` reported only through the user-facing `systemMessage`, and neither provider loaded folder `AGENTS.md` files outside its native path; the guard now also returns `hookSpecificOutput.additionalContext` with its guidance and each write target's folder `AGENTS.md` chain, root gateway excluded, once per session, and a state or session failure never blocks. Claude delivery observed in-session; Codex delivery DEFER until the usage limit resets. All three criteria accepted on 2026-11-06; the reading rule was promoted to `agent-execution.md`. Recover with `git show ea4e36be:<path>`. | `docs/03.specs/0149-agents-md-hook-context/` |
| SPEC-0150 | completed spec | Fixed AUD-0001 F-10: `docs/90.references/AGENTS.md` rule 3 was unenforced; `validate-document-contract-registry.py` now compares each changed Stage 90 member with its HEAD version, following renames, and refuses with `REFERENCE_PUBLISHED_REWRITE` any change to a published member beyond its `status`, `version` and `updated` values and single-token link destinations, in local staged QA; the lifecycle validator is unchanged (REQ-0003-FR-0027). Both criteria accepted on 2026-11-06; no durable contract introduced. Recover with `git show 35d9733a:<path>`. | `docs/03.specs/0150-stage90-published-freeze/` |
| SPEC-0151 | completed spec | Gave Claude every folder `AGENTS.md` natively: a one-line `@AGENTS.md` `CLAUDE.md` beside each of the 15 folder files, loaded with the import on the first Read, Write or Edit there (Read and Write observed in new 2.1.319 sessions; Edit per the documentation), with a `common/folder-claude-import` profile and a repository-quality pairing check; the shared guard names the folder `AGENTS.md` paths on every write and sends folder text only to Codex; a Claude `SessionStart` hook on compaction or resume re-injects the reading instruction, and the validator allows that one pinned session event per provider rule. All four criteria accepted on 2026-11-06; the reading rule was promoted to `agent-execution.md`. Recover with `git show bb5dc474:<path>`. | `docs/03.specs/0151-folder-claude-imports/` |
| SPEC-0152 | completed spec | All three VAL-DISP criteria accepted by the current user on 2026-11-10; local policy, reference procedure and bounded first-record approval contract promoted to their current owners. ADR-0056 acceptance is separate from the Task decision. The frozen completed Task recorded consumers, hold review, authority and Git-history-only method; the three-file recovery proof below was observed before disposition. The seven-stage W00–W11 roadmap remains follow-up work. | `docs/03.specs/0152-manual-document-disposition-policy/` |

**SPEC-0152 recovery proof.** The exact completed source is commit `4033d38e7ac6eac0130700c8cf259ea252f44916`, reachable from retained local `refs/heads/codex/manual-document-disposition-policy` (`git merge-base --is-ancestor` rc 0). The current user authorized this bounded package exit on 2026-11-10; no hold was identified in the current repository documents or request, and the Task's frozen disposition decision names consumers and preservation route. Before any deletion, QA confirmed `git cat-file -e` rc 0 for each `commit:path`, restored each with `git show` to a mode-0600 temporary file, and obtained `cmp -s` rc 0 against its unchanged current source; the temporary files were removed. The three exact paths and Git blob identities are:

- `4033d38e7ac6eac0130700c8cf259ea252f44916:docs/03.specs/0152-manual-document-disposition-policy/spec.md` — blob `4a884dd6cb38df27796156896884617e32ae3a19`; observed original/restored SHA-256 `5cbe592d7a3ca1177eaa6e94086ed623141c82f5eca57c6aa8869ae62cd851d2`.
- `4033d38e7ac6eac0130700c8cf259ea252f44916:docs/03.specs/0152-manual-document-disposition-policy/plan.md` — blob `64251df3b5e52056d97a5a2abcf2f023fca25f50`; observed original/restored SHA-256 `fe42a8e6256fd94e5e9fa20cf9b04633bea5b1654ff6472c41c925c27660545b`.
- `4033d38e7ac6eac0130700c8cf259ea252f44916:docs/03.specs/0152-manual-document-disposition-policy/tasks/tsk-0001-manual-document-disposition-policy.md` — blob `3ef18bc8c42e298579c940c235fd603ae52a3a34`; observed original/restored SHA-256 `ef81a3f466670479463b13a08c2ed4735e13d9849b9e465eb72bd9a3fc3c3a30`.

The original and restored SHA-256 values above were directly observed before deletion; no post-deletion `hash-object` command is claimed. The blob identity and byte comparison establish the same Git object content as each then-current source. This is a local retained-ref claim, not remote retention or hosted evidence. QA observed unchanged HEAD, index and clean worktree before and after the proof. If a hold or consumer emerges before closure, retain the affected source and defer its disposition.

**Closure verification.** On the initial eight-path working-tree closure candidate, affected quick QA session `15997` returned rc 1: six of seven selected gates passed and `links-and-owners` failed. The same-snapshot diagnostic session `54963` identified `BODY-LINK-TARGET-PROFILE`: the REQ-0003-FR-0020 Traceability cell linked an ADR where that bound cell permits an AD or Spec link. After retaining the AD-0006 link and making ADR-0056 a plain ID there, the corrected eight-path candidate's affected quick session `29042` returned rc 0 with all seven gates PASS. These runs preceded this evidence paragraph; the final active exact-index hook checks the resulting closure bytes. No hosted, live or remote result is claimed.
