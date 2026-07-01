"""
Generate 200+ MORE conversational Q&A pairs for the chatbot.
Covers: detailed concept variants, student common questions, reformulations,
math vocabulary, exam strategies, motivation, common confusions, practice tips.
"""

import json
from pathlib import Path

exercises = []
_id = 6000

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
        "source": "generated_chat_qa_v2",
    })

# ============================================================================
# 1. MAI MULTE CONCEPTE - variante de intrebari pe care le pun elevii
# ============================================================================

concepte_extra = [
    # Derivate - reformulari
    ("Explica-mi derivatele",
     "Derivata masoara cat de repede se schimba o functie. Daca f(x)=x², derivata f'(x)=2x iti spune ca la x=3, functia creste cu viteza 6.",
     ["Derivata = rata de variatie instantanee", "f'(x) = lim(h->0) [f(x+h)-f(x)]/h", "Exemplu: (x²)' = 2x"]),
    ("Ce inseamna sa derivezi?",
     "A deriva inseamna a gasi functia care iti da viteza de variatie. Daca ai pozitia, derivata iti da viteza. Daca ai viteza, derivata iti da acceleratia.",
     ["Derivarea = gasirea ratei de schimbare", "pozitie -> viteza -> acceleratie"]),
    ("Derivata lui e^x de ce e tot e^x?",
     "E^x este unica functie care e egala cu propria sa derivata. Asta vine din definitia numarului e ca limita (1+1/n)^n.",
     ["(e^x)' = e^x · lim(h→0) (e^h-1)/h = e^x · 1 = e^x"]),
    ("Care e derivata lui ln x?",
     "(ln x)' = 1/x. Se demonstreaza din faptul ca ln e functia inversa a lui e^x.",
     ["ln(x) = inversa lui e^x", "(ln x)' = 1/x", "Domeniu: x > 0"]),
    ("Cum derivez o functie compusa?",
     "Aplici regula lantului: (f(g(x)))' = f'(g(x)) · g'(x). Derivezi 'exteriorul' si inmultesti cu derivata 'interiorului'.",
     ["Regula lantului: derivata exteriorul × derivata interiorul",
      "Exemplu: (sin(3x))' = cos(3x) · 3 = 3cos(3x)",
      "(e^(x²))' = e^(x²) · 2x"]),
    ("Ce e derivata de ordin 2?",
     "Derivata a doua f''(x) este derivata derivatei. Arata convexitatea/concavitatea. f''>0 = convexa, f''<0 = concava.",
     ["f''(x) = (f'(x))'", "f''>0 => functia e convexa (forma de U)", "f''<0 => functia e concava (forma de ∩)"]),
    ("Cum gasesc punctele de inflexiune?",
     "Rezolvi f''(x)=0 si verifici ca f'' isi schimba semnul in acel punct.",
     ["1. Calculezi f''(x)", "2. Rezolvi f''(x)=0", "3. Verifici schimbarea de semn", "4. Daca se schimba, e punct de inflexiune"]),

    # Integrale - reformulari
    ("Explica-mi integralele",
     "Integrala e inversa derivatei. Daca stii viteza, integrala iti da pozitia. Geometric, calculeaza aria de sub un grafic.",
     ["Integrala nedefinita: gaseste F(x) cu F'(x) = f(x)", "Integrala definita: calculeaza aria de sub grafic"]),
    ("Ce e integrala nedefinita?",
     "Integrala nedefinita este multimea tuturor primitivelor: F(x) + C, unde F'(x) = f(x). C este constanta de integrare.",
     ["∫f(x)dx = F(x) + C", "F'(x) = f(x)", "C = constanta arbitrara"]),
    ("Ce e integrala definita?",
     "Integrala definita ∫[a,b] f(x)dx = F(b) - F(a) calculeaza aria cu semn de sub graficul functiei pe [a,b].",
     ["∫[a,b] f(x)dx = F(b) - F(a)", "Formula Leibniz-Newton", "Rezultatul e un numar, nu o functie"]),
    ("De ce punem +C la integrale?",
     "Pentru ca daca F'(x) = f(x), atunci si (F(x)+C)' = f(x) pentru orice constanta C. Exista infinit de primitive.",
     ["+C pentru ca derivata constantei = 0", "F(x)+5, F(x)-3, F(x)+100 sunt toate primitive"]),
    ("Cum integrez prin parti?",
     "∫u·dv = u·v - ∫v·du. Alegi u = functia care se simplifica la derivare (LIATE: Log, Invers trig, Algebric, Trig, Exponential).",
     ["∫u dv = uv - ∫v du", "u = functia care se simplifica", "Exemplu: ∫x·cos(x)dx, u=x, dv=cos(x)dx"]),
    ("Ce e integrarea prin substitutie?",
     "Inlocuiesti o parte din integrala cu t = g(x), dt = g'(x)dx. Simplifici integrala si apoi revii la x.",
     ["t = g(x), dt = g'(x)dx", "Exemplu: ∫2x·cos(x²)dx, t=x², dt=2xdx => ∫cos(t)dt = sin(t)+C = sin(x²)+C"]),

    # Limite - reformulari
    ("Explica-mi limitele",
     "Limita iti spune unde 'se duce' o functie cand x se apropie de o valoare. Ex: lim(x→2) x² = 4.",
     ["lim(x→a) f(x) = L inseamna f(x) se apropie de L cand x se apropie de a"]),
    ("Ce e o limita la infinit?",
     "Limita la infinit iti arata comportarea functiei pentru x foarte mare. Ex: lim(x→∞) 1/x = 0.",
     ["lim(x→∞) f(x) = L inseamna ca f(x) se stabilizeaza la L", "lim(x→∞) 1/x = 0, 1/x² = 0"]),
    ("Cum calculez o limita?",
     "Pasii: 1) Inlocuiesti direct. 2) Daca e nedeterminare (0/0, ∞/∞), factorizezi, L'Hopital, sau rationalizezi.",
     ["1. Substitutie directa", "2. Daca 0/0: factorizare sau L'Hopital", "3. Daca ∞/∞: imparti la puterea dominanta"]),
    ("Ce e continuitatea?",
     "O functie e continua in x0 daca: 1) f(x0) exista, 2) limita exista, 3) lim = f(x0). Graficul nu are 'sarituri'.",
     ["f continua in x0 <=> lim(x→x0) f(x) = f(x0)", "Nu poti desena graficul fara sa ridici creionul"]),

    # Matrice - reformulari
    ("Explica-mi matricele",
     "Matricele sunt tabele de numere pe linii si coloane. Le putem aduna, inmulti, calcula determinantul si inversa.",
     ["Matrice m×n: m linii, n coloane", "A+B: element cu element", "A·B: linie × coloana"]),
    ("Cum inmultesc doua matrice?",
     "Element (i,j) = suma produselor de pe linia i din A cu coloana j din B. A(m×n) · B(n×p) = C(m×p).",
     ["c_ij = Σ a_ik · b_kj", "Nr coloane A = Nr linii B", "Exemplu 2×2: [a b; c d]·[e f; g h] = [ae+bg af+bh; ce+dg cf+dh]"]),
    ("Ce e matricea inversa?",
     "A⁻¹ e matricea pentru care A·A⁻¹ = I (matricea identitate). Exista doar daca det(A) ≠ 0.",
     ["A·A⁻¹ = A⁻¹·A = I", "A⁻¹ = adj(A)/det(A)", "Conditie: det(A) ≠ 0"]),
    ("Ce e rangul unei matrice?",
     "Rangul = numarul maxim de linii (sau coloane) liniar independente. E important in studiul sistemelor.",
     ["rang(A) = nr maxim de linii independente", "rang determina nr de solutii ale unui sistem"]),
    ("Cum rezolv un sistem cu Cramer?",
     "x = Dx/D, y = Dy/D, z = Dz/D unde D = det sistemului si Dx = det cu coloana x inlocuita cu termenii liberi.",
     ["1. Scrii matricea si calculezi D", "2. Dx: inlocuiesti coloana x cu termenii liberi", "3. x = Dx/D"]),
    ("Cum rezolv un sistem cu Gauss?",
     "Transformi matricea extinsa in forma esulon (scara) prin operatii elementare pe linii, apoi rezolvi de jos in sus.",
     ["1. Scrii matricea extinsa [A|b]", "2. Eliminare: L2 = L2 - k·L1", "3. Obtii forma scara", "4. Substitutie inversa"]),

    # Combinatorica
    ("Ce e factorialul?",
     "n! = 1·2·3·...·n. Exemplu: 5! = 120. Prin conventie, 0! = 1.",
     ["n! = produsul numerelor de la 1 la n", "5! = 120, 4! = 24, 3! = 6", "0! = 1 (prin conventie)"]),
    ("Cum calculez combinari?",
     "C(n,k) = n! / (k! · (n-k)!). Cate moduri alegi k obiecte din n FARA sa conteze ordinea.",
     ["C(n,k) = n! / (k!(n-k)!)", "Exemplu: C(5,2) = 10", "Nu conteaza ordinea"]),
    ("Cum calculez probabilitati?",
     "P(A) = cazuri favorabile / cazuri posibile. Pentru BAC: identifica spatiul total si evenimentul.",
     ["P(A) = |A| / |Ω|", "Exemplu: zaruri, carti, bile"]),
    ("Ce e principiul incluziunii-excluziunii?",
     "|A ∪ B| = |A| + |B| - |A ∩ B|. Pentru probabilitati: P(A∪B) = P(A) + P(B) - P(A∩B).",
     ["|A ∪ B| = |A| + |B| - |A ∩ B|"]),

    # Numere complexe
    ("Cum adun numere complexe?",
     "(a+bi) + (c+di) = (a+c) + (b+d)i. Aduni partile reale si partile imaginare separat.",
     ["(a+bi) + (c+di) = (a+c) + (b+d)i"]),
    ("Cum inmultesc numere complexe?",
     "(a+bi)(c+di) = ac + adi + bci + bdi² = (ac-bd) + (ad+bc)i.",
     ["(a+bi)(c+di) = (ac-bd) + (ad+bc)i", "Se foloseste i² = -1"]),
    ("Ce e modulul unui numar complex?",
     "|z| = |a+bi| = √(a²+b²). Geometric, e distanta de la origine la punctul (a,b).",
     ["|a+bi| = √(a²+b²)", "Geometric: distanta la origine"]),
    ("Ce e conjugatul?",
     "Conjugatul lui z = a+bi este z̄ = a-bi. z·z̄ = a²+b² = |z|².",
     ["z̄ = a - bi", "z · z̄ = |z|²", "Util la impartirea numerelor complexe"]),
    ("Cum impart numere complexe?",
     "Inmultesti sus si jos cu conjugatul numitorului: (a+bi)/(c+di) = (a+bi)(c-di)/(c²+d²).",
     ["Inmultesti cu conjugatul numitorului", "(a+bi)/(c+di) · (c-di)/(c-di)", "Numitorul devine c²+d²"]),

    # Trigonometrie
    ("Ce e radianul?",
     "Radianul e unitatea de masura a unghiurilor. π radianti = 180°. Un cerc complet = 2π radianti.",
     ["π rad = 180°", "90° = π/2", "60° = π/3", "45° = π/4", "30° = π/6"]),
    ("Cum transform din grade in radiani?",
     "Inmultesti cu π/180. Exemplu: 60° = 60 · π/180 = π/3.",
     ["x° → x · π/180 radianti", "60° = π/3", "90° = π/2", "180° = π"]),
    ("Ce valori trebuie sa stiu la trigonometrie?",
     "sin(0)=0, sin(30°)=1/2, sin(45°)=√2/2, sin(60°)=√3/2, sin(90°)=1. cos e invers.",
     ["sin: 0, 1/2, √2/2, √3/2, 1", "cos: 1, √3/2, √2/2, 1/2, 0", "tg: 0, √3/3, 1, √3, nedef"]),
    ("Ce sunt functiile inverse trigonometrice?",
     "arcsin, arccos, arctg sunt inversele lui sin, cos, tg. arcsin(1/2) = 30° = π/6.",
     ["arcsin: [-1,1] → [-π/2, π/2]", "arccos: [-1,1] → [0, π]", "arctg: R → (-π/2, π/2)"]),

    # Progresii
    ("Cum gasesc ratia unei progresii aritmetice?",
     "Ratia r = a2 - a1 = a3 - a2 = ... Diferenta intre doi termeni consecutivi.",
     ["r = a(n+1) - a(n)", "Daca stii 2 termeni: r = (a_m - a_n) / (m - n)"]),
    ("Cum gasesc ratia unei progresii geometrice?",
     "Ratia q = b2/b1 = b3/b2 = ... Raportul intre doi termeni consecutivi.",
     ["q = b(n+1)/b(n)", "Daca stii 2 termeni: q = (b_m/b_n)^(1/(m-n))"]),
    ("Cum demonstrez ca un sir e progresie aritmetica?",
     "Arati ca a(n+1) - a(n) = constant sau ca 2·a(n) = a(n-1) + a(n+1).",
     ["Metoda 1: a(n+1) - a(n) = r constant", "Metoda 2: 2a_n = a_(n-1) + a_(n+1)"]),

    # Geometrie analitica
    ("Cum aflu ecuatia unui cerc?",
     "(x-a)² + (y-b)² = r² unde (a,b) e centrul si r raza.",
     ["Forma canonica: (x-a)² + (y-b)² = r²", "Forma dezvoltata: x² + y² + Dx + Ey + F = 0"]),
    ("Cum calculez aria unui triunghi cu coordonate?",
     "Aria = |x1(y2-y3) + x2(y3-y1) + x3(y1-y2)| / 2",
     ["Formula cu coordonate: A = |Σ x_i(y_(i+1) - y_(i-1))| / 2", "Sau cu determinant"]),
    ("Cum aflu daca 3 puncte sunt coliniare?",
     "Aria triunghiului format = 0, adica determinantul |x1 y1 1; x2 y2 1; x3 y3 1| = 0.",
     ["Metoda 1: aria = 0", "Metoda 2: panta AB = panta AC"]),
    ("Ce e distanta de la un punct la o dreapta?",
     "d(M, ax+by+c=0) = |a·x0 + b·y0 + c| / √(a²+b²)",
     ["d = |ax0 + by0 + c| / √(a²+b²)", "M(x0, y0), dreapta ax+by+c=0"]),

    # Functii
    ("Ce e domeniul de definitie?",
     "Multimea valorilor lui x pentru care functia are sens. Verifici: numitor≠0, radical≥0, logaritm>0.",
     ["Restrictii: 1/0 interzis", "√(negativ) interzis", "ln(0 sau negativ) interzis"]),
    ("Ce e o functie para? Dar impara?",
     "Para: f(-x) = f(x) (simetrica fata de Oy). Impara: f(-x) = -f(x) (simetrica fata de O).",
     ["f para: grafic simetric fata de Oy (ex: x², cos)", "f impara: grafic simetric fata de O (ex: x³, sin)"]),
    ("Ce sunt asimptotele verticale?",
     "Drepte x = a unde functia tinde la ±∞. Apar la punctele unde numitorul e 0.",
     ["x = a e asimptota verticala daca lim(x→a) f(x) = ±∞", "Exemplu: f(x) = 1/(x-2) are asimptota x = 2"]),
    ("Ce sunt asimptotele orizontale?",
     "Drepte y = L unde functia se stabilizeaza la ±∞. lim(x→±∞) f(x) = L.",
     ["y = L daca lim(x→∞) f(x) = L", "Exemplu: f(x) = (2x+1)/(x+3) are asimptota y = 2"]),
    ("Ce e asimptota oblica?",
     "Dreapta y = mx + n unde m = lim f(x)/x si n = lim(f(x) - mx). Apare cand limita la infinit nu e finita.",
     ["m = lim(x→∞) f(x)/x", "n = lim(x→∞) (f(x) - mx)", "Exista doar daca m ≠ 0 si n finit"]),
    ("Cum gasesc punctele de intersectie cu axele?",
     "Cu Ox: rezolvi f(x) = 0. Cu Oy: calculezi f(0).",
     ["Intersectie cu Ox: f(x) = 0", "Intersectie cu Oy: x = 0, punctul (0, f(0))"]),
    ("Ce e monotonia unei functii?",
     "Monotonia arata unde functia creste si unde scade. Se determina din semnul derivatei f'(x).",
     ["f'(x) > 0 => f crescatoare", "f'(x) < 0 => f descrescatoare", "f'(x) = 0 => punct critic"]),
    ("Ce e convexitatea?",
     "Convexitatea arata daca graficul e in forma de U (convexa, f''>0) sau ∩ (concava, f''<0).",
     ["f''(x) > 0 => convexa (U)", "f''(x) < 0 => concava (∩)", "f''(x) = 0 => posibil inflexiune"]),

    # Ecuatii si inecuatii
    ("Cum rezolv o inecuatie de gradul 2?",
     "Rezolvi ecuatia = 0 (gasesti radacinile), faci tabel de semn, si citesti solutia din tabel.",
     ["1. ax²+bx+c = 0 => x1, x2", "2. Tabel de semn", "3. a>0: negativ intre radacini, pozitiv in afara"]),
    ("Ce e metoda substitutiei la ecuatii?",
     "Inlocuiesti o expresie cu t pentru a simplifica. Ex: ecuatii biquadrate x⁴-5x²+4=0, t=x².",
     ["Notezi t = x² (sau alt termen)", "Rezolvi in t", "Revii la x"]),
    ("Cum rezolv ecuatii cu modul?",
     "|f(x)| = a => f(x) = a sau f(x) = -a. |f(x)| < a => -a < f(x) < a.",
     ["|f(x)| = a: f(x) = a SAU f(x) = -a", "|f(x)| < a: -a < f(x) < a", "|f(x)| > a: f(x) < -a SAU f(x) > a"]),
    ("Ce sunt ecuatiile logaritmice?",
     "Ecuatii cu log: log_a(f(x)) = b => f(x) = a^b. Conditii: baza > 0, baza ≠ 1, argument > 0.",
     ["log_a(x) = b <=> x = a^b", "Conditii: a>0, a≠1, x>0", "Proprietati: log(ab) = log(a)+log(b)"]),
    ("Ce sunt ecuatiile exponentiale?",
     "Ecuatii cu a^x: a^f(x) = a^g(x) => f(x) = g(x). Sau aduci la aceeasi baza.",
     ["a^f(x) = a^g(x) => f(x) = g(x)", "Metoda: aduci la aceeasi baza", "Sau aplici logaritm"]),

    # Probabilitati avansate
    ("Ce e probabilitatea conditionata?",
     "P(A|B) = P(A∩B)/P(B). Probabilitatea ca A sa se intample, stiind ca B s-a intamplat.",
     ["P(A|B) = P(A∩B)/P(B)", "Exemplu: bile din urna"]),
    ("Ce sunt evenimentele independente?",
     "A si B sunt independente daca P(A∩B) = P(A)·P(B). Un eveniment nu influenteaza pe celalalt.",
     ["P(A∩B) = P(A)·P(B)", "Exemplu: aruncari succesive de zar"]),
]

