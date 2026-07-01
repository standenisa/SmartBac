"""
Merge extracted BAC exercises into existing dataset and import into MongoDB.

Usage:
    python scripts/merge_and_import.py                # merge + import
    python scripts/merge_and_import.py --merge-only   # just merge JSON, no DB
    python scripts/merge_and_import.py --import-only   # just import to DB
"""

import json
import os
import sys
import argparse

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "backend"))

# --- Field mapping ---

TOPIC_TO_TYPE = {
    "progresii": "sequence",
    "functii": "function",
    "logaritmi": "equation",
    "matrice": "matrix",
    "determinanti": "matrix",
    "sisteme": "equation",
    "ecuatii": "equation",
    "numere_complexe": "complex_number",
    "geometrie": "geometry",
    "trigonometrie": "trigonometry",
    "derivate": "derivative",
    "integrale": "integral",
    "limite": "limit",
    "combinatorica": "combinatorics",
    "probabilitati": "probability",
    "vectori": "vector",
    "primitive": "integral",
    "continuitate": "function",
    "siruri": "sequence",
    "analiza": "function",
    "algebra": "equation",
    "permutari": "combinatorics",
    "aranjamente": "combinatorics",
    "combinari": "combinatorics",
    "binomul_lui_newton": "combinatorics",
}

DIFFICULTY_MAP = {
    "easy": 1,
    "medium": 2,
    "hard": 3,
}

PROFILE_MAP = {
    "mate-info": "M1",
    "st-nat": "M2",
    "tehnologic": "TEHNO",
    "pedagogic": "PEDA",
}

SUBJECT_MAP = {
    "I": 1,
    "II": 2,
    "III": 3,
}


def convert_extracted_to_db_format(ex, next_id):
    """Convert an extracted exercise to the DB document format."""
    topic = ex.get("topic", "")
    exercise_type = TOPIC_TO_TYPE.get(topic, topic)

    difficulty = ex.get("difficulty", "easy")
    if isinstance(difficulty, str):
        difficulty = DIFFICULTY_MAP.get(difficulty, 1)

    profile = PROFILE_MAP.get(ex.get("profile", ""), "BOTH")

    subject_roman = ex.get("subject_number", "I")
    subject = SUBJECT_MAP.get(subject_roman, 1)

    # Build solution steps from solution text
    solution_text = ex.get("solution", "")
    steps = []
    if solution_text:
        # Split on periods or newlines for step breakdown
        parts = [s.strip() for s in solution_text.replace("\n", ". ").split(". ") if s.strip()]
        steps = [f"Step {i+1}: {p}" for i, p in enumerate(parts)]

    return {
        "_id": next_id,
        "question": ex.get("text", ""),
        "answer": ex.get("answer", ""),
        "topic": topic,
        "exercise_type": exercise_type,
        "difficulty": difficulty,
        "subject": subject,
        "subject_roman": subject_roman,
        "points": ex.get("points", 5),
        "profile": profile,
        "year": ex.get("year"),
        "session": ex.get("session"),
        "exercise_number": ex.get("exercise_number"),
        "sub_part": ex.get("sub_part"),
        "solution": solution_text,
        "solution_steps": steps,
        "source": f"BAC {ex.get('year', '')} {ex.get('session', '')}".strip(),
        "latex": "",
        "hints": [],
    }


def convert_existing_to_db_format(ex):
    """Normalize an existing exercise to DB format."""
    return {
        "_id": ex.get("id"),
        "question": ex.get("question", ""),
        "answer": ex.get("answer", ""),
        "topic": ex.get("type", ""),
        "exercise_type": ex.get("type", ""),
        "difficulty": ex.get("difficulty", 1),
        "subject": ex.get("subject", 1),
        "points": 5,
        "profile": ex.get("profile", "BOTH"),
        "year": None,
        "session": None,
        "solution": "",
        "solution_steps": ex.get("steps", []),
        "source": ex.get("source", ""),
        "latex": ex.get("latex", ""),
        "hints": [],
    }


