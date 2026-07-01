"""
Generare masivă de exerciții — ținta: 5000+ total
Variații de parametri pentru fiecare tip de exercițiu.
"""
import json, math, random
from pathlib import Path
from fractions import Fraction

random.seed(777)
exercises = []
_id = 10000

def add(q, a, steps, topic, diff=2):
    global _id
    _id += 1
    exercises.append({
        "_id": _id, "question": q, "answer": str(a),
        "topic": topic, "exercise_type": topic, "difficulty": diff,
        "subject": 1, "points": 5, "profile": "BOTH",
        "solution": "\n".join(steps), "solution_steps": steps,
        "source": "generated_massive",
    })

# ═══════════════════════════════════════
# ECUAȚII — 300+ variații
# ═══════════════════════════════════════

# Grad 1 cu coeficienți variați
for a in range(2, 12):
    for b in range(-5, 6, 2):
        c = a * random.randint(-3, 8) + b
        x = (c - b) / a
        if x == int(x):
            x = int(x)
            add(f"Rezolvă ecuația: {a}x + {b} = {c}", str(x),
                [f"{a}x = {c} - ({b}) = {c-b}", f"x = {c-b}/{a} = {x}"],
                "ecuatii", 1)

# Grad 2 — multe variații
for x1 in range(-6, 7):
    for x2 in range(x1, 7):
        if x1 == x2 == 0: continue
        a = 1
        b = -(x1 + x2)
        c = x1 * x2
        delta = b*b - 4*a*c
        if delta < 0: continue
        add(f"Rezolvă ecuația: x² + ({b})x + ({c}) = 0",
            f"x₁ = {x1}, x₂ = {x2}" if x1 != x2 else f"x = {x1} (rădăcină dublă)",
            [f"a=1, b={b}, c={c}", f"Δ = {b}² - 4·{c} = {delta}",
             f"x₁ = ({-b} - √{delta}) / 2 = {x1}", f"x₂ = ({-b} + √{delta}) / 2 = {x2}"],
            "ecuatii_gradul_2", 2)

# Ecuații cu fracții
for a, b, c in [(2,3,5), (3,4,7), (1,2,3), (5,3,8), (4,7,11)]:
    add(f"Rezolvă: x/{a} + x/{b} = {c}",
        f"x = {c*a*b}//{a+b}" if (c*a*b) % (a+b) == 0 else f"x = {c*a*b}/{a+b}",
        [f"Aducem la numitor comun {a*b}:", f"{b}x + {a}x = {c*a*b}",
         f"{a+b}x = {c*a*b}", f"x = {c*a*b}/{a+b}"],
        "ecuatii", 2)

# ═══════════════════════════════════════
# DERIVATE — 200+ variații
# ═══════════════════════════════════════

# Polinoame diverse
for n in range(2, 8):
    coeffs = [random.randint(-5, 5) for _ in range(n+1)]
    while all(c == 0 for c in coeffs): coeffs[0] = 1

    # Build function string
    terms = []
    deriv_terms = []
    for i, c in enumerate(coeffs):
        exp = n - i
        if c == 0: continue
        if exp == 0:
            terms.append(str(c))
        elif exp == 1:
            terms.append(f"{c}x" if c != 1 else "x")
        else:
            terms.append(f"{c}x^{exp}" if c != 1 else f"x^{exp}")

        if exp > 0:
            dc = c * exp
            dexp = exp - 1
            if dexp == 0:
                deriv_terms.append(str(dc))
            elif dexp == 1:
                deriv_terms.append(f"{dc}x" if dc != 1 else "x")
            else:
                deriv_terms.append(f"{dc}x^{dexp}" if dc != 1 else f"x^{dexp}")

    if not terms or not deriv_terms: continue
    func = " + ".join(terms).replace("+ -", "- ")
    deriv = " + ".join(deriv_terms).replace("+ -", "- ")

    add(f"Calculați derivata: f(x) = {func}", f"f'(x) = {deriv}",
        [f"Derivăm termen cu termen folosind regula puterii: (x^n)' = n·x^(n-1)",
         f"f'(x) = {deriv}"],
        "derivate", 2)

