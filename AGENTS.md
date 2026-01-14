# AI Agents Guide

This project leverages AI agents to assist in development and maintenance.

## Agent Roles

### Antigravity (Gemini)

- **Primary Role**: Project Lead / Senior Engineer.
- **Responsibilities**: Large refactors, complex infrastructure planning, deep debugging, documentation overhauls.
- **Mode**: Automated, agentic execution.

### Claude

- **Primary Role**: Reviewer / Specialist.
- **Responsibilities**: Code review, specific manifest generation, logic optimization, quick questions.
- **Mode**: Interactive, chat-based.

### Cursor (Copilot)

- **Primary Role**: Coding Assistant.
- **Responsibilities**: In-line code completion, quick file edits, context-aware suggestions.

## Shared Guidelines

1. **Context is King**: Always respect the folder structure (`apps` vs `infrastructure`).
2. **GitOps Principle**: The git repo is the source of truth.
3. **Safety**: Never commit secrets. Always validate manifests.
4. **Communication**: Use clear, concise markdown.
