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

1. Run manifest YAML syntax validation for the changed scope. Where the
   selected profile includes the registered platform assurance check, run its
   offline Kustomize render and Kubernetes API-schema validation as a separate
   depth. Quick and staged profiles retain their change-scoped checks; do not
   treat a syntax pass as render or schema evidence.
2. Run kube-linter where the selected profile reaches it. The pinned pre-commit
   hook owns that tool and the change-scoped profiles do not run it, so a
   change-scoped result covers syntax, structure and secrets but not lint.
3. Run GitOps structure checks. Delegate selectorless cross-file Service and
   EndpointSlice relationships to `external-service-contract-audit`; the central
   QA registry selects its dedicated checker.
4. Run secret-handling checks.
5. Report each selected target's actual depth, tool identity/version, fallback,
   lane, and result using the meanings quality policy owns. Name every check
   the selected profile did not reach, explicitly distinguish any unsupported
   custom-resource schema from a schema PASS, and report unobserved live state
   as DEFER.

## Constraints

- `.kube-linter.yaml` is the lint baseline.
- Secret-handling violations are blocking.
- API-schema coverage is limited to the built-in kinds and fixed offline source
  selected by the registered checker. An unavailable required tool or schema
  fails that check; do not promote a partial result or a fallback to PASS.
- Validation must remain repository-backed and cluster-specific.
- Do not downgrade blocking failures into informational output.

## Expected Outputs

- Validation summary across selected syntax, render, schema, lint, structure,
  and secret checks, with actual depth and limitations per target
- Blocking reasons, if any
- Next action guidance for review or remediation

## Failure Handling

- Stop on syntax errors or blocking secret violations.
- If a tool is unavailable, report the limitation explicitly.
- Route remediation to the implementation owner, or report the finding to the
  supervising owner when the selected role has no implementation handoff.
