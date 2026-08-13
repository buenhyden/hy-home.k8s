---
title: 'GitHub CI and QA Evidence Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-07-27
artifact_id: "SPEC-0039"
---

# GitHub CI and QA Evidence Technical Specification (Spec)

## Overview

This Spec aligns .github automation, pre-commit, repository validators, AI
agent obligations, artifact retention, and protected-surface evidence with the
new lifecycle and archive contracts. It also closes the current portability
defect in the GitOps change-set self-test without weakening its non-regular-file
coverage.

The latest observed public `main` run, GitHub Actions run `29982910320` for
commit `bd93374d7f531317c3bd061eb1ef567c1e2e0084`, failed its `pre-commit`,
`repo-quality-static`, and aggregate jobs. The pre-commit environment lacked
repository system-hook dependencies and emitted a Node.js 20 deprecation
warning through `pre-commit/action`. This remote result is historical evidence
for the observed SHA; it is not a result for the current local branch.

GCQE-001 through GCQE-005 completed the reviewed repository-static
implementation through `7b536d1` and the committed integration evidence at
`aaee364`. Test-only commit
`096c5c48e364663c616a1984089c11a1fe5b3b61` fixed final-tranche lifecycle
fixtures and received `REQUIREMENTS COMPLIANT` / `QUALITY APPROVED` from
`/root/gcqe006_selftest_rapid_review`. Commit
`b5c3eea128b8b3be7c858f70803f83994be1fc77` advanced the active-corpus
validator to the exact Spec 039-done / Spec 040-active frontier and received
`REQUIREMENTS COMPLIANT` from `/root/gcqe006_frontier_requirements_review` and
`QUALITY APPROVED` from `/root/gcqe006_frontier_quality_review`. Test-only
commit `39e6150a6f7a79b710d0e2cd7bc2dee8349f871a` then bound current/advanced
assertions to exact index object identities; fresh reviewers
`/root/gcqe006_test_compat_requirements_review` and
`/root/gcqe006_test_compat_fresh_quality` returned `REQUIREMENTS COMPLIANT`
and `QUALITY APPROVED`. These scoped verdicts do not constitute whole-tranche
terminal approval.

GCQE-006 closed on 2026-07-27 in commit
`e1d1e910840337327a557ab4b84e86f8fced11d6`, with activation commit
`2ddfe4b7697e998b41d3125be94cdc4cee295388` as the explicit-ref origin. The
closure commit contains exactly
`docs/00.agent-governance/memory/progress.md`,
`docs/03.specs/0039-github-ci-qa-evidence/spec.md`,
`docs/03.specs/README.md`,
`docs/04.execution/plans/2026-07-26-github-ci-qa-evidence.md`,
`docs/04.execution/plans/README.md`,
`docs/04.execution/tasks/2026-07-26-github-ci-qa-evidence.md`,
`docs/04.execution/tasks/README.md`, and
`docs/99.templates/support/document-profiles.json`. Those paths atomically
record the terminal Spec/Plan/Task and index state plus the registry-owned
PRD-0006 program-lineage transition for Spec 039 while Spec 040 remains
`active`.

Advanced-state verification passed the 46-test residue class, 84-test module,
22-case residue self-test, exact `0/0` active controls, `4/2` terminal
controls, two terminal Specs, `13/29` guards, repository aggregate, 668-case
lifecycle self-test, staged lifecycle, and strict document gates. Earlier
terminal reviews found rollback omissions, the old-frontier aggregate failure,
three staged old-state assertions, and an index-OID P1; all remain recorded and
remediated. After the sole remaining invalid explicit-ref finding was
corrected, `/root/gcqe006_final_requirements` returned `REQUIREMENTS
COMPLIANT` and `/root/gcqe006_final_quality` returned `QUALITY APPROVED`, with
no findings against staged patch digest
`58640a0d26c08b4ab5872c0a69be2966610f796b4b1e906a5e3ebae0033758cc`.
Postflight then passed explicit-ref lifecycle with the two raw OIDs, the CI
Python contract at `3` jobs / `3` pins, GitHub Actions security, the GitOps
self-test, the clean-tree repository aggregate, and all applicable all-files
hooks; Dockerfile lint was a no-file `SKIP`. Status, diff, and diff-check
inspection were clean. Hosted run `29982910320` remains historical FAIL
evidence for its older SHA, and current hosted, provider, and live evidence
remains `DEFER`. This later evidence update does not identify or claim its own
commit.

