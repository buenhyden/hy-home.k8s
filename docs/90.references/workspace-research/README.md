# 90.references/workspace-research

> 2026-08-07 워크스페이스 엔지니어링 조사 결과와 워크스페이스 대조 분석이 여기에 있다.

> [!NOTE]
> All AI agent interactions with this directory must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

`workspace-research/`는 `hy-home.k8s`를 대상으로 2026-08-07에 수행한 외부 1차
소스 조사와 워크스페이스 현황 대조 분석을 보존한다. 다섯 개 주제 reference는
인접한 [research](../research/README.md) 컬렉션의 Current pack이 다루지 않은
영역을 채운다: Diátaxis 문서 아키텍처와 SDLC 문서 타입 역할, LLM 지식 인덱스
규약과 에이전트 지식 라우팅, GitHub Actions 규칙과 CI 증적 레인, 작업 특성별
모델·추론 설정 라우팅, 그리고 기억 계층이다. 여섯 번째 문서는 `research/`의
동일 목적 문서 간 대체 관계와 최신 관측이 뒤집은 주장을 정리한 통합 기록이다.

이 컬렉션이 `research/` 안의 dated pack이 아닌 형제 컬렉션인 이유는 명시적이다.
`docs/90.references/data/reference-information-architecture.json`이 Current
research pack의 멤버십과 `docs/90.references/research/README.md`의 바이트를
baseline 커밋에 고정하고 있어, 해당 경로에는 신규 파일을 추가할 수 없다. 그
경계를 우회하지 않고 보존한 채 새 증적을 남기기 위해 별도 컬렉션을 사용한다.

이 폴더는 설명용 참고 자료다. 실행 정책, 템플릿 route, 검증기 동작, 프로바이더
런타임, 배포 승인 절차를 정의하거나 변경하지 않는다.

### Collection Readers

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 2026-08-07에 확인한 1차 소스 findings과 그 명시적 한계
- 각 주제에 대한 워크스페이스 현황 대조와 gap routing
- 도달 실패한 소스의 실패 코드와 관측일 기록
- `docs/99.templates/templates/common/reference.template.md` 기반 reference 문서

### Out of Scope

- 활성 거버넌스 정책, 템플릿 route, frontmatter schema, status domain, 검증기 변경
- 실 클러스터, Vault/ESO, 클라우드, 프로바이더 런타임, hosted CI 관측
- 시장 분석 자료를 워크스페이스 운영 기준으로 격상하는 행위
- Current research pack 내용의 대체 또는 무효화

## Item Index

```text
workspace-research/
├── README.md                                  # 이 파일 (인덱스 및 증적 경계)
├── agent-memory-tiers-and-management.md       # 기억 계층 및 검증기 강제 범위
├── agent-model-routing-and-configuration.md   # 작업 특성별 모델·추론 설정 라우팅
├── documentation-architecture-and-diataxis.md # Diátaxis 4-mode 및 SDLC 문서 역할
├── github-actions-and-ci-evidence.md          # Actions 규칙, CI 선택 계약, 증적 레인
├── llm-wiki-and-knowledge-routing.md          # LLM 지식 인덱스 규약 및 드리프트 분류
└── research-consolidation-and-supersession-map.md # 리서치 통합·대체 관계 및 초과 주장 정리
```

### Item Registry

