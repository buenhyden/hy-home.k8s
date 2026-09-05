---
title: "Workspace Agent Governance Platform Architecture Description"
version: "1.0.0"
type: "sdlc/architecture-description"
status: "active"
owner: "platform"
updated: "2026-09-05"
layer: "architecture"
artifact_id: "AD-0006"
---

# Workspace Agent Governance Platform Architecture Description (AD)

## Overview

이 문서는 Stage 00 공통 거버넌스, Claude/Codex 어댑터, 공통 QA와 GitOps 운영의
책임 경계를 설명한다. [ADR-0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md)가
설계를, [SPEC-0072](../../03.specs/0072-agent-governance-and-quality-gate-consolidation/spec.md)가
전환과 수용 조건을 소유한다. 파일의 존재는 설치된 런타임의 탐색·권한 강제나
호스팅 CI의 성공을 입증하지 않는다. 실제 검증 상태는 해당 Task에서 확인한다.

## Boundaries & Non-goals

- Stage 00은 공통 정책·역할·스킬 의미와 역할 메타데이터를 소유한다.
- Stage 99는 문서 프로필과 양식을 소유하며 역할 권한이나 실행 성공을 정의하지 않는다.
- 실행 레지스트리와 scripts는 검사 선택, 실행 한도, 실패 처리를 소유한다.
- Provider 계정·인증·모델 접근 권한과 전역 설치는 저장소가 소유하지 않는다.
- GitOps desired state, Kubernetes 정책, 외부 서비스 인터페이스는 기존 도메인에 둔다.

## Quality Attributes

| Attribute | Architecture requirement | Evidence |
| --- | --- | --- |
| Consistency | Common meaning and machine field each have one owner | Role/schema/reference checks and profile routing |
| Security | Native permissions do not exceed registered scope; external mutation needs approval | Independent permission/path rejection tests and native evidence when authorized |
| Reliability | Commands have finite time/output limits and descendant cleanup | Bounded-runner timeout, overflow, cancellation, and pipe regressions |
| Recoverability | Work evidence preserves inputs, failures, ownership, and next action | Task/Git trace; isolated archive recovery checks |
| Reproducibility | Local full and CI share logical gates and configuration | Profile parity, single execution, interpreter and dependency checks |
| Legibility | Gateways point to common owners without copied policy bodies | Native syntax parse and canonical-reference tests |

## System Overview & Context

| Component | Canonical owner | Responsibility |
| --- | --- | --- |
| Entry | Root `AGENTS.md` and `CLAUDE.md` | Explicitly select common policy and relevant procedures |
| Policy | `docs/00.agent-governance/policies/` | Approval, security, Git, document and quality meaning |
| Role metadata | `docs/00.agent-governance/roles/registry.json` and adjacent schema | Stable IDs, permissions, handoffs, skill and adapter references |
| Role bodies and procedures | Stage 00 `roles/` and `skills/` | Neutral responsibilities and reusable work steps |
| Provider contract | Stage 00 `providers/` | Supported native syntax, loading route, and evidence limits |
| Native adapters | `.claude/` and `.codex/` | Native metadata and explicit common references |
| QA execution | `scripts/qa.py`, validation registry and bounded runner | Profile selection, one execution per gate/input, fail-closed results |
| Change evidence | Stage 03 Task and Git | Actual commands, scope, failures, limitations and handoff |

Claude exposes native `SKILL.md` packages through its repository skill link.
Codex explicitly reads the referenced Stage 00 procedure; `.codex/skills` is
not treated as automatic discovery. No repository `.agents/` compatibility
folder or renderer is required. A native hook is registered only for an actual
supported event; routine tool completion does not invoke whole-repository QA.

## Data Architecture

Role metadata references canonical role bodies and skill IDs; it does not copy
policy prose. Provider files retain native format and model bindings. Static
metadata validation cannot prove account availability or authenticated execution.

