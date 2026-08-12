---
title: "Archive Record: Documentation Governance Consistency Spec"
type: "content/archive"
status: "archived"
owner: "platform"
updated: "2026-06-02"
original_type: "spec"
original_path: "docs/03.specs/007-docs-governance-consistency/spec.md"
archived_on: "2026-06-02"
archive_reason: "superseded"
replacement: "docs/04.execution/plans/2026-06-02-docs-01-05-current-implementation-alignment.md"
source_commit: "82f0e1922d9748a88b1487a32a59629ba523f408"
source_blob: "cc803905127970c28fbb343ee69d71c27e0184f4"
content_sha256: "2143740f6a4c670976992e99e7ca8b35cc49e252912916991840b4a862dcfcbb"
---
<!-- archive-envelope:v1 payload=rest-of-file encoding=git-blob-bytes -->
---
title: 'Documentation Governance Consistency Technical Specification'
type: spec
status: active
owner: platform
updated: 2026-05-28
---

# Documentation Governance Consistency Technical Specification (Spec)

---

## Overview (KR)

이 문서는 `hy-home.k8s` 워크스페이스의 문서 거버넌스 일관성 정비 작업의 기술 명세다.
`docs/99.templates/`를 canonical SSoT로 삼아, 모든 운영 문서(policies, runbooks, guides), 실행 문서(plans, tasks),
아키텍처 문서(01-03)의 템플릿 준수율을 높이고, 레거시 파일을 제거하며, CI/CD 정책 게이트와 훅 스코프를 정비한다.

## Strategic Boundaries & Non-goals

**In Scope:**

- `docs/99.templates/` 템플릿과 실제 문서 간 구조 불일치 해소
- 레거시/Superseded 파일 삭제 및 cross-reference 업데이트
- `docs/05.operations/policies` 전체에 `## AI Agent Policy Section` 추가
- `docs/05.operations/runbooks` 전체에 `## Runbook Type` 표준화 및 `## Agent Operations` 추가
- `docs/05.operations/guides` 구조 정렬 (H2 → H3 demote)
- `docs/04.execution` status 어휘 표준화 (`complete` → `done`)
- `.claude/hooks/post-validate.sh` 워크스페이스 스코프 제한
- CI `manifest-static` 잡에 `validate-policy-gates.sh` 추가

**Non-goals:**

- 인프라 매니페스트(`gitops/`) 변경
- 신규 ADR, ARD, PRD 작성
- 클러스터 Live 상태 변경
- docs/05.operations/incidents (README 완료 상태 — 변경 불필요)

## Related Inputs

- **ARD**: [../../02.architecture/requirements/0007-current-local-gitops-platform.md](../../02.architecture/requirements/0007-current-local-gitops-platform.md)
- **ADR**: [../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)

## Contracts

- **Template Contract**: `docs/99.templates/`의 각 템플릿 파일이 정의하는 필수 섹션은 해당 타입의 모든 문서에 존재해야 한다.
- **Status Vocabulary Contract**: `docs/04.execution/` 내 frontmatter status는 `draft | active | done` 중 하나여야 한다. `complete`는 유효하지 않다.
- **Governance Contract**: AI Agent가 작동하는 모든 policies와 runbooks는 AI Agent 범위를 명시적으로 선언하거나 N/A를 기술해야 한다.

## Core Design

- **Approach**: Template-first — 템플릿을 먼저 수정한 후, 하위 문서에 cascade 적용
- **Key Dependencies**: `scripts/validate-repo-quality-gates.sh`, `scripts/validate-policy-gates.sh`, `.github/workflows/ci.yml`, `.claude/hooks/post-validate.sh`
- **Execution Order**: Template → Legacy Removal → Policies → Runbooks → Guides → Plans/Tasks → CI/Hooks → Validation

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: N/A — 이 스펙은 문서 파일 구조를 다루며 데이터베이스 스키마가 없다.
- **Migration / Transition Plan**: 레거시 파일 삭제 및 cross-reference 업데이트 순서는 Plan의 Task 2에 정의된다.

## Interfaces & Data Structures

문서 타입별 필수 섹션 계약:

| Document Type        | Required Sections Added by This Work                     |
| -------------------- | -------------------------------------------------------- |
| `runbook`            | `## Runbook Type`, `## Agent Operations (If Applicable)` |
| `operation` (policy) | `## AI Agent Policy Section (If Applicable)`             |
| `plan`               | `## Agent Rollout & Evaluation Gates (If Applicable)`    |

## Edge Cases & Error Handling

- **markdownlint auto-fix 충돌**: `fix: true` 설정이 MD032 적용 시 MD012 위반을 유발한다. 영향 받는 파일에 `<!-- markdownlint-disable MD012 MD031 -->` 인라인 directive를 적용한다.
- **broken cross-reference**: 레거시 파일 삭제 전에 `grep -rl` 로 모든 참조 파일을 확인하고 대체 경로로 업데이트한다.
- **validate-policy-gates.sh conftest 부재**: 스크립트가 conftest 바이너리 없이 graceful exit 0으로 종료하는지 확인 후 CI 추가한다.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: `pre-commit run --all-files` 실패 시 변경 커밋을 중단한다.
- **Fallback**: 개별 파일 단위로 `pre-commit run --files <path>` 를 실행해 오류를 격리한다.
- **Human Escalation**: `validate-repo-quality-gates.sh` 통과 불가 상태가 지속되면 human operator가 스크립트 로직을 검토한다.

## Verification Commands

```bash
# 템플릿 준수 검증
bash scripts/validate-repo-quality-gates.sh .

# 정책 게이트 검증
bash scripts/validate-policy-gates.sh .

# GitOps 구조 검증
bash scripts/validate-gitops-structure.sh

# 시크릿 핸들링 검증
bash scripts/check-secret-handling.sh .

# pre-commit 전체 실행
pre-commit run --all-files
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: `grep -c "AI Agent Policy Section" docs/05.operations/policies/000[1-7]-*.md` → 7개 파일 × 1 match
- **VAL-SPC-002**: `grep -l "## Runbook Type" docs/05.operations/runbooks/*.md | wc -l` → 10개 파일
- **VAL-SPC-003**: `grep -l "## Agent Operations" docs/05.operations/runbooks/*.md | wc -l` → 10개 파일
- **VAL-SPC-004**: `grep -r "^status: complete$" docs/04.execution/` → 출력 없음
- **VAL-SPC-005**: `bash scripts/validate-repo-quality-gates.sh .` → PASS
- **VAL-SPC-006**: `pre-commit run --all-files` → all hooks pass
- **VAL-SPC-007**: `grep -r "0005-new-app-gitops-onboarding-guide\|0006-new-app-onboarding-runbook" docs/` → 출력 없음

## Related Documents

- **Plan**: `[../../04.execution/plans/2026-05-28-docs-governance-consistency.md]`
- **Tasks**: `[../../04.execution/tasks/2026-05-28-docs-governance-consistency.md]`
- **Runbook Template**: `[../../05.operations/../99.templates/runbook.template.md]`
- **Policy Template**: `[../../05.operations/../99.templates/policy.template.md]`
- **Guide Template**: `[../../05.operations/../99.templates/guide.template.md]`
