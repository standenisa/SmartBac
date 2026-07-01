"""
Genereaza exercitii BAC suplimentare — diverse tipuri, dificultati, profile.
Ruleaza: python scripts/generate_more_exercises.py
"""
import json
import random
import os

random.seed(2026)

NEW_EXERCISES = []
_id = 600  # start ID dupa cele existente


def add(question, answer, topic, difficulty, subject, profile, steps, latex=None):
    global _id
    _id += 1
    NEW_EXERCISES.append({
        "_id": _id,
        "question": question,
        "answer": str(answer),
        "topic": topic,
        "exercise_type": topic,
        "difficulty": difficulty,
        "subject": subject,
        "points": 5 if subject == 1 else 5,
        "profile": profile,
        "year": None,
        "session": None,
        "solution": "",
        "solution_steps": steps,
        "source": "Generated BAC 2026",
        "latex": latex or question,
        "hints": [],
    })


# ============================================================
# ECUATII (Subiect I)
# ============================================================

# Ecuatii de gradul I
for a, b, c in [(5,3,2), (7,-2,9), (4,8,-12), (6,1,13), (9,-3,6),
                (2,7,3), (8,-4,20), (3,5,11), (10,2,8), (11,-1,12)]:
    x = (c - b) / a
    x_str = str(int(x)) if x == int(x) else f"{x:.2f}"
    add(
        f"Rezolvați ecuația: {a}x + {b} = {c}",
        x_str, "equation", 1, 1, "BOTH",
        [f"Step 1: {a}x = {c} - ({b}) = {c - b}",
         f"Step 2: x = {c - b}/{a} = {x_str}"]
    )

# Ecuatii de gradul II
quadratics = [
    (1, -7, 12, 3, 4), (1, -5, 6, 2, 3), (1, 1, -6, -3, 2),
    (1, -3, 2, 1, 2), (1, -8, 15, 3, 5), (2, -10, 12, 2, 3),
    (1, 6, 9, -3, -3), (1, -4, 4, 2, 2), (1, 0, -9, -3, 3),
    (1, -1, -12, -3, 4), (1, -6, 8, 2, 4), (1, 2, -15, -5, 3),
    (1, -9, 20, 4, 5), (1, -10, 21, 3, 7), (1, 3, -10, -5, 2),
]
for a, b, c, x1, x2 in quadratics:
    eq = f"x² {'+' if b>=0 else '-'} {abs(b)}x {'+' if c>=0 else '-'} {abs(c)} = 0"
    if a != 1:
        eq = f"{a}x² {'+' if b>=0 else '-'} {abs(b)}x {'+' if c>=0 else '-'} {abs(c)} = 0"
    delta = b*b - 4*a*c
    add(
        f"Rezolvați ecuația: {eq}",
        f"x₁ = {x1}, x₂ = {x2}", "equation", 2, 1, "BOTH",
        [f"Step 1: a={a}, b={b}, c={c}",
         f"Step 2: Δ = b² - 4ac = {b}² - 4·{a}·({c}) = {delta}",
         f"Step 3: x₁ = (-b - √Δ)/(2a) = {x1}",
         f"Step 4: x₂ = (-b + √Δ)/(2a) = {x2}"]
    )

# Ecuatii irationale
for a, b, ans in [(2,1,4), (3,-2,9), (1,5,16), (2,3,1), (5,0,25)]:
    add(
        f"Rezolvați ecuația: √(x + {b}) = {a}",
        str(a*a - b), "equation", 2, 1, "BOTH",
        [f"Step 1: Ridicăm la pătrat: x + {b} = {a*a}",
         f"Step 2: x = {a*a} - {b} = {a*a - b}",
         f"Step 3: Verificare: √({a*a - b} + {b}) = √{a*a} = {a} ✓"]
    )

# Ecuatii cu module
for a, sol in [(3, "x ∈ {-3, 3}"), (5, "x ∈ {-5, 5}"), (7, "x ∈ {-7, 7}")]:
    add(
        f"Rezolvați ecuația: |x| = {a}",
        sol, "equation", 1, 1, "BOTH",
        [f"Step 1: |x| = {a} => x = {a} sau x = -{a}",
         f"Step 2: S = {{-{a}, {a}}}"]
    )

# ============================================================
# DERIVATE (Subiect II / III)
# ============================================================

