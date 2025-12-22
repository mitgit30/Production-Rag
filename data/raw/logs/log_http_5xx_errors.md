---
doc_type: log_doc
domain: sre
category: http_5xx
---

# HTTP 5xx Error Log Patterns

## Purpose
Common log patterns observed when applications return HTTP 5xx errors indicating
server-side failures.

---

## Common Log Patterns

### Internal server error
```text
500 Internal Server Error
Unhandled exception occurred
```
### Upstream timeout
```text
504 Gateway Timeout
Upstream server did not respond in time
```
### Service unavailable
```text
503 Service Unavailable
The service is temporarily unavailable
```
### Bad gateway
```text
502 Bad Gateway
Received invalid response from upstream server
```
Typical Causes:
-Application crashes or unhandled exceptions
-Database connectivity issues
-Resource exhaustion (CPU, memory)
-Network latency or failures

Next Steps:-
-Check application logs for errors
-Review database and external service connectivity
-Monitor resource usage on the server
-Refer to the HTTP 5xx Errors runbook

