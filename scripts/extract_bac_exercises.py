#!/usr/bin/env python3
"""
Extract BAC math exercises from PDF exam papers using Claude Vision API.
Pairs each subject PDF with its barem (answer key) PDF, sends page images
to Claude, and outputs structured JSON.
"""

import os
import re
import json
import base64
import time
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict

import fitz  # PyMuPDF
import anthropic

# ─── Config ───────────────────────────────────────────────────────────────────

DESKTOP = Path.home() / "Desktop"
PROJECT = DESKTOP / "bac-prep-ai"
OUTPUT_DIR = PROJECT / "data" / "bac_extracted"

# Load API key from .env files or CLI argument
def load_api_key():
    if os.environ.get("ANTHROPIC_API_KEY"):
        return
    # Check multiple .env locations
    for env_path in [PROJECT / ".env", PROJECT / "backend" / ".env"]:
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "ANTHROPIC_API_KEY" in line:
                    k, v = line.split("=", 1)
                    os.environ["ANTHROPIC_API_KEY"] = v.strip().strip('"').strip("'")
                    print(f"Loaded API key from {env_path}")
                    return
    # Accept as CLI argument: python3 script.py --key sk-ant-...
    for i, arg in enumerate(sys.argv):
        if arg == "--key" and i + 1 < len(sys.argv):
            os.environ["ANTHROPIC_API_KEY"] = sys.argv[i + 1]
            print("Loaded API key from --key argument")
            return
    print("ERROR: ANTHROPIC_API_KEY not found!")
    print("Set it via: export ANTHROPIC_API_KEY=sk-ant-...")
    print("Or: python3 scripts/extract_bac_exercises.py --key sk-ant-...")
    print("Or: add ANTHROPIC_API_KEY=sk-ant-... to .env file in project root")
    sys.exit(1)

load_api_key()

FOLDERS = {
    "mate-info":   DESKTOP / "Subiecte bac mate info",
    "st-nat":      DESKTOP / "Subiecte bac st-nat",
    "tehnologic":  DESKTOP / "Subiecte bac tehnologic",
    "pedagogic":   DESKTOP / "Subiect bac pedagogic",
}

# Claude API
MODEL = "claude-sonnet-4-20250514"
client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env var

# ─── PDF pairing logic ────────────────────────────────────────────────────────

@dataclass
class ExamPair:
    profile: str
    year: str
    session: str
    session_code: str
    subject_pdf: Path
    barem_pdf: Path | None = None

def parse_filename(filename: str) -> dict | None:
    """Parse the standardized MEC filename format."""
    # Examples:
    # 2025_E_c_Matematica_S1_M_mate-info_Subiect_01_LRO.pdf
    # 2025_E_c_Matematica_SM_M_mate-info_Simulare_XII_Subiect_LRO.pdf
    # 2025_E_c_Matematica_SM_M_mate-info_Model_Subiect_LRO.pdf
    # 2026_E_c_Matematica_SM_M_mate-info_Model_Barem_LRO.pdf

    name = filename.replace(".pdf", "")
    parts = name.split("_")

    year = parts[0] if parts else None
    if not year or not year.isdigit():
        return None

    # Determine if this is Subiect or Barem
    is_subiect = "Subiect" in filename
    is_barem = "Barem" in filename
    if not is_subiect and not is_barem:
        return None

    # Extract session code (S1, S2, SS, SM)
    session_code = None
    for p in parts:
        if p in ("S1", "S2", "SS", "SM"):
            session_code = p
            break

    if not session_code:
        return None

    session_map = {
        "S1": "vara",
        "S2": "toamna",
        "SS": "speciala",
        "SM": "model" if "Model" in filename else "simulare",
    }
    session = session_map.get(session_code, session_code)
    # Refine SM: check if it's Model or Simulare
    if session_code == "SM":
        if "Model" in filename:
            session = "model"
        elif "Simulare" in filename:
            session = "simulare"

    # Extract profile
    profile = None
    for prof in ["mate-info", "st-nat", "tehnologic", "pedagogic"]:
        if prof in filename:
            profile = prof
            break

    # Build a matching key (everything except Subiect/Barem distinction)
    # We need to match subjects to barems
    key_parts = []
    key_parts.append(year)
    key_parts.append(session_code)
    key_parts.append(profile or "unknown")
    # Add numeric identifier if present (01, 03, 09, etc.)
    nums = re.findall(r'_(\d{2})_LRO', filename)
    if nums:
        key_parts.append(nums[0])
    elif "Model" in filename:
        key_parts.append("model")
    elif "Simulare" in filename:
        key_parts.append("simulare")

    return {
        "year": year,
        "session": session,
        "session_code": session_code,
        "profile": profile,
        "is_subiect": is_subiect,
        "is_barem": is_barem,
        "match_key": "_".join(key_parts),
    }