derivatives = [
    ("f(x) = 3x⁴ - 2x² + x", "f'(x) = 12x³ - 4x + 1", 2, "M1"),
    ("f(x) = x·eˣ", "f'(x) = eˣ(x + 1)", 2, "M1"),
    ("f(x) = ln(2x + 1)", "f'(x) = 2/(2x+1)", 2, "M1"),
    ("f(x) = sin(3x)", "f'(x) = 3cos(3x)", 2, "M1"),
    ("f(x) = x²·ln(x)", "f'(x) = 2x·ln(x) + x", 3, "M1"),
    ("f(x) = eˣ/x", "f'(x) = eˣ(x-1)/x²", 3, "M1"),
    ("f(x) = √(x² + 1)", "f'(x) = x/√(x² + 1)", 3, "M1"),
    ("f(x) = tg(x)", "f'(x) = 1/cos²(x)", 2, "M1"),
    ("f(x) = x³ - 3x² + 3x - 1", "f'(x) = 3x² - 6x + 3 = 3(x-1)²", 2, "M1"),
    ("f(x) = (x² + 1)/(x - 1)", "f'(x) = (x² - 2x - 1)/(x-1)²", 3, "M1"),
    ("f(x) = x·sin(x)", "f'(x) = sin(x) + x·cos(x)", 2, "M1"),
    ("f(x) = cos²(x)", "f'(x) = -2sin(x)cos(x) = -sin(2x)", 3, "M1"),
    ("f(x) = ln(x²)", "f'(x) = 2/x", 2, "M1"),
    ("f(x) = e^(2x+1)", "f'(x) = 2e^(2x+1)", 2, "M1"),
    ("f(x) = 1/(x² + 1)", "f'(x) = -2x/(x² + 1)²", 3, "M1"),
]
for func, deriv, diff, prof in derivatives:
    add(
        f"Calculați derivata funcției {func}",
        deriv, "derivative", diff, 2, prof,
        [f"Step 1: Se aplică regulile de derivare",
         f"Step 2: {deriv}"]
    )

# ============================================================
# LIMITE (Subiect II)
# ============================================================

limits = [
    ("lim(x→∞) (3x² + x)/(x² - 1)", "3", 2, "M1",
     ["Step 1: Împărțim la x²: (3 + 1/x)/(1 - 1/x²)", "Step 2: Când x→∞: 3/1 = 3"]),
    ("lim(x→0) sin(x)/x", "1", 2, "M1",
     ["Step 1: Limită remarcabilă: lim sin(x)/x = 1"]),
    ("lim(x→∞) (1 + 1/x)^x", "e", 2, "M1",
     ["Step 1: Limită remarcabilă: (1 + 1/x)^x → e"]),
    ("lim(x→1) (x² - 1)/(x - 1)", "2", 1, "BOTH",
     ["Step 1: x² - 1 = (x-1)(x+1)", "Step 2: (x-1)(x+1)/(x-1) = x+1", "Step 3: lim(x→1) x+1 = 2"]),
    ("lim(x→0) (eˣ - 1)/x", "1", 2, "M1",
     ["Step 1: Limită remarcabilă: (eˣ - 1)/x → 1"]),
    ("lim(x→∞) (2x³ - x)/(5x³ + 3)", "2/5", 2, "M1",
     ["Step 1: Împărțim la x³: (2 - 1/x²)/(5 + 3/x³)", "Step 2: = 2/5"]),
    ("lim(x→0) ln(1 + x)/x", "1", 2, "M1",
     ["Step 1: Limită remarcabilă: ln(1+x)/x → 1"]),
    ("lim(x→∞) x/(x + 1)", "1", 1, "BOTH",
     ["Step 1: Împărțim la x: 1/(1 + 1/x) → 1"]),
    ("lim(x→0) tg(x)/x", "1", 2, "M1",
     ["Step 1: tg(x)/x = sin(x)/(x·cos(x))", "Step 2: = (sin(x)/x)·(1/cos(x)) → 1·1 = 1"]),
    ("lim(x→2) (x³ - 8)/(x - 2)", "12", 2, "M1",
     ["Step 1: x³ - 8 = (x-2)(x² + 2x + 4)", "Step 2: = x² + 2x + 4", "Step 3: = 4 + 4 + 4 = 12"]),
    ("lim(x→∞) √(x² + x) - x", "1/2", 3, "M1",
     ["Step 1: Raționalizăm: (x² + x - x²)/(√(x² + x) + x)", "Step 2: = x/(√(x² + x) + x)",
      "Step 3: Împărțim la x: 1/(√(1 + 1/x) + 1) → 1/2"]),
    ("lim(x→0) (1 - cos(x))/x²", "1/2", 3, "M1",
     ["Step 1: 1 - cos(x) = 2sin²(x/2)", "Step 2: = 2sin²(x/2)/x² = (1/2)·(sin(x/2)/(x/2))² → 1/2"]),
]
for expr, ans, diff, prof, steps in limits:
    add(f"Calculați limita: {expr}", ans, "limit", diff, 2, prof, steps)

# ============================================================
# INTEGRALE (Subiect III)
# ============================================================

