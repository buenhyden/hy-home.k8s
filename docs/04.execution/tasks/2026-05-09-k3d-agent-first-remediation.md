---
title: 'Task: k3d Workspace and Agent-first Remediation'
type: task
status: done
owner: 'platform'
updated: 2026-05-22
---

# Task: k3d Workspace and Agent-first Remediation

## Overview (KR)

이 문서는 k3d 운영 문서와 Agent-first 실행 계약 보정 작업의 구현·검증 작업 목록이다.
Plan에서 파생된 작업을 추적 가능하게 기록한다.

2026-05-09 gateway/runtime audit 보정은 새 plan/task 문서를 만들지 않고 이 작업 문서에 누적한다. 현재 구조는 이미 thin gateway와 local harness runtime을 갖추고 있으므로, 보정 범위는 catalog clarity와 regression gate 강화로 제한한다.

2026-05-09 하네스/Agent-first 구성요소 추가 조사는 `harness-catalog.md`의 compact matrix와 `agentic.md`의 matrix-first/context hierarchy 규칙으로 추적한다. 새 runtime surface 또는 새 stage 문서는 만들지 않는다.

2026-05-09 command-boundary follow-up은 새 runtime surface 없이 기존 plan/task 문서에 누적한다. 목적은 authored docs의 위험 명령 예시가 Agent 기본 실행 경로로 해석되지 않도록 문서 문맥과 repo quality gate를 함께 고정하는 것이다.

2026-05-09 hardening follow-up은 완료 상태를 뒤집지 않고 보강한다. 추가 조사에서 확인된 gap은 `docs/05.operations/policies` risky-command gate 누락, 대화 출력에 의존하는 완료 증거, matrix 검증 범위의 과장 가능성, direct push 차단 표현의 범위 불일치다. Final multi-agent disposition은 REVISE 후 승인 가능이며, 남은 보강은 readiness 의미 축소, matrix gap 표현 가능성, validator 범위 정합성, 검증 증거의 snapshot 성격으로 제한한다.

2026-05-22 governance/docs/lifecycle follow-up은 `.agent-work/`를 제외한 tracked repository surface만 대상으로 한다. `docs/01~05` 검토 결과는 구조적 템플릿 coverage, lifecycle hook contract, governance/runtime 문서 정합성, repo-backed validation evidence로 이 문서에 누적한다.

2026-05-22 추가 요청에 따라 구조적 템플릿 누락 방지를 우선 구현했다. 품질 게이트는 이제 canonical authored stage의 비-README Markdown이 정확히 하나의 structural template mapping에 포함되는지 확인하고, 해당 mapping이 실제 템플릿 파일을 가리키는지도 검증한다.

## Inputs

- **Parent Spec**: not applicable; this remediation does not introduce a new technical contract.
- **Parent Plan**: [`../plans/2026-05-09-k3d-agent-first-remediation.md`](../plans/2026-05-09-k3d-agent-first-remediation.md)

## Working Rules

