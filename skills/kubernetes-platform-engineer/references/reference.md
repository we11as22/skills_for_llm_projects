# Kubernetes Platform Reference

## Table of Contents

1. Workload design
2. Deployment standards
3. Scaling and resilience
4. Security baseline
5. Operations

## 1. Workload Design

- Stateless services: Deployment + Service + HPA.
- Stateful workloads: StatefulSet + PVC + backup policy.
- Async workers: Deployment + queue metrics-driven autoscaling.

## 2. Deployment Standards

- Readiness and liveness probes required.
- Resource requests/limits mandatory.
- Config via ConfigMap; secrets via Secret manager.

## 3. Scaling and Resilience

- HPA based on CPU/memory/custom metrics.
- PodDisruptionBudget for critical services.
- Topology spread/anti-affinity for HA.

## 4. Security Baseline

- RBAC least privilege.
- NetworkPolicy default deny with explicit allow.
- Pod Security Standards (restricted profile where feasible).
- Image scanning and signature verification.

## 5. Operations

- Use rolling updates with max unavailable controls.
- Keep dashboards for latency, error rate, saturation.
- Define rollback triggers and SLO alert thresholds.
