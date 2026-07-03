# Antigravity Workspace Rules

This file defines Gemini-specific workspace rules for `hy-home.k8s` that supplement the global Stage 00 agent governance.

## 1. Template-First Enforcement

- All architecture, requirement, spec, and operations documents must follow the
  route in `docs/99.templates/support/template-routing.md` and start from the
  matching template under `docs/99.templates/templates/`.
- Do not create ad-hoc markdown structures. If a template exists, use it.
- **Routing**: use `docs/00.agent-governance/rules/document-stage-routing.md`
  for stage selection and `docs/99.templates/support/template-routing.md` for
  the exact target-pattern/template map.

## 2. GitOps Immutable Principle

- Do not modify the live k3d cluster directly without explicit user permission for emergency break-glass procedures.
- All cluster mutations must be recorded as manifest updates in `gitops/` or `infrastructure/`.
- Validate manifests locally (via `scripts/validate-repo-quality-gates.sh` or equivalent pre-commit hooks) before considering a task complete.

## 3. Tool and Validation Priority

- Always define validation evidence before executing edits.
- Use `QA/CI/CD Workflow` (`.agents/workflows/qa-cicd-workflow.md`) to verify changes.
- Prioritize reading `graphify-out/GRAPH_REPORT.md` before performing deep codebase searches if the file exists.

## 4. Reasoning & Model Policy

- For complex planning or code refactoring, leverage `Gemini 3.1 Pro`.
- For simple formatting, documentation, or task breakdown, leverage `Gemini 3.5 Flash`.
- Keep reasoning loops explicit: state assumptions, explain the plan, ask for confirmation if ambiguous, and execute iteratively.
