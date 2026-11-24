---
title: "Selected Session Content"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0233"
---

# Selected Session Content Technical Specification (Spec)

## 문서 개요

### 목적과 독자

This Spec states the P10 change contract for session capture, its retention
and the periodic analysis that reads it. The platform owner, reviewers and
implementers use it to judge whether the capture keeps the Q-02 selected
content safely and briefly, and whether each independent workspace runs its
own analysis.

### 책임과 적용 범위

This Spec owns the P10 behavior and acceptance criteria. The [Plan](plan.md)
owns the work order, risks and rollback, and the
[Task](01.tasks/tsk-0001-selected-session-content.md) owns execution and
evidence.

## 내용 계약

### 입력과 전제

The operator entered `prompts/P10-SESSIONS.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
on 2026-11-24 at `main@30bd8dd5b3fc9220a3c57c0961607e6531cfd34e`. Decision
Q-02, design D10, the session retention policy 1.1.0 and finding K23-09 ask
the metadata-only capture to keep redacted selected content with 30-day and
90-day limits, failure identity, and a scheduler per independent workspace.
The live capture held 146,397 structure records and no content.

### 본문과 규칙

#### Overview

##### Goal

In the transaction that stores a line's structure, capture also stores its
visible prompt, visible response and tool result after redaction,
abridgement, a second redaction and a UTF-8 byte cap. Content and metadata
expire, the body store is bounded, failed tool results carry a call ID and a
failure class, two rules turn classified refusals into harness candidates,
unpromoted candidates expire, and the timer name carries the workspace ID.

###### Owning Requirements

[REQ-0003-FR-0022 and FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md)
keep session and memory state apart from Task status and evidence and
require one shared implementation behind thin provider surfaces.
[AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md)
keeps one store per Git common directory; no new architecture decision is
needed.

##### Consumers

`scripts/session_capture.py` (hooks, `scan`, `status`, `contents`,
`expire`), `scripts/session_analysis.py` (rules, expiry, `install-timer`),
the user timer and the
[context and memory policy](../../../.agents/governance/context-and-memory.md).

#### Scope

##### In Scope

- Selected content with redaction before any cut, a re-check and byte caps.
- Retention and capacity limits applied to deletion, retries and rescans.
- Call IDs and failure classes, and two classified analysis rules.
- Candidate expiry and the per-workspace timer with legacy retirement.

##### Out of Scope

New external or paid analysis, any raw transcript copy or export, hidden
reasoning or tool arguments, telling a deliberate negative test apart from a
real failure, generation fences (P17), and the memory store (P09).

#### Behavior Contract

##### Inputs and Outputs

A new `content` table holds per line part: role (`prompt`, `response`,
`tool_result`), selection (`selected`, `summary`, `gap`), call ID, failure
class, redacted text, byte size, truncation flag, gap reason, turn, event
time, expiry and the parser and redaction editions. A turn's final response
and a failed tool result stay selected up to 16 KiB; earlier responses and
successful results share a 4 KiB summary per turn. Selected content expires
30 days after its event time and summaries 90 days after; a session's
metadata leaves after 90 days while its cursor stays.

##### Failure Behavior

A value that still matches a secret pattern after cleaning, a used-up turn
summary or a full 256 MiB body store leaves a gap reason and no text. A
retried or rescanned line is stored once. `install-timer` retires the legacy
unit only when its service is this checkout's.

#### Acceptance Criteria

##### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| AC-0001 | Capture stores only redacted selected content in the order redact, abridge, re-check, cap, persist, never hidden reasoning, tool arguments or injected meta lines, and stores each line once across retries. |
| AC-0002 | Selected content, summaries, metadata and unpromoted candidates expire on their limits, the body store and per-event and per-turn byte limits hold, and expired lines are not stored again. |
| AC-0003 | Failed tool results carry their call ID and failure class, classified refusals become harness candidates, and each independent workspace registers and runs its own analysis timer. |

##### Verification Strategy

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| CHK-CAPTURE | Selection, redaction order, caps, idempotency, expiry and gaps | Temporary transcripts | Module behavior only | Every capture change | `session-capture-regressions` |
| CHK-ANALYSIS | Classified rules, candidate expiry, unit naming and legacy retirement | Temporary stores and unit directory | Module behavior only | Every analysis change | `session-analysis-regressions` |
| CHK-LIVE | Live scan, redaction residue, timer registration and one unit run | Local live stores and user systemd | Local host only | Once for this change | Task Results |

###### Normative and Evidence

The [context and memory policy](../../../.agents/governance/context-and-memory.md)
owns the capture and analysis rules (CTX-R006, R022, R023). The package D10
design and retention policy are dated inputs.

###### Historical and Navigation

None apply.

##### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0001 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Capture regressions |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0002 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Capture and analysis regressions |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0003 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Analysis regressions and live observation |

## 적용과 확인

### 적용 방법

Both providers' hooks feed the same capture; the user timer runs the
analysis, which scans, expires and analyzes.

### 확인 기준

Regressions prove module behavior; the live observation shows the local
stores and the user timer.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [Workspace governance requirements](../../01.requirements/0003-workspace-agent-governance-platform.md) |
| designs | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) |

### 외부 근거

Decision Q-02, design D10, the retention policy 1.1.0 and K23-09 are dated
inputs; no external standard is adopted.
