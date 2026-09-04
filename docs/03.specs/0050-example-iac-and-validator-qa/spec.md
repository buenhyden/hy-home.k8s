---
title: "Example IaC and Validator QA Technical Specification"
version: "1.0.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0050"
---

# Example IaC and Validator QA Technical Specification (Spec)

## Overview

### Current Execution Disposition (2026-09-05)

Keep Spec 0050 and its Plan `draft`, with every Task `queued`. Resume only
after Spec 0049 and its package-local Plan/Tasks close with their required
evidence, through the legal Spec/Plan `draft → active` and activation Task
`queued → in-progress` transitions. Accepted
[ADR-0031](../../02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md)
and [ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md)
own this package-local route. ADR-0021 is superseded historical context;
activation and closure create no public program-instance roster.

The current validation registry declares no Terraform or Bicep validator;
the proposed example-IaC implementation remains unfinished.
Before activation, reconcile the older planned paths, provider examples,
commands, and scope with the current canonical owners. This disposition
preserves unfinished work and authorizes no implementation or protected action.

This specification gives the executable AWS Terraform and Azure Bicep examples
provider-native, non-deploy validation and closes the direct regression-test
gaps handed off by Spec 049. It also consolidates example, script, test, policy,
and tracked-secret QA routing without creating a third machine contract or
claiming cloud readiness.

The examples remain reference implementations outside the local Argo CD
desired-state tree. Native static validation proves formatting, initialization,
configuration semantics, lint, and compilation only; it does not prove account,
subscription, cost, quota, IAM, network, managed-service, or runtime support.

## Strategic Boundaries & Non-goals

- **Owns**: example-IaC validator; Terraform lock and static validation
  contract; Bicep lint/build contract; exact tool evidence extension; direct
  fixtures for tool absence, syntax, references, and forbidden actions;
  example README claim alignment; unnecessary placeholder cleanup; and
  successor handoff.
- **Consumes**: Specs 047-049, executable example files, technology inventory,
  `platform-validation-evidence.json`, existing manifest/policy/secret gates,
  script and test indexes, and dated AWS/Azure snapshots.
- **Does not own**: cloud provider currentness research, credentials, accounts,
  subscriptions, Terraform state/backend, deployment planning, live cost,
  Kubernetes admission, or provider resource mutation.
- **Non-goals**: `terraform plan` or `apply`; Azure login, deployment, or
  `what-if`; changing resource topology merely to satisfy a linter; downloading
  floating latest tools; reading ignored state; or treating a regex-only check
  as provider-native semantic PASS.

## Contracts

### Common example validation contract

`scripts/validate-example-iac.py` is the focused orchestrator. It extends the
Spec 049 platform evidence contract with Terraform and Bicep targets and
records:

- exact target root and language;
- required native commands and prohibited commands;
- exact tool version, source, and checksum evidence;
- network requirement and isolated cache locations;
- result, evidence depth, lane, limitation, owner, and retry trigger;
- redacted command output suitable for Task evidence.

The orchestrator accepts a repository root, rejects outside/symlinked unsafe
roots, never invokes a shell string, and runs only closed argv templates.
Developer diagnostics may report native-tool `SKIP`; the required CI-equivalent
lane prepares the pinned tool or fails.

### Terraform contract

- Pin Terraform to one version allowed by the example's
  `>= 1.14.0, < 2.0.0` constraint and record its official checksum.
- Commit and verify `.terraform.lock.hcl` for the declared AWS and Kubernetes
  providers. Module versions remain exact in source.
- Run `terraform fmt -check -recursive`.
- Run `terraform init -backend=false -input=false -lockfile=readonly` with
  `TF_DATA_DIR` and plugin cache in ignored temporary storage.
- Run `terraform validate -no-color` after successful initialization.
- Reject backend activation, state writes in tracked paths, plan, apply,
  destroy, import, refresh, cloud credentials, and interactive prompts.

Network access for official tool/provider/module retrieval is an explicit CI
preparation dependency. Checksums, lock data, and exact module versions provide
reproducibility; a network failure is not a successful validation.

### Bicep contract

- Pin the standalone Bicep CLI to one exact official release and checksum; do
  not require the Azure CLI or login for static validation.
- Run `bicep lint` for each declared entrypoint and module file as supported by
  the pinned CLI.
- Run `bicep build --stdout` for `main.bicep` and direct module fixtures.
- Treat warnings according to a documented severity policy; compiler errors,
  missing modules, invalid resource types, or invalid references fail.
- Reject `az login`, deployment commands, `what-if`, subscription reads, and
  any credential-bearing environment dependency.

### Tracked secret and placeholder boundary

