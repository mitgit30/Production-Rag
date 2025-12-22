---
service: generic
environment: prod
severity: high
owner: platform-engineering
doc_type: runbook
domain: sre
---

# Investigate Database Connection Exhaustion

## Purpose
This runbook describes how to diagnose and mitigate issues caused by database connection
exhaustion, where applications are unable to acquire new database connections, leading to
timeouts, errors, or service outages.

## When to Use
- Application logs show database connection timeout errors
- Database reports maximum connections reached
- Increased request latency or HTTP 5xx errors related to database access
- Alerts indicate connection pool saturation

## When NOT to Use
- During planned database maintenance or migrations
- If database errors are confirmed to be unrelated to connection limits
- Without incident awareness in production environments

## Preconditions
- You are the on-call engineer
- An incident ticket has been created (for production)
- You have access to the Kubernetes cluster
- You have visibility into database metrics or logs

## Impact
- Requests depending on the database may fail
- Increased latency across services
- Potential cascading failures in dependent systems

---

## Diagnostic Steps (Recommended)

### 1. Confirm database-related errors
Inspect application logs for connection-related failures.

```bash
kubectl logs <pod_name> -n <namespace>
```
Look for errors such as:
- "Too many connections"
- "Connection timeout"

### 2. Identify affected services and pods
Check which services or pods are reporting database connection issues.

```bash
kubectl get pods -n <namespace> | grep <service_name>
```

### 3. Analyze database metrics
Access your database monitoring tool (e.g., Datadog, New Relic) to check:
- Current number of active connections
- Maximum allowed connections
- Connection pool usage statistics

### 4. Check application connection pool settings
Review the configuration of your application's database connection pool (e.g., max connections, idle timeout).
### 5. Review recent deployments or changes
Check if any recent deployments or configuration changes could have affected connection usage.

```bash
kubectl rollout history deployment/<deployment_name> -n <namespace>
```

### Comman causes and fixes

Connection Pool Too Small:
- Cause: The application’s connection pool is not sized appropriately for the workload.
- Fix: Increase the maximum number of connections in the application configuration.

Connection Leaks:
- Cause: Connections are not being released back to the pool after use.
- Fix: Review application code to ensure connections are properly closed after use.

Database Limits:
- Cause: The database has a low maximum connection limit.
- Fix: Increase the maximum connections allowed on the database server.
- Cause: A sudden spike in traffic has overwhelmed the connection pool.

