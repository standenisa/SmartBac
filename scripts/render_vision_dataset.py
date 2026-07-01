"""
Render Vision Dataset — transformă exerciții text → imagini + JSONL pentru Qwen2.5-VL.

Ia fiecare exercițiu din exercises_merged.json, îl renderează ca imagine PNG cu
augmentări variate (fonturi, fundal, rotație, zgomot, contrast), apoi generează
un JSONL în format conversație Qwen2.5-VL.

Usage:
    python scripts/render_vision_dataset.py \
        --input data/processed/exercises_merged.json \
        --output data/vision \
        --augmentations 6
"""

import json
import os
import re
import random
import math
import argparse
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np


# ─── Config ───

BACKGROUNDS = [
    ("white", (255, 255, 255)),
    ("cream", (252, 248, 230)),
    ("grid", None),   # drawn programmatically
    ("lined", None),   # drawn programmatically
    ("gray", (240, 240, 245)),
]

TEXT_COLORS = [
    (15, 15, 15),       # near-black (printed)
    (30, 30, 80),       # dark blue (pen)
    (40, 40, 40),       # charcoal
    (20, 20, 60),       # navy
    (50, 50, 50),       # dark gray (pencil)
]

# Fonts to try (system fonts, fallback to default)
FONT_CANDIDATES = [
    # macOS
    "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "/System/Library/Fonts/Supplemental/Courier New.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Verdana.ttf",
    "/System/Library/Fonts/Supplemental/Palatino.ttc",
    "/System/Library/Fonts/NewYork.ttf",
    "/System/Library/Fonts/Menlo.ttc",
    # Linux / Colab / Kaggle
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
]


def _find_fonts() -> list:
    """Find available system fonts."""
    found = []
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            found.append(path)
    if not found:
        found.append(None)  # will use PIL default
    return found


AVAILABLE_FONTS = _find_fonts()


# ─── Background generators ───

def _bg_solid(w: int, h: int, color: tuple) -> Image.Image:
    return Image.new("RGB", (w, h), color)


def _bg_grid(w: int, h: int) -> Image.Image:
    bg_color = random.choice([(255, 255, 255), (252, 250, 240), (248, 248, 255)])
    img = Image.new("RGB", (w, h), bg_color)
    draw = ImageDraw.Draw(img)
    spacing = random.randint(24, 40)
    line_color = tuple(c - random.randint(15, 35) for c in bg_color)
    for x in range(0, w, spacing):
        draw.line([(x, 0), (x, h)], fill=line_color, width=1)
    for y in range(0, h, spacing):
        draw.line([(0, y), (w, y)], fill=line_color, width=1)
    return img


def _bg_lined(w: int, h: int) -> Image.Image:
    bg_color = (255, 255, 250)
    img = Image.new("RGB", (w, h), bg_color)
    draw = ImageDraw.Draw(img)
    spacing = random.randint(28, 38)
    for y in range(spacing * 2, h, spacing):
        draw.line([(40, y), (w - 40, y)], fill=(200, 200, 210), width=1)
    # Red margin line
    draw.line([(60, 0), (60, h)], fill=(220, 150, 150), width=1)
    return img


def make_background(w: int, h: int) -> Image.Image:
    bg_type, bg_color = random.choice(BACKGROUNDS)
    if bg_type == "grid":
        return _bg_grid(w, h)
    elif bg_type == "lined":
        return _bg_lined(w, h)
    else:
        return _bg_solid(w, h, bg_color)


# ─── Text rendering ───

