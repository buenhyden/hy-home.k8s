---
title: 'GitHub CI and QA Evidence Technical Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-07-15
---

# GitHub CI and QA Evidence Technical Specification (Spec)

## Overview

This Spec aligns .github automation, pre-commit, repository validators, AI
agent obligations, artifact retention, and protected-surface evidence with the
new lifecycle and archive contracts. It also closes the current portability
defect in the GitOps change-set self-test without weakening its non-regular-file
coverage.

## Strategic Boundaries & Non-goals

- **In scope**: .github workflows and native forms, pre-commit lanes,
  affected-surface selection, full-document escalation, aggregate verdict,
  Action identity/permissions, artifact retention, relevant validators and
  fixtures, and QA guidance.
- **Non-goals**: Live deployment, Kubernetes or Vault mutation, remote
  branch-protection changes, secret inspection, release publication, or
  relabeling skipped tools as passing.

## Contracts

- The required CI workflow always starts; internal work may be conditional.
- ci-summary is the single aggregate remote verdict.
- Affected checks provide fast feedback, but registry, schema, template,
  governance, validator, and bulk archive changes escalate to global document
  validation.
- AI agents run staged/affected checks during work and pre-commit across all
  files before each logical commit.
- Third-party Actions use full commit SHA identity and least permissions.
- Changelog preview is transient, non-canonical evidence retained for seven
  days.
- Optional, remote, and live evidence uses PASS, SKIP, FAIL, and DEFER
  accurately.

## Core Design

One affected-surface registry maps paths to local hooks, repository validators,
CI jobs, evidence lanes, and escalation rules. GitHub path filters do not own
required-check behavior because documented diff and skip limits can leave a
required workflow unresolved. The workflow starts and its aggregate job
interprets internal job outcomes.

Document-contract changes select registry/schema, Markdown profiles,
cross-document owners/links, archive integrity, historical links, generated
outputs, repository quality, native workflow validation, and the final
aggregate.

The GitOps change-set self-test replaces its unconditional FIFO creation with a
portable capability-aware fixture. Unsupported FIFO creation must still test
the boundary through a deterministic alternative or report an explicit SKIP;
the self-test cannot abort with an uncaught filesystem error.

## Data Modeling & Storage Strategy

CI evidence is classified as commit evidence, transient artifact, repository
closure record, or remote/live evidence. Only repository closure records are
durable program evidence. Artifact retention is explicit per workflow.

Selector fixtures cover changed paths, coupled paths, workflow paths, archive
payloads, templates, references, and protected surfaces. Exhaustive path facts
remain in the affected-surface owner rather than copied into workflow YAML.

## Interfaces & Data Structures

- Local interface: staged, affected, all-files, manual, and live lanes.
- Selector interface: changed path set to validators, jobs, escalation, and
  evidence classification.
- Workflow interface: always-running entry, conditional jobs, aggregate result,
  explicit permissions, immutable Action identity, and retention.
- Portability interface: capability probe, covered fallback, or named SKIP
  without traceback.

The implementation follows official pre-commit changed-ref/all-files modes and
GitHub's workflow, security, and artifact-retention guidance:

- https://pre-commit.com/
- https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
- https://docs.github.com/en/actions/reference/security/secure-use
- https://docs.github.com/en/organizations/managing-organization-settings/configuring-the-retention-period-for-github-actions-artifacts-and-logs-in-your-organization

## Edge Cases & Error Handling

- A docs-only change can still select global validation when it changes a
  machine contract.
- A skipped internal job does not make ci-summary disappear.
- Missing optional tooling is distinct from a failed required validator.
- An unsupported FIFO filesystem does not bypass boundary coverage silently.
- Remote branch rules and workflow results remain DEFER until independently
  observed.

## Failure Modes & Fallback / Human Escalation

- If path filters cannot represent a coupled surface, select a conservative
  repo-owned escalation rather than skipping the workflow.
- If a portability fallback cannot prove the non-regular-file boundary, retain
  an explicit SKIP and open a bounded test-environment follow-up.
- If artifact consumers require longer retention, change the duration only
  through a named consumer decision.

## Verification Commands

- Run affected-surface selector self-tests and positive/negative fixtures.
- Run the GitOps change-set self-test on the current filesystem.
- Run actionlint, zizmor, YAML validation, and workflow contract checks.
- Run staged, affected, repository quality, and all-files pre-commit lanes.
- Record remote and live checks separately as DEFER when not observed.

## Success Criteria & Verification Plan

- **VAL-GCQE-001**: Required workflow entry and ci-summary always exist for
  supported events.
- **VAL-GCQE-002**: Contract and bulk-migration paths select the full document
  gate.
- **VAL-GCQE-003**: Action identities, permissions, and artifact retention pass
  native and repository checks.
- **VAL-GCQE-004**: The GitOps self-test completes without uncaught FIFO errors
  while preserving boundary evidence.
- **VAL-GCQE-005**: AI-agent completion guidance requires all-files pre-commit
  and review of formatter changes.
- **VAL-GCQE-006**: PASS, SKIP, FAIL, and DEFER remain distinct in aggregate and
  handoff evidence.

## Traceability

- **Foundation**: [Spec 035](../035-document-schema-and-lifecycle-contract/spec.md)
- **Final integrator**: [Spec 040](../040-contract-cutover-and-program-closure/spec.md)
- **PRD**: [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **ARD**: [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-WDLEC-010](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-GCQE-001 | Workflow fixtures assert entry and aggregate topology. |
| [REQ-WDLEC-010](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-GCQE-002 | Selector fixtures cover every contract and migration path class. |
| [REQ-WDLEC-010](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-GCQE-003 | actionlint, zizmor, and repository policy checks pass. |
| [REQ-WDLEC-010](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-GCQE-004 | Portability fixtures run on FIFO-capable and unsupported environments. |
| [REQ-WDLEC-011](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-GCQE-005 | Agent QA contract and all-files evidence are checked together. |
| [REQ-WDLEC-012](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-GCQE-006 | Result-class fixtures reject SKIP/DEFER as PASS. |
