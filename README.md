# Flask + MongoDB + Docker + Kubernetes (Minikube)

This project demonstrates a **Flask backend application** connected with **MongoDB**, containerized using **Docker**, and deployed on **Kubernetes** using **Minikube**.

It allows users to insert and retrieve data via REST endpoints and demonstrates **replica scaling**, **service discovery**, and **container orchestration**.

---

## 🗂 Project Structure

flask-mongo-k8s/
├── app/
│ ├── app.py # Flask application code
│ ├── Dockerfile # Dockerfile for Flask app
│ └── requirements.txt # Python dependencies
├── k8s/
│ ├── flask.yaml # Flask Deployment and Service YAML
│ └── mongodb.yaml # MongoDB Deployment and Service YAML
├── deploy.bat # Optional deployment script for Windows
└── README.md # This file

yaml
Copy code

---

## 🐳 Dockerfile for Flask Application

Below is the Dockerfile used to containerize the Flask application:

```dockerfile
# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY requirements.txt .
COPY app.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]
Note: Ensure Flask app listens on 0.0.0.0 to allow access from Kubernetes pods.

🐳 Build and Push Docker Image
Step 1: Build Docker Image Locally
bash
Copy code
cd app
docker build -t flask-app:1.0 .
Step 2: Push Docker Image to DockerHub
Tag your image:

bash
Copy code
docker tag flask-app:1.0 <your-dockerhub-username>/flask-app:1.0
Push the image:

bash
Copy code
docker push <your-dockerhub-username>/flask-app:1.0
Tip: Login to DockerHub first: docker login

☸ Kubernetes YAML Files
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
⚡ Steps to Deploy on Minikube
Start Minikube:

bash
Copy code
minikube start
Deploy MongoDB:

bash
Copy code
kubectl apply -f k8s/mongodb.yaml
Deploy Flask application:

bash
Copy code
kubectl apply -f k8s/flask.yaml
Access the Flask service:

bash
Copy code
minikube service flask-service
🌐 DNS Resolution in Kubernetes
Kubernetes provides internal DNS for all services.

Each service gets a DNS name:

pgsql
Copy code
<service-name>.<namespace>.svc.cluster.local
Pods can communicate using the service name instead of IP addresses.

Example: Flask connects to MongoDB using mongodb-service.

💼 Resource Requests and Limits
To ensure cluster stability, we set requests (minimum guaranteed resources) and limits (maximum allowed resources):

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
Flask + MongoDB: Chosen for lightweight, fast REST API prototyping and flexible JSON storage.

Docker: Ensures portability across environments.

Kubernetes (Minikube): Local testing, easy to demonstrate replicas and scaling.

Alternatives considered:

PostgreSQL instead of MongoDB → Not chosen because MongoDB supports flexible JSON-like storage which is more suitable for prototype REST APIs.

✅ Testing Scenarios (Cookie Point)
Database interactions:

Insert data via POST /data endpoint

Retrieve data via GET /data endpoint

Verified multiple pods read/write to the same database successfully

Autoscaling / High Traffic Simulation:

bash
Copy code
kubectl scale deployment flask-deployment --replicas=4
Verified that new pods handled requests without downtime

Simulated multiple concurrent requests using curl or Postman → all requests were served correctly

Issues Encountered During Testing:

Flask must listen on 0.0.0.0 to allow inter-pod communication

Docker networking on Windows required proper container network

🖥 Output Example
pgsql
Copy code
Welcome to the Flask app! The current time is: 2026-01-04 18:29:23.545362
Tip: Include a screenshots/ folder in your repo with actual output.

👤 Author
Diwanshi Mathur

markdown
Copy code



