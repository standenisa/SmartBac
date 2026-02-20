"""
ML Router - Grade prediction and insights
"""

from fastapi import APIRouter, Depends, HTTPException, Query

from database import get_db

router = APIRouter(prefix="/api/ml", tags=["ml"])

# ML Predictor - lazy loaded
_predictor = None


def _get_predictor():
    global _predictor
    if _predictor is not None:
        return _predictor

    try:
        import sys, os
        sys.path.insert(0, os.path.dirname(__file__) + "/..")
        from ml_predictor_advanced import AdvancedGradePredictor

        _predictor = AdvancedGradePredictor(model_type="ensemble")

        model_paths = [
            "backend/models/grade_predictor_advanced.pkl",
            "models/grade_predictor_advanced.pkl",
            "backend/models/grade_predictor.pkl",
            "models/grade_predictor.pkl",
        ]

        for path in model_paths:
            if os.path.exists(path):
                _predictor.load(path)
                break
    except Exception:
        _predictor = None

    return _predictor


def _format_attempts(attempts, exercises_map):
    """Format attempts for the ML predictor."""
    formatted = []
    for attempt in attempts:
        exercise = exercises_map.get(attempt["exercise_id"])
        if exercise:
            formatted.append({
                "user_id": attempt["user_id"],
                "exercise_id": exercise["_id"],
                "exercise_subject": exercise.get("subject"),
                "exercise_difficulty": exercise.get("difficulty"),
                "exercise_topic": exercise.get("topic"),
                "is_correct": attempt["is_correct"],
                "time_spent": attempt.get("time_spent", 60),
                "timestamp": attempt["created_at"].isoformat() if attempt.get("created_at") else "",
                "profile": exercise.get("profile"),
            })
    return formatted


@router.get("/predict-grade")
def predict_grade(user_id: int = Query(1), db=Depends(get_db)):
    predictor = _get_predictor()
    if not predictor:
        raise HTTPException(status_code=500, detail="Modelul ML nu este disponibil")

    attempts = list(db.attempts.find({"user_id": user_id}))

    if len(attempts) < 10:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "insufficient_data",
                "message": "Rezolva minim 10 exercitii pentru predictie",
                "required": 10,
                "current": len(attempts),
            },
        )

    if not predictor.is_trained:
        raise HTTPException(status_code=500, detail="Modelul ML nu este antrenat")

    exercise_ids = [a["exercise_id"] for a in attempts]
    exercises = list(db.exercises.find({"_id": {"$in": exercise_ids}}))
    exercises_map = {e["_id"]: e for e in exercises}

    formatted = _format_attempts(attempts, exercises_map)

    try:
        prediction = predictor.predict(formatted)
        return {"success": True, "prediction": prediction, "message": "Predictie generata cu succes"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/model-info")
def model_info():
    predictor = _get_predictor()
    if not predictor:
        return {
            "is_trained": False,
            "model_type": "Unavailable",
            "message": "Modelul ML nu este disponibil",
        }

    return {
        "is_trained": getattr(predictor, "is_trained", False),
        "model_type": getattr(predictor, "model_type", "unknown"),
        "min_attempts_required": 10,
    }


@router.get("/insights")
def get_insights(user_id: int = Query(1), db=Depends(get_db)):
    attempts = list(db.attempts.find({"user_id": user_id}).sort("created_at", 1))

    if len(attempts) < 5:
        raise HTTPException(
            status_code=400,
            detail="Rezolva minim 5 exercitii pentru insights",
        )

    correct = sum(1 for a in attempts if a["is_correct"])
    accuracy = correct / len(attempts)

    exercise_ids = [a["exercise_id"] for a in attempts]
    exercises = list(db.exercises.find({"_id": {"$in": exercise_ids}}))
    exercises_map = {e["_id"]: e for e in exercises}

    # Group by subject
    subjects = {1: [], 2: [], 3: []}
    for attempt in attempts:
        ex = exercises_map.get(attempt["exercise_id"])
        if ex:
            subjects[ex["subject"]].append(attempt["is_correct"])

    subject_accs = {}
    for s, results in subjects.items():
        subject_accs[s] = sum(results) / len(results) if results else 0

    insights = []

    # Strengths
    best = max(subject_accs.items(), key=lambda x: x[1] if x[1] > 0 else -1)
    if best[1] > 0.7:
        insights.append({
            "type": "strength",
            "message": f"Excelent la Subiectul {best[0]}! ({best[1]*100:.0f}% acuratete)",
        })

    # Weaknesses
    worst = min(subject_accs.items(), key=lambda x: x[1] if x[1] > 0 else 1)
    if 0 < worst[1] < 0.5:
        insights.append({
            "type": "focus",
            "message": f"Concentreaza-te pe Subiectul {worst[0]} pentru imbunatatire",
        })

    # Trend
    if len(attempts) >= 10:
        first_half = attempts[: len(attempts) // 2]
        second_half = attempts[len(attempts) // 2 :]
        first_acc = sum(1 for a in first_half if a["is_correct"]) / len(first_half)
        second_acc = sum(1 for a in second_half if a["is_correct"]) / len(second_half)
        if second_acc > first_acc + 0.1:
            insights.append({
                "type": "positive",
                "message": "Progresezi excelent! Performanta ta se imbunatateste constant.",
            })

    return {
        "success": True,
        "insights": insights,
        "stats": {
            "total_attempts": len(attempts),
            "accuracy": round(accuracy * 100, 1),
            "subject_accuracies": {
                f"subject_{k}": round(v * 100, 1) for k, v in subject_accs.items()
            },
        },
    }