- Documentation-only work still needs validation evidence.
- No Kubernetes manifest change is included unless a new human-approved plan expands scope.
- Direct cluster mutation guidance must be marked as human-approved bootstrap/break-glass only.
- Agent execution must remain repo-backed and GitOps-first by default.
- This document remains the execution-tracking source of truth for this remediation.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Add remediation plan and task documents | doc | n/a | PLN-001 | Stage README indexes include new docs | Platform | Done |
| T-002 | Clarify direct `kubectl apply/patch` guidance as bootstrap/break-glass only | ops | n/a | PLN-002 | `rg` review plus repo quality gate | Platform | Done |
| T-003 | Strengthen current-contract language for Headlamp and `172.18.x` where touched | doc | n/a | PLN-003 | stale contract gate remains PASS | Platform | Done |
| T-004 | Add harness readiness matrix and Agent-first execution boundary | guardrail | n/a | PLN-004 | harness catalog checks remain PASS | Platform | Done |
| T-005 | Run repo-backed validation bundle | test | n/a | PLN-005 | validation command output reviewed | Platform | Done |
| T-006 | Clarify Claude permission hooks versus Codex context hook in the harness catalog | doc | n/a | PLN-006 | repo quality gate validates hook-boundary wording | Platform | Done |
| T-007 | Mark historical harness memory as an initial snapshot with current-source pointers | doc | n/a | PLN-006 | repo quality gate validates historical/current-source wording | Platform | Done |
| T-008 | Add gateway/runtime regression checks to repo quality gate | test | n/a | PLN-007 | gateway thinness, English-only governance/runtime, and hook-boundary checks pass | Platform | Done |
| T-009 | Add Harness Engineering and Agent-first Engineering component audit matrices | doc | n/a | PLN-008 | matrix headings and `Gap`/`Remediation` columns pass repo quality gate | Platform | Done |
| T-010 | Add matrix-first and context hierarchy rules for future harness changes | guardrail | n/a | PLN-009 | agentic rule phrases pass repo quality gate | Platform | Done |
| T-011 | Extend repo quality gate for component audit matrix presence | test | n/a | PLN-008, PLN-009 | quality gate fails if matrix or rule contracts are removed | Platform | Done |
| T-012 | Add authored-doc command-boundary regression gate | test | n/a | PLN-010 | quality gate rejects unmarked risky command examples, bare/main direct push examples, and push examples without PR-flow context | Platform | Done |
| T-013 | Mark authored-doc risky command examples with human/operator boundaries and PR flow | doc | n/a | PLN-010 | final `rg` review finds no unmarked risky command examples and no PR-flow-bypassing push examples | Platform | Done |
| T-014 | Include `docs/05.operations/policies` in risky-command boundary scanning | test | n/a | PLN-010 | quality gate scans operations policies for unmarked `kubectl apply/patch`, `argocd app sync`, and `vault kv put` examples | Platform | Done |
| T-015 | Add durable verification evidence summary | doc | n/a | PLN-011 | this task records date, command result, and skipped optional tool evidence | Platform | Done |
| T-016 | Validate matrix tables as structure/regression guards | test | n/a | PLN-008 | quality gate validates matrix header, row column count, and non-empty fields | Platform | Done |
| T-017 | Align push-example checks and wording with PR flow | test | n/a | PLN-010 | bare/main direct push and push examples without nearby PR-flow context fail | Platform | Done |
| T-018 | Add matrix status contract and future gap pathway | guardrail | n/a | PLN-012 | catalog limits matrix status to Ready/Partial/Missing and describes evidence lanes | Platform | Done |
| T-019 | Validate status/gap/remediation consistency | test | n/a | PLN-012 | quality gate allows Ready/Partial/Missing and requires concrete gaps for Partial/Missing rows | Platform | Done |
| T-020 | Align push-scope and verification snapshot wording | doc | n/a | PLN-011, PLN-013 | README and task summary distinguish authored-doc PR-flow checks from broader Markdown direct-push checks and mark validation as a dated snapshot | Platform | Done |
| T-021 | Keep provider hook enforcement semantics precise | guardrail | n/a | PLN-013 | agentic rule states Claude permissions/hooks and Codex context hook are not equivalent enforcement layers | Platform | Done |
| T-022 | Add structural template coverage checks to repo quality gate | test | n/a | PLN-014 | every non-README authored Markdown under `docs/01~05` and `docs/90.references` matches exactly one structural template mapping | Platform | Done |
| T-023 | Align template/governance/doc-writer guidance with structural template mapping | doc | n/a | PLN-014, PLN-017 | `docs/99.templates`, documentation rules, and doc-writer mirrors require exactly one mapping before authoring | Platform | Done |
| T-024 | Add lifecycle guard script and executable mode | tool | n/a | PLN-015 | `.claude/hooks/lifecycle-guard.sh` parses Stop/SubagentStop/PreCompact payloads and passes shell syntax | Platform | Done |
| T-025 | Wire lifecycle guard into Claude and Codex hook configs | guardrail | n/a | PLN-015 | `.claude/settings.json` and `.codex/hooks.json` include Stop, SubagentStop, and PreCompact lifecycle wiring | Platform | Done |
| T-026 | Simulate lifecycle hook clean, failing, and advisory payloads in quality gate | test | n/a | PLN-016 | quality gate verifies Stop/SubagentStop block forced failures and PreCompact remains advisory | Platform | Done |
| T-027 | Update governance/runtime documentation for lifecycle hook semantics | doc | n/a | PLN-017 | harness catalog, agentic rule, postflight checklist, provider notes, and runtime baseline describe lifecycle boundaries | Platform | Done |
| T-028 | Run 2026-05-22 validation bundle and record limitations | test | n/a | PLN-018 | verification summary records repo-backed checks and skipped optional/live checks | Platform | Done |

## Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`

## Agent-specific Types (If Applicable)

- `prompt`
- `tool`
- `memory`
- `guardrail`
- `eval`
- `observability`

## Phase View (Optional)

### Phase 1

- [x] T-001 Add remediation tracking documents
- [x] T-002 Clarify direct mutation boundaries
- [x] T-003 Strengthen current-contract language where touched
- [x] T-004 Add harness readiness matrix

### Phase 2

- [x] T-005 Run and record repo-backed validation bundle
- [x] T-006 Clarify hook boundary in harness catalog
- [x] T-007 Clarify historical memory current-source pointers
- [x] T-008 Add gateway/runtime regression checks
- [x] T-009 Add component audit matrices
- [x] T-010 Add matrix-first/context hierarchy rules
- [x] T-011 Extend component audit regression checks
- [x] T-012 Add authored-doc command-boundary regression gate
- [x] T-013 Mark authored-doc risky command examples
- [x] T-014 Include operations policies in risky-command scans
- [x] T-015 Add durable verification evidence summary
- [x] T-016 Validate matrix table structure and non-empty fields
- [x] T-017 Align push-example gate and wording with PR flow
- [x] T-018 Add matrix status contract and future gap pathway
- [x] T-019 Validate status/gap/remediation consistency
- [x] T-020 Align push-scope and verification snapshot wording
- [x] T-021 Keep provider hook enforcement semantics precise
- [x] T-022 Add structural template coverage checks
- [x] T-023 Align template/governance/doc-writer guidance
- [x] T-024 Add lifecycle guard script
- [x] T-025 Wire Claude/Codex lifecycle hooks
- [x] T-026 Simulate lifecycle hook payloads in quality gate
- [x] T-027 Update lifecycle governance/runtime docs
- [x] T-028 Run 2026-05-22 validation bundle

