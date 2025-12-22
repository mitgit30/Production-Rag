---
incident_id: INC-004
service: user-service
environment: prod
severity: high
owner: platform-engineering
doc_type: incident
domain: sre
---

# INC-004: Database Connection Exhaustion

## Summary
On 2024-06-02, the `user-service` experienced elevated error rates and request timeouts
due to database connection exhaustion. The service was unable to acquire new database
connections, leading to partial unavailability.

## Impact
- User profile and authentication requests failed intermittently
- Increased HTTP 5xx error rates across dependent services
- Degraded user experience for approximately 40 minutes
- No data loss or corruption occurred

## Timeline
- **16:10 UTC** – Increase in request latency observed for user-service
- **16:12 UTC** – Alerts triggered for database connection errors
- **16:15 UTC** – Incident declared and on-call engineer engaged
- **16:20 UTC** – Database reported max connections reached
- **16:25 UTC** – Connection pool misconfiguration identified
- **16:30 UTC** – Deployment scaled and pods restarted
- **16:50 UTC** – Connection usage stabilized and service recovered

## Detection
The issue was detected through application logs indicating database connection timeouts
and monitoring alerts showing saturation of the database connection pool.

## Root Cause
A recent configuration change reduced the maximum size of the application’s database
connection pool. During a traffic increase, connections were exhausted quickly, preventing
new requests from being served.

## Resolution
- Increased the application connection pool size
- Restarted affected pods to release stuck connections
- Scaled the deployment to distribute database load
- Monitored database metrics to confirm recovery

## Lessons Learned
- Connection pool configurations must be reviewed carefully
- Traffic patterns should be considered when tuning database settings
- Database limits should be monitored alongside application metrics

## Action Items
- Add alerts for early warning of connection pool saturation
- Document recommended connection pool settings
- Include database load testing in pre-release checks

## Related Runbooks
- Investigate Database Connection Exhaustion
- Handle HTTP 5xx Error Spikes
- Restart a Kubernetes Service Safely
