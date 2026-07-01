"""
Generate comprehensive BAC math exercises with step-by-step solutions.
Covers all 4 profiles (M1, M2, M3, M4) and all exam topics.
"""

import json
import random
import os
from pathlib import Path

random.seed(42)

exercises = []
_id = 1000  # Start from 1000 to avoid conflicts


def add(question, answer, steps, ex_type, topic, difficulty, profile, subject=1):
    global _id
    _id += 1
    exercises.append({
        "id": _id,
        "question": question,
        "answer": answer,
        "type": ex_type,
        "steps": steps,
        "difficulty": difficulty,
        "profile": profile,
        "subject": subject,
        "topic": topic,
        "source": "generated_bac_2026",
    })


# ============================================================================
# SUBIECTUL I - Toate profilele
# ============================================================================

# --- ECUATII DE GRADUL 1 ---
for a, b in [(2,6), (3,9), (5,15), (7,21), (4,12), (6,18), (8,24), (9,27), (10,30), (3,15)]:
    x = b // a
    add(f"Rezolvati ecuatia: {a}x = {b}", f"x = {x}",
        [f"Impartim ambele parti la {a}", f"x = {b}/{a}", f"x = {x}"],
        "equation", "ecuatii gradul 1", 1, "BOTH")

for a, b, c in [(2,3,7), (3,5,11), (4,1,9), (5,3,13), (6,2,14), (7,1,15), (3,4,10), (8,3,19), (2,7,13), (4,5,17)]:
    x = (c - b) / a
    add(f"Rezolvati ecuatia: {a}x + {b} = {c}", f"x = {x:.0f}" if x == int(x) else f"x = {x}",
        [f"Mutam {b} in dreapta: {a}x = {c} - {b}", f"{a}x = {c-b}", f"x = {c-b}/{a}", f"x = {x}"],
        "equation", "ecuatii gradul 1", 1, "BOTH")

# --- ECUATII DE GRADUL 2 ---
pairs = [(1,2), (1,3), (1,4), (1,5), (2,3), (2,5), (3,4), (3,5), (4,5), (1,6),
         (2,7), (3,6), (1,7), (2,4), (3,7), (4,6), (5,6), (1,8), (2,6), (3,8)]
for x1, x2 in pairs:
    b = -(x1 + x2)
    c = x1 * x2
    bstr = f"+ {b}" if b > 0 else f"- {-b}"
    cstr = f"+ {c}" if c > 0 else f"- {-c}"
    delta = b*b - 4*c
    add(f"Rezolvati ecuatia: x² {bstr}x {cstr} = 0",
        f"x1 = {x1}, x2 = {x2}",
        [f"Identificam a=1, b={b}, c={c}",
         f"Calculam delta = b² - 4ac = {b}² - 4·1·{c} = {b*b} - {4*c} = {delta}",
         f"sqrt(delta) = {int(delta**0.5)}",
         f"x1 = ({-b} - {int(delta**0.5)}) / 2 = {x1}",
         f"x2 = ({-b} + {int(delta**0.5)}) / 2 = {x2}"],
        "equation", "ecuatii gradul 2", 2, "BOTH")

# Ecuatii de gradul 2 cu a != 1
for a, x1, x2 in [(2,1,3), (2,2,5), (3,1,2), (2,1,4), (3,2,3), (2,3,4), (3,1,4), (2,2,3), (4,1,2), (3,1,5)]:
    b = -a * (x1 + x2)
    c = a * x1 * x2
    add(f"Rezolvati ecuatia: {a}x² {'+' if b>=0 else '-'} {abs(b)}x {'+' if c>=0 else '-'} {abs(c)} = 0",
        f"x1 = {x1}, x2 = {x2}",
        [f"a={a}, b={b}, c={c}",
         f"delta = {b}² - 4·{a}·{c} = {b*b} - {4*a*c} = {b*b - 4*a*c}",
         f"x1 = ({-b} - sqrt({b*b-4*a*c})) / (2·{a}) = {x1}",
         f"x2 = ({-b} + sqrt({b*b-4*a*c})) / (2·{a}) = {x2}"],
        "equation", "ecuatii gradul 2", 3, "BOTH")

# --- SISTEME DE ECUATII ---
systems = [
    (1,1,5, 1,-1,1, 3,2), (2,1,7, 1,3,8, 3,5/3),
    (1,2,8, 3,1,9, 2,3), (2,3,12, 1,1,5, 3,2),
    (3,2,13, 1,4,11, 3,2), (1,1,7, 2,3,16, 5,2),
    (4,1,9, 2,3,8, 2.5, 1/3), (1,3,10, 2,1,5, 1,3),
    (3,1,7, 1,2,8, 2,3), (5,2,11, 1,1,4, 3,1),
]
for a1,b1,c1,a2,b2,c2,x,y in systems:
    add(f"Rezolvati sistemul: {a1}x + {b1}y = {c1}, {a2}x + {b2}y = {c2}",
        f"x = {x}, y = {y}",
        [f"Din ecuatia 1: {a1}x + {b1}y = {c1}",
         f"Din ecuatia 2: {a2}x + {b2}y = {c2}",
         f"Folosim metoda substitutiei sau reducerii",
         f"x = {x}, y = {y}"],
        "equation", "sisteme ecuatii", 2, "BOTH")

# --- PUTERI SI RADICALI ---
for b, e in [(2,3), (2,4), (2,5), (3,2), (3,3), (3,4), (5,2), (5,3), (4,3), (7,2)]:
    add(f"Calculati: {b}^{e}", f"{b**e}",
        [f"Inmultim {b} de {e} ori", f"{b}^{e} = {b**e}"],
        "equation", "puteri", 1, "BOTH")

for n in [4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225]:
    r = int(n**0.5)
    add(f"Calculati: sqrt({n})", f"{r}",
        [f"Cautam numarul care ridicat la patrat da {n}", f"sqrt({n}) = {r} deoarece {r}² = {n}"],
        "equation", "radicali", 1, "BOTH")

