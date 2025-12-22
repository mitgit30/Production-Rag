---
doc_type: log_doc
domain: sre
category: crashloop
---

# CrashLoopBackOff Log Patterns

## Purpose
This document lists common log patterns observed when a Kubernetes pod repeatedly
restarts and enters the `CrashLoopBackOff` state.

---

## Common Log Patterns

### Application crash on startup
```text
Application failed to start
Process exited with code 1
```
Meaning:
The application crashed during initialization due to a startup error.

### Missing environment variable
```text
Error: ENV_VAR_NAME not set
at com.example.Main.main(Main.java:15)
``` 
Meaning:
The application tried to access an environment variable that was not set.

### Port binding failure
```text
Error: Address already in use
at java.net.PlainSocketImpl.bind(PlainSocketImpl.java:123)
```
Meaning:
The application attempted to bind to a port that is already in use.

Typical Causes:
-Misconfigured ConfigMaps or Secrets
-Invalid startup commands
-Breaking configuration changes
-Missing environment variables

Next Steps:-
-Inspect pod events using kubectl describe pod
-Review recent configuration changes
-Refer to the CrashLoopBackOff runbook
