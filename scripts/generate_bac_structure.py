"""
Generare exerciții pe STRUCTURA REALĂ a subiectelor BAC Matematică M1 + M2.

STRUCTURA BAC (M1 Mate-Info):
═══════════════════════════════════════════════════
SUBIECTUL I (30p) — Algebră & Elemente de analiză
  1. Mulțimi, intervale, ecuații simple (5p)
  2. Funcții (grad 1, grad 2, proprietăți) (5p)
  3. Șiruri / Progresii (aritmetice, geometrice) (5p)
  4. Combinatorică (permutări, aranjamente, combinări) (5p)
  5. Matrice, determinanți (2×2, 3×3) (5p)
  6. Numere complexe (operații, modul, formă trigonometrică) (5p)

SUBIECTUL II (30p) — Geometrie
  1. Vectori în plan (5p)
  2. Dreapta în plan (ecuație, paralelism, perpendicular) (5p)
  3. Geometrie plană (arii, distanțe, triunghiuri) (5p)
  4. Geometrie în spațiu (plan, dreaptă, unghi) (5p)
  5. Corp geometric (volum, arie laterală/totală) (5p)
  6. Secțiuni / Geometrie metrică spațiu (5p)

SUBIECTUL III (30p) — Analiză matematică
  1. Limite de funcții (5p)
  2. Derivate (calculare, tangentă) (5p)
  3. Monotonie, extreme (studiu cu derivata) (5p)
  4. Integrale nedefinite / Primitive (5p)
  5. Integrale definite / Arii (5p)
  6. Studiu complet funcție / Proprietăți (5p)
═══════════════════════════════════════════════════
"""

import json, math, random
from pathlib import Path
from fractions import Fraction

random.seed(2024)
exercises = []
_id = 30000

def add(q, a, steps, topic, subj, diff=2):
    global _id; _id += 1
    exercises.append({
        "_id": _id, "question": q, "answer": str(a),
        "topic": topic, "exercise_type": topic,
        "difficulty": diff, "subject": subj,
        "points": 5, "profile": "M1",
        "solution": "\n".join(steps), "solution_steps": steps,
        "source": "bac_structure",
    })

# ═══════════════════════════════════════════════════
# SUBIECTUL I — Algebră (subject=1)
# ═══════════════════════════════════════════════════

# --- I.1 Mulțimi, ecuații simple ---
print("Generez Subiectul I.1 — Mulțimi, ecuații...")

# Reuniune, intersecție cu intervale
for a in range(-5, 5):
    for b in range(a+2, a+8):
        c, d = a+1, b+3
        add(f"Fie A = [{a}, {b}] și B = [{c}, {d}]. Calculați A ∩ B.",
            f"[{c}, {b}]" if c <= b else "∅",
            [f"A ∩ B = elementele comune", f"max({a},{c}) = {c}, min({b},{d}) = {b}",
             f"A ∩ B = [{c}, {b}]" if c <= b else "A ∩ B = ∅"],
            "multimi", 1, 1)

# Ecuații simple cu radicali
for a in [1,2,3,4,5,6,7,8,9]:
    add(f"Calculați √{a*a} + √{(a+1)*(a+1)}.",
        f"{a} + {a+1} = {2*a+1}",
        [f"√{a*a} = {a}", f"√{(a+1)*(a+1)} = {a+1}", f"= {a} + {a+1} = {2*a+1}"],
        "ecuatii", 1, 1)

# Ecuații de gradul 1 diverse
for a in range(2, 10):
    for b in range(-5, 6):
        c = random.randint(-10, 20)
        x = c - b
        if x % a != 0: continue
        x = x // a
        add(f"Rezolvați ecuația {a}x + ({b}) = {c}.",
            f"x = {x}",
            [f"{a}x = {c} - ({b}) = {c-b}", f"x = {c-b}/{a} = {x}"],
            "ecuatii", 1, 1)

# --- I.2 Funcții ---
print("Generez Subiectul I.2 — Funcții...")

for a in range(-3, 4):
    for b in range(-5, 6):
        if a == 0: continue
        add(f"Fie f: ℝ → ℝ, f(x) = {a}x + ({b}). Calculați f(0) + f(1).",
            f"{b} + {a+b} = {2*b+a}",
            [f"f(0) = {b}", f"f(1) = {a}+({b}) = {a+b}", f"f(0)+f(1) = {b}+{a+b} = {2*b+a}"],
            "functii", 1, 1)

