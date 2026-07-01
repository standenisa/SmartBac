"""
Generate conversational Q&A pairs for the chatbot.
Covers: conceptual questions, "de ce", "cum", "explica", formulas, tips, mistakes, BAC advice.
"""

import json
from pathlib import Path

exercises = []
_id = 5000

def add(question, answer, steps, ex_type, topic, difficulty=1, profile="BOTH"):
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
        "subject": 1,
        "topic": topic,
        "source": "generated_chat_qa",
    })

# ============================================================================
# CONCEPTE MATEMATICE - "Ce este...?"
# ============================================================================

concepte = [
    # Derivate
    ("Ce este derivata?",
     "Derivata masoara viteza de variatie a unei functii. Geometric, este panta tangentei la grafic intr-un punct.",
     ["Derivata lui f in x0 = lim(h->0) [f(x0+h) - f(x0)] / h",
      "Geometric: panta tangentei la graficul functiei in punctul x0",
      "Fizic: viteza instantanee (derivata pozitiei = viteza)"]),
    ("La ce foloseste derivata?",
     "Derivata se foloseste pentru: studiul monotoniei, puncte de extrem, tangente, studiul complet al functiei.",
     ["1. Monotonie: f'>0 => f crescatoare, f'<0 => f descrescatoare",
      "2. Puncte de extrem: f'(x0)=0 si schimba semnul",
      "3. Ecuatia tangentei: y - f(x0) = f'(x0)(x - x0)",
      "4. Studiu complet: domeniu, monotonie, extreme, convexitate, grafic"]),
    ("Care sunt regulile de derivare?",
     "Regulile principale: (xⁿ)'=nxⁿ⁻¹, (fg)'=f'g+fg', (f/g)'=(f'g-fg')/g², (f∘g)'=f'(g)·g'",
     ["(c)' = 0 (constanta)", "(xⁿ)' = n·xⁿ⁻¹", "(e^x)' = e^x", "(ln x)' = 1/x",
      "(sin x)' = cos x", "(cos x)' = -sin x",
      "Regula produsului: (f·g)' = f'·g + f·g'",
      "Regula catului: (f/g)' = (f'·g - f·g') / g²",
      "Regula lantului: (f(g(x)))' = f'(g(x)) · g'(x)"]),
    ("Ce greseli se fac la derivate?",
     "Cele mai frecvente greseli: uitarea regulii lantului, derivata produsului gresita, confundarea cu integrala.",
     ["1. (fg)' ≠ f'·g' (GRESIT! Trebuie f'g + fg')",
      "2. Uitarea regulii lantului: (sin(2x))' ≠ cos(2x), ci = 2cos(2x)",
      "3. (1/x)' = -1/x², NU 1/x²",
      "4. (e^(2x))' = 2e^(2x), nu e^(2x)"]),

    # Integrale
    ("Ce este integrala?",
     "Integrala este operatia inversa derivarii. Geometric, calculeaza aria de sub graficul unei functii.",
     ["Integrala nedefinita: F(x) + C unde F'(x) = f(x)",
      "Integrala definita: ∫[a,b] f(x)dx = aria de sub grafic intre a si b",
      "Teorema fundamentala: ∫[a,b] f(x)dx = F(b) - F(a)"]),
    ("Care sunt formulele de integrare?",
     "Formulele de baza: ∫xⁿdx = xⁿ⁺¹/(n+1)+C, ∫e^xdx = e^x+C, ∫1/xdx = ln|x|+C",
     ["∫xⁿ dx = xⁿ⁺¹/(n+1) + C (n≠-1)", "∫e^x dx = e^x + C",
      "∫1/x dx = ln|x| + C", "∫sin(x) dx = -cos(x) + C",
      "∫cos(x) dx = sin(x) + C", "∫1/(x²+1) dx = arctg(x) + C",
      "∫1/sqrt(1-x²) dx = arcsin(x) + C"]),
    ("Cum se calculeaza aria cu integrale?",
     "Aria = ∫[a,b] |f(x)| dx. Daca f(x)>=0, aria = ∫[a,b] f(x)dx.",
     ["1. Gasim punctele unde f(x) = 0 (intersectii cu Ox)",
      "2. Impartim intervalul in subintervale unde f are semn constant",
      "3. Aria = suma |∫ f(x)dx| pe fiecare subinterval",
      "Aria intre 2 curbe: ∫[a,b] |f(x) - g(x)| dx"]),

    # Limite
    ("Ce este limita unei functii?",
     "Limita descrie comportarea functiei cand x se apropie de o valoare. lim(x->a) f(x) = L.",
     ["Intuitiv: valorile f(x) se apropie de L cand x se apropie de a",
      "Limita poate exista chiar daca f(a) nu e definita",
      "Exemple: lim(x->0) sin(x)/x = 1"]),
    ("Care sunt limitele remarcabile?",
     "lim sin(x)/x=1, lim (e^x-1)/x=1, lim ln(1+x)/x=1, lim (1+1/x)^x=e",
     ["1. lim(x->0) sin(x)/x = 1",
      "2. lim(x->0) (e^x - 1)/x = 1",
      "3. lim(x->0) ln(1+x)/x = 1",
      "4. lim(x->inf) (1 + 1/x)^x = e",
      "5. lim(x->0) (1-cos(x))/x² = 1/2",
      "6. lim(x->0) tg(x)/x = 1",
      "7. lim(x->0) (a^x-1)/x = ln(a)"]),
    ("Ce e regula lui L'Hopital?",
     "Se aplica la forme nedeterminate 0/0 sau inf/inf: lim f(x)/g(x) = lim f'(x)/g'(x).",
     ["Conditii: forma 0/0 sau inf/inf",
      "lim f(x)/g(x) = lim f'(x)/g'(x)",
      "Se poate aplica de mai multe ori daca tot forma nedeterminata",
      "Exemplu: lim(x->0) sin(x)/x = lim cos(x)/1 = 1"]),
    ("Ce forme nedeterminate exista?",
     "0/0, inf/inf, 0·inf, inf-inf, 0^0, 1^inf, inf^0",
     ["0/0 - se foloseste L'Hopital sau factorizare",
      "inf/inf - se imparte la termenul dominant",
      "0·inf - se transforma in 0/0 sau inf/inf",
      "inf-inf - se aduce la numitor comun",
      "1^inf - se foloseste lim (1+1/x)^x = e"]),

    # Matrice
    ("Ce este o matrice?",
     "O matrice este un tabel de numere aranjate pe linii si coloane. Se noteaza A(m×n).",
     ["Matrice m×n: m linii, n coloane",
      "Matrice patrata: m = n",
      "Matrice unitate I: 1 pe diagonala, 0 in rest",
      "Operatii: adunare, inmultire cu scalar, inmultire de matrice"]),
    ("Cum se calculeaza determinantul?",
     "Det 2×2: ad-bc. Det 3×3: regula lui Sarrus sau dezvoltare dupa linie/coloana.",
     ["Det 2×2: |a b; c d| = ad - bc",
      "Det 3×3: regula lui Sarrus (diagonale)",
      "Sau dezvoltare: det = a11·A11 - a12·A12 + a13·A13",
      "Proprietati: det(A·B) = det(A)·det(B)"]),
    ("Cum se calculeaza inversa unei matrice?",
     "A⁻¹ = (1/det(A)) · adj(A). Conditie: det(A) ≠ 0.",
     ["1. Calculam det(A) - daca e 0, nu exista inversa",
      "2. Calculam matricea cofactorilor",
      "3. Transpunem => matricea adjuncta adj(A)",
      "4. A⁻¹ = (1/det(A)) · adj(A)",
      "Pentru 2×2: A⁻¹ = (1/(ad-bc)) · (d -b; -c a)"]),
    ("Ce este metoda lui Cramer?",
     "Cramer rezolva sisteme cu det ≠ 0: x = Dx/D, y = Dy/D, z = Dz/D.",
     ["1. Calculam D (determinantul sistemului)",
      "2. Dx = inlocuim coloana lui x cu termenii liberi",
      "3. Dy = inlocuim coloana lui y cu termenii liberi",
      "4. x = Dx/D, y = Dy/D"]),

    # Ecuatii
    ("Cum se rezolva o ecuatie de gradul 2?",
     "ax²+bx+c=0: delta=b²-4ac. Daca delta>0: 2 solutii, delta=0: 1 solutie, delta<0: nu are solutii reale.",
     ["1. Identificam a, b, c",
      "2. Calculam delta = b² - 4ac",
      "3. Daca delta > 0: x1,2 = (-b ± sqrt(delta)) / (2a)",
      "4. Daca delta = 0: x = -b/(2a)",
      "5. Daca delta < 0: nu are solutii reale",
      "Relatiile lui Vieta: x1+x2 = -b/a, x1·x2 = c/a"]),
    ("Ce sunt relatiile lui Vieta?",
     "Pentru ax²+bx+c=0: x1+x2 = -b/a si x1·x2 = c/a. Leaga solutiile de coeficienti.",
     ["Suma solutiilor: S = x1 + x2 = -b/a",
      "Produsul solutiilor: P = x1 · x2 = c/a",
      "Utile cand nu trebuie sa gasim solutiile explicit",
      "Exemplu: x²-5x+6=0 => S=5, P=6"]),

    # Progresii
    ("Ce este o progresie aritmetica?",
     "Sir in care diferenta intre termeni consecutivi e constanta (ratia r). an = a1 + (n-1)r.",
     ["Definitie: an+1 - an = r (constant)",
      "Termen general: an = a1 + (n-1)·r",
      "Suma primilor n termeni: Sn = n·(a1 + an)/2",
      "Proprietate: an = (an-1 + an+1) / 2"]),
    ("Ce este o progresie geometrica?",
     "Sir in care raportul intre termeni consecutivi e constant (ratia q). bn = b1·q^(n-1).",
     ["Definitie: bn+1/bn = q (constant)",
      "Termen general: bn = b1 · q^(n-1)",
      "Suma: Sn = b1·(q^n - 1)/(q - 1) pentru q≠1",
      "Proprietate: bn² = bn-1 · bn+1"]),

    # Trigonometrie
    ("Ce formule de trigonometrie trebuie sa stiu?",
     "sin²+cos²=1, sin(a±b), cos(a±b), sin(2a)=2sin(a)cos(a), cos(2a)=cos²a-sin²a",
     ["Identitatea fundamentala: sin²x + cos²x = 1",
      "sin(a+b) = sin(a)cos(b) + cos(a)sin(b)",
      "cos(a+b) = cos(a)cos(b) - sin(a)sin(b)",
      "sin(2a) = 2sin(a)cos(a)",
      "cos(2a) = cos²a - sin²a = 2cos²a - 1 = 1 - 2sin²a",
      "tg(a) = sin(a)/cos(a)",
      "Valorile remarcabile: sin(30°)=1/2, cos(30°)=√3/2, sin(45°)=√2/2, sin(60°)=√3/2"]),
    ("Ce este cercul trigonometric?",
     "Cercul cu raza 1 si centrul in origine. Un unghi x are sin(x)=ordonata, cos(x)=abscisa punctului de pe cerc.",
     ["Cercul unitate: x² + y² = 1",
      "Punctul P(cos(t), sin(t)) pe cerc",
      "Cadranul I (0-90°): sin>0, cos>0",
      "Cadranul II (90-180°): sin>0, cos<0",
      "Cadranul III (180-270°): sin<0, cos<0",
      "Cadranul IV (270-360°): sin<0, cos>0"]),

    # Combinatorica
    ("Care e diferenta intre permutari, aranjamente si combinari?",
     "Pn=n! (ordine, toate), A(n,k)=n!/(n-k)! (ordine, k din n), C(n,k)=n!/(k!(n-k)!) (fara ordine, k din n).",
     ["Permutari P(n) = n! - toate elementele, conteaza ordinea",
      "Aranjamente A(n,k) = n!/(n-k)! - k elemente din n, conteaza ordinea",
      "Combinari C(n,k) = n!/(k!·(n-k)!) - k elemente din n, NU conteaza ordinea",
      "Exemplu: din {1,2,3} aleg 2:",
      "  Aranjamente: (1,2),(2,1),(1,3),(3,1),(2,3),(3,2) = 6",
      "  Combinari: {1,2},{1,3},{2,3} = 3"]),
    ("Ce este binomul lui Newton?",
     "(a+b)^n = Σ C(n,k) · a^(n-k) · b^k, k=0..n",
     ["(a+b)^n = C(n,0)·a^n + C(n,1)·a^(n-1)·b + ... + C(n,n)·b^n",
      "Exemplu: (a+b)² = a² + 2ab + b²",
      "(a+b)³ = a³ + 3a²b + 3ab² + b³",
      "Triunghiul lui Pascal da coeficientii"]),

    # Numere complexe
    ("Ce sunt numerele complexe?",
     "z = a + bi unde i² = -1. a = partea reala, b = partea imaginara.",
     ["Forma algebrica: z = a + bi",
      "Modulul: |z| = sqrt(a² + b²)",
      "Conjugatul: z̄ = a - bi",
      "Operatii: (a+bi)+(c+di) = (a+c)+(b+d)i",
      "Inmultire: (a+bi)(c+di) = (ac-bd)+(ad+bc)i",
      "i² = -1, i³ = -i, i⁴ = 1"]),

    # Geometrie
    ("Cum se calculeaza distanta intre 2 puncte?",
     "d(A,B) = sqrt((xB-xA)² + (yB-yA)²)",
     ["Formula distantei in plan:",
      "d = sqrt((x2-x1)² + (y2-y1)²)",
      "Exemplu: A(1,2), B(4,6)",
      "d = sqrt(9+16) = sqrt(25) = 5"]),
    ("Cum determin ecuatia unei drepte?",
     "Prin 2 puncte: (y-y1)/(y2-y1) = (x-x1)/(x2-x1). Sau: y-y1 = m(x-x1) cu panta m.",
     ["Forma panta-punct: y - y1 = m(x - x1)",
      "Panta: m = (y2-y1)/(x2-x1)",
      "Forma generala: ax + by + c = 0",
      "Drepte paralele: m1 = m2",
      "Drepte perpendiculare: m1·m2 = -1"]),

    # Functii
    ("Ce inseamna studiul complet al unei functii?",
     "Domeniu, paritate, monotonie, extreme, convexitate/concavitate, inflexiune, asimptote, grafic.",
     ["1. Domeniu de definitie",
      "2. Paritate: f(-x)=f(x) para, f(-x)=-f(x) impara",
      "3. f'(x) = 0 => puncte critice",
      "4. Semnul f' => monotonie",
      "5. f''(x) = 0 => puncte de inflexiune",
      "6. Semnul f'' => convexitate/concavitate",
      "7. Asimptote: orizontale, verticale, oblice",
      "8. Tabel de variatie si grafic"]),
    ("Ce sunt asimptotele?",
     "Drepte de care graficul se apropie la infinit. Verticale (x=a), orizontale (y=L), oblice (y=mx+n).",
     ["Asimptota verticala: x=a daca lim f(x) = ±inf cand x->a",
      "Asimptota orizontala: y=L daca lim f(x) = L cand x->±inf",
      "Asimptota oblica: y=mx+n unde m=lim f(x)/x, n=lim(f(x)-mx)"]),
]

