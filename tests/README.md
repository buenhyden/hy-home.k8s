---
title: "tests"
version: "0.1.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-04"
---
# tests

## Overview

`tests/`는 repository validation code의 독립 behavior coverage와 synthetic
fixtures를 소유한다. production validator는 현재 저장소 상태만 검사하고,
이 폴더의 테스트가 mutation, malformed input, timeout, staged-index ambiguity,
consumer-zero, and failure-diagnostic cases를 구성한다.

이 폴더의 PASS는 repository-static evidence다. hosted CI, provider runtime,
credentials, deployment, remote state, 또는 live cluster readiness를 주장하지
않는다.

### Audience

- Quality engineers
- Platform maintainers
- Validator authors
- AI agents

### Scope

#### In Scope

- production module의 공개 함수·CLI·diagnostic behavior 회귀
- temporary repository와 synthetic mutation을 사용한 실패 경계 검증
- staged index와 worktree authority 구분
- fixture consumer ownership과 orphan fixture 방지
- hooks, routing, document, archive, Agent, CI, and GitOps static contracts

#### Out of Scope

- production runtime data API
- 고정 test-case 수 또는 fixture 수 정책
- secret, credential, kubeconfig, provider token, or live diagnostics
- live cluster bootstrap, ArgoCD sync, Vault mutation, remote CI rerun

## Structure

### Test families

| Family | Representative modules |
| --- | --- |
| Validation ownership and routing | `test_validation_tooling_ownership.py`, `test_affected_surface_migration.py`, `test_validate_affected_surfaces.py`, `test_run_validation_lane.py`, `test_current_executable_references.py` |
| Document contracts and lifecycle | `test_document_strict_cutover.py`, `test_document_lifecycle_migration.py`, `test_document_lifecycle_cumulative_history.py`, `test_document_lifecycle_archive_cutover.py`, `test_document_lifecycle_agent_roster_cutover.py`, `test_reference_pack_routes.py` |
| Archive and recovery | `test_archive_recovery.py`, `test_archive_validation.py`, `test_archive_cutover.py`, `test_archive_historical_proof.py`, `test_generic_migration_recovery.py` |
| Agent governance | `test_validate_agent_registry.py`, `test_validate_agent_harness_contract.py`, `test_validate_agent_harness_semantics.py`, `test_validate_agent_governance_ci.py`, `test_validate_agent_legacy_cutover.py`, `test_validate_agent_loop_lifecycle.py`, `test_validate_agent_checkpoint.py`, `test_validate_agent_provider_config.py`, `test_validate_agent_provider_canaries.py`, `test_validate_agent_core_cutover.py`, `test_delegated_execution_ownership.py` |
| CI, GitOps, Vault, and workspace | `test_validate_ci_python_contract.py`, `test_validate_github_actions_security.py`, `test_validate_gitops_change_set.py`, `test_validate_vault_eso_contracts.py`, `test_workspace_boundary.py` |
| Hook boundaries | `test_k8s_pre_edit_hook.py`, `test_provider_post_validate_hook.py`, `test_post_validate_runner_result.py` |
| Migration tooling | `test_migrate_document_work_units.py` |

### Fixture families

| Fixture | Independent consumer |
| --- | --- |
| `fixtures/agent-checkpoint.json` | `test_validate_agent_checkpoint.py` |
| `fixtures/agent-governance-ci.json` | `test_validate_agent_governance_ci.py` |
| `fixtures/agent-loop-lifecycle.json` | `test_validate_agent_loop_lifecycle.py` |
| `fixtures/agent-provider-runtime-evidence.json` | Agent provider evidence tests |
| `fixtures/github-actions-security.json` | `test_validate_github_actions_security.py` |
| `fixtures/gitops-change-set/` | `test_validate_gitops_change_set.py` |
| `fixtures/validation-surfaces.json` | `test_validate_affected_surfaces.py` and routing migration tests |
| `fixtures/vault-eso-contracts.json` | `test_validate_vault_eso_contracts.py` |

Fixtures are bounded examples, not production registries. A fixture remains
only while an independent test consumes it; combinations should normally be
generated in temporary directories instead of expanding a permanent matrix.

## Configuration Boundary

- Tests may import production modules from `scripts/`; the reverse dependency
  is forbidden.
- Tests may read `tests/fixtures/`; production modules may not.
- Temporary Git repositories and directories must be disposable and contain no
  credentials or user data.
- Network, provider authentication, hosted CI mutation, and live cluster access
  are outside the default test boundary.
- Assertions target behavior, diagnostic IDs, and semantic ownership rather
  than permanent file counts, line counts, current SHA values, or mutation counts.

## Validation

Run focused suites before broad discovery:

```bash
python3 -m unittest tests.test_reference_pack_routes
python3 -m unittest tests.test_validation_tooling_ownership
python3 -m unittest tests.test_validate_affected_surfaces tests.test_run_validation_lane
python3 -m unittest tests.test_validate_agent_governance_ci
python3 -m unittest tests.test_document_strict_cutover
python3 -m unittest discover --start-directory tests --top-level-directory tests --pattern 'test_*.py'
bash scripts/validate-repo-quality-gates.sh .
git diff --check
```

The completion order and PASS/FAIL/SKIP/DEFER meanings are owned by the
[Quality policy](../docs/00.agent-governance/policies/quality.md). This README
lists current test entrypoints but does not redefine that policy.

## Operations

### Working Procedure

1. Reproduce a defect in the narrowest independent test.
2. Use temporary data for a one-off mutation; add a persistent fixture only
   when several cases share a durable semantic input.
3. Make the production change without importing or reading this tree.
4. Run the focused suite, ownership checks, affected/staged validation, and
   broad validation required by the changed surface.
5. Remove a fixture when its last independent consumer is retired.
6. Report unavailable hosted/provider/live checks as `DEFER`, never as local PASS.

Test modules may be added, merged, or retired as responsibilities change.
Their count and exact method inventory are observations, not governance.

## Related Documents

- [Scripts](../scripts/README.md)
- [Quality policy](../docs/00.agent-governance/policies/quality.md)
- [Work lifecycle](../docs/00.agent-governance/skills/work-lifecycle.md)
- [Validation ownership ADR](../docs/02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md)
- [Validation tooling Spec](../docs/98.archive/completed/03.specs/0066-validation-tooling-ownership/spec.md)
- [Validation tooling Task](../docs/98.archive/completed/03.specs/0066-validation-tooling-ownership/tasks/tsk-0001-vto-000.md)
