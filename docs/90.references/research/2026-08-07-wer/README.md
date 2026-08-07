# Workspace Engineering Research Pack (2026-08-07)

## Overview

이 폴더는 `hy-home.k8s` 워크스페이스를 대상으로 2026-08-07에 수행한 외부 1차
소스 조사와 워크스페이스 대조 분석을 보존하는 dated research pack이다. 다섯
개 주제 reference는 `2026-07-07` 팩이 다루지 않은 영역을 채운다: Diátaxis 문서
아키텍처와 SDLC 문서 타입 역할, LLM 지식 인덱스 규약과 에이전트 지식 라우팅,
GitHub Actions 규칙과 CI 증적 레인, 작업 특성별 모델·추론 설정 라우팅, 그리고
기억 계층이다. 여섯 번째 문서는 `research/` 안의 동일 목적 문서 간 대체 관계와
최신 관측이 뒤집은 주장을 정리한 통합 기록이다.

이 폴더는 설명용 참고 자료다. 실행 정책, 템플릿 route, 검증기 동작, 프로바이더
런타임, 배포 승인 절차를 정의하거나 변경하지 않는다.

### Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

### Scope

#### In Scope

- 2026-08-07에 확인한 1차 소스 findings과 그 명시적 한계
- 각 주제에 대한 워크스페이스 현황 대조와 gap routing
- 도달 실패한 소스의 실패 코드와 관측일 기록
- `2026-07-04`와 `2026-07-07` 팩 사이의 대체 관계 및 이월 사실 정리

#### Out of Scope

- 활성 거버넌스 정책, 템플릿 route, frontmatter schema, 검증기 변경
- 실 클러스터, Vault/ESO, 클라우드, 프로바이더 런타임, hosted CI 관측
- 시장 분석 자료를 워크스페이스 운영 기준으로 격상하는 행위
- 이전 팩 내용의 무효화. 이전 팩은 인용된 dated 증적으로 보존한다

### Structure

```text
2026-08-07-wer/
├── README.md                                     # 이 파일 (인덱스 및 증적 경계)
├── agent-memory-tiers-and-management.md          # 기억 계층 및 검증기 강제 범위
├── agent-model-routing-and-configuration.md      # 작업 특성별 모델·추론 설정 라우팅
├── documentation-architecture-and-diataxis.md    # Diátaxis 4-mode 및 SDLC 문서 역할
├── github-actions-and-ci-evidence.md             # Actions 규칙, CI 선택 계약, 증적 레인
├── llm-wiki-and-knowledge-routing.md             # LLM 지식 인덱스 규약 및 드리프트 분류
└── research-consolidation-and-supersession-map.md # 통합·대체 관계 및 초과 주장 정리
```

### Source Priority

소스 간 내용이 상충하면 다음 우선순위를 따른다:

1. Canonical repository owners (거버넌스, 계약, 스크립트 정본)
2. Official product, provider, standards documentation
3. Repo-backed evidence (tracked manifests, configs, templates)
4. Official issue trackers, release notes
5. Market scan, vendor marketing, blog, benchmark

시장 분석 자료는 비권위(non-authoritative)로 분류하며 워크스페이스 정책을
덮어쓸 수 없다.

### Link Basis

이 README의 링크 기준 위치는 `docs/90.references/research/2026-08-07-wer/`다.

- 같은 팩 문서는 `./<file>`로 연결한다.
- 이전 팩 문서는 `../2026-07-07-wer/<file>` 또는 `../2026-07-04-wer/<file>`로 연결한다.
- 상위 Research README는 `../README.md`로 연결한다.
- canonical stages 경로는 `../../../<stage>/`로 계산한다.

## Snapshot Contract

- Pack role: 2026-08-07 dated research evidence.
- Snapshot date: 2026-08-07.
- Repository observation date: 2026-08-07.
- Provider/model source cutoff: 이 팩의 프로바이더 findings은 2026-08-07
  current-only 관측이며, `2026-07-10 10:00 KST` 고정 cutoff를 이동시키지 않는다.
  cutoff 이후 관측은 충돌(conflict)로 기록하고 해소하지 않는다.
