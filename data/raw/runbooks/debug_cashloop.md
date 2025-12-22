---
service: generic
environment: prod
severity: high
owner: platform-engineering
doc_type: runbook
domain: sre
---

# Debug Pods in CrashLoopBackOff

## Purpose
This runbook describes the steps to diagnose and resolve issues causing Kubernetes pods
to repeatedly crash and restart, resulting in a CrashLoopBackOff state.

## When to Use
- Pods are repeatedly restarting
- Pod status shows `CrashLoopBackOff`
- Application fails immediately after startup
- Deployment does not stabilize after rollout

## When NOT to Use
- When the pod is intentionally terminating (job completion)
- If the issue is caused by a planned shutdown
- Without incident awareness in production environments

## Preconditions
- You are the on-call engineer
- An incident ticket has been created (for production)
- You have access to the Kubernetes cluster
- You know the namespace and pod or deployment name

## Impact
- Service functionality may be partially or fully unavailable
- Dependent services may experience errors
- Repeated restarts can increase resource usage

---

## Diagnostic Steps

### 1. Identify the affected pod
List pods and confirm the CrashLoopBackOff status.

```bash
kubectl get pods -n <namespace>
 ```

### 2. Inspect pod details and events
Describe the pod to review events, exit codes, and failure reasons.
```bash
kubectl describe pod <pod_name> -n <namespace>
```
### 3.Check container logs
Review the logs from the last container attempt.

```bash
kubectl logs <pod_name> -n <namespace> --previous
```
If multiple containers exist:

```bash 
kubectl logs <pod_name> -c <container_name> -n <namespace> --previous
```
### 4.Verify resource limits and requests
Check if CPU or memory limits are too low.
```bash
kubectl get pod <pod_name> -n <namespace> -o yaml

```
### 5.Check configuration and secrets
Validate ConfigMaps, Secrets, and environment variables used by the pod.
```bash
kubectl describe configmap <configmap_name> -n <namespace>
kubectl describe secret <secret_name> -n <namespace>

```
### Roll Back the Deployment
If a recent deployment caused the CrashLoopBackOff, consider rolling back to a previous stable version.

```bash
kubectl rollout undo deployment/<deployment_name> -n <namespace>
```

Common Causes and Fixes

Application Crash on Startup:-
-Misconfigured environment variables
-Missing dependencies
-Invalid startup commands

Fix:
-Correct configuration
-Roll back to a previous stable deployment

OOMKilled Containers
-Memory limits exceeded
-Memory leak

Fix:
-Increase memory limits
-Investigate application memory usage


Failed Health Probes
-Incorrect probe configuratio
-Application startup takes longer than expected

Image Pull Errors
-Incorrect image name or tag
-Registry authentication issues


Fix:
-Correct image reference
-Verify image pull secrets

