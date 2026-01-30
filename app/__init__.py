from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    #Database connection setup
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["github_webhooks"]
    collection = db["webhooks-events"]

    try:
        client.admin.command("ping")
        print("MongoDB Connected")
    except Exception as e:
        print("MongoDB Error", e)

    # home url that renders the event page
    @app.route("/")
    def home():
        return render_template('index.html')

    # webhook endpoint is used to by github repo to send the post message in case of push, pull or merge events
    @app.route("/webhook", methods=['POST'])
    def webhook():
        event_type = request.headers.get("X-GitHub-Event")
        payload = request.json

        # creates empty reference document
        doc = {
            "request_id": None,
            "author": None,
            "action": None,
            "from_branch": None,
            "to_branch": None,
            "timestamp": datetime.now(timezone.utc)
        }

        # this section parse the json into a document format
        if event_type == "push":
            doc["request_id"] = payload.get("after")
            doc["author"] = payload["pusher"]["name"]
            doc["action"] = "PUSH"
            doc["to_branch"] = payload["ref"].split("/")[-1]

        elif event_type == "pull_request":
            pr = payload["pull_request"]
            doc["request_id"] = pr["id"]
            doc["author"] = pr["user"]["login"]
            doc["from_branch"] = pr["head"]["ref"]
            doc["to_branch"] = pr["base"]["ref"]
            doc["action"] = "MERGE" if pr.get("merged") else "PULL_REQUEST"

        # document is saved to mongodb
        if doc["action"]:
            collection.insert_one(doc)

        return {"status": "ok"}, 200

    # this endpoint if for ui to poll every 15s to fetch recent records.
    @app.route("/events")
    def events():
        cutoff_time = datetime.now(timezone.utc) - timedelta(seconds=15)
        query = {"timestamp": {"$gte": cutoff_time}}
        
        records = list(collection.find(query))
        for record in records:
            record['_id'] = str(record['_id'])
            if isinstance(record.get('timestamp'), datetime):
                record['timestamp'] = record['timestamp'].isoformat()

        return jsonify(records)

    return app