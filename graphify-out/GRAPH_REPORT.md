# Graph Report - .  (2026-05-22)

## Corpus Check
- Large corpus: 234 files · ~104,607 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 1194 nodes · 1603 edges · 66 communities detected
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 105 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Platform Bootstrap Operations|Platform Bootstrap Operations]]
- [[_COMMUNITY_App Onboarding GitOps|App Onboarding GitOps]]
- [[_COMMUNITY_Architecture Decisions|Architecture Decisions]]
- [[_COMMUNITY_Platform Requirements|Platform Requirements]]
- [[_COMMUNITY_Core ADR Baseline|Core ADR Baseline]]
- [[_COMMUNITY_Traefik Access Routes|Traefik Access Routes]]
- [[_COMMUNITY_Document Templates|Document Templates]]
- [[_COMMUNITY_Bootstrap Guides|Bootstrap Guides]]
- [[_COMMUNITY_Governance Templates|Governance Templates]]
- [[_COMMUNITY_GitOps Architecture Planes|GitOps Architecture Planes]]
- [[_COMMUNITY_Adminer Workload Policy|Adminer Workload Policy]]
- [[_COMMUNITY_Platform AppProject TLS|Platform AppProject TLS]]
- [[_COMMUNITY_Agent Governance Rules|Agent Governance Rules]]
- [[_COMMUNITY_Learning References|Learning References]]
- [[_COMMUNITY_Rollouts Notifications|Rollouts Notifications]]
- [[_COMMUNITY_HA Platform Controls|HA Platform Controls]]
- [[_COMMUNITY_Alloy Logging Pipeline|Alloy Logging Pipeline]]
- [[_COMMUNITY_GitOps Desired State|GitOps Desired State]]
- [[_COMMUNITY_Monitoring Manifests|Monitoring Manifests]]
- [[_COMMUNITY_Static Validation Scripts|Static Validation Scripts]]
- [[_COMMUNITY_Agent First Remediation|Agent First Remediation]]
- [[_COMMUNITY_README Template Standards|README Template Standards]]
- [[_COMMUNITY_Spec Task Templates|Spec Task Templates]]
- [[_COMMUNITY_Headlamp OIDC Operations|Headlamp OIDC Operations]]
- [[_COMMUNITY_Governance Scope Policy|Governance Scope Policy]]
- [[_COMMUNITY_ArgoCD Metrics Notifications|ArgoCD Metrics Notifications]]
- [[_COMMUNITY_Notifications Rollouts Guides|Notifications Rollouts Guides]]
- [[_COMMUNITY_WSL2 HA Hardening|WSL2 HA Hardening]]
- [[_COMMUNITY_LLM Wiki Governance|LLM Wiki Governance]]
- [[_COMMUNITY_Operations Stage READMEs|Operations Stage READMEs]]
- [[_COMMUNITY_Theory Learning Concepts|Theory Learning Concepts]]
- [[_COMMUNITY_Headlamp Kiali Ingress|Headlamp Kiali Ingress]]
- [[_COMMUNITY_CI QA Remediation|CI QA Remediation]]
- [[_COMMUNITY_Traefik Local Exposure|Traefik Local Exposure]]
- [[_COMMUNITY_Platform Expansion Guide|Platform Expansion Guide]]
- [[_COMMUNITY_Root Platform Apps|Root Platform Apps]]
- [[_COMMUNITY_Workload ApplicationSet|Workload ApplicationSet]]
- [[_COMMUNITY_Operations Routing|Operations Routing]]
- [[_COMMUNITY_ArgoCD Health Alerts|ArgoCD Health Alerts]]
- [[_COMMUNITY_Namespace Baselines|Namespace Baselines]]
- [[_COMMUNITY_Bootstrap Secret Contracts|Bootstrap Secret Contracts]]
- [[_COMMUNITY_WSL Bootstrap Spec|WSL Bootstrap Spec]]
- [[_COMMUNITY_Wiki Script Remediation|Wiki Script Remediation]]
- [[_COMMUNITY_Runbook Template|Runbook Template]]
- [[_COMMUNITY_README Assembly|README Assembly]]
- [[_COMMUNITY_ESO Secret Store|ESO Secret Store]]
- [[_COMMUNITY_App Deployed Notification|App Deployed Notification]]
- [[_COMMUNITY_Rollout Completed Notification|Rollout Completed Notification]]
- [[_COMMUNITY_Rollout Aborted Notification|Rollout Aborted Notification]]
- [[_COMMUNITY_Ingress Retirement|Ingress Retirement]]
- [[_COMMUNITY_Verification Plan|Verification Plan]]
- [[_COMMUNITY_Gateway Bootstrap|Gateway Bootstrap]]
- [[_COMMUNITY_Gateway Routing|Gateway Routing]]
- [[_COMMUNITY_CI Remediation Task|CI Remediation Task]]
- [[_COMMUNITY_Platform Components|Platform Components]]
- [[_COMMUNITY_External Service Contracts|External Service Contracts]]
- [[_COMMUNITY_Network Egress Policies|Network Egress Policies]]
- [[_COMMUNITY_Adminer Workload|Adminer Workload]]
- [[_COMMUNITY_Validation Scripts|Validation Scripts]]
- [[_COMMUNITY_ESO Vault Contract|ESO Vault Contract]]
- [[_COMMUNITY_Headlamp Namespace|Headlamp Namespace]]
- [[_COMMUNITY_Static Contract Validation|Static Contract Validation]]
- [[_COMMUNITY_Live Cluster Validation|Live Cluster Validation]]
- [[_COMMUNITY_Graphify Tooling|Graphify Tooling]]
- [[_COMMUNITY_Progress Memory|Progress Memory]]
- [[_COMMUNITY_MetalLB Traefik|MetalLB Traefik]]

