---
title: 'Document Schema and Lifecycle Contract Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-07-17
---

# Document Schema and Lifecycle Contract Technical Specification (Spec)

## Overview

This Spec advances the registry to a closed, profile-specific schema for
frontmatter values, ordering, lifecycle states, admission, transitions,
transition evidence, template parity, and full-document validation. It
preserves the five-key baseline for ordinary Markdown and adds no
archive-specific metadata.

DSLC-001 through DSLC-005 implemented the registry, metadata, lifecycle,
evidence, role/source, template, and native-surface contracts in independently
reviewed logical packages. DSLC-006 stages their terminal Spec/Plan/Task and
program-relation closure as one exact eight-file change. Staged lifecycle and
repository QA have completed, and remediated independent requirements and
quality reviews returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`;
the closure commit and post-commit verification remain open until their actual
results exist. The
independently approved `b3fd537` rollover correction keeps the registry and
lifecycle self-tests valid as the dependency-ready tranche moves from Spec 035
to Spec 036.

## Strategic Boundaries & Non-goals

- **In scope**: Stage 99 registry/schema/support/forms, Stage 00 routing
  summaries, profile validators, transition comparison, fixtures, and current
  draft/active authored consumers.
- **Non-goals**: Adding universal identifiers, relationship arrays, reviewers,
  or schema-version frontmatter; rewriting immutable evidence; converting the
  archive corpus; changing native GitHub or API contracts into Markdown;
  bulk-normalizing operations, helper, Plan, or Task bodies.

## Contracts

- Ordinary authored Markdown uses title, type, status, owner, and updated in
  repository order.
- Allowed types, states, values, sections, and conditional evidence are owned
  by the selected registry profile.
- Unknown keys and additional schema properties fail.
- Status transitions are family-specific and compared against the base change.
- Existing Tombstones are a baseline-only read-compatibility profile. New
  Tombstones are rejected; Spec 036 owns the full-body content/archive route,
  archive envelope, corpus conversion, and compatibility-profile removal.
- Forms provide copyable shape; support documents explain rationale; neither
  duplicates the complete registry inventory.

## Core Design

The state model distinguishes product, architecture, decision, specification,
execution, operations, reference, template, and archive roles. Forward
transitions require the profile's evidence owner. Reverse transitions create a
successor document rather than reopening terminal evidence. Archive has only
the archived state.

The Current document-type format and evidence matrix is refreshed before a
role changes. Guide, Policy, Runbook, Incident, Postmortem, and helper Tests
remain distinct: reader guidance does not own controls, policy does not copy
commands, runbooks own protected repeatable procedures, incidents own live
facts, postmortems own learning and actions, and helper Tests describe Spec
verification rather than replacing execution Tasks or test code.

Validation uses base-to-proposed comparison for changed status. A transition
must be allowed and must satisfy the registry-owned predicate for that exact
edge. Each predicate names allowed evidence profiles and states, the
Traceability link location, whether evidence must change in the same diff, and
the required evidence table contract. The validator returns a stable rule ID,
path, profile, expected transition, observed transition, base mode, and
evidence gap.

## Data Modeling & Storage Strategy

Registry objects remain closed JSON Schema objects. Status graphs, conditional
fields, body-contract status scope, role decisions, transition evidence, and
validator escalation are declarative data. Exhaustive inventory checks derive
from the registry; independent mutation fixtures do not copy the production
inventory. Spec 035 adds the schema capability needed by a future archive
profile but does not introduce that route or its archive-specific values.

Compatibility is explicit and temporary. The old Tombstone profile may remain
readable until Spec 036 migrates every record, but new authored Tombstones are
rejected.

## Interfaces & Data Structures

- Registry loader: one parse per validator process with schema version check.
- Profile selector: exact-one route or explicit native exception.
- Frontmatter validator: key order, type, enum, pattern, required, conditional,
  and placeholder checks.
- Transition validator: base status, proposed status, allowed edge, evidence
  profile/state, Traceability target, same-diff requirement, evidence body
  contract, and immutable-body guard.
- Form validator: source-profile parity plus template-only prompt allowance.

GitHub issue forms, workflow YAML, CODEOWNERS, PR templates, OpenAPI, GraphQL,
and protobuf keep native syntax ownership and do not acquire SDLC frontmatter.
This tranche invokes only native validators already available in the
repository; missing API-language toolchains remain an explicit Spec 039 DEFER.
README documents remain frontmatter-free and match one route-specific README
profile; README bodies route readers and do not absorb contract or governance
sections.

Creation and movement are profile-owned admission decisions. Authored profiles
default to draft-only creation; the reciprocal execution pair may be created
draft or active. Delete, rename, and same-path profile change are denied unless
a later Spec adds the exact movement predicate and destination route in the
same change. Existing Tombstone paths are a pinned readable baseline, not a
creation or movement destination.

Base selection is deterministic:

- staged mode compares HEAD with the Git index;
- CI mode compares the configured pull-request merge base with the proposed
  head;
- explicit ref mode compares from-ref with to-ref;
- snapshot/all-files mode validates current states but reports transition
  history as not evaluated rather than PASS.

Every declared allowed edge has positive evidence and missing-evidence, wrong-profile,
wrong-state, wrong-section, unchanged-evidence, and ambiguous-base fixtures.
No current authored profile declares an edge into or out of `archived` in this
tranche. Spec 036 must add its archive edge and same-diff source-removal,
archive-record, and archive-index predicate atomically with its new route.

## Edge Cases & Error Handling

- A file with valid global status but invalid family status fails.
- A changed status with no accessible base is reported as a comparison DEFER,
  not silently passed.
- Generic conditional-value fixtures prove the registry capability without
  introducing archive reason or replacement keys; Spec 036 owns those exact
  archive values and their dependencies.
- Template placeholders are valid only in template profiles.
- Historical payload text is excluded from active contract-residue scans.

## Failure Modes & Fallback / Human Escalation

- If a profile cannot express a rule without executable code, add a named
  validator capability rather than arbitrary registry expressions.
- If transition evidence conflicts with immutable history, create a successor
  record and escalate the relation decision.
- If compatibility weakens production enforcement outside migration paths,
  stop and combine the affected schema and migration changes atomically.

## Verification Commands

- Run registry schema self-tests and mutation probes.
- Run strict Markdown profile and transition validation.
- Run template-to-source parity validation.
- Run link/owner and historical-body guards.
- Run repository quality and all-files pre-commit.

## Success Criteria & Verification Plan

- **VAL-DSLC-001**: Every governed document matches one closed profile.
- **VAL-DSLC-002**: Unsupported key, order, enum, pattern, conditional value,
  and placeholder fixtures fail.
- **VAL-DSLC-003**: Family-invalid status and transition fixtures fail.
- **VAL-DSLC-004**: Unexplained reverse transitions and every archive
  reactivation fail.
- **VAL-DSLC-005**: Canonical templates match their authored source profiles
  without copying governance inventories.
- **VAL-DSLC-006**: Native contract surfaces remain frontmatter-free.
- **VAL-DSLC-007**: Every SDLC/common family and README profile has one
  reviewed role/source decision, and operations/helper-role overlap fixtures
  fail.
- **VAL-DSLC-008**: Every lifecycle edge has one closed evidence predicate and
  deterministic base-mode fixtures; missing or mismatched evidence fails.

### Closure Evidence

The exact eight-file staged change passes lifecycle validation. Registry 121,
lifecycle 651, Markdown-profile, cross-document, YAML, GitHub Actions security,
actionlint, zizmor, and the repository-quality aggregate pass. All-files
pre-commit passes every hook except the isolated filesystem's reproducible
`os.mkfifo` `Errno 95`, which remains Spec 039 portability scope. The first
independent closure requirements review found stale ledger rollback boundaries;
after all three rows were corrected to `b3fd537` and
`3aa25dc^..b3fd537`, re-review returned `REQUIREMENTS COMPLIANT`. The closure
quality review then required current QA evidence, precise future-ready fixture
wording, and the complete 036–040 successor set; after remediation, re-review
returned `QUALITY APPROVED`. The closure commit and its post-commit
strict/snapshot/clean-tree checks are intentionally not pre-claimed.

## Traceability

- **Predecessor**: [Spec 034](../034-authority-and-lineage-foundation/spec.md)
- **Successors**: [Spec 036](../036-archive-record-and-workspace-boundary/spec.md), [Spec 037](../037-active-corpus-and-execution-retention/spec.md), [Spec 038](../038-reference-information-architecture/spec.md), [Spec 039](../039-github-ci-qa-evidence/spec.md), and [Spec 040](../040-contract-cutover-and-program-closure/spec.md)
- **PRD**: [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **ARD**: [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- **Completed execution history**: [Archive Index](../../98.archive/README.md#document-index)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-WDLEC-001](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-DSLC-001 | Strict registry selection reports zero uncovered or ambiguous paths. |
| N/A — VAL-DSLC-002 shares the PRD-006 source linked in VAL-DSLC-001 | VAL-DSLC-002 | Frontmatter mutation fixtures cover closed metadata contracts. |
| N/A — VAL-DSLC-003 shares the PRD-006 source linked in VAL-DSLC-001 | VAL-DSLC-003 | Base-to-proposed lifecycle fixtures cover each family edge. |
| N/A — VAL-DSLC-004 shares the PRD-006 source linked in VAL-DSLC-001 | VAL-DSLC-004 | Negative transition fixtures reject reopen and reactivation. |
| N/A — VAL-DSLC-005 shares the PRD-006 source linked in VAL-DSLC-001 | VAL-DSLC-005 | Registry-derived parity checks cover Markdown forms. |
| N/A — VAL-DSLC-006 shares the PRD-006 source linked in VAL-DSLC-001 | VAL-DSLC-006 | Route fixtures reject SDLC frontmatter on native surfaces; available native validators remain authoritative, while CI toolchain expansion stays with Spec 039. |
| N/A — VAL-DSLC-007 shares the PRD-006 source linked in VAL-DSLC-001 | VAL-DSLC-007 | Type/source matrix and role-overlap fixtures verify operations, helper Tests, and README boundaries. |
| N/A — VAL-DSLC-008 shares the PRD-006 source linked in VAL-DSLC-001 | VAL-DSLC-008 | Edge-to-evidence and base-selection fixtures prove deterministic transition enforcement. |
