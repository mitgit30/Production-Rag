---
service: platform
environment: prod
owner: platform-engineering
doc_type: infra_doc
domain: sre
---

# Kubernetes Cluster Architecture

## Purpose
This document provides an overview of the Kubernetes cluster architecture used to run
production services. It explains how workloads are deployed, how traffic flows through
the system, and how core components interact.

This document is intended to help engineers understand **how the platform is built**,
not how to respond to incidents.

---

## High-Level Architecture Overview
The production platform is built on a Kubernetes cluster consisting of:
- A managed control plane
- Multiple worker nodes
- Namespace-isolated workloads
- Shared networking and storage components

All application services are deployed as Kubernetes Deployments and exposed internally
or externally via Services and Ingress resources.

---

## Control Plane Components
The Kubernetes control plane is responsible for maintaining the desired state of the
cluster.

Key components include:
- **API Server** – Entry point for all cluster operations
- **Scheduler** – Assigns pods to worker nodes based on resource availability
- **Controller Manager** – Ensures desired state (replicas, health, restarts)
- **etcd** – Stores cluster state and configuration data

The control plane does not run application workloads.

---

## Worker Nodes
Worker nodes are responsible for running application pods.

Each node includes:
- kubelet (node agent)
- Container runtime (e.g., containerd)
- Networking components
- Local disk and memory resources

Pods are scheduled onto worker nodes based on:
- Resource requests
- Node availability
- Taints, tolerations, and affinity rules

---

## Namespaces and Isolation
Namespaces are used to logically isolate workloads and resources.

Typical namespaces include:
- `prod` – Production workloads
- `staging` – Pre-production testing
- `monitoring` – Observability components
- `kube-system` – Kubernetes system components

Namespaces help enforce:
- Resource quotas
- Access control
- Logical separation of services

---

## Workload Deployment Model
Applications are deployed using the following Kubernetes resources:
- **Deployment** – Defines desired pod replicas and rollout strategy
- **ReplicaSet** – Ensures the correct number of pods are running
- **Pod** – Smallest deployable unit containing one or more containers

Deployments manage:
- Rolling updates
- Pod restarts
- Rollbacks to previous revisions

---

## Service Networking
Each application is exposed using Kubernetes Services.

Service types commonly used:
- **ClusterIP** – Internal service-to-service communication
- **NodePort / LoadBalancer** – External access (via cloud provider)
- **Ingress** – HTTP routing and TLS termination

Traffic flow typically follows:
Ingress → Service → Pod

---

## Traffic Flow Overview
1. External traffic enters through an Ingress controller
2. Ingress routes requests to the appropriate Service
3. Service load-balances traffic across healthy pods
4. Pods process requests and communicate with dependencies

Health checks determine pod readiness and traffic eligibility.

---

## Scheduling and Resilience
The scheduler places pods based on:
- CPU and memory requests
- Node capacity
- Scheduling constraints

Resilience mechanisms include:
- Pod restarts on failure
- Rescheduling on node failure
- Rolling updates during deployments

If a node becomes unavailable, pods are rescheduled onto healthy nodes.

---

## Failure Domains
Failures may occur at different levels:
- Pod-level (application crash)
- Node-level (resource exhaustion, hardware failure)
- Network-level (connectivity issues)
- Control-plane-level (rare, managed by provider)

Understanding failure domains helps in incident diagnosis and mitigation.

---

## Related Runbooks
- Restart a Kubernetes Service Safely
- Resolve Pod Scheduling Failures
- Handle Kubernetes Node NotReady

## Related Incidents
- INC-005: Node NotReady Leading to Pod Evictions
