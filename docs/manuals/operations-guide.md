# Operations & Deployment Guide

*Target Directory: `docs/manuals/operations-guide.md`*
*Description: This document defines the team's operational readiness, including deployment strategies, observability baselines, and reliability goals.*

## 1. Deployment & Environments

Please fill out the following operational agreements before initiating deployment.

| Category | Check Question | Priority | Notes / Agreements |
| --- | --- | --- | --- |
| **Environments** | Are the environment tiers (Dev/Staging/Prod) defined? | **Mandatory** | |
| **Deployment Strategy** | Is the strategy (Manual, CI/CD, Blue-Green, Canary) decided? | **Mandatory** | |
| **Release Approval** | Is the approval process for production deploys defined (who & what criteria)? | **Mandatory** | |
| **Config & Secrets** | How will environment variables and secrets be managed (Vault, .env, Secrets Manager)? | **Mandatory** | |

## 2. Observability

| Category | Check Question | Priority | Notes / Agreements |
| --- | --- | --- | --- |
| **Logging Strategy** | Are log formats (struct/JSON) and storage destinations defined? | **Mandatory** | |
| **Monitoring** | Are key metrics (Request rate, Error rate, Latency) and dashboards specified? | **Mandatory** | |
| **Alerts** | Are alerting conditions (thresholds) and channels (Slack/PagerDuty) established? | **Mandatory** | |

## 3. Reliability & Cost

| Category | Check Question | Priority | Notes / Agreements |
| --- | --- | --- | --- |
| **Incident Response** | Are procedures (Escalation, On-call, Post-mortem records) defined? | *Optional* | |
| **Backup Strategy** | Are data backup scheduling, retention periods, and locations established? | **Mandatory** | |
| **Recovery Goals** | Are RTO (Recovery Time Objective) and RPO (Recovery Point Objective) quantified? | *Optional* | |
| **Cost Monitoring** | Is there a policy for infrastructure cost monitoring, alerts, and resource tagging? | *Optional* | |

## 4. Custom Operations Rules

- **WSL2 Resource limits**: Ensure `.wslconfig` in the Windows host user directory limits RAM/CPU to prevent host starvation.
- **Systemd**: `systemd=true` in `/etc/wsl.conf` is optional for the default k3d-only workflow; require it only if you run Linux-managed services directly inside WSL2 (e.g., a direct `k3s` install).
- **IP Variability**: Note that WSL2 IP changes on reboot; use `localhost` port forwarding provided by k3d for stable connectivity.
- **Filesystem performance**: Keep all project files, cluster data, and Docker volumes on the Linux filesystem (`/home/hy/...`) for 10x better performance than `/mnt/c/`.
