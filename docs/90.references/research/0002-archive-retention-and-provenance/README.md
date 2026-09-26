---
title: "Archive Retention and Provenance Research Pack"
version: "0.1.1"
type: "common/readme-research-pack"
status: "active"
owner: "platform"
updated: "2026-09-26"
layer: "references"
---

# Archive Retention and Provenance Research Pack

## Overview

이 pack은 ADR-0039가 결정하는 Stage 98 보존·인용 문제의 외부 증거를 기록한다.
Git이 객체에 이름을 붙이고 보관하는 방식, 대체된 결정과 incident 기록을 보관하는
방식, 공개 URL 이동을 알리는 방식, schema annotation이 검증과 어떻게 다른지가
여기에 해당한다. 날짜가 붙은 서술 증거이며 정책이 아니다.

## Research Contract

- **관찰 날짜**: 2026-09-15.
- **출처 종류**: Git, HTTP, JSON Schema, CommonMark, GitHub의 1차 문서, ADR
  원문 글, Google SRE postmortem 장, Diátaxis framework 사이트.
- **방법**: 각 출처는 관찰 날짜에 가져왔고 인용문을 확보한 주장만 기록한다.
  가져올 수 없었던 출처는 주장 없이 `unreachable`로 기록한다.
- **권한**: 현재 권한은 [common governance](../../../../.agents/README.md), Stage 99
  registry, 승인된 아키텍처 결정에 있다. 여기의 발견은 결정을 뒷받침하거나 그
  범위를 정할 뿐, 결정을 대신하지 않는다.

## Report Index

| Reference | Role |
| --- | --- |
| [Git provenance and superseded record citation](m0001-git-provenance-and-superseded-record-citation.md) | 객체 이름, 도달 가능성, 대체된 기록의 관행, URL 이동, schema annotation, link 파싱 |

## Refresh and Succession

출처가 인용한 절을 바꾸거나, 그 주장에 기대는 결정이 개정되면 주장을 갱신한다.
새 발견은 이전 발견 옆에 날짜를 붙여 추가하며 기존 주장은 다시 쓰지 않는다.

## Evidence Boundary

이 발견은 외부 문서다. 저장소 동작, hosted CI 결과, provider runtime, live
cluster 상태를 입증하지 않으며 여기서 인용했다고 해서 그 표준을 채택하거나
인증한 것도 아니다.

## Related Documents

- [Research collection](../README.md)
- [ADR-0039](../../../02.architecture/decisions/0039-unit-archive-retention-and-citation-table.md)
- [Spec 0082](../../../98.archive/completed/03.specs/0082-unit-archive-retention-contract/spec.md)
