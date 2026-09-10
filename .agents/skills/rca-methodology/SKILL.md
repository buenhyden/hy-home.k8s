---
name: "rca-methodology"
description: "Use when performing root cause analysis with 5 Whys, Fishbone diagrams, Fault Tree Analysis, change analysis, incident cause analysis, or cognitive-bias checks. Timeline reconstruction and remediation planning are outside this skill's scope."
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# RCA Methodology — Tracing an Incident to Its Cause

Choose a root cause analysis technique for a cluster incident, apply it against
captured evidence, and return the result in the structure this skill owns.

## Workflow Steps

1. State the problem as one observable fact with a time boundary. An analysis
   that starts from a suspicion inherits it as a conclusion.
2. Choose the technique with the selection guide in
   `references/techniques.md`. A linear chain, compound causes, a
   safety-critical failure, and a post-deployment failure each suit a different
   one, and combining 5 Whys with change analysis covers most cases.
3. Apply it against evidence that was captured, citing a log, event, or metric
   at each step. A step that rests on recollection is marked as such rather
   than left to read as established.
4. Run the cognitive-bias checklist before concluding. It exists because the
   first plausible cause is the one an analysis stops at.
5. Return the result in the Output Format below. Where a durable record then
   belongs is owned by the `incident-postmortem` skill and the Stage 99 profile
   it names; this skill owns the technique and the structure, not the
   destination.

## Reference Material

`references/techniques.md` holds the five techniques worked through on a
cluster incident, with their pitfalls and the selection guide. It is read for
the technique in use rather than in full, since an analysis applies one or two.

## Output Format

Return scratch RCA output in the response when acting in a read-only role. An
explicitly authorized author may record it in the assigned Task. Where a
durable finding then belongs is owned by the `incident-postmortem` skill and
the Stage 99 profile it names; this skill owns the technique and the structure
below, not the destination. Use this structure:

```markdown
# Root Cause Analysis

## Primary Root Cause

[One-sentence statement of the confirmed root cause]

## Contributing Factors

| Factor   | Category                         | Evidence                     |
| -------- | -------------------------------- | ---------------------------- |
| [Factor] | [Process/Tech/People/Monitoring] | [Log/event/metric reference] |

## 5 Whys Chain

Why 1: [Question] → [Answer]
Why 2: [Question] → [Answer]
Why 3: [Question] → [Answer]
Why 4: [Question] → [Answer]
Why 5: [Question] → [Answer]
Root Cause: [Conclusion]

## Bias Checks Performed

- [ ] Counterexamples searched
- [ ] Evidence-based (not verbal assumption)
- [ ] System/process focus confirmed (no blame language)
```
