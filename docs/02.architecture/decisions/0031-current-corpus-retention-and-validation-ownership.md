---
title: 'ADR-0031: Current Corpus Retention and Validation Ownership'
type: sdlc/adr
status: proposed
owner: platform
updated: 2026-08-31
artifact_id: "ADR-0031"
---

# ADR-0031: Current Corpus Retention and Validation Ownership

## Overview

This proposed decision reduces the current document and validation control
planes to one owner per responsibility. It retains only current, distinct
authority in the active corpus; moves validation routing out of human
governance; removes execution-instance rosters and mutable branch identity
from permanent contracts; and makes Git the default terminal-history owner.

Upon acceptance, this decision is the successor to ADR-0016, ADR-0017,
ADR-0020, ADR-0021, and ADR-0022. Their decision bodies remain in the Stage 02
decision log. The acceptance transaction changes each predecessor from
`accepted` to `superseded`, adds this ADR's `supersedes` relation, adds each
predecessor's reciprocal `superseded_by: ADR-0031`, and updates the Decisions
README state and explanation. This proposal does not change predecessor status
or reciprocal links before acceptance. Upon acceptance, it makes exactly two scoped
amendments to ADR-0030: validator tests and fixtures remain under top-level
`tests/` rather than `validation/tests/`, and module review follows
responsibility and risk rather than a mandatory above-800-line exception.
These are scoped normative amendments, not an ADR lifecycle supersession:
ADR-0030 remains accepted and authoritative in every other respect.

## Context

The current repository expresses overlapping lifecycle and validation rules
through Stage 00 contracts, the Stage 99 document registry, program and
standalone execution rosters, validators, fixtures, workflow jobs, approval
sentence matchers, corpus counts, and branch-relative SHA evidence. A change
to one current document can therefore require unrelated registry, fixture,
digest, and gate updates even when no behavioral contract changed.

This overlap also obscures authority. Human governance and an executable
validation-surface registry share Stage 00; the document registry contains
point-in-time work-package relations; and terminal bodies are copied into
Stage 98 even though Git already preserves them. Existing validators can pass
while these structural ownership conflicts remain, so a green aggregate is
not by itself evidence that the control plane is coherent.

[ADR-0030](./0030-authority-first-sdlc-and-agent-governance-convergence.md)
already establishes authority-first convergence, a minimal active topology,
consumer-first deletion, bounded validation, and Git-backed recovery. This
decision applies those principles to the current corpus and validation
routing. [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md)
owns the integrated governance convergence, while
[Spec 0066](../../03.specs/0066-validation-tooling-ownership/spec.md) owns the
delegated validation-tooling transition.

## Decision

### One current owner per responsibility

The terminal ownership map is:

| Responsibility | Terminal owner | Boundary |
| --- | --- | --- |
| Architecture and long-lived governance decisions | Accepted ADRs | Stage 00 explains the approved model but does not create a parallel decision contract. |
| Integrated convergence implementation and acceptance | Active Spec 0054 | Delegated packages report evidence to Spec 0054 and do not replace its acceptance boundary. |
| Document profiles, frontmatter, lifecycle domains, and document relations | `docs/99.templates/registry.json` | The registry describes document kinds and normalized lifecycle rules, not current execution instances. |
| Validation selection, routing, command arguments, and CI projection | `scripts/validation/registry.json` | The existing Stage 00 validation-surfaces contract and schema move atomically to this path and are reused rather than copied. |
| Agent role, permission, skill, and handoff topology | `.agents/registry.json` | Provider projections consume this registry and do not redefine shared authority. |
| Terminal execution and content history | Git | Stage 98 adds only a bounded lookup record when Git history alone cannot preserve a required immutable link. |

Stage 00 remains a human-readable governance stage. Executable contracts
under Stage 00 move to their machine-owner path or are retired after every
consumer has moved. The validation registry move includes its schema,
consumers, tests, and diagnostics in one transition; the old path is removed
in that same change and is not retained as a redirect or body copy.

### Current corpus retention

A current document remains tracked only when it has a distinct current owner,
an active consumer, or a decision-log obligation. Conflicting predecessors,
duplicate-purpose documents, legacy compatibility forms, and completed work
packages leave the current corpus after lifecycle normalization, consumer-zero
proof, and Git recovery proof. Accepted and superseded ADRs remain in Stage 02
because the decision log itself is their durable purpose.

Historical status does not exempt a document from current governance. A
historical body that is not a decision record and has no current consumer is
removed rather than kept as a current rule source. A current index reports
semantic ownership and lifecycle; exact document, script, fixture, negative
case, role, adapter, or entrypoint counts are observations, not policy.

### Package-local execution authority

