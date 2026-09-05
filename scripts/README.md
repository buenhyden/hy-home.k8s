---
title: "scripts"
version: "0.1.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-04"
---
# scripts

## Overview

`scripts/`는 저장소의 문서, Agent governance, GitOps, CI, 보안 경계를
repository-static 방식으로 검증하는 실행 코드의 소유 경로다. 사람에게 보이는
규칙은 각 canonical 문서가 소유하고, 이 폴더는 그 규칙의 machine enforcement와
검증 routing만 구현한다.

검증 선택과 command mapping의 단일 machine owner는
`validation/registry.json`이다. 개별 validator는 자기 진단 의미를 소유하며,
`validate-repo-quality-gates.sh`와 `run-validation-lane.py`는 선택된 owner를
호출하고 결과를 정규화한다. production module은 top-level `tests/`를 import하거나
`tests/fixtures/`를 runtime input으로 읽지 않는다.

### Audience

- Platform maintainers
- Quality engineers
- Documentation maintainers
- AI agents

### Scope

#### In Scope

- document profile, lifecycle, link, owner, and archive validation
- Agent registry, provider projection, loop, and CI contract validation
- affected/staged/all-files routing and bounded subprocess execution
- GitOps, Kubernetes, Vault/ESO, GitHub Actions, and CI Python checks
- repository-wide contracts that do not yet have a narrower focused owner

#### Out of Scope

- hosted CI, branch-protection, provider-runtime, credential, deployment, or live-cluster evidence
- test fixtures, synthetic mutations, or fixed negative-case inventories
- branch-tip, current-document, current-script, line-number, or corpus-count pins
- policy prose duplicated from Stage 00, SDLC stages, or Operations

## Structure

### Routing and orchestration

| Path | Responsibility |
| --- | --- |
| `validation/registry.json` and `validation/registry.schema.json` | validator, surface, lane, argument, fallback, and CI routing contract |
| `select-affected-surfaces.py` | pure path-to-surface selection projection |
| `validate-affected-surfaces.py` | registry and tracked-path coverage validation |
| `run-validation-lane.py` | bounded execution and result normalization for affected, staged, and all-files lanes |
| `validate-repo-quality-gates.sh` | dependency preflight plus one registry-owned `all-files` runner invocation; contains no validator argv or rule implementation |
| `validation/repository/quality.py` | repository-wide rules not already owned by a focused validator |
| `validation/current_executable_references.py` | current executable target and Git-first historical recovery distinction |

### Document and archive owners

| Path family | Responsibility |
| --- | --- |
| `document_contracts.py`, `validate-document-contract-registry.py`, `validate-markdown-profiles.py` | route/profile classification and authored Markdown semantics |
| `document_authority.py`, `validate-links-and-owners.py` | current owner and cross-document relation semantics |
| `document_lifecycle.py`, `validate-document-lifecycle.py` | registry-classified lifecycle and staged-index transitions |
| `archive_recovery.py`, `archive_validation.py`, `archive_cutover.py`, `archive_cutover_manifest.py` | bounded historical recovery and sealed Archive checks |
| `json_schema_validation.py` | offline JSON Schema loading shared by production validators |

### Agent governance owners

| Path | Responsibility |
| --- | --- |
| `agent_registry_loader.py` | bounded Stage 00 role-registry loading shared by governance validation |
| `validate-agent-governance.py` | role/schema, native metadata, permission, skill, and consumer integrity |
| `agent_governance_consumers.py` | bounded current-consumer and Git-backed historical recovery checks |

### Platform and supply-chain owners

| Path | Responsibility |
| --- | --- |
| `validate-gitops-change-set.py`, `validate-gitops-structure.sh` | GitOps identity and structure validation |
| `validate-k8s-manifests.sh`, `validate-policy-gates.sh` | manifest syntax and repository policy checks |
| `validate-vault-eso-contracts.py`, `check-secret-handling.sh` | Vault/ESO reference contracts and redacted secret-pattern checks |
| `validate-github-actions-security.py`, `validate-ci-python-contract.py` | workflow supply-chain and Python dependency contracts |
| `validate-workspace-boundary.py` | staged workspace boundary and ignored-path contract |
| `validate-harness.sh` | thin manual dispatcher for the retained harness-focused checks |
| `render-platform-chart-kinds.sh` | operator-invoked chart-kind review helper |

## Configuration Boundary

- Document route/profile values come only from `docs/99.templates/registry.json`.
- Agent roles, permissions, skills, handoffs, and projections come only from
  `.agents/roles/registry.json`.
- Validation selection and command arguments come only from
  `scripts/validation/registry.json`.
- `.github/workflows/ci.yml` and `.pre-commit-config.yaml` are projections and
  must not introduce an undeclared validator or duplicate rule owner.
- Claude write-boundary enforcement lives in `.claude/hooks/`; provider settings
  register the native event. Quality validation is an explicit QA operation.
- Tests and bounded synthetic data remain under `tests/` and `tests/fixtures/`.
- Git history is the default recovery source. Only externally immutable
  dependency identity or sealed historical recovery coordinates justify a digest.

All subprocess calls from Python validators use a finite timeout. Text inputs
are read as explicit UTF-8, symlink/non-regular boundaries fail closed where
the owning contract requires them, and diagnostics avoid secret values.

## Validation

Run the smallest owner first, then the affected/staged lane required by the
current work, and finally the aggregate when closing a logical unit.

```bash
python3 -m unittest tests.test_validation_tooling_ownership
python3 scripts/validate-affected-surfaces.py --root .
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-agent-governance.py --root .
bash scripts/validate-repo-quality-gates.sh .
git diff --check
```

The aggregate command discovers tracked paths internally. Direct affected or
staged lane calls continue to require an explicit bounded NUL path file.

For an explicit NUL-delimited changed-path set:

```bash
python3 scripts/run-validation-lane.py \
  --root . \
  --lane affected \
  --paths-file /tmp/hy-home-k8s-paths.nul \
  --delimiter nul
```

Repository-static PASS proves only the checked repository state. It does not
prove hosted execution, native provider enforcement, credentials, remote state,
deployment, or live-cluster behavior.

## Operations

### Working Procedure

1. Locate the rule in `validation/registry.json` and its focused semantic owner.
2. Add or adapt an independent top-level test before changing behavior.
3. Keep production data beside its production owner; keep synthetic data under
   `tests/fixtures/` with an independent test consumer.
4. Add a validator to one routing owner and project it into hook/CI only where
   the declared lanes require it.
5. Retire a wrapper only after current-consumer-zero and
   unique-diagnostic-zero evidence; use Git for recovery rather than a redirect.
6. Review `git diff --check`, the relevant focused suite, affected/staged
   selection, and the aggregate before commit.

Do not create a compatibility CLI, duplicate registry, fixed script inventory,
or embedded mutation suite merely to preserve a retired implementation shape.
The observed required external CI check name is `ci-summary`; local workflow
changes preserve that name. No remote branch-protection setting is changed.

## Related Documents

- [Agent execution policy](../.agents/governance/agent-execution.md)
- [Quality policy](../.agents/governance/quality.md)
- [Document authoring policy](../.agents/governance/document-authoring.md)
- [Validation ownership ADR](../docs/02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md)
- [Validation tooling Spec](../docs/98.archive/completed/03.specs/0066-validation-tooling-ownership/spec.md)
- [Validation tooling Task](../docs/98.archive/completed/03.specs/0066-validation-tooling-ownership/tasks/tsk-0001-vto-000.md)
- [Tests](../tests/README.md)
