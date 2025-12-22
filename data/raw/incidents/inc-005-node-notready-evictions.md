---
incident_id: INC-005
service: inventory-service
environment: prod
severity: high
owner: platform-engineering
doc_type: incident
domain: sre
---

# INC-005: Node NotReady Leading to Pod Evictions

## Summary
On 2024-07-14, one of the Kubernetes worker nodes hosting the `inventory-service`
transitioned to a `NotReady` state due to disk pressure. As a result, multiple pods were
evicted, causing partial service disruption until workloads were rescheduled.

## Impact
- Inventory availability checks failed intermittently
- Pods running on the affected node were evicted
- New pods could not be scheduled temporarily
- Service degradation lasted approximately 35 minutes
- No data loss occurred

## Timeline
- **11:05 UTC** – Disk usage on a worker node began increasing rapidly
- **11:08 UTC** – Node condition changed to `DiskPressure`
- **11:10 UTC** – Node transitioned to `NotReady`
- **11:12 UTC** – Pods evicted from the affected node
- **11:15 UTC** – Alerts triggered for node health and pod evictions
- **11:18 UTC** – Incident declared and on-call engineer engaged
- **11:25 UTC** – Node cordoned and drained
- **11:30 UTC** – Workloads rescheduled to healthy nodes
- **11:40 UTC** – Service stabilized and alerts cleared

## Detection
The issue was detected through monitoring alerts indicating node health degradation and
pod eviction events, followed by service-level error alerts.

## Root Cause
The affected node ran out of available disk space due to accumulated container images and
logs. This triggered `DiskPressure`, causing the kubelet to mark the node as `NotReady`
and evict running pods.

## Resolution
- Cordoned and drained the affected node
- Rescheduled pods to healthy nodes
- Cleaned up unused container images and logs
- Increased disk capacity thresholds and monitoring

## Lessons Learned
- Disk usage on nodes must be monitored proactively
- Regular cleanup of unused images and logs is necessary
- Node-level alerts should trigger before `NotReady` state

## Action Items
- Add alerts for high disk usage on nodes
- Automate cleanup of unused container images
- Review node disk capacity planning

## Related Runbooks
- Handle Kubernetes Node NotReady
- Resolve Pod Scheduling Failures
- Debug OOMKilled Pods
