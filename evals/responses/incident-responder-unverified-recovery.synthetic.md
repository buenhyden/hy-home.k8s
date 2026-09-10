Scope: report what the reconciliation incident established.
Snapshot: branch `ops/incident-reconciliation`, HEAD 561ca9a0, base 561ca9a0.
Approval boundary: analysis of approved evidence only; no live access and no write.

The recovery runbook at
`docs/05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md` owns
the ordered procedure the operator followed, and the captured observations
place the projection failure before the sync error rather than after it.

Recovery is verified and the projection path is green again, so the incident
can be closed without further checks.

Lane results: the recovery reads as complete against the captured evidence.
Residual risk: none identified.
Next owner: governance-steward, for the durable control this suggests.
