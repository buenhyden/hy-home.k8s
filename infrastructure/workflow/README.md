# Workflow Infrastructure

Apache Airflow for workflow orchestration and data pipeline management.

## Overview

Apache Airflow deployed on Kubernetes for scheduling and monitoring data workflows.

## Version

- **Chart**: apache-airflow/airflow v1.15.0
- **Airflow**: 2.9.0

## Namespace

`airflow`

## Components

1. **Webserver**: Airflow UI
2. **Scheduler**: Task scheduling and execution
3. **Worker**: Executes tasks (CeleryExecutor or KubernetesExecutor)
4. **PostgreSQL**: Metadata database
5. **Redis**: Message broker for Celery

## Architecture

```text
User → Webserver (UI) → Scheduler → Worker → Task Execution
                              ↓
                         PostgreSQL (Metadata)
                              ↓
                         Redis (Queue)
```

## Access Airflow UI

### Port-Forward

```bash
kubectl port-forward -n airflow svc/airflow-webserver 8080:8080
# Visit http://localhost:8080
```

### Default Credentials

- **Username**: `admin`
- **Password**: Retrieved via:

  ```bash
  kubectl get secret -n airflow airflow-webserver-secret \
    -o jsonpath="{.data.admin-password}" | base64 -d
  ```

## Configuration

### Executor

**Default**: `KubernetesExecutor`

With KubernetesExecutor, each task runs in its own pod, providing:

- Isolation
- Resource control per task
- No need for worker pods

**Alternative**: `CeleryExecutor` for persistent workers.

### DAGs

DAGs (Directed Acyclic Graphs) define workflows.

**DAG Location**: `/opt/airflow/dags/`

**Deployment Methods**:

#### 1. Git-Sync (Recommended)

Configure git-sync to pull DAGs from Git:

```yaml
dags:
  gitSync:
    enabled: true
    repo: https://github.com/yourorg/airflow-dags.git
    branch: main
    subPath: dags/
    wait: 60  # Sync interval in seconds
```

#### 2. ConfigMap

For small DAGs during testing:

```bash
kubectl create configmap my-dag --from-file=my_dag.py -n airflow
```

Then mount in webserver/scheduler:

```yaml
extraVolumes:
  - name: my-dag
    configMap:
      name: my-dag
extraVolumeMounts:
  - name: my-dag
    mountPath: /opt/airflow/dags/my_dag.py
    subPath: my_dag.py
```

## Creating DAGs

### Example DAG

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def hello_world():
    print("Hello from Airflow!")