for q, a, steps in concepte_extra:
    topic = "concepte"
    q_low = q.lower()
    if "derivat" in q_low or "derivez" in q_low or "inflexiune" in q_low: topic = "derivate"
    elif "integral" in q_low or "primitiv" in q_low or "substitut" in q_low: topic = "integrale"
    elif "limit" in q_low or "continu" in q_low: topic = "limite"
    elif "matric" in q_low or "determinant" in q_low or "cramer" in q_low or "gauss" in q_low or "rang" in q_low: topic = "matrice"
    elif "ecuati" in q_low or "inecuat" in q_low or "modul" in q_low or "logaritm" in q_low or "exponential" in q_low: topic = "ecuatii"
    elif "progres" in q_low or "sir" in q_low or "ratia" in q_low: topic = "progresii"
    elif "trigono" in q_low or "radian" in q_low or "cerc" in q_low or "sin" in q_low or "cos" in q_low: topic = "trigonometrie"
    elif "combin" in q_low or "permut" in q_low or "aranjam" in q_low or "binom" in q_low or "factorial" in q_low or "probabilit" in q_low: topic = "combinatorica"
    elif "complex" in q_low or "conjugat" in q_low or "modul" in q_low or "impart" in q_low: topic = "numere complexe"
    elif "geometr" in q_low or "dreapt" in q_low or "distanta" in q_low or "cerc" in q_low or "coliniare" in q_low or "triunghi" in q_low: topic = "geometrie"
    elif "functie" in q_low or "asimptot" in q_low or "monoton" in q_low or "domeniu" in q_low or "para" in q_low or "convex" in q_low or "intersect" in q_low: topic = "functii"
    add(q, a, steps, "concept", topic)


