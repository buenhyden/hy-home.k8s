---
title: 'Platform Validation and Security Evidence Implementation Plan'
type: sdlc/plan
status: draft
owner: platform
updated: 2026-08-02
artifact_id: "PLAN-0049"
---

# Platform Validation and Security Evidence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development`; assign each PVSE package to a
> fresh worker, run specification review before quality/security review, and
> preserve value-free diagnostics and the repository-static/live boundary.

## Overview

**Goal:** Add one closed platform-evidence contract, render all thirteen
current Kustomize roots with an exact checksum-verified tool, validate
built-in Kubernetes schemas and explicit external-GVK dispositions, add
Traefik product-semantic validation, and prove the existing policy, secret,
GitOps, Vault/ESO, and image controls through direct regressions.

**Architecture:** `scripts/validation/registry.json` remains the sole path router.
`platform-validation-evidence.json` owns target, depth, tool, result,
limitation, and retry metadata. A focused Python orchestrator invokes existing
canonical validators, while a second focused validator owns Traefik reference
semantics. CI prepares exact tools in runner-temporary storage and the current
`manifest-static` job remains the primary hosted owner.

**Tech Stack:** Python 3, JSON Schema Draft 2020-12, PyYAML, unittest, Bash,
Kubernetes `kubectl`/Kustomize, kubeconform, Conftest/Rego, GitOps static
validators, Traefik file-provider YAML, pre-commit, and GitHub Actions.

## Context

[Spec 049](spec.md)
consumes the target and routing evidence from Specs 047-048. Current repository
checks parse YAML, enforce focused GitOps/policy/secret/Vault contracts, and
render selected structures, but they do not yet expose one depth-aware target
ledger, exact Kustomize/schema tool evidence for all thirteen roots, or a
Traefik cross-file reference graph.

The approved Linux amd64 tool set is exact and checksum verified:

| Tool | Version | Artifact | SHA-256 | Official source |
| --- | --- | --- | --- | --- |
| `kubectl` | `v1.35.0` | `bin/linux/amd64/kubectl` | `a2e984a18a0c063279d692533031c1eff93a262afcc0afdc517375432d060989` | `https://dl.k8s.io/release/v1.35.0/bin/linux/amd64/kubectl.sha256` |
| `kubeconform` | `v0.7.0` | `kubeconform-linux-amd64.tar.gz` | `c31518ddd122663b3f3aa874cfe8178cb0988de944f29c74a0b9260920d115d3` | `https://github.com/yannh/kubeconform/releases/download/v0.7.0/CHECKSUMS` |
| `conftest` | `v0.68.2` | `conftest_0.68.2_Linux_x86_64.tar.gz` | `e8144c6d6d2ae0260b869caa60c7c262a1f95ac63ec1e5d2fb19be452d606347` | `https://github.com/open-policy-agent/conftest/releases/download/v0.68.2/checksums.txt` |

`kubectl v1.35.0` is selected to match the current 1.35.x K3s target rather
than the ambient 1.30.x client. The official kubeconform release documents
strict built-in schema validation but not controller admission, and the
official Conftest release supplies the policy engine while the repository's
built-in fallback remains mandatory. Tool downloads and schema caches stay in
runner or operator temporary storage and never become tracked artifacts.

### Global Constraints

- Every shell command begins with `rtk`.
- Never inspect ignored/private state, secret values, credentials, auth files,
  shell history, provider payloads, RTK logs, kubeconfig, or live responses.
- No apply, diff against a live cluster, deployment, Argo CD sync, Vault/ESO
  mutation, TLS probe, push, workflow dispatch, or other remote mutation is
  authorized.
- Preserve result vocabulary `PASS`, `FAIL`, `SKIP`, and `DEFER`; a lower
  depth never promotes a higher one and a required-lane tool failure is FAIL.
- `scripts/validation/registry.json` owns paths; the new contract references surface
  IDs and must not copy routing patterns.
