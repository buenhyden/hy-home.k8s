---
title: 'Protected Surface and Supply Chain Hardening Technical Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-07-12
---

# Protected Surface and Supply Chain Hardening Technical Specification (Spec)

## Overview

This Spec hardens repository-static workflow identity, GitOps change assurance,
Vault and ESO configuration boundaries, secret handling, and policy evidence.
It is the final tranche and consumes the affected-surface and agent QA contract.

## Strategic Boundaries & Non-goals

This tranche may change tracked protected surfaces and their validators. It
does not read secret values, modify ignored certificates or local settings,
push, change remote repository rules, or apply to Kubernetes, Vault, Argo CD,
ESO, or provider accounts. Repository evidence does not establish live
readiness, SLSA level, or OpenSSF compliance.

## Contracts

- **Config Contract**: Third-party Actions use full commit SHA plus a reviewable
  version comment; workflows default to read-only permissions; write permissions
  are job-scoped and justified; immutable-action linting is enabled.
- **Data / Interface Contract**: GitOps validation renders changed objects and
  deletion candidates; Vault/ESO validation checks transport, audience, scope,
  RBAC, and redaction without resolving secret values.
- **Governance Contract**: Protected changes require negative fixtures,
  independent review, rollback instructions, and explicit repo-static versus
  remote/live evidence labels.

## Core Design

- **Component Boundary**: `.github/workflows`, Dependabot and security lint
  configuration, GitOps applications and Vault/ESO manifests, infrastructure
  contracts, policy gates, secret-handling scripts, and related tests/runbooks.
  In workflow files this Spec may change Action references, permissions, and
  protected domain steps but must preserve the selector and job-routing contract
  established by Spec 031.
- **Key Dependencies**: Specs 026–031, official GitHub, OpenGitOps, Kubernetes,
  ESO, and Vault guidance, and existing repository fallbacks.
- **Tech Stack**: Full-SHA GitHub Actions, Dependabot, zizmor or equivalent
  static lint, Kustomize/render checks, YAML validation, built-in policy
  fallback, secret scan, shell syntax, and static infrastructure contracts.

Hardening decisions:

- Pin third-party and GitHub-hosted `owner/repository@ref` Actions and external
  reusable workflows to reviewed full commit SHAs, retain version comments,
  remove the `unpinned-uses` suppression, and keep automated update proposals
  subject to review and tests. Local `./path` Actions and same-repository local
  reusable workflows retain repository paths. `docker://` Actions use immutable
  image digests and a human-readable version comment rather than a Git commit
  SHA. Fixtures distinguish these reference classes.
- Verify workflow permissions and disallow broad write tokens without a named
  job consumer.
- Validate GitOps declarative, versioned, pull/reconcile boundaries; render
  manifests and review prune/delete sets without claiming reconciliation.
- Prefer namespaced Vault/ESO access where feasible; otherwise constrain
  cluster-scoped access, bind ServiceAccount name/namespace/audience, use
  least-privilege policies and RBAC, and require TLS for non-local production
  claims.
- Treat Kubernetes Secret base64 as encoding, not encryption, and retain etcd
  encryption/RBAC as independent operational requirements.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Protected-surface fixtures contain redacted
  positive and negative manifests/workflows. Evidence records tool availability,
  fallback result, rendered objects, deletion set, and unverified live boundary.
- **Migration / Transition Plan**: Pin Actions and enable immutable checks,
  harden permissions, add protected selector fixtures, then change Vault/ESO and
  GitOps contracts only where repository prerequisites and rollback are explicit.

## Interfaces & Data Structures

### Core Interfaces

```text
protected change
  -> affected-surface selection
  -> static render/lint/secret/policy checks
  -> independent review
  -> repository commit + rollback
  -> separately approved live/operator workflow
```

## Edge Cases & Error Handling

- Reject tag-only `owner/repository@ref` Actions and external reusable workflows
  even when the tag is familiar; full SHA is the immutable identity. Do not
  apply this rule to local paths, and require an image digest for `docker://`.
- A Dependabot update is a proposal, not trusted evidence until tests and release
  notes are reviewed.
- If kube-linter or Conftest is unavailable, record tool SKIP and built-in
  fallback outcome separately.
- Do not manufacture TLS references, Vault audience, or namespace restrictions
  that the repository cannot satisfy; surface an explicit operator prerequisite
  and retain fail-safe configuration.
- Never print secret-bearing arguments, environment, temporary content, or
  decoded Kubernetes Secret data.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: A security hardening change would break a declared local
  environment because its certificate, identity, or endpoint prerequisite is
  absent.
- **Fallback**: Preserve a clearly labeled local-only path, reject production
  claims, add the prerequisite and migration contract, and do not apply live.
- **Human Escalation**: Live rollout, remote branch protection, credential
  changes, or expanded tool permissions require explicit separate approval.

## Verification Commands

```bash
python3 scripts/validate-affected-surfaces.py --root .
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
bash scripts/validate-policy-gates.sh .
bash infrastructure/tests/verify-contracts-static.sh
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
git diff --check
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: All `owner/repository@ref` Actions and external reusable
  workflows use full SHAs with version comments; `docker://` uses immutable
  digest; local path references remain local; default permissions are read-only;
  and unpinned-action suppression is absent.
- **VAL-SPC-002**: Protected path fixtures select manifest, GitOps structure,
  secret handling, policy, static contract, and repository gates as applicable.
- **VAL-SPC-003**: Vault/ESO tracked configuration and tests enforce the approved
  transport, audience, scope, RBAC, and redaction boundary or explicitly label a
  local-only prerequisite without a production claim.
- **VAL-SPC-004**: All required static gates pass; optional tool SKIP and
  fallback outcomes are accurately recorded; remote/live lanes remain DEFER.

## Traceability

### Inputs

- **PRD**: [Workspace Document Assurance Modernization](../../01.requirements/005-workspace-document-assurance-modernization.md)
- **ARD**: [Workspace Document Assurance Operating Model](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- **Lineage ADR**: [Program-to-Tranche Document Lineage](../../02.architecture/decisions/0016-program-to-tranche-document-lineage.md)
- **Affected Surface Spec**: [Affected Surface and Agent QA](../031-affected-surface-agent-qa/spec.md)
- **Audit**: [Kubernetes Infrastructure and Security](../../90.references/audits/2026-07-11-weia/kubernetes-infrastructure-security.md)

### Delivery and References

- **GitHub Actions Security**: [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- **GitOps Principles**: [OpenGitOps](https://opengitops.dev/)
- **ESO Security**: [External Secrets security best practices](https://external-secrets.io/v2.0.0/guides/security-best-practices/)
- **Vault Hardening**: [Vault production hardening](https://developer.hashicorp.com/vault/docs/concepts/production-hardening)