for q, a, steps in concepte:
    topic = "concepte"
    if "derivat" in q.lower(): topic = "derivate"
    elif "integral" in q.lower() or "aria" in q.lower(): topic = "integrale"
    elif "limit" in q.lower() or "hopital" in q.lower(): topic = "limite"
    elif "matric" in q.lower() or "determinant" in q.lower() or "cramer" in q.lower(): topic = "matrice"
    elif "ecuat" in q.lower() or "vieta" in q.lower(): topic = "ecuatii"
    elif "progres" in q.lower(): topic = "progresii"
    elif "trigono" in q.lower() or "cerc" in q.lower(): topic = "trigonometrie"
    elif "combin" in q.lower() or "permut" in q.lower() or "aranjam" in q.lower() or "binom" in q.lower(): topic = "combinatorica"
    elif "complex" in q.lower(): topic = "numere complexe"
    elif "geometr" in q.lower() or "dreapt" in q.lower() or "distanta" in q.lower(): topic = "geometrie"
    elif "functie" in q.lower() or "asimptot" in q.lower() or "studiu" in q.lower(): topic = "functii"
    add(q, a, steps, "concept", topic)

# ============================================================================
# INTREBARI "DE CE?" / "CUM?" / "EXPLICA"
# ============================================================================

de_ce = [
    ("De ce derivata lui x^n este n*x^(n-1)?",
     "Se demonstreaza din definitie: lim(h->0) [(x+h)^n - x^n]/h. Dupa dezvoltarea binomiala si simplificare, rezulta n·x^(n-1).",
     ["Din definitie: f'(x) = lim(h->0) [(x+h)^n - x^n] / h",
      "Dezvoltam (x+h)^n cu binomul lui Newton",
      "(x+h)^n = x^n + n·x^(n-1)·h + termeni cu h², h³...",
      "[(x+h)^n - x^n]/h = n·x^(n-1) + termeni cu h",
      "Cand h->0, ramane n·x^(n-1)"]),
    ("De ce integrala este aria de sub grafic?",
     "Integrala definita sumeaza infinit de dreptunghiuri foarte subtiri sub grafic. Suma Riemann → integrala.",
     ["Impartim [a,b] in n intervale egale",
      "Pe fiecare interval, aproximam cu un dreptunghi",
      "Aria ≈ Σ f(xi)·Δx (suma Riemann)",
      "Cand n -> inf si Δx -> 0, suma -> integrala",
      "∫[a,b] f(x)dx = limita sumelor Riemann"]),
    ("De ce formula discriminantului functioneaza?",
     "Se obtine completand patratul in ax²+bx+c=0 si izolandu-l pe x.",
     ["ax² + bx + c = 0, impartim la a:",
      "x² + (b/a)x + c/a = 0",
      "Completam patratul: (x + b/(2a))² = b²/(4a²) - c/a",
      "(x + b/(2a))² = (b² - 4ac) / (4a²)",
      "x + b/(2a) = ± sqrt(b²-4ac) / (2a)",
      "x = (-b ± sqrt(b²-4ac)) / (2a)"]),
    ("De ce sin²x + cos²x = 1?",
     "Din teorema lui Pitagora aplicata pe cercul unitate: cateta² + cateta² = ipotenuza² = 1.",
     ["Pe cercul unitate (raza=1), un punct P are coordonatele (cos(t), sin(t))",
      "P este pe cerc: x² + y² = 1",
      "Deci cos²(t) + sin²(t) = 1",
      "Aceasta e identitatea fundamentala a trigonometriei"]),
    ("De ce det(A) = 0 inseamna ca sistemul nu are solutie unica?",
     "det(A)=0 inseamna ca liniile matricei sunt dependente liniar, deci ecuatiile nu sunt independente.",
     ["Daca det=0, matricea nu e inversabila",
      "Liniile sunt dependente liniar (una e combinatie a celorlalte)",
      "Sistemul are fie 0 solutii (incompatibil), fie infinite solutii (nedeterminat)",
      "Cramer nu se poate aplica cand det=0"]),
    ("De ce e^x este propria sa derivata?",
     "Din definitia lui e ca limita: e = lim(1+1/n)^n. Aceasta proprietate unica face e^x special.",
     ["e este definit ca numarul a carei functie exponentiala e egala cu derivata sa",
      "Demonstratie: (e^x)' = lim(h->0) (e^(x+h) - e^x)/h",
      "= e^x · lim(h->0) (e^h - 1)/h",
      "= e^x · 1 = e^x",
      "Limita remarcabila: lim(h->0) (e^h-1)/h = 1"]),
    ("De ce ln este inversa lui e^x?",
     "Prin definitie: ln(x) = y daca si numai daca e^y = x. Sunt functii inverse.",
     ["e^(ln(x)) = x si ln(e^x) = x",
      "Graficele sunt simetrice fata de y=x",
      "(ln(x))' = 1/x (derivata inversului)"]),
    ("Cum stiu daca o functie e crescatoare sau descrescatoare?",
     "Calculezi derivata: f'(x)>0 => crescatoare, f'(x)<0 => descrescatoare.",
     ["1. Calculezi f'(x)",
      "2. Rezolvi f'(x) = 0 (puncte critice)",
      "3. Studiezi semnul f' pe intervale",
      "4. f' > 0 pe interval => f crescatoare acolo",
      "5. f' < 0 pe interval => f descrescatoare acolo"]),
    ("Cum stiu daca un punct e minim sau maxim?",
     "La punctul critic x0: daca f' schimba din + in -, e maxim. Din - in +, e minim. Sau: f''(x0)>0 minim, f''(x0)<0 maxim.",
     ["Metoda 1: semnul derivatei",
      "  f' trece din + in - => maxim local",
      "  f' trece din - in + => minim local",
      "Metoda 2: derivata a doua",
      "  f''(x0) > 0 => minim",
      "  f''(x0) < 0 => maxim",
      "  f''(x0) = 0 => nu se poate decide"]),
    ("Cum se face integrarea prin parti?",
     "∫u·dv = u·v - ∫v·du. Alegem u = functia care se simplifica la derivare.",
     ["Formula: ∫u·dv = u·v - ∫v·du",
      "Regula LIATE pentru alegerea lui u:",
      "  L - logaritmic, I - invers trig, A - algebric, T - trig, E - exponential",
      "Exemplu: ∫x·e^x dx",
      "  u = x, dv = e^x dx",
      "  du = dx, v = e^x",
      "  = x·e^x - ∫e^x dx = x·e^x - e^x + C"]),
    ("Cum se aplica metoda substitutiei la integrale?",
     "Alegem t = g(x), dt = g'(x)dx, si inlocuim in integrala.",
     ["1. Identificam o parte a integralei ca g(x) si g'(x)",
      "2. Substitutie: t = g(x), dt = g'(x)dx",
      "3. Rescriim integrala in functie de t",
      "4. Integram si revenim la x",
      "Exemplu: ∫2x·e^(x²) dx, t=x², dt=2xdx",
      "= ∫e^t dt = e^t + C = e^(x²) + C"]),
]

