---
name: "k8s-security-audit"
description: "Use when auditing Kubernetes RBAC, NetworkPolicy gaps, Secret handling, container security context, image supply chain, or related cluster security hardening. Real-time intrusion detection and WAF configuration are outside this skill's scope."
metadata:
  title: "K8s Security Audit"
  version: "1.0.3"
  type: "governance/skill"
  status: "active"
  owner: "platform"
  updated: "2026-11-13"
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# k8s Security Audit — Cluster Security Assessment

## Purpose and Trigger

### When to Use

Assess a repository's Kubernetes security posture across five dimensions and
report what each one found, at a severity that says what the finding obliges.

### When Not to Use

- Matching individual manifests to known-bad shapes; use `vulnerability-patterns`, which owns pattern-to-level.
- Checking manifest and GitOps structure rather than posture; use `k8s-validate`.
- Carrying a finding forward as a tracked operational risk; use `risk-report`.

- Joining external Service and EndpointSlice declarations; use
  `external-service-contract-audit`. Its static relationship result does not
  establish security posture or permission to contact an endpoint.

## Procedure

### Steps

#### Workflow Steps

1. Fix the audit scope and type: which namespaces, paths, or manifests, and
   whether this is a full audit or one dimension. A finding outside the stated
   scope is context, not a result.
2. Work the dimensions in order — RBAC, NetworkPolicy, secrets, container
   security context, image supply chain — using
   `references/audit-dimensions.md` for the detection targets of each. The
   order is deliberate: an RBAC finding changes what a NetworkPolicy gap is
   worth.
3. Assign each finding a level with the table below, taking the pattern-to-level
   mapping from `vulnerability-patterns` where one applies.
4. Stop immediately on plaintext secret exposure and report it before
   continuing; the remaining dimensions do not change what that requires.
5. Write the report with the format below, and record the closing state rather
   than deciding acceptance, which this procedure does not own.

#### Severity Classification

This table owns what a level obliges. It does not map manifest patterns onto
levels: `vulnerability-patterns` owns that mapping together with the conditions
that escalate a pattern, and its assignment governs where the two could be read
against each other. The right column illustrates a tier rather than classifying
anything.

| Severity     | Response Required            | Illustrative finding                                                              |
| ------------ | ---------------------------- | --------------------------------------------------------------------------------- |
| **CRITICAL** | Immediate stop — block merge | Plaintext secrets, container runtime socket mounted, cluster-admin to workload SA |
| **HIGH**     | Fix before next release      | Missing NetworkPolicy, root or privileged containers, unrestricted egress         |
| **MEDIUM**   | Fix within sprint            | Missing readOnlyRootFilesystem, default SA token automount                        |
| **LOW**      | Track in backlog             | Image tag conventions, label hygiene                                              |

### Failure Handling

- Plaintext secret exposure → **immediate stop condition**; do not proceed until resolved.
- RBAC findings and network isolation gaps → route remediation to the
  implementation owner, or record them for the supervising owner when the
  selected role has no implementation handoff.
- Escalate ambiguous security decisions to the supervising owner.

## Inputs and Outputs

### Inputs

`references/audit-dimensions.md` holds the per-dimension detection targets and
checklists. It is read a dimension at a time as step 2 works through them,
which is why it is not carried in the procedure itself.

### Outputs

```markdown
# Security Audit Report

**Scope**: [namespace/cluster/path]
**Date**: YYYY-MM-DD
**Auditor**: security-auditor agent
**Audit Type**: [RBAC / NetworkPolicy / Secrets / Container Security Context / Image Supply Chain / Full]

## Executive Summary

- **Overall Posture**: PASS / CONDITIONAL / BLOCK
- **Critical findings**: N
- **High findings**: N
- **Medium findings**: N
- **Low findings**: N

## Dimension Results

| Dimension                  | Audited | Findings |
| -------------------------- | ------- | -------- |
| RBAC                       | Y/N     | N        |
| NetworkPolicy              | Y/N     | N        |
| Secrets                    | Y/N     | N        |
| Container security context | Y/N     | N        |
| Image supply chain         | Y/N     | N        |

## Findings

### CRITICAL

| ID  | Resource | Issue | Evidence | Remediation |
| --- | -------- | ----- | -------- | ----------- |

### HIGH

...

### MEDIUM

...

### LOW

...

## Remediation Priority

1. [Item] — by [date]
2. ...

## Closing State

| Level    | State recorded                                                           |
| -------- | ------------------------------------------------------------------------ |
| CRITICAL | Resolved, or unresolved and routed by name to whoever decides acceptance |
| HIGH     | Remediation owner and target release, or explicitly unassigned           |
| MEDIUM   | Owner and target sprint, or explicitly unassigned                        |
| LOW      | Backlog entry, or explicitly untracked                                   |
```

Overall Posture summarises the Closing State and is not an acceptance:
**BLOCK** when any CRITICAL is unresolved; **CONDITIONAL** when no CRITICAL is
unresolved but a HIGH has no recorded owner and target release; **PASS** when
every CRITICAL is resolved and every HIGH has an owner and target release.
A dimension not audited is stated in Dimension Results, never read as clean.

State where each finding stands rather than ticking it off. Accepting an
unresolved CRITICAL finding weakens security semantics, which
[approval and safety](../../governance/approval-and-safety.md) places outside
what an audit may decide for itself, and [the SDLC flow](../../governance/sdlc.md)
never infers approval from a checkbox. A report that carries the acceptance
box also carries the invitation to tick it.

## Verification

### Checks

This skill defines no verification step separate from its Steps; the checks the invoking task selects under the quality policy apply. If it needs a separate one, list it here.

### Completion and Handoff

- `vulnerability-patterns` — Kubernetes manifest vulnerability pattern catalog (YAML/Helm)
