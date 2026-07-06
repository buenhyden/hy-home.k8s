---
title: 'Stage 03/04 Repo-Static Gap Closure Technical Specification'
type: sdlc/spec
status: draft
owner: platform
updated: 2026-07-06
---

# Stage 03/04 Repo-Static Gap Closure Technical Specification

## Overview

This specification defines a repo-static gap-closure pass for the authored
documents under `docs/03.specs/`, `docs/04.execution/plans/`, and
`docs/04.execution/tasks/`.

The approved scope is intentionally narrow: close implementation and evidence
gaps that can be resolved with repository-local document, governance,
validation, or index changes. Live runtime validation, secret value
inspection, remote GitHub changes, cloud/provider mutation, and operator-only
actions must be separated into explicit operator-approved follow-up records.

The first confirmed repo-static gap is the Workspace Engineering Research Pack
stream: the Stage 04 Plan and Task record show all WER work as complete, but
their document frontmatter and README indexes remain `draft`.

## Strategic Boundaries & Non-goals

In scope:

- Audit Stage 03 and Stage 04 document status, task tables, phase checklists,
  completion criteria, README indexes, and progress-memory handoff evidence.
- Implement repo-static closures where local evidence already proves the work
  is complete or where the gap can be closed by updating docs, contracts,
  governance, validators, or indexes.
- Preserve historical evidence without rewriting old execution facts into
  false current-state claims.
- Add or update deterministic validator coverage only when the rule is
  bounded, low-noise, and aligned with existing Stage 03/04 contracts.
- Record live/runtime, secret, remote, or provider-required items as
  operator-approved follow-up, not as completed implementation.

Out of scope:

- Live Kubernetes, Argo CD, Vault, External Secrets Operator, cloud, DNS,
  provider runtime, or third-party system mutation.
- Secret value inspection, credential regeneration, token changes, or
  certificate changes.
- Remote GitHub settings, branch protection, ruleset, workflow dispatch,
  PR creation, push, publish, or merge actions.
- Broad semantic reclassification of every historical `draft` Stage 03 spec
  unless repo evidence proves completion and the active README contract
  already supports that lifecycle transition.
- Runtime readiness claims based only on repo-static validation.

## Related Inputs

- **PRD**: No dedicated PRD exists. The controlling input is the approved user
  request to inspect Stage 03/04 content, identify unimplemented items,
  implement repo-static gaps first, and separate runtime/operator work.
- **ARD**: No dedicated ARD exists. The relevant architecture is the current
  documentation taxonomy and lifecycle contract.
- **Related ADRs**: None.
- **Related Specs**:
  - [Workspace Engineering Research Pack](../017-workspace-engineering-research-pack/spec.md)
  - [Workspace Engineering Implementation Audit Pack](../018-workspace-engineering-implementation-audit-pack/spec.md)
  - [Template Path Numbering Contract](../019-template-path-numbering-contract/spec.md)
  - [Workspace Contract Governance Normalization](../020-workspace-contract-governance-normalization/spec.md)
  - [SDLC Lifecycle Contract](../021-sdlc-lifecycle-contract/spec.md)
  - [Control Surface and Cloud Example Documentation Normalization](../022-control-cloud-doc-normalization/spec.md)

## Contracts

- **Config Contract**:
  - No runtime configuration, manifest semantics, provider adapter settings,
    credentials, or remote settings are changed by this specification.
  - Repo-static validation scripts may be updated only to enforce documented
    Stage 03/04 lifecycle and evidence rules.
- **Data / Interface Contract**:
  - Stage 03 specs use numbered feature folders and `sdlc/spec` frontmatter.
  - Stage 04 plans and tasks use `sdlc/plan` and `sdlc/task` frontmatter,
    README index rows, and evidence sections that must agree on status and
    updated date.
  - Gap records must distinguish `repo-static`, `operator-approved`, and
    `out-of-scope` evidence lanes.
- **Governance Contract**:
  - Stage 03 owns design contracts.
  - Stage 04 owns execution status and validation evidence.
  - Stage 00, Stage 05, Stage 90, Stage 99, scripts, workflows, and policy
    files remain canonical owners for their existing domains.
  - Operator-approved follow-up must not masquerade as completed repo-static
    implementation.

## Core Design