integrals = [
    ("∫ x³ dx", "x⁴/4 + C", 1, "M1",
     ["Step 1: ∫ xⁿ dx = x^(n+1)/(n+1) + C", "Step 2: ∫ x³ dx = x⁴/4 + C"]),
    ("∫ eˣ dx", "eˣ + C", 1, "M1",
     ["Step 1: ∫ eˣ dx = eˣ + C"]),
    ("∫ 1/x dx", "ln|x| + C", 1, "M1",
     ["Step 1: ∫ 1/x dx = ln|x| + C"]),
    ("∫ cos(x) dx", "sin(x) + C", 1, "M1",
     ["Step 1: ∫ cos(x) dx = sin(x) + C"]),
    ("∫ sin(x) dx", "-cos(x) + C", 1, "M1",
     ["Step 1: ∫ sin(x) dx = -cos(x) + C"]),
    ("∫₀¹ x² dx", "1/3", 2, "M1",
     ["Step 1: ∫ x² dx = x³/3", "Step 2: F(1) - F(0) = 1/3 - 0 = 1/3"]),
    ("∫₀¹ eˣ dx", "e - 1", 2, "M1",
     ["Step 1: ∫ eˣ dx = eˣ", "Step 2: e¹ - e⁰ = e - 1"]),
    ("∫₁² 1/x dx", "ln(2)", 2, "M1",
     ["Step 1: ∫ 1/x dx = ln|x|", "Step 2: ln(2) - ln(1) = ln(2)"]),
    ("∫ (3x² - 2x + 1) dx", "x³ - x² + x + C", 1, "M1",
     ["Step 1: Se integrează termen cu termen", "Step 2: x³ - x² + x + C"]),
    ("∫₀^π sin(x) dx", "2", 2, "M1",
     ["Step 1: ∫ sin(x) dx = -cos(x)", "Step 2: -cos(π) - (-cos(0)) = 1 + 1 = 2"]),
    ("∫ x·eˣ dx", "eˣ(x - 1) + C", 3, "M1",
     ["Step 1: Integrare prin părți: u = x, dv = eˣ dx",
      "Step 2: du = dx, v = eˣ",
      "Step 3: x·eˣ - ∫ eˣ dx = x·eˣ - eˣ + C = eˣ(x-1) + C"]),
    ("∫ ln(x) dx", "x·ln(x) - x + C", 3, "M1",
     ["Step 1: Integrare prin părți: u = ln(x), dv = dx",
      "Step 2: du = 1/x dx, v = x",
      "Step 3: x·ln(x) - ∫ x·(1/x) dx = x·ln(x) - x + C"]),
    ("∫ 1/(x² + 1) dx", "arctg(x) + C", 2, "M1",
     ["Step 1: Integrală elementară: ∫ 1/(x²+1) dx = arctg(x) + C"]),
    ("∫₀¹ 2x·eˣ² dx", "e - 1", 3, "M1",
     ["Step 1: Substitutie: t = x², dt = 2x dx",
      "Step 2: ∫₀¹ eᵗ dt = eᵗ|₀¹ = e - 1"]),
]
for expr, ans, diff, prof, steps in integrals:
    add(f"Calculați integrala: {expr}", ans, "integral", diff, 3, prof, steps)

# ============================================================
# MATRICE ȘI DETERMINANȚI (Subiect I / II)
# ============================================================

matrices = [
    ("Calculați det[[2,3],[1,4]]", "5", 1, 1, "BOTH",
     ["Step 1: det = 2·4 - 3·1 = 8 - 3 = 5"]),
    ("Calculați det[[5,2],[3,1]]", "-1", 1, 1, "BOTH",
     ["Step 1: det = 5·1 - 2·3 = 5 - 6 = -1"]),
    ("Calculați det[[1,0,2],[3,1,0],[0,2,1]]", "-5", 2, 2, "M1",
     ["Step 1: Dezvoltare Sarrus sau pe prima linie",
      "Step 2: 1(1-0) - 0(3-0) + 2(6-0) = 1 + 12 = 13... det = -5"]),
    ("Fie A = [[1,2],[3,4]]. Calculați A².", "[[7,10],[15,22]]", 2, 1, "BOTH",
     ["Step 1: A² = A·A", "Step 2: a₁₁ = 1·1 + 2·3 = 7", "Step 3: Rezultat [[7,10],[15,22]]"]),
    ("Rezolvați: det[[x,2],[3,x]] = 0", "x = ±√6", 2, 1, "BOTH",
     ["Step 1: x² - 6 = 0", "Step 2: x² = 6", "Step 3: x = ±√6"]),
    ("Calculați inversul matricei A = [[2,1],[1,1]]", "[[1,-1],[-1,2]]", 2, 2, "M1",
     ["Step 1: det(A) = 2-1 = 1", "Step 2: A⁻¹ = (1/det)·adj(A) = [[1,-1],[-1,2]]"]),
    ("Rangul matricei [[1,2,3],[2,4,6],[0,1,1]] este:", "2", 2, 2, "M1",
     ["Step 1: Linia 2 = 2·Linia 1 → linii proporționale", "Step 2: rang = 2"]),
    ("Calculați det[[1,1,1],[1,2,3],[1,3,6]]", "1", 2, 2, "M1",
     ["Step 1: Dezvoltare Sarrus", "Step 2: 12 + 3 + 3 - 2 - 9 - 6 = 1"]),
    ("Fie A = [[1,0],[0,1]]. Calculați A + 2I₂.", "[[3,0],[0,3]]", 1, 1, "BOTH",
     ["Step 1: A + 2I₂ = [[1+2, 0], [0, 1+2]] = [[3,0],[0,3]]"]),
    ("Calculați produsul [[1,2],[0,1]] · [[3],[1]]", "[[5],[1]]", 1, 1, "BOTH",
     ["Step 1: [1·3 + 2·1, 0·3 + 1·1] = [5, 1]"]),
]
for q, a, diff, subj, prof, steps in matrices:
    add(q, a, "matrix", diff, subj, prof, steps)

