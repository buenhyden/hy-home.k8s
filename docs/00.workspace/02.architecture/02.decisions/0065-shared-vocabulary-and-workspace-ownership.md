---
title: "Shared Vocabulary and Workspace Ownership"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "platform"
updated: "2026-11-20"
artifact_id: "ADR-0065"
supersedes: "ADR-0064"
---

# ADR-0065: Shared Vocabulary and Workspace Ownership

## Context

### Problem and Drivers

ADR-0064 established the physical workspace policy owner and separated work-system
architecture from the GitOps product. Those boundaries remain useful. Its glossary
location clause placed shared meanings and local terminology in one document. The
current P03 request instead requires separate common and local meaning owners and
an environment owner with actual preparation content.

### Decision Scope

Correct vocabulary ownership and name the environment owner. Preserve the W/A
policy split, architecture subjects, numbered categories, shared AD/ADR sequence
and stable identifiers. Consumers are knowledge, document profiles and validators,
workspace routers, provider readers and architecture descriptions. Common-contract
adoption, native permissions, renumbering and later runtime work are excluded.

## Options

### Considered Options

Keep one local glossary, copy definitions into both locations, or divide meanings
by scope and update their consumers together.

### Trade-offs

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| One local glossary | No path migration. | Shared meanings stay coupled to local terminology. | Does not meet the current P03 requirement. |
| Duplicate definitions | Both entry points contain every definition. | Independent sources can disagree about one meaning. | Conflicts with the single-owner requirement. |
| Divide by scope | One definition per meaning and explicit local terminology. | Readers and validators follow two owners. | Selected by the current request, preserving IDs and updating consumers together. |

## Decision

### Chosen Option

This proposed decision records boundaries implemented under the separate current
user authorization:

1. `.agents/knowledge/glossary.md` owns shared Repository Vocabulary meanings,
   stable TERM IDs, scope and consumer/policy-owner links. It grants no permission
   and copies no operating rule. ADR-0058's admission of one meaning document into
   the otherwise pointer-only common knowledge surface remains intact.
2. `docs/00.workspace/01.project/glossary.md` owns local Kubernetes/GitOps terms and
   links to common definitions. Scoped local meanings do not redefine common
   terms; aliases are search aids, not another authority.
3. `docs/00.workspace/` remains the W layer: purpose and local terms in
   `01.project/`, work-system architecture in `02.architecture/`, SDLC/document/Git
   process in `03.process/`, quality/formatting/approval in `04.quality/`,
   reproducible preparation in `05.environment/` and workspace maintenance in
   `06.maintenance/`. Create a category only for real content. Preparation points
   to tool, lock, sandbox and resource owners without secrets or runtime claims.
4. `.agents/` retains common agent execution, roles, skills and procedures that
   read workspace policy. `.claude/` and `.codex/` retain native settings and thin
   adapters. SAFE and GIT keep their existing W/A rule lists and one owner per
   Rule ID. Provider projections have no independent policy authority.
5. Work-system architecture describes development, validation, memory and harness
   structure under `docs/00.workspace/02.architecture/`. The GitOps product and
   deployment interfaces stay under `docs/02.architecture/`. Both use
   `01.descriptions/` and `02.decisions/` for actual descriptions and decisions.
   Correctly placed architecture is retained.
6. Two-digit numbered `docs/` categories, the shared AD/ADR sequence, document IDs and rule
   IDs stay unchanged. Moves preserve identities and historical bodies under
   DOCLIFE-R023. Final renumbering and history disposition remain later work.

### Authority and Effect

The user's 2026-11-20 P03 request separately authorizes implementation and consumer
repair, recorded in the [current Task authorization](../../../03.specs/0223-work-residue-handoff/01.tasks/tsk-0001-work-residue-handoff.md#p03-110-current-authorization).
That request overrides the old location clause; this proposed ADR is not execution
authority. It remains `proposed` until the user accepts the decision itself.
Implementation, static checks, PR merge and acceptance are separate outcomes.
Focused knowledge, profile, relationship, link and lifecycle checks confirm only
the changed repository contract.

#### Sources

- [REQ-0003-FR-0032](../../../01.requirements/0003-workspace-agent-governance-platform.md)
  requires one owner for shared meanings and separate policy rules.
- [AD-0006](../01.descriptions/0006-workspace-agent-governance-platform.md) owns the
  work-system view; [AD-0007](../../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md)
  owns the product view.
- [ADR-0058](0058-repository-vocabulary-in-knowledge-surface.md) admits the common
  glossary and stable IDs without turning knowledge into policy.

#### Supersession

ADR-0064 is removed through this authorized correction, with its accepted history
and retained obligations summarized in [AD-0006 Archived Lineage](../01.descriptions/0006-workspace-agent-governance-platform.md#archived-lineage).
Its acceptance remains historical evidence in SPEC-0224, not acceptance of this
successor. Every ADR-0058 clause apart from the later location change is preserved.
No approval or native-runtime result is inferred from replacement.

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [AD-0006 Archived Lineage](../01.descriptions/0006-workspace-agent-governance-platform.md#archived-lineage), ADR-0064 | Supersedes ADR-0064 under current P03 authority; retains W/A, architecture and identifier obligations | [SPEC-0223](../../../03.specs/0223-work-residue-handoff/spec.md); its Task holds separate P03 authority and evidence, while completed residue-transfer constraints stay historical |
| [ADR-0058](0058-repository-vocabulary-in-knowledge-surface.md) | Preserves the common glossary admission and non-location obligations | [SPEC-0223](../../../03.specs/0223-work-residue-handoff/spec.md), separate P03 follow-up |

## Consequences

### Impacts

Common readers and both provider gateways reach one meaning owner. Local terms
remain beside the workspace. The additional navigation boundary is checked by
existing document and knowledge consumers. Native settings, cluster runtime and
completed P00/P01/P02 behavior are retained.

### Follow-up

The current Task records checks, review, delivery and pending decision acceptance.
A failed change is recovered through a normal corrective PR, with predecessor
bytes retained in Git. P04 owns later common-form work, the runtime prompts own
native observations, and P17 owns final renumbering and approved history
handling. None is performed by this ADR.
