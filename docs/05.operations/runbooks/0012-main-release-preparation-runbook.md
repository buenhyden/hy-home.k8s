---
title: "Main Release Preparation"
version: "1.0.0"
type: "operation/runbook"
status: "active"
owner: "platform"
updated: "2026-10-08"
layer: "operations"
artifact_id: "RUN-0012"
---

# Main Release Preparation Runbook

## Overview

이 Runbook은 main의 검토된 변경을 정규 `CHANGELOG.md`에 기록하고 한
생산자로 SemVer tag와 GitHub Release를 준비하는 순서를 제공한다. 릴리스는
저장소의 공개 계약 이력이다. k3d·ArgoCD·Vault의 배포 완료나 live 검증을
증명하지 않는다. 계약은 [SPEC-0107](../../03.specs/0107-local-qa-and-release/spec.md),
실제 실행 증적은 해당 변경의 Task가 소유한다.

## Runbook Type

- **Type**: Repository release preparation and publication
- **Executor**: 검토된 main revision과 원격 Release 권한을 확인한 운영자
- **Boundary**: PR 준비와 로컬 검사는 저장소 작업이다. tag·Release 게시,
  원격 설정·자산 조작은 대상과 승인 출처가 확인된 operator 단계다.

## When to Use

main에 통합된 공개 계약 변경을 릴리스하려는 경우 사용한다. 먼저
[Git Policy](../../../.agents/governance/git.md)와
[Quality Policy](../../../.agents/governance/quality.md)를 읽고,
실제 main commit·기존 tag/Release·release 설정을 확인한다. 변경의
필수 로컬 검사가 실패했거나 미실행이고, operator 승인이나 원격 대상이
불확실하면 게시 단계에서 멈춘다.

Python과 구현의 trusted resolver가 받아들이는 `git`, `git-cliff`, `gh`
도구를 사전에 확인한다. 일반 PATH에서 명령이 보이는 것만으로 이 조건이
충족되지는 않는다. 특히 `git-cliff`의 사용자별 NVM 경로가 거부된 과거
관측은 SPEC-0107 Task에 남아 있다. 운영자는 실제 도구 설치와 신뢰 경로를
준비하고 해당 릴리스 Task에 관측 결과를 기록한다. 환경 미확보는 그 실행의
`DEFER`이며 업무 기한이나 검증 reserve 승인으로 바꾸지 않는다.

## Procedure or Checklist

| Step | Action | Expected result | Stop / escalate when |
| --- | --- | --- | --- |
| 1 | main에 통합된 범위와 공개 호환성 영향을 검토한다. 지원 CLI/options, JSON Schema, 문서 profile/frontmatter, GitOps desired state, 외부 서비스 인터페이스의 변경을 분류한다. | 릴리스 범위와 실제 변경 근거가 Task/PR에 연결된다. | 기존 릴리스의 공개 계약이나 배포 결과를 추측해야 한다. |
| 2 | main에서 `release/vX.Y.Z` 브랜치를 만들고 release tool의 `prepare` preview로 제안 내용을 확인한 뒤, 명시적 `--write`로 정규 `CHANGELOG.md`를 작성해 release-preparation PR을 연다. 1.0 이후 breaking/additive compatible/compatible fix는 major/minor/patch다. 첫 0.y는 운영자가 version과 호환성 약속을 명시한다. | 릴리스 노트가 실제 통합 내용에 대응한다. | dev push 또는 7일 artifact만으로 정규 이력을 대신하려 한다. |
| 3 | 변경 입력에 해당하는 focused·affected·exact-index 및 명명된 목적·Archive·보안 단위 검사를 수행하고 로컬 커밋 직전 최종 index의 필수 lint·format을 확인한다. 오래 걸리는 full/ci 일괄 검사와 blanket unit discovery는 완료 조건으로 실행하지 않는다. 독립 리뷰, 별도 PR SHA/run의 hosted style 결과와 정상 PR/merge 결과를 확인한다. | Task에 서로 다른 입력의 결과, 도구, 승인 경계와 최종 main SHA가 기록된다. | 선택된 필수 검사 실패, `NOT_RUN`, 중요한 리뷰 finding, 또는 SHA 불일치가 있다. |
| 4 | 게시 직전 현재 main commit, 해당 SemVer tag/Release의 부재 또는 동일 대상, 변경된 승인 조건을 원격에서 확인한다. 이전 `main-<full SHA>` tag는 역사로 그대로 둔다. | 정확한 대상과 재시도 가능 조건이 확정된다. | 기존 tag를 이동해야 하거나 remote 설정·권한이 미관측이다. |
| 5 | release tool의 `publish` preview를 읽고, 원격 대상·승인·자산을 대조한 운영자만 `--execute`를 사용한다. 구현은 정확한 main SHA에서 모든 자산을 붙인 draft를 만든 후 게시한다. immutable Release 설정이 실제 활성이라면 자산 확인 후에만 게시한다. | 하나의 SemVer tag와 Release가 검토된 main commit에 연결된다. | 승인 범위, 자산, 원격 상태가 다르거나 producer가 두 개다. |
| 6 | tag 대상, Release 상태, `CHANGELOG.md`가 반영된 main SHA를 다시 읽고 Task에 관측 사실을 기록한다. | publish 결과 또는 `DEFER` 원인이 한 owner에 남는다. | 원격 결과가 없으면 로컬 파일로 성공을 추정한다. |

