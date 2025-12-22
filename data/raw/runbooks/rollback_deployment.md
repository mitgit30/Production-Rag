---
service: generic
environment: prod
severity: high
owner: platform-engineering
doc_type: runbook
domain: sre
---

# Roll Back a Faulty Deployment

## Purpose
This runbook describes the procedure to safely roll back a Kubernetes Deployment to a
previous stable revision when a recent release causes service degradation, errors, or
unexpected behavior in production.

## When to Use
- Error rates or latency increase after a deployment
- Service health checks start failing post-release
- Functional regressions are observed after a rollout
- A recent change is identified as the likely root cause

## When NOT to Use
- When the issue is unrelated to the recent deployment
- If the deployment rollback would cause data incompatibility
- Without incident awareness or approval in production environments

## Preconditions
- You are the on-call engineer
- An incident ticket is created (for production)
- You have access to the Kubernetes cluster
- The faulty deployment revision is known or can be identified

## Impact
- Traffic may be briefly disrupted during the rollback
- Users may experience degraded service temporarily
- Recent feature changes will be reverted

---


### 1.Roll Back to the Previous Revision
Kubernetes keeps a history of Deployment revisions. Rolling back reverts the Deployment
to the last known stable configuration.

View the rollout history:

```bash
kubectl rollout history deployment/<deployment_name> -n <namespace>
```
### 2. Monitor the rollback progress:
```bash
kubectl rollout status deployment/<deployment_name> -n <namespace>
```
Verification
After the rollback, verify the following:
-Pods are running the expected container image version
-Service health checks return successful responses
-Error rates and latency return to baseline
-No new alerts are triggere

Rollback Failure Handling
If the rollback fails or does not resolve the issue, escalate to the appropriate team
-Review logs and metrics to diagnose the problem
-Consider alternative mitigation strategies
-Document the incident and actions taken for future reference

Escalation
-Escalate the incident if:
-Rollback does not stabilize the service
-Multiple rollback attempts fail
-Data integrity concerns are identifid