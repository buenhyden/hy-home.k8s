# Security Infrastructure

Security components for policy enforcement, certificate management, and secrets encryption.

## Components

- **kyverno**: Policy engine for Kubernetes
- **cert-manager**: Automated certificate management
- **sealed-secrets**: Encrypted secrets for GitOps

## Kyverno

### Purpose

Policy engine that validates, mutates, and generates Kubernetes resources.

### Version

- **Chart**: kyverno/kyverno v3.2.0
- **Kyverno**: v1.12.0

### Namespace

`kyverno`

### Key Policies

#### Block Latest Tag

Prevents using `:latest` image tags in production:

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-latest-tag
spec:
  validationFailureAction: Enforce
  rules:
    - name: require-image-tag
      match:
        resources:
          kinds:
            - Pod
      validate:
        message: "Using 'latest' tag is not allowed"
        pattern:
          spec:
            containers:
              - image: "!*:latest"
```

#### Require Non-Root

Enforces containers run as non-root users:

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-run-as-non-root
spec:
  validationFailureAction: Enforce
  rules:
    - name: check-runAsNonRoot
      match:
        resources:
          kinds:
            - Pod
      validate:
        message: "Containers must run as non-root"
        pattern:
          spec:
            securityContext:
              runAsNonRoot: true
```

#### Require Resource Limits

Ensures all containers have resource limits:

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resource-limits
spec:
  validationFailureAction: Enforce
  rules:
    - name: check-limits
      match:
        resources:
          kinds:
            - Pod
      validate:
        message: "Resource limits must be defined"
        pattern:
          spec:
            containers:
              - resources:
                  limits:
                    memory: "?*"
                    cpu: "?*"
```

### Using Kyverno

**Check policy reports**:

```bash
kubectl get policyreport -A
kubectl describe policyreport -n default
```

**Test policy locally**:

```bash
# Install kyverno CLI
kubectl kyverno apply policy.yaml --resource resource.yaml
```

### Troubleshooting

**Policy not applying**:

```bash
kubectl get clusterpolicy
kubectl describe clusterpolicy disallow-latest-tag
```

**Check Kyverno logs**:

```bash
kubectl logs -n kyverno -l app.kubernetes.io/name=kyverno
```

## Cert-Manager

### Purpose

Automates certificate issuance and renewal from various sources (Let's Encrypt, self-signed, etc.).

### Version

- **Chart**: jetstack/cert-manager v1.16.0
- **Cert-Manager**: v1.16.0

### Namespace

`cert-manager`

### Components

1. **cert-manager-controller**: Main controller
2. **cert-manager-webhook**: Validates CRDs
3. **cert-manager-cainjector**: Injects CA bundles

### Certificate Issuers

#### Self-Signed Issuer

For development:

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned-issuer
spec:
  selfSigned: {}
```

#### Let's Encrypt (Production)

For production TLS certificates:

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
      - http01:
          ingress:
            class: istio
```

### Requesting Certificates

**Create Certificate resource**:

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: my-app-tls
  namespace: default
spec:
  secretName: my-app-tls-secret
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
    - my-app.example.com
```

**Use in Istio Gateway**:

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: my-gateway
spec:
  selector:
    istio: gateway
  servers:
    - port:
        number: 443
        name: https
        protocol: HTTPS
      tls:
        mode: SIMPLE
        credentialName: my-app-tls-secret
      hosts:
        - my-app.example.com
```

### Troubleshooting

**Certificate not ready**:

```bash
kubectl get certificate -n default
kubectl describe certificate my-app-tls -n default
```

**Check certificate request**:

```bash
kubectl get certificaterequest -n default
kubectl describe certificaterequest <request-name> -n default
```

**Check cert-manager logs**:

```bash
kubectl logs -n cert-manager -l app=cert-manager
kubectl logs -n cert-manager -l app=webhook
```

## Sealed Secrets

### Purpose

Allows storing encrypted k8s secrets safely in Git, then decrypts them in-cluster.

### Version

- **Chart**: sealed-secrets/sealed-secrets v2.16.0
- **Kubeseal**: v0.27.0

### Namespace

`kube-system`

### How It Works

1. Sealed Secrets controller generates encryption keypair
2. You encrypt secrets using `kubeseal` CLI with controller's public key
3. Commit encrypted `SealedSecret` to Git
4. Controller decrypts and creates standard Kubernetes `Secret`

### Installing kubeseal CLI

```bash
# macOS
brew install kubeseal

