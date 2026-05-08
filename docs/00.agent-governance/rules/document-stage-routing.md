# Document Stage Routing Rules (April 2026)

Route all generated documentation into the existing `docs/` stage taxonomy.

## Purpose

- Prevent parallel documentation trees such as `docs/superpowers/**`.
- Keep generated outputs aligned with the stage authoring matrix.
- Ensure document-writing skills produce repository-native paths.

## Core Routing Policy

Use the existing stage structure only.

| Document Intent | Canonical Path | Required Template | Notes |
| --- | --- | --- | --- |
| Technical specification | `docs/04.specs/<feature-id>/spec.md` | `docs/99.templates/spec.template.md` | Use for implementation contracts and detailed design. |
| Implementation plan | `docs/05.plans/YYYY-MM-DD-<feature>.md` | `docs/99.templates/plan.template.md` | Use for execution order, risks, gates, and rollout. |
| API contract | `docs/04.specs/<feature-id>/api-spec.md` | `docs/99.templates/api-spec.template.md` | Never route to `docs/api/**`. |
| Agent design | `docs/04.specs/<feature-id>/agent-design.md` | `docs/99.templates/agent-design.template.md` | Use for role/tool/policy/memory design tied to one feature. |
| Data model | `docs/04.specs/<feature-id>/data-model.md` | `docs/99.templates/data-model.template.md` | Use for schema and storage design tied to one feature. |
| Test design | `docs/04.specs/<feature-id>/tests.md` | `docs/99.templates/tests.template.md` | Use for verification strategy tied to one feature. |
| User or operator guide | `docs/07.guides/<doc>.md` | `docs/99.templates/guide.template.md` | Use after the relevant spec is stable. |
| Operations policy | `docs/08.operations/<doc>.md` | `docs/99.templates/operation.template.md` | Required for release and operational controls. |
| Runbook | `docs/09.runbooks/<doc>.md` | `docs/99.templates/runbook.template.md` | Use for executable operational procedures. |
| Incident record | `docs/10.incidents/YYYY/YYYY-MM-DD-<incident>.md` | `docs/99.templates/incident.template.md` | Use for facts, timelines, mitigations, and active incident evidence. |
| Postmortem | `docs/10.incidents/postmortems/YYYY/YYYY-MM-DD-<incident>.md` | `docs/99.templates/postmortem.template.md` | Use for RCA, prevention actions, and post-incident learning. |
| Durable reference | `docs/90.references/<category>/<topic>.md` | `docs/99.templates/reference.template.md` | Use for slow-moving concepts, glossaries, standards, and reusable agent knowledge. |
| Governance memory | `docs/00.agent-governance/memory/<topic>.md` | `docs/99.templates/memory.template.md` | Use for reusable agent governance lessons. |

## Prohibited Paths

The following paths are not valid authored-document targets in this repository:

- `docs/superpowers/**`
- `docs/api/**`
- Legacy postmortem top-level trees
- Legacy learning top-level trees
- Ad hoc top-level trees for plans, specs, or references outside the canonical stage folders

When a skill suggests one of these paths, reroute the output into the canonical stage location instead of creating the proposed path.

## Routing Decision Rules

### Feature-Bound vs Durable Knowledge

- If the content is tied to one feature, service, or rollout stream, route it to `docs/04.specs/` or `docs/05.plans/`.
- If the content is long-lived reusable knowledge, route it to `docs/90.references/`.
- If the content changes governance or agent execution policy, route it to `docs/00.agent-governance/`.

### Named Skill Handling

#### `agent-memory-systems`

- Feature-specific memory or context strategy belongs in `docs/04.specs/<feature-id>/agent-design.md`.
- Reusable memory-system concepts belong in `docs/90.references/agents/<topic>.md`.

#### `agent-md-refactor`

- `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` must remain thin gateways.
- Detailed execution rules belong in `docs/00.agent-governance/**` or local `.claude/skills/**`.
- Any new authored doc proposed by this skill must use the canonical stage path and template.

#### `claude-md-improver`

- Root `CLAUDE.md` remains a provider shim.
- Project-specific runtime guidance belongs in `.claude/CLAUDE.md`, `docs/00.agent-governance/**`, or local `.claude/skills/**`, depending on ownership.
- Suggestions to create `docs/superpowers/specs`, `docs/superpowers/plans`, or similar parallel trees must be rejected and rerouted.

## Authoring Guardrails

- Read the matching template under `docs/99.templates/` before creating any stage document.
- New or moved authored documents must trigger a same-change update to the owning folder `README.md`.
- Every newly created authored document must include `## Related Documents`.
- Governance docs remain English-only; human-facing READMEs remain Korean.
- Root gateway files must stay thin and should link to rule docs instead of duplicating rule text.

## Related Documents

- [Documentation Protocol](./documentation-protocol.md)
- [Stage Authoring Matrix](./stage-authoring-matrix.md)
- [Templates README](../../99.templates/README.md)
