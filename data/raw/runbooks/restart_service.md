---
service: generic
environment: prod
severity: medium
owner: platform-engineering
doc_type: runbook
domain: sre
---

# Restart a Kubernetes Service Safely

## Purpose
This runbook describes the safe procedure to restart a Kubernetes-based service in production
when the service is unresponsive, degraded, or exhibiting abnormal behavior.

## When to Use
- Service health checks are failing
- Elevated error rates or timeouts
- Pods are running but not responding correctly
- Restart is recommended as a mitigation step during an incident

## When NOT to Use
- During an active deployment or rollout
- When the root cause is known to be data corruption
- Without incident awareness in production

## Preconditions
- You are the on-call engineer
- An incident ticket is created (for production)
- You have cluster access
- You have confirmed no active deployments are running

## Impact
- Brief service disruption may occur
- Existing connections may be dropped
- Traffic may be rerouted during restart

## Steps

### 1.Rolling restart the deployment
This method is recommended for triggering a restart when you haven’t made changes to the deployment manifest but want the pods to refresh (e.g., to pick up new secrets, reinitialize a process, etc.). A rollout restart will kill one pod at a time, and then new pods will be scaled up. 

This method works on Kubernetes and kubectl 1.15 and newer, which includes all currently supported Kubernetes releases.

```bash
kubectl rollout restart deployment <deployment_name> -n <namespace>
```
This command tells Kubernetes to restart the Deployment, which causes all the associated pods to be replaced one by one.

### 2. Scale deployment replicas
Scaling a Deployment down to 0 replicas and then back up forces Kubernetes to terminate all existing pods and create fresh ones. This is essentially a “restart” because the new pods are instantiated from the Deployment’s pod template.

However, this method will introduce an outage and is not recommended. If downtime is not an issue, it can be used as a quicker alternative to the kubectl rollout restart  method (your pod may have to run through a lengthy continuous integration/deployment process before it is redeployed).

If there is no YAML file associated with the deployment, you can set the number of replicas to 0.

```bash
kubectl scale deployment <deployment_name> --replicas=0 -n <namespace>
```
Pod status can be checked during the scaling using:

```bash
kubectl get pods -n <namespace>
```

### 3.Delete an individual pod
If the pod is managed by a Deployment, ReplicaSet, or StatefulSet, you can safely delete the pod with kubectl delete pod since Kubernetes will automatically recreate it.

Each pod can be deleted individually if required:

```bash
kubectl delete pod <pod_name> -n <namespace>
```
### 4. Force replace a Pod
The pod you want to replace can be retrieved using the kubectl get pod to get the YAML statement of the currently running pod and passed it to the kubectl replace command with the --force flag specified in order to achieve a restart. This is useful if no YAML file is available and the pod has been started.
```bash
kubectl get pod <pod_name> -n <namespace> -o yaml | kubectl replace --force -f -
```
This method only works for manually created pods or those not controlled by higher-level objects like Deployments, StatefulSets, etc. If you try this on a pod that’s part of a Deployment, Kubernetes might immediately recreate a second pod (since the Deployment notices one went missing), leading to duplicates or conflicts.
### 5.Update environment variables
A simple and effective way to restart pods in Kubernetes is by using the kubectl set env command to update an environment variable in a Deployment. Kubernetes triggers a rolling restart whenever the pod template changes, and changing or adding an environment variable is enough to make that happen.

The example below sets the environment variable DEPLOY_DATE to the date specified, causing the pod to restart.

```bash
kubectl set env deployment <deployment name> -n <namespace> DEPLOY_DATE="$(date)"
```
This method is safe, causes no downtime (thanks to the rolling update), and is perfect for triggering restarts after updating ConfigMaps and Secrets or refreshing the application state without changing the app code or deployment image. It’s also a popular approach in automation scripts and CI/CD pipelines.

Verification

After performing a restart, verify the following:-
-All pods reach Running and Ready state
-Service health checks return successful responses
-Error rates and latency return to baseline
-No new alerts are triggered

Escalation
Escalate the incident if:
-The restart does not resolve the issue
-New issues arise post-restart
-Review logs and metrics to diagnose the problem
-Consider alternative mitigation strategies