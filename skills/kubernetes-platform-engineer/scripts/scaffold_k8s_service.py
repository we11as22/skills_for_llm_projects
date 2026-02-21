#!/usr/bin/env python3
"""Generate Kubernetes manifests for a service (Deployment, Service, HPA, Ingress, Kustomization)."""

from __future__ import annotations

import argparse
from pathlib import Path


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="Service name")
    parser.add_argument("--image", default="ghcr.io/example/app:1.0.0")
    parser.add_argument("--namespace", default="default")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--output", type=Path, default=Path("k8s"))
    args = parser.parse_args()

    n = args.name
    ns = args.namespace
    p = args.port

    deployment = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {n}
  namespace: {ns}
spec:
  replicas: 2
  selector:
    matchLabels:
      app: {n}
  template:
    metadata:
      labels:
        app: {n}
    spec:
      securityContext:
        runAsNonRoot: true
      containers:
        - name: {n}
          image: {args.image}
          ports:
            - containerPort: {p}
          resources:
            requests:
              cpu: "200m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "1Gi"
          readinessProbe:
            httpGet:
              path: /health
              port: {p}
            initialDelaySeconds: 5
          livenessProbe:
            httpGet:
              path: /health
              port: {p}
            initialDelaySeconds: 15
"""

    service = f"""apiVersion: v1
kind: Service
metadata:
  name: {n}
  namespace: {ns}
spec:
  selector:
    app: {n}
  ports:
    - port: 80
      targetPort: {p}
  type: ClusterIP
"""

    hpa = f"""apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {n}
  namespace: {ns}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {n}
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
"""

    ingress = f"""apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {n}
  namespace: {ns}
spec:
  rules:
    - host: {n}.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: {n}
                port:
                  number: 80
"""

    kustomization = """apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - service.yaml
  - hpa.yaml
  - ingress.yaml
"""

    out = args.output / n
    write(out / "deployment.yaml", deployment)
    write(out / "service.yaml", service)
    write(out / "hpa.yaml", hpa)
    write(out / "ingress.yaml", ingress)
    write(out / "kustomization.yaml", kustomization)

    print(f"Kubernetes manifests generated at {out}")


if __name__ == "__main__":
    main()
