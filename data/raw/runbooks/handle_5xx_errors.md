---
service: generic
environment: prod
severity: high
owner: platform-engineering
doc_type: runbook
domain: sre
---

# Handle HTTP 5xx Error Spikes

## Purpose
This runbook describes how to investigate and mitigate spikes in HTTP 5xx errors,
which indicate server-side failures and can lead to service outages or degraded
user experience.

## When to Use
- HTTP 5xx error rate alerts are firing
- Sudden increase in failed API requests
- Clients report server errors or timeouts
- Monitoring dashboards show elevated 5xx responses

## When NOT to Use
- During planned maintenance windows
- When errors are confirmed to originate from client-side issues (4xx)
- Without incident awareness or coordination in production environments

## Preconditions
- You are the on-call engineer
- An incident ticket has been created (for production)
- You have access to the Kubernetes cluster
- Application logs and metrics are available

## Impact
- Requests fail for end users
- Downstream services may experience cascading failures
- Potential SLA/SLO violations

---

## Diagnostic Steps (Recommended)

### 1. Confirm the scope of the issue
Identify which service and endpoints are returning 5xx errors.

```bash
kubectl get pods -n <namespace>
```
### 2. Check recent deployments
Review deployment history to see if recent changes could be causing the issue.

```bash
kubectl rollout history deployment/<deployment-name> -n <namespace>
```
### 3. Inspect application logs
Check logs for error messages or stack traces that indicate the root cause.

```bash
kubectl logs <pod-name> -n <namespace>
```
### 4. Investigate dependencies

Determine whether the service depends on:
-Databases
-Caches
-External APIs
-Message queues
-Check for timeouts, connection errors, or rate limiting.

### Common Causes and Fixes

Application Errors:
-cause: Bugs or exceptions in the code
-fix: Roll back recent changes or deploy hotfixes

Resource Exhaustion:
-cause: Insufficient CPU/memory leading to crashes
-fix: Scale up resources or optimize resource requests/limits

Dependency Failures:
-cause: Downstream services are unavailable or slow
-fix: Implement retries, circuit breakers, or failover strategies

Configuration Issues:
-cause: Misconfigured environment variables or settings
-fix: Verify and correct configurations as needed

