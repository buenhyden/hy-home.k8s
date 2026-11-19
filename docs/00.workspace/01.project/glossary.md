---
title: "K8s Workspace Vocabulary"
version: "2.1.0"
type: "governance/vocabulary"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# Repository Vocabulary

## Purpose

이 저장소의 Kubernetes와 GitOps 작업에서 쓰는 로컬 용어의 의미를 정의한다. 공통 작업·거버넌스 어휘의 단일 소유자는 [Common Repository Vocabulary](../../../.agents/knowledge/glossary.md)다. 각 행의 소유자 링크가 구체적 구조와 운영 규칙을 맡는다.

## Scope

이 문서는 이 저장소의 로컬 k3d 클러스터, kubeconfig context, Kubernetes namespace, Argo CD Application을 가리키는 말만 정의한다. 같은 단어가 다른 시스템에서 쓰일 때 아래의 범위가 그 뜻을 제한한다. 공통 TERM ID, 승인·실행 규칙, live 상태 주장은 범위 밖이다.

## Normative Language

대문자 MUST, MUST NOT, SHOULD, MAY는 RFC 2119와 RFC 8174의 읽기 규칙을 따른다. 이 문서는 뜻을 설명하며 표현 자체로 권한을 만들지 않는다.

## Repository Vocabulary

| Term ID | Term | Korean | Definition | Not to Confuse | Policy Owner | Contract Version |
| --- | --- | --- | --- | --- | --- | --- |
| TERM-K8S-CLUSTER | Cluster | 클러스터 | 이 저장소의 범위에서는 Linux 서버의 k3d `hyhome` 클러스터와 그 선언된 Kubernetes 자원 집합. | 다른 환경의 클러스터 또는 현재 live 상태 | [Local GitOps platform architecture](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md) | 1.0.0 |
| TERM-K8S-CONTEXT | Context | 쿠버네티스 컨텍스트 | 이 저장소의 로컬 클러스터를 대상으로 선택하는 kubeconfig의 연결·인증·namespace 조합. | 대화 세션의 문맥 또는 접근 승인 | [Bootstrap runbook](../../05.operations/03.runbooks/0001-argocd-platform-bootstrap-runbook.md) | 1.0.0 |
| TERM-K8S-NAMESPACE | Namespace | 네임스페이스 | 이 저장소가 선언한 클러스터 안에서 자원을 구분하는 Kubernetes 논리 범위. | 저장소 디렉터리 또는 보안 경계 전체 | [Local GitOps platform architecture](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md) | 1.0.0 |
| TERM-K8S-APPLICATION | Application | 애플리케이션 | 이 저장소의 범위에서는 root, platform 또는 workload의 원하는 상태를 조정하는 Argo CD Application 자원. | 제품 기능 또는 실행 중인 Pod 하나 | [Local GitOps platform architecture](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md) | 1.0.0 |

## Local Extensions

추가 로컬 확장은 없다. 공통 용어는 [공통 용어집](../../../.agents/knowledge/glossary.md)에서 읽는다.

## Maintenance

로컬 의미 변경은 연결된 구조·운영 소유자의 실제 선언을 확인하고 이 행의 ID와 계약 판본을 관리한다. Stage 99 profile과 링크·소유자·knowledge 검사는 문서 구조와 경로를 확인하며 live 클러스터 상태나 사용자 인수를 대신하지 않는다.

## References

- [공통 용어집](../../../.agents/knowledge/glossary.md)
- [용어집 profile과 양식 안내](../../99.templates/README.md)
- [Local GitOps platform architecture](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md)
- [Bootstrap runbook](../../05.operations/03.runbooks/0001-argocd-platform-bootstrap-runbook.md)
