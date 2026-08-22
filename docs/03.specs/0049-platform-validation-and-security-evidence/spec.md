---
title: 'Platform Validation and Security Evidence Technical Specification'
type: sdlc/spec
status: draft
owner: platform
updated: 2026-08-02
artifact_id: "SPEC-0049"
---

# Platform Validation and Security Evidence Technical Specification (Spec)

## Overview

This specification implements layered repository-static evidence for the
Kubernetes, GitOps, infrastructure, policy, secret, and Traefik surfaces handed
off by Spec 048. It makes syntax, render, schema or policy, product-semantic,
and live evidence explicit; renders all thirteen current Kustomize roots; adds
Traefik reference validation; and gives existing shell safety gates direct
negative and fallback tests.

The tranche preserves the current local platform topology and its explicit
local-only transport exceptions. It improves evidence about desired state; it
does not claim that Argo CD reconciled it, Vault authenticated it, ESO synced
it, TLS verified it, or a live cluster admitted it.

## Strategic Boundaries & Non-goals

- **Owns**: platform validation evidence contract/schema; Kustomize root
  inventory and render lane; built-in Kubernetes schema and external-GVK
  dispositions; Traefik product-semantic validator; direct shell-validator
  fixtures; image-policy disposition; exact tool/fallback evidence; and
  platform successor handoff.
- **Consumes**: Specs 047-048, current platform topology owners, GitOps and
  infrastructure desired state, Traefik files, policy Rego, secret and
  Vault/ESO validators, technology inventory, and validation-surface IDs.
- **Does not own**: component topology, remote Helm source availability,
  provider credentials, cluster admission, runtime health, secret values,
  Vault policy mutation, certificate rotation, or cloud deployment.
- **Non-goals**: replacing local-only HTTP or `insecureSkipVerify` without live
  CA evidence; treating YAML parsing as render/schema proof; silently ignoring
  unknown GVKs; installing global tools; converting every image to a digest;
  or applying manifests.

## Contracts

### Evidence-depth contract

`docs/00.agent-governance/contracts/platform-validation-evidence.json` is the
sole machine owner for platform target, required depth, exact tool identity,
execution mode, fallback, evidence lane, limitation, owner, and retry trigger.
Its closed schema defines these depths:

| Depth | Proves | Does not prove |
| --- | --- | --- |
| `syntax` | Input parses as the declared serialization or language. | Kustomize references, Kubernetes GVK validity, product references, or admission. |
| `render` | One declared root resolves and emits non-empty deterministic desired state. | API schema validity, policy, controller behavior, or live admission. |
| `schema-policy` | Available built-in schemas and repository policies accept the rendered objects. | External CRD controller behavior or product cross-reference semantics. |
| `product-semantic` | Repository-owned GitOps, Vault/ESO, secret, image, and Traefik relationships are internally valid. | Authenticated runtime or endpoint health. |
| `live` | Separately authorized observation of a named environment. | Any other cluster, provider, time, or revision. |

Each result is `PASS`, `FAIL`, `SKIP`, or `DEFER`. A lower-depth PASS never
promotes a higher depth, and required CI-equivalent tooling failure is FAIL.

### Kustomize and schema contract

- The contract enumerates exactly these current roots: `examples/sample-app`,
  `gitops/apps/root`, `gitops/clusters/local`, `gitops/workloads/adminer`, and
  nine roots under `gitops/platform` for Argo CD, cert-manager, ESO, external
  services, Headlamp, Kiali, monitoring, namespaces, and network policies.
- Every root renders non-empty output with one repository-pinned Kustomize tool
  identity compatible with the target Kubernetes/K3s minor.
- Ambient `kubectl 1.30.14` is diagnostic-only while the repository target is
  1.35.x. Required evidence uses a checksum-verified ephemeral binary recorded
  by exact version and source.
- A pinned kubeconform lane validates built-in Kubernetes resources in strict
  mode. External CRD GVKs must be explicitly allowlisted and assigned a pinned
  schema or a bounded `SKIP/DEFER`; an unknown missing schema fails.
- Remote Helm chart fetch/render remains `DEFER` unless a later Plan pins the
  source and authorizes networked supply-chain evidence.

### Product-semantic and security contract

- Traefik validation resolves router-to-service and service-to-
  `serversTransport` references, duplicate names, URL shape, entry points, and
  TLS field shape across current dynamic files and the sample template.
- GitOps structure, AppProject restrictions, image non-`latest` rules,
  tag-or-digest identity, policy fallback, secret redaction, and Vault/ESO
  local contract remain mandatory.
- The current Vault SecretStore's local-only HTTP annotation and audience/SA
  binding remain explicit. Traefik `insecureSkipVerify` remains an explicit
  local browser-proxy exception. Neither becomes a production recommendation.
