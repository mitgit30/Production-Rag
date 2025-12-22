---
service: generic
environment: prod
severity: medium
owner: platform-engineering
doc_type: runbook
domain: sre
---

# Resolve Pod Scheduling Failures

## Purpose
This runbook provides steps to diagnose and resolve Kubernetes pods that remain in
`Pending` state due to scheduling failures.

## When to Use
- Pods remain in `Pending` state for an extended period
- Alerts indicate unschedulable pods
- New deployments fail to start pods
- Capacity-related incidents are suspected

## When NOT to Use
- During intentional node maintenance or drain operations
- If pods are paused intentionally for testing
- Without incident awareness in production environments

## Preconditions
- You are the on-call engineer
- An incident ticket has been created (for production)
- You have access to the Kubernetes cluster
- You know the namespace and pod or deployment name

## Impact
- Application is unavailable or partially unavailable
- New workloads cannot be scheduled
- Potential service degradation or outage

---

## Diagnostic Steps (Recommended)

### 1. Identify pending pods
List pods and confirm their scheduling status.

```bash
kubectl get pods -n <namespace>

```
### 2. Describe the pending pod
Get detailed information about the pod to identify scheduling issues.

```bash
kubectl describe pod <pod-name> -n <namespace>
```
Look for events at the bottom of the output indicating scheduling problems.

### 3. Check node capacity
Examine node resources to see if there is enough capacity for new pods.

```bash
kubectl get nodes -o wide
kubectl describe nodes
``` 
### 4. Review resource requests and limits
Check if the pod's resource requests exceed available node resources.

```bash
kubectl describe pod <pod-name> -n <namespace>
```
Look for `Requests` and `Limits` under the container specifications.

### 5. Check node labels and taints
Ensure that the pod's node selectors or tolerations match the nodes' labels and taints.

```bash
kubectl get nodes --show-labels
kubectl describe node <node-name>
```

### Common causes and Fixes:

Insufficient Node Resources:
cause : Node capacity is insufficient for the pod's resource requests.
fix : Ensure that the pod's resource requests are within the available node capacity.   Consider scaling the cluster or adjusting resource requests.

Node Selectors/Taints Mismatch:
cause : Pod's node selectors or tolerations do not match any available nodes.
fix : Update the pod's node selectors or tolerations to match available nodes, or modify node labels/taints as needed.

Affinity/Anti-affinity Rules:
cause : Pod's affinity or anti-affinity rules prevent scheduling.
fix : Review and adjust affinity/anti-affinity rules to allow scheduling.

