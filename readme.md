# GitHub Webhook Event Tracker

A lightweight Flask application that listens for GitHub Webhooks (Push, Pull and Merge Request events), stores the payloads in MongoDB, and displays them via a simple web interface.

## Tech Stack
- **Backend:** Flask (Python)
- **Database:** MongoDB
- **Tunneling:** ngrok (for local development)

---

## Getting Started

### 1. Clone the Repository
git clone <your-repo-url>
cd <repo-name>

### 2. Set Up Virtual Environment
# Create the environment
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on Mac/Linux:
source venv/bin/activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Environment Configuration
Create a .env file in the root directory and add your MongoDB connection string:
MONGO_URI=your_mongodb_connection_string_here

### 5. Database Optimization
To ensure fast retrieval of the latest events, index the timestamp field in your MongoDB collection:
db.events.createIndex({ "timestamp": -1 })

### 6. Run the Application
python run.py

The server will start locally on http://127.0.0.1:5000.

---

## 🌐 Setting Up the Webhook

Since GitHub needs a public URL to send data, use ngrok:

1. Download ngrok: https://ngrok.com/download
2. Authenticate: ngrok config add-authtoken <your-auth-key>
3. Start Tunnel: ngrok http 5000
4. Copy the Forwarding URL: It will look like https://xxxx-xxxx.ngrok-free.app.

---

## ⚓ GitHub Integration
1. Navigate to your GitHub Repository Settings > Webhooks.
2. Click "Add webhook".
3. Payload URL: Paste your ngrok URL (e.g., https://xxxx-xxxx.ngrok-free.app/webhook).
4. Content type: Select application/json.
5. Which events: Select "Pushes" and "Pull requests".
6. Click "Add webhook".

Your UI should now automatically populate whenever an event occurs on GitHub!