# AWS Executable Examples

## Overview

This entrypoint separates executable AWS example assets from the
[dated consolidated snapshot](../../docs/90.references/cloud-examples/aws/2026-07-12-aws-example-snapshot.md). The Terraform and
Kubernetes files are reference implementations, not active local desired state
or proof of current AWS support, account readiness, cost, or provider-latest
configuration.

## Structure

| Path | Role | Authority boundary |
| --- | --- | --- |
| [`terraform/`](terraform/) | VPC, EKS, data, cache, and secret-service Terraform examples. | Executable reference assets; review provider support and account inputs before use. |
| [`kubernetes/`](kubernetes/) | Karpenter, External Secrets, and external-service Kubernetes examples. | Executable reference assets; not reconciled by this repository's local ArgoCD tree. |
| [Stage 90 snapshot](../../docs/90.references/cloud-examples/aws/2026-07-12-aws-example-snapshot.md) | Dated PRD, architecture, spec, execution, and operations snapshot. | Durable documentation destination; Spec 030 consolidation is complete. |

## Configuration Boundary

Do not commit AWS credentials, account identifiers that are not approved for
publication, Terraform state, kubeconfigs, tokens, keys, certificates, or
secret values. Resolve versions against the repository's dated Cloud Example
Snapshot and re-check official AWS/provider support before any approved use.

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

Start with the dated [AWS operations knowledge](../../docs/90.references/cloud-examples/aws/2026-07-12-aws-example-snapshot.md#definitions--facts)
and [migration task history](../../docs/90.references/cloud-examples/aws/2026-07-12-aws-example-snapshot.md#scope), then obtain human
approval before any provider or live-cluster action. Spec 030 retired the 26
AWS source59 documentation paths after consolidating their durable knowledge;
the executable assets remain under this provider tree.

## Related Documents

- [Stage 90 AWS provider handoff](../../docs/90.references/cloud-examples/aws/README.md)
- [Authored Document Migration Spec](../../docs/03.specs/030-authored-document-migration/spec.md)
- [Examples index](../README.md)
- [Tech Stack Version Inventory](../../docs/90.references/data/tech-stack-version-inventory.md)