- Digest, SBOM, signature, and provenance expansion requires an ADR-backed
  consumer, registry capability, rollback path, and compatibility test; this
  tranche records adopt/defer decisions but performs no blanket rewrite.

## Core Design

1. Add the closed evidence contract/schema with exact current root and
   validator inventory.
2. Introduce `validate-platform-evidence.py` as the orchestrator and contract
   validator. It invokes existing focused owners rather than copying their
   policy logic.
3. Add Kustomize render and built-in schema execution with exact tool
   preparation, non-empty output checks, allowlisted external GVK handling,
   and per-root evidence.
4. Add a dedicated Traefik product-contract validator and fixtures.
5. Add direct isolated tests for the current manifest, policy, GitOps, and
   secret shell validators, including their required fallback behavior.
6. Register the new focused validators and target paths once in the existing
   validation-surface owner and manifest/repository-quality lanes.
7. Review explicit local-only exceptions and artifact consumers; record
   unresolved live or supply-chain expansion as bounded DEFER.

The orchestrator writes no generated output into tracked desired-state paths.
Machine-readable closure data remains in the contract and Task; transient
rendered YAML and downloaded tools stay in ignored temporary storage.

## Data Modeling & Storage Strategy

The evidence contract contains:

- contract/schema versions and source contract references;
- ordered target records with `targetId`, `surfaceId`, `targetClass`, and
  repository-relative root;
- required depth records with validator ID, tool ID, exact version, checksum
  source, execution mode, expected output, and fallback;
- external GVK records with group, version, kind, schema disposition, owner,
  limitation, and retry trigger;
- product-semantic checks and their canonical focused validator;
- explicit local-only exceptions with environment, rationale, prohibition,
  owner, and promotion trigger;
- separate repo-static, CI, and remote/live observations.

No rendered Secret, credential, token, kubeconfig, Vault response, provider
log, live endpoint data, or ignored scratch payload is stored in the contract
or fixtures.

## Interfaces & Data Structures

| Interface | Required input | Output | Failure behavior |
| --- | --- | --- | --- |
| Kustomize renderer | Exact root and pinned tool | Non-empty deterministic YAML stream | Fail on missing resource, load restriction, empty output, or tool mismatch. |
| Kubernetes schema lane | Rendered stream, Kubernetes version, external GVK registry | Per-object schema result | Fail unknown GVK; bound only known unavailable external schemas. |
| Policy lane | Tracked YAML and `policy/conftest` | Conftest result plus mandatory built-in fallback | Fail when fallback disagrees, cannot run, or detects unsafe state. |
| Traefik semantic lane | Current dynamic YAML set | Reference graph and field diagnostics | Fail undefined/duplicate references or invalid supported field shapes. |
| Secret/Vault lane | Tracked manifests and current contract | Redacted diagnostics and contract result | Never emit values; fail plaintext or boundary drift. |
| Evidence reporter | All focused results | Depth- and lane-specific summary | Reject promotion, ownerless limitation, and required SKIP. |

Official design inputs are Kubernetes Kustomize and `kubectl diff`, OpenGitOps
principles, Argo CD automated sync boundaries, Vault policies and Kubernetes
auth, ESO Vault CA/audience guidance and security practices, Conftest policy
testing, and Traefik file-provider configuration:

- https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/
- https://kubernetes.io/docs/reference/kubectl/generated/kubectl_diff/
- https://opengitops.dev/
- https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/
- https://developer.hashicorp.com/vault/docs/concepts/policies
- https://developer.hashicorp.com/vault/api-docs/auth/kubernetes
- https://external-secrets.io/latest/provider/hashicorp-vault/
- https://external-secrets.io/v0.19.2/guides/security-best-practices/
- https://www.openpolicyagent.org/ecosystem/entry/conftest
- https://doc.traefik.io/traefik/reference/dynamic-configuration/file/

## Edge Cases & Error Handling

- A Kustomize root that parses but references a missing file fails render.
- An empty render fails even when the renderer exits zero.
- A built-in kind reported as missing schema fails; it cannot use the external
  CRD exception path.
- A known external CRD with no pinned schema reports its exact limitation while
  all other depths continue; the overall required contract cannot call that
  schema depth PASS.
- A Rego syntax error fails even when the built-in policy fallback would pass.
- Missing optional conftest still runs the mandatory built-in fallback; missing
  Python/PyYAML fails because the fallback cannot execute.
- Symlinked roots, outside-root paths, FIFO/non-regular inputs, and lexical
  traversal are rejected without opening unsafe targets.
- Secret diagnostics report path, line, kind, and key only; values remain
  redacted.
- A Traefik service or transport defined in another approved file is resolved
  across the declared file set; undeclared external providers require an
  explicit exception.

## Failure Modes & Fallback / Human Escalation

