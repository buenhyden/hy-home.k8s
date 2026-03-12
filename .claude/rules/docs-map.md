# Docs Map

- `docs/`: durable project knowledge only, never runtime code or scripts
- `docs/prd/`: product requirements, personas, metrics, scope; use `templates/prd-template.md`
- `docs/specs/`: exact implementation specs and API details; use `templates/spec-template.md`, `templates/plan-template.md`, `templates/api-spec-template.md`
- `docs/plans/`: execution roadmaps; do not let plans replace approved specs
- `docs/adr/`: architecture decisions and consequences; use `templates/adr-template.md`
- `docs/ard/`: architecture reference structure and diagrams; use `templates/ard-template.md`
- `docs/runbooks/`: operator procedures and rollback; use `templates/runbook-template.md`
- `docs/incidents/`: incident reports and postmortems; use `templates/incident-template.md` or `templates/postmortem-template.md`
- `docs/operations/`: strategic operations blueprints only, not runbook step-by-step procedures

Nearest scoped `AGENTS.md`, `GEMINI.md`, and `CLAUDE.md` files govern local work inside each subtree.
