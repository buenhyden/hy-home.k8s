# Azure Executable Examples

## Overview

This entrypoint separates executable Azure example assets from the dated
migration documentation under [`docs/`](docs/README.md). The Bicep, GitOps, and
Kubernetes files are reference implementations, not active local desired state
or proof of current Azure support, subscription readiness, cost, or
provider-latest configuration.

## Structure

| Path | Role | Authority boundary |
| --- | --- | --- |
| [`infrastructure/`](infrastructure/README.md) | AKS, AGC, network, database, and cache Bicep examples. | Executable reference assets; provider inputs and approval remain external. |
| [`gitops/`](gitops/README.md) | Managed Identity, Gateway API, and secret-provider platform examples. | Executable reference assets; not reconciled by the local ArgoCD tree. |
| [`kubernetes/`](kubernetes/README.md) | Workload Identity, external-service, and application manifest examples. | Executable reference assets; validate before promotion to an owned desired-state tree. |
| [`docs/`](docs/README.md) | Dated PRD, architecture, spec, execution, and operations snapshot. | Reference documentation only; Spec 030 owns consolidation into Stage 90. |

## Configuration Boundary

Do not commit Azure credentials, subscription state that is not approved for
publication, deployment outputs, kubeconfigs, tokens, keys, certificates, or
secret values. Inject parameters through reviewed interfaces and re-check
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

Start with the dated [Azure onboarding guide](docs/05.operations/guides/0001-azure-onboarding-guide.md)
and [migration task index](docs/04.execution/tasks/README.md), then obtain human
approval before any provider or live-cluster action. Spec 030 will remove the
example-local SDLC documents after their durable knowledge is consolidated;
the executable assets remain under this provider tree.

## Related Documents

- [Stage 90 Azure provider handoff](../../docs/90.references/cloud-examples/azure/README.md)
- [Authored Document Migration Spec](../../docs/03.specs/030-authored-document-migration/spec.md)
- [Examples index](../README.md)
- [Tech Stack Version Inventory](../../docs/90.references/data/tech-stack-version-inventory.md)