The lifecycle-domain definitions are normalized as a top-level
`lifecycleDomains` registry section. `programLineage.programs`,
`referenceCurrentPacks`, and `standaloneExecutions` are removed from the
current document-contract control plane. Permanent registries do not enumerate
current Spec instances, exact approval sentences, active Task paths, or fixed
relation counts.

A directly human-approved Spec may proceed without a fabricated Requirement
or Architecture Description owner when the Spec records the approval boundary
and its Plan and Task records link reciprocally to that Spec. The approval is a
semantic fact, not an exact prose token. Delegated work records the parent and
delegate relationship in the affected Spec, Plan, and Task packages. Package
lifecycle rules and per-package execution constraints remain enforceable
without a repository-wide instance roster.

A delegated execution component is package-local: its Plan and Task link only
to each other and their own Spec for execution ownership. The child Spec and
its accepting parent Spec link reciprocally, and an accepted ADR authorizes the
delegation. The ownership gate admits that component only when those relations
are closed, lifecycle states agree, one parent acceptance package is
unambiguous, and no second standalone child row exists. Missing reciprocity,
an unaccepted decision, multiple candidate parents, cross-package Plan/Task
execution links, or duplicate roster authority fail closed.

During the bounded transition before instance rosters are removed, the one
existing Spec 0054 `standaloneExecutions` row may follow the current parent
Task. It never points at Spec 0066 and never authorizes child execution. The
parent handoff rotates that row to TSK-0054-0010, activation rotates it to
TSK-0054-0011, and terminal parent handoff rotates it to queued
TSK-0054-0013 before that Task activates. Each rotation is atomic with the
corresponding legal Task transition. WP-013 removes the compatibility row and
its consumers after the package-local rule is current.

Consistent with accepted ADR-0030, a frontmatter-free package `README.md` is a
navigation projection, not an authored lifecycle artifact. Every Stage 03 work
unit, including a draft package, owns its thin router. Router creation and
updates are governed by the Markdown profile plus link and owner checks; they
are not Migration, Tombstone, or lifecycle state-transition events. No Stage
98 record is created solely to admit navigation.

### Validation ownership and evidence

The validation registry owns only the executable routing graph: responsibility
domain, canonical command, selection criteria, arguments, CI consumer, and
transition alias while one is necessary. A Task and its reviewable diff own
point-in-time disposition evidence. Independent tests and fixtures own
behavioral examples for the rule they test; they do not restate the repository
inventory. Their physical owner is the top-level `tests/` and
`tests/fixtures/` surface, while their semantic grouping and case selection
follow the responsible production module and independent failure families. No
exact path subdivision or case count is itself a governance invariant.

Aggregate runners and compatibility wrappers contain no rule semantics.
Obsolete wrappers are deleted after consumer-zero proof and a unique canonical
diagnostic exists. Validation remains fail-closed for bounded input, strict
UTF-8, subprocess timeouts, index/worktree drift, missing current executable
references, and unresolved transition aliases. A missing executable cannot be
treated as current merely because an active Spec proposes it.

Required hosted check names remain stable until authorized evidence confirms
that external branch-protection consumers can migrate safely. Internal job
steps and local routing may simplify without claiming that external settings
have changed.

### SHA and terminal-history boundary

SHA identity is retained only for an external immutable dependency or sealed
recovery evidence. Third-party CI action pins and a reachable Git object used
to recover a deleted path are valid uses. A working branch, baseline branch,
current HEAD, ordinary document, validator, registry, template, line number,
or corpus snapshot must not be pinned as permanent current policy.

Git is the default full-body archive. Stage 98 contains no prior-body clone or
redirect chain. A Migration may record one bounded authority or path mapping;
a Tombstone may record one minimal stable-path replacement only when an actual
immutable historical link requires it. Routine move, merge, supersession, and
deletion rely on Git and current links without generating one archival record
per source document.

## Explicit Non-goals

- Changing the terminal stage topology, four-digit identity, consumer-first
  migration, or fail-closed recovery principles accepted by ADR-0030.
- Changing live infrastructure, hosted branch protection, remote refs,
  credentials, provider accounts, or deployment state.
- Rewriting Git history or editing sealed Stage 98 records in place.
- Treating every old path as an immutable historical link that requires a
  Tombstone.
- Defining a permanent validator, fixture, file-size, command, or document
  count.
- Amending ADR-0030 beyond the validator-test location and mandatory 800-line
  exception clauses identified by this decision.
- Activating Spec 0066 or changing accepted predecessor status as part of this
  proposed design checkpoint.

## Consequences

### Positive

- Each rule has one normative or executable owner, so changes no longer fan
  out across unrelated rosters, approval maps, fixtures, and digest ledgers.
- Spec 0054 can govern the integrated cleanup while Spec 0066 owns a bounded,
  reviewable tooling delegation.
- Stage 00 becomes easier for humans and agents to interpret because machine
  routing state is no longer mixed with policy prose.
