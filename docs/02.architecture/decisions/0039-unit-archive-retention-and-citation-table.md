---
title: "Unit Archive Retention and Citation Table"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-16"
layer: "architecture"
artifact_id: "ADR-0039"
supersedes: "ADR-0038"
---

# ADR-0039: Unit Archive Retention and Citation Table

## Overview

This decision revises the Stage 98 contract that ADR-0038 accepted. It keeps
ADR-0038's two kinds, six dispositions, single Retention Envelope, withdrawn
decision-log exception, and frozen generations. It changes what a disposition
retains and proves and how a citation into Stage 98 is decided. A disposition
retains a whole unit byte for byte, the unit's state decides its class, one
catalog row names the unit's Git object, one ordered registry table decides
every citation, and a move between active stages is tracked by identity rather
than by a migration record.

This decision supersedes ADR-0038 as a whole. Until the machine cutover in
Spec 0082, the validators admit only ADR-0038's routes.

## Context

A read-only survey at commit `8a76bd3b` compared ADR-0038 with the registry,
validators, and tests that implement it. The
[proposal Task](../../03.specs/0082-unit-archive-retention-contract/tasks/tsk-0001-propose-the-unit-retention-contract.md)
records each finding with its evidence.

- A retained body is compared with its source after relative links are
  rebased. The comparison rewrites link text to resolved paths, including
  link-like text inside code, so it proves equivalence after an admitted
  transformation rather than identity with the object the envelope names.
- ADR-0038 retains a Stage 03 package whole, but no check compares a package's
  members with the comparison base. Only a resolved Incident needs its
  Postmortem to exist. Class admission reads each document's own state, and
  `cancelled` is admitted by both `completed/` and `retired/`.
- The envelope check proves ancestry and object ID equality. It checks neither
  object type nor file mode, and nothing re-verifies an existing row later.
- Citability is written in three places that disagree. `CITABLE_NAMINGS`
  states which namings are citable. The link validator exempts Incident and
  Postmortem sources for every archive path, route records included. The
  archive validator repeats the target rule only for active and accepted
  documents, without the exemption. The pre-acceptance consumers that the
  policy calls enumerated exist only as Task prose.
- A move between active stages that comes without a scope migration fails as a
  rename or a creation, although ADR-0038 describes migrations as routes for
  consumers outside the repository. A route envelope must be a repository path,
  so a public URL cannot be recorded at all.
- Policy names a Git-history-only retention, but no profile is bound to it.
- The lifecycle gate compares a pull request with its merge base, so one
  document takes one state edge per integration.

## Decision

### What ADR-0038 keeps

Stage 98 keeps two kinds and six dispositions with the holdings ADR-0038 gave
them. One Retention Envelope `<commit>:<original path>` per catalog row stays
the only recovery reference, with no redirect, path ledger, self-designed
digest, branch SHA, or recovery commit. A superseded architecture decision
leaves Stage 02. The frozen ADR-0032 records, ledgers, and retained packages
keep their bytes and routes. Every disposition needs its own authorization.

### A disposition retains a unit

The registry declares three retention units. A Stage 03 spec package is
everything tracked under its directory, and its anchor is `spec.md`. An
Incident bundle is `incident.md` with its `postmortem.md`, and its anchor is
the Incident. Any other governed document is its own unit.

The anchor's state decides the class. `completed/` admits `done`,
`superseded/` admits `superseded`, `retired/` admits `withdrawn`, `retired`,
`rejected`, or `invalidated`, and `resolved/` admits a `closed` Incident whose
Postmortem is `published`. Every other member must be terminal in its own
family. A completed package may therefore retain a cancelled Task, and a
withdrawn package is retired rather than completed.

Completion does not authorize disposition. A finished unit waits in its stage
until its disposition is approved, and while it waits it is neither current
authority nor a permit for new execution. Age, size, missing inbound links, and
merge state are review signals, never authorization.

### Retention is exact

A retained unit is its source Git object, unchanged. Its catalog row names a
blob for a document and a tree for a package or bundle. Every entry under the
retained path, compared as relative path, file mode, and blob, equals the entry
of the envelope object. The envelope object equals the object the comparison
base holds at the original path. Nothing is rewritten, links included.

A retained body's links are read at its original path in the envelope commit,
never against the current tree. A retained unit is then frozen: it is not
edited, deleted, renamed, or recreated. The sixteen bodies retained under
ADR-0038 with rebased links keep that generation. The registry names them by
exact path, they are verified by link-resolved equivalence, and the set cannot
grow.

### An envelope stays verifiable

An envelope object must exist, have the unit's object type, and stay reachable
from the default branch. Full validation re-verifies every catalog row. A
missing object or unavailable history is a failure, never a skip.

