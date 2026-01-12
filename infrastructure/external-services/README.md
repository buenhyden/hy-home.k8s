# External Services Infrastructure

Kubernetes connectors for external services running in Docker (PostgreSQL, Redis, Kafka, OpenSearch).

## Overview

This directory contains Kubernetes resources that allow pods to communicate with external services running in Docker containers outside the cluster.

**Network Architecture**:

- **Kind Cluster**: 172.18.0.0/16
- **External Services**: 172.19.0.0/16 (Docker network)
- **Connectivity**: Headless Services + Static Endpoints

## Components

- **postgres**: PostgreSQL connector (Patroni HA cluster)
- **redis**: Redis connector (6-node cluster)
- **kafka**: Apache Kafka connector
- **opensearch**: OpenSearch connector

## How It Works

### 1. Headless Service

Creates a service without a ClusterIP:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres-external
  namespace: default
spec:
  clusterIP: None  # Headless
  ports:
    - port: 15432
      targetPort: 15432
```

### 2. Static Endpoints

Points to the Docker container IP:

```yaml
apiVersion: v1
kind: Endpoints
metadata:
  name: postgres-external
  namespace: default
subsets:
  - addresses:
      - ip: 172.19.0.56  # PostgreSQL Docker IP
    ports:
      - port: 15432
```

### 3. Application Usage

Applications connect using the service name:

```python
# PostgreSQL connection
DATABASE_URL = "postgresql://user:pass@postgres-external:15432/mydb"
```

## PostgreSQL

### Configuration

**Service Name**: `postgres-external`

**Port**: 15432

**Docker IP**: 172.19.0.56

**High Availability**: Patroni 3-node cluster

### Connection Details

**From Kubernetes**:

```yaml
env:
  - name: DATABASE_URL
    value: "postgresql://postgres:password@postgres-external:15432/mydb"
```

**Python Example**:

```python
import psycopg2

conn = psycopg2.connect(
    host="postgres-external",
    port=15432,
    database="mydb",
    user="postgres",
    password="password"
)
```

**Node.js Example**:

```javascript
const { Pool } = require('pg');

const pool = new Pool({
  host: 'postgres-external',
  port: 15432,
  database: 'mydb',
  user: 'postgres',
  password: 'password'
});
```

### Testing Connection

```bash
# Deploy test pod
kubectl run psql-test --image=postgres:15 -it --rm -- bash

# Inside pod
psql -h postgres-external -p 15432 -U postgres -d mydb
```

## Redis

### Configuration

**Service Name**: `redis-external`

**Port**: 16379

**Docker IP Range**: 172.19.0.60-65

**Cluster**: 6 nodes (3 masters, 3 replicas)

### Connection Details

**From Kubernetes**:

```yaml
env:
  - name: REDIS_URL
    value: "redis://redis-external:16379"
```

**Python Example**:

```python
import redis

# Single node connection
r = redis.Redis(
    host='redis-external',
    port=16379,
    decode_responses=True
)

# Cluster connection
from redis.cluster import RedisCluster
rc = RedisCluster(
    host='redis-external',
    port=16379
)
```

**Node.js Example**:

```javascript
const Redis = require('ioredis');

const redis = new Redis({
  host: 'redis-external',
  port: 16379
});
```

### Testing Connection

```bash
# Deploy test pod
kubectl run redis-test --image=redis:7 -it --rm -- bash

# Inside pod
redis-cli -h redis-external -p 16379 ping
```

## Kafka

### Configuration

**Service Name**: `kafka-external`

**Port**: 19092

**Docker IP**: 172.19.0.70

### Connection Details

**From Kubernetes**:

```yaml
env:
  - name: KAFKA_BROKERS
    value: "kafka-external:19092"
```

**Python Example**:

```python
from kafka import KafkaProducer, KafkaConsumer

# Producer
producer = KafkaProducer(
    bootstrap_servers=['kafka-external:19092']
)

# Consumer
consumer = KafkaConsumer(
    'my-topic',
    bootstrap_servers=['kafka-external:19092'],
    group_id='my-group'
)
```

**Java/Spring Example**:

```yaml
spring:
  kafka:
    bootstrap-servers: kafka-external:19092
```

### Testing Connection

```bash
# Deploy Kafka client pod
kubectl run kafka-test --image=confluentinc/cp-kafka:latest -it --rm -- bash

# Inside pod
kafka-topics --bootstrap-server kafka-external:19092 --list
```

## OpenSearch

### Configuration

**Service Name**: `opensearch-external`

**Port**: 19200

**Docker IP**: 172.19.0.80

### Connection Details

**From Kubernetes**:

```yaml
env:
  - name: OPENSEARCH_URL
    value: "http://opensearch-external:19200"
