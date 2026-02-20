"""
Seed PostgreSQL database with exercises from BOTH data sources.

Merges:
  - exercises_database.py  (~150 exercises, IDs 1-150) — has markdown `solution`
  - exercises_with_solutions.py (~92 exercises, IDs 9-100) — has structured fields

For overlapping IDs (9-100): uses exercises_database.py as base, overlays
structured fields (solution_steps, hints, explanation, formula) from
exercises_with_solutions.py.

Run:  cd backend && python seed_postgresql.py
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal, init_db
from models.exercise import Exercise
from models.achievement import Achievement
from models.user import User

# ── Topic → exercise_type mapping (comprehensive) ────────────────────────
TOPIC_TYPE_MAP = {
    # Equations
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
    # Functions
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
    # Geometry
    "Geometrie analitica": "geometry",
    "Geometrie analitică": "geometry",
    "Geometrie analitică - Mijloc": "geometry",
    "Geometrie analitică - Pantă": "geometry",
    "Geometrie analitică - Ecuații": "geometry",
    "Geometrie analitică - Distanță": "geometry",
    "Geometrie spațială": "geometry",
    "Geometrie - Pitagora": "geometry",
    # Vectors
    "Vectori": "vector",
    "Vectori - Componente": "vector",
    "Vectori - Adunare": "vector",
    "Vectori - Înmulțire scalar": "vector",
    "Vectori - Modul": "vector",
    "Vectori - Produs scalar": "vector",
    "Vectori - Ortogonalitate": "vector",
    # Matrices
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
    # Limits
    "Limite": "limit",
    "Limite la infinit": "limit",
    "Limite remarcabile": "limit",
    # Derivatives
    "Derivate": "derivative",
    "Derivate - Produs": "derivative",
    "Derivate - Raport": "derivative",
    "Derivate - Extreme": "derivative",
    "Derivate - Calcul": "derivative",
    "Derivate - Aplicații": "derivative",
    "Derivate - Funcții compuse": "derivative",
    # Integrals
    "Integrale": "integral",
    "Integrale definite": "integral",
    "Integrale - Arii": "integral",
    "Primitive": "integral",
    # Combinatorics
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
    # Probability
    "Probabilitati": "probability",
    "Probabilități": "probability",
    # Complex numbers
    "Numere complexe": "complex_number",
    # Sequences
    "Progresii": "sequence",
    "Progresii aritmetice": "sequence",
    "Progresii geometrice": "sequence",
    "Medie aritmetică": "sequence",
    # Trigonometry
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
    """Map topic name to standardized exercise type, with prefix fallback."""
    if topic in TOPIC_TYPE_MAP:
        return TOPIC_TYPE_MAP[topic]
    for key, value in TOPIC_TYPE_MAP.items():
        if topic.startswith(key.split(" - ")[0]):
            return value
    return "equation"


def merge_exercise_sources():
    """Merge exercises from both sources.

    exercises_database.py is the base (IDs 1-150, has `solution` markdown).
    exercises_with_solutions.py overlays structured fields for IDs 9-100.
    """
    from exercises_database import EXERCISES_WITH_SOLUTIONS
    from exercises_with_solutions import exercises_with_solutions

    # Build lookup for structured data
    structured_by_id = {ex["id"]: ex for ex in exercises_with_solutions}

    merged = {}

    # Start with exercises_database as base
    for ex in EXERCISES_WITH_SOLUTIONS:
        merged[ex["id"]] = dict(ex)

    # Overlay structured fields from exercises_with_solutions
    for ex_id, structured in structured_by_id.items():
        if ex_id in merged:
            # Overlay structured fields onto existing entry
            for field in ("solution_steps", "hints", "explanation", "formula"):
                if structured.get(field):
                    merged[ex_id][field] = structured[field]
        else:
            # New exercise not in exercises_database
            merged[ex_id] = dict(structured)

    return list(merged.values())


def seed():
    print("Initializing database...")
    init_db()

    db = SessionLocal()

    try:
        # ── Seed achievements ──
        print("Seeding achievements...")
        for ach_id, ach_def in ACHIEVEMENTS.items():
            existing = db.query(Achievement).filter(Achievement.id == ach_id).first()
            if not existing:
                db.add(Achievement(id=ach_id, **ach_def))
        db.commit()
        print(f"  {len(ACHIEVEMENTS)} achievement definitions seeded.")

        # ── Merge and seed exercises ──
        print("Merging exercises from both sources...")
        all_exercises = merge_exercise_sources()
        print(f"  Merged total: {len(all_exercises)} exercises")

        count = 0
        for ex_data in all_exercises:
            existing = db.query(Exercise).filter(Exercise.id == ex_data["id"]).first()
            if existing:
                continue

            # Serialize list fields to JSON strings
            solution_steps = ex_data.get("solution_steps")
            if solution_steps and isinstance(solution_steps, list):
                solution_steps_json = json.dumps(solution_steps, ensure_ascii=False)
            else:
                solution_steps_json = None

            hints = ex_data.get("hints")
            if hints and isinstance(hints, list):
                hints_json = json.dumps(hints, ensure_ascii=False)
            else:
                hints_json = None

            exercise = Exercise(
                id=ex_data["id"],
                question=ex_data["question"],
                answer=str(ex_data["answer"]),
                difficulty=ex_data.get("difficulty", 1),
                topic=ex_data.get("topic", "General"),
                subject=ex_data.get("subject", 1),
                points=ex_data.get("points", 5),
                profile=ex_data.get("profile", "BOTH"),
                exercise_type=get_exercise_type(ex_data.get("topic", "")),
                solution=ex_data.get("solution"),
                solution_steps=solution_steps_json,
                hints=hints_json,
                explanation=ex_data.get("explanation"),
                formula=ex_data.get("formula"),
            )
            db.add(exercise)
            count += 1

        db.commit()
        print(f"  {count} exercises seeded.")

        # ── Create default user ──
        existing_user = db.query(User).filter(User.id == 1).first()
        if not existing_user:
            user = User(
                email="student@bac.ro",
                username="student",
                profile="M1",
            )
            user.set_password("student123")
            db.add(user)
            db.commit()
            print("  Default user created (student@bac.ro / student123)")

        # ── Summary ──
        total_ex = db.query(Exercise).count()
        total_ach = db.query(Achievement).count()
        total_users = db.query(User).count()
        print(f"\nDatabase seeded successfully!")
        print(f"  Exercises:    {total_ex}")
        print(f"  Achievements: {total_ach}")
        print(f"  Users:        {total_users}")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
