---
title: 'Document Taxonomy Consolidation Technical Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-08-09
---

# Document Taxonomy Consolidation Technical Specification (Spec)

## Overview

This specification implements
[PRD-008](../../01.requirements/008-workspace-document-taxonomy-consolidation.md),
[ARD-0011](../../02.architecture/requirements/0011-document-taxonomy-consolidation-architecture.md),
and the human-approved direction recorded in accepted
[ADR-0023](../../02.architecture/decisions/0023-work-unit-document-taxonomy-and-governance-authority.md).
It replaces the earlier Spec 052 direction that would have renumbered
`05.operations` and deleted several validator families without current
consumer proof.

The terminal result co-locates each retained Spec/Plan/Task work unit in Stage
03, removes the Stage 04 execution tree, preserves Stage 05, excludes a Release
family, consolidates document and AI-agent governance authorities, reconciles
validators and scripts by behavior, disposes of legacy material with explicit
provenance, and closes the observed pre-change validation failures.

This is an implementation-ready repository-static contract. It does not claim
that a provider consumed an adapter, enforced a policy, executed an approved
action, ran hosted CI, or changed remote/live infrastructure.

## Strategic Boundaries & Non-goals

Authorized paths are `docs/**`, repository-local agent/provider instruction
projections, document and harness contracts, templates, scripts, tests,
fixtures, generated documentation outputs, indexes, and cross-links affected
by the migration. Git history may be read to establish provenance.

Existing `docs/98.archive/**` envelopes and payloads are read-only. New unique
history may be appended through the existing ArchiveEnvelope mechanism and
indexed, but no existing digest-sealed record may change. Dated Stage 90
observation bodies retain their historical meaning; only contract-permitted
navigation or explicit annotations may change.

The implementation must not renumber Stage 05 or any lifecycle identifier,
create a Release family, create tutorial/explanation families, change platform
desired state, inspect secret values, authenticate providers, mutate hosted CI,
publish, push, merge, deploy, or operate live infrastructure.

## Contracts

### DTC-1 Work-unit topology

The terminal live route is `docs/03.specs/<NNN>-<slug>/`. `spec.md` is the work
unit owner. `plan.md` is optional but requires the Spec. `tasks.md` is optional
but requires both Spec and Plan. No live Spec, Plan, Task, or index remains
under `docs/04.execution/`.

### DTC-2 Stable identity and date exceptions

Mutable PRD, ARD, ADR, Spec, Plan, Task, Guide, Policy, and Runbook filenames
use stable identifiers or slugs and carry authoring dates in frontmatter.
Dates remain in paths only for dated Stage 90 observation/snapshot identity,
real Incident/Postmortem identity, and Stage 98 historical mirrors. The
registry owns the exact path classes and exceptions.

### DTC-3 Stage and document-family boundary

`docs/05.operations/` remains the only live operations stage and contains
guides, incidents, policies, and runbooks. Stage 04 is unused after execution
retirement. No Release profile, template, folder, lifecycle, or validator is
introduced.

### DTC-4 Authority uniqueness

`document-profiles.json` and its schema are the sole machine owner of routes,
profile IDs, frontmatter keys and states, headings, canonical forms,
relationships, and exceptions. Stage 00 owns agent-facing authoring policy.
Stage 99 `document-contract.md` and `document-lifecycle.md` explain template
and lifecycle rationale. README files are navigation and inventory only.

### DTC-5 Lineage integrity

Existing identifiers are unchanged. Program and standalone lineage remains in
the closed registry relations and reciprocal lifecycle tables; no competing
frontmatter lineage keys are added. The unrelated ADR-0021 association was
corrected atomically when reviewed ADR-0023 was accepted; the registry and
immutable self-test projection now require ADR-0023.

### DTC-6 Route transition

The registry and validators implement explicit `legacy`, `transition`, and
`terminal` route modes. Transition accepts only the enumerated mapping and
rejects duplicate active ownership. Terminal mode rejects every live Stage 04
execution path and every mutable consumer of that path.

### DTC-7 Disposition evidence

Each retired document, contract, script, test, fixture, or generated artifact
has exactly one reviewed disposition: `move-current`, `archive-unique`,
`retain-observation`, `merge-successor`, `delete-redundant`, or
`retain-contract`. Deletion requires a named successor or reproducibility,
zero live consumers, and no unique negative fixture or rule.

### DTC-8 Agent-governance control

