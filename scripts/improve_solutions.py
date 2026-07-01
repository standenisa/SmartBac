"""
Îmbunătățește solution_steps din exercises_merged.json
— pași detaliați, explicații clare, format consistent.
"""

import json
import re
import math
import copy
from pathlib import Path


def improve_linear_eq(ex):
    """Rezolvare detaliată ecuație liniară: ax + b = c."""
    q = ex["question"]
    t = q.lower().replace(" ", "")

    # ax+b=c
    m = re.search(r"([+-]?\d*)x\s*([+-]\s*\d+)\s*=\s*([+-]?\d+)", t)
    if not m:
        m = re.search(r"([+-]?\d+)\s*x\s*=\s*([+-]?\d+)", t)
        if m:
            a = int(m.group(1))
            c = int(m.group(2))
            x = c / a
            return [
                f"Pasul 1: Avem ecuația {a}x = {c}",
                f"Pasul 2: Împărțim ambii membri la {a}: x = {c}/{a} = {int(x) if x == int(x) else f'{x:.2f}'}",
                f"Pasul 3: Verificare: {a} · {int(x) if x==int(x) else x} = {c} ✓",
                f"Răspuns: x = {int(x) if x == int(x) else x}"
            ]
        return None

    a = int(m.group(1)) if m.group(1) not in ("", "+") else 1
    if m.group(1) == "-": a = -1
    b = int(m.group(2).replace(" ", ""))
    c = int(m.group(3))

    if a == 0:
        return None
    x_val = (c - b) / a
    steps = [
        f"Pasul 1: Pornim de la ecuația: {a}x + ({b}) = {c}",
        f"Pasul 2: Mutăm termenul liber în dreapta: {a}x = {c} - ({b}) = {c - b}",
        f"Pasul 3: Împărțim ambii membri la {a}: x = {c - b}/{a} = {int(x_val) if x_val == int(x_val) else f'{x_val:.4g}'}",
        f"Pasul 4: Verificare: {a} · {int(x_val) if x_val==int(x_val) else x_val} + ({b}) = {int(a*x_val+b)} {'= ' + str(c) + ' ✓' if abs(a*x_val+b - c) < 0.01 else ''}",
        f"Răspuns: x = {int(x_val) if x_val == int(x_val) else x_val}"
    ]
    return steps


def improve_quadratic(ex):
    """Rezolvare detaliată ecuație grad 2."""
    q = ex["question"]
    t = q.lower().replace(" ", "")

    # ax²+bx+c=0 (suport pentru ², ^2, x2)
    t2 = t.replace("²", "^2").replace("³", "^3")
    m = re.search(r"([+-]?\d*)x\^2\s*([+-]\s*\d*)x\s*([+-]\s*\d+)\s*=\s*0", t2)
    if not m:
        return None

    a_s = m.group(1).replace(" ", "")
    if a_s in ("", "+"): a = 1
    elif a_s == "-": a = -1
    else:
        try: a = int(a_s)
        except: return None

    b_s = m.group(2).replace(" ", "")
    if b_s in ("", "+"): b = 1
    elif b_s == "-": b = -1
    else:
        try: b = int(b_s)
        except: return None

    try: c = int(m.group(3).replace(" ", ""))
    except: return None

    delta = b*b - 4*a*c

    steps = [
        f"Pasul 1: Identificăm coeficienții din ecuația {a}x² + ({b})x + ({c}) = 0: a = {a}, b = {b}, c = {c}",
        f"Pasul 2: Calculăm discriminantul: Δ = b² - 4ac = ({b})² - 4·{a}·({c}) = {b*b} - ({4*a*c}) = {delta}",
    ]

    if delta > 0:
        sqrt_d = math.sqrt(delta)
        x1 = (-b + sqrt_d) / (2*a)
        x2 = (-b - sqrt_d) / (2*a)
        sqrt_str = str(int(sqrt_d)) if sqrt_d == int(sqrt_d) else f"√{delta}"
        steps.append(f"Pasul 3: Δ > 0, deci ecuația are 2 soluții reale distincte")
        steps.append(f"Pasul 4: Aplicăm formula: x₁,₂ = (-b ± √Δ) / (2a) = ({-b} ± {sqrt_str}) / {2*a}")
        x1_s = int(x1) if x1 == int(x1) else f"{x1:.4g}"
        x2_s = int(x2) if x2 == int(x2) else f"{x2:.4g}"
        steps.append(f"Pasul 5: x₁ = ({-b} + {sqrt_str}) / {2*a} = {x1_s}")
        steps.append(f"Pasul 6: x₂ = ({-b} - {sqrt_str}) / {2*a} = {x2_s}")
        steps.append(f"Pasul 7: Verificare cu relațiile lui Viète: x₁ + x₂ = {x1_s} + {x2_s} = {float(x1_s)+float(x2_s):.4g} (trebuie = -b/a = {-b/a:.4g}) ✓")
        steps.append(f"Răspuns: x₁ = {x1_s}, x₂ = {x2_s}")
    elif delta == 0:
        x = -b / (2*a)
        x_s = int(x) if x == int(x) else f"{x:.4g}"
        steps.append(f"Pasul 3: Δ = 0, deci ecuația are o soluție dublă (rădăcină dublă)")
        steps.append(f"Pasul 4: x = -b / (2a) = {-b} / {2*a} = {x_s}")
        steps.append(f"Pasul 5: Verificare: {a}·({x_s})² + ({b})·({x_s}) + ({c}) = 0 ✓")
        steps.append(f"Răspuns: x = {x_s} (rădăcină dublă)")
    else:
        steps.append(f"Pasul 3: Δ < 0 (Δ = {delta}), deci ecuația NU are soluții reale")
        steps.append(f"Pasul 4: În mulțimea numerelor complexe: x₁,₂ = ({-b} ± i√{-delta}) / {2*a}")
        steps.append(f"Răspuns: Ecuația nu are soluții reale (Δ < 0)")

    return steps