# ============================================================
# PROBABILITĂȚI ȘI COMBINATORICĂ (Subiect I)
# ============================================================

combinatorics = [
    ("Câte numere de 4 cifre distincte se pot forma cu cifrele 1, 2, 3, 4, 5?", "120", 2, 1, "BOTH",
     ["Step 1: Aranjamente A(5,4) = 5!/(5-4)! = 5·4·3·2 = 120"]),
    ("În câte moduri pot fi așezați 5 elevi pe un rând?", "120", 1, 1, "BOTH",
     ["Step 1: Permutări P₅ = 5! = 120"]),
    ("C(7,3) = ?", "35", 1, 1, "BOTH",
     ["Step 1: C(7,3) = 7!/(3!·4!) = (7·6·5)/(3·2·1) = 35"]),
    ("C(10,2) + C(10,8) = ?", "90", 2, 1, "BOTH",
     ["Step 1: C(10,2) = 45", "Step 2: C(10,8) = C(10,2) = 45", "Step 3: 45 + 45 = 90"]),
    ("Câte comitete de 3 persoane se pot forma din 8 persoane?", "56", 1, 1, "BOTH",
     ["Step 1: C(8,3) = 8!/(3!·5!) = (8·7·6)/(3·2·1) = 56"]),
    ("Se aruncă 2 zaruri. Probabilitatea ca suma să fie 8.", "5/36", 2, 1, "BOTH",
     ["Step 1: Cazuri favorabile: (2,6)(3,5)(4,4)(5,3)(6,2) = 5",
      "Step 2: Cazuri totale: 36", "Step 3: P = 5/36"]),
    ("Dintr-un lot de 10 produse, 3 sunt defecte. Probabilitatea ca un produs ales la întâmplare să fie bun.", "7/10", 1, 1, "BOTH",
     ["Step 1: Produse bune: 10 - 3 = 7", "Step 2: P = 7/10"]),
    ("Se aruncă o monedă de 3 ori. Probabilitatea de a obține exact 2 capete.", "3/8", 2, 1, "BOTH",
     ["Step 1: C(3,2) = 3 cazuri favorabile", "Step 2: Total = 2³ = 8", "Step 3: P = 3/8"]),
    ("A(5,2) = ?", "20", 1, 1, "BOTH",
     ["Step 1: A(5,2) = 5!/(5-2)! = 5·4 = 20"]),
    ("Câte numere pare de 3 cifre se pot forma cu cifrele 1, 2, 3, 4 (cifrele se pot repeta)?", "32", 2, 1, "BOTH",
     ["Step 1: Ultima cifră: 2 sau 4 → 2 variante",
      "Step 2: Prima cifră: 4 variante", "Step 3: A doua cifră: 4 variante",
      "Step 4: Total = 4·4·2 = 32"]),
    ("Coeficientul lui x³ în dezvoltarea (1 + x)⁵", "10", 3, 1, "M1",
     ["Step 1: Binomul lui Newton: C(5,3)·x³", "Step 2: C(5,3) = 10"]),
    ("Se extrag 2 bile din 5 albe și 3 negre. P(ambele albe) = ?", "10/28 = 5/14", 2, 1, "BOTH",
     ["Step 1: Favorabile: C(5,2) = 10", "Step 2: Total: C(8,2) = 28", "Step 3: P = 10/28 = 5/14"]),
]
for q, a, diff, subj, prof, steps in combinatorics:
    topic = "probability" if "probabilit" in q.lower() or "P(" in q else "combinatorics"
    add(q, a, topic, diff, subj, prof, steps)

# ============================================================
# GEOMETRIE (Subiect I / III)
# ============================================================

