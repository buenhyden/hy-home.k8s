---
title: 'Current Surface and Stash Reconciliation Technical Specification'
type: sdlc/spec
status: draft
owner: platform
updated: 2026-08-02
---

# Current Surface and Stash Reconciliation Technical Specification (Spec)

## Overview

This specification establishes the first tranche of the PRD-007 repository
delivery and platform assurance program. It re-observes every approved target
against current `main`, assigns one canonical owner and disposition, activates
the ordered program lineage after written-plan approval, and reconciles saved
stash object `6370311e...` without applying an obsolete snapshot over current
contracts.

Spec 047 is an evidence and ownership foundation. It does not implement the
GitHub routing, platform validation, or IaC validation gaps assigned to Specs
048 through 050. It hands only current, classified, rollback-ready facts to
those tranches.

## Strategic Boundaries & Non-goals

- **Owns**: tracked target inventory; current audit delta; canonical owner and
  disposition matrix; duplicate/conflict proof; protected-surface boundary;
  program activation; stash hunk classification; generated-object refresh;
  and successor handoff.
- **Consumes**: the Current 2026-07-11 audit pack, PRD-007, ARD-0010,
  ADR-0021, current Git indexes, `validation-surfaces.json`, Stage 99 profiles,
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

1. PRD-007, ARD-0010, ADR-0021, and Specs 047-051 must exist as reviewed draft
   documents before Plan authoring begins.
2. After human review, Spec 047 alone may enroll PRD `007`, ARD `0010`, and
   ordered Specs `047` through `051` in the registry program lineage.
3. Exactly the first unfinished tranche may have a reciprocal Plan/Task pair.
   Later tranche execution records remain absent until their predecessor is
   done.
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

No path is edited merely to satisfy coverage. README frontmatter remains absent
where the selected profile requires a frontmatter-free implementation or
GitHub-native form.

### Stash reconciliation contract

- Identify the stash by object ID before each destructive stash operation; do
  not rely on a mutable numeric position after another stash appears.
- Compare base-to-index and index-to-worktree deltas without applying them.
- Classify every hunk as `already-present`, `port`, `regenerate-current`,
  `superseded`, or `preserve-history`.
- Treat the retired GitHub hub filename to `.github/README.md` cutover as
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
  PRD/ARD/ADR/Spec links, and program-lineage state.
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
- **VAL-CSASR-003**: Program lineage contains PRD-007, ARD-0010, ordered Specs
  047-051, one first-tranche execution component, and no later Plan/Task.
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
  [PRD-007](../../01.requirements/007-repository-delivery-and-platform-assurance.md)
- **Architecture**:
  [ARD-0010](../../02.architecture/requirements/0010-repository-delivery-evidence-architecture.md)
- **Decision**:
  [ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- **Plan**:
  [Current Surface and Stash Reconciliation Implementation Plan](../../04.execution/plans/2026-08-02-current-surface-and-stash-reconciliation.md)
- **Task**:
  [Current Surface and Stash Reconciliation Task](../../04.execution/tasks/2026-08-02-current-surface-and-stash-reconciliation.md)
- **Successor**:
  [Spec 048](../048-github-routing-and-ci-evidence/spec.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-RDPA-001](../../01.requirements/007-repository-delivery-and-platform-assurance.md#functional-requirements) | VAL-CSASR-001 | Tracked inventory and current disposition matrix prove complete scoped ownership. |
| N/A — REQ-RDPA-001 shares the PRD-007 source linked above. | VAL-CSASR-002 | Current evidence classification reconciles every dated audit finding. |
| N/A — REQ-RDPA-010 shares the PRD-007 source linked above. | VAL-CSASR-003 | Registry and cross-document validators prove ordered program activation. |
| N/A — REQ-RDPA-002 shares the PRD-007 source linked above. | VAL-CSASR-004 | Stash ledger proves one semantic disposition per hunk. |
| N/A — REQ-RDPA-002 shares the PRD-007 source linked above. | VAL-CSASR-005 | Generator comparison proves current object identities. |
| N/A — REQ-RDPA-009 shares the PRD-007 source linked above. | VAL-CSASR-006 | Status, scope, and review evidence prove protected boundaries. |
| N/A — REQ-RDPA-012 shares the PRD-007 source linked above. | VAL-CSASR-007 | Focused and aggregate QA prove contract-compliant authored output. |
| N/A — REQ-RDPA-010 shares the PRD-007 source linked above. | VAL-CSASR-008 | Independent review records prove requirements and quality/security approval. |
| N/A — REQ-RDPA-001 shares the PRD-007 source linked above. | VAL-CSASR-009 | Successor handoff matrix proves bounded downstream ownership. |
