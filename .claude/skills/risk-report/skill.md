---
name: risk-report
description: Risk register workflow for identifying, scoring, and reporting cluster-specific operational and security risks.
---

# risk-report

## Purpose

Define how to identify, score, and report cluster risks in a repeatable format for `hy-home.k8s`.

## Trigger Phrases

- "create a risk register"
- "analyze cluster risk"
- "summarize operational risk"
- "prepare a risk review"

## Workflow Steps

1. Identify risks across security, availability, operations, and change management.
2. Score risks using a simple likelihood and impact model.
3. Record leading indicators or monitoring hooks where applicable.
4. Produce a cluster-specific risk summary with recommended actions.

## Constraints

- Keep the register specific to `hy-home.k8s`.
- Prefer repository and approved inspection evidence over generic risk lists.
- Distinguish blocking risks from monitor-only risks.
- Do not create source-path lineage or upstream reference leakage in the output.

## Expected Outputs

- A structured risk register or risk summary
- Severity-ranked recommendations
- Monitoring or review cues for follow-up work

## Failure Handling

- If live inspection is unavailable, fall back to repository-backed static analysis and state the limitation.
- If security-critical findings emerge, escalate to `security-auditor.md`.
- If ownership or routing is unclear, escalate to `supervisor.md`.
