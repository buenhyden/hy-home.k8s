# Graph Report - .  (2026-05-25)

## Corpus Check
- Large corpus: 245 files · ~143,316 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 1271 nodes · 1729 edges · 71 communities detected
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 122 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_05 Operations Runbooks|05 Operations Runbooks]]
- [[_COMMUNITY_App Gitops Onboarding Policy|App Gitops Onboarding Policy]]
- [[_COMMUNITY_003 Platform Expansion|003 Platform Expansion]]
- [[_COMMUNITY_Agent Framework Contract|Agent Framework Contract]]
- [[_COMMUNITY_Architecture Decision Records Stage|Architecture Decision Records Stage]]
- [[_COMMUNITY_Requirements Stage|Requirements Stage]]
- [[_COMMUNITY_Technical Specification|Technical Specification]]
- [[_COMMUNITY_Canonical Template Stage|Canonical Template Stage]]
- [[_COMMUNITY_Platform Expansion Bootstrap Guide|Platform Expansion Bootstrap Guide]]
- [[_COMMUNITY_Platform Expansion Specification|Platform Expansion Specification]]
- [[_COMMUNITY_Networkpolicy Allow Kiali Egress To|Networkpolicy Allow Kiali Egress To]]
- [[_COMMUNITY_Appproject Platform|Appproject Platform]]
- [[_COMMUNITY_Argo Rollouts Progressive Delivery Backfill|Argo Rollouts Progressive Delivery Backfill]]
- [[_COMMUNITY_Local Argocd Values|Local Argocd Values]]
- [[_COMMUNITY_Infrastructure To Theory Learning Roadmap|Infrastructure To Theory Learning Roadmap]]
- [[_COMMUNITY_Argocd K3D Traefik Router|Argocd K3D Traefik Router]]
- [[_COMMUNITY_External Services Kustomization|External Services Kustomization]]
- [[_COMMUNITY_Wsl2 K3D K3S Argocd Ha|Wsl2 K3D K3S Argocd Ha]]
- [[_COMMUNITY_Gitops|Gitops]]
- [[_COMMUNITY_Deployment Kube State Metrics|Deployment Kube State Metrics]]
- [[_COMMUNITY_K3D Workspace And Agent First|K3D Workspace And Agent First]]
- [[_COMMUNITY_Repository Validation Model|Repository Validation Model]]
- [[_COMMUNITY_Specs Stage|Specs Stage]]
- [[_COMMUNITY_Tech Stack Version Inventory|Tech Stack Version Inventory]]
- [[_COMMUNITY_Reference Document|Reference Document]]
- [[_COMMUNITY_Test And Evaluation Strategy Template|Test And Evaluation Strategy Template]]
- [[_COMMUNITY_New App Gitops Onboarding Guide|New App Gitops Onboarding Guide]]
- [[_COMMUNITY_05 Operations Operations Hub|05 Operations Operations Hub]]
- [[_COMMUNITY_Ai Agent Standards|Ai Agent Standards]]
- [[_COMMUNITY_Argocd Metrics Nodeport Services|Argocd Metrics Nodeport Services]]
- [[_COMMUNITY_Argo Rollouts Progressive Delivery Contract|Argo Rollouts Progressive Delivery Contract]]
- [[_COMMUNITY_Agent First Harness Llm Wiki|Agent First Harness Llm Wiki]]
- [[_COMMUNITY_Ingress Headlamp|Ingress Headlamp]]
- [[_COMMUNITY_Wsl2 K3D Argocd Ha Setup|Wsl2 K3D Argocd Ha Setup]]
- [[_COMMUNITY_Traefik Dynamic Config Examples|Traefik Dynamic Config Examples]]
- [[_COMMUNITY_Platform Expansion Execution|Platform Expansion Execution]]
- [[_COMMUNITY_Wsl2 K3D K3S Argocd Ha|Wsl2 K3D K3S Argocd Ha]]
- [[_COMMUNITY_Canonical Template Stage|Canonical Template Stage]]
- [[_COMMUNITY_Application Platform Cert Manager|Application Platform Cert Manager]]
- [[_COMMUNITY_Appproject Apps|Appproject Apps]]
- [[_COMMUNITY_Operations Document Routing|Operations Document Routing]]
- [[_COMMUNITY_Defaulttriggers|Defaulttriggers]]
- [[_COMMUNITY_Namespaces Kustomization|Namespaces Kustomization]]
- [[_COMMUNITY_Vault Kv Secret Platform Argocd|Vault Kv Secret Platform Argocd]]
- [[_COMMUNITY_Wsl K3D K3S Argocd Platform|Wsl K3D K3S Argocd Platform]]
- [[_COMMUNITY_Llm Wiki Generated Index Contract|Llm Wiki Generated Index Contract]]
- [[_COMMUNITY_Runbook Template|Runbook Template]]
- [[_COMMUNITY_Usage Guide|Usage Guide]]
- [[_COMMUNITY_Eso Kustomization|Eso Kustomization]]
- [[_COMMUNITY_Reference Stage Index|Reference Stage Index]]
- [[_COMMUNITY_Template App Deployed|Template App Deployed]]
- [[_COMMUNITY_Trigger On Rollout Completed|Trigger On Rollout Completed]]
- [[_COMMUNITY_Trigger On Rollout Aborted|Trigger On Rollout Aborted]]
- [[_COMMUNITY_Cloud Native Ingress Paths|Cloud Native Ingress Paths]]
- [[_COMMUNITY_Success Criteria And Verification|Success Criteria And Verification]]
- [[_COMMUNITY_K3D Agent First Remediation|K3D Agent First Remediation]]
- [[_COMMUNITY_Gateway Jit Bootstrap Order|Gateway Jit Bootstrap Order]]
- [[_COMMUNITY_Gateway Routing Map|Gateway Routing Map]]
- [[_COMMUNITY_Github Qa And Ci Remediation|Github Qa And Ci Remediation]]
- [[_COMMUNITY_Gitops Platform Components|Gitops Platform Components]]
- [[_COMMUNITY_External Services Contracts|External Services Contracts]]
- [[_COMMUNITY_Network Egress Policies|Network Egress Policies]]
- [[_COMMUNITY_Workloads Adminer Reference Workload|Workloads Adminer Reference Workload]]
- [[_COMMUNITY_Gitops Validation Scripts|Gitops Validation Scripts]]
- [[_COMMUNITY_External Secrets And Vault Contract|External Secrets And Vault Contract]]
- [[_COMMUNITY_Namespace Headlamp|Namespace Headlamp]]
- [[_COMMUNITY_Static Contract Validation|Static Contract Validation]]
- [[_COMMUNITY_Live Cluster Validation|Live Cluster Validation]]
- [[_COMMUNITY_Optional Graphify Tool|Optional Graphify Tool]]
- [[_COMMUNITY_Metallb And Traefik|Metallb And Traefik]]
- [[_COMMUNITY_Execution Implementation Audit|Execution Implementation Audit]]

