"""
Exercises Router - CRUD and answer submission
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from database import get_db, get_next_id
from models.exercise import exercise_to_dict
from models.attempt import create_attempt_doc
from schemas import SubmitAnswerRequest, SubmitAnswerResponse
from services.gamification import check_achievements_for_user

router = APIRouter(prefix="/api/exercises", tags=["exercises"])


@router.get("")
def get_exercises(
    difficulty: Optional[int] = Query(None, ge=1, le=5),
    subject: Optional[int] = Query(None, ge=1, le=3),
    profile: Optional[str] = Query(None, pattern="^(M1|M2|BOTH)$"),
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

    is_correct = req.answer.strip().lower() == exercise["answer"].strip().lower()

    # Save attempt
    attempt_id = get_next_id("attempts")
    attempt_doc = create_attempt_doc(
        attempt_id, req.user_id, req.exercise_id,
        req.answer.strip(), is_correct, req.time_spent,
    )
    db.attempts.insert_one(attempt_doc)

    # Update user streak
    user = db.users.find_one({"_id": req.user_id})
    if user:
        if is_correct:
            new_streak = (user.get("current_streak", 0) or 0) + 1
            best = max(user.get("best_streak", 0) or 0, new_streak)
            db.users.update_one(
                {"_id": req.user_id},
                {"$set": {"current_streak": new_streak, "best_streak": best}},
            )
        else:
            db.users.update_one(
                {"_id": req.user_id},
                {"$set": {"current_streak": 0}},
            )

    # Check new achievements
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
def get_hints(exercise_id: int, db=Depends(get_db)):
    exercise = db.exercises.find_one({"_id": exercise_id})
    hints = exercise.get("hints", []) if exercise else []
    formula = exercise.get("formula") if exercise else None

    if not hints:
        hints = ["Gandeste-te la formulele invatate"]

    return {"success": True, "hints": hints, "formula": formula}
