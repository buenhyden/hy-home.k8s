# Agent Quality Standards (March 2026)

Quality gates for governance and execution alignment.

## Required Quality Dimensions

- Accuracy: policy text matches actual workspace behavior.
- Concision: avoid repetitive or generic instructions.
- Actionability: every rule implies a concrete action.
- Consistency: no conflicts across bootstrap, persona, scope, and provider docs.

## Minimum Verification for Governance Updates

- Structure parity with expected governance tree.
- English-only check under `docs/00.agent-governance/`.
- Root shim link checks for `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`.
- Checklist references remain valid (`preflight`, `postflight`, `stage-authoring-matrix`, `stage-checklists`).
- Diff check confirms no unintended edits outside the approved change scope.