## God Nodes (most connected - your core abstractions)
1. `Canonical Template Stage README` - 21 edges
2. `AppProject platform` - 19 edges
3. `Agent Framework Contract` - 18 edges
4. `Platform Expansion Specification` - 18 edges
5. `Technical Specification` - 17 edges
6. `Local Harness Catalog` - 16 edges
7. `App GitOps Onboarding Policy` - 16 edges
8. `Local Harness Catalog` - 15 edges
9. `Requirements Stage` - 13 edges
10. `Product Requirements Document` - 13 edges

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

## Communities

### Community 0 - "05 Operations Runbooks"
Cohesion: 0.03
Nodes (104): ArgoCD Platform Bootstrap Runbook, WSL2 k3d GitOps Platform Bootstrap Procedure, K8s GitOps Platform Operations Policy, K8s GitOps Platform Operations Policy, External Service Port Contract, External Service Port Contracts, External Service Port Contract, GitOps Path and Branch Verification Gate (+96 more)

### Community 1 - "App Gitops Onboarding Policy"
Cohesion: 0.03
Nodes (81): apps-generator ApplicationSet, External Repo Application CR, GitOps Sync Verification, New App GitOps Onboarding Runbook, Onboarding Troubleshooting, Superseded Generic Onboarding, Vault ESO Secret Setup, AnalysisTemplate Required (+73 more)

