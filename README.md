# 🐍 Flask + MongoDB + Docker + Kubernetes (Minikube)


This project demonstrates a **Flask backend application** connected with **MongoDB**, containerized using **Docker**, and deployed on **Kubernetes** using **Minikube**.  

It supports inserting and retrieving data via REST endpoints and demonstrates **replica scaling**, **service discovery**, and **container orchestration**.


## 🗂 Project Structure
```

flask-mongo-k8s/
├── app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── k8s/
│   ├── flask.yaml
│   └── mongodb.yaml
├── deploy.bat
└── README.md
```


## Dockerfile for Flask Application
```dockerfile
# Use official Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask app code
COPY app.py .

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
```

## Build and Push Docker Image
cd app
docker build -t flask-app:1.0 .


## Push to Docker Hub (or any container registry):

docker tag flask-app:1.0 <your-dockerhub-username>/flask-app:1.0
docker push <your-dockerhub-username>/flask-app:1.0
## MongoDB Deployment (k8s/mongodb.yaml)
```

apiVersion: v1
kind: Service
metadata:
  name: mongodb-service
spec:
  selector:
    app: mongodb
  ports:
    - protocol: TCP
      port: 27017
      targetPort: 27017
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mongodb-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      labels:
        app: mongodb
    spec:
      containers:
      - name: mongodb
        image: mongo:6.0
        env:
        - name: MONGO_INITDB_ROOT_USERNAME
          value: "admin"
        - name: MONGO_INITDB_ROOT_PASSWORD
          value: "admin123"
        ports:
        - containerPort: 27017
```

## Flask Deployment (k8s/flask.yaml)
```
apiVersion: v1
kind: Service
metadata:
  name: flask-service
spec:
  selector:
    app: flask
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000
  type: NodePort
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask
  template:
    metadata:
      labels:
        app: flask
    spec:
      containers:
      - name: flask
        image: <your-dockerhub-username>/flask-app:1.0
        env:
        - name: MONGO_HOST
          value: "mongodb-service"
        - name: MONGO_USER
          value: "admin"
        - name: MONGO_PASSWORD
          value: "admin123"
        ports:
        - containerPort: 5000
```

## Deploy on Minikube
```
# Start Minikube
minikube start

# Deploy MongoDB
kubectl apply -f k8s/mongodb.yaml

# Deploy Flask app
kubectl apply -f k8s/flask.yaml

# Access Flask service
minikube service flask-service

```
## DNS Resolution in Kubernetes
Kubernetes automatically creates a DNS service.

Each Service gets a DNS name (<service-name>.<namespace>.svc.cluster.local).

Pods can resolve and communicate with other pods using this DNS name.

Example: Flask connects to MongoDB using mongodb-service instead of IP addresses. Kubernetes DNS handles resolution internally.
## Resource Requests and Limits
Requests: Minimum resources guaranteed to a container (CPU, memory).

Limits: Maximum resources a container can use.

Reason: Ensures stable cluster performance, prevents pods from consuming all node resources.

Example YAML snippet:
```

resources:
  requests:
    memory: "128Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

## Design Choices
Flask + MongoDB: Lightweight, simple, easy for prototyping.

Docker: Containerization for portability.

Kubernetes (Minikube): Local cluster for testing deployment and scalability.

Alternatives considered:

Postgres instead of MongoDB → Chose MongoDB for JSON-friendly schema (fits Flask REST API).

Kubernetes cloud cluster → Chose Minikube for local testing to simplify submission and avoid cloud dependency.

Replica count 2 for Flask: For basic high availability and horizontal scaling demo.
## Testing Scenarios

Database interactions:

POSTed JSON data to /data endpoint, verified insertion with GET requests.

Ensured multiple pods accessed the same MongoDB service.

Autoscaling simulation:

Scaled Flask deployment with:
```

kubectl scale deployment flask-deployment --replicas=4

```
Verified new pods handled requests via Kubernetes Service.

Observed response time remained stable.
## Issues encountered:
Docker networking inside Windows required using container network (flask-mongo-net) for local testing.

Flask container must listen on 0.0.0.0 for pod-to-pod communication.
## Output
```
Welcome to the Flask app! The current time is: 2026-01-04 18:29:23.545362
```
<img width="1920" height="948" alt="image" src="https://github.com/user-attachments/assets/ffb30f4e-b453-4111-9c2c-d29fa355a9fd" />
<img width="1920" height="795" alt="image" src="https://github.com/user-attachments/assets/3c6108b2-542e-4588-93e3-219e22596c05" />




