import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

_client = None
_db = None
_collection = None


def get_collection():
    """
    Lazy MongoDB connection.
    Works in production.
    Skips DB in CI if env vars are missing.
    """
    global _client, _db, _collection

    if _collection is not None:
        return _collection

    MONGO_USERNAME = os.getenv("MONGO_USERNAME")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

    # 🚨 CI / local safety: no env → no DB
    if not all([MONGO_USERNAME, MONGO_PASSWORD, MONGO_CLUSTER, MONGO_DB_NAME]):
        print("MongoDB env vars not found — skipping DB connection")
        return None

    uri = (
        f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}"
        f"@{MONGO_CLUSTER}/{MONGO_DB_NAME}"
        "?retryWrites=true&w=majority"
    )

    _client = MongoClient(uri)
    _db = _client[MONGO_DB_NAME]
    _collection = _db["predictions"]

    return _collection


def save_prediction(url, result):
    collection = get_collection()
    if collection is None:
        return  # CI-safe
    collection.insert_one({
        "url": url,
        "result": result,
        "timestamp": datetime.now()
    })


def get_history(limit=10):
    collection = get_collection()
    if collection is None:
        return []
    return list(collection.find().sort("timestamp", -1).limit(limit))
