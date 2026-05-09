# Infrastructure to Theory: 2026 Learning Roadmap

## Overview (KR)

이 가이드는 `hy-home.k8s` 인프라 구축 경험을 바탕으로, 실무 기술이 어떤 컴퓨터 과학(CS) 및 공학(CE) 이론에 뿌리를 두고 있는지 연결합니다. 단순히 도구를 사용하는 법을 넘어, **"왜 이렇게 동작하는가?"**에 대한 해답을 찾는 여정입니다.

---

## Purpose

로컬 Kubernetes/GitOps/AI infrastructure 경험을 운영체제, 네트워크, 분산 시스템, 소프트웨어 공학 이론 학습으로 연결한다.

## Scope

- `hy-home.k8s`에서 사용하는 인프라 도구와 관련 CS/CE 이론 연결
- 개인 학습용 reading list와 미니 프로젝트 아이디어
- 운영 절차, 정책, 사고 대응, 버전 계약은 제외한다.

## Definitions / Facts

- **Reconciliation Loop**: 선언된 desired state와 실제 상태를 지속적으로 맞추는 제어 패턴이다.
- **Vector Indexing**: RAG 검색에서 고차원 벡터를 근사 탐색하는 자료구조/알고리즘 계열이다.
- **Virtual Memory Paging**: 제한된 물리 메모리를 페이지 단위로 관리하는 운영체제 메모리 모델이다.

## Sources

- Recommended Reading List의 논문과 이 저장소의 GitOps/observability 구현 경험을 학습 출발점으로 삼는다.

---

## Theoretical Mapping (Infrastructure -> CS Theory)

| Current Tool | Academic Domain | Key Concept | Reference |
| --- | --- | --- | --- |
| **k3d / Docker** | Operating Systems | Namespace & CGroups, Virtualization | OS virtualization theory |
| **MetalLB / Traefik** | Networking | L2/L3 Routing, BGP, Load Balancing | Network theory |
| **ArgoCD (GitOps)** | Software Engineering | Declarative State, Reconciliation Loop | Security automation theory |
| **vLLM / Valkey** | Distributed Systems | PagedAttention, Vector Indexing (HNSW) | AI infrastructure theory |

---

## Deep Dive Modules

### Module A: The Memory Wall (vLLM & OS Paging)

- **Problem**: LLM 추론 시 KV Cache가 메모리를 과도하게 점유하여 처리량이 저하됨.
- **Theory**: 운영체제의 **Virtual Memory Paging**.
- **Assignment**: Kwon et al. (2023) 논문을 읽고, vLLM이 어떻게 메모리 파편화를 해결하는지 파악하세요.
- **Mini-Project**: [Custom Controller 구현](#module-c-mini-project-custom-initialization-controller)

### Module B: The Vector Space (RAG & Geometry)

- **Problem**: 텍스트의 의미를 어떻게 숫자로 표현하고 빠르게 검색할 것인가?
- **Theory**: **High-dimensional Vector Space** & **Graph Theory (HNSW)**.
- **Reference**: RAG and vector database theory

---

## Module C: Mini-Project (Custom Initialization Controller)

실질적인 인프라 제어 로직을 이해하기 위한 실습 과제입니다.

### [Task] ConfigMap Watcher Controller

Kubernetes의 특정 ConfigMap이 변경될 때마다 관련 Pod을 자동으로 재시작(Rolling Update)하는 간단한 컨트롤러를 구현합니다.

- **Objective**: Kubernetes Reconciliation Loop의 원리 이해.
- **Tech Stack**: Python (kubernetes-client) or Go (controller-runtime).
- **Core Logic**:
  1. `ConfigMap` 리소스를 리스트하고 이벤트를 감시(Watch)합니다.
  2. 변경 감지 시, 해당 `ConfigMap`을 사용하는 `Deployment`의 Annotations에 타임스탬프를 추가하여 재배포를 유도합니다.
- **Validation**: GitOps manifest 변경 후 ArgoCD reconciliation으로 Pod 교체를 확인합니다.

---

## Recommended Reading List

1. Kwon et al., "Efficient Memory Management for LLM Serving with PagedAttention" (SOSP '23)
2. Vaswani et al., "Attention Is All You Need" (2017)
3. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (2020)

---

> [!TIP]
> 이 저장소의 활성 에이전트 런타임은 `.claude/`와 `.codex/` 기준입니다. 내구성 있는 학습 참고 자료를 추가할 때는 빈 `.agent/` 경로를 만들지 말고 `docs/90.references/` 또는 현재 활성 런타임 문서로 연결하세요.

## Related Documents

- [References README](../README.md)
- [Agent Governance Hub](../../00.agent-governance/README.md)
