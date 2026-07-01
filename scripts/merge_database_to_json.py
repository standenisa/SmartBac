"""
Script simplu: ia exercitiile din exercises_database.py,
le combina cu exercises_merged.json, si salveaza rezultatul.

Rulezi o singura data, apoi uploadezi noul JSON pe Kaggle.
"""

import json
import sys
from pathlib import Path

# Paths
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from exercises_database import EXERCISES_WITH_SOLUTIONS

MERGED_PATH = ROOT / "data" / "processed" / "exercises_merged.json"

# 1. Incarca JSON-ul existent
with open(MERGED_PATH, "r", encoding="utf-8") as f:
    existing = json.load(f)

print(f"Exercitii existente in JSON: {len(existing)}")
print(f"Exercitii in exercises_database.py: {len(EXERCISES_WITH_SOLUTIONS)}")

# 2. Colecteaza intrebarile existente ca sa evitam duplicatele
existing_questions = set()
for ex in existing:
    q = ex.get("question", "").strip().lower()
    if q:
        existing_questions.add(q)

# 3. Converteste exercitiile din Python in formatul JSON
added = 0
for ex in EXERCISES_WITH_SOLUTIONS:
    q = ex.get("question", "").strip().lower()

    # Skip daca deja exista
    if q in existing_questions:
        continue

    # Converteste solution in solution_steps
    solution = ex.get("solution", "")
    steps = []
    if solution:
        for line in solution.split("\n"):
            line = line.strip()
            if line and line.startswith("**Pasul"):
                steps.append(line.replace("**", ""))

    new_entry = {
        "_id": len(existing) + added + 1,
        "question": ex.get("question", ""),
        "answer": ex.get("answer", ""),
        "topic": ex.get("topic", "").lower().replace(" ", "_").replace("ă", "a").replace("ț", "t").replace("ș", "s").replace("î", "i").replace("â", "a"),
        "exercise_type": ex.get("topic", "").lower().replace(" ", "_").replace("ă", "a").replace("ț", "t").replace("ș", "s").replace("î", "i").replace("â", "a"),
        "difficulty": ex.get("difficulty", 1),
        "subject": ex.get("subject", 1),
        "points": ex.get("points", 5),
        "profile": ex.get("profile", "BOTH"),
        "year": None,
        "session": None,
        "solution": solution,
        "solution_steps": steps if steps else [solution] if solution else [],
        "source": "exercises_database",
        "latex": "",
        "hints": []
    }

    existing.append(new_entry)
    existing_questions.add(q)
    added += 1

print(f"\nExercitii noi adaugate: {added}")
print(f"Total final: {len(existing)}")

# 4. Salveaza
with open(MERGED_PATH, "w", encoding="utf-8") as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print(f"\nSalvat in: {MERGED_PATH}")
print("Acum uploadeaza acest fisier pe Kaggle si ruleaza notebook-ul!")
