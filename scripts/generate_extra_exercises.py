"""
Generează exerciții extra diverse cu variații de formulare.
Scopul: diversitate maximă pentru model training + app usage.
"""
import json
import math
import random
from pathlib import Path

random.seed(123)
exercises = []
_id = 5000

def add(q, a, steps, topic, diff=2, subj=1):
    global _id
    _id += 1
    exercises.append({
        "_id": _id, "question": q, "answer": str(a),
        "topic": topic, "exercise_type": topic, "difficulty": diff,
        "subject": subj, "points": 5, "profile": "BOTH",
        "year": None, "session": None,
        "solution": "\n".join(steps), "solution_steps": steps,
        "source": "generated_extra", "latex": "", "hints": [],
    })

# ═══════════════════════════════════════════
# ECUAȚII DIVERSE
# ═══════════════════════════════════════════

# Ecuații cu modul
for a, b in [(3, 7), (5, 2), (1, 4), (2, 6)]:
    add(f"Rezolvați |{a}x - {b}| = {b}",
        f"x = 0 sau x = {2*b}/{a}" if 2*b % a != 0 else f"x = 0 sau x = {2*b//a}",
        [f"|{a}x - {b}| = {b}", f"Cazul 1: {a}x - {b} = {b} => {a}x = {2*b} => x = {2*b}/{a}",
         f"Cazul 2: {a}x - {b} = -{b} => {a}x = 0 => x = 0",
         f"Răspuns: x = 0 sau x = {2*b/a:g}"],
        "ecuatii", 2, 1)

# Ecuații iraționale
for a, b, n in [(1, 4, 2), (2, 1, 3), (1, 9, 3), (3, 0, 5)]:
    add(f"Rezolvați √(x + {b}) = {n}",
        str(n*n - b),
        [f"√(x + {b}) = {n}", f"Ridicăm la pătrat: x + {b} = {n*n}",
         f"x = {n*n} - {b} = {n*n - b}",
         f"Verificare: √({n*n-b} + {b}) = √{n*n} = {n} ✓",
         f"Răspuns: x = {n*n - b}"],
        "ecuatii", 2, 1)

# Ecuații exponențiale
for base, exp in [(2, 5), (3, 4), (2, 8), (5, 3)]:
    result = base ** exp
    add(f"Rezolvați {base}^x = {result}",
        str(exp),
        [f"{base}^x = {result}", f"{base}^x = {base}^{exp}",
         f"Bazele sunt egale, deci x = {exp}",
         f"Răspuns: x = {exp}"],
        "ecuatii", 2, 1)

# Ecuații logaritmice
for base, result in [(2, 3), (3, 2), (5, 2), (10, 2)]:
    arg = base ** result
    add(f"Rezolvați log_{base}(x) = {result}",
        str(arg),
        [f"log_{base}(x) = {result}", f"x = {base}^{result} = {arg}",
         f"Răspuns: x = {arg}"],
        "ecuatii", 2, 1)

# ═══════════════════════════════════════════
# DERIVATE AVANSATE
# ═══════════════════════════════════════════

advanced_derivs = [
    ("x·ln(x)", "ln(x) + 1", ["Regula produsului: (uv)' = u'v + uv'", "u=x, v=ln(x)", "= 1·ln(x) + x·(1/x) = ln(x) + 1"]),
    ("e^x·sin(x)", "e^x(sin(x) + cos(x))", ["(e^x·sin(x))' = e^x·sin(x) + e^x·cos(x)", "= e^x(sin(x) + cos(x))"]),
    ("x²·e^x", "e^x(x² + 2x)", ["(x²·e^x)' = 2x·e^x + x²·e^x = e^x(x² + 2x)"]),
    ("ln(x)/x", "(1 - ln(x))/x²", ["Regula câtului: (f/g)' = (f'g - fg')/g²", "= (1/x·x - ln(x)·1)/x² = (1-ln(x))/x²"]),
    ("sin²(x)", "2sin(x)cos(x) = sin(2x)", ["Regula lanțului: 2·sin(x)·cos(x) = sin(2x)"]),
    ("cos³(x)", "-3cos²(x)sin(x)", ["Regula lanțului: 3·cos²(x)·(-sin(x)) = -3cos²(x)sin(x)"]),
    ("√(x²+1)", "x/√(x²+1)", ["(√u)' = u'/(2√u), u = x²+1", "= 2x/(2√(x²+1)) = x/√(x²+1)"]),
    ("arctan(x)", "1/(1+x²)", ["Derivata funcției arctan: (arctan x)' = 1/(1+x²)"]),
    ("e^(x²)", "2x·e^(x²)", ["Regula lanțului: e^u · u', u = x²", "= e^(x²)·2x"]),
    ("ln(sin(x))", "cos(x)/sin(x) = ctg(x)", ["(ln u)' = u'/u, u = sin(x)", "= cos(x)/sin(x) = ctg(x)"]),
    ("(x+1)/(x-1)", "-2/(x-1)²", ["Regula câtului:", "= (1·(x-1) - (x+1)·1)/(x-1)²", "= (x-1-x-1)/(x-1)² = -2/(x-1)²"]),
    ("x^x", "x^x(ln(x) + 1)", ["y = x^x => ln(y) = x·ln(x)", "y'/y = ln(x) + 1", "y' = x^x(ln(x) + 1)"]),
]

