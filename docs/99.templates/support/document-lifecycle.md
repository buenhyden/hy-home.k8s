---
title: 'Document Lifecycle Support'
type: governance/template-support
status: active
owner: platform
updated: 2026-08-13
---

# Document Lifecycle Support

## Overview

This support contract explains why repository documents have distinct
lifecycle roles and how promotion, supersession, retention, archive, date
exceptions, and legacy disposition preserve trustworthy evidence. It
consolidates the former SDLC, common-documentation, and legacy-cleanup
rationale while leaving exact states, transitions, routes, values, and
exceptions in the Document Profile Registry.

## Purpose

Lifecycle guidance must let authors distinguish current authority from
historical evidence without rewriting the past or keeping duplicate active
owners. It must also preserve README navigation, references, archive records,
memory, progress, native contracts, and dated observations according to their
actual roles rather than forcing them into one delivery sequence.

## Owned Contract

### Lifecycle authority

The [Document Profile Registry](../registry.json) is the sole machine
owner of lifecycle domains, transitions, terminal states, evidence
predicates, relationship classes, admission rules, routes, and registered
exceptions. This document owns rationale and author procedure only.

[Document Contract](./document-contract.md) owns exact-one-profile, form,
body, and frontmatter rationale. [Document
Authoring](../../00.agent-governance/rules/document-authoring.md) owns agent
timing, stage choice, language, safety, checklist, and validation order.

### Delivery lifecycle and feedback

Requirements express product, system/software, and interface need;
Architecture Descriptions express the current structure and views; ADRs
record durable choices; Specs define implementation contracts; sibling Plans
and Tasks define order and execution evidence; operations guidance, policy,
runbooks, incidents, and postmortems operate and improve the system. The
numbered stages are responsibility boundaries, not a one-way waterfall.

New feature PRDs and Specs share stable lineage where the registry declares
it. Architecture uses its own stable identifiers. Stage 03 Plan and Task names
are fixed sibling roles, not date identities. Incident records may retain
year/event identity. Historical identifier mismatches remain explicit
evidence and are linked rather than cosmetically renumbered.

Lifecycle handoff is reciprocal and role-specific: requirements link to
architecture and Specs; architecture links upstream and downstream; Specs link
to input and execution evidence; Plans and Tasks link to their siblings;
operations link to the promoted contract, evidence, incident, or policy
owner; archive records retain original and replacement provenance.

### Supersession and Historical Preservation

- Accepted decisions are append-only decision evidence. A changed choice uses
  a successor ADR with an explicit supersession relation.
- Done execution evidence remains historical. New execution creates or
  activates the appropriate sibling Plan/Task rather than rewriting the old
  result.
- Current body enforcement applies only to registry-selected current
  consumers. Canonical forms keep source parity; accepted/done history is not
  retrofitted to manufacture evidence.
- Stages 01 through 03 cannot keep multiple active owners with the same role,
  purpose, and lineage.
- Superseded, duplicate, obsolete, migrated, or implementation-conflicting
  content receives a reviewed disposition. A status label alone cannot hide a
  conflicting current contract.
- Historical references remain only when their observation/evidence role is
  explicit and they cannot be mistaken for current instruction.

### README, reference, memory, and progress roles

- README files are frontmatter-free indexes selected by path. They mirror
  inventory and link canonical owners; they do not own lifecycle rules.
- Reference documents own durable lookup facts, authority/source boundaries,
  freshness, and dated snapshots. They do not duplicate current requirements,
  decisions, Specs, Plans, Tasks, policies, or runbooks.
- Reference role labels such as Current, Historical, Resolved, Included, or
  Index describe collection membership, not substitute frontmatter states.
- Standalone governance memory uses the memory form and a same-change progress
  entry. `progress.md` is reserved for the canonical append-only ledger.
- Provider-local recall and ignored scratch are auxiliary, non-authoritative,
  and subordinate to repository evidence.

### Archive and retention

- Stage 98 stores immutable terminal history under stable paths. The outer
  record preserves source path, replacement, source commit/blob, payload
  digest, legacy evidence, and complete original bytes.
- Active documents link historical content through the Stage 98 collection
  index. Direct record links belong only to index, migration, and provenance
  owners.
- Archive records and index rows are evidence, not current operating guidance.
  The current replacement owns active behavior.
- Existing payload/provenance is byte-stable. Generic formatting does not
  normalize it; archive validation, recovery, digest, secret classification,
  and index parity remain fail closed.
