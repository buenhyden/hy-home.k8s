---
title: 'GitHub Routing and CI Evidence Technical Specification'
version: "1.0.0"
type: sdlc/spec
layer: "specs"
status: draft
owner: platform
updated: 2026-08-02
artifact_id: "SPEC-0048"
---

# GitHub Routing and CI Evidence Technical Specification (Spec)

## Overview

This specification closes the repository-static GitHub projection and CI
evidence gaps handed off by Spec 047. It introduces one surface-ID-based
contract for label and CODEOWNERS parity, corrects current native projection
drift, keeps intentional validation jobs separate, and records read-only remote
GitHub observations without claiming hosted evidence for unpushed local work.

The observed remote repository had six active workflows including Dependabot,
required only `ci-summary`, and showed repeated historical CI failures for a
remote SHA behind local `main`. Those facts are dated remote evidence, not a
reason to rewrite local job topology or weaken the aggregate verdict.

## Strategic Boundaries & Non-goals

- **Owns**: GitHub surface-routing contract and schema; projection validator;
  labeler and CODEOWNERS parity; workflow/document claim consistency; primary
  validator-lane ownership; remote metadata evidence; fixtures; and CI handoff.
- **Consumes**: Spec 047 current matrix, `validation-surfaces.json`, native
  `.github` controls, existing CI validators, workflow security checks, and
  read-only repository/workflow/branch metadata.
- **Does not own**: path regexes, document lifecycle, agent semantics, platform
  validation depth, branch-protection settings, reviewer enrollment, hosted
  reruns, or live infrastructure.
- **Non-goals**: merging jobs because commands share dependencies; adding path
  filters that can leave a required workflow pending; requiring an unavailable
  second reviewer; reading secret-bearing workflow logs; pushing; dispatching;
  or mutating GitHub settings.

## Contracts

### Canonical projection contract

`docs/00.agent-governance/contracts/github-surface-routing.json` is the sole
mapping from existing validation surface IDs to expected GitHub label and
CODEOWNERS projection classes. It must:

- identify `validation-surfaces.json` and its compatible schema version;
- reference surface IDs instead of copying exact or regex routes;
- assign at most one label class and one owner class per mapped surface;
- record explicit exceptions with limitation, owner, and retry trigger;
- reject unknown surface IDs, duplicate mappings, route copies, unowned
  exceptions, and projection-state ambiguity;
- remain repository-static evidence rather than a branch-protection or hosted
  workflow result.

The validator resolves current tracked paths through the validation-surface
owner, then evaluates native labeler glob semantics and CODEOWNERS last-match
semantics. The comparison proves effective projection and explicit ownership,
not merely presence of similar strings.

### CI topology contract

- `ci.yml` remains the required workflow and always exposes `ci-summary` for
  supported events.
- `pre-commit`, `repo-quality-static`, `agent-governance-static`, and
  `manifest-static` remain independent evidence jobs.
- A focused validator has one primary execution owner inside a lane. A job may
  consume or aggregate its result without rerunning the same command graph.
- The aggregate repository script does not absorb a focused agent-governance
  closure command when the agent lane and pre-commit hooks already own its
  required execution.
- Action references remain full commit SHAs; permissions stay least-privilege;
  concurrency, timeouts, and artifact retention remain explicit.
- The changelog workflow remains tag-triggered, transient, and non-mutating;
  documentation must not claim a manual trigger that is absent from YAML.

### Review policy boundary

The current CODEOWNERS file may express explicit path ownership, but remote
enforcement of one CODEOWNER approval remains `DEFER` while read-only metadata
shows one eligible collaborator. The trigger is a second eligible reviewer plus
green hosted CI for the intended baseline. This Spec does not change branch
protection, rulesets, admin enforcement, conversation resolution, linear
history, merge methods, or branch-deletion settings.

## Core Design

Implementation proceeds in five steps:

1. Add the closed routing contract/schema and positive/negative fixture set.
2. Add a validator that resolves surface routes, expands the tracked corpus,
   evaluates effective labeler and CODEOWNERS behavior, and emits deterministic
   diagnostics.
