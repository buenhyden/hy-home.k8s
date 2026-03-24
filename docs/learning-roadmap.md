---
layer: "meta"
---
# Learning Roadmap: hy-home.k8s

## 개요

이 로드맵은 6년 차 백엔드 개발자의 시각에서 Kubernetes와 GitOps의 **핵심 원리(Concepts & Why)**를 체계적으로 학습하기 위해 설계되었습니다. 단순한 명령어 실행을 넘어, 각 기술이 왜 필요한지, 그리고 백엔드 아키텍처와 어떻게 연결되는지를 중심으로 학습합니다.

---

## Level 1: Core Fundamentals (기본 다지기)

Kubernetes를 배우기 전, 현대적인 인프라 운영의 근간이 되는 기술들을 이해합니다.

### 1. 전공 기초 & OS (Linux/WSL2)

- **학습 내용**: 프로세스 관리, 파일 시스템 계층 구조(FHS), 권한 관리.
- **핵심 개념**: 왜 윈도우에서 직접 안 하고 WSL2(Linux)를 쓰는가? (커널 공유 및 호환성)
- **관련 파일**: `GEMINI.md`, `ARCHITECTURE.md` (WSL2 언급 부분)

### 2. Networking 101

- **학습 내용**: IP 주소, 서브넷 마스크(CIDR), 라우팅, 브릿지 네트워크.
- **핵심 개념**: 내 컴퓨터 안에서 Docker 컨테이너들이 어떻게 서로 통신하는가?
- **관련 커맨드**: `docker network create --subnet 172.20.0.0/16 ...` (README.md 참조)

### 3. 컨테이너 (Docker/Containerd)

- **학습 내용**: 이미지 레이어링, 볼륨 마운트, 컨테이너 통신(Bridge).
- **핵심 개념**: "내 컴퓨터에선 되는데 서버에선 안 돼요" 문제를 컨테이너가 어떻게 해결했는가?
- **관련 파일**: `scripts/setup-env.sh` (WSL2 환경 구성)

---

## Level 2: Kubernetes Infrastructure (심화 I)

실제 클러스터를 구성하며 인프라 추상화 계층을 학습합니다.

### 1. Kubernetes Cluster (k3d/k3s)

- **학습 내용**: Control Plane vs Worker Node, etcd의 역할, k3s가 왜 가벼운가?
- **핵심 개념**: 선언적(Declarative) 상태 관리란 무엇인가? (원하는 상태와 실제 상태의 일치)
- **상세 가이드**: [K8s (k3s & k3d) Mastery Skill](file:///home/hy/projects/hy-home.k8s/.agent/skills/k8s-k3s-k3d/SKILL.md)
- **관련 파일**: `infrastructure/k3d/k3d-cluster.yaml`

### 2. Load Balancing & Ingress (MetalLB & Nginx)

- **학습 내용**: External IP 할당 원리, Ingress Controller의 역할.
- **핵심 개념**: 외부 사용자가 내 클러스터 내부의 특정 서비스까지 도달하는 물리적/논리적 경로.
- **상세 가이드**: [Load Balancing & Ingress Mastery Skill](file:///home/hy/projects/hy-home.k8s/.agent/skills/load-balancing-ingress/SKILL.md)
- **관련 파일**: `infrastructure/metallb/`, `infrastructure/ingress-nginx/`

### 3. Secret Management (Sealed Secrets)

- **학습 내용**: 왜 Git에 비밀번호를 올리면 안 되는가?, 암호화 복호화 워크플로우.
- **핵심 개념**: 소스 코드에 비밀번호를 올리면 안 되는 이유와 이를 안전하게 자동화하는 방법.
- **상세 가이드**: [Sealed Secrets Mastery Skill](file:///home/hy/projects/hy-home.k8s/.agent/skills/sealed-secrets/SKILL.md)
- **관련 파일**: `infrastructure/sealed-secrets/`

---

## Level 3: GitOps & Automation (심화 II)

현업 수준의 운영 자동화와 AI Agent 협업 방식을 학습합니다.

### 1. ArgoCD & GitOps

- **학습 내용**: Pull-based 배포 방식, Single Source of Truth, 자동 동기화(Self-healing).
- **핵심 개념**: "Git이 유일한 진실의 원천(Single Source of Truth)"이 되는 배포 자동화.
- **상세 가이드**: [ArgoCD & GitOps Mastery Skill](file:///home/hy/projects/hy-home.k8s/.agent/skills/argocd-gitops/SKILL.md)
- **관련 파일**: `infrastructure/argocd/`

### 2. Spec-Driven Development

- **학습 내용**: `docs/specs/` 파일을 통한 설계 우선 방식. 인프라 변경 전 합의의 중요성.
- **핵심 개념**: 코드를 짜기 전에 '왜 이렇게 설계했는가'를 기록하는 문화의 중요성.
- **관련 파일**: `docs/adr/`, `docs/specs/`

### 3. AI Agent Collaboration (AGENTS.md)

- **학습 내용**: 에이전트에게 명확한 가이드(Context)를 제공하는 법, 효율적인 협업 워크플로우.
- **핵심 개념**: AI가 스스로 문제를 인지하고 해결할 수 있도록 가이드라인을 작성하는 방법.
- **관련 파일**: `AGENTS.md`, `docs/agentic/`

---

## 🎓 학습 팁
1. **직접 실행**: 모든 개념은 `make deploy` 등으로 직접 클러스터를 띄워보며 확인하세요.
2. **로그 확인**: 에러 발생 시 `kubectl logs`와 ArgoCD UI를 통해 원인을 파악하는 습관을 기릅니다.
3. **작은 성공부터**: k3d 클러스터를 띄우는 것부터 시작해서 하나씩 '체크'해 나가세요.
