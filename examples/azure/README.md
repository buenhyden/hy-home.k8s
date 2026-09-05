---
title: "Azure Executable Examples"
version: "0.1.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-04"
---
# Azure Executable Examples

## Overview

### Current authority transfer

The original REQ-0007 / AD-0010 program lineage remains historical context.
Current platform requirements and architecture are [REQ-0004](../../docs/01.requirements/0004-current-local-gitops-platform.md) and
[AD-0007](../../docs/02.architecture/descriptions/0007-current-local-gitops-platform.md); shared routing, approval and QA are [REQ-0003](../../docs/01.requirements/0003-workspace-agent-governance-platform.md)
and [AD-0006](../../docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md). Package-local execution state and unfinished
0047..0051 obligations are unchanged; this transfer is not acceptance or closure.

This entrypoint defines the boundary of the executable Azure example assets.
The Bicep, GitOps, and Kubernetes files are reference implementations, not
active local desired state or proof of current Azure support, subscription
readiness, cost, or provider-latest configuration.

## Structure

| Path | Role | Authority boundary |
| --- | --- | --- |
| [`infrastructure/`](infrastructure/README.md) | AKS, AGC, network, database, and cache Bicep examples. | Executable reference assets; provider inputs and approval remain external. |
| [`gitops/`](gitops/README.md) | Managed Identity, Gateway API, and secret-provider platform examples. | Executable reference assets; not reconciled by the local ArgoCD tree. |
| [`kubernetes/`](kubernetes/README.md) | Workload Identity, external-service, and application manifest examples. | Executable reference assets; validate before promotion to an owned desired-state tree. |

## Configuration Boundary

Do not commit Azure credentials, subscription state that is not approved for
publication, deployment outputs, kubeconfigs, tokens, keys, certificates, or
secret values. The exact Bicep, GitOps, and Kubernetes files own their version
constraints. Inject parameters through reviewed interfaces and re-check
official Azure support before any approved use.

## Validation

Use the component entrypoints and repository-static checks first:

```bash
az bicep build --file examples/azure/infrastructure/main.bicep --stdout
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
bash scripts/validate-repo-quality-gates.sh .
```

These commands do not prove live subscription, AKS, Managed Identity, Key
Vault, network, cost, secret, or provider readiness.

## Operations

These assets do not define a provider operation. Review the exact source diff,
current official Azure support, credentials boundary, cost, and rollback, then
obtain human approval before any provider or live-cluster action.

## Related Documents

- [Examples index](../README.md)
- [REQ-0004 — current platform requirements](../../docs/01.requirements/0004-current-local-gitops-platform.md)
- [AD-0007 — current platform architecture](../../docs/02.architecture/descriptions/0007-current-local-gitops-platform.md)
