---
service: generic
environment: prod
severity: medium
owner: platform-engineering
doc_type: runbook
domain: sre
---

# Investigate High CPU Utilization

## Purpose
This runbook provides steps to investigate and mitigate high CPU utilization in Kubernetes
workloads that may cause increased latency, request failures, or service instability.

## When to Use
- CPU utilization alerts are firing
- Increased request latency or timeouts
- Pods are throttled or unresponsive
- Autoscaling events are triggered unexpectedly

## When NOT to Use
- During planned load tests
- If high CPU usage is expected due to batch processing
- Without incident awareness in production environments

## Preconditions
- You are the on-call engineer
- An incident ticket has been created (for production)
- You have access to the Kubernetes cluster
- Metrics collection (e.g., Prometheus) is available

## Impact
- Increased response times
- Request failures under load
- Potential pod restarts or throttling

---

## Diagnostic Steps (Recommended)

### 1. Identify affected pods and namespaces
List pods and review current CPU usage.

```bash
kubectl get pods -n <namespace>
```
### 2. Check node-level CPU usage
Determine if the issue is isolated to a pod or affecting the entire node.
```bash
kubectl top nodes
```
### 3. Review recent deployments or changes
Identify whether a recent deployment or configuration change introduced the issue.
```bash
kubectl rollout history deployment/<deployment_name> -n <namespace>
```
### 4.Inspect pod resource requests and limits
Verify CPU requests and limits are configured appropriately.
```bash
kubectl get pod <pod_name> -n <namespace> -o yaml

```
### 5.Examine application behavior
Check application logs for excessive loops, retries, or unexpected load patterns.
```bash
kubectl logs <pod_name> -n <namespace>

```
Common Causes and Fixes

CPU Limits Too Low :-

Pod is CPU throttled due to restrictive limits
Fix:
-Increase CPU limits
-Adjust CPU requests to match usage

Traffic Spikes:-
-Sudden increase in user or internal traffic

Fix:
-Enable or tune Horizontal Pod Autoscaler (HPA)
-Implement rate limiting if necessary

Inefficient Application Code:-
-Tight loops or expensive computations

Fix:
-Profile the application
-Optimize or cache expensive operations

Noisy Neighbor on Node:-
-Other workloads consuming excessive CPU

Fix:
-Reschedule pods to different nodes
-Apply node affinity or resource isolation