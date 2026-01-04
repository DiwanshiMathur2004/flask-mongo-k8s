from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

# ----------------------------
# Flask app initialization
# ----------------------------
app = Flask(__name__)

# ----------------------------
# MongoDB configuration
# ----------------------------
# Use environment variables if provided, otherwise defaults
MONGO_USER = os.environ.get("MONGO_USER", "admin")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD", "admin123")
MONGO_HOST = os.environ.get("MONGO_HOST", "host.docker.internal")  # Works on Windows Docker
MONGO_PORT = os.environ.get("MONGO_PORT", "27017")
MONGO_DB = os.environ.get("MONGO_DB", "flask_db")

# Construct MongoDB URI
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # 5 sec timeout
    client.server_info()  # Trigger connection check
    db = client[MONGO_DB]
    collection = db.data
    print(f"✅ Connected to MongoDB at {MONGO_HOST}:{MONGO_PORT}")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    collection = None

# ----------------------------
# Routes
# ----------------------------

@app.route('/')
def index():
    return f"Welcome to the Flask app! The current time is: {datetime.now()}"

@app.route('/data', methods=['GET', 'POST'])
def data():
    if collection is None:
        return jsonify({"error": "MongoDB not connected"}), 500

    if request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No JSON data provided"}), 400
            collection.insert_one(data)
            return jsonify({"status": "Data inserted"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == 'GET':
        try:
            data_list = list(collection.find({}, {"_id": 0}))  # Exclude _id field
            return jsonify(data_list), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    if collection is None:
        return jsonify({"status": "MongoDB not connected"}), 500
    return jsonify({"status": "OK"}), 200

# ----------------------------
# Run the app
# ----------------------------
if __name__ == '__main__':
    # Listen on all interfaces (0.0.0.0) so Docker can access it
    app.run(host='0.0.0.0', port=5000)
