---
title: "Current Surface and Stash Reconciliation Technical Specification"
version: "1.0.0"
type: "sdlc/spec"
status: "active"
owner: "platform"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0047"
---

# Current Surface and Stash Reconciliation Technical Specification (Spec)

## Overview

This specification establishes the first tranche of the PRD-0007 repository
delivery and platform assurance program. It re-observes every approved target
against current `main`, assigns one canonical owner and disposition, activates
the ordered program lineage after written-plan approval, and reconciles saved
stash object `6370311e...` without applying an obsolete snapshot over current
contracts.

Spec 0047 resumes after Spec 0052's semantic closure under accepted ADR-0031
and ADR-0033. Its package-local activation Task is complete; implementation
Tasks CSASR-001 through CSASR-005 remain queued. Specs 0048 through 0051 remain
draft and resume sequentially only after their predecessor closes. The saved
stash object remains reachable and still needs tracked-hunk reconciliation;
activation does not claim that work complete.

Spec 047 is an evidence and ownership foundation. It does not implement the
GitHub routing, platform validation, or IaC validation gaps assigned to Specs
048 through 050. It hands only current, classified, rollback-ready facts to
those tranches.

## Strategic Boundaries & Non-goals

- **Owns**: tracked target inventory; current audit delta; canonical owner and
  disposition matrix; duplicate/conflict proof; protected-surface boundary;
  program activation; stash hunk classification; generated-object refresh;
  and successor handoff.
- **Consumes**: the Current 2026-07-11 audit pack, PRD-0007, AD-0010,
  accepted ADR-0031, current Git indexes, `scripts/validation/registry.json`, Stage 99 profiles,
  native control files, validators, tests, and read-only GitHub metadata.
- **Does not own**: labeler/CODEOWNERS projection implementation, workflow
  routing, Kustomize/schema/Traefik implementation, Terraform/Bicep validation,
  remote settings, or live infrastructure.
- **Non-goals**: touching every file for uniformity; reopening completed Specs;
  rewriting historical audits; reading ignored scratch or secrets; applying
  the stash wholesale; copying stale object IDs; or dropping the stash before
  verified local integration.

## Contracts

### Program activation contract

1. The approved package-local Spec, Plan, and Task records own execution under
   accepted ADR-0031 and the v9 document contract of ADR-0033. ADR-0021 is
   superseded historical context; no public program-instance roster is added.
2. After Spec 0052 closes, Spec 0047 and its Plan follow `draft → active`,
   and the existing activation Task follows `in-progress → done` in the same
   validated change as the Stage 03 index.
3. Existing successor Plans remain draft and their Tasks queued. Spec 0048
   may follow its package-local `draft → active` route only after Spec 0047
   and its Plan and Tasks close with their required evidence. The same rule
   applies sequentially through Spec 0051.
4. Repository-static completion never promotes hosted, provider-runtime,
   credential-bearing, or live evidence.

### Current-surface disposition contract

Every tracked item under `.github`, `examples`, `gitops`, `infrastructure`,
`policy`, `scripts`, `secrets`, `tests`, and `traefik` receives exactly one
disposition:

- `change`: current evidence proves a defect, conflict, duplicate, stale claim,
  unsafe boundary, or missing validation owner;
- `no-change`: the selected current contract and observed file agree;
- `defer`: the gap requires unavailable authority or evidence and includes an
  owner plus retry trigger.

No path is edited merely to satisfy coverage. README metadata follows its
selected v9 profile under ADR-0033.

### Stash reconciliation contract

- Identify the stash by object ID before each destructive stash operation; do
  not rely on a mutable numeric position after another stash appears.
- Compare base-to-index and index-to-worktree deltas without applying them.
- Classify every hunk as `already-present`, `port`, `regenerate-current`,
  `superseded`, or `preserve-history`.
- Treat the retired GitHub hub filename to `.github/repository-surface.md` cutover as
  current only where active readers still need it. Historical plans, tasks,
  audits, and
  completed Specs retain provenance wording unless it is an active broken link.