- Current-document edits use semantic validation instead of mutable branch
  identity and exact-count rebaselines.
- Git recovery and minimal Stage 98 mappings eliminate tracked full-body
  archive duplication.

### Costs and transition constraints

- The validation registry move must update all consumers atomically; a copied
  successor and compatibility redirect would create two current owners.
- Removing registry instance rosters requires package-local reciprocal links
  and lifecycle validation to be active first.
- The transition must keep the existing Spec 0054 compatibility row aligned
  with a non-terminal parent Task until WP-013 removes that row; no child row
  is introduced.
- Lifecycle validation must stop treating frontmatter-free navigation
  projections as proof-backed Migration events while continuing to fail closed
  for registry-classified authored lifecycle documents.
- Current green validators need focused ownership tests because their existing
  pass result does not detect every duplicated control plane.
- Remote durability for a recovery object cannot be inferred from a local
  branch. Deletion dependent on remote ancestry remains deferred until an
  authorized remote check proves it.

## Alternatives

### Keep execution rosters in the Stage 99 document registry

Rejected because document profiles and current work-package instances change
at different rates. Combining them turns each Spec activation, approval
wording change, and terminal cleanup into a registry schema concern.

### Copy the Stage 00 validation contract into `scripts/validation/`

Rejected because a copied registry creates two current routing authorities.
The source contract, schema, consumers, and validation move as one unit.

### Keep validation routing in Stage 00

Rejected because Stage 00 is the human governance boundary. Executable
selection and CI routing belong beside the scripts that implement them.

### Preserve every terminal body or old path in Stage 98

Rejected because Git already provides the full body and most old paths have no
immutable consumer. A record without a required lookup purpose increases
current corpus and redirect complexity without improving recovery.

### Pin the working branch and current corpus for reproducibility

Rejected because mutable branch and corpus identities make normal edits fail
for historical rather than semantic reasons. Reproducibility is served by
sealed recovery objects and external dependency pins at the boundary where
byte identity is meaningful.

## Traceability

Upon acceptance, this ADR will supersede the current lineage and routing
control-plane decisions in
[ADR-0016](./0016-program-to-tranche-document-lineage.md),
[ADR-0017](./0017-program-follow-up-lineage-semantics.md),
[ADR-0020](./0020-document-lifecycle-program-closure-evidence.md),
[ADR-0021](./0021-canonical-surface-routing-and-evidence-depth.md), and
[ADR-0022](./0022-direct-approval-standalone-execution-lineage.md). Their
historical decision bodies remain in Stage 02. Acceptance must atomically add
the `supersedes` relation to this ADR, change each predecessor from `accepted`
to `superseded`, add reciprocal `superseded_by: ADR-0031` evidence to each
predecessor, and update the Decisions README state and explanation; this
proposed checkpoint deliberately does none of those changes.

The same acceptance unit must add a reciprocal scoped-amendment note to
ADR-0030's Traceability and update the Decisions README. That note identifies
only the `validation/tests/` co-location and mandatory above-800-line exception
clauses as governed by the later ADR-0031 decision. ADR-0030 keeps status
`accepted`; its ADR lifecycle relation does not become `superseded_by`, and no
other ADR-0030 clause is amended. Spec 0066 cannot activate before this
reciprocal evidence and the ADR-0031 `proposed → accepted` transition are
committed and validated together.

That same acceptance index rewrites every current Stage 02/03 navigation and
Spec-package label that calls ADR-0031 `Proposed` or `proposed` to an
accepted/current description. Historical bodies are not rewritten merely for
terminology. ADR-0030 stays `accepted`; only the five named predecessors move
to `superseded`.

[ADR-0030](./0030-authority-first-sdlc-and-agent-governance-convergence.md)
remains the accepted topology and convergence authority. Upon acceptance,
ADR-0031 governs only ADR-0030's physical `validation/tests/` co-location
requirement and mandatory reviewed exception above 800 lines as later scoped
amendments. Those clauses become top-level independent tests and
responsibility/risk-based module review. It preserves
ADR-0030's other single-owner, minimal-current-corpus, consumer-first deletion,
immutable external dependency, and Git-recovery principles while defining the
narrower validation-routing and execution-instance boundaries needed by Specs
0054 and 0066.

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| N/A — predecessor reciprocal links are deferred until this proposal is accepted | Intended successor to ADR-0016, ADR-0017, ADR-0020, ADR-0021, and ADR-0022; scoped amendment, not lifecycle supersession, of the two identified ADR-0030 validation-layout clauses | [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| N/A — delegated validation transition starts only after design acceptance | Spec 0066 implements the validation-owner move under Spec 0054 | [Spec 0066](../../03.specs/0066-validation-tooling-ownership/spec.md) |