- **Component Boundary**:
  - `Stage 03/04 gap audit`: scans status, indexes, task tables, completion
    criteria, and live/runtime boundary language.
  - `Repo-static closure`: applies local changes for gaps whose evidence is
    already present or can be made present without external mutation.
  - `Operator follow-up ledger`: records live/runtime, secret, remote, and
    provider items with explicit approval boundaries.
  - `Validator hardening`: adds focused checks for drift that the repository
    can reliably detect.
  - `Evidence closure`: updates Stage 04 task records, progress memory, and
    README indexes after validation.
- **Key Dependencies**:
  - Existing Stage 03/04 README index validation.
  - `scripts/validate-repo-quality-gates.sh`.
  - Stage 04 evidence from prior completed work.
  - Existing progress ledger entries under
    `docs/00.agent-governance/memory/progress.md`.
- **Tech Stack**:
  - Markdown, shell, Python embedded in repository validation scripts, `rg`,
    `git`, and existing repo-static validation scripts.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - Gap records are stored in a Stage 04 task document using a table with:
    `Gap ID`, `Source`, `Evidence lane`, `Finding`, `Resolution`,
    `Owner`, and `Status`.
  - `Evidence lane` values are:
    - `repo-static`: resolvable through repository files and local validation.
    - `operator-approved`: requires explicit approval for live/runtime,
      credential, remote, or provider action.
    - `out-of-scope`: intentionally excluded or superseded.
  - Completion updates must keep frontmatter, README index status, and README
    index updated-date fields synchronized.
- **Migration / Transition Plan**:
  - Add Stage 04 plan/task records for this spec.
  - Audit the target stages and populate the gap table.
  - Close repo-static gaps in logical commits.
  - Add follow-up rows for operator-approved gaps.
  - Run final validation and close the Stage 04 evidence.

## Interfaces & Data Structures

### Core Interfaces

```typescript
type EvidenceLane = "repo-static" | "operator-approved" | "out-of-scope";
type GapStatus = "Open" | "Closed" | "Follow-up";

interface StageGapRecord {
  id: string;
  source: string;
  evidenceLane: EvidenceLane;
  finding: string;
  resolution: string;
  owner: "platform" | "operator";
  status: GapStatus;
}
```

## API Contract (If Applicable)

This work exposes no application API. No OpenAPI, GraphQL, protobuf, or public
runtime API contract is required.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Documentation lifecycle auditor and repo-static remediation
  implementer.
- **Inputs**: This spec, Stage 03 specs, Stage 04 plans/tasks, README indexes,
  progress memory, Stage 00/99 governance contracts, and local validation
  output.
- **Outputs**: Stage 04 plan/task records, repo-static remediation commits,
  optional validator updates, operator-approved follow-up records, progress
  memory, and validation evidence.
- **Success Definition**: All repo-static gaps identified in scope are either
  closed or explicitly classified. Runtime/operator-only gaps are separated
  without being reported as implemented.

## Tools & Tool Contract (If Applicable)

- **Tool List**:
  - `rg` for fast repository discovery.
  - `sed` for targeted file reads.
  - `apply_patch` for manual edits.
  - `git` for branch, staging, commits, and history inspection.
  - Existing validation scripts for final evidence.
- **Permission Boundary**:
  - Repository-local reads and writes are allowed.
  - Live runtime, remote GitHub, credential, provider, cloud, and third-party
    actions require a separate explicit approval.
- **Failure Handling**:
  - If a gap cannot be closed without external mutation, move it to the
    operator-approved follow-up lane.
  - If a validator rule is too broad or noisy, record the finding in the task
    evidence instead of adding the rule.

## Prompt / Policy Contract (If Applicable)

- Do not treat `draft` as automatically unimplemented.
- Do not treat a `Done` task table as sufficient by itself; verify frontmatter,
  README index, completion criteria, and validation evidence.
- Do not claim live/runtime readiness from repo-static checks.
- Keep historical plan command literals and evidence blocks intact unless they
  are current active contradictions.

## Memory & Context Strategy (If Applicable)

- Durable progress and reusable lessons go in
  `../../00.agent-governance/memory/progress.md`.
- The Stage 04 task record is the canonical execution ledger for this pass.
- Untracked pre-existing files remain user-owned unless explicitly brought
  into scope.

## Guardrails (If Applicable)

- **Input Guardrails**:
  - Read Stage 03/04 files before classifying a gap.
  - Treat generated or historical evidence as evidence, not active policy.
  - Preserve existing user-owned untracked files.
