# Git Workflow

## Branch Roles

- `main`: production and release baseline.
- `dev`: integration baseline for active development.

## Adapted Git Flow

### Standard work from `dev`

Start these branch types from `dev`:

- `feat/<ticket-or-domain>-<slug>`
- `fix/<ticket-or-domain>-<slug>`
- `docs/<ticket-or-domain>-<slug>`
- `refactor/<ticket-or-domain>-<slug>`
- `chore/<ticket-or-domain>-<slug>`

Default pull request target for these branches is `dev`.

### Release flow

- Create `release/<version-or-slug>` from `dev`.
- Stabilize and verify on the release branch.
- Merge release branch into both `main` and `dev`.
- Use this when preparing deployable cuts, version promotions, or coordinated release validation.

### Hotfix flow

- Create `hotfix/<ticket-or-domain>-<slug>` from `main`.
- Apply only the production-critical fix.
- Merge hotfix branch into both `main` and `dev`.
- Use this for production regressions, security patches, or urgent deploy blockers.

## Naming Rules

- Use lowercase kebab-case after the prefix.
- Format: `<type>/<ticket-or-domain>-<slug>`.
- Examples:
  - `feat/web-search-shell`
  - `docs/00-agent-md-refactor`
  - `hotfix/web-build-export-regression`
  - `release/2026-03-web-renewal-v2`

## Commit and PR Discipline

- Use Conventional Commits.
- Keep commits atomic and traceable.
- Prefer PRs into `dev` unless the branch is `release/*` or `hotfix/*`.
- Re-run the relevant verification ladder before opening or updating a PR.
- Do not force-push protected branches.

## Recommended Workflow Helpers

These helpers are recommended when they fit the task, but they are not mandatory:

- `git-advanced-workflows`
- `git-pr-workflows-git-workflow`
- `git-flow-branch-creator`

Use them to accelerate clean branch creation, history cleanup, PR preparation, and merge/rebase recovery without making the repository dependent on any one helper.
