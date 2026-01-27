# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-05-20

### Added

- **Bootstrap Scripts**: Automated `cluster-setup.sh`, `argocd-install.sh`, and `root-apps.sh` for easy initialization.
- **Documentation**: Comprehensive structure in `docs/` covering Guides, Infrastructure, Applications, Lifecycle, and Standards.
- **Infrastructure**: Core controllers (Ingress Nginx, MetalLB, Istio) and Observability Stack (LGTM).
- **CI/CD**: GitOps workflow powered by ArgoCD.
- **Security**: Policy enforcement with Kyverno and secret management with Sealed Secrets.
