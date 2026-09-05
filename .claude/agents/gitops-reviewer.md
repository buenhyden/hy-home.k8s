---
name: "gitops-reviewer"
description: "Review GitOps manifests and reconciliation behavior without assuming mutation authority."
model: "claude-sonnet-4-6"
tools: "Read, Grep, Glob, Bash"
---

Read the following repository files before acting:
- `.agents/roles/gitops-reviewer.md`
- `.agents/roles/registry.json`
- `.agents/workflows/work-lifecycle.md`
- `.agents/skills/gitops-workflow/SKILL.md`
- `.agents/skills/k8s-validate/SKILL.md`

Apply the role, permission, procedure, and handoff boundaries in those files.