# ============================================================================
# 2. INTREBARI DE TIP "NU INTELEG" / "REPETA" / "ALTFEL"
# ============================================================================

reformulari = [
    ("Nu inteleg derivatele",
     "Gandeste-te asa: derivata iti spune cu cat se schimba rezultatul cand schimbi putin inputul. Ex: daca f(x) = 3x, derivata e 3 (pentru fiecare +1 la x, f creste cu 3).",
     ["Derivata = schimbarea outputului / schimbarea inputului"]),
    ("Repeta despre integrale",
     "Integrala este opusul derivatei. Daca (x²)' = 2x, atunci ∫2x dx = x² + C. Geometric, calculeaza aria de sub grafic.",
     ["Integrala = antiderivata", "∫f(x)dx = F(x)+C unde F'=f"]),
    ("Poti sa explici altfel limitele?",
     "Imagineaza-ti ca mergi pe un drum si te apropii de un punct. Limita iti spune unde ajungi, chiar daca nu poti calca exact pe acel punct.",
     ["Limita = valoarea de care te apropii"]),
    ("Mai simplu te rog",
     "Sigur! Spune-mi exact ce concept nu intelegi si il explic cat mai simplu, cu exemple concrete.",
     ["Spune-mi ce nu intelegi"]),
    ("Poti da un exemplu?",
     "Da! Spune-mi la ce subiect vrei exemplu: derivate, integrale, matrice, ecuatii, sau altceva?",
     ["Cu placere, spune-mi subiectul"]),
    ("Nu am inteles pasul ala",
     "Care pas anume? Spune-mi numarul pasului sau copiaza ce nu intelegi si il explic mai detaliat.",
     ["Spune-mi care pas exact"]),
    ("Explica ca pentru cineva de clasa a 5-a",
     "Sigur! Spune-mi ce concept vrei sa explic simplu si il descompun in pasi foarte mici cu exemple din viata reala.",
     ["Spune-mi ce sa explic simplu"]),
    ("Da-mi mai multe detalii",
     "Despre ce anume? Pot detalia orice pas din rezolvare, formula, sau concept. Spune-mi exact.",
     ["Ce vrei sa detaliez?"]),
    ("Nu stiu formula",
     "Spune-mi la ce subiect ai nevoie de formula: derivate, integrale, trigonometrie, matrice? Ti-o dau cu explicatie.",
     ["Spune-mi subiectul"]),
    ("Am uitat formulele",
     "Nu-i nimic! Cele mai importante formule de BAC sunt: derivate de baza, integrale de baza, formule trigonometrice, Cramer, discriminant. Vrei sa le reluam?",
     ["Derivate, integrale, trig, Cramer, discriminant"]),
    ("Cum verific daca am rezolvat bine?",
     "Cel mai simplu: derivezi rezultatul integralei (trebuie sa obtii functia initiala), inlocuiesti in ecuatie, sau verifici conditiile.",
     ["Integrale: derivezi rezultatul", "Ecuatii: inlocuiesti in ecuatie", "Sisteme: verifici in toate ecuatiile"]),
]

