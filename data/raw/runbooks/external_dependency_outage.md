---
service: generic
environment: prod
severity: high
owner: platform-engineering
doc_type: runbook
domain: sre
---

# Handle External Dependency Outage

## Purpose
This runbook describes how to detect, investigate, and mitigate outages or degradation
caused by failures in external dependencies such as third-party APIs, payment gateways,
identity providers, or managed services.

## When to Use
- Increased error rates or timeouts when calling external services
- Alerts indicate dependency failures
- Service functionality relying on third-party systems is degraded
- External provider reports an outage or incident

## When NOT to Use
- When failures are caused by internal service issues
- During planned maintenance of the external dependency
- Without incident awareness in production environments

## Preconditions
- You are the on-call engineer
- An incident ticket has been created (for production)
- You have access to application logs and metrics
- You know which external dependency is involved

## Impact
- Partial or complete service degradation
- Increased latency or request failures
- Potential revenue or user experience impact

---

## Diagnostic Steps (Recommended)

### 1. Confirm dependency-related errors
Inspect application logs for errors related to external calls.

```bash
kubectl logs <pod_name> -n <namespace>
```
### 2. Identify affected services and pods
Check which services or pods are reporting issues with the external dependency.

```bash
kubectl get pods -n <namespace> | grep <service_name>
```
### 3. Analyze metrics and traces
Review application metrics and distributed traces to identify patterns of failure.

```bash
kubectl top pods -n <namespace>
```
Look for:
- Increased error rates
- Elevated latency for external calls
- Timeouts or circuit breaker activations

### 4. Check external dependency status
Visit the status page or dashboard of the external service to check for reported outages.
- [External Service Status Page](https://status.example.com)
### 5. Review recent changes
Check if any recent deployments or configuration changes could have affected interactions with the external dependency.

### Common causes and fixes 

External Service Outage
causes- The external service is experiencing an outage.
fixes- Monitor the external service status page for updates. Communicate with the provider if necessary.

API Rate Limiting
causes- The service has exceeded its allowed API request limits.
fixes- Implement exponential backoff and retry logic. Consider requesting a rate limit increase from the provider.

Network Issues
causes- Network connectivity problems between your service and the external dependency.
fixes- Check network configurations, firewalls, and DNS settings. Work with your network team to resolve connectivity issues.