# --- PROGRESII ARITMETICE ---
for a1, r in [(1,2), (3,4), (5,3), (2,5), (10,3), (1,7), (4,6), (7,2), (0,5), (3,8)]:
    a5 = a1 + 4*r
    s5 = 5 * (a1 + a5) // 2
    add(f"Fie progresia aritmetica cu a1 = {a1} si ratia r = {r}. Calculati a5 si S5.",
        f"a5 = {a5}, S5 = {s5}",
        [f"a5 = a1 + 4r = {a1} + 4·{r} = {a5}",
         f"S5 = 5·(a1 + a5)/2 = 5·({a1} + {a5})/2 = {s5}"],
        "sequence", "progresii aritmetice", 2, "BOTH")

# --- PROGRESII GEOMETRICE ---
for b1, q in [(1,2), (2,3), (3,2), (1,3), (2,2), (5,2), (1,4), (4,2), (3,3), (1,5)]:
    b4 = b1 * q**3
    s4 = b1 * (q**4 - 1) // (q - 1)
    add(f"Fie progresia geometrica cu b1 = {b1} si ratia q = {q}. Calculati b4 si S4.",
        f"b4 = {b4}, S4 = {s4}",
        [f"b4 = b1 · q³ = {b1} · {q}³ = {b4}",
         f"S4 = b1 · (q⁴ - 1)/(q - 1) = {b1} · ({q**4} - 1)/({q} - 1) = {s4}"],
        "sequence", "progresii geometrice", 2, "BOTH")

# ============================================================================
# SUBIECTUL II - ALGEBRA (M1, M2)
# ============================================================================

# --- MATRICE ---
for a,b,c,d in [(1,2,3,4), (2,1,1,3), (3,0,1,2), (1,1,2,1), (4,1,2,3),
                (2,3,1,4), (5,1,3,2), (1,4,2,3), (3,2,1,1), (2,2,3,1)]:
    det = a*d - b*c
    add(f"Calculati determinantul matricei A = ({a} {b} / {c} {d})",
        f"det(A) = {det}",
        [f"det(A) = {a}·{d} - {b}·{c}", f"det(A) = {a*d} - {b*c}", f"det(A) = {det}"],
        "matrix", "determinanti 2x2", 2, "M1")

# Matrice 3x3
mats_3x3 = [
    (1,0,2, 3,1,0, 0,2,1), (2,1,0, 1,3,2, 0,1,1),
    (1,2,3, 0,1,2, 1,0,1), (3,1,2, 0,2,1, 1,1,3),
    (1,1,1, 2,1,3, 1,2,1), (2,0,1, 1,1,0, 3,2,1),
    (1,3,0, 2,1,1, 0,2,3), (4,1,0, 2,3,1, 1,0,2),
    (1,2,1, 0,1,3, 2,1,0), (3,0,2, 1,1,1, 2,3,0),
]
for vals in mats_3x3:
    a,b,c,d,e,f,g,h,i = vals
    det = a*(e*i-f*h) - b*(d*i-f*g) + c*(d*h-e*g)
    add(f"Calculati determinantul matricei 3x3: ({a} {b} {c} / {d} {e} {f} / {g} {h} {i})",
        f"det = {det}",
        [f"Dezvoltam dupa prima linie (regula lui Sarrus)",
         f"det = {a}·({e}·{i}-{f}·{h}) - {b}·({d}·{i}-{f}·{g}) + {c}·({d}·{h}-{e}·{g})",
         f"det = {a}·{e*i-f*h} - {b}·{d*i-f*g} + {c}·{d*h-e*g}",
         f"det = {a*(e*i-f*h)} - {b*(d*i-f*g)} + {c*(d*h-e*g)}",
         f"det = {det}"],
        "matrix", "determinanti 3x3", 3, "M1")

# Inmultire matrice
for a,b,c,d,e,f,g,h in [(1,2,3,4,5,6,7,8), (2,1,0,3,1,2,3,1), (1,0,1,1,2,1,0,3),
                          (3,1,2,0,1,1,2,1), (1,3,2,1,0,2,1,3)]:
    r11, r12 = a*e+b*g, a*f+b*h
    r21, r22 = c*e+d*g, c*f+d*h
    add(f"Calculati produsul matricelor A = ({a} {b} / {c} {d}) si B = ({e} {f} / {g} {h})",
        f"A·B = ({r11} {r12} / {r21} {r22})",
        [f"(A·B)₁₁ = {a}·{e} + {b}·{g} = {r11}",
         f"(A·B)₁₂ = {a}·{f} + {b}·{h} = {r12}",
         f"(A·B)₂₁ = {c}·{e} + {d}·{g} = {r21}",
         f"(A·B)₂₂ = {c}·{f} + {d}·{h} = {r22}"],
        "matrix", "inmultire matrice", 2, "M1")

# Inversa matrice 2x2
for a,b,c,d in [(2,1,1,1), (3,1,2,1), (1,2,1,3), (4,1,3,1), (2,3,1,2),
                (3,2,1,1), (5,2,3,1), (1,1,2,3), (2,1,3,2), (4,3,2,1)]:
    det = a*d - b*c
    if det != 0:
        add(f"Calculati inversa matricei A = ({a} {b} / {c} {d})",
            f"A⁻¹ = (1/{det})·({d} {-b} / {-c} {a})",
            [f"det(A) = {a}·{d} - {b}·{c} = {det}",
             f"Matricea adjuncta: ({d} {-b} / {-c} {a})",
             f"A⁻¹ = (1/{det}) · adjuncta",
             f"A⁻¹ = ({d}/{det} {-b}/{det} / {-c}/{det} {a}/{det})"],
            "matrix", "inversa matrice", 3, "M1")

# Sisteme cu Cramer
for a1,b1,c1,a2,b2,c2 in [(2,1,5,1,3,8), (3,2,8,1,1,3), (1,1,4,2,3,9),
                            (4,1,9,1,2,7), (3,1,7,2,3,12)]:
    D = a1*b2 - a2*b1
    Dx = c1*b2 - c2*b1
    Dy = a1*c2 - a2*c1
    if D != 0:
        add(f"Rezolvati sistemul prin metoda lui Cramer: {a1}x + {b1}y = {c1}, {a2}x + {b2}y = {c2}",
            f"x = {Dx//D if Dx%D==0 else Dx/D}, y = {Dy//D if Dy%D==0 else Dy/D}",
            [f"D = {a1}·{b2} - {a2}·{b1} = {D}",
             f"Dx = {c1}·{b2} - {c2}·{b1} = {Dx}",
             f"Dy = {a1}·{c2} - {a2}·{c1} = {Dy}",
             f"x = Dx/D = {Dx}/{D} = {Dx/D}",
             f"y = Dy/D = {Dy}/{D} = {Dy/D}"],
            "matrix", "metoda Cramer", 3, "M1")

