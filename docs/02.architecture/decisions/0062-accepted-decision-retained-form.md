---
title: "Accepted Decision Retained Form"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "platform"
updated: "2026-11-14"
artifact_id: "ADR-0062"
---

# ADR-0062: Accepted Decision Retained Form

## Context

### Problem and Drivers

[ADR-0059](./0059-registry-common-form-model.md) Decision 5 says the H2 lists
stay only for profiles whose role has no form yet, and that the change that
moves the last role removes the lists and their checks. Decision 2 of the same
record says a role receives its form only in the change that moves its
documents, and its Follow-up says the ADR family keeps its current form for
accepted ADRs until each is replaced (W03-D02). The two cannot both hold once
the ADR role receives its form: the accepted ADRs keep seven H2 that the form
tree does not have, so their lists and the checks that read them must outlive
the change that moves the last role. [ADR-0061](./0061-registry-schema-version-semver.md)
is the last accepted ADR written in the form of its day.

On 2026-11-14 the user decided W03-D52 (the accepted-ADR exception is a retained
form bounded by a closed identity range) and, by W03-D69, that the range is
ADR-0001 to ADR-0061. The sixty-one identities include numbers whose ADR has
left the tree, which `LIFECYCLE-IDENTITY-REUSE` already refuses to mint again.
[REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md)
makes the registry the single machine owner of document form;
[AD-0006](../descriptions/0006-workspace-agent-governance-platform.md) is the
governance view.

### Decision Scope

This record covers the ADR role only: the form an accepted ADR is checked
against, the key `layer`, and how the removal in ADR-0059 Decision 5 reads for
the ADR role. It changes no accepted ADR, no other role's form and no lifecycle
state. The removal of the H2-list model for profiles, of `_form_headings` and of
the list-mode checks stays with the change that moves the last role.

## Decision

### Chosen Option

1. **Retained form.** An accepted ADR whose identity is in ADR-0001 to ADR-0061
   keeps the seven H2 it was accepted with (Overview, Context, Decision,
   Explicit Non-goals, Consequences, Alternatives, Traceability). The registry
   holds them as one `retained_form` extension of the ADR form, bounded by an
   anchored identity expression that matches those sixty-one identities and
   nothing else.
2. **Common form after the range.** Every ADR written after ADR-0061 takes the
   common ADR form in every status, `accepted` included. The bound is closed:
   the registry check refuses a bound of the ADR role that matches ADR-0062,
   and the bound is never widened.
3. **Narrowing of ADR-0059 Decision 5.** The H2 lists and list checks of
   profiles leave with the change that moves the last role, as Decision 5 says.
   The retained H2 lists of the accepted ADRs in the range are not profile
   lists. They stay, with their checks, as a registered extension under
   Decision 2 until a successor replaces each of those ADRs. This record
   replaces no paragraph of ADR-0059 and every other clause of it stays.
4. **Layer key.** The key `layer` stays only on an accepted ADR inside the same
   range and is never added to a new document, so both accepted-ADR exceptions
   share the one identity discriminator.

### Authority and Effect

The current user is the decision maker and decides acceptance of this record;
it is `proposed` until the user's approval is recorded in the SPEC-0198 Task and
in the commit that sets it `accepted`. That acceptance accepts no SPEC-0198
criterion by itself. Once accepted, the narrowing applies from that commit, and
ADR-0059 gains one dated current-state clarification that links this record.
Compliance is confirmed by the registry, Markdown profile, links and lifecycle
validators, the SPEC-0198 regression tests and the SPEC-0198 Task.

## Alternatives

### Considered Options

- **Retain through ADR-0060 (W03-D52 as first written):** rejected by W03-D69;
  ADR-0061 was accepted before this change lands and is written in the old form.
- **Retain by status alone:** rejected; an ADR accepted in the common form would
  fail against the retained lists.
- **Migrate every accepted ADR to the common form:** rejected; W03-D02 keeps an
  accepted ADR in the form it was accepted in, and an accepted decision is never
  edited in place.
- **Remove the lists with the last role regardless:** rejected; the accepted
  ADRs would then have no H2 contract at all.

### Trade-offs

| Alternative | Trade-off |
| --- | --- |
| Closed identity range (chosen) | Two heading models coexist for the ADR role until each ADR in the range is replaced; the bound and its check keep the range from widening unnoticed. |
| Retain through ADR-0060 | Needs one more accepted ADR to be migrated or exempted, which breaks W03-D02. |
| Retain by status alone | Makes the exception open-ended, so a new accepted ADR could keep the old form. |
| Migrate every accepted ADR | Rewrites accepted decisions and their approval history. |
| Remove the lists with the last role regardless | Leaves 36 accepted ADRs unchecked. |

## Consequences

### Impacts

- **Positive:** the ADR role has a form and a TemplateDefinition, a new ADR
  starts from the common form, and the exception is a registered, bounded and
  checked extension instead of an open status rule.
- **Negative:** a reader must combine ADR-0059 with this record until each ADR
  in the range is replaced.
- **Operational:** the bound is an anchored expression over the artifact
  identity, and `layer` follows it.

### Follow-up

The retained form is removed when no ADR in the range remains in the tree, each
having been replaced by a successor. The package that removes the H2-list model
for profiles (package 7 of W03-D49) keeps this extension. The SPEC-0198 package
exit rewrites the affected-Spec cell below to the left-the-tree form.

## Traceability

### Sources

- **Requirements:** [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md), [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md).
- **Architecture:** [AD-0006](../descriptions/0006-workspace-agent-governance-platform.md).
- **Decisions:** W03-D02, W03-D52 and W03-D69, recorded in the SPEC-0161 Task.

### Supersession

This record supersedes no ADR. It narrows Decision 5 of
[ADR-0059](./0059-registry-common-form-model.md) as Decision 3 states and
leaves every other clause of it in force.

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0059](./0059-registry-common-form-model.md) | Narrows only Decision 5 by dated clarification; replaces no paragraph and every other clause stays | [SPEC-0198](../../03.specs/0198-w03-adr-form/spec.md) |
