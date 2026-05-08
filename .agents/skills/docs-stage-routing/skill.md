---
name: docs-stage-routing
description: Route generated documents into the canonical docs stage tree for this repository and block parallel hierarchies such as docs/superpowers.
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
- "AGENTS.md improver"

## Workflow Steps

1. Classify the requested output as governance, feature-bound design, execution plan, operational doc, or durable reference.
2. Reject non-canonical targets such as `docs/superpowers/**` and reroute the request into the stage tree.
3. Read the matching template in `docs/99.templates/` before creating any authored stage document.
4. Use the canonical path for the selected document type.
5. Update the owning folder `README.md` in the same change if files are added, moved, or removed.
6. Ensure each newly created authored document includes `## Related Documents`.

## Routing Matrix

| Requested Output | Route To |
| --- | --- |
| Spec | `docs/04.specs/<feature-id>/spec.md` |
| Plan | `docs/05.plans/YYYY-MM-DD-<feature>.md` |
| API spec | `docs/04.specs/<feature-id>/api-spec.md` |
| Agent design | `docs/04.specs/<feature-id>/agent-design.md` |
| Data model | `docs/04.specs/<feature-id>/data-model.md` |
| Test design | `docs/04.specs/<feature-id>/tests.md` |
| Guide | `docs/07.guides/<doc>.md` |
| Operations policy | `docs/08.operations/<doc>.md` |
| Runbook | `docs/09.runbooks/<doc>.md` |
| Durable agent/reference doc | `docs/90.references/<category>/<topic>.md` |

## Named Skill Routing

### `agent-memory-systems`

- Feature-specific memory strategy goes to `docs/04.specs/<feature-id>/agent-design.md`.
- Durable reusable memory concepts go to `docs/90.references/agents/<topic>.md`.

### `agent-md-refactor`

- Keep root gateway files thin.
- Move detailed rules into `docs/00.agent-governance/**` or local `.Codex/skills/**`.
- Any new authored document must follow the canonical stage tree.

### `Codex-md-improver`

- Keep root `AGENTS.md` as a provider shim.
- Route runtime-specific additions to `.Codex/AGENTS.md`, governance policy to `docs/00.agent-governance/**`, and durable references to `docs/90.references/**` as appropriate.
- Block suggestions that create `docs/superpowers/specs`, `docs/superpowers/plans`, or similar parallel paths.

## Constraints

- Do not modify global skills under `/home/hy/.agents/skills/*` for this workflow.
- Do not create `docs/superpowers/**`.
- Keep governance docs in English.
- Keep human-facing `README.md` files in Korean.
- Keep `AGENTS.md` and `AGENTS.md` thin and non-duplicative.

## Expected Outputs

- A canonical target path for the document request
- The matching template to use
- README sync requirements for any folder-level change
- Rerouting guidance when the requested path is not valid in this repository

## Failure Handling

- If the request does not map cleanly to one stage, stop and classify it before writing.
- If content mixes durable reference and feature design, split the durable parts into `docs/90.references/**` and the feature contract into `docs/04.specs/**`.
- If governance and authored-stage content are mixed together, keep policy in `docs/00.agent-governance/**` and route authored content to the correct stage folder.
