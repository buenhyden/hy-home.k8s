---
title: "00.workspace/02.architecture/02.decisions"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-19"
---

# 00.workspace/02.architecture/02.decisions

## Responsibility

### Purpose

> 작업 시스템 ADR collection이다.

문서 계약, 에이전트 거버넌스, QA·CI, Git·릴리스, 문서 처분, 작업 잔여 원장에 관한 결정을 보존한다. 각 ADR의 승인·대체 상태는 해당 문서의 frontmatter가 소유한다.

#### Inputs and Outputs

##### In Scope

- 일하는 방식에 관한 결정 1건씩의 ADR

##### Out of Scope

- 제품 플랫폼 결정(`docs/02.architecture/02.decisions/`)

### Excluded Responsibilities

제품 결정과 상세 구현·운영 절차는 이 collection이 소유하지 않는다.

## Current Contents

### Paths

| Path | Purpose |
| --- | --- |
| [`./0030-authority-first-sdlc-and-agent-governance-convergence.md`](./0030-authority-first-sdlc-and-agent-governance-convergence.md) | Authority-first SDLC document, agent governance, Archive, template, and script convergence decision |
| [`./0031-current-corpus-retention-and-validation-ownership.md`](./0031-current-corpus-retention-and-validation-ownership.md) | Current corpus retention, package-local execution lineage, and validation routing ownership decision |
| [`./0033-common-document-contract-v9.md`](./0033-common-document-contract-v9.md) | Common document contract v9 and governed router envelope decision |
| [`./0036-common-knowledge-and-prompt-surfaces.md`](./0036-common-knowledge-and-prompt-surfaces.md) | Common knowledge and prompt surface adoption |
| [`./0047-agent-contract-and-resource-ownership.md`](./0047-agent-contract-and-resource-ownership.md) | Agent 계약과 resource 소유 경계의 한정 개정 |
| [`./0048-local-qa-and-semver-release-ownership.md`](./0048-local-qa-and-semver-release-ownership.md) | 로컬 QA 단계별 책임과 단일 SemVer 릴리스 생산자 결정. 호스팅 검사 조항은 ADR-0063이 개정한다. |
| [`./0052-single-main-trunk-branch-strategy.md`](./0052-single-main-trunk-branch-strategy.md) | `main` 하나만 장기 branch로 두고 짧은 feature branch로 통합. 이 결정에 기록된 `independent-review` 필수 체크는 당시 설정이며, 현재 선언은 [main 보호 설정](../../../../.github/rulesets/main-protection.md)이 소유한다. |
| [`./0053-unvalidated-archive.md`](./0053-unvalidated-archive.md) | `docs/98.archive`를 검증하지 않고 Git history로만 복구 |
| [`./0055-governance-decision-current-state-amendment.md`](./0055-governance-decision-current-state-amendment.md) | 거버넌스 ADR(0030, 0031, 0033, 0036, 0047, 0048, 0053)의 현행 불일치 조항을 운영자 승인으로 한정 개정 |
| [`./0056-manual-document-disposition-review.md`](./0056-manual-document-disposition-review.md) | 현재 문서 처분 전 소비자·보존·권한·Git 원문 복구를 수동으로 확인하는 개정안 |
| [`./0057-package-exit-shape-check.md`](./0057-package-exit-shape-check.md) | 끝난 Stage 03 package가 잘못된 모양으로 tree를 떠나는 것을 staged commit에서 막도록 ADR-0056 Decision 6을 좁히는 개정 |
| [`./0058-repository-vocabulary-in-knowledge-surface.md`](./0058-repository-vocabulary-in-knowledge-surface.md) | `docs/00.workspace/01.project/glossary.md` 하나만 용어 의미를 소유하는 Repository Vocabulary로 허용하도록 ADR-0036 Decision 3의 포인터 전용 조항을 좁히는 개정 |
| [`./0059-registry-common-form-model.md`](./0059-registry-common-form-model.md) | Stage 99 registry(generation 10 유지)에 선택 키를 더해 역할별 공통 문서 양식, 문서 역할, TemplateDefinition, 공유 계약 승인 필드를 담도록 ADR-0033의 현재 상태 키 목록을 개정 |
| [`./0060-work-residue-ledger-amendment.md`](./0060-work-residue-ledger-amendment.md) | 작업 잔여물(미완료 handoff, conflict, adoption, survey)만 담는 단일 JSON work residue ledger를 허용하도록 ADR-0031, ADR-0036, ADR-0047, ADR-0048의 무원장 조항을 "경쟁하는 progress ledger 금지"로 좁히는 개정 |
| [`./0061-registry-schema-version-semver.md`](./0061-registry-schema-version-semver.md) | Amendment that makes the Stage 99 registry `schema_version` a SemVer string (generation 10 is `10.0.0`, adoption edition is `11.0.0`) and states the four-level bump rule, amending the integer sentences of ADR-0033 and ADR-0059 Decision 1. The current edition is recorded in `docs/99.templates/registry.json`. |
| [`./0062-accepted-decision-retained-form.md`](./0062-accepted-decision-retained-form.md) | Amendment that keeps the seven-H2 form for accepted ADRs in the closed range ADR-0001 to ADR-0061 as a registered retained form, gives every later ADR the common ADR form in every status, and narrows ADR-0059 Decision 5 for the ADR role |
| [`./0063-affected-pr-gitops-validation.md`](./0063-affected-pr-gitops-validation.md) | PR의 누적 변경에 따라 기존 필수 job `style-pr`에서 style, CI lock, 정적 GitOps identity 검사를 선택해 fail-closed aggregate로 보고하도록 ADR-0048의 호스팅 검사 조항만 개정 (2026-11-18 승인). 선택된 CI lock·GitOps leaf가 실제로 실행된 호스팅 run은 아직 관측되지 않았다. |
| [`./0064-workspace-layer-physical-owner.md`](./0064-workspace-layer-physical-owner.md) | W 계층을 `docs/00.workspace/`에 두고 `docs/` 분류 폴더를 번호화하며 작업 시스템 ADR을 이곳으로 분리하는 결정 (proposed) |

### Owners

| 범위 | ADR |
| --- | --- |
| 문서 계약·양식·Registry | 0033, 0059, 0061, 0062 |
| 거버넌스·에이전트 | 0030, 0036, 0047, 0055, 0058, 0064 |
| 처분·보존 | 0031, 0053, 0056, 0057, 0060 |
| QA·CI·Git·릴리스 | 0048, 0052, 0063 |

## Usage

### Entry Points

1. 새 ADR은 `docs/99.templates/02.templates/02.architecture/decision.template.md`에서 시작하고 target은 `docs/00.workspace/02.architecture/02.decisions/####-<short-title>.md`다.
2. 수락된 ADR 본문은 다시 쓰지 않고 후속 ADR로 개정한다.

#### Upstream and Downstream

- [Workspace architecture](../README.md)
- [Workspace description](../01.descriptions/README.md)
- [Product decisions](../../../02.architecture/02.decisions/README.md)

#### Policy and Templates

- [Decision form](../../../99.templates/02.templates/02.architecture/decision.template.md)

### Checks

ADR 처분은 문서 수명주기 정책의 조건을 따른다. 2026-11-19 경로 전환으로 이 collection에 옮겨진 ADR은 ID와 본문을 그대로 유지한다.
