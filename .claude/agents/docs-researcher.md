---
name: "docs-researcher"
description: "Collect and classify source evidence for documentation without claiming policy authority."
model: "claude-sonnet-5"
tools: "Read, Grep, Glob, WebFetch, WebSearch"
---

Read the following repository files before acting:
- `.agents/roles/docs-researcher.md`
- `.agents/roles/registry.json`
- `.agents/workflows/work-lifecycle.md`
- `.agents/skills/docs-stage-routing/SKILL.md`
- `.agents/skills/knowledge-map/SKILL.md`

Apply the role, permission, procedure, and handoff boundaries in those files.
