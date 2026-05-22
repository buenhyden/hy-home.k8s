---
title: 'Reference: {Item Name}'
type: reference
status: draft
owner: '{team-or-person}'
updated: YYYY-MM-DD
---

<!-- Target: docs/90.references/<category>/<topic>.md -->

# Reference: [Item Name]

> Use this template for `docs/90.references/<category>/<topic>.md`.
>
> Rules:
>
> - Keep this document factual, slow-moving, and explicitly bounded.
> - Do not duplicate active requirements, specs, plans, tasks, policies, or runbooks.
> - Use relative links only, calculated from the final authored document location.
> - Keep placeholder or optional target paths as code literals until the target exists.

---

## Overview (KR)

이 문서는 [주제]에 대한 참고 문서다. 느리게 변하는 기준 정보, 용어, 외부 표준 요약을 정리한다.

## Purpose

[Why this reference exists.]

## Reference Type

- Type: version-contract-inventory | external-standard-snapshot | durable-concept | learning-roadmap | glossary | faq
- Source checked: YYYY-MM-DD
- Refresh trigger: [What event requires review.]

## Authority Boundary

- **Authoritative for**:
  - [Facts, versions, concepts, or lookup material this document owns.]
- **Not authoritative for**:
  - [Requirements, decisions, implementation contracts, plans, tasks, policies, or runbooks that belong in other stages.]

## Scope

- [What is covered]
- [What is not covered]

## Definitions / Facts

- **Term / Fact 1**:
- **Term / Fact 2**:

## Sources

- [Source 1]
- [Source 2]

## Review and Freshness

- Review cadence: [monthly | quarterly | on source change | on dependency bump]
- Last reviewed: YYYY-MM-DD
- Next review trigger: [Manifest/config change, cloud-provider support change, or linked stage update.]

## Related Documents

Target-relative examples below assume the authored file will be created at
`docs/90.references/<category>/<topic>.md`.

- **ARD**: `[../../02.architecture/requirements/####-<system-or-domain>.md]`
- **Spec**: `[../../03.specs/<feature-id>/spec.md]`
- **Reference maintenance runbook**: `../../05.operations/runbooks/0011-reference-maintenance-runbook.md`
- **LLM Wiki curation guide**: `../../05.operations/guides/0009-llm-wiki-curation-guide.md`
