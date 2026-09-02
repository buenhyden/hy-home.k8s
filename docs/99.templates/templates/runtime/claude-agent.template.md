---
name: "{role-name}"
description: "One sentence naming the bounded responsibility this role executes."
model: "{claude-model-id}"
tools: "{Read, Grep, Glob}"
---

# {role-name}

## Runtime Bootstrap

Load the provider gateway, the work lifecycle procedure, this role's
responsibility, and the active Task before acting.

## Responsibility

State the bounded outcome this role owns and the surfaces it may write.

## Authority Boundary

Name what this role must not do, including any protected action it must hand
back rather than perform.

## Evidence

Name the checks this role runs and the lane each result is reported under.
