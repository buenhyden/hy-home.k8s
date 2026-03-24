---
layer: "meta"
---
# Global Persona Rules

This file defines the cross-model persona and interaction standards for the `hy-home.k8s` repository.

## 1. Response Language
- **Korean Protocol**: Unless explicitly requested otherwise by the USER in English, all summaries, explanations, and architectural discussions MUST be provided in **Korean**.
- **Code & Tech Terms**: Keep technical terms (Kubernetes, Pod, GitOps, etc.) and code snippets in English.

## 공통 페르소나 (Global Persona)

- **언어 원칙**: 모든 요약 및 설명은 **한국어**로 작성한다 (필수).
- **기술 환경**: 모든 작업은 WSL2 및 k3d 환경을 전제로 수행한다.

## 핵심 제약 사항 (Core Constraints)

- **Spec-First**: 모든 코드 변경은 `docs/specs/` 내 승인된 명세서를 필요로 한다.
- **Traceability**: 모든 작업 단계와 문서는 상호 추적 가능해야 한다.

## 인프라 원칙

- **Kubernetes**: k3s/k3d 기반의 가벼운 로컬 클러스터를 지향한다.
- **GitOps**: ArgoCD를 통한 선언적 배포를 준수한다.

## 2. Interaction Style
- **Concise & Direct**: Provide information in a concise, GitHub-style markdown format.
- **Spec-Driven**: Always refer to `docs/specs/` before suggesting code changes.
- **Safety First**: Verify all commands against `docs/00.agent/rules/core.md` before execution.

## 3. Metadata Compliance
- Every documentation file created or modified MUST include `layer:` metadata in the frontmatter.
