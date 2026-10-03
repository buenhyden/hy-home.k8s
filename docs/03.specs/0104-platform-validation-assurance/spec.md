---
title: "Platform Validation Depth and Reference Assurance"
version: "1.1.0"
type: "sdlc/spec"
status: "completed"
owner: "platform"
updated: "2026-10-04"
layer: "specs"
artifact_id: "SPEC-0104"
---

# Platform Validation Depth and Reference Assurance Technical Specification

## Overview

This work unit closes the remaining repository-static assurance of
[REQ-0004-FR-0008](../../01.requirements/0004-current-local-gitops-platform.md)
and [REQ-0004-FR-0010](../../01.requirements/0004-current-local-gitops-platform.md).
The current validation registry, bounded runner, manifest syntax check, GitOps
structure check, required policy gate, secret and Vault/ESO checks, and product
validators already cover parts of those requirements. This Spec adds the
missing evidence classification, rendered-manifest/API-schema checks, and
bounded ingress and resource-kind cross-reference checks at their existing
owners. [AD-0007](../../02.architecture/descriptions/0007-current-local-gitops-platform.md)
and [ADR-0043](../../02.architecture/decisions/0043-dedicated-k8s-ingress-router.md)
define the current ingress-nginx topology; retired Traefik validation is not
restored.

