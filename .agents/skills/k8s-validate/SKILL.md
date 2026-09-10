---
name: "k8s-validate"
description: "Use when validating Kubernetes manifests, GitOps structure, and secret-handling checks in this cluster repository."
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# k8s-validate

## Purpose

Define the validation sequence for manifest changes before GitOps review or merge preparation.

## Trigger Phrases

- "validate manifests"
- "run kube-linter checks"
- "check GitOps structure"
- "scan for secret-handling violations"

## When NOT to Use

- Reviewing manifests for security anti-patterns; use `vulnerability-patterns`.
- Auditing cluster security posture across dimensions; use `k8s-security-audit`.
- Onboarding or diagnosing a workload through the GitOps path; use `gitops-workflow`.

## Workflow Steps

1. Run manifest YAML syntax validation for the changed scope.
2. Run kube-linter where the selected profile reaches it. The pinned pre-commit
   hook owns that tool and the change-scoped profiles do not run it, so a
   change-scoped result covers syntax, structure and secrets but not lint.
3. Run GitOps structure checks.
4. Run secret-handling checks.
5. Report each check using the result meanings quality policy owns, and name
   every check the selected profile did not reach.

## Constraints

- `.kube-linter.yaml` is the lint baseline.
- Secret-handling violations are blocking.
- No gate here validates manifests against Kubernetes API schemas, so a syntax
  result is never reported as a schema result.
- Validation must remain repository-backed and cluster-specific.
- Do not downgrade blocking failures into informational output.

## Expected Outputs

- Validation summary across syntax, lint, structure, and secrets
- Blocking reasons, if any
- Next action guidance for review or remediation

## Failure Handling

- Stop on syntax errors or blocking secret violations.
- If a tool is unavailable, report the limitation explicitly.
- Route remediation to the implementation owner, or report the finding to the
  supervising owner when the selected role has no implementation handoff.
