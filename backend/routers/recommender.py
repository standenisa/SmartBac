"""
Recommender Router - Content-based exercise recommendations
"""

import random
from fastapi import APIRouter, Depends, Query

from database import get_db
from models.exercise import exercise_to_dict

router = APIRouter(prefix="/api/recommender", tags=["recommender"])


def _get_topic_accuracy(user_id: int, db) -> dict:
    """Calculate accuracy per topic for a user using aggregation."""
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
            "_id": "$exercise.topic",
            "total": {"$sum": 1},
            "correct": {"$sum": {"$cond": ["$is_correct", 1, 0]}},
        }},
    ]
    results = list(db.attempts.aggregate(pipeline))

    topic_acc = {}
    for row in results:
        total = row["total"]
        correct = row["correct"]
        topic_acc[row["_id"]] = {
            "total": total,
            "correct": correct,
            "accuracy": correct / total if total > 0 else 0,
        }
    return topic_acc


@router.get("/exercises")
def recommend_exercises(
    user_id: int = Query(1),
    count: int = Query(5, ge=1, le=20),
    db=Depends(get_db),
):
    """
    Content-based recommendation engine.
    Strategy:
    1. Find weak topics (accuracy < 60%)
    2. Recommend unsolved exercises from weak topics
    3. If few weak topics, mix in slightly harder exercises from strong topics
    4. Avoid recently solved exercises
    """
    topic_acc = _get_topic_accuracy(user_id, db)

    # Get IDs of exercises already attempted
    attempted_ids = list(set(
        a["exercise_id"]
        for a in db.attempts.find({"user_id": user_id}, {"exercise_id": 1})
    ))

    # Find weak and strong topics
    weak_topics = [t for t, s in topic_acc.items() if s["accuracy"] < 0.6]
    strong_topics = [t for t, s in topic_acc.items() if s["accuracy"] >= 0.6]

    recommended = []

    # Priority 1: Unsolved exercises from weak topics
    if weak_topics:
        query = {"topic": {"$in": weak_topics}}
        if attempted_ids:
            query["_id"] = {"$nin": attempted_ids}
        weak_exercises = list(
            db.exercises.find(query).sort("difficulty", 1).limit(count)
        )
        recommended.extend(weak_exercises)

    # Priority 2: Harder exercises from strong topics (for challenge)
    remaining = count - len(recommended)
    if remaining > 0 and strong_topics:
        # Find max difficulty user has succeeded at
        max_diff_pipeline = [
            {"$match": {"user_id": user_id, "is_correct": True}},
            {"$lookup": {
                "from": "exercises",
                "localField": "exercise_id",
                "foreignField": "_id",
                "as": "exercise",
            }},
            {"$unwind": "$exercise"},
            {"$group": {"_id": None, "max_diff": {"$max": "$exercise.difficulty"}}},
        ]
        max_diff_result = list(db.attempts.aggregate(max_diff_pipeline))
        max_solved_diff = max_diff_result[0]["max_diff"] if max_diff_result else 1

        query = {
            "topic": {"$in": strong_topics},
            "difficulty": {"$gte": max_solved_diff},
        }
        if attempted_ids:
            query["_id"] = {"$nin": attempted_ids}
        challenge_exercises = list(
            db.exercises.find(query).sort("difficulty", 1).limit(remaining)
        )
        recommended.extend(challenge_exercises)

    # Priority 3: Any unsolved exercises
    remaining = count - len(recommended)
    if remaining > 0:
        rec_ids = [e["_id"] for e in recommended]
        exclude = attempted_ids + rec_ids
        query = {}
        if exclude:
            query["_id"] = {"$nin": exclude}
        any_exercises = list(db.exercises.find(query))
        random.shuffle(any_exercises)
        recommended.extend(any_exercises[:remaining])

    reason = "Exercitii recomandate pe baza performantei tale"
    if weak_topics:
        reason = f"Focus pe: {', '.join(weak_topics[:3])}"

    return {
        "success": True,
        "exercises": [exercise_to_dict(e) for e in recommended],
        "reason": reason,
        "weak_topics": weak_topics,
        "strong_topics": strong_topics,
    }
