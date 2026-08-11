# 02.architecture/descriptions (AD)

> PRD를 시스템 경계, 품질 속성, 참조 아키텍처 요구로 확장하는 AD stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

이 경로는 PRD 요구를 시스템 경계, 품질 속성, 데이터 흐름, 보안·관측성·운영성 요구로 확장하는 AD(Architecture Description) stage다.
여기서 정의한 아키텍처 관점은 ADR과 Spec의 상위 입력으로 사용된다.

AD는 참조 아키텍처와 품질 속성을 설명한다. 단일 기술 선택 자체는 `../decisions/`의 ADR에 남기고,
파일 단위 구현 설계나 운영 명령 절차는 각각 `../../03.specs/`, `../../05.operations/`로 넘긴다.

### Collection Readers

이 README의 주요 독자:

- Platform Architects
- Platform Engineers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 시스템 경계와 책임
- 품질 속성, 데이터 흐름, 보안/관측성/운영성 요구
- 참조 아키텍처와 하위 ADR/Spec 링크

### Out of Scope

- 단일 기술 결정 기록
- 세부 구현 파일 설계
- 운영 명령 절차

## Item Index

```text
02.architecture/descriptions/
├── ad-0004-argo-rollouts-progressive-delivery.md
├── ad-0005-argo-notifications-slack.md
├── ad-0006-workspace-agent-governance-platform.md
├── ad-0007-current-local-gitops-platform.md
├── ad-0008-workspace-document-assurance-operating-model.md
├── ad-0009-document-lifecycle-evidence-operating-model.md
├── ad-0010-repository-delivery-evidence-architecture.md
├── ad-0011-document-taxonomy-consolidation-architecture.md
└── README.md
```

## Add and Find