- An active owner moves only after replacement coverage, reviewed
  disposition, source and target identity, secret classification, index
  membership, and recovery pass atomically.
- Deletion or merge never erases terminal evidence: the migration/tombstone
  contract retains a unique stable record and the action/replacement semantics
  selected by the registry.

### Date identity and exceptions

Mutable authored routes use stable identifiers rather than calendar dates.
Dates remain metadata unless the registry admits a bounded observation/event
identity, such as a dated Stage 90 pack or a real Incident/Postmortem path.
Terminal Stage 98 paths are stable and date-free. A new date-bearing route is
invalid unless its exact class and evidence boundary are registered; prose
cannot create an exception.

### Legacy disposition

Classify every retired key, value, heading, route, template, owner, active
consumer, generated residue, or tracked scratch surface before removal:

- migrate current semantics to the named owner;
- retain explicit historical or native evidence where its role is still true;
- archive implementation-conflicting content through the approved mechanism;
- delete exact duplicates, reproducible unowned output, or zero-consumer
  residue only after proof; and
- keep validators whose rule, input, diagnostics, negative fixture, evidence,
  or recovery responsibility is distinct.

Active contracts reject deprecated owner values, duplicate README policy
bodies, copied form instructions, unsupported metadata and headings,
frontmatter on GitHub-native controls, retired provider-doc trees, and tracked
backup/auth/token/cache/history/log residue. A dated audit may preserve a
resolved finding; its current successor records resolution instead of
rewriting the original observation.

## Authoring Rules

1. Classify the final path and read its lifecycle/evidence contract from the
   registry.
2. Start new content in an admitted draft state and require the named evidence
   for promotion; do not self-promote.
3. Preserve accepted decisions and done evidence, using successor and
   reciprocal lineage when behavior changes.
4. Reject duplicate active owners before authoring another document for the
   same role, purpose, and lineage.
5. Keep stable identity separate from review/update dates. Use only registered
   event/observation date exceptions.
6. Review README membership and reciprocal links in the same change.
7. Before archive or deletion, prove current replacement, reviewed
   disposition, exact payload/provenance, secret classification, index parity,
   and read-only recovery.
8. Keep generated, native, provider, and historical evidence within its
   declared boundary; repository-static PASS cannot promote runtime evidence.
9. Record validation lanes, limitation, rollback, residual risk, and next
   owner in the Task and progress ledger.

### Common-document rules

- GitHub-native controls remain frontmatter-free and point to durable owners.
- Cloud example snapshots remain approved Stage 90 evidence; retired provider
  documentation trees stay absent.
- The generic reference form contains no archive policy; archive behavior
  belongs to the archive form, registry, index, and this lifecycle rationale.
- The progress form defines an appendable entry, not an alternate progress
  file or whole-document schema.

## Validation Contract

Lifecycle changes must prove:

- the registry, schema, forms, current consumers, README mirrors, and fixtures
  agree on one state/evidence model;
- accepted and done evidence was not rewritten without a reviewed finite
  projection;
- no duplicate active role/lineage owner remains;
- mutable authored and terminal Stage 98 routes are date-free, with only
  registered observation/event exceptions;
- legacy dispositions are complete and no current consumer points to a
  removed owner;
- archive bytes, provenance, index membership, secret classification, and
  recovery remain exact; and
- repository-static results remain separate from CI, provider-runtime,
  remote, credential-bearing, and live evidence.

Run:

```bash
python3 scripts/validate-document-lifecycle.py --root . --self-test
python3 scripts/validate-document-lifecycle.py --root . --mode staged
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/archive_cutover.py --root .
bash scripts/validate-repo-quality-gates.sh .
```

Historical preservation is not an exemption from exact current-owner,
replacement, provenance, or recovery checks. Any ambiguous disposition stops
the lifecycle change.

## Related Documents

- [Document Profile Registry](../registry.json)
- [Document Route Contract](../contracts/route-contract.json)
- [Document Registry Form Schema](../contracts/registry-form.schema.json)
- [Document Contract](./document-contract.md)
- [Document Authoring](../../00.agent-governance/rules/document-authoring.md)
- [Archive Index](../../98.archive/README.md)
- [Spec-Driven SDLC and Document Contracts](../../90.references/research/2026-08-08-wer/spec-driven-sdlc-and-document-contracts.md)
