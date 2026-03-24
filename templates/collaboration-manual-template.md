---
layer: 'meta'
---
# Collaboration Manual (COLLABORATION.md)

_Target Location: `COLLABORATION.md` (Project Root) or `docs/manuals/collaboration-manual.md`_
_Description: Defines the team's working agreements, development methodology, and communication SLAs._

## Overview (KR)
이 문서는 팀의 협업 방식, 커뮤니케이션 규칙(SLA), 그리고 개발 방법론에 대한 표준을 정의합니다. 팀원 간의 원활한 협업과 일관된 작업 품질을 보장하기 위한 가이드라인을 포함합니다.

---

## 1. Team Roster & Decision Makers

Explicitly define who makes the final calls to prevent deadlocks.

| Role | Name | Responsibilities |
| :--- | :--- | :--- |
| **Product Owner (PO)** | [Name] | Business requirements, priority, final feature sign-off |
| **Tech Lead (TL)** | [Name] | Architecture decisions, code review final say |
| **QA Lead** | [Name] | Test strategy, release sign-off |

## 2. Communication Channels & SLAs (Senior)

| Channel | Purpose | Expected Response SLA |
| :--- | :--- | :--- |
| **Slack/Teams** | Daily syncs, quick questions | < 4 hours |
| **GitHub PRs** | Code Review & Feedback | < 24 business hours |
| **Urgent Incidents** | P0/SEV-1 Production Downs | < 15 minutes |

## 3. Development Methodology

- **Process Type**: [e.g., Scrum / Kanban]
- **Sprint Length**: [e.g., 2 weeks]
- **Sync Rituals**:
  - **Planning**: [e.g., Every other Monday at 10 AM]
  - **Daily Standup**: [e.g., Async on Slack by 9:30 AM]

## 4. Definition of Ready (DoR) & Definition of Done (DoD)

### Definition of Ready (Before coding starts)
- [ ] Issue has a clear **Problem Statement**.
- [ ] Issue has measurable **Acceptance Criteria**.
- [ ] Technical implementation approach is approved (e.g., via ADR or Spec).

### Definition of Done (Before merging/closing)
- [ ] All Acceptance Criteria are met and verified.
- [ ] Unit & Integration tests are written and passing in CI.
- [ ] Code has been reviewed and approved by at least [N] reviewers.
- [ ] Relevant documentation (API specs, runbooks) updated.

## 5. Branching & Merge Strategy

- **Branching Model**: [e.g., GitHub Flow / Trunk-Based]
- **Branch Naming**: `feat/[issue-id]-short-desc`
- **Merge Policy**: [e.g., Squash and Merge enforced]

## 6. Code Review Guidelines
- **Reviewer Count**: Minimum [N] approvals required.
- **PR Size Limits**: Recommended < 400 lines per PR.
- **Expectations**: Focus on logic, security, and architecture; leave syntax to CI.
