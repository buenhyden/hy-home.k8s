Scope: regenerate both provider projections after a registry skill reference changed.
Snapshot: branch `docs/0076-role-coverage`, HEAD 66305bcb, base 66305bcb.
Approval boundary: authoring within `.agents/` and the two adapter trees; no commit authorized.

I edited `.agents/roles/registry.json` and regenerated the two projections from
it rather than editing them by hand, so the reading list and the native
metadata both follow the registry entry. The permission class was not changed.

Lane results: repo-static PASS from `python3 scripts/validate-agent-governance.py`.
Provider discovery and runtime enforcement were not observed and are not claimed.
Residual risk: none identified for this change.
Next owner: quality-engineer, for the staged profile on the exact index.
