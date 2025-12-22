---
incident_id: INC-006
service: checkout-service
environment: prod
severity: critical
owner: platform-engineering
doc_type: incident
domain: sre
---

# INC-006: External Payment Gateway Outage

## Summary
On 2024-08-05, the `checkout-service` experienced widespread request failures due to an
outage in a third-party payment gateway used for transaction processing. The external
dependency became unavailable, causing checkout attempts to fail until mitigation and
degraded-mode handling were applied.

## Impact
- Checkout and payment processing failed for a majority of users
- Increased HTTP 5xx error rates on checkout endpoints
- Revenue-impacting customer transactions were blocked
- No internal data loss occurred

## Timeline
- **18:40 UTC** – Increase in payment request failures observed
- **18:42 UTC** – Alerts triggered for elevated 5xx errors on checkout-service
- **18:45 UTC** – Incident declared and on-call engineer engaged
- **18:48 UTC** – Logs confirmed timeouts to external payment gateway
- **18:52 UTC** – External provider status page reported an active outage
- **18:55 UTC** – Fallback and degraded-mode logic enabled
- **19:05 UTC** – Error rates reduced and service partially restored
- **19:30 UTC** – External provider recovered and normal operations resumed

## Detection
The incident was detected through application monitoring alerts indicating increased
HTTP 5xx errors and timeouts on payment-related API calls, followed by confirmation from
the external provider’s status page.

## Root Cause
The third-party payment gateway experienced an outage in one of its regions, resulting
in failed API calls from the checkout-service. The service initially lacked aggressive
fallback behavior, amplifying user-facing errors.

## Resolution
- Enabled degraded-mode behavior to bypass non-critical payment flows
- Applied temporary request throttling to reduce error amplification
- Communicated incident status to stakeholders and support teams
- Monitored recovery of the external dependency

## Lessons Learned
- External dependencies are a single point of failure without isolation
- Fallback and circuit breaker mechanisms reduce customer impact
- Dependency health should be continuously monitored

## Action Items
- Implement circuit breakers for all external payment calls
- Add automated fallback strategies for checkout flows
- Improve alerting for external dependency latency and failures

## Related Runbooks
- Handle External Dependency Outage
- Handle HTTP 5xx Error Spikes
- Incident Response and Escalation
