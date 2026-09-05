---
name: "incident-postmortem"
description: "Use when writing a cluster incident postmortem or routing post-incident analysis through timeline reconstruction, root cause analysis, impact assessment, and remediation planning. Real-time on-call response, monitoring setup, and alert configuration are outside this skill's scope."
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# Incident Postmortem — Cluster Incident Post-Analysis Pipeline

The `incident-responder` agent leads timeline reconstruction → root cause analysis → impact assessment → remediation planning → postmortem report generation.

## Execution Mode

The read-only `incident-responder` analyzes approved evidence and returns a
report draft. An authorized author owns any durable document writes; this
skill never expands the responder's permissions.

## Workspace Boundary

`_workspace/` is scratch-only for intermediate analysis. Durable incident bundles live under
`docs/05.operations/incidents/YYYY/INC-###-<title>/`: the fact record is
`INC-###-<title>.md`, and the postmortem is `postmortem.md` when needed,
using the approved templates.

## Workflow

### Phase 0: Context Check

1. Use only incident evidence supplied or explicitly approved for this task.
2. Select a partial or full analysis from the requested scope. Do not rename,
   read or replace unrelated existing scratch or personal state.

### Phase 1: Input Collection

Extract from user input:

- **Incident description** — what happened and when
- **Evidence** (optional) — logs, metric screenshots, alert records, chat records
- **Impact information** (optional) — affected services, user count, duration
- **Actions taken** (optional) — emergency measures already performed

Summarize input in the response. Only an explicitly authorized author may
write an assigned scratch or durable document; no automatic scratch creation.

### Phase 2: Timeline Reconstruction → `_workspace/01_timeline.md`

Reconstruct the full event sequence:

```markdown
# Incident Timeline

## Summary

- **Incident ID**: [ID or description]
- **Detection Time**: [YYYY-MM-DD HH:MM UTC]
- **Resolution Time**: [YYYY-MM-DD HH:MM UTC]
- **Total Duration**: [X hours Y minutes]

## Event Log

| Time (UTC) | Event               | Source             | Actor           |
| ---------- | ------------------- | ------------------ | --------------- |
| HH:MM      | [Event description] | [Log/Alert/Verbal] | [System/Person] |

## Gap Analysis

- [Unconfirmed] tags mark events reconstructed from verbal accounts
- Gaps in evidence noted with time range and source limitation
```

### Phase 3: Root Cause Analysis → `_workspace/02_root_cause.md`

Apply structured RCA (see `rca-methodology` skill for full technique guide):

- **5 Whys** for linear cause chains
- **Fishbone** for multi-dimensional factors (People, Process, Technology, Environment, Monitoring)
- **Change Analysis** for deployment-related incidents

```markdown
# Root Cause Analysis

## Primary Root Cause

[One-sentence statement of the root cause]

## Contributing Factors

| Factor   | Category              | Evidence               |
| -------- | --------------------- | ---------------------- |
| [Factor] | [Process/Tech/People] | [Log/metric reference] |

## 5 Whys Chain

Why 1 → [Answer]
Why 2 → [Answer]
...
Root Cause: [Conclusion]
```

### Phase 4: Impact Assessment → `_workspace/03_impact_assessment.md`

```markdown
# Impact Assessment

## Service Impact

| Service | Impact | Duration | Recovery Method |
| ------- | ------ | -------- | --------------- |

## SLA/SLO Status

| SLO | Target | Actual | Error Budget Consumed |
| --- | ------ | ------ | --------------------- |

## Operational Risk

- Security breach indicators: [None/Details]
- Data integrity concerns: [None/Details]
```

### Phase 5: Remediation Planning → `_workspace/04_remediation_plan.md`

```markdown
# Remediation Plan

## Immediate Actions (< 24h)

| Action | Owner | Due | Status |
| ------ | ----- | --- | ------ |

## Short-term Actions (< 2 weeks)

## Long-term Actions (< 3 months)

## Action Items

- [ ] SMART action items with owner, due date, and success criteria
```

### Phase 6: Final Postmortem Report → `_workspace/postmortem_report.md`

```markdown
# Postmortem: [Incident Title]

**Date**: YYYY-MM-DD
**Severity**: P1/P2/P3
**Duration**: X hours Y minutes
**Status**: Resolved

## Summary

[2-3 sentences covering what happened, root cause, and current status]

## Timeline

[Reference or inline from 01_timeline.md]

## Root Cause

[Reference or inline from 02_root_cause.md]

## Impact

[Reference or inline from 03_impact_assessment.md]

## Remediation

[Reference or inline from 04_remediation_plan.md]

## What Went Well

- [System, process, or team behavior that helped]

## Lessons Learned

- [Non-blame, system-focused insights]
```

## Modes by Task Scale

| User Request Pattern                                       | Execution Mode       | Phases                   |
| ---------------------------------------------------------- | -------------------- | ------------------------ |
| "Write a postmortem"                                       | **Full Pipeline**    | 1 → 6                    |
| "Organize the incident timeline"                           | **Timeline Mode**    | 1 → 2 only               |
| "Analyze the root cause"                                   | **RCA Mode**         | 1 → 3                    |
| "Just create remediation measures" (cause analysis exists) | **Remediation Mode** | Phase 5 only             |
| "Review this postmortem"                                   | **Review Mode**      | Validate existing report |

## Data Protocol

- The phase filenames above are optional author output examples. A read-only role returns analysis in its response and writes no files.
- An explicitly authorized author places durable final reports in `docs/05.operations/incidents/YYYY/INC-###-[incident-slug]/postmortem.md` when a postmortem record is requested.
- An explicitly authorized author places durable incident records in `docs/05.operations/incidents/YYYY/INC-###-[incident-slug]/INC-###-[incident-slug].md` when an incident log is requested.
- Use profile `operation/postmortem` and
  `docs/99.templates/templates/operations/postmortem.template.md` as the structural baseline

## Error Handling

| Error Type                        | Strategy                                                            |
| --------------------------------- | ------------------------------------------------------------------- |
| Insufficient incident information | Ask additional questions; tag uncertain parts with `[Unconfirmed]`  |
| Logs/metrics inaccessible         | Reconstruct from verbal accounts; tag with `[Verbal account-based]` |
| Blaming language                  | Rewrite immediately — blameless culture is an absolute principle    |
| Incomplete impact data            | Use conservative estimates with explicit confidence levels          |

## Failure Handling

- Route to `security-auditor.md` if security breach indicators emerge.
- Route to `k8s-implementer.md` if remediation requires manifest changes.
- Escalate to `supervisor.md` if incident scope exceeds cluster boundaries.

## Test Scenarios

### Normal Flow

**Prompt**: "Yesterday at 14:00 UTC the payment namespace was unavailable for 30 minutes. It happened right after an ArgoCD sync and was recovered by rollback. Write a postmortem."
**Expected**: Full pipeline → timeline with sync event → RCA identifying misconfigured resource limits → impact with user count estimate → remediation with canary rollout adoption → formatted postmortem.

### Existing File Flow

**Prompt**: "Review this postmortem" + report provided
**Expected**: Validate structure against template, check blameless language, verify SMART action items, return improvement suggestions.

### Minimal Input Flow

**Prompt**: "The API gateway was slow this morning. Analyze the cause."
**Expected**: Collect missing details via questions, execute RCA mode, mark uncertain parts clearly.

## Related Skills

- `rca-methodology` — Detailed 5 Whys, Fishbone, FTA, and change analysis techniques
