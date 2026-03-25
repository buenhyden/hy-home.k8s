# Contextual Memory (`docs/00.agent-governance/memory/`)

This directory stores historical context, lessons learned, and "gotchas" discovered during development. It prevents regression and repeats of past mistakes.

## 1. Governance Strategy

Memory is not a full archive of everything but a curated collection of non-obvious insights.

- **Primary Goal**: Improve agent performance by providing contextually relevant history.
- **Language**: English (Technical/Technical Insight).

## 2. Usage Policy

- **Record**: Create a new entry (using `template.md`) after a post-mortem or after resolving a complex, non-obvious issue.
- **Search**: This is triggered during **Step 5** of the JIT protocol (Context-Aware Loading).
- **Format**: Follow `template.md` (Problem, Context, Solution, Prevention).

---
*Ref: [agent-instructions.md](../agent-instructions.md)*