# ============================================================================
# SUBIECTUL II - ANALIZA (M1)
# ============================================================================

# --- DERIVATE ---
derivate = [
    ("x²", "2x", ["Aplicam (xⁿ)' = n·xⁿ⁻¹", "(x²)' = 2x"]),
    ("x³", "3x²", ["(x³)' = 3x²"]),
    ("x⁴", "4x³", ["(x⁴)' = 4x³"]),
    ("3x²", "6x", ["(3x²)' = 3·2x = 6x"]),
    ("5x³", "15x²", ["(5x³)' = 5·3x² = 15x²"]),
    ("x² + 3x", "2x + 3", ["(x²)' = 2x", "(3x)' = 3", "f'(x) = 2x + 3"]),
    ("x³ - 2x²", "3x² - 4x", ["(x³)' = 3x²", "(-2x²)' = -4x", "f'(x) = 3x² - 4x"]),
    ("x³ + x² - 4x + 1", "3x² + 2x - 4", ["(x³)' = 3x²", "(x²)' = 2x", "(-4x)' = -4", "(1)' = 0"]),
    ("2x³ - 3x² + x - 5", "6x² - 6x + 1", ["(2x³)' = 6x²", "(-3x²)' = -6x", "(x)' = 1", "(-5)' = 0"]),
    ("x⁴ - 2x³ + x", "4x³ - 6x² + 1", ["(x⁴)' = 4x³", "(-2x³)' = -6x²", "(x)' = 1"]),
    ("sin(x)", "cos(x)", ["Derivata lui sin(x) = cos(x)"]),
    ("cos(x)", "-sin(x)", ["Derivata lui cos(x) = -sin(x)"]),
    ("e^x", "e^x", ["Derivata lui e^x = e^x"]),
    ("ln(x)", "1/x", ["Derivata lui ln(x) = 1/x"]),
    ("x·e^x", "e^x + x·e^x", ["Aplicam regula produsului: (fg)' = f'g + fg'", "f=x, g=e^x", "f'=1, g'=e^x", "(x·e^x)' = 1·e^x + x·e^x = e^x(1+x)"]),
    ("x²·sin(x)", "2x·sin(x) + x²·cos(x)", ["(fg)' = f'g + fg'", "f=x², g=sin(x)", "(x²·sin(x))' = 2x·sin(x) + x²·cos(x)"]),
    ("x·ln(x)", "ln(x) + 1", ["(x·ln(x))' = 1·ln(x) + x·(1/x) = ln(x) + 1"]),
    ("e^(2x)", "2e^(2x)", ["Aplicam regula lantului", "(e^u)' = u'·e^u cu u=2x", "(e^(2x))' = 2·e^(2x)"]),
    ("ln(x²+1)", "2x/(x²+1)", ["(ln(u))' = u'/u cu u=x²+1", "u' = 2x", "(ln(x²+1))' = 2x/(x²+1)"]),
    ("sin(2x)", "2cos(2x)", ["(sin(u))' = u'·cos(u) cu u=2x", "(sin(2x))' = 2·cos(2x)"]),
    ("(x²+1)³", "6x(x²+1)²", ["(uⁿ)' = n·uⁿ⁻¹·u' cu u=x²+1", "((x²+1)³)' = 3(x²+1)²·2x = 6x(x²+1)²"]),
    ("x/(x+1)", "1/(x+1)²", ["Aplicam regula catului: (f/g)' = (f'g - fg')/g²", "f=x, g=x+1", "(x/(x+1))' = (1·(x+1) - x·1)/(x+1)² = 1/(x+1)²"]),
    ("(2x+1)/(x-1)", "-3/(x-1)²", ["(f/g)' = (f'g - fg')/g²", "((2x+1)/(x-1))' = (2(x-1) - (2x+1)·1)/(x-1)²", "= (2x-2-2x-1)/(x-1)² = -3/(x-1)²"]),
    ("sqrt(x)", "1/(2·sqrt(x))", ["sqrt(x) = x^(1/2)", "(x^(1/2))' = (1/2)·x^(-1/2) = 1/(2·sqrt(x))"]),
    ("sqrt(x²+1)", "x/sqrt(x²+1)", ["(u^(1/2))' = u'/(2·sqrt(u))", "((x²+1)^(1/2))' = 2x/(2·sqrt(x²+1)) = x/sqrt(x²+1)"]),
]
for func, deriv, steps in derivate:
    add(f"Calculati derivata functiei f(x) = {func}", f"f'(x) = {deriv}", steps,
        "derivative", "derivate", 2 if "·" not in func else 3, "M1")

# Derivate - puncte critice si monotonie
for func, deriv, critice, monotonie in [
    ("x³ - 3x", "3x² - 3", "x = -1, x = 1", "crescatoare pe (-inf,-1)U(1,inf), descrescatoare pe (-1,1)"),
    ("x³ - 12x", "3x² - 12", "x = -2, x = 2", "crescatoare pe (-inf,-2)U(2,inf), descrescatoare pe (-2,2)"),
    ("x² - 4x + 3", "2x - 4", "x = 2", "descrescatoare pe (-inf,2), crescatoare pe (2,inf)"),
    ("-x² + 6x - 5", "-2x + 6", "x = 3", "crescatoare pe (-inf,3), descrescatoare pe (3,inf)"),
    ("x³/3 - x²/2 - 2x", "x² - x - 2", "x = -1, x = 2", "cresc. pe (-inf,-1)U(2,inf), desc. pe (-1,2)"),
]:
    add(f"Studiati monotonia functiei f(x) = {func}",
        f"Puncte critice: {critice}. {monotonie}",
        [f"Calculam f'(x) = {deriv}",
         f"Rezolvam f'(x) = 0: {deriv} = 0",
         f"Puncte critice: {critice}",
         f"Studiem semnul derivatei",
         f"Monotonia: {monotonie}"],
        "derivative", "monotonie", 3, "M1")