def _wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Word-wrap text to fit within max_width pixels."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            test = current + " " + word
            bbox = font.getbbox(test)
            if bbox[2] - bbox[0] <= max_width:
                current = test
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def _clean_for_render(text: str) -> str:
    """Clean text for image rendering — make LaTeX readable."""
    t = text
    # Common LaTeX → unicode for visual rendering
    replacements = [
        (r"\\frac\{([^}]*)\}\{([^}]*)\}", r"(\1)/(\2)"),
        (r"\\sqrt\{([^}]*)\}", r"√(\1)"),
        (r"\\int", "∫"),
        (r"\\sum", "∑"),
        (r"\\prod", "∏"),
        (r"\\lim", "lim"),
        (r"\\infty", "∞"),
        (r"\\pi", "π"),
        (r"\\alpha", "α"),
        (r"\\beta", "β"),
        (r"\\gamma", "γ"),
        (r"\\theta", "θ"),
        (r"\\lambda", "λ"),
        (r"\\mu", "μ"),
        (r"\\sigma", "σ"),
        (r"\\delta", "δ"),
        (r"\\epsilon", "ε"),
        (r"\\phi", "φ"),
        (r"\\omega", "ω"),
        (r"\\cdot", "·"),
        (r"\\times", "×"),
        (r"\\div", "÷"),
        (r"\\pm", "±"),
        (r"\\leq", "≤"),
        (r"\\geq", "≥"),
        (r"\\neq", "≠"),
        (r"\\in", "∈"),
        (r"\\subset", "⊂"),
        (r"\\cup", "∪"),
        (r"\\cap", "∩"),
        (r"\\forall", "∀"),
        (r"\\exists", "∃"),
        (r"\\rightarrow", "→"),
        (r"\\Rightarrow", "⇒"),
        (r"\\left\(", "("),
        (r"\\right\)", ")"),
        (r"\\left\[", "["),
        (r"\\right\]", "]"),
        (r"\\left\|", "|"),
        (r"\\right\|", "|"),
        (r"\\\[", ""),
        (r"\\\]", ""),
        (r"\\\(", ""),
        (r"\\\)", ""),
        (r"\\,", " "),
        (r"\\;", " "),
        (r"\\!", ""),
        (r"\\quad", "  "),
        (r"\\text\{([^}]*)\}", r"\1"),
    ]
    for pattern, repl in replacements:
        t = re.sub(pattern, repl, t)
    # Clean remaining backslashes
    t = re.sub(r"\\([a-zA-Z]+)", r"\1", t)
    # Superscripts
    sup_map = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
               "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
               "n": "ⁿ", "x": "ˣ", "i": "ⁱ"}
    def _sup(m):
        s = m.group(1) if m.group(1) else m.group(2)
        return "".join(sup_map.get(c, c) for c in s)
    t = re.sub(r"\^\{([^}]*)\}|\^(\w)", _sup, t)
    # Subscripts
    sub_map = {"0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄",
               "5": "₅", "6": "₆", "7": "₇", "8": "₈", "9": "₉",
               "n": "ₙ", "i": "ᵢ", "k": "ₖ"}
    def _sub(m):
        s = m.group(1) if m.group(1) else m.group(2)
        return "".join(sub_map.get(c, c) for c in s)
    t = re.sub(r"_\{([^}]*)\}|_(\w)", _sub, t)
    return t.strip()


def render_exercise(text: str, aug_id: int) -> Image.Image:
    """Render an exercise as an image with random augmentations."""
    # Choose font
    font_path = random.choice(AVAILABLE_FONTS)
    font_size = random.randint(18, 30)
    try:
        font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    text_color = random.choice(TEXT_COLORS)
    clean_text = _clean_for_render(text)

    # Determine image size from text
    max_text_w = random.randint(600, 1000)
    margin_x = random.randint(40, 80)
    margin_y = random.randint(30, 70)

    lines = _wrap_text(clean_text, font, max_text_w)
    line_height = font_size + random.randint(6, 14)
    text_h = len(lines) * line_height

    img_w = max_text_w + margin_x * 2
    img_h = text_h + margin_y * 2

    # Create background
    img = make_background(img_w, img_h)
    draw = ImageDraw.Draw(img)

    # Draw text
    y = margin_y
    for line in lines:
        draw.text((margin_x, y), line, fill=text_color, font=font)
        y += line_height

    # ─── Augmentations ───

    # Rotation (small)
    angle = random.uniform(-3.5, 3.5)
    if abs(angle) > 0.5:
        img = img.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=(255, 255, 255))

    # Gaussian noise
    if random.random() < 0.5:
        arr = np.array(img).astype(np.float32)
        noise = np.random.normal(0, random.uniform(2, 8), arr.shape)
        arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(arr)

    # Brightness / contrast
    if random.random() < 0.6:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(random.uniform(0.85, 1.15))
    if random.random() < 0.6:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(random.uniform(0.85, 1.2))

    # Slight blur (simulates camera blur)
    if random.random() < 0.3:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.3, 1.0)))

    # Resize to target range
    target_w = random.randint(800, 1200)
    ratio = target_w / img.width
    target_h = int(img.height * ratio)
    img = img.resize((target_w, target_h), Image.LANCZOS)

    return img


