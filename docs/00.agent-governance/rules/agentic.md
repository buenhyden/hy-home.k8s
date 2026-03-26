# Agentic Execution Rules

Rules for autonomous task execution quality and safety.

## Execution Contract

- Complete `rules/preflight-checklist.md` before substantial work.
- Always identify target layer before editing.
- Always load matching scope rules before taking action.
- Use the smallest set of rules required for the task.
- Complete `rules/postflight-checklist.md` before completion.

## Persona and Rule Enforcement

- Every non-trivial task must align to one persona in `rules/persona.md`.
- If work spans layers, process one layer at a time and declare transitions.

## Escalation and Safety

- Stop and ask for clarification when requirements conflict.
- Do not silently override explicit user constraints.
- Record non-obvious lessons in `memory/` when recurrence risk exists.