# --- LIMITE ---
limite = [
    ("lim(x->inf) (2x+1)/(x+3)", "2", ["Impartim la x", "lim (2+1/x)/(1+3/x) = 2/1 = 2"]),
    ("lim(x->inf) (3x²+1)/(x²-2)", "3", ["Impartim la x²", "lim (3+1/x²)/(1-2/x²) = 3"]),
    ("lim(x->inf) (x²+x)/(2x²+1)", "1/2", ["Impartim la x²", "lim (1+1/x)/(2+1/x²) = 1/2"]),
    ("lim(x->0) sin(x)/x", "1", ["Limita remarcabila: lim sin(x)/x = 1 cand x->0"]),
    ("lim(x->0) (e^x-1)/x", "1", ["Limita remarcabila: lim (e^x-1)/x = 1 cand x->0"]),
    ("lim(x->0) ln(1+x)/x", "1", ["Limita remarcabila: lim ln(1+x)/x = 1 cand x->0"]),
    ("lim(x->inf) (1+1/x)^x", "e", ["Limita remarcabila: lim (1+1/n)^n = e"]),
    ("lim(x->1) (x²-1)/(x-1)", "2", ["Factorizam: (x²-1) = (x-1)(x+1)", "Simplificam cu (x-1)", "lim(x->1) (x+1) = 2"]),
    ("lim(x->2) (x²-4)/(x-2)", "4", ["(x²-4) = (x-2)(x+2)", "Simplificam", "lim(x->2) (x+2) = 4"]),
    ("lim(x->3) (x²-9)/(x-3)", "6", ["(x²-9) = (x-3)(x+3)", "Simplificam", "lim(x->3) (x+3) = 6"]),
    ("lim(x->0) sin(3x)/x", "3", ["sin(3x)/x = 3·sin(3x)/(3x)", "lim sin(3x)/(3x) = 1", "Rezultat: 3"]),
    ("lim(x->0) (1-cos(x))/x²", "1/2", ["Limita remarcabila: lim (1-cos(x))/x² = 1/2"]),
    ("lim(x->inf) x·sin(1/x)", "1", ["Substitutie t=1/x, t->0", "lim sin(t)/t = 1"]),
    ("lim(x->0) tg(x)/x", "1", ["tg(x)/x = sin(x)/(x·cos(x))", "lim sin(x)/x = 1, cos(0) = 1", "Rezultat: 1"]),
    ("lim(x->inf) (x+1)/(x-1)", "1", ["Impartim la x: (1+1/x)/(1-1/x) = 1"]),
    ("lim(x->0) (e^(2x)-1)/x", "2", ["(e^(2x)-1)/x = 2·(e^(2x)-1)/(2x)", "lim = 2·1 = 2"]),
    ("lim(x->0) (3^x-1)/x", "ln(3)", ["Limita remarcabila: lim (a^x-1)/x = ln(a)", "Rezultat: ln(3)"]),
    ("lim(x->inf) ln(x)/x", "0", ["Aplicam L'Hopital: (1/x)/1 = 1/x -> 0"]),
    ("lim(x->inf) x/e^x", "0", ["Aplicam L'Hopital: 1/e^x -> 0"]),
    ("lim(x->1) (x³-1)/(x-1)", "3", ["x³-1 = (x-1)(x²+x+1)", "Simplificam", "lim(x->1) x²+x+1 = 3"]),
]
for expr, ans, steps in limite:
    add(expr, ans, steps, "limit", "limite", 2, "M1")

# --- INTEGRALE ---
integrale = [
    ("∫ x dx", "x²/2 + C", ["Aplicam formula: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C", "∫x dx = x²/2 + C"]),
    ("∫ x² dx", "x³/3 + C", ["∫x² dx = x³/3 + C"]),
    ("∫ x³ dx", "x⁴/4 + C", ["∫x³ dx = x⁴/4 + C"]),
    ("∫ 3x² dx", "x³ + C", ["∫3x² dx = 3·x³/3 = x³ + C"]),
    ("∫ (2x + 1) dx", "x² + x + C", ["∫2x dx = x²", "∫1 dx = x", "Rezultat: x² + x + C"]),
    ("∫ (x² + 2x + 1) dx", "x³/3 + x² + x + C", ["Integram termen cu termen"]),
    ("∫ e^x dx", "e^x + C", ["∫e^x dx = e^x + C"]),
    ("∫ 1/x dx", "ln|x| + C", ["∫1/x dx = ln|x| + C"]),
    ("∫ sin(x) dx", "-cos(x) + C", ["∫sin(x) dx = -cos(x) + C"]),
    ("∫ cos(x) dx", "sin(x) + C", ["∫cos(x) dx = sin(x) + C"]),
    ("∫ e^(2x) dx", "e^(2x)/2 + C", ["Substitutie u=2x, du=2dx", "∫e^u · du/2 = e^u/2 + C"]),
    ("∫ 1/(x²+1) dx", "arctg(x) + C", ["Formula: ∫1/(x²+1) dx = arctg(x) + C"]),
    ("∫ 1/sqrt(1-x²) dx", "arcsin(x) + C", ["Formula: ∫1/sqrt(1-x²) dx = arcsin(x) + C"]),
    ("∫₀¹ x² dx", "1/3", ["∫₀¹ x² dx = [x³/3]₀¹ = 1/3 - 0 = 1/3"]),
    ("∫₀¹ (2x + 1) dx", "2", ["∫₀¹ (2x+1) dx = [x²+x]₀¹ = (1+1) - 0 = 2"]),
    ("∫₁² 1/x dx", "ln(2)", ["∫₁² 1/x dx = [ln|x|]₁² = ln(2) - ln(1) = ln(2)"]),
    ("∫₀^π sin(x) dx", "2", ["∫₀^π sin(x) dx = [-cos(x)]₀^π = -cos(π)+cos(0) = 1+1 = 2"]),
    ("∫₀¹ e^x dx", "e - 1", ["∫₀¹ e^x dx = [e^x]₀¹ = e¹ - e⁰ = e - 1"]),
    ("∫ (3x² - 2x + 5) dx", "x³ - x² + 5x + C", ["Integram termen cu termen"]),
    ("∫₁³ x dx", "4", ["∫₁³ x dx = [x²/2]₁³ = 9/2 - 1/2 = 4"]),
]
for expr, ans, steps in integrale:
    add(expr, ans, steps, "integral", "integrale", 3, "M1")

