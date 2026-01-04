# Flask + MongoDB + Docker + Kubernetes (Minikube)

This project demonstrates a **Flask backend application** connected with **MongoDB**, containerized using **Docker**, and deployed on **Kubernetes** using **Minikube**.

It allows users to insert and retrieve data via REST endpoints and demonstrates **replica scaling**, **service discovery**, and **container orchestration**.

---

## 🗂 Project Structure

flask-mongo-k8s/
├── app/
│ ├── app.py
│ ├── Dockerfile
│ └── requirements.txt
├── k8s/
│ ├── flask.yaml
│ └── mongodb.yaml
├── deploy.bat
└── README.md

yaml
Copy code

---

## 🐳 Build Docker Image

### Build Docker Image Locally

```bash
cd app
docker build -t flask-app:1.0 .
Push Docker Image to DockerHub
bash
Copy code
docker tag flask-app:1.0 <your-dockerhub-username>/flask-app:1.0
docker push <your-dockerhub-username>/flask-app:1.0
☸ Kubernetes Deployment (Minikube)
MongoDB Deployment (k8s/mongodb.yaml)
yaml
Copy code
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
---
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
  type: ClusterIP
Flask Deployment (k8s/flask.yaml)
yaml
Copy code
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
---
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
⚡ Deploy on Minikube
bash
Copy code
# Start Minikube
minikube start

# Deploy MongoDB
kubectl apply -f k8s/mongodb.yaml

# Deploy Flask app
kubectl apply -f k8s/flask.yaml

# Access Flask service
minikube service flask-service
🌐 DNS Resolution in Kubernetes
Kubernetes provides internal DNS for all services. Each service gets a DNS name like:

pgsql
Copy code
<service-name>.<namespace>.svc.cluster.local
Pods can communicate using the service name instead of IP addresses.

Example: Flask connects to MongoDB using mongodb-service.

💼 Resource Requests and Limits
Requests: Minimum guaranteed CPU/memory

Limits: Maximum allowed CPU/memory

yaml
Copy code
resources:
  requests:
    memory: "128Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
🎨 Design Choices
Flask + MongoDB: Lightweight and fast for prototyping REST APIs

Docker: Portability across environments

Kubernetes (Minikube): Local testing, easy to show replicas and scaling

Alternative considered: Postgres instead of MongoDB → Chose MongoDB for flexible JSON storage

✅ Testing Scenarios
Database interactions:

Insert data via POST /data endpoint

Retrieve data via GET /data endpoint

Verified multiple pods read/write to same DB

Autoscaling:

bash
Copy code
kubectl scale deployment flask-deployment --replicas=4
Verified new pods served requests without downtime

⚠ Issues Encountered
Networking inside Docker for Windows required container network

Flask must listen on 0.0.0.0 for inter-pod access

🖥 Output Example
pgsql
Copy code
Welcome to the Flask app! The current time is: 2026-01-04 18:29:23.545362
📸 Screenshot

Tip: Add a screenshots/ folder in your repo and include actual output screenshots.

👤 Author
Diwanshi Mathur

yaml
Copy code


