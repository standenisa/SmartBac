"""
Database Configuration - MongoDB with PyMongo
BAC Prep AI
"""

from pymongo import MongoClient, ReturnDocument
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "bac_prep_ai")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]


def get_db():
    """Dependency for FastAPI - returns MongoDB database."""
    return db


def get_next_id(collection_name: str) -> int:
    """Auto-increment ID for a collection."""
    counter = db.counters.find_one_and_update(
        {"_id": collection_name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return counter["seq"]


def init_db():
    """Create indexes for all collections."""
    db.users.create_index("email", unique=True)
    db.users.create_index("username", unique=True)
    db.exercises.create_index("topic")
    db.exercises.create_index("subject")
    db.exercises.create_index("profile")
    db.exercises.create_index("exercise_type")
    db.attempts.create_index("user_id")
    db.attempts.create_index("exercise_id")
    db.attempts.create_index("created_at")
    db.user_achievements.create_index(
        [("user_id", 1), ("achievement_id", 1)], unique=True
    )
    db.exam_simulations.create_index("user_id")

    # Adaptive learning
    db.user_exercise_history.create_index(
        [("user_id", 1), ("exercise_id", 1)], unique=True
    )
    db.user_exercise_history.create_index([("user_id", 1), ("next_review", 1)])
    db.user_exercise_history.create_index([("user_id", 1), ("topic", 1)])

    # Daily challenges
    db.daily_challenge_attempts.create_index(
        [("user_id", 1), ("date", 1)], unique=True
    )

    # Leagues
    db.leagues.create_index([("week_start", 1), ("league", 1)])
    db.leagues.create_index(
        [("user_id", 1), ("week_start", 1)], unique=True
    )

    # Chat history
    db.chat_history.create_index([("user_id", 1), ("timestamp", -1)])