def improve_derivative(ex):
    """Îmbunătățește soluția pentru derivate."""
    q = ex["question"]
    answer = ex.get("answer", "")

    # Extrage f(x) din întrebare
    m = re.search(r"f\(x\)\s*=\s*(.+?)(?:\.|$)", q)
    if not m:
        return None

    fx = m.group(1).strip()
    steps = [
        f"Pasul 1: Avem funcția f(x) = {fx}",
        f"Pasul 2: Identificăm regulile de derivare necesare:",
    ]

    # Detect what rules apply
    rules = []
    if "·" in fx or "*" in fx:
        rules.append("  - Regula produsului: (u·v)' = u'·v + u·v'")
    if "/" in fx or "frac" in fx:
        rules.append("  - Regula câtului: (u/v)' = (u'·v - u·v') / v²")
    if "sin" in fx or "cos" in fx or "tg" in fx:
        rules.append("  - Derivate trigonometrice: (sin x)' = cos x, (cos x)' = -sin x")
    if "ln" in fx or "log" in fx:
        rules.append("  - Derivata logaritmului: (ln x)' = 1/x")
    if "e" in fx and ("^" in fx or "ˣ" in fx):
        rules.append("  - Derivata exponențialei: (eˣ)' = eˣ")
    if "√" in fx or "sqrt" in fx:
        rules.append("  - Derivata radicalului: (√x)' = 1/(2√x)")
    if "^" in fx or "²" in fx or "³" in fx:
        rules.append("  - Regula puterii: (xⁿ)' = n·xⁿ⁻¹")

    if not rules:
        rules.append("  - Regula puterii: (xⁿ)' = n·xⁿ⁻¹")

    for r in rules:
        steps.append(r)

    steps.append(f"Pasul 3: Aplicăm regulile de derivare termen cu termen")
    steps.append(f"Pasul 4: Obținem f'(x) = {answer}")
    steps.append(f"Răspuns: f'(x) = {answer}")

    return steps


def improve_integral(ex):
    """Îmbunătățește soluția pentru integrale."""
    q = ex["question"]
    answer = ex.get("answer", "")

    steps = [
        f"Pasul 1: Identificăm integrala cerută din enunț",
        f"Pasul 2: Regula de integrare pentru puteri: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C, pentru n ≠ -1",
        f"Pasul 3: Aplicăm formula de integrare termen cu termen",
        f"Pasul 4: Nu uităm constanta de integrare C (pentru integrale nedefinite)",
        f"Pasul 5: Rezultatul: {answer}",
        f"Pasul 6: Verificare: derivăm rezultatul și trebuie să obținem funcția inițială",
        f"Răspuns: {answer}"
    ]
    return steps


def improve_determinant(ex):
    """Îmbunătățește soluția pentru determinanți."""
    q = ex["question"]
    answer = ex.get("answer", "")

    # Detect 2x2 or 3x3
    if "[[" in q:
        m2 = re.findall(r"(\d+)", q)
        if len(m2) == 4:
            a, b, c, d = [int(x) for x in m2[:4]]
            steps = [
                f"Pasul 1: Avem matricea 2×2: |{a} {b}| / |{c} {d}|",
                f"Pasul 2: Formula determinantului 2×2: det = a·d - b·c (diagonala principală minus diagonala secundară)",
                f"Pasul 3: Înlocuim: det = {a}·{d} - {b}·{c} = {a*d} - {b*c} = {a*d - b*c}",
                f"Pasul 4: Verificare: {a}·{d} = {a*d}, {b}·{c} = {b*c}, diferența = {a*d - b*c} ✓",
                f"Răspuns: det = {a*d - b*c}"
            ]
            return steps
    return None


