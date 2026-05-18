# Graph Report - .  (2026-05-18)

## Corpus Check

- Large corpus: 310 files · ~119,616 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary

- 1205 nodes · 1528 edges · 82 communities detected
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 101 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)

- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_Docs References|Docs References]]
- [[_COMMUNITY_Docs References|Docs References]]
- [[_COMMUNITY_Docs References|Docs References]]
- [[_COMMUNITY_Operations Policy|Operations Policy]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_Observability|Observability]]
- [[_COMMUNITY_Docs References|Docs References]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_Azure Examples|Azure Examples]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_Progressive Delivery|Progressive Delivery]]
- [[_COMMUNITY_Vault Secrets|Vault Secrets]]
- [[_COMMUNITY_Local Platform|Local Platform]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_Docs References|Docs References]]
- [[_COMMUNITY_Operations Policy|Operations Policy]]
- [[_COMMUNITY_Runbooks|Runbooks]]
- [[_COMMUNITY_Docs References|Docs References]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Docs References|Docs References]]
- [[_COMMUNITY_Docs References|Docs References]]
- [[_COMMUNITY_Headlamp Dashboard|Headlamp Dashboard]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_Docs References|Docs References]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_Operations Policy|Operations Policy]]
- [[_COMMUNITY_Headlamp Dashboard|Headlamp Dashboard]]
- [[_COMMUNITY_Docs References|Docs References]]
- [[_COMMUNITY_AWS Examples|AWS Examples]]
- [[_COMMUNITY_Docs References|Docs References]]
- [[_COMMUNITY_Docs References|Docs References]]
- [[_COMMUNITY_Runbooks|Runbooks]]
- [[_COMMUNITY_Runbooks|Runbooks]]
- [[_COMMUNITY_Docs References|Docs References]]
- [[_COMMUNITY_Progressive Delivery|Progressive Delivery]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_ArgoCD GitOps|ArgoCD GitOps]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Docs References|Docs References]]
- [[_COMMUNITY_Docs References|Docs References]]
- [[_COMMUNITY_Azure Examples|Azure Examples]]
- [[_COMMUNITY_Operations Policy|Operations Policy]]
- [[_COMMUNITY_Docs References|Docs References]]
- [[_COMMUNITY_Vault Secrets|Vault Secrets]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Azure Examples|Azure Examples]]
- [[_COMMUNITY_Docs References|Docs References]]
- [[_COMMUNITY_Progressive Delivery|Progressive Delivery]]
- [[_COMMUNITY_Progressive Delivery|Progressive Delivery]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_AWS Examples|AWS Examples]]
- [[_COMMUNITY_AWS Examples|AWS Examples]]
- [[_COMMUNITY_AWS Examples|AWS Examples]]
- [[_COMMUNITY_Azure Examples|Azure Examples]]
- [[_COMMUNITY_Azure Examples|Azure Examples]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Observability|Observability]]
- [[_COMMUNITY_Headlamp Dashboard|Headlamp Dashboard]]
- [[_COMMUNITY_Community 77|Community 77]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Community 80|Community 80]]
- [[_COMMUNITY_Community 81|Community 81]]

## God Nodes (most connected - your core abstractions)

1. `Canonical Template Stage README` - 21 edges
2. `AppProject platform` - 19 edges
3. `Agent Framework Contract` - 18 edges
4. `Platform Expansion Specification` - 18 edges
5. `Local Harness Catalog` - 15 edges
6. `AWS Migration Product Requirements Document` - 15 edges
7. `AWS Migration Technical Specification` - 13 edges
8. `05.operations Runbooks README` - 13 edges
9. `Template Folder Mapping` - 13 edges
10. `Architecture Decision Records Stage` - 12 edges

## Surprising Connections (you probably didn't know these)

- `External Vault PostgreSQL Valkey Runtime Contracts` --semantically_similar_to--> `External Services Service EndpointSlice Contract`  [INFERRED] [semantically similar]
  README.md → docs/02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md
- `Reference Only Examples Area` --semantically_similar_to--> `Optional Graphify Knowledge Graph Refresh`  [INFERRED] [semantically similar]
  examples/README.md → scripts/README.md
- `docs Project Documentation Hub` --references--> `Agent Governance Hub`  [EXTRACTED]
  /home/hy/project-infra/hy-home.k8s/docs/README.md → docs/90.references/learning/README.md