for q, a, steps in reformulari:
    add(q, a, steps, "conversation", "conversatie")


# ============================================================================
# 3. MOTIVATIE SI SFATURI PRACTICE
# ============================================================================

motivatie = [
    ("Mi-e frica de BAC",
     "E normal sa fii stresat, dar cu pregatire constanta vei fi ok! Rezolva zilnic macar un subiect complet si vei vedea progresul.",
     ["Pregatire constanta > invatare de ultima ora", "1 subiect/zi = 30 subiecte in ultima luna"]),
    ("Nu am timp sa invat",
     "Fa un plan: 30-45 minute pe zi conteaza mult. Subiectul I (45 min), Subiectul II (45 min), Subiectul III (1 ora). Altereaza zilnic.",
     ["30-45 min/zi e suficient", "Alternezi subiectele"]),
    ("E prea greu Subiectul III",
     "Subiectul III pare greu dar are un sablon fix: studiu de functie. Invata sablonul (domeniu, derivata, monotonie, extreme, grafic) si exerseaza-l.",
     ["Sablonul fix: D, f', monotonie, extreme, grafic", "Exerseaza 20 de studii de functie"]),
    ("Cum iau 10 la BAC?",
     "Pentru nota 10: rezolva subiecte complete corect si complet, scrie curat, justifica FIECARE pas, verifica rezultatele.",
     ["Rezolvare completa si clara", "Justificare la fiecare pas", "Verificare la final"]),
    ("Cum iau minim 5 la BAC?",
     "Focus pe Subiectul I (30p) - sunt exercitii directe. Plus 1-2 exercitii din Subiectul II (matrice simple). Total ~40p => nota ~6.",
     ["Subiectul I complet = 30p", "1-2 din Subiectul II = 10-15p", "Total: ~45p => nota ~6.5"]),
    ("Cat mai e pana la BAC?",
     "Indiferent cat mai e, important e sa incepi acum! Fiecare zi conteaza. Fa-ti un plan si tine-te de el.",
     ["Incepe acum!", "Planul e mai important decat numarul de zile"]),
    ("Sunt prost la mate",
     "Nu esti prost! Matematica e o abilitate care se dezvolta cu practica. Nimeni nu s-a nascut stiind derivate. Ia-o pas cu pas!",
     ["Matematica = abilitate, nu talent", "Practica face perfect"]),
    ("Nu imi place matematica",
     "Inteleg, dar la BAC trebuie sa treci. Gandeste-te la ea ca la un joc cu reguli - inveti regulile si aplici. Nu trebuie sa-ti placa, trebuie doar sa o faci!",
     ["Trateaz-o ca un joc cu reguli", "Invata regulile si aplica"]),
    ("Merita sa iau meditatii?",
     "Daca te poti pregati singur cu discipline, nu e obligatoriu. Dar daca ai lacune mari sau nu stii de unde sa incepi, un mediator bun ajuta enorm.",
     ["Depinde de nivelul tau", "Daca ai lacune mari, da"]),
    ("Ce resurse recomanzi?",
     "Subiecte de BAC din anii anteriori (2015-2025), manualul M1/M2, canale YouTube de matematica, si aplicatia asta! Cel mai important: practica!",
     ["Subiecte BAC anterioare", "Manual", "YouTube", "Aceasta aplicatie"]),
]

