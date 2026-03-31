# Infrastructure to Theory: 2026 Learning Roadmap

## 1. Overview

이 가이드는 `hy-home.k8s` 인프라 구축 경험을 바탕으로, 실무 기술이 어떤 컴퓨터 과학(CS) 및 공학(CE) 이론에 뿌리를 두고 있는지 연결합니다. 단순히 도구를 사용하는 법을 넘어, **"왜 이렇게 동작하는가?"**에 대한 해답을 찾는 여정입니다.

---

## 2. Theoretical Mapping (Infrastructure -> CS Theory)

| Current Tool | Academic Domain | Key Concept | Reference |
| --- | --- | --- | --- |
| **k3d / Docker** | Operating Systems | Namespace & CGroups, Virtualization | [OS Theory](../.agent/skills/self-learning-guide/references/os-virtualization/theory.md) |
| **MetalLB / Traefik** | Networking | L2/L3 Routing, BGP, Load Balancing | [Network Theory](../.agent/skills/self-learning-guide/references/network/theory.md) |
| **ArgoCD (GitOps)** | Software Engineering | Declarative State, Reconciliation Loop | [Ops Theory](../.agent/skills/self-learning-guide/references/security-automation/theory.md) |
| **vLLM / Valkey** | Distributed Systems | PagedAttention, Vector Indexing (HNSW) | [AI Infra](../.agent/skills/self-learning-guide/references/ai-infra/theory.md) |

---

## 3. Deep Dive Modules

### Module A: The Memory Wall (vLLM & OS Paging)

- **Problem**: LLM 추론 시 KV Cache가 메모리를 과도하게 점유하여 처리량이 저하됨.
- **Theory**: 운영체제의 **Virtual Memory Paging**.
- **Assignment**: Kwon et al. (2023) 논문을 읽고, vLLM이 어떻게 메모리 파편화를 해결하는지 파악하세요.
- **Mini-Project**: [Custom Controller 구현](#module-c-mini-project-custom-initialization-controller)

### Module B: The Vector Space (RAG & Geometry)

- **Problem**: 텍스트의 의미를 어떻게 숫자로 표현하고 빠르게 검색할 것인가?
- **Theory**: **High-dimensional Vector Space** & **Graph Theory (HNSW)**.
- **Reference**: [RAG & Vector DB Theory](../.agent/skills/self-learning-guide/references/rag-vector-db/theory.md)

---

## 4. Module C: Mini-Project (Custom Initialization Controller)

실질적인 인프라 제어 로직을 이해하기 위한 실습 과제입니다.

### [Task] ConfigMap Watcher Controller

Kubernetes의 특정 ConfigMap이 변경될 때마다 관련 Pod을 자동으로 재시작(Rolling Update)하는 간단한 컨트롤러를 구현합니다.

- **Objective**: Kubernetes Reconciliation Loop의 원리 이해.
- **Tech Stack**: Python (kubernetes-client) or Go (controller-runtime).
- **Core Logic**:
    1. `ConfigMap` 리소스를 리스트하고 이벤트를 감시(Watch)합니다.
    2. 변경 감지 시, 해당 `ConfigMap`을 사용하는 `Deployment`의 Annotations에 타임스탬프를 추가하여 재배포를 유도합니다.
- **Validation**: `kubectl apply` 후 Pod이 새롭게 생성되는지 확인.

---

## 5. Recommended Reading List

1. Kwon et al., "Efficient Memory Management for LLM Serving with PagedAttention" (SOSP '23)
2. Vaswani et al., "Attention Is All You Need" (2017)
3. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (2020)

---

> [!TIP]
> 모든 이론은 `.agent/skills/self-learning-guide/references/` 폴더 내의 `validation_guide.md`를 통해 실제 터미널에서 검증할 수 있습니다.