### Retention modes are bound to profiles

The registry binds each retention mode to the profiles that may use it.

- `move-frozen-body` retains a unit in one of the four retention classes.
- `sealed-record` covers only the frozen ADR-0032 records and ledgers and admits
  no new record.
- `retain-in-place` keeps Stage 99 control documents and README routers in
  place and updates them there.
- `git-history-only` removes a Stage 99 form without a Stage 98 record; the
  removing commit named in its Task recovers it.

A mode with no bound profile cannot be applied.

### One ordered table decides citation

The registry holds an ordered citation table with a default of rejection. The
first matching rule decides. A target's kind comes from its registry profile,
not from its directory name, so a frozen record placed under a citable class is
still a frozen record.

1. A source under `docs/98.archive/` may link anywhere; its links are
   historical and validated in their own snapshot.
2. Any source may link the Archive index.
3. No other source links a route record, frozen migration ledger included; it
   reaches one through the index.
4. No other source links a frozen sealed record; it names the record by
   identifier and reaches it through the index.
5. An `operation/incident` or `operation/postmortem` source may link a retained
   body in any of the four retention classes as historical evidence.
6. Any source may link a retained body in `completed/` or `resolved/`.
7. Anything else is rejected.

Every validator that judges a citation consumes this one decision. This is a
local policy choice. External practice keeps superseded decisions citable, and
this repository instead sends a current reader to the successor so that a
replaced rule does not read as current. The Incident exemption is narrowed
because a route record holds no evidence body. No enumerated-consumer
exception carries forward; the cutover proves with the link gate that no
active citation depends on one.

### A move between active stages keeps its identity

A document that moves between active stages in one change, keeping its
`artifact_id`, family, and state, with its source removed and its inbound links
updated, is tracked by identity lineage and needs no Stage 98 record. A scope
migration is recorded only when a consumer outside the repository reads the
moved repository paths. Route dispositions name repository paths. Redirects
and gone responses for a public service URL belong to that site's owner, not to
Stage 98.

### Security precedes retention

Secret-bearing content follows the secret-handling process, which rotates the
credential first. Retention never keeps a credential and never stands in for a
history purification, which needs its own approval.

## Explicit Non-goals

- It does not rewrite, re-seal, or re-home the frozen ADR-0032 generation or the
  sixteen bodies retained under ADR-0038.
- It does not itself change the registry, forms, or validators.
  [Spec 0082](../../03.specs/0082-unit-archive-retention-contract/spec.md) owns
  that cutover after acceptance.
- It does not add lifecycle states or edges.
- It does not retain ADR-0038. That disposition needs its own authorization
  after the supersession is accepted.
- It does not route public URLs, and it adopts no external preservation standard
  or certification.
- It authorizes no live cluster, provider runtime, or network action.

## Consequences

One comparison of Git objects proves a unit's membership, bytes, and file
modes. New dispositions need no link-rewriting code, one table answers every
citation question, and an internal move no longer needs a record.

The registry grows by units, modes, the citation table, and a finite legacy set.
Full validation needs the history the envelopes name, so a shallow or partial
clone fails it rather than skipping it. A retained body's relative links do not
resolve from its archive location in a file browser; a reader follows them at
the envelope commit. Incident and Postmortem records lose direct links to route
records.

The one-edge rule turns this change into three integrations: this proposal, then
acceptance with the machine cutover, then the retention of ADR-0038.

## Alternatives

**Keep link rebasing with a stricter comparison.** Rejected: the retained bytes
would still differ from the object the envelope recovers, and every comparison
would still depend on a link parser agreeing with the renderer.

**One catalog row per file, with membership compared against the base
listing.** Rejected: it repeats what one tree object already hashes and
multiplies rows without adding evidence.

**Amend ADR-0038 clause by clause.** Rejected: its core clauses would then
conflict between two accepted decisions, which is the drift ADR-0038 set out to
remove.

**Keep citability derived from naming.** Rejected: the derivation was itself a
stipulation in code, and the Incident exemption lived outside it.

**Keep a scope migration for every move.** Rejected: without an outside
consumer the record repeats the identity lineage the lifecycle gate already
records.

**Keep the Incident exemption for every archive path.** Rejected: a route record
holds no evidence body to cite.

## Traceability

### Lifecycle Traceability

| Decision lineage | Replacement relation                                                                                                             | Affected Spec                                                            |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| ADR-0038 | Supersedes ADR-0038; the frozen ADR-0032 generation and the sixteen ADR-0038 retained bodies keep their generation | [Spec 0082](../../03.specs/0082-unit-archive-retention-contract/spec.md) |