for q, a, steps in motivatie:
    add(q, a, steps, "advice", "motivatie")


# ============================================================================
# 4. CONVERSATII GENERALE - raspunsuri naturale
# ============================================================================

conversatii = [
    ("Cine esti?", "Sunt SmartBAC, asistentul tau de matematica pentru BAC! Pot rezolva exercitii, explica concepte si te ajuta cu pregatirea.",
     ["Sunt SmartBAC"]),
    ("Esti real?", "Sunt un chatbot creat sa te ajute cu matematica de BAC. Nu sunt om, dar stiu matematica!",
     ["Sunt un chatbot specializat pe BAC"]),
    ("Ce materii stii?", "Sunt specializat pe matematica de BAC: algebra, analiza, geometrie, combinatorica. Nu pot ajuta cu alte materii deocamdata.",
     ["Doar matematica de BAC"]),
    ("Ma poti ajuta la romana?", "Din pacate nu, sunt specializat doar pe matematica. Dar pentru BAC la mate, sunt aici!",
     ["Doar matematica"]),
    ("Esti mai bun decat ChatGPT?", "Sunt specializat pe matematica de BAC romanesc, deci la exercitiile de BAC ar trebui sa fiu mai precis! Hai sa testam.",
     ["Sunt specializat pe BAC romanesc"]),
    ("Glumeste ceva", "De ce a trecut limita peste drum? Ca sa ajunga la cealalta parte... a intervalului! 😄 Acum hai la treaba!",
     ["Gluma matematica"]),
    ("Pa", "La revedere! Succes la pregatire si nu uita sa exersezi zilnic! 📚",
     ["La revedere!"]),
    ("Buna dimineata", "Buna dimineata! Gata de matematica? Cu ce incepem azi?",
     ["Cu ce te ajut?"]),
    ("Buna seara", "Buna seara! Sesiune de studiu seara? Ce exercitii rezolvam?",
     ["Ce rezolvam?"]),
    ("Noapte buna", "Noapte buna! Odihna e importanta pentru invatare. Maine continuam!",
     ["Odihna buna!"]),
    ("Mersi mult", "Cu placere! Sunt aici oricand ai nevoie. Succes!",
     ["Cu placere!"]),
    ("Esti destept", "Multumesc! Am fost antrenat sa rezolv exercitii de BAC. Hai sa rezolvam unul impreuna!",
     ["Hai sa rezolvam!"]),
    ("Te iubesc", "Haha, multumesc! Si eu te apreciez ca inveti! Hai sa ne concentram pe mate acum. 😊",
     ["Hai la mate!"]),
    ("Ce faci?", "Sunt gata sa te ajut cu matematica! Ce exercitiu ai sau ce vrei sa intelegi?",
     ["Pregatit sa te ajut"]),
    ("Ma plictisesc", "Hai sa facem matematica interesanta! Vrei un exercitiu provocator, un puzzle logic, sau sa vedem cat de repede rezolvi 5 exercitii?",
     ["Exercitiu provocator sau mini-quiz?"]),
    ("Ce ora e?", "Nu stiu exact ora, dar stiu ca e mereu un moment bun sa inveti! Ce exercitiu rezolvam?",
     ["E mereu timp de mate"]),
    ("Stii engleza?", "Sunt facut pentru matematica in limba romana, special pentru BAC-ul romanesc. Hai sa vorbim in romana!",
     ["Vorbesc romana"]),
    ("Esti gratuit?", "Da! Sunt parte din aplicatia SmartBAC si te pot ajuta gratuit cu pregatirea pentru BAC.",
     ["Da, sunt gratuit"]),
    ("Ce tema am?", "Nu stiu ce tema ai, dar daca imi spui exercitiile te ajut sa le rezolvi pas cu pas!",
     ["Spune-mi exercitiile"]),
    ("Am o problema", "Spune-mi problema si o rezolvam impreuna! Scrie enuntul complet si iti dau rezolvarea pas cu pas.",
     ["Scrie enuntul"]),
]

for q, a, steps in conversatii:
    add(q, a, steps, "conversation", "conversatie")


# ============================================================================
# 5. ERORI SPECIFICE COMUNE
# ============================================================================

erori_extra = [
    ("Am gresit la determinant. Ce fac gresit?",
     "Greselile frecvente: semne gresite la Sarrus (diagonalele secundare se scad), inversarea liniilor cu coloanele, erori de calcul.",
     ["Verifica: diagonalele principale se aduna", "Diagonalele secundare se SCAD", "Recalculeaza fiecare produs"]),
    ("De ce imi da limita infinit?",
     "Daca limita e infinit, functia nu are asimptota orizontala in acea directie. Verifica daca ai impartit corect la termenul dominant.",
     ["lim = ∞ inseamna ca functia creste fara limita", "Verifica gradul numaratorului vs numitorului"]),
    ("Am rezolvat integrala si profesorul a zis ca e gresit",
     "Verificare rapida: deriveaza rezultatul tau. Trebuie sa obtii functia de sub integrala. Daca nu, ai gresit undeva.",
     ["Derivezi F(x) si compari cu f(x)", "Verifica si constanta +C la integrale nedefinite"]),
    ("De ce imi da sistemul incompatibil?",
     "det = 0 si cel putin un Dx sau Dy ≠ 0 => incompatibil (fara solutie). Ecuatiile sunt contraditorii.",
     ["det = 0 si Dx ≠ 0 => incompatibil", "Geometric: dreptele sunt paralele"]),
    ("Nu imi iese rezultatul din carte",
     "Posibil: 1) Ai gresit un calcul mic (verifica semnele), 2) Cartea are o eroare (se intampla), 3) Ai simplificat altfel dar rezultatul e echivalent.",
     ["Verifica semnele", "Compara forma, nu doar cifra", "Cartile pot avea erori"]),
    ("Am pus gresit parantezele si nu stiu unde am gresit",
     "Parantezele sunt critice! Regula: inmultirea se face INAINTE de adunare. Rescrie pas cu pas, punand paranteze la fiecare operatie.",
     ["Prioritate: paranteze > puteri > inmultire > adunare", "Rescrie pas cu pas"]),
    ("De ce mi-a iesit un rezultat negativ la arie?",
     "Aria e mereu pozitiva! Daca ti-a iesit negativ: 1) Ai inversat limitele de integrare, 2) Nu ai pus modul. Aria = |∫f(x)dx|.",
     ["Aria = |∫f(x)dx|", "Verifica limitele de integrare a < b"]),
    ("Am obtinut 2 solutii dar una nu merge",
     "Probabil una din solutii nu respecta conditiile de existenta (domeniul). La logaritmi: argument > 0. La radicali: sub radical >= 0.",
     ["Verifica conditiile de existenta", "Inlocuieste in ecuatia originala"]),
    ("De ce la matrice ordinea conteaza?",
     "La inmultirea matricelor, A·B ≠ B·A in general. Ordinea conteaza! La adunare, ordinea nu conteaza.",
     ["A·B ≠ B·A (in general)", "Dar A+B = B+A (mereu)"]),
    ("Cum stiu cand sa aplic L'Hopital si cand nu?",
     "L'Hopital DOAR la 0/0 sau ∞/∞. Daca nu e forma nedeterminata, NU aplici. Prima data incearca substitutia directa!",
     ["DOAR la 0/0 sau ∞/∞", "Prima data substitutie directa", "Daca nu e nedeterminare, nu folosesti L'Hopital"]),
]

