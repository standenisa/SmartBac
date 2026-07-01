"""
Math Tutor Service — Deterministic rule-based math solver
Rezolvă exerciții PAS CU PAS cu explicații clare, fără ML extern.

Supported types:
  - Ecuații liniare, gradul 2
  - Derivate (putere, sumă)
  - Integrale (putere)
  - Limite (doar îndrumare metodică)
  - Determinanți 2×2, 3×3
  - Combinări, Aranjamente, Permutări
  - Progresii aritmetice, geometrice
  - Trigonometrie valori exacte
"""

import re
import math


# ─── EXERCISE TYPE DETECTION ───

EXERCISE_PATTERNS = [
    ("ecuatie_grad2", [
        r"([+-]?\d*)\s*x\s*[²\^]2?\s*([+-]\s*\d*)\s*x\s*([+-]\s*\d+)\s*=\s*0",
        r"x\s*[²\^]2?\s*([+-]\s*\d+)\s*x?\s*([+-]\s*\d+)?\s*=\s*0",
        r"([+-]?\d*)x\^2\s*([+-]\s*\d*x)?\s*([+-]\s*\d+)?\s*=\s*0",
    ]),
    ("ecuatie_liniara", [
        r"([+-]?\d*)x\s*([+-]\s*\d+)\s*=\s*([+-]?\d+)",
        r"([+-]?\d+)\s*x\s*=\s*([+-]?\d+)",
        r"x\s*([+-]\s*\d+)\s*=\s*([+-]?\d+)",
        r"x\s*=\s*([+-]?\d+)",
    ]),
    ("derivata", [
        r"(?:deriv(?:ata|eaza)|f'\s*\(x\)|calculea?z[aă]\s+derivata)",
        r"(?:\(.*\))\s*'",
        r"deriv",
    ]),
    ("integrala", [
        r"(?:integra(?:la|eaza)|∫|calculeaz[aă]\s+integrala)",
        r"primitiv",
    ]),
    ("limita", [
        r"(?:lim(?:ita)?|lim\s*[\(_{])",
        r"limita",
    ]),
    ("determinant", [
        r"(?:determinantul|determinant(?:ul)?)",
        r"calculeaz[aă]\s+det\b",
        r"\[\s*\[",
        r"\bdet\s*\[\[",
        r"\bdet\s*\(",
    ]),
    ("combinari", [
        r"(?:c(?:ombinari|omb)?[\s\(]\s*\d+[\s,]\s*\d+|C\(\d+,\s*\d+\)|C\s*\d+\s*\d+)",
    ]),
    ("aranjamente", [
        r"(?:a(?:ranjamente|ranj)?[\s\(]\s*\d+[\s,]\s*\d+|A\(\d+,\s*\d+\)|A\s*\d+\s*\d+)",
    ]),
    ("permutari", [
        r"(?:p(?:ermutari|erm)?[\s\(]\s*\d+|P\(\d+\)|\d+!)",
    ]),
    ("progresie_geometrica", [
        r"progresie\s+geometr",
    ]),
    ("progresie_aritmetica", [
        r"progresie\s+aritmet",
        r"(?:\bratia\b|\ba\d+\b|\ban\b|suma\s+(?:primilor|termenilor))",
    ]),
    ("trigonometrie", [
        r"(?:sin|cos|tan|tg|ctg|cot)\s*[\(]\s*\d+",
        r"(?:sin|cos|tan|tg)\s*\d+",
        r"trigonometr",
    ]),
]


def detect_exercise_type(text: str) -> str:
    """Detect the type of math exercise from text."""
    t = text.lower().strip()
    for etype, patterns in EXERCISE_PATTERNS:
        for p in patterns:
            if re.search(p, t, re.IGNORECASE):
                return etype
    return "necunoscut"


# ─── SOLVERS ───

def solve(text: str) -> dict:
    """Main entry: detect type and solve."""
    etype = detect_exercise_type(text)
    solvers = {
        "ecuatie_liniara": _solve_linear,
        "ecuatie_grad2": _solve_quadratic,
        "derivata": _solve_derivative,
        "integrala": _solve_integral,
        "limita": _solve_limit,
        "determinant": _solve_determinant,
        "combinari": _solve_combinations,
        "aranjamente": _solve_arrangements,
        "permutari": _solve_permutations,
        "progresie_aritmetica": _solve_arithmetic_prog,
        "progresie_geometrica": _solve_geometric_prog,
        "trigonometrie": _solve_trig,
    }
    solver = solvers.get(etype)
    if solver:
        try:
            return solver(text)
        except Exception as e:
            return _error_result(text, str(e))
    return _unknown_result(text)