### Community 2 - "003 Platform Expansion"
Cohesion: 0.05
Nodes (73): ARD-0001 WSL k3d/k3s ArgoCD Platform, External PostgreSQL and Valkey Services, ArgoCD GitOps Control Plane, ESO and Vault Secret Plane, WSL k3d/k3s ArgoCD Platform, External Traefik to k3d Ingress Access Plane, ARD-0002 WSL2 k3d/k3s ArgoCD HA Platform, CI Static Gates (+65 more)

### Community 3 - "Agent Framework Contract"
Cohesion: 0.07
Nodes (62): AI Agent Governance Hub, Agentic Execution Rules, GitOps First Mutation Boundary, GitOps First Execution Boundary, Agent Framework Contract, AGENTS.md Provider Notes, Repository Execution Constraints, Agent Bootstrap Governance (+54 more)

### Community 4 - "Architecture Decision Records Stage"
Cohesion: 0.06
Nodes (59): ADR-0001: k3d Topology and External Network Baseline, External Network Baseline, k3d 1 Server 3 Agents Topology, ADR-0001 k3d Topology and External Network Baseline, ADR-0002 ArgoCD Helm Install with App-of-Apps and ApplicationSet, ADR-0002: ArgoCD Helm Install with App-of-Apps and ApplicationSet, App-of-Apps and ApplicationSet Model, ArgoCD Helm Installation Model (+51 more)

### Community 5 - "Requirements Stage"
Cohesion: 0.05
Nodes (57): ADR-0001 k3d Topology and External Network Baseline, servers=1 agents=3 k3d Topology, ADR-0002 ArgoCD Helm and GitOps Model, App-of-Apps and ApplicationSet, ADR-0003 ESO Vault Kubernetes Auth, Least Privilege Secret Sync, ADR-0004 External Services and Valkey Backend, ArgoCD External Valkey Backend (+49 more)

### Community 6 - "Technical Specification"
Cohesion: 0.04
Nodes (56): Action Items, Agent Metadata, Required Documentation Feedback Loop, Incident Document, Postmortem Document, Prevention and Verification, Root Cause Analysis, AI Agent Requirements (+48 more)

### Community 7 - "Canonical Template Stage"
Cohesion: 0.06
Nodes (56): Architecture Decision Record Template, Agent Design Template, Agent Governance Hub, Agent Reference Area README, Feature Agent Design Location, Agent Runtime Truth Locations, API Specification Template, Architecture Reference Document Template (+48 more)

### Community 8 - "Platform Expansion Bootstrap Guide"
Cohesion: 0.04
Nodes (53): ArgoCD root-platform Application, infrastructure/bootstrap-local.sh, WSL k3d ArgoCD Bootstrap Guide, External Secrets Operator Sync, External Services Contract, Vault Secret Contract, CI Static Validation, WSL2 k3d/k3s ArgoCD HA Setup Guide (+45 more)

### Community 9 - "Platform Expansion Specification"
Cohesion: 0.07
Nodes (51): ArgoCD App-of-Apps, ESO Vault Secret Plane, External PostgreSQL and Valkey Services, GitOps Platform, GitOps, Secret, and External Data Planes, WSL k3d/k3s ArgoCD Platform ARD, cert-manager TLS Plane, Istio Mesh Plane (+43 more)