for q, a, steps in de_ce:
    topic = "explicatii"
    if "derivat" in q.lower(): topic = "derivate"
    elif "integral" in q.lower() or "aria" in q.lower() or "parti" in q.lower() or "substitut" in q.lower(): topic = "integrale"
    elif "discriminant" in q.lower() or "ecuati" in q.lower(): topic = "ecuatii"
    elif "sin" in q.lower() or "cos" in q.lower() or "trig" in q.lower(): topic = "trigonometrie"
    elif "det" in q.lower() or "matric" in q.lower(): topic = "matrice"
    elif "cresc" in q.lower() or "minim" in q.lower() or "maxim" in q.lower() or "functie" in q.lower(): topic = "functii"
    elif "ln" in q.lower() or "e^x" in q.lower(): topic = "functii"
    elif "limit" in q.lower(): topic = "limite"
    add(q, a, steps, "explanation", topic, 2)

# ============================================================================
# SFATURI PENTRU BAC
# ============================================================================

sfaturi = [
    ("Cum ma pregatesc pentru BAC la matematica?",
     "Rezolva cat mai multe subiecte din anii anteriori. Incepe cu subiectul I (cel mai usor), apoi II si III.",
     ["1. Invata formulele pe de rost",
      "2. Rezolva subiecte din anii anteriori (2015-2025)",
      "3. Incepe cu Subiectul I - e cel mai accesibil",
      "4. La Subiectul II, exerseaza matrice si sisteme",
      "5. La Subiectul III, derivate si integrale (M1) sau functii (M2)",
      "6. Fa zilnic 1-2 subiecte complete",
      "7. Cronometreaza-te (3 ore la BAC)"]),
    ("Ce pica la BAC la matematica?",
     "Subiectul I: ecuatii, progresii, combinatorica. Subiectul II: matrice, sisteme. Subiectul III: analiza (derivate, integrale, limite).",
     ["Subiectul I (30p): exercitii diverse, nivel mediu",
      "  - Ecuatii, inecuatii",
      "  - Progresii aritmetice si geometrice",
      "  - Combinatorica, probabilitati",
      "  - Numere complexe (M1)",
      "Subiectul II (30p): algebra",
      "  - Matrice, determinanti",
      "  - Sisteme de ecuatii (Cramer, Gauss)",
      "Subiectul III (30p): analiza",
      "  - Studiu de functie complet",
      "  - Derivate, monotonie, extreme",
      "  - Integrale, arii"]),
    ("Cat timp am la BAC?",
     "3 ore (180 de minute) pentru toate cele 3 subiecte.",
     ["Total: 3 ore",
      "Recomandare: Subiectul I - 45 min",
      "Subiectul II - 45 min",
      "Subiectul III - 60 min",
      "Verificare: 30 min"]),
    ("Ce nota imi trebuie la BAC?",
     "Minim 5 pentru promovare. Media BAC = (romana + profil + alegere) / 3, minim 6.",
     ["Nota minima per proba: 5",
      "Media minima BAC: 6",
      "Media = (nota_romana + nota_profil + nota_alegere) / 3",
      "Matematica e proba obligatorie la profilul real"]),
    ("Ce formule trebuie sa stiu pe de rost?",
     "Derivate de baza, integrale de baza, formule trigonometrice, relatiile lui Vieta, formula discriminantului.",
     ["DERIVATE: (xⁿ)'=nxⁿ⁻¹, (sinx)'=cosx, (cosx)'=-sinx, (e^x)'=e^x, (lnx)'=1/x",
      "INTEGRALE: ∫xⁿ=xⁿ⁺¹/(n+1), ∫sinx=-cosx, ∫cosx=sinx, ∫e^x=e^x, ∫1/x=ln|x|",
      "ECUATII: delta=b²-4ac, x=(-b±√delta)/(2a), Vieta: x1+x2=-b/a, x1·x2=c/a",
      "TRIGONOMETRIE: sin²+cos²=1, sin2a=2sinacosa, cos2a=cos²a-sin²a",
      "MATRICE: det2x2=ad-bc, Cramer",
      "COMBINATORICA: C(n,k)=n!/(k!(n-k)!), A(n,k)=n!/(n-k)!, P(n)=n!"]),
    ("Ce greseli frecvente se fac la BAC?",
     "Greseli de calcul, uitarea +C la integrale, confundarea regulilor de derivare, nerespectarea conditiilor de existenta.",
     ["1. Greseli de calcul cu semne (minus!)",
      "2. Uitarea constantei +C la integrale nedefinite",
      "3. (fg)' = f'g' (GRESIT! e f'g + fg')",
      "4. Uitarea regulii lantului la derivate compuse",
      "5. Nerespectarea conditiilor: logaritm(>0), radical(>=0), numitor(≠0)",
      "6. La Cramer: gresirea semnelor in determinanti",
      "7. La limite: impartirea la 0 fara sa verifici"]),
]