def _fmt(val: float) -> str:
    """Format number nicely."""
    if val == int(val):
        return str(int(val))
    return f"{val:.4g}"


def _parse_coef(s: str) -> int:
    """Parse a signed coefficient: '' and '+' mean 1, '-' means -1."""
    if s in ("", "+"):
        return 1
    if s == "-":
        return -1
    return int(s)


def _parse_poly_terms(func_str: str) -> list:
    """Parse terms like '3x^4+2x-5' into (coef, exp, const) tuples; const is None for x-terms."""
    terms = []
    matches = re.findall(r"([+-]?\s*\d*)\s*x\s*(?:\^(\d+))?|([+-]?\s*\d+)(?!x)", func_str.replace(" ", ""))
    for coef_str, exp_str, const_str in matches:
        if const_str:
            terms.append((None, None, int(const_str)))
        else:
            terms.append((_parse_coef(coef_str), int(exp_str) if exp_str else 1, None))
    return terms


def _parse_n_k(text: str):
    """Extract n and k from text (swapped so n >= k); None if fewer than two numbers."""
    nums = re.findall(r"\d+", text)
    if len(nums) < 2:
        return None
    n, k = int(nums[0]), int(nums[1])
    if n < k:
        n, k = k, n
    return n, k


# ─── ECUAȚIE LINIARĂ ───

def _solve_linear(text: str) -> dict:
    t = text.lower().replace(" ", "")

    # Pattern: ax+b=c or ax-b=c
    m = re.search(r"([+-]?\d*)x([+-]\d+)=([+-]?\d+)", t)
    if m:
        a = _parse_coef(m.group(1))
        b = int(m.group(2))
        c = int(m.group(3))

        steps = []
        steps.append({"pas": 1, "actiune": "Scriem ecuația", "rezultat": f"{a}x + ({b}) = {c}"})
        steps.append({"pas": 2, "actiune": f"Mutăm {b} în membrul drept (schimbăm semnul)", "rezultat": f"{a}x = {c} - ({b}) = {c - b}"})
        x_val = (c - b) / a
        steps.append({"pas": 3, "actiune": f"Împărțim ambii membri la {a}", "rezultat": f"x = {c - b} / {a} = {_fmt(x_val)}"})

        # Verificare
        verif = a * x_val + b
        steps.append({"pas": 4, "actiune": "Verificare: înlocuim x în ecuație", "rezultat": f"{a} · {_fmt(x_val)} + ({b}) = {_fmt(verif)} {'✓' if abs(verif - c) < 1e-9 else '✗'}"})

        return {
            "tip": "Ecuație liniară",
            "ce_avem": f"Ecuația {a}x + ({b}) = {c}",
            "ce_aplicam": "Izolăm pe x: mutăm termenii liberi în dreapta, apoi împărțim la coeficientul lui x",
            "pasi": steps,
            "raspuns": f"x = {_fmt(x_val)}",
            "verificare": f"{a}·{_fmt(x_val)} + ({b}) = {_fmt(verif)} = {c} ✓",
            "greseli_frecvente": [
                "Uitarea schimbării semnului la mutarea termenilor",
                "Greșirea împărțirii cu numere negative",
            ],
        }

    # Pattern: ax = b
    m = re.search(r"([+-]?\d+)x=([+-]?\d+)", t)
    if m:
        a = int(m.group(1))
        b = int(m.group(2))
        x_val = b / a
        return {
            "tip": "Ecuație liniară simplă",
            "ce_avem": f"{a}x = {b}",
            "ce_aplicam": "Împărțim ambii membri la coeficientul lui x",
            "pasi": [
                {"pas": 1, "actiune": "Scriem ecuația", "rezultat": f"{a}x = {b}"},
                {"pas": 2, "actiune": f"Împărțim la {a}", "rezultat": f"x = {b}/{a} = {_fmt(x_val)}"},
            ],
            "raspuns": f"x = {_fmt(x_val)}",
            "verificare": f"{a} · {_fmt(x_val)} = {_fmt(a * x_val)} = {b} ✓",
            "greseli_frecvente": ["Confuzie între înmulțire și împărțire"],
        }

    # Pattern: x + b = c or x - b = c
    m = re.search(r"x([+-]\d+)=([+-]?\d+)", t)
    if m:
        b = int(m.group(1))
        c = int(m.group(2))
        x_val = c - b
        return {
            "tip": "Ecuație liniară simplă",
            "ce_avem": f"x + ({b}) = {c}",
            "ce_aplicam": "Mutăm termenul liber în dreapta",
            "pasi": [
                {"pas": 1, "actiune": "Scriem ecuația", "rezultat": f"x + ({b}) = {c}"},
                {"pas": 2, "actiune": f"Mutăm {b} în dreapta", "rezultat": f"x = {c} - ({b}) = {_fmt(x_val)}"},
            ],
            "raspuns": f"x = {_fmt(x_val)}",
            "verificare": f"{_fmt(x_val)} + ({b}) = {c} ✓",
            "greseli_frecvente": ["Uitarea schimbării semnului"],
        }

    return _unknown_result(text)


