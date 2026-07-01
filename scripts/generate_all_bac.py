#!/usr/bin/env python3
"""
generate_all_bac.py — Generare completă exerciții BAC Matematică M1 & M2
Target: 2000+ exerciții unice cu rezolvări pas cu pas.
"""
import json, math, os, random, sys
from collections import defaultdict
from fractions import Fraction

random.seed(42)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = os.path.join(ROOT, "data", "bac_complete")
OUT_FILE = os.path.join(OUT_DIR, "bac_all_exercises.json")

# ═══════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════
_SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
def sup(n): return str(n).translate(_SUP)
def sub(n): return str(n).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))

def fs(f):
    if isinstance(f, Fraction):
        return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"
    if isinstance(f, float):
        return str(int(f)) if f == int(f) else f"{f:.4g}"
    return str(f)

def ps(terms, var='x'):
    ts = sorted([(c, p) for c, p in terms if c != 0], key=lambda x: -x[1])
    if not ts: return "0"
    parts = []
    for i, (c, p) in enumerate(ts):
        ac = abs(c) if not isinstance(c, Fraction) else abs(c)
        if p == 0: t = fs(ac)
        elif p == 1: t = var if ac == 1 else f"{fs(ac)}{var}"
        else: t = f"{var}{sup(p)}" if ac == 1 else f"{fs(ac)}{var}{sup(p)}"
        neg = c < 0
        if i == 0: parts.append(f"-{t}" if neg else t)
        else: parts.append(f" - {t}" if neg else f" + {t}")
    return "".join(parts)

def deriv(terms):
    return [(c * p, p - 1) for c, p in terms if p > 0]

def antideriv(terms):
    return [(Fraction(c, p + 1), p + 1) for c, p in terms]

def eval_poly(terms, x):
    return sum(Fraction(c) * Fraction(x)**p for c, p in terms)

def St(n, action, result, explanation=""):
    return {"step": n, "action": action, "result": str(result), "explanation": explanation}

_ID = [0]
def E(prof, subj, exn, topic, diff, q, ans, steps, hints, formula, mistakes, tags):
    _ID[0] += 1
    return {"id": f"bac_{prof.lower()}_s{subj}_{topic}_{_ID[0]:04d}",
            "year": 2024, "profile": prof, "subject": subj,
            "exercise_number": exn, "topic": topic, "difficulty": diff,
            "question": q, "answer": str(ans), "points": 5,
            "solution_steps": steps, "hints": hints,
            "formula": formula, "common_mistakes": mistakes, "tags": tags}

NZ = [i for i in range(-9, 10) if i != 0]

# ═══════════════════════════════════════
# SUBIECTUL I
# ═══════════════════════════════════════

def gen_multimi(n=80):
    exs, seen = [], set()
    ops = ["∩", "∪", "\\"]
    while len(exs) < n:
        a1 = random.randint(-8, 2); a2 = a1 + random.randint(4, 10)
        b1 = random.randint(a1+1, a2-1); b2 = b1 + random.randint(4, 10)
        la = random.choice(["(","["]); ra = random.choice([")","]"])
        lb = random.choice(["(","["]); rb = random.choice([")","]"])
        op = random.choice(ops)
        key = (a1,a2,b1,b2,la,ra,lb,rb,op)
        if key in seen: continue
        seen.add(key)
        A = f"{la}{a1}, {a2}{ra}"; B = f"{lb}{b1}, {b2}{rb}"
        prof = "M1" if len(exs) % 2 == 0 else "M2"
        if op == "∩":
            left, right = max(a1,b1), min(a2,b2)
            lbr = "[" if ((left==a1 and la=="[") and (left==b1 and lb=="[")) or (left==a1 and la=="[" and left>b1) or (left==b1 and lb=="[" and left>a1) else "("
            if left == a1 and left == b1: lbr = "[" if la=="[" and lb=="[" else "("
            elif left == a1: lbr = la
            else: lbr = lb
            if right == a2 and right == b2: rbr = "]" if ra=="]" and rb=="]" else ")"
            elif right == a2: rbr = ra
            else: rbr = rb
            ans = f"{lbr}{left}, {right}{rbr}"
            q = f"Fie A = {A} și B = {B}. Calculați A ∩ B."
            steps = [St(1,"Identificăm intervalele",f"A = {A}, B = {B}"),
                     St(2,"Intersecția: luăm maximul capetelor stângi și minimul dreptelor",f"max({a1},{b1})={left}, min({a2},{b2})={right}"),
                     St(3,"Determinăm parantezele",ans)]
        elif op == "∪":
            left, right = min(a1,b1), max(a2,b2)
            if left == a1: lbr = la
            elif left == b1: lbr = lb
            else: lbr = la
            if right == a2: rbr = ra
            elif right == b2: rbr = rb
            else: rbr = ra
            ans = f"{lbr}{left}, {right}{rbr}"
            q = f"Fie A = {A} și B = {B}. Calculați A ∪ B."
            steps = [St(1,"Identificăm intervalele",f"A = {A}, B = {B}"),
                     St(2,"Reuniunea: luăm minimul stâng și maximul drept",f"min({a1},{b1})={left}, max({a2},{b2})={right}"),
                     St(3,"Rezultat",ans)]
        else:
            left, right = a1, b1
            lbr, rbr = la, ")" if lb == "[" else "]"
            ans = f"{lbr}{left}, {right}{rbr}" if left < right else "∅"
            q = f"Fie A = {A} și B = {B}. Calculați A \\ B."
            steps = [St(1,"A\\B = elementele din A care nu sunt în B",""),
                     St(2,"Eliminăm partea comună",f"A \\ B = {ans}")]
        exs.append(E(prof,1,1,"multimi",2,q,ans,steps,
                     ["Desenați intervalele pe axa numerelor"],
                     "A∩B, A∪B, A\\B","Confundă intersecția cu reuniunea",["multimi","intervale",op]))
    return exs

def gen_ecuatii_liniare(n=70):
    exs, seen = [], set()
    while len(exs) < n:
        a = random.choice(NZ); b = random.randint(-15,15); c = random.randint(-15,15)
        if (a,b,c) in seen: continue
        seen.add((a,b,c))
        x = Fraction(c-b, a)
        prof = "M1" if len(exs)%2==0 else "M2"
        q = f"Rezolvați ecuația: {ps([(a,1),(b,0)])} = {c}"
        exs.append(E(prof,1,2,"ecuatie_liniara",1,q,f"x = {fs(x)}",
            [St(1,"Izolăm x",f"{a}x = {c} - ({b}) = {c-b}"),
             St(2,"Împărțim",f"x = {c-b}/{a} = {fs(x)}"),
             St(3,"Verificare",f"{a}·({fs(x)}) + {b} = {c} ✓")],
            ["Izolați x în membrul stâng"],"ax+b=c ⟹ x=(c-b)/a",
            ["Greșesc semnul la mutarea termenilor"],["ecuatii","liniare"]))
    return exs

def gen_ecuatii_grad2(n=100):
    exs, seen = [], set()
    while len(exs) < n:
        r1 = random.randint(-8,8); r2 = random.randint(-8,8)
        a = random.choice([1,1,1,2])
        b = -a*(r1+r2); c = a*r1*r2
        if (a,b,c) in seen: continue
        seen.add((a,b,c))
        delta = b*b - 4*a*c
        prof = "M1" if len(exs)%2==0 else "M2"
        poly_str = ps([(a,2),(b,1),(c,0)])
        if r1 == r2:
            ans = f"x₁ = x₂ = {r1}"
        else:
            x1, x2 = min(r1,r2), max(r1,r2)
            ans = f"x₁ = {x1}, x₂ = {x2}"
        exs.append(E(prof,1,2,"ecuatie_grad2",2,
            f"Rezolvați ecuația: {poly_str} = 0", ans,
            [St(1,"Identificăm coeficienții",f"a={a}, b={b}, c={c}"),
             St(2,"Calculăm discriminantul",f"Δ = b²-4ac = {b}²-4·{a}·{c} = {delta}"),
             St(3,"Aplicăm formula",f"x = (-b±√Δ)/(2a) = ({-b}±{int(math.sqrt(delta))})/{2*a}" if delta>=0 else "Δ<0, fără soluții reale"),
             St(4,"Soluțiile",ans)],
            ["Δ = b²-4ac","x = (-b±√Δ)/(2a)"],"ax²+bx+c=0, Δ=b²-4ac",
            ["Greșesc semnul lui b în formulă","Uită să verifice Δ≥0"],
            ["ecuatii","grad2","discriminant"]))
    return exs

