---
title: "Six-Disposition Archive Stage"
version: "1.2.0"
type: "sdlc/architecture-decision"
status: "superseded"
owner: "platform"
updated: "2026-09-15"
layer: "architecture"
artifact_id: "ADR-0038"
supersedes: "ADR-0032"
superseded_by: "ADR-0039"
---

# ADR-0038: Six-Disposition Archive Stage

## Overview

This decision gives Stage 98 six dispositions of two kinds. Four
retention classes hold a whole body that was once current, and two route
dispositions hold no body. Each family's citability is derived from what its
record names rather than stipulated beside it. This decision supersedes
ADR-0032. It applies forward: content already frozen in Stage 98
keeps its generation.

**Superseded (2026-09-15).** [ADR-0039](./0039-unit-archive-retention-and-citation-table.md)
supersedes this decision as a whole. It retains a whole unit as its
source Git object, decides a class from the unit anchor's state, names one Git
object per unit, decides every citation from one ordered registry table, and
tracks moves between active stages by identity. Its routes stay the only ones the validators admit
until the machine cutover in Spec 0082.

## Context

ADR-0032 gave Stage 98
four directories. `completed/` retains a document itself; `superseded/` and
`tombstones/` hold sealed records whose ArchiveEnvelope carries `source_commit`,
`source_blob`, and `content_sha256`; `migrations/` holds ledgers whose rows pin
a commit, a blob, and a digest again. One source object therefore carries up to
three recovery identities that must agree with Git and with each other. Git
already recovers the object, so the digest and the per-row path ledger are a
second recovery ledger rather than evidence Git lacks.

The record form also replaces a document's own identity metadata. ADR-0032
rejected that form for `completed/` for exactly this reason, and the reason
does not depend on why the document ended.

The taxonomy has gaps. A rule or scope withdrawn with no successor has no home
that says so, and a closed Incident with its published Postmortem has no
retention route at all. Citability is written separately from the taxonomy: the
documentation hub admits lineage citation of any archive document, the
authoring policy admits links only to `completed/`, and the link validator
hardcodes that one directory.

Finally, the decision-log exception keeps superseded architecture decisions in
Stage 02. On 2026-09-15 fifteen superseded decisions sat beside the current
ones, which is the condition ADR-0032 named for the other stages: an active
stage describing finished work as if it were current.

## Decision

### Two kinds of disposition

A **retention class** holds a whole body that was once current, under the
profile that governed it then. A governed document that is no longer current
leaves Stages 01, 02, 03, 05, 90, and 99 and is kept in the class that matches
what happened to it.

| Class         | Holds                                             | Must name                                              | Citable from an active stage |
| ------------- | ------------------------------------------------- | ------------------------------------------------------ | ---------------------------- |
| `completed/`  | Work that finished and landed                     | What it promoted                                       | yes                          |
| `superseded/` | Content a newer current authority replaced        | The document that replaced it                          | no; cite its successor       |
| `retired/`    | A rule or scope withdrawn with no successor       | Why it was withdrawn                                   | no                           |
| `resolved/`   | A closed Incident bundle and published Postmortem | Closure evidence and the current corrective-work owner | yes, as historical evidence  |

A **route disposition** holds no body. It names a route for a consumer outside
this repository, so a current document cites the current route and never the
record that names it.

| Family        | Holds   | Must name                                                   | Citable from an active stage |
| ------------- | ------- | ----------------------------------------------------------- | ---------------------------- |
| `tombstones/` | Nothing | The retired route, its successor or absence, and the reason | no                           |
| `migrations/` | Nothing | The moved scope and its current owner, as `MIG-####`        | no                           |

Each disposition owns a directory that is created by the change that first uses
it, so a disposition with no record yet has no directory.

### Retention follows the profile

A retained body keeps its own profile, identity, and terminal state, and sits
at `docs/98.archive/<class>/<its own stage path>`. Frozen bodies remain
immutable, while a Git-history-only disposition retains recoverable provenance
without a compatibility copy. Every disposition requires its own authorization.

ADR-0032's package unit and consumer-zero rules carry over unchanged: a Stage 03
package is retained whole, and a document still reached through current
traceability has not finished being current.

### The decision-log exception is withdrawn