# Graficul funcției de grad 2
for a in [1, -1, 2]:
    for p in range(-3, 4):
        q = random.randint(-5, 5)
        b = -2*a*p
        c = a*p*p + q
        add(f"Fie f(x) = {a}x² + ({b})x + ({c}). Determinați coordonatele vârfului parabolei.",
            f"V({p}, {q})",
            [f"xV = -b/(2a) = {-b}/(2·{a}) = {p}",
             f"yV = f({p}) = {a}·{p*p}+({b})·{p}+({c}) = {q}",
             f"V({p}, {q})"],
            "functii", 1, 2)

# --- I.3 Șiruri / Progresii ---
print("Generez Subiectul I.3 — Progresii...")

for a1 in range(-2, 6):
    for r in range(-3, 5):
        if r == 0: continue
        add(f"PA cu a₁ = {a1} și rația r = {r}. Calculați a₁₀.",
            f"a₁₀ = {a1 + 9*r}",
            [f"aₙ = a₁ + (n-1)·r", f"a₁₀ = {a1} + 9·({r}) = {a1+9*r}"],
            "progresii", 1, 1)
        sn = 10*(2*a1 + 9*r)//2
        add(f"PA cu a₁ = {a1} și r = {r}. Calculați S₁₀.",
            f"S₁₀ = {sn}",
            [f"S₁₀ = 10·(2·{a1}+9·{r})/2 = 10·{2*a1+9*r}/2 = {sn}"],
            "progresii", 1, 2)

for b1 in [1, 2, 3]:
    for q in [2, 3, -2]:
        b5 = b1 * q**4
        add(f"PG cu b₁ = {b1} și q = {q}. Calculați b₅.",
            f"b₅ = {b5}",
            [f"bₙ = b₁·qⁿ⁻¹", f"b₅ = {b1}·{q}⁴ = {b1}·{q**4} = {b5}"],
            "progresii", 1, 2)

# Trei numere în PA
for d in range(1, 6):
    for m in range(0, 8):
        a, b, c = m-d, m, m+d
        add(f"Trei numere sunt în PA: {a}, {b}, {c}. Verificați și aflați rația.",
            f"r = {d}",
            [f"{b}-{a} = {d}", f"{c}-{b} = {d}", f"Rația r = {d}"],
            "progresii", 1, 1)

# --- I.4 Combinatorică ---
print("Generez Subiectul I.4 — Combinatorică...")

for n in range(3, 12):
    for k in range(1, min(n, 5)):
        val = math.comb(n, k)
        add(f"Calculați C({n},{k}).",
            str(val),
            [f"C({n},{k}) = {n}!/({k}!·{n-k}!) = {val}"],
            "combinatorica", 1, 1)

# Probleme tip BAC
for n in [5, 6, 7, 8]:
    add(f"Câte comitete de 3 persoane se pot forma din {n} persoane?",
        f"C({n},3) = {math.comb(n,3)}",
        [f"Ordinea nu contează → combinări", f"C({n},3) = {math.comb(n,3)}"],
        "combinatorica", 1, 2)

for n in [4, 5, 6]:
    add(f"În câte moduri pot fi aranjate {n} cărți pe un raft?",
        f"P({n}) = {math.factorial(n)}",
        [f"Ordinea contează, toate elementele → permutări", f"P({n}) = {n}! = {math.factorial(n)}"],
        "combinatorica", 1, 2)

# Binomul lui Newton
for n in [3, 4, 5, 6]:
    add(f"Determinați coeficientul lui x² din dezvoltarea (x+1)^{n}.",
        f"C({n},2) = {math.comb(n,2)}",
        [f"Termenul general: C({n},k)·x^({n}-k)", f"x² => {n}-k=2 => k={n-2}",
         f"Coeficient = C({n},{n-2}) = C({n},2) = {math.comb(n,2)}"],
        "combinatorica", 1, 3)

# --- I.5 Matrice și determinanți ---
print("Generez Subiectul I.5 — Matrice, determinanți...")