The existing harness contract and schema gain a closed `agentSystems` policy
and record-shape section covering purpose, intended/prohibited use,
accountable owner, lifecycle, contextual risk, treatment, residual risk,
review cadence, tool/data trust, oversight, stop conditions, approval/trace
evidence references, evaluation, and component provenance. Actual runtime
records remain at their approved Task, Runbook, Incident, or provider-evidence
owner. Provider adapters contain provider-native deltas only.

The current approval-boundary `Evidence Location` column is the human routing
input. The target harness selects one closed `evidenceOwnerPolicy` whose owner
type is `task`, `runbook-record`, `incident`, or `provider-runtime-record`.
The policy binds a canonical owner reference, allowed append principal class,
immutability rule, retention class, validator, and trust anchor. Missing or
self-asserted identity cannot close approval. The harness schema,
approval-boundary projection, provider evidence contract, and validators must
activate atomically; until then this control remains designed, not enforced.

### DTC-9 Approval and trust boundary

An action requiring approval records `approvalPolicyRef`, `actionClass`,
`approvalId`, `actionFingerprint`, `requesterPrincipal`,
`approverPrincipal`, normalized/redacted target metadata plus digest,
`argumentsDigest`, `authorityScope`, `issuedAt`, `expiresAt`, `decision`,
`approvalEvidenceRef`, and `resultEvidenceRef`. Untrusted prompts, retrieved
context, and tool output remain untrusted until a named control validates or
isolates them. General conversation approval cannot authorize a different
target, arguments, action class, or authority scope.

### DTC-10 Evidence non-promotion

Repository declaration, provider-runtime enforcement, hosted-CI observation,
and authorized remote/live observation are separate states. Each control
separates `designEnforcementDisposition` from
`observedEnforcementEvidenceRef`; the latter remains `DEFER` without matching
provider-runtime evidence. Static schema or adapter validation cannot satisfy
an enforcement or execution state.

### DTC-11 Validator semantic preservation

The aggregate quality gate remains. Selection/orchestration duplication is
consolidated through `validation-surfaces.json`. Registry, Markdown,
links/owners, archive, security, CI, and agent-semantic validators remain
separate where inputs, negative fixtures, failures, or evidence differ.
`validate-harness.sh` is removed only after its live consumers migrate.

### DTC-12 Green terminal baseline

The program closes the recorded registry self-test memory allocation failure,
detect-secrets false-positive/baseline drift, and Markdown heading failure
without disabling the corresponding checks. Every logical commit records
focused and aggregate results; terminal acceptance requires all-files PASS.

## Core Design

### Tranche dependency graph

```text
approved design and recorded baseline
  -> transition fixtures and route support
  -> explicit work-unit mapping and git moves
  -> unique-history archive / redundant-material disposition
  -> Stage 00 and Stage 99 authority consolidation
  -> harness-contract and provider-projection alignment
  -> validator orchestration and generated/memory cleanup
  -> terminal route cutover and PRD-007 resumption handoff
```

Tests and fixtures precede each production contract change. Later tranches may
depend on earlier path moves, but archive creation, rule consolidation,
agent-governance extension, and script retirement remain separate logical
commits so each can be reviewed or reverted independently.

### Work-unit inventory and mapping

The 2026-08-09 baseline contains 49 `spec.md` files, 65 authored Plans, and 67
authored Tasks. The earlier 39-triad/24-orphan/3-orphan-task classification is
a candidate inventory, not an execution truth; it is regenerated from current
HEAD before migration because Spec 053 completed after the earlier census.

The committed mapping enumerates every source, target, work-unit ID, slug,
current status, and disposition. Same-slug correspondence is evidence for
review, not an automatic move rule. A source cannot appear twice, a target
cannot appear twice, and an existing target blocks application.

### Document-governance consolidation

Stage 00's target `rules/document-authoring.md` absorbs the current stage
routing, authoring matrix, checklist, and documentation-protocol rules that
govern agent timing and execution. Stage 99's target
`support/document-contract.md` absorbs template selection, body, frontmatter,
and profile rationale; `support/document-lifecycle.md` absorbs lifecycle,
supersession, retention, archive, and legacy-disposition rationale.

The migration first builds a rule-to-owner ledger. A source document is
deleted only after every non-duplicate rule maps to one target section and all
consumers route to that target. Machine values are removed from prose when the
registry already owns them.

### AI-agent governance integration

The harness contract remains the provider-neutral owner. Its role roster is
not duplicated inside `agentSystems`; systems reference roles, permission
classes, evidence classes, evaluation suites, and provider surfaces by ID.
New schema definitions are closed and have positive and negative fixtures for
risk owner, prohibited use, untrusted data, tool coverage, oversight, stop,
approval binding, trace availability, evaluation adjudication, component
digest, and evidence-class non-promotion.

