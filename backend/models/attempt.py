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
