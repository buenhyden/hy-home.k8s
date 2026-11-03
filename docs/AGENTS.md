# AGENTS.md

Agent instructions for `docs/` and every stage below it. The READMEs in this
tree are for human readers; these rules are for AI agents. The repository root
gateway (`AGENTS.md` or `CLAUDE.md`) and `.agents/governance/` still apply.

## Purpose

`docs/` is the staged documentation source of truth: requirements (01),
architecture (02), change Specs (03), operations (05), references (90), the
unvalidated archive (98) and the Stage 99 registry and forms. Agents here
write or review governed documents; they do not change runtime state.

## Responsibilities and Projections

Pick the responsibility first, then read its common role and skills and the
projection for your provider.

| Work in `docs/` | Role (`.agents/roles/`) | Skills (`.agents/skills/<id>/SKILL.md`) | Claude | Codex |
| --- | --- | --- | --- | --- |
| Author or update a governed document | [doc-writer](../.agents/roles/doc-writer.md) | `docs-stage-routing`, `docs-stage-conformance`, `requirements-to-design` | `.claude/agents/doc-writer.md` | `.codex/agents/doc-writer.toml` |
| Stage 01/02 requirements and decisions | [architect](../.agents/roles/architect.md) | `requirements-to-design`, `docs-stage-routing` | `.claude/agents/architect.md` | `.codex/agents/architect.toml` |
| Stage 03 Spec, Plan and Task breakdown | [supervisor](../.agents/roles/supervisor.md) | `task-breakdown`, `execution-plan`, `risk-report` | `.claude/agents/supervisor.md` | `.codex/agents/supervisor.toml` |
| Stage 05 runbooks and incident records | [incident-responder](../.agents/roles/incident-responder.md) | `incident-postmortem`, `rca-methodology` | `.claude/agents/incident-responder.md` | `.codex/agents/incident-responder.toml` |
| Stage 90 research and evidence | [docs-researcher](../.agents/roles/docs-researcher.md) | `docs-stage-routing`, `knowledge-map` | `.claude/agents/docs-researcher.md` | `.codex/agents/docs-researcher.toml` |
| README navigation and cross-links | [wiki-curator](../.agents/roles/wiki-curator.md) | `docs-stage-conformance`, `knowledge-map` | `.claude/agents/wiki-curator.md` | `.codex/agents/wiki-curator.toml` |

Claude reads each skill through `.claude/skills/<id>`, a link to the common
skill. A documentation change request follows the
[doc-update prompt](../.agents/prompts/doc-update.md), exposed as
`.claude/commands/doc-update.md`. Native loading and permission limits are in
[`.claude/provider.md`](../.claude/provider.md) and
[`.codex/provider.md`](../.codex/provider.md).

## Rules

1. Follow the [work lifecycle](../.agents/workflows/work-lifecycle.md),
   [document authoring](../.agents/governance/document-authoring.md) and
   [document lifecycle](../.agents/governance/document-lifecycle.md) policies.
2. Choose the owning stage and profile from `docs/99.templates/registry.json`
   and start from the matching form in `docs/99.templates/templates/`.
3. Write agent-executable sections such as `AI Agent Requirements` and
   `Agent Execution Notes` in English. Human-facing prose follows the
   document language contract of its profile.
4. Keep READMEs human-facing. Put agent rules for a folder in its
   `AGENTS.md`, never in a README.
5. Treat `docs/98.archive/` as unvalidated history. Never use it as current
   authority or design input; link the current owner instead.
6. Do not rewrite completed Task evidence to satisfy a later form.
7. In Stage 05, by default limit agent work to Git file edits, review,
   ArgoCD reconciliation planning and evidence organization. A command
   boundary marker in an operations document never grants execution
   authority.
8. After a change, run the strict document checks:
   `python3 scripts/validate-document-contract-registry.py --root . --mode strict`,
   `python3 scripts/validate-markdown-profiles.py --root . --mode strict`,
   `python3 scripts/validate-links-and-owners.py --root . --mode strict` and
   `python3 scripts/validate-document-lifecycle.py --root . --mode strict`.
