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
| README or folder index | `README.md`, `docs/**/README.md` | `docs/99.templates/readme.template.md` | Use for repository, stage, and nested folder entrypoints. |
| Product requirement | `docs/01.requirements/YYYY-MM-DD-<feature-or-system>.md` | `docs/99.templates/prd.template.md` | Use for product intent, scope, success criteria, and acceptance criteria. |
| Architecture requirement | `docs/02.architecture/requirements/####-<system-or-domain>.md` | `docs/99.templates/ard.template.md` | Use for architecture requirements and quality attributes. |
| Architecture decision | `docs/02.architecture/decisions/####-<short-title>.md` | `docs/99.templates/adr.template.md` | Use for decision context, selected option, alternatives, and consequences. |
| Technical specification | `docs/03.specs/<feature-id>/spec.md` | `docs/99.templates/spec.template.md` | Use for implementation contracts and detailed design. |
| Implementation plan | `docs/04.execution/plans/YYYY-MM-DD-<feature>.md` | `docs/99.templates/plan.template.md` | Use for execution order, risks, gates, and rollout. |
| Task record | `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md` | `docs/99.templates/task.template.md` | Use for implementation status, validation evidence, and handoff. |
| API contract | `docs/03.specs/<feature-id>/api-spec.md` | `docs/99.templates/api-spec.template.md` | Never route to `docs/api/**`. |
| Agent design | `docs/03.specs/<feature-id>/agent-design.md` | `docs/99.templates/agent-design.template.md` | Use for role/tool/policy/memory design tied to one feature. |
| Data model | `docs/03.specs/<feature-id>/data-model.md` | `docs/99.templates/data-model.template.md` | Use for schema and storage design tied to one feature. |
| Test design | `docs/03.specs/<feature-id>/tests.md` | `docs/99.templates/tests.template.md` | Use for verification strategy tied to one feature. |
| User or operator guide | `docs/05.operations/guides/<doc>.md` | `docs/99.templates/guide.template.md` | Use after the relevant spec is stable. |
| Operations policy | `docs/05.operations/policies/<doc>.md` | `docs/99.templates/operation.template.md` | Required for release and operational controls. |
| Runbook | `docs/05.operations/runbooks/<doc>.md` | `docs/99.templates/runbook.template.md` | Use for executable operational procedures. |
| Incident record | `docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident>.md` | `docs/99.templates/incident.template.md` | Use for facts, timelines, mitigations, and active incident evidence. |
| Postmortem | `docs/05.operations/incidents/YYYY-MM-DD-<incident>-postmortem.md` | `docs/99.templates/postmortem.template.md` | Use for RCA, prevention actions, and post-incident learning. |
| Durable reference | `docs/90.references/<category>/<topic>.md` | `docs/99.templates/reference.template.md` | Use for slow-moving concepts, glossaries, standards, and reusable agent knowledge. |
| LLM Wiki generated index | `docs/90.references/llm-wiki/wiki-index.md` | `docs/99.templates/reference.template.md` through `scripts/generate-llm-wiki-index.sh` | Use only as a generated canonical-owner link map. |
| Governance memory | `docs/00.agent-governance/memory/<topic>.md` | `docs/99.templates/memory.template.md` | Use for reusable agent governance lessons. |

## Legacy Path Migration Map

The repository uses the reduced canonical docs model below. Do not recreate the
old top-level 13-folder model.

| Legacy Path | Canonical Path |
| --- | --- |
| `docs/01.prd/` | `docs/01.requirements/` |
| `docs/02.ard/` | `docs/02.architecture/requirements/` |
| `docs/03.adr/` | `docs/02.architecture/decisions/` |
| `docs/04.specs/` | `docs/03.specs/` |
| `docs/05.plans/` | `docs/04.execution/plans/` |
| `docs/06.tasks/` | `docs/04.execution/tasks/` |
| `docs/07.guides/` | `docs/05.operations/guides/` |
| `docs/08.operations/` | `docs/05.operations/policies/` |
| `docs/09.runbooks/` | `docs/05.operations/runbooks/` |
| `docs/10.incidents/` | `docs/05.operations/incidents/` |
| `docs/00.agent-governance/` | `docs/00.agent-governance/` |
| `docs/90.references/` | `docs/90.references/` |
| `docs/99.templates/` | `docs/99.templates/` |

## Prohibited Paths

The following paths are not valid authored-document targets in this repository:

- `docs/superpowers/**`
- `docs/api/**`
- `docs/01.prd/**`
- `docs/02.ard/**`
- `docs/03.adr/**`
- `docs/04.specs/**`
- `docs/05.plans/**`
- `docs/06.tasks/**`
- `docs/07.guides/**`
- `docs/08.operations/**`
- `docs/09.runbooks/**`
- `docs/10.incidents/**`
- Legacy postmortem top-level trees
- Legacy learning top-level trees
- Ad hoc top-level trees for plans, specs, or references outside the canonical stage folders

When a skill suggests one of these paths, reroute the output into the canonical stage location instead of creating the proposed path.

## Routing Decision Rules

### Feature-Bound vs Durable Knowledge

- If the content is tied to one feature, service, or rollout stream, route it to `docs/03.specs/` or `docs/04.execution/plans/`.
- If the content is long-lived reusable knowledge, route it to `docs/90.references/`.
- If the content changes governance or agent execution policy, route it to `docs/00.agent-governance/`.

### Operational Knowledge Split

- Use `docs/05.operations/guides/` when the reader needs stable user, developer, or operator guidance.
- Use `docs/05.operations/policies/` when the content defines a reusable policy, boundary, or standard.
- Use `docs/05.operations/runbooks/` when the content must be executable in order, including verification, rollback, or recovery steps.
- Use `docs/90.references/` when the content is a durable reference, glossary, external standard summary, or dated version snapshot.
- Do not duplicate the same operational content across guide, policy, and runbook stages. Link to the canonical owner instead.

### Named Skill Handling

#### `agent-memory-systems`

- Feature-specific memory or context strategy belongs in `docs/03.specs/<feature-id>/agent-design.md`.
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

- Read `docs/99.templates/README.md`, then read the matching template under `docs/99.templates/` before creating any stage document.
- Confirm the target path matches exactly one structural template mapping before authoring; uncovered stage paths are invalid even when they sit under an allowed docs folder.
- New authored documents must set `status: draft` until a human promotes the lifecycle state.
- The required template headings are part of the document contract and must not be omitted.
- New or moved authored documents must trigger a same-change update to the owning folder `README.md`.
- Every newly created authored document must include `## Related Documents`.
- Agents must return the template path used and validation evidence in the handoff.
- Claude and Codex edit hooks must warn on authored stage doc paths and run post-edit template enforcement through the repository quality gate.
- Governance docs remain English-only; human-facing READMEs remain Korean.
- Root gateway files must stay thin and should link to rule docs instead of duplicating rule text.

## Related Documents

- [Documentation Protocol](./documentation-protocol.md)
- [Stage Authoring Matrix](./stage-authoring-matrix.md)
- [Templates README](../../99.templates/README.md)