A superseded architecture decision follows the same rule as every other family
and leaves Stage 02 for `superseded/`. Its successor carries the lineage
through `supersedes`, and the decision index names the predecessor by
identifier.

### Citability is derived from naming

A retention class may be cited exactly when its own body still leads a reader to
current authority: `completed` through its promotion declaration and `resolved`
through its corrective-work owner. A `superseded` body names its replacement,
so the citation belongs on that successor, because citing a replaced rule is how
it returns. `retired` carries no pointer, so citing it would strand a reader on
a withdrawn rule. A route disposition is never cited; the current route is.

### One recovery reference

No Stage 98 record, in any family, carries a second recovery ledger: no
redirect, path ledger, self-designed body digest, branch SHA, or recovery
commit. The Stage 98 catalog's Retention Envelope names the source Git object
once, as `<commit>:<original path>`, and normal Git history recovers it with
`git show`. The named commit must stay reachable from the default branch, which
the Git policy's prohibition on history rewriting already protects.

### Frozen content keeps its generation

Content sealed or retained before this decision is accepted keeps its bytes,
envelope, digests, pinned ledger rows, and historical links. Validators
classify it by generation and never rewrite it to the new form. The six
dispositions and the derived citation rule apply to dispositions made after
acceptance and to documents authored or revised after it; citations that
predate acceptance are an enumerated consumer set, not a violation to erase.

## Explicit Non-goals

- It does not rewrite, re-seal, or re-home any frozen Stage 98 record, ledger,
  or retained package.
- It does not itself change registry routes, archive forms, or validators.
  [Spec 0079](../../03.specs/0079-six-disposition-archive-stage/spec.md) owns
  that cutover as one atomic change.
- It does not add lifecycle states or edges. Which states are terminal stays
  with the Stage 99 registry.
- It does not move the superseded decisions already in Stage 02; each
  disposition needs its own authorization.
- It does not retain untracked or generated output, secrets, or anything
  outside the governed document stages.

## Consequences

The active stages, including the decision log, describe only current intent, and
a reader finds replaced, withdrawn, and closed material by the disposition that
names what happened to it.

Recovery has one identity per source object. A reader recovers original bytes
with one `git show` against the catalog entry instead of reconciling a blob, a
digest, and a ledger row.

Stage 98 holds two generations until no frozen record remains relevant. The
validators must classify by generation, which the cutover Spec owns, and the
registry must keep frozen records and retained bodies from matching the same
profile.

Recovery depends on the named commit staying reachable. A rewrite of the default
branch would break it; that is accepted because the Git policy already forbids
the rewrite.

Spec 0079 moved the registry routes, archive forms, and validators to this
model in one change. The registry routes frozen records and ledgers by exact
path, so the frozen generation cannot grow, and the lifecycle gate admits a
retained body through its catalog row and a move through a body-less scope
migration.

## Alternatives

**Keep ADR-0032's record form for `superseded/`.** Rejected: it replaces the
document's identity metadata and multiplies recovery identities for one object.

**Name the Git blob object ID in the envelope.** Rejected: a content address
drops the original path and tree context, so finding the commit that held it
needs a history search, and an unreachable blob gives no route back.

**Stipulate citability per family.** Rejected: a rule written beside the naming
drifts from it, which is how the hub, the authoring policy, and the link
validator came to disagree.

**Rewrite frozen content to the new form.** Rejected: frozen bytes are evidence,
and rewriting them is the silent provenance repair the archive exists to
refuse.

**Keep the decision-log exception.** Rejected: it leaves one active stage
describing finished work as current and makes the retention rule depend on the
family.

## Traceability

### Lifecycle Traceability

| Decision lineage                                                | Replacement relation                                                  | Affected Spec                                                          |
| --------------------------------------------------------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| ADR-0032 | Supersedes ADR-0032; its records and ledgers stay a frozen generation | [Spec 0079](../../03.specs/0079-six-disposition-archive-stage/spec.md) |
| [ADR-0039](./0039-unit-archive-retention-and-citation-table.md) | Supersedes this decision; its routes stay the only admitted ones until the cutover | [Spec 0082](../../03.specs/0082-unit-archive-retention-contract/spec.md) |
