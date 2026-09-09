# Security Policy

## Supported Versions

We currently support the following versions of the `hy-home.k8s` platform:

| Version                     | Supported          |
| --------------------------- | ------------------ |
| `main` at its current commit | :white_check_mark: |
| any earlier commit           | :x:                |

This repository publishes no release tag, so support is stated against the
integration branch rather than a version series.

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please follow these steps:

1. **Do NOT** open a public issue.
2. Contact the maintainer directly through the repository owner profile or an existing private maintainer channel.
3. Provide a detailed description of the vulnerability and steps to reproduce.

Do not include secret values, Vault tokens, private keys, or credential
material in reports. Secret-handling and protected-surface boundaries are
routed through
[`.agents/governance/approval-and-safety.md`](../.agents/governance/approval-and-safety.md).

We will acknowledge receipt of your report within 48 hours and provide a timeline for resolution if the vulnerability is confirmed.