## Verification Steps

준비 PR의 문서·링크·상태와 실제 index는 해당 Task의 local QA 증거로
검증한다. 아래는 구현된 `scripts/release.py`의 CLI이며, 현재 소스와
`--help`, `prepare --help`, `publish --help`에서 확인했다. 도움말 확인은
prepare 실행이나 원격 게시 성공을 증명하지 않는다.
`prepare`와 `publish`의 기본형은 읽기 전용 preview다.

```bash
python3 scripts/release.py --root . prepare --version vX.Y.Z
python3 scripts/release.py --root . prepare --version vX.Y.Z --write
python3 scripts/release.py --root . publish --version vX.Y.Z --asset relative/path
```

`prepare --write`는 `release/vX.Y.Z` 브랜치에서만 정규 CHANGELOG를
작성한다. 게시 입력은 version, 깨끗한 정확한 local/remote main SHA, 저장소
identity, main의 추적된 CHANGELOG section, tag 충돌 부재, 저장소 안의
일반 파일인 상대 경로 자산을 확인해야 한다.

유효한 기존 SemVer tag가 하나도 없는 최초 릴리스에는 운영자가 첫 버전을
선택했다는 사실을 `prepare`와 `publish` 모두에서 명시적
`--initial-version`으로 전달한다. 이후 릴리스에서 이 flag는 거부된다.
최초 릴리스의 preview와 쓰기/게시 형식은 다음과 같다.

```bash
python3 scripts/release.py --root . prepare --version vX.Y.Z --initial-version
python3 scripts/release.py --root . prepare --version vX.Y.Z --initial-version --write
python3 scripts/release.py --root . publish --version vX.Y.Z --initial-version --asset relative/path
```

다음 `--execute` 명령은 **별도 승인과 원격 검증 후 운영자만** 실행한다.

```bash
python3 scripts/release.py --root . publish --version vX.Y.Z --asset relative/path --execute
```

최초 릴리스를 실제 게시할 때만 위 `--execute` 명령에도
`--initial-version`을 함께 전달한다. 이 flag는 승인 자체나 첫 버전의
적합성 증거가 아니며, 운영자의 선택·검토 결과를 Task에 별도로 남긴다.

게시 후에는 GitHub의 tag ref, Release 대상과 자산 상태를 직접 확인한다.
원격 조회가 없으면 그 단계는 `DEFER`다. CLI 옵션과 동작이 실제 구현에서
달라지면 이 절차를 먼저 수정한다.

## Observability and Evidence Sources

- 현재 main commit과 release-preparation PR의 reviewed diff
- 실제 로컬 check receipt와 독립 리뷰가 붙은 Task
- GitHub tag ref, Release draft/published 상태와 필요한 자산 목록
- 정규 main `CHANGELOG.md`와 기존 `main-<full SHA>` 역사

GitHub의 표시와 정적 workflow 설정은 서로 다른 입력이다. 실제 게시 여부는
해당 원격 ref와 Release 관측으로만 판정한다.

## Safe Rollback or Recovery Procedure

준비 PR의 내용 오류는 forward corrective commit으로 고친다. 이미 게시된
SemVer tag를 이동하거나 덮어쓰지 않는다. 게시 후 정정이 필요한 경우
operator가 새 버전의 범위와 승인·회복 경로를 결정하고, 원래 Task와
Release 이력을 보존한다. 원격 결과가 불명확하면 재시도 전에 동일 대상
존재 여부부터 조회한다.

## Traceability

### Lifecycle Traceability

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| [SPEC-0107](../../03.specs/0107-local-qa-and-release/spec.md) | Reviewed main release-preparation PR, one SemVer producer and external publication boundary | Release Task, Git history and observed GitHub Release/tag |
