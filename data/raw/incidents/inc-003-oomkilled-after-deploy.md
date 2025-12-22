---
incident_id: INC-003
service: order-service
environment: prod
severity: high
owner: platform-engineering
doc_type: incident
domain: sre
---

# INC-003: OOMKilled Pods After Deployment

## Summary
On 2024-05-10, the `order-service` experienced repeated pod restarts due to `OOMKilled`
events shortly after a new version was deployed to production. The issue resulted in
service instability and increased error rates.

## Impact
- Order creation requests failed intermittently
- Increased HTTP 5xx error rates
- Service availability was degraded for approximately 30 minutes
- No data corruption or loss occurred

## Timeline
- **09:40 UTC** – New version of `order-service` deployed to production
- **09:43 UTC** – Pods began restarting with `OOMKilled` status
- **09:45 UTC** – Alerts triggered for pod restarts and memory usage
- **09:47 UTC** – Incident declared and on-call engineer engaged
- **09:52 UTC** – Memory limits identified as insufficient for new release
- **09:56 UTC** – Deployment rolled back to previous stable version
- **10:10 UTC** – Pods stabilized and service health restored

## Detection
The issue was detected through monitoring alerts indicating repeated pod restarts and
memory limit violations shortly after the deployment.

## Root Cause
The new application release introduced increased in-memory caching, significantly raising
memory consumption. The existing memory limits were not updated accordingly, causing the
containers to exceed their limits and be terminated by the kubelet.

## Resolution
- Rolled back the deployment to the previous stable version
- Verified pod stability and memory usage post-rollback
- Disabled the newly introduced caching feature temporarily

## Lessons Learned
- Memory usage changes must be evaluated before production deployments
- Resource limits should be reviewed as part of release planning
- Load and memory testing should be included in pre-release checks

## Action Items
- Profile memory usage for future releases
- Update deployment resource limits based on observed usage
- Add alerts for rapid memory growth after deployment

## Related Runbooks
- Debug OOMKilled Pods
- Roll Back a Faulty Deployment