# ─── ECUAȚIE GRAD 2 ───

def _solve_quadratic(text: str) -> dict:
    t = text.lower().replace(" ", "").replace("²", "^2")

    # Full: ax^2 + bx + c = 0
    m = re.search(r"([+-]?\d*)x\^2([+-]\d*)x([+-]\d+)=0", t)
    if m:
        a = _parse_coef(m.group(1))
        b = _parse_coef(m.group(2))
        c = int(m.group(3))
    else:
        # x^2 - c = 0
        m = re.search(r"x\^2([+-]\d+)=0", t)
        if m:
            a, b = 1, 0
            c = int(m.group(1))
        else:
            return _unknown_result(text)

    delta = b * b - 4 * a * c
    steps = [
        {"pas": 1, "actiune": "Identificăm coeficienții", "rezultat": f"a = {a}, b = {b}, c = {c}"},
        {"pas": 2, "actiune": "Calculăm discriminantul Δ = b² - 4ac", "rezultat": f"Δ = ({b})² - 4·{a}·({c}) = {b*b} - {4*a*c} = {delta}"},
    ]

    if delta > 0:
        sqrt_d = math.sqrt(delta)
        x1 = (-b + sqrt_d) / (2 * a)
        x2 = (-b - sqrt_d) / (2 * a)
        steps.append({"pas": 3, "actiune": "Δ > 0 → 2 soluții reale distincte", "rezultat": f"√Δ = {_fmt(sqrt_d)}"})
        steps.append({"pas": 4, "actiune": "x₁ = (-b + √Δ) / 2a", "rezultat": f"x₁ = ({-b} + {_fmt(sqrt_d)}) / {2*a} = {_fmt(x1)}"})
        steps.append({"pas": 5, "actiune": "x₂ = (-b - √Δ) / 2a", "rezultat": f"x₂ = ({-b} - {_fmt(sqrt_d)}) / {2*a} = {_fmt(x2)}"})
        raspuns = f"x₁ = {_fmt(x1)}, x₂ = {_fmt(x2)}"
        verif = f"{a}·({_fmt(x1)})² + {b}·({_fmt(x1)}) + {c} = {_fmt(a*x1*x1 + b*x1 + c)} ✓"
    elif delta == 0:
        x = -b / (2 * a)
        steps.append({"pas": 3, "actiune": "Δ = 0 → soluție unică (dublă)", "rezultat": f"x = -b / 2a = {-b} / {2*a} = {_fmt(x)}"})
        raspuns = f"x = {_fmt(x)} (soluție dublă)"
        verif = f"{a}·({_fmt(x)})² + {b}·({_fmt(x)}) + {c} = {_fmt(a*x*x + b*x + c)} ✓"
    else:
        steps.append({"pas": 3, "actiune": "Δ < 0 → Nu are soluții reale", "rezultat": f"Δ = {delta} < 0 → ecuația nu are soluții în ℝ"})
        raspuns = "Ecuația nu are soluții reale (Δ < 0)"
        verif = "N/A - nu există soluții reale"

    return {
        "tip": "Ecuație de gradul II",
        "ce_avem": f"{a}x² + ({b})x + ({c}) = 0",
        "ce_aplicam": "Formula: x = (-b ± √Δ) / 2a, unde Δ = b² - 4ac",
        "pasi": steps,
        "raspuns": raspuns,
        "verificare": verif,
        "greseli_frecvente": [
            "Greșirea semnului la -b (uitarea minusului)",
            "Calcularea greșită a discriminantului (confuzie la 4ac)",
            "Împărțirea doar a numărătorului la 2a, nu a întregii fracții",
        ],
    }