3. Add `.agents/**` and `.gemini/**` to the `area/agent` label projection and
   explicit agent ownership class without changing the global fallback owner.
4. Correct `.github/repository-surface.md` so the changelog row describes tag-only
   execution and documents intentional CI lane ownership without copying the
   contract inventory.
5. Wire the focused validator once into repository quality and the appropriate
   affected/CI selection, then record remote metadata as a separate result.

No workflow or job is removed unless comparison proves identical trigger,
owner, command graph, output, retention, and required-check semantics. The
current five tracked workflow files and eleven unique job identifiers do not
meet that duplicate threshold.

## Data Modeling & Storage Strategy

The routing contract contains:

- `schemaVersion`, `contractId`, and `sourceContract`;
- an ordered `mappings` array with `surfaceId`, `labelClass`, `ownerClass`,
  and `projectionState`;
- a closed owner-class table containing GitHub identities without credentials;
- bounded exceptions with limitation, owner, retry trigger, and evidence lane;
- remote observation metadata containing repository, observed SHA, timestamp,
  and result only when refreshed by an authorized read-only command.

Native `.github/labeler.yml` and `.github/CODEOWNERS` remain executable
projections. Workflow YAML remains the job and trigger owner. The routing
contract must not store workflow bodies, branch-protection settings, tokens,
logs, or duplicated path patterns.

## Interfaces & Data Structures

| Interface | Input | Output | Failure behavior |
| --- | --- | --- | --- |
| Surface resolver | Tracked path and `validation-surfaces.json` | Exactly one applicable routing context | Fail on unknown or ambiguous surface ownership. |
| Labeler evaluator | Native labeler rules and changed path | Effective label set | Fail on missing required label, unexpected mapped label, or unsupported rule shape. |
| CODEOWNERS evaluator | Native rules and tracked path | Effective owner identity and explicit class | Fail on missing effective owner or required explicit class drift. |
| Workflow topology validator | Native workflows and validator owner map | Job, dependency, trigger, and aggregate evidence | Fail on missing `ci-summary`, duplicate primary execution, unpinned Action, or overbroad permissions. |
| Remote observer | Read-only GitHub metadata | SHA-bound `PASS`, `FAIL`, or `DEFER` observation | Never infer a result for a different SHA or read logs by default. |

The implementation follows GitHub's official secure-use guidance for immutable
Action identity and least privilege, CODEOWNERS last-match behavior, reusable
workflow guidance, concurrency semantics, and the documented risk that skipped
required workflows can remain pending:

- https://docs.github.com/en/actions/reference/security/secure-use
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- https://docs.github.com/en/actions/concepts/workflows-and-actions/reusing-workflow-configurations
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency
- https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs

## Edge Cases & Error Handling

- A path may receive the global CODEOWNER and still lack the required explicit
  agent ownership class; effective and explicit coverage are reported
  separately.
- CODEOWNERS last-match semantics can override an earlier specific-looking
  pattern; fixtures must cover ordering and directory anchors.
- A surface may intentionally map to no label. It requires a bounded exception,
  not an omitted row or implicit null.
- A docs-only change can select global validation when it changes a machine
  contract, schema, workflow, or broad routing owner.
- Dependabot can be active remotely without a tracked workflow YAML; it is
  remote platform automation and must not be fabricated as a local file.
- A historical failed run remains valid for its exact SHA but cannot fail or
  pass the current local branch.
- If a workflow log is required for root-cause analysis, obtain separate
  approval and apply redaction; metadata-only evidence leaves cause unresolved.

## Failure Modes & Fallback / Human Escalation

- **Projection ambiguity**: fail the routing validator and correct the machine
  mapping or native projection; do not add precedence prose.
- **Required workflow can be skipped**: keep the entry workflow unconditional
  and condition internal work, preserving `ci-summary`.
- **Apparent duplicate job**: require exact semantic comparison before merge;
  otherwise document intentional overlap and primary command owner.
- **Solo-review deadlock**: retain explicit CODEOWNERS but defer approval
  enforcement until the reviewer trigger is met.
