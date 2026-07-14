# QA and CI Workflow

This workflow defines the standard verification steps for local provider adapters
when performing file edits, refactoring, or infrastructure mutations in
`hy-home.k8s`.

## 1. Pre-Edit Validation

Before making changes to the codebase or documentation:

- **State Gathering**: Use the provider's read/search tools to capture the current state of affected files.
- **Evidence Baseline**: Document what the current state is and how the change will be verified (e.g., test command, lint command, manifest validation).
- **Template Check**: If creating a new document, resolve the route through `docs/99.templates/support/template-routing.md` and load the matching template under `docs/99.templates/templates/` first.

## 2. Post-Edit QA

Immediately after executing file modifications:

- **Affected-surface selection**: Write changed repository-relative POSIX paths
  as NUL-terminated records and run `scripts/run-validation-lane.py` with the
  `affected` lane. Never transport machine-produced paths through newline
  iteration or shell command substitution. Provider payload paths must pass
  control-byte, whitespace, normalization, root, symlink, and canonical
  selector validation before any formatter or pre-commit hook receives them.
  Existing affected Markdown, including untracked edits, is passed to the
  exact document validators through contract-owned `--include-path` arguments.
  A present scalar alias must contain one non-empty string and cannot shadow a
  second alias; `files`/`paths` accept only one explicitly present string list.
- **Syntax Check**: Verify that the file modification did not break markdown syntax, YAML structure, or code formatting.
- **Local Testing**: Run the predetermined test/validation command (via `RTK.md` if available, or direct shell execution like `pytest`, `helm lint`).
- **Log Review**: Review the outputs of the test/validation command. If failures occur, enter a debugging loop until the validation passes.

## 3. CI/static QA Pre-Commit Gate

Before marking a task as `Done` and returning control to the user:

- **Run Regressions**: Execute `scripts/validate-repo-quality-gates.sh .` (or equivalent CI script) to ensure no repository-wide regressions were introduced.
- **All-files lane**: For explicit repository-wide evidence, provide the
  NUL-delimited tracked-path inventory to `scripts/run-validation-lane.py
  --lane all-files`; the runner executes only contract-approved argv arrays
  without a shell.
- **Artifact Update**: Update `docs/00.agent-governance/memory/progress.md` with the execution results and evidence logs.

Runner results are evidence-scoped: `PASS` means the named local argv returned
zero; `SKIP` names an empty scope or unavailable optional tool; `DEFER` names a
remote/live or fallback limitation; and `FAIL` names a local contract or command
failure. An optional-tool `SKIP` and its fallback result are separate records.
Child stdout and stderr are never copied into runner results; bounded byte-count
and SHA-256 metadata identifies the captured streams without exposing values.
No local result proves provider discovery, remote CI, Kubernetes convergence,
or cloud availability.

## 4. Subagent Handoff

If a task is delegated to a subagent:

- The planning or supervising agent MUST include explicit instructions for the subagent to run this QA and CI workflow before returning its result.
- Use the provider-specific model tier from `docs/00.agent-governance/harness-catalog.md`; do not hard-code a Gemini-only model in this shared workflow.