- Registry boundary: research 컬렉션은 Current-pack 레지스트리에서 회수되었다.
  이 팩과 이전 팩은 일반 Stage 90 reference로 관리되며, 감사 팩과
  `2026-07-04` 스냅샷 동결은 유지된다.
- Authority: dated research evidence only. 현재 정책과 구현 진실은 각 canonical
  repository owner가 보유한다.

## Report Index

| Reference                                                                                        | Lifecycle | Role                                                                          | Authority Boundary                                                            |
| ------------------------------------------------------------------------------------------------ | --------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| [agent-memory-tiers-and-management.md](agent-memory-tiers-and-management.md)                     | `active`  | 장기·단기·영역별·프로바이더-로컬 기억 계층과 체크포인트·루프 검증기 강제 범위 | 기억 계층 설명서; 클래스, 소유자, 보존 규칙은 Stage 00 memory 계약이 소유     |
| [agent-model-routing-and-configuration.md](agent-model-routing-and-configuration.md)             | `active`  | 작업 특성별 모델·추론 설정 라우팅, 48개 튜플 현황, cutoff 충돌 목록           | 라우팅 분석; 모델 값, tier, 임계값, 승격 결정은 Stage 00 계약이 소유          |
| [documentation-architecture-and-diataxis.md](documentation-architecture-and-diataxis.md)         | `active`  | Diátaxis 4-mode 문서 아키텍처와 SDLC 문서 타입별 역할·금지·구조·수명주기      | 설명용 매핑; 템플릿 route, heading 계약, status domain은 Stage 99가 소유      |
| [github-actions-and-ci-evidence.md](github-actions-and-ci-evidence.md)                           | `active`  | Actions 보안 규칙, CI 선택 계약, 검증기 소유권, 증적 레인 분리                | 워크플로우 분석; pin 선택과 lane 정의는 `.github/`와 quality-standards가 소유 |
| [llm-wiki-and-knowledge-routing.md](llm-wiki-and-knowledge-routing.md)                           | `active`  | llms.txt/MCP/지시 파일 규약과 생성 인덱스의 결정성 및 드리프트 3분류          | 인덱스 분석; 생성기 내용과 JIT 로딩 순서는 각 canonical owner가 소유          |
| [research-consolidation-and-supersession-map.md](research-consolidation-and-supersession-map.md) | `active`  | 동일 목적 문서의 대체 관계, 이월 사실, 최신 관측이 뒤집은 이전 팩 주장        | 통합 기록; 이전 팩 문서를 수정하거나 무효화하지 않음                          |

## Refresh and Succession

- 각 reference의 `Review and Freshness` 절이 개별 refresh trigger를 소유한다.
- 이 팩은 `2026-07-07` 팩을 대체하지 않는다. 두 팩은 서로 다른 관측일의 증적을
  보유하며, 상충 시 더 최근 관측일을 명시한 쪽이 해당 사실의 관측 증거다.
  대체 관계는 통합 기록 문서가 행 단위로 소유한다.
- 프로바이더 문서는 current-only 표면이다. 여기 기록된 모든 프로바이더 사실은
  2026-08-07 관측이며, 승격 전 재관측이 필요하다.

## Evidence Boundary

- 이 팩의 모든 결과는 repository-static 및 공개 문서 관측이다.
- provider-runtime, hosted CI, remote, live 레인은 `DEFER`다. 어떤 항목도 실
  클러스터, Argo CD, Vault, ESO, 인증, 자격, 배포 준비 상태를 증명하지 않는다.
- 도달 실패한 소스는 각 문서의 `Sources` 절에 실패 코드와 날짜로 기록했다.
- 추론은 추론으로 표시했으며 정책으로 승격되지 않았다.

## Related Documents

- [Research Collection](../README.md)
- [Research Pack (2026-07-07)](../2026-07-07-wer/README.md)
- [Research Pack (2026-07-04)](../2026-07-04-wer/README.md)
- [Stage 90 References](../../README.md)
- [Agent Quality Standards](../../../00.agent-governance/rules/quality-standards.md)