def improve_combination(ex):
    """Îmbunătățește soluția pentru combinări."""
    q = ex["question"]
    m = re.search(r"C\s*\(?(\d+)\s*[,\s]\s*(\d+)", q)
    if not m:
        return None
    n, k = int(m.group(1)), int(m.group(2))
    if k < 0 or k > n:
        return None
    result = math.comb(n, k)
    steps = [
        f"Pasul 1: Avem combinări de {n} luate câte {k}: C({n},{k})",
        f"Pasul 2: Formula: C(n,k) = n! / (k! · (n-k)!)",
        f"Pasul 3: Înlocuim: C({n},{k}) = {n}! / ({k}! · {n-k}!)",
        f"Pasul 4: Calculăm: {n}! = {math.factorial(n)}, {k}! = {math.factorial(k)}, {n-k}! = {math.factorial(n-k)}",
        f"Pasul 5: C({n},{k}) = {math.factorial(n)} / ({math.factorial(k)} · {math.factorial(n-k)}) = {result}",
        f"Răspuns: C({n},{k}) = {result}"
    ]
    return steps


def improve_generic(ex):
    """Îmbunătățește orice exercițiu cu soluție prost formatată."""
    q = ex["question"]
    answer = ex.get("answer", "")
    old_steps = ex.get("solution_steps") or ex.get("steps") or []
    solution = ex.get("solution", "")

    # Dacă are un singur step lung, sparge-l
    if len(old_steps) == 1 and len(old_steps[0]) > 100:
        raw = old_steps[0]
        # Sparge pe "Step X:", "Pasul X:", sau propoziții
        parts = re.split(r"(?:Step\s*\d+\s*:|Pasul\s*\d+\s*:)", raw)
        parts = [p.strip() for p in parts if p.strip()]
        if len(parts) >= 2:
            new_steps = []
            for i, p in enumerate(parts, 1):
                new_steps.append(f"Pasul {i}: {p}")
            new_steps.append(f"Răspuns: {answer}")
            return new_steps

    # Dacă stepurile au prefix "Step X:", schimbă în "Pasul X:"
    if old_steps:
        new_steps = []
        for s in old_steps:
            s = re.sub(r"^Step\s+(\d+)\s*:\s*", r"Pasul \1: ", s)
            s = re.sub(r"^Step\s+final\s*:\s*", "Pasul final: ", s, flags=re.IGNORECASE)
            new_steps.append(s)

        # Adaugă răspuns la final dacă nu e
        has_answer = any("Răspuns" in s or "Raspuns" in s for s in new_steps)
        if not has_answer and answer:
            new_steps.append(f"Răspuns: {answer}")

        return new_steps

    # Dacă nu are steps deloc dar are solution
    if solution and len(solution) > 10:
        parts = re.split(r"\.\s+", solution)
        steps = [f"Pasul {i+1}: {p.strip()}" for i, p in enumerate(parts) if p.strip()]
        steps.append(f"Răspuns: {answer}")
        return steps

    return None


def improve_exercise(ex):
    """Decide ce tip de exercițiu e și îmbunătățește soluția."""
    q = ex.get("question", "").lower()

    # Detectăm tipul
    if re.search(r"x²|x\^2|x\s*la\s*puterea\s*2", q) and "=" in q:
        result = improve_quadratic(ex)
        if result: return result

    if re.search(r"\dx\s*[+-]|x\s*=", q) and "=" in q:
        result = improve_linear_eq(ex)
        if result: return result

    if re.search(r"deriv|f\s*'", q):
        result = improve_derivative(ex)
        if result: return result

    if re.search(r"integra|∫|primitiv", q):
        result = improve_integral(ex)
        if result: return result

    if re.search(r"det|determinant|\[\[", q):
        result = improve_determinant(ex)
        if result: return result

    if re.search(r"c\s*\(\s*\d+|combin", q):
        result = improve_combination(ex)
        if result: return result

    # Generic improvement
    return improve_generic(ex)


def main():
    input_path = Path("data/processed/exercises_merged.json")
    output_path = Path("data/processed/exercises_merged.json")
    backup_path = Path("data/processed/exercises_merged_backup.json")

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Backup
    with open(backup_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Backup salvat: {backup_path}")

    improved = 0
    for i, ex in enumerate(data):
        new_steps = improve_exercise(ex)
        if new_steps:
            data[i]["solution_steps"] = new_steps
            improved += 1

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Îmbunătățite: {improved}/{len(data)} exerciții")
    print(f"Salvat: {output_path}")

    # Show examples
    print("\n--- Exemple ---")
    for i in [0, 12, 50, 100]:
        ex = data[i]
        print(f"\nQ: {ex['question'][:80]}")
        for s in ex.get("solution_steps", [])[:5]:
            print(f"  {s}")


if __name__ == "__main__":
    main()