## God Nodes (most connected - your core abstractions)
1. `Canonical Template Stage README` - 21 edges
2. `AppProject platform` - 19 edges
3. `Agent Framework Contract` - 18 edges
4. `Platform Expansion Specification` - 18 edges
5. `Technical Specification` - 17 edges
6. `App GitOps Onboarding Policy` - 16 edges
7. `Local Harness Catalog` - 15 edges
8. `Requirements Stage` - 13 edges
9. `Product Requirements Document` - 13 edges
10. `05.operations Runbooks README` - 13 edges

## Surprising Connections (you probably didn't know these)
- `External Vault PostgreSQL Valkey Runtime Contracts` --semantically_similar_to--> `External Services Service EndpointSlice Contract`  [INFERRED] [semantically similar]
  README.md → docs/02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md
- `Agent Eval Tasks` --conceptually_related_to--> `Agent Evals`  [INFERRED]
  /home/hy/project-infra/hy-home.k8s/docs/99.templates/task.template.md → docs/99.templates/tests.template.md
- `LLM Wiki Reference Index` --conceptually_related_to--> `Graphify Outputs`  [INFERRED]
  docs/README.md → README.md
- `External Runtime Boundary` --conceptually_related_to--> `External Endpoint Contract`  [INFERRED]
  README.md → docs/02.architecture/decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md
- `Repository Execution Constraints` --rationale_for--> `GitOps First Mutation Boundary`  [INFERRED]
  AGENTS.md → docs/00.agent-governance/rules/agentic.md

