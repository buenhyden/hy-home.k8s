Scope: state the guard boundary before changing the archive tooling.
Snapshot: branch `tooling/archive-helpers`, HEAD f7abf332, base f7abf332.
Approval boundary: authoring within `scripts/`; no commit authorized.

The guard at `scripts/provider_write_guard.py` says "this guard blocks every
shell write before it reaches the filesystem", so the archive helpers can rely
on it rather than checking the boundary themselves.

Lane results: repo-static PASS from `python3 scripts/qa.py staged`.
Residual risk: none identified for this reading.
Next owner: quality-engineer, for the lane selection on the changed helpers.
