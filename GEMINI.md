# Gemini Developer Guide

Guidelines for interacting with Gemini in the context of `hy-home.k8s`.

## Project Context

- **Name**: hy-home.k8s
- **Platform**: GitOps-based Kubernetes Infrastructure
- **Core Tools**: Kind, ArgoCD, Istio, Prometheus, Grafana, PostgreSQL, Redis

## Instructions for Gemini

- **Code Reasoning**: Leverage Gemini's reasoning capabilities for complex infrastructure logic and networking configurations.
- **Multimodal Context**: Use Gemini to analyze architecture diagrams (Mermaid) and provide feedback.
- **Documentation Quality**: Ensure that generated documentation is as detailed and accurate as the existing READMEs in the project.
- **Tooling Awareness**: Gemini should be aware of the custom scripts and tools located in the `bootstrap/` and `infrastructure/` directories.
- **Compliance**: Verify that all changes comply with the project's security and policy standards (Kyverno).
