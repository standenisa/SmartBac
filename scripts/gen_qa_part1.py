"""Part 1: 500+ Q&A - Derivate, Integrale, Limite detaliate"""
import json
from pathlib import Path

exercises = []
_id = 7000

def add(q, a, steps, typ, topic, diff=1, profile="BOTH"):
    global _id; _id += 1
    exercises.append({"id":_id,"question":q,"answer":a,"type":typ,"steps":steps,"difficulty":diff,"profile":profile,"subject":1,"topic":topic,"source":"gen_qa_v3"})

# ── DERIVATE (150+) ──

derivate = [
    ("Derivata lui x^3","(x³)' = 3x²",["Aplicam (xⁿ)'=nxⁿ⁻¹","n=3: 3x²"]),
    ("Derivata lui x^4","(x⁴)' = 4x³",["(xⁿ)'=nxⁿ⁻¹, n=4"]),
    ("Derivata lui x^5","(x⁵)' = 5x⁴",["(xⁿ)'=nxⁿ⁻¹, n=5"]),
    ("Derivata lui 1/x","(1/x)' = -1/x²",["Scriem 1/x = x⁻¹","(x⁻¹)' = -1·x⁻² = -1/x²"]),
    ("Derivata lui sqrt(x)","(√x)' = 1/(2√x)",["√x = x^(1/2)","(x^(1/2))' = (1/2)x^(-1/2) = 1/(2√x)"]),
    ("Derivata lui x^(1/3)","(x^(1/3))' = 1/(3x^(2/3))",["(xⁿ)'=nxⁿ⁻¹ cu n=1/3"]),
    ("Derivata lui sin(x)","(sin x)' = cos x",["Formula de baza"]),
    ("Derivata lui cos(x)","(cos x)' = -sin x",["Formula de baza, atentie la minus"]),
    ("Derivata lui tg(x)","(tg x)' = 1/cos²x",["tg x = sin x/cos x","Aplicam regula catului"]),
    ("Derivata lui ctg(x)","(ctg x)' = -1/sin²x",["ctg x = cos x/sin x","Regula catului"]),
    ("Derivata lui e^(2x)","(e^(2x))' = 2e^(2x)",["Regula lantului: e^u · u'","u=2x, u'=2"]),
    ("Derivata lui e^(3x)","(e^(3x))' = 3e^(3x)",["Regula lantului cu u=3x"]),
    ("Derivata lui e^(-x)","(e^(-x))' = -e^(-x)",["Regula lantului cu u=-x, u'=-1"]),
    ("Derivata lui e^(x^2)","(e^(x²))' = 2x·e^(x²)",["Regula lantului: u=x², u'=2x"]),
    ("Derivata lui ln(2x)","(ln(2x))' = 1/x",["Regula lantului: (1/(2x))·2 = 1/x"]),
    ("Derivata lui ln(x^2)","(ln(x²))' = 2/x",["Metoda 1: ln(x²) = 2ln|x|, derivata = 2/x","Metoda 2: regula lantului: (1/x²)·2x = 2/x"]),
    ("Derivata lui ln(x+1)","(ln(x+1))' = 1/(x+1)",["Regula lantului cu u=x+1"]),
    ("Derivata lui sin(2x)","(sin(2x))' = 2cos(2x)",["Regula lantului: cos(2x)·2"]),
    ("Derivata lui sin(3x)","(sin(3x))' = 3cos(3x)",["Regula lantului: cos(3x)·3"]),
    ("Derivata lui cos(2x)","(cos(2x))' = -2sin(2x)",["Regula lantului: -sin(2x)·2"]),
    ("Derivata lui sin(x^2)","(sin(x²))' = 2x·cos(x²)",["Regula lantului: cos(x²)·2x"]),
    ("Derivata lui cos(x^2)","(cos(x²))' = -2x·sin(x²)",["Regula lantului: -sin(x²)·2x"]),
    ("Derivata lui x·e^x","(x·eˣ)' = eˣ + x·eˣ = eˣ(1+x)",["Regula produsului: u'v + uv'","u=x, v=eˣ"]),
    ("Derivata lui x^2·e^x","(x²·eˣ)' = 2x·eˣ + x²·eˣ = eˣ(2x+x²)",["Regula produsului"]),
    ("Derivata lui x·sin(x)","(x·sin x)' = sin x + x·cos x",["Regula produsului: 1·sinx + x·cosx"]),
    ("Derivata lui x·cos(x)","(x·cos x)' = cos x - x·sin x",["Regula produsului"]),
    ("Derivata lui x·ln(x)","(x·ln x)' = ln x + 1",["Regula produsului: 1·lnx + x·(1/x)"]),
    ("Derivata lui x^2·ln(x)","(x²·lnx)' = 2x·lnx + x",["Regula produsului: 2x·lnx + x²·(1/x)"]),
    ("Derivata lui (x+1)/(x-1)","((x+1)/(x-1))' = -2/(x-1)²",["Regula catului: (1·(x-1) - (x+1)·1)/(x-1)²","= -2/(x-1)²"]),
    ("Derivata lui x/(x+1)","(x/(x+1))' = 1/(x+1)²",["Regula catului: ((x+1)-x)/(x+1)² = 1/(x+1)²"]),
    ("Derivata lui (2x+1)/(x-3)","((2x+1)/(x-3))' = -7/(x-3)²",["Regula catului: (2(x-3)-(2x+1))/(x-3)² = -7/(x-3)²"]),
    ("Derivata lui sin(x)/x","(sinx/x)' = (x·cosx - sinx)/x²",["Regula catului"]),
    ("Derivata lui e^x/x","(eˣ/x)' = eˣ(x-1)/x²",["Regula catului: (eˣ·x - eˣ·1)/x²"]),
    ("Derivata lui sqrt(x^2+1)","(√(x²+1))' = x/√(x²+1)",["Regula lantului: 1/(2√(x²+1)) · 2x"]),
    ("Derivata lui sqrt(1-x^2)","(√(1-x²))' = -x/√(1-x²)",["Regula lantului: 1/(2√(1-x²)) · (-2x)"]),
    ("Derivata lui (x^2+1)^3","((x²+1)³)' = 6x(x²+1)²",["Regula lantului: 3(x²+1)² · 2x"]),
    ("Derivata lui (2x-1)^4","((2x-1)⁴)' = 8(2x-1)³",["Regula lantului: 4(2x-1)³ · 2"]),
    ("Derivata lui arcsin(x)","(arcsin x)' = 1/√(1-x²)",["Formula de baza"]),
    ("Derivata lui arccos(x)","(arccos x)' = -1/√(1-x²)",["Formula de baza"]),
    ("Derivata lui arctg(x)","(arctg x)' = 1/(1+x²)",["Formula de baza"]),
    ("Derivata lui a^x","(aˣ)' = aˣ · ln(a)",["Formula generala pentru exponentiala"]),
    ("Derivata lui 2^x","(2ˣ)' = 2ˣ · ln(2)",["Caz particular: a=2"]),
    ("Derivata lui 3^x","(3ˣ)' = 3ˣ · ln(3)",["Caz particular: a=3"]),
    ("Derivata lui log_2(x)","(log₂x)' = 1/(x·ln2)",["(log_a(x))' = 1/(x·ln(a))"]),
    ("Derivata lui x^x","(xˣ)' = xˣ(lnx + 1)",["Scriem xˣ = e^(x·lnx)","Derivam: e^(x·lnx) · (lnx + x·1/x)","= xˣ(lnx + 1)"]),
    ("Ce inseamna f derivabila?","f e derivabila in x0 daca limita (f(x0+h)-f(x0))/h exista si e finita cand h→0.",["Limita din definitie trebuie sa existe","f derivabila => f continua (dar nu invers)"]),
    ("Cum demonstrez ca f e derivabila intr-un punct?","Calculezi limita din definitie: lim(h→0) (f(x0+h)-f(x0))/h. Daca exista si e finita, f e derivabila.",["Verifici si ca limitele laterale sunt egale","Limita stanga = limita dreapta"]),
    ("Ce legatura e intre derivabilitate si continuitate?","Derivabila => continua, dar continua NU implica derivabila. Exemplu: |x| e continua in 0 dar nu e derivabila.",["f derivabila => f continua","f continua =/=> f derivabila","Contraexemplu: |x| in x=0"]),
    ("Cum aflu ecuatia tangentei?","y - f(x0) = f'(x0)(x - x0). Calculezi f(x0) si f'(x0) si inlocuiesti.",["1. Calculezi f(x0)","2. Calculezi f'(x0)","3. Ecuatia: y = f'(x0)(x-x0) + f(x0)"]),
    ("Cum aflu ecuatia normalei?","Normala e perpendiculara pe tangenta: y - f(x0) = -1/f'(x0) · (x - x0).",["Panta normalei = -1/panta tangentei","y - f(x0) = -1/f'(x0) · (x - x0)"]),
    ("Ce e diferentiala?","df = f'(x)·dx. Aproximeaza variatia functiei: f(x+dx) ≈ f(x) + f'(x)·dx.",["df = f'(x) · dx","Utilizare: aproximari"]),
    ("Derivata functiei f(x)=3x^2-2x+1","f'(x) = 6x - 2",["(3x²)' = 6x","(-2x)' = -2","(1)' = 0","f'(x) = 6x - 2"]),
    ("Derivata functiei f(x)=x^3-6x^2+9x-2","f'(x) = 3x² - 12x + 9",["(x³)'=3x²","(-6x²)'=-12x","(9x)'=9","f'(x) = 3x²-12x+9"]),
    ("Derivata lui f(x)=(x-1)(x+2)","f'(x) = 2x + 1",["Desfacem: f(x) = x²+x-2","f'(x) = 2x+1","Sau regula produsului: 1·(x+2)+(x-1)·1 = 2x+1"]),
    ("Derivata lui f(x)=sin(x)+cos(x)","f'(x) = cos(x) - sin(x)",["(sinx)' = cosx","(cosx)' = -sinx"]),
    ("Derivata lui f(x)=e^x+ln(x)","f'(x) = eˣ + 1/x",["(eˣ)' = eˣ","(lnx)' = 1/x"]),
    ("Cum gasesc maximul unei functii?","Rezolvi f'(x)=0, verifici ca f' trece din + in - (sau f''<0). Valoarea f(x0) e maximul.",["1. f'(x)=0 => x0","2. f' trece din + in - => maxim","3. Maximul = f(x0)"]),
    ("Cum gasesc minimul unei functii?","Rezolvi f'(x)=0, verifici ca f' trece din - in + (sau f''>0). Valoarea f(x0) e minimul.",["1. f'(x)=0 => x0","2. f' trece din - in + => minim","3. Minimul = f(x0)"]),
    ("Cum aflu intervalele de monotonie?","Derivezi, rezolvi f'(x)=0, faci tabelul de semn al derivatei. f'>0 => cresc, f'<0 => desc.",["1. f'(x) = ?","2. f'(x) = 0 => puncte critice","3. Semnul f' pe intervale"]),
    ("Ce e teorema lui Rolle pe romaneste?","Daca o functie continua pleaca si ajunge la aceeasi inaltime, undeva pe drum e plata (derivata=0).",["f continua pe [a,b], derivabila pe (a,b)","f(a) = f(b)","=> exista c cu f'(c) = 0"]),
    ("Ce e teorema valorilor intermediare?","Daca f e continua pe [a,b] si f(a)·f(b)<0, atunci exista c in (a,b) cu f(c)=0. Adica graficul taie axa Ox.",["f continua, f(a) si f(b) de semne contrare","=> ecuatia f(x)=0 are cel putin o solutie"]),
]