- `Repository Execution Constraints` --rationale_for--> `GitOps First Mutation Boundary`  [INFERRED]
  AGENTS.md → docs/00.agent-governance/rules/agentic.md
- `GitOps Platform Scope` --conceptually_related_to--> `GitOps First Mutation Boundary`  [INFERRED]
  README.md → docs/00.agent-governance/rules/agentic.md

## Hyperedges (group relationships)

- **Platform GitOps Foundation** — concept_k3d_multinode_topology, readme_app_of_apps_gitops, concept_external_services_endpointslice, concept_vault_eso_secret_sync [EXTRACTED 1.00]
- **Platform Expansion Stack** — concept_cert_manager_mkcert_tls, concept_headlamp_cluster_ui, concept_istio_service_mesh, concept_kiali_external_observability [EXTRACTED 1.00]
- **Progressive Delivery Notifications** — concept_argo_rollouts_progressive_delivery, concept_argo_notifications_slack, concept_vault_eso_secret_sync [EXTRACTED 1.00]
- **WSL k3d ArgoCD Platform Traceability Chain** — 0001_wsl_k3d_argocd_platform_ard, 001_wsl_k3d_argocd_platform_spec, 2026_03_27_wsl_k3d_argocd_platform_plan [EXTRACTED 1.00]
- **Argo Rollouts Backfill Chain** — 0004_argo_rollouts_progressive_delivery_ard, 004_argo_rollouts_progressive_delivery_spec, 2026_05_18_argo_rollouts_progressive_delivery_plan [EXTRACTED 1.00]
- **Argo Notifications Slack Backfill Chain** — 0005_argo_notifications_slack_ard, 005_argo_notifications_slack_spec, 2026_05_18_argo_notifications_slack_plan [EXTRACTED 1.00]
- **Execution Stage Plan Task Evidence Contract** — plans_readme_plan_stage, tasks_readme_task_stage, plans_readme_task_evidence, tasks_readme_execution_evidence [EXTRACTED 1.00]
- **ArgoCD and Kubernetes Observability Stack** — guide_argocd_prometheus_grafana, guide_k8s_observability_bootstrap, guide_argocd_metrics_nodeport, guide_k8s_observability_nodeports, argo_rollouts_progressive_delivery [INFERRED 0.85]
- **GitOps Onboarding Progressive Delivery Pattern** — guide_new_app_gitops_onboarding, guide_github_app_gitops_onboarding, guide_new_app_applicationset, guide_github_app_rollout_pattern, argo_rollouts_progressive_delivery [INFERRED 0.85]
- **GitOps Secret Contracts** — 0001_k8s_gitops_operations_policy_vault_secret_source, 0002_wsl2_k3d_gitops_ha_operations_policy_vault_endpoint_contract, 0007_app_gitops_onboarding_policy_app_vault_external_secret, 0002_argocd_eso_vault_recovery_runbook_vault_endpoint_hotfix [EXTRACTED 1.00]
- **Observability Operations Stack** — 0003_service_mesh_cert_manager_policy_kiali_external_observability, 0005_observability_platform_operations_policy_argocd_metrics_nodeports, 0006_k8s_observability_operations_policy_alloy_k8s_logs, 0009_k8s_observability_runbook_k8s_observability_recovery [EXTRACTED 1.00]
- **App Onboarding Rollout Flow** — 0007_app_gitops_onboarding_policy_rollout_required, 0007_app_gitops_onboarding_policy_apps_generator_workload_layout, 0006_new_app_onboarding_runbook_apps_generator_onboarding, 0010_github_app_gitops_onboarding_runbook_github_app_rollout_onboarding [EXTRACTED 1.00]
- **Reference Boundary Documents** — readme_learning_references, readme_llm_wiki_index, readme_versions_references, reference_template_reference [EXTRACTED 1.00]
- **Template Governance Set** — readme_templates, readme_template_folder_mapping, readme_contract_template_placement, readme_template_readme [EXTRACTED 1.00]
- **Agent Documentation Templates** — agent_design_template_agent_design, operation_template_operations_policy, incident_template_incident, postmortem_template_postmortem [INFERRED 0.85]
- **Feature Document Template Set** — spec_spec_template, task_task_template, tests_tests_template [EXTRACTED 1.00]
- **GitOps App Onboarding Path** — examples_sample_app, sample_app_gitops_onboarding, gitops_workloads, gitops_argocd_app_of_apps [EXTRACTED 1.00]
- **Repository Static Validation Suite** — scripts_quality_gates, scripts_gitops_structure_validator, scripts_k8s_manifest_validator, scripts_secret_handling_checker, scripts_llm_wiki_index_generator [EXTRACTED 1.00]