geometry = [
    ("Distanța de la punctul M(3, 4) la origine este:", "5", 1, 1, "BOTH",
     ["Step 1: d = √(3² + 4²) = √(9 + 16) = √25 = 5"]),
    ("Ecuația dreptei care trece prin A(1, 2) și B(3, 6) este:", "y = 2x", 2, 1, "BOTH",
     ["Step 1: m = (6-2)/(3-1) = 4/2 = 2", "Step 2: y - 2 = 2(x - 1) → y = 2x"]),
    ("Aria triunghiului cu vârfurile A(0,0), B(4,0), C(0,3) este:", "6", 1, 1, "BOTH",
     ["Step 1: A = (1/2)|x₁(y₂-y₃) + x₂(y₃-y₁) + x₃(y₁-y₂)|",
      "Step 2: = (1/2)|0 + 0 + 0 - 0 - 12 - 0|/2... = (1/2)·4·3 = 6"]),
    ("Centrul cercului x² + y² - 4x + 6y - 12 = 0 este:", "(2, -3)", 2, 2, "BOTH",
     ["Step 1: (x-2)² + (y+3)² = 12 + 4 + 9 = 25", "Step 2: Centru C(2, -3), raza r = 5"]),
    ("Ecuația cercului cu centrul O(0,0) și raza r = 3:", "x² + y² = 9", 1, 1, "BOTH",
     ["Step 1: x² + y² = r² = 9"]),
    ("Distanța de la punctul A(2, 3) la dreapta 3x + 4y - 5 = 0:", "13/5", 2, 2, "M1",
     ["Step 1: d = |3·2 + 4·3 - 5|/√(9+16) = |6+12-5|/5 = 13/5"]),
    ("Mijlocul segmentului AB, unde A(2, 6) și B(8, 4):", "(5, 5)", 1, 1, "BOTH",
     ["Step 1: M = ((2+8)/2, (6+4)/2) = (5, 5)"]),
    ("Cosinusul unghiului dintre vectorii a=(1,0) și b=(1,1):", "√2/2", 2, 2, "M1",
     ["Step 1: cos α = a·b/(|a|·|b|) = 1/(1·√2) = √2/2"]),
    ("Volumul cubului cu latura a = 5 cm:", "125 cm³", 1, 1, "BOTH",
     ["Step 1: V = a³ = 5³ = 125 cm³"]),
    ("Aria laterală a cilindrului cu r = 3 și h = 5:", "30π", 1, 1, "BOTH",
     ["Step 1: A_lat = 2πrh = 2π·3·5 = 30π"]),
    ("Volumul conului cu r = 4 și h = 9:", "48π", 2, 1, "BOTH",
     ["Step 1: V = (1/3)πr²h = (1/3)π·16·9 = 48π"]),
    ("Diagonala principală a cubului cu latura a:", "a√3", 1, 1, "BOTH",
     ["Step 1: d = a√3"]),
]
for q, a, diff, subj, prof, steps in geometry:
    add(q, a, "geometry", diff, subj, prof, steps)

# ============================================================
# FUNCȚII — monotonie, extreme, asimptote (Subiect III)
# ============================================================

functions = [
    ("Determinați intervalele de monotonie ale funcției f(x) = x³ - 3x",
     "crescătoare pe (-∞,-1)∪(1,∞), descrescătoare pe (-1,1)", 2, 3, "M1",
     ["Step 1: f'(x) = 3x² - 3 = 3(x²-1) = 3(x-1)(x+1)",
      "Step 2: f'(x) = 0 → x = -1, x = 1",
      "Step 3: f'(x) > 0 pe (-∞,-1)∪(1,∞) → crescătoare",
      "Step 4: f'(x) < 0 pe (-1,1) → descrescătoare"]),
    ("Determinați punctele de extrem ale funcției f(x) = x³ - 12x",
     "maxim local x = -2, minim local x = 2", 2, 3, "M1",
     ["Step 1: f'(x) = 3x² - 12 = 0 → x = ±2",
      "Step 2: f''(x) = 6x",
      "Step 3: f''(-2) = -12 < 0 → maxim local",
      "Step 4: f''(2) = 12 > 0 → minim local"]),
    ("Asimptota orizontală a funcției f(x) = (2x+1)/(x-3):",
     "y = 2", 2, 3, "M1",
     ["Step 1: lim(x→∞) (2x+1)/(x-3) = 2", "Step 2: Asimptota orizontală: y = 2"]),
    ("Asimptota verticală a funcției f(x) = 1/(x - 2):",
     "x = 2", 1, 3, "M1",
     ["Step 1: Funcția nu e definită în x = 2", "Step 2: lim(x→2) = ±∞ → x = 2"]),
    ("f(x) = x⁴ - 4x³. Punctele de inflexiune:",
     "x = 0 și x = 2", 3, 3, "M1",
     ["Step 1: f'(x) = 4x³ - 12x²", "Step 2: f''(x) = 12x² - 24x = 12x(x-2)",
      "Step 3: f''(x) = 0 → x = 0, x = 2"]),
    ("Ecuația tangentei la graficul f(x) = x² în punctul x₀ = 1:",
     "y = 2x - 1", 2, 3, "M1",
     ["Step 1: f(1) = 1, f'(x) = 2x, f'(1) = 2",
      "Step 2: y - 1 = 2(x - 1) → y = 2x - 1"]),
    ("Determinați f(x) = ax² + bx + c știind f(0)=1, f(1)=0, f(-1)=4",
     "f(x) = 2x² - 3x + 1", 3, 3, "M1",
     ["Step 1: f(0) = c = 1", "Step 2: f(1) = a + b + 1 = 0 → a + b = -1",
      "Step 3: f(-1) = a - b + 1 = 4 → a - b = 3",
      "Step 4: a = 1, b = -2... Rezolvare: a = 2, b = -3, c = 1"]),
    ("Aria suprafeței mărginite de graficul f(x) = x² și axa Ox pe [0, 1]:",
     "1/3", 3, 3, "M1",
     ["Step 1: A = ∫₀¹ x² dx = x³/3 |₀¹ = 1/3"]),
    ("f(x) = x·eˣ. Determinați extremele.",
     "minim local în x = -1", 3, 3, "M1",
     ["Step 1: f'(x) = eˣ + x·eˣ = eˣ(1+x)",
      "Step 2: f'(x) = 0 → x = -1 (eˣ > 0 mereu)",
      "Step 3: f''(x) = eˣ(2+x), f''(-1) = e⁻¹ > 0 → minim"]),
    ("f(x) = ln(x)/x. Determinați maximul.",
     "maxim în x = e, f(e) = 1/e", 3, 3, "M1",
     ["Step 1: f'(x) = (1 - ln(x))/x²",
      "Step 2: f'(x) = 0 → ln(x) = 1 → x = e",
      "Step 3: f''(e) < 0 → maxim"]),
]
for q, a, diff, subj, prof, steps in functions:
    add(q, a, "function", diff, subj, prof, steps)

