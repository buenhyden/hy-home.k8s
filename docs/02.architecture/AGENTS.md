# AGENTS.md

Agent instructions for `docs/02.architecture/` and its `descriptions/` and
`decisions/` collections. The parent [`docs/AGENTS.md`](../AGENTS.md) still
applies.

## Scope

### Allowed Surface

Stage 02 holds Architecture Descriptions (AD), which expand requirements into
system boundaries, views and quality attributes, and Architecture Decision
Records (ADR), which record durable technical and operating decisions.

| Work here | Role (`.agents/roles/`) | Skills | Claude | Codex |
| --- | --- | --- | --- | --- |
| Make or change a structural decision | [architect](../../.agents/roles/architect.md) | `requirements-to-design`, `docs-stage-routing` | `.claude/agents/architect.md` | `.codex/agents/architect.toml` |
| Author AD or ADR text | [doc-writer](../../.agents/roles/doc-writer.md) | `docs-stage-conformance`, `docs-stage-routing`, `requirements-to-design` | `.claude/agents/doc-writer.md` | `.codex/agents/doc-writer.toml` |
| Review a decision's risk | [code-reviewer](../../.agents/roles/code-reviewer.md) | `risk-report` | `.claude/agents/code-reviewer.md` | `.codex/agents/code-reviewer.toml` |
| Keep collection indexes current | [wiki-curator](../../.agents/roles/wiki-curator.md) | `docs-stage-conformance`, `knowledge-map` | `.claude/agents/wiki-curator.md` | `.codex/agents/wiki-curator.toml` |

### Non-goals

Non-goals are stated in rules 5 and 6 under Local Obligations.

## Required Policies

### Canonical Sources

Canonical sources are the documents linked or named in the opening paragraph and in the rules under Local Obligations.

### Local Obligations

1. The parent folder decides the type: `descriptions/####-<slug>.md` uses
   `sdlc/architecture-description`, `decisions/####-<slug>.md` uses
   `sdlc/architecture-decision`. Start from the matching form in
   `docs/99.templates/templates/architecture/`.
2. AD states are `draft`, `in-review` and `active`; ADR states are
   `proposed`, `accepted` and `rejected`. Moving an ADR to `accepted` needs
   the operator's recorded approval. `rejected` is the decision outcome that
   triggers the ADR's exit, not a state kept in the tree: once the manual
   disposition review is satisfied, summarize the ADR in the owning AD's
   `Archived Lineage` and delete it in the same change, as the
   [document lifecycle policy](../../.agents/governance/document-lifecycle.md)
   requires; otherwise defer.
3. Never edit an accepted decision in place. Write a successor ADR whose
   `supersedes` and Traceability keep the predecessor ID, summarize the
   predecessor in the owning AD's `Archived Lineage` table, and delete it in
   the same change. There is no `superseded` state in this stage.
4. Trace every AD and ADR to full `REQ-####-(FR|NFR|IF)-####` IDs and to the
   affected Spec; a deleted Spec is written as
   `N/A — SPEC-xxxx left the tree; Git history recovers it`.
5. Apply arc42 sections proportionally and prefer C4 context and container
   views. Do not copy Kubernetes manifests or GitOps desired state into a
   document body; link the implementing path.
6. Hand implementer-level contracts to `docs/03.specs/` and operating
   procedures to `docs/05.operations/`.
7. Update `descriptions/README.md` or `decisions/README.md` in the same change
   that adds, retitles or deletes a document.

## Workflow

### Inspect and Change

Inspecting and changing files follows the rules under Local Obligations.

### Handoff

Handoff is stated in rule 6 under Local Obligations.

## Verification

### Required Checks

Run the strict document checks listed in the parent `AGENTS.md`.

### Evidence and Limits

This folder adds no evidence rule beyond the quality policy's handoff contract; if a check here has a limit to report, state it here.

## Safety

### Protected Actions

Protected actions are stated in rules 2 and 3 under Local Obligations.

### Stop and Escalate

Stop and escalation conditions are stated in rule 2 under Local Obligations.