## Communities

### Community 0 - "ArgoCD GitOps"

Cohesion: 0.03
Nodes (87): Application Load Balancer, Application Pods, AWS WAF, Data Boundaries, GitOps with ArgoCD, IAM Pod Identity, Kubernetes Secret, Multi-AZ Reliability (+79 more)

### Community 1 - "ArgoCD GitOps"

Cohesion: 0.04
Nodes (84): ArgoCD Platform Bootstrap Runbook, WSL2 k3d GitOps Platform Bootstrap Procedure, K8s GitOps Platform Operations Policy, External Service Port Contract, External Service Port Contracts, GitOps Platform Operations, Vault as Secret Source of Truth, Human Approved Break Glass Boundary (+76 more)

### Community 2 - "ArgoCD GitOps"

Cohesion: 0.05
Nodes (70): ADR-0001: k3d Topology and External Network Baseline, External Network Baseline, k3d 1 Server 3 Agents Topology, ADR-0001 k3d Topology and External Network Baseline, ADR-0002 ArgoCD Helm Install with App-of-Apps and ApplicationSet, ADR-0002: ArgoCD Helm Install with App-of-Apps and ApplicationSet, App-of-Apps and ApplicationSet Model, ArgoCD Helm Installation Model (+62 more)

### Community 3 - "ArgoCD GitOps"

Cohesion: 0.04
Nodes (62): Bicep Provisioning Checks, AKS Provisioning Security Expectations, AKS Cluster Provisioning Task, Application Gateway for Containers and Gateway API, AKS Cluster, ArgoCD GitOps Pull Model, Azure Cache for Redis, Azure Key Vault (+54 more)

### Community 4 - "ArgoCD GitOps"

Cohesion: 0.04
Nodes (53): ArgoCD root-platform Application, infrastructure/bootstrap-local.sh, WSL k3d ArgoCD Bootstrap Guide, External Secrets Operator Sync, External Services Contract, Vault Secret Contract, CI Static Validation, WSL2 k3d/k3s ArgoCD HA Setup Guide (+45 more)

### Community 5 - "ArgoCD GitOps"

Cohesion: 0.07
Nodes (51): ArgoCD App-of-Apps, ESO Vault Secret Plane, External PostgreSQL and Valkey Services, GitOps Platform, GitOps, Secret, and External Data Planes, WSL k3d/k3s ArgoCD Platform ARD, cert-manager TLS Plane, Istio Mesh Plane (+43 more)

### Community 6 - "Docs References"

Cohesion: 0.08
Nodes (45): Architecture Decision Record Template, Agent Design Template, Agent Governance Hub, Agent Reference Area README, Feature Agent Design Location, Agent Runtime Truth Locations, API Specification Template, Architecture Reference Document Template (+37 more)

### Community 7 - "Docs References"

Cohesion: 0.05
Nodes (45): platform cluster resource whitelist, platform destination allowlist, platform namespace resource whitelist, AppProject platform, platform-readonly role, platform source repository allowlist, ClusterIssuer mkcert-ca-issuer, mkcert-root-ca secret reference (+37 more)

### Community 8 - "Docs References"

Cohesion: 0.07
Nodes (42): AnalysisTemplate adminer-stability, AnalysisTemplate <appname>-stability, container-restarts metric, kube_pod_container_status_restarts_total, kube-state-metrics restart metric, Prometheus external platform service, Namespace apps, PostgreSQL external services (+34 more)

### Community 9 - "Operations Policy"

Cohesion: 0.11
Nodes (41): Agentic Execution Rules, GitOps First Mutation Boundary, Agent Framework Contract, AGENTS.md Provider Notes, Repository Execution Constraints, Agent Bootstrap Governance, Bootstrap JIT Loading Sequence, Claude Provider Notes (+33 more)

