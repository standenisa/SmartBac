#!/usr/bin/env python3
"""
Data augmentation script for BAC math exercises.
Generates programmatic exercises to reach 5000+ training pairs.

Usage:
    python scripts/augment_data.py
"""

import random
import json
import os
import math
from fractions import Fraction

# Reproducibility
random.seed(42)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "exercises_bac.json")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "augmented_exercises.json")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sign_str(val):
    """Return a string like '+ 3' or '- 3' for display in expressions."""
    if val >= 0:
        return f"+ {val}"
    return f"- {abs(val)}"


def _poly_str(coeffs, var="x"):
    """Build a human-readable polynomial string from highest to lowest degree.
    coeffs = [a_n, a_{n-1}, ..., a_1, a_0]
    """
    n = len(coeffs) - 1
    parts = []
    for i, c in enumerate(coeffs):
        deg = n - i
        if c == 0:
            continue
        # coefficient part
        if deg == 0:
            token = str(abs(c))
        elif deg == 1:
            token = f"{abs(c)}{var}" if abs(c) != 1 else var
        else:
            token = f"{abs(c)}{var}^{deg}" if abs(c) != 1 else f"{var}^{deg}"
        # sign
        if not parts:
            parts.append(f"-{token}" if c < 0 else token)
        else:
            parts.append(f"- {token}" if c < 0 else f"+ {token}")
    return " ".join(parts) if parts else "0"


def _frac_str(num, den):
    """Return a fraction as a string, simplifying when possible."""
    if den == 1:
        return str(num)
    g = math.gcd(abs(num), abs(den))
    num //= g
    den //= g
    if den < 0:
        num, den = -num, -den
    if den == 1:
        return str(num)
    return f"{num}/{den}"


def _factorial(n):
    return math.factorial(n)


def _comb(n, k):
    return math.comb(n, k)


def _perm(n, k):
    return _factorial(n) // _factorial(n - k)


# ---------------------------------------------------------------------------
# Question-preamble variations (Romanian)
# ---------------------------------------------------------------------------
EQ_PREAMBLES = [
    "Rezolva ecuatia:",
    "Determina solutiile ecuatiei:",
    "Gaseste x din ecuatia:",
    "Rezolvati ecuatia:",
    "Aflati solutiile ecuatiei:",
]

FUNC_PREAMBLES = [
    "Fie functia f: R -> R,",
    "Se considera functia f,",
    "Fie f: R -> R definita prin",
]

DERIV_PREAMBLES = [
    "Calculeaza derivata functiei f(x) = ",
    "Determinati f'(x) pentru f(x) = ",
    "Gasiti derivata functiei f(x) = ",
]

LIMIT_PREAMBLES = [
    "Calculati limita:",
    "Determinati limita:",
    "Gasiti valoarea limitei:",
]

INTEGRAL_PREAMBLES = [
    "Calculati integrala:",
    "Determinati primitiva functiei:",
    "Gasiti integrala:",
]

# ---------------------------------------------------------------------------
# 1. Equations
# ---------------------------------------------------------------------------

