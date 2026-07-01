"""
Generează exerciții complete cu soluții pas cu pas
pentru TOATĂ materia de matematică clasele 9-12.
Output: data/processed/exercises_curriculum.json
"""

import json
import random
import math
from pathlib import Path

random.seed(42)

exercises = []
_id = 3000  # start ID to avoid conflicts


def add(question, answer, steps, topic, difficulty=2, subject=1, cls=9):
    global _id
    _id += 1
    exercises.append({
        "_id": _id,
        "question": question,
        "answer": str(answer),
        "topic": topic,
        "exercise_type": topic,
        "difficulty": difficulty,
        "subject": subject,
        "points": 5,
        "profile": "BOTH",
        "year": None,
        "session": None,
        "solution": "\n".join(steps),
        "solution_steps": steps,
        "source": f"generated_cls{cls}",
        "latex": "",
        "hints": [],
        "class": cls,
    })


# ═══════════════════════════════════════════════════════════════
# CLASA 9 — Algebră și Geometrie
# ═══════════════════════════════════════════════════════════════

# --- Mulțimi și intervale ---
for a, b in [(-3, 5), (0, 7), (-2, 4), (1, 10), (-5, 0)]:
    add(f"Determinați A ∩ B dacă A = [{a}, {b}] și B = [{a+1}, {b+2}].",
        f"[{a+1}, {b}]",
        [f"A = [{a}, {b}], B = [{a+1}, {b+2}]",
         f"A ∩ B conține elementele comune ambelor intervale",
         f"Capătul stâng: max({a}, {a+1}) = {a+1}",
         f"Capătul drept: min({b}, {b+2}) = {b}",
         f"Răspuns: A ∩ B = [{a+1}, {b}]"],
        "multimi", 1, 1, 9)

for a, b in [(-3, 5), (0, 7), (-2, 4)]:
    add(f"Determinați A ∪ B dacă A = [{a}, {b}] și B = [{a+1}, {b+2}].",
        f"[{a}, {b+2}]",
        [f"A = [{a}, {b}], B = [{a+1}, {b+2}]",
         f"A ∪ B conține toate elementele din A sau B",
         f"Capătul stâng: min({a}, {a+1}) = {a}",
         f"Capătul drept: max({b}, {b+2}) = {b+2}",
         f"Răspuns: A ∪ B = [{a}, {b+2}]"],
        "multimi", 1, 1, 9)

