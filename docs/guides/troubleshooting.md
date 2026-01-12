# Troubleshooting Guide

Common issues and solutions for the hy-home.k8s platform.

## Bootstrap Issues

### Kind Cluster Creation Fails

**Problem**: `kind create cluster` fails

**Solutions:**

1. Check Docker is running:

   ```bash
   docker ps
   ```

2. Delete existing cluster:

   ```bash
   kind delete cluster --name docker-desktop
   kind create cluster --config kind-config.yaml --name docker-desktop
   ```

3. Check Docker resources (Settings → Resources):
   - CPU: Min 4 cores
   - Memory: Min 8GB

### ArgoCD Pods Not Starting

**Problem**: ArgoCD pods stuck in Pending or CrashLoopBackOff

**Check:**

```bash
kubectl get pods -n argocd
kubectl describe pod <pod-name> -n argocd
```

**Common causes:**

- Insufficient resources: Increase Docker memory
- Image pull timeout: Wait longer or check internet
- Port conflicts: Check no other process using 8080

**Solution:**

```bash
# Delete and reinstall
kubectl delete namespace argocd
./bootstrap/argocd-install.sh
```

## Networking Issues

### Cannot Access External Services

**Problem**: Pods can't connect to PostgreSQL/Redis (172.19.0.x)

**Verify routing:**

```bash
docker exec -it docker-desktop-worker ip route
# Should show: 172.19.0.0/16 via 172.18.0.1
```

**Fix:**

```bash
GATEWAY=$(docker network inspect infra_net --format "{{(index .IPAM.Config 0).Gateway}}")

docker exec -it docker-desktop-control-plane ip route add 172.19.0.0/16 via $GATEWAY
docker exec -it docker-desktop-worker ip route add 172.19.0.0/16 via $GATEWAY
docker exec -it docker-desktop-worker2 ip route add 172.19.0.0/16 via $GATEWAY
docker exec -it docker-desktop-worker3 ip route add 172.19.0.0/16 via $GATEWAY
```

### MetalLB LoadBalancer Stuck Pending

**Problem**: Service type=LoadBalancer shows EXTERNAL-IP as `<pending>`

**Check:**

```bash
kubectl get pods -n metallb-system
kubectl get ipaddresspool -n metallb-system
kubectl get l2advertisement -n metallb-system
```

**Solution:**

```bash
# Restart MetalLB
kubectl rollout restart deployment controller -n metallb-system
kubectl rollout restart daemonset speaker -n metallb-system
```

### Istio Gateway Not Accessible

**Problem**: Can't access services through Istio Gateway

**Check Gateway IP:**

```bash
kubectl get svc -n istio-system istio-gateway
```

**Test connectivity:**

```bash
GATEWAY_IP=$(kubectl get svc -n istio-system istio-gateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl http://$GATEWAY_IP
```

**Check VirtualService:**

```bash
kubectl get virtualservice -A
kubectl describe virtualservice <name> -n <namespace>
```

## ArgoCD Issues

### Application Stuck in "Progressing"

**Problem**: Application shows Progressing for >10 minutes

**Check resource status:**

```bash
kubectl get application <app-name> -n argocd -o yaml
```

**Common causes:**

- Large Helm chart (Prometheus): Wait 10-15 minutes
- Image pull: Check `kubectl get pods -A` for ImagePullBackOff
- Resource limits: Check node resources

**Force sync:**

```bash
kubectl patch application <app-name> -n argocd \
  --type merge -p '{"operation":{"sync":{"revision":"HEAD"}}}'
```

### Application Shows "OutOfSync"

**Problem**: Application status is OutOfSync

**Reasons:**

- Manual kubectl changes (expected - self-heal will fix)
- Git has newer changes (sync incoming)
- Kustomize build error

**Solutions:**

```bash
# View diff
kubectl get application <app-name> -n argocd -o yaml

# Manual sync
argocd app sync <app-name>

# Or via kubectl
kubectl patch application <app-name> -n argocd \
  --type merge -p '{"operation":{"initiatedBy":{"username":"admin"},"sync":{"revision":"HEAD"}}}'
```

### Can't Access ArgoCD UI

**Problem**: <https://localhost:8080> not accessible

**Check port-forward:**

```bash
# Kill existing
pkill -f "port-forward.*argocd"

# Restart
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

**Get admin password:**

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

## Application Deployment Issues

### Pods CrashLoopBackOff

**Check logs:**

```bash
kubectl logs <pod-name> -n <namespace>