for func, deriv, steps in advanced_derivs:
    add(f"Calculați derivata funcției f(x) = {func}",
        f"f'(x) = {deriv}",
        steps + [f"Răspuns: f'(x) = {deriv}"],
        "derivate", 3, 2)

# ═══════════════════════════════════════════
# INTEGRALE AVANSATE
# ═══════════════════════════════════════════

advanced_integrals = [
    ("∫ x·e^x dx", "(x-1)·e^x + C", ["Integrare prin părți: u=x, dv=e^x dx", "= x·e^x - ∫e^x dx = x·e^x - e^x + C = (x-1)e^x + C"]),
    ("∫ x·sin(x) dx", "-x·cos(x) + sin(x) + C", ["Integrare prin părți: u=x, dv=sin(x)dx", "= -x·cos(x) + ∫cos(x)dx = -x·cos(x) + sin(x) + C"]),
    ("∫ x²·e^x dx", "(x²-2x+2)·e^x + C", ["Integrare prin părți de 2 ori", "Pas 1: u=x², dv=e^xdx => x²e^x - 2∫xe^xdx", "Pas 2: ∫xe^x dx = (x-1)e^x", "= x²e^x - 2(x-1)e^x = (x²-2x+2)e^x + C"]),
    ("∫ 1/(x²+1) dx", "arctan(x) + C", ["Integrală standard: ∫ 1/(x²+1) dx = arctan(x) + C"]),
    ("∫ 1/√(1-x²) dx", "arcsin(x) + C", ["Integrală standard: ∫ 1/√(1-x²) dx = arcsin(x) + C"]),
    ("∫ sin²(x) dx", "x/2 - sin(2x)/4 + C", ["sin²(x) = (1-cos(2x))/2", "∫ (1-cos(2x))/2 dx = x/2 - sin(2x)/4 + C"]),
    ("∫ e^(2x)·cos(x) dx", "e^(2x)(2cos(x)+sin(x))/5 + C", ["Integrare prin părți de 2 ori + ecuație", "Rezultat: e^(2x)(2cos(x)+sin(x))/5 + C"]),
    ("∫ ln(x) dx", "x·ln(x) - x + C", ["Integrare prin părți: u=ln(x), dv=dx", "= x·ln(x) - ∫(x·1/x)dx = x·ln(x) - x + C"]),
    ("∫ x/√(x²+1) dx", "√(x²+1) + C", ["Substituție: u = x²+1, du = 2xdx", "∫ du/(2√u) = √u + C = √(x²+1) + C"]),
]

for expr, result, steps in advanced_integrals:
    add(f"Calculați {expr}", result, steps + [f"Răspuns: {result}"], "integrale", 3, 2)

# ═══════════════════════════════════════════
# MATRICE AVANSATE
# ═══════════════════════════════════════════

# Inversa matricei 2x2
for a,b,c,d in [(2,1,1,1), (3,1,2,1), (1,2,3,4), (4,3,2,1)]:
    det = a*d - b*c
    if det == 0: continue
    add(f"Calculați inversa matricei A = [[{a},{b}],[{c},{d}]]",
        f"A⁻¹ = [[{d}/{det},{-b}/{det}],[{-c}/{det},{a}/{det}]]",
        [f"det(A) = {a}·{d} - {b}·{c} = {det}",
         f"A⁻¹ = (1/det) · [[{d},{-b}],[{-c},{a}]]",
         f"= (1/{det}) · [[{d},{-b}],[{-c},{a}]]",
         f"Răspuns: A⁻¹ = [[{d}/{det},{-b}/{det}],[{-c}/{det},{a}/{det}]]"],
        "matrice", 3, 1)

