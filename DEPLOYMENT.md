# Deployment & Infrastructure

## Overview
We use a **GitOps** approach using **Kustomize** for configuration management. The infrastructure is defined in the `sentiment-analysis-gitops` repository.

## GitOps Structure (`sentiment-analysis-gitops`)

We use a standard Kustomize **Base + Overlay** pattern:

```text
/
├── manifests/
│   ├── base/               # Common definitions for all environments
│   │   ├── backend/
│   │   ├── frontend/
│   │   ├── kafka/          # Strimzi Kafka Cluster
│   │   ├── spark/          # Spark Service Accounts
│   │   ├── qdrant/
│   │   ├── sealed-secrets/
│   │   └── kustomization.yaml
│   │
│   └── overlays/           # Environment-specific patches
│       ├── dev/
│       ├── stg/
│       ├── uat/
│       ├── pro/
│
└── README.md
```

## Prerequisities
- **WSL 2** (Windows Subsystem for Linux)
- **Docker Desktop** (configured with WSL 2 backend)
- **Kind** or **Minikube**
- **Kubectl**
- **Kustomize**

## Deployment Commands

To deploy an environment (e.g., `dev`):

```bash
# From the root of the gitops repo
kustomize build manifests/overlays/dev | kubectl apply -f -
```

## Secrets Management
We use **Sealed Secrets** to encrypt sensitive data (API keys, DB passwords) in the git repo.
- **Controller**: Deployed via `manifests/base/sealed-secrets`.
- **Usage**:
  1. Create a secret locally: `kubectl create secret generic my-secret --dry-run=client --from-literal=foo=bar -o json > secret.json`
  2. Seal it: `kubeseal < secret.json > sealed-secret.yaml`
  3. Commit `sealed-secret.yaml` to the repo.

## Scaling
- **Horizontal Pod Autoscaler (HPA)**: Can be added as a patch in `overlays/pro`.
- **Replicas**: Managed via patches in `overlays/<env>/patches/replicas-patch.yaml` (Removed if unnecessary).
