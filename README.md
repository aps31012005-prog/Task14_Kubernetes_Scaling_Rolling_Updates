# Task 14: Kubernetes Scaling and Rolling Updates

## 1. Project Overview

This project demonstrates the scaling and deployment update capabilities of Kubernetes using a containerized deep learning application.

The application consists of a Flask-based backend API and a Streamlit-based frontend. Kubernetes is used to manage application replicas, perform rolling updates, monitor resource utilization, and verify application availability.

---

## 2. Objective

The objective of this task is to implement scalability and deployment update strategies using Kubernetes.

The major objectives are:

* Scale application replicas using Kubernetes.
* Configure and perform rolling updates.
* Monitor deployment and pod status.
* Monitor CPU and memory utilization.
* Validate application availability after scaling and updates.
* Verify the stability of the deployed application.

---

## 3. Technologies Used

* Python
* Flask
* Streamlit
* Docker
* Kubernetes
* Minikube
* kubectl
* Kubernetes Metrics Server
* CIFAR-10 Deep Learning Model

---

## 4. Project Structure

```text
Task14_Kubernetes_Scaling_Rolling_Updates/
│
├── flask-deployment.yaml
├── flask-service.yaml
├── streamlit-deployment.yaml
├── streamlit-service.yaml
├── README.md
│
└── screenshots/
    ├── 01_task14_cluster_status.png
    ├── 02_task14_initial_deployment_status.png
    ├── 03_flask_api_scaled_to_3_replicas.png
    ├── 04_flask_scaling_rollout_status.png
    ├── 05_flask_api_availability_after_scaling.png
    ├── 06_task14_resource_utilization.png
    ├── 07_task14_rolling_update_configuration.png
    ├── 08_task14_rolling_update_execution.png
    ├── 09_task14_rollout_history.png
    ├── 10_task14_final_deployment_pod_status.png
    ├── 11_task14_resource_utilization_after_update.png
    ├── 12_task14_api_availability_after_update.png
    ├── 13_task14_services_verification.png
    ├── 14_task14_streamlit_application.png
    ├── 15_task14_frog_prediction_after_update.png
    ├── 16_task14_final_kubernetes_verification.png
    └── 17_task14_final_resource_and_rollout_status.png
```

---

## 5. Kubernetes Cluster Setup

Minikube was used to create a local Kubernetes cluster.

The cluster was started using the Docker driver:

```bash
minikube start --driver=docker
```

The Kubernetes node was verified using:

```bash
kubectl get nodes
```

The node was successfully reported as `Ready`.

---

## 6. Initial Deployment Verification

The existing Flask API and Streamlit frontend deployments were verified using:

```bash
kubectl get deployments
```

The deployed applications were running successfully before performing scaling operations.

Pods were checked using:

```bash
kubectl get pods -o wide
```

This confirmed that the application pods were in the `Running` state.

---

## 7. Application Scaling

The Flask API deployment was initially configured with two replicas.

The deployment was scaled to three replicas using:

```bash
kubectl scale deployment flask-api --replicas=3
```

The result was verified using:

```bash
kubectl get deployments
kubectl get pods -o wide
```

After scaling, the Flask deployment reported:

```text
flask-api   3/3   3   3
```

Three Flask API pods were running successfully.

This demonstrates horizontal scaling at the Kubernetes deployment level.

---

## 8. Scaling Availability Verification

After scaling the Flask API, its service availability was tested from inside the Kubernetes cluster.

The following command was used:

```bash
kubectl run flask-test --rm -it --restart=Never --image=curlimages/curl -- curl -s http://flask-api-service:5000/
```

The API returned the following response:

```json
{
  "endpoint": "/predict",
  "message": "CIFAR-10 Flask Prediction API is running",
  "method": "POST"
}
```

This verified that the Flask service remained accessible after scaling.

---

## 9. Resource Monitoring

Kubernetes Metrics Server was enabled to monitor CPU and memory utilization.

The Metrics Server was enabled using:

```bash
minikube addons enable metrics-server
```

Resource utilization was monitored using:

```bash
kubectl top pods
```

After scaling, the three Flask API replicas showed stable resource utilization.

Example observed values:

```text
Flask Replica 1: 1m CPU, 252Mi Memory
Flask Replica 2: 1m CPU, 252Mi Memory
Flask Replica 3: 1m CPU, 252Mi Memory
```

The resource monitoring results were used to observe the resource consumption of individual application replicas.

---

## 10. Rolling Update Configuration

The Flask deployment was configured to use the Kubernetes `RollingUpdate` strategy.

The deployment configuration included:

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 1
    maxSurge: 1
```

The deployment was maintained at three replicas during the update.

The `maxUnavailable` and `maxSurge` settings control how many pods can be unavailable or additionally created during the update process.

---

## 11. Rolling Update Implementation

A pod-template configuration change was introduced using an environment variable:

```yaml
env:
  - name: TASK14_VERSION
    value: "v2"
```

This change modified the pod template and triggered a new Kubernetes ReplicaSet while keeping the same application image.

The updated deployment was applied using:

```bash
kubectl apply -f flask-deployment.yaml
```

The rollout was monitored using:

```bash
kubectl rollout status deployment/flask-api
```

The rollout completed successfully.

---

## 12. ReplicaSet Verification

The ReplicaSets created for the Flask deployment were checked using:

```bash
kubectl get rs
```

The latest ReplicaSet contained three ready replicas, while previous ReplicaSets had been scaled down.

This confirmed that Kubernetes performed the rolling update by transitioning from the previous ReplicaSet to the new ReplicaSet.

---

## 13. Rollout History

The deployment rollout history was checked using:

```bash
kubectl rollout history deployment/flask-api
```

Multiple deployment revisions were recorded, confirming that Kubernetes maintained deployment revision history.

---

## 14. Final Deployment Verification

The final deployment state was checked using:

```bash
kubectl get deployments
kubectl get pods -o wide
```

The final state showed:

```text
flask-api   3/3   3   3
streamlit   2/2   2   2
```

All Flask API replicas were in the `Running` state and ready to receive requests.

---

## 15. Service Verification

The Kubernetes services were verified using:

```bash
kubectl get services
```

The Flask API was exposed through a ClusterIP service on port `5000`.

The Streamlit frontend was exposed through a NodePort service on port `8501`.

The Streamlit service was accessed using:

```bash
minikube service streamlit-service --url
```

The application opened successfully in the web browser.

---

## 16. Application Prediction Verification

The Streamlit application was tested by uploading a CIFAR-10 Frog image.

The application successfully returned:

```text
Predicted Class: Frog
Confidence: 99.01%
```

This verified that the frontend, backend API, and deep learning prediction workflow remained functional after the Kubernetes scaling and rolling update operations.

---

## 17. Results and Observations

The Kubernetes scaling operation successfully increased the Flask API replicas from two to three.

The rolling update was completed successfully using the configured `RollingUpdate` strategy.

Resource utilization was monitored using Kubernetes Metrics Server and `kubectl top pods`.

The Flask API remained accessible after scaling and after the rolling update.

The Streamlit frontend remained accessible and successfully performed image classification after the deployment update.

The final Kubernetes cluster showed all required application replicas in the `Running` and `Ready` state.

---

## 18. Conclusion

This task successfully demonstrated Kubernetes scaling and rolling update capabilities for a containerized deep learning application.

The Flask API was horizontally scaled to three replicas, resource utilization was monitored, and a rolling update was successfully performed without interrupting application availability.

The final verification confirmed that the Flask backend and Streamlit frontend remained operational after the scaling and update operations.
