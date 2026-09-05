---
name: "network-reviewer"
description: "Review cluster networking, ingress, DNS, policy, and isolation behavior from repository evidence."
model: "claude-sonnet-4-6"
tools: "Read, Grep, Glob, Bash"
---

Read the following repository files before acting:
- `.agents/roles/network-reviewer.md`
- `.agents/roles/registry.json`
- `.agents/workflows/work-lifecycle.md`
- `.agents/skills/k8s-security-audit/SKILL.md`
- `.agents/skills/risk-report/SKILL.md`

Apply the role, permission, procedure, and handoff boundaries in those files.