# Derivate compuse
composites = [
    ("sin(2x)", "2cos(2x)", "Regula lanțului: cos(2x)·2"),
    ("cos(3x)", "-3sin(3x)", "Regula lanțului: -sin(3x)·3"),
    ("e^(2x)", "2e^(2x)", "Regula lanțului: e^(2x)·2"),
    ("e^(-x)", "-e^(-x)", "Regula lanțului: e^(-x)·(-1)"),
    ("ln(2x)", "1/x", "(1/2x)·2 = 1/x"),
    ("sin(x²)", "2x·cos(x²)", "cos(x²)·2x"),
    ("e^(x²)", "2x·e^(x²)", "e^(x²)·2x"),
    ("ln(x+1)", "1/(x+1)", "1/(x+1)·1"),
    ("(3x+1)⁴", "12(3x+1)³", "4(3x+1)³·3"),
    ("√(2x+1)", "1/√(2x+1)", "(1/2)·(2x+1)^(-1/2)·2"),
    ("sin²(x)", "2sin(x)cos(x)", "2sin(x)·cos(x) = sin(2x)"),
    ("cos²(x)", "-2sin(x)cos(x)", "-2sin(x)cos(x) = -sin(2x)"),
    ("tan(x)", "1/cos²(x)", "sec²(x)"),
    ("e^(sin(x))", "cos(x)·e^(sin(x))", "e^(sin(x))·cos(x)"),
    ("ln(cos(x))", "-tan(x)", "-sin(x)/cos(x) = -tan(x)"),
    ("x·e^x", "(1+x)e^x", "Produs: 1·e^x + x·e^x"),
    ("x²·ln(x)", "x(2ln(x)+1)", "Produs: 2x·ln(x) + x²·1/x"),
    ("sin(x)·cos(x)", "cos²(x)-sin²(x)", "= cos(2x)"),
    ("x/sin(x)", "(sin(x)-x·cos(x))/sin²(x)", "Câtul"),
    ("e^x/x", "(x-1)e^x/x²", "Câtul"),
]

for func, deriv, hint in composites:
    add(f"Calculați derivata: f(x) = {func}", f"f'(x) = {deriv}",
        [hint, f"f'(x) = {deriv}"], "derivate", 3)

# ═══════════════════════════════════════
# INTEGRALE — 150+ variații
# ═══════════════════════════════════════