for q, a, steps in erori_extra:
    topic = "erori"
    q_low = q.lower()
    if "derivat" in q_low: topic = "derivate"
    elif "integral" in q_low or "aria" in q_low or "arie" in q_low: topic = "integrale"
    elif "determinant" in q_low or "matrice" in q_low or "sistem" in q_low: topic = "matrice"
    elif "limit" in q_low or "hopital" in q_low: topic = "limite"
    elif "parantez" in q_low or "rezultat" in q_low or "solutii" in q_low: topic = "erori comune"
    add(q, a, steps, "error_analysis", topic, 2)


# ============================================================================
# 6. STRATEGII DE REZOLVARE
# ============================================================================

strategii = [
    ("Cum abordez un studiu de functie?",
     "Sablonul fix: 1) Domeniu, 2) Limite la capete, 3) Derivata si tabel semne, 4) Monotonie, extreme, 5) f'' pt convexitate, 6) Grafic.",
     ["1. D = domeniul de definitie", "2. Limite la capetele domeniului (asimptote)",
      "3. f'(x), semnul, tabel variatie", "4. Monotonie si puncte de extrem",
      "5. f''(x) pentru convexitate si inflexiune", "6. Graficul functiei"]),
    ("Cum rezolv exercitiile de la Subiectul I?",
     "Subiectul I: citeste ATENT, sunt exercitii directe (aplici formula). Greseli frecvente: calcul gresit, semne inversate. Verifica!",
     ["Citeste enuntul cu atentie", "Aplica formula direct", "Verifica raspunsul"]),
    ("Cum rezolv exercitiile de la Subiectul II?",
     "Subiectul II: matrice si sisteme. Invata Cramer, Gauss, puterea matricelor. Atentie la calcule cu determinanti!",
     ["Matrice: det, inversa, putere", "Sisteme: Cramer (det≠0) sau Gauss (det=0)", "Verifica inmultirile"]),
    ("Cum fac tabelul de variatie?",
     "1) Derivezi f(x). 2) Rezolvi f'(x)=0. 3) Determini semnul f' pe intervale. 4) Notezi crescator/descrescator. 5) Adaugi valorile extreme.",
     ["1. f'(x) = 0 => puncte critice", "2. Semnul f' pe intervale",
      "3. + = crescator, - = descrescator", "4. Valorile f(xi) la punctele critice"]),
    ("Cum demonstrez ca o functie e bijectiva?",
     "O functie e bijectiva daca e injectiva (strict monotona) si surjectiva (ia toate valorile din codomeniu). La BAC: arata ca e strict monotona.",
     ["Bijectiva = injectiva + surjectiva", "Strict crescatoare/descrescatoare => injectiva",
      "lim la capete acopera tot codomeniul => surjectiva"]),
    ("Cum rezolv un exercitiu cu parametru?",
     "Discuti dupa valorile parametrului: de obicei cand e 0, pozitiv, negativ. La ecuatii: discuti dupa discriminant (delta > 0, = 0, < 0).",
     ["Discuti dupa valorile parametrului", "La ecuatii: delta > 0, = 0, < 0",
      "Nu uita cazurile speciale (a = 0 la ecuatie de grad 2)"]),
    ("Cum demonstrez o inegalitate?",
     "Metode: 1) Treci totul intr-o parte si arati ca e >=0. 2) Folosesti AM-GM. 3) Derivezi si arati ca minimul e >=0.",
     ["Metoda 1: f(x) >= 0, arata ca f are minim >= 0",
      "Metoda 2: AM >= GM", "Metoda 3: Jensen/convexitate"]),
    ("Cum rezolv probleme de geometrie analitica?",
     "1) Alegi un sistem de coordonate bun. 2) Scrii ecuatiile dreptelor/cercurilor. 3) Rezolvi intersectii/distante.",
     ["Alege bine originea si axele", "Scrie ecuatiile", "Intersectii = rezolvi sisteme"]),
]

for q, a, steps in strategii:
    add(q, a, steps, "strategy", "strategie", 2)


# ============================================================================
# 7. INTREBARI SPECIFICE PROFIL M3/M4
# ============================================================================

