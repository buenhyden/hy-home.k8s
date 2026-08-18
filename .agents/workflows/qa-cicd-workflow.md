# QA and CI Workflow

This workflow defines the standard verification steps for local provider adapters
when performing file edits, refactoring, or infrastructure mutations in
`hy-home.k8s`.

## 1. Pre-Edit Validation

Before making changes to the codebase or documentation:

- **State Gathering**: Use the provider's read/search tools to capture the current state of affected files.
- **Evidence Baseline**: Document what the current state is and how the change will be verified (e.g., test command, lint command, manifest validation).
- **Template Check**: If creating a new document, resolve the route through `docs/99.templates/support/document-contract.md` and load the matching template under `docs/99.templates/templates/` first.

## 2. Canonical Post-Edit QA

The sole order, lane, result, formatter, and handoff semantics owner is
`docs/00.agent-governance/rules/quality-standards.md`. This workflow
operationalizes that owner without redefining its meanings:

`targeted -> affected -> staged -> tests -> all-files -> formatter-review -> rerun -> diff-checks`

1. **targeted**: Run the predetermined focused test or validation command for
   the edited surface and review its output.
2. **affected**: Write every changed repository-relative POSIX path as a
   NUL-terminated record and run
   `python3 scripts/run-validation-lane.py --root . --lane affected --paths-file
   <paths.nul> --delimiter nul`. Never reconstruct machine-produced paths
   through newline iteration or shell command substitution.
3. **staged**: Stage the exact logical file set, create a NUL-delimited path
   inventory from that exact index, run
   `python3 scripts/run-validation-lane.py --root . --lane staged --paths-file
   <staged-paths.nul> --delimiter nul`, and then run plain `pre-commit run`
   against the same exact Git index. The affected and all-files runner modes
   are not staged substitutes.
4. **tests**: Run the relevant direct test suites and
   `bash scripts/validate-repo-quality-gates.sh .` when the repository
   aggregate applies; review every result.
5. **all-files**: Run `pre-commit run --all-files`. A separate
   `run-validation-lane.py --lane all-files` invocation may provide
   contract-selected repository-static evidence, but it is not completion
   evidence for this step or for `staged`.
6. **formatter-review**: Inspect `git status --short`, `git diff`, and
   `git diff --cached` for every formatter mutation and confirm each changed
   file remains within the approved scope.
7. **rerun**: If a formatter changes any file, review it, restage the exact
   logical set, and rerun `affected`, both staged checks, and
   `pre-commit run --all-files`; the mutating invocation is not completion
   evidence.
8. **diff-checks**: Run `git diff --check` and
   `git diff --cached --check`, verify final staged and unstaged scope, and
   record all eight results through the canonical owner vocabulary.

Provider payload paths must pass control-byte, whitespace, normalization, root,
symlink, and canonical selector validation before any formatter or pre-commit
hook receives them. Existing affected Markdown, including untracked edits, is
passed to the exact document validators through contract-owned
`--include-path` arguments. A present scalar alias must contain one non-empty
string and cannot shadow a second alias; `files`/`paths` accept only one
explicitly present string list. Child output stays within the bounded runner
evidence contract owned by the quality standard.

Update `docs/00.agent-governance/memory/progress.md` with the execution results
and evidence logs when the task scope authorizes that repository change.

## 3. CI/static QA Boundary

Local results remain scoped to the evidence class defined by the canonical
quality owner. They do not prove provider discovery, hosted CI, Kubernetes
convergence, or cloud availability.

## 4. Subagent Handoff

If a task is delegated to a subagent:

- The planning or supervising agent MUST include explicit instructions for the subagent to run this QA and CI workflow before returning its result.
- Use the provider-specific model tier from `docs/00.agent-governance/harness-catalog.md`; do not hard-code a Gemini-only model in this shared workflow.