### Community 10 - "Networkpolicy Allow Kiali Egress To"
Cohesion: 0.07
Nodes (47): AnalysisTemplate adminer-stability, kube_pod_container_status_restarts_total, NetworkPolicy allow-egress-apps, Namespace apps, In-cluster pod-to-pod traffic, Istiod control plane, kube-dns, PostgreSQL external services (+39 more)

### Community 11 - "Appproject Platform"
Cohesion: 0.05
Nodes (45): platform cluster resource whitelist, platform destination allowlist, platform namespace resource whitelist, AppProject platform, platform-readonly role, platform source repository allowlist, ClusterIssuer mkcert-ca-issuer, mkcert-root-ca secret reference (+37 more)

### Community 12 - "Argo Rollouts Progressive Delivery Backfill"
Cohesion: 0.07
Nodes (39): Argo Rollouts Progressive Delivery ARD, platform-rollouts ArgoCD Application, Argo Rollouts Notifications and Headlamp Operations Policy, Argo Notifications Slack Controls, Argo Rollouts Controls, Traefik External Artifacts, Argo Notifications Slack ARD, ArgoCD Notifications Controller (+31 more)

### Community 13 - "Local Argocd Values"
Cohesion: 0.07
Nodes (33): argocd host rule, ArgoCD Helm values, GitOps and ArgoCD reconciliation, infrastructure directory, local k3d Kubernetes platform, MetalLB bootstrap manifests, IPAddressPool, 172.18.0.240-172.18.0.250 (+25 more)

### Community 14 - "Infrastructure To Theory Learning Roadmap"
Cohesion: 0.07
Nodes (31): ArgoCD GitOps, k3d and Docker, Efficient Memory Management for LLM Serving with PagedAttention, Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, Reconciliation Loop, Infrastructure to Theory Learning Roadmap, Attention Is All You Need, Vector Indexing (+23 more)

### Community 15 - "Argocd K3D Traefik Router"
Cohesion: 0.08
Nodes (26): argocd-k3d Traefik router, argocd-k3d Traefik service, argocd-k3d transport, k3d-hyhome-serverlb:443, websecure entryPoint, Headlamp service headlamp:4466, headlamp host rule, headlamp-k3d Traefik router (+18 more)

### Community 16 - "External Services Kustomization"
Cohesion: 0.08
Nodes (25): EndpointSlice alloy-external-1, Service alloy-external, Alloy discovery.kubernetes pods, Alloy discovery.relabel pod_logs, Alloy loki.process events_label, Alloy loki.source.kubernetes_events events, Alloy loki.source.kubernetes pods, Alloy loki.write external_loki (+17 more)

### Community 17 - "Wsl2 K3D K3S Argocd Ha"
Cohesion: 0.11
Nodes (25): Access and TLS Contract, CI Control Plane, CI Static Gate, WSL2 k3d/k3s ArgoCD HA Platform ARD, External Endpoint Contract, ArgoCD Pull Reconciliation Model, AppProject and Vault Minimum Privilege Controls, Static Contract CI Gates (+17 more)

### Community 18 - "Gitops"
Cohesion: 0.13
Nodes (22): Adminer Reference Workload, ArgoCD App of Apps, clusters local Bootstrap Boundary, Local k3d GitOps Desired State, External Secrets and Vault Contract, GitOps README, Platform Components, GitOps Workloads (+14 more)

### Community 19 - "Deployment Kube State Metrics"
Cohesion: 0.13
Nodes (19): ClusterRole alloy-k8s-logs, ClusterRoleBinding alloy-k8s-logs, ConfigMap alloy-k8s-logs-config, Deployment alloy-k8s-logs, In-cluster Kubernetes log collection, ServiceAccount alloy-k8s-logs, ClusterRole kube-state-metrics, ClusterRoleBinding kube-state-metrics (+11 more)