for _ in range(50):
    a,b,c,d = [random.randint(-4,5) for _ in range(4)]
    det = a*d - b*c
    add(f"Calculați determinantul matricei A = ({a} {b} / {c} {d}).",
        f"det(A) = {det}",
        [f"det = {a}·{d} - {b}·{c} = {a*d} - {b*c} = {det}"],
        "determinanti", 1, 1)

# Inversa 2x2
for a,b,c,d in [(2,1,1,1),(3,2,1,1),(1,1,2,3),(4,1,1,2),(2,3,1,2)]:
    det = a*d - b*c
    if det == 0: continue
    add(f"Determinați inversa matricei A = ({a} {b} / {c} {d}).",
        f"A⁻¹ = (1/{det})·({d} {-b} / {-c} {a})",
        [f"det(A) = {a}·{d}-{b}·{c} = {det}",
         f"A⁻¹ = (1/{det})·({d} {-b} / {-c} {a})"],
        "matrice", 1, 2)

# A + B, A·B
for _ in range(20):
    m1 = [[random.randint(-3,4) for _ in range(2)] for _ in range(2)]
    m2 = [[random.randint(-3,4) for _ in range(2)] for _ in range(2)]
    s = [[m1[i][j]+m2[i][j] for j in range(2)] for i in range(2)]
    add(f"A = ({m1[0][0]} {m1[0][1]} / {m1[1][0]} {m1[1][1]}), B = ({m2[0][0]} {m2[0][1]} / {m2[1][0]} {m2[1][1]}). Calculați A+B.",
        f"({s[0][0]} {s[0][1]} / {s[1][0]} {s[1][1]})",
        [f"Adunăm element cu element",
         f"A+B = ({s[0][0]} {s[0][1]} / {s[1][0]} {s[1][1]})"],
        "matrice", 1, 1)

# Sisteme Cramer 2x2
for _ in range(30):
    x, y = random.randint(-3, 5), random.randint(-3, 5)
    a1, b1 = random.randint(1, 4), random.randint(-3, 3)
    a2, b2 = random.randint(-3, 3), random.randint(1, 4)
    det = a1*b2 - a2*b1
    if det == 0: continue
    c1, c2 = a1*x + b1*y, a2*x + b2*y
    add(f"Rezolvați sistemul prin metoda Cramer: {a1}x+({b1})y={c1}, {a2}x+({b2})y={c2}.",
        f"x={x}, y={y}",
        [f"D = {a1}·{b2}-{a2}·{b1} = {det}",
         f"Dx = {c1}·{b2}-{c2}·{b1} = {c1*b2-c2*b1}",
         f"Dy = {a1}·{c2}-{a2}·{c1} = {a1*c2-a2*c1}",
         f"x = Dx/D = {x}, y = Dy/D = {y}"],
        "sisteme_cramer", 1, 2)

# --- I.6 Numere complexe ---
print("Generez Subiectul I.6 — Numere complexe...")

for a in range(-4, 5):
    for b in range(-4, 5):
        if a == 0 and b == 0: continue
        mod2 = a*a + b*b
        mod = math.sqrt(mod2)
        ms = str(int(mod)) if mod == int(mod) else f"√{mod2}"
        add(f"Calculați modulul numărului complex z = {a}+{b}i.",
            f"|z| = {ms}",
            [f"|z| = √({a}²+{b}²) = √{mod2} = {ms}"],
            "numere_complexe", 1, 1)

for a1,b1,a2,b2 in [(2,3,1,-1),(1,1,2,2),(3,-1,1,4),(2,0,0,3),(-1,2,3,1),
                      (4,1,-2,3),(1,-3,2,1),(3,2,-1,-2),(0,5,5,0),(2,-2,3,3)]:
    re = a1*a2 - b1*b2
    im = a1*b2 + b1*a2
    add(f"Calculați ({a1}+{b1}i)·({a2}+{b2}i).",
        f"{re}+{im}i" if im >= 0 else f"{re}{im}i",
        [f"= ({a1}·{a2}-{b1}·{b2}) + ({a1}·{b2}+{b1}·{a2})i",
         f"= {re} + {im}i"],
        "numere_complexe", 1, 2)

