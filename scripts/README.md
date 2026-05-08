# Utilities & Automation Scripts (`scripts/`)

This directory is reserved for repository maintenance, static validation, and automation helpers.

## 1. Necessity and Purpose

This folder is necessary to encapsulate repository checks that support the k3d/GitOps workflow.

- Separation of Concerns: It keeps static repository validation separate from GitOps manifests (`gitops/`) and live runtime checks (`infrastructure/tests/`).
- Consistent Execution: It provides small, repeatable checks for manifest syntax, GitOps structure, and plaintext secret handling. Use `.pre-commit-config.yaml` and `.github/workflows/ci.yml` as the authoritative command inventory.

## 2. Required Content

- **Content**: Small, target-specific bash, Python, or Node scripts (`.sh`, `.py`, `.js`).
- Ensure cross-platform compatibility where possible, or document explicit OS dependencies at the top of the file.

## 3. Agent Workflow Standardization

Any automation scripts or workflows added to this directory MUST comply with the **Idempotent and Deterministic** principles defined in [bootstrap.md](../docs/00.agent-governance/rules/bootstrap.md).

- **Idempotency**: Running a script twice should have the exact same effect as running it once (e.g., no corrupted state or duplicate data).
- **Clear Boundaries**: Scripts should have single responsibilities and handle failures gracefully.
- **No Hardcoded Secrets**: Scripts here MUST NEVER contain hardcoded API keys or passwords. They must fetch credentials securely from environment variables.
