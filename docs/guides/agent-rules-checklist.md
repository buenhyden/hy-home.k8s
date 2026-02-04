# Agent Rules & Governance Checklist

This guide maps the **5 Governance Pillars** to the active **Agent Rules**
(`.agent/rules`). It demonstrates how the AI agent is programmed to autonomously
enforce the project's standards.

## 1. Business & Product Checklist

**Role Enforced**: Lead Project Manager

| Checklist Item | Enforcing Rule | Description |
| :--- | :--- | :--- |
| **Requirements Traceability** | [`0200-workflow-standard.md`](../../.agent/rules/0200-Workflows/0200-workflow-standard.md) | Enforces that every code change maps to a refined Issue/Task. |
| **Acceptance Criteria** | [`0200-workflow-standard.md`](../../.agent/rules/0200-Workflows/0200-workflow-standard.md) | Requires GWT (Given-When-Then) format for "Ready" items. |

## 2. Architecture & Tech Stack Checklist

**Role Enforced**: Senior Principal Engineer

| Checklist Item | Enforcing Rule | Description |
| :--- | :--- | :--- |
| **Proactive Reasoning** | [`0000-agentic-pillar-standard.md`](../../.agent/rules/0000-Agents/0000-agentic-pillar-standard.md) | Mandates logical dependency analysis and "Think before Act". |
| **Stack Alignment** | [`0002-strong-reasoner-agent.md`](../../.agent/rules/0000-Agents/0002-strong-reasoner-agent.md) | Enforces alignment with `ARCHITECTURE.md` and Stack rules. |

## 3. Development Process & Collaboration Checklist

**Role Enforced**: DevOps Governance

| Checklist Item | Enforcing Rule | Description |
| :--- | :--- | :--- |
| **Branching Strategy** | [`0200-workflow-standard.md`](../../.agent/rules/0200-Workflows/0200-workflow-standard.md) | Enforces `<type>/<id>-<desc>` naming convention. |
| **Commit Discipline** | [`0200-workflow-standard.md`](../../.agent/rules/0200-Workflows/0200-workflow-standard.md) | Enforces Conventional Commits style. |
| **PR Quality Gate** | [`0200-workflow-standard.md`](../../.agent/rules/0200-Workflows/0200-workflow-standard.md) | Blocks merging if CI checks fail or PR description is empty. |

## 4. Quality, Testing & Security Checklist

**Role Enforced**: QA Automation Engineer / Security Engineer

| Checklist Item | Enforcing Rule | Description |
| :--- | :--- | :--- |
| **Testing Pyramid** | [`0700-testing-and-qa-standard.md`](../../.agent/rules/0700-Testing_and_QA/0700-testing-and-qa-standard.md) | Enforces appropriate mix of Unit/Integration/E2E tests. |
| **Coverage (>80%)** | [`0700-testing-and-qa-standard.md`](../../.agent/rules/0700-Testing_and_QA/0700-testing-and-qa-standard.md) | Mandates 80% coverage and 100% on new logic. |
| **Secure by Default** | [`2200-security-pillar.md`](../../.agent/rules/2200-Security/2200-security-pillar.md) | Enforces OWASP A01-A10 (Auth, Secrets, Injection). |

## 5. Operations, Deployment & Monitoring Checklist

**Role Enforced**: Site Reliability Engineer (SRE)

| Checklist Item | Enforcing Rule | Description |
| :--- | :--- | :--- |
| **Structured Logging** | [`2600-observability-pillar.md`](../../.agent/rules/2600-Observability/2600-observability-pillar.md) | Mandates JSON format for logs with correlation IDs. |
| **RED Metrics** | [`2600-observability-pillar.md`](../../.agent/rules/2600-Observability/2600-observability-pillar.md) | Requires Rate, Errors, Duration metrics for all services. |
