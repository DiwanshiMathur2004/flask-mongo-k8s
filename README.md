\# Flask + MongoDB + Docker + Kubernetes (Minikube)



This project demonstrates a \*\*Flask backend application\*\* connected with \*\*MongoDB\*\*, containerized using \*\*Docker\*\*, and deployed on \*\*Kubernetes\*\* using \*\*Minikube\*\*.



---



\## Project Structure



flask-mongo-k8s/

│

├── app/

│ ├── app.py

│ ├── Dockerfile

│ └── requirements.txt

│

├── k8s/

│ ├── flask.yaml

│ └── mongodb.yaml

│

├── deploy.bat

└── README.md





---



\## Build Docker Image Locally



```bash

cd app

docker build -t flask-app:1.0 .

Push Docker Image to Container Registry

bash

Copy code

docker tag flask-app:1.0 <your-dockerhub-username>/flask-app:1.0

docker push <your-dockerhub-username>/flask-app:1.0

Kubernetes Deployment (Minikube)

MongoDB Deployment (k8s/mongodb.yaml)



apiVersion: apps/v1

kind: Deployment

metadata:

&nbsp; name: mongodb-deployment

spec:

&nbsp; replicas: 1

&nbsp; selector:

&nbsp;   matchLabels:

&nbsp;     app: mongodb

&nbsp; template:

&nbsp;   metadata:

&nbsp;     labels:

&nbsp;       app: mongodb

&nbsp;   spec:

&nbsp;     containers:

&nbsp;     - name: mongodb

&nbsp;       image: mongo:6.0

&nbsp;       env:

&nbsp;       - name: MONGO\_INITDB\_ROOT\_USERNAME

&nbsp;         value: "admin"

&nbsp;       - name: MONGO\_INITDB\_ROOT\_PASSWORD

&nbsp;         value: "admin123"

&nbsp;       ports:

&nbsp;       - containerPort: 27017

---

apiVersion: v1

kind: Service

metadata:

&nbsp; name: mongodb-service

spec:

&nbsp; selector:

&nbsp;   app: mongodb

&nbsp; ports:

&nbsp;   - protocol: TCP

&nbsp;     port: 27017

&nbsp;     targetPort: 27017

&nbsp; type: ClusterIP

Flask Deployment (k8s/flask.yaml)

apiVersion: apps/v1

kind: Deployment

metadata:

&nbsp; name: flask-deployment

spec:

&nbsp; replicas: 2

&nbsp; selector:

&nbsp;   matchLabels:

&nbsp;     app: flask

&nbsp; template:

&nbsp;   metadata:

&nbsp;     labels:

&nbsp;       app: flask

&nbsp;   spec:

&nbsp;     containers:

&nbsp;     - name: flask

&nbsp;       image: <your-dockerhub-username>/flask-app:1.0

&nbsp;       env:

&nbsp;       - name: MONGO\_HOST

&nbsp;         value: "mongodb-service"

&nbsp;       - name: MONGO\_USER

&nbsp;         value: "admin"

&nbsp;       - name: MONGO\_PASSWORD

&nbsp;         value: "admin123"

&nbsp;       ports:

&nbsp;       - containerPort: 5000

---

apiVersion: v1

kind: Service

metadata:

&nbsp; name: flask-service

spec:

&nbsp; selector:

&nbsp;   app: flask

&nbsp; ports:

&nbsp;   - protocol: TCP

&nbsp;     port: 5000

&nbsp;     targetPort: 5000

&nbsp; type: NodePort

Note: Full YAML files are in k8s/ folder; snippets here are for readability.



Deploy on Minikube

bash

Copy code

\# Start Minikube

minikube start



\# Deploy MongoDB

kubectl apply -f k8s/mongodb.yaml



\# Deploy Flask app

kubectl apply -f k8s/flask.yaml



\# Access Flask service

minikube service flask-service

DNS Resolution in Kubernetes

Kubernetes provides internal DNS for all services.



Each service gets a DNS name like:



e

<service-name>.<namespace>.svc.cluster.local

Pods can communicate with other pods using the service name instead of IP addresses.



Example: Flask connects to MongoDB using mongodb-service.



Resource Requests and Limits

Requests: Minimum guaranteed CPU/memory.



Limits: Maximum allowed CPU/memory.





resources:

&nbsp; requests:

&nbsp;   memory: "128Mi"

&nbsp;   cpu: "250m"

&nbsp; limits:

&nbsp;   memory: "512Mi"

&nbsp;   cpu: "500m"

Design Choices

Flask + MongoDB: Lightweight and fast for prototyping REST APIs.



Docker: Portability across environments.



Kubernetes (Minikube): Local testing, easy to show replicas and scaling.



Alternative considered: Postgres instead of MongoDB → Chose MongoDB for flexible JSON storage.



Testing Scenarios

Database interactions:



Inserted data via POST /data endpoint.



Retrieved data via GET /data endpoint.



Verified multiple pods read/write to same DB.



Autoscaling:





kubectl scale deployment flask-deployment --replicas=4

Verified new pods served requests without downtime.



Issues encountered:



Networking inside Docker for Windows required container network.



Flask must listen on 0.0.0.0 for inter-pod access.



Output:

Welcome to the Flask app! The current time is: 2026-01-04 18:29:23.545362



Author

Diwanshi Mathur

