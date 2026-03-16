# Formal Documentation Remediation Plan

- **Status**: Planned
- **layer:** meta

**Overview (KR):** 정식 문서 감사 결과 발견된 미비점(운영 문서 템플릿 미준수, ADR 참조 누락 등)을 최종적으로 보완하기 위한 실행 계획입니다.

## 1. Context & Introduction

This plan addresses the final "long-tail" issues identified during the formal documentation audit. It ensures that 100% of the files in `docs/` not only follow naming and metadata rules but also strictly adhere to their respective structural templates and maintain complete traceability back-links.

## 2. Goals & In-Scope

- **Goals:**
  - 100% template compliance for `docs/operations/`.
  - Comprehensive back-link coverage in `docs/adr/`.
  - Consolidation of redundant architectural documentation.
- **In-Scope:**
  - `docs/operations/incident-management.md`
  - `docs/operations/postmortem-standard.md`
  - All existing files in `docs/adr/*.md` (Back-link audit).
  - Merging redundant sections between `ard/documentation-system` and `ard/architecture-checklist`.

## 3. Non-Goals & Out-of-Scope

- **Non-Goals:**
  - Writing new project features.
  - Modifying `infrastructure/` code.

## 4. Requirements & Constraints

- **Requirement [REQ-REM-001]**: All `docs/adr/*.md` MUST contain a `Related PRD` or `PRD Reference` line.
- **Requirement [REQ-REM-002]**: Operational documents MUST include `Status`, `Owner`, and `Overview (KR)` headers.
- **Constraint**: Must maintain existing relative link stability.

## 5. Work Breakdown (Tasks & Traceability)

| Task | Description | Files Affected | Target REQ | Validation Criteria |
| ---- | ----------- | -------------- | ---------- | ------------------- |
| TASK-001 | Standardize ADR back-references | `docs/adr/*.md` | [REQ-REM-001] | Grep confirms PRD references |
| TASK-002 | Align Operations with templates | `docs/operations/*.md` | [REQ-REM-002] | Headers match templates |
| TASK-003 | Merge redundant ARD components | `docs/ard/*.md` | [Common] | No duplicated sections |

## 6. Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| -- | ----- | ----------- | -------------------- | ------------- |
| VAL-PLN-001 | Structural | Template Header Verification | `grep -r "Owner:" docs/operations` | Header exists in all |
| VAL-PLN-002 | Relational | ADR Traceability Check | `grep -r "prd/" docs/adr/` | All ADRs have PRD links |

## 7. Completion Criteria

- [ ] All ADRs linked to PRDs.
- [ ] Operations docs aligned with `incident-template.md` and `postmortem-template.md`.
- [ ] Redundant ARD content merged.
- [ ] Final audit pass (v3) shows zero violations.
