---
service: platform
environment: prod
owner: platform-engineering
doc_type: infra_doc
domain: sre
---

# Resource Management and Autoscaling

## Purpose
This document explains how CPU and memory resources are managed for workloads running
in the Kubernetes cluster, and how autoscaling mechanisms respond to changes in load.

It provides context for understanding performance issues, scaling behavior, and
resource-related incidents.

---

## Resource Requests and Limits

### CPU Requests and Limits
- **CPU requests** define the minimum CPU guaranteed to a pod
- **CPU limits** define the maximum CPU a pod can use

If a pod exceeds its CPU limit:
- It is throttled by the kernel
- Performance may degrade, but the pod is not terminated

### Memory Requests and Limits
- **Memory requests** define the minimum memory reserved for a pod
- **Memory limits** define the maximum memory a pod can use

If a pod exceeds its memory limit:
- The container is terminated
- The pod enters an `OOMKilled` state

Correct sizing of requests and limits is critical for stability.

---

## How the Scheduler Uses Requests
The Kubernetes scheduler uses **resource requests**, not limits, when placing pods on
nodes.

Scheduling decisions consider:
- Available CPU and memory on nodes
- Existing pod requests
- Scheduling constraints (taints, affinity)

Overstated requests can lead to poor utilization, while understated requests can cause
resource contention.

---

## Horizontal Pod Autoscaler (HPA)

### What HPA Does
The Horizontal Pod Autoscaler automatically adjusts the number of pod replicas based on
observed metrics.

Common metrics include:
- CPU utilization
- Memory utilization
- Custom application metrics

### HPA Behavior
- HPA periodically evaluates metrics
- Scaling decisions are based on rolling averages
- Scale-up is usually faster than scale-down

HPA does not react instantly to sudden traffic spikes.

---

## Autoscaling Limitations
HPA has important limitations:
- Requires metrics availability
- Scaling is bounded by min and max replica counts
- Node capacity can limit scaling effectiveness

If nodes are saturated, HPA may be unable to scale even if replicas increase.

---

## Node Capacity and Overcommitment
Nodes have finite CPU and memory capacity.

Common practices:
- CPU is often overcommitted
- Memory overcommitment is risky and discouraged

If total memory usage exceeds node capacity:
- Pods may be evicted
- Nodes may enter `NotReady` state

---

## Common Resource-Related Failure Modes
Resource misconfiguration can lead to:
- CPU throttling and latency spikes
- OOMKilled pods
- Pending pods due to insufficient capacity
- Ineffective autoscaling during traffic spikes

Understanding these patterns helps diagnose incidents quickly.

---

## Observability and Monitoring
Key metrics to monitor include:
- Pod CPU and memory usage
- Node utilization
- HPA scaling events
- Throttling and eviction events

Correlating metrics with deployments and traffic changes is essential.

---

## Design Guidelines
General best practices:
- Set realistic resource requests based on observed usage
- Avoid overly restrictive memory limits
- Tune HPA thresholds based on real traffic patterns
- Test scaling behavior under load

Resource configuration should evolve as services change.

---

## Related Runbooks
- Investigate High CPU Utilization
- Debug OOMKilled Pods
- Resolve Pod Scheduling Failures

## Related Incidents
- INC-002: High CPU Utilization Causing API Latency Spike
- INC-003: OOMKilled Pods After Deployment