# --- FUNCTII - studiu complet ---
for func, dom, deriv, crit, mono, conv in [
    ("x² - 4x + 3", "R", "2x - 4", "x=2 (minim)", "desc. pe (-inf,2), cresc. pe (2,inf)", "convexa pe R"),
    ("-x² + 2x + 3", "R", "-2x + 2", "x=1 (maxim)", "cresc. pe (-inf,1), desc. pe (1,inf)", "concava pe R"),
    ("x³ - 3x", "R", "3x² - 3", "x=-1(max local), x=1(min local)", "cresc(-inf,-1)U(1,inf), desc(-1,1)", "concava(-inf,0), convexa(0,inf)"),
    ("x³ - 6x² + 9x", "R", "3x² - 12x + 9", "x=1(max), x=3(min)", "cresc(-inf,1)U(3,inf), desc(1,3)", "inflexiune in x=2"),
    ("e^x - x", "R", "e^x - 1", "x=0 (minim)", "desc(-inf,0), cresc(0,inf)", "convexa pe R"),
]:
    add(f"Realizati studiul complet al functiei f(x) = {func}",
        f"Domeniu: {dom}, f'(x)={deriv}, Puncte critice: {crit}, Monotonie: {mono}",
        [f"Domeniu: {dom}", f"f'(x) = {deriv}", f"f'(x) = 0 => {crit}", f"Monotonie: {mono}", f"Convexitate: {conv}"],
        "function", "studiu functie", 4, "M1")

# ============================================================================
# COMBINATORICA SI PROBABILITATI
# ============================================================================

# Combinari
for n, k in [(5,2), (6,2), (7,3), (8,2), (8,3), (9,2), (9,3), (10,2), (10,3), (10,4),
             (12,3), (15,2), (6,3), (7,2), (20,2)]:
    def comb(n, k):
        if k > n: return 0
        r = 1
        for i in range(k):
            r = r * (n - i) // (i + 1)
        return r
    c = comb(n, k)
    add(f"Calculati C({n},{k})", f"C({n},{k}) = {c}",
        [f"C({n},{k}) = {n}! / ({k}! · {n-k}!)", f"C({n},{k}) = {c}"],
        "combinatorics", "combinari", 2, "BOTH")

# Aranjamente
for n, k in [(5,2), (6,2), (7,3), (8,2), (9,3), (10,2), (4,3), (6,3), (5,3), (8,3)]:
    def aranj(n, k):
        r = 1
        for i in range(k):
            r *= (n - i)
        return r
    a = aranj(n, k)
    add(f"Calculati A({n},{k})", f"A({n},{k}) = {a}",
        [f"A({n},{k}) = {n}! / ({n-k})!", f"A({n},{k}) = {'·'.join(str(n-i) for i in range(k))}", f"A({n},{k}) = {a}"],
        "combinatorics", "aranjamente", 2, "BOTH")

# Permutari
for n in [3, 4, 5, 6, 7, 8]:
    p = 1
    for i in range(1, n+1):
        p *= i
    add(f"Calculati P({n})", f"P({n}) = {p}",
        [f"P({n}) = {n}!", f"P({n}) = {'·'.join(str(i) for i in range(1,n+1))}", f"P({n}) = {p}"],
        "combinatorics", "permutari", 1, "BOTH")

# Probabilitati
probabilitati = [
    ("Se arunca un zar. Care e probabilitatea sa cada un numar par?", "1/2",
     ["Numere pare: {2, 4, 6} = 3 cazuri favorabile", "Total cazuri: 6", "P = 3/6 = 1/2"]),
    ("Se arunca doua zaruri. Care e probabilitatea ca suma sa fie 7?", "1/6",
     ["Cazuri favorabile: (1,6)(2,5)(3,4)(4,3)(5,2)(6,1) = 6", "Total: 36", "P = 6/36 = 1/6"]),
    ("Dintr-o urna cu 5 bile albe si 3 negre se extrage una. P(alba)?", "5/8",
     ["Bile albe: 5", "Total bile: 8", "P = 5/8"]),
    ("Se arunca o moneda de 3 ori. P(exact 2 steme)?", "3/8",
     ["Total cazuri: 2³ = 8", "Cazuri favorabile: C(3,2) = 3", "P = 3/8"]),
    ("Dintr-un lot de 10 produse, 3 sunt defecte. Se extrag 2. P(ambele bune)?", "7/15",
     ["Produse bune: 7", "C(7,2) = 21 moduri de a alege 2 bune", "C(10,2) = 45 total", "P = 21/45 = 7/15"]),
    ("Se arunca 2 zaruri. P(suma > 10)?", "1/12",
     ["Cazuri: (5,6)(6,5)(6,6) = 3", "Total: 36", "P = 3/36 = 1/12"]),
    ("Dintr-un pachet de 52 carti se extrage una. P(as)?", "1/13",
     ["Asi: 4", "Total: 52", "P = 4/52 = 1/13"]),
    ("Se arunca 3 zaruri. P(toate egale)?", "1/36",
     ["Cazuri favorabile: (1,1,1)(2,2,2)...(6,6,6) = 6", "Total: 216", "P = 6/216 = 1/36"]),
    ("Din 20 elevi, 12 sunt fete. Se aleg 3. P(toate fete)?", "44/228",
     ["C(12,3) = 220", "C(20,3) = 1140", "P = 220/1140 = 44/228"]),
    ("Se extrag 2 bile din 4 rosii si 6 albastre. P(culori diferite)?", "8/15",
     ["C(4,1)·C(6,1) = 24 cazuri", "C(10,2) = 45 total", "P = 24/45 = 8/15"]),
]
for q, a, s in probabilitati:
    add(q, a, s, "probability", "probabilitati", 2, "BOTH")

# ============================================================================
# GEOMETRIE
# ============================================================================

# Vectori
vectori = [
    ("Calculati produsul scalar a·b daca a=(1,2) si b=(3,4)", "11",
     ["a·b = 1·3 + 2·4 = 3 + 8 = 11"]),
    ("Calculati |v| daca v = (3, 4)", "5",
     ["|v| = sqrt(3² + 4²) = sqrt(9 + 16) = sqrt(25) = 5"]),
    ("Calculati |v| daca v = (5, 12)", "13",
     ["|v| = sqrt(25 + 144) = sqrt(169) = 13"]),
    ("Determinati daca vectorii a=(2,3) si b=(4,6) sunt coliniari", "Da, sunt coliniari",
     ["Verificam: 2·6 - 3·4 = 12 - 12 = 0", "Deoarece produsul vectorial e 0, sunt coliniari"]),
    ("Calculati unghiul dintre a=(1,0) si b=(0,1)", "90°",
     ["cos(α) = a·b/(|a|·|b|) = 0/(1·1) = 0", "α = arccos(0) = 90°"]),
]
for q, a, s in vectori:
    add(q, a, s, "vector", "vectori", 2, "M1")

