---
title: "scripts"
version: "0.3.1"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-09"
---
# scripts

## Overview

`scripts/`는 저장소의 문서, Agent governance, GitOps, CI, 보안 경계를
repository-static 방식으로 검증하는 실행 코드의 소유 경로다. 사람에게 보이는
규칙은 각 canonical 문서가 소유하고, 이 폴더는 그 규칙의 machine enforcement와
검증 routing만 구현한다.

검증 선택과 command mapping의 단일 machine owner는
`validation/registry.json`이다. 개별 validator는 자기 진단 의미를 소유하며,
`qa.py`와 `run-validation-lane.py`는 선택된 owner를
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
| `githooks/chained-hook.sh` and its `pre-commit`, `commit-msg`, `pre-push` links | run the user's global Git hook and then this workspace's, returning the first non-zero status |
| `validate-affected-surfaces.py` | registry and tracked-path coverage validation |
| `run-validation-lane.py` | bounded execution and result normalization for affected, staged, and all-files lanes |
| `qa.py` | supported QA entrypoint; resolves a profile's gate IDs from the registry and runs them over an isolated final-tree or exact-index snapshot; contains no validator argv or rule implementation |
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
| `run-agent-evaluations.py` | grades recorded agent responses against registry-derived criteria |

### Platform and supply-chain owners

| Path | Responsibility |
| --- | --- |
| `validate-gitops-change-set.py`, `validate-gitops-structure.sh` | GitOps identity and structure validation |
| `validate-k8s-manifests.sh`, `validate-policy-gates.sh` | manifest syntax and repository policy checks |
| `validate-infrastructure-contracts.sh` | repository-static infrastructure contract checks; the live cluster checks are `infrastructure/verify/` |
| `validate-vault-eso-contracts.py`, `check-secret-handling.sh` | Vault/ESO reference contracts and redacted secret-pattern checks |
| `validate-github-actions-security.py`, `validate-ci-python-contract.py` | workflow supply-chain and Python dependency contracts |
| `validate-workspace-boundary.py` | staged workspace boundary and ignored-path contract |
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
current work. Each local commit needs exact-index staged QA; full runs before
final handoff under the shared quality policy.

```bash
python3 -m unittest tests.test_validation_tooling_ownership
python3 scripts/validate-affected-surfaces.py --root .
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-agent-governance.py --root .
python3 scripts/qa.py full
git diff --check
```

QA selects tracked and applicable non-ignored untracked paths itself, including
hidden paths, deletions and renames. Use `qa.py quick` for working-tree changes
and `qa.py staged` for the exact index. The lower-level runner is a diagnostic
interface, not a substitute for QA snapshot isolation; its explicit path files
must be bounded and NUL-delimited.

### Reproducing the hosted dependency identity

Validators run under whichever interpreter invokes them, so a machine carrying
different library versions than CI can pass a gate that CI fails, and the
difference is invisible until a hosted run reports it. Reproduce the hosted
identity by consuming the same lock CI installs rather than by tracking a
version list here:

```bash
# Choose a task-owned environment outside the checkout being validated,
# under account-owned directories with no group/other write permission.
python3 -m venv "$VALIDATION_VENV"
"$VALIDATION_VENV/bin/python" -m pip install --disable-pip-version-check \
  --only-binary :all: --require-hashes \
  --requirement .github/requirements/ci-validation.txt
"$VALIDATION_VENV/bin/python" scripts/qa.py full
```

Set `VALIDATION_VENV` to the approved environment path first. The invoking
Python is preserved for Python gates. Other tools use fixed system paths;
pre-commit also permits a trusted interpreter-adjacent or exact account-owned
fallback. A repository-local venv or namespace-mapped ancestor ownership can
make that fallback differ: record the resolved executable, not just the venv
activation. Shell validators' `python3` follows the closed system PATH, so its
library identity also needs separate observation. HOME stays closed; reviewed
pre-commit/Go/Rust/Node caches stay under the account-owned cache directory.

Use this when a gate passes locally and fails hosted, or before changing a
module that a locked dependency owns. It is closer evidence than a local run,
and it is still local evidence: it proves nothing about the hosted runner.

Run formatters through `pre-commit` rather than invoking them directly. The
hook configuration narrows `ruff-format` to Python on purpose; the bare
command also claims Markdown and rewrites fenced snippets inside authored and
archived documents. Shfmt and whitespace fixes are also explicit `--files`
operations on reviewed source paths. Full/ci run the manual stage once in an
isolated snapshot: a formatter change fails validation. Commit-msg is separate;
follow the shared Git policy for the actual candidate message.

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
- Validation ownership ADR (`docs/02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md`)
- Validation tooling Spec (`docs/98.archive/completed/03.specs/0066-validation-tooling-ownership/spec.md`)
- Validation tooling Task (`docs/98.archive/completed/03.specs/0066-validation-tooling-ownership/tasks/tsk-0001-vto-000.md`)
- [Tests](../tests/README.md)