# ─── DERIVATE ───

def _solve_derivative(text: str) -> dict:
    # Extract function after "derivata lui" or "f(x)="
    func_match = re.search(r"(?:derivata\s*(?:lui|pentru|din)?|f\(x\)\s*=|f'\(x\)\s*=|deriveaza)\s*(.+)", text.lower())
    func_str = func_match.group(1).strip() if func_match else text

    # Parse terms like 3x^4 + 2x^2 - 5x + 7
    terms = _parse_poly_terms(func_str)

    if not terms:
        return _unknown_result(text)

    deriv_parts = []
    steps = []

    step_num = 1
    steps.append({"pas": step_num, "actiune": "Identificăm funcția", "rezultat": f"f(x) = {func_str}"})
    step_num += 1
    steps.append({"pas": step_num, "actiune": "Aplicăm regulile de derivare termen cu termen", "rezultat": "Regula puterii: (xⁿ)' = n·xⁿ⁻¹, constanta' = 0"})
    step_num += 1

    for coef, exp, const in terms:
        if const is not None:
            steps.append({"pas": step_num, "actiune": f"({const})' = 0 (derivata constantei)", "rezultat": "0"})
            step_num += 1
            continue

        # Derivative
        new_coef = coef * exp
        new_exp = exp - 1

        if new_exp == 0:
            deriv_parts.append(_fmt(new_coef))
            steps.append({"pas": step_num, "actiune": f"({coef}x^{exp})' = {exp}·{coef}·x^{exp-1}", "rezultat": f"{_fmt(new_coef)}"})
        elif new_exp == 1:
            deriv_parts.append(f"{_fmt(new_coef)}x")
            steps.append({"pas": step_num, "actiune": f"({coef}x^{exp})' = {exp}·{coef}·x^{exp-1}", "rezultat": f"{_fmt(new_coef)}x"})
        else:
            deriv_parts.append(f"{_fmt(new_coef)}x^{new_exp}")
            steps.append({"pas": step_num, "actiune": f"({coef}x^{exp})' = {exp}·{coef}·x^{exp-1}", "rezultat": f"{_fmt(new_coef)}x^{new_exp}"})
        step_num += 1

    result_str = " + ".join(deriv_parts).replace("+ -", "- ") if deriv_parts else "0"

    return {
        "tip": "Derivată",
        "ce_avem": f"f(x) = {func_str}",
        "ce_aplicam": "Regula puterii: (axⁿ)' = n·a·xⁿ⁻¹ și (c)' = 0",
        "pasi": steps,
        "raspuns": f"f'(x) = {result_str}",
        "verificare": "Fiecare termen derivat conform regulii puterii",
        "greseli_frecvente": [
            "Uitarea scăderii cu 1 a exponentului",
            "Neînmulțirea coeficientului cu exponentul",
            "Derivata constantei NU este constanta, ci 0",
        ],
    }


# ─── INTEGRALE ───

def _solve_integral(text: str) -> dict:
    func_match = re.search(r"(?:integrala\s*(?:lui|din)?|∫|primitivela\s*lui|primitiva)\s*(.+?)(?:\s*dx)?$", text.lower())
    func_str = func_match.group(1).strip() if func_match else text

    terms = _parse_poly_terms(func_str)

    if not terms:
        return _unknown_result(text)

    integ_parts = []
    steps = [
        {"pas": 1, "actiune": "Identificăm funcția", "rezultat": f"f(x) = {func_str}"},
        {"pas": 2, "actiune": "Aplicăm formula de integrare", "rezultat": "∫ axⁿ dx = (a/(n+1))·xⁿ⁺¹ + C"},
    ]
    step_num = 3

    for coef, exp, const in terms:
        if const is not None:
            integ_parts.append(f"{const}x")
            steps.append({"pas": step_num, "actiune": f"∫ {const} dx = {const}x", "rezultat": f"{const}x"})
            step_num += 1
            continue

        new_exp = exp + 1
        new_coef = coef / new_exp

        if new_coef == int(new_coef):
            new_coef = int(new_coef)

        integ_parts.append(f"{_fmt(new_coef)}x^{new_exp}")
        steps.append({"pas": step_num, "actiune": f"∫ {coef}x^{exp} dx = ({coef}/{new_exp})x^{new_exp}", "rezultat": f"{_fmt(new_coef)}x^{new_exp}"})
        step_num += 1

    result_str = " + ".join(integ_parts).replace("+ -", "- ") + " + C"

    return {
        "tip": "Integrală nedefinită",
        "ce_avem": f"∫ ({func_str}) dx",
        "ce_aplicam": "Regula puterii inversată: ∫ axⁿ dx = (a/(n+1))·xⁿ⁺¹ + C",
        "pasi": steps,
        "raspuns": f"F(x) = {result_str}",
        "verificare": "Derivăm rezultatul și trebuie să obținem funcția originală",
        "greseli_frecvente": [
            "Uitarea constantei de integrare +C",
            "Greșirea la creșterea exponentului (n+1, nu n-1)",
            "Confuzia cu regula derivatei (se adună 1, nu se scade)",
        ],
    }


