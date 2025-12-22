---
incident_id: INC-002
service: api-gateway
environment: prod
severity: medium
owner: platform-engineering
doc_type: incident
domain: sre
---

# INC-002: High CPU Utilization Causing API Latency Spike

## Summary
On 2024-04-03, the `api-gateway` service experienced a significant increase in request
latency due to sustained high CPU utilization across multiple pods. The issue was
triggered by a sudden traffic spike combined with insufficient autoscaling configuration.

## Impact
- Increased API response latency for end users
- Intermittent request timeouts
- No complete service outage occurred
- No data loss was observed

## Timeline
- **14:20 UTC** – Traffic spike detected on API gateway
- **14:22 UTC** – CPU utilization crossed alert thresholds
- **14:25 UTC** – Latency alerts triggered
- **14:27 UTC** – Incident declared and on-call engineer engaged
- **14:32 UTC** – High CPU usage confirmed across gateway pods
- **14:36 UTC** – Deployment scaled horizontally
- **14:45 UTC** – Latency stabilized and CPU usage returned to normal

## Detection
The issue was detected through monitoring alerts for high CPU utilization and increased
request latency on the API gateway service.

## Root Cause
The Horizontal Pod Autoscaler (HPA) was configured with conservative scaling limits and
did not react quickly enough to the sudden increase in incoming traffic. As a result,
existing pods became CPU-saturated, leading to slower request processing.

## Resolution
- Manually scaled the deployment to increase replica count
- Adjusted HPA target CPU utilization and scaling limits
- Monitored metrics to ensure stable performance

## Lessons Learned
- Autoscaling thresholds must account for traffic burst patterns
- CPU utilization should be monitored alongside latency metrics
- HPA configurations should be reviewed regularly

## Action Items
- Re-evaluate HPA configuration for API gateway
- Add proactive alerts for sustained CPU saturation
- Conduct load testing to validate scaling behavior

## Related Runbooks
- Investigate High CPU Utilization
- Handle HTTP 5xx Error Spikes
