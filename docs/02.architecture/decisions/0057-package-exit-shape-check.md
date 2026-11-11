---
title: "Package Exit Shape Check"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "platform"
updated: "2026-11-11"
layer: "architecture"
artifact_id: "ADR-0057"
---

# ADR-0057: Package Exit Shape Check

## Overview

This proposed amendment narrows one clause of accepted
[ADR-0056](./0056-manual-document-disposition-review.md) Decision 6,
"Existing validators do not enforce them", for Stage 03 packages only. A
staged commit that removes a Stage 03 package in the wrong shape becomes a
validation failure. The rest of ADR-0056 is unchanged: recovery proof, hold
review, consumer transfer and disposition authority stay a manual procedure
with independent review, and no archive-content or historical-cutover gate is
introduced. ADR-0056 keeps its body; this decision amends it, as ADR-0056
amended ADR-0053 and ADR-0055.

## Context

ADR-0056 Decisions 4 to 6 define how a completed Stage 03 package leaves the
tree: the package Task freezes its consumer, hold, authority and method
decision before the final source commit; the surviving Requirement's Archived
Lineage records each file's recovery proof; then the package is deleted. Its
Consequences say a bypass is not rejected automatically and that enforcement
needs a separately designed follow-up.

The W02 intake of the external v14.2 execution package (evidence only) found
that the lifecycle comparison reports nothing for deleted paths. An unfinished
package, part of a package, a package without an Archived Lineage entry, and
edits to a finished package's Spec or Plan all pass every check. A presence
check, which fails while a finished package is still in the tree, was
rejected: ADR-0056 Decision 5 lets a source stay in place without a time
limit, and marking each deferral would need a new field the lifecycle policy
forbids.

## Decision

1. **Event-scoped shape check.** In the lifecycle validator's `staged` mode,
   rule `LIFECYCLE-PACKAGE-EXIT` refuses a staged change that deletes any
   Markdown file of a Stage 03 package that is not finished at the base (R1),
   deletes only some of a package's Markdown files (R2), deletes a whole package while no
   Requirement changed in the same commit names its path in an Archived
   Lineage section (R3), or edits the Spec or Plan of a package that has at
   least one Task, all terminal (R4). The rule reads only the governed
   Markdown the lifecycle validator already reads; other file types in a
   package stay outside it.
2. **Finished.** A package is finished when every Task it has is `completed`
   or `cancelled` and either it has at least one Task or its Spec is
   `cancelled`.
3. **Manual remainder.** The rule checks the shape of one change only. It does
   not parse or verify recovery proof, holds, consumers or authority, does not
   check whether a finished package still exists, reads no archive, and runs
   in no CI or explicit-ref comparison. ADR-0056 Decision 6 still governs
   everything except the shape named in Decision 1.

## Explicit Non-goals

- Editing ADR-0056, ADR-0053 or ADR-0055.
- A presence, age or deferral-marker check, or a new field on any profile.
- Authenticating authority, verifying recovery bytes, or reading the archive.
- Coverage in CI or explicit-ref modes; per-commit replay is separate follow-up
  work.

## Consequences

- **Positive:** the closure shape ADR-0056 describes is enforced at commit
  time, and a finished package cannot silently become live scope again.
- **Trade-off:** a withdrawal takes two commits, the cancellation first and
  the deletion with its lineage summary later. A commit made without the
  active hooks is not checked.
- **Follow-up:** replay coverage over committed ranges remains open work.

## Alternatives

- **Presence gate:** rejected; it conflicts with ADR-0056 Decision 5 and
  needs a deferral marker the policy forbids.
- **No check:** rejected by the user on 2026-11-11 in favour of this rule.
- **Range check in CI:** rejected for now; the merge base hides a package
  created and closed in one range.

## Traceability

- **Requirements:** [REQ-0003-FR-0015, REQ-0003-FR-0020 and REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md).
- **Architecture:** [AD-0006](../descriptions/0006-workspace-agent-governance-platform.md).
- **Change:** [SPEC-0159](../../03.specs/0159-package-exit-shape-check/spec.md).
- **Policy:** [document lifecycle](../../../.agents/governance/document-lifecycle.md).

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0056](./0056-manual-document-disposition-review.md) | Narrows only Decision 6's "validators do not enforce them" for the Stage 03 package exit shape; every other clause stays | [SPEC-0159](../../03.specs/0159-package-exit-shape-check/spec.md) |
