---
doc_type: log_doc
domain: sre
category: database
---

# Database Connection Error Log Patterns

## Purpose
Common log patterns observed when applications fail to acquire or use database
connections successfully.

---

## Common Log Patterns

### Connection pool exhausted
```text
ERROR: connection pool exhausted
Timeout acquiring database connection
```
### Authentication failure
```text
ERROR: authentication failure
FATAL: password authentication failed for user "dbuser"
```
### Network connectivity issue
```text
ERROR: could not connect to server: Connection timed out
Is the server running on host "db.example.com" 
and accepting TCP/IP connections on port 5432?
```
### SQL syntax error
```text
ERROR: syntax error at or near "FROMM"
LINE 1: SELECT * FROMM users WHERE id = 1;
                     ^
```
Typical Causes:
-Exhausted connection pool due to high load
-Invalid database credentials
-Network issues between application and database
-Malformed SQL queries

Next Steps:-
-Check database connection pool settings
-Verify database credentials and permissions
-Inspect network connectivity and firewall rules
-Review and test SQL queries for correctness
-Refer to the Database Connection Errors runbook