- Regenerate `active-corpus-residue-closure.json` from the current generator and
  current HEAD; never copy the stash's old object identities.
- Store temporary comparison data only in ignored `_workspace` scratch and
  delete it before closure. Store the durable disposition summary in the Task.
- Drop the matching stash only after all Specs are reviewed, the branch is
  locally integrated, and main postflight passes.

## Core Design

The tranche executes in four passes:

1. **Inventory**: enumerate tracked paths, document profiles, validation
   surfaces, native controls, scripts, fixtures, workflow jobs, Kustomize
   roots, IaC roots, and current owner links.
2. **Re-observation**: compare each dated audit finding with current file and
   validator evidence. Mark resolved history, residual gap, false positive, or
   external-lane limitation without editing the dated finding.
3. **Ownership and stash reconciliation**: build the target disposition matrix
   and stash hunk ledger, port only current intent, and regenerate derived
   artifacts from their canonical producer.
4. **Foundation closure**: validate indexes, profiles, cross-links, generated
   output, protected boundaries, and exact changed scope; record review and
   hand Spec 048 a stable baseline.

The matrix is a Task-owned execution artifact, not a third machine routing
contract. Existing path and technology owners remain canonical.

## Data Modeling & Storage Strategy

The durable Task matrix contains:

| Field | Meaning |
| --- | --- |
| `target` | Repository-relative tracked path or bounded path class |
| `surfaceId` | Existing validation-surface identifier or explicit unowned finding |
| `canonicalOwner` | Current contract, native control, validator, or stage document |
| `auditFinding` | Dated finding identifier or `none` |
| `observation` | Current repo or read-only remote evidence with SHA and date |
| `disposition` | `change`, `no-change`, or `defer` |
| `nextSpec` | Spec 048, 049, 050, 051, or none |
| `limitation` | Required for DEFER; otherwise null |
| `owner` | Responsible follow-up owner |
| `retryTrigger` | Observable event that reopens a DEFER |

The stash ledger additionally records stash object ID, parent relation, path,
hunk identity, category, destination owner, adopted commit, and review result.
It records no credential, ignored content, shell history, raw provider log, or
secret-bearing payload.

## Interfaces & Data Structures

- **Git interface**: tracked file inventory, status, object metadata, stash
  parents, path diffs, and generated-output comparison. No checkout, reset, or
  stash apply is needed.
- **Audit interface**: immutable observation rows plus a current dated
  disposition in the Task; past findings are not rewritten as current fact.
- **Document interface**: selected profiles, Stage indexes, reciprocal
  requirement/architecture links, and package-local Spec/Plan/Task state.
- **Successor interface**: a closed list of Spec 048-051 owned changes and
  evidence-backed no-change rows.
- **Scratch interface**: ignored, non-secret `_workspace` ledger with no
  durable authority; Task evidence is the promotion target.

## Edge Cases & Error Handling

- If the stash numeric position changes, resolve the recorded object ID and
  stop if it is absent or ambiguous.
- If a hunk combines valid rename intent with stale generated data, split its
  disposition rather than adopting the whole file.
- If a current path has no selected profile or more than one validation owner,
  fail the tranche and route the contract gap before editing consumers.
- If an audit statement is historically correct but no longer current, retain
  it and record the current disposition outside the observation row.
- If a generated file differs but its producer cannot recreate it, fail rather
  than manually editing generated identities.
- If a native README already passes its profile, use `no-change`; do not add
  governance sections to make the audit matrix appear complete.
- If the worktree becomes dirty from unrelated changes, stop and preserve the
  user-owned change instead of folding it into this tranche.

## Failure Modes & Fallback / Human Escalation

- **Unknown current owner**: stop and escalate the ownership decision; do not
  create a parallel owner in a README or audit.
- **Stash mismatch**: preserve all stashes and escalate with object evidence;
  do not drop or apply a substitute.
- **Protected-surface conflict**: update the governing Spec or ADR before
  implementation if evidence changes the approved boundary.
