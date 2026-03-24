---
layer: "meta"
---
# Collaboration Manual (COLLABORATION.md)

_Target Location: `docs/manuals/collaboration-manual.md`_
_Description: This document defines the team's working agreements, development methodology, and communication SLAs for the `hy-home.k8s` project._

## Overview (KR)
이 문서는 팀의 협업 방식, 커뮤니케이션 규칙(SLA), 그리고 개발 방법론에 대한 표준을 정의합니다. 일관된 작업 흐름을 보장하기 위한 분기 전략, 리뷰 가이드라인, 그리고 의사결정 체계를 포함합니다.

---

## 1. Team Roster & Decision Makers

| Role | Responsibility | Primary Lead |
| :--- | :--- | :--- |
| **Tech Lead (TL)** | Architecture, Core logic, Final code review approval | [Name/ID] |
| **DevOps Lead** | K8s Infrastructure, CI/CD, Secret Management | [Name/ID] |
| **Product Owner** | Feature Priority, Acceptance Criteria validation | [Name/ID] |

## 2. Communication Channels & SLAs (Senior)

| Channel | Purpose | Expected Response |
| :--- | :--- | :--- |
| **Slack/Teams** | Daily syncs, quick blockers, general chat | < 4 business hours |
| **GitHub PRs** | Code Review, Technical feedback | < 24 business hours |
| **Incidents (Pager)** | P0/P1 Production issues | < 15 minutes |

## 3. Development Methodology

- **Process**: Kanban (Flow-based)
- **Review Cycle**: Mandatory peer review for all changes to `main`.
- **Definition of Ready (DoR)**: Clear problem statement and validated Acceptance Criteria (AC).
- **Definition of Done (DoD)**: Tests passed, documentation updated, code reviewed.

## 4. Branching & Merge Strategy

- **Strategy**: GitHub Flow (Feature branches -> `main`).
- **Naming**: `feat/[issue-id]-short-desc`, `fix/[issue-id]-short-desc`.
- **Merge Policy**: Squash and Merge is enforced for clean git history.
- **Rules**: Direct pushes to `main` are strictly forbidden.

## 5. Code Review Guidelines
- **Focus**: Logic, security, and architectural alignment.
- **Checklist**:
  - [ ] Are tests included for new logic?
  - [ ] Does it adhere to the `layer:` metadata rule?
  - [ ] Are secrets managed via Sealed Secrets (no plain text)?
  - [ ] Is there any technical debt introduced (if so, document it)?

## 6. Setup Checklist
- [ ] SSH keys/GPG signing configured.
- [ ] Pre-commit hooks installed (`pre-commit install`).
- [ ] Environment variables synced from `SENSITIVE_ENV_VARS.md.example`.