# z + z̄ = 2·Re(z)
for a, b in [(3,4),(2,-1),(5,2),(-1,3),(4,-3)]:
    add(f"Fie z = {a}+{b}i. Calculați z + z̄.",
        f"{2*a}",
        [f"z̄ = {a}-{b}i", f"z + z̄ = ({a}+{b}i) + ({a}-{b}i) = {2*a}"],
        "numere_complexe", 1, 1)


# ═══════════════════════════════════════════════════
# SUBIECTUL II — Geometrie (subject=2)
# ═══════════════════════════════════════════════════

print("\nGenerez Subiectul II — Geometrie...")

# --- II.1 Vectori ---
for x1,y1,x2,y2 in [(1,2,4,6),(0,3,5,1),(-1,2,3,-1),(2,5,7,3),(-3,1,2,4),
                      (1,0,0,1),(3,3,-1,2),(4,-2,1,5),(0,0,3,4),(2,1,-2,-1)]:
    add(f"Fie A({x1},{y1}) și B({x2},{y2}). Determinați vectorul AB.",
        f"AB = ({x2-x1}, {y2-y1})",
        [f"AB = (xB-xA, yB-yA) = ({x2}-{x1}, {y2}-{y1}) = ({x2-x1}, {y2-y1})"],
        "vectori", 2, 1)

# Coliniaritate
for _ in range(15):
    x1,y1 = random.randint(-3,3), random.randint(-3,3)
    t = random.randint(1,3)
    dx, dy = random.randint(-2,2), random.randint(-2,2)
    if dx == 0 and dy == 0: continue
    x2, y2 = x1+dx, y1+dy
    x3, y3 = x1+t*dx, y1+t*dy
    add(f"Verificați dacă A({x1},{y1}), B({x2},{y2}), C({x3},{y3}) sunt coliniare.",
        "Da, sunt coliniare",
        [f"AB = ({dx},{dy}), AC = ({t*dx},{t*dy})",
         f"AC = {t}·AB => coliniare"],
        "vectori", 2, 2)

# --- II.2 Ecuația dreptei ---
for _ in range(20):
    x1,y1 = random.randint(-3,4), random.randint(-3,4)
    x2,y2 = random.randint(-3,4), random.randint(-3,4)
    if x1 == x2: continue
    m = Fraction(y2-y1, x2-x1)
    n = Fraction(y1) - m*x1
    add(f"Scrieți ecuația dreptei care trece prin A({x1},{y1}) și B({x2},{y2}).",
        f"y = {m}x + {n}" if n >= 0 else f"y = {m}x - {-n}",
        [f"m = ({y2}-{y1})/({x2}-{x1}) = {m}",
         f"y - {y1} = {m}(x - {x1})", f"y = {m}x + {n}"],
        "dreapta", 2, 2)

# Distanța punct-dreaptă
for a,b,c,x0,y0 in [(1,1,-2,3,1),(2,-1,3,1,4),(3,4,-5,2,1),(1,0,-3,5,2),(0,1,-2,4,3)]:
    d_num = abs(a*x0 + b*y0 + c)
    d_den = math.sqrt(a*a + b*b)
    d = d_num / d_den
    add(f"Calculați distanța de la P({x0},{y0}) la dreapta {a}x+{b}y+({c})=0.",
        f"d = {d_num}/√{a*a+b*b}" if d != int(d) else f"d = {int(d)}",
        [f"d = |{a}·{x0}+{b}·{y0}+({c})|/√({a}²+{b}²)",
         f"= |{a*x0+b*y0+c}|/√{a*a+b*b} = {d_num}/√{a*a+b*b}"],
        "dreapta", 2, 2)

# --- II.3-4 Geometrie plană/spațiu ---
# Aria triunghi cu coordonate
for _ in range(15):
    x1,y1 = random.randint(-3,3), random.randint(-3,3)
    x2,y2 = random.randint(-3,3), random.randint(-3,3)
    x3,y3 = random.randint(-3,3), random.randint(-3,3)
    area2 = abs(x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2))
    if area2 == 0: continue
    add(f"Calculați aria triunghiului cu vârfurile A({x1},{y1}), B({x2},{y2}), C({x3},{y3}).",
        f"S = {area2}/2" if area2 % 2 != 0 else f"S = {area2//2}",
        [f"S = |x₁(y₂-y₃)+x₂(y₃-y₁)+x₃(y₁-y₂)|/2",
         f"= |{x1}·{y2-y3}+{x2}·{y3-y1}+{x3}·{y1-y2}|/2",
         f"= {area2}/2"],
        "geometrie", 2, 2)

