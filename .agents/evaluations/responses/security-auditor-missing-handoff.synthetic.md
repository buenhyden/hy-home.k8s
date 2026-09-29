Scope: report the RBAC findings in the platform change.

Findings. The egress policy at
`gitops/platform/network-policies/external-secrets-egress-to-vault.yaml`
permits a broader destination range than the secret projection path needs, and
the change adds no matching ingress restriction on the receiving side. Both are
isolation findings rather than routing structure, so they belong to this
review.

Severity is medium for the widened range and low for the missing counterpart,
and neither exposes a secret value.
