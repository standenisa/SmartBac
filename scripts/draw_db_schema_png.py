"""Schema bazei de date SmartBAC — varianta scurta, curata (stil deck)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "diagrams", "schema_db_simpla.png")

BLUE_F, BLUE_B = "#E3F2FD", "#1565C0"
GREEN_F, GREEN_B = "#E8F5E9", "#2E7D32"
ORANGE_F, ORANGE_B = "#FFF3E0", "#E65100"
DARK = "#202020"
GRAY = "#5A5A5A"

fig, ax = plt.subplots(figsize=(11.5, 7.0), dpi=200)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")


def entity(cx, cy, w, h, fc, ec, title, fields):
    x, y = cx - w / 2, cy - h / 2
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0,rounding_size=1.5",
                 fc=fc, ec=ec, lw=2.5))
    ax.text(cx, y + h - 4.5, title, ha="center", va="center",
            fontsize=14, fontweight="bold", color=ec)
    ax.plot([x + 3, x + w - 3], [y + h - 9, y + h - 9], color=ec, lw=1.2)
    ax.text(x + 4, y + h - 12.5, fields, ha="left", va="top",
            fontsize=10, color=DARK, linespacing=1.6, family="monospace")


def rel(x1, y1, x2, y2, label, lx, ly):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-",
                 lw=2, color=GRAY, shrinkA=2, shrinkB=2))
    ax.text(lx, ly, label, ha="center", va="center", fontsize=11,
            fontweight="bold", color=GRAY,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))


ax.text(50, 97, "Schema bazei de date (MongoDB)", ha="center", va="center",
        fontsize=18, fontweight="bold", color="#1A237E")

# Entitatile principale (conform Tabel 1/2/3 din lucrare)
entity(20, 62, 32, 42, BLUE_F, BLUE_B, "users",
       "_id  (PK)\nname · email\npassword_hash\nxp · level\nstreak_days\nweekly_xp · league")
entity(80, 62, 34, 42, GREEN_F, GREEN_B, "exercises",
       "_id  (PK)\nsubject · topic\ndifficulty\nquestion · answer\nsolution · hints")
entity(50, 22, 36, 32, ORANGE_F, ORANGE_B, "attempts",
       "_id  (PK)\nuser_id  (FK)\nexercise_id  (FK)\nuser_answer\nis_correct · time_spent")

# Relatii 1 — *
rel(27, 44, 41, 37, "1 — ∗", 30, 42)
rel(73, 44, 59, 37, "1 — ∗", 70, 42)

# Nota colectii secundare
ax.text(50, 3,
        "+ 5 colecții: progres SM-2 · achievements · ligi · daily challenge · chat",
        ha="center", va="center", fontsize=11, style="italic", color=DARK)

plt.savefig(OUT, bbox_inches="tight", facecolor="white", pad_inches=0.3)
print("✅ Salvat:", OUT)
