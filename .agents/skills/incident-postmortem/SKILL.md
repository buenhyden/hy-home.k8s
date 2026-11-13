---
name: "incident-postmortem"
description: "Use when writing a cluster incident postmortem or routing post-incident analysis through timeline reconstruction, root cause analysis, impact assessment, and remediation planning. Real-time on-call response, monitoring setup, and alert configuration are outside this skill's scope."
metadata:
  title: "Incident Postmortem"
  version: "1.0.4"
  type: "governance/skill"
  status: "active"
  owner: "platform"
  updated: "2026-11-13"
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# Incident Postmortem — Cluster Incident Post-Analysis Pipeline

## Purpose and Trigger

### When to Use

The `incident-responder` agent leads timeline reconstruction → root cause analysis → impact assessment → remediation planning → postmortem report generation.

### When Not to Use

- Applying one analysis technique rather than running the pipeline; use `rca-methodology`.
- Turning a remediation into a repeatable operational procedure; use `ops-runbook`.
- Recording residual risk for later tracking; use `risk-report`.

#### Workspace Boundary

`_workspace/repo-support/analysis/` is scratch-only for intermediate analysis
(see `_workspace/README.md`). A durable fact record belongs to the
`operation/incident` profile and its analysis to `operation/postmortem`. The
Stage 99 registry (`docs/99.templates/registry.json`) owns the directory
grammar, filename, template, and required sections for both; resolve the
profile at write time rather than copying a path out of this procedure. Use the
current operations README for navigation.

## Procedure

### Steps

#### Execution Mode

The read-only `incident-responder` analyzes approved evidence and returns a
report draft. An authorized author owns any durable document writes; this
skill never expands the responder's permissions.

#### Workflow

##### Phase 0: Context Check

1. Use only incident evidence supplied or explicitly approved for this task.
2. Select a partial or full analysis from the requested scope. Do not rename,
   read or replace unrelated existing scratch or personal state.

##### Phase 1: Input Collection

Extract from user input:

- **Incident description** — what happened and when
- **Evidence** (optional) — logs, metric screenshots, alert records, chat records
- **Impact information** (optional) — affected services, user count, duration
- **Actions taken** (optional) — emergency measures already performed

Summarize input in the response.

##### Phase 2: Timeline Reconstruction

Reconstruct the event sequence (UTC time, event, source, actor) with detection
time, resolution time and duration. Tag events reconstructed from verbal
accounts `[Verbal account-based]` and mark gaps with their time range and source
limitation. The durable form is the `operation/incident` template
(registry entry; see [Stage 99 templates](../../../docs/99.templates/README.md)).

##### Phase 3: Root Cause Analysis

Apply structured RCA (see `rca-methodology` for the technique guide):

- **5 Whys** for linear cause chains
- **Fishbone** for multi-dimensional factors (People, Process, Technology, Environment, Monitoring)
- **Change Analysis** for deployment-related incidents

Write the Root Cause Analysis structure that `rca-methodology` defines under
its Output Format heading. That skill owns the structure; this phase decides
which techniques the incident needs.

##### Phase 4: Impact Assessment

Cover service impact (service, impact, duration, recovery method), SLO status
(target, actual, error budget consumed), and operational risk (security breach
indicators, data integrity concerns). The incident template carries the
impact fields; state estimates with their confidence.

##### Phase 5: Remediation Planning

Group actions by horizon (immediate under 24 h, short-term under 2 weeks,
long-term under 3 months). Each action item is SMART: owner, due date and
success criterion. The postmortem template carries them under Corrective
Actions (Actions and Verification); the closing approver goes in Evidence >
Review Decision.

##### Phase 6: Final Postmortem Report

Assemble the report in the `operation/postmortem` template
(registry entry; see [Stage 99 templates](../../../docs/99.templates/README.md)), which owns its
section set and ordering. Severity uses the incident template's SEV-1 to SEV-4 scale.
Keep the language blameless and system-focused.

#### Modes by Task Scale

| User Request Pattern                                       | Execution Mode       | Phases                   |
| ---------------------------------------------------------- | -------------------- | ------------------------ |
| "Write a postmortem"                                       | **Full Pipeline**    | 1 → 6                    |
| "Organize the incident timeline"                           | **Timeline Mode**    | 1 → 2 only               |
| "Analyze the root cause"                                   | **RCA Mode**         | 1 → 3                    |
| "Just create remediation measures" (cause analysis exists) | **Remediation Mode** | Phase 5 only             |
| "Review this postmortem"                                   | **Review Mode**      | Validate existing report |

### Failure Handling

| Error Type                        | Strategy                                                            |
| --------------------------------- | ------------------------------------------------------------------- |
| Insufficient incident information | Ask additional questions; tag uncertain parts with `[Unconfirmed]`  |
| Logs/metrics inaccessible         | Reconstruct from verbal accounts; tag with `[Verbal account-based]` |
| Blaming language                  | Rewrite immediately — blameless culture is an absolute principle    |
| Incomplete impact data            | Use conservative estimates with explicit confidence levels          |

- Route to the security review owner if security breach indicators emerge.
- Route to the implementation owner if remediation requires manifest changes.
- Escalate to the supervising owner if incident scope exceeds cluster boundaries.

## Inputs and Outputs

### Inputs

Under the execution mode stated above, a read-only role returns the analysis in
its response and writes nothing. Creating a scratch file under
`_workspace/repo-support/analysis/` is a write like any other and needs
authorization. A durable record takes its path, template, and required sections
from the Stage 99 registry entry for the profile being written.

### Outputs

This procedure defines no output format of its own beyond the results its Steps describe; if it needs one, define it here.

## Verification

### Checks

The test scenarios are stated below.

#### Normal Flow

**Prompt**: "Yesterday at 14:00 UTC the payment namespace was unavailable for 30 minutes. It happened right after an ArgoCD sync and was recovered by rollback. Write a postmortem."
**Expected**: Full pipeline → timeline with sync event → RCA separating observed evidence from unconfirmed causes → impact with explicitly bounded estimates → remediation justified by the established cause → formatted postmortem.

#### Existing File Flow

**Prompt**: "Review this postmortem" + report provided
**Expected**: Validate structure against template, check blameless language, verify SMART action items, return improvement suggestions.

#### Minimal Input Flow

**Prompt**: "The API gateway was slow this morning. Analyze the cause."
**Expected**: Collect missing details via questions, execute RCA mode, mark uncertain parts clearly.

### Completion and Handoff

- `rca-methodology` — Detailed 5 Whys, Fishbone, FTA, and change analysis techniques
- `ops-runbook` — Turning a remediation into a repeatable operational procedure
- `risk-report` — Recording residual risk for later tracking
