# 03. ADR (Architecture Decision Records)

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## 목적

이 폴더는 아키텍처 결정 기록(Architecture Decision Record, ADR)을 저장한다. ADR은 중요한 기술·아키텍처 결정 1건을 1문서로 기록한다.

## 포함할 내용

- 맥락(Context)
- 결정(Decision)
- 비목표(Non-goals)
- 대안(Alternatives)
- 결과(Consequences)
- 관련 PRD/ARD/Spec/Plan/기타 ADR 링크

## 포함하지 말아야 할 내용

- 상세 구현 설계
- 운영 절차
- 장문의 제품 배경 설명

## Agent 관련 ADR 예시

- 모델 선택
- Tool Gating
- Guardrail 전략
- Planner-Executor 채택 여부
- Fallback 모델 정책

## Templates

- `../99.templates/adr.template.md`

## 문서 인덱스

| 문서 | 설명 | 상태 | 최종 수정 |
| --- | --- | --- | --- |
| [`0001-k3d-topology-and-network.md`](./0001-k3d-topology-and-network.md) | k3d 토폴로지와 외부 네트워크 기준 결정 | Accepted | 2026-03-27 |
| [`0002-argocd-helm-and-gitops-model.md`](./0002-argocd-helm-and-gitops-model.md) | ArgoCD Helm 설치와 GitOps 모델 결정 | Accepted | 2026-03-27 |
| [`0003-eso-vault-k8s-auth.md`](./0003-eso-vault-k8s-auth.md) | ESO + Vault Kubernetes Auth 시크릿 패턴 결정 | Accepted | 2026-03-27 |
| [`0004-external-services-endpoints-and-valkey-backend.md`](./0004-external-services-endpoints-and-valkey-backend.md) | 외부 서비스 접근 모델(PostgreSQL EndpointSlice, Valkey ExternalName, Vault 외부 URL)과 ArgoCD Valkey 백엔드 결정 | Accepted | 2026-03-27 |
| [`0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](./0005-wsl2-ha-baseline-and-external-endpoint-contract.md) | Valkey EndpointSlice 전환 + ArgoCD TLS/Traefik 443 계약 + AppProject/Vault 최소권한 기준 결정 | Accepted | 2026-03-28 |
