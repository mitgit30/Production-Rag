---
service: generic
environment: prod
severity: medium
owner: platform-engineering
doc_type: runbook
domain: sre
---

# Debug Failed CI/CD Deployment

## Purpose
This runbook describes how to investigate and resolve failures in CI/CD pipelines or
deployment stages that prevent applications from being built, tested, or deployed
successfully to Kubernetes environments.

## When to Use
- CI/CD pipeline fails during build, test, or deploy stages
- Deployment does not reach production or staging
- Rollout is blocked due to pipeline errors
- Alerts indicate failed or stalled deployments

## When NOT to Use
- During intentionally paused or manually approved deployments
- If failures are expected due to planned changes
- Without incident awareness in production environments

## Preconditions
- You are the on-call engineer
- An incident ticket has been created (for production)
- You have access to the CI/CD system (e.g., GitHub Actions, GitLab CI, Jenkins)
- You have access to the Kubernetes cluster

## Impact
- New application changes are not released
- Bug fixes or features are delayed
- Potential operational or business impact

---

## Diagnostic Steps (Recommended)

### 1. Identify the failing pipeline stage
Review the CI/CD pipeline execution and identify which stage failed.

Common stages:
- Build
- Test
- Security scans
- Deploy

Check logs and error messages in the CI/CD tool.

---

### 2. Review recent code or configuration changes
Determine whether recent commits introduced the failure.

- Application code changes
- Dockerfile updates
- Infrastructure or deployment manifest changes

---

### 3. Inspect build artifacts
If the build stage failed, verify:
- Dependency installation
- Compilation errors
- Test failures

Check logs for:
- Missing dependencies
- Version conflicts
- Test assertions

---

### 4. Validate container image build and push
Ensure the container image was built and pushed successfully.

- Verify image tag exists in the registry
- Confirm correct image name and version
- Check registry authentication

---

### 5. Investigate deployment stage failures
If deployment failed, inspect Kubernetes-related errors.

```bash
kubectl get deployments -n <namespace>
kubectl describe deployment <deployment_name> -n <namespace>
kubectl get events -n <namespace>
```

### 2. Check for common deployment issues
Look for:
- Insufficient resources (CPU, memory)
- Image pull errors
- Configuration or secret issues
- RBAC or permission errors

### 3. Review rollback or retry mechanisms
Check if the CI/CD tool attempted to roll back or retry the deployment.
- Verify rollback logs
- Confirm previous stable version is intact
```bash
kubectl rollout history deployment/<deployment_name> -n <namespace>
```

### 4. Review recent deployments or changes
Check if any recent deployments or configuration changes could have affected the deployment process.
```bash
kubectl rollout history deployment/<deployment_name> -n <namespace>
```

### Common causes and fixes
Misconfigured CI/CD Pipeline:
- Cause: Errors in pipeline configuration or scripts.
- Fix: Review and correct pipeline definitions or scripts.

Insufficient Permissions:
- Cause: CI/CD system lacks permissions to deploy to the cluster.
- Fix: Update RBAC roles or service accounts used by the CI/CD system.

Network or Registry Issues:
- Cause: Network problems or registry access issues.
- Fix: Verify network connectivity and registry credentials.

