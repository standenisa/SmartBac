"""Diagrama de arhitectura SmartBAC pe 3 straturi (sus-jos), PNG curat ȘI corect.
Predicția (ensemble regresie) rulează în BACKEND; doar DeepSeek + Qwen pe Kaggle.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "diagrams", "arhitectura_simpla.png")

BLUE_F, BLUE_B = "#E3F2FD", "#1565C0"
GREEN_F, GREEN_B = "#E8F5E9", "#2E7D32"
ORANGE_F, ORANGE_B = "#FFF3E0", "#E65100"
PURPLE_F, PURPLE_B = "#F3E5F5", "#6A1B9A"
DARK = "#202020"
GRAY = "#5A5A5A"

fig, ax = plt.subplots(figsize=(11.5, 7.6), dpi=200)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")


def box(cx, cy, w, h, fc, ec, title, sub, sub_size=10.5, note=None):
    x, y = cx - w / 2, cy - h / 2
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0,rounding_size=2",
                 fc=fc, ec=ec, lw=2.5))
    ax.text(cx, y + h - h * 0.24, title, ha="center", va="center",
            fontsize=15, fontweight="bold", color=ec)
    ax.text(cx, y + h * (0.46 if note else 0.40), sub, ha="center", va="center",
            fontsize=sub_size, color=DARK, linespacing=1.5)
    if note:
        ax.text(cx, y + h * 0.16, note, ha="center", va="center",
                fontsize=9, style="italic", color=ec)


def arrow(x1, y1, x2, y2, color, label, lx, ly):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="<|-|>",
                 mutation_scale=18, lw=2.4, color=color, shrinkA=3, shrinkB=3))
    ax.text(lx, ly, label, ha="center", va="center", fontsize=10,
            style="italic", color=GRAY,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))


# Titlu
ax.text(50, 97, "Arhitectura sistemului — SmartBAC", ha="center", va="center",
        fontsize=18, fontweight="bold", color="#1A237E")

# STRAT 1 — sus
box(50, 83, 40, 13, BLUE_F, BLUE_B, "Aplicație mobilă",
    "React Native + Expo · 16 ecrane")
# STRAT 2 — mijloc (predictia + MathTutor ruleaza AICI)
box(50, 54, 52, 19, GREEN_F, GREEN_B, "Backend — FastAPI",
    "auth · exerciții · gamificare\npredicție · chat · scanare",
    note="rulează pe server: MathTutor + Ensemble regresie (.pkl)")
# STRAT 3 — jos
box(26, 15, 32, 17, ORANGE_F, ORANGE_B, "MongoDB",
    "users · exercises · attempts\nprogress · gamification")
box(74, 15, 40, 18, PURPLE_F, PURPLE_B, "Servicii AI — Kaggle",
    "DeepSeek-R1 — rezolvare exerciții\nQwen3-VL — recunoaștere din imagini",
    sub_size=10)

# Sageti bidirectionale
arrow(50, 76.5, 50, 63.5, BLUE_B, "REST / JSON", 60.5, 70)
arrow(40, 44.5, 33, 24, ORANGE_B, "citește / scrie", 29, 34)
arrow(62, 44.5, 71, 24, PURPLE_B, "cerere / răspuns AI", 76, 35)

plt.savefig(OUT, bbox_inches="tight", facecolor="white", pad_inches=0.3)
print("✅ Salvat:", OUT)
