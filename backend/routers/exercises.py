"""
Exercises Router - CRUD, answer submission, adaptive learning, progressive hints, quick practice
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
import re

from database import get_db, get_next_id
from models.exercise import exercise_to_dict
from models.attempt import create_attempt_doc
from schemas import SubmitAnswerRequest, SubmitAnswerResponse
from services.gamification import check_achievements_for_user
from services.adaptive import AdaptiveLearning
from services.leagues import increment_weekly_xp

router = APIRouter(prefix="/api/exercises", tags=["exercises"])


def _normalize_answer(text: str) -> str:
    """Normalize math answer for comparison: strip spaces, unify formatting."""
    t = text.strip().lower()
    t = t.replace(" ", "").replace("\t", "")
    t = t.replace("{", "").replace("}", "")
    t = t.replace("×", "*").replace("·", "*").replace("÷", "/")
    t = t.replace(",", ".")  # 3,5 → 3.5
    t = t.replace("−", "-")  # unicode minus
    t = re.sub(r"^x=", "", t)  # "x=4" → "4"
    t = re.sub(r"^y=", "", t)
    t = re.sub(r"^f\(x\)=", "", t)
    try:
        val = float(t)
        t = f"{val:g}"
    except ValueError:
        pass
    return t


def _answers_match(user_answer: str, correct_answer: str) -> bool:
    """Compare answers with math-aware normalization."""
    return _normalize_answer(user_answer) == _normalize_answer(correct_answer)


@router.get("/next")
def get_next_exercise(user_id: int = Query(1), db=Depends(get_db)):
    """Get the next best exercise using adaptive learning."""
    adaptive = AdaptiveLearning(db)
    exercise = adaptive.get_next_exercise(user_id)
    if not exercise:
        return {"success": False, "message": "Nu mai exista exercitii disponibile"}
    return {"success": True, "exercise": exercise_to_dict(exercise)}


@router.get("/quick-practice")
def get_quick_practice(
    user_id: int = Query(1),
    count: int = Query(3, ge=1, le=10),
    db=Depends(get_db),
):
    """Get exercises from weak topics for quick practice."""
    adaptive = AdaptiveLearning(db)
    user = db.users.find_one({"_id": user_id})
    profile = user.get("profile", "M1") if user else "M1"

    weak_topics = adaptive.get_weak_topics(user_id, count=5)
    exercises = []

    if weak_topics:
        for wt in weak_topics:
            if len(exercises) >= count:
                break
            topic = wt["_id"]
            found = list(db.exercises.find({
                "topic": topic,
                "$or": [{"profile": profile}, {"profile": "BOTH"}],
            }, limit=1))
            exercises.extend(found)

    # Fill remaining with random exercises
    if len(exercises) < count:
        seen_ids = [e["_id"] for e in exercises]
        remaining = list(db.exercises.aggregate([
            {"$match": {
                "_id": {"$nin": seen_ids},
                "$or": [{"profile": profile}, {"profile": "BOTH"}],
            }},
            {"$sample": {"size": count - len(exercises)}},
        ]))
        exercises.extend(remaining)

    return {
        "success": True,
        "exercises": [exercise_to_dict(e) for e in exercises[:count]],
        "count": min(len(exercises), count),
    }


@router.get("")
def get_exercises(
    difficulty: Optional[int] = Query(None, ge=1, le=5),
    subject: Optional[int] = Query(None, ge=1, le=3),
    profile: Optional[str] = Query(None, pattern="^(M1|M2|M3|M4|BOTH)$"),
    exercise_type: Optional[str] = None,
    topic: Optional[str] = None,
    db=Depends(get_db),
):
    query = {}

    if difficulty:
        query["difficulty"] = difficulty
    if subject:
        query["subject"] = subject
    if profile:
        query["$or"] = [{"profile": profile}, {"profile": "BOTH"}]
    if exercise_type:
        query["exercise_type"] = exercise_type
    if topic:
        query["topic"] = {"$regex": topic, "$options": "i"}

    exercises = list(db.exercises.find(query))
    return [exercise_to_dict(e) for e in exercises]


@router.get("/{exercise_id}")
def get_exercise(exercise_id: int, db=Depends(get_db)):
    exercise = db.exercises.find_one({"_id": exercise_id})
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise_to_dict(exercise)


@router.post("/submit-answer", response_model=SubmitAnswerResponse)
def submit_answer(req: SubmitAnswerRequest, db=Depends(get_db)):
    exercise = db.exercises.find_one({"_id": req.exercise_id})
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    is_correct = _answers_match(req.answer, exercise["answer"])

    attempt_id = get_next_id("attempts")
    attempt_doc = create_attempt_doc(
        attempt_id, req.user_id, req.exercise_id,
        req.answer.strip(), is_correct, req.time_spent,
    )
    db.attempts.insert_one(attempt_doc)

    # Update user streak & XP
    user = db.users.find_one({"_id": req.user_id})
    xp_earned = 0
    if user:
        if is_correct:
            new_streak = (user.get("current_streak", 0) or 0) + 1
            best = max(user.get("best_streak", 0) or 0, new_streak)
            xp_earned = 10
            db.users.update_one(
                {"_id": req.user_id},
                {"$set": {"current_streak": new_streak, "best_streak": best},
                 "$inc": {"xp": xp_earned}},
            )
            increment_weekly_xp(db, req.user_id, xp_earned)
        elif user.get("streak_freeze_active"):
            # An active freeze absorbs one wrong answer instead of resetting the streak
            db.users.update_one(
                {"_id": req.user_id},
                {"$set": {"streak_freeze_active": False}},
            )
        else:
            db.users.update_one(
                {"_id": req.user_id},
                {"$set": {"current_streak": 0}},
            )

    adaptive = AdaptiveLearning(db)
    adaptive.record_attempt(req.user_id, req.exercise_id, is_correct)

    new_achievements = check_achievements_for_user(req.user_id, db)

    return SubmitAnswerResponse(
        correct=is_correct,
        correct_answer=exercise["answer"] if not is_correct else None,
        message="Corect!" if is_correct else "Incearca din nou!",
        new_achievements=new_achievements,
    )


@router.get("/{exercise_id}/solution")
def get_solution(exercise_id: int, db=Depends(get_db)):
    exercise = db.exercises.find_one({"_id": exercise_id})
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    return {
        "success": True,
        "solution": {
            "id": exercise["_id"],
            "question": exercise["question"],
            "answer": exercise["answer"],
            "solution": exercise.get("solution"),
            "solution_steps": exercise.get("solution_steps", []),
            "hints": exercise.get("hints", []),
            "explanation": exercise.get("explanation") or f"Raspunsul corect este: {exercise['answer']}",
            "formula": exercise.get("formula"),
            "latex": exercise.get("latex"),
        },
    }


@router.get("/{exercise_id}/hints")
def get_hints(
    exercise_id: int,
    level: int = Query(1, ge=1, le=3),
    user_id: int = Query(1),
    db=Depends(get_db),
):
    """Progressive hints: Level 1 (free), Level 2 (-5 XP), Level 3 (-10 XP)."""
    exercise = db.exercises.find_one({"_id": exercise_id})
    if not exercise:
        return {"success": False, "hints": [], "formula": None}

    hints_list = exercise.get("hints", [])
    solution_steps = exercise.get("solution_steps", [])
    answer = exercise.get("answer", "")

    # Build progressive hints
    all_hints = []

    # Level 1: General hint (free)
    if hints_list:
        all_hints.append(hints_list[0])
    else:
        all_hints.append("Gandeste-te la formulele invatate")

    # Level 2: Concrete hint (-5 XP)
    if level >= 2:
        if len(hints_list) > 1:
            all_hints.append(hints_list[1])
        elif solution_steps:
            first_step = solution_steps[0] if isinstance(solution_steps[0], str) else solution_steps[0].get("action", "")
            all_hints.append(f"Pasul 1: {first_step}")
        else:
            all_hints.append("Verifica daca ai aplicat formula corect")

    # Level 3: Near-answer (-10 XP)
    if level >= 3:
        if len(hints_list) > 2:
            all_hints.append(hints_list[2])
        elif answer:
            partial = answer[:len(answer)//2] + "..."
            all_hints.append(f"Raspunsul incepe cu: {partial}")
        else:
            all_hints.append("Esti foarte aproape! Verifica calculele")

    if level == 2:
        db.users.update_one(
            {"_id": user_id, "xp": {"$gte": 5}},
            {"$inc": {"xp": -5}},
        )
    elif level == 3:
        db.users.update_one(
            {"_id": user_id, "xp": {"$gte": 10}},
            {"$inc": {"xp": -10}},
        )

    xp_cost = {1: 0, 2: 5, 3: 10}[level]

    return {
        "success": True,
        "hints": all_hints,
        "formula": exercise.get("formula"),
        "level": level,
        "xp_cost": xp_cost,
    }