Existing `current` and `repository-static-evaluation-ready` values are renamed
or explicitly scoped so a reader cannot interpret them as provider enforced.
Consumer docs and adapters migrate in the same logical change as the schema.

### Validator and script disposition

The script audit starts from command consumers in pre-commit, workflows,
`validation-surfaces.json`, root/Stage 00 docs, tests, and active execution
records. Similar names do not establish duplication. For each candidate pair,
the audit compares rule owner, accepted arguments, input domain, exit behavior,
diagnostics, negative fixtures, lane, and downstream evidence.

`validate-repo-quality-gates.sh` is retained. Pre-commit and affected selection
use one declared orchestration path. `validate-harness.sh` is a retire
candidate after root README, PR template, tests, scripts index, and current
work-unit consumers migrate. Active-corpus validators remain until their
current rule and fixture dispositions are proved; historical lifecycle checks
may be quarantined from the hot path but are not deleted without the same
proof.

### One-time and generated cleanup

The progress ledger is rotated only after archived sections are recoverable
and linked. Stale tracked `graphify-out/**` content is treated as a generated
snapshot, verified for consumers and reproducibility, then removed or admitted
through an explicit governed snapshot route. Future scratch output is ignored.
Tracked `__pycache__` or equivalent one-time runtime residue is removed only by
exact path inventory; broad recursive deletion is forbidden.

## Data Modeling & Storage Strategy

### Migration mapping

```json
{
  "schemaVersion": 1,
  "mode": "transition",
  "entries": [
    {
      "source": "docs/04.execution/plans/<legacy-name>.md",
      "target": "docs/03.specs/<NNN>-<slug>/plan.md",
      "workUnit": "Spec-<NNN>",
      "disposition": "move-current",
      "sourceBlob": "<git-blob-sha>",
      "reviewed": true
    }
  ]
}
```

The production artifact may use the existing registry or a temporary ignored
review artifact as selected by the implementation plan. If tracked, it needs a
canonical profile and lifecycle; no unprofiled one-shot file is committed.

### Disposition ledger

The ledger records path, blob identity, classification, current consumer count,
unique rule/fixture count, successor or archive target, reviewer, and result.
Generated output additionally records generator, reproducibility command, and
whether the terminal output is tracked or ignored.

### Harness data

`agentSystems` references existing role, permission, evidence, evaluation, and
surface IDs rather than copying their values. The contract stores policy,
required record shapes, digests, redacted metadata, and immutable evidence
references; actual approval/trace/action records live append-only at the
approved Task, Runbook, Incident, or provider evidence owner. Approval argument
bodies, raw targets, and secret-bearing payloads are never stored. Trace policy
records `traceAvailability`, risk tier, and whether audit evidence is required.
A required but unavailable trace stops or stays `DEFER` unless an approved
operator Runbook records a bounded exception.

`evidenceOwnerPolicies` is a closed list keyed by the canonical
approval-boundary surface. Each entry names the owner type and canonical ID,
append principal class, Git or provider trust anchor, immutability rule,
retention class, and validator. Repository evidence is integrity-bound to a
reviewed Git blob and commit. Provider evidence resolves through
`provider-runtime-evidence.json`; a provider claim without its required
observed identity remains `DEFER`.

### Archive and memory

New ArchiveEnvelope payloads preserve exact source blob bytes and source
commits. Existing envelopes remain unchanged. Progress rotation uses the same
append-only mechanism; the live ledger contains only the approved current
window after recovery validation passes.

## Interfaces & Data Structures

### Route validator interface

The document validators accept an explicit contract mode or derive it from one
closed registry state. They report the mode, selected profile, legacy target,
and ambiguity reason. They never choose a path by declaration order.

```text
validate-document-contract-registry --root . --mode strict --route-state legacy
validate-document-contract-registry --root . --mode strict --route-state transition
validate-document-contract-registry --root . --mode strict --route-state terminal
```

Exact command-line spelling is finalized by the implementation plan and tests;
the three-state behavior and fail-closed results are normative.

### Approval evidence interface

An approval record is created at its approved evidence owner before the action,
binds policy, action class, requester and approver principals, authority scope,
target and arguments digests, expires, and links the later result. Reject,
expiry, principal/scope/target/argument mismatch, missing immutable evidence,
or missing result produces a non-approved state; there is no fallback to a
broader task approval or self-asserted approver string. The owner policy
resolver also rejects an owner class inconsistent with the approval-boundary
surface, a writer outside `appendPrincipalClass`, or an unverifiable Git or
provider trust anchor.