# ─── LIMITE ───

def _solve_limit(text: str) -> dict:
    # Try to extract limit details
    m = re.search(r"lim.*?x\s*(?:->|→|tinde)\s*([+-]?\d+|inf|∞)", text.lower())
    point = m.group(1) if m else "?"

    func_match = re.search(r"(?:lim.*?(?:\)|de|din|pentru)\s*)(.+)", text.lower())
    func_str = func_match.group(1).strip() if func_match else text

    steps = [
        {"pas": 1, "actiune": f"Avem limita când x → {point}", "rezultat": f"lim(x→{point}) {func_str}"},
        {"pas": 2, "actiune": "Încercăm substituția directă (înlocuim x cu valoarea)", "rezultat": f"Înlocuim x = {point} în expresie"},
        {"pas": 3, "actiune": "Dacă obținem formă nedeterminată (0/0, ∞/∞), aplicăm L'Hôpital", "rezultat": "Regula L'Hôpital: lim f/g = lim f'/g'"},
    ]

    return {
        "tip": "Limită",
        "ce_avem": f"lim(x→{point}) {func_str}",
        "ce_aplicam": "1. Substituție directă  2. Dacă 0/0 sau ∞/∞ → L'Hôpital  3. Factorizare/raționalizare",
        "pasi": steps,
        "raspuns": f"Aplică substituția directă: înlocuiește x = {point}",
        "verificare": "Verifică dacă rezultatul e finit și consistent",
        "greseli_frecvente": [
            "Aplicarea L'Hôpital când NU e formă nedeterminată",
            "Uitarea că lim(1/x) când x→0 este ∞, nu 0",
            "Confuzia între limita laterală stângă și dreaptă",
        ],
    }


# ─── DETERMINANȚI ───

def _solve_determinant(text: str) -> dict:
    # Extract numbers from matrix notation
    nums = [int(n) for n in re.findall(r"[+-]?\d+", text)]

    if len(nums) == 4:
        a, b, c, d = nums
        det = a * d - b * c
        return {
            "tip": "Determinant 2×2",
            "ce_avem": f"|{a}  {b}|\n|{c}  {d}|",
            "ce_aplicam": "Formula: det = a·d - b·c (diagonala principală minus diagonala secundară)",
            "pasi": [
                {"pas": 1, "actiune": "Identificăm elementele matricei", "rezultat": f"a={a}, b={b}, c={c}, d={d}"},
                {"pas": 2, "actiune": "Aplicăm formula det = a·d - b·c", "rezultat": f"det = {a}·{d} - {b}·{c} = {a*d} - {b*c} = {det}"},
            ],
            "raspuns": f"det = {det}",
            "verificare": f"{a}·{d} - {b}·{c} = {a*d} - {b*c} = {det}",
            "greseli_frecvente": [
                "Confuzia între diagonala principală și secundară",
                "Greșirea semnului la scădere",
            ],
        }

    if len(nums) == 9:
        a, b, c, d, e, f_, g, h, i = nums
        # Sarrus
        pos = a*e*i + b*f_*g + c*d*h
        neg = c*e*g + b*d*i + a*f_*h
        det = pos - neg
        return {
            "tip": "Determinant 3×3 (Regula lui Sarrus)",
            "ce_avem": f"|{a}  {b}  {c}|\n|{d}  {e}  {f_}|\n|{g}  {h}  {i}|",
            "ce_aplicam": "Regula lui Sarrus: sumă diagonale principale - sumă diagonale secundare",
            "pasi": [
                {"pas": 1, "actiune": "Diagonale principale (↘)", "rezultat": f"{a}·{e}·{i} + {b}·{f_}·{g} + {c}·{d}·{h} = {a*e*i} + {b*f_*g} + {c*d*h} = {pos}"},
                {"pas": 2, "actiune": "Diagonale secundare (↙)", "rezultat": f"{c}·{e}·{g} + {b}·{d}·{i} + {a}·{f_}·{h} = {c*e*g} + {b*d*i} + {a*f_*h} = {neg}"},
                {"pas": 3, "actiune": "det = principale - secundare", "rezultat": f"det = {pos} - {neg} = {det}"},
            ],
            "raspuns": f"det = {det}",
            "verificare": f"{pos} - {neg} = {det}",
            "greseli_frecvente": [
                "Confuzia la diagonalele lui Sarrus (trebuie 'extinsă' matricea)",
                "Greșirea ordinii elementelor pe diagonale",
            ],
        }

    return _unknown_result(text)