profil_specific = [
    ("Ce e diferit la M3 fata de M1?",
     "M3 (Tehnologic) are programa mai usoara: fara numere complexe, integrale mai simple, fara studii de functie dificile. Focus pe aplicatii practice.",
     ["M3 = varianta mai accesibila", "Fara numere complexe", "Integrale si derivate de baza"]),
    ("Ce pica la M3?",
     "La M3: ecuatii, sisteme, matrice 2x2, derivate de baza, integrale simple, progresii. Fara numere complexe sau studii de functie grele.",
     ["Ecuatii si sisteme", "Matrice 2x2", "Derivate si integrale de baza", "Progresii"]),
    ("Ce e diferit la M4 fata de M1?",
     "M4 (Pedagogic) e similar cu M3 dar cu accent pe geometrie si matematica aplicata. Mai putin abstract.",
     ["Similar cu M3", "Accent pe geometrie", "Matematica aplicata"]),
    ("Ce pica la M4?",
     "La M4: ecuatii de baza, sisteme 2x2, matrice simple, derivate de baza, integrale simple, geometrie analitica.",
     ["Ecuatii si sisteme de baza", "Matrice 2x2", "Derivate simple", "Geometrie"]),
    ("Ce e diferit la M2 fata de M1?",
     "M2 (Stiinte) e foarte similar cu M1 dar cu exercitii putin mai usoare la Subiectul III. Aceleasi subiecte, nivel usor mai mic.",
     ["Similar cu M1", "Exercitii putin mai usoare la Subiectul III", "Aceleasi teme"]),
    ("Ce profil e mai greu?",
     "M1 > M2 > M3 ≈ M4 ca dificultate. M1 (Mate-Info) e cel mai greu, M3 si M4 sunt cele mai accesibile.",
     ["M1 cel mai greu", "M3/M4 cele mai usoare"]),
]

for q, a, steps in profil_specific:
    add(q, a, steps, "advice", "profile BAC")


# ============================================================================
# 8. CONCEPTE SUPLIMENTARE
# ============================================================================

suplimentare = [
    ("Ce e sirul lui Fibonacci?",
     "1, 1, 2, 3, 5, 8, 13, ... Fiecare termen = suma celor 2 anteriori: F(n) = F(n-1) + F(n-2).",
     ["F(1)=1, F(2)=1", "F(n) = F(n-1) + F(n-2)", "1, 1, 2, 3, 5, 8, 13, 21, 34..."]),
    ("Ce e numarul e?",
     "e ≈ 2.71828... E baza logaritmului natural. e = lim(n→∞) (1+1/n)^n. E special pentru ca (e^x)' = e^x.",
     ["e ≈ 2.71828", "e = lim(1+1/n)^n", "(e^x)' = e^x"]),
    ("Ce e numarul pi?",
     "π ≈ 3.14159... Raportul dintre circumferinta si diametrul oricarui cerc. Apare in trigonometrie, integrale, serii.",
     ["π ≈ 3.14159", "Circumferinta = 2πr", "Aria cerc = πr²"]),
    ("Ce e un logaritm?",
     "log_a(b) = x inseamna a^x = b. Logaritmul iti spune 'la ce putere ridici baza ca sa obtii numarul'.",
     ["log_a(b) = x <=> a^x = b", "ln(x) = log_e(x)", "lg(x) = log_10(x)"]),
    ("Ce sunt numerele irationale?",
     "Numere care nu pot fi scrise ca fractie. Exemple: √2, π, e. Au infinit de zecimale neperiodice.",
     ["Nu se pot scrie p/q", "Exemple: √2, √3, π, e"]),
    ("Ce e inductia matematica?",
     "Metoda de demonstratie: 1) Verifici pentru n=1 (baza). 2) Presupui pt n=k (ipoteza). 3) Demonstrezi pt n=k+1 (pas inductiv).",
     ["1. Baza: verifici n=1", "2. Ipoteza: presupui pt n=k",
      "3. Pasul: demonstrezi pt n=k+1"]),
    ("Ce e teorema lui Rolle?",
     "Daca f e continua pe [a,b], derivabila pe (a,b), si f(a)=f(b), atunci exista c in (a,b) cu f'(c)=0.",
     ["Conditii: f continua, derivabila, f(a)=f(b)", "Concluzie: exista c cu f'(c)=0"]),
    ("Ce e teorema lui Lagrange?",
     "Daca f e continua pe [a,b] si derivabila pe (a,b), exista c in (a,b) cu f'(c) = (f(b)-f(a))/(b-a).",
     ["Generalizarea teoremei lui Rolle", "f'(c) = (f(b)-f(a))/(b-a)", "Panta tangentei = panta secantei"]),
    ("Ce e teorema lui Fermat?",
     "Daca f are extrem local in x0 si f e derivabila in x0, atunci f'(x0) = 0.",
     ["Extrem + derivabila => f'(x0) = 0", "Atentie: reciproca nu e adevarata"]),
    ("Ce e formula lui Taylor?",
     "f(x) ≈ f(a) + f'(a)(x-a) + f''(a)(x-a)²/2! + ... Aproximeaza o functie cu un polinom.",
     ["f(x) = Σ f^(n)(a)/n! · (x-a)^n", "Caz particular a=0: McLaurin"]),
    ("Ce e o serie?",
     "O serie este o suma infinita: Σ a_n. Poate fi convergenta (are o suma finita) sau divergenta.",
     ["Σ a_n = a_1 + a_2 + a_3 + ...", "Convergenta: suma finita", "Divergenta: suma infinita sau nu exista"]),
    ("Ce e spatiul vectorial?",
     "O multime cu operatii de adunare si inmultire cu scalar care respecta anumite axiome. Exemplu: R², R³.",
     ["V cu + si · scalar", "Axiome: asociativitate, comutativitate, element neutru, etc."]),
]

for q, a, steps in suplimentare:
    topic = "concepte avansate"
    q_low = q.lower()
    if "fibonacci" in q_low or "sir" in q_low: topic = "progresii"
    elif "logaritm" in q_low: topic = "functii"
    elif "inducti" in q_low: topic = "demonstratii"
    elif "rolle" in q_low or "lagrange" in q_low or "fermat" in q_low or "taylor" in q_low: topic = "teoreme"
    elif "serie" in q_low: topic = "serii"
    elif "vector" in q_low: topic = "algebra liniara"
    add(q, a, steps, "concept", topic)


# ============================================================================
# 9. MINI-DIALOG - intrebari scurte, raspunsuri rapide
# ============================================================================

