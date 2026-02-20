"""Attempt helpers for MongoDB documents"""

from datetime import datetime


def create_attempt_doc(attempt_id, user_id, exercise_id, user_answer, is_correct, time_spent=0):
    """Create an attempt document for MongoDB insertion."""
    return {
        "_id": attempt_id,
        "user_id": user_id,
        "exercise_id": exercise_id,
        "user_answer": user_answer,
        "is_correct": is_correct,
        "time_spent": time_spent,
        "created_at": datetime.utcnow(),
    }


def attempt_to_dict(doc):
    """Convert a MongoDB attempt document to API response dict."""
    if not doc:
        return None
    return {
        "id": doc["_id"],
        "user_id": doc["user_id"],
        "exercise_id": doc["exercise_id"],
        "user_answer": doc.get("user_answer"),
        "is_correct": doc.get("is_correct", False),
        "time_spent": doc.get("time_spent", 0),
        "created_at": doc["created_at"].isoformat() if doc.get("created_at") else None,
    }