## Verification Summary

- **Test Commands**:
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `bash infrastructure/tests/verify-contracts-static.sh`
  - `bash scripts/validate-gitops-structure.sh`
  - `bash scripts/validate-k8s-manifests.sh .`
  - `bash scripts/check-secret-handling.sh .`
  - `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +`
  - `git diff --check`
  - Legacy external harness source-label scan across root gateways, `.claude`, `.codex`, and `docs/00.agent-governance`
  - Harness and Agent-first component matrix structure/regression check through `scripts/validate-repo-quality-gates.sh`
  - Authored-doc command-boundary regression check through `scripts/validate-repo-quality-gates.sh`, including `docs/05.operations/policies`
  - Push-example regression check through `scripts/validate-repo-quality-gates.sh`; authored docs reject bare/main direct push and push examples without nearby PR-flow context, while broader Markdown roots reject bare/main direct push examples
- **Eval Commands**: not applicable; no prompt/model behavior is changed.
- **Logs / Evidence Location**: repo-discoverable summary in this section. This is a 2026-05-09 execution snapshot, not proof of future CI/toolchain/live k3d/ArgoCD state. Rerun the validation bundle before using it for future handoff claims. Latest follow-up validation on 2026-05-09:
  - `bash scripts/validate-repo-quality-gates.sh .` — PASS after hardening edits.
  - `bash infrastructure/tests/verify-contracts-static.sh` — PASS.
  - `bash scripts/validate-gitops-structure.sh` — PASS.
  - `bash scripts/validate-k8s-manifests.sh .` — PASS for YAML syntax; `kube-linter` skipped because it is not installed locally.
  - `bash scripts/check-secret-handling.sh .` — PASS.
  - `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` — PASS.
  - `git diff --check` — PASS.
  - Targeted risky-command review — PASS through `scripts/validate-repo-quality-gates.sh`; `docs/05.operations/policies` is included in authored-doc scanning.
  - Targeted push-example review — PASS through `scripts/validate-repo-quality-gates.sh`; authored-doc feature-branch push examples carry nearby PR-flow context, authored docs reject bare/main direct push and push examples without PR-flow context, and broader Markdown roots reject bare/main direct push examples.
  - Targeted matrix status review — PASS through `scripts/validate-repo-quality-gates.sh`; `Ready` rows require `Gap=None`, while future `Partial`/`Missing` rows require concrete `Gap` and `Remediation`.
  - Authored SSoT rewrite boundary — unchanged; rewriting `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, or `docs/99.templates` outside the current command-boundary hardening scope requires separate human approval.
  - Targeted legacy external harness source-label scan — PASS; only validator sentinel definitions remain.
- Latest 2026-05-22 follow-up scope:
  - Structural template coverage was added to `scripts/validate-repo-quality-gates.sh`; canonical authored stage Markdown now fails if it is not covered by exactly one template mapping.
  - Stop/SubagentStop/PreCompact lifecycle hook wiring was added to Claude and Codex runtime configs.
  - `scripts/validate-repo-quality-gates.sh .` now simulates lifecycle clean/failing/advisory payloads.
  - `bash scripts/validate-repo-quality-gates.sh .` — PASS, including structural template coverage and lifecycle hook payload simulation.
  - `git diff --check` — PASS.
  - `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
  - `bash infrastructure/tests/verify-contracts-static.sh` — PASS.
  - `bash scripts/validate-gitops-structure.sh` — PASS.
  - `bash scripts/validate-k8s-manifests.sh .` — PASS for YAML syntax; optional `kube-linter` was skipped because it is not installed locally.
  - `bash scripts/check-secret-handling.sh .` — PASS.
  - `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` — PASS.
  - `python3 -m json.tool .claude/settings.json` and `python3 -m json.tool .codex/hooks.json` — PASS.
  - Direct lifecycle self-tests — clean Stop exited `0` with no block output; forced-failure Stop and SubagentStop emitted `decision=block`; PreCompact emitted `systemMessage` advisory and did not block.
  - `command -v rtk` — not found; direct repo-backed commands were used.
  - Live k3d/ArgoCD reconciliation, external Vault changes, plaintext secret creation, and GitHub settings/ruleset changes were not executed.

## Related Documents

- **Plan**: [`../plans/2026-05-09-k3d-agent-first-remediation.md`](../plans/2026-05-09-k3d-agent-first-remediation.md)
- **Governance**: [`../../00.agent-governance/harness-catalog.md`](../../00.agent-governance/harness-catalog.md)
- **Agent-first Rules**: [`../../00.agent-governance/rules/agentic.md`](../../00.agent-governance/rules/agentic.md)