# --- Ecuații de gradul I ---
for a, b, c in [(3, -5, 7), (2, 1, 9), (5, -3, 12), (4, 7, -1), (7, -2, 19),
                (6, 3, 15), (8, -1, 23), (3, 4, 13), (9, -6, 21), (2, 8, -4),
                (5, 2, 17), (4, -3, 9), (7, 5, -2), (6, -4, 22), (3, 7, -8)]:
    sol = round((c - b) / a, 4)
    sol_display = f"{c - b}/{a}" if (c - b) % a != 0 else str((c - b) // a)
    add(f"Rezolvă ecuația: {a}x + {b} = {c}",
        sol_display,
        [f"Ecuația: {a}x + {b} = {c}",
         f"Pasul 1: Mutăm {b} în dreapta: {a}x = {c} - ({b}) = {c - b}",
         f"Pasul 2: Împărțim la {a}: x = {c - b}/{a}" + (f" = {(c-b)//a}" if (c-b)%a==0 else ""),
         f"Verificare: {a}·({sol_display}) + {b} = {c} ✓",
         f"Răspuns: x = {sol_display}"],
        "ecuatii_gradul_1", 1, 1, 9)

# --- Ecuații de gradul II ---
for a, b, c, x1, x2 in [(1,-5,6,2,3), (1,-7,12,3,4), (1,3,-10,-5,2), (1,-1,-6,-2,3),
                          (1,-8,15,3,5), (1,2,-15,-5,3), (1,-3,-4,-1,4), (1,-9,20,4,5),
                          (2,-10,12,2,3), (1,-6,8,2,4), (1,1,-12,-4,3), (1,-4,3,1,3),
                          (1,-10,24,4,6), (1,5,6,-2,-3), (1,-2,-8,-2,4),
                          (3,-12,9,1,3), (2,-6,4,1,2), (1,-11,30,5,6),
                          (1,7,10,-2,-5), (1,-13,42,6,7)]:
    delta = b*b - 4*a*c
    add(f"Rezolvă ecuația: {a}x² + ({b})x + ({c}) = 0",
        f"x₁ = {x1}, x₂ = {x2}",
        [f"Ecuația: {a}x² + ({b})x + ({c}) = 0",
         f"Pasul 1: Identificăm a={a}, b={b}, c={c}",
         f"Pasul 2: Δ = b² - 4ac = ({b})² - 4·{a}·({c}) = {b*b} - ({4*a*c}) = {delta}",
         f"Pasul 3: Δ = {delta} > 0, deci ecuația are 2 soluții reale",
         f"Pasul 4: x₁ = (-b - √Δ) / 2a = ({-b} - {int(math.sqrt(delta))}) / {2*a} = {x1}",
         f"Pasul 5: x₂ = (-b + √Δ) / 2a = ({-b} + {int(math.sqrt(delta))}) / {2*a} = {x2}",
         f"Verificare Viète: x₁+x₂ = {x1+x2} = -b/a = {-b}/{a} ✓",
         f"Răspuns: x₁ = {x1}, x₂ = {x2}"],
        "ecuatii_gradul_2", 2, 1, 9)

# --- Sisteme de ecuații liniare 2x2 ---
systems = [
    (2,3,13, 1,-1,1, 4,1),   # 2x+3y=13, x-y=1 => x=4,y=1... nah let me recalculate
]
for a1,b1,c1,a2,b2,c2 in [(2,1,7,1,3,11), (3,2,12,1,-1,1), (1,1,5,2,-1,1),
                            (4,1,9,2,3,13), (3,-1,5,1,2,7), (5,2,16,3,1,10),
                            (1,4,14,3,2,12), (2,3,11,4,1,9), (1,-2,-1,3,1,8),
                            (2,5,19,1,3,11)]:
    det = a1*b2 - a2*b1
    if det == 0:
        continue
    x = (c1*b2 - c2*b1) / det
    y = (a1*c2 - a2*c1) / det
    if x != int(x) or y != int(y):
        continue
    x, y = int(x), int(y)
    add(f"Rezolvă sistemul: {a1}x + {b1}y = {c1} și {a2}x + {b2}y = {c2}",
        f"x = {x}, y = {y}",
        [f"Sistemul: {a1}x + {b1}y = {c1} ... (1)",
         f"         {a2}x + {b2}y = {c2} ... (2)",
         f"Pasul 1: Determinantul: D = {a1}·{b2} - {a2}·{b1} = {det}",
         f"Pasul 2: Dx = {c1}·{b2} - {c2}·{b1} = {c1*b2 - c2*b1}",
         f"Pasul 3: Dy = {a1}·{c2} - {a2}·{c1} = {a1*c2 - a2*c1}",
         f"Pasul 4: x = Dx/D = {c1*b2 - c2*b1}/{det} = {x}",
         f"Pasul 5: y = Dy/D = {a1*c2 - a2*c1}/{det} = {y}",
         f"Verificare: {a1}·{x} + {b1}·{y} = {a1*x + b1*y} = {c1} ✓",
         f"Răspuns: x = {x}, y = {y}"],
        "sisteme_ecuatii", 2, 1, 9)

# --- Inecuații de gradul I ---
for a, b, c in [(3, -2, 7), (5, 1, 16), (2, -4, 8), (4, 3, 15), (7, -1, 20)]:
    sol = (c - b) / a
    add(f"Rezolvă inecuația: {a}x + {b} > {c}",
        f"x > {(c-b)/a}" if (c-b)%a != 0 else f"x > {(c-b)//a}",
        [f"Inecuația: {a}x + {b} > {c}",
         f"Pasul 1: {a}x > {c} - ({b}) = {c - b}",
         f"Pasul 2: x > {c - b}/{a}" + (f" = {(c-b)//a}" if (c-b)%a==0 else ""),
         f"(Împărțim la {a} > 0, semnul se păstrează)",
         f"Răspuns: x ∈ ({(c-b)/a}, +∞)"],
        "inecuatii", 1, 1, 9)

# --- Inecuații de gradul II ---
for a, x1, x2 in [(1, -3, 2), (1, -1, 4), (1, 0, 5), (1, -2, 3), (1, 1, 6)]:
    b = -(x1 + x2)
    c = x1 * x2
    add(f"Rezolvă inecuația: x² + ({b})x + ({c}) < 0",
        f"x ∈ ({x1}, {x2})",
        [f"Inecuația: x² + ({b})x + ({c}) < 0",
         f"Pasul 1: Rezolvăm x² + ({b})x + ({c}) = 0",
         f"Pasul 2: Δ = ({b})² - 4·({c}) = {b*b - 4*c}",
         f"Pasul 3: x₁ = {x1}, x₂ = {x2}",
         f"Pasul 4: Coeficientul lui x² este pozitiv (a=1>0)",
         f"Pasul 5: Parabola e negativă ÎNTRE rădăcini",
         f"Răspuns: x ∈ ({x1}, {x2})"],
        "inecuatii", 2, 1, 9)

# --- Funcții de gradul I ---
for a, b in [(2, 3), (-1, 5), (3, -2), (4, 1), (-2, 7), (1, -3), (5, 2), (-3, 4)]:
    add(f"Fie f: ℝ → ℝ, f(x) = {a}x + {b}. Calculați f(0), f(1), f(-1).",
        f"f(0) = {b}, f(1) = {a + b}, f(-1) = {-a + b}",
        [f"f(x) = {a}x + {b}",
         f"f(0) = {a}·0 + {b} = {b}",
         f"f(1) = {a}·1 + {b} = {a + b}",
         f"f(-1) = {a}·(-1) + {b} = {-a + b}",
         f"Răspuns: f(0) = {b}, f(1) = {a+b}, f(-1) = {-a+b}"],
        "functii_gradul_1", 1, 1, 9)

# --- Funcții de gradul II: vertex, monotonie ---
for a, p, q in [(1, -2, -3), (1, 1, -4), (-1, 2, 1), (2, -1, -5), (1, 3, -2)]:
    b = -2*a*p
    c = a*p*p + q
    add(f"Fie f(x) = {a}x² + ({b})x + ({c}). Determinați vârful parabolei.",
        f"V({p}, {q})",
        [f"f(x) = {a}x² + ({b})x + ({c})",
         f"Pasul 1: xV = -b/(2a) = {-b}/(2·{a}) = {p}",
         f"Pasul 2: yV = f(xV) = f({p}) = {a}·{p}² + ({b})·{p} + ({c})",
         f"       = {a*p*p} + ({b*p}) + ({c}) = {q}",
         f"Răspuns: Vârful parabolei este V({p}, {q})"],
        "functii_gradul_2", 2, 1, 9)

# --- Radicali ---
for n in [2, 3, 8, 12, 18, 27, 32, 48, 50, 72, 75, 98, 128, 200]:
    # Simplificăm √n
    outside = 1
    inside = n
    for p in [2, 3, 5, 7]:
        while inside % (p*p) == 0:
            inside //= (p*p)
            outside *= p
    if inside == 1:
        ans = str(outside)
    else:
        ans = f"{outside}√{inside}"
    add(f"Simplificați √{n}",
        ans,
        [f"√{n}",
         f"Pasul 1: Descompunem {n} în factori primi",
         f"Pasul 2: Scoatem factorii care apar de 2 ori de sub radical",
         f"Răspuns: √{n} = {ans}"],
        "radicali", 1, 1, 9)

# --- Puteri cu exponent rațional ---
for base, exp_num, exp_den in [(4, 3, 2), (8, 2, 3), (27, 2, 3), (16, 3, 4), (9, 5, 2)]:
    result = round(base ** (exp_num / exp_den))
    add(f"Calculați {base}^({exp_num}/{exp_den})",
        str(result),
        [f"{base}^({exp_num}/{exp_den})",
         f"Pasul 1: {base}^({exp_num}/{exp_den}) = (ⁿ√{base})^{exp_num}",
         f"Pasul 2: ⁿ√{base} = {round(base**(1/exp_den))}",
         f"Pasul 3: {round(base**(1/exp_den))}^{exp_num} = {result}",
         f"Răspuns: {result}"],
        "puteri", 1, 1, 9)

# --- Logaritmi ---
for base, arg, result in [(2, 8, 3), (2, 16, 4), (2, 32, 5), (3, 9, 2), (3, 27, 3),
                           (3, 81, 4), (5, 25, 2), (5, 125, 3), (10, 100, 2), (10, 1000, 3),
                           (2, 64, 6), (4, 16, 2), (4, 64, 3), (7, 49, 2), (6, 36, 2)]:
    add(f"Calculați log_{base}({arg})",
        str(result),
        [f"log_{base}({arg}) = ?",
         f"Pasul 1: Căutăm x astfel încât {base}^x = {arg}",
         f"Pasul 2: {base}^{result} = {arg}",
         f"Răspuns: log_{base}({arg}) = {result}"],
        "logaritmi", 1, 1, 9)

# --- Proprietăți logaritmi ---
add("Calculați log₂(8) + log₂(4)", "5",
    ["log₂(8) + log₂(4)", "= log₂(8·4) = log₂(32)", "= 5 (deoarece 2⁵ = 32)", "Răspuns: 5"],
    "logaritmi", 2, 1, 9)
add("Calculați log₃(27) - log₃(9)", "1",
    ["log₃(27) - log₃(9)", "= log₃(27/9) = log₃(3)", "= 1", "Răspuns: 1"],
    "logaritmi", 2, 1, 9)
add("Calculați 2·log₅(5) + log₅(25)", "4",
    ["2·log₅(5) + log₅(25)", "= 2·1 + 2 = 4", "Răspuns: 4"],
    "logaritmi", 2, 1, 9)

# --- Vectori ---
for x1, y1, x2, y2 in [(1,2,4,6), (0,3,5,1), (-1,2,3,-1), (2,5,7,3), (-3,1,2,4)]:
    add(f"Fie A({x1},{y1}) și B({x2},{y2}). Calculați vectorul AB.",
        f"AB = ({x2-x1}, {y2-y1})",
        [f"A({x1},{y1}), B({x2},{y2})",
         f"AB = (xB - xA, yB - yA)",
         f"AB = ({x2} - ({x1}), {y2} - ({y1}))",
         f"AB = ({x2-x1}, {y2-y1})",
         f"Răspuns: AB = ({x2-x1}, {y2-y1})"],
        "vectori", 1, 1, 9)

# Modul vector
for x, y in [(3, 4), (5, 12), (8, 6), (1, 1), (0, 5), (7, 24), (9, 12)]:
    modul = math.sqrt(x*x + y*y)
    modul_str = str(int(modul)) if modul == int(modul) else f"√{x*x+y*y}"
    add(f"Calculați modulul vectorului v = ({x}, {y})",
        f"|v| = {modul_str}",
        [f"v = ({x}, {y})",
         f"|v| = √(x² + y²) = √({x}² + {y}²)",
         f"= √({x*x} + {y*y}) = √{x*x+y*y}",
         f"= {modul_str}",
         f"Răspuns: |v| = {modul_str}"],
        "vectori", 1, 1, 9)

# Produs scalar
for x1,y1,x2,y2 in [(1,2,3,4), (2,-1,1,3), (3,0,0,5), (-1,4,2,1), (5,2,-3,1)]:
    ps = x1*x2 + y1*y2
    add(f"Calculați produsul scalar u·v dacă u = ({x1},{y1}) și v = ({x2},{y2})",
        str(ps),
        [f"u = ({x1},{y1}), v = ({x2},{y2})",
         f"u·v = x₁·x₂ + y₁·y₂",
         f"= {x1}·{x2} + {y1}·{y2}",
         f"= {x1*x2} + {y1*y2} = {ps}",
         f"Răspuns: u·v = {ps}"],
        "vectori", 2, 1, 9)

# --- Geometrie plan: distanță, mijloc ---
for x1,y1,x2,y2 in [(0,0,3,4), (1,2,4,6), (-1,3,5,0), (2,-1,8,7), (0,5,12,0)]:
    dx, dy = x2-x1, y2-y1
    d2 = dx*dx + dy*dy
    d = math.sqrt(d2)
    d_str = str(int(d)) if d == int(d) else f"√{d2}"
    mx, my = (x1+x2)/2, (y1+y2)/2
    add(f"Calculați distanța dintre A({x1},{y1}) și B({x2},{y2})",
        f"d = {d_str}",
        [f"A({x1},{y1}), B({x2},{y2})",
         f"d = √((x₂-x₁)² + (y₂-y₁)²)",
         f"= √(({x2}-{x1})² + ({y2}-{y1})²)",
         f"= √({dx}² + {dy}²) = √({dx*dx} + {dy*dy})",
         f"= √{d2}" + (f" = {int(d)}" if d == int(d) else ""),
         f"Răspuns: d = {d_str}"],
        "geometrie_analitica", 1, 1, 9)

    mx_s = f"{(x1+x2)/2:g}"
    my_s = f"{(y1+y2)/2:g}"
    add(f"Calculați mijlocul segmentului AB dacă A({x1},{y1}) și B({x2},{y2})",
        f"M({mx_s}, {my_s})",
        [f"A({x1},{y1}), B({x2},{y2})",
         f"M = ((xA+xB)/2, (yA+yB)/2)",
         f"= (({x1}+{x2})/2, ({y1}+{y2})/2)",
         f"= ({(x1+x2)/2:g}, {(y1+y2)/2:g})",
         f"Răspuns: M({mx_s}, {my_s})"],
        "geometrie_analitica", 1, 1, 9)

# --- Ecuația dreptei ---
for m, n in [(2, 1), (-1, 3), (3, -2), (1, 5), (-2, 4), (4, -1), (1, 0), (0, 3)]:
    add(f"Scrieți ecuația dreptei cu panta m = {m} care trece prin punctul A(0, {n})",
        f"y = {m}x + {n}" if n >= 0 else f"y = {m}x - {-n}",
        [f"Ecuația dreptei: y = mx + n",
         f"m = {m}, punctul (0, {n}) => n = {n}",
         f"Răspuns: y = {m}x + {n}"],
        "geometrie_analitica", 1, 1, 9)


# ═══════════════════════════════════════════════════════════════
# CLASA 10 — Combinatorică, Matrice, Nr. Complexe
# ═══════════════════════════════════════════════════════════════

# --- Permutări ---
for n in range(3, 9):
    result = math.factorial(n)
    add(f"Calculați P({n}) (numărul de permutări de {n} elemente)",
        str(result),
        [f"P({n}) = {n}!",
         f"= " + "·".join(str(i) for i in range(n, 0, -1)),
         f"= {result}",
         f"Răspuns: P({n}) = {result}"],
        "combinatorica", 1, 1, 10)

# --- Aranjamente ---
for n, k in [(5,2), (6,3), (7,2), (8,3), (4,3), (5,3), (6,2), (9,2), (10,3), (7,4)]:
    result = math.perm(n, k)
    add(f"Calculați A({n},{k})",
        str(result),
        [f"A({n},{k}) = {n}!/({n}-{k})! = {n}!/{n-k}!",
         f"= " + "·".join(str(i) for i in range(n, n-k, -1)),
         f"= {result}",
         f"Răspuns: A({n},{k}) = {result}"],
        "combinatorica", 2, 1, 10)

# --- Combinări ---
for n, k in [(5,2), (6,3), (7,2), (8,3), (4,3), (5,3), (6,4), (10,2), (10,3), (8,5),
             (9,4), (7,3), (12,2), (6,2), (10,4)]:
    result = math.comb(n, k)
    add(f"Calculați C({n},{k})",
        str(result),
        [f"C({n},{k}) = {n}!/({k}!·({n}-{k})!)",
         f"= {n}!/({k}!·{n-k}!)",
         f"= {result}",
         f"Răspuns: C({n},{k}) = {result}"],
        "combinatorica", 2, 1, 10)

# --- Binomul lui Newton ---
for n in [2, 3, 4, 5]:
    terms = []
    for k in range(n + 1):
        coef = math.comb(n, k)
        if k == 0:
            terms.append(f"x^{n}")
        elif k == n:
            terms.append(f"{coef}" if coef > 1 else "1")
        else:
            exp = n - k
            terms.append(f"{coef}x^{exp}" if exp > 1 else f"{coef}x")
    expansion = " + ".join(terms)
    add(f"Dezvoltați (x+1)^{n} folosind binomul lui Newton",
        expansion,
        [f"(x+1)^{n} = Σ C({n},k)·x^({n}-k)·1^k",
         f"= " + expansion,
         f"Răspuns: {expansion}"],
        "combinatorica", 2, 1, 10)

# --- Probabilități ---
add("Se aruncă un zar. Care e probabilitatea să obținem un număr par?",
    "1/2",
    ["Spațiul total: Ω = {1,2,3,4,5,6}, |Ω| = 6",
     "Evenimentul A = {2,4,6}, |A| = 3",
     "P(A) = |A|/|Ω| = 3/6 = 1/2",
     "Răspuns: P = 1/2"],
    "probabilitati", 1, 1, 10)

add("Se aruncă 2 zaruri. Care e probabilitatea ca suma să fie 7?",
    "1/6",
    ["Spațiul total: |Ω| = 6·6 = 36",
     "Cazuri favorabile: (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) = 6",
     "P = 6/36 = 1/6",
     "Răspuns: P = 1/6"],
    "probabilitati", 2, 1, 10)

add("Dintr-o urnă cu 5 bile roșii și 3 albe se extrag 2 bile. P(ambele roșii)?",
    "5/14",
    ["Total bile: 5+3 = 8",
     "Cazuri posibile: C(8,2) = 28",
     "Cazuri favorabile (2 roșii): C(5,2) = 10",
     "P = 10/28 = 5/14",
     "Răspuns: P = 5/14"],
    "probabilitati", 2, 1, 10)

add("Se aruncă o monedă de 3 ori. P(exact 2 capete)?",
    "3/8",
    ["Spațiul total: |Ω| = 2³ = 8",
     "Cazuri favorabile: C(3,2) = 3 (alegem 2 din 3 aruncări pt cap)",
     "P = 3/8",
     "Răspuns: P = 3/8"],
    "probabilitati", 2, 1, 10)

for n_total, n_fav, desc in [
    (52, 4, "Se extrage o carte dintr-un pachet de 52. P(as)?"),
    (52, 13, "Se extrage o carte dintr-un pachet de 52. P(inimă)?"),
    (52, 12, "Se extrage o carte dintr-un pachet de 52. P(figură)?"),
]:
    from math import gcd
    g = gcd(n_fav, n_total)
    add(desc, f"{n_fav//g}/{n_total//g}",
        [f"Total: {n_total} cărți",
         f"Favorabile: {n_fav}",
         f"P = {n_fav}/{n_total} = {n_fav//g}/{n_total//g}",
         f"Răspuns: P = {n_fav//g}/{n_total//g}"],
        "probabilitati", 1, 1, 10)

# --- Matrice: adunare, înmulțire ---
for (a,b,c,d), (e,f,g,h) in [((1,2,3,4),(5,6,7,8)), ((2,0,1,3),(1,4,2,1)),
                                ((3,1,0,2),(1,2,3,4)), ((-1,2,3,0),(4,1,-2,5))]:
    add(f"Calculați A + B dacă A = [[{a},{b}],[{c},{d}]] și B = [[{e},{f}],[{g},{h}]]",
        f"[[{a+e},{b+f}],[{c+g},{d+h}]]",
        [f"A + B = [[{a}+{e}, {b}+{f}], [{c}+{g}, {d}+{h}]]",
         f"= [[{a+e}, {b+f}], [{c+g}, {d+h}]]",
         f"Răspuns: [[{a+e},{b+f}],[{c+g},{d+h}]]"],
        "matrice", 1, 1, 10)

# Înmulțire matrice 2x2
for (a,b,c,d), (e,f,g,h) in [((1,2,3,4),(5,6,7,8)), ((2,1,0,3),(1,0,2,1)),
                                ((1,0,0,1),(3,4,5,6)), ((2,3,1,4),(1,2,3,1))]:
    r11 = a*e + b*g
    r12 = a*f + b*h
    r21 = c*e + d*g
    r22 = c*f + d*h
    add(f"Calculați A·B dacă A = [[{a},{b}],[{c},{d}]] și B = [[{e},{f}],[{g},{h}]]",
        f"[[{r11},{r12}],[{r21},{r22}]]",
        [f"(A·B)₁₁ = {a}·{e} + {b}·{g} = {a*e} + {b*g} = {r11}",
         f"(A·B)₁₂ = {a}·{f} + {b}·{h} = {a*f} + {b*h} = {r12}",
         f"(A·B)₂₁ = {c}·{e} + {d}·{g} = {c*e} + {d*g} = {r21}",
         f"(A·B)₂₂ = {c}·{f} + {d}·{h} = {c*f} + {d*h} = {r22}",
         f"Răspuns: A·B = [[{r11},{r12}],[{r21},{r22}]]"],
        "matrice", 2, 1, 10)

# --- Determinanți 2x2 ---
for a,b,c,d in [(3,1,2,4), (5,2,3,1), (1,0,0,1), (4,-1,2,3), (2,5,1,3),
                (6,2,4,1), (7,3,2,5), (-1,4,3,2), (8,1,3,4), (5,0,2,7)]:
    det = a*d - b*c
    add(f"Calculați determinantul: |{a} {b}; {c} {d}|",
        str(det),
        [f"det = {a}·{d} - {b}·{c}",
         f"= {a*d} - {b*c}",
         f"= {det}",
         f"Răspuns: det = {det}"],
        "determinanti", 1, 1, 10)

# --- Determinanți 3x3 (Sarrus) ---
for (a,b,c,d,e,f,g,h,i) in [
    (1,2,3,4,5,6,7,8,9), (2,1,0,1,3,2,0,2,1), (1,0,2,0,1,0,3,0,1),
    (3,1,2,1,4,1,2,1,5), (1,2,1,3,1,2,1,3,1)]:
    det = a*(e*i-f*h) - b*(d*i-f*g) + c*(d*h-e*g)
    add(f"Calculați determinantul matricei 3×3: [[{a},{b},{c}],[{d},{e},{f}],[{g},{h},{i}]]",
        str(det),
        [f"Folosim regula lui Sarrus sau dezvoltare după prima linie:",
         f"det = {a}·({e}·{i}-{f}·{h}) - {b}·({d}·{i}-{f}·{g}) + {c}·({d}·{h}-{e}·{g})",
         f"= {a}·{e*i-f*h} - {b}·{d*i-f*g} + {c}·{d*h-e*g}",
         f"= {a*(e*i-f*h)} + ({-b*(d*i-f*g)}) + {c*(d*h-e*g)}",
         f"= {det}",
         f"Răspuns: det = {det}"],
        "determinanti", 2, 1, 10)

# --- Numere complexe ---
for a1,b1,a2,b2 in [(2,3,1,4), (3,-1,2,5), (1,1,-2,3), (4,2,1,-1), (5,0,0,3),
                      (-1,2,3,1), (2,-3,4,2), (0,5,3,0)]:
    add(f"Calculați z₁ + z₂ dacă z₁ = {a1}+{b1}i și z₂ = {a2}+{b2}i",
        f"{a1+a2}+{b1+b2}i" if b1+b2>=0 else f"{a1+a2}{b1+b2}i",
        [f"z₁ + z₂ = ({a1}+{b1}i) + ({a2}+{b2}i)",
         f"= ({a1}+{a2}) + ({b1}+{b2})i",
         f"= {a1+a2} + {b1+b2}i",
         f"Răspuns: z₁+z₂ = {a1+a2}+{b1+b2}i"],
        "numere_complexe", 1, 1, 10)

# Înmulțire complexe
for a1,b1,a2,b2 in [(1,2,3,4), (2,1,1,3), (3,-1,2,2), (1,1,1,-1)]:
    re = a1*a2 - b1*b2
    im = a1*b2 + b1*a2
    add(f"Calculați z₁·z₂ dacă z₁ = {a1}+{b1}i și z₂ = {a2}+{b2}i",
        f"{re}+{im}i" if im >= 0 else f"{re}{im}i",
        [f"z₁·z₂ = ({a1}+{b1}i)·({a2}+{b2}i)",
         f"= {a1}·{a2} + {a1}·{b2}i + {b1}i·{a2} + {b1}·{b2}·i²",
         f"= {a1*a2} + {a1*b2}i + {b1*a2}i + ({b1*b2})·(-1)",
         f"= ({a1*a2} - {b1*b2}) + ({a1*b2} + {b1*a2})i",
         f"= {re} + {im}i",
         f"Răspuns: z₁·z₂ = {re}+{im}i"],
        "numere_complexe", 2, 1, 10)

# Modul număr complex
for a, b in [(3,4), (5,12), (1,1), (0,5), (8,6), (2,3), (7,24)]:
    modul = math.sqrt(a*a + b*b)
    m_str = str(int(modul)) if modul == int(modul) else f"√{a*a+b*b}"
    add(f"Calculați |z| dacă z = {a}+{b}i",
        m_str,
        [f"|z| = √(a² + b²) = √({a}² + {b}²)",
         f"= √({a*a} + {b*b}) = √{a*a+b*b}",
         f"= {m_str}",
         f"Răspuns: |z| = {m_str}"],
        "numere_complexe", 1, 1, 10)

# Conjugat
for a, b in [(3, 4), (2, -1), (0, 5), (-1, 3), (4, 2)]:
    add(f"Calculați conjugatul lui z = {a}+{b}i",
        f"{a}+{-b}i" if -b >= 0 else f"{a}{-b}i",
        [f"Conjugatul lui z = a+bi este z̄ = a-bi",
         f"z = {a}+{b}i => z̄ = {a}-({b})i = {a}+{-b}i",
         f"Răspuns: z̄ = {a}{'-' if b>0 else '+'}{abs(b)}i"],
        "numere_complexe", 1, 1, 10)

# --- Progresii aritmetice ---
for a1, r in [(2, 3), (5, -2), (1, 4), (10, -3), (0, 7), (3, 5), (-2, 6)]:
    for n in [5, 10, 15]:
        an = a1 + (n-1)*r
        sn = n * (a1 + an) // 2
        add(f"PA cu a₁ = {a1}, r = {r}. Calculați a_{n} și S_{n}.",
            f"a_{n} = {an}, S_{n} = {sn}",
            [f"a₁ = {a1}, r = {r}",
             f"aₙ = a₁ + (n-1)·r = {a1} + ({n}-1)·{r} = {a1} + {(n-1)*r} = {an}",
             f"Sₙ = n·(a₁+aₙ)/2 = {n}·({a1}+{an})/2 = {n}·{a1+an}/2 = {sn}",
             f"Răspuns: a_{n} = {an}, S_{n} = {sn}"],
            "progresii_aritmetice", 2, 1, 10)

# --- Progresii geometrice ---
for b1, q in [(2, 3), (1, 2), (3, 2), (5, -2), (4, 3)]:
    for n in [4, 5, 6]:
        bn = b1 * q**(n-1)
        sn = b1 * (q**n - 1) // (q - 1) if q != 1 else b1 * n
        add(f"PG cu b₁ = {b1}, q = {q}. Calculați b_{n} și S_{n}.",
            f"b_{n} = {bn}, S_{n} = {sn}",
            [f"b₁ = {b1}, q = {q}",
             f"bₙ = b₁·qⁿ⁻¹ = {b1}·{q}^{n-1} = {b1}·{q**(n-1)} = {bn}",
             f"Sₙ = b₁·(qⁿ-1)/(q-1) = {b1}·({q**n}-1)/({q}-1) = {sn}",
             f"Răspuns: b_{n} = {bn}, S_{n} = {sn}"],
            "progresii_geometrice", 2, 1, 10)


# ═══════════════════════════════════════════════════════════════
# CLASA 11 — Limite, Derivate, Studiu funcții
# ═══════════════════════════════════════════════════════════════

# --- Limite la infinit ---
for a, b, c, d in [(2,1,3,-1), (1,3,1,-2), (5,0,2,1), (3,-1,4,2), (1,1,1,1)]:
    add(f"Calculați lim(x→∞) ({a}x² + {b}x) / ({c}x² + {d}x)",
        f"{a}/{c}",
        [f"lim(x→∞) ({a}x² + {b}x) / ({c}x² + {d}x)",
         f"Pasul 1: Împărțim la x² (puterea maximă)",
         f"= lim ({a} + {b}/x) / ({c} + {d}/x)",
         f"Pasul 2: Când x→∞, {b}/x→0 și {d}/x→0",
         f"= {a}/{c}",
         f"Răspuns: limita = {a}/{c}"],
        "limite", 2, 2, 11)

# --- Limite remarcabile ---
add("Calculați lim(x→0) sin(x)/x", "1",
    ["Aceasta este limita remarcabilă fundamentală",
     "lim(x→0) sin(x)/x = 1",
     "Răspuns: 1"],
    "limite", 2, 2, 11)
add("Calculați lim(x→0) (eˣ - 1)/x", "1",
    ["Limită remarcabilă: lim(x→0) (eˣ-1)/x = 1",
     "Răspuns: 1"],
    "limite", 2, 2, 11)
add("Calculați lim(x→0) ln(1+x)/x", "1",
    ["Limită remarcabilă: lim(x→0) ln(1+x)/x = 1",
     "Răspuns: 1"],
    "limite", 2, 2, 11)
add("Calculați lim(x→∞) (1 + 1/x)^x", "e",
    ["Limită remarcabilă: lim(x→∞) (1+1/x)^x = e",
     "Aceasta este definiția numărului e ≈ 2.718",
     "Răspuns: e"],
    "limite", 2, 2, 11)

# --- Limite cu factorizare (forma 0/0) ---
for a in [1, 2, 3, 4, 5]:
    add(f"Calculați lim(x→{a}) (x² - {a*a})/(x - {a})",
        f"{2*a}",
        [f"Forma 0/0: la x={a}, numărătorul={a}²-{a*a}=0, numitorul={a}-{a}=0",
         f"Factorizăm: x²-{a*a} = (x-{a})(x+{a})",
         f"lim = lim (x-{a})(x+{a})/(x-{a}) = lim (x+{a})",
         f"= {a}+{a} = {2*a}",
         f"Răspuns: {2*a}"],
        "limite", 2, 2, 11)

# --- Derivate funcții elementare ---
derivate_data = [
    ("x²", "2x", ["(x²)' = 2x (regula puterii: n·xⁿ⁻¹)"]),
    ("x³", "3x²", ["(x³)' = 3x² (regula puterii)"]),
    ("x⁴", "4x³", ["(x⁴)' = 4x³ (regula puterii)"]),
    ("5x³", "15x²", ["(5x³)' = 5·3x² = 15x²"]),
    ("x³ - 3x² + 2x", "3x² - 6x + 2", ["Derivăm termen cu termen:", "(x³)' = 3x²", "(-3x²)' = -6x", "(2x)' = 2", "f'(x) = 3x² - 6x + 2"]),
    ("x⁴ - 2x³ + x", "4x³ - 6x² + 1", ["(x⁴)' = 4x³", "(-2x³)' = -6x²", "(x)' = 1", "f'(x) = 4x³ - 6x² + 1"]),
    ("eˣ", "eˣ", ["(eˣ)' = eˣ"]),
    ("ln(x)", "1/x", ["(ln x)' = 1/x"]),
    ("sin(x)", "cos(x)", ["(sin x)' = cos x"]),
    ("cos(x)", "-sin(x)", ["(cos x)' = -sin x"]),
    ("tg(x)", "1/cos²(x)", ["(tg x)' = 1/cos²x"]),
    ("√x", "1/(2√x)", ["(√x)' = (x^(1/2))' = (1/2)·x^(-1/2) = 1/(2√x)"]),
    ("1/x", "-1/x²", ["(1/x)' = (x⁻¹)' = -x⁻² = -1/x²"]),
    ("x·eˣ", "(1+x)·eˣ", ["Regula produsului: (fg)' = f'g + fg'", "(x)' · eˣ + x · (eˣ)' = eˣ + x·eˣ = (1+x)·eˣ"]),
    ("x²·sin(x)", "2x·sin(x) + x²·cos(x)", ["Regula produsului:", "(x²)'·sin(x) + x²·(sin(x))'", "= 2x·sin(x) + x²·cos(x)"]),
    ("ln(x²+1)", "2x/(x²+1)", ["Regula lanțului: (ln u)' = u'/u", "u = x²+1, u' = 2x", "f'(x) = 2x/(x²+1)"]),
    ("e^(2x)", "2e^(2x)", ["Regula lanțului: (eᵘ)' = u'·eᵘ", "u = 2x, u' = 2", "f'(x) = 2·e^(2x)"]),
    ("sin(2x)", "2cos(2x)", ["Regula lanțului: (sin u)' = u'·cos u", "u = 2x, u' = 2", "f'(x) = 2·cos(2x)"]),
    ("(2x+1)³", "6(2x+1)²", ["Regula lanțului: (uⁿ)' = n·uⁿ⁻¹·u'", "u = 2x+1, u' = 2", "f'(x) = 3·(2x+1)²·2 = 6(2x+1)²"]),
    ("x/(x+1)", "1/(x+1)²", ["Regula câtului: (f/g)' = (f'g - fg')/g²", "f=x, f'=1, g=x+1, g'=1", "= (1·(x+1) - x·1)/(x+1)² = 1/(x+1)²"]),
]

for func, deriv, steps in derivate_data:
    add(f"Calculați derivata funcției f(x) = {func}",
        f"f'(x) = {deriv}",
        steps + [f"Răspuns: f'(x) = {deriv}"],
        "derivate", 2, 2, 11)

# --- Tangenta la grafic ---
for func, deriv_fn, x0 in [("x²", lambda x: 2*x, 1), ("x²", lambda x: 2*x, 2),
                             ("x³", lambda x: 3*x*x, 1), ("x²-2x", lambda x: 2*x-2, 3)]:
    fn_vals = {"x²": lambda x: x**2, "x³": lambda x: x**3, "x²-2x": lambda x: x**2-2*x}
    y0 = fn_vals[func](x0)
    m = deriv_fn(x0)
    add(f"Scrieți ecuația tangentei la graficul f(x) = {func} în x₀ = {x0}",
        f"y = {m}x + {y0 - m*x0}" if y0 - m*x0 >= 0 else f"y = {m}x - {-(y0 - m*x0)}",
        [f"f(x) = {func}",
         f"Pasul 1: f({x0}) = {y0}",
         f"Pasul 2: f'({x0}) = {m} (panta tangentei)",
         f"Pasul 3: y - {y0} = {m}(x - {x0})",
         f"y = {m}x + {y0 - m*x0}",
         f"Răspuns: y = {m}x + {y0 - m*x0}"],
        "derivate", 2, 2, 11)

# --- Monotonie ---
add("Studiați monotonia funcției f(x) = x³ - 3x",
    "Crescătoare pe (-∞,-1)∪(1,+∞), descrescătoare pe (-1,1)",
    ["f(x) = x³ - 3x",
     "f'(x) = 3x² - 3 = 3(x²-1) = 3(x-1)(x+1)",
     "f'(x) = 0 => x = -1 sau x = 1",
     "f'(x) > 0 pentru x < -1 sau x > 1 (crescătoare)",
     "f'(x) < 0 pentru -1 < x < 1 (descrescătoare)",
     "Răspuns: f crescătoare pe (-∞,-1)∪(1,+∞), descrescătoare pe (-1,1)"],
    "studiu_functie", 3, 2, 11)

add("Determinați punctele de extrem ale funcției f(x) = x³ - 12x + 1",
    "Maxim local în x=-2, minim local în x=2",
    ["f'(x) = 3x² - 12 = 3(x²-4) = 3(x-2)(x+2)",
     "f'(x) = 0 => x = -2, x = 2",
     "f''(x) = 6x",
     "f''(-2) = -12 < 0 => maxim local în x=-2, f(-2) = -8+24+1 = 17",
     "f''(2) = 12 > 0 => minim local în x=2, f(2) = 8-24+1 = -15",
     "Răspuns: Maxim local (-2, 17), minim local (2, -15)"],
    "studiu_functie", 3, 2, 11)

# --- Asimptote ---
add("Determinați asimptotele funcției f(x) = (2x+1)/(x-1)",
    "AV: x=1, AO: y=2",
    ["f(x) = (2x+1)/(x-1)",
     "Asimptota verticală: numitorul = 0 => x = 1",
     "Asimptota orizontală: lim(x→∞) (2x+1)/(x-1) = 2",
     "Răspuns: AV: x = 1, AO: y = 2"],
    "studiu_functie", 3, 2, 11)


# ═══════════════════════════════════════════════════════════════
# CLASA 12 — Integrale, Primitive
# ═══════════════════════════════════════════════════════════════

# --- Primitive (integrale nedefinite) ---
integrale_data = [
    ("∫ x dx", "x²/2 + C", ["∫ x dx = x^(1+1)/(1+1) + C = x²/2 + C"]),
    ("∫ x² dx", "x³/3 + C", ["∫ x² dx = x³/3 + C"]),
    ("∫ x³ dx", "x⁴/4 + C", ["∫ x³ dx = x⁴/4 + C"]),
    ("∫ (3x² + 2x) dx", "x³ + x² + C", ["∫ 3x² dx = x³", "∫ 2x dx = x²", "Rezultat: x³ + x² + C"]),
    ("∫ (x³ - 4x + 1) dx", "x⁴/4 - 2x² + x + C", ["∫ x³ dx = x⁴/4", "∫ -4x dx = -2x²", "∫ 1 dx = x", "Rezultat: x⁴/4 - 2x² + x + C"]),
    ("∫ eˣ dx", "eˣ + C", ["∫ eˣ dx = eˣ + C"]),
    ("∫ (1/x) dx", "ln|x| + C", ["∫ (1/x) dx = ln|x| + C"]),
    ("∫ sin(x) dx", "-cos(x) + C", ["∫ sin(x) dx = -cos(x) + C"]),
    ("∫ cos(x) dx", "sin(x) + C", ["∫ cos(x) dx = sin(x) + C"]),
    ("∫ (1/cos²x) dx", "tg(x) + C", ["∫ (1/cos²x) dx = tg(x) + C"]),
    ("∫ e^(3x) dx", "e^(3x)/3 + C", ["Substituție: u = 3x, du = 3dx", "∫ eᵘ · du/3 = eᵘ/3 + C = e^(3x)/3 + C"]),
    ("∫ (2x+1)³ dx", "(2x+1)⁴/8 + C", ["u = 2x+1, du = 2dx", "∫ u³ · du/2 = u⁴/8 + C = (2x+1)⁴/8 + C"]),
    ("∫ x·eˣ dx", "(x-1)·eˣ + C", ["Integrare prin părți: u=x, dv=eˣdx", "du=dx, v=eˣ", "= x·eˣ - ∫eˣdx = x·eˣ - eˣ + C = (x-1)·eˣ + C"]),
    ("∫ ln(x) dx", "x·ln(x) - x + C", ["Integrare prin părți: u=ln(x), dv=dx", "du=1/x dx, v=x", "= x·ln(x) - ∫x·(1/x)dx = x·ln(x) - x + C"]),
    ("∫ x·cos(x) dx", "x·sin(x) + cos(x) + C", ["Integrare prin părți: u=x, dv=cos(x)dx", "du=dx, v=sin(x)", "= x·sin(x) - ∫sin(x)dx = x·sin(x) + cos(x) + C"]),
]

for expr, result, steps in integrale_data:
    add(f"Calculați {expr}",
        result,
        steps + [f"Răspuns: {result}"],
        "integrale", 2, 2, 12)

# --- Integrale definite ---
add("Calculați ∫₀¹ x² dx",
    "1/3",
    ["∫₀¹ x² dx = [x³/3]₀¹",
     "= 1³/3 - 0³/3 = 1/3 - 0 = 1/3",
     "Răspuns: 1/3"],
    "integrale", 2, 2, 12)

add("Calculați ∫₀² (2x + 1) dx",
    "6",
    ["∫₀² (2x+1) dx = [x² + x]₀²",
     "= (4+2) - (0+0) = 6",
     "Răspuns: 6"],
    "integrale", 2, 2, 12)

add("Calculați ∫₁ᵉ (1/x) dx",
    "1",
    ["∫₁ᵉ (1/x) dx = [ln|x|]₁ᵉ",
     "= ln(e) - ln(1) = 1 - 0 = 1",
     "Răspuns: 1"],
    "integrale", 2, 2, 12)

add("Calculați ∫₀^π sin(x) dx",
    "2",
    ["∫₀^π sin(x) dx = [-cos(x)]₀^π",
     "= -cos(π) - (-cos(0)) = -(-1) + 1 = 1 + 1 = 2",
     "Răspuns: 2"],
    "integrale", 2, 2, 12)

add("Calculați aria sub graficul f(x) = x² pe [0, 3]",
    "9",
    ["A = ∫₀³ x² dx = [x³/3]₀³",
     "= 27/3 - 0 = 9",
     "Răspuns: A = 9"],
    "integrale", 2, 2, 12)

for a, b in [(0,1), (0,2), (1,3), (0,4), (1,2)]:
    val = (b**3 - a**3) / 3
    val_str = f"{val:g}"
    add(f"Calculați ∫_{a}^{b} x² dx",
        val_str,
        [f"∫_{a}^{b} x² dx = [x³/3]_{a}^{b}",
         f"= {b}³/3 - {a}³/3 = {b**3}/3 - {a**3}/3",
         f"= {(b**3 - a**3)/3:g}",
         f"Răspuns: {val_str}"],
        "integrale", 2, 2, 12)


# ═══════════════════════════════════════════════════════════════
# TRIGONOMETRIE (cls 9-11)
# ═══════════════════════════════════════════════════════════════

trig_vals = [
    (0, "0", "1"), (30, "1/2", "√3/2"), (45, "√2/2", "√2/2"),
    (60, "√3/2", "1/2"), (90, "1", "0"),
    (120, "√3/2", "-1/2"), (180, "0", "-1"),
]
for deg, sin_v, cos_v in trig_vals:
    add(f"Calculați sin({deg}°) și cos({deg}°)",
        f"sin({deg}°) = {sin_v}, cos({deg}°) = {cos_v}",
        [f"Din tabelul trigonometric:",
         f"sin({deg}°) = {sin_v}",
         f"cos({deg}°) = {cos_v}",
         f"Răspuns: sin({deg}°) = {sin_v}, cos({deg}°) = {cos_v}"],
        "trigonometrie", 1, 1, 9)

# Ecuații trigonometrice
add("Rezolvați sin(x) = 1/2, x ∈ [0°, 360°]",
    "x = 30° sau x = 150°",
    ["sin(x) = 1/2",
     "Soluția principală: x = 30° (sin 30° = 1/2)",
     "Sin e pozitiv în cadranul I și II",
     "x₂ = 180° - 30° = 150°",
     "Răspuns: x = 30° sau x = 150°"],
    "trigonometrie", 2, 1, 11)

add("Rezolvați cos(x) = -1/2, x ∈ [0°, 360°]",
    "x = 120° sau x = 240°",
    ["cos(x) = -1/2",
     "Cos e negativ în cadranele II și III",
     "Referința: cos(60°) = 1/2",
     "x₁ = 180° - 60° = 120°",
     "x₂ = 180° + 60° = 240°",
     "Răspuns: x = 120° sau x = 240°"],
    "trigonometrie", 2, 1, 11)

add("Verificați identitatea: sin²x + cos²x = 1",
    "Identitate fundamentală",
    ["Aceasta este identitatea trigonometrică fundamentală",
     "Din teorema lui Pitagora în cercul trigonometric:",
     "Punctul (cos x, sin x) e pe cercul x² + y² = 1",
     "Deci cos²x + sin²x = 1 ✓"],
    "trigonometrie", 1, 1, 9)

# Formule trigonometrice
add("Calculați sin(75°) folosind formula de adunare",
    "(√6+√2)/4",
    ["sin(75°) = sin(45° + 30°)",
     "= sin45°·cos30° + cos45°·sin30°",
     "= (√2/2)·(√3/2) + (√2/2)·(1/2)",
     "= √6/4 + √2/4 = (√6+√2)/4",
     "Răspuns: (√6+√2)/4"],
    "trigonometrie", 3, 1, 11)


# ═══════════════════════════════════════════════════════════════
# GEOMETRIE (cls 9-12)
# ═══════════════════════════════════════════════════════════════

# Aria triunghiului
for b, h in [(6, 4), (8, 5), (10, 3), (12, 7), (5, 8)]:
    add(f"Calculați aria triunghiului cu baza b = {b} și înălțimea h = {h}",
        f"{b*h//2}",
        [f"A = b·h/2 = {b}·{h}/2 = {b*h}/2 = {b*h//2}",
         f"Răspuns: A = {b*h//2}"],
        "geometrie", 1, 1, 9)

# Teorema lui Pitagora
for a, b in [(3,4), (5,12), (8,6), (7,24), (9,12), (8,15), (20,21)]:
    c_sq = a*a + b*b
    c = math.sqrt(c_sq)
    c_str = str(int(c)) if c == int(c) else f"√{c_sq}"
    add(f"În triunghiul dreptunghic cu catetele a={a}, b={b}, calculați ipotenuza",
        c_str,
        [f"Teorema lui Pitagora: c² = a² + b²",
         f"c² = {a}² + {b}² = {a*a} + {b*b} = {c_sq}",
         f"c = √{c_sq} = {c_str}",
         f"Răspuns: c = {c_str}"],
        "geometrie", 1, 1, 9)

# Volumul corpurilor
for r in [2, 3, 5, 7]:
    add(f"Calculați volumul sferei cu raza r = {r}",
        f"{4*r**3}π/3",
        [f"V = 4πr³/3",
         f"= 4π·{r}³/3 = 4π·{r**3}/3 = {4*r**3}π/3",
         f"Răspuns: V = {4*r**3}π/3"],
        "geometrie", 2, 1, 10)

for r, h in [(3, 5), (4, 7), (2, 10), (5, 6)]:
    add(f"Calculați volumul conului cu raza r = {r} și înălțimea h = {h}",
        f"{r*r*h}π/3",
        [f"V = πr²h/3 = π·{r}²·{h}/3",
         f"= π·{r*r}·{h}/3 = {r*r*h}π/3",
         f"Răspuns: V = {r*r*h}π/3"],
        "geometrie", 2, 1, 10)

for r, h in [(3, 5), (4, 7), (2, 10), (5, 6)]:
    add(f"Calculați volumul cilindrului cu raza r = {r} și înălțimea h = {h}",
        f"{r*r*h}π",
        [f"V = πr²h = π·{r}²·{h}",
         f"= π·{r*r}·{h} = {r*r*h}π",
         f"Răspuns: V = {r*r*h}π"],
        "geometrie", 1, 1, 10)


# ═══════════════════════════════════════════════════════════════
# SALVARE
# ═══════════════════════════════════════════════════════════════

print(f"Total exerciții generate: {len(exercises)}")

# Statistici pe topic
from collections import Counter
topics = Counter(e["topic"] for e in exercises)
print("\nDistribuție pe topicuri:")
for t, c in sorted(topics.items(), key=lambda x: -x[1]):
    print(f"  {t}: {c}")

# Statistici pe clasă
classes = Counter(e.get("class", "?") for e in exercises)
print("\nDistribuție pe clase:")
for c, n in sorted(classes.items()):
    print(f"  Clasa {c}: {n}")

# Salvare
out_path = Path(__file__).parent.parent / "data" / "processed" / "exercises_curriculum.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(exercises, f, ensure_ascii=False, indent=2)
print(f"\nSalvat: {out_path}")
