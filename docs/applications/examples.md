# Examples & Templates

To speed up development, `hy-home.k8s` provides templates and examples.

## 1. Templates (`apps/_templates`)

The `_templates` directory contains "Base" Kustomize configurations that abstract away common boilerplate (Service, Deployment, Ingress).

- **`base-app`**: A standard stateless generic application.
- **`manifests`**: Raw yaml files used by bases.

### Usage

In your application's `kustomization.yaml`:

```yaml
resources:
  - ../../../_templates/base-app

namespace: my-app

namePrefix: my-app-

patches:
  - path: deployment-patch.yaml
```

## 2. Examples (`apps/_examples`)

Reference implementations showing how to use the templates.

- **`podinfo`**: A Go application showing full feature set (Probes, UI, API).
- **`redis`**: Example of a specific persistent stateful application.

### Deploying an Example

To deploy the `podinfo` example:

1. Create a `Application` manifest in `clusters/docker-desktop/apps/`.
2. Point the `source.path` to `apps/_examples/podinfo`.
3. Commit and Sync.

*Note: For production apps, copy the pattern, don't link directly to `_examples` which might change.*