# ─── COMBINĂRI ───

def _solve_combinations(text: str) -> dict:
    nk = _parse_n_k(text)
    if nk is None:
        return _unknown_result(text)
    n, k = nk

    result = math.comb(n, k)
    return {
        "tip": "Combinări",
        "ce_avem": f"C({n}, {k})",
        "ce_aplicam": "Formula: C(n,k) = n! / (k! · (n-k)!)",
        "pasi": [
            {"pas": 1, "actiune": "Identificăm n și k", "rezultat": f"n = {n}, k = {k}"},
            {"pas": 2, "actiune": f"C({n},{k}) = {n}! / ({k}! · {n-k}!)", "rezultat": f"= {math.factorial(n)} / ({math.factorial(k)} · {math.factorial(n-k)})"},
            {"pas": 3, "actiune": "Calculăm", "rezultat": f"= {result}"},
        ],
        "raspuns": f"C({n},{k}) = {result}",
        "verificare": f"{n}! / ({k}! · {n-k}!) = {result}",
        "greseli_frecvente": [
            "Confuzia între combinări și aranjamente",
            "La combinări ORDINEA NU contează",
        ],
    }


# ─── ARANJAMENTE ───

def _solve_arrangements(text: str) -> dict:
    nk = _parse_n_k(text)
    if nk is None:
        return _unknown_result(text)
    n, k = nk

    result = math.perm(n, k)
    return {
        "tip": "Aranjamente",
        "ce_avem": f"A({n}, {k})",
        "ce_aplicam": "Formula: A(n,k) = n! / (n-k)!",
        "pasi": [
            {"pas": 1, "actiune": "Identificăm n și k", "rezultat": f"n = {n}, k = {k}"},
            {"pas": 2, "actiune": f"A({n},{k}) = {n}! / ({n-k})!", "rezultat": f"= {math.factorial(n)} / {math.factorial(n-k)}"},
            {"pas": 3, "actiune": "Calculăm", "rezultat": f"= {result}"},
        ],
        "raspuns": f"A({n},{k}) = {result}",
        "verificare": f"{n}! / {n-k}! = {result}",
        "greseli_frecvente": [
            "Confuzia cu combinările (la aranjamente ORDINEA contează)",
        ],
    }


# ─── PERMUTĂRI ───

def _solve_permutations(text: str) -> dict:
    nums = re.findall(r"\d+", text)
    if not nums:
        return _unknown_result(text)
    n = int(nums[0])
    result = math.factorial(n)
    return {
        "tip": "Permutări",
        "ce_avem": f"P({n}) = {n}!",
        "ce_aplicam": "Formula: P(n) = n! (produsul numerelor de la 1 la n)",
        "pasi": [
            {"pas": 1, "actiune": f"P({n}) = {n}!", "rezultat": " · ".join(str(i) for i in range(n, 0, -1))},
            {"pas": 2, "actiune": "Calculăm", "rezultat": f"= {result}"},
        ],
        "raspuns": f"P({n}) = {n}! = {result}",
        "verificare": f"{n}! = {result}",
        "greseli_frecvente": ["Uitarea că 0! = 1"],
    }


# ─── PROGRESIE ARITMETICĂ ───

