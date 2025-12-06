# Deployment & Infrastructure

## Overview
We follow a strict **GitOps** capability using **FluxCD**. This means all infrastructure changes are committed to code (IaC) and automatically reconciled by the cluster.

## Deployment Strategy

### 1. Environment Propagation
We define three core environments mapped to Kubernetes Namespaces:
- **`dev`**: Feature branches and rapid iteration.
- **`staging`**: Pre-production testing, identical config to prod.
- **`prod`**: User-facing stable environment.

### 2. GitOps Structure
We use the logic in our `sentiment-analysis-gitops` repository:

```text
/
├── apps/               # Application HelmRelease and Kustomizations
│   ├── base/           # Common config
│   ├── overlays/       # Env-specific patches
│   │   ├── dev/
│   │   ├── staging/
│   │   └── prod/
│
├── infrastructure/     # Infrastructure components (Kafka, databases)
│   ├── base/
│   └── controllers/    # Ingress Nginx, Cert-Manager, etc.
│
└── clusters/           # FluxCD Entrypoints
    ├── dev/
    └── prod/
```

## Prerequisites

### Tools
- **Docker**: For container runtime.
- **Kind** (Kubernetes in Docker) or **Minikube**: For local development.
- **Flux CLI**: For bootstrapping.
- **Terraform** (Optional): If deploying to AWS/GCP (files located in `/terraform`).

### Local Development Setup (Quickstart)

1.  **Start Cluster**
    ```bash
    kind create cluster --name sentiment-platform --config kind-config.yaml
    ```

2.  **Bootstrap Flux**
    ```bash
    flux bootstrap github \
      --owner=<your-github-user> \
      --repository=sentiment-analysis-gitops \
      --branch=main \
      --path=./clusters/dev \
      --personal
    ```

3.  **Port Forwarding**
    Access services locally:
    ```bash
    kubectl port-forward svc/frontend 8080:80 -n dev
    kubectl port-forward svc/grafana 3000:3000 -n monitoring
    ```

## Terraform (Cloud Provisioning)
*Note: For this project phase, we focus on local/VM based K8s, but the structure allows for cloud adoption.*

```hcl
# Example structure in /terraform/main.tf
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"
  cluster_name = "sentiment-prod"
  # ...
}
```

## Scaling Policies
- **HPA (Horizontal Pod Autoscaler)**: Enabled on backend and consumer services based on CPU/Memory usage.
- **KEDA (Kubernetes Event-driven Autoscaling)**: (Future) Scale Spark workers based on Kafka lag.