### Community 10 - "ArgoCD GitOps"

Cohesion: 0.08
Nodes (36): AWS EKS 1.35 Reference Example, Azure AKS 1.35 Reference Example, Examples README, Ingress NGINX Retirement Statement, Reference Only Examples Area, Sample App Onboarding Example, Tech Stack Version Inventory, Adminer Reference Workload (+28 more)

### Community 11 - "ArgoCD GitOps"

Cohesion: 0.07
Nodes (33): argocd host rule, ArgoCD Helm values, GitOps and ArgoCD reconciliation, infrastructure directory, local k3d Kubernetes platform, MetalLB bootstrap manifests, IPAddressPool, 172.18.0.240-172.18.0.250 (+25 more)

### Community 12 - "ArgoCD GitOps"

Cohesion: 0.06
Nodes (33): ArgoCD GitOps, k3d and Docker, Efficient Memory Management for LLM Serving with PagedAttention, Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, Reconciliation Loop, Infrastructure to Theory Learning Roadmap, Attention Is All You Need, Vector Indexing (+25 more)

### Community 13 - "ArgoCD GitOps"

Cohesion: 0.07
Nodes (29): Endpoints vault-external, Application platform-argocd-config, Application platform-cert-manager, Application platform-cert-manager-config, Helm chart cert-manager v1.17.2, AWS Migration Reference, Azure Migration Reference, Cloud Example Snapshot (+21 more)

### Community 14 - "ArgoCD GitOps"

Cohesion: 0.08
Nodes (26): argocd-k3d Traefik router, argocd-k3d Traefik service, argocd-k3d transport, k3d-hyhome-serverlb:443, websecure entryPoint, Headlamp service headlamp:4466, headlamp host rule, headlamp-k3d Traefik router (+18 more)

### Community 15 - "Observability"

Cohesion: 0.08
Nodes (25): EndpointSlice alloy-external-1, Service alloy-external, Alloy discovery.kubernetes pods, Alloy discovery.relabel pod_logs, Alloy loki.process events_label, Alloy loki.source.kubernetes_events events, Alloy loki.source.kubernetes pods, Alloy loki.write external_loki (+17 more)

### Community 16 - "Docs References"

Cohesion: 0.09
Nodes (24): Service postgres-external, Service redis-external, Application Gateway for Containers (AGC), Azure Cache for Redis, Azure CNI Overlay, Azure DB for PostgreSQL Flexible Server, Azure Infrastructure with Bicep, Azure infrastructure parameters (+16 more)

### Community 17 - "ArgoCD GitOps"

Cohesion: 0.14
Nodes (23): NetworkPolicy allow-egress-apps, In-cluster pod-to-pod traffic, Istiod control plane, kube-dns, NetworkPolicy allow-argocd-egress-to-external-valkey, Namespace argocd, External HTTPS endpoints, External Valkey (+15 more)

### Community 18 - "ArgoCD GitOps"

Cohesion: 0.14
Nodes (20): Access and TLS Contract, CI Control Plane, CI Static Gate, WSL2 k3d/k3s ArgoCD HA Platform ARD, External Endpoint Contract, ArgoCD Pull Reconciliation Model, AppProject and Vault Minimum Privilege Controls, Static Contract CI Gates (+12 more)

### Community 19 - "Azure Examples"

Cohesion: 0.12
Nodes (19): Azure CNI Overlay, ADR-0001 Azure CNI Overlay for AKS Networking, Azure Application Gateway for Containers, ADR-0002 AGC with Gateway API, Kubernetes Gateway API Standard, Azure Workload Identity, ADR-0003 Azure Workload Identity for Passwordless Auth, DefaultAzureCredential (+11 more)

### Community 20 - "ArgoCD GitOps"

Cohesion: 0.11
Nodes (19): TrafficController hyhome-agc, Service hyhome-app-service, Gateway hyhome-gateway, HTTPRoute hyhome-route, GatewayClass azure-alb-external, Service hy-home-app-svc, Certificate reference hy-home-cert, Gateway hy-home-gateway (+11 more)

### Community 21 - "Progressive Delivery"

