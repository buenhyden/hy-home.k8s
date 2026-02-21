# GitHub Configuration Hub

This directory is the home for GitHub-specific templates, Actions workflows, and automated checks.

## Content Mapping

- `workflows/` — CI/CD pipelines triggered on PRs, merges, or schedules.
- `gates/` — Custom shell scripts or policies (like coverage or security checks) used within workflows to enforce "Quality Gates" before merging or deployment.
- `ISSUE_TEMPLATE/` — Forms enforcing structured reporting for bug tracking or feature requests.
- `PULL_REQUEST_TEMPLATE.md` — Enforces PR traceability back to the `/specs` directory.
- `SECURITY.md` — The security policy outlining vulnerability reporting instructions.

## AI Interaction

The DevOps Agent manages the `.github/workflows/` when changes to deployment pipelines or test runners are approved in the `runbooks/`.
All configuration here is strictly bound by the following Project Standard Rules:

- CI/CD Pipelines: `.agent/rules/0330-infrastructure-cicd.md`
- Git Workflows & PR Templates: `.agent/rules/0401-git-workflow-standard.md`

### Multi-Language CI Adaptation

By default, the `verify-application.yml` is scaffolded for **Node.js/NPM**. If the project's `ARCHITECTURE.md` establishes a different stack for backend (`server/`) or native (`app/`) layers (e.g., Python, Go, Rust, Java), the DevOps Agent **MUST** modify the workflow's `Setup Environment` steps to provision the correct compiler/interpreter via the appropriate GitHub Actions before validating code.
