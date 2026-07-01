"""
Package data for Kaggle upload.

Creates a zip file with the data needed for training notebooks.
Upload the resulting zip as a Kaggle Dataset named 'bac-prep-data'.

Usage:
    python scripts/package_kaggle_data.py
"""

import os
import zipfile

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_ZIP = os.path.join(PROJECT_ROOT, "bac-prep-data.zip")

# Files to include
FILES = [
    "data/processed/exercises_merged.json",
    "data/raw/exercises_bac.json",
    "data/splits/finetune/train.jsonl",
    "data/splits/finetune/val.jsonl",
    "data/splits/finetune/test.jsonl",
    "data/splits/transformer/train.json",
    "data/splits/transformer/val.json",
    "data/splits/transformer/test.json",
]

# Optional files
OPTIONAL = [
    "ai/tokenizer/math_bpe.json",
]


def main():
    print("Packaging data for Kaggle...\n")

    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel_path in FILES:
            full = os.path.join(PROJECT_ROOT, rel_path)
            if os.path.exists(full):
                zf.write(full, rel_path)
                size = os.path.getsize(full)
                print(f"  + {rel_path} ({size / 1024:.1f} KB)")
            else:
                print(f"  ! MISSING: {rel_path}")

        for rel_path in OPTIONAL:
            full = os.path.join(PROJECT_ROOT, rel_path)
            if os.path.exists(full):
                zf.write(full, rel_path)
                size = os.path.getsize(full)
                print(f"  + {rel_path} ({size / 1024:.1f} KB) [optional]")

    zip_size = os.path.getsize(OUTPUT_ZIP)
    print(f"\nCreated: {OUTPUT_ZIP} ({zip_size / 1024:.1f} KB)")
    print("\nNext steps:")
    print("  1. Go to https://www.kaggle.com/datasets")
    print("  2. Click 'New Dataset'")
    print("  3. Name it 'bac-prep-data'")
    print(f"  4. Upload {OUTPUT_ZIP}")
    print("  5. In your notebooks, the data will be at /kaggle/input/bac-prep-data/")


if __name__ == "__main__":
    main()