```

**Python Example**:

```python
from opensearchpy import OpenSearch

client = OpenSearch(
    hosts=[{'host': 'opensearch-external', 'port': 19200}],
    http_auth=('admin', 'admin'),
    use_ssl=False
)
```

**cURL Example**:

```bash
curl -u admin:admin http://opensearch-external:19200/_cat/health
```

### Testing Connection

```bash
# Deploy test pod
kubectl run opensearch-test --image=curlimages/curl -it --rm -- sh

# Inside pod
curl -u admin:admin http://opensearch-external:19200
```

## Egress Policy

Istio egress policy allows traffic to external services:

**File**: `egress-policy.yaml`

```yaml
apiVersion: networking.istio.io/v1beta1
kind: ServiceEntry
metadata:
  name: external-postgres
  namespace: default
spec:
  hosts:
    - postgres-external
  addresses:
    - 172.19.0.56
  ports:
    - number: 15432
      name: postgres
      protocol: TCP
  location: MESH_EXTERNAL
  resolution: STATIC
  endpoints:
    - address: 172.19.0.56
```

## Troubleshooting

### Connection Refused

**Check Docker container is running**:

```bash
docker ps | grep postgres
docker ps | grep redis
```

**Check container IP**:

```bash
docker inspect <container-name> | grep IPAddress
```

**Update endpoints if IP changed**:

```bash
kubectl edit endpoints postgres-external
```

### DNS Resolution

**Test from pod**:

```bash
kubectl run test --image=busybox -it --rm -- sh
nslookup postgres-external
ping postgres-external
```

### Network Connectivity

**Test connection**:

```bash
kubectl run test --image=busybox -it --rm -- sh
nc -zv postgres-external 15432
nc -zv redis-external 16379
```

**Check routes** (from Kind node):

```bash
docker exec kind-control-plane ip route | grep 172.19
```

### Istio Sidecar Issues

If using Istio sidecar injection, verify ServiceEntry:

```bash
kubectl get serviceentry
kubectl describe serviceentry external-postgres
```

## Adding New External Service

### Step 1: Create Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service-external
  namespace: default
spec:
  clusterIP: None
  ports:
    - port: <service-port>
```

### Step 2: Create Endpoints

```yaml
apiVersion: v1
kind: Endpoints
metadata:
  name: my-service-external
  namespace: default
subsets:
  - addresses:
      - ip: <docker-container-ip>
    ports:
      - port: <service-port>
```

### Step 3: Add ServiceEntry (if using Istio)

```yaml
apiVersion: networking.istio.io/v1beta1
kind: ServiceEntry
metadata:
  name: external-my-service
  namespace: default
spec:
  hosts:
    - my-service-external
  addresses:
    - <docker-container-ip>
  ports:
    - number: <service-port>
      name: <protocol>
      protocol: TCP
  location: MESH_EXTERNAL
  resolution: STATIC
  endpoints:
    - address: <docker-container-ip>
```

### Step 4: Add to Kustomization

```yaml
# infrastructure/external-services/kustomization.yaml
resources:
  - my-service/service.yaml
  - my-service/endpoints.yaml
```

## Best Practices

1. **Use Secrets**: Store credentials in Kubernetes Secrets or Sealed Secrets
2. **Connection Pooling**: Configure appropriate connection pools in applications
3. **Health Checks**: Implement health checks for external services
4. **Monitoring**: Monitor connection metrics and errors
5. **Failover**: Leverage HA features (Patroni for PostgreSQL, Redis Cluster)

## Security Considerations

- **Network Isolation**: External services are on isolated Docker network
- **Access Control**: Use strong passwords and limit access
- **Encryption**: Enable TLS for production (PostgreSQL SSL, Redis TLS, etc.)
- **Secret Management**: Never hardcode credentials

## Connection Strings Reference

```bash
# PostgreSQL
postgresql://user:pass@postgres-external:15432/dbname

# Redis
redis://redis-external:16379

# Redis Cluster
redis://redis-external:16379?cluster=true

# Kafka
kafka-external:19092

# OpenSearch
http://opensearch-external:19200
```

## References

- [Istio ServiceEntry](https://istio.io/latest/docs/reference/config/networking/service-entry/)
- [Kubernetes Headless Services](https://kubernetes.io/docs/concepts/services-networking/service/#headless-services)
- [PostgreSQL Connection URIs](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)
- [Redis Connection](https://redis.io/docs/getting-started/)
- [Kafka Configuration](https://kafka.apache.org/documentation/#configuration)
