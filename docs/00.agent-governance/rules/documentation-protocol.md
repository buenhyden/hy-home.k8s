# Documentation Protocol (March 2026)

This protocol defines how governance references authored docs and how language boundaries are applied.

## Core Requirements

- Governance policy belongs in `docs/00.agent-governance/`.
- Product and delivery truth remains in `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, `docs/98.archive`, and `docs/99.templates`.
- Governance files must reference authored docs and must not duplicate stage content.
- Folder responsibilities are defined by `stage-authoring-matrix.md`; exact
  path-to-template routing is owned by
  `docs/99.templates/support/template-routing.md` and summarized by
  `docs/99.templates/README.md`. Provider adapters must point to those owners
  instead of carrying their own template maps.

## Document Output Routing

- Generated documents must use the canonical stage tree only.
- Use [document-stage-routing.md](./document-stage-routing.md) for path selection and skill-specific rerouting rules.
- Do not create parallel authored trees such as `docs/superpowers/**`.
- Do not place API contract docs under `docs/api/**`; keep them under `docs/03.specs/<feature-id>/`.

## Template Enforcement Policy

- All authored documents under `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, `docs/90.references/`, and `docs/98.archive/` must start from the matching template listed in `docs/99.templates/support/template-routing.md`.
- The canonical template map is the Template Routing Contract. If Stage 00
  summaries, provider adapters, hooks, or validators diverge from that support
  contract and `docs/99.templates/README.md`, fix the route owners first.
- README files must use `docs/99.templates/templates/common/readme.template.md`.
- README files must keep `## Link Basis` and `## Related Documents`; deprecated related-document headings are incomplete.
- PRD, ARD, ADR, Spec, Plan, Task, Guide, Operations Policy, Runbook, Incident, Postmortem, Reference, and Archive Tombstone documents must use their stage-specific templates from `docs/99.templates/`.
- `docs/03.specs/<feature-id>/api-spec.md`, `agent-design.md`, `data-model.md`, and `tests.md` must use their matching helper templates.
- Every non-README authored Markdown file under stage roots must match exactly one structural template mapping in `docs/99.templates/README.md` and `scripts/validate-repo-quality-gates.sh`; an uncovered path is incomplete.
- New authored documents must keep `status: draft` until a human promotes the lifecycle state.
- The canonical `owner` value for all authored documents in this repository is `platform`. Do not use deprecated team-owner values.
- Authored documents must keep the required template headings and must include `## Related Documents`.
- Agents must report the template path used and the validation evidence before handoff.
- Generated exceptions, such as `docs/90.references/llm-wiki/wiki-index.md`, must keep their generator contract and must not be edited by hand.
- `docs/98.archive` documents must be metadata-only Tombstones and must not preserve old full bodies.
- `docs/99.templates/templates/common/reference.template.md` must not own archive policy or contain archive wording; archive policy belongs in routing/governance docs and `archive-tombstone.template.md`.
- Provider event wiring must surface Template-First guidance before authored
  stage doc edits where the runtime supports it: Claude uses
  `.claude/settings.json`, Codex uses `.codex/hooks.json` context/validation
  wiring, and Gemini uses `.agents/hooks.json` behavioral wiring. Explicit
  validation commands remain required before handoff.

## Language Boundary Rules

- `docs/00.agent-governance/*`: English only.
- Human-facing README files: Korean (`README.md`, `docs/README.md`, and stage READMEs).
- Agent execution control documents under governance must be written in English.
- Technical specifications under `docs/03.specs/**/spec.md` must be written in
  English. Feature-local API, agent, data, and test contracts under
  `docs/03.specs/**` should also prefer English because they are implementation
  contracts.
- Implementation plans under `docs/04.execution/plans/*.md` must be written in
  English.
- Task records under `docs/04.execution/tasks/*.md` must be written in English
  because they are execution evidence, validation records, and agent handoff
  artifacts. The folder README may remain Korean as a human-facing index.
- Human-facing authored documents should prefer Korean for reader-facing
  overview, audience, and operational explanation. Sections whose explicit
  audience is an AI agent, including headings such as `AI Agent Requirements`,
  `Agent Execution Notes`, `Agent Harness Requirements`, or tool/prompt
  contracts, should be written in English even inside otherwise Korean
  documents.
- Operations documents under `docs/05.operations/**` may use Korean for
  human-facing guidance, policies, runbooks, and incident records, while any
  AI-agent execution notes, prompt/tool contracts, or automation guardrails
  inside those documents must remain English.
- Reference documents under `docs/90.references/**` may use Korean for
  human-facing overview and explanatory lookup context. `Reference Type`,
  `Authority Boundary`, `Sources`, `Review and Freshness`, generated-index
  contracts, version support boundaries, and AI-agent routing notes should
  remain English-first because they are consumed as factual contracts.

## Drift Garbage Collection

- Treat code drift, document drift, and structure drift as harness defects, not
  agent blame. When a repeated or material error is found, update the smallest
  durable harness surface that would have prevented it: rule, prompt/skill,
  hook, validator, template, README index, or memory entry.
- Code drift is closed by aligning implementation, examples, generated indexes,
  and validation scripts with the current repo-backed contract.
- Document drift is closed by updating, consolidating, or archiving active docs;
  do not keep conflicting current contracts in active stages.
- Structure drift is closed by restoring canonical stage paths, provider mirror
  parity, shared skill/workflow/output-style ownership, and template coverage.
- Temporary files, debug-only code, unused imports, and files named with
  `temp_`, `_new`, `_old`, or `_backup` are cleanup failures unless a
  repository policy explicitly permits them.
- Record durable drift lessons in `memory/progress.md` when recurrence risk
  exists, and add regression-gate coverage when the failure can be checked
  deterministically.

## Traceability Rules

- Every governance change should keep clear links to the canonical docs taxonomy (`01.requirements`, `02.architecture`, `03.specs`, `04.execution`, `05.operations`, `90.references`, `98.archive`, `99.templates`).
- Active documents must link old archived content only through `docs/98.archive/README.md`; direct links to Tombstones belong only in the archive index.
- Postmortems belong at `docs/05.operations/incidents/YYYY/INC-###-<title>/postmortem.md`, not a separate top-level docs stage.
- Persona and scope instructions must state which stage folders are authoritative.
- Stage expectations must map to [stage-authoring-matrix.md](stage-authoring-matrix.md).
- Repo-changing agent work must append progress and reusable memory to `docs/00.agent-governance/memory/progress.md` using `docs/99.templates/templates/common/progress.template.md`.
- `docs/00.agent-governance/memory/progress.md` is the canonical progress ledger and the only tracked `progress.md`. Standalone memory files are allowed, but the filename `progress.md` is forbidden outside the canonical path.
- Agent eval completion evidence belongs in the relevant Stage 04 Task record and the canonical progress ledger. Eval PASS must come from deterministic command evidence or recorded human/operator approval, not inferred file presence or unverified live runtime readiness.
- Standalone files under `docs/00.agent-governance/memory/` must use `docs/99.templates/templates/common/memory.template.md` and must be accompanied by a related `progress.md` entry in the same change.

## Template Link Policy

- Actual Markdown links inside templates must resolve relative to the template file location.
- Placeholder, optional, or target-relative examples must be written as code literals or fenced snippets and calculated from the final authored document location.
- Optional or project-specific files that may not exist (for example, `ARCHITECTURE.md`) should be shown as code literals, not Markdown links.
- Placeholder paths should be expressed as placeholders (`{path}`) or fenced snippets to avoid false-positive broken-link checks.

## Checklist Policy

- Run `preflight-checklist.md` before editing.
- Run `postflight-checklist.md` before finalization.

## Docs 3 Rules (HALT)

**R1 — Template-First:** Read `docs/99.templates/README.md` and `docs/99.templates/support/template-routing.md`, then read the matching template in `docs/99.templates/templates/` before creating any document. Confirm the target path has exactly one structural template mapping, fill all required fields and required template headings, and set `status: draft`. k8s-specific triggers: new namespace → ARD required; RBAC change → ADR required; production change → operations policy first.

**R2 — README Sync:** Any folder-level change (add, move, remove files) **or content modification to an existing document** requires the folder's `README.md` to be reviewed and updated in the same PR if its summary, link table, or description is now stale. Work is **BLOCKED** until the README reflects the current state and keeps `## Link Basis` plus `## Related Documents`.

**R3 — Related Documents:** Every authored document must include a `## Related Documents` section with upstream links. A document without this section is **INCOMPLETE**.

**R4 — Memory Ledger Coupling:** Repo-changing work updates the canonical progress ledger at `docs/00.agent-governance/memory/progress.md`. It is the only tracked `progress.md`; standalone memory files use `memory.template.md` and link back to their related progress entry.

**R5 — Archive Separation:** Current implementation conflicts cannot be hidden with historical or superseded markers in active docs. Move the old document to `docs/98.archive` as a Tombstone and link it from the archive index only.

**HALT conditions:** Missing template read → HALT. README not updated → HALT. README Link Basis absent → HALT. Related Documents section absent → HALT. Memory entry without progress ledger update → HALT. Active doc retaining stale implementation contract → HALT.