### Community 20 - "K3D Workspace And Agent First"
Cohesion: 0.14
Nodes (18): Agent-first Execution Boundary, k3d Workspace and Agent-first Remediation Plan, Harness Readiness Matrix, Repository Quality Gate, k3d Workspace and Agent-first Remediation Task, scripts Inventory Remediation Plan, Repo-root Argument Contract, scripts Directory Inventory (+10 more)

### Community 21 - "Repository Validation Model"
Cohesion: 0.14
Nodes (18): check-secret-handling.sh, generate-llm-wiki-index.sh, optional kube-linter, live cluster mutation exclusion, manifest-static CI job, Python PyYAML dependency, repo-backed static validation utilities, repo-quality-static CI job (+10 more)

### Community 22 - "Specs Stage"
Cohesion: 0.17
Nodes (18): WSL k3d ArgoCD Platform Plan, WSL2 k3d ArgoCD HA Platform Plan, Template Cross-link Fix Plan, Docs Governance Full AB Hardening Plan, Workspace Purpose Alignment Audit Plan, Workspace Harness Gap Analysis Plan, Architecture Requirements README, WSL k3d ArgoCD Platform Spec (+10 more)

### Community 23 - "Tech Stack Version Inventory"
Cohesion: 0.16
Nodes (18): Apps AppProject Workload Permissions, Platform AppProject Permissions, Platform App-of-Apps Kustomization, Local Cluster ArgoCD Bootstrap Kustomization, GitOps Desired State Boundary, Bootstrap Infrastructure Boundary, LLM WIKI Reference Index, Platform Cluster Config Root Application (+10 more)

### Community 24 - "Reference Document"
Cohesion: 0.15
Nodes (15): AI Agent Guidance, Base Structure, Documentation Standards, README Template, Snippet Library, SSoT Policy, Template Usage, Traceability Rules (+7 more)

### Community 25 - "Test And Evaluation Strategy Template"
Cohesion: 0.17
Nodes (15): Agent Role and IO Contract, API Spec, Guardrails, Parent Design Document, Technical Specification Template, Specification Verification Plan, Agent Specific Task Types, Task Evidence Requirement (+7 more)

### Community 26 - "New App Gitops Onboarding Guide"
Cohesion: 0.22
Nodes (14): ArgoCD Platform Bootstrap Runbook, WSL k3d ArgoCD Bootstrap Guide, WSL2 k3d ArgoCD HA Setup Guide, apps-generator ApplicationSet Onboarding, New App GitOps Onboarding Guide, Superseded by GitHub App Onboarding, New App Onboarding Runbook, App GitOps Onboarding Policy (+6 more)

### Community 27 - "05 Operations Operations Hub"
Cohesion: 0.18
Nodes (13): Headlamp Authentication and OIDC Guide, Keycloak Groups to Kubernetes RBAC Mapping, 05.operations Guides Stage, 05.operations Incidents Stage, No Tracked Incidents State, GitOps-first Agent Execution Boundary, k3d Workspace and Agent-first Remediation, Risky Command Boundary Gate (+5 more)

### Community 28 - "Ai Agent Standards"
Cohesion: 0.17
Nodes (12): Documentation Scope, Meta Scope, Stage Checklists, Execution Checklist Stage Taxonomy, AI Agent Standards, Documentation Boundary Policy, Just-in-Time Governance Loading Policy, Agent Language Policy (+4 more)

### Community 29 - "Argocd Metrics Nodeport Services"
Cohesion: 0.17
Nodes (12): Service argocd-application-controller-metrics-np, Service argocd-applicationset-controller-metrics-np, ArgoCD Metrics NodePort Services, Service argocd-notifications-controller-metrics-np, Docker Prometheus 172.18.0.10, Service argocd-repo-server-metrics-np, Service argocd-server-metrics-np, ConfigMap argocd-notifications-cm (+4 more)

