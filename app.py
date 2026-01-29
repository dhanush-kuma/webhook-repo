from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

app = Flask(__name__)

# DB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client["github_webhooks"]
collection = db["webhooks-events"]

try:
    client.admin.command("ping")
    print("MongoDB Connected")
except Exception as e:
    print("MongoDB Error", e)

# Hello World route
@app.route("/")
def home():
    print("HOME HIT", flush=True)
    return "Server is running"

@app.route("/webhook", methods = ['POST'])
def webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json

    doc = {
        "request_id": None,
        "author": None,
        "action": None,
        "from_branch": None,
        "to_branch": None,
        "timestamp": datetime.utcnow()
    }

    # PUSH
    if event_type == "push":
        doc["request_id"] = payload.get("after")  # commit hash
        doc["author"] = payload["pusher"]["name"]
        doc["action"] = "PUSH"
        doc["to_branch"] = payload["ref"].split("/")[-1]

    # PULL REQUEST / MERGE
    elif event_type == "pull_request":
        pr = payload["pull_request"]

        doc["request_id"] = pr["id"]
        doc["author"] = pr["user"]["login"]
        doc["from_branch"] = pr["head"]["ref"]
        doc["to_branch"] = pr["base"]["ref"]

        if pr["merged"]:
            doc["action"] = "MERGE"
        else:
            doc["action"] = "PULL_REQUEST"

    if doc["action"]:
        collection.insert_one(doc)

    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(debug=True)
