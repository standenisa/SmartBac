#!/usr/bin/env python3
"""
collect_data.py - Convert existing exercise data into standardized JSON for ML training.

Reads from:
  - backend/exercises_database.py   (EXERCISES_WITH_SOLUTIONS)
  - backend/exercises_with_solutions.py (exercises_with_solutions)

Outputs to:
  - data/raw/exercises_bac.json

Usage:
  python scripts/collect_data.py
  (run from project root)
"""

import json
import os
import re
import sys
from collections import Counter

# ---------------------------------------------------------------------------
# Path setup -- allow imports from backend/ regardless of working directory
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "exercises_bac.json")

sys.path.insert(0, BACKEND_DIR)

from exercises_database import EXERCISES_WITH_SOLUTIONS
from exercises_with_solutions import exercises_with_solutions

# ---------------------------------------------------------------------------
# Topic -> standardized type mapping
# ---------------------------------------------------------------------------
TOPIC_TYPE_MAP = {
    # Equations
    "Ecuații liniare": "equation",
    "Ecuații de gradul 2": "equation",
    "Ecuații de gradul 2 - Viète": "equation",
    "Ecuații cu modul": "equation",
    "Ecuații exponențiale": "equation",
    "Ecuații diferențiale": "equation",
    "Sisteme de ecuații": "equation",
    "Sisteme ecuații": "equation",

    # Functions
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
    "Combinatorică": "combinatorics",
    "Combinatorică - Factorial": "combinatorics",
    "Combinatorică - Permutări": "combinatorics",
    "Combinatorică - Combinări": "combinatorics",
    "Combinatorică - Aranjamente": "combinatorics",
    "Permutări": "combinatorics",
    "Aranjamente": "combinatorics",
    "Combinări": "combinatorics",

    # Probability
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


def topic_to_type(topic: str) -> str:
    """Map a Romanian topic name to a standardized English type string."""
    if topic in TOPIC_TYPE_MAP:
        return TOPIC_TYPE_MAP[topic]

    # Fallback: try prefix matching (e.g. "Derivate - Xyz" -> derivative)
    for key, value in TOPIC_TYPE_MAP.items():
        if topic.startswith(key.split(" - ")[0]):
            return value

    return "other"


# ---------------------------------------------------------------------------
# Simple text -> LaTeX converter
# ---------------------------------------------------------------------------
def text_to_latex(text: str) -> str:
    """
    Convert common math notation in plain text to LaTeX.

    Handles patterns such as:
      x^2       -> x^{2}
      x^10      -> x^{10}
      sqrt(x)   -> \\sqrt{x}
      a/b       -> \\frac{a}{b}   (simple single-token fractions)
      >=, <=    -> \\geq, \\leq
      !=        -> \\neq
      infinity  -> \\infty
      pi        -> \\pi
      *         -> \\cdot
    """
    s = text

    # Remove markdown bold markers
    s = s.replace("**", "")

    # Strip leading descriptive text (e.g. "Rezolvă ecuația:")
    # Try to extract the mathematical expression after the last colon
    if ":" in s:
        after_colon = s.rsplit(":", 1)[1].strip()
        # Only use the part after the colon if it looks mathematical
        if any(ch in after_colon for ch in "=+-*/^xyzXYZ0123456789"):
            s = after_colon

    # Unicode superscripts back to caret notation
    superscript_map = {"²": "^{2}", "³": "^{3}", "⁴": "^{4}", "⁵": "^{5}"}
    for uni, latex in superscript_map.items():
        s = s.replace(uni, latex)

    # sqrt(expr) -> \sqrt{expr}
    s = re.sub(r"sqrt\(([^)]+)\)", r"\\sqrt{\1}", s)

    # Exponents: x^12 or x^2 -> x^{12} or x^{2}
    s = re.sub(r"\^([0-9]+)", r"^{\1}", s)

    # Simple fractions: (expr)/(expr) -> \frac{expr}{expr}
    s = re.sub(r"\(([^)]+)\)/\(([^)]+)\)", r"\\frac{\1}{\2}", s)
    # Single-token fractions: a/b where a,b are single tokens (number or variable)
    s = re.sub(
        r"(?<![\\a-zA-Z])([0-9a-zA-Z]+)/([0-9a-zA-Z]+)(?![{}])",
        r"\\frac{\1}{\2}",
        s,
    )

    # Comparison operators
    s = s.replace(">=", "\\geq ")
    s = s.replace("<=", "\\leq ")
    s = s.replace("!=", "\\neq ")

    # Common symbols
    s = re.sub(r"\binfinity\b", r"\\infty", s)
    s = re.sub(r"\binfinit\b", r"\\infty", s)
    s = re.sub(r"\bpi\b", r"\\pi", s)

    # Multiplication dot (but not inside \frac or other commands)
    s = s.replace("·", "\\cdot ")
    s = s.replace(" * ", " \\cdot ")

    # Clean up whitespace
    s = re.sub(r"\s+", " ", s).strip()

    return s


# ---------------------------------------------------------------------------
# Solution text parsing (from exercises_database.py markdown format)
# ---------------------------------------------------------------------------
def parse_solution_markdown(solution_text: str) -> list:
    """
    Parse the markdown-style solution text from exercises_database.py into
    a list of step strings.

    The format typically contains lines like:
      **Pasul 1:** ...
      **Pasul 2:** ...
    or numbered patterns, or plain lines between headers.
    """
    if not solution_text:
        return []

    lines = solution_text.strip().split("\n")
    steps = []
    current_step = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Skip pure header lines like "**Rezolvare pas cu pas:**"
        if stripped == "**Rezolvare pas cu pas:**":
            continue

        # Detect step markers: **Pasul N:** or **Ecuația dată:** or **Verificare:** etc.
        step_match = re.match(r"\*\*(?:Pasul\s+\d+|Ecuația dată|Verificare|Răspuns)[:\s]?\*\*:?\s*(.*)", stripped)
        if step_match:
            # Save previous step if any
            if current_step:
                steps.append(" ".join(current_step))
                current_step = []

            remainder = step_match.group(1).strip()
            if remainder:
                current_step.append(remainder)
        else:
            # Continuation of current step or standalone line
            # Strip markdown bold markers for cleanliness
            clean = stripped.replace("**", "").strip()
            if clean:
                current_step.append(clean)

    if current_step:
        steps.append(" ".join(current_step))

    # If no structured steps were found, fall back to splitting on non-empty lines
    if not steps:
        for line in lines:
            clean = line.strip().replace("**", "").strip()
            if clean and clean != "Rezolvare pas cu pas:":
                steps.append(clean)

    # Prefix with "Step N:" if not already prefixed
    result = []
    for i, step in enumerate(steps, 1):
        if not re.match(r"^(Step|Pasul)\s+\d+", step, re.IGNORECASE):
            result.append(f"Step {i}: {step}")
        else:
            result.append(step)

    return result


# ---------------------------------------------------------------------------
# Solution steps parsing (from exercises_with_solutions.py structured format)
# ---------------------------------------------------------------------------
def parse_solution_steps(solution_steps: list) -> list:
    """
    Convert the structured solution_steps list (list of dicts with
    step/action/result) into a flat list of step strings.
    """
    if not solution_steps:
        return []

    result = []
    for item in solution_steps:
        step_num = item.get("step", "")
        action = item.get("action", "")
        step_result = item.get("result", "")

        if action and step_result:
            result.append(f"Step {step_num}: {action} -> {step_result}")
        elif action:
            result.append(f"Step {step_num}: {action}")
        elif step_result:
            result.append(f"Step {step_num}: {step_result}")

    return result


# ---------------------------------------------------------------------------
# Extract math expression from question text for LaTeX conversion
# ---------------------------------------------------------------------------
def extract_math_from_question(question: str) -> str:
    """
    Try to extract the core mathematical expression from a question string.
    E.g. 'Rezolva ecuatia: 3x - 5 = 7' -> '3x - 5 = 7'
    """
    # Try to get the part after the last colon
    if ":" in question:
        after = question.rsplit(":", 1)[1].strip()
        if after:
            return after

    # Try to get the part after common Romanian prefixes
    prefixes = [
        r"Rezolv[aăâ]\s+.*?ecuația\s*",
        r"Calculea?ză\s+",
        r"Determină\s+",
        r"Fie\s+.*?,\s*",
    ]
    for prefix in prefixes:
        match = re.search(prefix, question, re.IGNORECASE)
        if match:
            return question[match.end():].strip()

    return question


# ---------------------------------------------------------------------------
# Main conversion logic
# ---------------------------------------------------------------------------
def _claim_id(ex_id, seen_ids: set):
    """Handle duplicate IDs by generating a new unique one."""
    if ex_id in seen_ids:
        ex_id = max(seen_ids) + 1
    seen_ids.add(ex_id)
    return ex_id


def _build_exercise(exercise: dict, ex_id, steps: list, source: str) -> dict:
    """Build the standardized exercise dict shared by both converters."""
    question = exercise.get("question", "")
    math_expr = extract_math_from_question(question)

    return {
        "id": ex_id,
        "question": question,
        "answer": str(exercise.get("answer", "")),
        "type": topic_to_type(exercise.get("topic", "")),
        "steps": steps,
        "latex": text_to_latex(math_expr),
        "source": source,
        "difficulty": exercise.get("difficulty", 1),
        "profile": exercise.get("profile", "BOTH"),
        "subject": exercise.get("subject", 1),
    }


def convert_exercise_db(exercise: dict, seen_ids: set) -> dict:
    """Convert an exercise from exercises_database.py format."""
    ex_id = _claim_id(exercise.get("id", 0), seen_ids)
    steps = parse_solution_markdown(exercise.get("solution", ""))
    return _build_exercise(exercise, ex_id, steps, source="BAC 2024")


def convert_exercise_solutions(exercise: dict, seen_ids: set) -> dict:
    """Convert an exercise from exercises_with_solutions.py format."""
    ex_id = _claim_id(exercise.get("id", 0), seen_ids)

    steps = parse_solution_steps(exercise.get("solution_steps", []))

    # If no structured steps, try to build steps from explanation/hints
    if not steps:
        explanation = exercise.get("explanation", "")
        hints = exercise.get("hints", [])
        if hints:
            steps = [f"Step {i}: {h}" for i, h in enumerate(hints, 1)]
        if explanation:
            steps.append(f"Step {len(steps) + 1}: {explanation}")

    # Extract source year from question if present (e.g. "BAC 2024 Iulie -")
    source = "BAC 2024"
    source_match = re.match(r"(BAC\s+\d{4}(?:\s+\w+)?)", exercise.get("question", ""))
    if source_match:
        source = source_match.group(1)

    return _build_exercise(exercise, ex_id, steps, source=source)


# ---------------------------------------------------------------------------
# Statistics printer
# ---------------------------------------------------------------------------
def print_statistics(exercises: list) -> None:
    """Print summary statistics about the collected dataset."""
    total = len(exercises)
    print(f"\n{'=' * 60}")
    print(f"  DATA COLLECTION COMPLETE")
    print(f"{'=' * 60}")
    print(f"\n  Total exercises collected: {total}")

    # By type
    type_counts = Counter(ex["type"] for ex in exercises)
    print(f"\n  By type:")
    for t, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        bar = "#" * count
        print(f"    {t:<20s} {count:>4d}  {bar}")

    # By difficulty
    diff_counts = Counter(ex["difficulty"] for ex in exercises)
    print(f"\n  By difficulty:")
    for d in sorted(diff_counts.keys()):
        label = {1: "Easy", 2: "Medium", 3: "Hard"}.get(d, f"Level {d}")
        print(f"    {label:<20s} {diff_counts[d]:>4d}")

    # By subject
    subj_counts = Counter(ex["subject"] for ex in exercises)
    print(f"\n  By subject (subiect):")
    for s in sorted(subj_counts.keys()):
        print(f"    Subiectul {s:<12d} {subj_counts[s]:>4d}")

    # By profile
    prof_counts = Counter(ex["profile"] for ex in exercises)
    print(f"\n  By profile:")
    for p, count in sorted(prof_counts.items(), key=lambda x: -x[1]):
        print(f"    {p:<20s} {count:>4d}")

    # By source
    source_counts = Counter(ex["source"] for ex in exercises)
    print(f"\n  By source:")
    for s, count in sorted(source_counts.items(), key=lambda x: -x[1]):
        print(f"    {s:<30s} {count:>4d}")

    # Steps coverage
    with_steps = sum(1 for ex in exercises if ex["steps"])
    print(f"\n  Exercises with steps:    {with_steps}/{total} ({100 * with_steps / total:.1f}%)")

    # LaTeX coverage
    with_latex = sum(1 for ex in exercises if ex["latex"])
    print(f"  Exercises with LaTeX:    {with_latex}/{total} ({100 * with_latex / total:.1f}%)")

    # Unmapped types
    other_count = type_counts.get("other", 0)
    if other_count:
        print(f"\n  WARNING: {other_count} exercises mapped to 'other' (unmapped topic)")

    print(f"\n  Output file: {OUTPUT_FILE}")
    print(f"{'=' * 60}\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Collecting exercise data for ML training...")

    seen_ids = set()
    all_exercises = []

    # Source 1: exercises_database.py
    print(f"  Reading exercises_database.py ... ({len(EXERCISES_WITH_SOLUTIONS)} exercises)")
    for ex in EXERCISES_WITH_SOLUTIONS:
        converted = convert_exercise_db(ex, seen_ids)
        all_exercises.append(converted)

    db_count = len(all_exercises)

    # Source 2: exercises_with_solutions.py
    print(f"  Reading exercises_with_solutions.py ... ({len(exercises_with_solutions)} exercises)")
    for ex in exercises_with_solutions:
        converted = convert_exercise_solutions(ex, seen_ids)
        all_exercises.append(converted)

    sol_count = len(all_exercises) - db_count

    print(f"  Loaded {db_count} from exercises_database.py")
    print(f"  Loaded {sol_count} from exercises_with_solutions.py")

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Write JSON output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_exercises, f, ensure_ascii=False, indent=2)

    print(f"  Written to {OUTPUT_FILE}")

    # Print statistics
    print_statistics(all_exercises)


if __name__ == "__main__":
    main()
