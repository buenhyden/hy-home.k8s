# Gemini Developer Guide

Guidelines for interacting with Gemini (Antigravity) in `hy-home.k8s`.

## Project Context

- **Name**: hy-home.k8s
- **Type**: GitOps Kubernetes Platform
- **Core Components**: Kind, ArgoCD, Istio, Observability Stack

## Instructions for Gemini

### Workflow & Task Management

- **Task Mode**: ALWAYS use `task_boundary` for complex sets of actions.
- **Tracking**: Maintain `task.md` dutifully.
- **Workflows**: Check `.agent/workflows/` before inventing new processes.

### Navigation & Reasoning

- **Deep Dives**: When debugging, you are encouraged to look into `infrastructure/` helm charts.
- **Diagrams**: Use Mermaid to visualize complex network or resource relationships.
- **Bootstrapping**: Understand `bootstrap/` scripts to know how the cluster is built.

### Documentation

- **Quality**: Documentation you write must be on par with manually written docs.
- **Accuracy**: Verify paths and commands.