# --- II.5 Corpuri geometrice ---
# Piramidă
for a in [4, 6, 8, 10]:
    for h in [3, 5, 6, 8]:
        v = a*a*h//3
        add(f"Calculați volumul piramidei cu baza pătrat de latură {a} și înălțimea {h}.",
            f"V = {a*a}·{h}/3 = {v}",
            [f"V = Ab·h/3 = {a}²·{h}/3 = {a*a}·{h}/3 = {v}"],
            "geometrie_spatiu", 2, 2)

# Trunchi de con, prisma, etc
for r, h in [(3,4),(5,7),(4,6),(6,8)]:
    v = r*r*h  # V = πr²h, dar scriem fără π
    al = 2*r*h  # Al = 2πrh
    add(f"Cilindru cu r={r}, h={h}. Calculați V și Al.",
        f"V = {v}π, Al = {al}π",
        [f"V = πr²h = π·{r}²·{h} = {v}π",
         f"Al = 2πrh = 2π·{r}·{h} = {al}π"],
        "geometrie_spatiu", 2, 2)

for r, h in [(3,4),(5,12),(4,3),(6,8)]:
    g = math.sqrt(r*r + h*h)
    gs = f"√{r*r+h*h}" if g != int(g) else str(int(g))
    add(f"Con cu r={r}, h={h}. Calculați generatoarea și Al.",
        f"g = {gs}, Al = {r}·{gs}·π",
        [f"g = √(r²+h²) = √({r*r}+{h*h}) = {gs}",
         f"Al = πrg = π·{r}·{gs}"],
        "geometrie_spatiu", 2, 2)


# ═══════════════════════════════════════════════════
# SUBIECTUL III — Analiză matematică (subject=3)
# ═══════════════════════════════════════════════════

print("\nGenerez Subiectul III — Analiză...")

# --- III.1 Limite ---
# Forme 0/0
for a in range(1, 8):
    add(f"Calculați lim(x→{a}) (x²-{a*a})/(x-{a}).",
        f"{2*a}",
        [f"Formă 0/0. Factorizăm: (x-{a})(x+{a})/(x-{a}) = x+{a}",
         f"lim = {a}+{a} = {2*a}"],
        "limite", 3, 2)

# lim la infinit
for a, b in [(1,2),(2,3),(3,1),(4,5),(5,2),(1,1),(3,2),(2,5)]:
    add(f"Calculați lim(x→∞) ({a}x²+3x)/({b}x²-1).",
        f"{a}/{b}" if a != b else "1",
        [f"Grad egal ⟹ limita = coef. dominant/{b}",
         f"= {a}/{b}"],
        "limite", 3, 2)

# Limite remarcabile variații
for k in [1, 2, 3, 5]:
    add(f"Calculați lim(x→0) sin({k}x)/x.",
        f"{k}",
        [f"lim sin({k}x)/x = lim {k}·sin({k}x)/({k}x) = {k}·1 = {k}"],
        "limite", 3, 2)

for k in [1, 2, 3]:
    add(f"Calculați lim(x→0) (e^({k}x)-1)/x.",
        f"{k}",
        [f"lim (e^({k}x)-1)/x = {k}·lim (e^({k}x)-1)/({k}x) = {k}·1 = {k}"],
        "limite", 3, 2)

# --- III.2 Derivate ---
polys = [
    ("x³-3x²+2x-1", "3x²-6x+2"),
    ("2x⁴-x²+5x", "8x³-2x+5"),
    ("x³+x²-4x+7", "3x²+2x-4"),
    ("x⁵-2x³+x", "5x⁴-6x²+1"),
    ("-x³+6x²-9x+2", "-3x²+12x-9"),
    ("4x³-12x+1", "12x²-12"),
    ("x⁴-4x³+6x²-4x+1", "4x³-12x²+12x-4"),
]
for f, fp in polys:
    add(f"Calculați derivata funcției f(x) = {f}.",
        f"f'(x) = {fp}",
        [f"Derivăm termen cu termen", f"f'(x) = {fp}"],
        "derivate", 3, 2)