def find_exam_pairs(folder: Path, profile: str) -> list[ExamPair]:
    """Find and pair subject + barem PDFs in a folder."""
    if not folder.exists():
        print(f"  WARNING: Folder not found: {folder}")
        return []

    pdfs = sorted(folder.glob("*.pdf"))
    subjects = {}
    barems = {}

    for pdf in pdfs:
        info = parse_filename(pdf.name)
        if not info:
            print(f"  Skipping unparseable: {pdf.name}")
            continue

        # Skip files from wrong profile (e.g. st-nat barem in tehnologic folder)
        if info["profile"] != profile:
            print(f"  Skipping wrong profile ({info['profile']}): {pdf.name}")
            continue

        key = info["match_key"]
        if info["is_subiect"]:
            subjects[key] = (pdf, info)
        elif info["is_barem"]:
            barems[key] = (pdf, info)

    pairs = []
    for key, (subj_pdf, info) in subjects.items():
        barem_pdf = barems.get(key, (None, None))[0]
        pairs.append(ExamPair(
            profile=profile,
            year=info["year"],
            session=info["session"],
            session_code=info["session_code"],
            subject_pdf=subj_pdf,
            barem_pdf=barem_pdf,
        ))
        status = "✓ paired" if barem_pdf else "⚠ no barem"
        print(f"  {status}: {subj_pdf.name}")

    return pairs


# ─── PDF → images ─────────────────────────────────────────────────────────────

def pdf_to_images(pdf_path: Path, dpi: int = 200) -> list[bytes]:
    """Convert PDF pages to PNG image bytes."""
    doc = fitz.open(str(pdf_path))
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        images.append(pix.tobytes("png"))
    doc.close()
    return images


# ─── Claude API extraction ────────────────────────────────────────────────────

EXTRACT_PROMPT = """You are an expert at reading Romanian Baccalaureate math exam papers.

I'm showing you the pages of a BAC math exam paper (SUBIECT) and optionally its answer key (BAREM).

**Exam metadata:**
- Year: {year}
- Session: {session}
- Profile: {profile}

**Your task:** Extract EVERY individual exercise/sub-exercise from this exam into structured JSON.

**IMPORTANT RULES:**
1. The exam has 3 subjects (SUBIECTUL I, SUBIECTUL al II-lea, SUBIECTUL al III-lea), each 30 points.
2. SUBIECTUL I has 6 standalone exercises worth 5p each.
3. SUBIECTUL II and III have 2 problems each, with sub-parts a), b), c) worth 5p each.
4. For sub-parts: create a SEPARATE entry for each sub-part (a, b, c).
5. Include the parent problem statement in each sub-part's text.
6. Preserve ALL mathematical notation as closely as possible (use Unicode math symbols: √, ∈, ∀, ≤, ≥, π, ∞, ∫, Σ, etc.)
7. For matrices, use the format [[a,b],[c,d]].
8. For the solution field, extract the key steps and final answer from the BAREM if provided.
9. Classify each exercise's topic from: algebra, ecuatii, progresii, functii, logaritmi, combinatorica, probabilitate, geometrie, trigonometrie, matrice, determinanti, sisteme, analiza, limite, derivate, integrale, siruri, numere_complexe, vectori
10. Difficulty: "easy" for Sub I problems 1-3, "medium" for Sub I problems 4-6 and Sub II, "hard" for Sub III.

Return ONLY a JSON array (no markdown, no explanation) with this exact structure for each exercise:

[
  {{
    "subject_number": "I",
    "exercise_number": 1,
    "sub_part": null,
    "points": 5,
    "text": "full exercise text in Romanian",
    "topic": "one of the topics listed above",
    "difficulty": "easy/medium/hard",
    "solution": "key solution steps from barem, or null if no barem",
    "answer": "final numerical/symbolic answer, or null"
  }},
  {{
    "subject_number": "II",
    "exercise_number": 1,
    "sub_part": "a",
    "points": 5,
    "text": "parent statement + sub-part text",
    "topic": "...",
    "difficulty": "medium",
    "solution": "...",
    "answer": "..."
  }}
]
"""