# Geometrie analitica
geo = [
    ("Determinati ecuatia dreptei prin A(1,2) si B(3,6)", "y = 2x",
     ["Panta: m = (6-2)/(3-1) = 4/2 = 2", "y - 2 = 2(x - 1)", "y = 2x"]),
    ("Calculati distanta dintre A(1,2) si B(4,6)", "5",
     ["d = sqrt((4-1)² + (6-2)²) = sqrt(9 + 16) = sqrt(25) = 5"]),
    ("Determinati ecuatia cercului cu centrul C(0,0) si raza r=5", "x² + y² = 25",
     ["Ecuatia: (x-a)² + (y-b)² = r²", "Cu C(0,0) si r=5: x² + y² = 25"]),
    ("Calculati aria triunghiului cu varfurile A(0,0), B(4,0), C(0,3)", "6",
     ["Aria = |x_A(y_B-y_C) + x_B(y_C-y_A) + x_C(y_A-y_B)| / 2", "= |0+12+0| / 2 = 6"]),
    ("Determinati mijlocul segmentului AB cu A(2,4) si B(6,8)", "M(4, 6)",
     ["M = ((x_A+x_B)/2, (y_A+y_B)/2)", "M = ((2+6)/2, (4+8)/2) = (4, 6)"]),
    ("Ecuatia dreptei prin A(0,3) cu panta m=2", "y = 2x + 3",
     ["y - y_A = m(x - x_A)", "y - 3 = 2(x - 0)", "y = 2x + 3"]),
    ("Distanta de la P(3,4) la dreapta 3x + 4y - 5 = 0", "4",
     ["d = |3·3 + 4·4 - 5| / sqrt(9+16)", "d = |9+16-5| / 5 = 20/5 = 4"]),
    ("Sunt perpendiculare dreptele y=2x+1 si y=-x/2+3?", "Da",
     ["m1 = 2, m2 = -1/2", "m1·m2 = 2·(-1/2) = -1", "Daca m1·m2 = -1, dreptele sunt perpendiculare"]),
    ("Ecuatia tangentei la f(x)=x² in punctul x=1", "y = 2x - 1",
     ["f(1) = 1", "f'(x) = 2x, f'(1) = 2", "y - 1 = 2(x - 1)", "y = 2x - 1"]),
    ("Aria paralelogramului cu laturile pe vectorii a=(3,0) si b=(0,4)", "12",
     ["Aria = |a x b| = |3·4 - 0·0| = 12"]),
]
for q, a, s in geo:
    add(q, a, s, "geometry", "geometrie analitica", 2, "M1")

# ============================================================================
# TRIGONOMETRIE
# ============================================================================

trig = [
    ("Calculati sin(30°)", "1/2", ["sin(30°) = 1/2 (valoare remarcabila)"]),
    ("Calculati cos(60°)", "1/2", ["cos(60°) = 1/2 (valoare remarcabila)"]),
    ("Calculati tg(45°)", "1", ["tg(45°) = sin(45°)/cos(45°) = 1"]),
    ("Calculati sin(60°)", "√3/2", ["sin(60°) = √3/2"]),
    ("Calculati cos(30°)", "√3/2", ["cos(30°) = √3/2"]),
    ("Calculati sin²(30°) + cos²(30°)", "1", ["sin²(30°) + cos²(30°) = 1/4 + 3/4 = 1 (identitate fundamentala)"]),
    ("Rezolvati sin(x) = 1/2, x in [0, 2π]", "x = π/6 sau x = 5π/6",
     ["sin(x) = 1/2", "x = π/6 (cadranul I)", "x = π - π/6 = 5π/6 (cadranul II)"]),
    ("Rezolvati cos(x) = 0, x in [0, 2π]", "x = π/2 sau x = 3π/2",
     ["cos(x) = 0", "x = π/2 sau x = 3π/2"]),
    ("Calculati sin(2·30°) folosind formula dublului unghi", "√3/2",
     ["sin(2α) = 2·sin(α)·cos(α)", "sin(60°) = 2·sin(30°)·cos(30°) = 2·(1/2)·(√3/2) = √3/2"]),
    ("In triunghiul ABC cu a=3, b=4, C=90°, calculati c", "5",
     ["Teorema lui Pitagora: c² = a² + b²", "c² = 9 + 16 = 25", "c = 5"]),
    ("In triunghiul cu a=6, b=8, c=10, verificati daca e dreptunghic", "Da",
     ["Verificam: a² + b² = c²?", "36 + 64 = 100", "100 = 100 ✓ Este dreptunghic"]),
    ("Calculati aria triunghiului cu a=5, b=7, unghi C=30°", "35/4",
     ["S = (1/2)·a·b·sin(C)", "S = (1/2)·5·7·sin(30°)", "S = (1/2)·5·7·(1/2) = 35/4"]),
    ("Rezolvati 2sin²(x) - 1 = 0", "x = π/4 + kπ/2",
     ["sin²(x) = 1/2", "sin(x) = ±√2/2", "x = π/4 + kπ/2, k intreg"]),
    ("Calculati tg(30°)", "√3/3",
     ["tg(30°) = sin(30°)/cos(30°) = (1/2)/(√3/2) = 1/√3 = √3/3"]),
    ("Verificati: sin²(x) + cos²(x) = 1", "Identitate adevarata",
     ["Aceasta este identitatea fundamentala a trigonometriei", "Este adevarata pentru orice x real"]),
]
for q, a, s in trig:
    add(q, a, s, "trigonometry", "trigonometrie", 2, "BOTH")

# ============================================================================
# NUMERE COMPLEXE (M1)
# ============================================================================

