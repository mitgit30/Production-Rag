---
service: generic
environment: prod
severity: high
owner: platform-engineering
doc_type: runbook
domain: sre
---

# Handle Kubernetes Node NotReady

## Purpose
This runbook describes how to investigate and mitigate situations where one or more
Kubernetes nodes transition to a `NotReady` state, potentially impacting workload
availability and cluster stability.

## When to Use
- Node status changes to `NotReady`
- Alerts indicate node unavailability
- Pods are evicted or fail to schedule
- Degraded cluster performance is observed

## When NOT to Use
- During planned node maintenance or upgrades
- If the node is intentionally cordoned or drained
- Without incident awareness in production environments

## Preconditions
- You are the on-call engineer
- An incident ticket has been created (for production)
- You have access to the Kubernetes cluster
- You can access underlying node infrastructure if required

## Impact
- Pods on the affected node may be evicted or unavailable
- New pods may fail to schedule
- Potential cascading impact on dependent services

---

## Diagnostic Steps (Recommended)

### 1. Identify affected nodes
List nodes and confirm the `NotReady` status.

```bash
kubectl get nodes

```
### 2. Describe the NotReady node
Get detailed information about the node to identify issues.

```bash
kubectl describe node <node-name>
```
### 3. Check node conditions
Look for conditions in the output that indicate why the node is `NotReady`.
### 4. Review node logs
Access the node and check system logs for errors.

```bash
ssh <node-ip>
journalctl -xe
```
### 5. Verify kubelet status
Check if the kubelet service is running properly.

```bash
systemctl status kubelet
```
### Comman causes and fixes

Resource Exhaustion:
- Cause: Node runs out of CPU, memory, or disk space.
- Fix: Free up resources or scale the cluster.

Network Issues:
- Cause: Network misconfiguration or failure.
- Fix: Check network connectivity and configurations.
- Restart network services if necessary.

Kubelet Failures:
- Cause: Kubelet crashes or is misconfigured.
- Fix: Restart the kubelet service and check its configuration.
- Ensure kubelet has proper permissions and configurations.

Hardware Failures:
- Cause: Underlying hardware issues.
- Fix: Investigate hardware health and replace faulty components.
- Coordinate with infrastructure teams if needed.

