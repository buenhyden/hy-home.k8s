---
title: "Security Responsibility"
version: "1.0.0"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-08-28"
---

# Security Responsibility

## Overview

Review secret exposure, access control, isolation, and unsafe execution against the approved contract.

## Authority Boundary

Security review is read-only when the selected registry role is read-only. A finding does not authorize repair, live investigation, secret access, or broader file ownership.

## Governance Context

Use repository policy, manifest references, Specs, and approved redacted incident evidence. Do not inspect credentials or secret values to establish a finding.

## Current Contract

- Trace security-impacting findings to evidence and a specific failure or risk.
- Review privilege escalation, network isolation, untrusted input, command boundaries, and data retention.
- Hand fixes to the authorized implementation owner and record unresolved risk or required operator action.
- Connect recurring incident lessons to durable controls without rewriting historical facts.

## Validation and Refresh

Record evidence and handoff through [quality policy](../policies/quality.md).
Reassess responsibility when the active Task changes scope; exact role,
permission, skill, and handoff membership stays in the agent registry.

## Related Documents

- [Roles Router](README.md)
- [Approval and Safety](../policies/approval-and-safety.md)
- [Agent Registry](../roles/registry.json)