for q, a, steps in sfaturi:
    add(q, a, steps, "advice", "sfaturi BAC", 1)

# ============================================================================
# CONVERSATIONAL / GENERAL
# ============================================================================

general = [
    ("Salut", "Salut! Sunt asistentul tau de matematica. Cu ce te pot ajuta? Pot rezolva exercitii, explica concepte sau te ajuta sa te pregatesti pentru BAC.",
     ["Sunt asistentul tau de matematica BAC"]),
    ("Buna", "Buna! Ce exercitiu vrei sa rezolvam azi?",
     ["Cu ce te ajut?"]),
    ("Ce poti face?", "Pot rezolva exercitii de matematica pas cu pas, explica concepte, ajuta cu formulele si sfaturi pentru BAC. Scrie orice exercitiu!",
     ["Rezolv exercitii pas cu pas", "Explic concepte", "Dau formule si sfaturi"]),
    ("Multumesc", "Cu placere! Daca mai ai intrebari, sunt aici. Succes la pregatire!",
     ["Cu placere!"]),
    ("Nu inteleg", "Spune-mi exact ce nu intelegi si te ajut. Pot re-explica orice pas sau concept mai simplu.",
     ["Spune-mi ce anume nu intelegi"]),
    ("E greu", "Inteleg ca pare greu, dar o luam pas cu pas. Care e exercitiul concret? Il descompunem in pasi mici.",
     ["Hai sa o luam pas cu pas"]),
    ("Ajutor", "Sunt aici sa te ajut! Poti sa: scrii un exercitiu de rezolvat, intrebi 'ce e derivata?', sau ceri sfaturi de BAC.",
     ["Scrie un exercitiu", "Intreaba un concept", "Cere sfaturi BAC"]),
    ("Poti sa ma ajuti cu matematica?", "Da, sigur! Sunt specializat pe matematica de BAC. Scrie exercitiul sau intrebarea si o rezolvam impreuna.",
     ["Da, sunt specializat pe BAC"]),
    ("Nu stiu de unde sa incep", "Incepe cu Subiectul I care e cel mai accesibil. Vrei sa rezolvam cateva exercitii de tip grila?",
     ["Incepe cu Subiectul I", "Exercitii de grila sunt un bun inceput"]),
    ("Ce e mai important la BAC?", "Subiectul III aduce cele mai multe puncte si e cel mai greu. Dar incepe cu I si II sa iei punctele sigure.",
     ["Subiectul III e cel mai important dar incepe cu I si II"]),
]

