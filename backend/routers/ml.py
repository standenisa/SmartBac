"""
ML Router - Grade prediction and insights
"""

from fastapi import APIRouter, Depends, Query

from database import get_db

router = APIRouter(prefix="/api/ml", tags=["ml"])

_predictor = None


def _get_predictor():
    global _predictor
    if _predictor is not None:
        return _predictor

    import sys, os
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, backend_dir)

    # Modelul antrenat pe Kaggle (prezicere-note.ipynb) are prioritate
    try:
        from ml_predictor_perfect import PerfectGradePredictor, DEFAULT_MODEL_PATH

        if os.path.exists(DEFAULT_MODEL_PATH):
            predictor = PerfectGradePredictor()
            predictor.load(DEFAULT_MODEL_PATH)
            _predictor = predictor
            return _predictor
    except Exception as e:
        print(f"[ml] kaggle predictor load failed: {e}")

    try:
        from ml_predictor_advanced import AdvancedGradePredictor

        _predictor = AdvancedGradePredictor(model_type="ensemble")

        for name in ("grade_predictor_advanced.pkl", "grade_predictor.pkl"):
            path = os.path.join(backend_dir, "models", name)
            if os.path.exists(path):
                _predictor.load(path)
                break
    except Exception as e:
        print(f"[ml] predictor load failed: {e}")
        _predictor = None

    return _predictor


# Load the model at import time, not lazily: unpickling sklearn models after
# routers/chat.py has loaded the MLX Qwen model segfaults the process, and
# main.py imports this router before chat.
_get_predictor()


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


def _subject_results(db, attempts):
    """Fetch attempted exercises and group correctness by subject."""
    exercise_ids = [a["exercise_id"] for a in attempts]
    exercises = list(db.exercises.find({"_id": {"$in": exercise_ids}}))
    exercises_map = {e["_id"]: e for e in exercises}

    subjects = {1: [], 2: [], 3: []}
    for attempt in attempts:
        ex = exercises_map.get(attempt["exercise_id"])
        if ex:
            subjects[ex.get("subject", 1)].append(attempt["is_correct"])

    return subjects, exercises_map


@router.get("/predict-grade")
def predict_grade(user_id: int = Query(1), db=Depends(get_db)):
    attempts = list(db.attempts.find({"user_id": user_id}))

    if len(attempts) < 3:
        return {
            "success": False,
            "prediction": None,
            "message": f"Rezolva minim 3 exercitii pentru predictie ({len(attempts)}/3)",
        }

    subjects, exercises_map = _subject_results(db, attempts)

    predictor = _get_predictor()
    if predictor and predictor.is_trained and len(attempts) >= 10:
        try:
            formatted = _format_attempts(attempts, exercises_map)
            prediction = predictor.predict(formatted)
            return {"success": True, "prediction": prediction, "message": "Predictie generata cu succes"}
        except Exception:
            pass

    correct = sum(1 for a in attempts if a["is_correct"])
    accuracy = correct / len(attempts)

    subject_acc = {s: sum(r) / len(r) for s, r in subjects.items() if r}

    breakdown = {}
    for s, results in subjects.items():
        if results:
            acc = subject_acc[s]
            breakdown[f"subject_{s}"] = {
                "accuracy": round(acc * 100, 1),
                "estimated_points": round(acc * 30, 1),
                "max_points": 30,
                "exercises_solved": len(results),
            }

    grade = round(1 + accuracy * 9, 2)
    grade = max(1.0, min(10.0, grade))

    insights = []
    if accuracy >= 0.7:
        insights.append({"type": "positive", "message": "Esti pe drumul cel bun! Continua asa."})
    if accuracy < 0.5:
        insights.append({"type": "focus", "message": "Concentreaza-te pe exercitii mai usoare pentru a-ti creste increderea."})
    worst = min(subject_acc.items(), key=lambda x: x[1], default=(None, 1))
    if worst[1] < 0.5:
        insights.append({"type": "focus", "message": f"Concentreaza-te pe Subiectul {worst[0]} pentru imbunatatire."})

    confidence = "low" if len(attempts) < 10 else "medium" if len(attempts) < 30 else "high"

    prediction = {
        "predicted_grade": grade,
        "confidence_interval": [max(1.0, grade - 1.0), min(10.0, grade + 1.0)],
        "confidence_level": confidence,
        "breakdown": breakdown,
        "total_attempts": len(attempts),
        "insights": insights,
        "model_type": "formula",
    }

    return {"success": True, "prediction": prediction, "message": "Predictie generata cu succes"}


@router.get("/model-info")
def model_info():
    predictor = _get_predictor()
    if not predictor:
        return {
            "is_trained": False,
            "model_type": "Unavailable",
            "message": "Modelul ML nu este disponibil",
        }

    info = {
        "is_trained": getattr(predictor, "is_trained", False),
        "model_type": getattr(predictor, "model_type", "unknown"),
        "min_attempts_required": 10,
    }

    holdout = getattr(predictor, "holdout_metrics", None)
    if holdout:
        info["metrics"] = {
            "r2": round(float(holdout.get("holdout_r2", 0)), 3),
            "mae": round(float(holdout.get("holdout_mae", 0)), 3),
            "rmse": round(float(holdout.get("holdout_rmse", 0)), 3),
        }

    return info


@router.get("/insights")
def get_insights(user_id: int = Query(1), db=Depends(get_db)):
    attempts = list(db.attempts.find({"user_id": user_id}).sort("created_at", 1))

    if len(attempts) < 2:
        return {
            "success": True,
            "insights": [{"type": "tip", "message": "Rezolva mai multe exercitii pentru recomandari personalizate."}],
            "stats": {"total_attempts": len(attempts), "accuracy": 0, "subject_accuracies": {}},
        }

    correct = sum(1 for a in attempts if a["is_correct"])
    accuracy = correct / len(attempts)

    subjects, _ = _subject_results(db, attempts)

    subject_accs = {}
    for s, results in subjects.items():
        subject_accs[s] = sum(results) / len(results) if results else 0

    insights = []

    # Strengths
    best = max(subject_accs.items(), key=lambda x: x[1])
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