def extract_exercises_from_pair(pair: ExamPair, max_retries: int = 2) -> list[dict]:
    """Send exam PDF images to Claude and extract exercises."""

    # Build image content blocks
    content = []

    # Subject pages
    subject_images = pdf_to_images(pair.subject_pdf)
    content.append({"type": "text", "text": f"=== SUBIECT ({pair.subject_pdf.name}) ==="})
    for i, img_bytes in enumerate(subject_images):
        b64 = base64.standard_b64encode(img_bytes).decode()
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": "image/png", "data": b64},
        })

    # Barem pages (if available)
    if pair.barem_pdf:
        barem_images = pdf_to_images(pair.barem_pdf)
        content.append({"type": "text", "text": f"=== BAREM ({pair.barem_pdf.name}) ==="})
        for i, img_bytes in enumerate(barem_images):
            b64 = base64.standard_b64encode(img_bytes).decode()
            content.append({
                "type": "image",
                "source": {"type": "base64", "media_type": "image/png", "data": b64},
            })

    # Add extraction prompt
    prompt = EXTRACT_PROMPT.format(
        year=pair.year,
        session=pair.session,
        profile=pair.profile,
    )
    content.append({"type": "text", "text": prompt})

    for attempt in range(max_retries + 1):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=8000,
                messages=[{"role": "user", "content": content}],
            )

            text = response.content[0].text.strip()

            # Clean up potential markdown wrappers
            if text.startswith("```"):
                text = re.sub(r'^```(?:json)?\n?', '', text)
                text = re.sub(r'\n?```$', '', text)

            exercises = json.loads(text)

            # Add metadata to each exercise
            for ex in exercises:
                ex["year"] = pair.year
                ex["session"] = pair.session
                ex["profile"] = pair.profile

            return exercises

        except json.JSONDecodeError as e:
            print(f"    JSON parse error (attempt {attempt+1}): {e}")
            if attempt < max_retries:
                print(f"    Retrying...")
                time.sleep(2)
            else:
                # Save raw response for debugging
                debug_path = OUTPUT_DIR / "debug" / f"{pair.subject_pdf.stem}_raw.txt"
                debug_path.parent.mkdir(parents=True, exist_ok=True)
                debug_path.write_text(text)
                print(f"    Saved raw response to {debug_path}")
                return []

        except anthropic.RateLimitError:
            wait = 30 * (attempt + 1)
            print(f"    Rate limited, waiting {wait}s...")
            time.sleep(wait)

        except Exception as e:
            print(f"    API error (attempt {attempt+1}): {e}")
            if attempt < max_retries:
                time.sleep(5)
            else:
                return []

    return []


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_exercises = []
    by_profile = {}

    print("=" * 60)
    print("BAC Exercise Extractor")
    print("=" * 60)

    # Step 1: Find all exam pairs
    all_pairs = []
    for profile, folder in FOLDERS.items():
        print(f"\n📁 {profile} ({folder.name}):")
        pairs = find_exam_pairs(folder, profile)
        all_pairs.extend(pairs)

    print(f"\n{'=' * 60}")
    print(f"Found {len(all_pairs)} exam papers to process")
    print(f"{'=' * 60}\n")

    # Step 2: Process each pair
    for i, pair in enumerate(all_pairs):
        label = f"{pair.year} {pair.session} {pair.profile}"
        print(f"\n[{i+1}/{len(all_pairs)}] Processing: {label}")
        print(f"  Subject: {pair.subject_pdf.name}")
        print(f"  Barem:   {pair.barem_pdf.name if pair.barem_pdf else 'NONE'}")

        exercises = extract_exercises_from_pair(pair)
        print(f"  ✓ Extracted {len(exercises)} exercises")

        all_exercises.extend(exercises)
        by_profile.setdefault(pair.profile, []).extend(exercises)

        # Save incremental progress after each pair
        progress_path = OUTPUT_DIR / "exercises_progress.json"
        with open(progress_path, "w", encoding="utf-8") as f:
            json.dump(all_exercises, f, ensure_ascii=False, indent=2)

        # Small delay between API calls
        if i < len(all_pairs) - 1:
            time.sleep(2)

    # Step 3: Save final outputs
    print(f"\n{'=' * 60}")
    print(f"Total exercises extracted: {len(all_exercises)}")

    # Main flat file
    out_path = OUTPUT_DIR / "exercises_bac_all.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_exercises, f, ensure_ascii=False, indent=2)
    print(f"Saved: {out_path}")

    # By-profile files
    for profile, exs in by_profile.items():
        p_path = OUTPUT_DIR / f"exercises_{profile}.json"
        with open(p_path, "w", encoding="utf-8") as f:
            json.dump(exs, f, ensure_ascii=False, indent=2)
        print(f"Saved: {p_path} ({len(exs)} exercises)")

    # MongoDB-ready version (with _id, proper types)
    mongo_exercises = []
    for idx, ex in enumerate(all_exercises):
        mongo_ex = {
            "_id": f"bac_{ex['profile']}_{ex['year']}_{ex['session']}_{ex['subject_number']}_{ex['exercise_number']}",
            "question": ex["text"],
            "topic": ex["topic"],
            "difficulty": {"easy": 1, "medium": 2, "hard": 3}.get(ex["difficulty"], 2),
            "difficulty_label": ex["difficulty"],
            "subject": {"I": 1, "II": 2, "III": 3}.get(ex["subject_number"], 1),
            "subject_roman": ex["subject_number"],
            "exercise_number": ex["exercise_number"],
            "sub_part": ex.get("sub_part"),
            "points": ex["points"],
            "year": int(ex["year"]),
            "session": ex["session"],
            "profile": ex["profile"],
            "answer": ex.get("answer"),
            "solution": ex.get("solution"),
            "source": "bac_official",
        }
        # Make _id unique for sub-parts
        if ex.get("sub_part"):
            mongo_ex["_id"] += f"_{ex['sub_part']}"
        mongo_exercises.append(mongo_ex)

    mongo_path = OUTPUT_DIR / "exercises_bac_mongodb.json"
    with open(mongo_path, "w", encoding="utf-8") as f:
        json.dump(mongo_exercises, f, ensure_ascii=False, indent=2)
    print(f"Saved: {mongo_path} (MongoDB-ready, {len(mongo_exercises)} docs)")

    # Summary stats
    print(f"\n{'=' * 60}")
    print("Summary by profile:")
    for profile, exs in by_profile.items():
        print(f"  {profile}: {len(exs)} exercises")
    print(f"\nSummary by topic:")
    topics = {}
    for ex in all_exercises:
        topics[ex["topic"]] = topics.get(ex["topic"], 0) + 1
    for topic, count in sorted(topics.items(), key=lambda x: -x[1]):
        print(f"  {topic}: {count}")


if __name__ == "__main__":
    main()
