---
name: kubernetes-platform-engineer
description: Design, deploy, and operate production Kubernetes workloads with manifests, Helm/Kustomize structure, autoscaling, networking, security hardening, and observability. Use when containerized services must run on Kubernetes, when designing platform standards, or when creating deployment templates and operational runbooks.
---

# Kubernetes Platform Engineer

## Overview

Implement production-grade Kubernetes deployments with repeatable manifests and operational guardrails.

## Workflow

1. Define workload profile (stateless/stateful, traffic, SLOs).
2. Generate baseline manifests (Deployment, Service, ConfigMap, HPA, Ingress).
3. Add readiness/liveness/startup probes.
4. Add resource requests/limits and autoscaling policy.
5. Add security context, RBAC, and network policies.
6. Add observability (metrics, logs, traces) and rollout strategy.

## Core Rules

- Always set resource requests/limits.
- Run as non-root by default.
- Use immutable image tags in production.
- Separate config and secrets.
- Enforce progressive delivery for risky changes.

## Included Resources

- `references/reference.md`: architecture and operations guide.
- `references/examples.md`: manifest snippets and rollout patterns.
- `scripts/scaffold_k8s_service.py`: generate deployable manifest bundle.
- `assets/kustomization.base.yaml`: base kustomization example.

## Output Format

1. Workload profile and requirements
2. Namespace and resource topology
3. Manifest set
4. Security/observability controls
5. Rollout and rollback runbook