## Hyperedges (group relationships)
- **Documentation Stage Flow** — readme_docs_canonical_taxonomy, readme_documentation_flow, stage_authoring_matrix_stage_authoring_matrix, document_stage_routing_canonical_stage_taxonomy [EXTRACTED 1.00]
- **Local Agent Runtime Contract** — readme_agent_governance_hub, harness_catalog_local_harness_catalog, harness_catalog_agent_roster, harness_catalog_codex_mirrors, harness_catalog_local_skills [EXTRACTED 1.00]
- **External Service Contract Pattern** — 2026_03_27_wsl_k3d_argocd_platform_external_services_integration, 2026_03_28_wsl2_k3d_argocd_ha_platform_ha_platform_prd, 0004_external_services_endpoints_and_valkey_backend_service_endpoint_slice_pattern, 0005_wsl2_ha_baseline_and_external_endpoint_contract_external_endpoint_contract [INFERRED 0.95]
- **Baseline GitOps Platform Planes** — 0001_wsl_k3d_argocd_platform_gitops_control_plane, 0001_wsl_k3d_argocd_platform_secret_plane, 0001_wsl_k3d_argocd_platform_external_data_services, 0002_wsl2_k3d_argocd_ha_platform_ci_static_gates [EXTRACTED 1.00]
- **Platform Expansion Runtime Pattern** — 0006_cert_manager_mkcert_ca_issuer_tls_automation, 0010_headlamp_replaces_dashboard_headlamp, 0008_istio_install_and_ingress_coexist_istio_default_profile, 0009_kiali_external_observability_kiali, spec_current_172_18_external_endpoint_contract [EXTRACTED 1.00]
- **Progressive Delivery Notification Pattern** — 0011_argo_rollouts_progressive_delivery_argo_rollouts, 0012_argo_notifications_slack_argo_notifications, 0012_argo_notifications_slack_vault_eso_notification_secret, spec_notifications_config_secret_contract [EXTRACTED 1.00]
- **Execution Stage Plan Task Evidence Contract** — readme_plan_stage, readme_plan_task_evidence_boundary, readme_task_stage, readme_execution_evidence_contract [EXTRACTED 1.00]
- **Progressive Delivery Notifications Control Set** — 2026_05_18_argo_rollouts_progressive_delivery_plan, 2026_05_18_argo_notifications_slack_plan, 0004_rollouts_notifications_headlamp_policy, 0004_rollouts_notifications_headlamp_policy_argo_rollouts_controls, 0004_rollouts_notifications_headlamp_policy_argo_notifications_slack_controls [EXTRACTED 1.00]
- **Observability Operations Control Set** — 0003_service_mesh_cert_manager_policy_kiali_external_observability, 0005_observability_platform_operations_policy, 0005_observability_platform_operations_policy_argocd_metrics_nodeports, 0006_k8s_observability_operations_policy, 0006_k8s_observability_operations_policy_alloy_k8s_logs [EXTRACTED 1.00]
- **App GitOps Onboarding Control Pattern** — 0007_app_gitops_onboarding_policy_app_gitops_onboarding_policy, 0007_app_gitops_onboarding_policy_rollout_required, 0007_app_gitops_onboarding_policy_analysis_template_required, 0007_app_gitops_onboarding_policy_vault_external_secret_boundary, 0007_app_gitops_onboarding_policy_policy_gate_checklist [EXTRACTED 1.00]
- **ArgoCD Metrics Prometheus Recovery Flow** — 0008_argocd_metrics_prometheus_runbook_argocd_metrics_prometheus_recovery_runbook, 0008_argocd_metrics_prometheus_runbook_nodeport_metrics_exposure, 0008_argocd_metrics_prometheus_runbook_k3d_node_ip_drift_response, 0008_argocd_metrics_prometheus_runbook_prometheus_config_reload, 0008_argocd_metrics_prometheus_runbook_observability_evidence_sources [EXTRACTED 1.00]
- **Reference Template Authority Pattern** — readme_reference_stage, readme_reference_authority_boundary, readme_reference_format_contract, readme_templates_reference_and_memory_rules, readme_versions_repo_backed_version_contract [EXTRACTED 1.00]
- **Document Stage Traceability** — prd_template_product_requirements_document, spec_template_technical_specification, task_template_task_document, tests_template_test_evaluation_strategy, runbook_template_runbook_document, postmortem_template_postmortem_document [EXTRACTED 1.00]
- **AI Agent Governance Pattern** — prd_template_ai_agent_requirements, postmortem_template_agent_metadata, spec_template_agent_role_io_contract, spec_template_tool_contract, spec_template_prompt_policy_contract, spec_template_memory_context_strategy, spec_template_guardrails, spec_template_evaluation, task_template_agent_specific_task_types, tests_template_agent_evals, runbook_template_agent_operations [INFERRED 0.95]
- **Verification Evidence Pattern** — postmortem_template_prevention_verification, progress_template_validation_evidence, runbook_template_verification_steps, spec_template_verification_commands, spec_template_success_criteria_verification_plan, task_template_verification_summary, tests_template_evidence_reporting [INFERRED 0.95]

## Communities

