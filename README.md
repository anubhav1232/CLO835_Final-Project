
# CLO835 Final Project: Flask App on EKS

This repository contains the code and Kubernetes manifests for deploying a Flask-based web application on Amazon EKS. The application retrieves a background image from a private S3 bucket and displays it on the homepage. The image URL and other configuration values are stored in a ConfigMap.

## Setup

### Prerequisites
- AWS Account with IAM permissions for EKS, ECR, S3, etc.
- eksctl installed
- kubectl installed
- Docker installed

### Steps

1. **Build and Push Docker Image**
   - Build the Docker image for the Flask app and push it to ECR.

2. **Create EKS Cluster**
   - Create the EKS cluster using `eksctl`.

3. **Deploy MySQL and Flask App**
   - Apply the Kubernetes manifests (`kubectl apply -f k8s/`) to deploy MySQL and the Flask app.

4. **Set up CI/CD with GitHub Actions**
   - Configure GitHub Actions to automatically build and push Docker images.

5. **Configure Flux for Automatic Deployment (Optional)**
   - Use Flux to sync Kubernetes manifests from GitHub.

### Accessing the Application

Once deployed, access the Flask app via the external LoadBalancer URL provided by the Kubernetes service.


```

# CLO835 Final Project: Flask App on EKS

This repository contains the code and Kubernetes manifests for deploying a Flask-based web application on Amazon EKS. The application retrieves a background image from a private S3 bucket and displays it on the homepage. The image URL and other configuration values are stored in a ConfigMap.

## Setup

### Prerequisites
- AWS Account with IAM permissions for EKS, ECR, S3, etc.
- eksctl installed
- kubectl installed
- Docker installed

### Steps

1. **Build and Push Docker Image**
   - Build the Docker image for the Flask app and push it to ECR.

2. **Create EKS Cluster**
   - Create the EKS cluster using `eksctl`.

3. **Deploy MySQL and Flask App**
   - Apply the Kubernetes manifests (`kubectl apply -f k8s/`) to deploy MySQL and the Flask app.

4. **Set up CI/CD with GitHub Actions**
   - Configure GitHub Actions to automatically build and push Docker images.

5. **Configure Flux for Automatic Deployment (Optional)**
   - Use Flux to sync Kubernetes manifests from GitHub.

### Accessing the Application

Once deployed, access the Flask app via the external LoadBalancer URL provided by the Kubernetes service.


```#Vijay

#Demonstrate the application functionality locally using Docker images.
#Show the automatic creation and pushing of the application image to Amazon ECR using GitHub Actions.

# Anubhav
#Display the application deployment into the "final" namespace on Amazon EKS.
#Verify that the application loads the background image from a private Amazon S3 bucket.
#Confirm data persistence when a pod is deleted and re-created by the ReplicaSet.
#Prove that an Amazon EBS volume and Kubernetes PersistentVolume are dynamically created when the application pod is deployed.

#Parikshek
#Demonstrate Internet access to the application.
#Change the background image URL in the ConfigMap and verify that the new image appears in the browser.
#(Bonus) Show auto-scaling functionality in response to traffic load.

docker pull relevant images

docker network create my-network
docker run --name mysql-app --env-file .env_mysql -d --network my-network -p 3306:3306 318623136204.dkr.ecr.us-east-1.amazonaws.com/docker-containers:mysql-app_latest
docker run --name flask-app --env-file .env -d --network my-network -p 81:81 318623136204.dkr.ecr.us-east-1.amazonaws.com/docker-containers:flask-app_latest

eksctl create cluster -f eks-cluster.yaml

kubectl apply -f namespace.yaml
kubectl apply -f storageclass.yaml
kubectl apply -f persistent-volume-claim.yaml
kubectl apply -f secret-db-credentials.yaml 
kubectl apply -f serviceaccount.yaml 
kubectl apply -f service-mysql.yaml
kubectl apply -f statefulset.yaml
kubectl apply -f deployment-mysql.yaml 

kubectl apply -f config-map.yaml
kubectl apply -f deployment-flask.yaml 
kubectl apply -f role-clusterrole.yaml 
kubectl apply -f rolebinding.yaml
kubectl apply -f service-flask.yaml 

kubectl get all -n final
#get load balancer url to show 

kubectl get pv
kubectl get pvc -n final

kubectl exec -it mysql-0 -n final -- mysql -u root -p

#>> USE employees;
#>> SELECT * FROM employee;
#>> INSERT INTO employee VALUES ('12345','Anubhav','Vijay','Parikshek','local');

kubectl delete pod mysql-0 -n final

#Wait for pod to come back
kubectl exec -it mysql-0 -n final -- mysql -u root -p

#>> USE employees;
#>> SELECT * FROM employee;

kubectl get service flask-service -n final  

kubectl apply -f hpa.yaml

while true; do curl -s http://adbf823bb7d7f44f1bc7e95799bacc03-1367741731.us-east-1.elb.amazonaws.com > /dev/null; echo "Hit Successful"; done


# Do changes in config-map.yaml file
kubectl apply -f config-map.yaml -n final                                                                                
kubectl delete deployment flask-app -n final                                                                              
kubectl apply -f deployment-flask.yaml   

kubectl get pods -n final                                                                             
kubectl get all -n final

#vist load balancer URL from here
```
```