- **Pinned tool unavailable or checksum mismatch**: fail the required lane and
  preserve the local syntax result separately; do not use ambient fallback as
  equivalent evidence.
- **Target-version mismatch**: update the technology owner and evidence
  contract together after official compatibility research; do not float to
  latest.
- **Live-only uncertainty**: record `DEFER` with cluster/Vault/TLS owner and
  retry trigger; no direct mutation is authorized.
- **Local-only exception promotion request**: require a new ADR/Spec with CA,
  rotation, compatibility, observability, and rollback evidence.
- **Artifact assurance expansion**: stop at the current tag-or-digest gate
  until consumer and registry evidence satisfies ADR-0021.

## Verification Commands

```bash
python3 scripts/validate-platform-evidence.py --root . --self-test
python3 scripts/validate-platform-evidence.py --root .
python3 -m unittest tests/test_validate_platform_evidence.py
python3 scripts/validate-traefik-contracts.py --root . --self-test
python3 scripts/validate-traefik-contracts.py --root .
python3 -m unittest tests/test_validate_traefik_contracts.py
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
bash scripts/validate-policy-gates.sh .
bash scripts/check-secret-handling.sh .
python3 scripts/validate-vault-eso-contracts.py --root .
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
git diff --check
```

The platform-evidence and Traefik commands are Spec 049 deliverables and do not
exist until implementation. The Task records the exact Kustomize and schema
commands and tool identities selected by the approved Plan.

## Success Criteria & Verification Plan

- **VAL-PVSE-001**: The evidence contract/schema rejects unknown keys, depths,
  results, surfaces, tools, GVKs, ownerless limitations, and cross-lane
  promotion.
- **VAL-PVSE-002**: All thirteen current Kustomize roots render non-empty output
  with the approved exact tool identity.
- **VAL-PVSE-003**: Built-in Kubernetes objects receive strict schema evidence;
  known external CRDs have explicit schema dispositions and unknown GVKs fail.
- **VAL-PVSE-004**: Traefik fixtures prove router, service, transport, URL,
  entry-point, duplicate, and TLS-field semantics.
- **VAL-PVSE-005**: GitOps, policy, secret, Vault/ESO, and image controls retain
  mandatory fail-closed behavior and redacted diagnostics.
- **VAL-PVSE-006**: Direct shell-validator tests cover malformed YAML, missing
  resource, empty render, missing tool, invalid Rego, plaintext secret, unsafe
  root, symlink, and fallback behavior.
- **VAL-PVSE-007**: Local-only transport exceptions and remote Helm/live
  limitations have owner, environment, prohibition, and retry trigger without
  desired-state mutation.
- **VAL-PVSE-008**: Focused, affected, staged, aggregate, all-files, formatter,
  diff, requirements, and quality/security reviews pass.

## Traceability

- **Program requirement**:
  [PRD-0007](../../01.requirements/0007-repository-delivery-and-platform-assurance.md)
- **Architecture**:
  [AD-0010](../../02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md)
- **Decision**:
  [ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- **Plan**:
  [Platform Validation and Security Evidence Implementation Plan](plan.md)
- **Task**:
  [Platform Validation and Security Evidence Task](README.md#task-records)
- **Predecessor**:
  [Spec 048](../0048-github-routing-and-ci-evidence/spec.md)
- **Successor**:
  [Spec 050](../0050-example-iac-and-validator-qa/spec.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0007-FR-0005](../../01.requirements/0007-repository-delivery-and-platform-assurance.md#functional-requirements) | VAL-PVSE-001 | Closed contract/schema and mutation fixtures prove depth and lane integrity. |
| N/A — REQ-0007-FR-0005 shares the PRD-0007 source linked above. | VAL-PVSE-002 | Exact-root render evidence proves deterministic desired-state construction. |
| N/A — REQ-0007-FR-0005 shares the PRD-0007 source linked above. | VAL-PVSE-003 | Schema and GVK fixtures prove built-in and external disposition boundaries. |
| N/A — REQ-0007-FR-0006 shares the PRD-0007 source linked above. | VAL-PVSE-004 | Product-semantic fixtures prove Traefik reference and field behavior. |
| N/A — REQ-0007-FR-0006 shares the PRD-0007 source linked above. | VAL-PVSE-005 | Existing focused gates and new direct tests prove security contract retention. |
| N/A — REQ-0007-FR-0008 shares the PRD-0007 source linked above. | VAL-PVSE-006 | Isolated positive, negative, and fallback suites prove deterministic failure behavior. |
| N/A — REQ-0007-FR-0009 shares the PRD-0007 source linked above. | VAL-PVSE-007 | Exception and DEFER rows prove honest live/transport boundaries. |
| N/A — REQ-0007-FR-0010 shares the PRD-0007 source linked above. | VAL-PVSE-008 | Local QA and independent reviews prove rollback-ready closure. |