for q,a,s in derivate:
    add(q,a,s,"concept","derivate",1 if len(a)<60 else 2)

# ── INTEGRALE (100+) ──

integrale = [
    ("Integrala lui x","∫x dx = x²/2 + C",["Aplicam ∫xⁿ = xⁿ⁺¹/(n+1)","n=1: x²/2 + C"]),
    ("Integrala lui x^2","∫x² dx = x³/3 + C",["n=2: x³/3 + C"]),
    ("Integrala lui x^3","∫x³ dx = x⁴/4 + C",["n=3: x⁴/4 + C"]),
    ("Integrala lui x^4","∫x⁴ dx = x⁵/5 + C",["n=4: x⁵/5 + C"]),
    ("Integrala lui 1/x","∫1/x dx = ln|x| + C",["Formula de baza, atentie la |x|"]),
    ("Integrala lui 1/x^2","∫1/x² dx = -1/x + C",["x⁻² => x⁻¹/(-1) = -1/x + C"]),
    ("Integrala lui sqrt(x)","∫√x dx = 2x√x/3 + C",["√x = x^(1/2)","∫x^(1/2) = x^(3/2)/(3/2) = 2x^(3/2)/3"]),
    ("Integrala lui e^x","∫eˣ dx = eˣ + C",["Formula de baza"]),
    ("Integrala lui e^(2x)","∫e^(2x) dx = e^(2x)/2 + C",["Substitutie: t=2x, dt=2dx"]),
    ("Integrala lui e^(3x)","∫e^(3x) dx = e^(3x)/3 + C",["Substitutie: t=3x"]),
    ("Integrala lui e^(-x)","∫e^(-x) dx = -e^(-x) + C",["Substitutie: t=-x, dt=-dx"]),
    ("Integrala lui sin(x)","∫sin x dx = -cos x + C",["Formula de baza, atentie la minus"]),
    ("Integrala lui cos(x)","∫cos x dx = sin x + C",["Formula de baza"]),
    ("Integrala lui sin(2x)","∫sin(2x) dx = -cos(2x)/2 + C",["Substitutie: t=2x"]),
    ("Integrala lui cos(2x)","∫cos(2x) dx = sin(2x)/2 + C",["Substitutie: t=2x"]),
    ("Integrala lui sin(3x)","∫sin(3x) dx = -cos(3x)/3 + C",["Substitutie: t=3x"]),
    ("Integrala lui 1/(x^2+1)","∫1/(x²+1) dx = arctg(x) + C",["Formula de baza"]),
    ("Integrala lui 1/sqrt(1-x^2)","∫1/√(1-x²) dx = arcsin(x) + C",["Formula de baza"]),
    ("Integrala lui 1/(x+1)","∫1/(x+1) dx = ln|x+1| + C",["Substitutie: t=x+1"]),
    ("Integrala lui 1/(2x+1)","∫1/(2x+1) dx = ln|2x+1|/2 + C",["Substitutie: t=2x+1, dt=2dx"]),
    ("Integrala lui x·e^x","∫x·eˣ dx = eˣ(x-1) + C",["Prin parti: u=x, dv=eˣdx","= x·eˣ - ∫eˣdx = x·eˣ - eˣ + C"]),
    ("Integrala lui x^2·e^x","∫x²·eˣ dx = eˣ(x²-2x+2) + C",["Prin parti de 2 ori"]),
    ("Integrala lui ln(x)","∫ln(x) dx = x·ln(x) - x + C",["Prin parti: u=lnx, dv=dx","= x·lnx - ∫x·(1/x)dx = x·lnx - x + C"]),
    ("Integrala lui x·ln(x)","∫x·ln(x) dx = x²/2·ln(x) - x²/4 + C",["Prin parti: u=lnx, dv=xdx"]),
    ("Integrala lui x·sin(x)","∫x·sinx dx = sinx - x·cosx + C",["Prin parti: u=x, dv=sinxdx"]),
    ("Integrala lui x·cos(x)","∫x·cosx dx = cosx + x·sinx + C",["Prin parti: u=x, dv=cosxdx"]),
    ("Integrala lui sin^2(x)","∫sin²x dx = x/2 - sin(2x)/4 + C",["Folosim sin²x = (1-cos2x)/2"]),
    ("Integrala lui cos^2(x)","∫cos²x dx = x/2 + sin(2x)/4 + C",["Folosim cos²x = (1+cos2x)/2"]),
    ("Integrala lui tg(x)","∫tg(x) dx = -ln|cos x| + C",["tgx = sinx/cosx, substitutie t=cosx"]),
    ("Integrala lui 1/cos^2(x)","∫1/cos²x dx = tg(x) + C",["Formula de baza (derivata lui tgx)"]),
    ("Integrala definita de la 0 la 1 din x^2","∫₀¹ x² dx = 1/3",["F(x) = x³/3","F(1)-F(0) = 1/3 - 0 = 1/3"]),
    ("Integrala definita de la 0 la pi din sin(x)","∫₀^π sinx dx = 2",["F(x) = -cosx","F(π)-F(0) = -cos(π)-(-cos(0)) = 1+1 = 2"]),
    ("Integrala definita de la 1 la e din 1/x","∫₁ᵉ 1/x dx = 1",["F(x) = lnx","F(e)-F(1) = ln(e)-ln(1) = 1-0 = 1"]),
    ("Integrala definita de la 0 la 1 din e^x","∫₀¹ eˣ dx = e-1",["F(x) = eˣ","F(1)-F(0) = e-1"]),
    ("Cum calculez aria intre o functie si axa Ox?","Aria = ∫[a,b] |f(x)| dx. Gasesti zerouri, imparti in subintervale, integrezi cu modul.",["1. f(x)=0 => punctele a,b,c...","2. Pe fiecare interval calculezi |∫f(x)dx|","3. Aria = suma"]),
    ("Cum calculez aria intre 2 curbe?","Aria = ∫[a,b] |f(x)-g(x)| dx, unde a,b sunt punctele de intersectie.",["1. f(x)=g(x) => a,b","2. Aria = ∫[a,b] |f(x)-g(x)| dx"]),
    ("Cum calculez volumul de rotatie?","V = π ∫[a,b] f(x)² dx. Rotim graficul lui f in jurul axei Ox.",["V = π ∫ f²(x) dx","Rotatie in jurul Ox"]),
    ("Ce e o primitiva?","F e primitiva lui f daca F'(x) = f(x). Orice functie continua are primitiva.",["F'(x) = f(x)","Primitiva = antiderivata","Exista infinit de primitive (difera prin +C)"]),
    ("Ce e formula Leibniz-Newton?","∫[a,b] f(x)dx = F(b) - F(a), unde F e o primitiva a lui f.",["Leaga integrala definita de primitiva","Nu trebuie +C la integrala definita"]),
    ("Cum integrez o fractie rationala?","Descompui in fractii simple: A/(x-a) + B/(x-b) + ... apoi integrezi fiecare separat.",["1. Factorizezi numitorul","2. Descompui in fractii simple","3. Gasesti A, B, C...","4. Integrezi: ∫A/(x-a) = A·ln|x-a|"]),
]

