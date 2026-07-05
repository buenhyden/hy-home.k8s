# Document Stage Routing Rules (April 2026)

Route all generated documentation into the existing `docs/` stage taxonomy.

## Purpose

- Prevent parallel documentation trees such as `docs/superpowers/**`.
- Keep generated outputs aligned with the stage authoring matrix.
- Ensure document-writing skills produce repository-native paths.

## Core Routing Policy

Use the existing stage structure only. The exact current route map is owned by
the [Template Routing Contract](../../99.templates/support/template-routing.md)
and summarized in [Templates README](../../99.templates/README.md). This Stage
00 rule owns the decision policy for choosing the right stage; it must not carry
a competing copy of the full template route table.

README entrypoints use
`docs/99.templates/templates/common/readme.template.md`; exact README route
variants remain in the support route map.
Operations policy documents use `policy.template.md` through the support route
map.

`.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and
`.github/SECURITY.md` are GitHub-native control Markdown files. They remain
frontmatter-free and are not structural stage documents; durable policy must
route back to Stage 00, Stage 05, scripts, or workflow owners.

Cloud Example Snapshot material under `examples/aws/docs/**` and
`examples/azure/docs/**` is not an active SDLC route target for wholesale
frontmatter migration. Future provider-refresh work must promote any scoped
change through an approved spec and support contract update.

## Lifecycle Pre-Edit Contract

Before editing or creating lifecycle documents, agents must align with the
Stage 99 owners instead of copying full governance bodies into README files.

| Document Family | Lifecycle Transition |
| --- | --- |
| PRD | `draft -> active -> done | archived` |
| ARD/ADR | `draft -> active -> accepted | archived` |
| Spec | `draft -> active -> done | archived` |
| Plan/Task | `draft -> active -> done | archived` |
| Operations | `draft -> active -> accepted | archived` |
| Archive Tombstone | `archived` only |

- Stage 01 PRDs use `docs/01.requirements/<###-Numbering>-<feature-or-system>.md`.
- Stage 03 specs use `docs/03.specs/<###-Numbering>-<feature-id>/spec.md`.
- Stage 04 plans and tasks stay date-based execution records.
- README files route readers to lifecycle contract owners instead of carrying
  full governance bodies.
- Handoff links must connect PRD, architecture, spec, plan, task, operations,
  and archive records through `## Related Documents` or equivalent route-owned
  link sections.
- Active-surface duplicate rule: stages 01 through 04 must not keep multiple
  active documents that own the same role, purpose, and feature lineage.

| Document Intent | Canonical Stage | Route Owner | Notes |
| --- | --- | --- | --- |
| README or folder index | Repository or folder-local `README.md` | Template Routing Contract | Use for repository, stage, and nested folder entrypoints. |
| Product requirement | `docs/01.requirements/` | Template Routing Contract | Use for product intent, scope, success criteria, and acceptance criteria. |
| Architecture requirement | `docs/02.architecture/requirements/` | Template Routing Contract | Use for architecture requirements and quality attributes. |
| Architecture decision | `docs/02.architecture/decisions/` | Template Routing Contract | Use for decision context, selected option, alternatives, and consequences. |
| Technical specification and helper contracts | `docs/03.specs/` | Template Routing Contract | Use for implementation contracts, feature-local API, agent, data, test, OpenAPI, GraphQL, and protobuf contracts. |
| Implementation plan | `docs/04.execution/plans/` | Template Routing Contract | Use for execution order, risks, gates, and rollout. |
| Task record | `docs/04.execution/tasks/` | Template Routing Contract | Use for implementation status, validation evidence, and handoff. |
| User or operator guide | `docs/05.operations/guides/` | Template Routing Contract | Use after the relevant spec is stable. |
| Operations policy | `docs/05.operations/policies/` | Template Routing Contract | Required for release and operational controls. |
| Runbook | `docs/05.operations/runbooks/` | Template Routing Contract | Use for executable operational procedures. |
| Incident record and postmortem | `docs/05.operations/incidents/` | Template Routing Contract | Use for facts, timelines, mitigations, RCA, and post-incident learning. |
| Durable reference | `docs/90.references/` | Template Routing Contract | Use for slow-moving concepts, glossaries, standards, and reusable agent knowledge. |
| Generated LLM Wiki index | `docs/90.references/llm-wiki/wiki-index.md` | Generator contract and Template Routing Contract | Use only as a generated canonical-owner link map. |
| Archive Tombstone | `docs/98.archive/` | Template Routing Contract | Use only for metadata-only Tombstones of old docs moved out of active stages. |
| Governance memory | `docs/00.agent-governance/memory/` | Template Routing Contract | Use for reusable agent governance lessons and repo-changing progress entries. |

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
| `docs/98.archive/` | `docs/98.archive/` |
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

### Archive Routing

- Use `docs/98.archive/` only when an old active-stage document under `docs/01.requirements` through `docs/05.operations` conflicts with current repo-backed implementation, is deprecated-only, or is superseded-only.
- Mirror the original docs subpath under `docs/98.archive/<original-docs-subpath>`.
- For `docs/05.operations`, preserve the operations bucket mirror under `docs/98.archive/05.operations/{guides,policies,runbooks,incidents}`.
- Replace the moved document body with a Tombstone created from `docs/99.templates/templates/common/archive-tombstone.template.md`; do not preserve the old body text.
- Tombstones must preserve archive traceability metadata defined by
  `docs/99.templates/support/frontmatter-schema.md` and
  `docs/99.templates/templates/common/archive-tombstone.template.md`.
- Active docs may link archive content only through `docs/98.archive/README.md`.
- Current replacement coverage must exist before moving a document that owned still-current scope.

### Named Skill Handling

#### `agent-memory-systems`

- Feature-specific memory or context strategy belongs in `docs/03.specs/<###-Numbering>-<feature-id>/agent-design.md`.
- Reusable memory-system concepts belong in `docs/90.references/data/<topic>.md`.

#### `agent-md-refactor`

- `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` must remain thin gateways.
- Detailed execution rules belong in `docs/00.agent-governance/**` or shared `.agents/skills/**`.
- Any new authored doc proposed by this skill must use the canonical stage path and template.

#### `claude-md-improver`

- Root `CLAUDE.md` remains a provider shim.
- Project-specific runtime guidance belongs in `.claude/CLAUDE.md`, `docs/00.agent-governance/**`, or shared `.agents/skills/**`, depending on ownership.
- Suggestions to create `docs/superpowers/specs`, `docs/superpowers/plans`, or similar parallel trees must be rejected and rerouted.

## Authoring Guardrails

- Read `docs/99.templates/support/template-routing.md` to select the exact
  target-pattern/template route, use `docs/99.templates/README.md` only as the
  synchronized index summary, then read the matching template under
  `docs/99.templates/templates/` before creating any stage document.
- Confirm the target path matches exactly one structural template mapping before authoring; uncovered stage paths are invalid even when they sit under an allowed docs folder.
- New authored documents must set `status: draft` until a human promotes the lifecycle state.
- The required template headings are part of the document contract and must not be omitted.
- Required heading enforcement is derived from literal second-level headings
  in the matched template. Headings containing placeholders or marked optional
  are guidance, not required coverage.
- New or moved authored documents must trigger a same-change update to the owning folder `README.md`.
- Every newly created authored document must include `## Related Documents`.
- Old active-stage docs cannot remain current merely by adding historical, superseded, or current-contract notes when their body conflicts with the implementation.
- Agents must return the template path used and validation evidence in the handoff.
- Provider event wiring must warn on authored stage doc paths where supported
  and run post-edit template enforcement through the repository quality gate.
  Claude uses native settings; Codex and Gemini hook JSON remain
  context/validation wiring and do not replace explicit validation commands.
- Governance docs remain English-only; human-facing READMEs remain Korean.
- Root gateway files must stay thin and should link to rule docs instead of duplicating rule text.

## Related Documents

- [Documentation Protocol](./documentation-protocol.md)
- [Stage Authoring Matrix](./stage-authoring-matrix.md)
- [Templates README](../../99.templates/README.md)
