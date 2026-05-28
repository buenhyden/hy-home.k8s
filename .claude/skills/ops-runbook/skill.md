---
name: ops-runbook
description: Use when authoring or reviewing operations runbooks for bootstrap, recovery, deployment, backup, and incident procedures in hy-home.k8s.
---

# ops-runbook

## Purpose

Author and review operations runbooks (`docs/05.operations/runbooks/`) for this repository's
WSL2+k3d+ArgoCD platform. Ensure runbooks are executable, verifiable, and safe for operator
use without requiring cluster access delegation.

## Trigger Phrases

- "write a runbook"
- "create runbook for"
- "document the bootstrap procedure"
- "ops procedure for"
- "how do we recover from"
- "incident response runbook"
- "deployment runbook"

## When to Use

- Documenting bootstrap, recovery, deployment, backup, or incident response procedures.
- Reviewing an existing runbook for correctness, completeness, and safety.
- Translating a break-glass or operator-bound action into a reproducible, step-by-step guide.
- Producing files under `docs/05.operations/runbooks/` or `docs/05.operations/playbooks/`.

## When NOT to Use

- Authoring an execution plan or task unit; use `execution-plan` or `task-breakdown`.
- Tracing requirements or architecture decisions; use `requirements-to-design`.
- Diagnosing a live incident without an existing runbook; use incident-postmortem after.

## Workflow Steps

1. Identify the runbook type: bootstrap, recovery, deployment, backup, or incident.
2. State the pre-conditions (required cluster state, credentials, environment variables).
3. List every step with the exact command, expected output, and failure signal.
4. Include a verification step after each destructive or irreversible action.
5. Write a Rollback section that undoes each step in reverse order.
6. State post-conditions that confirm the procedure succeeded.
7. Link to the relevant ArgoCD apps, Vault paths, or ESO SecretStore resources.
8. Save the file under `docs/05.operations/runbooks/` or `docs/05.operations/playbooks/`
   following the existing naming convention.
9. Update `docs/05.operations/README.md` to include the new runbook link.

## Safety Rules

- Never include plaintext Kubernetes secrets or Vault tokens in runbook steps.
- Mark every live-cluster mutating step with `<!-- OPERATOR-BOUND -->` comment.
- Every bootstrap-boundary action (k3d create, ArgoCD install, root app apply) must state
  the exact `kubectl apply` or `helm install` command and its scope.
- Break-glass actions must record scope, rollback, and verification evidence in the runbook.