def _solve_arithmetic_prog(text: str) -> dict:
    nums = [int(n) for n in re.findall(r"[+-]?\d+", text)]
    if len(nums) >= 3:
        a1, r, n = nums[0], nums[1], nums[2]
        an = a1 + (n - 1) * r
        sn = n * (a1 + an) // 2
        return {
            "tip": "Progresie aritmetică",
            "ce_avem": f"a₁ = {a1}, rația r = {r}, n = {n}",
            "ce_aplicam": "aₙ = a₁ + (n-1)·r  și  Sₙ = n·(a₁ + aₙ)/2",
            "pasi": [
                {"pas": 1, "actiune": f"aₙ = a₁ + (n-1)·r", "rezultat": f"a{n} = {a1} + ({n}-1)·{r} = {a1} + {(n-1)*r} = {an}"},
                {"pas": 2, "actiune": f"Sₙ = n·(a₁ + aₙ)/2", "rezultat": f"S{n} = {n}·({a1} + {an})/2 = {n}·{a1+an}/2 = {sn}"},
            ],
            "raspuns": f"a{n} = {an}, S{n} = {sn}",
            "verificare": f"a{n} = {a1} + {(n-1)*r} = {an}",
            "greseli_frecvente": ["Confuzia între n și n-1 în formulă"],
        }
    return _unknown_result(text)


# ─── PROGRESIE GEOMETRICĂ ───

def _solve_geometric_prog(text: str) -> dict:
    nums = [int(n) for n in re.findall(r"[+-]?\d+", text)]
    if len(nums) >= 3:
        a1, q, n = nums[0], nums[1], nums[2]
        an = a1 * (q ** (n - 1))
        sn = a1 * (q ** n - 1) // (q - 1) if q != 1 else a1 * n
        return {
            "tip": "Progresie geometrică",
            "ce_avem": f"b₁ = {a1}, rația q = {q}, n = {n}",
            "ce_aplicam": "bₙ = b₁·qⁿ⁻¹  și  Sₙ = b₁·(qⁿ-1)/(q-1)",
            "pasi": [
                {"pas": 1, "actiune": f"bₙ = b₁·q^(n-1)", "rezultat": f"b{n} = {a1}·{q}^{n-1} = {a1}·{q**(n-1)} = {an}"},
                {"pas": 2, "actiune": f"Sₙ = b₁·(qⁿ-1)/(q-1)", "rezultat": f"S{n} = {a1}·({q}^{n}-1)/({q}-1) = {sn}"},
            ],
            "raspuns": f"b{n} = {an}, S{n} = {sn}",
            "verificare": f"b{n} = {a1}·{q}^{n-1} = {an}",
            "greseli_frecvente": ["Confuzia între rație aditivă (aritmetică) și multiplicativă (geometrică)"],
        }
    return _unknown_result(text)


# ─── TRIGONOMETRIE ───

TRIG_VALUES = {
    0: {"sin": "0", "cos": "1", "tan": "0", "cot": "nedefinit"},
    30: {"sin": "1/2", "cos": "√3/2", "tan": "√3/3", "cot": "√3"},
    45: {"sin": "√2/2", "cos": "√2/2", "tan": "1", "cot": "1"},
    60: {"sin": "√3/2", "cos": "1/2", "tan": "√3", "cot": "√3/3"},
    90: {"sin": "1", "cos": "0", "tan": "nedefinit", "cot": "0"},
    120: {"sin": "√3/2", "cos": "-1/2", "tan": "-√3", "cot": "-√3/3"},
    135: {"sin": "√2/2", "cos": "-√2/2", "tan": "-1", "cot": "-1"},
    150: {"sin": "1/2", "cos": "-√3/2", "tan": "-√3/3", "cot": "-√3"},
    180: {"sin": "0", "cos": "-1", "tan": "0", "cot": "nedefinit"},
    270: {"sin": "-1", "cos": "0", "tan": "nedefinit", "cot": "0"},
    360: {"sin": "0", "cos": "1", "tan": "0", "cot": "nedefinit"},
}