Only Git-tracked placeholder or contract files under `secrets/**` are in scope.
Ignored auth files, tokens, shell history, state, diagnostics, and secret values
are never opened. The now-redundant `examples/.gitkeep` is deleted once the
tracked example corpus is confirmed non-empty.

## Core Design

1. Extend `platform-validation-evidence.json` with the AWS Terraform and Azure
   Bicep target records, using the existing technology inventory as version
   research owner.
2. Add the closed-argv Python orchestrator, self-test mutation set, and focused
   unit tests with fake tool executables.
3. Generate and review the Terraform provider lock using the pinned tool;
   retain no `.terraform`, state, plan, or credential artifact.
4. Add required CI preparation and execution to the existing manifest/static
   or repository-quality ownership path without duplicating the command in
   multiple primary jobs.
5. Correct AWS/Azure README validation commands and evidence boundaries only
   where they disagree with the implemented native lane.
6. Remove the unnecessary root placeholder and update examples/scripts/tests
   indexes if their selected profiles require an inventory change.
7. Run positive, negative, missing-tool, and forbidden-action tests before the
   aggregate and all-files gates.

Kubernetes and GitOps YAML under the examples remains covered by Spec 049's
manifest, policy, secret, and Kustomize contracts. This Spec does not duplicate
those validators in the IaC orchestrator.

## Data Modeling & Storage Strategy

Terraform data lives only in source `.tf` files and the reviewed provider lock.
`.terraform/`, plugin/module caches, state, crash logs, plan files, and variable
secret files remain ignored and absent from commits. Bicep build output is
captured in memory or temporary files and is not committed unless a later Spec
defines a generated artifact owner.

Test fixtures use minimal isolated source trees and fake executable shims. They
must not contain real account IDs, subscription IDs, credentials, provider
tokens, private endpoints, secret values, or copied user configuration.

Task evidence records command argv, tool/version, result, network dependency,
redacted diagnostic summary, limitation, and retry trigger. It does not record
full environment variables or provider download credentials.

## Interfaces & Data Structures

| Interface | Input | Required result | Forbidden side effect |
| --- | --- | --- | --- |
| Terraform formatter | AWS Terraform root | Exact-format PASS | File mutation during check mode |
| Terraform initializer | Source, lock, isolated data/cache dirs | Backend-disabled, noninteractive initialization PASS | Backend/state activation or tracked cache |
| Terraform validator | Initialized isolated root | Configuration-valid PASS | Plan, refresh, provider API mutation |
| Bicep linter | Declared `.bicep` sources | Severity-policy PASS | Azure authentication or deployment |
| Bicep compiler | `main.bicep` and module fixtures | Deterministic stdout build PASS | Persistent deployment artifact or provider call |
| Orchestrator | Root, contract, exact tools | Per-target lane/depth summary | Shell evaluation, unsafe path traversal, secret output |

The design follows Terraform's official `validate` and canonical `fmt`
contracts plus Microsoft's Bicep linter, CLI build, and separately bounded
deployment what-if guidance:

- https://developer.hashicorp.com/terraform/cli/commands/validate
- https://developer.hashicorp.com/terraform/cli/commands/fmt
- https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/linter
- https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/bicep-cli
- https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-what-if

## Edge Cases & Error Handling

- An absent native tool yields diagnostic SKIP locally but required-lane FAIL
  unless exact tool preparation succeeds.
- Terraform format failure must not autoformat in the validation command; a
  separately reviewed formatter change is rerun through all gates.
- A stale or incomplete lock fails `-lockfile=readonly`; the validator does not
  silently rewrite it.
- Provider or module download failure records network preparation FAIL and
  preserves no partial tracked cache.
- Terraform syntax can parse while initialization or validation fails because
  of provider/module semantics; results remain at their actual depth.
- Bicep can lint a module but fail entrypoint build because of missing outputs
  or parameter types; both results remain visible.
- A fake or malicious tool path outside the approved cache is rejected even if
  it reports the expected version string.
- An attempted `plan`, `apply`, `destroy`, `deploy`, login, or `what-if` argv in
  the contract or fixture fails the closed-command validator.
- Example README prose remains a boundary and routing surface; no governance
  body or unsupported frontmatter is added.

## Failure Modes & Fallback / Human Escalation

- **Tool checksum or provenance failure**: stop the required lane; do not fall
  back to an ambient or floating binary.
- **Official version incompatibility**: update the dated technology research
  and approved Plan before changing constraints or example resources.
- **Provider/network unavailable**: record FAIL for required CI or SKIP for a
  bounded developer diagnostic, with owner and retry trigger.
