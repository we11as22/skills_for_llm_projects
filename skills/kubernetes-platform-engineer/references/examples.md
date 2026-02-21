# Kubernetes Examples

## Example 1: Deployment Probe

```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
```

## Example 2: HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  minReplicas: 2
  maxReplicas: 10
```

## Example 3: Rollout

- Deploy with canary 10% traffic.
- Monitor errors and latency.
- Promote to 50%, then 100%.