- **Remote/live dependency**: record `DEFER`, owner, limitation, and retry
  trigger; do not weaken repository gates or request credentials implicitly.
- **Formatter spillover**: inspect every changed path, separate or revert
  unrelated formatter output safely, and rerun the affected/staged/all-files
  sequence before commit.

## Verification Commands

```bash
git status --short --branch
git diff --check
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
```

Stash inspection uses read-only Git object and diff commands recorded in the
Task. The implementation must not invoke `git stash apply`, `git stash pop`,
or `git stash drop` in this tranche.

## Success Criteria & Verification Plan

- **VAL-CSASR-001**: The exact approved target population has one current
  disposition and owner, with no uncovered or duplicated current-purpose row.
- **VAL-CSASR-002**: Every Current audit finding is classified as residual,
  resolved, false positive, or external DEFER against current evidence.
- **VAL-CSASR-003**: Package-local reciprocal Spec/Plan/Task evidence proves
  Spec 0047 activation, sequential predecessor closure for Specs 0048–0051,
  and no premature successor execution or public program-instance roster.
- **VAL-CSASR-004**: Every stash hunk has one durable category and adopted or
  non-adopted rationale; no wholesale apply occurs.
- **VAL-CSASR-005**: Generated residue identities, if affected, are produced by
  the current generator and current HEAD rather than copied from the stash.
- **VAL-CSASR-006**: Ignored/private state, secrets, credentials, remote
  settings, and live systems remain untouched.
- **VAL-CSASR-007**: Strict document, repository aggregate, all-files,
  formatter-review, and diff gates pass for the exact logical commit scope.
- **VAL-CSASR-008**: Independent requirements and quality/security reviewers
  approve the tranche with a rollback unit and no open finding.
- **VAL-CSASR-009**: Spec 048 receives a committed routing/CI gap set, while
  Specs 049-051 receive their exact bounded successor rows.

## Traceability

- **Program requirement**:
  [PRD-0007](../../01.requirements/0007-repository-delivery-and-platform-assurance.md)
- **Architecture**:
  [AD-0010](../../02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md)
- **Current execution decisions**:
  [ADR-0031](../../02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md)
  and [ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md)
- **Historical decision**:
  [superseded ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- **Plan**:
  [Current Surface and Stash Reconciliation Implementation Plan](plan.md)
- **Task**:
  [Current Surface and Stash Reconciliation Task](plan.md)
- **Successor**:
  [Spec 048](../0048-github-routing-and-ci-evidence/spec.md)

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0007-FR-0001](../../01.requirements/0007-repository-delivery-and-platform-assurance.md#functional-requirements) | VAL-CSASR-001 | Tracked inventory and current disposition matrix prove complete scoped ownership. |
| N/A — REQ-0007-FR-0001 shares the PRD-0007 source linked above. | VAL-CSASR-002 | Current evidence classification reconciles every dated audit finding. |
| N/A — REQ-0007-FR-0010 shares the PRD-0007 source linked above. | VAL-CSASR-003 | Lifecycle and cross-document validators prove package-local activation and sequential successor disposition. |
| N/A — REQ-0007-FR-0002 shares the PRD-0007 source linked above. | VAL-CSASR-004 | Stash ledger proves one semantic disposition per hunk. |
| N/A — REQ-0007-FR-0002 shares the PRD-0007 source linked above. | VAL-CSASR-005 | Generator comparison proves current object identities. |
| N/A — REQ-0007-FR-0009 shares the PRD-0007 source linked above. | VAL-CSASR-006 | Status, scope, and review evidence prove protected boundaries. |
| N/A — REQ-0007-NFR-0002 shares the PRD-0007 source linked above. | VAL-CSASR-007 | Focused and aggregate QA prove contract-compliant authored output. |
| N/A — REQ-0007-FR-0010 shares the PRD-0007 source linked above. | VAL-CSASR-008 | Independent review records prove requirements and quality/security approval. |
| N/A — REQ-0007-FR-0001 shares the PRD-0007 source linked above. | VAL-CSASR-009 | Successor handoff matrix proves bounded downstream ownership. |
