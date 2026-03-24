---
layer: "meta"
---
# Architecture Decision Record (ADR)

_Target Location: `docs/adr/NNNN-<short-title>.md`_
_Description: This document records a critical technical decision, its context, rationale, and consequences. It is the permanent record of 'Why' a choice was made._

## Overview (KR)
이 문서는 아키텍처 결정 사항과 그 배경, 선택 이유, 그리고 결정에 따른 영향을 기록합니다. 나중에 의사결정 과정을 추적하고 기술 부채나 트레이드오프를 이해하는 데 사용됩니다.

---

## 1. Metadata

- **ADR Number**: NNNN
- **Status**: [Accepted | Superseded | Deprecated]
- **Date**: YYYY-MM-DD
- **Deciders**: [buenhyden, Team Name]
- **layer**: [meta | infra | gitops | app | ops]

## 2. Context & Problem Statement

[Describe the context, the core conflict or limitation, and why a decision is required now. What happens if we do nothing?]

## 3. Decision Drivers (Senior)

- **Driver 1**: [e.g., Security: Need to comply with SOC2 data encryption rules]
- **Driver 2**: [e.g., Performance: Current latencies exceed 500ms for p95]
- **Driver 3**: [e.g., Maintainability: Codebase is becoming too coupled to [Library]]

## 4. Alternatives Considered

### Option A: [Title]
- **Pros**: [Benefit 1], [Benefit 2]
- **Cons**: [Risk 1], [Trade-off 1]

### Option B: [Title]
- **Pros**: [Benefit 1]
- **Cons**: [Risk 1]

## 5. Decision Outcome (The Record)

**Chosen Option: [Selected Option]**

### Rationale
[Explain why this option was chosen over others. Link back to Decision Drivers.]

### Consequences
- **Positive**: [e.g., Reduced build time, better type safety]
- **Negative / Neutral**: [e.g., New dependency added, requires team training]

## 6. Technical Debt & Risk Assessment (Senior)

- **Debt Incurred**: [e.g., We are skipping [Feature] for now to hit the deadline; will require refactor in Q3]
- **Risk Score**: [Low | Medium | High]
- **Mitigation Plan**: [How we will handle the debt or risks identified]

## 7. Deferred Decisions (ADL - Architecture Decision Log)

[List any decisions that were NOT made during this record and are deferred to a later date or another ADR.]
- **Deferred Item 1**: [Description + Trigger for when to decide]

## 8. Related Artifacts
- **ARD Reference**: `[../ard/system-ard.md]`
- **Spec Reference**: `[../specs/YYYY-MM-DD-feature.md]`
- **Supersedes**: `[NNNN-old-decision.md]`