### Validation selection interface

`validation-surfaces.json` remains the only machine owner of surface IDs,
tracked path selection, argv, lane, evidence class, and fallback. Wrappers call
that contract or the aggregate gate; they do not maintain a second validator
inventory.

## Edge Cases & Error Handling

| Condition | Deterministic behavior |
| --- | --- |
| Mapping source is missing, duplicated, or changed from its reviewed blob | Stop before writes and report the source entry. |
| Mapping target already exists or is named by another entry | Stop before writes and report both owners. |
| Transition produces both legacy and target active owners | Fail route validation; do not commit. |
| Plan lacks a sibling Spec, or Task lacks Spec/Plan | Fail work-unit validation with the missing sibling. |
| A date-prefixed mutable file has no registered identity exception | Fail profile validation and name the matched family. |
| Any existing Stage 98 path changes | Stop the tranche; separate new archive/index additions from existing records. |
| A Stage 90 observation body would be rewritten | Stop and require retain/annotation/merge disposition review. |
| A deleted script still has a consumer or unique negative fixture | Retain it and record `retain-contract`. |
| A static record claims provider enforcement or action execution | Fail evidence non-promotion validation. |
| Approval policy, principals, scope, target, argument digest, expiry, or result does not match | Reject the action evidence and require a new approval. |
| Approval evidence owner, append principal, retention, validator, or trust anchor does not match the surface policy | Reject the record; retain `DEFER` and require the canonical owner/controller. |
| Required high-risk trace collection is unavailable | Stop or retain `DEFER`; only a separately approved operator-Runbook exception may proceed. |
| Baseline gate fails for a new reason | Stop and isolate the regression from the recorded pre-change failures. |
| Baseline defect remains at terminal cutover | Do not mark the program done. |

## Failure Modes & Fallback / Human Escalation

Each logical commit must pass its focused tests, affected lane, registry and
document checks, archive diff boundary, `git diff --check`, and the aggregate
gate applicable to its scope. The final state additionally requires
`pre-commit run --all-files` PASS. Recorded baseline failures are not accepted
terminal exceptions.

If a tranche fails, retain its evidence, reverse only that uncommitted tranche
with a reviewed patch or revert its isolated commit, and re-run the last known
green state. Never use a broad destructive reset. Contract consolidation that
cannot preserve a rule or fixture is deferred as `retain-contract`, not forced
through for line-count reduction.

Human escalation is required for any proposed edit to an existing archive
record, uncertain historical disposition, removal of a unique rule or fixture,
unapproved lifecycle identifier change, new document family, evidence-class
promotion, credential or secret access, external write, remote action, or live
mutation.

## Verification Commands

```bash
# Document profile, route, body, and link contracts.
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict

# Archive integrity and agent-governance contracts.
python3 -m unittest tests/test_archive_validation.py
python3 scripts/archive_cutover.py --root .
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-agent-harness-semantics.py --root .

# Aggregate and all-files repository-static evidence.
git diff --check
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
```

The recorded pre-change all-files run failed before design edits: the document
registry self-test could not allocate its configured temporary directory,
detect-secrets reported three existing findings and tried to rewrite its
baseline, and Markdown lint found an H1-to-H3 increment in the completed Spec
053 Plan. The hook-created baseline change was reverted and the isolated
worktree returned to clean. These results are baseline evidence only.

All commands above are repository-static. They do not prove provider runtime,
hosted CI, remote settings, secret safety, deployment, or live operation.

## Success Criteria & Verification Plan