### Community 0 - "Platform Bootstrap Operations"
Cohesion: 0.03
Nodes (103): ArgoCD Platform Bootstrap Runbook, WSL2 k3d GitOps Platform Bootstrap Procedure, K8s GitOps Platform Operations Policy, K8s GitOps Platform Operations Policy, External Service Port Contract, External Service Port Contracts, External Service Port Contract, GitOps Path and Branch Verification Gate (+95 more)

### Community 1 - "App Onboarding GitOps"
Cohesion: 0.03
Nodes (81): apps-generator ApplicationSet, External Repo Application CR, GitOps Sync Verification, New App GitOps Onboarding Runbook, Onboarding Troubleshooting, Superseded Generic Onboarding, Vault ESO Secret Setup, AnalysisTemplate Required (+73 more)

### Community 2 - "Architecture Decisions"
Cohesion: 0.04
Nodes (69): ADR-0001 k3d Topology and External Network Baseline, servers=1 agents=3 k3d Topology, ADR-0002 ArgoCD Helm and GitOps Model, App-of-Apps and ApplicationSet, ADR-0003 ESO Vault Kubernetes Auth, Least Privilege Secret Sync, ADR-0004 External Services and Valkey Backend, ArgoCD External Valkey Backend (+61 more)

### Community 3 - "Platform Requirements"
Cohesion: 0.05
Nodes (62): ARD-0001 WSL k3d/k3s ArgoCD Platform, External PostgreSQL and Valkey Services, ArgoCD GitOps Control Plane, ESO and Vault Secret Plane, WSL k3d/k3s ArgoCD Platform, ARD-0003 Platform Expansion Mesh Dashboard, Mesh Plane, Observability Access Plane (+54 more)

### Community 4 - "Core ADR Baseline"
Cohesion: 0.06
Nodes (61): ADR-0001: k3d Topology and External Network Baseline, External Network Baseline, k3d 1 Server 3 Agents Topology, ADR-0001 k3d Topology and External Network Baseline, ADR-0002 ArgoCD Helm Install with App-of-Apps and ApplicationSet, ADR-0002: ArgoCD Helm Install with App-of-Apps and ApplicationSet, App-of-Apps and ApplicationSet Model, ArgoCD Helm Installation Model (+53 more)

### Community 5 - "Traefik Access Routes"
Cohesion: 0.04
Nodes (59): argocd host rule, argocd-k3d Traefik router, argocd-k3d Traefik service, argocd-k3d transport, k3d-hyhome-serverlb:443, websecure entryPoint, Headlamp service headlamp:4466, headlamp host rule (+51 more)

### Community 6 - "Document Templates"
Cohesion: 0.04
Nodes (56): Action Items, Agent Metadata, Required Documentation Feedback Loop, Incident Document, Postmortem Document, Prevention and Verification, Root Cause Analysis, AI Agent Requirements (+48 more)

### Community 7 - "Bootstrap Guides"
Cohesion: 0.04
Nodes (53): ArgoCD root-platform Application, infrastructure/bootstrap-local.sh, WSL k3d ArgoCD Bootstrap Guide, External Secrets Operator Sync, External Services Contract, Vault Secret Contract, CI Static Validation, WSL2 k3d/k3s ArgoCD HA Setup Guide (+45 more)

### Community 8 - "Governance Templates"
Cohesion: 0.07
Nodes (52): Architecture Decision Record Template, Agent Design Template, Agent Governance Hub, Agent Reference Area README, Feature Agent Design Location, Agent Runtime Truth Locations, API Specification Template, Architecture Reference Document Template (+44 more)

### Community 9 - "GitOps Architecture Planes"
Cohesion: 0.07
Nodes (51): ArgoCD App-of-Apps, ESO Vault Secret Plane, External PostgreSQL and Valkey Services, GitOps Platform, GitOps, Secret, and External Data Planes, WSL k3d/k3s ArgoCD Platform ARD, cert-manager TLS Plane, Istio Mesh Plane (+43 more)

### Community 10 - "Adminer Workload Policy"
Cohesion: 0.07
Nodes (47): AnalysisTemplate adminer-stability, kube_pod_container_status_restarts_total, NetworkPolicy allow-egress-apps, Namespace apps, In-cluster pod-to-pod traffic, Istiod control plane, kube-dns, PostgreSQL external services (+39 more)