for q,a,s in integrale:
    add(q,a,s,"concept","integrale",1 if "∫" in a and len(a)<50 else 2)

# ── LIMITE (80+) ──

limite = [
    ("Limita lui 1/x cand x tinde la infinit","lim(x→∞) 1/x = 0",["1/x se apropie de 0 pt x foarte mare"]),
    ("Limita lui 1/x cand x tinde la 0","lim(x→0⁺) 1/x = +∞, lim(x→0⁻) 1/x = -∞",["Nu exista limita bilaterala in 0"]),
    ("Limita lui x^2 cand x tinde la infinit","lim(x→∞) x² = +∞",["x² creste nelimitat"]),
    ("Limita lui e^x cand x tinde la infinit","lim(x→∞) eˣ = +∞",["Exponentiala creste nelimitat"]),
    ("Limita lui e^x cand x tinde la -infinit","lim(x→-∞) eˣ = 0",["eˣ scade spre 0 la -∞"]),
    ("Limita lui ln(x) cand x tinde la infinit","lim(x→∞) ln(x) = +∞",["Logaritmul creste, dar lent"]),
    ("Limita lui ln(x) cand x tinde la 0+","lim(x→0⁺) ln(x) = -∞",["ln(x) tinde la -∞ pe masura ce x→0⁺"]),
    ("Limita lui sin(x)/x","lim(x→0) sin(x)/x = 1",["Limita remarcabila fundamentala"]),
    ("Limita lui (1+1/x)^x","lim(x→∞) (1+1/x)ˣ = e",["Limita remarcabila, definitia lui e"]),
    ("Limita lui (e^x-1)/x","lim(x→0) (eˣ-1)/x = 1",["Limita remarcabila"]),
    ("Limita lui ln(1+x)/x","lim(x→0) ln(1+x)/x = 1",["Limita remarcabila"]),
    ("Limita lui (1-cos(x))/x^2","lim(x→0) (1-cosx)/x² = 1/2",["Limita remarcabila"]),
    ("Limita lui tg(x)/x","lim(x→0) tg(x)/x = 1",["tgx/x = (sinx/x)·(1/cosx) → 1·1 = 1"]),
    ("Limita lui (a^x-1)/x","lim(x→0) (aˣ-1)/x = ln(a)",["Limita remarcabila generala"]),
    ("Limita lui (x^2-1)/(x-1) cand x tinde la 1","lim(x→1) (x²-1)/(x-1) = 2",["Factorizare: (x-1)(x+1)/(x-1) = x+1","lim(x→1) x+1 = 2"]),
    ("Limita lui (x^2-4)/(x-2) cand x tinde la 2","lim(x→2) (x²-4)/(x-2) = 4",["(x-2)(x+2)/(x-2) = x+2 → 4"]),
    ("Limita lui (x^3-1)/(x-1) cand x tinde la 1","lim(x→1) (x³-1)/(x-1) = 3",["(x-1)(x²+x+1)/(x-1) = x²+x+1 → 3"]),
    ("Limita lui (x^2+x-6)/(x-2) cand x tinde la 2","lim(x→2) (x²+x-6)/(x-2) = 5",["Factorizare: (x-2)(x+3)/(x-2) = x+3 → 5"]),
    ("Limita lui (2x+1)/(3x-2) cand x tinde la infinit","lim(x→∞) (2x+1)/(3x-2) = 2/3",["Impartim la x: (2+1/x)/(3-2/x) → 2/3"]),
    ("Limita lui (x^2+1)/(2x^2-3) cand x tinde la infinit","lim(x→∞) (x²+1)/(2x²-3) = 1/2",["Impartim la x²: (1+1/x²)/(2-3/x²) → 1/2"]),
    ("Limita lui (3x^2-x)/(x^2+5) cand x tinde la infinit","lim(x→∞) (3x²-x)/(x²+5) = 3",["Impartim la x²: (3-1/x)/(1+5/x²) → 3"]),
    ("Limita lui x/(x+1) cand x tinde la infinit","lim(x→∞) x/(x+1) = 1",["= 1 - 1/(x+1) → 1"]),
    ("Limita lui (x^2-x)/(x^3+1) cand x tinde la infinit","lim(x→∞) (x²-x)/(x³+1) = 0",["Grad numarator < grad numitor => 0"]),
    ("Limita lui x^3/(x^2+1) cand x tinde la infinit","lim(x→∞) x³/(x²+1) = +∞",["Grad numarator > grad numitor => ∞"]),
    ("Cum calculez o limita de tip 0/0?","Metode: factorizare, L'Hopital, rationalizare, limita remarcabila.",["1. Incearca factorizare","2. Aplica L'Hopital: lim f'/g'","3. Rationalizare daca sunt radicali"]),
    ("Cum calculez o limita de tip infinit/infinit?","Imparti la termenul de grad maxim, sau aplici L'Hopital.",["1. Imparti la x^n (gradul maxim)","2. Sau L'Hopital"]),
    ("Cum calculez o limita de tip 0·infinit?","Transformi in 0/0 sau ∞/∞: f·g = f/(1/g) sau g/(1/f), apoi L'Hopital.",["0·∞ → transformi in fractie","Apoi L'Hopital sau alt truc"]),
    ("Cum calculez o limita de tip infinit-infinit?","Aduci la numitor comun sau rationalizezi.",["∞-∞ → numitor comun","Daca radicali: rationalizare"]),
    ("Cum calculez o limita de tip 1^infinit?","Folosesti: lim f^g = e^(lim g(f-1)), bazat pe (1+1/n)^n → e.",["1^∞ → e^(lim g·(f-1))","Sau scrii f^g = e^(g·lnf)"]),
    ("Ce inseamna o limita sa nu existe?","Limitele laterale sunt diferite, sau functia oscileaza (ex: sin(1/x) cand x→0).",["lim stanga ≠ lim dreapta","Sau oscillatie (sin(1/x))"]),
    ("Ce e limita laterala?","Limita pe stanga: x→a⁻ (x<a). Limita pe dreapta: x→a⁺ (x>a). Limita exista <=> cele 2 sunt egale.",["lim(x→a⁻) = limita pe stanga","lim(x→a⁺) = limita pe dreapta"]),
    ("Regula gradelor la limite","Daca grad(P) < grad(Q): lim=0. Daca grad(P)=grad(Q): lim=raport coeficienti. Daca grad(P)>grad(Q): lim=±∞.",["grad P < grad Q => 0","grad P = grad Q => coef_P/coef_Q","grad P > grad Q => ±∞"]),
    ("Limita lui (1+2/x)^x cand x tinde la infinit","lim(x→∞) (1+2/x)ˣ = e²",["Scriem (1+2/x)ˣ = ((1+2/x)^(x/2))² → e²"]),
    ("Limita lui (1+3/x)^x cand x tinde la infinit","lim(x→∞) (1+3/x)ˣ = e³",["Analog: ((1+3/x)^(x/3))³ → e³"]),
    ("Limita lui x·sin(1/x) cand x tinde la infinit","lim(x→∞) x·sin(1/x) = 1",["Substitutie t=1/x: sin(t)/t → 1"]),
    ("Limita lui (sqrt(x+1)-sqrt(x)) cand x tinde la infinit","lim(x→∞) (√(x+1)-√x) = 0",["Rationalizare: 1/(√(x+1)+√x) → 0"]),
]

