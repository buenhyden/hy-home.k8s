# 00. Agent Governance

This folder contains the dedicated execution instructions and rules for AI agents performing sagas within the `hy-home.k8s` project. All agents must prioritize and adhere to the guidelines provided in this folder.

## 1. Operating Principles and Language Guide

The following language principles are enforced to ensure efficient context management and accurate task execution:

- **Internal Documentation (Internal Docs)**: All instructions interpreted by AI agents (Rules, Scopes, Providers) MUST be written in **English**. This maximizes the model's reasoning accuracy and optimizes token usage.
- **Language Mandate**: Even though human-facing READMEs elsewhere may be in Korean, all files within `docs/00.agent/` are strictly English-only to serve as reliable machine-readable governance.
- **Response Protocol**: Regardless of the internal documentation language, all responses to user requests must be delivered in **Korean (한국어)**.

## 2. Lazy Loading Protocol (JIT)

Agents do not load all documents at the start of a session. Instead, they follow the Just-In-Time (JIT) protocol:

1. **Intent Identification**: Determine the nature of the requested task.
2. **Bootstrap Loading**: Load [rules/bootstrap.md](rules/bootstrap.md) to verify the core taxonomy.
3. **Scope Loading**: Load only the specific detailed instructions from the [scopes/](scopes/) directory that match the identified task layer.

## 3. Core Components

- **[agent-instructions.md](agent-instructions.md)**: The unified gateway for all agent executions.
- **[rules/persona-matrix.md](rules/persona-matrix.md)**: A mapping table for persona-specific tasks and rule layers.
- **[claude-provider.md](claude-provider.md) / [gemini-provider.md](gemini-provider.md)**: Optimization guidelines tailored for specific AI model engines.

---
> [!IMPORTANT]
> Any changes to the Agent Operating Policy must undergo the control procedures defined in [08.operations/](../08.operations/README.md).
