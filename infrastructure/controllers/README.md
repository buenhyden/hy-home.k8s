# Controllers Infrastructure

Platform controllers that provide core Kubernetes functionality: service mesh and load balancing.

## Components

### Istio Service Mesh

- **istio-base**: Istio base charts with CRDs
- **istio-istiod**: Istio control plane (istiod)
- **istio-gateway**: Istio ingress gateway

### MetalLB

- **metallb**: Load balancer for bare metal/local Kubernetes

## Istio Configuration

### Version

- **Istio**: v1.24.0
- **Chart**: istio/base, istio/istiod, istio/gateway

### Components

#### istio-base

**Purpose**: Install Istio Custom Resource Definitions (CRDs)

**Namespace**: `istio-system`

**Key Resources**:

- Istio CRDs (VirtualService, Gateway, DestinationRule, ServiceEntry, etc.)

**Deployment**:

```bash
kubectl apply -k infrastructure/controllers/istio-base
```

#### istio-istiod

**Purpose**: Istio control plane that manages configuration and certificate distribution

**Namespace**: `istio-system`

**Key Configuration**:

```yaml
pilot:
  autoscaleEnabled: true
  resources:
    requests:
      cpu: 100m
      memory: 256Mi
```

**Features Enabled**:

- mTLS for all services
- Traffic management
- Distributed tracing integration
- Metrics collection

**Access Istiod**:

```bash
kubectl get pods -n istio-system -l app=istiod
kubectl logs -n istio-system -l app=istiod
```

#### istio-gateway

**Purpose**: Ingress gateway for external traffic

**Namespace**: `istio-system`

**Service Type**: LoadBalancer (MetalLB assigns IP from pool)

**Key Configuration**:

```yaml
service:
  type: LoadBalancer
  ports:
    - name: http
      port: 80
    - name: https
      port: 443
```

**Access Gateway**:

```bash
# Get LoadBalancer IP
kubectl get svc -n istio-system istio-gateway

# Test connection
curl http://<GATEWAY-IP>
```

### Using Istio

#### Enable Sidecar Injection

Label namespace for automatic sidecar injection:

```bash
kubectl label namespace default istio-injection=enabled
```

#### Create VirtualService

Route traffic to your application:

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-app
spec:
  hosts:
    - my-app
  http:
    - route:
        - destination:
            host: my-app
            port:
              number: 8000
```

#### Create Gateway

Expose service externally:

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: my-gateway
  namespace: istio-system
spec:
  selector:
    istio: gateway
  servers:
    - port:
        number: 80
        name: http
        protocol: HTTP
      hosts:
        - "*"
```

## MetalLB Configuration

### Purpose

Provides LoadBalancer IPs for services in local/bare metal Kubernetes clusters.

### Namespace

`metallb-system`

### IP Address Pool

**Range**: 172.18.255.200-250

**Configuration**:

```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: first-pool
  namespace: metallb-system
spec:
  addresses:
    - 172.18.255.200-172.18.255.250
```

**L2Advertisement**:

```yaml
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: l2-advert
  namespace: metallb-system
spec:
  ipAddressPools:
    - first-pool
```

### Using MetalLB

Create a LoadBalancer service:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 8000
  selector:
    app: my-app
```

Check assigned IP:

```bash
kubectl get svc my-service
# EXTERNAL-IP column shows assigned IP from pool
```

## Deployment Order

The controllers are deployed in this order:

1. **istio-base** - CRDs must be installed first
2. **istio-istiod** - Control plane depends on CRDs
3. **istio-gateway** - Gateway depends on control plane
4. **metallb** - Can be deployed anytime, but gateway needs it

## Troubleshooting

### Istio Not Working

**Check istiod**:

```bash
kubectl get pods -n istio-system
kubectl logs -n istio-system deployment/istiod
```

**Verify sidecars are injected**:

```bash
kubectl get pods -o jsonpath='{.items[*].spec.containers[*].name}'
# Should see 'istio-proxy' alongside your app container
```

**Check VirtualService**:

```bash
kubectl get virtualservice
kubectl describe virtualservice my-app
```

### MetalLB Not Assigning IPs

**Check MetalLB pods**:

```bash
kubectl get pods -n metallb-system
kubectl logs -n metallb-system -l app=metallb
```

**Verify IP pool**:

```bash
kubectl get ipaddresspool -n metallb-system
kubectl get l2advertisement -n metallb-system
```

**Check service**:

```bash
kubectl describe svc my-service
# Look for Events related to LoadBalancer provisioning
```

### mTLS Issues

**Verify mTLS policy**:

```bash
kubectl get peerauthentication --all-namespaces
```

**Check certificates**:

```bash
istioctl proxy-config secret <pod-name> -n <namespace>
```

## Access and Testing

### Istio Dashboard

```bash
# Install Kiali (if not already installed)
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.24/samples/addons/kiali.yaml

# Port-forward
kubectl port-forward -n istio-system svc/kiali 20001:20001

# Visit http://localhost:20001
```

### Istio Metrics

```bash
# Prometheus (if Prometheus stack is installed)
kubectl port-forward -n observability svc/kube-prometheus-stack-prometheus 9090:9090

# Query Istio metrics:
# istio_requests_total
# istio_request_duration_milliseconds
```

## Best Practices

1. **Always use mTLS**: Keep default STRICT mode
2. **Namespace isolation**: Use separate namespaces for apps
3. **Resource limits**: Set limits for istiod to prevent resource exhaustion
4. **Monitor metrics**: Use Grafana dashboards for Istio metrics
5. **Test before production**: Validate VirtualService routing in dev

## Upgrading

### Upgrade Istio

```bash
# 1. Upgrade CRDs (istio-base)
kubectl apply -k infrastructure/controllers/istio-base

# 2. Upgrade control plane (istio-istiod)
kubectl apply -k infrastructure/controllers/istio-istiod

# 3. Restart pods to get new sidecar version
kubectl rollout restart deployment -n <namespace>
```

### Upgrade MetalLB

```bash
kubectl apply -k infrastructure/controllers/metallb
```

## References

- [Istio Documentation](https://istio.io/latest/docs/)
- [MetalLB Documentation](https://metallb.universe.tf/)
- [Istio VirtualService Reference](https://istio.io/latest/docs/reference/config/networking/virtual-service/)
- [MetalLB Configuration](https://metallb.universe.tf/configuration/)