- `manifest-static` owns the hosted platform command graph. Repository-quality
  may invoke the focused package locally, but no second CI job may duplicate
  primary execution.
- Keep local-only Vault HTTP and Traefik `insecureSkipVerify` exceptions
  explicit; do not rewrite transport without live CA and compatibility proof.

### Legacy Task ledger inputs

This Task is the sole durable execution-evidence owner for Spec 049. It will
record the closed evidence package, exact tools, thirteen Kustomize renders,
built-in and external-GVK schema results, Traefik graph, direct security and
fallback regressions, routing/CI ownership, reviews, commits, closure, and
Spec 050 handoff. Every row is queued; this draft claims no implementation,
download, hosted-current result, remote Helm result, or live evidence.

- Parent [Spec 049](spec.md)
- Parent [Implementation Plan](plan.md)
- [PRD-0007](../../01.requirements/0007-repository-delivery-and-platform-assurance.md),
  [AD-0010](../../02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md),
  and [ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- Spec 048 target/routing handoff and current `scripts/validation/registry.json`
- Current Kustomize roots, GitOps/infrastructure desired state, policy Rego,
  tracked secret contract, Vault/ESO contract, Traefik dynamic files, CI,
  aggregate, inventories, and exact official tool/checksum sources
## Goals & In-Scope

- Create the closed platform evidence contract/schema and mutation fixture.
- Implement exact tool identity, safe temporary preparation, depth/result
  validation, target execution, and value-free reporting.
- Render all thirteen declared Kustomize roots to non-empty deterministic YAML.
- Validate built-in objects with strict kubeconform and require explicit
  disposition for every external GVK.
- Add Traefik cross-file router/service/transport, duplicate, URL, entry-point,
  and TLS-field validation for the current files and sample template.
- Directly test malformed YAML, missing resources, empty render, unavailable
  tools, invalid Rego, fallback disagreement, plaintext secret handling,
  unsafe roots, symlinks, and non-regular inputs.
- Keep GitOps, AppProject, image, policy, secret, and Vault/ESO focused owners
  canonical and invoke them without copying their policy logic.
- Register the validators once in affected routing, aggregate QA, inventories,
  CI, and CI contract tests; close with independent review and Spec 050 handoff.

## Non-Goals & Out-of-Scope

- Remote Helm chart fetch/render, cluster admission, controller behavior,
  runtime health, Vault authentication, ESO sync, TLS verification, DNS, or
  cloud/provider readiness.
- Global tool installation, floating releases, unchecked downloads, committed
  render/schema caches, or ambient binaries as equivalent required evidence.
- Blanket digest conversion, SBOM/signature/provenance rollout, component
  topology change, production transport promotion, or secret value handling.
- Duplicating existing GitOps, policy, image, secret, or Vault/ESO rules inside
  the new orchestrator.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| PVSE-000 | Activate reciprocal Spec 049 execution path | Spec 048 closure | Spec 049 is first unfinished relation | Spec/Plan/Task/index/progress/program row activate atomically |
| PVSE-001 | Define contract and orchestrator RED behavior | PVSE-000 | Current roots and exact tools observed | Focused tests reject named schema, path, depth, tool, GVK, promotion, and execution defects |
| PVSE-002 | Implement contract, exact-tool, render, schema, and evidence lanes | PVSE-001 | Expected RED failures observed | Contract/schema/fixture and platform orchestrator self-test, production, and unittest pass |
| PVSE-003 | Implement Traefik product-semantic validation | PVSE-002 | Current dynamic file set declared | Positive and mutation fixtures prove cross-file references and supported field shapes |
| PVSE-004 | Close focused security-validator regression gaps | PVSE-003 | Canonical shell/Python owners identified | Direct isolated tests prove fail-closed and fallback behavior without secret values |
| PVSE-005 | Wire routing, aggregate, and CI exactly once | PVSE-004 | All focused production checks pass | Affected surfaces, manifest job, CI contract, inventories, and aggregate agree |
| PVSE-006 | Review, close, and hand off | PVSE-005 | Required local gates pass | Zero open finding, reciprocal closure, bounded DEFER matrix, and Spec 050 handoff |

### File map and interfaces

**Create:**

- `docs/00.agent-governance/contracts/platform-validation-evidence.json`
- `docs/00.agent-governance/contracts/platform-validation-evidence.schema.json`
- `tests/fixtures/platform-validation-evidence.json`
- `scripts/validate-platform-evidence.py`
- `tests/test_validate_platform_evidence.py`
- `scripts/validate-traefik-contracts.py`
- `tests/test_validate_traefik_contracts.py`
- `tests/test_validate_vault_eso_contracts.py`
- focused fixture trees under `tests/fixtures/platform-validation/` and
  `tests/fixtures/traefik-contracts/`

**Modify when evidence requires:**

- `scripts/validation/registry.json`
- `tests/fixtures/validation-surfaces.json`
- `.github/workflows/ci.yml`
- `scripts/validate-ci-python-contract.py`
- `tests/test_validate_ci_python_contract.py`
- `scripts/validate-repo-quality-gates.sh`
- `.pre-commit-config.yaml`
- `scripts/README.md`, `tests/README.md`, `traefik/README.md`
- `docs/90.references/data/tech-stack-version-inventory.md`
- reciprocal Spec/Plan/Task/index/progress/program-lineage surfaces

**Implement these exact public interfaces:**

| Symbol | Input | Output / contract |
| --- | --- | --- |
| `EvidenceError` | `rule_id: str`, `path: str = "."` | Stable, value-free exception with safe repository-relative path |
| `ToolSpec` | ID, version, URL, SHA-256, archive member | Immutable exact-tool declaration |
| `DepthResult` | target, depth, lane, result, limitation, owner, retry trigger | Immutable result; rejects promotion and ownerless non-PASS states |
| `load_json_document` | path and rule ID | Duplicate-key-rejecting JSON value |
| `validate_contract_data` | root, contract, optional schema/surfaces | Normalized target/tool summary or `EvidenceError` |
| `resolve_tool` | `ToolSpec`, cache root, prepare flag | Verified executable path; never accepts unverified ambient fallback |
| `render_kustomize_root` | root, target path, verified `kubectl` | Non-empty bytes from `kubectl kustomize`; rejects unsafe roots and stderr leaks |
| `validate_schema_stream` | rendered bytes, verified kubeconform, GVK registry | Per-object built-in/external disposition summary |
| `run_focused_validators` | repository root and closed validator table | Stable product-semantic result map without shell evaluation |
| `validate_repository` | root, tool cache, prepare/required flags | Depth- and lane-specific summary |
| `run_self_test` | repository root | Mutation counts with every named rule exercised |
| `main` | `--root`, `--self-test`, `--tool-cache`, `--prepare-tools`, `--require-tools` | exit `0` pass, `1` finding, `2` input/config error |

The Traefik module exposes `TraefikContractError`,
`load_declared_documents`, `build_reference_graph`, `validate_repository`,
`run_self_test`, and the same exit-code convention. Existing private helpers
from `validate-gitops-change-set.py` may be refactored into import-safe public
helpers only when a regression test proves parity; route or policy data is not
copied.

### Task 1: PVSE-000 — activate the reciprocal execution path

- [ ] Confirm Spec 048 closure, clean worktree, and first-unfinished relation.

  ```bash
  rtk git status --short --branch
  rtk python3 scripts/validate-document-contract-registry.py --root . --mode strict
  rtk python3 scripts/validate-document-lifecycle.py --root . --mode staged
  ```

- [ ] Set Spec 049, this Plan, its Task, and the Spec 049 program row to active;
  update Stage 03/04 indexes and progress in the same diff.

- [ ] Validate and commit only the activation unit.

  ```bash
  rtk python3 scripts/validate-markdown-profiles.py --root . --mode strict
  rtk python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
  rtk git diff --check
  rtk git add docs/00.agent-governance/memory/progress.md docs/03.specs/0049-platform-validation-and-security-evidence/spec.md docs/03.specs/README.md docs/03.specs/0049-platform-validation-and-security-evidence/plan.md docs/03.specs/0049-platform-validation-and-security-evidence/plan.md docs/03.specs/0049-platform-validation-and-security-evidence/README.md#task-records docs/03.specs/0049-platform-validation-and-security-evidence/README.md#task-records docs/99.templates/registry.json
  rtk git commit -m "docs: activate platform validation evidence plan"
  ```

### Task 2: PVSE-001 — define focused RED behavior

- [ ] Create the contract fixture and `tests/test_validate_platform_evidence.py`.
  Cover duplicate JSON keys, unknown keys, copied route values, unknown or
  duplicate surface/target/tool IDs, invalid depth/result/lane, ownerless
  limitation, missing retry trigger, lower-depth promotion, wrong checksum,
  unsafe cache/root, symlink/non-regular input, empty render, built-in missing
  schema, unknown external GVK, and required-tool absence.

- [ ] Add subprocess fakes that record argv only and assert the exact required
  renderer/schema commands.

  ```python
  self.assertEqual(
      kubectl_argv,
      [verified_kubectl, "kustomize", str(target_root)],
  )
  self.assertEqual(
      kubeconform_argv[:6],
      [verified_kubeconform, "-strict", "-summary", "-output", "json", "-kubernetes-version"],
  )
  ```

- [ ] Run the focused test and record RED caused only by absent production
  artifacts or behavior.

  ```bash
  rtk python3 -m unittest tests/test_validate_platform_evidence.py
  ```

- [ ] Keep tests and GREEN implementation in one rollback-safe commit; the
  Task records the observed RED command/result.

### Task 3: PVSE-002 — implement the evidence contract and layered validator

- [ ] Add a Draft 2020-12 closed schema whose enums are exactly the five
  depths and four results from Spec 049. Require `limitation`, `owner`, and
  `retryTrigger` for every `SKIP`/`DEFER`; reject required-lane `SKIP`.

- [ ] Add the exact thirteen root records and exact tool rows. Record official
  URL, artifact, version, SHA-256, execution mode, target Kubernetes version,
  cache boundary, fallback, and evidence lane. Reference existing surface IDs
  only.

- [ ] Enumerate external CRD GVKs from current rendered desired state. Assign
  each one a pinned schema source or bounded `SKIP/DEFER`; do not use blanket
  `-ignore-missing-schemas` as PASS.

- [ ] Implement checksum-verified preparation into the explicit temporary
  cache, archive-member allowlisting, executable-mode setting, and atomic
  replacement. Reject redirects or archive members that escape the cache.

- [ ] Implement all-root render, multi-document parsing with duplicate-key
  rejection, deterministic identity summaries, strict built-in schema
  validation, and external-GVK reconciliation. Keep manifest bodies and
  Secret values out of output.

- [ ] Invoke canonical focused owners through fixed argv:
  `validate-gitops-structure.sh`, `validate-policy-gates.sh`,
  `check-secret-handling.sh`, `validate-vault-eso-contracts.py`, and the
  Traefik validator delivered in PVSE-003.

- [ ] Run self-test and focused tests with fake tools, then prepare exact tools
  in ignored temporary storage and run production validation.

  ```bash
  rtk python3 scripts/validate-platform-evidence.py --root . --self-test
  rtk python3 -m unittest tests/test_validate_platform_evidence.py
  rtk python3 scripts/validate-platform-evidence.py --root . --tool-cache /tmp/hy-home-platform-tools --prepare-tools --require-tools
  ```

- [ ] Update the tech-stack inventory with the three versions, artifact names,
  checksums, official checksum sources, compatibility rationale, and refresh
  triggers; commit contract, fixture, test, validator, and inventory together.

  ```bash
  rtk git add docs/00.agent-governance/contracts/platform-validation-evidence.json docs/00.agent-governance/contracts/platform-validation-evidence.schema.json docs/90.references/data/tech-stack-version-inventory.md scripts/validate-platform-evidence.py tests/fixtures/platform-validation-evidence.json tests/fixtures/platform-validation tests/test_validate_platform_evidence.py
  rtk git commit -m "feat: add layered platform validation evidence"
  ```

### Task 4: PVSE-003 — implement Traefik product-semantic validation

- [ ] Create `tests/test_validate_traefik_contracts.py` and fixtures for one
  valid cross-file graph plus undefined service/transport, duplicate qualified
  name, invalid URL scheme/host, undeclared entry point, invalid TLS field,
  unsafe path, duplicate YAML key, symlink, and non-regular input.

- [ ] Declare exactly these production inputs in the platform contract:
  `traefik/argocd-k3d.yaml`, the Headlamp, Kiali, and Rollouts variants,
  `examples/sample-app/traefik-k3d.yaml.example`, and `traefik/README.md` as
  the prose boundary.

- [ ] Implement provider-qualified router/service/transport symbol tables,
  cross-file resolution, duplicate detection, supported URL/entry-point/TLS
  shape checks, and local-only exception reconciliation. Report paths and
  stable rule IDs, never endpoint credentials or response content.

- [ ] Observe RED, implement GREEN, run production, and commit the focused
  owner as one unit.

  ```bash
  rtk python3 -m unittest tests/test_validate_traefik_contracts.py
  rtk python3 scripts/validate-traefik-contracts.py --root . --self-test
  rtk python3 scripts/validate-traefik-contracts.py --root .
  rtk git add scripts/validate-traefik-contracts.py tests/test_validate_traefik_contracts.py tests/fixtures/traefik-contracts traefik/README.md
  rtk git commit -m "feat: validate traefik reference contracts"
  ```

### Task 5: PVSE-004 — prove focused security and fallback behavior

- [ ] Extend the platform evidence test fixture trees to run the real shell
  gates against minimal temporary repository roots. Cover malformed YAML,
  missing Kustomize resource, empty render, invalid Rego syntax, missing
  Conftest, Conftest disagreement, built-in fallback failure, plaintext Secret,
  redacted sensitive key output, AppProject wildcard, `latest` image, unsafe
  root, symlink, and non-regular file behavior.

- [ ] Refactor a focused script only when direct tests prove a current defect.
  Preserve current CLI compatibility and make optional Conftest absence run the
  mandatory fallback; invalid Rego or disagreement must fail.

- [ ] Add `tests/test_validate_vault_eso_contracts.py` around the current
  import-safe Vault/ESO validation functions and fixture. Ensure
  `validate-platform-evidence.py` invokes each focused owner once. Keep the
  aggregate's README inventory and current image-policy owner intact; move
  only Traefik YAML reference-graph semantics to the new focused validator and
  make the aggregate invoke that owner instead of repeating those graph rules.

- [ ] Run the direct regressions and existing Vault/GitOps tests.

  ```bash
  rtk python3 -m unittest tests/test_validate_platform_evidence.py tests/test_validate_traefik_contracts.py tests/test_validate_gitops_change_set.py tests/test_validate_vault_eso_contracts.py
  rtk bash scripts/validate-gitops-structure.sh
  rtk bash scripts/validate-policy-gates.sh .
  rtk bash scripts/check-secret-handling.sh .
  rtk python3 scripts/validate-vault-eso-contracts.py --root .
  ```

- [ ] Commit only proven focused-owner or regression changes.

  ```bash
  rtk git add scripts/validate-k8s-manifests.sh scripts/validate-policy-gates.sh scripts/check-secret-handling.sh scripts/validate-gitops-structure.sh scripts/validate-vault-eso-contracts.py tests/test_validate_platform_evidence.py tests/fixtures/platform-validation
  rtk git commit -m "test: harden platform security validator regressions"
  ```

  Omit unchanged paths from the actual staged set.

### Task 6: PVSE-005 — wire routing, aggregate, and CI once

- [ ] Register platform contract, tool/schema inputs, Traefik inputs, and both
  focused validators in the existing `manifests` surface and fixture. Keep the
  selector source-owned; do not add parallel path expressions in workflow YAML.

- [ ] Add focused self-test/production commands to repository-quality in the
  canonical order. Use one primary aggregate invocation and remove any inline
  duplicate whose semantics moved to a focused owner.

- [ ] Update `manifest-static` to prepare the three exact tools under
  `$RUNNER_TEMP`, verify the recorded hashes, and run the platform orchestrator
  with `--require-tools`. Keep workflow permissions, timeouts, concurrency,
  artifact retention, and `ci-summary` unchanged.

- [ ] Update CI Python contract expectations and tests for the exact
  preparation/invocation sequence. Update script/test/Traefik inventories and
  `.pre-commit-config.yaml` only if the existing repository-quality hook does
  not already own the aggregate; do not add a duplicate hook.

- [ ] Run routing, CI, security, and aggregate checks.

  ```bash
  rtk python3 scripts/validate-affected-surfaces.py --root . --self-test
  rtk python3 scripts/validate-affected-surfaces.py --root .
  rtk python3 scripts/validate-ci-python-contract.py --root . --self-test
  rtk python3 scripts/validate-ci-python-contract.py --root .
  rtk python3 scripts/validate-github-actions-security.py --root .
  rtk bash scripts/validate-repo-quality-gates.sh .
  ```

- [ ] Commit integration as one rollback unit.

  ```bash
  rtk git add .github/workflows/ci.yml .pre-commit-config.yaml scripts/validation/registry.json scripts/README.md scripts/validate-ci-python-contract.py scripts/validate-repo-quality-gates.sh tests/README.md tests/fixtures/validation-surfaces.json tests/test_validate_ci_python_contract.py traefik/README.md
  rtk git commit -m "ci: route layered platform validation"
  ```

  Omit unchanged files from the actual staged set.

### Task 7: PVSE-006 — review, close, and hand off

- [ ] Run focused, all-test, platform-static, strict-document, aggregate,
  all-files, formatter, and diff gates using the verified tool cache.

  ```bash
  rtk python3 scripts/validate-platform-evidence.py --root . --self-test
  rtk python3 scripts/validate-platform-evidence.py --root . --tool-cache /tmp/hy-home-platform-tools --require-tools
  rtk python3 scripts/validate-traefik-contracts.py --root . --self-test
  rtk python3 scripts/validate-traefik-contracts.py --root .
  rtk python3 -m unittest discover -s tests -p 'test_*.py'
  rtk bash infrastructure/tests/verify-contracts-static.sh
  rtk bash scripts/validate-repo-quality-gates.sh .
  rtk python3 scripts/validate-document-contract-registry.py --root . --mode strict
  rtk python3 scripts/validate-markdown-profiles.py --root . --mode strict
  rtk python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
  rtk pre-commit run --all-files
  rtk git status --short
  rtk git diff --check
  rtk git diff --cached --check
  ```

- [ ] Dispatch exact-diff requirements review followed by quality/security,
  GitOps, network, and secret-boundary reviews. Fix every finding in the
  smallest owning commit and require zero open finding.

- [ ] Record exact tool/results, thirteen-root evidence, GVK dispositions,
  local exceptions, tests, reviews, commits, and residual remote/live DEFER in
  the Task. Transition Spec/Plan/Task/program relation atomically and activate
  no successor implementation prematurely.

- [ ] Validate terminal lifecycle and commit closure.

  ```bash
  rtk python3 scripts/validate-document-lifecycle.py --root . --mode staged
  rtk git diff --check
  rtk git add docs/00.agent-governance/memory/progress.md docs/03.specs/0049-platform-validation-and-security-evidence/spec.md docs/03.specs/README.md docs/03.specs/0049-platform-validation-and-security-evidence/plan.md docs/03.specs/0049-platform-validation-and-security-evidence/plan.md docs/03.specs/0049-platform-validation-and-security-evidence/README.md#task-records docs/03.specs/0049-platform-validation-and-security-evidence/README.md#task-records docs/99.templates/registry.json
  rtk git commit -m "docs: close platform validation evidence tranche"
  ```

## Verification Plan

| Layer | Required evidence | Failure rule |
| --- | --- | --- |
| Contract | Closed schema, source-version parity, mutation self-test | Unknown/copy/promotion/ownerless state fails |
| Syntax | Duplicate-key-aware YAML/JSON/Rego parsing | Parse defect fails target |
| Render | Thirteen non-empty `kubectl kustomize` results | Missing/empty/unsafe root or tool mismatch fails |
| Schema-policy | Strict built-in schema plus explicit external GVK registry | Unknown built-in/external GVK fails; bounded known external may DEFER |
| Product semantic | GitOps, policy, secret, Vault/ESO, image, Traefik focused owners | Canonical owner disagreement or unsafe state fails |
| CI | Exact tools, selector routing, CI contract, required summary | Preparation or primary invocation failure fails |
| Closure | Full tests, aggregate, all-files, diff, independent reviews | Any open finding or required SKIP/DEFER blocks closure |

### Legacy Task verification evidence

Not executed. Implementation will record exact contract/schema versions, all
three tool versions/artifacts/checksums, thirteen target results, object/GVK
counts, every `SKIP`/`DEFER` limitation/owner/retry trigger, Traefik graph and
mutation counts, focused fallback/redaction tests, routing/CI ownership,
formatter effects, reviews, and logical commits. Planned commands and official
release metadata are not current PASS evidence.
## Risks & Mitigations

- **Tool or schema supply-chain drift:** pin artifact, SHA-256, official source,
  target version, and refresh trigger; fail closed on mismatch.
- **External CRD false green:** enumerate each observed GVK and reject blanket
  missing-schema success.
- **Validator duplication:** declare focused owners and assert command graph
  uniqueness in routing/CI contract tests.
- **Secret leakage through diagnostics:** retain only rule ID, path, line, kind,
  key, counts, and redacted result; mutation tests reject value echo.
- **Local exception promotion:** keep environment, rationale, prohibition,
  owner, and retry trigger in the contract; require later ADR/Spec for change.
- **Network brittleness:** separate tool preparation from validation, keep
  caches temporary, and classify required preparation failure as FAIL rather
  than silently falling back.

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: new platform contract/schema/fixtures/validators/tests;
  current validation routing and fixture; manifest CI job and CI contract;
  repository aggregate/pre-commit/inventories; Traefik README; exact tool
  inventory; reciprocal SDLC documents/indexes/progress/program relation.
- **Forbidden Paths**: ignored/private files, secret values, credentials,
  kubeconfig, auth caches, shell history, RTK logs, provider responses,
  rendered Secret bodies, tracked tool/schema caches, and live-system state.
- **Approval Required**: push, PR, hosted dispatch/rerun, deployment, apply,
  cluster admission, Argo CD sync, Vault/ESO/TLS mutation, provider login, or
  other remote/live mutation. None is authorized here.
- **Static Validation**: exact checksum preparation, contract self-test and
  production, thirteen renders, schema/GVK disposition, Traefik tests,
  focused security tests, affected/CI/security/aggregate/all-files/diff, and
  independent requirements/quality/security/GitOps/network review.
- **Live Validation**: `DEFER`; remote Helm, cluster, Vault, ESO, TLS, DNS,
  controller, and provider evidence require a separately approved context.
- **Secret / Vault Handling**: value-free diagnostics only; store path, line,
  kind, key, rule ID, count, result, limitation, owner, and retry trigger.
- **Rollback Plan**: revert closure, CI/routing, focused security changes,
  Traefik validator, and evidence package in reverse order. Contract/tool
  identity and its validator/tests revert together; focused-owner registration
  and duplicate inline removal revert together.
- **Evidence Location**: this Task and
  `../../00.agent-governance/memory/progress.md`.
## Completion Criteria

- The closed contract/schema/fixture and both focused validators pass their
  self-tests, unit tests, and production repository-static execution.
- All thirteen Kustomize roots render non-empty with the exact verified
  `kubectl`; built-in schema and every external GVK have honest evidence.
- Traefik and the existing GitOps/policy/secret/Vault/image gates have direct
  positive, negative, fallback, unsafe-path, and redaction regressions.
- Affected routing, repository aggregate, `manifest-static`, CI contract,
  inventories, and pre-commit ownership contain no duplicate primary command.
- Required local lanes PASS, independent reviews have zero open finding, and
  remote Helm/live/provider evidence remains bounded `DEFER`.
- Spec 049, Plan, Task, indexes, progress, and program relation close
  reciprocally and hand off only the approved IaC work to Spec 050.

## Traceability

- **Spec**: [Platform Validation and Security Evidence](spec.md)
- **Task**: [Platform Validation and Security Evidence Task](README.md#task-records)
- **Program**: [PRD-0007](../../01.requirements/0007-repository-delivery-and-platform-assurance.md)
- **Architecture**: [AD-0010](../../02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md)
- **Decision**: [ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- **Predecessor**: Spec 048 GitHub Routing and CI Evidence in the PRD-0007
  program lineage
- **Successor**: Spec 050 Example IaC and Validator QA in the PRD-0007 program
  lineage

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-PVSE-001](spec.md#success-criteria--verification-plan) | PVSE-001, PVSE-002 | [Contract/schema mutation and source-parity results](tasks/tsk-0002-pvse-001.md) |
| N/A — VAL-PVSE-002 and VAL-PVSE-003 share the Spec source above | PVSE-002 | [Exact-tool thirteen-root render and per-GVK schema evidence](tasks/tsk-0003-pvse-002.md) |
| N/A — VAL-PVSE-004 shares the Spec source above | PVSE-003 | [Traefik positive/negative graph results](tasks/tsk-0004-pvse-003.md) |
| N/A — VAL-PVSE-005 and VAL-PVSE-006 share the Spec source above | PVSE-004 | [Canonical focused security/fallback regression results](tasks/tsk-0005-pvse-004.md) |
| N/A — VAL-PVSE-007 shares the Spec source above | PVSE-002, PVSE-003, PVSE-006 | [Exception and remote/live DEFER matrix](tasks/tsk-0003-pvse-002.md) |
| N/A — VAL-PVSE-008 shares the Spec source above | PVSE-005, PVSE-006 | [Routing, CI, QA, review, and closure evidence](tasks/tsk-0006-pvse-005.md) |

### Legacy Task traceability

- **Spec**: Platform Validation and Security Evidence
- **Plan**: Platform Validation and Security Evidence Implementation Plan
- **Predecessor**: Spec 048 GitHub Routing and CI Evidence
- **Successor**: Spec 050 Example IaC and Validator QA

#### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [PVSE-000](plan.md#work-breakdown) | Not executed | Queued activation evidence. |
| N/A — PVSE-001 shares the Plan and Spec sources above | Not executed | Queued focused RED evidence. |
| N/A — PVSE-002 shares the Plan and Spec sources above | Not executed | Queued contract, exact-tool, render, schema, and depth evidence. |
| N/A — PVSE-003 shares the Plan and Spec sources above | Not executed | Queued Traefik product-semantic evidence. |
| N/A — PVSE-004 shares the Plan and Spec sources above | Not executed | Queued security/fallback/redaction regression evidence. |
| N/A — PVSE-005 shares the Plan and Spec sources above | Not executed | Queued affected/aggregate/CI ownership evidence. |
| N/A — PVSE-006 shares the Plan and Spec sources above | Not executed | Queued QA, review, closure, and successor evidence. |
