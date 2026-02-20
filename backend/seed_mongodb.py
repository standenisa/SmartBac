"""
Seed MongoDB database with exercises from BOTH data sources.

Merges:
  - exercises_database.py  (~150 exercises, IDs 1-150) — has markdown `solution`
  - exercises_with_solutions.py (~92 exercises, IDs 9-100) — has structured fields

For overlapping IDs (9-100): uses exercises_database.py as base, overlays
structured fields (solution_steps, hints, explanation, formula) from
exercises_with_solutions.py.

Run:  cd backend && python seed_mongodb.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from database import db, init_db
from models.user import create_user_doc
from datetime import datetime

# ── Topic → exercise_type mapping ────────────────────────
TOPIC_TYPE_MAP = {
    "Ecuatii liniare": "equation",
    "Ecuații liniare": "equation",
    "Ecuatii de gradul 2": "equation",
    "Ecuații de gradul 2": "equation",
    "Ecuații de gradul 2 - Viète": "equation",
    "Ecuații cu modul": "equation",
    "Ecuații exponențiale": "equation",
    "Ecuații diferențiale": "equation",
    "Sisteme de ecuații": "equation",
    "Sisteme ecuații": "equation",
    "Functii": "function",
    "Funcții": "function",
    "Funcții - Ecuații": "function",
    "Funcții cu modul": "function",
    "Funcții - Zerouri": "function",
    "Funcții - Grafice": "function",
    "Funcții pătratice": "function",
    "Funcții - Tipuri": "function",
    "Studiu funcții": "function",
    "Studiu funcții - Extreme": "function",
    "Logaritmi": "function",
    "Geometrie analitica": "geometry",
    "Geometrie analitică": "geometry",
    "Geometrie analitică - Mijloc": "geometry",
    "Geometrie analitică - Pantă": "geometry",
    "Geometrie analitică - Ecuații": "geometry",
    "Geometrie analitică - Distanță": "geometry",
    "Geometrie spațială": "geometry",
    "Geometrie - Pitagora": "geometry",
    "Vectori": "vector",
    "Vectori - Componente": "vector",
    "Vectori - Adunare": "vector",
    "Vectori - Înmulțire scalar": "vector",
    "Vectori - Modul": "vector",
    "Vectori - Produs scalar": "vector",
    "Vectori - Ortogonalitate": "vector",
    "Matrice": "matrix",
    "Matrice - Operații": "matrix",
    "Matrice - Operații simple": "matrix",
    "Matrice - Determinanți": "matrix",
    "Matrice - Determinanți 3×3": "matrix",
    "Matrice - Înmulțire scalar": "matrix",
    "Matrice - Puteri": "matrix",
    "Matrice - Rang": "matrix",
    "Matrice - Elemente": "matrix",
    "Matrice - Adunare": "matrix",
    "Matrice - Identitate": "matrix",
    "Determinanți": "matrix",
    "Determinanti": "matrix",
    "Determinanți - Proprietăți": "matrix",
    "Limite": "limit",
    "Limite la infinit": "limit",
    "Limite remarcabile": "limit",
    "Derivate": "derivative",
    "Derivate - Produs": "derivative",
    "Derivate - Raport": "derivative",
    "Derivate - Extreme": "derivative",
    "Derivate - Calcul": "derivative",
    "Derivate - Aplicații": "derivative",
    "Derivate - Funcții compuse": "derivative",
    "Integrale": "integral",
    "Integrale definite": "integral",
    "Integrale - Arii": "integral",
    "Primitive": "integral",
    "Combinatorica": "combinatorics",
    "Combinatorică": "combinatorics",
    "Combinatorică - Factorial": "combinatorics",
    "Combinatorică - Permutări": "combinatorics",
    "Combinatorică - Combinări": "combinatorics",
    "Combinatorică - Aranjamente": "combinatorics",
    "Permutari": "combinatorics",
    "Permutări": "combinatorics",
    "Aranjamente": "combinatorics",
    "Combinari": "combinatorics",
    "Combinări": "combinatorics",
    "Probabilitati": "probability",
    "Probabilități": "probability",
    "Numere complexe": "complex_number",
    "Progresii": "sequence",
    "Progresii aritmetice": "sequence",
    "Progresii geometrice": "sequence",
    "Medie aritmetică": "sequence",
    "Trigonometrie": "trigonometry",
}

ACHIEVEMENTS = {
    "first_correct": {"name": "Prima Victorie", "description": "Ai raspuns corect la primul exercitiu", "icon": "star", "xp": 10, "category": "milestone"},
    "streak_3": {"name": "In Forma", "description": "3 raspunsuri corecte la rand", "icon": "fire", "xp": 25, "category": "streak"},
    "streak_5": {"name": "Imbatabil", "description": "5 raspunsuri corecte la rand", "icon": "zap", "xp": 50, "category": "streak"},
    "streak_10": {"name": "Legenda", "description": "10 raspunsuri corecte la rand", "icon": "crown", "xp": 100, "category": "streak"},
    "exercises_10": {"name": "Incepator", "description": "Ai rezolvat 10 exercitii", "icon": "book", "xp": 30, "category": "exercises"},
    "exercises_50": {"name": "Dedicat", "description": "Ai rezolvat 50 exercitii", "icon": "target", "xp": 100, "category": "exercises"},
    "exercises_100": {"name": "Expert", "description": "Ai rezolvat 100 exercitii", "icon": "trophy", "xp": 250, "category": "exercises"},
    "accuracy_80": {"name": "Precizie", "description": "Ai atins 80% acuratete (minim 20 exercitii)", "icon": "target", "xp": 100, "category": "accuracy"},
}


def get_exercise_type(topic: str) -> str:
    """Map topic name to standardized exercise type."""
    if topic in TOPIC_TYPE_MAP:
        return TOPIC_TYPE_MAP[topic]
    for key, value in TOPIC_TYPE_MAP.items():
        if topic.startswith(key.split(" - ")[0]):
            return value
    return "equation"


def merge_exercise_sources():
    """Merge exercises from both sources."""
    from exercises_database import EXERCISES_WITH_SOLUTIONS
    from exercises_with_solutions import exercises_with_solutions

    structured_by_id = {ex["id"]: ex for ex in exercises_with_solutions}

    merged = {}

    for ex in EXERCISES_WITH_SOLUTIONS:
        merged[ex["id"]] = dict(ex)

    for ex_id, structured in structured_by_id.items():
        if ex_id in merged:
            for field in ("solution_steps", "hints", "explanation", "formula"):
                if structured.get(field):
                    merged[ex_id][field] = structured[field]
        else:
            merged[ex_id] = dict(structured)

    return list(merged.values())


def seed():
    print("=== Seeding MongoDB ===\n")

    # Create indexes
    init_db()

    # ── Clear existing data ──
    db.exercises.drop()
    db.achievements.drop()
    db.users.drop()
    db.attempts.drop()
    db.user_achievements.drop()
    db.counters.drop()
    db.exam_simulations.drop()

    # ── Seed exercises ──
    print("Merging exercises from both sources...")
    all_exercises = merge_exercise_sources()
    print(f"  Merged total: {len(all_exercises)} exercises")

    docs = []
    for ex in all_exercises:
        doc = {
            "_id": ex["id"],
            "question": ex["question"],
            "answer": str(ex["answer"]),
            "difficulty": ex.get("difficulty", 1),
            "topic": ex.get("topic", "General"),
            "subject": ex.get("subject", 1),
            "points": ex.get("points", 5),
            "profile": ex.get("profile", "BOTH"),
            "exercise_type": get_exercise_type(ex.get("topic", "")),
            "solution": ex.get("solution"),
            "solution_steps": ex.get("solution_steps", []),
            "hints": ex.get("hints", []),
            "explanation": ex.get("explanation"),
            "formula": ex.get("formula"),
            "latex": ex.get("latex"),
            "year": ex.get("year"),
            "session": ex.get("session"),
            "created_at": datetime.utcnow(),
        }
        docs.append(doc)

    if docs:
        db.exercises.insert_many(docs)
    print(f"  {len(docs)} exercises inserted.")

    # ── Seed achievements ──
    ach_docs = []
    for ach_id, ach_def in ACHIEVEMENTS.items():
        ach_docs.append({
            "_id": ach_id,
            **ach_def,
        })
    db.achievements.insert_many(ach_docs)
    print(f"  {len(ach_docs)} achievements inserted.")

    # ── Create default user ──
    user_doc = create_user_doc(1, "student@bac.ro", "student", "parola123", "M1")
    db.users.insert_one(user_doc)
    print("  Default user created (student@bac.ro / parola123)")

    # ── Initialize counters ──
    db.counters.insert_many([
        {"_id": "users", "seq": 1},
        {"_id": "attempts", "seq": 0},
        {"_id": "exam_simulations", "seq": 0},
    ])

    # Recreate indexes
    init_db()

    # ── Summary ──
    print(f"\n=== Seed complete! ===")
    print(f"  Exercises:    {db.exercises.count_documents({})}")
    print(f"  Achievements: {db.achievements.count_documents({})}")
    print(f"  Users:        {db.users.count_documents({})}")


if __name__ == "__main__":
    seed()
