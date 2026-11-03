# AGENTS.md

Agent instructions for `docs/03.specs/` and every Spec package below it. The
parent [`docs/AGENTS.md`](../AGENTS.md) still applies.

## Purpose

Stage 03 holds change packages `####-<slug>/`: `spec.md` owns the change
contract and acceptance criteria, `plan.md` the work order, risks and
rollback, and `tasks/tsk-####-<slug>.md` the actual execution, evidence and
criterion acceptance. A package exists only while its change is open.

## Responsibilities and Projections

| Work here | Role (`.agents/roles/`) | Skills | Claude | Codex |
| --- | --- | --- | --- | --- |
| Break work into a Spec, Plan and Task | [supervisor](../../.agents/roles/supervisor.md) | `task-breakdown`, `execution-plan`, `risk-report` | `.claude/agents/supervisor.md` | `.codex/agents/supervisor.toml` |
| Author package documents | [doc-writer](../../.agents/roles/doc-writer.md) | `docs-stage-conformance`, `docs-stage-routing`, `requirements-to-design` | `.claude/agents/doc-writer.md` | `.codex/agents/doc-writer.toml` |
| Run checks and record Task evidence | [quality-engineer](../../.agents/roles/quality-engineer.md) | `k8s-validate`, `workspace-harness-audit` | `.claude/agents/quality-engineer.md` | `.codex/agents/quality-engineer.toml` |
| Independent change review | [code-reviewer](../../.agents/roles/code-reviewer.md) | `risk-report` | `.claude/agents/code-reviewer.md` | `.codex/agents/code-reviewer.toml` |

## Rules

1. Start from `docs/99.templates/templates/specs/{spec,plan,task}.template.md`.
   Do not add a README or other router inside a package.
2. Create a new Spec and Plan as `draft` and approve them in a separate
   commit after review; the approval records the operator's request in the
   Task Inputs. Approval never claims implementation or acceptance.
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
   `Promotion` table, is summarized in the Requirement's `Archived Lineage`
   table, and is deleted. Update this stage's README in the same change.

## Checks

Run the strict document checks listed in the parent `AGENTS.md`, plus
`python3 scripts/validate-document-lifecycle.py --root . --mode staged`
before each commit, and `python3 scripts/qa.py staged` on the exact index.