- **Cloud semantics require API access**: record `DEFER`; obtain separate
  credentials and action approval only in a later live-readiness Spec.
- **Example defect requires topology change**: update PRD/AD/ADR/Spec scope
  before altering the reference implementation.

## Verification Commands

```bash
rtk python3 scripts/validate-example-iac.py --root . --self-test
rtk python3 scripts/validate-example-iac.py --root .
rtk python3 -m unittest tests/test_validate_example_iac.py
rtk terraform fmt -check -recursive examples/aws/terraform
rtk terraform -chdir=examples/aws/terraform init -backend=false -input=false -lockfile=readonly
rtk terraform -chdir=examples/aws/terraform validate -no-color
rtk bicep lint examples/azure/infrastructure/main.bicep
rtk bicep build examples/azure/infrastructure/main.bicep --stdout
rtk bash scripts/validate-k8s-manifests.sh .
rtk bash scripts/validate-policy-gates.sh .
rtk bash scripts/check-secret-handling.sh .
rtk bash scripts/validate-repo-quality-gates.sh .
rtk pre-commit run --all-files
rtk git diff --check
```

The focused validator and native tool commands become executable only after
the Plan pins and prepares the exact tools. Direct native commands run in the
isolated environment described above, not an unreviewed ambient configuration.

## Success Criteria & Verification Plan

- **VAL-EIVQ-001**: The orchestrator rejects unknown targets, unsafe roots,
  unapproved tools, open argv, forbidden commands, ownerless limitations, and
  lane/depth promotion.
- **VAL-EIVQ-002**: Terraform format, backend-disabled readonly-lock init, and
  validate pass with one approved tool and no tracked runtime artifact.
- **VAL-EIVQ-003**: The committed provider lock, exact module versions, and
  technology inventory agree and fail on drift.
- **VAL-EIVQ-004**: Bicep lint and build pass for the declared entrypoint and
  modules without Azure CLI authentication or deployment.
- **VAL-EIVQ-005**: Fixtures prove missing-tool, syntax, format, lock, module,
  reference, unsafe-path, and forbidden-action failure behavior.
- **VAL-EIVQ-006**: Example README commands and evidence claims match actual
  validator ownership; `examples/.gitkeep` is absent and no arbitrary section
  or frontmatter is added.
- **VAL-EIVQ-007**: Tracked secret checks stay redacted and no ignored/private
  state, credential, cloud API, state, plan, or deployment is accessed.
- **VAL-EIVQ-008**: Focused, affected, staged, aggregate, all-files, formatter,
  diff, requirements, and quality/security reviews pass.

## Traceability

- **Program requirement**:
  [PRD-0007](../../01.requirements/0007-repository-delivery-and-platform-assurance.md)
- **Architecture**:
  [AD-0010](../../02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md)
- **Decision**:
  [superseded ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- **Plan**:
  [Example IaC and Validator QA Implementation Plan](plan.md)
- **Task**:
  [Example IaC and Validator QA Task](plan.md)
- **Predecessor**:
  [Spec 049](../0049-platform-validation-and-security-evidence/spec.md)
- **Successor**:
  [Spec 051](../0051-repository-assurance-integration-and-closure/spec.md)

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0007-FR-0007](../../01.requirements/0007-repository-delivery-and-platform-assurance.md#functional-requirements) | VAL-EIVQ-001 | Closed-command orchestrator and mutation fixtures prove execution safety. |
| N/A — REQ-0007-FR-0007 shares the PRD-0007 source linked above. | VAL-EIVQ-002 | Native Terraform commands prove non-deploy configuration semantics. |
| N/A — REQ-0007-FR-0007 shares the PRD-0007 source linked above. | VAL-EIVQ-003 | Lock and inventory comparison proves reproducible provider/module identity. |
| N/A — REQ-0007-FR-0007 shares the PRD-0007 source linked above. | VAL-EIVQ-004 | Native Bicep lint/build proves static module semantics without login. |
| N/A — REQ-0007-FR-0008 shares the PRD-0007 source linked above. | VAL-EIVQ-005 | Isolated negative and fallback tests prove deterministic error handling. |
| N/A — REQ-0007-NFR-0002 shares the PRD-0007 source linked above. | VAL-EIVQ-006 | Profile and direct command comparison proves accurate example routing prose. |
| N/A — REQ-0007-FR-0009 shares the PRD-0007 source linked above. | VAL-EIVQ-007 | Redacted scope and filesystem evidence proves protected boundaries. |
| N/A — REQ-0007-FR-0010 shares the PRD-0007 source linked above. | VAL-EIVQ-008 | Local QA and independent reviews prove rollback-ready closure. |