# Rang matrice
add("Determinați rangul matricei A = [[1,2,3],[2,4,6],[1,1,1]]",
    "2",
    ["Reducem prin operații pe linii:",
     "L2 = L2 - 2·L1: [[1,2,3],[0,0,0],[1,1,1]]",
     "L3 = L3 - L1: [[1,2,3],[0,0,0],[0,-1,-2]]",
     "Avem 2 linii nenule => rang(A) = 2",
     "Răspuns: rang(A) = 2"],
    "matrice", 3, 1)

# ═══════════════════════════════════════════
# NUMERE COMPLEXE AVANSATE
# ═══════════════════════════════════════════

# Forma trigonometrică
for a, b, r, theta in [(1, 1, "√2", "π/4"), (0, 2, "2", "π/2"), (1, -1, "√2", "-π/4"),
                        (-1, 0, "1", "π"), (3, 4, "5", "arctan(4/3)")]:
    add(f"Scrieți z = {a}+{b}i în formă trigonometrică",
        f"z = {r}(cos({theta}) + i·sin({theta}))",
        [f"z = {a}+{b}i",
         f"|z| = √({a}²+{b}²) = {r}",
         f"θ = arctan({b}/{a}) = {theta}",
         f"z = {r}(cos({theta}) + i·sin({theta}))"],
        "numere_complexe", 3, 1)

# ═══════════════════════════════════════════
# STUDIU COMPLET FUNCȚIE
# ═══════════════════════════════════════════

studies = [
    ("f(x) = x³ - 3x + 2", [
        "Domeniu: D = ℝ",
        "f'(x) = 3x² - 3 = 3(x-1)(x+1)",
        "f'(x) = 0 => x = -1 (maxim local), x = 1 (minim local)",
        "f(-1) = -1+3+2 = 4 (maxim local)",
        "f(1) = 1-3+2 = 0 (minim local)",
        "f''(x) = 6x, f''(0) = 0 => x=0 punct de inflexiune",
        "lim(x→-∞) f(x) = -∞, lim(x→+∞) f(x) = +∞",
        "Funcția e crescătoare pe (-∞,-1)∪(1,+∞), descrescătoare pe (-1,1)",
    ]),
    ("f(x) = x⁴ - 4x²", [
        "Domeniu: D = ℝ",
        "f'(x) = 4x³ - 8x = 4x(x²-2)",
        "f'(x) = 0 => x=0, x=±√2",
        "f(-√2) = 4-8 = -4 (minim local)",
        "f(0) = 0 (maxim local)",
        "f(√2) = 4-8 = -4 (minim local)",
        "f''(x) = 12x²-8, puncte inflexiune: x = ±√(2/3)",
        "lim(x→±∞) f(x) = +∞",
    ]),
    ("f(x) = xe^(-x)", [
        "Domeniu: D = ℝ",
        "f'(x) = e^(-x) - xe^(-x) = e^(-x)(1-x)",
        "f'(x) = 0 => x = 1 (maxim global)",
        "f(1) = 1/e ≈ 0.368",
        "f''(x) = e^(-x)(x-2), f''(0) = -2 < 0 => maxim confirmat",
        "lim(x→-∞) f(x) = -∞, lim(x→+∞) f(x) = 0",
        "Asimptotă orizontală: y = 0 (la +∞)",
    ]),
    ("f(x) = (x²-1)/(x²+1)", [
        "Domeniu: D = ℝ (numitorul > 0 mereu)",
        "f'(x) = (2x(x²+1) - (x²-1)·2x)/(x²+1)² = 4x/(x²+1)²",
        "f'(x) = 0 => x = 0 (minim global)",
        "f(0) = -1",
        "f crescătoare pe (0,+∞), descrescătoare pe (-∞,0)",
        "lim(x→±∞) f(x) = 1",
        "Asimptotă orizontală: y = 1",
        "Imagine: [-1, 1)",
    ]),
]

for func, steps in studies:
    add(f"Studiați funcția {func} (domeniu, derivată, monotonie, extreme, asimptote)",
        f"Studiu complet — vezi pașii",
        steps, "studiu_functie", 3, 2)

# ═══════════════════════════════════════════
# GEOMETRIE SPAȚIU
# ═══════════════════════════════════════════