### Community 30 - "Argo Rollouts Progressive Delivery Contract"
Cohesion: 0.17
Nodes (12): Notifications Slack Secret Boundary, Argo Notifications Slack Backfill, Argo Rollouts Progressive Delivery Contract, Argo Rollouts Progressive Delivery Backfill, ArgoCD Metrics NodePort Exposure, ArgoCD Prometheus Metrics and Grafana Guide, GitHub App GitOps Onboarding Guide, Rollout AnalysisTemplate Istio mTLS TLS Pattern (+4 more)

### Community 31 - "Agent First Harness Llm Wiki"
Cohesion: 0.22
Nodes (10): Canonical Owner Rule, LLM Wiki Curation Guide, Generated Markdown Link Map, wiki-curator Agent, Agent-first Harness, LLM Wiki, and Hook Contract Closure Plan, Hook Feedback Loop, Legacy Docs Path Migration Map, Repo-local LLM Wiki (+2 more)

### Community 32 - "Ingress Headlamp"
Cohesion: 0.22
Nodes (9): Ingress headlamp, Headlamp kustomization, ClusterIssuer mkcert-ca-issuer, Service headlamp, TLS Secret headlamp-tls, Ingress kiali, Kiali kustomization, Service kiali (+1 more)

### Community 33 - "Wsl2 K3D Argocd Ha Setup"
Cohesion: 0.25
Nodes (9): Branch Policy Gate, Repo Quality Gate CI Contract Checks, .github QA and CI Remediation, CI Static Validation, Local Runtime Validation, WSL2 k3d ArgoCD HA Setup Guide, WSL2 k3d/k3s ArgoCD HA Platform Execution, Static Contract Verification (+1 more)

### Community 34 - "Traefik Dynamic Config Examples"
Cohesion: 0.25
Nodes (8): Argo Rollouts UI local exposure, ArgoCD UI local exposure, Traefik dynamic config examples, canonical GitOps and ArgoCD deployment path, Headlamp UI local exposure, hy-home.docker Traefik gateway, Kiali UI local exposure, traefik directory

### Community 35 - "Platform Expansion Execution"
Cohesion: 0.33
Nodes (7): Platform Expansion Bootstrap Guide, cert-manager Headlamp Istio Kiali Bootstrap Components, cert-manager Platform Component, Headlamp and 172.18.x Current Contract, Headlamp Platform UI, Istio and Kiali Platform Components, Platform Expansion Execution

### Community 36 - "Wsl2 K3D K3S Argocd Ha"
Cohesion: 0.48
Nodes (7): External Service Current Contract, Platform Expansion Mesh Dashboard Architecture Reference Document, Requirements Stage, WSL2 k3d k3s ArgoCD HA Platform Architecture Reference Document, WSL2 k3d k3s ArgoCD HA Platform Product Requirements, WSL k3d k3s ArgoCD Platform Architecture Reference Document, WSL2 k3s k3d ArgoCD Platform Product Requirements

### Community 37 - "Canonical Template Stage"
Cohesion: 0.57
Nodes (7): Agent Design Template Contract, Incident Fact Record Template, Operations Policy Template Contract, Postmortem Analysis Template Contract, Reference Authority Boundary Template, Executable Runbook Template Contract, Canonical Template Stage

### Community 38 - "Application Platform Cert Manager"
Cohesion: 0.4
Nodes (6): Application platform-argocd-config, Application platform-cert-manager, Application platform-cert-manager-config, Helm chart cert-manager v1.17.2, ArgoCD App-of-Apps, apps/root platform Kustomization

