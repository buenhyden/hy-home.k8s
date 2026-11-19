# AGENTS.md

Agent instructions for `docs/03.specs/` and every Spec package below it. The
parent [`docs/AGENTS.md`](../AGENTS.md) still applies.

## Scope

### Allowed Scope

Stage 03 holds change packages `####-<slug>/`: `spec.md` owns the change
contract and acceptance criteria, `plan.md` the work order, risks and
rollback, and `tasks/tsk-####-<slug>.md` the actual execution, evidence and
criterion acceptance. A package exists only while its change is open. The folder also holds
`work-residue-ledger.json`, the work residue ledger of open handoff, conflict,
adoption and survey residue as pointers; the Task owns execution state.

| Work here | Role (`.agents/roles/`) | Skills | Claude | Codex |
| --- | --- | --- | --- | --- |
| Break work into a Spec, Plan and Task | [supervisor](../../.agents/roles/supervisor.md) | `task-breakdown`, `execution-plan`, `risk-report` | `.claude/agents/supervisor.md` | `.codex/agents/supervisor.toml` |
| Author package documents | [doc-writer](../../.agents/roles/doc-writer.md) | `docs-stage-conformance`, `docs-stage-routing`, `requirements-to-design` | `.claude/agents/doc-writer.md` | `.codex/agents/doc-writer.toml` |
| Run checks and record Task evidence | [quality-engineer](../../.agents/roles/quality-engineer.md) | `k8s-validate`, `workspace-harness-audit` | `.claude/agents/quality-engineer.md` | `.codex/agents/quality-engineer.toml` |
| Independent or requested change review | [code-reviewer](../../.agents/roles/code-reviewer.md) | `risk-report` | `.claude/agents/code-reviewer.md` | `.codex/agents/code-reviewer.toml` |

#### Non-goals

This folder adds no non-goal beyond the parent `AGENTS.md` and the governance policies; if work here must be excluded, state it here.

### Instruction Precedence

#### Canonical Sources

Canonical sources are the documents linked or named in the opening paragraph and in the rules under Local Obligations.

## Workflow

### Intake

#### Local Obligations

1. Start from `docs/99.templates/templates/specs/{spec,plan,task}.template.md`.
   Do not add a README or other router inside a package.
2. Create a new Spec and Plan as `draft` and approve them in a separate
   commit after review. When scoped user approval and actual batch review
   precede their first Git record, the local first-record approval extension
   in the [document lifecycle policy](../../.agents/governance/document-lifecycle.md)
   permits both same-package documents to enter at `approved` together only
   with the exact review and approval receipt in the Task's Results table. Keep
   the user's request in the Task's Inputs and Authority; do not invent a draft-only commit or omit observed
   evidence. Approval never claims implementation, criterion acceptance, ADR
   acceptance, or protected-action authority.
3. Task rows move `draft` → `ready` → `in-progress` → `completed`. A row is
   `completed` only with PASS evidence; record a blocker with its cause,
   resume condition and next owner. A Task with one item keeps its state in
   frontmatter `status`, and that row's `Status` holds the marker
   `frontmatter`. A Task with several items omits frontmatter `status`:
   readers derive the summary from its rows, and a status that is present must
   equal that summary (`TASK-EXECUTION-SUMMARY`).
4. Task evidence is append-only. Keep every recorded `EVD-###` row and its
   factual fields unchanged; add a new row whose `Resolves` cell names the
   row it closes. Never rewrite completed evidence to fit a later form. A
   Task's tables are read only under the core header of the registry.
5. Record only observed results with their exact revision or run identity.
   An unobserved hosted or live check stays `NOT_RUN` or `DEFER` with a named
   next owner.
6. Criterion acceptance is the operator's decision; an agent records PASS
   evidence and leaves `Acceptance` pending until the operator accepts.
7. For ordinary completed-package disposition, promote each durable contract through the Plan's
   promotion table under Promotion Map > Durable Owners (Promotion ID,
   Target Owner, Acceptance, Evidence). Before its final source commit, its Task freezes the
   consumer, hold, authority and method decision. After that commit, the
   Requirement's `Archived Lineage` records each file's recovery proof and
   summary, and the whole package is deleted in that same change with this
   stage's README updated. Residue is written as a `Residue Handoff` row in the
   Task and an entry in the ledger in the same change, and a terminal entry is
   deleted no later than the exit commit of the package whose Task holds its
   closure row. An unresolved condition defers the deletion. The
   staged `LIFECYCLE-PACKAGE-EXIT` check refuses the wrong shape; see the
   [document lifecycle policy](../../.agents/governance/document-lifecycle.md).

### Execution

Inspecting and changing files follows the rules under Local Obligations.

## Boundaries

### Authority

#### Stop and Escalate

Stop and escalation conditions are stated in rules 3, 5 and 7 under Local Obligations.

### Secrets and External Effects

#### Protected Actions

Protected actions are stated in rules 2 and 6 under Local Obligations.

## Verification

### Checks

Select the document checks in the parent `AGENTS.md`. For delivery, the
staged QA route runs the selected lifecycle and document checks against the
exact index.

### Reporting

#### Evidence and Limits

Evidence rules are stated in rules 4 and 5 under Local Obligations.

#### Handoff

Handoff is stated in rules 3 and 5 under Local Obligations.