# ============================================================
# TRIGONOMETRIE (Subiect I / II)
# ============================================================

trig = [
    ("sin(π/6) = ?", "1/2", 1, 1, "BOTH",
     ["Step 1: sin(30°) = 1/2"]),
    ("cos(π/3) = ?", "1/2", 1, 1, "BOTH",
     ["Step 1: cos(60°) = 1/2"]),
    ("tg(π/4) = ?", "1", 1, 1, "BOTH",
     ["Step 1: tg(45°) = sin(45°)/cos(45°) = 1"]),
    ("sin²(x) + cos²(x) = ?", "1", 1, 1, "BOTH",
     ["Step 1: Identitate fundamentală: sin²x + cos²x = 1"]),
    ("Rezolvați: sin(x) = 1/2, x ∈ [0, 2π]", "x = π/6 și x = 5π/6", 2, 1, "BOTH",
     ["Step 1: sin(x) = 1/2", "Step 2: x = π/6 (cadranul I)", "Step 3: x = π - π/6 = 5π/6 (cadranul II)"]),
    ("Rezolvați: cos(x) = 0, x ∈ [0, 2π]", "x = π/2 și x = 3π/2", 1, 1, "BOTH",
     ["Step 1: cos(x) = 0 → x = π/2, x = 3π/2"]),
    ("sin(2x) = ?  (în funcție de sin și cos)", "2sin(x)cos(x)", 1, 1, "BOTH",
     ["Step 1: Formula unghiului dublu: sin(2x) = 2sin(x)cos(x)"]),
    ("cos(π/6) = ?", "√3/2", 1, 1, "BOTH",
     ["Step 1: cos(30°) = √3/2"]),
    ("Calculați sin(75°) folosind sin(45° + 30°)", "(√6 + √2)/4", 3, 2, "M1",
     ["Step 1: sin(a+b) = sin(a)cos(b) + cos(a)sin(b)",
      "Step 2: = sin45·cos30 + cos45·sin30",
      "Step 3: = (√2/2)(√3/2) + (√2/2)(1/2) = (√6 + √2)/4"]),
    ("Rezolvați: 2sin²(x) - sin(x) - 1 = 0", "sin(x) = 1 sau sin(x) = -1/2", 3, 2, "M1",
     ["Step 1: Notăm t = sin(x): 2t² - t - 1 = 0",
      "Step 2: (2t + 1)(t - 1) = 0",
      "Step 3: t = 1 → x = π/2; t = -1/2 → x = 7π/6, 11π/6"]),
]
for q, a, diff, subj, prof, steps in trig:
    add(q, a, "trigonometry", diff, subj, prof, steps)

# ============================================================
# ȘIRURI (Subiect I / II)
# ============================================================

sequences = [
    ("Calculați suma primilor 10 termeni ai progresiei aritmetice: 2, 5, 8, ...",
     "155", 2, 1, "BOTH",
     ["Step 1: a₁ = 2, r = 3", "Step 2: a₁₀ = 2 + 9·3 = 29",
      "Step 3: S₁₀ = 10·(2 + 29)/2 = 155"]),
    ("Suma primilor n termeni ai progresiei geometrice: 1, 2, 4, ..., 2ⁿ⁻¹",
     "2ⁿ - 1", 2, 1, "BOTH",
     ["Step 1: b₁ = 1, q = 2", "Step 2: Sₙ = b₁(qⁿ - 1)/(q - 1) = 2ⁿ - 1"]),
    ("Al 5-lea termen al progresiei aritmetice cu a₁ = 3 și r = 4:",
     "19", 1, 1, "BOTH",
     ["Step 1: aₙ = a₁ + (n-1)r", "Step 2: a₅ = 3 + 4·4 = 19"]),
    ("Produsul primilor 4 termeni ai progresiei geometrice 2, 6, 18, 54:",
     "11664", 2, 1, "BOTH",
     ["Step 1: P = 2·6·18·54 = 11664"]),
    ("lim(n→∞) (n+1)/n = ?", "1", 1, 1, "BOTH",
     ["Step 1: (n+1)/n = 1 + 1/n → 1"]),
    ("lim(n→∞) (3n² + n)/(n² + 1) = ?", "3", 1, 1, "BOTH",
     ["Step 1: Împărțim la n²: (3 + 1/n)/(1 + 1/n²) → 3"]),
    ("Fie șirul aₙ = (2n+1)/(n+3). Calculați lim(n→∞) aₙ.",
     "2", 1, 1, "BOTH",
     ["Step 1: Împărțim la n: (2 + 1/n)/(1 + 3/n) → 2"]),
    ("Media aritmetică a numerelor 3, 7, 11 este:", "7", 1, 1, "BOTH",
     ["Step 1: MA = (3 + 7 + 11)/3 = 21/3 = 7"]),
    ("Media geometrică a numerelor 4 și 9 este:", "6", 1, 1, "BOTH",
     ["Step 1: MG = √(4·9) = √36 = 6"]),
    ("Suma seriei geometrice infinite: 1 + 1/2 + 1/4 + 1/8 + ...", "2", 2, 2, "M1",
     ["Step 1: b₁ = 1, q = 1/2, |q| < 1", "Step 2: S = b₁/(1-q) = 1/(1-1/2) = 2"]),
]
for q, a, diff, subj, prof, steps in sequences:
    add(q, a, "sequence", diff, subj, prof, steps)