## Strategic Boundaries & Non-goals

- **In scope**: .github workflows and native forms, pre-commit lanes,
  affected-surface selection, full-document escalation, aggregate verdict,
  Action identity/permissions, artifact retention, relevant validators and
  fixtures, one pinned CI validation-dependency contract, replacement of the
  deprecated `pre-commit/action` execution path, and QA guidance.
- **Non-goals**: Live deployment, Kubernetes or Vault mutation, remote
  branch-protection changes, secret inspection, release publication, or
  relabeling skipped tools as passing. Push and workflow dispatch require
  separate approval.

## Contracts

- The required CI workflow always starts; internal work may be conditional.
- ci-summary is the single aggregate remote verdict.
- Affected checks provide fast feedback, but registry, schema, template,
  governance, validator, and bulk archive changes escalate to global document
  validation.
- AI agents run staged/affected checks during work and pre-commit across all
  files before each logical commit.
- Third-party Actions use full commit SHA identity and least permissions.
- CI-owned Python dependencies used by repository `language: system` hooks are
  installed from one exact-version file before pre-commit or repository
  quality execution.
- The pre-commit job invokes `pre-commit run --all-files` explicitly instead of
  delegating execution and cache behavior to `pre-commit/action`.
- Changelog preview is transient, non-canonical evidence retained for seven
  days.
- Optional, remote, and live evidence uses PASS, SKIP, FAIL, and DEFER
  accurately.
- The settled 446-row Spec 030 migration ledger is a protected terminal
  snapshot. Post-settlement Plan/Task admission is governed by the current
  registry, lifecycle, reciprocal-link, and index contracts, not by appending
  new rows to that ledger.

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

The CI jobs that execute repository system hooks install the same pinned
validation dependencies before running their commands. A dependency failure is
a required-lane FAIL, not an optional SKIP. Removing `pre-commit/action` also
removes its transitive Node.js runtime warning without changing the
repository's all-files completion contract.

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
- A public run for an older SHA remains valid historical evidence but cannot be
  promoted to a current-HEAD result.

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
- Record run `29982910320` as observed FAIL for its exact SHA and retain the
  post-change remote rerun as DEFER until a separately approved push executes.

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

- **Foundation**: [Spec 035](../0035-document-schema-and-lifecycle-contract/spec.md)
- **Final integrator**: [Spec 040](../0040-contract-cutover-and-program-closure/spec.md)
- **PRD**: [PRD-0006](../../01.requirements/0006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **AD**: [AD-0009](../../02.architecture/descriptions/ad-0009-document-lifecycle-evidence-operating-model.md)
- **Plan**: [GitHub CI and QA Evidence Plan](plan.md)
- **Task**: [GitHub CI and QA Evidence Task](tasks.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-WDLEC-010](../../01.requirements/0006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-GCQE-001 | Workflow fixtures assert entry and aggregate topology. |
| N/A — REQ-WDLEC-010 / VAL-GCQE-002 shares the PRD-0006 source linked in VAL-GCQE-001 | VAL-GCQE-002 | Selector fixtures cover every contract and migration path class. |
| N/A — REQ-WDLEC-010 / VAL-GCQE-003 shares the PRD-0006 source linked in VAL-GCQE-001 | VAL-GCQE-003 | actionlint, zizmor, and repository policy checks pass. |
| N/A — REQ-WDLEC-010 / VAL-GCQE-004 shares the PRD-0006 source linked in VAL-GCQE-001 | VAL-GCQE-004 | Portability fixtures run on FIFO-capable and unsupported environments. |
| N/A — REQ-WDLEC-011 / VAL-GCQE-005 shares the PRD-0006 source linked in VAL-GCQE-001 | VAL-GCQE-005 | Agent QA contract and all-files evidence are checked together. |
| N/A — REQ-WDLEC-012 / VAL-GCQE-006 shares the PRD-0006 source linked in VAL-GCQE-001 | VAL-GCQE-006 | Result-class fixtures reject SKIP/DEFER as PASS. |
