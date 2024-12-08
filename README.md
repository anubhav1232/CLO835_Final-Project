# **CLO835 Final Project: Flask App Deployment on AWS EKS**

This repository contains the codebase and Kubernetes manifests for deploying a cloud-native Flask-based Employee Management Application on an Amazon Elastic Kubernetes Service (EKS) cluster. The application integrates with a MySQL database and dynamically retrieves a background image from a private Amazon S3 bucket. This project showcases the use of Kubernetes objects, CI/CD pipelines, and cloud infrastructure.

---

## **Team Members**
- **Anubhav Thakur** ([GitHub: @anubhav1232](https://github.com/anubhav1232))
- **Parikshek Gaju** ([GitHub: @Parikshek](https://github.com/Parikshek))
- **Vijay Kumar** ([GitHub: @booleandigit](https://github.com/booleandigit))

---

## **Project Objectives**
1. Deploy a Flask application and a MySQL database on AWS EKS using Kubernetes.
2. Integrate the application with AWS services, including Amazon S3 for assets and Amazon EBS for persistent storage.
3. Use Kubernetes resources such as ConfigMaps, Secrets, StatefulSets, and PersistentVolumeClaims to manage the deployment.
4. Set up CI/CD pipelines using GitHub Actions for automated Docker image builds and pushes to Amazon Elastic Container Registry (ECR).
5. Demonstrate advanced Kubernetes functionalities such as Horizontal Pod Autoscaling (HPA) and dynamic storage provisioning.

---

## **Prerequisites**
Before proceeding, ensure the following tools and configurations are in place:
- An AWS account with sufficient permissions for EKS, ECR, and S3.
- **Installed Tools**:
  - `eksctl` for cluster management.
  - `kubectl` for Kubernetes resource management.
  - `Docker` for containerization.
- **AWS CLI**: Configured with access keys for your account.
- A private Amazon S3 bucket to store the application’s background image.

---

## **Deployment Steps**

### **1. Build and Push Docker Images**
1. Build the Docker images for the Flask application and MySQL database:
   ```bash
   docker build -t flask-app -f application/Dockerfile application/
   docker build -t mysql-app -f application/Dockerfile_mysql application/
   ```
2. Push the images to Amazon ECR:
   ```bash
   docker tag flask-app <ECR_REPO_URL>/flask-app:latest
   docker push <ECR_REPO_URL>/flask-app:latest

   docker tag mysql-app <ECR_REPO_URL>/mysql-app:latest
   docker push <ECR_REPO_URL>/mysql-app:latest
   ```

---

### **2. Create EKS Cluster**
1. Define your cluster configuration in `eks/eks-cluster.yaml`.
2. Create the EKS cluster using `eksctl`:
   ```bash
   eksctl create cluster -f eks/eks-cluster.yaml
   ```

---

### **3. Deploy Kubernetes Resources**
1. Deploy the **namespace** and **storage configurations**:
   ```bash
   kubectl apply -f k8s/namespace.yaml
   kubectl apply -f k8s/storageclass.yaml
   kubectl apply -f k8s/persistent-volume-claim.yaml
   ```

2. Deploy **MySQL database**:
   ```bash
   kubectl apply -f k8s/secret-db-credentials.yaml
   kubectl apply -f k8s/service-mysql.yaml
   kubectl apply -f k8s/statefulset.yaml
   kubectl apply -f k8s/deployment-mysql.yaml
   ```

3. Deploy the **Flask application**:
   ```bash
   kubectl apply -f k8s/config-map.yaml
   kubectl apply -f k8s/deployment-flask.yaml
   kubectl apply -f k8s/service-flask.yaml
   ```

4. Set up RBAC for the cluster:
   ```bash
   kubectl apply -f k8s/role-clusterrole.yaml
   kubectl apply -f k8s/rolebinding.yaml
   kubectl apply -f k8s/serviceaccount.yaml
   ```

---

### **4. Verify the Deployment**
1. Check all resources in the namespace:
   ```bash
   kubectl get all -n final
   ```
2. Access the Flask application using the external LoadBalancer URL:
   ```bash
   kubectl get service flask-service -n final
   ```

---

### **5. Test Application Functionality**
1. Log into the MySQL database pod and verify data persistence:
   ```bash
   kubectl exec -it mysql-0 -n final -- mysql -u root -p
   ```
   Run SQL queries to test:
   ```sql
   USE employees;
   INSERT INTO employee VALUES ('12345','Anubhav','Vijay','Parikshek','local');
   SELECT * FROM employee;
   ```

2. Test application functionality in the browser:
   - Add and retrieve employee records.
   - Confirm that the application fetches the background image from the S3 bucket.

3. Test dynamic storage provisioning:
   - Delete the MySQL pod:
     ```bash
     kubectl delete pod mysql-0 -n final
     ```
   - Confirm data persistence after the pod restarts.

---

### **6. Configure Horizontal Pod Autoscaling (HPA)**
1. Apply the HPA configuration:
   ```bash
   kubectl apply -f k8s/hpa.yaml
   ```
2. Simulate traffic to trigger autoscaling:
   ```bash
   while true; do curl -s <LOAD_BALANCER_URL> > /dev/null; echo "Hit Successful"; done
   ```

---

### **7. Update Background Image**
1. Update the background image URL in `k8s/config-map.yaml`.
2. Redeploy the ConfigMap and Flask application:
   ```bash
   kubectl apply -f k8s/config-map.yaml -n final
   kubectl delete deployment flask-app -n final
   kubectl apply -f k8s/deployment-flask.yaml
   ```

3. Verify that the updated image appears on the application homepage.

---

## **Key Features**
1. **Dynamic Resource Allocation**: Amazon EBS volumes and Kubernetes PersistentVolumes dynamically provisioned for the MySQL database.
2. **CI/CD Integration**: GitHub Actions configured for automated Docker image builds and pushes.
3. **Auto-scaling**: HPA configuration to scale application pods based on CPU usage.
4. **Secure Configuration Management**: ConfigMaps and Secrets used to manage application configurations and credentials.
5. **Data Persistence**: Ensured through StatefulSets and PersistentVolumes.

---

## **Future Enhancements**
- Add SSL/TLS termination using an Ingress controller.
- Monitor resource usage with Prometheus and Grafana.
- Implement end-to-end CI/CD with automated deployments using FluxCD.

---