# With Istio sidecar
kubectl logs <pod-name> -n <namespace> -c app
```

**Common causes:**

1. **Missing environment variables**
   - Check secret exists: `kubectl get secret <app>-secrets`

2. **Database connection failure**
   - Test: `kubectl exec -it <pod> -- ping postgres-external`

3. **Port already in use**
   - Check containerPort in rollout.yaml

### Image Pull Errors

**Problem**: `ImagePullBackOff` or `ErrImagePull`

**Check:**

```bash
kubectl describe pod <pod-name>
```

**Solutions:**

1. Verify image exists:

   ```bash
   docker pull <image>:<tag>
   ```

2. For private registries, create pull secret:

   ```bash
   kubectl create secret docker-registry ghcr-secret \
     --docker-server=ghcr.io \
     --docker-username=<username> \
     --docker-password=<token>
   ```

3. Add to rollout.yaml:

   ```yaml
   spec:
     template:
       spec:
         imagePullSecrets:
           - name: ghcr-secret
   ```

### Rollout Fails Canary

**Problem**: Argo Rollout stuck or failed during canary

**Check rollout:**

```bash
kubectl argo rollouts get rollout <name>
kubectl argo rollouts status <name>
```

**Abort and rollback:**

```bash
kubectl argo rollouts abort <name>
kubectl argo rollouts undo <name>
```

**Common issues:**

- Metrics unavailable: Check Prometheus
- Analysis failed: Check AnalysisTemplate
- Manual pause: Use `kubectl argo rollouts promote <name>`

## Kyverno Policy Violations

### Blocked by "latest" Tag Policy

**Error**: `Using a mutable image tag e.g. 'latest' is not allowed`

**Solution**: Use specific version tags

```yaml
# ❌ Bad
image: myapp:latest

# ✅ Good
image: myapp:v1.2.3
image: myapp:sha-abc123
```

### Blocked by Non-Root Policy

**Error**: `Running as root is not allowed`

**Solution**: Add securityContext

```yaml
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
        - name: app
          securityContext:
            allowPrivilegeEscalation: false
```

## Observability Issues

### Prometheus Not Scraping

**Check targets:**

```bash
kubectl port-forward -n observability svc/kube-prometheus-stack-prometheus 9090:9090
# Visit http://localhost:9090/targets
```

**Verify ServiceMonitor:**

```bash
kubectl get servicemonitor -A
```

### Can't Access Grafana

**Port-forward:**

```bash
kubectl port-forward -n observability svc/kube-prometheus-stack-grafana 3000:80
```

**Get password:**

```bash
kubectl get secret -n observability kube-prometheus-stack-grafana \
  -o jsonpath="{.data.admin-password}" | base64 -d
```

### Logs Not Appearing in Loki

**Check Alloy:**

```bash
kubectl get pods -n observability -l app.kubernetes.io/name=alloy
kubectl logs -n observability <alloy-pod>
```

**Verify Loki ingestion:**

```bash
kubectl port-forward -n observability svc/loki 3100:3100
curl http://localhost:3100/ready
```

## Performance Issues

### High CPU Usage

**Identify resource hogs:**

```bash
kubectl top nodes
kubectl top pods -A --sort-by=cpu
```

**Solutions:**

- Increase CPU limits
- Enable HPA for auto-scaling
- Check for resource leaks

### High Memory Usage

**Check:**

```bash
kubectl top pods -A --sort-by=memory
kubectl describe node <node-name>
```

**Solutions:**

- Increase memory limits
- Check for memory leaks (restart pods)
- Reduce replica count if over-provisioned

### Slow Deployments

**Common causes:**

1. Large images: Use multi-stage builds
2. Slow image pull: Use image caching
3. Resource contention: Increase node resources

## Data Issues

### Secrets Not Decrypting

**Problem**: SealedSecret exists but Secret not created

**Check controller:**

```bash
kubectl get pods -n kube-system -l name=sealed-secrets-controller
kubectl logs -n kube-system <sealed-secrets-pod>
```

**Verify SealedSecret:**

```bash
kubectl get sealedsecret <name> -o yaml
kubectl get secret <name>  # Should exist
```

### ConfigMap Not Loading

**Check:**

```bash
kubectl get configmap <name> -o yaml
```

**Force pod restart:**

```bash
kubectl rollout restart deployment/<name>
```

## Diagnostic Commands

### General Health Check

```bash
# All pods
kubectl get pods -A | grep -v Running

# All applications
kubectl get applications -n argocd

# Node status
kubectl get nodes

# Events
kubectl get events -A --sort-by='.lastTimestamp' | tail -20
```

### Detailed Pod Debugging

```bash
# Describe pod
kubectl describe pod <pod-name> -n <namespace>

# Logs
kubectl logs <pod-name> -n <namespace> --previous
kubectl logs <pod-name> -c <container> -n <namespace>

# Execute commands
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh

# Check DNS
kubectl exec -it <pod-name> -n <namespace> -- nslookup kubernetes.default
```

### Network Debugging

```bash
# Test service DNS
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup <service-name>

# Test connectivity
kubectl run -it --rm debug --image=busybox --restart=Never -- wget -O- http://<service>:<port>

# Check Istio sidecar
kubectl exec -it <pod-name> -n <namespace> -c istio-proxy -- curl localhost:15000/config_dump
```

## Getting Help

If none of these solutions work:

1. **Check logs**: `kubectl logs` for the failing component
2. **Check events**: `kubectl get events -A --sort-by='.lastTimestamp'`
3. **Review docs**: See [documentation index](../README.md)
4. **GitHub Issues**: [Create an issue](https://github.com/buenhyden/hy-home.k8s/issues)

## Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| Pods pending | Check resources: `kubectl top nodes` |
| ImagePullBackOff | Verify image exists, check pull secrets |
| CrashLoopBackOff | Check logs: `kubectl logs <pod>` |
| Service unreachable | Check ingress/gateway configuration |
| ArgoCD out of sync | Manual sync or wait for auto-sync |
| High resource usage | Enable HPA or increase limits |