def gen_ecuatii_irationale(n=50):
    exs, seen = [], set()
    while len(exs) < n:
        a = random.choice([1,2,3]); b = random.randint(-10,10)
        c = random.randint(1,8)
        x = Fraction(c*c - b, a)
        if x < 0 or (a,b,c) in seen: continue
        seen.add((a,b,c))
        prof = "M1" if len(exs)%2==0 else "M2"
        exs.append(E(prof,1,2,"ecuatie_irationala",2,
            f"Rezolvați ecuația: √({ps([(a,1),(b,0)])}) = {c}",
            f"x = {fs(x)}",
            [St(1,"Ridicăm la pătrat",f"{a}x + {b} = {c}² = {c*c}"),
             St(2,"Izolăm x",f"{a}x = {c*c-b}, x = {fs(x)}"),
             St(3,"Verificare condiție",f"{a}·{fs(x)}+{b} = {c*c} ≥ 0 ✓")],
            ["Ridicați ambii membri la pătrat"],"√(ax+b)=c ⟹ ax+b=c², c≥0",
            ["Uită condiția c≥0","Nu verifică soluția"],["ecuatii","irationale"]))
    return exs

def gen_ecuatii_modul(n=50):
    exs, seen = [], set()
    while len(exs) < n:
        a = random.choice(NZ); b = random.randint(-10,10)
        c = random.randint(1,12)
        if (a,b,c) in seen: continue
        seen.add((a,b,c))
        x1, x2 = Fraction(c-b,a), Fraction(-c-b,a)
        prof = "M1" if len(exs)%2==0 else "M2"
        exs.append(E(prof,1,2,"ecuatie_modul",2,
            f"Rezolvați ecuația: |{ps([(a,1),(b,0)])}| = {c}",
            f"x₁ = {fs(x1)}, x₂ = {fs(x2)}",
            [St(1,"Deschidem modulul",f"{a}x+{b} = {c} sau {a}x+{b} = -{c}"),
             St(2,"Cazul 1",f"x = ({c}-{b})/{a} = {fs(x1)}"),
             St(3,"Cazul 2",f"x = ({-c}-{b})/{a} = {fs(x2)}")],
            ["|expr|=c ⟹ expr=c sau expr=-c"],"|ax+b|=c ⟹ ax+b=±c",
            ["Uită cazul negativ"],["ecuatii","modul"]))
    return exs

def gen_ecuatii_exp(n=60):
    exs, seen = [], set()
    bases = [2,3,5,7,10]
    while len(exs) < n:
        base = random.choice(bases)
        exp = random.randint(1,6)
        val = base**exp
        if (base,exp) in seen: continue
        seen.add((base,exp))
        prof = "M1" if len(exs)%2==0 else "M2"
        exs.append(E(prof,1,2,"ecuatie_exponentiala",2,
            f"Rezolvați ecuația: {base}ˣ = {val}", f"x = {exp}",
            [St(1,"Scriem membrul drept ca putere",f"{val} = {base}{sup(exp)}"),
             St(2,"Egalăm exponenții",f"x = {exp}")],
            [f"Scrieți {val} ca putere a lui {base}"],f"{base}ˣ = {base}ⁿ ⟹ x=n",
            ["Nu recunosc puterea"],["ecuatii","exponentiale"]))
    # Extra: with coefficients
    while len(exs) < n:
        base = random.choice([2,3]); k = random.randint(1,4)
        a = random.choice([2,3,4]); b = random.randint(-5,5)
        val = a * base**k + b
        exs.append(E("M1",1,2,"ecuatie_exponentiala",3,
            f"Rezolvați: {a}·{base}ˣ + {b} = {val}", f"x = {k}",
            [St(1,"Izolăm termenul exponențial",f"{a}·{base}ˣ = {val-b}"),
             St(2,"Împărțim",f"{base}ˣ = {(val-b)//a}"),
             St(3,"Rezolvăm",f"x = {k}")],
            ["Izolați termenul cu baza"],"",["Greșesc la izolare"],["ecuatii","exponentiale"]))
    return exs

def gen_ecuatii_log(n=60):
    exs, seen = [], set()
    while len(exs) < n:
        base = random.choice([2,3,5,10])
        exp = random.randint(1,5)
        val = base**exp
        if (base,val) in seen: continue
        seen.add((base,val))
        prof = "M1" if len(exs)%2==0 else "M2"
        b_str = "" if base == 10 else sub(base)
        exs.append(E(prof,1,2,"ecuatie_logaritmica",2,
            f"Rezolvați ecuația: log{b_str}(x) = {exp}", f"x = {val}",
            [St(1,"Aplicăm definiția logaritmului",f"x = {base}{sup(exp)}"),
             St(2,"Calculăm",f"x = {val}"),
             St(3,"Verificare: x > 0",f"{val} > 0 ✓")],
            ["log_a(x)=b ⟹ x=aᵇ"],f"log_a(x)=b ⟹ x=aᵇ",
            ["Uită condiția x>0"],["ecuatii","logaritmice"]))
    return exs

