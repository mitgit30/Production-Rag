---
service: platform
environment: prod
owner: platform-engineering
doc_type: infra_doc
domain: sre
---

# Deployment and Rollout Strategy

## Purpose
This document describes how application services are deployed to the Kubernetes cluster
and how rollout, rollback, and restart mechanisms work. It provides context for
understanding deployment-related incidents and recovery actions.

This document explains **how deployments behave**, not how to respond to incidents.

---

## Deployment Model
All application services are deployed using Kubernetes **Deployments**.

A Deployment defines:
- Desired number of replicas
- Pod template (container image, config, resources)
- Rollout and update strategy

Each Deployment manages one or more **ReplicaSets**, which in turn manage pods.

---

## Rolling Update Strategy
Production services use a rolling update strategy by default.

Key characteristics:
- Pods are replaced gradually
- Old and new versions may run simultaneously
- Availability is maintained if configured correctly

Common parameters:
- `maxUnavailable`
- `maxSurge`

Incorrect values can cause:
- Reduced availability
- Increased load on remaining pods

---

## Rollout Lifecycle
A typical rollout follows this sequence:
1. New Deployment revision is created
2. New pods are scheduled
3. Readiness probes gate traffic
4. Old pods are terminated gradually
5. Rollout completes when desired state is reached

If any step fails, the rollout may stall or degrade service.

---

## Rollout Restarts
A rollout restart triggers pod recreation without changing the Deployment spec.

Typical use cases:
- Refreshing configuration
- Reloading secrets
- Recovering from transient issues

Rollout restarts:
- Create a new ReplicaSet
- Replace pods one by one
- Do not change application code

---

## Rollback Mechanism
Kubernetes maintains a history of Deployment revisions.

Rollback behavior:
- Reverts to a previous ReplicaSet
- Restores the previous pod template
- Does not restore external state (e.g., database changes)

Rollback is effective only if:
- Previous revision is stable
- Configuration compatibility is maintained

---

## Rollout Failures
Common reasons for rollout failure:
- Application crash on startup
- Failed readiness or liveness probes
- Resource misconfiguration
- Invalid container image

Failed rollouts may result in:
- Partial availability
- Increased error rates
- Pods stuck in CrashLoopBackOff

---

## Configuration Changes and Risk
Configuration changes are applied via:
- ConfigMaps
- Secrets
- Environment variables

Risks include:
- Missing required values
- Incompatible configuration formats
- Immediate startup failures

Configuration changes should be treated with the same care as code changes.

---

## Deployment Safety Practices
Recommended practices:
- Use readiness probes to protect traffic
- Roll out changes gradually
- Monitor metrics during rollouts
- Prefer reversible changes
- Avoid large, untested configuration changes

Deployment safety directly impacts system reliability.

---

## Observability During Rollouts
Key signals to monitor:
- Pod restarts
- Readiness failures
- Error rates and latency
- Rollout progress status

Early detection allows faster rollback and mitigation.

---

## Related Runbooks
- Roll Back a Faulty Deployment
- Restart a Kubernetes Service Safely
- Debug Pods in CrashLoopBackOff

## Related Incidents
- INC-001: CrashLoopBackOff After Configuration Change
- INC-003: OOMKilled Pods After Deployment
- INC-011: Failed CI/CD Deployment
