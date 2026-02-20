"""Exam simulation helpers for MongoDB documents"""

from datetime import datetime


def create_exam_doc(exam_id, user_id):
    """Create an exam simulation document for MongoDB insertion."""
    return {
        "_id": exam_id,
        "user_id": user_id,
        "score_subject1": 0,
        "score_subject2": 0,
        "score_subject3": 0,
        "total_score": 0,
        "time_spent": 0,
        "completed": False,
        "started_at": datetime.utcnow(),
        "completed_at": None,
    }


def exam_to_dict(doc):
    """Convert a MongoDB exam simulation document to API response dict."""
    if not doc:
        return None
    return {
        "id": doc["_id"],
        "user_id": doc["user_id"],
        "score_subject1": doc.get("score_subject1", 0),
        "score_subject2": doc.get("score_subject2", 0),
        "score_subject3": doc.get("score_subject3", 0),
        "total_score": doc.get("total_score", 0),
        "time_spent": doc.get("time_spent", 0),
        "completed": doc.get("completed", False),
        "started_at": doc["started_at"].isoformat() if doc.get("started_at") else None,
        "completed_at": doc["completed_at"].isoformat() if doc.get("completed_at") else None,
    }