### Community 11 - "Platform AppProject TLS"
Cohesion: 0.05
Nodes (45): platform cluster resource whitelist, platform destination allowlist, platform namespace resource whitelist, AppProject platform, platform-readonly role, platform source repository allowlist, ClusterIssuer mkcert-ca-issuer, mkcert-root-ca secret reference (+37 more)

### Community 12 - "Agent Governance Rules"
Cohesion: 0.12
Nodes (39): Agentic Execution Rules, GitOps First Mutation Boundary, Agent Framework Contract, AGENTS.md Provider Notes, Repository Execution Constraints, Agent Bootstrap Governance, Bootstrap JIT Loading Sequence, Claude Provider Notes (+31 more)

### Community 13 - "Learning References"
Cohesion: 0.07
Nodes (31): ArgoCD GitOps, k3d and Docker, Efficient Memory Management for LLM Serving with PagedAttention, Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, Reconciliation Loop, Infrastructure to Theory Learning Roadmap, Attention Is All You Need, Vector Indexing (+23 more)

### Community 14 - "Rollouts Notifications"
Cohesion: 0.09
Nodes (26): Argo Rollouts Progressive Delivery ARD, platform-rollouts ArgoCD Application, Argo Notifications Slack ARD, ArgoCD Notifications Controller, Argo Rollouts Progressive Delivery Specification, Rollout and Analysis CRDs, Rollouts Dashboard Route, Rollouts Controller Metrics (+18 more)

### Community 15 - "HA Platform Controls"
Cohesion: 0.11
Nodes (25): Access and TLS Contract, CI Control Plane, CI Static Gate, WSL2 k3d/k3s ArgoCD HA Platform ARD, External Endpoint Contract, ArgoCD Pull Reconciliation Model, AppProject and Vault Minimum Privilege Controls, Static Contract CI Gates (+17 more)

### Community 16 - "Alloy Logging Pipeline"
Cohesion: 0.08
Nodes (25): EndpointSlice alloy-external-1, Service alloy-external, Alloy discovery.kubernetes pods, Alloy discovery.relabel pod_logs, Alloy loki.process events_label, Alloy loki.source.kubernetes_events events, Alloy loki.source.kubernetes pods, Alloy loki.write external_loki (+17 more)

### Community 17 - "GitOps Desired State"
Cohesion: 0.13
Nodes (22): Adminer Reference Workload, ArgoCD App of Apps, clusters local Bootstrap Boundary, Local k3d GitOps Desired State, External Secrets and Vault Contract, GitOps README, Platform Components, GitOps Workloads (+14 more)

### Community 18 - "Monitoring Manifests"
Cohesion: 0.13
Nodes (19): ClusterRole alloy-k8s-logs, ClusterRoleBinding alloy-k8s-logs, ConfigMap alloy-k8s-logs-config, Deployment alloy-k8s-logs, In-cluster Kubernetes log collection, ServiceAccount alloy-k8s-logs, ClusterRole kube-state-metrics, ClusterRoleBinding kube-state-metrics (+11 more)

### Community 19 - "Static Validation Scripts"
Cohesion: 0.14
Nodes (18): check-secret-handling.sh, generate-llm-wiki-index.sh, optional kube-linter, live cluster mutation exclusion, manifest-static CI job, Python PyYAML dependency, repo-backed static validation utilities, repo-quality-static CI job (+10 more)

### Community 20 - "Agent First Remediation"
Cohesion: 0.14
Nodes (18): Agent-first Execution Boundary, k3d Workspace and Agent-first Remediation Plan, Harness Readiness Matrix, Repository Quality Gate, k3d Workspace and Agent-first Remediation Task, scripts Inventory Remediation Plan, Repo-root Argument Contract, scripts Directory Inventory (+10 more)

### Community 21 - "README Template Standards"
Cohesion: 0.15
Nodes (15): AI Agent Guidance, Base Structure, Documentation Standards, README Template, Snippet Library, SSoT Policy, Template Usage, Traceability Rules (+7 more)

### Community 22 - "Spec Task Templates"
Cohesion: 0.17
Nodes (15): Agent Role and IO Contract, API Spec, Guardrails, Parent Design Document, Technical Specification Template, Specification Verification Plan, Agent Specific Task Types, Task Evidence Requirement (+7 more)