Cohesion: 0.13
Nodes (19): ClusterRole alloy-k8s-logs, ClusterRoleBinding alloy-k8s-logs, ConfigMap alloy-k8s-logs-config, Deployment alloy-k8s-logs, In-cluster Kubernetes log collection, ServiceAccount alloy-k8s-logs, ClusterRole kube-state-metrics, ClusterRoleBinding kube-state-metrics (+11 more)

### Community 22 - "Vault Secrets"

Cohesion: 0.14
Nodes (18): check-secret-handling.sh, generate-llm-wiki-index.sh, optional kube-linter, live cluster mutation exclusion, manifest-static CI job, Python PyYAML dependency, repo-backed static validation utilities, repo-quality-static CI job (+10 more)

### Community 23 - "Local Platform"

Cohesion: 0.14
Nodes (18): Agent-first Execution Boundary, k3d Workspace and Agent-first Remediation Plan, Harness Readiness Matrix, Repository Quality Gate, k3d Workspace and Agent-first Remediation Task, scripts Inventory Remediation Plan, Repo-root Argument Contract, scripts Directory Inventory (+10 more)

### Community 24 - "ArgoCD GitOps"

Cohesion: 0.15
Nodes (15): Argo Rollouts Progressive Delivery ARD, platform-rollouts ArgoCD Application, Argo Notifications Slack ARD, ArgoCD Notifications Controller, Argo Rollouts Progressive Delivery Specification, Rollout and Analysis CRDs, Rollouts Dashboard Route, Rollouts Controller Metrics (+7 more)

### Community 25 - "Docs References"

Cohesion: 0.17
Nodes (15): Agent Role and IO Contract, API Spec, Guardrails, Parent Design Document, Technical Specification Template, Specification Verification Plan, Agent Specific Task Types, Task Evidence Requirement (+7 more)

### Community 26 - "Operations Policy"

Cohesion: 0.15
Nodes (13): AWS Disaster Recovery Runbook, AWS IaC and Backup-based Disaster Recovery, AWS Infrastructure Operations Policy, AWS IaC Governance, AWS Network Access Controls, AWS Resource Tagging Standard, AWS AI Agent Safety Policy, AWS Migration Operations Policy (+5 more)

### Community 27 - "Runbooks"

Cohesion: 0.18
Nodes (13): Headlamp Authentication and OIDC Guide, Keycloak Groups to Kubernetes RBAC Mapping, 05.operations Guides Stage, 05.operations Incidents Stage, No Tracked Incidents State, GitOps-first Agent Execution Boundary, k3d Workspace and Agent-first Remediation, Risky Command Boundary Gate (+5 more)

### Community 28 - "Docs References"

Cohesion: 0.17
Nodes (12): Documentation Scope, Meta Scope, Stage Checklists, Execution Checklist Stage Taxonomy, AI Agent Standards, Documentation Boundary Policy, Just-in-Time Governance Loading Policy, Agent Language Policy (+4 more)

### Community 29 - "ArgoCD GitOps"

Cohesion: 0.17
Nodes (12): Service argocd-application-controller-metrics-np, Service argocd-applicationset-controller-metrics-np, ArgoCD Metrics NodePort Services, Service argocd-notifications-controller-metrics-np, Docker Prometheus 172.18.0.10, Service argocd-repo-server-metrics-np, Service argocd-server-metrics-np, ConfigMap argocd-notifications-cm (+4 more)

### Community 30 - "ArgoCD GitOps"

Cohesion: 0.17
Nodes (12): Notifications Slack Secret Boundary, Argo Notifications Slack Backfill, Argo Rollouts Progressive Delivery Contract, Argo Rollouts Progressive Delivery Backfill, ArgoCD Metrics NodePort Exposure, ArgoCD Prometheus Metrics and Grafana Guide, GitHub App GitOps Onboarding Guide, Rollout AnalysisTemplate Istio mTLS TLS Pattern (+4 more)

### Community 31 - "Community 31"

Cohesion: 0.22
Nodes (10): Canonical Owner Rule, LLM Wiki Curation Guide, Generated Markdown Link Map, wiki-curator Agent, Agent-first Harness, LLM Wiki, and Hook Contract Closure Plan, Hook Feedback Loop, Legacy Docs Path Migration Map, Repo-local LLM Wiki (+2 more)

### Community 32 - "Docs References"