# ─── Solution formatting ───

def format_solution(exercise: dict) -> str:
    """Format exercise solution as assistant response."""
    parts = []

    steps = exercise.get("solution_steps") or exercise.get("steps") or []
    if isinstance(steps, list) and steps:
        for i, step in enumerate(steps, 1):
            s = step if isinstance(step, str) else step.get("action", str(step))
            parts.append(f"Pasul {i}: {s}")
    elif exercise.get("solution"):
        parts.append(exercise["solution"])

    answer = exercise.get("answer", "")
    if answer:
        parts.append(f"Răspuns: {answer}")

    if not parts:
        parts.append(f"Răspuns: {answer}")

    return "\n".join(parts)


# ─── Main ───

def main():
    parser = argparse.ArgumentParser(description="Render vision dataset for Qwen2.5-VL")
    parser.add_argument("--input", default="data/processed/exercises_merged.json")
    parser.add_argument("--output", default="data/vision")
    parser.add_argument("--augmentations", type=int, default=6)
    parser.add_argument("--max-exercises", type=int, default=None)
    parser.add_argument("--val-split", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)

    # Load exercises
    with open(args.input, "r", encoding="utf-8") as f:
        exercises = json.load(f)

    if args.max_exercises:
        exercises = exercises[:args.max_exercises]

    print(f"Loaded {len(exercises)} exercises")
    print(f"Augmentations per exercise: {args.augmentations}")
    print(f"Total images to generate: {len(exercises) * args.augmentations}")

    # Create output dirs
    img_dir = Path(args.output) / "images"
    img_dir.mkdir(parents=True, exist_ok=True)

    # Generate images + conversations
    all_samples = []
    skipped = 0

    for idx, ex in enumerate(exercises):
        question = ex.get("question", "").strip()
        if not question or len(question) < 5:
            skipped += 1
            continue

        solution = format_solution(ex)
        if not solution or len(solution) < 3:
            skipped += 1
            continue

        # Use latex field if available, else question
        render_text = ex.get("latex", "") or question

        for aug in range(args.augmentations):
            sample_id = f"ex_{idx:05d}_aug_{aug}"
            img_path = img_dir / f"{sample_id}.png"

            try:
                img = render_exercise(render_text, aug)
                img.save(str(img_path), "PNG", optimize=True)
            except Exception as e:
                print(f"  [SKIP] {sample_id}: {e}")
                continue

            sample = {
                "id": sample_id,
                "image": str(img_path),
                "conversations": [
                    {
                        "role": "user",
                        "content": "<image>\nRezolvă exercițiul din imagine."
                    },
                    {
                        "role": "assistant",
                        "content": solution
                    }
                ]
            }
            all_samples.append(sample)

        if (idx + 1) % 200 == 0:
            print(f"  [{idx+1}/{len(exercises)}] {len(all_samples)} samples generated")

    print(f"\nTotal: {len(all_samples)} samples ({skipped} exercises skipped)")

    # Split train/val
    random.shuffle(all_samples)
    val_count = max(1, int(len(all_samples) * args.val_split))
    val_samples = all_samples[:val_count]
    train_samples = all_samples[val_count:]

    # Write JSONL files
    out_dir = Path(args.output)
    for split_name, split_data in [("train", train_samples), ("val", val_samples)]:
        path = out_dir / f"{split_name}.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            for sample in split_data:
                f.write(json.dumps(sample, ensure_ascii=False) + "\n")
        print(f"Wrote {path} ({len(split_data)} samples)")

    # Summary
    print(f"\n{'='*50}")
    print(f"Dataset ready at: {args.output}/")
    print(f"  images/    — {len(all_samples)} PNG files")
    print(f"  train.jsonl — {len(train_samples)} samples")
    print(f"  val.jsonl   — {len(val_samples)} samples")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
