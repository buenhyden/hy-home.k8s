# AI Agents Guide

This project leverages AI agents to assist in development and maintenance.

## Recommended Agents

### Antigravity

- **Role**: Primary coding and infrastructure assistant.
- **Strengths**: Understanding the entire workspace context, creating detailed implementation plans, executing multi-step tasks, and following GitOps workflows.
- **Usage**: Use Antigravity for large refactors, new feature implementations, and documentation updates.

### Claude / Gemini

- **Role**: Specialized assistants for code review, logic optimization, and documentation.
- **Instruction Files**: See `CLAUDE.md` and `GEMINI.md` for specific instructions.

## Agent Guidelines

1. **Context Awareness**: Always provide agents with the relevant workspace context.
2. **Review Plans**: Carefully review the `implementation_plan.md` created by agents before execution.
3. **Verify Changes**: Agents must verify their changes (e.g., linting, manifest validation) before creating a walkthrough.
4. **AI Disclosure**: Mark the use of AI tools in pull request descriptions.
