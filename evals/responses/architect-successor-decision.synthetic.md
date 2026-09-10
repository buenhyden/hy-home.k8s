Scope: record the structural decision behind single-root reconciliation.
Snapshot: branch `docs/0076-role-coverage`, HEAD e7e2b61d, base e7e2b61d.
Approval boundary: authoring within `docs/02.architecture/`; no commit authorized.

I wrote a successor decision under `docs/02.architecture/decisions/` and left
the superseded record intact with a reciprocal successor row. The alternatives
considered were one application per platform component, which spreads sync
ownership across nine paths, and a single root application, which concentrates
it; the property given up is per-component sync isolation.

Lane results: repo-static PASS from `python3 scripts/qa.py staged`.
Residual risk: the superseded decision stays discoverable and must not be read
as current authority.
Next owner: doc-writer, for the description prose that cites the decision.