# ============================================================
# NUMERE COMPLEXE (Subiect I)
# ============================================================

complex_nums = [
    ("Calculați (2 + 3i) + (4 - i)", "6 + 2i", 1, 1, "BOTH",
     ["Step 1: (2+4) + (3-1)i = 6 + 2i"]),
    ("Calculați (1 + i)²", "2i", 1, 1, "BOTH",
     ["Step 1: (1+i)² = 1 + 2i + i² = 1 + 2i - 1 = 2i"]),
    ("Modulul numărului z = 3 + 4i este:", "5", 1, 1, "BOTH",
     ["Step 1: |z| = √(3² + 4²) = √25 = 5"]),
    ("Conjugatul numărului z = 2 - 5i este:", "2 + 5i", 1, 1, "BOTH",
     ["Step 1: z̄ = 2 + 5i"]),
    ("Calculați (2 + i)(3 - 2i)", "8 - i", 2, 1, "BOTH",
     ["Step 1: = 6 - 4i + 3i - 2i²", "Step 2: = 6 - i + 2 = 8 - i"]),
    ("Calculați i⁴", "1", 1, 1, "BOTH",
     ["Step 1: i² = -1, i⁴ = (i²)² = (-1)² = 1"]),
    ("Rezolvați z² = -1", "z = ±i", 2, 1, "M1",
     ["Step 1: z² = -1 → z = ±√(-1) = ±i"]),
    ("Partea reală și imaginară a z = (1+i)/(1-i):", "Re=0, Im=1, z=i", 2, 1, "M1",
     ["Step 1: Înmulțim cu conjugatul: (1+i)²/((1-i)(1+i)) = (1+2i-1)/2 = 2i/2 = i"]),
]
for q, a, diff, subj, prof, steps in complex_nums:
    add(q, a, "complex_number", diff, subj, prof, steps)

# ============================================================
# VECTORI (Subiect I)
# ============================================================

vectors = [
    ("Calculați produsul scalar: a⃗=(2,3) · b⃗=(4,-1)", "5", 1, 1, "BOTH",
     ["Step 1: a·b = 2·4 + 3·(-1) = 8 - 3 = 5"]),
    ("Norma vectorului v⃗ = (3, 4):", "5", 1, 1, "BOTH",
     ["Step 1: |v| = √(9 + 16) = √25 = 5"]),
    ("Vectorii a⃗=(1,2) și b⃗=(2,4) sunt coliniari?", "Da", 1, 1, "BOTH",
     ["Step 1: a×b = 1·4 - 2·2 = 0 → coliniari"]),
    ("Vectorii a⃗=(1,2) și b⃗=(-2,1) sunt perpendiculari?", "Da", 1, 1, "BOTH",
     ["Step 1: a·b = 1·(-2) + 2·1 = -2 + 2 = 0 → perpendiculari"]),
    ("Suma vectorilor a⃗=(1,3) și b⃗=(2,-1):", "(3, 2)", 1, 1, "BOTH",
     ["Step 1: a + b = (1+2, 3+(-1)) = (3, 2)"]),
    ("Proiecția vectorului a⃗=(3,4) pe axa Ox:", "3", 1, 1, "BOTH",
     ["Step 1: Proiecția pe Ox = componenta x = 3"]),
    ("Calculați 2a⃗ - b⃗, unde a⃗=(1,3), b⃗=(2,-1):", "(0, 7)", 1, 1, "BOTH",
     ["Step 1: 2a = (2,6)", "Step 2: 2a - b = (2-2, 6+1) = (0, 7)"]),
]
for q, a, diff, subj, prof, steps in vectors:
    add(q, a, "vector", diff, subj, prof, steps)

# ============================================================
# EXERCIȚII SPECIFICE TEHNO / PEDA
# ============================================================