add("Calculați volumul tetraedrului regulat cu muchia a = 6",
    "18√2",
    ["V = a³√2/12 = 6³·√2/12 = 216√2/12 = 18√2",
     "Răspuns: V = 18√2"],
    "geometrie", 3, 1)

add("Calculați aria laterală a conului cu R = 5 și g = 13",
    "65π",
    ["Al = π·R·g = π·5·13 = 65π",
     "Răspuns: Al = 65π"],
    "geometrie", 2, 1)

add("Calculați aria totală a cilindrului cu r = 3 și h = 8",
    "66π",
    ["Al = 2πrh = 2π·3·8 = 48π",
     "Ab = 2πr² = 2π·9 = 18π",
     "At = Al + Ab = 48π + 18π = 66π",
     "Răspuns: At = 66π"],
    "geometrie", 2, 1)

# Geometrie analitică avansată
add("Determinați ecuația cercului cu centrul C(2, 3) și raza r = 5",
    "(x-2)² + (y-3)² = 25",
    ["Ecuația cercului: (x-a)² + (y-b)² = r²",
     "C(2,3), r=5",
     "(x-2)² + (y-3)² = 25",
     "Răspuns: (x-2)² + (y-3)² = 25"],
    "geometrie_analitica", 2, 1)

add("Calculați distanța de la punctul P(3, 4) la dreapta 3x + 4y - 5 = 0",
    "4",
    ["d = |ax₀ + by₀ + c| / √(a²+b²)",
     "= |3·3 + 4·4 - 5| / √(9+16)",
     "= |9+16-5| / √25 = |20| / 5 = 4",
     "Răspuns: d = 4"],
    "geometrie_analitica", 2, 1)

add("Determinați ecuația dreptei care trece prin A(1,2) și B(3,6)",
    "y = 2x",
    ["m = (y₂-y₁)/(x₂-x₁) = (6-2)/(3-1) = 4/2 = 2",
     "y - 2 = 2(x - 1) => y = 2x",
     "Răspuns: y = 2x"],
    "geometrie_analitica", 1, 1)

# ═══════════════════════════════════════════
# STATISTICĂ & PROBABILITĂȚI AVANSATE
# ═══════════════════════════════════════════

add("Se aruncă 3 zaruri. P(suma = 10)?",
    "27/216 = 1/8",
    ["Total: 6³ = 216 cazuri",
     "Cazuri favorabile: combinațiile (a,b,c) cu a+b+c=10",
     "Se numără: 27 de combinații",
     "P = 27/216 = 1/8",
     "Răspuns: P = 1/8"],
    "probabilitati", 3, 1)

add("Distribuția binomială: n=5, p=0.3. P(X=2)?",
    "≈0.3087",
    ["P(X=k) = C(n,k)·p^k·(1-p)^(n-k)",
     "P(X=2) = C(5,2)·0.3²·0.7³",
     "= 10 · 0.09 · 0.343",
     "= 10 · 0.03087 = 0.3087",
     "Răspuns: P(X=2) ≈ 0.3087"],
    "probabilitati", 3, 1)

add("Media și dispersia: 2, 4, 4, 4, 5, 5, 7, 9",
    "Media = 5, Dispersia = 4",
    ["n = 8, Suma = 2+4+4+4+5+5+7+9 = 40",
     "Media = 40/8 = 5",
     "Dispersia = Σ(xi-x̄)²/n",
     "= (9+1+1+1+0+0+4+16)/8 = 32/8 = 4",
     "Răspuns: Media = 5, Dispersia = 4"],
    "probabilitati", 2, 1)

# ═══════════════════════════════════════════
# SALVARE
# ═══════════════════════════════════════════

print(f"Total exerciții extra generate: {len(exercises)}")

from collections import Counter
topics = Counter(e["topic"] for e in exercises)
for t, c in sorted(topics.items(), key=lambda x: -x[1]):
    print(f"  {t}: {c}")

# Merge cu existente
merged_path = Path(__file__).parent.parent / "data" / "processed" / "exercises_merged.json"
existing = json.load(open(merged_path, encoding="utf-8"))
existing_q = {e.get("question", "").strip().lower() for e in existing}

added = 0
for ex in exercises:
    if ex["question"].strip().lower() not in existing_q:
        existing.append(ex)
        existing_q.add(ex["question"].strip().lower())
        added += 1

print(f"\nAdăugate: {added} (de la {len(existing)-added} la {len(existing)})")

with open(merged_path, "w", encoding="utf-8") as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)
print(f"Salvat: {merged_path}")
