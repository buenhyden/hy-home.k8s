# PULL REQUEST TEMPLATE

## 1. Description

A clear and concise description of the changes being proposed.

## 2. Related Issue

Fixes # (link to issue if applicable)

## 3. Type of Change

- [ ] `feat`: New feature or enhancement
- [ ] `fix`: Bug fix
- [ ] `refactor`: Code reorganization
- [ ] `docs`: Documentation updates
- [ ] `infra`: Changes to kubernetes manifests

## 4. Breaking Changes

- [ ] Yes
- [ ] No

If yes, please describe the impact and migration path.

## 5. How Has This Been Tested?

Describe the manual verification or automated tests conducted.

- [ ] `kubectl apply --dry-run=client` successful
- [ ] `kustomize build` successful
- [ ] ArgoCD sync status verified (if applicable)

## 6. Checklist

- [ ] My code follows the [Naming Conventions](../../docs/standards/naming-conventions.md).
- [ ] I have updated the documentation accordingly.
- [ ] My commit messages follow the [Conventional Commits](../../.gitmessage.json).
- [ ] (Security) Any new secrets have been encrypted with [Sealed Secrets](../../docs/guides/secret-management.md).