Cohesion: 0.2
Nodes (10): Agent Eval Tasks, Execution-tracking Source of Truth, Task Template, TDD Default, Traceability-first Tasks, Agent Evals, Evidence and Reporting, TDD Scope (+2 more)

### Community 33 - "Docs References"

Cohesion: 0.31
Nodes (9): ConfigMap Watcher Controller, Efficient Memory Management for LLM Serving with PagedAttention, Infrastructure to Theory Learning Roadmap, Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, Reconciliation Loop, Attention Is All You Need, Vector Indexing, Virtual Memory Paging (+1 more)

### Community 34 - "Headlamp Dashboard"

Cohesion: 0.22
Nodes (9): Ingress headlamp, Headlamp kustomization, ClusterIssuer mkcert-ca-issuer, Service headlamp, TLS Secret headlamp-tls, Ingress kiali, Kiali kustomization, Service kiali (+1 more)

### Community 35 - "ArgoCD GitOps"

Cohesion: 0.25
Nodes (9): Branch Policy Gate, Repo Quality Gate CI Contract Checks, .github QA and CI Remediation, CI Static Validation, Local Runtime Validation, WSL2 k3d ArgoCD HA Setup Guide, WSL2 k3d/k3s ArgoCD HA Platform Execution, Static Contract Verification (+1 more)

### Community 36 - "Docs References"

Cohesion: 0.25
Nodes (8): Agent Role and IO Contract, API Contract, Specification Contracts, Evaluation, Guardrails, PRD and ARD References, Technical Specification Template, Verification

### Community 37 - "ArgoCD GitOps"

Cohesion: 0.25
Nodes (8): Argo Rollouts UI local exposure, ArgoCD UI local exposure, Traefik dynamic config examples, canonical GitOps and ArgoCD deployment path, Headlamp UI local exposure, hy-home.docker Traefik gateway, Kiali UI local exposure, traefik directory

### Community 38 - "Operations Policy"

Cohesion: 0.29
Nodes (7): Azure Monitor and Log Analytics, Observability Evidence Sources, PostgreSQL Backup Retention, Azure Maintenance and Operations Policy, Azure Monitor Alerting Policy, AKS Node Autoupgrade Policy, Operational Policies Directory

### Community 39 - "Headlamp Dashboard"

Cohesion: 0.33
Nodes (7): Platform Expansion Bootstrap Guide, cert-manager Headlamp Istio Kiali Bootstrap Components, cert-manager Platform Component, Headlamp and 172.18.x Current Contract, Headlamp Platform UI, Istio and Kiali Platform Components, Platform Expansion Execution

### Community 40 - "Docs References"

Cohesion: 0.33
Nodes (6): AI Agent Guidance, Base Structure, Documentation Standards, README Template, Snippet Library, Traceability Rules

### Community 41 - "AWS Examples"

Cohesion: 0.47
Nodes (6): ALB-backed Kubernetes Ingress, AWS External Services Integration, PostgreSQL ExternalName Service for AWS RDS/Aurora, Valkey ExternalName Service for AWS ElastiCache, Karpenter Configuration, AWS Managed Services Migration Stack

### Community 42 - "Docs References"

