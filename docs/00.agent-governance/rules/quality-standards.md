# Agent Quality Standards (March 2026)

Quality gates for governance and execution alignment.

## Required Quality Dimensions

- Accuracy: policy text matches actual workspace behavior.
- Concision: avoid repetitive or generic instructions.
- Actionability: every rule implies a concrete action.
- Consistency: no conflicts across bootstrap, persona, scope, and provider docs.

## Coverage Applicability

- Future testable application code should target at least 90% line and branch coverage where a language-specific test framework and coverage tool exist.
- Current Bash/YAML/Markdown infrastructure work uses validation-matrix coverage instead of fake numeric code coverage.
- The validation matrix for this repository includes repository quality gates, GitOps structure checks, Kubernetes manifest syntax, static infrastructure contracts, secret handling scans, shell syntax, CI workflow checks, README/template checks, and explicit live-check limitations.
- PR verification must state which coverage lane applies: 90% code coverage for future testable application code, or validation-matrix coverage for current infrastructure artifacts.

## Minimum Verification for Governance Updates

- Structure parity with expected governance tree.
- English-only check under `docs/00.agent-governance/`.
- Root shim link checks for `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`.
- Checklist references remain valid (`preflight`, `postflight`, `stage-authoring-matrix`, `stage-checklists`).
- Diff check confirms no unintended edits outside the approved change scope.
