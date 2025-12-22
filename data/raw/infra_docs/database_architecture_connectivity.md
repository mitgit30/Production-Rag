---
service: platform
environment: prod
owner: platform-engineering
doc_type: infra_doc
domain: sre
---

# Database Architecture and Connectivity

## Purpose
This document explains how application services connect to the database layer, how
connections are managed, and how database-related limits impact system behavior.

It provides architectural context for diagnosing database performance issues and
connection exhaustion incidents.

---

## Database Architecture Overview
Production services rely on a shared, managed relational database.

Key characteristics:
- Centralized database cluster
- Multiple application services connect concurrently
- High availability provided by the database platform
- Read/write traffic served through a primary endpoint

The database is a critical shared dependency across services.

---

## Application Connectivity Model
Each application pod establishes database connections using an internal connection pool.

Typical flow:
Application Pod → Connection Pool → Database Endpoint

Connections are opened at startup and reused across requests.

---

## Connection Pooling
Connection pooling is used to:
- Reduce connection creation overhead
- Limit total open connections
- Improve performance under load

Common pool parameters include:
- Maximum pool size
- Minimum idle connections
- Connection timeout
- Idle timeout

Incorrect pool sizing can cause:
- Connection starvation
- Increased latency
- Request failures

---

## Database Connection Limits
Databases enforce a maximum number of concurrent connections.

If the limit is reached:
- New connection requests are rejected
- Applications experience timeouts
- Error rates increase rapidly

Scaling application pods increases the total number of potential connections.

---

## Traffic and Scaling Implications
Horizontal scaling affects database load:
- More pods → more connection pools
- More pools → more open connections

Autoscaling application pods does **not** automatically scale database capacity.

Database limits must be considered when tuning:
- HPA thresholds
- Replica counts
- Pool sizes

---

## Common Failure Modes

### Connection Exhaustion
Occurs when:
- Pool size is too large
- Too many pods are running
- Traffic spikes unexpectedly

Symptoms:
- Database timeout errors
- HTTP 5xx responses
- Increased request latency

---

### Long-Running Queries
Queries that hold connections for extended periods can block new requests.

Common causes:
- Missing indexes
- Inefficient queries
- Large result sets

---

### Connection Leaks
Connections are not returned to the pool due to application bugs or misconfiguration.

This gradually exhausts available connections.

---

## Observability and Monitoring
Key metrics to monitor:
- Active and idle connections
- Connection acquisition latency
- Query execution time
- Database CPU and memory usage

Logs should be reviewed for:
- Connection timeout errors
- Pool exhaustion warnings

---

## Design Guidelines
Recommended practices:
- Keep connection pools conservative
- Scale database capacity separately from application pods
- Monitor connection usage continuously
- Test behavior under traffic spikes
- Prefer backpressure over unlimited retries

Database stability is critical for overall platform reliability.

---

## Related Runbooks
- Investigate Database Connection Exhaustion
- Handle HTTP 5xx Error Spikes
- Restart a Kubernetes Service Safely

## Related Incidents
- INC-004: Database Connection Exhaustion
