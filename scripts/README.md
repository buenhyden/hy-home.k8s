# Utilities & Automation Scripts (`scripts/`)

This directory is reserved for repository maintenance, static validation, and automation helpers.

## 1. Necessity and Purpose

This folder is necessary to encapsulate repository checks that support the k3d/GitOps workflow.

- Separation of Concerns: It keeps static repository validation separate from GitOps manifests (`gitops/`) and live runtime checks (`infrastructure/tests/`).
- Consistent Execution: It provides small, repeatable checks for manifest syntax, GitOps structure, and plaintext secret handling. Use `.pre-commit-config.yaml` and `.github/workflows/ci.yml` as the authoritative command inventory.

## 2. Required Content

- **Content**: Small, target-specific bash, Python, or Node scripts (`.sh`, `.py`, `.js`).
- Ensure cross-platform compatibility where possible, or document explicit OS dependencies at the top of the file.

## 3. Script Inventory

| Script | Status | Purpose |
| --- | --- | --- |
| `validate-k8s-manifests.sh` | CI-used / manual fallback | YAML syntax validation and optional `kube-linter` coverage for manifests. |
| `validate-gitops-structure.sh` | CI-wired / manual fallback | ArgoCD root app, root app kind, and GitOps kustomization structure validation. |
| `check-secret-handling.sh` | CI-wired / manual fallback | Plaintext secret pattern scan for GitOps and infrastructure manifests. |

## 4. Agent Workflow Standardization

Any automation scripts or workflows added to this directory MUST comply with the **Idempotent and Deterministic** principles defined in [bootstrap.md](../docs/00.agent-governance/rules/bootstrap.md).

- **Idempotency**: Running a script twice should have the exact same effect as running it once (e.g., no corrupted state or duplicate data).
- **Clear Boundaries**: Scripts should have single responsibilities and handle failures gracefully.
- **No Hardcoded Secrets**: Scripts here MUST NEVER contain hardcoded API keys or passwords. They must fetch credentials securely from environment variables.

## 5. Local Tool Availability

Use local tools when they are present, but keep repository validation unblocked when optional developer tools are missing.

- `pre-commit`: local wrapper for the full hook set in `.pre-commit-config.yaml`. If it is not on `PATH`, run the scoped repository scripts directly and rely on CI for the complete hook matrix.
- `kube-linter`: used by `scripts/validate-k8s-manifests.sh` when available. If it is missing, that script skips kube-linter coverage and reports a limited local validation state.
- `graphify`: optional knowledge graph refresh. If it is not on `PATH`, use direct source inspection and record that graph refresh was not performed.
- `python3` with `PyYAML`: required by all current validation scripts. Missing Python/YAML support is a hard failure, not a skipped local check.