# Derivate compuse tip BAC
composites = [
    ("ln(x²+1)", "2x/(x²+1)"),
    ("e^(2x+1)", "2e^(2x+1)"),
    ("sin(3x+π/4)", "3cos(3x+π/4)"),
    ("(2x+1)⁵", "10(2x+1)⁴"),
    ("√(x²+4)", "x/√(x²+4)"),
    ("ln(sin x)", "cos x/sin x = ctg x"),
    ("e^(x²)", "2x·e^(x²)"),
    ("x·e^x", "(x+1)·e^x"),
    ("x²·ln x", "x(2ln x + 1)"),
    ("x/(x+1)", "1/(x+1)²"),
]
for f, fp in composites:
    add(f"Calculați f'(x) dacă f(x) = {f}.",
        f"f'(x) = {fp}",
        [f"Aplicăm regula lanțului/produsului/câtului", f"f'(x) = {fp}"],
        "derivate", 3, 3)

# Tangenta
for x0 in [0, 1, 2, -1]:
    y0 = x0**3 - 3*x0 + 2
    m = 3*x0**2 - 3
    n = y0 - m*x0
    add(f"Ecuația tangentei la f(x) = x³-3x+2 în x₀={x0}.",
        f"y = {m}x + {n}" if n >= 0 else f"y = {m}x - {-n}",
        [f"f({x0}) = {y0}", f"f'(x) = 3x²-3, f'({x0}) = {m}",
         f"y - {y0} = {m}(x-{x0}) ⟹ y = {m}x + {n}"],
        "derivate", 3, 3)

# --- III.3 Monotonie, extreme ---
studies = [
    ("x³-3x", "3x²-3=3(x-1)(x+1)", "cresc. (-∞,-1)∪(1,+∞), desc. (-1,1)", "max local x=-1: f(-1)=2, min local x=1: f(1)=-2"),
    ("x³-12x", "3x²-12=3(x-2)(x+2)", "cresc. (-∞,-2)∪(2,+∞), desc. (-2,2)", "max local x=-2: f(-2)=16, min local x=2: f(2)=-16"),
    ("-x³+3x", "-3x²+3=-3(x-1)(x+1)", "cresc. (-1,1), desc. (-∞,-1)∪(1,+∞)", "min local x=-1, max local x=1"),
    ("x⁴-4x²", "4x³-8x=4x(x²-2)", "cresc. (-√2,0)∪(√2,+∞), desc. (-∞,-√2)∪(0,√2)", "min x=±√2: f=-4, max local x=0: f=0"),
    ("xe^(-x)", "e^(-x)(1-x)", "cresc. (-∞,1), desc. (1,+∞)", "max global x=1: f(1)=1/e"),
]
for func, deriv, mono, extreme in studies:
    add(f"Studiați monotonia și extremele funcției f(x) = {func}.",
        f"Monotonie: {mono}. Extreme: {extreme}",
        [f"f'(x) = {deriv}", f"f'(x) = 0: rezolvăm", f"Monotonie: {mono}", f"Extreme: {extreme}"],
        "studiu_functie", 3, 3)

# --- III.4 Primitive / Integrale nedefinite ---
prims = [
    ("∫(3x²+2x-1)dx", "x³+x²-x+C"),
    ("∫(4x³-6x²+2)dx", "x⁴-2x³+2x+C"),
    ("∫(e^x+1/x)dx", "e^x+ln|x|+C"),
    ("∫(sin x + cos x)dx", "-cos x + sin x + C"),
    ("∫(2x+1)³dx", "(2x+1)⁴/8+C"),
    ("∫e^(3x)dx", "e^(3x)/3+C"),
    ("∫cos(2x)dx", "sin(2x)/2+C"),
    ("∫x·e^x dx", "(x-1)e^x+C"),
    ("∫ln(x)dx", "x·ln(x)-x+C"),
    ("∫1/(x²+1)dx", "arctan(x)+C"),
]
for expr, result in prims:
    add(f"Calculați {expr}.",
        result,
        [f"Aplicăm regulile de integrare", f"= {result}"],
        "integrale", 3, 2)

