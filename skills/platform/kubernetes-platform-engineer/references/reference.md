# Kubernetes Platform Engineer Reference

## Table of Contents

1. Workload Profile Decision
2. Baseline Manifest Set
3. Resource Management
4. Health Probes
5. Security Hardening
6. RBAC Design
7. Autoscaling (HPA)
8. Observability
9. Progressive Delivery
10. Anti-Patterns Checklist

---

## 1. Workload Profile Decision

| Signal | Choose |
|---|---|
| HTTP API, stateless, scales horizontally | Deployment |
| Persistent storage, ordered startup/shutdown | StatefulSet |
| One-shot or scheduled tasks | Job / CronJob |
| System daemon on every node | DaemonSet |
| Fan-out to many replicas | Deployment + HPA |

---

## 2. Baseline Manifest Set

### Production Deployment (minimum viable)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-service
  namespace: production
  labels:
    app: my-service
    version: "1.2.3"
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-service
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
      maxSurge: 1
  template:
    metadata:
      labels:
        app: my-service
        version: "1.2.3"
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: my-service
      securityContext:
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: my-service
          image: registry.example.com/my-service:1.2.3
          ports:
            - name: http
              containerPort: 8080
          envFrom:
            - configMapRef:
                name: my-service-config
          env:
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: my-service-secrets
                  key: db-password
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          securityContext:
            runAsNonRoot: true
            runAsUser: 1000
            readOnlyRootFilesystem: true
            allowPrivilegeEscalation: false
            capabilities:
              drop: ["ALL"]
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
            failureThreshold: 3
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 20
            failureThreshold: 3
          startupProbe:
            httpGet:
              path: /health/live
              port: 8080
            failureThreshold: 30
            periodSeconds: 5
          volumeMounts:
            - name: tmp-dir
              mountPath: /tmp
      volumes:
        - name: tmp-dir
          emptyDir: {}
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: kubernetes.io/hostname
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: my-service
```

---

## 3. Resource Management

### Sizing guide

| Profile | CPU req | CPU lim | Mem req | Mem lim |
|---|---|---|---|---|
| Light API | 50m | 200m | 64Mi | 256Mi |
| Standard API | 100m | 500m | 128Mi | 512Mi |
| Heavy compute | 500m | 2000m | 512Mi | 2Gi |
| ML inference | 1000m | 4000m | 2Gi | 8Gi |

**Rules:**
- Always set BOTH requests and limits — missing limits allows unbounded memory.
- CPU throttling at limit is gradual; memory at limit = OOMKill.
- Set memory limit at 2x normal peak usage.
- Use `kubectl top pods` and Prometheus to tune based on real data.

### HPA (HorizontalPodAutoscaler)
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-service-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-service
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Pods
          value: 1
          periodSeconds: 60
```

---

## 4. Health Probes

| Probe | Purpose | Failure result |
|---|---|---|
| `readinessProbe` | Pod ready to serve traffic? | Removed from Service endpoints |
| `livenessProbe` | Pod still alive (not deadlocked)? | Container restarted |
| `startupProbe` | App finished slow startup? | Blocks liveness check until done |

### Health endpoints (FastAPI example)
```python
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/health/ready")
async def readiness():
    # Check DB, cache, external dependencies
    return {"status": "ready"}

@app.get("/health/live")
async def liveness():
    return {"status": "alive"}
```

---

## 5. Security Hardening

### Required security context for every container
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
```

### NetworkPolicy (deny all by default, allow explicitly)
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: my-service-netpol
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: my-service
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: ingress-nginx
      ports:
        - port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - port: 5432
    - to:   # DNS resolution
        - namespaceSelector: {}
      ports:
        - port: 53
          protocol: UDP
```

---

## 6. RBAC Design

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-service
  namespace: production
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: my-service-role
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: my-service-binding
  namespace: production
subjects:
  - kind: ServiceAccount
    name: my-service
roleRef:
  kind: Role
  name: my-service-role
  apiGroup: rbac.authorization.k8s.io
```

**Rules:** never use the `default` ServiceAccount; never grant cluster-admin; grant only what the service actually calls.

---

## 7. Observability

### Prometheus annotations (pod-level scraping)
```yaml
annotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "8080"
  prometheus.io/path: "/metrics"
```

### Key application metrics (Python)
```python
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "http_requests_total", "Total requests",
    ["method", "path", "status_code"]
)
REQUEST_DURATION = Histogram(
    "http_request_duration_seconds", "Request latency",
    ["method", "path"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5]
)
```

---

## 8. Progressive Delivery

### Rollout runbook
```bash
# Deploy new version
kubectl set image deployment/my-service my-service=registry.example.com/my-service:1.3.0 -n production

# Watch rollout progress
kubectl rollout status deployment/my-service -n production

# Rollback on failure (immediate)
kubectl rollout undo deployment/my-service -n production

# Verify rollback
kubectl get pods -l app=my-service -n production
kubectl logs -l app=my-service -n production --tail=100
```

### PodDisruptionBudget (required for SLO workloads)
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-service-pdb
  namespace: production
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: my-service
```

---

## 9. Anti-Patterns Checklist

| Anti-pattern | Risk | Fix |
|---|---|---|
| No resource limits | OOM kills neighbors | Always set requests + limits |
| `latest` image tag | Non-deterministic deploys | Pin to version tag or SHA digest |
| Running as root | Container escape risk | `runAsNonRoot: true`, `runAsUser: 1000` |
| No readinessProbe | Traffic to unready pods | Add readinessProbe to every container |
| Secrets in ConfigMap | Secret leakage | Use Secret resource |
| No NetworkPolicy | Unrestricted pod comms | Add deny-all + allow-necessary |
| Single replica for SLO | No fault tolerance | minReplicas ≥ 2 + PDB |
| No topologySpread | All pods on one node | Add topologySpreadConstraints |
| Direct secrets as env vars | Secret leakage via `/proc` | Use `secretKeyRef` or mounted secret volume |