The repository-static criteria were demonstrated on PR #131 implementation
head `4bfe21923b059843736c1414025f34dcd65e406f`: hosted
[run 37133944612](https://github.com/buenhyden/hy-home.k8s/actions/runs/37133944612)
passed branch policy, isolated QA, full QA, and `ci-summary` on synthetic
checkout `de4646e62b3e1bc331b64db8394427879eed4c84`. The platform gate
reported 14 roots and 92 rows: 46 PASS, 45 DEFER, one SKIP, zero FAIL.
Custom-resource schema, generated chart output, and live observation retain
the separate owners and retry conditions in [Task 4](tasks/tsk-0004-integration.md).
The final documentation head still needs its own required hosted checks before
PR delivery; this completed static contract does not assert live readiness.

## Strategic Boundaries & Non-goals

- Extend the registered platform validation route, its focused fixtures, and
  evidence output. Keep the registry as the gate/argv authority and the bounded
  runner as executor; preserve quick/staged latency and run the deeper offline
  render/schema check only at the appropriate full/CI boundary.
- Validate tracked desired-state declarations and explicit references. A Helm
  chart's expected resources are identified from reviewed pinned chart values
  and template declarations; a missing tracked resource cannot be silently
  treated as chart-managed.
- Do not claim that an offline check proves API-server admission, generated
  chart output, host DNS/IP bindings, TLS
  availability, or live Argo CD reconciliation. Those require separately
  authorized observation.
- Do not broaden local-only transport exceptions, image provenance, namespace
  enforcement, external service provisioning, or unrelated withdrawn Specs.
  Required Conftest/policy, secret, and Vault/ESO failure semantics remain
  fail-closed.
- No live cluster, cloud, secret-value, or external-service mutation is in
  scope. Hosted workflow/tool installation changes need the CI owner and a
  reviewed fixed tool/schema source if the selected implementation needs them.

## Contracts

### Evidence and execution

For each selected platform target, the result identifies validation depth
(`syntax`, `render`, `schema/policy`, `product semantic`, or `live observation`),
the concrete tool and version or pinned source identity, selected fallback,
execution lane, result, and target. `PASS` means that the named check actually
ran at the named depth; a syntax PASS never implies a render or schema PASS.
`SKIP`, `DEFER`, and a fallback are explicit dispositions, never silent PASS.
The runner retains its existing exact snapshot and required-tool behavior.
Unavailable required tooling or a missing schema for a required covered kind
fails the deep check. Live observation remains `DEFER` with an operator and
retry condition until independently observed; it does not block a clearly
named repository-static result.

The existing fast syntax, structure, policy, secret, and product checks keep
their registered lanes. One separate offline platform gate at full/CI consumes
13 current GitOps Kustomization roots and the sample-app root, plus relevant
raw platform declarations, without a live API or implicit network download.
It uses standalone Kustomize 5.8.1 (Linux amd64 release SHA-256
`029a7f0f4e1932c52a0476cf02a0fd855c0bb85694b82c338fc648dcb53a819d`),
existing jsonschema 4.26.0, and vendored strict Kubernetes 1.35.0 built-in
schemas from upstream commit `8df8a883b68a24a104b4a9e43c1288090ae60b3b`,
with source/license and per-file hashes retained. Repeating a check at another
boundary requires a different input, trust claim, or environment as defined by the common
[quality policy](../../../.agents/governance/quality.md).

### Platform reference integrity

The platform validator checks the full Kubernetes group/version/kind of
tracked declarations and their allowed AppProject resource kinds. It verifies
tracked Ingress class, host, TLS secret reference, backend Service name and
port, and namespace against the tracked destination or an explicitly declared
chart/operator-managed destination. The ingress-nginx apex redirect's
controller Service is a chart-managed reference checked against reviewed
pinned chart values and template declarations, rather than rejected as an
absent tracked Service. This static check does not observe the generated
Service. Broken, ambiguous, or unsupported references fail closed.

Existing GitOps tree, policy, secret handling, Vault/ESO, and local-only
transport contracts continue to run through their owning validators. The
new check must not make a local HTTPS exception a general allowance for
insecure service transport. Product-specific semantic claims remain distinct
from API-schema validation.

## Core Design

The validation registry selects the affected fast gates and the full/CI deep
gate. The bounded runner executes them on its existing trusted checkout or
exact-index snapshot. The existing syntax validator remains unchanged. A
separate full/CI platform validator builds reviewed local Kustomizations and
validates rendered built-in Kubernetes kinds against the pinned offline schema
corpus. Before invoking Kustomize, it accepts only currently reviewed
`apiVersion`, `kind`, and `resources` keys and regular same-root relative local
YAML references; it rejects symlinks, remote URLs, absolute paths, parent
traversal, and unknown load directives. Known reviewed custom GVKs without a
supplied schema receive explicit `DEFER` with
`external-crd-schema-unavailable` and their separate semantic gate; unknown or
malformed GVKs fail. The platform contract validator resolves
resource identity and Ingress references from the same tracked desired state
and reviewed chart declaration boundaries. The Task records which roots and kinds
are covered and which require another owner or live observation.

This design keeps YAML parsing, structural GitOps checks, policy evaluation,
and product checks at their current owners. It does not create a second gate
catalog or parallel progress ledger.

## Data Modeling & Storage Strategy

The registry and executable sources own target selection and tool versions;
the work-unit Task owns observed commands, results, and limitations. A bounded
machine-readable result, if emitted by the runner, uses the same result IDs
and snapshot identity as existing QA evidence. It contains paths and metadata
only, never secret values or live responses. No persistent cache or runtime
database is introduced. Versioned schema assets or a reviewed lock must be
traceable to a fixed upstream release and validated as part of the repository.

## Interfaces & Data Structures

The bounded `platform-depth-v1` result protocol carries each target's
`target`, `depth`, `tool`, `toolVersion`, `fallback`, and `result`; the central
runner adds the execution `lane` and retains bounded diagnostics. Fallback
codes are `none`, `external-crd-schema-unavailable`, `operator-live-check`,
`separate-required-gate`, and `not-applicable`. The named owner of a DEFER or
failure is recorded in its Task or platform result mapping. Syntax remains
the existing required gate, so depth is composed across named gates rather
than rerunning YAML parsing. Result values follow the
[quality vocabulary](../../../.agents/governance/quality.md#result-vocabulary).
The validator accepts repository-owned paths only. Kustomize root inventory,
resource identities (`apiVersion`, `kind`, `metadata.namespace`,
`metadata.name`), Ingress destination references, and chart-declaration boundaries
come from reviewed declarative inputs, not arbitrary user-supplied commands.
Any format extension stays backward compatible with existing human QA logs.

## Edge Cases & Error Handling

- Reject missing required tools, malformed or duplicate YAML documents,
  unsafe path/symlink escape, an absent declared Kustomize root, failed build,
  and schema-source mismatch or unavailable covered-kind schema.
- Reject unknown or disallowed group/kind pairs and duplicate resource
  identities within one rendered root. Identical declarations reached through
  overlapping parent/child roots are deduplicated; the same identity with
  conflicting content across roots fails.
- Reject missing tracked Ingress backend/port/TLS destination and ambiguous
  chart-managed destinations. A deliberate external/chart boundary needs
  explicit source evidence before it can satisfy a reference.
- Show the selected fallback and actual depth when an optional tool is absent.
  A fallback that does not execute the required check fails its required gate.
- An API schema check does not replace security policy or product-specific
  meaning. A syntax-only result cannot be promoted to schema PASS.
- The sample app receives schema evidence for supported built-in kinds. Its
  platform product-semantic row is `SKIP` with `not-applicable`, because it is
  an example rather than a platform Application; this is not a schema skip.

## Failure Modes & Fallback / Human Escalation

A required gate fails on missing tools, invalid inputs, unresolved references,
or unavailable required schema; the existing runner reports command and
evidence lane. The fix is to repair desired state or supply the reviewed tool
or schema input, not to downgrade the requirement. If an upstream chart or
operator declaration cannot be verified from reviewed inputs, report that target's
limitation and owner explicitly. Live observation remains operator-owned and
DEFER until authorized runtime evidence is collected. Rollback is a revert of
the scoped validator/registry/CI changes, preserving the prior required
checks.

## Verification Commands

- Run focused negative and positive fixtures for metadata classification,
  missing tool, malformed input, unsafe path, fallback, Kustomize build,
  schema validation, full GVK, and Ingress reference failures.
- Run `python3 scripts/qa.py quick` for affected-path checks and
  `python3 scripts/qa.py staged` on the exact index before each logical commit.
- The full/CI registry invokes
  `python3 scripts/validation/platform/assurance.py --root .` with its pinned
  tool in the hosted environment. A standalone local probe may use a
  separately verified temporary Kustomize binary, but it is diagnostic and
  does not replace the registered full/CI run.
- Run hosted full/CI on the PR checkout for the deep gate and full registry
  contract. Record exact run, job and result in the integration Task.
- Independent read-only review checks requirement coverage and that no
  static result is described as live readiness.

## Success Criteria & Verification Plan

| Criterion | Observable evidence |
| --- | --- |
| VAL-PVA-001 | Each selected platform target reports depth, tool identity/version, fallback, lane, result, and no promoted PASS; focused result fixtures pass. |
| VAL-PVA-002 | Declared Kustomize roots build offline and supported Kubernetes kinds receive pinned API-schema checks at full/CI; invalid build/schema and missing required tool/schema fail. |
| VAL-PVA-003 | Full GVK, tracked Ingress references, explicit chart-owned destinations, and local-only transport boundaries fail closed in focused fixtures; existing GitOps/policy/secret/Vault-ESO gates still pass. |
| VAL-PVA-004 | Exact-index staged QA, hosted full CI, independent semantic review, and Task evidence distinguish static PASS from live DEFER; requirement/AD links identify the delivered owner. |

## Traceability

[REQ-0004](../../01.requirements/0004-current-local-gitops-platform.md)
owns the need, [AD-0007](../../02.architecture/descriptions/0007-current-local-gitops-platform.md)
owns the platform view, [ADR-0043](../../02.architecture/decisions/0043-dedicated-k8s-ingress-router.md)
owns ingress topology, [Plan](plan.md) orders implementation, and the
[Task records](tasks/tsk-0001-evidence.md) own execution evidence. Existing
validators are partial coverage, and retired Spec 0049 is historical through
the [Archive index](../../98.archive/README.md#document-index).

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0004-FR-0008](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-PVA-001 | [Evidence Task](tasks/tsk-0001-evidence.md), runner/registry focused tests |
| [REQ-0004-FR-0008](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-PVA-002 | [Render/schema Task](tasks/tsk-0002-render-schema.md), offline build/schema negative tests and hosted CI |
| [REQ-0004-FR-0010](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-PVA-003 | [Reference Task](tasks/tsk-0003-platform-references.md), negative references and existing gate results |
| [REQ-0004-FR-0008](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-PVA-004 | [Integration Task](tasks/tsk-0004-integration.md), exact-index and hosted evidence |
| [REQ-0004-FR-0010](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-PVA-004 | [Integration Task](tasks/tsk-0004-integration.md), trace/read-only review and lane limits |