# --- III.5 Integrale definite / Arii ---
for a, b in [(0,1),(0,2),(1,3),(0,3),(-1,1),(1,2),(0,4),(2,4)]:
    # ∫ x² dx
    val = (b**3 - a**3) / 3
    add(f"Calculați ∫_{a}^{b} x² dx.",
        f"{val:g}",
        [f"∫x²dx = x³/3", f"[x³/3]_{a}^{b} = {b**3}/3 - {a**3}/3 = {val:g}"],
        "integrale", 3, 2)
    # ∫ 2x dx
    val2 = b**2 - a**2
    add(f"Calculați ∫_{a}^{b} 2x dx.",
        f"{val2}",
        [f"∫2x dx = x²", f"[x²]_{a}^{b} = {b**2} - {a**2} = {val2}"],
        "integrale", 3, 1)

# Arii
add("Calculați aria cuprinsă între graficul f(x)=x² și axa Ox pe [0,2].",
    "8/3",
    ["A = ∫₀² x² dx = [x³/3]₀² = 8/3"],
    "integrale", 3, 3)
add("Calculați aria dintre f(x)=x² și g(x)=x pe [0,1].",
    "1/6",
    ["A = ∫₀¹ (x-x²) dx = [x²/2-x³/3]₀¹ = 1/2-1/3 = 1/6"],
    "integrale", 3, 3)

# --- III.6 Studiu complet funcție ---
full_studies = [
    ("(x²-1)/(x²+1)", [
        "D = ℝ (numitorul > 0)",
        "f'(x) = 4x/(x²+1)²",
        "f'(x) = 0 ⟹ x = 0 (minim global)",
        "f(0) = -1",
        "f crescătoare pe (0,+∞), descrescătoare pe (-∞,0)",
        "lim(x→±∞) = 1 ⟹ asimptota orizontală y = 1",
        "Imagine: [-1, 1)"
    ]),
    ("x·e^(-x)", [
        "D = ℝ",
        "f'(x) = e^(-x)(1-x)",
        "f'(x) = 0 ⟹ x = 1 (maxim global)",
        "f(1) = 1/e",
        "lim(x→-∞) = -∞, lim(x→+∞) = 0",
        "AO: y = 0 (la +∞)",
    ]),
    ("(2x+1)/(x-1)", [
        "D = ℝ\\{1}",
        "f'(x) = -3/(x-1)² < 0 ⟹ f strict descrescătoare",
        "AV: x = 1",
        "AO: y = 2 (lim = 2)",
        "f nu are extreme",
    ]),
    ("ln(x)/x", [
        "D = (0, +∞)",
        "f'(x) = (1-ln x)/x²",
        "f'(x) = 0 ⟹ x = e (maxim global)",
        "f(e) = 1/e",
        "lim(x→0+) = -∞, lim(x→+∞) = 0",
    ]),
]
for func, steps in full_studies:
    add(f"Efectuați studiul complet al funcției f(x) = {func}.",
        "Vezi rezolvarea completă",
        steps,
        "studiu_functie", 3, 3)


# ═══════════════════════════════════════════════════
# SALVARE
# ═══════════════════════════════════════════════════

print(f"\nTotal exerciții generate: {len(exercises)}")

# Deduplicare
seen = set()
unique = []
for ex in exercises:
    q = ex["question"].strip().lower()
    if q not in seen:
        seen.add(q)
        unique.append(ex)
exercises = unique
print(f"Unice: {len(exercises)}")

# Distribuție
from collections import Counter
for subj in [1, 2, 3]:
    sub_ex = [e for e in exercises if e["subject"] == subj]
    topics = Counter(e["topic"] for e in sub_ex)
    print(f"\nSubiectul {subj} ({len(sub_ex)} exerciții):")
    for t, c in topics.most_common():
        print(f"  {t}: {c}")

# Merge cu existente
merged_path = Path("/Users/stanioanadennisa/Desktop/bac-prep-ai/data/processed/exercises_merged.json")
existing = json.load(open(merged_path, encoding="utf-8"))
existing_q = {e.get("question", "").strip().lower() for e in existing}

added = 0
for ex in exercises:
    if ex["question"].strip().lower() not in existing_q:
        existing.append(ex)
        existing_q.add(ex["question"].strip().lower())
        added += 1

print(f"\nAdăugate: {added}")
print(f"TOTAL FINAL: {len(existing)}")

with open(merged_path, "w", encoding="utf-8") as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)
print("Salvat!")
