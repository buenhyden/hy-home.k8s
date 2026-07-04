# Security Policy

## Supported Versions

We currently support the following versions of the `hy-home.k8s` platform:

| Version | Supported          |
| ------- | ------------------ |
| v1.0.x  | :white_check_mark: |
| < v1.0  | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please follow these steps:

1. **Do NOT** open a public issue.
2. Contact the maintainer directly through the repository owner profile or an existing private maintainer channel.
3. Provide a detailed description of the vulnerability and steps to reproduce.

Do not include secret values, Vault tokens, private keys, or credential
material in reports. Secret-handling and protected-surface boundaries are
routed through
[`docs/00.agent-governance/rules/approval-boundaries.md`](../docs/00.agent-governance/rules/approval-boundaries.md).

We will acknowledge receipt of your report within 48 hours and provide a timeline for resolution if the vulnerability is confirmed.