QA profiles contain gate IDs. The execution registry alone owns commands and
selection configuration; the runner owns bounded process handling. Quick checks
working-tree changes, full checks the final working tree, and staged validation
checks the real index in an isolated snapshot. CI checks its immutable checkout.
Snapshot preparation preserves Git history for recovery while keeping the user's
index and working files unchanged.

Historical facts remain in Git or isolated retained records. Active policy,
provider loading, and command selection do not consume a retired proposal as
current authority. Test fixtures are bounded synthetic inputs, never production
configuration or runtime admission evidence.

## Infrastructure & Deployment

GitHub Actions validates repository bytes through the common QA entrypoint.
`ci-summary` retains its externally observed check name and propagates failure,
cancellation, missing results, and unexpected skips. Static QA uses pinned tools
and minimal permissions; it does not need provider credentials or a cluster.

Argo CD reconciles `gitops/` desired state within the existing operating boundary.
`infrastructure/` supplies bootstrap support, `traefik/` carries integration
references, and `examples/` contains examples. `policy/` is Kubernetes
Conftest/Rego policy, separate from common agent policy. External Vault,
PostgreSQL, and Valkey remain interface contracts, not services operated by QA.

A local commit does not authorize push, PR creation, workflow dispatch, release,
cluster mutation, or external service changes. Hosted, native provider, and live
verification require their own actual evidence and applicable authorization.

## Traceability

### Lifecycle Traceability

The existing requirement IDs retain their identity. ADR-0034 and SPEC-0072
own the current governance and QA implementation; predecessor decisions remain
historical evidence rather than parallel operating instructions.

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Stage 00 durable policy와 owner graph | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | Thin gateway와 provider projection | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-FR-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) | Skill provenance와 gap evidence | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-FR-0004](../../01.requirements/0003-workspace-agent-governance-platform.md) | Strategy axis와 scope owner | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-FR-0005](../../01.requirements/0003-workspace-agent-governance-platform.md) | Execution/checkpoint/handoff evidence | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-FR-0006](../../01.requirements/0003-workspace-agent-governance-platform.md) | Form/profile와 routing contract | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | GitOps, secret, privilege와 approval boundary | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-FR-0008](../../01.requirements/0003-workspace-agent-governance-platform.md) | Registry-derived admitted-provider projection | [ADR 0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| [REQ-0003-FR-0009](../../01.requirements/0003-workspace-agent-governance-platform.md) | Provider schema/model/effort/MCP와 canary | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-FR-0010](../../01.requirements/0003-workspace-agent-governance-platform.md) | Machine harness contract/schema | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-FR-0011](../../01.requirements/0003-workspace-agent-governance-platform.md) | Bounded loop/checkpoint/compaction | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-NFR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Registry-derived parity and eval/admission | [ADR 0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | CI/QA/all-files evidence | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-IF-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Legacy cutover/current-owner integrity | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-IF-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | Evidence-only external role admission | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 01](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Owner graph consistency | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 02](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Reciprocal lifecycle chain | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 03](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Gateway/evidence-class separation | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 04](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Repository static gate | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 05](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Template form authority | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 06](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Registry-derived role/provider parity | [ADR 0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| N/A — [Acceptance criterion 07](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Admitted-provider independent canary classification and readiness evidence | [ADR 0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| N/A — [Acceptance criterion 08](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Contract/schema/provider parity | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 09](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Recovery fixture and safe resume | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 10](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Eval/model-fitness evidence | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 11](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | CI and all-files gate | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 12](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Zero stale legacy/orphan reference | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |

- **Requirement Package**: [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)
- **Current decision**: [ADR-0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md)
- **Current implementation**: [SPEC-0072](../../03.specs/0072-agent-governance-and-quality-gate-consolidation/spec.md)
- **Wider SDLC program**: [SPEC-0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md)
- **Historical decisions**: [ADR-0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md), [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)

The prior architecture narrative is recoverable from this same path at commit
`bb73116b7b09c4f257fc81baa12cfa8359495fc0`. Its retired providers, fixed retry
counts, synthetic runtime records, and separate agent CI topology are not
current contracts.
