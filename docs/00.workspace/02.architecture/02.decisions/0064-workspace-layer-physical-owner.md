---
title: "Workspace Layer Physical Owner and Numbered Categories"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-11-19"
artifact_id: "ADR-0064"
---

# ADR-0064: Workspace Layer Physical Owner and Numbered Categories

## Context

### Problem and Drivers

The shared work rules of people and agents (the W layer of SDLC-R036) lived in
`.agents/governance/` beside the agent execution policies, and the common
vocabulary lived in the agent knowledge surface, so the folder did not show
which meaning was shared and which was agent-only. The category folders of
`docs/` were unnumbered, unlike the stages.

### Decision Scope

This decision amends only the location clause of ADR-0058 Decision 1: the
Repository Vocabulary moves from `.agents/knowledge/glossary.md` to
`docs/00.workspace/01.project/glossary.md`. Every other ADR-0058 clause, the
term IDs and the vocabulary contract version stay.

## Options

### Considered Options

Keep the current paths, copy W rules into a new folder, or move each W owner
once with its consumers.

### Trade-offs

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| Keep current paths | No consumer change. | The folder keeps mixing W and A meaning. | Not selected: the user adopted `docs/00.workspace/` on 2026-11-18. |
| Copy W rules | Old links keep working. | Two active sources of one rule. | Not selected: one meaning has one active source. |
| Move once with consumers | One owner per meaning; history stays recoverable. | Every reader and link changes in one commit. | Chosen: the Problem asks for a visible single owner. |

## Decision

### Chosen Option

`docs/00.workspace/` owns the W layer: the vocabulary (`01.project/`), the
workspace architecture (`02.architecture/`), SDLC, document and Git process
(`03.process/`), quality, formatting and approval (`04.quality/`) and
maintenance (`06.maintenance/`). Approval and safety and Git are split along
their W and A rule lists, each rule ID keeping one owner. The category folders
of `docs/` carry two-digit numbers. Architecture is split by the system a
record changes: the work system (documents, agents, QA, CI, Git, release,
disposition) in `docs/00.workspace/02.architecture/`, the product platform in
`docs/02.architecture/`. ADR-0030, 0031, 0033, 0036, 0047, 0048, 0052, 0053,
0055 to 0063 and AD-0006 are work-system records; AD and ADR numbers share one
sequence. A move keeps every document ID, rule ID and historical body
(DOCLIFE-R023).

### Authority and Effect

The user adopted the physical owner on 2026-11-18 (SDLC-H01) and the path plan
on 2026-11-19 (DOC-H01), asked for this change on 2026-11-19, and accepted this
decision on 2026-11-19 after reviewing it (SPEC-0224 Task EVD-012). The
implementation is in SPEC-0224, commits `0806c3b0` and `8557aa8e`.

#### Sources

[ADR-0058](./0058-repository-vocabulary-in-knowledge-surface.md),
[AD-0006](../01.descriptions/0006-workspace-agent-governance-platform.md) and
the [SDLC policy](../../03.process/sdlc.md) SDLC-R036.

#### Supersession

No ADR is superseded; ADR-0058 is amended in its location clause only.

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0058 Decision 1 location](./0058-repository-vocabulary-in-knowledge-surface.md) | Amends only the glossary location; every other clause stays | [SPEC-0224](../../../03.specs/0224-workspace-path-cutover/spec.md) |

## Consequences

### Impacts

Readers find shared rules under `docs/00.workspace/` and agent-only rules
under `.agents/governance/`. Validators, profiles and links use the numbered
paths; history at `4b2b670d` recovers the old paths.

### Follow-up

ID renumbering, history rewrite and Stage 98 disposal stay with Q07-CUTOVER
after Q07-H01.
