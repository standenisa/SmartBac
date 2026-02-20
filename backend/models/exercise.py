"""Exercise helpers for MongoDB documents"""


def exercise_to_dict(doc, include_solution=False):
    """Convert a MongoDB exercise document to API response dict."""
    if not doc:
        return None
    data = {
        "id": doc["_id"],
        "question": doc["question"],
        "answer": doc["answer"],
        "difficulty": doc.get("difficulty", 1),
        "topic": doc.get("topic", ""),
        "subject": doc.get("subject", 1),
        "points": doc.get("points", 5),
        "profile": doc.get("profile", "BOTH"),
        "year": doc.get("year"),
        "session": doc.get("session"),
        "exercise_type": doc.get("exercise_type"),
    }
    if include_solution:
        data["solution"] = doc.get("solution")
        data["solution_steps"] = doc.get("solution_steps", [])
        data["hints"] = doc.get("hints", [])
        data["explanation"] = doc.get("explanation")
        data["formula"] = doc.get("formula")
        data["latex"] = doc.get("latex")
    return data