def gen_inecuatii(n=80):
    exs = []
    # Grade 1
    for v in range(n//2):
        a = random.choice(NZ); b = random.randint(-10,10)
        op = random.choice([">","<","≥","≤"])
        x = Fraction(-b, a)
        if a > 0:
            ans = f"x {op} {fs(x)}" if op in [">","≥"] else f"x {op} {fs(x)}"
        else:
            flipped = {">":"<","<":">","≥":"≤","≤":"≥"}[op]
            ans = f"x {flipped} {fs(x)}"
        prof = "M1" if v%2==0 else "M2"
        exs.append(E(prof,1,2,"inecuatie_grad1",1,
            f"Rezolvați inecuația: {ps([(a,1),(b,0)])} {op} 0", ans,
            [St(1,"Izolăm x",f"{a}x {op} {-b}"),
             St(2,"Împărțim la {a}".format(a=a),f"{'Schimbăm sensul!' if a<0 else ''} x {'<' if (a<0 and op=='>') or (a>0 and op=='<') else '>'} {fs(x)}")],
            ["Izolați x"],"ax+b>0",["Uită să schimbe sensul la împărțire cu negativ"],["inecuatii","grad1"]))
    # Grade 2
    for v in range(n - n//2):
        r1 = random.randint(-5,5); r2 = random.randint(r1+1,r1+6)
        a = 1; b = -(r1+r2); c = r1*r2
        prof = "M1" if v%2==0 else "M2"
        ans_pos = f"x ∈ (-∞, {r1}) ∪ ({r2}, +∞)"
        ans_neg = f"x ∈ ({r1}, {r2})"
        op = random.choice([">0","<0"])
        ans = ans_pos if op == ">0" else ans_neg
        exs.append(E(prof,1,2,"inecuatie_grad2",2,
            f"Rezolvați: {ps([(a,2),(b,1),(c,0)])} {op}",ans,
            [St(1,"Găsim rădăcinile",f"x²+({b})x+{c}=0 → x₁={r1}, x₂={r2}"),
             St(2,"Tabel de semn",f"Polinom pozitiv în afara rădăcinilor"),
             St(3,"Soluția",ans)],
            ["Rezolvați ecuația asociată, apoi tabel semn"],"",
            ["Greșesc sensul inecuației"],["inecuatii","grad2"]))
    return exs

def gen_progresii(n=130):
    exs = []
    # Aritmetice
    for v in range(n//2):
        a1 = random.randint(-5,10); r = random.choice(NZ)
        nv = random.randint(5,20)
        an = a1 + (nv-1)*r
        sn = nv*(a1+an)//2
        prof = "M1" if v%2==0 else "M2"
        qtype = random.choice(["termen","suma"])
        if qtype == "termen":
            exs.append(E(prof,1,3,"progresie_aritmetica",2,
                f"Într-o progresie aritmetică a₁ = {a1} și rația r = {r}. Calculați a{sub(nv)}.",
                f"a{sub(nv)} = {an}",
                [St(1,"Formula termenului general",f"aₙ = a₁ + (n-1)·r"),
                 St(2,"Înlocuim",f"a{sub(nv)} = {a1} + ({nv}-1)·{r} = {a1} + {(nv-1)*r} = {an}")],
                ["aₙ = a₁ + (n-1)r"],"aₙ = a₁ + (n-1)r",
                ["Greșesc (n-1) ca n"],["progresii","aritmetica"]))
        else:
            exs.append(E(prof,1,3,"progresie_aritmetica",2,
                f"Într-o progresie aritmetică a₁ = {a1}, r = {r}. Calculați S{sub(nv)}.",
                f"S{sub(nv)} = {sn}",
                [St(1,"Calculăm a{0}".format(sub(nv)),f"a{sub(nv)} = {a1}+{(nv-1)}·{r} = {an}"),
                 St(2,"Aplicăm formula sumei",f"S{sub(nv)} = {nv}·(a₁+a{sub(nv)})/2 = {nv}·({a1}+{an})/2 = {sn}")],
                ["Sₙ = n(a₁+aₙ)/2"],"Sₙ = n(a₁+aₙ)/2",
                ["Uită /2 în formulă"],["progresii","aritmetica","suma"]))
    # Geometrice
    for v in range(n - n//2):
        b1 = random.choice([1,2,3,-1,-2,-3])
        q = random.choice([2,3,-2,-1*random.choice([2,3]),Fraction(1,2),Fraction(1,3)])
        nv = random.randint(3,7)
        bn = Fraction(b1) * Fraction(q)**(nv-1)
        prof = "M1" if v%2==0 else "M2"
        exs.append(E(prof,1,3,"progresie_geometrica",2,
            f"Într-o progresie geometrică b₁ = {b1}, q = {fs(q)}. Calculați b{sub(nv)}.",
            f"b{sub(nv)} = {fs(bn)}",
            [St(1,"Formula termenului general",f"bₙ = b₁·qⁿ⁻¹"),
             St(2,"Înlocuim",f"b{sub(nv)} = {b1}·({fs(q)}){sup(nv-1)} = {fs(bn)}")],
            ["bₙ = b₁·qⁿ⁻¹"],"bₙ = b₁·qⁿ⁻¹",
            ["Confundă n cu n-1 la exponent"],["progresii","geometrica"]))
    return exs

def gen_combinatorica(n=170):
    exs = []
    # Combinări
    for v in range(n*35//100):
        nv = random.randint(4,15); k = random.randint(1,min(nv-1,8))
        ans = math.comb(nv, k)
        prof = "M1" if v%2==0 else "M2"
        exs.append(E(prof,1,4,"combinari",2,
            f"Calculați C({nv},{k}).", f"{ans}",
            [St(1,"Aplicăm formula",f"C({nv},{k}) = {nv}!/({k}!·{nv-k}!)"),
             St(2,"Calculăm",f"= {ans}")],
            ["C(n,k) = n!/(k!(n-k)!)"],"C(n,k) = n!/(k!(n-k)!)",
            ["Confundă C cu A"],["combinatorica","combinari"]))
    # Aranjamente
    for v in range(n*25//100):
        nv = random.randint(4,10); k = random.randint(2,min(nv,5))
        ans = math.perm(nv, k)
        prof = "M1" if v%2==0 else "M2"
        exs.append(E(prof,1,4,"aranjamente",2,
            f"Calculați A({nv},{k}).", f"{ans}",
            [St(1,"Aplicăm formula",f"A({nv},{k}) = {nv}!/({nv-k})!"),
             St(2,"Calculăm",f"= {ans}")],
            ["A(n,k) = n!/(n-k)!"],"A(n,k) = n!/(n-k)!",
            ["Confundă A cu C"],["combinatorica","aranjamente"]))
    # Permutări
    for v in range(n*15//100):
        nv = random.randint(3,8)
        ans = math.factorial(nv)
        prof = "M1" if v%2==0 else "M2"
        exs.append(E(prof,1,4,"permutari",2,
            f"Calculați P({nv}) = {nv}!.", f"{ans}",
            [St(1,"Aplicăm formula",f"P({nv}) = {nv}! = {'·'.join(str(i) for i in range(nv,0,-1))}"),
             St(2,"Calculăm",f"= {ans}")],
            ["Pₙ = n!"],"Pₙ = n!",["Greșesc la înmulțire"],["combinatorica","permutari"]))
    # Binom Newton
    for v in range(n - len(exs)):
        nv = random.randint(3,8); k = random.randint(1,nv-1)
        a = random.choice([1,2,3]); b = random.choice([1,-1,2,-2])
        coef = math.comb(nv,k) * a**(nv-k) * b**k
        prof = "M1" if v%2==0 else "M2"
        term = f"x{sup(nv-k)}" if nv-k > 0 else ""
        exs.append(E(prof,1,4,"binom_newton",3,
            f"Găsiți coeficientul lui x{sup(nv-k)} în dezvoltarea ({a}x + {b}){sup(nv)}.",
            f"{coef}",
            [St(1,"Formula termenului general",f"T(k+1) = C({nv},{k})·({a}x)^({nv}-{k})·({b})^{k}"),
             St(2,"Calculăm",f"C({nv},{k})·{a}{sup(nv-k)}·({b}){sup(k)} = {math.comb(nv,k)}·{a**(nv-k)}·{b**k} = {coef}")],
            ["Tk = C(n,k)·aⁿ⁻ᵏ·bᵏ"],"(a+b)ⁿ: Tk = C(n,k)·aⁿ⁻ᵏ·bᵏ",
            ["Greșesc puterea lui a sau b"],["combinatorica","binom","newton"]))
    return exs

def gen_matrice(n=200):
    exs = []
    # Operații (A+B, A·B, A²)
    for v in range(n*30//100):
        a = [[random.randint(-4,4) for _ in range(2)] for _ in range(2)]
        b = [[random.randint(-4,4) for _ in range(2)] for _ in range(2)]
        op = random.choice(["sum","prod","sq"])
        if op == "sum":
            r = [[a[i][j]+b[i][j] for j in range(2)] for i in range(2)]
            q = f"Calculați A + B, unde A = {mat2s(a)}, B = {mat2s(b)}."
            ans = mat2s(r)
            steps = [St(1,"Adunăm element cu element",f"A+B = {mat2s(r)}")]
        elif op == "prod":
            r = [[a[i][0]*b[0][j]+a[i][1]*b[1][j] for j in range(2)] for i in range(2)]
            q = f"Calculați A·B, unde A = {mat2s(a)}, B = {mat2s(b)}."
            ans = mat2s(r)
            steps = [St(1,"(A·B)ᵢⱼ = Σ aᵢₖ·bₖⱼ",""),
                     St(2,"Calculăm",mat2s(r))]
        else:
            r = [[a[i][0]*a[0][j]+a[i][1]*a[1][j] for j in range(2)] for i in range(2)]
            q = f"Calculați A², unde A = {mat2s(a)}."
            ans = mat2s(r)
            steps = [St(1,"A² = A·A",""),St(2,"Calculăm",mat2s(r))]
        exs.append(E("M1",1,5,"matrice_operatii",2,q,ans,steps,
            ["Înmulțirea: linie × coloană"],"(A·B)ᵢⱼ = Σaᵢₖbₖⱼ",
            ["Greșesc la înmulțire (adună în loc de linie×coloană)"],["matrice","operatii"]))
    # Determinant 2×2
    for v in range(n*20//100):
        a = [[random.randint(-5,5) for _ in range(2)] for _ in range(2)]
        d = a[0][0]*a[1][1] - a[0][1]*a[1][0]
        exs.append(E("M1",1,5,"determinant_2x2",1,
            f"Calculați det(A), unde A = {mat2s(a)}.", f"{d}",
            [St(1,"Formula det 2×2",f"det = a₁₁·a₂₂ - a₁₂·a₂₁"),
             St(2,"Înlocuim",f"det = {a[0][0]}·{a[1][1]} - {a[0][1]}·{a[1][0]} = {a[0][0]*a[1][1]} - {a[0][1]*a[1][0]} = {d}")],
            ["det = ad - bc"],"det((a,b),(c,d)) = ad-bc",
            ["Greșesc semnul la bc"],["matrice","determinant"]))
    # Determinant 3×3
    for v in range(n*15//100):
        m = [[random.randint(-3,3) for _ in range(3)] for _ in range(3)]
        d = (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
            -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
            +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
        exs.append(E("M1",1,5,"determinant_3x3",3,
            f"Calculați det(A), unde A = {mat3s(m)}.", f"{d}",
            [St(1,"Regula lui Sarrus sau dezvoltare după prima linie",""),
             St(2,"Dezvoltăm",f"det = {m[0][0]}·({m[1][1]}·{m[2][2]}-{m[1][2]}·{m[2][1]}) - {m[0][1]}·({m[1][0]}·{m[2][2]}-{m[1][2]}·{m[2][0]}) + {m[0][2]}·({m[1][0]}·{m[2][1]}-{m[1][1]}·{m[2][0]})"),
             St(3,"Rezultat",f"det = {d}")],
            ["Regula lui Sarrus sau dezvoltare Laplace"],"Dezvoltare după prima linie",
            ["Greșesc semnele la cofactori"],["matrice","determinant","3x3"]))
    # Inversă 2×2
    for v in range(n*18//100):
        while True:
            a = [[random.randint(-4,4) for _ in range(2)] for _ in range(2)]
            d = a[0][0]*a[1][1] - a[0][1]*a[1][0]
            if d != 0: break
        inv = [[Fraction(a[1][1],d), Fraction(-a[0][1],d)],
               [Fraction(-a[1][0],d), Fraction(a[0][0],d)]]
        inv_s = f"(({fs(inv[0][0])}, {fs(inv[0][1])}), ({fs(inv[1][0])}, {fs(inv[1][1])}))"
        exs.append(E("M1",1,5,"matrice_inversa",3,
            f"Calculați inversa matricei A = {mat2s(a)}.", inv_s,
            [St(1,"Calculăm det(A)",f"det = {d}"),
             St(2,"Formula inversei",f"A⁻¹ = (1/det)·adj(A)"),
             St(3,"Inversăm",inv_s)],
            ["A⁻¹ = (1/det)·((d,-b),(-c,a))"],"A⁻¹ = (1/det)·adj(A)",
            ["Uită să schimbe semnele","Det = 0 ⟹ nu are inversă"],["matrice","inversa"]))
    # Cramer 2×2
    for v in range(n - len(exs)):
        while True:
            a = [[random.randint(-4,4) for _ in range(2)] for _ in range(2)]
            d = a[0][0]*a[1][1] - a[0][1]*a[1][0]
            if d != 0: break
        b = [random.randint(-8,8), random.randint(-8,8)]
        dx = b[0]*a[1][1] - a[0][1]*b[1]
        dy = a[0][0]*b[1] - b[0]*a[1][0]
        x, y = Fraction(dx,d), Fraction(dy,d)
        exs.append(E("M1",1,5,"sistem_cramer",3,
            f"Rezolvați sistemul prin regula lui Cramer:\n{a[0][0]}x + {a[0][1]}y = {b[0]}\n{a[1][0]}x + {a[1][1]}y = {b[1]}",
            f"x = {fs(x)}, y = {fs(y)}",
            [St(1,"det(A)",f"{d}"),St(2,"det(Ax)",f"{dx}"),St(3,"det(Ay)",f"{dy}"),
             St(4,"Soluția",f"x = {dx}/{d} = {fs(x)}, y = {dy}/{d} = {fs(y)}")],
            ["x = det(Ax)/det(A), y = det(Ay)/det(A)"],"Regula lui Cramer",
            ["Greșesc la construirea determinanților"],["matrice","cramer","sistem"]))
    return exs

def mat2s(m):
    return f"(({m[0][0]}, {m[0][1]}), ({m[1][0]}, {m[1][1]}))"
def mat3s(m):
    return f"(({m[0][0]}, {m[0][1]}, {m[0][2]}), ({m[1][0]}, {m[1][1]}, {m[1][2]}), ({m[2][0]}, {m[2][1]}, {m[2][2]}))"

def gen_functii(n=160):
    exs = []
    # f(a) evaluation
    for v in range(n*30//100):
        terms = [(random.choice(NZ), random.randint(1,3))]
        terms.append((random.randint(-8,8), 0))
        if random.random() > 0.5:
            terms.insert(1, (random.choice(NZ), 1))
        a = random.randint(-3,5)
        val = sum(c*a**p for c,p in terms)
        prof = "M1" if v%2==0 else "M2"
        exs.append(E(prof,1,6,"functie_eval",1,
            f"Fie f: ℝ → ℝ, f(x) = {ps(terms)}. Calculați f({a}).", f"f({a}) = {val}",
            [St(1,"Înlocuim x cu {0}".format(a),f"f({a}) = {' + '.join(f'{c}·{a}^{p}' for c,p in terms)}"),
             St(2,"Calculăm",f"f({a}) = {val}")],
            ["Înlocuiți x cu valoarea dată"],"",
            ["Greșesc la ridicare la putere"],["functii","evaluare"]))
    # Funcție inversă (liniară)
    for v in range(n*30//100):
        a = random.choice(NZ); b = random.randint(-10,10)
        prof = "M1" if v%2==0 else "M2"
        inv_a = Fraction(1,a); inv_b = Fraction(-b,a)
        exs.append(E(prof,1,6,"functie_inversa",2,
            f"Fie f: ℝ → ℝ, f(x) = {ps([(a,1),(b,0)])}. Determinați f⁻¹(x).",
            f"f⁻¹(x) = {ps([(inv_a,1),(inv_b,0)])}",
            [St(1,"Notăm y = f(x)",f"y = {a}x + {b}"),
             St(2,"Exprimăm x",f"x = (y-{b})/{a} = {fs(inv_a)}y + ({fs(inv_b)})"),
             St(3,"Inversăm notațiile",f"f⁻¹(x) = {ps([(inv_a,1),(inv_b,0)])}")],
            ["y = ax+b ⟹ x = (y-b)/a"],"f⁻¹: y=f(x) → x=...",
            ["Uită să inverseze notația x↔y"],["functii","inversa"]))
    # Compunere f∘g
    for v in range(n*25//100):
        a1 = random.choice(NZ); b1 = random.randint(-5,5)
        a2 = random.choice(NZ); b2 = random.randint(-5,5)
        # (f∘g)(x) = f(g(x)) = a1*(a2*x+b2)+b1 = a1*a2*x + a1*b2+b1
        rc = a1*a2; rd = a1*b2+b1
        prof = "M1" if v%2==0 else "M2"
        exs.append(E(prof,1,6,"functie_compunere",2,
            f"Fie f(x) = {ps([(a1,1),(b1,0)])}, g(x) = {ps([(a2,1),(b2,0)])}. Calculați (f∘g)(x).",
            f"(f∘g)(x) = {ps([(rc,1),(rd,0)])}",
            [St(1,"(f∘g)(x) = f(g(x))",f"= f({ps([(a2,1),(b2,0)])})"),
             St(2,"Înlocuim în f",f"= {a1}·({ps([(a2,1),(b2,0)])}) + {b1} = {rc}x + {rd}")],
            ["(f∘g)(x) = f(g(x))"],"(f∘g)(x) = f(g(x))",
            ["Confundă f∘g cu g∘f"],["functii","compunere"]))
    # Vârf parabolă
    for v in range(n - len(exs)):
        a = random.choice([-3,-2,-1,1,2,3])
        r1 = random.randint(-5,5); r2 = random.randint(-5,5)
        b = -a*(r1+r2); c = a*r1*r2
        xv = Fraction(-b, 2*a); yv = eval_poly([(a,2),(b,1),(c,0)], xv)
        prof = "M1" if v%2==0 else "M2"
        exs.append(E(prof,1,6,"functie_varf",2,
            f"Determinați vârful parabolei f(x) = {ps([(a,2),(b,1),(c,0)])}.",
            f"V({fs(xv)}, {fs(yv)})",
            [St(1,"xᵥ = -b/(2a)",f"xᵥ = {-b}/(2·{a}) = {fs(xv)}"),
             St(2,"yᵥ = f(xᵥ)",f"yᵥ = {fs(yv)}"),
             St(3,"Vârful",f"V({fs(xv)}, {fs(yv)})")],
            ["V = (-b/(2a), f(-b/(2a)))"],"xᵥ = -b/(2a)",
            ["Greșesc semnul la -b/(2a)"],["functii","parabola","varf"]))
    return exs

# ═══════════════════════════════════════
# SUBIECTUL II
# ═══════════════════════════════════════

def gen_limite(n=170):
    exs = []
    # Directe (substituție)
    for v in range(n*25//100):
        terms = [(random.choice([1,2,3,-1,-2]),random.randint(1,3)),(random.randint(-5,5),0)]
        a = random.randint(-2,3)
        val = eval_poly(terms, a)
        prof = "M1" if v%2==0 else "M2"
        exs.append(E(prof,2,1,"limita_directa",1,
            f"Calculați lim(x→{a}) ({ps(terms)}).", f"{fs(val)}",
            [St(1,"Substituim x = {0}".format(a),f"f({a}) = {fs(val)}"),
             St(2,"Limita există și este finită",f"lim = {fs(val)}")],
            ["Substituiți direct x=a"],"lim(x→a) f(x) = f(a) dacă f continuă",
            ["Nu verifică dacă e formă nedeterminată"],["limite","directa"]))
    # 0/0 factorizare: lim(x→a) (x²-a²)/(x-a) = 2a
    for v in range(n*25//100):
        a = random.randint(-5,5)
        k = random.choice([1,2,3])
        # (x²-a²)/(x-a) = x+a, lim=2a
        # Or (x²-(2a-k)x+a(a-k))/(x-a) = x-(a-k), lim = k
        # simpler: (x^2 - a^2)/(x-a)
        prof = "M1" if v%2==0 else "M2"
        exs.append(E(prof,2,1,"limita_factorizare",2,
            f"Calculați lim(x→{a}) (x² - {a*a})/(x - {a}).", f"{2*a}",
            [St(1,"Observăm formă 0/0","Numărător: {0}²-{1}=0, Numitor: {0}-{0}=0".format(a,a*a)),
             St(2,"Factorizăm",f"x²-{a*a} = (x-{a})(x+{a})"),
             St(3,"Simplificăm",f"lim = lim(x→{a}) (x+{a}) = {2*a}")],
            ["Factorizați numărătorul"],"a²-b² = (a-b)(a+b)",
            ["Nu recunosc forma a²-b²"],["limite","factorizare","00"]))
    # ∞/∞: lim(x→∞) polinom/polinom
    for v in range(n*25//100):
        a1 = random.choice(NZ); b1 = random.randint(-5,5)
        a2 = random.choice(NZ); b2 = random.randint(-5,5)
        deg = random.choice([2,3])
        prof = "M1" if v%2==0 else "M2"
        ans = Fraction(a1, a2)
        p_num = ps([(a1,deg),(b1,0)]); p_den = ps([(a2,deg),(b2,0)])
        exs.append(E(prof,2,1,"limita_infinit",2,
            f"Calculați lim(x→∞) ({p_num})/({p_den}).", f"{fs(ans)}",
            [St(1,"Grade egale → raportul coeficienților dominanți",""),
             St(2,"Calculăm",f"lim = {a1}/{a2} = {fs(ans)}")],
            ["Comparați gradele numărătorului și numitorului"],
            "Grade egale: lim = aₙ/bₙ",
            ["Confundă regula gradelor"],["limite","infinit","raport"]))
    # Remarcabile
    remarcabile = [
        ("lim(x→0) sin(x)/x", "1", "Limită remarcabilă fundamentală"),
        ("lim(x→∞) (1 + 1/x)ˣ", "e", "Definiția numărului e"),
        ("lim(x→0) (eˣ-1)/x", "1", "Limită remarcabilă exponențială"),
        ("lim(x→0) ln(1+x)/x", "1", "Limită remarcabilă logaritmică"),
        ("lim(x→0) tg(x)/x", "1", "Se reduce la sin(x)/x"),
    ]
    for v in range(n - len(exs)):
        idx = v % len(remarcabile)
        q_base, ans, expl = remarcabile[idx]
        # Variază cu coeficienți
        k = random.choice([2,3,4,5])
        prof = "M1" if v%2==0 else "M2"
        if idx == 0:
            q = f"Calculați lim(x→0) sin({k}x)/({k}x)."
            exs.append(E(prof,2,1,"limita_remarcabila",2,q,"1",
                [St(1,"Notăm t = {0}x, t→0".format(k),""),
                 St(2,"lim(t→0) sin(t)/t = 1","Limită remarcabilă")],
                ["sin(t)/t → 1 când t→0"],"lim sin(x)/x = 1",
                ["Confundă sin(x)/x cu x/sin(x)"],["limite","remarcabile"]))
        elif idx == 1:
            q = f"Calculați lim(x→∞) (1 + {k}/x)ˣ."
            exs.append(E(prof,2,1,"limita_remarcabila",3,q,f"e{sup(k)}",
                [St(1,f"Scriem ca ((1+{k}/x)^(x/{k}))^{k}",""),
                 St(2,f"lim(x→∞)(1+{k}/x)^(x/{k}) = e",""),
                 St(3,f"Rezultat = e{sup(k)}","")],
                ["(1+k/x)ˣ → eᵏ"],"(1+a/x)ˣ → eᵃ",
                ["Greșesc exponentul"],["limite","remarcabile","e"]))
        else:
            q = q_base + "."
            exs.append(E(prof,2,1,"limita_remarcabila",2,q,ans,
                [St(1,"Limită remarcabilă",expl),St(2,"Rezultat",ans)],
                [expl],"Limite remarcabile",["Nu le recunosc"],["limite","remarcabile"]))
    return exs

def gen_derivate(n=230):
    exs = []
    # Polinom
    for v in range(n*30//100):
        num_terms = random.randint(2,4)
        powers = sorted(random.sample(range(0,6), num_terms), reverse=True)
        terms = [(random.choice(NZ), p) for p in powers]
        d = deriv(terms)
        prof = "M1" if v%2==0 else "M2"
        exs.append(E(prof,2,2,"derivata_polinom",2,
            f"Calculați derivata funcției f(x) = {ps(terms)}.",
            f"f'(x) = {ps(d) if d else '0'}",
            [St(i+1, f"({ps([(c,p)])})'", f"= {ps([(c*p,p-1)])}") for i,(c,p) in enumerate(terms) if p > 0] +
            [St(len([t for t in terms if t[1]>0])+1, "Rezultat", f"f'(x) = {ps(d)}")],
            ["(xⁿ)' = n·xⁿ⁻¹"],"(xⁿ)' = nxⁿ⁻¹, (c)' = 0",
            ["Uită derivata constantei (nu e 1, e 0!)"],["derivate","polinom"]))
    # Produs: (f·g)'
    for v in range(n*15//100):
        a1,b1 = random.choice(NZ),random.randint(-5,5)
        a2,b2 = random.choice(NZ),random.randint(-5,5)
        f1 = ps([(a1,1),(b1,0)]); f2 = ps([(a2,1),(b2,0)])
        # (a1x+b1)(a2x+b2) deriv = a1(a2x+b2) + a2(a1x+b1) = 2a1a2x + a1b2+a2b1
        rc = 2*a1*a2; rd = a1*b2+a2*b1
        prof = "M1" if v%2==0 else "M2"
        exs.append(E(prof,2,2,"derivata_produs",2,
            f"Calculați derivata: f(x) = ({f1})·({f2}).",
            f"f'(x) = {ps([(rc,1),(rd,0)])}",
            [St(1,"(f·g)' = f'·g + f·g'",""),
             St(2,"f'="+str(a1)+", g'="+str(a2),""),
             St(3,"Rezultat",f"{a1}·({f2}) + ({f1})·{a2} = {ps([(rc,1),(rd,0)])}")],
            ["(f·g)' = f'·g + f·g'"],"(fg)' = f'g + fg'",
            ["Aplică greșit (fg)' = f'·g'"],["derivate","produs"]))
    # Compuse (regula lanțului)
    for v in range(n*15//100):
        a = random.choice(NZ); b = random.randint(-5,5)
        nn = random.randint(2,5)
        prof = "M1" if v%2==0 else "M2"
        inner = ps([(a,1),(b,0)]); outer_d = nn
        exs.append(E(prof,2,2,"derivata_compusa",3,
            f"Calculați derivata: f(x) = ({inner}){sup(nn)}.",
            f"f'(x) = {nn*a}·({inner}){sup(nn-1) if nn-1>1 else ''}",
            [St(1,"Aplicăm regula lanțului","(uⁿ)' = n·uⁿ⁻¹·u'"),
             St(2,"u = "+inner+", u' = "+str(a),""),
             St(3,"Rezultat",f"{nn}·({inner}){sup(nn-1)}·{a} = {nn*a}·({inner}){sup(nn-1)}")],
            ["(f(g(x)))' = f'(g(x))·g'(x)"],"Regula lanțului",
            ["Uită derivata interioară"],["derivate","compuse","lant"]))
    # Tangenta
    for v in range(n*20//100):
        terms = [(random.choice([1,-1,2,-2,3]),random.randint(2,3)),(random.randint(-4,4),1),(random.randint(-5,5),0)]
        x0 = random.randint(-2,3)
        y0 = eval_poly(terms, x0)
        d = deriv(terms)
        m = eval_poly(d, x0)
        prof = "M1" if v%2==0 else "M2"
        # y - y0 = m(x - x0) → y = mx - mx0 + y0
        b_tang = -m*x0 + y0
        exs.append(E(prof,2,2,"tangenta",3,
            f"Determinați ecuația tangentei la graficul funcției f(x) = {ps(terms)} în punctul x₀ = {x0}.",
            f"y = {ps([(m,1),(b_tang,0)])}",
            [St(1,"Calculăm f(x₀)",f"f({x0}) = {fs(y0)}"),
             St(2,"Calculăm f'(x)",f"f'(x) = {ps(d)}"),
             St(3,"Panta tangentei",f"m = f'({x0}) = {fs(m)}"),
             St(4,"Ecuația tangentei",f"y - {fs(y0)} = {fs(m)}(x - {x0}) → y = {ps([(m,1),(b_tang,0)])}")],
            ["y - f(a) = f'(a)(x-a)"],"y = f'(x₀)(x-x₀) + f(x₀)",
            ["Uită să calculeze f(x₀)"],["derivate","tangenta"]))
    # Monotonie / Extrem
    for v in range(n - len(exs)):
        r1 = random.randint(-4,3); r2 = random.randint(r1+1,r1+5)
        a = random.choice([1,-1])
        terms = [(a,2),(-(r1+r2)*a,1),(r1*r2*a,0)]
        d = deriv(terms)
        prof = "M1" if v%2==0 else "M2"
        y1 = eval_poly(terms, r1); y2 = eval_poly(terms, r2)
        if a > 0:
            mono = f"f crescătoare pe (-∞,{r1})∪({r2},+∞), descrescătoare pe ({r1},{r2})"
            extrem = f"Maxim local: f({r1})={fs(y1)}, Minim local: f({r2})={fs(y2)}"
        else:
            mono = f"f descrescătoare pe (-∞,{r1})∪({r2},+∞), crescătoare pe ({r1},{r2})"
            extrem = f"Minim local: f({r1})={fs(y1)}, Maxim local: f({r2})={fs(y2)}"
        exs.append(E(prof,2,2,"monotonie_extrem",3,
            f"Studiați monotonia și determinați punctele de extrem ale funcției f(x) = {ps(terms)}.",
            extrem,
            [St(1,"Calculăm f'(x)",f"f'(x) = {ps(d)}"),
             St(2,"f'(x) = 0",f"x₁ = {r1}, x₂ = {r2}"),
             St(3,"Tabel de semn",mono),
             St(4,"Puncte de extrem",extrem)],
            ["f'(x) = 0 pentru punctele critice"],"f'(x)=0, tabel semn",
            ["Nu analizează semnul derivatei"],["derivate","monotonie","extrem"]))
    return exs

def gen_integrale_nedef(n=110):
    exs = []
    # Polinom
    for v in range(n*55//100):
        num_terms = random.randint(2,4)
        powers = sorted(random.sample(range(0,5), num_terms), reverse=True)
        terms = [(random.choice(NZ), p) for p in powers]
        anti = antideriv(terms)
        prof = "M1" if v%2==0 else "M2"
        exs.append(E(prof,2,3,"integrala_polinom",2,
            f"Calculați ∫({ps(terms)})dx.", f"{ps(anti)} + C",
            [St(i+1, f"∫{ps([(c,p)])}dx", f"= {ps([(Fraction(c,p+1),p+1)])}") for i,(c,p) in enumerate(terms)] +
            [St(len(terms)+1, "Adăugăm constanta", f"{ps(anti)} + C")],
            ["∫xⁿdx = xⁿ⁺¹/(n+1) + C"],"∫xⁿdx = xⁿ⁺¹/(n+1) + C",
            ["Uită +C","Greșesc la n+1"],["integrale","nedefinite","polinom"]))
    # Exponențiale și trigonometrice
    trig_integrals = [
        ("sin(x)", "-cos(x) + C", "∫sin(x)dx = -cos(x) + C"),
        ("cos(x)", "sin(x) + C", "∫cos(x)dx = sin(x) + C"),
        ("eˣ", "eˣ + C", "∫eˣdx = eˣ + C"),
        ("1/x", "ln|x| + C", "∫(1/x)dx = ln|x| + C"),
    ]
    for v in range(n*25//100):
        idx = v % len(trig_integrals)
        func, ans, formula = trig_integrals[idx]
        k = random.choice([2,3,4,5])
        prof = "M1" if v%2==0 else "M2"
        if idx == 0:
            q = f"Calculați ∫{k}·sin(x)dx."
            a = f"-{k}·cos(x) + C"
        elif idx == 1:
            q = f"Calculați ∫{k}·cos(x)dx."
            a = f"{k}·sin(x) + C"
        elif idx == 2:
            q = f"Calculați ∫{k}·eˣdx."
            a = f"{k}·eˣ + C"
        else:
            q = f"Calculați ∫{k}/x dx."
            a = f"{k}·ln|x| + C"
        exs.append(E(prof,2,3,"integrala_trig_exp",2,q,a,
            [St(1,"Scoatem constanta",f"{k}·∫{func}dx"),
             St(2,"Aplicăm formula",f"= {a}")],
            [formula],formula,["Greșesc semnul la sin/cos"],["integrale","nedefinite"]))
    # Substituție simplă
    for v in range(n - len(exs)):
        a = random.choice([2,3,4,5]); b = random.randint(-5,5)
        nn = random.randint(2,4)
        prof = "M1" if v%2==0 else "M2"
        # ∫(ax+b)^n dx = (ax+b)^(n+1) / (a(n+1)) + C
        coef = Fraction(1, a*(nn+1))
        exs.append(E(prof,2,3,"integrala_substitutie",3,
            f"Calculați ∫({a}x+{b}){sup(nn)}dx.",
            f"{fs(coef)}·({a}x+{b}){sup(nn+1)} + C",
            [St(1,"Substituim t = {0}x+{1}, dt = {0}dx".format(a,b),""),
             St(2,"∫t{0}·dt/{1}".format(sup(nn),a),f"= (1/{a})·t{sup(nn+1)}/{nn+1}"),
             St(3,"Revenim la x",f"= {fs(coef)}·({a}x+{b}){sup(nn+1)} + C")],
            ["Substituție: t = ax+b"],"∫(ax+b)ⁿdx = (ax+b)ⁿ⁺¹/(a(n+1))",
            ["Uită să împartă la derivata interioară"],["integrale","substitutie"]))
    return exs

def gen_integrale_def(n=100):
    exs = []
    # Leibniz-Newton polinomiale
    for v in range(n*55//100):
        terms = [(random.choice([1,2,3,-1,-2]),random.randint(1,3)),(random.randint(-3,3),0)]
        a = random.randint(-1,2); b = random.randint(a+1,a+4)
        anti = antideriv(terms)
        Fb = eval_poly(anti, b); Fa = eval_poly(anti, a)
        val = Fb - Fa
        prof = "M1" if v%2==0 else "M2"
        exs.append(E(prof,2,4,"integrala_definita",2,
            f"Calculați ∫ de la {a} la {b} ({ps(terms)})dx.", f"{fs(val)}",
            [St(1,"Primitiva",f"F(x) = {ps(anti)}"),
             St(2,f"F({b}) - F({a})",f"= {fs(Fb)} - ({fs(Fa)}) = {fs(val)}")],
            ["∫ₐᵇ f(x)dx = F(b)-F(a)"],"Leibniz-Newton: F(b)-F(a)",
            ["Greșesc la evaluarea primitivei"],["integrale","definite","leibniz"]))
    # Arii
    for v in range(n - len(exs)):
        # Aria sub graficul unui polinom pozitiv pe [a,b]
        a_coef = random.choice([1,2])
        terms = [(a_coef,2),(random.randint(0,3),0)]
        a_int = 0; b_int = random.randint(1,4)
        anti = antideriv(terms)
        Fb = eval_poly(anti, b_int); Fa = eval_poly(anti, a_int)
        area = abs(Fb - Fa)
        prof = "M1" if v%2==0 else "M2"
        exs.append(E(prof,2,4,"arie_sub_grafic",3,
            f"Calculați aria cuprinsă între graficul f(x) = {ps(terms)}, axa Ox și dreptele x={a_int}, x={b_int}.",
            f"A = {fs(area)}",
            [St(1,"A = ∫ₐᵇ |f(x)|dx","f(x) ≥ 0 pe intervalul dat"),
             St(2,"Primitiva",f"F(x) = {ps(anti)}"),
             St(3,"Calculăm",f"A = F({b_int})-F({a_int}) = {fs(Fb)}-{fs(Fa)} = {fs(area)}")],
            ["A = ∫|f(x)|dx"],"Aria = |∫ₐᵇ f(x)dx|",
            ["Uită valoarea absolută"],["integrale","arii"]))
    return exs

def gen_studiu(n=35):
    exs = []
    for v in range(n):
        # f(x) = (ax+b)/(cx+d) — funcție rațională simplă
        a = random.choice(NZ); b = random.randint(-5,5)
        c = random.choice([1,2,-1,-2]); d = random.randint(-5,5)
        while a*d == b*c: d = random.randint(-5,5)
        asimpt_v = Fraction(-d, c)
        asimpt_h = Fraction(a, c)
        exs.append(E("M1",2,5,"studiu_functii",3,
            f"Studiați funcția f(x) = ({a}x+{b})/({c}x+{d}): domeniu, asimptote, monotonie.",
            f"D=ℝ\\{{{fs(asimpt_v)}}}, AV: x={fs(asimpt_v)}, AO: y={fs(asimpt_h)}",
            [St(1,"Domeniu",f"D = ℝ \\ {{{fs(asimpt_v)}}} ({c}x+{d}≠0)"),
             St(2,"Asimptota verticală",f"x = {fs(asimpt_v)}"),
             St(3,"Asimptota orizontală",f"lim(x→±∞) f(x) = {a}/{c} = {fs(asimpt_h)}, deci y = {fs(asimpt_h)}"),
             St(4,"Derivata",f"f'(x) = ({a*d-b*c})/({c}x+{d})², semnul: {'pozitiv' if a*d-b*c>0 else 'negativ'} → f {'crescătoare' if a*d-b*c>0 else 'descrescătoare'}")],
            ["Domeniu → Asimptote → Derivată → Monotonie"],"",
            ["Uită domeniul"],["studiu","functii","asimptote","monotonie"]))
    return exs

def gen_geometrie(n=65):
    exs = []
    # Ecuația dreptei prin 2 puncte
    for v in range(n*40//100):
        x1,y1 = random.randint(-5,5),random.randint(-5,5)
        x2,y2 = random.randint(-5,5),random.randint(-5,5)
        while x1==x2: x2 = random.randint(-5,5)
        m = Fraction(y2-y1, x2-x1)
        b = Fraction(y1) - m*x1
        exs.append(E("M2",2,5,"ecuatia_dreptei",2,
            f"Determinați ecuația dreptei prin punctele A({x1},{y1}) și B({x2},{y2}).",
            f"y = {ps([(m,1),(b,0)])}",
            [St(1,"Panta",f"m = (y₂-y₁)/(x₂-x₁) = ({y2}-{y1})/({x2}-{x1}) = {fs(m)}"),
             St(2,"Ecuația",f"y - {y1} = {fs(m)}(x - {x1})"),
             St(3,"Forma finală",f"y = {ps([(m,1),(b,0)])}")],
            ["m = (y₂-y₁)/(x₂-x₁)"],"y-y₁ = m(x-x₁)",
            ["Inversează x și y la pantă"],["geometrie","dreapta"]))
    # Distanța punct-dreaptă
    for v in range(n*30//100):
        a = random.choice(NZ); b = random.choice(NZ); c = random.randint(-10,10)
        px,py = random.randint(-5,5),random.randint(-5,5)
        d = abs(a*px+b*py+c) / math.sqrt(a*a+b*b)
        d_exact = f"|{a}·{px}+{b}·{py}+{c}|/√({a*a}+{b*b})"
        num = abs(a*px+b*py+c)
        den_sq = a*a+b*b
        exs.append(E("M2",2,5,"distanta_punct_dreapta",2,
            f"Calculați distanța de la punctul P({px},{py}) la dreapta {a}x+{b}y+{c}=0.",
            f"d = {num}/√{den_sq}" if den_sq != 1 else f"d = {num}",
            [St(1,"Formula",f"d = |ax₀+by₀+c|/√(a²+b²)"),
             St(2,"Înlocuim",f"d = |{a}·{px}+{b}·{py}+{c}|/√({a}²+{b}²) = {num}/√{den_sq}")],
            ["d = |ax₀+by₀+c|/√(a²+b²)"],"d = |ax₀+by₀+c|/√(a²+b²)",
            ["Uită valoarea absolută"],["geometrie","distanta"]))
    # Șiruri convergente
    for v in range(n - len(exs)):
        a = random.choice([2,3,4,5])
        exs.append(E("M2",2,6,"sir_convergent",2,
            f"Calculați lim(n→∞) ({a}n+1)/({a}n-3).", "1",
            [St(1,"Împărțim la n",f"lim ({a}+1/n)/({a}-3/n)"),
             St(2,"Când n→∞",f"= {a}/{a} = 1")],
            ["Împărțiți la cea mai mare putere a lui n"],"",
            ["Nu simplifică corect"],["siruri","convergenta"]))
    return exs

# ═══════════════════════════════════════
# SUBIECTUL III
# ═══════════════════════════════════════

def gen_s3(n=60):
    exs = []
    # M1: Integrale cu parametru
    for v in range(n//3):
        a = random.choice([1,2,3]); k = random.randint(1,4)
        # ∫₀¹ (ax^k) dx = a/(k+1)
        val = Fraction(a, k+1)
        exs.append(E("M1",3,1,"integrala_parametru",3,
            f"Calculați ∫ de la 0 la 1 ({a}x{sup(k)})dx.",
            f"{fs(val)}",
            [St(1,"Primitiva",f"F(x) = {a}·x{sup(k+1)}/{k+1} = {fs(Fraction(a,k+1))}·x{sup(k+1)}"),
             St(2,"Leibniz-Newton",f"F(1)-F(0) = {fs(val)} - 0 = {fs(val)}")],
            ["∫xⁿdx = xⁿ⁺¹/(n+1)"],"",
            ["Greșesc la evaluare"],["integrale","parametru"]))
    # M1: Matrice Aⁿ
    for v in range(n//3):
        # Matrice diagonală simplă
        d1 = random.choice([1,2,3,-1]); d2 = random.choice([1,2,-1,-2])
        nn = random.randint(2,5)
        d1n, d2n = d1**nn, d2**nn
        exs.append(E("M1",3,2,"matrice_putere",3,
            f"Calculați A{sup(nn)}, unde A = (({d1}, 0), (0, {d2})).",
            f"(({d1n}, 0), (0, {d2n}))",
            [St(1,"A este diagonală","Aⁿ = diag(d₁ⁿ, d₂ⁿ)"),
             St(2,f"d₁{sup(nn)} = {d1}{sup(nn)} = {d1n}",""),
             St(3,f"d₂{sup(nn)} = {d2}{sup(nn)} = {d2n}",""),
             St(4,"Rezultat",f"A{sup(nn)} = (({d1n}, 0), (0, {d2n}))")],
            ["Pentru matrice diagonale: Aⁿ = diag(d₁ⁿ, d₂ⁿ)"],"",
            ["Nu recunosc matricea diagonală"],["matrice","putere"]))
    # M2: Funcții avansate
    for v in range(n - len(exs)):
        a = random.choice([1,2,3]); b = random.randint(-3,3)
        terms = [(a,3),(b,1)]
        d = deriv(terms)
        dd = deriv(d)
        r_dd = [Fraction(-t[0], dd[0][0]) for t in dd[1:]] if len(dd) > 1 else [Fraction(0)]
        prof = "M2"
        exs.append(E(prof,3,3,"functie_convexitate",3,
            f"Studiați convexitatea funcției f(x) = {ps(terms)}.",
            f"f''(x) = {ps(dd)}, inflexiune la x = 0",
            [St(1,"f'(x) = "+ps(d),""),
             St(2,"f''(x) = "+ps(dd),""),
             St(3,"f''(x) = 0",f"x = 0"),
             St(4,"Convexitate",f"f concavă pe (-∞,0), convexă pe (0,+∞)" if a>0 else f"f convexă pe (-∞,0), concavă pe (0,+∞)")],
            ["f''(x)=0 pentru puncte de inflexiune"],"",
            ["Confundă concavitatea cu convexitatea"],["functii","convexitate","inflexiune"]))
    return exs

# ═══════════════════════════════════════
# MAIN
# ═══════════════════════════════════════

def main():
    print("Generare exerciții BAC Matematică...\n")
    all_exs = []

    generators = [
        ("S1 - Mulțimi",        gen_multimi),
        ("S1 - Ecuații liniare", gen_ecuatii_liniare),
        ("S1 - Ecuații grad 2",  gen_ecuatii_grad2),
        ("S1 - Ecuații iraționale", gen_ecuatii_irationale),
        ("S1 - Ecuații modul",   gen_ecuatii_modul),
        ("S1 - Ecuații exp",     gen_ecuatii_exp),
        ("S1 - Ecuații log",     gen_ecuatii_log),
        ("S1 - Inecuații",       gen_inecuatii),
        ("S1 - Progresii",      gen_progresii),
        ("S1 - Combinatorică",  gen_combinatorica),
        ("S1 - Matrice",        gen_matrice),
        ("S1 - Funcții",        gen_functii),
        ("S2 - Limite",         gen_limite),
        ("S2 - Derivate",       gen_derivate),
        ("S2 - Integrale nedef",gen_integrale_nedef),
        ("S2 - Integrale def",  gen_integrale_def),
        ("S2 - Studiu funcții", gen_studiu),
        ("S2 - Geometrie",      gen_geometrie),
        ("S3 - Probleme",       gen_s3),
    ]

    for name, gen_fn in generators:
        exs = gen_fn()
        all_exs.extend(exs)
        print(f"  {name}: {len(exs)} exerciții")

    print(f"\n{'='*50}")
    print(f"TOTAL: {len(all_exs)} exerciții\n")

    # Statistici per subiect
    by_subj = defaultdict(int)
    by_topic = defaultdict(int)
    by_prof = defaultdict(int)
    for ex in all_exs:
        by_subj[f"Subiectul {ex['subject']}"] += 1
        by_topic[ex['topic']] += 1
        by_prof[ex['profile']] += 1

    print("Per subiect:")
    for k in sorted(by_subj): print(f"  {k}: {by_subj[k]}")
    print("\nPer profil:")
    for k in sorted(by_prof): print(f"  {k}: {by_prof[k]}")
    print("\nPer topic:")
    for k in sorted(by_topic, key=lambda x: -by_topic[x]):
        print(f"  {k}: {by_topic[k]}")

    # Salvare JSON
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_exs, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nSalvat în {OUT_FILE}")

    # Seed MongoDB
    try:
        sys.path.insert(0, os.path.join(ROOT, "backend"))
        from pymongo import MongoClient
        from database import MONGO_URI, MONGO_DB

        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]

        # Ștergem exercițiile generate anterior
        result = db.exercises.delete_many({"tags": {"$exists": True}, "year": 2024})
        print(f"\nȘterse {result.deleted_count} exerciții vechi din MongoDB")

        # Inserăm cu ID-uri auto-increment
        from database import get_next_id
        docs = []
        for ex in all_exs:
            doc = dict(ex)
            doc["_id"] = get_next_id("exercises")
            doc["source"] = "generated_bac"
            docs.append(doc)

        if docs:
            db.exercises.insert_many(docs)
            print(f"Inserate {len(docs)} exerciții în MongoDB")
            print(f"Colecția exercises: {db.exercises.count_documents({})} total")
    except Exception as e:
        print(f"\nMongoDB seed opțional (eroare: {e})")
        print("Exercițiile sunt salvate în JSON — pot fi importate manual.")

if __name__ == "__main__":
    main()