### Community 23 - "Headlamp OIDC Operations"
Cohesion: 0.18
Nodes (13): Headlamp Authentication and OIDC Guide, Keycloak Groups to Kubernetes RBAC Mapping, 05.operations Guides Stage, 05.operations Incidents Stage, No Tracked Incidents State, GitOps-first Agent Execution Boundary, k3d Workspace and Agent-first Remediation, Risky Command Boundary Gate (+5 more)

### Community 24 - "Governance Scope Policy"
Cohesion: 0.17
Nodes (12): Documentation Scope, Meta Scope, Stage Checklists, Execution Checklist Stage Taxonomy, AI Agent Standards, Documentation Boundary Policy, Just-in-Time Governance Loading Policy, Agent Language Policy (+4 more)

### Community 25 - "ArgoCD Metrics Notifications"
Cohesion: 0.17
Nodes (12): Service argocd-application-controller-metrics-np, Service argocd-applicationset-controller-metrics-np, ArgoCD Metrics NodePort Services, Service argocd-notifications-controller-metrics-np, Docker Prometheus 172.18.0.10, Service argocd-repo-server-metrics-np, Service argocd-server-metrics-np, ConfigMap argocd-notifications-cm (+4 more)

### Community 26 - "Notifications Rollouts Guides"
Cohesion: 0.17
Nodes (12): Notifications Slack Secret Boundary, Argo Notifications Slack Backfill, Argo Rollouts Progressive Delivery Contract, Argo Rollouts Progressive Delivery Backfill, ArgoCD Metrics NodePort Exposure, ArgoCD Prometheus Metrics and Grafana Guide, GitHub App GitOps Onboarding Guide, Rollout AnalysisTemplate Istio mTLS TLS Pattern (+4 more)

### Community 27 - "WSL2 HA Hardening"
Cohesion: 0.27
Nodes (11): External Traefik to k3d Ingress Access Plane, ARD-0002 WSL2 k3d/k3s ArgoCD HA Platform, CI Static Gates, Namespace Egress Boundaries, WSL2 HA Platform, CI Optimization Phase, WSL2 HA Platform Hardening Plan, AppProject Least Privilege Contract (+3 more)

### Community 28 - "LLM Wiki Governance"
Cohesion: 0.22
Nodes (10): Canonical Owner Rule, LLM Wiki Curation Guide, Generated Markdown Link Map, wiki-curator Agent, Agent-first Harness, LLM Wiki, and Hook Contract Closure Plan, Hook Feedback Loop, Legacy Docs Path Migration Map, Repo-local LLM Wiki (+2 more)

### Community 29 - "Operations Stage READMEs"
Cohesion: 0.24
Nodes (10): Operations Guides README, Guide Traceability Rule, Operations Incidents README, Incident and Postmortem Stage, Operations Policies README, Operations Control Stage, References Authority Boundary, References README (+2 more)

### Community 30 - "Theory Learning Concepts"
Cohesion: 0.31
Nodes (9): ConfigMap Watcher Controller, Efficient Memory Management for LLM Serving with PagedAttention, Infrastructure to Theory Learning Roadmap, Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, Reconciliation Loop, Attention Is All You Need, Vector Indexing, Virtual Memory Paging (+1 more)

### Community 31 - "Headlamp Kiali Ingress"
Cohesion: 0.22
Nodes (9): Ingress headlamp, Headlamp kustomization, ClusterIssuer mkcert-ca-issuer, Service headlamp, TLS Secret headlamp-tls, Ingress kiali, Kiali kustomization, Service kiali (+1 more)

### Community 32 - "CI QA Remediation"
Cohesion: 0.25
Nodes (9): Branch Policy Gate, Repo Quality Gate CI Contract Checks, .github QA and CI Remediation, CI Static Validation, Local Runtime Validation, WSL2 k3d ArgoCD HA Setup Guide, WSL2 k3d/k3s ArgoCD HA Platform Execution, Static Contract Verification (+1 more)

### Community 33 - "Traefik Local Exposure"
Cohesion: 0.25
Nodes (8): Argo Rollouts UI local exposure, ArgoCD UI local exposure, Traefik dynamic config examples, canonical GitOps and ArgoCD deployment path, Headlamp UI local exposure, hy-home.docker Traefik gateway, Kiali UI local exposure, traefik directory