1. 관련 `01.requirements/` 문서를 먼저 읽어 요구사항 경계를 고정한다.
2. 새 AD는 `../../99.templates/templates/sdlc/architecture/ad.template.md`에서 시작하고, canonical target pattern은 `docs/02.architecture/descriptions/ad-####-<system-or-domain>.md`다.
3. 주요 설계 결정은 `02.architecture/decisions/`에 별도 ADR로 연결한다.
4. 현재 구현과 상충하는 old/superseded AD는 full-body Archive Record로 보존하고 `../../98.archive/README.md`에만 인덱싱하며, 활성 AD는 개별 record에 직접 연결하지 않는다.
5. 구현 가능한 계약은 `03.specs/`로 내려보내고 양방향 링크를 유지한다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/02.architecture/descriptions/`다.

- 같은 폴더의 AD 문서는 `./`로 시작한다.
- sibling ADR stage는 `../decisions/`로 연결한다.
- upstream/downstream docs stage는 `../../01.requirements/`, `../../03.specs/`, `../../04.execution/`, `../../05.operations/`로 연결한다.
- 새 AD의 실제 Markdown 링크는 최종 AD 파일 위치 기준으로 다시 계산하고, placeholder target은 code literal로 남긴다.

### Current AD Index

| 문서 | 역할 | 문서 상태 | 현재성 | 다음 단계 |
| --- | --- | --- | --- | --- |
| [`./ad-0004-argo-rollouts-progressive-delivery.md`](./ad-0004-argo-rollouts-progressive-delivery.md) | Argo Rollouts 점진적 배포 참조 아키텍처 | Active | Current-contract backfill. `platform-rollouts` Application, dashboard, metrics, AppProject 경계를 소유한다. | [`../../03.specs/004-argo-rollouts-progressive-delivery/spec.md`](../../03.specs/004-argo-rollouts-progressive-delivery/spec.md) |
| [`./ad-0005-argo-notifications-slack.md`](./ad-0005-argo-notifications-slack.md) | ArgoCD Notifications Slack 알림 참조 아키텍처 | Active | Current-contract backfill. ArgoCD Notifications와 Vault/ESO credential 경계를 소유한다. | [`../../03.specs/005-argo-notifications-slack/spec.md`](../../03.specs/005-argo-notifications-slack/spec.md) |
| [`./ad-0006-workspace-agent-governance-platform.md`](./ad-0006-workspace-agent-governance-platform.md) | Workspace AI Agent governance, provider-native harness, loop, model, and evidence reference architecture | Active | Accepted current ADR-0019의 local/Antigravity·Claude·Codex·Gemini native surface, 12-role/48-adapter target, bounded loop, eval, CI/QA 및 독립 provider-runtime evidence architecture를 정의한다. ADR-0013은 earlier tranche의 accepted historical predecessor다. | [`ADR-0019 (accepted current)`](../decisions/0019-provider-native-agent-harness-and-loop-model.md); [`ADR-0013 (accepted historical predecessor)`](../decisions/0013-stage-00-canonical-adapter-model.md) |
| [`./ad-0007-current-local-gitops-platform.md`](./ad-0007-current-local-gitops-platform.md) | 현재 local GitOps platform reference architecture | Active | Current repo-backed baseline. Headlamp, ingress-nginx, ArgoCD App-of-Apps, ESO/Vault, external services, Kiali/Istio, Rollouts, Notifications, monitoring, adminer 경계를 소유한다. | [`../../03.specs/008-current-local-gitops-platform/spec.md`](../../03.specs/008-current-local-gitops-platform/spec.md) |
| [`./ad-0008-workspace-document-assurance-operating-model.md`](./ad-0008-workspace-document-assurance-operating-model.md) | Workspace document assurance 운영 모델 | Accepted | Registry, template, authored document, validation, CI/QA, provider, protected-surface 책임과 데이터 흐름을 정의한다. | [`../../03.specs/026-document-contract-registry/spec.md`](../../03.specs/026-document-contract-registry/spec.md) |
| [`./ad-0009-document-lifecycle-evidence-operating-model.md`](./ad-0009-document-lifecycle-evidence-operating-model.md) | Document lifecycle, full-body archive, reference currentness, and QA evidence 운영 모델 | Accepted | 2026-07-28 exact terminal closure commit `c5adc27b13893d7cbd1266c9225372cfb7df79e9`에서 Specs 034–040 repository-static contract와 `0/0·6/3·3` frontier를 종료하고, reciprocal accepted ADR-0020을 same-diff role-decision evidence로 사용한다. Parent `35d8552ba423e3e2d92294ddeb81674392b8f333`부터 closure까지 explicit-ref와 clean-tree aggregate는 PASS이며 external security/provider/remote/live evidence는 `DEFER`다. | [`ADR-0020`](../decisions/0020-document-lifecycle-program-closure-evidence.md) 및 [`Spec 040`](../../03.specs/040-contract-cutover-and-program-closure/spec.md) |
| [`./ad-0010-repository-delivery-evidence-architecture.md`](./ad-0010-repository-delivery-evidence-architecture.md) | Repository delivery routing, layered validation evidence, and local integration reference architecture | Active | Existing validation-surface and platform topology owners remain canonical; two reference-based machine contracts close GitHub projection and platform evidence-depth gaps. | [`ADR-0021`](../decisions/0021-canonical-surface-routing-and-evidence-depth.md), active Spec 047 및 planned Specs 048–051 |
| [`./ad-0011-document-taxonomy-consolidation-architecture.md`](./ad-0011-document-taxonomy-consolidation-architecture.md) | Document taxonomy, governance authority, AI-agent control, and validator topology reference architecture | Active | Stage 03 work unit, stable Stage 05, registry-owned lineage, fail-closed route transition, Archive/observation integrity, harness-contract 확장 및 validator 의미 보존을 정의한다. | [`ADR-0024 (accepted current)`](../decisions/0024-terminal-artifact-identity-and-archive-layout.md), [`ADR-0023 (transition predecessor)`](../decisions/0023-work-unit-document-taxonomy-and-governance-authority.md), [`Spec 052`](../../03.specs/052-document-taxonomy-consolidation/spec.md) |

## Related Documents

- [Architecture README](../README.md)
- [01.requirements](../../01.requirements/README.md)
- [02.architecture/decisions](../decisions/README.md)
- [03.specs](../../03.specs/README.md)
- [99.templates AD Template](../../99.templates/templates/sdlc/architecture/ad.template.md)
- [Archive Index](../../98.archive/README.md)
