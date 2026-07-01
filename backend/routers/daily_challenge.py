"""
Daily Challenge Router - One exercise per day with bonus XP
"""

from fastapi import APIRouter, Depends, Query
from datetime import datetime, timedelta
import hashlib

from database import get_db
from models.exercise import exercise_to_dict
from routers.exercises import _answers_match
from services.leagues import increment_weekly_xp

router = APIRouter(prefix="/api/daily-challenge", tags=["daily_challenge"])


def _get_daily_exercise_id(db, date_str: str) -> int:
    """Deterministic exercise selection seeded by date."""
    exercises = list(db.exercises.find({}, {"_id": 1}, sort=[("_id", 1)]))
    if not exercises:
        return -1
    seed = int(hashlib.md5(date_str.encode()).hexdigest(), 16)
    idx = seed % len(exercises)
    return exercises[idx]["_id"]


@router.get("")
def get_daily_challenge(user_id: int = Query(1), db=Depends(get_db)):
    today = datetime.utcnow().strftime("%Y-%m-%d")

    exercise_id = _get_daily_exercise_id(db, today)
    if exercise_id == -1:
        return {"success": False, "message": "Nu exista exercitii"}

    exercise = db.exercises.find_one({"_id": exercise_id})
    if not exercise:
        return {"success": False, "message": "Exercitiu negasit"}

    # Check if user already attempted today
    attempt = db.daily_challenge_attempts.find_one({"user_id": user_id, "date": today})

    # Countdown to midnight
    now = datetime.utcnow()
    midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_left = max(0, int((midnight - now).total_seconds()))

    return {
        "success": True,
        "exercise": exercise_to_dict(exercise),
        "date": today,
        "attempted": attempt is not None,
        "completed": attempt.get("is_correct", False) if attempt else False,
        "attempt_count": attempt.get("attempt_count", 0) if attempt else 0,
        "countdown_seconds": seconds_left,
        "xp_reward": 0 if (attempt and attempt.get("is_correct")) else (15 if attempt else 25),
    }


@router.post("/submit")
def submit_daily_challenge(
    data: dict,
    db=Depends(get_db),
):
    user_id = data.get("user_id", 1)
    answer = data.get("answer", "").strip()
    today = datetime.utcnow().strftime("%Y-%m-%d")

    exercise_id = _get_daily_exercise_id(db, today)
    exercise = db.exercises.find_one({"_id": exercise_id})
    if not exercise:
        return {"success": False, "message": "Exercitiu negasit"}

    is_correct = _answers_match(answer, exercise["answer"])

    existing = db.daily_challenge_attempts.find_one({"user_id": user_id, "date": today})

    xp_earned = 0
    if is_correct:
        if not existing:
            xp_earned = 25  # First correct
        elif not existing.get("is_correct"):
            xp_earned = 15  # Correct on a retry (reduced reward)

    if existing:
        db.daily_challenge_attempts.update_one(
            {"_id": existing["_id"]},
            {"$set": {"is_correct": existing.get("is_correct") or is_correct},
             "$inc": {"attempt_count": 1}},
        )
    else:
        db.daily_challenge_attempts.insert_one({
            "user_id": user_id,
            "date": today,
            "exercise_id": exercise_id,
            "is_correct": is_correct,
            "attempt_count": 1,
            "submitted_at": datetime.utcnow(),
        })

    if xp_earned > 0:
        db.users.update_one({"_id": user_id}, {"$inc": {"xp": xp_earned}})
        increment_weekly_xp(db, user_id, xp_earned)

    return {
        "success": True,
        "correct": is_correct,
        "correct_answer": exercise["answer"] if not is_correct else None,
        "xp_earned": xp_earned,
        "message": "Corect! 🎉" if is_correct else "Incearca din nou!",
    }
