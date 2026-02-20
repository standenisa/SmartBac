"""
Statistics Router - User performance analytics
"""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query

from database import get_db

router = APIRouter(prefix="/api/stats", tags=["statistics"])


@router.get("")
def get_stats(user_id: int = Query(1), db=Depends(get_db)):
    total = db.attempts.count_documents({"user_id": user_id})
    correct = db.attempts.count_documents({"user_id": user_id, "is_correct": True})

    return {
        "total_attempts": total,
        "correct_answers": correct,
        "accuracy": round((correct / total) * 100, 2) if total > 0 else 0,
    }


@router.get("/detailed")
def get_detailed_stats(user_id: int = Query(1), db=Depends(get_db)):
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$lookup": {
            "from": "exercises",
            "localField": "exercise_id",
            "foreignField": "_id",
            "as": "exercise",
        }},
        {"$unwind": "$exercise"},
        {"$group": {
            "_id": "$exercise.subject",
            "attempts": {"$sum": 1},
            "correct": {"$sum": {"$cond": ["$is_correct", 1, 0]}},
        }},
    ]
    results = list(db.attempts.aggregate(pipeline))

    stats = {
        "total": {"attempts": 0, "correct": 0, "accuracy": 0},
        "subject_1": {"attempts": 0, "correct": 0, "accuracy": 0},
        "subject_2": {"attempts": 0, "correct": 0, "accuracy": 0},
        "subject_3": {"attempts": 0, "correct": 0, "accuracy": 0},
    }

    for row in results:
        subject = row["_id"]
        attempts = row["attempts"]
        correct = row["correct"]
        key = f"subject_{subject}"
        if key in stats:
            stats[key]["attempts"] = attempts
            stats[key]["correct"] = correct
            stats[key]["accuracy"] = round((correct / attempts) * 100, 2) if attempts > 0 else 0
            stats["total"]["attempts"] += attempts
            stats["total"]["correct"] += correct

    t = stats["total"]
    t["accuracy"] = round((t["correct"] / t["attempts"]) * 100, 2) if t["attempts"] > 0 else 0

    return stats


@router.get("/analytics/detailed")
def get_analytics_detailed(user_id: int = Query(1), db=Depends(get_db)):
    """Detailed analytics: per-topic accuracy, 30-day trend, study time, predicted grade."""

    # ── Per-topic accuracy ──
    topic_pipeline = [
        {"$match": {"user_id": user_id}},
        {"$lookup": {
            "from": "exercises",
            "localField": "exercise_id",
            "foreignField": "_id",
            "as": "exercise",
        }},
        {"$unwind": "$exercise"},
        {"$group": {
            "_id": "$exercise.topic",
            "attempts": {"$sum": 1},
            "correct": {"$sum": {"$cond": ["$is_correct", 1, 0]}},
        }},
    ]
    topic_results = list(db.attempts.aggregate(topic_pipeline))

    topics = []
    for row in topic_results:
        attempts = row["attempts"]
        correct = row["correct"]
        topics.append({
            "topic": row["_id"],
            "attempts": attempts,
            "correct": correct,
            "accuracy": round((correct / attempts) * 100, 2) if attempts > 0 else 0,
        })

    # ── 30-day trend ──
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    trend_pipeline = [
        {"$match": {"user_id": user_id, "created_at": {"$gte": thirty_days_ago}}},
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}},
            "attempts": {"$sum": 1},
            "correct": {"$sum": {"$cond": ["$is_correct", 1, 0]}},
        }},
        {"$sort": {"_id": 1}},
    ]
    trend_results = list(db.attempts.aggregate(trend_pipeline))

    trend = []
    for row in trend_results:
        attempts = row["attempts"]
        correct = row["correct"]
        trend.append({
            "date": row["_id"],
            "attempts": attempts,
            "correct": correct,
            "accuracy": round((correct / attempts) * 100, 2) if attempts > 0 else 0,
        })

    # ── Study time (sum of time_spent) ──
    time_pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {"_id": None, "total_time": {"$sum": "$time_spent"}}},
    ]
    time_result = list(db.attempts.aggregate(time_pipeline))
    total_time = time_result[0]["total_time"] if time_result else 0

    # ── Predicted grade ──
    total_attempts = db.attempts.count_documents({"user_id": user_id})
    total_correct = db.attempts.count_documents({"user_id": user_id, "is_correct": True})

    if total_attempts >= 5:
        accuracy = total_correct / total_attempts
        predicted_grade = round(1 + accuracy * 9, 2)
    else:
        predicted_grade = None

    return {
        "topics": topics,
        "trend": trend,
        "studyTime": total_time,
        "predictedGrade": predicted_grade,
        "totalAttempts": total_attempts,
        "totalCorrect": total_correct,
    }