mini_dialog = [
    ("Da", "Super! Continua sa exersezi si o sa vezi rezultatele. Ce exercitiu urmeaza?",
     ["Hai mai departe"]),
    ("Nu", "Ok, nu-i problema! Spune-mi cu ce te pot ajuta altfel.",
     ["Cu ce te ajut?"]),
    ("Ok", "Perfect! Daca ai alte intrebari, sunt aici. Hai la urmatorul exercitiu!",
     ["Sunt aici"]),
    ("Am inteles", "Excelent! Vrei sa trecem la urmatorul subiect sau sa mai exersam?",
     ["Mai exersam sau trecem mai departe?"]),
    ("Mai vreau", "Sigur! Ce vrei: un exercitiu mai greu, acelasi tip dar altul, sau alt subiect?",
     ["Exercitiu mai greu, alt exercitiu, sau alt subiect?"]),
    ("Gata", "Bine! Felicitari pentru sesiunea de studiu! Revin oricand ai nevoie. Succes!",
     ["Bravo ca ai exersat!"]),
    ("Alt exercitiu", "Sigur! Ce tip vrei: ecuatii, derivate, integrale, matrice, sau altceva?",
     ["Ce tip de exercitiu?"]),
    ("Mai greu", "Ok, iti dau ceva mai provocator! Spune-mi subiectul si iti dau un exercitiu de dificultate mare.",
     ["Ce subiect vrei?"]),
    ("Mai usor", "Nicio problema! Hai sa luam ceva mai simplu si crestem treptat dificultatea.",
     ["Incepem mai simplu"]),
    ("Cum?", "Intrebarea ta e prea generala. Spune-mi exact ce vrei sa stii: cum se rezolva un exercitiu? cum se aplica o formula?",
     ["Fii mai specific"]),
    ("De ce?", "Buna intrebare! Dar trebuie sa fiu mai specific - de ce ce anume? De ce o formula, un rezultat, o metoda?",
     ["Spune-mi la ce te referi"]),
    ("Care?", "Depinde de context! Spune-mi mai exact la ce te referi si iti raspund detaliat.",
     ["Fii mai specific"]),
    ("Serios?", "Da, serios! Matematica e logica pura, nu minte niciodata. Vrei sa iti demonstrez?",
     ["Da, verificam impreuna"]),
    ("Wow", "Da, matematica poate fi surprinzatoare! Vrei sa exploram mai multe lucruri interesante?",
     ["Matematica e frumoasa"]),
    ("Bravo", "Multumesc! Dar meritele sunt ale tale ca inveti! Continua asa!",
     ["Continua sa inveti!"]),
    ("Ce tema sa fac?", "Depinde ce ai la scoala! Dar pentru BAC recomand: derivate si integrale zilnic, matrice de 3 ori pe saptamana, si exercitii diverse in weekend.",
     ["Derivate si integrale zilnic", "Matrice de 3 ori/saptamana"]),
    ("Ce note ai?", "Sunt un chatbot, nu am note! Dar te ajut sa iei tu note mari la BAC! Ce exercitiu rezolvam?",
     ["Te ajut cu BAC"]),
    ("Esti prost", "Imi pare rau daca nu te-am ajutat bine! Spune-mi exact ce ai nevoie si incerc din nou mai bine.",
     ["Incerc din nou"]),
    ("Nu functionezi bine", "Imi pare rau! Spune-mi exact ce intrebare ai si incerc sa dau un raspuns mai bun. Cu cat esti mai specific, cu atat pot ajuta mai bine.",
     ["Fii specific si incerc din nou"]),
    ("Vreau sa rezolv ceva", "Perfect! Scrie exercitiul complet (cu tot enuntul) si il rezolv pas cu pas.",
     ["Scrie exercitiul complet"]),
]

for q, a, steps in mini_dialog:
    add(q, a, steps, "conversation", "conversatie")


# ============================================================================
# 10. INTREBARI FRECVENTE DIVERSE
# ============================================================================

diverse = [
    ("Ce e o functie?",
     "O functie f: A→B asociaza fiecarui element din A exact un element din B. Exemplu: f(x) = 2x+1.",
     ["f: A → B", "Fiecarui x ii corespunde un singur f(x)", "Graficul: multimea punctelor (x, f(x))"]),
    ("Ce e o ecuatie?",
     "O egalitate care contine o necunoscuta. A rezolva = a gasi valorile necunoscutei care fac egalitatea adevarata.",
     ["Exemplu: 2x + 3 = 7", "Solutia: x = 2"]),
    ("Ce e o inecuatie?",
     "Ca o ecuatie, dar cu <, >, ≤, ≥ in loc de =. Solutia e un interval sau reuniune de intervale.",
     ["Exemplu: 2x + 1 > 5 => x > 2", "Solutia: (2, +∞)"]),
    ("Ce e un polinom?",
     "Expresie de forma a_n·x^n + ... + a_1·x + a_0. Gradul = cea mai mare putere cu coeficient nenul.",
     ["P(x) = a_n·xⁿ + ... + a₁x + a₀", "Grad n = puterea maxima", "Exemplu: 3x²-2x+1 e grad 2"]),
    ("Cum factorizez?",
     "Metode: 1) Factor comun, 2) Formule scurte (a²-b², a³±b³), 3) Grupare, 4) Radacini (schema Horner).",
     ["a²-b² = (a-b)(a+b)", "a²+2ab+b² = (a+b)²", "Schema Horner: imparti la (x-r)"]),
    ("Ce sunt formulele de calcul prescurtat?",
     "(a+b)² = a²+2ab+b², (a-b)² = a²-2ab+b², a²-b² = (a-b)(a+b), (a+b)³ = a³+3a²b+3ab²+b³",
     ["(a±b)² = a² ± 2ab + b²", "a²-b² = (a-b)(a+b)", "(a±b)³ = a³ ± 3a²b + 3ab² ± b³"]),
    ("Cum rezolv un sistem de 3 ecuatii cu 3 necunoscute?",
     "Metoda Cramer (daca det≠0) sau Gauss (mereu). La BAC, de obicei Cramer.",
     ["Cramer: x=Dx/D, y=Dy/D, z=Dz/D", "Gauss: eliminare si substitutie inversa"]),
    ("Ce e un numar prim?",
     "Un numar natural > 1 care se divide doar cu 1 si cu el insusi. Primele: 2, 3, 5, 7, 11, 13...",
     ["Definitie: doar 2 divizori: 1 si numarul", "2 e singurul numar prim par"]),
    ("Ce e CMMDC si CMMMC?",
     "CMMDC = cel mai mare divizor comun. CMMMC = cel mai mic multiplu comun. CMMDC·CMMMC = a·b.",
     ["CMMDC(12,8) = 4", "CMMMC(12,8) = 24", "CMMDC(a,b) · CMMMC(a,b) = a · b"]),
    ("Ce e valoarea absoluta?",
     "|x| = x daca x≥0, |x| = -x daca x<0. Geometric: distanta de la x la 0 pe axa numerelor.",
     ["|x| = distanta la 0", "|3| = 3, |-3| = 3", "|a-b| = distanta intre a si b"]),
]

for q, a, steps in diverse:
    topic = "concepte"
    q_low = q.lower()
    if "functie" in q_low: topic = "functii"
    elif "ecuatie" in q_low or "inecuati" in q_low: topic = "ecuatii"
    elif "polinom" in q_low or "factorizez" in q_low or "formule" in q_low: topic = "algebra"
    elif "sistem" in q_low: topic = "sisteme"
    elif "prim" in q_low or "cmmdc" in q_low or "absolut" in q_low: topic = "aritmetica"
    add(q, a, steps, "concept", topic)


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
