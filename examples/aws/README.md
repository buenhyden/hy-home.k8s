---
title: "AWS Executable Examples"
version: "0.1.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-04"
---
# AWS Executable Examples

## Overview

### Current authority transfer

The original REQ-0007 / AD-0010 program lineage remains historical context.
Current platform requirements and architecture are [REQ-0004](../../docs/01.requirements/0004-current-local-gitops-platform.md) and
[AD-0007](../../docs/02.architecture/descriptions/0007-current-local-gitops-platform.md); shared routing, approval and QA are [REQ-0003](../../docs/01.requirements/0003-workspace-agent-governance-platform.md)
and [AD-0006](../../docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md). Package-local execution state and unfinished
0047..0051 obligations are unchanged; this transfer is not acceptance or closure.

This entrypoint defines the boundary of the executable AWS example assets.
The Terraform and Kubernetes files are reference implementations, not active
local desired state or proof of current AWS support, account readiness, cost,
or provider-latest configuration.

## Structure

| Path | Role | Authority boundary |
| --- | --- | --- |
| [`terraform/`](terraform/) | VPC, EKS, data, cache, and secret-service Terraform examples. | Executable reference assets; review provider support and account inputs before use. |
| [`kubernetes/`](kubernetes/) | Karpenter, External Secrets, and external-service Kubernetes examples. | Executable reference assets; not reconciled by this repository's local ArgoCD tree. |

## Configuration Boundary

Do not commit AWS credentials, account identifiers that are not approved for
publication, Terraform state, kubeconfigs, tokens, keys, certificates, or
secret values. The exact Terraform and Kubernetes files own their version
constraints; re-check official AWS/provider support before any approved use.

## Validation

Use repository-static checks first:

```bash
terraform fmt -check -recursive examples/aws/terraform
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
bash scripts/validate-repo-quality-gates.sh .
```

These commands do not authenticate to AWS or prove live EKS, IAM, network,
cost, secret, or provider readiness.

## Operations

These assets do not define a provider operation. Review the exact source diff,
current official AWS/provider support, credentials boundary, cost, and rollback,
then obtain human approval before any provider or live-cluster action.

## Related Documents

- [Examples index](../README.md)
- [REQ-0004 — current platform requirements](../../docs/01.requirements/0004-current-local-gitops-platform.md)
- [AD-0007 — current platform architecture](../../docs/02.architecture/descriptions/0007-current-local-gitops-platform.md)