for q, a, steps in general:
    add(q, a, steps, "conversation", "conversatie", 1)

# ============================================================================
# INTREBARI DESPRE ERORI SPECIFICE
# ============================================================================

erori = [
    ("Am calculat derivata lui sin(2x) si mi-a dat cos(2x). E corect?",
     "Nu! Ai uitat regula lantului. Derivata lui sin(2x) = 2·cos(2x), nu cos(2x).",
     ["sin(2x) e o functie compusa: sin(u) cu u=2x",
      "Regula lantului: (sin(u))' = cos(u) · u'",
      "u = 2x, u' = 2",
      "Deci (sin(2x))' = cos(2x) · 2 = 2cos(2x)"]),
    ("Am calculat integrala lui 2x si mi-a dat x^2 + C. E corect?",
     "Da, e corect! ∫2x dx = x² + C. Poti verifica derivand: (x²+C)' = 2x ✓",
     ["∫2x dx = 2 · x²/2 + C = x² + C",
      "Verificare: (x² + C)' = 2x ✓"]),
    ("De ce imi da 0 cand calculez determinantul?",
     "det=0 inseamna ca liniile/coloanele sunt dependente liniar. Verifica daca o linie e multiplu al alteia.",
     ["det = 0 inseamna dependenta liniara",
      "Posibil: o linie e combinatie liniara a celorlalte",
      "Sistemul asociat nu are solutie unica"]),
    ("Am calculat limita si imi da 0/0. Ce fac?",
     "0/0 e forma nedeterminata. Factorizeaza, simplifica, sau aplica L'Hopital.",
     ["0/0 = forma nedeterminata",
      "Metoda 1: factorizare si simplificare",
      "Metoda 2: regula L'Hopital: lim f/g = lim f'/g'",
      "Metoda 3: inmultire cu conjugata (la radicali)"]),
    ("De ce imi da delta negativ?",
     "Delta < 0 inseamna ca ecuatia nu are solutii reale. Are 2 solutii complexe conjugate.",
     ["delta = b² - 4ac < 0",
      "Ecuatia nu are solutii in R",
      "Are solutii in C: x = (-b ± i·√|delta|) / (2a)",
      "Solutiile sunt complexe conjugate"]),
    ("Am pus +C si profesorul mi-a pus gresit. De ce?",
     "Probabil la integrala definita. La ∫[a,b] NU se pune +C. +C se pune doar la integrala nedefinita.",
     ["+C se pune DOAR la integrala NEDEFINITA",
      "La integrala definita ∫[a,b]: se calculeaza F(b) - F(a), fara C",
      "C-urile se anuleaza: (F(b)+C) - (F(a)+C) = F(b) - F(a)"]),
]

