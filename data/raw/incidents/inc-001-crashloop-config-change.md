---
incident_id: INC-001
service: payment-service
environment: prod
severity: high
owner: platform-engineering
doc_type: incident
domain: sre
---

# INC-001: CrashLoopBackOff After Configuration Change

## Summary
On 2024-03-12, the `payment-service` experienced repeated pod restarts and entered a
`CrashLoopBackOff` state shortly after a configuration change was applied in production.
The incident resulted in partial service unavailability and increased error rates.

## Impact
- Payment API requests failed intermittently
- Increased HTTP 5xx error rates
- Customer checkout attempts were impacted
- No data loss occurred

## Timeline
- **10:05 UTC** – Configuration update applied via ConfigMap
- **10:07 UTC** – Pods began restarting and entered `CrashLoopBackOff`
- **10:10 UTC** – Monitoring alerts triggered for pod restarts and error rates
- **10:12 UTC** – Incident declared and on-call engineer engaged
- **10:18 UTC** – Root cause identified as misconfigured environment variable
- **10:22 UTC** – Configuration reverted and pods restarted
- **10:30 UTC** – Service stabilized and error rates returned to normal

## Detection
The issue was detected through automated monitoring alerts indicating repeated pod
restarts and elevated HTTP 5xx responses for the payment API.

## Root Cause
A required environment variable was removed during a ConfigMap update. The application
failed to start without this configuration, causing the container to exit immediately
and enter a `CrashLoopBackOff` state.

## Resolution
- Reverted the ConfigMap to the previous stable version
- Restarted the affected Deployment to apply the corrected configuration
- Verified successful pod startup and service health

## Lessons Learned
- Configuration changes should be validated before production rollout
- Missing required environment variables can cause immediate startup failures
- ConfigMap changes should be tested in staging environments first

## Action Items
- Add configuration validation checks during startup
- Improve pre-deployment configuration review process
- Add alerts for configuration-related startup failures

## Related Runbooks
- Debug Pods in CrashLoopBackOff
- Restart a Kubernetes Service Safely