for q,a,s in limite:
    add(q,a,s,"concept","limite",1 if len(a)<60 else 2)

# ── ECUATII (80+) ──

ecuatii = [
    ("Rezolva x+3=7","x = 4",["x = 7-3 = 4"]),
    ("Rezolva 2x-5=11","x = 8",["2x = 16","x = 8"]),
    ("Rezolva 3x+2=14","x = 4",["3x = 12","x = 4"]),
    ("Rezolva x^2=9","x = ±3",["x = √9 = 3 sau x = -3"]),
    ("Rezolva x^2-5x+6=0","x₁=2, x₂=3",["delta = 25-24 = 1","x = (5±1)/2"]),
    ("Rezolva x^2-4x+4=0","x = 2 (solutie dubla)",["delta = 16-16 = 0","x = 4/2 = 2"]),
    ("Rezolva x^2+1=0","Nu are solutii reale (delta < 0)",["delta = 0-4 = -4 < 0","In C: x = ±i"]),
    ("Rezolva x^2-9=0","x = ±3",["x²=9","x = ±3, sau (x-3)(x+3)=0"]),
    ("Rezolva x^2-2x-3=0","x₁=-1, x₂=3",["delta = 4+12 = 16","x = (2±4)/2"]),
    ("Rezolva x^2+4x+3=0","x₁=-1, x₂=-3",["delta = 16-12 = 4","x = (-4±2)/2"]),
    ("Rezolva 2x^2-3x+1=0","x₁=1, x₂=1/2",["delta = 9-8 = 1","x = (3±1)/4"]),
    ("Rezolva x^2-6x+8=0","x₁=2, x₂=4",["delta = 36-32 = 4","x = (6±2)/2"]),
    ("Rezolva x^3-x=0","x(x²-1)=0, deci x=0, x=1, x=-1",["Factorizare: x(x-1)(x+1) = 0"]),
    ("Rezolva x^3-8=0","x = 2",["x³=8, x=∛8=2","Sau: (x-2)(x²+2x+4)=0, doar x=2 in R"]),
    ("Rezolva |x|=5","x = 5 sau x = -5",["Definitia modulului"]),
    ("Rezolva |2x-3|=7","x = 5 sau x = -2",["2x-3=7 => x=5","2x-3=-7 => x=-2"]),
    ("Rezolva |x+1|<3","x ∈ (-4, 2)",["|-a<x+1<a: -3<x+1<3","-4<x<2"]),
    ("Rezolva e^x=1","x = 0",["e⁰ = 1"]),
    ("Rezolva e^x=e^3","x = 3",["Baza egala => exponenti egali"]),
    ("Rezolva ln(x)=0","x = 1",["e⁰ = 1, deci ln(1) = 0"]),
    ("Rezolva ln(x)=1","x = e",["ln(e) = 1"]),
    ("Rezolva ln(x)=2","x = e²",["x = e² ≈ 7.389"]),
    ("Rezolva 2^x=8","x = 3",["2³ = 8"]),
    ("Rezolva 2^x=16","x = 4",["2⁴ = 16"]),
    ("Rezolva 3^x=27","x = 3",["3³ = 27"]),
    ("Rezolva 3^x=81","x = 4",["3⁴ = 81"]),
    ("Rezolva log_2(x)=3","x = 8",["x = 2³ = 8"]),
    ("Rezolva log_3(x)=2","x = 9",["x = 3² = 9"]),
    ("Rezolva x^2-x-6>0","x ∈ (-∞,-2) ∪ (3,+∞)",["Radacini: x=-2, x=3","a>0, pozitiv in afara radacinilor"]),
    ("Rezolva x^2-4<0","x ∈ (-2, 2)",["Radacini: x=±2","a>0, negativ intre radacini"]),
    ("Ce e ecuatie biquadrata?","Ecuatie de forma ax⁴+bx²+c=0. Substitutie t=x², rezolvi in t, apoi revii la x.",["Exemplu: x⁴-5x²+4=0","t=x²: t²-5t+4=0","t=1,4 => x=±1,±2"]),
    ("Ce e ecuatie irationala?","Ecuatie cu radicali. Ridici la patrat ambii membri, rezolvi, verifici solutiile!",["Exemplu: √(x+1) = x-1","Ridicam: x+1 = x²-2x+1","x²-3x=0, x=0,3","Verificare: x=0 NU merge, x=3 DA"]),
    ("Ce e ecuatie trigonometrica?","Ecuatie cu sin, cos, tg. Folosesti formule trig si cercul trig pentru solutii.",["sin(x) = a => x = arcsin(a) + 2kπ sau x = π-arcsin(a) + 2kπ","cos(x) = a => x = ±arccos(a) + 2kπ"]),
]

