---
name: docs-stage-routing
description: Use when routing generated documents into the canonical docs stage tree for this repository or blocking parallel hierarchies such as docs/superpowers.
---

# docs-stage-routing

## Purpose

Define the repository-local routing contract for document-generation workflows.

## Trigger Phrases

- "write a spec"
- "write a plan"
- "write an agent design"
- "write a reference doc"
- "document this skill"
- "docs/superpowers"
- "agent memory systems"
- "AGENTS.md refactor"
- "CLAUDE.md improver"

## Workflow Steps

1. Classify the requested output as governance, feature-bound design, execution plan, operational doc, or durable reference.
2. Reject non-canonical targets such as `docs/superpowers/**` and reroute the request into the stage tree.
3. Confirm the required template in `docs/99.templates/README.md`.
4. Read the matching template in `docs/99.templates/` before creating any authored stage document.
5. Use the canonical path for the selected document type.
6. Set new authored documents to `status: draft`, use `owner: platform`, and keep all required template headings.
7. Update the owning folder `README.md` in the same change if files are added, moved, or removed.
8. Ensure each newly created authored document includes `## Related Documents`.
9. Expect Claude and Codex edit hooks to warn before authored stage doc edits and run post-edit documentation template enforcement.
10. Report the template path used and validation evidence in the handoff.

## Routing Matrix

| Requested Output | Route To | Required Template |
| --- | --- | --- |
| README or folder index | `README.md`, `docs/**/README.md` | `docs/99.templates/templates/common/readme.template.md` |
| PRD | `docs/01.requirements/YYYY-MM-DD-<feature-or-system>.md` | `docs/99.templates/templates/sdlc/requirements/prd.template.md` |
| ARD | `docs/02.architecture/requirements/####-<system-or-domain>.md` | `docs/99.templates/templates/sdlc/architecture/ard.template.md` |
| ADR | `docs/02.architecture/decisions/####-<short-title>.md` | `docs/99.templates/templates/sdlc/architecture/adr.template.md` |
| Spec | `docs/03.specs/<feature-id>/spec.md` | `docs/99.templates/templates/sdlc/specs/spec.template.md` |
| Plan | `docs/04.execution/plans/YYYY-MM-DD-<feature>.md` | `docs/99.templates/templates/sdlc/execution/plan.template.md` |
| Task record | `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md` | `docs/99.templates/templates/sdlc/execution/task.template.md` |
| API spec | `docs/03.specs/<feature-id>/api-spec.md` | `docs/99.templates/templates/sdlc/specs/api-spec.template.md` |
| Agent design | `docs/03.specs/<feature-id>/agent-design.md` | `docs/99.templates/templates/sdlc/specs/agent-design.template.md` |
| Data model | `docs/03.specs/<feature-id>/data-model.md` | `docs/99.templates/templates/sdlc/specs/data-model.template.md` |
| Test design | `docs/03.specs/<feature-id>/tests.md` | `docs/99.templates/templates/sdlc/specs/tests.template.md` |
| Guide | `docs/05.operations/guides/<doc>.md` | `docs/99.templates/templates/sdlc/operations/guide.template.md` |
| Operations policy | `docs/05.operations/policies/<doc>.md` | `docs/99.templates/templates/sdlc/operations/policy.template.md` |
| Runbook | `docs/05.operations/runbooks/<doc>.md` | `docs/99.templates/templates/sdlc/operations/runbook.template.md` |
| Incident record | `docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident>.md` | `docs/99.templates/templates/sdlc/operations/incident.template.md` |
| Postmortem | `docs/05.operations/incidents/postmortems/YYYY/YYYY-MM-DD-<incident>.md` | `docs/99.templates/templates/sdlc/operations/postmortem.template.md` |
| Durable agent/reference doc | `docs/90.references/<category>/<topic>.md` | `docs/99.templates/templates/common/reference.template.md` |

## Named Skill Routing

### `agent-memory-systems`

- Feature-specific memory strategy goes to `docs/03.specs/<feature-id>/agent-design.md`.
- Durable reusable memory concepts go to `docs/90.references/agents/<topic>.md`.

### `agent-md-refactor`

- Keep root gateway files thin.
- Move detailed rules into `docs/00.agent-governance/**` or local `.claude/skills/**`.
- Any new authored document must follow the canonical stage tree.

### `claude-md-improver`

- Keep root `CLAUDE.md` as a provider shim.
- Route runtime-specific additions to `.claude/CLAUDE.md`, governance policy to `docs/00.agent-governance/**`, and durable references to `docs/90.references/**` as appropriate.
- Block suggestions that create `docs/superpowers/specs`, `docs/superpowers/plans`, or similar parallel paths.

## Constraints

- Do not modify global skills under `/home/hy/.agents/skills/*` for this workflow.
- Do not create `docs/superpowers/**`.
- Keep governance docs in English.
- Keep human-facing `README.md` files in Korean.
- Keep `AGENTS.md` and `CLAUDE.md` thin and non-duplicative.

## Expected Outputs

- A canonical target path for the document request
- The matching template to use
- README sync requirements for any folder-level change
- `status: draft` for new authored documents
- Confirmation that required template headings and `## Related Documents` are present
- Validation evidence for the authored document
- Rerouting guidance when the requested path is not valid in this repository

## Failure Handling

- If the request does not map cleanly to one stage, stop and classify it before writing.
- If content mixes durable reference and feature design, split the durable parts into `docs/90.references/**` and the feature contract into `docs/03.specs/**`.
- If governance and authored-stage content are mixed together, keep policy in `docs/00.agent-governance/**` and route authored content to the correct stage folder.
