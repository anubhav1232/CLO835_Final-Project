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


```eksctl create cluster -f eks-cluster.yaml
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

>> USE employees;
>> SELECT * FROM employee;
>> INSERT INTO employee VALUES ('1','Anubhav','Vijay','Parikshek','local');

kubectl delete pod mysql-0 -n final

#Wait for pod to come back
kubectl exec -it mysql-0 -n final -- mysql -u root -p

>> USE employees;
>> SELECT * FROM employee;



kubectl get service flask-service -n final  

kubectl apply -f hpa.yaml

while true; do curl -s http://adbf823bb7d7f44f1bc7e95799bacc03-1367741731.us-east-1.elb.amazonaws.com > /dev/null; sleep 1; echo "Hit Successful"; done


# Do changes in config-map.yaml file
kubectl apply -f config-map.yaml -n final                                                                                
kubectl delete deployment flask-app -n final                                                                              
kubectl apply -f deployment-flask.yaml   

kubectl get pods -n final                                                                             
kubectl get all -n final

#vist load balancer URL from here

```