- **Hosted failure without safe cause evidence**: record remote FAIL and cause
  `DEFER`; do not weaken local gates.
- **Remote mutation request**: stop and obtain separate human approval for the
  exact setting, repository, rollback, and expected check names.

## Verification Commands

```bash
python3 scripts/validate-github-surface-routing.py --root . --self-test
python3 scripts/validate-github-surface-routing.py --root .
python3 -m unittest tests/test_validate_github_surface_routing.py
actionlint
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
git diff --check
```

The first three commands are Spec 048 deliverables and do not exist until the
implementation Plan creates their contract, schema, validator, and fixtures.
Read-only `gh` metadata commands are recorded separately in the Task with the
observed repository and SHA.

## Success Criteria & Verification Plan

- **VAL-GRCE-001**: The routing contract/schema rejects copied routes, unknown
  surfaces, duplicate mappings, unowned exceptions, and unsupported versions.
- **VAL-GRCE-002**: `.agents/**`, `.claude/**`, `.codex/**`, `.gemini/**`, root
  provider gateways, and Stage 00 governance resolve the expected agent label
  and explicit CODEOWNERS class.
- **VAL-GRCE-003**: Native labeler and CODEOWNERS effective behavior matches
  every mapped tracked path and all negative ordering fixtures.
- **VAL-GRCE-004**: Current workflow triggers, job ownership, full-SHA actions,
  permissions, concurrency, timeouts, retention, and `ci-summary` pass native
  and repository checks with no duplicated primary validator execution.
- **VAL-GRCE-005**: `.github/repository-surface.md` describes tag-only changelog execution
  and does not duplicate policy or machine inventories.
- **VAL-GRCE-006**: Remote run and branch metadata remains timestamped,
  SHA-bound, read-only evidence; current unpushed hosted evidence stays DEFER.
- **VAL-GRCE-007**: Reviewer-enforcement deferral records the second-reviewer
  and green-CI triggers without changing remote settings.
- **VAL-GRCE-008**: Focused tests, actionlint, affected/staged/all-files gates,
  formatter review, diff checks, and independent reviews pass.

## Traceability

- **Program requirement**:
  [PRD-0007](../../01.requirements/0007-repository-delivery-and-platform-assurance.md)
- **Architecture**:
  [AD-0010](../../02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md)
- **Decision**:
  [ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- **Plan**:
  [GitHub Routing and CI Evidence Implementation Plan](plan.md)
- **Task**:
  [GitHub Routing and CI Evidence Task](plan.md)
- **Predecessor**:
  [Spec 047](../0047-current-surface-and-stash-reconciliation/spec.md)
- **Successor**:
  [Spec 049](../0049-platform-validation-and-security-evidence/spec.md)

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0007-FR-0003](../../01.requirements/0007-repository-delivery-and-platform-assurance.md#functional-requirements) | VAL-GRCE-001 | Closed schema and mutation fixtures prove a reference-only projection owner. |
| N/A — REQ-0007-FR-0003 shares the PRD-0007 source linked above. | VAL-GRCE-002 | Agent surface fixtures prove complete label and explicit owner coverage. |
| N/A — REQ-0007-FR-0003 shares the PRD-0007 source linked above. | VAL-GRCE-003 | Native-semantics comparison proves effective projection parity. |
| N/A — REQ-0007-FR-0004 shares the PRD-0007 source linked above. | VAL-GRCE-004 | Workflow topology and security validators prove independent CI evidence. |
| N/A — REQ-0007-NFR-0002 shares the PRD-0007 source linked above. | VAL-GRCE-005 | Markdown profiles and direct workflow comparison prove accurate hub prose. |
| N/A — REQ-0007-FR-0004 shares the PRD-0007 source linked above. | VAL-GRCE-006 | SHA-bound remote metadata separates historical and current results. |
| N/A — REQ-0007-FR-0009 shares the PRD-0007 source linked above. | VAL-GRCE-007 | Task evidence records limitation, owner, and retry trigger without mutation. |
| N/A — REQ-0007-FR-0010 shares the PRD-0007 source linked above. | VAL-GRCE-008 | Local QA and independent review records prove rollback-ready closure. |