| Material                                                                                   | Status   | Role                                                                          | Authority Boundary                                                            |
| ------------------------------------------------------------------------------------------ | -------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| [README.md](./README.md)                                                                   | Index    | 컬렉션 진입점 및 소스 우선순위 안내                                           | 폴더 라우팅에만 권위가 있으며 활성 정책이 아님                                |
| [agent-memory-tiers-and-management.md](./agent-memory-tiers-and-management.md)             | Included | 장기·단기·영역별·프로바이더-로컬 기억 계층과 체크포인트·루프 검증기 강제 범위 | 기억 계층 설명서; 클래스, 소유자, 보존 규칙은 Stage 00 memory 계약이 소유     |
| [agent-model-routing-and-configuration.md](./agent-model-routing-and-configuration.md)     | Included | 작업 특성별 모델·추론 설정 라우팅, 48개 튜플 현황, cutoff 충돌 목록           | 라우팅 분석; 모델 값, tier, 임계값, 승격 결정은 Stage 00 계약이 소유          |
| [documentation-architecture-and-diataxis.md](./documentation-architecture-and-diataxis.md) | Included | Diátaxis 4-mode 문서 아키텍처와 SDLC 문서 타입별 역할·금지·구조·수명주기      | 설명용 매핑; 템플릿 route, heading 계약, status domain은 Stage 99가 소유      |
| [github-actions-and-ci-evidence.md](./github-actions-and-ci-evidence.md)                   | Included | Actions 보안 규칙, CI 선택 계약, 검증기 소유권, 증적 레인 분리                | 워크플로우 분석; pin 선택과 lane 정의는 `.github/`와 quality-standards가 소유 |
| [llm-wiki-and-knowledge-routing.md](./llm-wiki-and-knowledge-routing.md)                   | Included | llms.txt/MCP/지시 파일 규약과 생성 인덱스의 결정성 및 드리프트 3분류          | 인덱스 분석; 생성기 내용과 JIT 로딩 순서는 각 canonical owner가 소유          |
| [research-consolidation-and-supersession-map.md](./research-consolidation-and-supersession-map.md) | Included | `research/` 동일 목적 문서의 대체 관계, 이월 사실, 최신 관측이 뒤집은 Current 팩 주장 | 통합 기록; 동결 문서의 내용을 수정하거나 무효화하지 않음 |

### Source Priority

소스 간 내용이 상충하면 다음 우선순위를 따른다:

1. Canonical repository owners (거버넌스, 계약, 스크립트 정본)
2. Official product, provider, standards documentation
3. Repo-backed evidence (tracked manifests, configs, templates)
4. Official issue trackers, release notes
5. Market scan, vendor marketing, blog, benchmark

시장 분석 자료는 비권위(non-authoritative)로 분류하며 워크스페이스 정책을
덮어쓸 수 없다.

### Evidence Boundary

- 이 컬렉션의 모든 결과는 repository-static 및 공개 문서 관측이다.
- provider-runtime, hosted CI, remote, live 레인은 `DEFER`다. 어떤 항목도 실
  클러스터, Argo CD, Vault, ESO, 인증, 자격, 배포 준비 상태를 증명하지 않는다.
- 프로바이더 findings은 2026-08-07 current-only 관측이며,
  `2026-07-10 10:00 KST` 고정 cutoff를 이동시키지 않는다. cutoff 이후 관측은
  충돌로 기록하고 해소하지 않는다.
- 추론은 추론으로 표시했으며 정책으로 승격되지 않았다.

## Add and Find

1. 새 문서를 추가하기 전에 상위 Spec, Plan, Task를 먼저 읽는다.
2. reference 문서는 [reference.template.md](../../99.templates/templates/common/reference.template.md)로 작성한다.
3. 소스 주장에는 `Source checked` 일자, `Sources`, `Review and Freshness`를 명시하고 경계를 밝힌다.
4. 공식 문서와 repo-backed 증거를 시장 분석보다 우선한다.
5. 시장 findings은 비권위로 표시하고 공식·repo 소스를 덮어쓰지 않는다.
6. 활성 정책, 구현 계약, 런북, 태스크 증적은 각 canonical owner로 라우팅한다.
7. 구조나 검증 증적이 바뀌면 이 README와 상위 [90.references README](../README.md), 그리고 태스크 기록을 같은 변경에서 갱신한다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/90.references/workspace-research/`다.

- 같은 컬렉션 문서는 `./<file>`로 연결한다.
- 인접 research 컬렉션은 `../research/<path>`로 연결한다.
- 상위 Stage 90 README는 `../README.md`로 연결한다.
- canonical stages 경로는 `../../<stage>/`로 계산한다.

## Related Documents

- [Stage 90 References](../README.md)
- [Research Collection](../research/README.md)
- [Current Research Pack (2026-07-07)](../research/2026-07-07-wer/README.md)
- [Agent Quality Standards](../../00.agent-governance/rules/quality-standards.md)