# Linux
wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.27.0/kubeseal-0.27.0-linux-amd64.tar.gz
tar -xvzf kubeseal-0.27.0-linux-amd64.tar.gz
sudo install -m 755 kubeseal /usr/local/bin/kubeseal
```

### Creating Sealed Secrets

**Step 1**: Create plain secret YAML:

```bash
kubectl create secret generic my-secret \
  --from-literal=username=admin \
  --from-literal=password=supersecret \
  --dry-run=client -o yaml > secret.yaml
```

**Step 2**: Encrypt with kubeseal:

```bash
kubeseal < secret.yaml > sealed-secret.yaml
```

**Step 3**: Commit to Git:

```bash
git add sealed-secret.yaml
git commit -m "feat: add my-secret sealed secret"
git push
```

**Step 4**: Apply via GitOps:

```bash
# ArgoCD will auto-sync, or manual apply:
kubectl apply -f sealed-secret.yaml
```

### Using Sealed Secrets

The decrypted secret is used like any other secret:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  containers:
    - name: app
      image: my-app:latest
      env:
        - name: USERNAME
          valueFrom:
            secretKeyRef:
              name: my-secret
              key: username
        - name: PASSWORD
          valueFrom:
            secretKeyRef:
              name: my-secret
              key: password
```

### Backup and Restore

**Backup controller keys** (IMPORTANT):

```bash
kubectl get secret -n kube-system \
  -l sealedsecrets.bitnami.com/sealed-secrets-key=active \
  -o yaml > sealed-secrets-keys-backup.yaml

# Store securely (e.g., encrypted vault)
```

**Restore keys** (e.g., new cluster):

```bash
kubectl apply -f sealed-secrets-keys-backup.yaml
kubectl delete pod -n kube-system -l app.kubernetes.io/name=sealed-secrets
```

### Troubleshooting

**SealedSecret not decrypting**:

```bash
kubectl get sealedsecret
kubectl describe sealedsecret my-secret
```

**Check controller logs**:

```bash
kubectl logs -n kube-system -l app.kubernetes.io/name=sealed-secrets
```

**Verify secret created**:

```bash
kubectl get secret my-secret
```

## Best Practices

### Kyverno

1. **Start with Audit mode**: Test policies before enforcing
2. **Exclude system namespaces**: Avoid blocking critical system pods
3. **Use policy reports**: Monitor violations before enforcement
4. **Gradual rollout**: Apply new policies to a few namespaces first

### Cert-Manager

1. **Use staging issuer first**: Test with Let's Encrypt staging before production
2. **Monitor certificate expiry**: Set up alerts for certificates expiring soon
3. **Backup certificates**: Export critical TLS certificates
4. **Rate limits**: Be aware of Let's Encrypt rate limits (50 certs/domain/week)

### Sealed Secrets

1. **Backup encryption keys**: Store controller keys securely
2. **Rotate secrets regularly**: Update and re-seal secrets periodically
3. **Namespace scoping**: Scope secrets to specific namespaces
4. **Never commit plain secrets**: Always encrypt before committing to Git

## Security Checklist

- [ ] All pods run as non-root (Kyverno policy)
- [ ] Image tags are specific versions, not `:latest` (Kyverno policy)
- [ ] Resource limits defined for all containers (Kyverno policy)
- [ ] TLS certificates managed via cert-manager
- [ ] Secrets encrypted with Sealed Secrets before committing to Git
- [ ] Sealed Secrets encryption keys backed up
- [ ] Regular secret rotation schedule established

## Accessing Services

```bash
# Kyverno policy reports
kubectl get policyreport -A

# Cert-Manager certificates
kubectl get certificate -A
kubectl get certificaterequest -A

# Sealed Secrets
kubectl get sealedsecret -A
```

## References

- [Kyverno Documentation](https://kyverno.io/)
- [Kyverno Policies Library](https://kyverno.io/policies/)
- [Cert-Manager Documentation](https://cert-manager.io/docs/)
- [Sealed Secrets GitHub](https://github.com/bitnami-labs/sealed-secrets)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