def is_duplicate(new_ex, existing_questions):
    """Check if exercise is a duplicate based on question text similarity."""
    q = new_ex.get("text", "").strip().lower()[:80]
    return q in existing_questions


def merge(existing_path, extracted_path, output_path):
    """Merge existing + extracted exercises into one unified dataset."""
    # Load existing
    with open(existing_path, "r", encoding="utf-8") as f:
        existing = json.load(f)
    print(f"  Existing exercises: {len(existing)}")

    # Load extracted
    with open(extracted_path, "r", encoding="utf-8") as f:
        extracted = json.load(f)
    print(f"  Extracted exercises: {len(extracted)}")

    # Build dedup set from existing questions
    existing_questions = set()
    for ex in existing:
        q = ex.get("question", "").strip().lower()[:80]
        existing_questions.add(q)

    # Convert existing
    merged = []
    for ex in existing:
        merged.append(convert_existing_to_db_format(ex))

    # Add new (non-duplicate) exercises
    next_id = max(ex["_id"] for ex in merged) + 1
    added = 0
    skipped = 0
    for ex in extracted:
        if is_duplicate(ex, existing_questions):
            skipped += 1
            continue
        merged.append(convert_extracted_to_db_format(ex, next_id))
        # Add to dedup set
        q = ex.get("text", "").strip().lower()[:80]
        existing_questions.add(q)
        next_id += 1
        added += 1

    print(f"  Added: {added}, Skipped duplicates: {skipped}")
    print(f"  Total merged: {len(merged)}")

    # Save
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"  Saved to: {output_path}")

    return merged


def import_to_mongodb(exercises):
    """Import exercises into MongoDB."""
    from database import db, init_db

    init_db()

    # Clear existing exercises
    existing_count = db.exercises.count_documents({})
    print(f"  Existing in DB: {existing_count}")

    if existing_count > 0:
        db.exercises.delete_many({})
        print("  Cleared existing exercises")

    # Insert all
    if exercises:
        db.exercises.insert_many(exercises)
        print(f"  Inserted {len(exercises)} exercises")

    # Update counter
    max_id = max(ex["_id"] for ex in exercises) if exercises else 0
    db.counters.update_one(
        {"_id": "exercises"},
        {"$set": {"seq": max_id}},
        upsert=True,
    )
    print(f"  Counter set to: {max_id}")

    # Verify
    count = db.exercises.count_documents({})
    print(f"  Verification - exercises in DB: {count}")

    # Show breakdown
    pipeline = [{"$group": {"_id": "$profile", "count": {"$sum": 1}}}]
    for doc in db.exercises.aggregate(pipeline):
        print(f"    {doc['_id']}: {doc['count']}")


def main():
    parser = argparse.ArgumentParser(description="Merge and import BAC exercises")
    parser.add_argument("--merge-only", action="store_true", help="Only merge JSON files")
    parser.add_argument("--import-only", action="store_true", help="Only import to MongoDB")
    args = parser.parse_args()

    existing_path = os.path.join(PROJECT_ROOT, "data", "raw", "exercises_bac.json")
    extracted_path = os.path.join(PROJECT_ROOT, "data", "bac_extracted", "exercises_bac_all.json")
    output_path = os.path.join(PROJECT_ROOT, "data", "processed", "exercises_merged.json")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if args.import_only:
        print("\n[Import only]")
        with open(output_path, "r", encoding="utf-8") as f:
            exercises = json.load(f)
        print(f"  Loaded {len(exercises)} exercises from {output_path}")
        import_to_mongodb(exercises)
    elif args.merge_only:
        print("\n[Merge only]")
        merge(existing_path, extracted_path, output_path)
    else:
        print("\n[Step 1] Merging exercises...")
        exercises = merge(existing_path, extracted_path, output_path)
        print("\n[Step 2] Importing to MongoDB...")
        import_to_mongodb(exercises)

    print("\nDone!")


if __name__ == "__main__":
    main()
