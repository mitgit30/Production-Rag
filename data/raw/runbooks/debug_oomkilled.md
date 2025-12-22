---
service: generic
environment: prod
severity: high
owner: platform-engineering
doc_type: runbook
domain: sre
---

# Debug OOMKilled Pods

## Purpose
This runbook provides steps to diagnose and resolve Kubernetes pods that are terminated
with an `OOMKilled` status due to exceeding memory limits.

## When to Use
- Pod status shows `OOMKilled`
- Pods restart repeatedly with memory-related errors
- Sudden service degradation after traffic increase
- Memory usage alerts are firing

## When NOT to Use
- When pod restarts are intentional (e.g., short-lived jobs)
- During planned load or stress testing
- Without incident awareness in production environments

## Preconditions
- You are the on-call engineer
- An incident ticket has been created (for production)
- You have access to the Kubernetes cluster
- Metrics collection (e.g., Prometheus) is available

## Impact
- Service instability or downtime
- Increased response latency
- Potential cascading failures in dependent services

---

## Diagnostic Steps 

### 1. Identify OOMKilled pods
List pods and confirm the OOMKilled status.

```bash
kubectl get pods -n <namespace>
```
### 2. Describe the OOMKilled pod
Get detailed information about the pod to understand the context of the OOM event.

```bash
kubectl describe pod <pod-name> -n <namespace>
```
### 3.Check memory requests and limits
Review the pod's resource requests and limits to see if they are appropriately set.

```bash
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 5 resources
```
### 4.Examine actual memory usage
If metrics are available, check real-time and historical memory usage.

```bash
kubectl top pod <pod-name> -n <namespace>
```
### 5. Check node-level memory pressure
Determine whether the node itself is under memory pressure.
```bash
kubectl describe node <node-name>
```
Look for:
MemoryPressure condition
Eviction events

Common Causes and Fixes

Memory Limits Too Low:
- Cause: The pod's memory limit is set too low for its workload.
- Fix: Increase the memory limit in the pod's resource specification.

Memory Leaks:
- Cause: The application has a memory leak, causing it to consume more memory over time.
- Fix: Investigate application logs and profiling tools to identify and fix memory leaks.

Traffic or Load Spikes:
- Cause: Sudden increases in traffic lead to higher memory usage.
- Fix: Implement autoscaling or optimize application memory usage.

Large Payloads or Misconfiguration:
- Cause: The application processes large payloads or is misconfigured.
- Fix: Optimize payload handling and review application configuration.