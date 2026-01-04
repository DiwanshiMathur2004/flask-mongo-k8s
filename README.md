🐍 Flask + MongoDB + Docker + Kubernetes (Minikube)

This project demonstrates a Flask backend application connected with MongoDB, containerized using Docker, and deployed on Kubernetes using Minikube.

It supports inserting and retrieving data via REST endpoints and demonstrates replica scaling, service discovery, and container orchestration.

🗂 Project Structure
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

🐳 Dockerfile for Flask Application
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

# Run the Flask app
CMD ["python", "app.py"]


⚠️ Note: Ensure Flask app listens on 0.0.0.0 to allow access from Kubernetes pods.

🚀 Build & Push Docker Image
Step 1️⃣: Build Docker Image Locally
cd app
docker build -t flask-app:1.0 .

Step 2️⃣: Push Docker Image to DockerHub
docker tag flask-app:1.0 <your-dockerhub-username>/flask-app:1.0
docker push <your-dockerhub-username>/flask-app:1.0


💡 Tip: Login first using docker login.

☸ Kubernetes Deployment
Step 1️⃣: Deploy MongoDB
kubectl apply -f k8s/mongodb.yaml


MongoDB Service: mongodb-service (used by Flask pods)

Step 2️⃣: Deploy Flask Application
kubectl apply -f k8s/flask.yaml


Flask Service: flask-service

⚡ Access Flask Service
minikube service flask-service

🌐 DNS Resolution in Kubernetes

Kubernetes provides internal DNS for all services.

Each service gets a DNS name:

<service-name>.<namespace>.svc.cluster.local


Pods can communicate using the service name instead of IP addresses.

Example: Flask connects to MongoDB using mongodb-service.

💼 Resource Requests & Limits
resources:
  requests:
    memory: "128Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"


Requests: Minimum guaranteed CPU/memory

Limits: Maximum allowed CPU/memory

🎨 Design Choices

Flask + MongoDB: Lightweight, fast REST API prototyping, flexible JSON storage

Docker: Portability across environments

Kubernetes (Minikube): Local testing, replicas, and scaling

Alternative considered: PostgreSQL → Not chosen due to JSON flexibility requirements

✅ Testing Scenarios

Insert data via POST /data

Retrieve data via GET /data

Verified multiple pods read/write to same DB

Autoscaling:

kubectl scale deployment flask-deployment --replicas=4


Verified new pods handled requests without downtime

Simulated multiple concurrent requests using curl or Postman

⚠ Issues Encountered

Flask must listen on 0.0.0.0 to allow inter-pod communication

Docker networking on Windows required proper container network configuration

🖥 Output Example
Welcome to the Flask app! The current time is: 2026-01-04 18:29:23.545362


Tip: Add a screenshots/ folder in your repo with actual output screenshots.

👤 Author

Diwanshi Mathur