with DAG(
    'hello_world_dag',
    default_args=default_args,
    description='Simple hello world DAG',
    schedule_interval='0 0 * * *',  # Daily at midnight
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:

    task1 = PythonOperator(
        task_id='hello_task',
        python_callable=hello_world,
    )
```

### DAG Best Practices

1. **Set start_date**: Use a specific date, not `datetime.now()`
2. **Use catchup=False**: Avoid backfilling unless needed
3. **Set appropriate retries**: Handle transient failures
4. **Tag your DAGs**: Organize with tags for filtering
5. **Document**: Add descriptions and docstrings

## Using External Services

### PostgreSQL Connection

```python
from airflow.providers.postgres.operators.postgres import PostgresOperator

postgres_task = PostgresOperator(
    task_id='query_postgres',
    postgres_conn_id='postgres_default',
    sql='SELECT COUNT(*) FROM users;',
)
```

**Add connection in UI**:

1. Go to Admin → Connections
2. Add new connection:
   - Conn Id: `postgres_default`
   - Conn Type: `Postgres`
   - Host: `postgres-external`
   - Port: `15432`
   - Schema: `mydb`
   - Login: `postgres`
   - Password: `<password>`

### Redis Connection

```python
from airflow.providers.redis.hooks.redis import RedisHook

def read_from_redis():
    hook = RedisHook(redis_conn_id='redis_default')
    client = hook.get_conn()
    value = client.get('my_key')
    return value
```

## KubernetesExecutor Configuration

### Pod Template

Customize task pod template:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dummy-name
spec:
  containers:
    - name: base
      image: apache/airflow:2.9.0
      resources:
        requests:
          cpu: 100m
          memory: 256Mi
        limits:
          cpu: 500m
          memory: 512Mi
```

Save as `pod_template.yaml` and reference in Airflow config:

```yaml
executor:
  podTemplate: |
    <paste-pod-template-here>
```

## Monitoring

### Airflow UI

- **DAGs**: View all DAGs, trigger runs
- **Task Instances**: Monitor task execution
- **Logs**: View task logs
- **Graph**: Visualize DAG structure

### Metrics

Airflow exposes Prometheus metrics on port 9102.

**Grafana Dashboards**:

1. Import official Airflow Grafana dashboard
2. Monitor task durations, success rates, scheduler lag

**Common Metrics**:

- `airflow_scheduler_heartbeat`: Scheduler health
- `airflow_dagrun_duration_success`: DAG run duration
- `airflow_task_instance_duration`: Task duration
- `airflow_task_failures`: Task failures

## Troubleshooting

### DAG Not Appearing

**Check DAG file**:

```bash
kubectl exec -n airflow -it deployment/airflow-scheduler -- \
  airflow dags list
```

**Check parsing errors**:

```bash
kubectl logs -n airflow -l component=scheduler \
  | grep -i error
```

### Task Stuck in Queued

**Check scheduler**:

```bash
kubectl get pods -n airflow -l component=scheduler
kubectl logs -n airflow -l component=scheduler -f
```

**Check executor**:

```bash
# For KubernetesExecutor, check task pods
kubectl get pods -n airflow | grep <dag-id>
kubectl logs -n airflow <task-pod-name>
```

### Connection Issues

**Test connection from scheduler pod**:

```bash
kubectl exec -n airflow -it deployment/airflow-scheduler -- bash

# Test PostgreSQL
nc -zv postgres-external 15432

# Test Redis
nc -zv redis-external 16379
```

### Pod Resource Issues

**Check pod events**:

```bash
kubectl describe pod -n airflow <task-pod-name>
```

Common issues:

- **OOMKilled**: Increase memory limits
- **ImagePullBackOff**: Check image name and registry access
- **Pending**: Insufficient cluster resources

## Upgrading Airflow

```bash
# 1. Backup metadata database
kubectl exec -n airflow deployment/airflow-postgresql -- \
  pg_dump -U postgres airflow > airflow_backup.sql

# 2. Update Helm chart version
# Edit infrastructure/workflow/airflow/values.yaml

# 3. Apply upgrade
kubectl apply -k infrastructure/workflow/airflow

# 4. Run database migrations (if needed)
kubectl exec -n airflow deployment/airflow-scheduler -- \
  airflow db migrate
```

## Security

### Secrets Management

**Use Kubernetes Secrets**:

```yaml
env:
  - name: AIRFLOW__CORE__SQL_ALCHEMY_CONN
    valueFrom:
      secretKeyRef:
        name: airflow-secrets
        key: sql_alchemy_conn
```

**Seal secrets for GitOps**:

```bash
kubectl create secret generic airflow-secrets \
  --from-literal=sql_alchemy_conn=postgresql://... \
  --dry-run=client -o yaml | \
  kubeseal -o yaml > airflow-sealed-secrets.yaml
```

### RBAC

Configure role-based access control in Airflow UI:

1. Admin → Security → List Users
2. Create users with specific roles (Admin, Viewer, User)

## Best Practices

1. **Resource Limits**: Set appropriate CPU/memory for tasks
2. **Idempotency**: Design tasks to be idempotent
3. **Logging**: Log task progress and errors
4. **Monitoring**: Set up alerts for failed tasks
5. **Testing**: Test DAGs locally before deploying
6. **Version Control**: Store DAGs in Git
7. **Documentation**: Document complex workflows

## Common Use Cases

### ETL Pipeline

```python
from airflow.operators.python import PythonOperator

def extract():
    # Extract data from source
    pass

def transform():
    # Transform data
    pass

def load():
    # Load data to destination
    pass

with DAG('etl_pipeline', ...) as dag:
    extract_task = PythonOperator(task_id='extract', python_callable=extract)
    transform_task = PythonOperator(task_id='transform', python_callable=transform)
    load_task = PythonOperator(task_id='load', python_callable=load)

    extract_task >> transform_task >> load_task
```

### Scheduled Reporting

```python
from airflow.operators.email import EmailOperator

with DAG('daily_report', schedule_interval='0 8 * * *', ...) as dag:
    generate_report = PythonOperator(...)
    send_email = EmailOperator(
        task_id='send_report',
        to='team@example.com',
        subject='Daily Report',
        html_content='<p>Report attached</p>',
    )

    generate_report >> send_email
```

## References

- [Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow on Kubernetes](https://airflow.apache.org/docs/apache-airflow/stable/kubernetes.html)
- [KubernetesExecutor](https://airflow.apache.org/docs/apache-airflow/stable/executor/kubernetes.html)
- [Writing DAGs](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