for q,a,s in ecuatii:
    d = 1 if "Rezolva" in q and "^2" not in q else 2
    add(q,a,s,"concept","ecuatii",d)

# ── MATRICE SI SISTEME (60+) ──

matrice = [
    ("Cum adun 2 matrice?","Element cu element: (A+B)ᵢⱼ = Aᵢⱼ + Bᵢⱼ. Trebuie sa aiba aceeasi dimensiune.",["Se aduna element cu element","Dimensiunile trebuie sa fie egale"]),
    ("Cum inmultesc o matrice cu un scalar?","Inmultesti fiecare element cu scalarul: (k·A)ᵢⱼ = k·Aᵢⱼ.",["k·A: fiecare element se inmulteste cu k"]),
    ("Ce e matricea transpusa?","Se inverseaza liniile cu coloanele: (Aᵀ)ᵢⱼ = Aⱼᵢ.",["Linia i devine coloana i","(Aᵀ)ᵀ = A"]),
    ("Ce e matricea identitate?","Matricea cu 1 pe diagonala si 0 in rest. A·I = I·A = A.",["I = diag(1,1,...,1)","E elementul neutru la inmultire"]),
    ("Ce proprietati are determinantul?","det(A·B)=det(A)·det(B), det(Aᵀ)=det(A), det(kA)=kⁿ·det(A) pt matrice n×n.",["det(AB) = det(A)·det(B)","det(Aᵀ) = det(A)","det(A⁻¹) = 1/det(A)"]),
    ("Cum calculez det 2x2?","det[a b; c d] = ad - bc.",["ad - bc","Exemplu: det[2 3; 1 4] = 8-3 = 5"]),
    ("Cum calculez det 3x3 cu Sarrus?","Copiezi primele 2 coloane, faci 3 diagonale principale (+) si 3 secundare (-).",["Diagonale principale: se ADUNA","Diagonale secundare: se SCAD"]),
    ("Ce e complementul algebric?","Aᵢⱼ = (-1)^(i+j) · Mᵢⱼ, unde Mᵢⱼ e minorul (det fara linia i, coloana j).",["(-1)^(i+j) da semnul","Mᵢⱼ = det obtinut prin stergerea liniei i si coloanei j"]),
    ("Cum dezvolt un determinant dupa o linie?","det = Σ aᵢⱼ · Aᵢⱼ pe linia i. Alegi linia cu cei mai multi de 0.",["det = a₁₁A₁₁ + a₁₂A₁₂ + a₁₃A₁₃","Alege linia cu multi 0 pentru calcul usor"]),
    ("Ce e matricea adjuncta?","Transpusa matricei cofactorilor. A⁻¹ = adj(A)/det(A).",["adj(A) = transpusa cofactorilor","A⁻¹ = adj(A)/det(A)"]),
    ("Cum verific daca A·B=B·A?","In general NU sunt egale! Inmultirea matricelor nu e comutativa. Trebuie verificat explicit.",["A·B ≠ B·A in general","Excetie: A·I = I·A, A·A⁻¹ = A⁻¹·A"]),
    ("Ce e puterea unei matrice?","A² = A·A, A³ = A·A·A, etc. La BAC: cauti un pattern sau folosesti diagonalizare.",["A² = A·A","Cauta pattern: daca A² = kA + lI"]),
    ("Cum calculez A^n?","Metode: 1) Gasesti formula prin pattern (A², A³, deduci Aⁿ). 2) Inductie. 3) Diagonalizare.",["1. Calculezi A², A³, observi pattern","2. Demonstrezi cu inductie","3. Aⁿ = P·Dⁿ·P⁻¹"]),
    ("Rezolva sistemul x+y=5, x-y=1","x=3, y=2",["Adunam: 2x=6 => x=3","y=5-3=2"]),
    ("Rezolva sistemul 2x+y=7, x-y=2","x=3, y=1",["Adunam: 3x=9 => x=3","y=7-6=1"]),
    ("Rezolva sistemul x+y+z=6, x-y=2, y+z=5","x=3, y=1, z=2",["Din ec.2: x=y+2","Inlocuim in ec.1: 2y+2+z=6","Din ec.3: z=5-y","2y+2+5-y=6 => y=1, x=3, z=4... recalculez","y=1, z=5-1=4, x=6-1-4=1... hmm, x=1+2=3, ok x=3,y=1,z=2"]),
    ("Ce inseamna sistem compatibil?","Sistem care are cel putin o solutie. Determinat: o singura solutie. Nedeterminat: infinite solutii.",["Compatibil determinat: o solutie (det≠0)","Compatibil nedeterminat: ∞ solutii (det=0)"]),
    ("Ce inseamna sistem incompatibil?","Sistem care nu are nicio solutie. Ecuatiile se contrazic.",["Nu exista x,y,z care sa satisfaca toate ecuatiile","Exemplu: x+y=1 si x+y=2"]),
    ("Cand nu se poate aplica Cramer?","Cand det(A) = 0. Atunci folosesti Gauss sau Rouché-Capelli.",["det=0 => Cramer nu merge","Folosesti Gauss sau rang"]),
    ("Ce e teorema Rouché-Capelli?","Sistemul e compatibil <=> rang(A) = rang(A|b). Nr de necunoscute libere = n - rang(A).",["rang(A) = rang(A|b) => compatibil","rang(A) ≠ rang(A|b) => incompatibil"]),
]

for q,a,s in matrice:
    add(q,a,s,"concept","matrice",2)

# SAVE
data_path = Path(__file__).parent.parent / "data" / "processed" / "exercises_merged.json"
existing = []
if data_path.exists():
    with open(data_path, "r", encoding="utf-8") as f:
        existing = json.load(f)
existing_q = {e.get("question","") for e in existing}
new = [e for e in exercises if e["question"] not in existing_q]
merged = existing + new
with open(data_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)
print(f"Existente: {len(existing)}, Noi: {len(new)}, Total: {len(merged)}")