for q, a, steps in erori:
    topic = "erori"
    if "derivat" in q.lower() or "sin" in q.lower(): topic = "derivate"
    elif "integral" in q.lower(): topic = "integrale"
    elif "determinant" in q.lower(): topic = "matrice"
    elif "limit" in q.lower(): topic = "limite"
    elif "delta" in q.lower(): topic = "ecuatii"
    add(q, a, steps, "error_analysis", topic, 2)

# ============================================================================
# SAVE
# ============================================================================

data_path = Path(__file__).parent.parent / "data" / "processed" / "exercises_merged.json"
existing = []
if data_path.exists():
    with open(data_path, "r", encoding="utf-8") as f:
        existing = json.load(f)

existing_questions = {e.get("question", "") for e in existing}
new_exercises = [e for e in exercises if e["question"] not in existing_questions]
merged = existing + new_exercises

with open(data_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"Exercitii existente: {len(existing)}")
print(f"Q&A noi generate: {len(new_exercises)}")
print(f"Total dupa merge: {len(merged)}")

# Stats pe tipuri
types = {}
for e in merged:
    t = e.get("type", "?")
    types[t] = types.get(t, 0) + 1
print("\nPe tipuri:")
for t, c in sorted(types.items(), key=lambda x: -x[1]):
    print(f"  {t}: {c}")