def generate_equations(count=450):
    exercises = []
    per_sub = count // 4  # linear, quadratic, system, mixed

    # --- Linear: ax + b = c  (a != 0, integer solution) ---
    for _ in range(per_sub):
        a = random.choice([i for i in range(-10, 11) if i != 0])
        x_sol = random.randint(-20, 20)
        b = random.randint(-30, 30)
        c = a * x_sol + b
        preamble = random.choice(EQ_PREAMBLES)
        eq_str = f"{a}x {_sign_str(b)} = {c}"
        question = f"{preamble} {eq_str}"
        steps = [
            f"Ecuatia: {eq_str}",
            f"Mutam termenul liber: {a}x = {c} - ({b}) = {c - b}",
            f"Impartim la {a}: x = {c - b}/{a} = {x_sol}",
        ]
        latex = f"{a}x {'+' if b >= 0 else '-'} {abs(b)} = {c}"
        exercises.append({
            "question": question,
            "answer": f"x = {x_sol}",
            "type": "equation",
            "steps": steps,
            "latex": latex,
            "difficulty": 1,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Quadratic: ax^2 + bx + c = 0 with delta >= 0 ---
    for _ in range(per_sub):
        a = random.choice([i for i in range(-5, 6) if i != 0])
        # ensure discriminant >= 0 by constructing from roots
        x1 = random.randint(-10, 10)
        x2 = random.randint(-10, 10)
        # a(x-x1)(x-x2) = a*x^2 - a(x1+x2)x + a*x1*x2
        b_coeff = -a * (x1 + x2)
        c_coeff = a * x1 * x2
        delta = b_coeff * b_coeff - 4 * a * c_coeff
        preamble = random.choice(EQ_PREAMBLES)
        eq_str = f"{_poly_str([a, b_coeff, c_coeff])} = 0"
        question = f"{preamble} {eq_str}"
        if x1 == x2:
            answer_str = f"x = {x1} (solutie dubla)"
        else:
            s1, s2 = sorted([x1, x2])
            answer_str = f"x1 = {s1}, x2 = {s2}"
        sqrt_delta = int(math.isqrt(delta)) if delta >= 0 else 0
        steps = [
            f"Ecuatia: {eq_str}",
            f"a = {a}, b = {b_coeff}, c = {c_coeff}",
            f"Delta = b^2 - 4ac = {b_coeff}^2 - 4*{a}*{c_coeff} = {delta}",
            f"sqrt(Delta) = {sqrt_delta}",
            f"x1 = (-b - sqrt(Delta)) / (2a) = ({-b_coeff} - {sqrt_delta}) / {2*a} = {min(x1,x2)}",
            f"x2 = (-b + sqrt(Delta)) / (2a) = ({-b_coeff} + {sqrt_delta}) / {2*a} = {max(x1,x2)}",
        ]
        exercises.append({
            "question": question,
            "answer": answer_str,
            "type": "equation",
            "steps": steps,
            "latex": f"{_poly_str([a, b_coeff, c_coeff])} = 0",
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Systems of 2 linear equations ---
    for _ in range(per_sub):
        # build from known solution
        x_sol = random.randint(-10, 10)
        y_sol = random.randint(-10, 10)
        a1 = random.choice([i for i in range(-6, 7) if i != 0])
        b1 = random.choice([i for i in range(-6, 7) if i != 0])
        c1 = a1 * x_sol + b1 * y_sol
        a2 = random.choice([i for i in range(-6, 7) if i != 0])
        b2 = random.choice([i for i in range(-6, 7) if i != 0])
        # avoid parallel lines
        while a1 * b2 == a2 * b1:
            a2 = random.choice([i for i in range(-6, 7) if i != 0])
            b2 = random.choice([i for i in range(-6, 7) if i != 0])
        c2 = a2 * x_sol + b2 * y_sol
        eq1 = f"{a1}x {_sign_str(b1)}y = {c1}"
        eq2 = f"{a2}x {_sign_str(b2)}y = {c2}"
        preamble = random.choice(EQ_PREAMBLES[:3])
        question = f"{preamble} sistemul {{ {eq1} ; {eq2} }}"
        steps = [
            f"Sistemul: {eq1}, {eq2}",
            f"Folosim metoda substitutiei sau reducerii.",
            f"Din prima ecuatie: x = ({c1} - {b1}y) / {a1}",
            f"Inlocuim in a doua ecuatie si obtinem y = {y_sol}",
            f"Apoi x = {x_sol}",
        ]
        exercises.append({
            "question": question,
            "answer": f"x = {x_sol}, y = {y_sol}",
            "type": "equation",
            "steps": steps,
            "latex": f"\\begin{{cases}} {a1}x + {b1}y = {c1} \\\\ {a2}x + {b2}y = {c2} \\end{{cases}}",
            "difficulty": 3,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Variation / absolute-value style linear ---
    for _ in range(count - 3 * per_sub):
        a = random.choice([i for i in range(-8, 9) if i != 0])
        b = random.randint(-15, 15)
        c = random.randint(-15, 15)
        d = random.randint(-15, 15)
        # (a)x + b = cx + d  =>  (a-c)x = d - b
        if a == c:
            c += 1
        x_sol_num = d - b
        x_sol_den = a - c
        g = math.gcd(abs(x_sol_num), abs(x_sol_den))
        x_sol_num //= g
        x_sol_den //= g
        if x_sol_den < 0:
            x_sol_num, x_sol_den = -x_sol_num, -x_sol_den
        eq_str = f"{a}x {_sign_str(b)} = {c}x {_sign_str(d)}"
        preamble = random.choice(EQ_PREAMBLES)
        question = f"{preamble} {eq_str}"
        ans = f"x = {x_sol_num}" if x_sol_den == 1 else f"x = {x_sol_num}/{x_sol_den}"
        steps = [
            f"Ecuatia: {eq_str}",
            f"Grupam: ({a} - {c})x = {d} - ({b})",
            f"{a - c}x = {d - b}",
            f"{ans}",
        ]
        exercises.append({
            "question": question,
            "answer": ans,
            "type": "equation",
            "steps": steps,
            "latex": eq_str,
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    return exercises


# ---------------------------------------------------------------------------
# 2. Functions
# ---------------------------------------------------------------------------

def generate_functions(count=450):
    exercises = []
    per_sub = count // 4

    # --- f(x) = ax + b, calculate f(k) ---
    for _ in range(per_sub):
        a = random.choice([i for i in range(-10, 11) if i != 0])
        b = random.randint(-20, 20)
        k = random.randint(-10, 10)
        result = a * k + b
        preamble = random.choice(FUNC_PREAMBLES)
        question = f"{preamble} f(x) = {_poly_str([a, b])}. Calculati f({k})."
        steps = [
            f"f(x) = {_poly_str([a, b])}",
            f"f({k}) = {a}*({k}) + ({b})",
            f"f({k}) = {a * k} + ({b}) = {result}",
        ]
        exercises.append({
            "question": question,
            "answer": f"f({k}) = {result}",
            "type": "function",
            "steps": steps,
            "latex": f"f(x) = {_poly_str([a, b])}, \\; f({k}) = ?",
            "difficulty": 1,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- f(x) = ax^2 + bx + c, calculate f(k) ---
    for _ in range(per_sub):
        a = random.choice([i for i in range(-5, 6) if i != 0])
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
        k = random.randint(-5, 5)
        result = a * k * k + b * k + c
        preamble = random.choice(FUNC_PREAMBLES)
        question = f"{preamble} f(x) = {_poly_str([a, b, c])}. Calculati f({k})."
        steps = [
            f"f(x) = {_poly_str([a, b, c])}",
            f"f({k}) = {a}*({k})^2 + ({b})*({k}) + ({c})",
            f"f({k}) = {a * k * k} + ({b * k}) + ({c}) = {result}",
        ]
        exercises.append({
            "question": question,
            "answer": f"f({k}) = {result}",
            "type": "function",
            "steps": steps,
            "latex": f"f(x) = {_poly_str([a, b, c])}, \\; f({k}) = ?",
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Find x when f(x) = k, f linear ---
    for _ in range(per_sub):
        a = random.choice([i for i in range(-10, 11) if i != 0])
        b = random.randint(-20, 20)
        x_sol = random.randint(-15, 15)
        k = a * x_sol + b
        preamble = random.choice(FUNC_PREAMBLES)
        question = f"{preamble} f(x) = {_poly_str([a, b])}. Determinati x astfel incat f(x) = {k}."
        steps = [
            f"f(x) = {_poly_str([a, b])}",
            f"Punem f(x) = {k}: {a}x + ({b}) = {k}",
            f"{a}x = {k} - ({b}) = {k - b}",
            f"x = {k - b}/{a} = {x_sol}",
        ]
        exercises.append({
            "question": question,
            "answer": f"x = {x_sol}",
            "type": "function",
            "steps": steps,
            "latex": f"f(x) = {_poly_str([a, b])}, \\; f(x) = {k}",
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Domain / codomain questions ---
    templates = [
        ("f(x) = sqrt({val} - x)", "(-inf, {val}]", "Domeniul: {val} - x >= 0, deci x <= {val}."),
        ("f(x) = 1/(x - {val})", "R \\ {{{val}}}", "Domeniul: x - {val} != 0, deci x != {val}."),
        ("f(x) = ln(x - {val})", "({val}, +inf)", "Domeniul: x - {val} > 0, deci x > {val}."),
    ]
    for _ in range(count - 3 * per_sub):
        tmpl = random.choice(templates)
        val = random.randint(-10, 10)
        f_str = tmpl[0].format(val=val)
        domain = tmpl[1].format(val=val)
        expl = tmpl[2].format(val=val)
        question = f"Determinati domeniul de definitie al functiei {f_str}."
        steps = [f"Functia: {f_str}", expl, f"D = {domain}"]
        exercises.append({
            "question": question,
            "answer": f"D = {domain}",
            "type": "function",
            "steps": steps,
            "latex": f_str,
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    return exercises


# ---------------------------------------------------------------------------
# 3. Derivatives
# ---------------------------------------------------------------------------

def generate_derivatives(count=450):
    exercises = []
    per_sub = count // 4

    # --- Power rule: (x^n)' = n*x^(n-1) ---
    for _ in range(per_sub):
        n = random.randint(2, 12)
        a = random.choice([i for i in range(-8, 9) if i != 0])
        preamble = random.choice(DERIV_PREAMBLES)
        f_str = f"{a}x^{n}" if abs(a) != 1 else (f"x^{n}" if a == 1 else f"-x^{n}")
        deriv_coeff = a * n
        deriv_exp = n - 1
        if deriv_exp == 1:
            deriv_str = f"{deriv_coeff}x" if abs(deriv_coeff) != 1 else ("x" if deriv_coeff == 1 else "-x")
        else:
            deriv_str = f"{deriv_coeff}x^{deriv_exp}" if abs(deriv_coeff) != 1 else (
                f"x^{deriv_exp}" if deriv_coeff == 1 else f"-x^{deriv_exp}"
            )
        question = f"{preamble}{f_str}"
        steps = [
            f"f(x) = {f_str}",
            f"Aplicam regula puterii: (ax^n)' = a*n*x^(n-1)",
            f"f'(x) = {a}*{n}*x^({n}-1) = {deriv_str}",
        ]
        exercises.append({
            "question": question,
            "answer": f"f'(x) = {deriv_str}",
            "type": "derivative",
            "steps": steps,
            "latex": f"f(x) = {f_str}, \\; f'(x) = ?",
            "difficulty": 1,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Sum rule: polynomial derivatives ---
    for _ in range(per_sub):
        deg = random.randint(2, 4)
        coeffs = [random.choice([i for i in range(-6, 7) if i != 0])]
        for _ in range(deg):
            coeffs.append(random.randint(-10, 10))
        f_str = _poly_str(coeffs)
        # derivative coefficients
        d_coeffs = []
        for i, c in enumerate(coeffs):
            power = deg - i
            if power > 0:
                d_coeffs.append(c * power)
        d_str = _poly_str(d_coeffs)
        preamble = random.choice(DERIV_PREAMBLES)
        question = f"{preamble}{f_str}"
        steps = [
            f"f(x) = {f_str}",
            "Derivam termen cu termen:",
        ]
        for i, c in enumerate(coeffs):
            power = deg - i
            if power > 0:
                steps.append(f"  ({c}x^{power})' = {c * power}x^{power - 1}" if power - 1 > 0
                             else f"  ({c}x)' = {c}")
            else:
                steps.append(f"  ({c})' = 0")
        steps.append(f"f'(x) = {d_str}")
        exercises.append({
            "question": question,
            "answer": f"f'(x) = {d_str}",
            "type": "derivative",
            "steps": steps,
            "latex": f"f(x) = {f_str}",
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Product rule: (uv)' = u'v + uv' with simple u,v ---
    for _ in range(per_sub):
        a = random.choice([i for i in range(-5, 6) if i != 0])
        b = random.randint(-8, 8)
        c = random.choice([i for i in range(-5, 6) if i != 0])
        d = random.randint(-8, 8)
        u_str = _poly_str([a, b])
        v_str = _poly_str([c, d])
        f_str = f"({u_str})({v_str})"
        # (ax+b)(cx+d) = acx^2 + (ad+bc)x + bd
        p = a * c
        q = a * d + b * c
        r = b * d
        expanded = _poly_str([p, q, r])
        dp = 2 * p
        dq = q
        deriv_str = _poly_str([dp, dq])
        preamble = random.choice(DERIV_PREAMBLES)
        question = f"{preamble}{f_str}"
        steps = [
            f"f(x) = {f_str}",
            f"Metoda 1: Desfacem produsul: f(x) = {expanded}",
            f"f'(x) = {deriv_str}",
            f"Metoda 2 (regula produsului): f'(x) = u'v + uv' = {a}*({v_str}) + ({u_str})*{c}",
            f"f'(x) = {deriv_str}",
        ]
        exercises.append({
            "question": question,
            "answer": f"f'(x) = {deriv_str}",
            "type": "derivative",
            "steps": steps,
            "latex": f"f(x) = ({u_str})({v_str})",
            "difficulty": 3,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Derivative at a point ---
    for _ in range(count - 3 * per_sub):
        a = random.choice([i for i in range(-5, 6) if i != 0])
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
        k = random.randint(-5, 5)
        f_str = _poly_str([a, b, c])
        dp = 2 * a * k + b
        preamble = random.choice(DERIV_PREAMBLES)
        question = f"{preamble}{f_str}. Calculati f'({k})."
        steps = [
            f"f(x) = {f_str}",
            f"f'(x) = {_poly_str([2 * a, b])}",
            f"f'({k}) = {2 * a}*({k}) + ({b}) = {dp}",
        ]
        exercises.append({
            "question": question,
            "answer": f"f'({k}) = {dp}",
            "type": "derivative",
            "steps": steps,
            "latex": f"f(x) = {f_str}, \\; f'({k}) = ?",
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    return exercises


# ---------------------------------------------------------------------------
# 4. Limits
# ---------------------------------------------------------------------------

def generate_limits(count=450):
    exercises = []
    per_sub = count // 3

    # --- lim(x->a) polynomial (direct substitution) ---
    for _ in range(per_sub):
        a_coeff = random.choice([i for i in range(-4, 5) if i != 0])
        b_coeff = random.randint(-8, 8)
        c_coeff = random.randint(-8, 8)
        pt = random.randint(-5, 5)
        result = a_coeff * pt * pt + b_coeff * pt + c_coeff
        f_str = _poly_str([a_coeff, b_coeff, c_coeff])
        preamble = random.choice(LIMIT_PREAMBLES)
        question = f"{preamble} lim(x->{pt}) ({f_str})"
        steps = [
            f"f(x) = {f_str}",
            f"Limita unui polinom in x = {pt} se calculeaza prin substitutie directa.",
            f"f({pt}) = {a_coeff}*({pt})^2 + ({b_coeff})*({pt}) + ({c_coeff}) = {result}",
        ]
        exercises.append({
            "question": question,
            "answer": str(result),
            "type": "limit",
            "steps": steps,
            "latex": f"\\lim_{{x \\to {pt}}} ({f_str})",
            "difficulty": 1,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- lim(x->inf) rational function (compare degrees) ---
    for _ in range(per_sub):
        # numerator and denominator degrees
        deg_num = random.randint(1, 3)
        deg_den = random.randint(1, 3)
        a_n = random.choice([i for i in range(-5, 6) if i != 0])
        b_m = random.choice([i for i in range(-5, 6) if i != 0])
        # build display strings
        num_coeffs = [a_n] + [random.randint(-4, 4) for _ in range(deg_num)]
        den_coeffs = [b_m] + [random.randint(-4, 4) for _ in range(deg_den)]
        num_str = _poly_str(num_coeffs)
        den_str = _poly_str(den_coeffs)
        if deg_num > deg_den:
            sign = "+" if (a_n > 0) == (b_m > 0) else "-"
            result = f"{sign}inf"
            expl = "Gradul numaratorului > gradul numitorului, limita este infinit."
        elif deg_num < deg_den:
            result = "0"
            expl = "Gradul numaratorului < gradul numitorului, limita este 0."
        else:
            frac = Fraction(a_n, b_m)
            result = str(frac)
            expl = f"Gradele sunt egale, limita = coeficientul dominant al numaratorului / coeficientul dominant al numitorului = {a_n}/{b_m} = {frac}."
        preamble = random.choice(LIMIT_PREAMBLES)
        question = f"{preamble} lim(x->inf) ({num_str}) / ({den_str})"
        steps = [
            f"Numarator: {num_str} (grad {deg_num})",
            f"Numitor: {den_str} (grad {deg_den})",
            expl,
            f"Limita = {result}",
        ]
        exercises.append({
            "question": question,
            "answer": str(result),
            "type": "limit",
            "steps": steps,
            "latex": f"\\lim_{{x \\to \\infty}} \\frac{{{num_str}}}{{{den_str}}}",
            "difficulty": 3,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- lim(x->0) sin(x)/x = 1 and variations ---
    for _ in range(count - 2 * per_sub):
        a = random.choice([i for i in range(-8, 9) if i != 0])
        b = random.choice([i for i in range(-8, 9) if i != 0])
        # lim(x->0) sin(ax)/(bx) = a/b
        frac = Fraction(a, b)
        preamble = random.choice(LIMIT_PREAMBLES)
        question = f"{preamble} lim(x->0) sin({a}x) / ({b}x)"
        steps = [
            f"Folosim limita fundamentala: lim(t->0) sin(t)/t = 1",
            f"sin({a}x)/({b}x) = ({a}/{b}) * sin({a}x)/({a}x)",
            f"Cand x->0, sin({a}x)/({a}x) -> 1",
            f"Limita = {a}/{b} = {frac}",
        ]
        exercises.append({
            "question": question,
            "answer": str(frac),
            "type": "limit",
            "steps": steps,
            "latex": f"\\lim_{{x \\to 0}} \\frac{{\\sin({a}x)}}{{{b}x}}",
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    return exercises


# ---------------------------------------------------------------------------
# 5. Integrals
# ---------------------------------------------------------------------------

def generate_integrals(count=450):
    exercises = []
    per_sub = count // 3

    # --- Power rule: int x^n dx ---
    for _ in range(per_sub):
        n = random.randint(1, 8)
        a = random.choice([i for i in range(-6, 7) if i != 0])
        f_str = f"{a}x^{n}" if abs(a) != 1 else (f"x^{n}" if a == 1 else f"-x^{n}")
        new_exp = n + 1
        frac = Fraction(a, new_exp)
        if frac.denominator == 1:
            result_str = f"{frac.numerator}x^{new_exp}"
        else:
            result_str = f"({frac})x^{new_exp}"
        preamble = random.choice(INTEGRAL_PREAMBLES)
        question = f"{preamble} integral din {f_str} dx"
        steps = [
            f"Aplicam formula: integral din ax^n dx = a*x^(n+1)/(n+1) + C",
            f"integral din {f_str} dx = {a}*x^{new_exp}/{new_exp} + C",
            f"= {result_str} + C",
        ]
        exercises.append({
            "question": question,
            "answer": f"{result_str} + C",
            "type": "integral",
            "steps": steps,
            "latex": f"\\int {f_str} \\, dx",
            "difficulty": 1,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Polynomial integral ---
    for _ in range(per_sub):
        deg = random.randint(2, 3)
        coeffs = [random.choice([i for i in range(-5, 6) if i != 0])]
        for _ in range(deg):
            coeffs.append(random.randint(-8, 8))
        f_str = _poly_str(coeffs)
        # integrate each term
        int_parts = []
        int_steps = []
        for i, c in enumerate(coeffs):
            power = deg - i
            new_p = power + 1
            frac = Fraction(c, new_p)
            if frac.denominator == 1:
                token = f"{frac.numerator}x^{new_p}" if new_p > 1 else f"{frac.numerator}x"
            else:
                token = f"({frac})x^{new_p}" if new_p > 1 else f"({frac})x"
            int_parts.append(token)
            int_steps.append(f"  integral din {c}x^{power} dx = {token}")
        int_result = " + ".join(int_parts) + " + C"
        preamble = random.choice(INTEGRAL_PREAMBLES)
        question = f"{preamble} integral din ({f_str}) dx"
        steps = [
            f"f(x) = {f_str}",
            "Integram termen cu termen:",
        ] + int_steps + [f"Rezultat: {int_result}"]
        exercises.append({
            "question": question,
            "answer": int_result,
            "type": "integral",
            "steps": steps,
            "latex": f"\\int ({f_str}) \\, dx",
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Definite integrals ---
    for _ in range(count - 2 * per_sub):
        a_coeff = random.choice([i for i in range(-4, 5) if i != 0])
        b_coeff = random.randint(-6, 6)
        lo = random.randint(-3, 2)
        hi = lo + random.randint(1, 5)
        # integral of ax+b from lo to hi = a/2*(hi^2-lo^2) + b*(hi-lo)
        result_num = a_coeff * (hi * hi - lo * lo)
        result_den = 2
        result_add = b_coeff * (hi - lo)
        total = Fraction(result_num, result_den) + Fraction(result_add)
        f_str = _poly_str([a_coeff, b_coeff])
        preamble = random.choice(INTEGRAL_PREAMBLES)
        question = f"{preamble} integral de la {lo} la {hi} din ({f_str}) dx"
        frac_a = Fraction(a_coeff, 2)
        antideriv = f"({frac_a})x^2 + ({b_coeff})x" if frac_a.denominator != 1 else f"{frac_a.numerator}x^2 + ({b_coeff})x" if frac_a.numerator != 0 else f"({b_coeff})x"
        # evaluate
        val_hi = Fraction(a_coeff, 2) * hi * hi + b_coeff * hi
        val_lo = Fraction(a_coeff, 2) * lo * lo + b_coeff * lo
        steps = [
            f"Calculam primitiva: F(x) = {antideriv}",
            f"F({hi}) = {val_hi}",
            f"F({lo}) = {val_lo}",
            f"Integrala = F({hi}) - F({lo}) = {val_hi} - ({val_lo}) = {total}",
        ]
        exercises.append({
            "question": question,
            "answer": str(total),
            "type": "integral",
            "steps": steps,
            "latex": f"\\int_{{{lo}}}^{{{hi}}} ({f_str}) \\, dx",
            "difficulty": 3,
            "source": "generated",
            "profile": "BOTH",
        })

    return exercises


# ---------------------------------------------------------------------------
# 6. Matrices
# ---------------------------------------------------------------------------

def generate_matrices(count=450):
    exercises = []
    per_sub = count // 4

    # --- 2x2 addition ---
    for _ in range(per_sub):
        A = [[random.randint(-10, 10) for _ in range(2)] for _ in range(2)]
        B = [[random.randint(-10, 10) for _ in range(2)] for _ in range(2)]
        C = [[A[i][j] + B[i][j] for j in range(2)] for i in range(2)]
        question = (
            f"Calculati A + B, unde A = [[{A[0][0]}, {A[0][1]}], [{A[1][0]}, {A[1][1]}]] "
            f"si B = [[{B[0][0]}, {B[0][1]}], [{B[1][0]}, {B[1][1]}]]."
        )
        answer = f"[[{C[0][0]}, {C[0][1]}], [{C[1][0]}, {C[1][1]}]]"
        steps = [
            f"A = [[{A[0][0]}, {A[0][1]}], [{A[1][0]}, {A[1][1]}]]",
            f"B = [[{B[0][0]}, {B[0][1]}], [{B[1][0]}, {B[1][1]}]]",
            "Adunam element cu element:",
            f"A + B = [[{A[0][0]}+{B[0][0]}, {A[0][1]}+{B[0][1]}], [{A[1][0]}+{B[1][0]}, {A[1][1]}+{B[1][1]}]]",
            f"= {answer}",
        ]
        exercises.append({
            "question": question,
            "answer": answer,
            "type": "matrix",
            "steps": steps,
            "latex": f"A + B",
            "difficulty": 1,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- 2x2 multiplication ---
    for _ in range(per_sub):
        A = [[random.randint(-5, 5) for _ in range(2)] for _ in range(2)]
        B = [[random.randint(-5, 5) for _ in range(2)] for _ in range(2)]
        C = [
            [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
            [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]],
        ]
        question = (
            f"Calculati A * B, unde A = [[{A[0][0]}, {A[0][1]}], [{A[1][0]}, {A[1][1]}]] "
            f"si B = [[{B[0][0]}, {B[0][1]}], [{B[1][0]}, {B[1][1]}]]."
        )
        answer = f"[[{C[0][0]}, {C[0][1]}], [{C[1][0]}, {C[1][1]}]]"
        steps = [
            f"A = [[{A[0][0]}, {A[0][1]}], [{A[1][0]}, {A[1][1]}]]",
            f"B = [[{B[0][0]}, {B[0][1]}], [{B[1][0]}, {B[1][1]}]]",
            f"C[0][0] = {A[0][0]}*{B[0][0]} + {A[0][1]}*{B[1][0]} = {C[0][0]}",
            f"C[0][1] = {A[0][0]}*{B[0][1]} + {A[0][1]}*{B[1][1]} = {C[0][1]}",
            f"C[1][0] = {A[1][0]}*{B[0][0]} + {A[1][1]}*{B[1][0]} = {C[1][0]}",
            f"C[1][1] = {A[1][0]}*{B[0][1]} + {A[1][1]}*{B[1][1]} = {C[1][1]}",
            f"A * B = {answer}",
        ]
        exercises.append({
            "question": question,
            "answer": answer,
            "type": "matrix",
            "steps": steps,
            "latex": f"A \\cdot B",
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- 2x2 determinant ---
    for _ in range(per_sub):
        A = [[random.randint(-10, 10) for _ in range(2)] for _ in range(2)]
        det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
        question = f"Calculati determinantul matricei A = [[{A[0][0]}, {A[0][1]}], [{A[1][0]}, {A[1][1]}]]."
        steps = [
            f"A = [[{A[0][0]}, {A[0][1]}], [{A[1][0]}, {A[1][1]}]]",
            f"det(A) = {A[0][0]}*{A[1][1]} - {A[0][1]}*{A[1][0]}",
            f"det(A) = {A[0][0] * A[1][1]} - {A[0][1] * A[1][0]} = {det}",
        ]
        exercises.append({
            "question": question,
            "answer": f"det(A) = {det}",
            "type": "matrix",
            "steps": steps,
            "latex": f"\\det(A)",
            "difficulty": 1,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Find inverse of 2x2 ---
    for _ in range(count - 3 * per_sub):
        # ensure invertible
        while True:
            A = [[random.randint(-5, 5) for _ in range(2)] for _ in range(2)]
            det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
            if det != 0:
                break
        # inverse = 1/det * [[d, -b], [-c, a]]
        inv_entries = [
            [Fraction(A[1][1], det), Fraction(-A[0][1], det)],
            [Fraction(-A[1][0], det), Fraction(A[0][0], det)],
        ]
        inv_str = f"[[{inv_entries[0][0]}, {inv_entries[0][1]}], [{inv_entries[1][0]}, {inv_entries[1][1]}]]"
        question = f"Gasiti inversa matricei A = [[{A[0][0]}, {A[0][1]}], [{A[1][0]}, {A[1][1]}]]."
        steps = [
            f"det(A) = {A[0][0]}*{A[1][1]} - {A[0][1]}*{A[1][0]} = {det}",
            f"A^(-1) = (1/{det}) * [[{A[1][1]}, {-A[0][1]}], [{-A[1][0]}, {A[0][0]}]]",
            f"A^(-1) = {inv_str}",
        ]
        exercises.append({
            "question": question,
            "answer": f"A^(-1) = {inv_str}",
            "type": "matrix",
            "steps": steps,
            "latex": f"A^{{-1}}",
            "difficulty": 3,
            "source": "generated",
            "profile": "BOTH",
        })

    return exercises


# ---------------------------------------------------------------------------
# 7. Vectors
# ---------------------------------------------------------------------------

def generate_vectors(count=450):
    exercises = []
    per_sub = count // 3

    # --- Addition and scalar multiplication ---
    for _ in range(per_sub):
        dim = random.choice([2, 3])
        u = [random.randint(-10, 10) for _ in range(dim)]
        v = [random.randint(-10, 10) for _ in range(dim)]
        op = random.choice(["add", "scalar"])
        if op == "add":
            result = [u[i] + v[i] for i in range(dim)]
            question = f"Calculati u + v, unde u = {u} si v = {v}."
            answer = str(result)
            steps = [
                f"u = {u}, v = {v}",
                "Adunam componenta cu componenta:",
                f"u + v = {result}",
            ]
            diff = 1
        else:
            k = random.choice([i for i in range(-5, 6) if i != 0])
            result = [k * u[i] for i in range(dim)]
            question = f"Calculati {k} * u, unde u = {u}."
            answer = str(result)
            steps = [
                f"u = {u}, k = {k}",
                "Inmultim fiecare componenta cu k:",
                f"{k} * u = {result}",
            ]
            diff = 1
        exercises.append({
            "question": question,
            "answer": answer,
            "type": "vector",
            "steps": steps,
            "latex": "",
            "difficulty": diff,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Dot product ---
    for _ in range(per_sub):
        dim = random.choice([2, 3])
        u = [random.randint(-8, 8) for _ in range(dim)]
        v = [random.randint(-8, 8) for _ in range(dim)]
        dot = sum(u[i] * v[i] for i in range(dim))
        question = f"Calculati produsul scalar u . v, unde u = {u} si v = {v}."
        prods = " + ".join(f"{u[i]}*{v[i]}" for i in range(dim))
        steps = [
            f"u = {u}, v = {v}",
            f"u . v = {prods}",
            f"u . v = {dot}",
        ]
        exercises.append({
            "question": question,
            "answer": f"u . v = {dot}",
            "type": "vector",
            "steps": steps,
            "latex": f"\\vec{{u}} \\cdot \\vec{{v}} = {dot}",
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Magnitude / norm ---
    for _ in range(count - 2 * per_sub):
        dim = random.choice([2, 3])
        u = [random.randint(-8, 8) for _ in range(dim)]
        sq_sum = sum(x * x for x in u)
        mag = math.sqrt(sq_sum)
        mag_str = f"sqrt({sq_sum})"
        if int(mag) ** 2 == sq_sum:
            mag_str = str(int(mag))
        question = f"Calculati norma (modulul) vectorului u = {u}."
        steps = [
            f"u = {u}",
            f"||u|| = sqrt({' + '.join(f'{x}^2' for x in u)})",
            f"||u|| = sqrt({sq_sum}) = {mag_str}",
        ]
        exercises.append({
            "question": question,
            "answer": f"||u|| = {mag_str}",
            "type": "vector",
            "steps": steps,
            "latex": f"||\\vec{{u}}|| = {mag_str}",
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    return exercises


# ---------------------------------------------------------------------------
# 8. Combinatorics
# ---------------------------------------------------------------------------

def generate_combinatorics(count=450):
    exercises = []
    per_sub = count // 4

    # --- C(n,k) ---
    for _ in range(per_sub):
        n = random.randint(3, 15)
        k = random.randint(0, n)
        result = _comb(n, k)
        question = f"Calculati C({n},{k})."
        steps = [
            f"C(n,k) = n! / (k! * (n-k)!)",
            f"C({n},{k}) = {n}! / ({k}! * {n - k}!)",
            f"C({n},{k}) = {result}",
        ]
        exercises.append({
            "question": question,
            "answer": f"C({n},{k}) = {result}",
            "type": "combinatorics",
            "steps": steps,
            "latex": f"C_{{{n}}}^{{{k}}} = {result}",
            "difficulty": 1,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- A(n,k) ---
    for _ in range(per_sub):
        n = random.randint(3, 12)
        k = random.randint(1, min(n, 6))
        result = _perm(n, k)
        question = f"Calculati A({n},{k}) (aranjamente)."
        steps = [
            f"A(n,k) = n! / (n-k)!",
            f"A({n},{k}) = {n}! / {n - k}!",
            f"A({n},{k}) = {result}",
        ]
        exercises.append({
            "question": question,
            "answer": f"A({n},{k}) = {result}",
            "type": "combinatorics",
            "steps": steps,
            "latex": f"A_{{{n}}}^{{{k}}} = {result}",
            "difficulty": 1,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- P(n) = n! ---
    for _ in range(per_sub):
        n = random.randint(1, 10)
        result = _factorial(n)
        question = f"Calculati P({n}) = {n}! (permutari)."
        steps = [
            f"P(n) = n!",
            f"P({n}) = {n}! = {result}",
        ]
        exercises.append({
            "question": question,
            "answer": f"P({n}) = {result}",
            "type": "combinatorics",
            "steps": steps,
            "latex": f"P_{{{n}}} = {n}! = {result}",
            "difficulty": 1,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Simple counting / word problems ---
    for _ in range(count - 3 * per_sub):
        problem_type = random.choice(["comitet", "echipa", "numere"])
        if problem_type == "comitet":
            n = random.randint(5, 15)
            k = random.randint(2, min(n, 5))
            result = _comb(n, k)
            question = f"In cate moduri se poate forma un comitet de {k} persoane din {n} candidati?"
            steps = [
                f"Ordinea nu conteaza => combinari",
                f"C({n},{k}) = {n}! / ({k}! * {n-k}!) = {result}",
            ]
            answer = str(result)
        elif problem_type == "echipa":
            n = random.randint(5, 12)
            k = random.randint(2, min(n, 4))
            result = _perm(n, k)
            question = (
                f"In cate moduri se pot alege si aranja {k} persoane din {n} "
                f"pentru {k} pozitii distincte?"
            )
            steps = [
                f"Ordinea conteaza => aranjamente",
                f"A({n},{k}) = {n}! / {n-k}! = {result}",
            ]
            answer = str(result)
        else:
            digits = random.randint(3, 5)
            result = 9 * (10 ** (digits - 1))
            question = f"Cate numere naturale de {digits} cifre exista?"
            steps = [
                f"Prima cifra: 9 posibilitati (1-9)",
                f"Celelalte {digits - 1} cifre: 10 posibilitati fiecare",
                f"Total: 9 * 10^{digits - 1} = {result}",
            ]
            answer = str(result)
        exercises.append({
            "question": question,
            "answer": answer,
            "type": "combinatorics",
            "steps": steps,
            "latex": "",
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    return exercises


# ---------------------------------------------------------------------------
# 9. Probability
# ---------------------------------------------------------------------------

def generate_probability(count=450):
    exercises = []
    per_sub = count // 3

    # --- Dice problems ---
    for _ in range(per_sub):
        n_dice = random.choice([1, 2])
        if n_dice == 1:
            targets = sorted(random.sample(range(1, 7), random.randint(1, 4)))
            favorable = len(targets)
            total = 6
            frac = Fraction(favorable, total)
            targets_str = ", ".join(str(t) for t in targets)
            question = f"Se arunca un zar. Care este probabilitatea sa obtinem una din valorile {{{targets_str}}}?"
            steps = [
                f"Cazuri totale: {total}",
                f"Cazuri favorabile: {favorable} (valorile {targets_str})",
                f"P = {favorable}/{total} = {frac}",
            ]
        else:
            target_sum = random.randint(2, 12)
            # count pairs (i,j) with i+j = target_sum, 1<=i,j<=6
            favorable = sum(1 for i in range(1, 7) for j in range(1, 7) if i + j == target_sum)
            total = 36
            frac = Fraction(favorable, total)
            question = f"Se arunca doua zaruri. Care este probabilitatea ca suma sa fie {target_sum}?"
            steps = [
                f"Cazuri totale: {total}",
                f"Cazuri favorabile (perechi cu suma {target_sum}): {favorable}",
                f"P = {favorable}/{total} = {frac}",
            ]
        exercises.append({
            "question": question,
            "answer": f"P = {frac}",
            "type": "probability",
            "steps": steps,
            "latex": f"P = {frac}",
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Coin problems ---
    for _ in range(per_sub):
        n_coins = random.randint(2, 5)
        k_heads = random.randint(0, n_coins)
        total = 2 ** n_coins
        favorable = _comb(n_coins, k_heads)
        frac = Fraction(favorable, total)
        question = (
            f"Se arunca {n_coins} monede. Care este probabilitatea "
            f"sa obtinem exact {k_heads} steme?"
        )
        steps = [
            f"Cazuri totale: 2^{n_coins} = {total}",
            f"Cazuri favorabile: C({n_coins},{k_heads}) = {favorable}",
            f"P = {favorable}/{total} = {frac}",
        ]
        exercises.append({
            "question": question,
            "answer": f"P = {frac}",
            "type": "probability",
            "steps": steps,
            "latex": f"P = {frac}",
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Card / urn problems ---
    for _ in range(count - 2 * per_sub):
        problem_type = random.choice(["bile", "carti"])
        if problem_type == "bile":
            red = random.randint(2, 10)
            blue = random.randint(2, 10)
            total = red + blue
            # pick one ball, probability red
            frac = Fraction(red, total)
            question = (
                f"O urna contine {red} bile rosii si {blue} bile albastre. "
                f"Se extrage o bila la intamplare. Care este probabilitatea sa fie rosie?"
            )
            steps = [
                f"Bile totale: {total}",
                f"Bile rosii: {red}",
                f"P(rosie) = {red}/{total} = {frac}",
            ]
        else:
            # simple card problem from 52 cards
            suit_count = 13
            total = 52
            k = random.choice([1, 2, 4, 13, 26])
            labels = {1: "asul de pica", 2: "un as rosu", 4: "un as",
                      13: "o carte de inima", 26: "o carte rosie"}
            label = labels[k]
            frac = Fraction(k, total)
            question = (
                f"Dintr-un pachet de 52 de carti se extrage una. "
                f"Care este probabilitatea sa fie {label}?"
            )
            steps = [
                f"Cazuri totale: {total}",
                f"Cazuri favorabile: {k}",
                f"P = {k}/{total} = {frac}",
            ]
        exercises.append({
            "question": question,
            "answer": f"P = {frac}",
            "type": "probability",
            "steps": steps,
            "latex": f"P = {frac}",
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    return exercises


# ---------------------------------------------------------------------------
# 10. Geometry
# ---------------------------------------------------------------------------

def generate_geometry(count=450):
    exercises = []
    per_sub = count // 5

    # --- Distance between 2 points ---
    for _ in range(per_sub):
        x1, y1 = random.randint(-10, 10), random.randint(-10, 10)
        x2, y2 = random.randint(-10, 10), random.randint(-10, 10)
        dx, dy = x2 - x1, y2 - y1
        sq = dx * dx + dy * dy
        dist = math.sqrt(sq)
        dist_str = f"sqrt({sq})"
        if int(dist) ** 2 == sq:
            dist_str = str(int(dist))
        question = f"Calculati distanta dintre punctele A({x1}, {y1}) si B({x2}, {y2})."
        steps = [
            f"d = sqrt((x2-x1)^2 + (y2-y1)^2)",
            f"d = sqrt(({x2}-{x1})^2 + ({y2}-{y1})^2)",
            f"d = sqrt({dx}^2 + {dy}^2) = sqrt({sq}) = {dist_str}",
        ]
        exercises.append({
            "question": question,
            "answer": f"d = {dist_str}",
            "type": "geometry",
            "steps": steps,
            "latex": f"d(A,B) = {dist_str}",
            "difficulty": 1,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Midpoint ---
    for _ in range(per_sub):
        x1, y1 = random.randint(-10, 10), random.randint(-10, 10)
        x2, y2 = random.randint(-10, 10), random.randint(-10, 10)
        mx = Fraction(x1 + x2, 2)
        my = Fraction(y1 + y2, 2)
        question = f"Gasiti mijlocul segmentului AB, cu A({x1}, {y1}) si B({x2}, {y2})."
        steps = [
            f"M = ((x1+x2)/2, (y1+y2)/2)",
            f"M = (({x1}+{x2})/2, ({y1}+{y2})/2)",
            f"M = ({mx}, {my})",
        ]
        exercises.append({
            "question": question,
            "answer": f"M = ({mx}, {my})",
            "type": "geometry",
            "steps": steps,
            "latex": f"M = ({mx}, {my})",
            "difficulty": 1,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Slope of line through 2 points ---
    for _ in range(per_sub):
        x1, y1 = random.randint(-10, 10), random.randint(-10, 10)
        x2 = x1
        while x2 == x1:
            x2 = random.randint(-10, 10)
        y2 = random.randint(-10, 10)
        slope = Fraction(y2 - y1, x2 - x1)
        question = (
            f"Calculati panta dreptei care trece prin A({x1}, {y1}) si B({x2}, {y2})."
        )
        steps = [
            f"m = (y2 - y1) / (x2 - x1)",
            f"m = ({y2} - {y1}) / ({x2} - {x1}) = {y2 - y1}/{x2 - x1} = {slope}",
        ]
        exercises.append({
            "question": question,
            "answer": f"m = {slope}",
            "type": "geometry",
            "steps": steps,
            "latex": f"m = {slope}",
            "difficulty": 1,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Equation of line through 2 points ---
    for _ in range(per_sub):
        x1, y1 = random.randint(-8, 8), random.randint(-8, 8)
        x2 = x1
        while x2 == x1:
            x2 = random.randint(-8, 8)
        y2 = random.randint(-8, 8)
        m = Fraction(y2 - y1, x2 - x1)
        # y - y1 = m(x - x1) => y = mx - m*x1 + y1
        b_val = -m * x1 + y1
        if m.denominator == 1:
            m_disp = str(m.numerator)
        else:
            m_disp = f"({m})"
        eq = f"y = {m_disp}x {'+' if b_val >= 0 else '-'} {abs(b_val)}" if b_val != 0 else f"y = {m_disp}x"
        question = (
            f"Scrieti ecuatia dreptei care trece prin A({x1}, {y1}) si B({x2}, {y2})."
        )
        steps = [
            f"Panta: m = ({y2}-{y1})/({x2}-{x1}) = {m}",
            f"Ecuatia: y - {y1} = {m}(x - {x1})",
            f"y = {m}x + ({-m * x1 + y1})",
            f"{eq}",
        ]
        exercises.append({
            "question": question,
            "answer": eq,
            "type": "geometry",
            "steps": steps,
            "latex": eq,
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Circle equations ---
    for _ in range(count - 4 * per_sub):
        h = random.randint(-8, 8)
        k = random.randint(-8, 8)
        r = random.randint(1, 10)
        question = (
            f"Scrieti ecuatia cercului cu centrul C({h}, {k}) si raza r = {r}."
        )
        eq = f"(x - {h})^2 + (y - {k})^2 = {r * r}"
        # expanded form
        steps = [
            f"Centru: C({h}, {k}), raza: r = {r}",
            f"Ecuatia: (x - {h})^2 + (y - {k})^2 = {r}^2",
            f"{eq}",
        ]
        exercises.append({
            "question": question,
            "answer": eq,
            "type": "geometry",
            "steps": steps,
            "latex": f"(x - {h})^2 + (y - {k})^2 = {r**2}",
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    return exercises


# ---------------------------------------------------------------------------
# 11. Sequences
# ---------------------------------------------------------------------------

def generate_sequences(count=450):
    exercises = []
    per_sub = count // 4

    # --- Arithmetic: find a_n ---
    for _ in range(per_sub):
        a1 = random.randint(-10, 20)
        d = random.choice([i for i in range(-8, 9) if i != 0])
        n = random.randint(2, 30)
        a_n = a1 + (n - 1) * d
        question = (
            f"Intr-o progresie aritmetica, a1 = {a1} si ratia d = {d}. "
            f"Calculati a_{n}."
        )
        steps = [
            f"a_n = a1 + (n-1)*d",
            f"a_{n} = {a1} + ({n}-1)*{d} = {a1} + {(n-1)*d} = {a_n}",
        ]
        exercises.append({
            "question": question,
            "answer": f"a_{n} = {a_n}",
            "type": "sequence",
            "steps": steps,
            "latex": f"a_{{{n}}} = {a_n}",
            "difficulty": 1,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Arithmetic: find S_n ---
    for _ in range(per_sub):
        a1 = random.randint(-5, 15)
        d = random.choice([i for i in range(-5, 6) if i != 0])
        n = random.randint(3, 20)
        a_n = a1 + (n - 1) * d
        s_n = n * (a1 + a_n) // 2 if (n * (a1 + a_n)) % 2 == 0 else Fraction(n * (a1 + a_n), 2)
        question = (
            f"Intr-o progresie aritmetica, a1 = {a1} si ratia d = {d}. "
            f"Calculati S_{n} (suma primilor {n} termeni)."
        )
        steps = [
            f"a_{n} = {a1} + ({n}-1)*{d} = {a_n}",
            f"S_n = n*(a1 + a_n)/2",
            f"S_{n} = {n}*({a1} + {a_n})/2 = {n}*{a1 + a_n}/2 = {s_n}",
        ]
        exercises.append({
            "question": question,
            "answer": f"S_{n} = {s_n}",
            "type": "sequence",
            "steps": steps,
            "latex": f"S_{{{n}}} = {s_n}",
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Geometric: find a_n ---
    for _ in range(per_sub):
        a1 = random.choice([i for i in range(-8, 9) if i != 0])
        r = random.choice([2, 3, -2, -3, Fraction(1, 2), Fraction(1, 3)])
        n = random.randint(2, 8)
        a_n = a1 * r ** (n - 1)
        question = (
            f"Intr-o progresie geometrica, a1 = {a1} si ratia q = {r}. "
            f"Calculati a_{n}."
        )
        steps = [
            f"a_n = a1 * q^(n-1)",
            f"a_{n} = {a1} * {r}^{n - 1} = {a1} * {r ** (n - 1)} = {a_n}",
        ]
        exercises.append({
            "question": question,
            "answer": f"a_{n} = {a_n}",
            "type": "sequence",
            "steps": steps,
            "latex": f"a_{{{n}}} = {a_n}",
            "difficulty": 2,
            "source": "generated",
            "profile": "BOTH",
        })

    # --- Geometric: find S_n ---
    for _ in range(count - 3 * per_sub):
        a1 = random.choice([i for i in range(-5, 6) if i != 0])
        r = random.choice([2, 3, -2])
        n = random.randint(3, 7)
        if r == 1:
            s_n = a1 * n
        else:
            s_n = a1 * (r ** n - 1) // (r - 1) if (a1 * (r ** n - 1)) % (r - 1) == 0 else Fraction(a1 * (r ** n - 1), r - 1)
        question = (
            f"Intr-o progresie geometrica, a1 = {a1} si ratia q = {r}. "
            f"Calculati S_{n} (suma primilor {n} termeni)."
        )
        steps = [
            f"S_n = a1 * (q^n - 1) / (q - 1)  (pentru q != 1)",
            f"S_{n} = {a1} * ({r}^{n} - 1) / ({r} - 1)",
            f"S_{n} = {a1} * ({r ** n} - 1) / {r - 1}",
            f"S_{n} = {a1} * {r ** n - 1} / {r - 1} = {s_n}",
        ]
        exercises.append({
            "question": question,
            "answer": f"S_{n} = {s_n}",
            "type": "sequence",
            "steps": steps,
            "latex": f"S_{{{n}}} = {s_n}",
            "difficulty": 3,
            "source": "generated",
            "profile": "BOTH",
        })

    return exercises


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

GENERATORS = {
    "equation": generate_equations,
    "function": generate_functions,
    "derivative": generate_derivatives,
    "limit": generate_limits,
    "integral": generate_integrals,
    "matrix": generate_matrices,
    "vector": generate_vectors,
    "combinatorics": generate_combinatorics,
    "probability": generate_probability,
    "geometry": generate_geometry,
    "sequence": generate_sequences,
}


def load_existing():
    """Load exercises produced by collect_data.py, if the file exists."""
    if os.path.exists(RAW_PATH):
        with open(RAW_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"Loaded {len(data)} existing exercises from {RAW_PATH}")
        return data
    print(f"No existing data at {RAW_PATH} -- starting from scratch.")
    return []


def main():
    existing = load_existing()

    all_exercises = list(existing)

    # Determine how many to generate per type to exceed 5000
    existing_count = len(existing)
    target_total = 5200
    remaining = max(0, target_total - existing_count)
    n_types = len(GENERATORS)
    per_type = max(300, remaining // n_types + 1)

    print(f"\nExisting exercises : {existing_count}")
    print(f"Target total       : {target_total}")
    print(f"Generating ~{per_type} per type ({n_types} types)\n")

    stats = {}
    for ex_type, gen_func in GENERATORS.items():
        generated = gen_func(count=per_type)
        stats[ex_type] = len(generated)
        all_exercises.extend(generated)
        print(f"  {ex_type:15s} : {len(generated):5d} generated")

    # Assign unique IDs
    for idx, ex in enumerate(all_exercises):
        ex["id"] = f"ex_{idx + 1:05d}"

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_exercises, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"Total exercises    : {len(all_exercises)}")
    print(f"  from raw data    : {len(existing)}")
    print(f"  generated        : {len(all_exercises) - len(existing)}")
    print(f"\nStatistics per type (generated):")
    for t, c in sorted(stats.items()):
        print(f"  {t:15s} : {c:5d}")
    print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
