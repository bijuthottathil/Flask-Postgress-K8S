# Kubernetes -Flask Microservice with Postgres, Argo CD and Prometheus
![image](https://github.com/user-attachments/assets/94e577e5-bcf5-4ffc-b0ed-a187055cd203)

# Steps involved
Create Flask based API supporting CRUD operations on a table
Postgres DB
Build and push Docker images to Docker hub
Create yaml files for Kubernetes deployment
Create yaml file for ArgoCD - GitOps continuous delivery (CD) tool specifically designed for Kubernetes
Setup Prometheus- Prometheus is a powerful, open-source monitoring
Postman- To test application

# Software prerequisites
Docker Desktop, VS Code, Minikube, PgAdmin, Python
Refer my GitHub for source code https://github.com/bijuthottathil/Flask-Postgress-K8S
I am sharing only important files and screenshot of exact deployment steps here.
This is Flask API file contains 4 operations

Once you download code from repository, you will see code base like below
Make sure that Docker Deskop it running
minikube start
minikube dashboard
Before do any deployment. Execute below command from Git Bash to invoke docker commands directly with Minikube's Docker environment.
eval $(minikube docker-env)

Create Docker file

Build and publish Docker image to Docker hub
docker build -t bijuthottathil/flask-postgres-microservice:latest .
docker push bijuthottathil/flask-postgres-microservice:latest

From VSCode Command Prompt. Execute below commands to create Deployments and Services
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/flask-deployment.yaml
kubectl apply -f k8s/flask-service.yaml
kubectl apply -f k8s/postgres-secret.yaml

You should get result like this after executing below commands
kubectl get pods
kubectl get services
kubectl get deployments

Next step , we will connect to postgress running in Kubernetes by portfowarding
kubectl port-forward svc/postgres 5432:5432

Create a new connection in PgAdmin poiting to 127.0.0.1 (localhost) using the credentials provided in postgres.yaml and postgres-secret.yaml (postgres/postgres)
create table and insert few records in the table
Now we are going to test functionality starting App service in Kubernetes. Once execute below command, service will run Kubernetes
minikube service flask-service - url

Calling get_items micro service in postman . You can see all data we entered is listed with Get http command in postman

2. Calling add_item micro service in postman . You can see all data we entered is listed with POST http command in postman
Same way you will be able to test update_item and delete_item

Next step, integrating prometheus client with code . Already I added promotheus related code to activae metrics in the code like below   

To activate metrics and see data , run application code using → python main.py. Then you need to open to see data
http://localhost:5000/metrics  

Next step is to integrate of Argo CD Gitops CI/CD tool for Kubenetes  

Run below commands from VSCode Prompt
kubectl create namespace argocd
 kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
Next run below command to get admin password to login to Argo CD UI ( I did it from Git bash prompt). Copy and note down password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
To access ArgoCD UI, expose port via port forward
kubectl port-forward svc/argocd-server -n argocd 8080:443
You can access Argo CD by http://localhost:8080
To load my application, I created a new application and provide my git url, https://github.com/bijuthottathil/Flask-Postgress-K8S
in above site, you can see app, services and pod details
You can do many activities using Argo CD, but I will show one basic example to increase replica of Flask app using Argo CD
What I did , just updated replicas from 1 to 3 → commit file in repository
PS D:\flask-postgres\Flask-Postgress-K8S> git add .
PS D:\flask-postgres\Flask-Postgress-K8S> git commit -m "Increased replicat to 3"
PS D:\flask-postgres\Flask-Postgress-K8S> git push origin main

As soon as we committed our changes in github, ArgoCD will automatically sync our change do upgradation of replicas
Refer above screen shot, you can see 3 pods are running. it was not added manually. ArgoCD taken care of it automatically based on the change in github repository
