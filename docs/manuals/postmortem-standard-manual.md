---
layer: "ops"
---
# Postmortem Standard Manual

_Target Location: `docs/manuals/postmortem-standard-manual.md`_
_Description: Defines the standards for conducting post-incident reviews to ensure continuous improvement._

## Overview (KR)
이 문서는 장애 발생 이후 진행되는 사후 분석(Postmortem)의 기준을 정의합니다. 비난 없는 문화(Blameless Culture) 기반의 분석, 근본 원인 파악 및 재발 방지 대책 수립 절차를 포함합니다.

---

## 1. Postmortem Thresholds
A postmortem is **MANDATORY** when:
- SEV-1 or SEV-2 incidents occur.
- Data loss or integrity issues are detected.
- Any incident requiring manual failover.

## 2. The Blameless Philosophy
- **Focus**: Process and system failures, not human error.
- **Goal**: Learn and improve, not punish.
- **Approach**: "What could we have known better?" instead of "Why did you do that?".

## 3. Postmortem Workflow
1. **Draft**: Within 24 hours of incident resolution.
2. **Review**: Collective review meeting with involved parties.
3. **Approve**: TL/DevOps Lead sign-off on action items.
4. **Publish**: Share learnings with the entire team.

## 4. Analysis Components
- **Timeline**: Exact sequence of events from detection to resolution.
- **The "5 Whys"**: Iterative interrogation to find the technical/process root cause.
- **Action Items**: Concrete, trackable tickets to prevent recurrence.

## 5. Metadata Reference
Use the [Postmortem Template](../../templates/postmortem-template.md) for individual reports.
