---
doc_type: log_doc
domain: sre
category: oomkilled
---

# OOMKilled Log Patterns

## Purpose
Common log patterns seen when a Kubernetes pod is terminated due to exceeding its
configured memory limit (`OOMKilled`).

---

## Common Log Patterns

### Container killed by kernel
```text
Container killed due to OOMKilled
Exit code 137
```
### Java heap exhaustion
```text
java.lang.OutOfMemoryError: Java heap space
at com.example.MyClass.myMethod(MyClass.java:123)
```
### Python memory allocation failure
```text
MemoryError: Unable to allocate 2.00 GiB for an array with shape (1000000, 1000) and data type float64
```
### Node OOM event
```text
Node out of memory: Kill process 12345 (myapp) score 1000 or sacrifice child
```

Typical Causes:
-Memory limits set too low
-Memory leak in application
-Increased traffic or payload size
-New release with higher memory usage

Next Steps:-
-Check pod memory requests and limits
-Review memory usage metrics
-Scale pods or roll back deployment