| Criterion ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-WDTC-001 | Every retained Spec/Plan/Task resolves in one Stage 03 work unit and no live Stage 04 execution path remains. | Reviewed mapping, terminal inventory, locality and route negative fixtures. |
| VAL-WDTC-002 | Stage 05 remains stable and no Release-family route or artifact exists. | Path inventory and focused registry/residue search. |
| VAL-WDTC-003 | Mutable authored filenames are date-free and every date-identity exception is registered. | Profile inventory, exception fixtures, and frontmatter preservation diff. |
| VAL-WDTC-004 | PRD-008 lineage uses ADR-0023 and all active relations are reciprocal without renumbering. | Registry, strict links/owners, and lifecycle traceability results. |
| VAL-WDTC-005 | Stage 00/99 prose and the document registry have disjoint human and machine authority. | Rule-to-owner ledger, duplicate-rule scan, profile/template validation. |
| VAL-WDTC-006 | Every removed path has a reviewed disposition and existing Stage 98 records are unchanged. | Disposition ledger, source blobs, archive validation, zero existing-archive diff. |
| VAL-WDTC-007 | Validator/script reduction removes no live consumer, rule, or unique negative fixture. | Consumer graph, semantic comparison, fixture mutation results, declared/executable parity. |
| VAL-WDTC-008 | Harness systems record risk, trust, oversight, approval, trace, evaluation, and provenance with non-promotable evidence. | Schema positive/negative fixtures and agent-governance semantic validation. |
| VAL-WDTC-009 | Progress and generated-output cleanup is recoverable and leaves no unowned tracked artifact. | Archive recovery, consumer/reproducibility checks, ignored-path and registry results. |
| VAL-WDTC-010 | The three pre-change validation failures and all migration regressions are closed. | Aggregate and all-files PASS with explicit secret-finding adjudication. |
| VAL-WDTC-011 | Specs 047–051 remain unexecuted during migration and have a valid consolidated resumption route. | Status, task evidence, and final path inventory. |
| VAL-WDTC-012 | No provider, hosted, remote, credential-bearing, or live result is claimed or performed. | Handoff evidence-class report and change inventory. |

## Traceability

- **Program requirement**:
  [PRD-008](../../01.requirements/008-workspace-document-taxonomy-consolidation.md)
- **Architecture**:
  [ARD-0011](../../02.architecture/requirements/0011-document-taxonomy-consolidation-architecture.md)
- **Accepted decision and PRD-008 lineage authority**:
  [ADR-0023](../../02.architecture/decisions/0023-work-unit-document-taxonomy-and-governance-authority.md)
- **Approved implementation Plan and Task, to move during transition**:
  [legacy Plan](../../04.execution/plans/2026-08-07-document-taxonomy-consolidation.md)
  and [legacy Task](../../04.execution/tasks/2026-08-07-document-taxonomy-consolidation.md)
- **External evidence boundary**:
  [Spec-driven SDLC and document contracts](../../90.references/research/2026-08-08-wer/spec-driven-sdlc-and-document-contracts.md)
  and [AI agents and Agency Agents](../../90.references/research/2026-08-08-wer/ai-agents-and-agency-agents.md)
- **Suspended program**:
  [PRD-007](../../01.requirements/007-repository-delivery-and-platform-assurance.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-WDTC-001](../../01.requirements/008-workspace-document-taxonomy-consolidation.md#functional-requirements) | VAL-WDTC-001 | Mapping and terminal route/locality fixtures prove Stage 03 co-location and Stage 04 retirement. |
| N/A — REQ-WDTC-002 shares the PRD source above. | VAL-WDTC-003 | Filename/frontmatter inventory and exception fixtures prove stable identity. |
| N/A — REQ-WDTC-003 and REQ-WDTC-007 share the PRD source above. | VAL-WDTC-002 | Residue and registry checks prove Stage 05 stability and Release exclusion. |
| N/A — REQ-WDTC-004 shares the PRD source above. | VAL-WDTC-004 | Registry and reciprocal-link validation prove stable lineage. |
| N/A — REQ-WDTC-005 and REQ-WDTC-006 share the PRD source above. | VAL-WDTC-005 | Rule-owner and profile/template checks prove authority separation. |
| N/A — REQ-WDTC-008 through REQ-WDTC-010 share the PRD source above. | VAL-WDTC-006 | Disposition, source-blob, archive, and path results prove safe migration. |
| N/A — REQ-WDTC-011 and REQ-WDTC-012 share the PRD source above. | VAL-WDTC-007 | Consumer, rule, fixture, and parity evidence prove safe script reconciliation. |
| N/A — REQ-WDTC-013 and REQ-WDTC-014 share the PRD source above. | VAL-WDTC-008 | Harness schema and semantic fixtures prove governance and evidence boundaries. |
| N/A — REQ-WDTC-015 shares the PRD source above. | VAL-WDTC-009 | Recovery and reproducibility evidence prove bounded cleanup. |
| N/A — REQ-WDTC-016 shares the PRD source above. | VAL-WDTC-010 | Aggregate and all-files PASS prove baseline and regression closure. |
| N/A — REQ-WDTC-017 shares the PRD source above. | VAL-WDTC-011 | Status and path evidence prove suspension and resumption safety. |
| N/A — REQ-WDTC-018 shares the PRD source above. | VAL-WDTC-012 | Evidence-class handoff proves local-only scope. |