### Community 39 - "Appproject Apps"
Cohesion: 0.33
Nodes (6): ApplicationSet apps-generator, apps project application template, gitops/workloads/* directory generator, AppProject apps, apps-readonly role, apps workload resource whitelist

### Community 40 - "Operations Document Routing"
Cohesion: 0.47
Nodes (6): Guide Runbook Policy Boundary, Operations Guides Stage, Incidents Stage, No Placeholder Incident Contract, Operations Document Routing, Operations Stage

### Community 41 - "Defaulttriggers"
Cohesion: 0.4
Nodes (5): template.app-health-degraded, template.app-sync-failed, defaultTriggers, trigger.on-health-degraded, trigger.on-sync-failed

### Community 42 - "Namespaces Kustomization"
Cohesion: 0.4
Nodes (5): Namespace apps, Istio injection enabled, Namespace argo-rollouts, Namespace cert-manager, Namespaces kustomization

### Community 43 - "Vault Kv Secret Platform Argocd"
Cohesion: 0.4
Nodes (5): bootstrap-local.sh, bootstrap-only kubectl apply exception, external Vault PostgreSQL Valkey services, valkey_password, Vault KV secret/platform/argocd

### Community 44 - "Wsl K3D K3S Argocd Platform"
Cohesion: 0.4
Nodes (5): WSL k3d ArgoCD Bootstrap Guide, Vault Valkey PostgreSQL External Services Contract, WSL k3d/k3s ArgoCD Platform Execution, ArgoCD Platform Bootstrap Runbook, 001 WSL k3d ArgoCD Platform Spec

### Community 45 - "Llm Wiki Generated Index Contract"
Cohesion: 0.5
Nodes (5): LLM Wiki Curation Guide, Deterministic Markdown Link Map, LLM Wiki Generated Index Contract, scripts Inventory Remediation, Tier A/B/C Script Retention Standard

### Community 46 - "Runbook Template"
Cohesion: 0.4
Nodes (5): Agent Operations Recovery, Immediate Execution Procedure, Operations Runbook, Runbook Template, Runbook Verification Steps

### Community 47 - "Usage Guide"
Cohesion: 0.5
Nodes (4): README Assembly Rules, Link Basis Rules, README Usage Guide, README Selection Guide

### Community 48 - "Eso Kustomization"
Cohesion: 0.67
Nodes (3): ESO kustomization, postgres-app-secret.yaml, vault-secret-store.yaml

### Community 49 - "Reference Stage Index"
Cohesion: 0.67
Nodes (3): Agent References Stage Index, Learning References Stage Index, Reference Stage Index

### Community 50 - "Template App Deployed"
Cohesion: 1.0
Nodes (2): template.app-deployed, trigger.on-deployed

### Community 51 - "Trigger On Rollout Completed"
Cohesion: 1.0
Nodes (2): trigger.on-rollout-completed, template.rollout-completed

### Community 52 - "Trigger On Rollout Aborted"
Cohesion: 1.0
Nodes (2): trigger.on-rollout-aborted, template.rollout-aborted

### Community 53 - "Cloud Native Ingress Paths"
Cohesion: 1.0
Nodes (2): cloud-native ingress paths, Ingress NGINX upstream retired statement

### Community 54 - "Success Criteria And Verification"
Cohesion: 1.0
Nodes (2): Success Criteria and Verification Plan, Verification Commands

### Community 55 - "K3D Agent First Remediation"
Cohesion: 1.0
Nodes (2): k3d Agent-first Remediation Plan, k3d Agent-first Remediation Task

### Community 56 - "Gateway Jit Bootstrap Order"
Cohesion: 1.0
Nodes (1): Gateway JIT Bootstrap Order

### Community 57 - "Gateway Routing Map"
Cohesion: 1.0
Nodes (1): Gateway Routing Map

### Community 58 - "Github Qa And Ci Remediation"
Cohesion: 1.0
Nodes (1): .github QA and CI Remediation Task

### Community 59 - "Gitops Platform Components"
Cohesion: 1.0
Nodes (1): GitOps platform components

### Community 60 - "External Services Contracts"
Cohesion: 1.0
Nodes (1): External services contracts

### Community 61 - "Network Egress Policies"
Cohesion: 1.0
Nodes (1): Network egress policies

### Community 62 - "Workloads Adminer Reference Workload"
Cohesion: 1.0
Nodes (1): workloads/adminer reference workload

### Community 63 - "Gitops Validation Scripts"
Cohesion: 1.0
Nodes (1): GitOps validation scripts

### Community 64 - "External Secrets And Vault Contract"
Cohesion: 1.0
Nodes (1): External Secrets and Vault contract

### Community 65 - "Namespace Headlamp"
Cohesion: 1.0
Nodes (1): Namespace headlamp

### Community 66 - "Static Contract Validation"
Cohesion: 1.0
Nodes (1): static contract validation

### Community 67 - "Live Cluster Validation"
Cohesion: 1.0
Nodes (1): live cluster validation

### Community 68 - "Optional Graphify Tool"
Cohesion: 1.0
Nodes (1): optional graphify tool

### Community 69 - "Metallb And Traefik"
Cohesion: 1.0
Nodes (1): MetalLB and Traefik

### Community 70 - "Execution Implementation Audit"
Cohesion: 1.0
Nodes (1): Spec Execution Implementation Audit Plan

## Knowledge Gaps
- **438 isolated node(s):** `Gateway JIT Bootstrap Order`, `Repository Execution Constraints`, `Gateway Routing Map`, `Spec Driven Docs Taxonomy`, `Local Skill Roster` (+433 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Template App Deployed`** (2 nodes): `template.app-deployed`, `trigger.on-deployed`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Trigger On Rollout Completed`** (2 nodes): `trigger.on-rollout-completed`, `template.rollout-completed`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Trigger On Rollout Aborted`** (2 nodes): `trigger.on-rollout-aborted`, `template.rollout-aborted`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Cloud Native Ingress Paths`** (2 nodes): `cloud-native ingress paths`, `Ingress NGINX upstream retired statement`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Success Criteria And Verification`** (2 nodes): `Success Criteria and Verification Plan`, `Verification Commands`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `K3D Agent First Remediation`** (2 nodes): `k3d Agent-first Remediation Plan`, `k3d Agent-first Remediation Task`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Gateway Jit Bootstrap Order`** (1 nodes): `Gateway JIT Bootstrap Order`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Gateway Routing Map`** (1 nodes): `Gateway Routing Map`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Github Qa And Ci Remediation`** (1 nodes): `.github QA and CI Remediation Task`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Gitops Platform Components`** (1 nodes): `GitOps platform components`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `External Services Contracts`** (1 nodes): `External services contracts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Network Egress Policies`** (1 nodes): `Network egress policies`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Workloads Adminer Reference Workload`** (1 nodes): `workloads/adminer reference workload`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Gitops Validation Scripts`** (1 nodes): `GitOps validation scripts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `External Secrets And Vault Contract`** (1 nodes): `External Secrets and Vault contract`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Namespace Headlamp`** (1 nodes): `Namespace headlamp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Static Contract Validation`** (1 nodes): `static contract validation`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Live Cluster Validation`** (1 nodes): `live cluster validation`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Optional Graphify Tool`** (1 nodes): `optional graphify tool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Metallb And Traefik`** (1 nodes): `MetalLB and Traefik`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Execution Implementation Audit`** (1 nodes): `Spec Execution Implementation Audit Plan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLM Wiki Reference Index` connect `Requirements Stage` to `App Gitops Onboarding Policy`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Why does `App GitOps Onboarding Policy` connect `App Gitops Onboarding Policy` to `05 Operations Runbooks`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Why does `Canonical Owner Pointers` connect `App Gitops Onboarding Policy` to `Requirements Stage`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **What connects `Gateway JIT Bootstrap Order`, `Repository Execution Constraints`, `Gateway Routing Map` to the rest of the system?**
  _438 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `05 Operations Runbooks` be split into smaller, more focused modules?**
  _Cohesion score 0.03 - nodes in this community are weakly interconnected._
- **Should `App Gitops Onboarding Policy` be split into smaller, more focused modules?**
  _Cohesion score 0.03 - nodes in this community are weakly interconnected._
- **Should `003 Platform Expansion` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._