Cohesion: 0.33
Nodes (6): ApplicationSet apps-generator, apps project application template, gitops/workloads/* directory generator, AppProject apps, apps-readonly role, apps workload resource whitelist

### Community 43 - "Docs References"

Cohesion: 0.47
Nodes (6): k3d Workspace and Agent-first Remediation Plan, Template Cross-link Fix Plan, Architecture Requirements ARD Stage, Document Stage Traceability, Execution Stage, Specs Stage

### Community 44 - "Runbooks"

Cohesion: 0.8
Nodes (5): AWS Execution Tasks, AWS Migration Documentation Hub, AWS Operational Guides, AWS Operations Policies, AWS Incident Response Runbooks

### Community 45 - "Runbooks"

Cohesion: 0.4
Nodes (5): AKS node pool replacement and scaling runbook, Azure Portal AKS Insights dashboard, AKS cluster autoscaler, Manual AKS node pool scaling, AKS node pool rolling update

### Community 46 - "Docs References"

Cohesion: 0.4
Nodes (5): template.app-health-degraded, template.app-sync-failed, defaultTriggers, trigger.on-health-degraded, trigger.on-sync-failed

### Community 47 - "Progressive Delivery"

Cohesion: 0.4
Nodes (5): Namespace apps, Istio injection enabled, Namespace argo-rollouts, Namespace cert-manager, Namespaces kustomization

### Community 48 - "ArgoCD GitOps"

Cohesion: 0.4
Nodes (5): bootstrap-local.sh, bootstrap-only kubectl apply exception, external Vault PostgreSQL Valkey services, valkey_password, Vault KV secret/platform/argocd

### Community 49 - "ArgoCD GitOps"

Cohesion: 0.4
Nodes (5): WSL k3d ArgoCD Bootstrap Guide, Vault Valkey PostgreSQL External Services Contract, WSL k3d/k3s ArgoCD Platform Execution, ArgoCD Platform Bootstrap Runbook, 001 WSL k3d ArgoCD Platform Spec

### Community 50 - "Community 50"

Cohesion: 0.5
Nodes (5): LLM Wiki Curation Guide, Deterministic Markdown Link Map, LLM Wiki Generated Index Contract, scripts Inventory Remediation, Tier A/B/C Script Retention Standard

### Community 51 - "Docs References"

Cohesion: 0.4
Nodes (5): Agent Operations Recovery, Immediate Execution Procedure, Operations Runbook, Runbook Template, Runbook Verification Steps

### Community 52 - "Docs References"

Cohesion: 0.5
Nodes (4): Agent Operations, Immediate Execution, Runbook Template, Safe Rollback or Recovery Procedure

### Community 53 - "Azure Examples"

Cohesion: 0.5
Nodes (4): ADR-0004 PostgreSQL Flexible Server HA, Azure Database for PostgreSQL Flexible Server, Zone-redundant PostgreSQL HA, Azure Managed Data Services Requirement

### Community 54 - "Operations Policy"

Cohesion: 0.5
Nodes (4): Azure Cost Optimization and Governance Policy, AKS Node Pool Right-sizing, Spot Instance Use for Non-production User Pools, Azure Cost Tagging Policy

### Community 55 - "Docs References"

Cohesion: 0.67
Nodes (3): Authority Boundary, Reference Template, Review and Freshness

### Community 56 - "Vault Secrets"

Cohesion: 0.67
Nodes (3): ESO kustomization, postgres-app-secret.yaml, vault-secret-store.yaml

### Community 57 - "Community 57"

Cohesion: 1.0
Nodes (2): S3 Backup Storage, S3 Intelligent-Tiering

### Community 58 - "Community 58"

Cohesion: 1.0
Nodes (2): Karpenter Default EC2NodeClass, Karpenter Default NodePool

### Community 59 - "Azure Examples"

Cohesion: 1.0
Nodes (2): AzureIdentity hy-home-app-identity, AzureIdentityBinding hy-home-app-identity-binding

### Community 60 - "Docs References"

Cohesion: 1.0
Nodes (2): template.app-deployed, trigger.on-deployed

### Community 61 - "Progressive Delivery"

Cohesion: 1.0
Nodes (2): trigger.on-rollout-completed, template.rollout-completed

### Community 62 - "Progressive Delivery"

Cohesion: 1.0
Nodes (2): trigger.on-rollout-aborted, template.rollout-aborted

### Community 63 - "Community 63"

Cohesion: 1.0
Nodes (2): cloud-native ingress paths, Ingress NGINX upstream retired statement

### Community 64 - "Community 64"

Cohesion: 1.0
Nodes (1): Gateway JIT Bootstrap Order

### Community 65 - "Community 65"

Cohesion: 1.0
Nodes (1): Gateway Routing Map

### Community 66 - "Community 66"

Cohesion: 1.0
Nodes (1): .github QA and CI Remediation Task

### Community 67 - "AWS Examples"

Cohesion: 1.0
Nodes (1): AWS EBS CSI Driver

### Community 68 - "AWS Examples"

Cohesion: 1.0
Nodes (1): AWS Distro for OpenTelemetry Observability

### Community 69 - "AWS Examples"

Cohesion: 1.0
Nodes (1): AWS Infrastructure Migration Implementation

### Community 70 - "Azure Examples"

Cohesion: 1.0
Nodes (1): Azure AKS Deployment and Onboarding Guide

### Community 71 - "Azure Examples"

Cohesion: 1.0
Nodes (1): Azure CNI Overlay

### Community 72 - "Community 72"

Cohesion: 1.0
Nodes (1): Operations KPIs

### Community 73 - "Community 73"

Cohesion: 1.0
Nodes (1): Post-mortem Requirements

### Community 74 - "Community 74"

Cohesion: 1.0
Nodes (1): ingress-nginx Istio sidecar mTLS chain

### Community 75 - "Observability"

Cohesion: 1.0
Nodes (1): Prometheus external dependency

### Community 76 - "Headlamp Dashboard"

Cohesion: 1.0
Nodes (1): Namespace headlamp

### Community 77 - "Community 77"

Cohesion: 1.0
Nodes (1): static contract validation

### Community 78 - "Community 78"

Cohesion: 1.0
Nodes (1): live cluster validation

### Community 79 - "Community 79"

Cohesion: 1.0
Nodes (1): optional graphify tool

### Community 80 - "Community 80"

Cohesion: 1.0
Nodes (1): Agent Progress and Memory Ledger

### Community 81 - "Community 81"

Cohesion: 1.0
Nodes (1): MetalLB and Traefik

## Knowledge Gaps

- **500 isolated node(s):** `Gateway JIT Bootstrap Order`, `Repository Execution Constraints`, `Gateway Routing Map`, `Spec Driven Docs Taxonomy`, `Local Skill Roster` (+495 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 57`** (2 nodes): `S3 Backup Storage`, `S3 Intelligent-Tiering`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 58`** (2 nodes): `Karpenter Default EC2NodeClass`, `Karpenter Default NodePool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Azure Examples`** (2 nodes): `AzureIdentity hy-home-app-identity`, `AzureIdentityBinding hy-home-app-identity-binding`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Docs References`** (2 nodes): `template.app-deployed`, `trigger.on-deployed`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Progressive Delivery`** (2 nodes): `trigger.on-rollout-completed`, `template.rollout-completed`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Progressive Delivery`** (2 nodes): `trigger.on-rollout-aborted`, `template.rollout-aborted`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 63`** (2 nodes): `cloud-native ingress paths`, `Ingress NGINX upstream retired statement`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 64`** (1 nodes): `Gateway JIT Bootstrap Order`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 65`** (1 nodes): `Gateway Routing Map`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 66`** (1 nodes): `.github QA and CI Remediation Task`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `AWS Examples`** (1 nodes): `AWS EBS CSI Driver`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `AWS Examples`** (1 nodes): `AWS Distro for OpenTelemetry Observability`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `AWS Examples`** (1 nodes): `AWS Infrastructure Migration Implementation`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Azure Examples`** (1 nodes): `Azure AKS Deployment and Onboarding Guide`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Azure Examples`** (1 nodes): `Azure CNI Overlay`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 72`** (1 nodes): `Operations KPIs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 73`** (1 nodes): `Post-mortem Requirements`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 74`** (1 nodes): `ingress-nginx Istio sidecar mTLS chain`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Observability`** (1 nodes): `Prometheus external dependency`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Headlamp Dashboard`** (1 nodes): `Namespace headlamp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 77`** (1 nodes): `static contract validation`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 78`** (1 nodes): `live cluster validation`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 79`** (1 nodes): `optional graphify tool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 80`** (1 nodes): `Agent Progress and Memory Ledger`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 81`** (1 nodes): `MetalLB and Traefik`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions

_Questions this graph is uniquely positioned to answer:_

- **Why does `GitOps Desired State` connect `ArgoCD GitOps` to `ArgoCD GitOps`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Why does `GitOps with ArgoCD` connect `ArgoCD GitOps` to `ArgoCD GitOps`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **What connects `Gateway JIT Bootstrap Order`, `Repository Execution Constraints`, `Gateway Routing Map` to the rest of the system?**
  _500 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ArgoCD GitOps` be split into smaller, more focused modules?**
  _Cohesion score 0.03 - nodes in this community are weakly interconnected._
- **Should `ArgoCD GitOps` be split into smaller, more focused modules?**
  _Cohesion score 0.04 - nodes in this community are weakly interconnected._
- **Should `ArgoCD GitOps` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._
- **Should `ArgoCD GitOps` be split into smaller, more focused modules?**
  _Cohesion score 0.04 - nodes in this community are weakly interconnected._