def _solve_trig(text: str) -> dict:
    m = re.search(r"(sin|cos|tan|tg|ctg|cot)\s*[\(]?\s*(\d+)", text.lower())
    if not m:
        return _unknown_result(text)

    func = m.group(1)
    angle = int(m.group(2))

    if func == "tg":
        func = "tan"
    elif func == "ctg":
        func = "cot"

    if angle in TRIG_VALUES and func in TRIG_VALUES[angle]:
        val = TRIG_VALUES[angle][func]
        return {
            "tip": "Trigonometrie - Valori exacte",
            "ce_avem": f"{func}({angle}°)",
            "ce_aplicam": "Tabel valori trigonometrice pentru unghiuri remarcabile",
            "pasi": [
                {"pas": 1, "actiune": f"Căutăm {func}({angle}°) în tabel", "rezultat": f"{func}({angle}°) = {val}"},
            ],
            "raspuns": f"{func}({angle}°) = {val}",
            "verificare": "Valoare din tabelul trigonometric",
            "greseli_frecvente": [
                "Confuzia între sin și cos (sunt 'inversate' la 30° și 60°)",
                "Uitarea semnului în cadranele II, III, IV",
            ],
        }

    # Not a standard angle
    rad = math.radians(angle)
    if func == "sin":
        val = math.sin(rad)
    elif func == "cos":
        val = math.cos(rad)
    elif func == "tan":
        val = math.tan(rad) if angle % 180 != 90 else None
    else:  # cot
        val = 1 / math.tan(rad) if angle % 180 != 0 else None
    val_str = _fmt(val) if val is not None else "nedefinit"

    return {
        "tip": "Trigonometrie",
        "ce_avem": f"{func}({angle}°)",
        "ce_aplicam": "Conversie în radiani și calcul",
        "pasi": [
            {"pas": 1, "actiune": f"Convertim: {angle}° = {angle}·π/180 rad", "rezultat": f"≈ {_fmt(math.radians(angle))} rad"},
            {"pas": 2, "actiune": f"Calculăm {func}({angle}°)", "rezultat": f"≈ {val_str}"},
        ],
        "raspuns": f"{func}({angle}°) ≈ {val_str}",
        "verificare": "Calculat numeric",
        "greseli_frecvente": ["Confuzia grade/radiani"],
    }


# ─── EXPLAIN WRONG ANSWER ───

def explain_wrong_answer(exercise: dict, user_answer: str, correct_answer: str) -> dict:
    """When a student gets it wrong, explain what likely went wrong."""
    topic = exercise.get("topic", "")
    question = exercise.get("question", "")

    common_mistakes = {
        "ecuatie": "Ai uitat să schimbi semnul când muți un termen în celălalt membru?",
        "derivat": "Ai uitat să scazi 1 din exponent sau să înmulțești cu exponentul?",
        "integral": "Ai uitat constanta +C sau ai scăzut în loc să aduni la exponent?",
        "limit": "Ai aplicat L'Hôpital fără să verifici forma nedeterminată?",
        "determinant": "Ai confundat diagonalele principală și secundară?",
        "matric": "Ai confundat linii cu coloane la înmulțire?",
        "combinari": "Ai confundat combinări cu aranjamente?",
        "trigonometr": "Ai confundat valorile sin/cos la 30° și 60°?",
    }

    probable_mistake = "Verifică fiecare pas al calculului."
    for key, msg in common_mistakes.items():
        if key in topic.lower() or key in question.lower():
            probable_mistake = msg
            break

    # Try to solve the exercise
    solution = solve(question)

    return {
        "analiza": f"Ai răspuns \"{user_answer}\", dar răspunsul corect este \"{correct_answer}\".",
        "greseala_probabila": probable_mistake,
        "rezolvare": solution,
        "sfat": "Încearcă să refaci calculul pas cu pas și verifică la final.",
    }


# ─── HELPERS ───

def _unknown_result(text: str) -> dict:
    return {
        "tip": "Nerecunoscut",
        "ce_avem": text,
        "ce_aplicam": "Nu am putut identifica tipul exercițiului",
        "pasi": [],
        "raspuns": "Reformulează exercițiul sau încearcă un format precum: 'rezolvă 3x+5=11' sau 'derivata lui x^3+2x'",
        "verificare": "",
        "greseli_frecvente": [],
    }


def _error_result(text: str, error: str) -> dict:
    return {
        "tip": "Eroare la rezolvare",
        "ce_avem": text,
        "ce_aplicam": f"A apărut o eroare: {error}",
        "pasi": [],
        "raspuns": "Reformulează exercițiul într-un format mai clar.",
        "verificare": "",
        "greseli_frecvente": [],
    }
