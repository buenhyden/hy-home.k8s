---
title: 'Example IaC and Validator QA Implementation Plan'
type: sdlc/plan
status: draft
owner: platform
updated: 2026-08-02
artifact_id: "SPEC-0050-PLAN-0001"
---

# Example IaC and Validator QA Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development`; assign each EIVQ package to a
> fresh worker, observe focused RED before GREEN, review exact tool and command
> boundaries independently, and keep cloud/provider actions unexecuted.

## Overview

**Goal:** Extend the Spec 049 platform evidence contract with deterministic,
provider-native, non-deploy validation for the AWS Terraform and Azure Bicep
examples; commit the Terraform provider lock; align CI, routing, tests,
inventories, and example guidance; and remove the redundant example placeholder.

**Architecture:** The platform evidence contract remains the sole tool/target/
depth owner. Shared exact-tool resolution moves into an import-safe helper used
by both platform and example validators. `validate-example-iac.py` executes only
closed argv templates against safe roots with isolated temporary caches. The
current `manifest-static` job remains the primary hosted owner and prepares the
exact binaries before invoking the focused validator.

**Tech Stack:** Python 3, unittest, JSON Schema, Terraform CLI/provider lock,
standalone Bicep CLI/linter/compiler, temporary tool/provider/module caches,
GitHub Actions, affected-surface routing, Bash aggregate QA, and pre-commit.

## Context

[Spec 050](spec.md) consumes
Spec 049's depth/result/tool contract. The AWS example declares Terraform
`>= 1.14.0, < 2.0.0`, AWS provider `>= 6.28, < 7.0`, Kubernetes provider
`~> 2.30`, and exact EKS/VPC/RDS module versions, but it has no committed
provider lock or native validation owner. The Azure example is a local Bicep
module graph, yet its README currently routes static checking through Azure CLI
and provider-context `what-if` rather than standalone lint/build.

The approved Linux amd64 tools are exact:

| Tool | Version | Artifact | SHA-256 | Official source |
| --- | --- | --- | --- | --- |
| Terraform | `1.14.9` | `terraform_1.14.9_linux_amd64.zip` | `2e5cffc20a0b48a67a76268723bd5a10b8666f69b2aa4f04906e206726bedd63` | `https://releases.hashicorp.com/terraform/1.14.9/terraform_1.14.9_SHA256SUMS` |
| Bicep | `0.46.1` | `bicep-linux-x64` | `3e011d629ea4311b7a7dd8f0040ab2b1a072ea4ff5d02cb75e0e55a9a6703fb9` | `https://github.com/Azure/bicep/releases/download/v0.46.1/bicep-linux-x64` |

Terraform 1.14.9 satisfies the tracked constraint and is verified against the
official HashiCorp checksum manifest. Bicep 0.46.1 is the signed latest release
at the 2026-08-02 cutoff; the recorded checksum is for the exact official
standalone Linux x64 release asset. Provider/module retrieval remains a network
preparation dependency, while no cloud credential or provider API is required.

### Global Constraints

- Every shell command begins with `rtk`.
- Never inspect ignored/private state, credentials, auth files, secret values,
  shell history, provider payloads, RTK logs, Terraform state, plan files, or
  live cloud/cluster state.
- Never run Terraform `plan`, `apply`, `destroy`, `import`, `refresh`, active
  backend actions, or interactive commands.
- Never run Azure CLI/login, Bicep deploy/local-deploy, deployment, `what-if`,
  subscription/resource reads, or other provider-context actions.
- Use only checksum-verified tools and closed argv templates; do not use shell
  evaluation, ambient fallback, floating URLs, or tracked cache/data output.
- Developer tool absence may be bounded `SKIP`; CI-equivalent required tool or
  network preparation failure is FAIL and cannot close the tranche.
- `platform-validation-evidence.json` remains the only platform/IaC evidence
  contract, and `scripts/validation/registry.json` remains the only path router.
- Preserve current example topology unless a native static failure proves an
  in-scope defect and a focused regression covers the repair.

### Legacy Task ledger inputs

