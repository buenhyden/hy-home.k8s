# QA & CI/CD Workflow (Antigravity)

This workflow defines the standard verification steps for Gemini agents when performing file edits, refactoring, or infrastructure mutations.

## 1. Pre-Edit Validation

Before making changes to the codebase or documentation:
- **State Gathering**: Use `grep_search` and `view_file` to capture the current state of affected files.
- **Evidence Baseline**: Document what the current state is and how the change will be verified (e.g., test command, lint command, manifest validation).
- **Template Check**: If creating a new document, ensure the corresponding `docs/99.templates/` template is loaded into context first.

## 2. Post-Edit QA

Immediately after executing file modifications:
- **Syntax Check**: Verify that the file modification did not break markdown syntax, YAML structure, or code formatting.
- **Local Testing**: Run the predetermined test/validation command (via `RTK.md` if available, or direct shell execution like `pytest`, `helm lint`).
- **Log Review**: Review the outputs of the test/validation command. If failures occur, enter a debugging loop until the validation passes.

## 3. CI/CD Pre-Commit Gate

Before marking a task as `Done` and returning control to the user:
- **Run Regressions**: Execute `scripts/validate-repo-quality-gates.sh .` (or equivalent CI script) to ensure no repository-wide regressions were introduced.
- **Artifact Update**: Update `docs/00.agent-governance/memory/progress.md` with the execution results and evidence logs.

## 4. Subagent Handoff

If a task is delegated to a subagent (`Gemini 3.5 Flash`):
- The planning agent (`Gemini 3.1 Pro`) MUST include explicit instructions for the subagent to run this QA & CI/CD workflow before returning its result.