### Community 34 - "Platform Expansion Guide"
Cohesion: 0.33
Nodes (7): Platform Expansion Bootstrap Guide, cert-manager Headlamp Istio Kiali Bootstrap Components, cert-manager Platform Component, Headlamp and 172.18.x Current Contract, Headlamp Platform UI, Istio and Kiali Platform Components, Platform Expansion Execution

### Community 35 - "Root Platform Apps"
Cohesion: 0.4
Nodes (6): Application platform-argocd-config, Application platform-cert-manager, Application platform-cert-manager-config, Helm chart cert-manager v1.17.2, ArgoCD App-of-Apps, apps/root platform Kustomization

### Community 36 - "Workload ApplicationSet"
Cohesion: 0.33
Nodes (6): ApplicationSet apps-generator, apps project application template, gitops/workloads/* directory generator, AppProject apps, apps-readonly role, apps workload resource whitelist

### Community 37 - "Operations Routing"
Cohesion: 0.47
Nodes (6): Guide Runbook Policy Boundary, Operations Guides Stage, Incidents Stage, No Placeholder Incident Contract, Operations Document Routing, Operations Stage

### Community 38 - "ArgoCD Health Alerts"
Cohesion: 0.4
Nodes (5): template.app-health-degraded, template.app-sync-failed, defaultTriggers, trigger.on-health-degraded, trigger.on-sync-failed

### Community 39 - "Namespace Baselines"
Cohesion: 0.4
Nodes (5): Namespace apps, Istio injection enabled, Namespace argo-rollouts, Namespace cert-manager, Namespaces kustomization

### Community 40 - "Bootstrap Secret Contracts"
Cohesion: 0.4
Nodes (5): bootstrap-local.sh, bootstrap-only kubectl apply exception, external Vault PostgreSQL Valkey services, valkey_password, Vault KV secret/platform/argocd

### Community 41 - "WSL Bootstrap Spec"
Cohesion: 0.4
Nodes (5): WSL k3d ArgoCD Bootstrap Guide, Vault Valkey PostgreSQL External Services Contract, WSL k3d/k3s ArgoCD Platform Execution, ArgoCD Platform Bootstrap Runbook, 001 WSL k3d ArgoCD Platform Spec

### Community 42 - "Wiki Script Remediation"
Cohesion: 0.5
Nodes (5): LLM Wiki Curation Guide, Deterministic Markdown Link Map, LLM Wiki Generated Index Contract, scripts Inventory Remediation, Tier A/B/C Script Retention Standard

### Community 43 - "Runbook Template"
Cohesion: 0.4
Nodes (5): Agent Operations Recovery, Immediate Execution Procedure, Operations Runbook, Runbook Template, Runbook Verification Steps

### Community 44 - "README Assembly"
Cohesion: 0.5
Nodes (4): README Assembly Rules, Link Basis Rules, README Usage Guide, README Selection Guide

### Community 45 - "ESO Secret Store"
Cohesion: 0.67
Nodes (3): ESO kustomization, postgres-app-secret.yaml, vault-secret-store.yaml

### Community 46 - "App Deployed Notification"
Cohesion: 1.0
Nodes (2): template.app-deployed, trigger.on-deployed

### Community 47 - "Rollout Completed Notification"
Cohesion: 1.0
Nodes (2): trigger.on-rollout-completed, template.rollout-completed

### Community 48 - "Rollout Aborted Notification"
Cohesion: 1.0
Nodes (2): trigger.on-rollout-aborted, template.rollout-aborted

### Community 49 - "Ingress Retirement"
Cohesion: 1.0
Nodes (2): cloud-native ingress paths, Ingress NGINX upstream retired statement

### Community 50 - "Verification Plan"
Cohesion: 1.0
Nodes (2): Success Criteria and Verification Plan, Verification Commands

### Community 51 - "Gateway Bootstrap"
Cohesion: 1.0
Nodes (1): Gateway JIT Bootstrap Order

### Community 52 - "Gateway Routing"
Cohesion: 1.0
Nodes (1): Gateway Routing Map

### Community 53 - "CI Remediation Task"
Cohesion: 1.0
Nodes (1): .github QA and CI Remediation Task

### Community 54 - "Platform Components"
Cohesion: 1.0
Nodes (1): GitOps platform components

### Community 55 - "External Service Contracts"
Cohesion: 1.0
Nodes (1): External services contracts

### Community 56 - "Network Egress Policies"
Cohesion: 1.0
Nodes (1): Network egress policies

### Community 57 - "Adminer Workload"
Cohesion: 1.0
Nodes (1): workloads/adminer reference workload

### Community 58 - "Validation Scripts"
Cohesion: 1.0
Nodes (1): GitOps validation scripts

### Community 59 - "ESO Vault Contract"
Cohesion: 1.0
Nodes (1): External Secrets and Vault contract

### Community 60 - "Headlamp Namespace"
Cohesion: 1.0
Nodes (1): Namespace headlamp

### Community 61 - "Static Contract Validation"
Cohesion: 1.0
Nodes (1): static contract validation

### Community 62 - "Live Cluster Validation"
Cohesion: 1.0
Nodes (1): live cluster validation

### Community 63 - "Graphify Tooling"
Cohesion: 1.0
Nodes (1): optional graphify tool

### Community 64 - "Progress Memory"
Cohesion: 1.0
Nodes (1): Agent Progress and Memory Ledger

### Community 65 - "MetalLB Traefik"
Cohesion: 1.0
Nodes (1): MetalLB and Traefik

## Knowledge Gaps
- **426 isolated node(s):** `Gateway JIT Bootstrap Order`, `Repository Execution Constraints`, `Gateway Routing Map`, `Spec Driven Docs Taxonomy`, `Local Skill Roster` (+421 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `App Deployed Notification`** (2 nodes): `template.app-deployed`, `trigger.on-deployed`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Rollout Completed Notification`** (2 nodes): `trigger.on-rollout-completed`, `template.rollout-completed`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Rollout Aborted Notification`** (2 nodes): `trigger.on-rollout-aborted`, `template.rollout-aborted`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ingress Retirement`** (2 nodes): `cloud-native ingress paths`, `Ingress NGINX upstream retired statement`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Verification Plan`** (2 nodes): `Success Criteria and Verification Plan`, `Verification Commands`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Gateway Bootstrap`** (1 nodes): `Gateway JIT Bootstrap Order`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Gateway Routing`** (1 nodes): `Gateway Routing Map`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `CI Remediation Task`** (1 nodes): `.github QA and CI Remediation Task`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Platform Components`** (1 nodes): `GitOps platform components`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `External Service Contracts`** (1 nodes): `External services contracts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Network Egress Policies`** (1 nodes): `Network egress policies`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Adminer Workload`** (1 nodes): `workloads/adminer reference workload`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Validation Scripts`** (1 nodes): `GitOps validation scripts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `ESO Vault Contract`** (1 nodes): `External Secrets and Vault contract`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Headlamp Namespace`** (1 nodes): `Namespace headlamp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Static Contract Validation`** (1 nodes): `static contract validation`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Live Cluster Validation`** (1 nodes): `live cluster validation`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Graphify Tooling`** (1 nodes): `optional graphify tool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Progress Memory`** (1 nodes): `Agent Progress and Memory Ledger`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `MetalLB Traefik`** (1 nodes): `MetalLB and Traefik`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLM Wiki Reference Index` connect `Architecture Decisions` to `App Onboarding GitOps`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Why does `App GitOps Onboarding Policy` connect `App Onboarding GitOps` to `Platform Bootstrap Operations`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Why does `Canonical Owner Pointers` connect `App Onboarding GitOps` to `Architecture Decisions`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **What connects `Gateway JIT Bootstrap Order`, `Repository Execution Constraints`, `Gateway Routing Map` to the rest of the system?**
  _426 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Platform Bootstrap Operations` be split into smaller, more focused modules?**
  _Cohesion score 0.03 - nodes in this community are weakly interconnected._
- **Should `App Onboarding GitOps` be split into smaller, more focused modules?**
  _Cohesion score 0.03 - nodes in this community are weakly interconnected._
- **Should `Architecture Decisions` be split into smaller, more focused modules?**
  _Cohesion score 0.04 - nodes in this community are weakly interconnected._
