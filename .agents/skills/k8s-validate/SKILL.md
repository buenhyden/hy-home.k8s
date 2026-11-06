---
name: "k8s-validate"
description: "Use when validating Kubernetes manifests, GitOps structure, and secret-handling checks in this cluster repository."
metadata:
  title: "K8s Validate"
  version: "1.0.2"
  type: "governance/skill"
  status: "active"
  owner: "platform"
  updated: "2026-11-06"
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# k8s-validate

## Purpose

Define the validation sequence for manifest changes before GitOps review or merge preparation.

## When NOT to Use

- Reviewing manifests for security anti-patterns; use `vulnerability-patterns`.
- Auditing cluster security posture across dimensions; use `k8s-security-audit`.
- Onboarding or diagnosing a workload through the GitOps path; use `gitops-workflow`.

## Workflow Steps

Run the checks through `python3 scripts/qa.py quick` or
`python3 scripts/qa.py staged`, selected and bounded as
[quality policy](../../governance/quality.md#validation-runner-envelope)
defines; `python3 scripts/qa.py --list` shows what each profile reaches.

1. Check manifest YAML syntax for the changed scope. Offline Kustomize render
   and Kubernetes API-schema validation belong to the registered platform
   assurance check and are a separate depth; a syntax pass is not render or
   schema evidence.
2. Check kube-linter. `staged` reaches it through `selected-nonstyle`; `quick`
   does not, so a `quick` result covers syntax, structure and secrets but not
   lint.
3. Check GitOps structure checks. Delegate selectorless cross-file Service and
   EndpointSlice relationships to `external-service-contract-audit`; the central
   QA registry selects its dedicated checker.
4. Check secret-handling.
5. Report each selected target's actual depth, tool identity/version, fallback,
   lane, and result using the meanings quality policy owns. Name every check
   the selected profile did not reach, explicitly distinguish any unsupported
   custom-resource schema from a schema PASS, and report unobserved live state
   as DEFER.

## Constraints

- `.kube-linter.yaml` is the lint baseline. An exclusion there waives a lint
  rule, never a security finding; route the finding to `k8s-security-audit`.
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
