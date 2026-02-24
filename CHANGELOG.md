# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## [0.0.1]

### Added

- Add expert rules for GitOps, Kubernetes, and DevSecOps.
- Add CI/CD pipelines rule covering concepts, tools, best practices, and security.
- Bootstrap Kubernetes cluster with core infrastructure components and sample applications.
- Add Airflow secrets definition for Kubernetes deployment.
- 업데이트된 README 및 추가 스크립트, CI/CD 파이프라인, 자격증명 가이드 및 템플릿 추가
- CI/CD 파이프라인 통합 및 기존 YAML 파일 삭제
- Add unified CI/CD workflow with linting, building, testing, and deployment for services, including Makefiles and an ArgoCD bootstrap script.
- Add yamllint configuration file with default rules and ignored paths.
- Add new Kubernetes agent workflows for safe operations, deployment, multi-environment deployment, and troubleshooting, along with general, security, and multi-environment rules.
- Add Kubernetes workflows for multi-environment deployment, safe operations, troubleshooting, and application deployment
- **agent:** Initialize comprehensive rules and workflows
- **apps:** Refine demo-backend and templates to follow project rules
- Initialize project with a comprehensive README detailing its AI-optimized GitOps structure and update agent rule paths.
- Initialize project with comprehensive documentation, CI/CD, governance, and an AI-ready GitOps Kubernetes platform.
- Establish initial repository structure with CI, Dependabot, PR template, and example application documentation.
- Add CI workflow for linting Markdown, GitHub Actions, and validating Kubernetes manifests.
- Add GitHub Actions CI workflow for Markdown, GitHub Actions, and Kubernetes manifest linting.
- Implement foundational development standards with `.editorconfig`, comprehensive CI pipelines for linting and validation, and updated Markdown linting configurations.
- Add a pre-commit git hook for various linting checks and update CONTRIBUTING.md with instructions to enable it.
- Add pre-commit hook to lint Markdown, GitHub Actions, Kubernetes, and Python files.
- Add pre-commit hooks for linting Markdown, GitHub Actions, Kubernetes, and Python code.
- Introduce development workflow documentation, pre-commit linting hooks, and bootstrap scripts for development tool installation.
- Introduce core Kubernetes manifests for applications and external services, along with initial developer tooling and CI/CD setup.
- Add GitHub Actions CI workflow for linting and bootstrap scripts for Kind cluster setup and ArgoCD installation.
- Add initial bootstrap scripts for Kind cluster setup, developer pre-commit tools, and ArgoCD SSH repository configuration with SealedSecrets.
- Add GitHub issue templates and Dependabot configuration for automated dependency updates.
- Introduce a comprehensive documentation framework with templates, creation scripts, and validation tools for ADRs, ARDs, Plans, PRDs, and Specs.
- Introduce agent system with comprehensive rules and workflows, replacing legacy documentation and scripts.
- Introduce comprehensive project templates, documentation, and operational runbooks, while updating GitHub issue templates and configuration files.
- Introduce minimal k3d cluster configuration, standardize k3d port mappings, and remove API reference from README.
- Add MetalLB configuration, update k3d cluster API exposure, and implement automated changelog generation using git-cliff.

### Changed

- Consolidate AI agent rules, introduce new project documentation, and update core repository files.
- Migrate local Kubernetes environment to k3d by removing previous infrastructure and application manifests and adding k3d cluster configuration.

### Documentation

- Update git commit message template
- **.github:** Update issue templates, policies, and repository config
- Update root repository assets and AI instruction guides
- Enhance README.md with badges, AI policy, and license info
- Comprehensive update to root README.md
- **.github:** Rename README.md to GITHUB_GUIDE.md
- Update AI agent rules and project documentation reference
- Add `CHANGELOG.md` and clear `CONTRIBUTING.md` content.
- Update AGENTS.md to use relative paths for all rule links.
- Add a comprehensive development workflow guide and instructions for installing pre-commit hook tools.

### Fixed

- **ci:** Format shell scripts and add missing psscriptanalyzer script
- **ci:** Fix psscriptanalyzer parameter binding
- **ci:** Iterate over files in psscriptanalyzer to avoid type mismatch
- **ci:** Silence powershell lint warnings in dev-tools
- **ci:** Fix powershell suppression syntax
- **ci:** Suppress write-host warning in psscriptanalyzer script

### Miscellaneous

- Remove inline comments from Renovate configuration.
- **deps:** Update helm release kube-prometheus-stack to v66.7.1
- **agent:** Consolidate AI agent rules into structured .agent/rules directory
- **agent:** Ignore .agent/rules and stop tracking contents
- **agent:** Ignore .agent/rules and stop tracking contents
- Update gitignore and add documentation issue template
- **project:** Standardize project metadata, assets and documentation
- **deps:** Bump DavidAnson/markdownlint-cli2-action from 16 to 22
- **deps:** Bump actions/stale from 9 to 10
- **deps:** Bump actions/labeler from 5 to 6
- **deps:** Bump actions/checkout from 4 to 6
- **deps:** Bump kindest/node from v1.28.0 to v1.35.0
- Add Zizmor configuration to disable unpinned-uses rule
- Migrate markdown linter pre-commit hook to `markdownlint-cli` and add `.markdownlintignore` for path exclusions.
- **deps:** Bump actions/checkout from 4 to 6
- **deps:** Bump actions/setup-go from 5 to 6
- **deps:** Bump actions/setup-python from 5 to 6
- **deps:** Bump DavidAnson/markdownlint-cli2-action from 16 to 22
- Remove explicit control-plane node image version from Kind configuration.

### Ci

- Add GitHub Actions workflow for markdown linting, actionlint, and Kubernetes manifest validation.