complexe = [
    ("Calculati (2+3i) + (1-i)", "3 + 2i", ["(2+1) + (3-1)i = 3 + 2i"]),
    ("Calculati (3+2i) - (1+4i)", "2 - 2i", ["(3-1) + (2-4)i = 2 - 2i"]),
    ("Calculati (2+i)(3-i)", "7 + i", ["6 - 2i + 3i - i² = 6 + i + 1 = 7 + i"]),
    ("Calculati |3 + 4i|", "5", ["|z| = sqrt(3² + 4²) = sqrt(25) = 5"]),
    ("Calculati conjugatul lui z = 2 - 3i", "2 + 3i", ["Conjugatul: schimbam semnul partii imaginare", "z̄ = 2 + 3i"]),
    ("Calculati i²", "-1", ["i² = -1 (definitia unitatii imaginare)"]),
    ("Calculati i⁴", "1", ["i² = -1", "i⁴ = (i²)² = (-1)² = 1"]),
    ("Calculati (1+i)²", "2i", ["(1+i)² = 1 + 2i + i² = 1 + 2i - 1 = 2i"]),
    ("Rezolvati z² = -4", "z = ±2i", ["z² = -4", "z = ±√(-4) = ±2i"]),
    ("Calculati (2+i)/(1-i)", "1/2 + 3/2·i",
     ["Inmultim cu conjugatul numitorului", "(2+i)(1+i)/((1-i)(1+i))", "= (2+2i+i+i²)/(1-i²)", "= (1+3i)/2"]),
]
for q, a, s in complexe:
    add(q, a, s, "complex_number", "numere complexe", 2, "M1")

# ============================================================================
# PROFIL M3 (TEHNOLOGIC) - exercitii specifice
# ============================================================================

# Ecuatii si inecuatii simple
for a, b in [(2,8), (3,12), (4,20), (5,15), (6,24), (7,28), (8,32), (9,36), (10,40), (3,21)]:
    add(f"Rezolvati ecuatia: {a}x = {b}", f"x = {b//a}",
        [f"x = {b}/{a} = {b//a}"], "equation", "ecuatii simple", 1, "M3")

# Functii de gradul I si II - grafice
for a, b in [(1,2), (2,1), (3,-1), (-1,3), (2,4), (-2,1), (1,-3), (3,2), (4,-2), (-3,4)]:
    add(f"Reprezentati grafic functia f(x) = {a}x + {b}",
        f"Dreapta cu panta {a} si ordonata la origine {b}",
        [f"f(0) = {b} (punctul (0,{b}))",
         f"f(x) = 0 cand x = {-b/a:.1f} (punctul ({-b/a:.1f}, 0))",
         f"Unim cele 2 puncte => dreapta cu panta {a}"],
        "function", "functii gradul 1", 1, "M3")

# Procente si proportii
procente = [
    ("Din 200 de elevi, 30% sunt baietii. Cati baieti sunt?", "60",
     ["30% din 200 = 30/100 · 200 = 60"]),
    ("Un produs costa 150 lei. Dupa reducere de 20%, cat costa?", "120 lei",
     ["Reducerea: 20% din 150 = 30 lei", "Pret final: 150 - 30 = 120 lei"]),
    ("Un produs s-a scumpit de la 80 la 100 lei. Cu cat % s-a scumpit?", "25%",
     ["Cresterea: 100 - 80 = 20 lei", "Procentul: 20/80 · 100 = 25%"]),
    ("30 este 60% din ce numar?", "50",
     ["30 = 60/100 · x", "x = 30 · 100/60 = 50"]),
    ("Media aritmetica a numerelor 4, 7, 9, 12 este:", "8",
     ["Media = (4+7+9+12)/4 = 32/4 = 8"]),
]
for q, a, s in procente:
    add(q, a, s, "equation", "procente", 1, "M3")

# Statistice simple
for vals_str, vals in [("2,4,6,8,10", [2,4,6,8,10]), ("1,3,5,7,9", [1,3,5,7,9]),
                        ("10,20,30,40,50", [10,20,30,40,50]), ("3,3,5,7,7", [3,3,5,7,7])]:
    media = sum(vals) / len(vals)
    add(f"Calculati media aritmetica a numerelor: {vals_str}", f"{media}",
        [f"Media = ({'+'.join(map(str,vals))}) / {len(vals)}", f"Media = {sum(vals)}/{len(vals)} = {media}"],
        "equation", "statistica", 1, "M3")

# ============================================================================
# PROFIL M4 (PEDAGOGIC) - exercitii specifice
# ============================================================================

# Logica matematica
logica = [
    ("Determinati valoarea de adevar: 'Daca 2+2=4 atunci 3+3=6'", "Adevarat",
     ["P: 2+2=4 (Adevarat)", "Q: 3+3=6 (Adevarat)", "P => Q: A => A = Adevarat"]),
    ("Negati propozitia: 'Toti elevii invata matematica'", "Exista un elev care nu invata matematica",
     ["Negatia lui 'pentru orice' este 'exista'", "¬(∀x P(x)) = ∃x ¬P(x)"]),
    ("Determinati A ∩ B daca A={1,2,3,4} si B={3,4,5,6}", "{3, 4}",
     ["Intersectia contine elementele comune", "A ∩ B = {3, 4}"]),
    ("Determinati A ∪ B daca A={1,2,3} si B={2,3,4}", "{1, 2, 3, 4}",
     ["Reuniunea contine toate elementele", "A ∪ B = {1, 2, 3, 4}"]),
    ("Calculati card(A × B) daca A={1,2} si B={a,b,c}", "6",
     ["card(A) = 2, card(B) = 3", "card(A × B) = 2 · 3 = 6"]),
]
for q, a, s in logica:
    add(q, a, s, "equation", "logica", 2, "M4")

# Multimi si relatii
multimi = [
    ("Determinati A \\ B daca A={1,2,3,4,5} si B={2,4}", "{1, 3, 5}",
     ["A \\ B contine elementele din A care nu sunt in B", "A \\ B = {1, 3, 5}"]),
    ("Cate submultimi are multimea {a, b, c}?", "8",
     ["Nr submultimi = 2^n = 2³ = 8"]),
    ("Cate submultimi are multimea {1, 2, 3, 4}?", "16",
     ["Nr submultimi = 2^4 = 16"]),
    ("Este functia f: {1,2,3} -> {a,b}, f(1)=a, f(2)=b, f(3)=a surjectiva?", "Da",
     ["Verificam: fiecare element din codomeniu are preimaginea", "a are preimaginile 1 si 3", "b are preimaginea 2", "Da, e surjectiva"]),
]
for q, a, s in multimi:
    add(q, a, s, "equation", "multimi", 2, "M4")