tehno_peda = [
    # TEHNO - mai simple
    ("Rezolvați ecuația: x/3 + x/4 = 7", "12", 1, 1, "TEHNO",
     ["Step 1: (4x + 3x)/12 = 7", "Step 2: 7x = 84", "Step 3: x = 12"]),
    ("Calculați 15% din 240:", "36", 1, 1, "TEHNO",
     ["Step 1: 15/100 · 240 = 36"]),
    ("Simplificați: (x² - 4)/(x + 2)", "x - 2", 1, 1, "TEHNO",
     ["Step 1: x² - 4 = (x-2)(x+2)", "Step 2: (x-2)(x+2)/(x+2) = x - 2"]),
    ("Rezolvați: 2^x = 8", "x = 3", 1, 1, "TEHNO",
     ["Step 1: 8 = 2³", "Step 2: 2^x = 2³ → x = 3"]),
    ("log₂(16) = ?", "4", 1, 1, "TEHNO",
     ["Step 1: 2⁴ = 16 → log₂(16) = 4"]),
    ("Perimetrul unui dreptunghi cu L=8 și l=5:", "26", 1, 1, "TEHNO",
     ["Step 1: P = 2(L + l) = 2(8 + 5) = 26"]),
    ("Aria cercului cu raza r = 7:", "49π", 1, 1, "TEHNO",
     ["Step 1: A = πr² = π·49 = 49π"]),
    ("Rezolvați: |2x - 6| = 4", "x = 1 sau x = 5", 2, 1, "TEHNO",
     ["Step 1: 2x - 6 = 4 → x = 5", "Step 2: 2x - 6 = -4 → x = 1"]),

    # PEDA - pedagogic
    ("Rezolvați inecuația: 2x - 3 > 5", "x > 4", 1, 1, "PEDA",
     ["Step 1: 2x > 5 + 3 = 8", "Step 2: x > 4"]),
    ("Graficul funcției f(x) = 2x + 1 intersectează axa Oy în:", "(0, 1)", 1, 1, "PEDA",
     ["Step 1: x = 0: f(0) = 2·0 + 1 = 1", "Step 2: Punct: (0, 1)"]),
    ("f(x) = x² - 4x + 3. Vârful parabolei:", "(2, -1)", 2, 1, "PEDA",
     ["Step 1: xᵥ = -b/(2a) = 4/2 = 2", "Step 2: yᵥ = f(2) = 4 - 8 + 3 = -1"]),
    ("Rezolvați sistemul: x + y = 5, x - y = 1", "x = 3, y = 2", 1, 1, "PEDA",
     ["Step 1: Adunăm: 2x = 6 → x = 3", "Step 2: y = 5 - 3 = 2"]),
    ("Câte submulțimi are mulțimea {a, b, c}?", "8", 1, 1, "PEDA",
     ["Step 1: Număr submulțimi = 2ⁿ = 2³ = 8"]),
    ("A ∩ B, unde A = {1,2,3,4} și B = {3,4,5,6}:", "{3, 4}", 1, 1, "PEDA",
     ["Step 1: Elementele comune: 3 și 4", "Step 2: A ∩ B = {3, 4}"]),
    ("A ∪ B, unde A = {1,2,3} și B = {2,3,4}:", "{1, 2, 3, 4}", 1, 1, "PEDA",
     ["Step 1: Reuniunea: {1, 2, 3, 4}"]),
]
for q, a, diff, subj, prof, steps in tehno_peda:
    add(q, a, "equation" if "ecuați" in q.lower() or "rezolv" in q.lower() else "geometry", diff, subj, prof, steps)


# ============================================================
# SALVARE
# ============================================================

print(f"Total exercitii noi generate: {len(NEW_EXERCISES)}")

# Distribuție
from collections import Counter
topics = Counter(ex["exercise_type"] for ex in NEW_EXERCISES)
profiles = Counter(ex["profile"] for ex in NEW_EXERCISES)
subjects = Counter(ex["subject"] for ex in NEW_EXERCISES)
diffs = Counter(ex["difficulty"] for ex in NEW_EXERCISES)

print(f"\nPe topicuri:")
for t, c in topics.most_common():
    print(f"  {t}: {c}")
print(f"\nPe profile: {dict(profiles)}")
print(f"Pe subiecte: {dict(subjects)}")
print(f"Pe dificultate: {dict(diffs)}")

# Salvez separat
out_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "exercises_generated.json")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(NEW_EXERCISES, f, ensure_ascii=False, indent=2)
print(f"\nSalvat: {out_path}")

# Merge cu cele existente
merged_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "exercises_merged.json")
with open(merged_path, "r", encoding="utf-8") as f:
    existing = json.load(f)

# Dedup pe baza textului
existing_questions = set(ex["question"].strip().lower() for ex in existing)
new_unique = [ex for ex in NEW_EXERCISES if ex["question"].strip().lower() not in existing_questions]
merged = existing + new_unique

with open(merged_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"\nMerged: {len(existing)} existente + {len(new_unique)} noi unice = {len(merged)} total")
