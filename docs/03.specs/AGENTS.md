# AGENTS.md

Agent instructions for `docs/03.specs/` and every Spec package below it. The
parent [`docs/AGENTS.md`](../AGENTS.md) still applies.

## Scope

### Allowed Surface

Stage 03 holds change packages `####-<slug>/`: `spec.md` owns the change
contract and acceptance criteria, `plan.md` the work order, risks and
rollback, and `tasks/tsk-####-<slug>.md` the actual execution, evidence and
criterion acceptance. A package exists only while its change is open.

| Work here | Role (`.agents/roles/`) | Skills | Claude | Codex |
| --- | --- | --- | --- | --- |
| Break work into a Spec, Plan and Task | [supervisor](../../.agents/roles/supervisor.md) | `task-breakdown`, `execution-plan`, `risk-report` | `.claude/agents/supervisor.md` | `.codex/agents/supervisor.toml` |
| Author package documents | [doc-writer](../../.agents/roles/doc-writer.md) | `docs-stage-conformance`, `docs-stage-routing`, `requirements-to-design` | `.claude/agents/doc-writer.md` | `.codex/agents/doc-writer.toml` |
| Run checks and record Task evidence | [quality-engineer](../../.agents/roles/quality-engineer.md) | `k8s-validate`, `workspace-harness-audit` | `.claude/agents/quality-engineer.md` | `.codex/agents/quality-engineer.toml` |
| Optional change review (never a required reviewer) | [code-reviewer](../../.agents/roles/code-reviewer.md) | `risk-report` | `.claude/agents/code-reviewer.md` | `.codex/agents/code-reviewer.toml` |

### Non-goals

This folder adds no non-goal beyond the parent `AGENTS.md` and the governance policies; if work here must be excluded, state it here.

## Required Policies

### Canonical Sources

Canonical sources are the documents linked or named in the opening paragraph and in the rules under Local Obligations.

### Local Obligations

1. Start from `docs/99.templates/templates/specs/{spec,plan,task}.template.md`.
   Do not add a README or other router inside a package.
2. Create a new Spec and Plan as `draft` and approve them in a separate
   commit after review. When scoped user approval and actual batch review
   precede their first Git record, the local first-record approval extension
   in the [document lifecycle policy](../../.agents/governance/document-lifecycle.md)
   permits both same-package documents to enter at `approved` together only
   with the exact Task Evidence review and approval receipt. Keep the user's
   request in Task Inputs; do not invent a draft-only commit or omit observed
   evidence. Approval never claims implementation, criterion acceptance, ADR
   acceptance, or protected-action authority.
3. Task rows move `draft` → `ready` → `in-progress` → `completed`. A row is
   `completed` only with PASS evidence; record a blocker with its cause,
   resume condition and next owner.
4. Task evidence is append-only. Keep every recorded `EVD-###` row and its
   factual fields unchanged; add a new row whose `Resolves` cell names the
   row it closes. Never rewrite completed evidence to fit a later form.
5. Record only observed results with their exact revision or run identity.
   An unobserved hosted or live check stays `NOT_RUN` or `DEFER` with a named
   next owner.
6. Criterion acceptance is the operator's decision; an agent records PASS
   evidence and leaves `Acceptance` pending until the operator accepts.
7. A finished package promotes each durable contract through the Plan's
   `Promotion` table. Before its final source commit, its Task freezes the
   consumer, hold, authority and method decision. After that commit, the
   Requirement's `Archived Lineage` records each file's recovery proof and
   summary, and the whole package is deleted in that same change with this
   stage's README updated. An unresolved condition defers the deletion. The
   staged `LIFECYCLE-PACKAGE-EXIT` check refuses the wrong shape; see the
   [document lifecycle policy](../../.agents/governance/document-lifecycle.md).

## Workflow

### Inspect and Change

Inspecting and changing files follows the rules under Local Obligations.

### Handoff

Handoff is stated in rules 3 and 5 under Local Obligations.

## Verification

### Required Checks

Run the strict document checks listed in the parent `AGENTS.md`, plus
`python3 scripts/validate-document-lifecycle.py --root . --mode staged`
before each commit, and `python3 scripts/qa.py staged` on the exact index.

### Evidence and Limits

Evidence rules are stated in rules 4 and 5 under Local Obligations.

## Safety

### Protected Actions

Protected actions are stated in rules 2 and 6 under Local Obligations.

### Stop and Escalate

Stop and escalation conditions are stated in rules 3, 5 and 7 under Local Obligations.
