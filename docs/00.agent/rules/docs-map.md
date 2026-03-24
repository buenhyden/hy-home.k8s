---
layer: "meta"
---
# Docs Map

- `docs/`: durable project knowledge only, never runtime code or scripts
- `docs/prd/`: product requirements, personas, metrics, scope; use `layer:` metadata
- `docs/specs/`: exact implementation specs and API details; use `layer:` metadata
- `docs/plans/`: execution roadmaps; do not let plans replace approved specs
- `docs/adr/`: architecture decisions and consequences; use `layer:` metadata
- `docs/ard/`: architecture reference structure and diagrams; use `layer:` metadata
- `docs/runbooks/`: operator procedures and rollback; use `layer:` metadata
- `docs/incidents/`: incident reports and postmortems; use `templates/incident-template.md`
- `docs/operations/`: strategic operations blueprints only, not runbook procedures

All documentation categories are now flattened. Files must include `layer:` metadata in frontmatter to distinguish between `infra`, `gitops`, etc.
Nearest scoped `AGENTS.md`, `GEMINI.md`, and `CLAUDE.md` files govern local work inside each subtree.