- **Output Guardrails**:
  - Use relative links based on final file locations.
  - Keep README updates to structure/index/status alignment.
  - Keep follow-up records explicit about approval boundaries.
- **Blocked Conditions**:
  - A requested closure requires secret values, live cluster access, remote
    GitHub settings, provider mutation, or third-party state changes.
  - Evidence conflicts and cannot be reconciled from repository history.
- **Escalation Rule**:
  - Stop and request explicit operator approval before live/runtime, secret,
    remote, or provider actions.

## Evaluation (If Applicable)

- **Eval Types**:
  - Status and index drift audit.
  - Repo-static gap classification review.
  - Validator regression check.
  - Final self-review against this spec.
- **Metrics**:
  - Zero Stage 04 README index status/date mismatches for touched documents.
  - Zero open repo-static gaps in the scoped task ledger.
  - All operator-required gaps are recorded as follow-up, not implemented.
  - Repository validation passes.
- **Datasets / Fixtures**:
  - Current `docs/03.specs/**`.
  - Current `docs/04.execution/plans/**`.
  - Current `docs/04.execution/tasks/**`.
  - Existing validation scripts.
- **How to Run**:
  - `git diff --check`
  - `bash -n scripts/validate-repo-quality-gates.sh`
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `bash scripts/validate-k8s-manifests.sh .`
  - `bash scripts/check-secret-handling.sh .`
  - `bash scripts/validate-policy-gates.sh .`

## Edge Cases & Error Handling

- **Draft spec with completed execution evidence**: do not automatically mark
  the spec done. Close the Stage 04 evidence first, then update the spec only
  if the lifecycle contract supports it.
- **Done task with pending live validation**: keep the task done for
  repo-static implementation only and record live validation as
  operator-approved follow-up.
- **Historical command literals containing stale paths or statuses**: preserve
  them when they describe past execution and do not break active links.
- **Missing optional tools**: report script-supported optional skips
  accurately.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: A repo-static gap actually requires live/runtime access.
  **Fallback**: Reclassify as `operator-approved` follow-up.
  **Human Escalation**: Required before running live or remote actions.
- **Failure Mode**: A validator hardening idea causes false positives.
  **Fallback**: Drop the validator change and preserve the finding in task
  evidence.
  **Human Escalation**: Not required unless the contract must change.
- **Failure Mode**: Stage 03/04 status semantics conflict.
  **Fallback**: Update support/governance contract text before editing many
  documents.
  **Human Escalation**: Required if the lifecycle model itself changes.

## Verification Commands

```bash
git diff --check
bash -n scripts/validate-repo-quality-gates.sh
bash scripts/validate-repo-quality-gates.sh .
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
bash scripts/validate-policy-gates.sh .
```

## Success Criteria & Verification Plan

- **VAL-SPC-023-001**: Stage 03/04 repo-static gaps are discovered and
  classified into `repo-static`, `operator-approved`, or `out-of-scope`.
- **VAL-SPC-023-002**: The Workspace Engineering Research Pack Stage 04
  Plan/Task lifecycle drift is closed when evidence confirms all WER tasks are
  complete.
- **VAL-SPC-023-003**: Runtime, secret, remote, or provider-required work is
  recorded as operator-approved follow-up and not counted as repo-static
  implementation.
- **VAL-SPC-023-004**: Any validator updates are narrow, deterministic, and
  pass the existing repository quality gate.
- **VAL-SPC-023-005**: Stage 04 task evidence and progress memory record final
  validation output and remaining approval boundaries.

## Related Documents

- **Spec**: [Workspace Engineering Research Pack](../017-workspace-engineering-research-pack/spec.md)
- **Spec**: [SDLC Lifecycle Contract](../021-sdlc-lifecycle-contract/spec.md)
- **Plan**: [../../04.execution/plans/2026-07-04-workspace-engineering-research-pack.md](../../04.execution/plans/2026-07-04-workspace-engineering-research-pack.md)
- **Tasks**: [../../04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md](../../04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md)
- **Template Routing**: [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
- **Frontmatter Schema**: [../../99.templates/support/frontmatter-schema.md](../../99.templates/support/frontmatter-schema.md)
- **Progress Memory**: [../../00.agent-governance/memory/progress.md](../../00.agent-governance/memory/progress.md)