This Task is the sole durable execution-evidence owner for Spec 050. It will
record the platform-contract extension, exact Terraform/Bicep tools, provider
lock, native non-deploy results, closed-argv and artifact regressions,
README/routing/CI ownership, placeholder cleanup, QA, reviews, commits,
closure, and Spec 051 handoff. Every row is queued; this draft claims no
implementation, cloud credential, plan, deployment, hosted-current, provider,
or live result.

- Parent [Spec 050](spec.md)
- Parent [Implementation Plan](plan.md)
- [PRD-0007](../../01.requirements/0007-repository-delivery-and-platform-assurance.md),
  [AD-0010](../../02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md),
  and [ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- Spec 049 platform contract, exact-tool helper behavior, validation routing,
  CI owner, aggregate, and residual DEFER records
- Current AWS Terraform source/constraints/modules, Azure Bicep module graph,
  example READMEs, `.gitignore`, inventories, and tracked placeholder
## Goals & In-Scope

- Extend the existing platform contract/schema/fixture with Terraform and
  Bicep target, tool, command, evidence-depth, and result records.
- Extract exact-tool download/checksum/cache handling into one import-safe
  shared helper without changing Spec 049 behavior.
- Implement a safe closed-argv example validator and focused fake-tool tests.
- Generate and review `.terraform.lock.hcl`, then require backend-disabled,
  noninteractive, readonly-lock initialization and `validate -no-color`.
- Run standalone Bicep lint for every declared source and build `main.bicep`
  plus direct module fixtures to stdout/temporary storage only.
- Reject forbidden commands, credential-bearing environment, unsafe roots,
  symlinks, missing/stale lock, tracked runtime artifacts, and open argv.
- Route the validator once through affected surfaces, aggregate QA,
  `manifest-static`, CI contract tests, inventories, and existing pre-commit
  ownership.
- Align example READMEs with the implemented evidence boundary and delete
  `examples/.gitkeep` after tracked corpus proof.
- Run full QA and independent review, close reciprocally, and hand off to
  Spec 051.

## Non-Goals & Out-of-Scope

- Cloud account/subscription validation, pricing, quota, IAM/RBAC, provider
  API compatibility, deployment planning, Kubernetes admission, or runtime
  support claims.
- Changing provider/module constraints or AWS/Azure topology merely to adopt a
  newer version or silence an unreviewed warning.
- Committing `.terraform/`, state, plans, crash logs, cache, compiled ARM JSON,
  credential files, variable secrets, or provider responses.
- Creating a third evidence contract, another path registry, another primary
  CI job, or duplicated Terraform/Bicep command owner.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| EIVQ-000 | Activate reciprocal Spec 050 execution path | Spec 049 closure | Spec 050 is first unfinished relation | Spec/Plan/Task/index/progress/program row activate atomically |
| EIVQ-001 | Define closed-argv and artifact-boundary RED behavior | EIVQ-000 | Current example/tool/lock state captured | Focused tests reject every named tool, path, argv, environment, lock, syntax, and artifact defect |
| EIVQ-002 | Extend the contract and implement the shared/helper validator | EIVQ-001 | Expected RED failures observed | Contract extension, shared helper, orchestrator self-test, and focused unittest pass |
| EIVQ-003 | Generate and validate Terraform provider lock | EIVQ-002 | Exact Terraform tool prepared | Reviewed lock, fmt/init/validate PASS, isolated caches, and zero tracked runtime artifact |
| EIVQ-004 | Validate Bicep and align example guidance | EIVQ-002 | Exact Bicep tool prepared | Lint/build results and README evidence boundary agree without Azure CLI/provider context |
| EIVQ-005 | Wire routing, aggregate, CI, inventories, and cleanup once | EIVQ-003, EIVQ-004 | Focused production validation passes | Selector, manifest job, CI contract, aggregate, inventories, ignore policy, and placeholder state agree |
| EIVQ-006 | Review, close, and hand off | EIVQ-005 | Required local lanes pass | Zero open finding, reciprocal closure, bounded cloud DEFER, and Spec 051 handoff |

### File map and interfaces

**Create:**

- `scripts/platform_validation_tools.py`
- `scripts/validate-example-iac.py`
- `tests/test_validate_example_iac.py`
- fixture trees under `tests/fixtures/example-iac/`
- `examples/aws/terraform/.terraform.lock.hcl`

**Modify:**

- `docs/00.agent-governance/contracts/platform-validation-evidence.json`
- `docs/00.agent-governance/contracts/platform-validation-evidence.schema.json`
- `tests/fixtures/platform-validation-evidence.json`
- `scripts/validate-platform-evidence.py`
- `tests/test_validate_platform_evidence.py`
- `docs/90.references/data/tech-stack-version-inventory.md`
- `scripts/validation/registry.json`
- `tests/fixtures/validation-surfaces.json`
- `scripts/validate-repo-quality-gates.sh`
- `.github/workflows/ci.yml`
- `scripts/validate-ci-python-contract.py`
- `tests/test_validate_ci_python_contract.py`
- `.gitignore`, `scripts/README.md`, `tests/README.md`
- `examples/README.md`, `examples/aws/README.md`, `examples/azure/README.md`,
  `examples/azure/infrastructure/README.md`
- reciprocal Spec/Plan/Task/index/progress/program-lineage surfaces

**Delete:** `examples/.gitkeep` after the tracked non-empty proof.

**Implement these exact public interfaces:**

| Symbol | Input | Output / contract |
| --- | --- | --- |
| `ToolResolutionError` | rule ID and safe path | Value-free shared exact-tool exception |
| `resolve_exact_tool` | tool spec, cache root, prepare flag | Verified executable path with atomic download/extract and SHA-256 enforcement |
| `safe_cache_root` | candidate path | Resolved non-symlink temporary/cache path outside tracked repository |
| `IaCValidationError` | rule ID and safe path | Stable example-validator exception with no environment or secret values |
| `CommandSpec` | tool ID, fixed argv template, allowed environment keys | Immutable closed command; rejects forbidden verbs and interpolation |
| `validate_contract_extension` | root, platform contract, schema, surfaces | Normalized Terraform/Bicep target and tool records |
| `validate_tool_identity` | executable, exact version and checksum | Verified identity or fail-closed diagnostic |
| `scan_forbidden_artifacts` | repository root and tracked path set | Stable path-only findings for state/cache/plan/crash/variable-secret artifacts |
| `run_terraform` | safe root, verified tool, isolated env | Ordered fmt/init/validate result with redacted diagnostics |
| `run_bicep` | safe root, verified tool, warning policy | Per-source lint and entrypoint/module build result |
| `validate_repository` | root, tool cache, prepare/required flags | Per-target depth/lane result summary |
| `run_self_test` | repository root | Named mutation counts including forbidden actions |
| `main` | `--root`, `--self-test`, `--tool-cache`, `--prepare-tools`, `--require-tools` | exit `0` pass, `1` finding, `2` input/config error |

The Bicep warning policy is closed: compiler errors fail; new or unowned warning
codes fail; an explicitly allowlisted warning requires rationale, owner, retry
trigger, and expiry/refresh condition in the platform contract. Full command
stdout/stderr is not durable evidence.

### Task 1: EIVQ-000 — activate the reciprocal execution path

- [ ] Confirm Spec 049 closure, clean worktree, and first-unfinished relation.

  ```bash
  rtk git status --short --branch
  rtk python3 scripts/validate-document-contract-registry.py --root . --mode strict
  rtk python3 scripts/validate-document-lifecycle.py --root . --mode staged
  ```

- [ ] Set Spec 050, this Plan, its Task, and the Spec 050 program row to active;
  update Stage 03/04 indexes and progress in the same diff.

- [ ] Validate strict documents and commit only activation.

  ```bash
  rtk python3 scripts/validate-markdown-profiles.py --root . --mode strict
  rtk python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
  rtk git diff --check
  rtk git add docs/00.agent-governance/memory/progress.md docs/03.specs/0050-example-iac-and-validator-qa/spec.md docs/03.specs/README.md docs/03.specs/0050-example-iac-and-validator-qa/plan.md docs/03.specs/0050-example-iac-and-validator-qa/plan.md docs/03.specs/0050-example-iac-and-validator-qa/README.md#task-records docs/03.specs/0050-example-iac-and-validator-qa/README.md#task-records docs/99.templates/registry.json
  rtk git commit -m "docs: activate example iac validation plan"
  ```

### Task 2: EIVQ-001 — define focused RED behavior

- [ ] Create `tests/test_validate_example_iac.py` with isolated example roots
  and fake Terraform/Bicep executables that record argv and selected safe
  environment keys only.

- [ ] Cover unknown target/tool/command, copied route, duplicate JSON key,
  unsafe/outside/symlink/non-regular root, wrong binary version/checksum,
  malicious cache/tool path, missing lock, stale/rewritten lock, active backend,
  format/syntax/module/reference failure, tracked runtime artifacts, forbidden
  command verbs, interactive flag, shell string, credential environment, and
  Bicep unowned-warning behavior.

- [ ] Assert the exact production argv sequence.

  ```python
  self.assertEqual(terraform_commands[0][1:], ["fmt", "-check", "-recursive"])
  self.assertIn("-backend=false", terraform_commands[1])
  self.assertIn("-input=false", terraform_commands[1])
  self.assertIn("-lockfile=readonly", terraform_commands[1])
  self.assertEqual(terraform_commands[2][-2:], ["validate", "-no-color"])
  self.assertEqual(bicep_commands[-1][-1:], ["--stdout"])
  ```

- [ ] Run focused tests and record RED caused only by missing production
  artifacts/behavior.

  ```bash
  rtk python3 -m unittest tests/test_validate_example_iac.py
  ```

### Task 3: EIVQ-002 — extend the contract and implement the validator

- [ ] Extend the Spec 049 contract/schema/fixture with exact Terraform/Bicep
  tools and targets, required native argv, prohibited verbs, network/cache
  boundary, result/depth/lane fields, warning policy, and refresh triggers.
  Reference the existing `examples` surface ID and create no new contract.

- [ ] Extract the already-tested exact-tool implementation from
  `validate-platform-evidence.py` into `platform_validation_tools.py` without
  changing behavior. Update Spec 049 tests first, then import the shared helper
  from both focused validators.

- [ ] Implement safe root/contract loading, closed argv, environment allowlist,
  artifact scan, bounded output, exact tool identity, self-test, and stable exit
  codes in `validate-example-iac.py`.

- [ ] Use `TF_IN_AUTOMATION=1`, `TF_INPUT=0`, and explicit temporary
  `TF_DATA_DIR`/`TF_PLUGIN_CACHE_DIR`; remove provider credential variables from
  the child environment rather than recording their values. Bicep receives no
  Azure credential or config environment.

- [ ] Run contract, shared-helper, and focused tests with fakes; then prepare
  the exact official tools in temporary storage and run production.

  ```bash
  rtk python3 scripts/validate-platform-evidence.py --root . --self-test
  rtk python3 -m unittest tests/test_validate_platform_evidence.py tests/test_validate_example_iac.py
  rtk python3 scripts/validate-example-iac.py --root . --self-test
  rtk python3 scripts/validate-example-iac.py --root . --tool-cache /tmp/hy-home-iac-tools --prepare-tools --require-tools
  ```

- [ ] Update the tech-stack inventory with exact CLI identities, checksums,
  provider-lock generation boundary, official sources, and refresh triggers;
  commit the contract/helper/validator/test package.

  ```bash
  rtk git add docs/00.agent-governance/contracts/platform-validation-evidence.json docs/00.agent-governance/contracts/platform-validation-evidence.schema.json docs/90.references/data/tech-stack-version-inventory.md scripts/platform_validation_tools.py scripts/validate-example-iac.py scripts/validate-platform-evidence.py tests/fixtures/example-iac tests/fixtures/platform-validation-evidence.json tests/test_validate_example_iac.py tests/test_validate_platform_evidence.py
  rtk git commit -m "feat: add example iac validation contract"
  ```

### Task 4: EIVQ-003 — generate and validate the Terraform lock

- [ ] Confirm the exact prepared binary and absence of tracked runtime output.

  ```bash
  rtk /tmp/hy-home-iac-tools/terraform version
  rtk git ls-files examples/aws/terraform
  rtk rg -n 'backend\s+"|required_version|required_providers|source\s*=|version\s*=' examples/aws/terraform
  ```

- [ ] Create isolated cache directories, generate the provider lock for Linux
  amd64 with the pinned CLI, and review the exact selected providers/hashes.
  The network action retrieves public provider metadata/packages only.

  ```bash
  rtk mkdir -p /tmp/hy-home-terraform-data /tmp/hy-home-terraform-plugin-cache
  rtk /tmp/hy-home-iac-tools/terraform -chdir=examples/aws/terraform providers lock -platform=linux_amd64 -platform=linux_arm64 -platform=darwin_arm64
  rtk git diff -- examples/aws/terraform/.terraform.lock.hcl
  ```

- [ ] Run format check, backend-disabled readonly-lock initialization in the
  isolated data/cache directories, and validate. Do not use an environment
  containing AWS/Kubernetes credentials.

  ```bash
  rtk env TF_DATA_DIR=/tmp/hy-home-terraform-data TF_PLUGIN_CACHE_DIR=/tmp/hy-home-terraform-plugin-cache TF_IN_AUTOMATION=1 TF_INPUT=0 /tmp/hy-home-iac-tools/terraform -chdir=examples/aws/terraform fmt -check -recursive
  rtk env TF_DATA_DIR=/tmp/hy-home-terraform-data TF_PLUGIN_CACHE_DIR=/tmp/hy-home-terraform-plugin-cache TF_IN_AUTOMATION=1 TF_INPUT=0 /tmp/hy-home-iac-tools/terraform -chdir=examples/aws/terraform init -backend=false -input=false -lockfile=readonly
  rtk env TF_DATA_DIR=/tmp/hy-home-terraform-data TF_PLUGIN_CACHE_DIR=/tmp/hy-home-terraform-plugin-cache TF_IN_AUTOMATION=1 TF_INPUT=0 /tmp/hy-home-iac-tools/terraform -chdir=examples/aws/terraform validate -no-color
  ```

- [ ] Record exact resolved provider versions and platform hashes in the Task;
  verify no `.terraform`, state, plan, crash, cache, or variable-secret artifact
  is tracked; commit only the reviewed lock and necessary ignore boundary.

  ```bash
  rtk git ls-files | rtk rg '(^|/)(\.terraform/|terraform\.tfstate|terraform\.tfplan|crash\.log)|\.tfvars$'
  rtk git add .gitignore examples/aws/terraform/.terraform.lock.hcl
  rtk git commit -m "chore: lock example terraform providers"
  ```

  The tracked-artifact scan is expected to return no matching path. Omit
  `.gitignore` from staging if no evidence-backed change is required.

### Task 5: EIVQ-004 — validate Bicep and align example guidance

- [ ] Run the exact standalone binary against every declared source. Use lint
  for each file, build the entrypoint to stdout, and build direct module
  fixtures to temporary output. The current graph has repository-local modules
  only; any later external registry module requires an explicit restore and
  supply-chain boundary before this lane can remain required.

  ```bash
  rtk /tmp/hy-home-iac-tools/bicep --version
  rtk /tmp/hy-home-iac-tools/bicep lint examples/azure/infrastructure/main.bicep
  rtk /tmp/hy-home-iac-tools/bicep build examples/azure/infrastructure/main.bicep --stdout
  rtk python3 scripts/validate-example-iac.py --root . --tool-cache /tmp/hy-home-iac-tools --require-tools
  ```

- [ ] Record per-source lint/build outcomes and any warning codes under the
  closed policy. Fix only proven in-scope syntax/reference defects with a
  regression; otherwise retain an owned bounded disposition.

- [ ] Align `examples/README.md`, AWS/Azure entrypoints, and Azure
  infrastructure README with the focused orchestrator and standalone native
  commands. Move `what-if` to an explicitly separate provider-approved/live
  boundary and do not add arbitrary README sections or frontmatter.

- [ ] Validate profiles/links and commit Bicep/evidence-prose changes.

  ```bash
  rtk python3 scripts/validate-markdown-profiles.py --root . --mode strict
  rtk python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
  rtk git diff --check
  rtk git add examples/README.md examples/aws/README.md examples/azure/README.md examples/azure/infrastructure/README.md examples/azure/infrastructure
  rtk git commit -m "docs: align example iac validation guidance"
  ```

  Omit unchanged Bicep source files from the actual staged set.

### Task 6: EIVQ-005 — wire routing, CI, inventories, and cleanup once

- [ ] Register the focused validator and all Terraform/Bicep contract/tool/
  source inputs in the existing `examples` surface and fixture. Add the
  self-test/production commands to the repository aggregate without copying
  path routes or native command bodies.

- [ ] Update `manifest-static` to prepare exact Terraform/Bicep binaries under
  `$RUNNER_TEMP`, verify hashes, use isolated Terraform cache/data, and invoke
  `validate-example-iac.py --require-tools`. Do not add a separate IaC job or
  duplicate the validator in another primary CI job.

- [ ] Update CI Python contract/tests and script/test indexes for the exact
  command graph. Add Terraform runtime ignore patterns proven necessary by the
  lock/native execution.

- [ ] Confirm the tracked example corpus is non-empty, delete
  `examples/.gitkeep`, and ensure no README structure is changed beyond its
  profile and evidence rows. Delete the tracked placeholder with an
  `apply_patch` delete-file patch, then stage the deletion explicitly.

  ```bash
  rtk git ls-files examples | rtk rg -v '^examples/\.gitkeep$'
  rtk git add -u examples/.gitkeep
  ```

- [ ] Run affected, CI, security, aggregate, and focused production checks.

  ```bash
  rtk python3 scripts/validate-affected-surfaces.py --root . --self-test
  rtk python3 scripts/validate-affected-surfaces.py --root .
  rtk python3 scripts/validate-ci-python-contract.py --root . --self-test
  rtk python3 scripts/validate-ci-python-contract.py --root .
  rtk python3 scripts/validate-github-actions-security.py --root .
  rtk python3 scripts/validate-example-iac.py --root . --tool-cache /tmp/hy-home-iac-tools --require-tools
  rtk bash scripts/validate-repo-quality-gates.sh .
  ```

- [ ] Commit CI/routing/inventory/cleanup as one rollback unit.

  ```bash
  rtk git add .github/workflows/ci.yml .gitignore scripts/validation/registry.json scripts/README.md scripts/validate-ci-python-contract.py scripts/validate-repo-quality-gates.sh tests/README.md tests/fixtures/validation-surfaces.json tests/test_validate_ci_python_contract.py
  rtk git add -u examples/.gitkeep
  rtk git commit -m "ci: route example iac validation"
  ```

  Omit unchanged files from the actual staged set.

### Task 7: EIVQ-006 — review, close, and hand off

- [ ] Run focused, platform regression, all-test, static security, strict
  documents, aggregate, all-files, formatter, and diff gates.

  ```bash
  rtk python3 scripts/validate-example-iac.py --root . --self-test
  rtk python3 scripts/validate-example-iac.py --root . --tool-cache /tmp/hy-home-iac-tools --require-tools
  rtk python3 scripts/validate-platform-evidence.py --root . --self-test
  rtk python3 -m unittest tests/test_validate_example_iac.py tests/test_validate_platform_evidence.py tests/test_validate_ci_python_contract.py
  rtk python3 -m unittest discover -s tests -p 'test_*.py'
  rtk bash scripts/validate-k8s-manifests.sh .
  rtk bash scripts/validate-policy-gates.sh .
  rtk bash scripts/check-secret-handling.sh .
  rtk bash scripts/validate-repo-quality-gates.sh .
  rtk python3 scripts/validate-document-contract-registry.py --root . --mode strict
  rtk python3 scripts/validate-markdown-profiles.py --root . --mode strict
  rtk python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
  rtk pre-commit run --all-files
  rtk git status --short
  rtk git diff --check
  rtk git diff --cached --check
  ```

- [ ] Dispatch exact-diff requirements review followed by quality/security and
  infrastructure reviews. Fix every finding in the smallest owning commit and
  require zero open finding.

- [ ] Record tool, provider lock, native command, warning, artifact, routing,
  CI, QA, review, commit, and cloud/live DEFER evidence in the Task. Close the
  Spec/Plan/Task/program relation atomically and hand off only to Spec 051.

- [ ] Validate terminal lifecycle and commit closure.

  ```bash
  rtk python3 scripts/validate-document-lifecycle.py --root . --mode staged
  rtk git diff --check
  rtk git add docs/00.agent-governance/memory/progress.md docs/03.specs/0050-example-iac-and-validator-qa/spec.md docs/03.specs/README.md docs/03.specs/0050-example-iac-and-validator-qa/plan.md docs/03.specs/0050-example-iac-and-validator-qa/plan.md docs/03.specs/0050-example-iac-and-validator-qa/README.md#task-records docs/03.specs/0050-example-iac-and-validator-qa/README.md#task-records docs/99.templates/registry.json
  rtk git commit -m "docs: close example iac validation tranche"
  ```

## Verification Plan

| Layer | Required evidence | Failure rule |
| --- | --- | --- |
| Contract/tool | Spec 049 contract extension, exact versions/checksums, shared helper tests | Unknown/open/mismatched/unverified state fails |
| Terraform | fmt, lock generation review, backend-disabled readonly init, validate | Format/lock/network/init/validate or tracked artifact defect fails |
| Bicep | Per-source lint and entrypoint/module build | Error or new/unowned warning fails |
| Safety | Forbidden argv/environment/artifact/root mutations | Any credential, live verb, shell evaluation, or unsafe path fails |
| Routing/CI | Existing examples surface, aggregate, manifest job, CI contract | Duplicate primary owner or tool preparation failure fails |
| Closure | Full tests, aggregate, all-files, diff, independent reviews | Open finding or required SKIP/DEFER blocks closure |

### Legacy Task verification evidence

Not executed. Implementation will record exact CLI versions/artifacts/
checksums, contract/schema versions, selected providers and lock hashes,
Terraform/Bicep argv and results, warning codes, cache/artifact boundaries,
README/routing/CI parity, formatter effects, reviews, commits, and bounded
cloud/provider DEFER. Planned commands and official release metadata are not
current PASS evidence.
## Risks & Mitigations

- **Provider/module network drift:** commit reviewed provider lock and exact
  module versions; use readonly follow-up and classify required retrieval
  failure honestly.
- **Cloud action leakage:** closed argv and environment allowlists reject
  deploy/live verbs and provider credentials before process execution.
- **Tracked Terraform residue:** explicit artifact scanner plus `.gitignore`
  and clean-tree checks reject state/cache/plan/crash/variable-secret output.
- **Bicep warning churn:** closed warning policy requires owner/rationale/retry
  metadata and fails unknown warnings.
- **Tool resolver duplication:** extract one tested helper and keep both focused
  consumers under cross-regression tests.
- **CI command duplication:** keep `manifest-static` primary and assert exact
  command ownership in routing/CI contract tests.

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: existing platform contract/schema/fixture and validator;
  new shared tool helper/example validator/test/fixtures; Terraform lock;
  `.gitignore`; validation routing/fixture; manifest CI and CI contract;
  aggregate/inventories; example READMEs and tracked placeholder; reciprocal
  SDLC documents/indexes/progress/program relation.
- **Forbidden Paths**: ignored/private files, credentials, auth files, shell
  history, RTK logs, secret values, Terraform state/plan/cache/crash/variable
  secret files, provider response bodies, compiled deployment artifacts, and
  live cloud/cluster state.
- **Approval Required**: push, PR, hosted dispatch, Terraform plan/apply/
  destroy/import/refresh/backend mutation, Azure login/deploy/what-if/resource
  read, credential use, or live mutation. None is authorized here.
- **Static Validation**: exact tool/checksum preparation, contract/helper/
  focused self-tests, fake-tool regressions, Terraform fmt/init/validate,
  Bicep lint/build, artifact scan, affected/CI/security/aggregate/all-files/
  diff, and independent requirements/quality/security/infrastructure reviews.
- **Live Validation**: `DEFER`; cloud/provider/account/subscription/cost/quota/
  IAM/runtime evidence requires a separate approved provider context.
- **Secret Handling**: child environments are allowlisted and durable output
  contains no credential variable/value or full provider response.
- **Rollback Plan**: revert closure, CI/routing/placeholder, Bicep guidance,
  Terraform lock, and contract/helper/validator packages in reverse order.
  CI workflow/contract/test and contract/helper/consumers always revert as
  matched units.
- **Evidence Location**: this Task and
  `../../00.agent-governance/memory/progress.md`.
## Completion Criteria

- The contract extension, shared tool helper, example validator, fake-tool
  tests, self-test, and exact-tool production run pass.
- The committed Terraform lock agrees with constraints and reviewed provider
  identities; fmt, readonly backend-disabled init, and validate pass with no
  tracked runtime artifact.
- Every Bicep source receives lint evidence and entrypoint/module builds pass
  under the closed warning policy without Azure CLI/login/provider action.
- Example READMEs, affected routing, aggregate, `manifest-static`, CI contract,
  inventories, ignore rules, and placeholder deletion agree with one owner.
- Full local QA and independent reviews pass with zero open finding; cloud,
  provider, hosted-current, deployment, and live evidence remains `DEFER`.
- Spec 050, Plan, Task, indexes, progress, and program relation close
  reciprocally and hand off to Spec 051.

## Traceability

- **Spec**: [Example IaC and Validator QA](spec.md)
- **Task**: [Example IaC and Validator QA Task](README.md#task-records)
- **Program**: [PRD-0007](../../01.requirements/0007-repository-delivery-and-platform-assurance.md)
- **Architecture**: [AD-0010](../../02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md)
- **Decision**: [ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- **Predecessor**: Spec 049 Platform Validation and Security Evidence in the
  PRD-0007 program lineage
- **Successor**: Spec 051 Repository Assurance Integration and Closure in the
  PRD-0007 program lineage

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-EIVQ-001](spec.md#success-criteria--verification-plan) | EIVQ-001, EIVQ-002 | [Closed contract/argv/tool/root mutation evidence](tasks/tsk-0002-eivq-001.md) |
| N/A — VAL-EIVQ-002 and VAL-EIVQ-003 share the Spec source above | EIVQ-003 | [Exact Terraform, provider lock, native result, and artifact evidence](tasks/tsk-0004-eivq-003.md) |
| N/A — VAL-EIVQ-004 shares the Spec source above | EIVQ-004 | [Per-source Bicep lint/build/warning evidence](tasks/tsk-0005-eivq-004.md) |
| N/A — VAL-EIVQ-005 shares the Spec source above | EIVQ-001, EIVQ-002 | [Focused negative/fallback regression evidence](tasks/tsk-0002-eivq-001.md) |
| N/A — VAL-EIVQ-006 and VAL-EIVQ-007 share the Spec source above | EIVQ-004, EIVQ-005 | [README, placeholder, redaction, and protected-boundary evidence](tasks/tsk-0005-eivq-004.md) |
| N/A — VAL-EIVQ-008 shares the Spec source above | EIVQ-005, EIVQ-006 | [Routing, CI, QA, review, and closure evidence](tasks/tsk-0006-eivq-005.md) |

### Legacy Task traceability

- **Spec**: [Example IaC and Validator QA](spec.md)
- **Plan**: [Example IaC and Validator QA Implementation Plan](plan.md)
- **Predecessor**: Spec 049 Platform Validation and Security Evidence in the
  PRD-0007 program lineage
- **Successor**: Spec 051 Repository Assurance Integration and Closure in the
  PRD-0007 program lineage

#### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [EIVQ-000](plan.md#work-breakdown) | Not executed | Queued activation evidence. |
| N/A — EIVQ-001 shares the Plan and Spec sources above | Not executed | Queued focused RED and closed-command evidence. |
| N/A — EIVQ-002 shares the Plan and Spec sources above | Not executed | Queued contract/helper/validator evidence. |
| N/A — EIVQ-003 shares the Plan and Spec sources above | Not executed | Queued Terraform lock/native/artifact evidence. |
| N/A — EIVQ-004 shares the Plan and Spec sources above | Not executed | Queued Bicep and README boundary evidence. |
| N/A — EIVQ-005 shares the Plan and Spec sources above | Not executed | Queued affected/aggregate/CI/cleanup evidence. |
| N/A — EIVQ-006 shares the Plan and Spec sources above | Not executed | Queued QA, review, closure, and successor evidence. |
