---
name: k8s-validate
description: Validation workflow for Kubernetes manifests, GitOps structure, and secret-handling checks in this cluster repository.
---

# k8s-validate

## Purpose

Define the validation sequence for manifest changes before GitOps review or merge preparation.

## Trigger Phrases

- "validate manifests"
- "run kube-linter checks"
- "check GitOps structure"
- "scan for secret-handling violations"

## Workflow Steps

1. Run YAML and schema validation for the changed scope.
2. Run kube-linter against the approved configuration.
3. Run GitOps structure checks.
4. Run secret-handling checks.
5. Return a pass, fail, or blocked outcome with evidence.

## Constraints

- `.kube-linter.yaml` is the lint baseline.
- Secret-handling violations are blocking.
- Validation must remain repository-backed and cluster-specific.
- Do not downgrade blocking failures into informational output.

## Expected Outputs

- Validation summary across syntax, lint, structure, and secrets
- Blocking reasons, if any
- Next action guidance for review or remediation

## Failure Handling

- Stop on syntax errors or blocking secret violations.
- If a tool is unavailable, report the limitation explicitly.
- Route remediation back to `k8s-implementer.md` or `supervisor.md` as appropriate.