# ============================================================================
# ECUATII/INECUATII DIVERSE (M2 - Stiinte)
# ============================================================================

m2_exercises = [
    ("Rezolvati inecuatia: 2x - 3 > 5", "x > 4",
     ["2x > 5 + 3", "2x > 8", "x > 4"]),
    ("Rezolvati inecuatia: x² - 4 < 0", "-2 < x < 2",
     ["x² < 4", "-2 < x < 2"]),
    ("Rezolvati: |x - 3| = 5", "x = 8 sau x = -2",
     ["x - 3 = 5 => x = 8", "x - 3 = -5 => x = -2"]),
    ("Rezolvati: |2x + 1| < 3", "-2 < x < 1",
     ["-3 < 2x + 1 < 3", "-4 < 2x < 2", "-2 < x < 1"]),
    ("Determinati semnul expresiei x² - 5x + 6", "Pozitiva pe (-inf,2)U(3,inf), negativa pe (2,3)",
     ["x² - 5x + 6 = (x-2)(x-3)", "Radacini: x=2, x=3", "Pozitiva in afara radacinilor"]),
    ("Rezolvati ecuatia: sqrt(x+3) = 5", "x = 22",
     ["Ridicam la patrat: x + 3 = 25", "x = 22", "Verificare: sqrt(25) = 5 ✓"]),
    ("Rezolvati: log₂(x) = 3", "x = 8",
     ["log₂(x) = 3 inseamna 2³ = x", "x = 8"]),
    ("Rezolvati: 3^x = 27", "x = 3",
     ["27 = 3³", "3^x = 3³", "x = 3"]),
    ("Rezolvati: 2^(x+1) = 16", "x = 3",
     ["16 = 2⁴", "2^(x+1) = 2⁴", "x + 1 = 4", "x = 3"]),
    ("Simplificati: log₃(9) + log₃(3)", "3",
     ["log₃(9) = 2 (deoarece 3² = 9)", "log₃(3) = 1", "2 + 1 = 3"]),
]
for q, a, s in m2_exercises:
    add(q, a, s, "equation", "ecuatii diverse", 2, "M2")

# Functii exponential si logaritmice (M2)
for base, exp_val in [(2, "2x"), (3, "x+1"), (2, "x²")]:
    add(f"Determinati domeniul functiei f(x) = {base}^({exp_val})", "R",
     [f"Functia exponentiala este definita pe R", f"Domeniul: R"],
     "function", "functii exponentiale", 2, "M2")

log_func = [
    ("Determinati domeniul functiei f(x) = ln(x-2)", "x > 2, adica (2, +inf)",
     ["Conditia: x - 2 > 0", "x > 2", "D = (2, +inf)"]),
    ("Determinati domeniul functiei f(x) = log₂(x²-1)", "x in (-inf,-1) U (1,+inf)",
     ["Conditia: x² - 1 > 0", "(x-1)(x+1) > 0", "x < -1 sau x > 1"]),
    ("Calculati f(e) daca f(x) = ln(x)", "1",
     ["f(e) = ln(e) = 1"]),
]
for q, a, s in log_func:
    add(q, a, s, "function", "functii logaritmice", 2, "M2")

# ============================================================================
# EXERCITII BAC TIP GRILA (toate profilele)
# ============================================================================

grila = [
    ("Suma solutiilor ecuatiei x² - 7x + 12 = 0 este:", "7",
     ["Vieta: x1 + x2 = -b/a = 7", "sau: x² - 7x + 12 = (x-3)(x-4), x1=3, x2=4, suma=7"], "M1"),
    ("Produsul solutiilor ecuatiei x² - 5x + 6 = 0 este:", "6",
     ["Vieta: x1 · x2 = c/a = 6"], "M1"),
    ("Numarul de submultimi ale multimii {1,2,3,4,5} este:", "32",
     ["2^5 = 32"], "BOTH"),
    ("Daca f(x) = 2x + 3, atunci f(2) =", "7",
     ["f(2) = 2·2 + 3 = 7"], "BOTH"),
    ("Daca f(x) = x² - 1, atunci f(-3) =", "8",
     ["f(-3) = (-3)² - 1 = 9 - 1 = 8"], "BOTH"),
    ("Restul impartirii lui 17 la 5 este:", "2",
     ["17 = 5·3 + 2, deci restul = 2"], "M3"),
    ("Cmmdc(12, 18) =", "6",
     ["12 = 2²·3, 18 = 2·3²", "cmmdc = 2·3 = 6"], "BOTH"),
    ("Cmmmc(4, 6) =", "12",
     ["4 = 2², 6 = 2·3", "cmmmc = 2²·3 = 12"], "BOTH"),
    ("Valoarea expresiei 2³ + 3² este:", "17",
     ["2³ = 8, 3² = 9", "8 + 9 = 17"], "BOTH"),
    ("sqrt(48) simplificat este:", "4√3",
     ["48 = 16·3", "sqrt(48) = sqrt(16)·sqrt(3) = 4√3"], "BOTH"),
]
for q, a, s, prof in grila:
    add(q, a, s, "equation", "grila BAC", 1, prof)


# ============================================================================
# SAVE
# ============================================================================

# Merge with existing
data_path = Path(__file__).parent.parent / "data" / "processed" / "exercises_merged.json"
existing = []
if data_path.exists():
    with open(data_path, "r", encoding="utf-8") as f:
        existing = json.load(f)

# Avoid duplicate questions
existing_questions = {e.get("question", "") for e in existing}
new_exercises = [e for e in exercises if e["question"] not in existing_questions]

merged = existing + new_exercises

with open(data_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"Exercitii existente: {len(existing)}")
print(f"Exercitii noi generate: {len(new_exercises)}")
print(f"Total dupa merge: {len(merged)}")

# Stats
profiles = {}
types = {}
for e in merged:
    p = e.get("profile", "?")
    t = e.get("type", e.get("exercise_type", "?"))
    profiles[p] = profiles.get(p, 0) + 1
    types[t] = types.get(t, 0) + 1

print("\nPe profile:")
for p, c in sorted(profiles.items()):
    print(f"  {p}: {c}")

print("\nPe tipuri:")
for t, c in sorted(types.items(), key=lambda x: -x[1]):
    print(f"  {t}: {c}")
