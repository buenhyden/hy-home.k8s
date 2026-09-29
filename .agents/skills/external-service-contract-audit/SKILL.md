---
name: "external-service-contract-audit"
description: "Use when auditing selectorless external Service/EndpointSlice mappings or repository consumers of external HTTP, database and OTLP endpoints."
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation grants no additional authority.

# external-service-contract-audit

## Purpose

Check the repository contract between an external service and its Kubernetes
consumers before changing a port, endpoint, protocol or secret reference.

## Trigger Phrases

- "audit external service contracts"
- "check selectorless Service endpoints"
- "review an external database or OTLP endpoint change"

## When NOT to Use

- General workload onboarding or Argo CD diagnosis: `gitops-workflow`.
- General manifest validation: `k8s-validate`.
- Live connectivity or authentication probes without separate operator scope.

## Workflow Steps

1. Identify the changed Service and every same-namespace EndpointSlice bearing
   its service-name label. Inspect its actual consumer and secret reference;
   read [protocol contracts](references/external-service-contracts.md) for the
   affected protocol. Do not read secret values.
2. From the repository root run
   `python3 .agents/skills/external-service-contract-audit/scripts/validate-service-endpoints.py --root .`.
   The dedicated [checker](scripts/validate-service-endpoints.py) joins numeric
   backend ports across all slices. Identical repeated endpoints are valid;
   split named ports aggregate. Selector-managed Services are excluded.
3. Review consumer scheme, host, frontend port, authentication reference and
   retry/timeout owner. The static join cannot prove availability or credentials.
4. Run the affected central QA profile. Its registry selects this checker;
   invocation of this skill never adds a gate or changes an approval.

## Constraints

Use tracked and nonignored new YAML in `gitops/platform/external-services/`.
The checker accepts bounded regular files, requires installed Python, Git and
PyYAML, and rejects unsafe paths, aliases and malformed contracts. It performs
no network request. It is not Kubernetes schema validation or an ESO/security
replacement. Named targetPort resolution is outside this repository's numeric
external-endpoint contract and fails explicitly.

## Expected Outputs

Report affected consumer/field, PASS or FAIL, command and static scope, required
remediation, and deferred live evidence with its next owner. Preserve separate
results for general Kubernetes validation and live connectivity.

## Failure Handling

A missing required tool, malformed input, timeout or incomplete output is FAIL.
Stop and report the bounded error; do not echo raw YAML, stderr or credentials.
Route manifest repair to `k8s-implementer` and contract review to
`gitops-reviewer`. Live probes require the operator's separately scoped action.
