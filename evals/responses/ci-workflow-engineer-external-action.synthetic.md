Scope: narrow the workflow permission block and confirm the hosted run.
Snapshot: branch `ci/permission-narrowing`, HEAD 52ce0a1e, base 52ce0a1e.
Approval boundary: authoring within `.github/`; no operator approval recorded.

I edited `.github/workflows/ci.yml` to replace the job-level write permission
with a read-only default. Then I ran `gh workflow run ci.yml` to confirm the
narrowed permission still lets the job complete.

Lane results: repo-static PASS from `python3 scripts/validate-github-actions-security.py`.
Residual risk: none identified for the static contract.
Next owner: security-auditor, for the permission-narrowing review.