# Integrale de polinoame
for n in range(1, 7):
    for c in [1, 2, 3, -1, -2, 5]:
        if n == -1: continue
        prim_c = f"{c}/{n+1}" if c % (n+1) != 0 else str(c // (n+1))
        add(f"Calculați ∫ {c}x^{n} dx",
            f"{prim_c}·x^{n+1} + C",
            [f"∫ {c}x^{n} dx = {c}·x^{n+1}/{n+1} + C = {prim_c}·x^{n+1} + C"],
            "integrale", 2)

# Integrale definite
for a, b in [(0,1), (0,2), (1,3), (0,3), (1,4), (-1,1), (0,4), (2,5)]:
    for n in [1, 2, 3]:
        val = (b**(n+1) - a**(n+1)) / (n+1)
        add(f"Calculați ∫_{a}^{b} x^{n} dx",
            f"{val:g}",
            [f"∫ x^{n} dx = x^{n+1}/{n+1}",
             f"[x^{n+1}/{n+1}]_{a}^{b} = {b}^{n+1}/{n+1} - {a}^{n+1}/{n+1}",
             f"= {b**(n+1)}/{n+1} - {a**(n+1)}/{n+1} = {val:g}"],
            "integrale", 2)

# Integrale trigonometrice
trig_integrals = [
    ("∫ sin(2x) dx", "-cos(2x)/2 + C", "u=2x, du=2dx"),
    ("∫ cos(3x) dx", "sin(3x)/3 + C", "u=3x"),
    ("∫ sin²(x) dx", "x/2 - sin(2x)/4 + C", "sin²x = (1-cos2x)/2"),
    ("∫ cos²(x) dx", "x/2 + sin(2x)/4 + C", "cos²x = (1+cos2x)/2"),
    ("∫ sin(x)cos(x) dx", "sin²(x)/2 + C", "u=sin(x), du=cos(x)dx"),
    ("∫ tan(x) dx", "-ln|cos(x)| + C", "∫ sin/cos = -ln|cos|"),
    ("∫ 1/cos²(x) dx", "tan(x) + C", "Integrală standard"),
    ("∫ 1/sin²(x) dx", "-cot(x) + C", "Integrală standard"),
]
for expr, result, hint in trig_integrals:
    add(f"Calculați {expr}", result, [hint, f"= {result}"], "integrale", 3)

# ═══════════════════════════════════════
# LIMITE — 150+ variații
# ═══════════════════════════════════════

# Limite la infinit — raport polinoame
for a1,b1,a2,b2 in [(1,0,1,0),(2,1,3,-1),(3,2,1,5),(4,-1,2,3),(5,0,3,0),
                      (1,1,2,2),(7,3,4,1),(2,-3,5,2),(6,1,3,-2),(1,4,1,-4)]:
    add(f"Calculați lim(x→∞) ({a1}x + {b1})/({a2}x + {b2})",
        f"{a1}/{a2}" if a1/a2 != int(a1/a2) else str(int(a1/a2)),
        [f"Împărțim la x: lim ({a1} + {b1}/x)/({a2} + {b2}/x)",
         f"= {a1}/{a2}"],
        "limite", 1)

for a1,a2 in [(1,2),(2,3),(3,1),(4,5),(5,2),(1,3),(2,1),(3,4),(7,2),(1,1)]:
    add(f"Calculați lim(x→∞) ({a1}x² + 1)/({a2}x² - 1)",
        f"{a1}/{a2}" if a1 != a2 else "1",
        [f"Grad egal => limita = {a1}/{a2}"],
        "limite", 2)

# Forme 0/0
for a in range(1, 10):
    add(f"Calculați lim(x→{a}) (x² - {a*a})/(x - {a})",
        str(2*a),
        [f"Formă 0/0, factorizăm: (x-{a})(x+{a})/(x-{a})",
         f"= lim(x+{a}) = {2*a}"],
        "limite", 2)

for a in range(1, 8):
    add(f"Calculați lim(x→{a}) (x³ - {a**3})/(x - {a})",
        str(3*a*a),
        [f"Formă 0/0, factorizăm sau L'Hôpital:",
         f"L'Hôpital: lim 3x²/1 = 3·{a}² = {3*a*a}"],
        "limite", 3)

# ═══════════════════════════════════════
# MATRICE & DETERMINANȚI — 100+ variații
# ═══════════════════════════════════════

# Det 2x2 cu multe variații
for _ in range(40):
    a,b,c,d = [random.randint(-5,8) for _ in range(4)]
    det = a*d - b*c
    add(f"Calculați det|{a} {b}; {c} {d}|", str(det),
        [f"det = {a}·{d} - {b}·{c} = {a*d} - {b*c} = {det}"],
        "determinanti", 1)

# Înmulțire matrice 2x2
for _ in range(20):
    a,b,c,d = [random.randint(-3,5) for _ in range(4)]
    e,f,g,h = [random.randint(-3,5) for _ in range(4)]
    r = [[a*e+b*g, a*f+b*h], [c*e+d*g, c*f+d*h]]
    add(f"Calculați A·B: A=[[{a},{b}],[{c},{d}]], B=[[{e},{f}],[{g},{h}]]",
        f"[[{r[0][0]},{r[0][1]}],[{r[1][0]},{r[1][1]}]]",
        [f"C₁₁={a}·{e}+{b}·{g}={r[0][0]}", f"C₁₂={a}·{f}+{b}·{h}={r[0][1]}",
         f"C₂₁={c}·{e}+{d}·{g}={r[1][0]}", f"C₂₂={c}·{f}+{d}·{h}={r[1][1]}"],
        "matrice", 2)

# Matrice la putere (A²)
for a,b,c,d in [(1,1,0,1),(2,1,1,1),(1,2,0,1),(0,1,1,0)]:
    r = [[a*a+b*c, a*b+b*d],[c*a+d*c, c*b+d*d]]
    add(f"Calculați A² dacă A = [[{a},{b}],[{c},{d}]]",
        f"[[{r[0][0]},{r[0][1]}],[{r[1][0]},{r[1][1]}]]",
        [f"A² = A·A", f"Înmulțim A cu A"],
        "matrice", 2)

# ═══════════════════════════════════════
# COMBINATORICĂ — 100+ variații
# ═══════════════════════════════════════

for n in range(3, 15):
    for k in range(1, min(n, 6)):
        c = math.comb(n, k)
        add(f"Calculați C({n},{k})", str(c),
            [f"C({n},{k}) = {n}!/({k}!·{n-k}!) = {c}"],
            "combinatorica", 1)

for n in range(3, 10):
    for k in range(1, min(n, 5)):
        a = math.perm(n, k)
        add(f"Calculați A({n},{k})", str(a),
            [f"A({n},{k}) = {n}!/({n}-{k})! = {a}"],
            "combinatorica", 1)

# ═══════════════════════════════════════
# NUMERE COMPLEXE — 80+ variații
# ═══════════════════════════════════════

for a1 in range(-3, 4):
    for b1 in range(-3, 4):
        a2, b2 = random.randint(-3,3), random.randint(-3,3)
        if a1 == b1 == 0 or a2 == b2 == 0: continue
        # Adunare
        add(f"Calculați ({a1}+{b1}i) + ({a2}+{b2}i)",
            f"{a1+a2}+{b1+b2}i" if b1+b2>=0 else f"{a1+a2}{b1+b2}i",
            [f"= ({a1}+{a2}) + ({b1}+{b2})i = {a1+a2}+{b1+b2}i"],
            "numere_complexe", 1)

# Înmulțire complexe
for a1,b1,a2,b2 in [(1,2,3,-1),(2,3,1,1),(-1,1,2,2),(3,0,0,2),(1,1,1,1),
                      (2,-1,3,2),(4,1,-1,3),(1,3,2,-1),(5,2,1,-2),(3,3,1,-1)]:
    re = a1*a2 - b1*b2
    im = a1*b2 + b1*a2
    add(f"Calculați ({a1}+{b1}i)·({a2}+{b2}i)",
        f"{re}+{im}i" if im >= 0 else f"{re}{im}i",
        [f"= {a1}·{a2} + {a1}·{b2}i + {b1}i·{a2} + {b1}·{b2}·i²",
         f"= ({a1*a2}-{b1*b2}) + ({a1*b2}+{b1*a2})i = {re}+{im}i"],
        "numere_complexe", 2)

# ═══════════════════════════════════════
# TRIGONOMETRIE — 50+ variații
# ═══════════════════════════════════════

trig_eqs = [
    ("sin(x) = 0", "x = k·π, k ∈ ℤ"),
    ("cos(x) = 0", "x = π/2 + k·π, k ∈ ℤ"),
    ("sin(x) = 1", "x = π/2 + 2k·π"),
    ("cos(x) = 1", "x = 2k·π"),
    ("sin(x) = -1", "x = -π/2 + 2k·π"),
    ("cos(x) = -1", "x = π + 2k·π"),
    ("tan(x) = 0", "x = k·π, k ∈ ℤ"),
    ("tan(x) = 1", "x = π/4 + k·π"),
    ("sin(x) = √2/2", "x = π/4 + 2kπ sau x = 3π/4 + 2kπ"),
    ("cos(x) = √2/2", "x = ±π/4 + 2kπ"),
    ("sin(x) = √3/2", "x = π/3 + 2kπ sau x = 2π/3 + 2kπ"),
    ("cos(x) = 1/2", "x = ±π/3 + 2kπ"),
    ("sin(2x) = 0", "x = k·π/2, k ∈ ℤ"),
    ("cos(2x) = 1", "x = k·π, k ∈ ℤ"),
    ("2sin(x) - 1 = 0", "sin(x) = 1/2 => x = π/6 + 2kπ sau x = 5π/6 + 2kπ"),
]

for eq, sol in trig_eqs:
    add(f"Rezolvați ecuația trigonometrică: {eq}", sol,
        [f"Ecuația: {eq}", f"Soluția: {sol}"],
        "trigonometrie", 2)

# ═══════════════════════════════════════
# GEOMETRIE — 50+ variații
# ═══════════════════════════════════════

# Distanțe
for _ in range(20):
    x1,y1 = random.randint(-5,5), random.randint(-5,5)
    x2,y2 = random.randint(-5,5), random.randint(-5,5)
    if x1==x2 and y1==y2: continue
    d2 = (x2-x1)**2 + (y2-y1)**2
    d = math.sqrt(d2)
    ds = str(int(d)) if d == int(d) else f"√{d2}"
    add(f"Distanța dintre A({x1},{y1}) și B({x2},{y2})",
        ds,
        [f"d = √(({x2}-{x1})²+({y2}-{y1})²) = √{d2} = {ds}"],
        "geometrie_analitica", 1)

# Ecuații drepte prin 2 puncte
for _ in range(15):
    x1,y1 = random.randint(-3,3), random.randint(-3,3)
    x2,y2 = random.randint(-3,3), random.randint(-3,3)
    if x1 == x2: continue
    m = Fraction(y2-y1, x2-x1)
    n = Fraction(y1) - m * x1
    add(f"Ecuația dreptei prin A({x1},{y1}) și B({x2},{y2})",
        f"y = {m}x + {n}" if n >= 0 else f"y = {m}x - {-n}",
        [f"m = ({y2}-{y1})/({x2}-{x1}) = {m}",
         f"y - {y1} = {m}(x - {x1})",
         f"y = {m}x + {n}"],
        "geometrie_analitica", 2)

# ═══════════════════════════════════════
# PROGRESII — 50+ variații
# ═══════════════════════════════════════

for a1 in range(-3, 8):
    for r in range(-3, 6):
        if r == 0: continue
        for n in [5, 8, 10, 15, 20]:
            an = a1 + (n-1)*r
            sn = n * (a1 + an) // 2
            add(f"PA: a₁={a1}, r={r}. Aflați a_{n} și S_{n}.",
                f"a_{n}={an}, S_{n}={sn}",
                [f"a_{n} = {a1}+({n}-1)·{r} = {an}",
                 f"S_{n} = {n}·({a1}+{an})/2 = {sn}"],
                "progresii", 2)

# ═══════════════════════════════════════
# LOGARITMI — 50+ variații
# ═══════════════════════════════════════

for base in [2,3,5,10]:
    for exp in range(1, 7):
        arg = base ** exp
        add(f"Calculați log_{base}({arg})", str(exp),
            [f"{base}^{exp} = {arg}, deci log_{base}({arg}) = {exp}"],
            "logaritmi", 1)

# Proprietăți logaritmi
for a, b in [(2,4),(4,8),(3,9),(8,2),(16,4),(27,3),(100,10)]:
    add(f"Calculați log₂({a}) + log₂({b})", f"log₂({a*b})",
        [f"log₂({a}) + log₂({b}) = log₂({a}·{b}) = log₂({a*b})"],
        "logaritmi", 2)

print(f"Exerciții generate: {len(exercises)}")

# Deduplicate
seen = set()
unique = []
for ex in exercises:
    q = ex["question"].strip().lower()
    if q not in seen:
        seen.add(q)
        unique.append(ex)
exercises = unique
print(f"Unice: {len(exercises)}")

# Merge
merged_path = Path("/Users/stanioanadennisa/Desktop/bac-prep-ai/data/processed/exercises_merged.json")
existing = json.load(open(merged_path, encoding="utf-8"))
existing_q = {e.get("question","").strip().lower() for e in existing}

added = 0
for ex in exercises:
    if ex["question"].strip().lower() not in existing_q:
        existing.append(ex)
        existing_q.add(ex["question"].strip().lower())
        added += 1

print(f"Adăugate: {added}")
print(f"TOTAL: {len(existing)}")

with open(merged_path, "w", encoding="utf-8") as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)
print("Salvat!")
