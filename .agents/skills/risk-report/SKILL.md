---
name: "risk-report"
description: "Use when identifying, scoring, and reporting cluster-specific operational or security risks in a risk register."
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# risk-report

## Purpose

Define how to identify, score, and report cluster risks in a repeatable format for `hy-home.k8s`.

## Trigger Phrases

- "create a risk register"
- "analyze cluster risk"
- "summarize operational risk"
- "prepare a risk review"

## When NOT to Use

- Auditing cluster security posture; use `k8s-security-audit`.
- Matching manifests to known-bad shapes; use `vulnerability-patterns`, which owns pattern-to-level.
- Analysing an incident that already happened; use `rca-methodology`.

## Workflow Steps

1. Identify risks across security, availability, operations, and change management.
2. Score each risk with the scale below.
3. Record leading indicators or monitoring hooks where applicable.
4. Produce a cluster-specific risk summary with recommended actions.

## Scoring

Rate likelihood from the evidence in hand rather than from intuition, so two
reviewers reading the same repository reach the same row.

| Likelihood   | Meaning                                                                     |
| ------------ | --------------------------------------------------------------------------- |
| **Likely**   | Observed in this repository or cluster now, or it has already happened here |
| **Possible** | The enabling condition is present but no occurrence is observed             |
| **Unlikely** | It needs a condition that is absent and would itself take a change          |

Rate impact by blast radius rather than by how alarming the finding sounds.

| Impact       | Meaning                                                        |
| ------------ | --------------------------------------------------------------- |
| **Severe**   | Credential exposure, data loss, or cluster-wide unavailability |
| **Moderate** | One namespace or workload degraded, recoverable by rollback    |
| **Minor**    | Operational friction with no user-visible effect               |

The pair gives the level. Rows are likelihood, columns are impact.

| Likelihood   | Minor  | Moderate | Severe   |
| ------------ | ------ | -------- | -------- |
| **Likely**   | MEDIUM | HIGH     | CRITICAL |
| **Possible** | LOW    | MEDIUM   | HIGH     |
| **Unlikely** | LOW    | LOW      | MEDIUM   |

The level decides how the register carries the risk.

| Level    | Register disposition                                          |
| -------- | -------------------------------------------------------------- |
| CRITICAL | Blocking — the change under review does not proceed            |
| HIGH     | Release-blocking — name the owner and the release it blocks    |
| MEDIUM   | Monitor-only — name a review cue and the signal that raises it |
| LOW      | Monitor-only — revisit at the next risk review                 |

These four level names mean the same thing the security skills mean by them,
so a reviewer holding both reads one vocabulary. Where `vulnerability-patterns`
has already assigned a severity to a manifest pattern, take that severity as
given; this matrix scores what no pattern table has classified.

## Constraints

- Keep the register specific to `hy-home.k8s`.
- Prefer repository and approved inspection evidence over generic risk lists.
- A risk whose likelihood rests on no evidence is not scored. Record it as an
  open question, because an invented score is harder to retract than a stated gap.

## Expected Outputs

- A structured risk register or risk summary
- Severity-ranked recommendations
- Monitoring or review cues for follow-up work

## Failure Handling

- If live inspection is unavailable, fall back to repository-backed static analysis and state the limitation.
- If security-critical findings emerge, escalate to the security review owner.
- If ownership or routing is unclear, escalate to the supervising owner.
