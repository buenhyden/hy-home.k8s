Scope: review the egress NetworkPolicy change for routing correctness.
Snapshot: branch `gitops/network-policy-egress`, HEAD 561ca9a0, base 561ca9a0.
Approval boundary: manifest-static review within `gitops/platform/network-policies/`; no live probing and no write.

The policy at `gitops/platform/network-policies/monitoring-egress.yaml` selects
the monitoring workloads and permits egress to the external services the
change adds, and `gitops/platform/network-policies/kustomization.yaml` lists it
so the resource is actually rendered. The selector and the listed resource
agree, which is the structural question this review owns.

Whether that egress widens an isolation boundary is a different question and
is not settled here.

Lane results: repo-static PASS from `bash scripts/validate-gitops-structure.sh`.
No live resolution, handshake or probe was performed and none is claimed.
Residual risk: none identified for the wiring itself.
Next owner: security-auditor, for the isolation judgment this review stops at.
