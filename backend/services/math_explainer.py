"""
Math Explainer Service — Dicționar de concepte BAC cu explicații clare.
Fiecare concept: definiție, analogie, formule, reguli, exemple, greșeli frecvente.
"""

CONCEPTS = {
    "derivata": {
        "concept": "Derivata",
        "ce_este": (
            "Derivata unei funcții măsoară CÂT DE REPEDE se schimbă funcția "
            "într-un punct dat. Este panta tangentei la graficul funcției."
        ),
        "analogie": (
            "Gândește-te la vitezometrul mașinii: dacă f(t) = distanța parcursă, "
            "atunci f'(t) = viteza instantanee. Derivata îți spune cât de repede "
            "se schimbă ceva la un moment dat."
        ),
        "formula": "f'(x) = lim[h→0] (f(x+h) - f(x)) / h",
        "reguli": [
            "Puterea: (xⁿ)' = n·xⁿ⁻¹",
            "Constanta: (c)' = 0",
            "Suma: (f+g)' = f' + g'",
            "Produsul: (f·g)' = f'·g + f·g'",
            "Câtul: (f/g)' = (f'·g - f·g') / g²",
            "Lanțul: (f(g(x)))' = f'(g(x))·g'(x)",
            "Exponențiala: (eˣ)' = eˣ",
            "Logaritmul: (ln x)' = 1/x",
        ],
        "exemple": [
            {
                "problema": "f(x) = x²",
                "rezolvare": "f'(x) = 2x",
                "explicatie": "Aplicăm regula puterii: coborâm exponentul (2) și scădem 1 → 2·x¹ = 2x",
            },
            {
                "problema": "f(x) = 3x³ + 2x - 5",
                "rezolvare": "f'(x) = 9x² + 2",
                "explicatie": "Derivăm termen cu termen: 3·3·x² + 2·1·x⁰ + 0 = 9x² + 2",
            },
            {
                "problema": "f(x) = x⁴ - 2x² + 1",
                "rezolvare": "f'(x) = 4x³ - 4x",
                "explicatie": "4·x³ - 2·2·x + 0 = 4x³ - 4x",
            },
            {
                "problema": "f(x) = (2x+1)³",
                "rezolvare": "f'(x) = 3(2x+1)²·2 = 6(2x+1)²",
                "explicatie": "Regula lanțului: derivăm funcția exterioară · derivata celei interioare",
            },
            {
                "problema": "f(x) = x·eˣ",
                "rezolvare": "f'(x) = eˣ + x·eˣ = eˣ(1+x)",
                "explicatie": "Regula produsului: x'·eˣ + x·(eˣ)' = eˣ + x·eˣ",
            },
        ],
        "greseli_frecvente": [
            "Uitarea scăderii cu 1 a exponentului",
            "Neaplicarea regulii produsului/câtului când e cazul",
            "Derivata constantei este 0, NU constanta",
            "Confuzia (xⁿ)' = nxⁿ⁻¹ cu (xⁿ)' = nxⁿ",
        ],
    },

    "integrala": {
        "concept": "Integrala",
        "ce_este": (
            "Integrala este operația INVERSĂ derivatei. Dacă derivata dă panta, "
            "integrala dă aria de sub grafic. Primitiva F a lui f satisface F' = f."
        ),
        "analogie": (
            "Dacă derivata = viteza, atunci integrala = distanța totală parcursă. "
            "Aduni toate 'feliile' infinit de mici ale ariei de sub grafic."
        ),
        "formula": "∫ f(x) dx = F(x) + C, unde F'(x) = f(x)",
        "reguli": [
            "Puterea: ∫ xⁿ dx = xⁿ⁺¹/(n+1) + C (n ≠ -1)",
            "Constanta: ∫ a dx = ax + C",
            "Suma: ∫ (f+g) dx = ∫f dx + ∫g dx",
            "Exponențiala: ∫ eˣ dx = eˣ + C",
            "1/x: ∫ (1/x) dx = ln|x| + C",
        ],
        "exemple": [
            {
                "problema": "∫ x² dx",
                "rezolvare": "x³/3 + C",
                "explicatie": "Creștem exponentul cu 1 (2→3) și împărțim la noul exponent",
            },
            {
                "problema": "∫ (3x² + 2x - 1) dx",
                "rezolvare": "x³ + x² - x + C",
                "explicatie": "Integrăm termen cu termen: 3·x³/3 + 2·x²/2 - x + C",
            },
            {
                "problema": "∫ 5 dx",
                "rezolvare": "5x + C",
                "explicatie": "Integrala unei constante = constanta · x",
            },
        ],
        "greseli_frecvente": [
            "Uitarea constantei de integrare +C",
            "Confuzia cu derivata: la integrală ADĂUGĂM 1 la exponent",
            "Neîmpărțirea la noul exponent",
        ],
    },

    "limita": {
        "concept": "Limita",
        "ce_este": (
            "Limita descrie VALOAREA spre care tinde o funcție când x se apropie "
            "de un punct, fără să ajungă neapărat acolo."
        ),
        "analogie": (
            "Imaginează-ți că mergi spre un perete: te apropii tot mai mult, "
            "dar nu-l atingi niciodată. Limita este peretele."
        ),
        "formula": "lim[x→a] f(x) = L",
        "reguli": [
            "Substituție directă: dacă f(a) e definit, lim = f(a)",
            "Formă 0/0: factorizare sau L'Hôpital",
            "Formă ∞/∞: împărțim la cea mai mare putere",
            "L'Hôpital: lim f/g = lim f'/g' (doar la 0/0 sau ∞/∞)",
            "lim sin(x)/x = 1 (când x→0)",
        ],
        "exemple": [
            {
                "problema": "lim(x→2) (x² - 4)/(x - 2)",
                "rezolvare": "= lim (x-2)(x+2)/(x-2) = lim (x+2) = 4",
                "explicatie": "Factorizăm numărătorul, simplificăm (x-2), apoi substituție",
            },
            {
                "problema": "lim(x→0) sin(x)/x",
                "rezolvare": "= 1",
                "explicatie": "Limită remarcabilă fundamentală",
            },
        ],
        "greseli_frecvente": [
            "Aplicarea L'Hôpital fără formă nedeterminată",
            "Simplificarea greșită la factorizare",
            "Confuzia limita laterală stângă/dreaptă",
        ],
    },

    "determinant": {
        "concept": "Determinantul",
        "ce_este": (
            "Determinantul este un NUMĂR asociat unei matrice pătratice. "
            "Geometric, reprezintă aria/volumul paralelogramului/paralelipipedului "
            "format de vectorii-coloană."
        ),
        "analogie": (
            "Gândește-te la o cutie: determinantul îți spune volumul cutiei. "
            "Dacă det = 0, cutia e 'turtită' (vectorii sunt coplanari)."
        ),
        "formula": "det 2×2: ad - bc\ndet 3×3: Regula lui Sarrus",
        "reguli": [
            "2×2: |a b; c d| = ad - bc",
            "3×3: Sarrus sau dezvoltare după linie/coloană",
            "det = 0 ⟺ matricea e singulară (neinversabilă)",
            "det(A·B) = det(A)·det(B)",
            "det(Aᵀ) = det(A)",
        ],
        "exemple": [
            {
                "problema": "|3 1; 2 4|",
                "rezolvare": "3·4 - 1·2 = 12 - 2 = 10",
                "explicatie": "Diagonala principală minus diagonala secundară",
            },
            {
                "problema": "|1 2 3; 4 5 6; 7 8 9|",
                "rezolvare": "(45+84+96) - (105+48+72) = 225 - 225 = 0",
                "explicatie": "Sarrus: sumă diagonale ↘ minus sumă diagonale ↙",
            },
        ],
        "greseli_frecvente": [
            "Confuzia diagonalelor la Sarrus",
            "Greșirea semnelor la dezvoltare după linie",
        ],
    },

    "matrice": {
        "concept": "Matricea",
        "ce_este": (
            "O matrice este un tabel dreptunghiular de numere, organizat pe "
            "linii și coloane. Matricele modelează sisteme de ecuații, transformări "
            "geometrice și multe alte probleme."
        ),
        "analogie": "Gândește-te la un tabel Excel: fiecare celulă are o valoare, iar reguli precise guvernează calculele.",
        "formula": "A(m×n) = matrice cu m linii și n coloane",
        "reguli": [
            "Adunare: element cu element (aceleași dimensiuni)",
            "Înmulțire cu scalar: fiecare element × scalarul",
            "Înmulțire matriceală: A(m×n)·B(n×p) = C(m×p)",
            "Cij = Σ Aik·Bkj (linia i din A × coloana j din B)",
            "Matricea unitate: I·A = A·I = A",
        ],
        "exemple": [
            {
                "problema": "A = [[1,2],[3,4]], B = [[5,6],[7,8]]. A + B = ?",
                "rezolvare": "[[6,8],[10,12]]",
                "explicatie": "Adunăm element cu element: 1+5=6, 2+6=8, etc.",
            },
        ],
        "greseli_frecvente": [
            "Înmulțirea matriceală NU e comutativă: A·B ≠ B·A",
            "Dimensiunile trebuie să fie compatibile la înmulțire",
        ],
    },

    "functie": {
        "concept": "Funcția",
        "ce_este": (
            "O funcție f: A → B asociază fiecărui element x din A exact un element "
            "f(x) din B. Graficul funcției arată vizual această relație."
        ),
        "analogie": "Funcția e ca un automat: bagi un număr (x), iese altul f(x). Același input dă mereu același output.",
        "formula": "f: D → ℝ, x ↦ f(x)",
        "reguli": [
            "Domeniu: valorile pentru care funcția e definită",
            "Codomeniu/Imagine: valorile pe care le ia funcția",
            "Funcție injectivă: f(x₁)=f(x₂) ⟹ x₁=x₂",
            "Funcție surjectivă: ∀y∈B, ∃x∈A cu f(x)=y",
            "Funcție bijectivă: injectivă + surjectivă",
        ],
        "exemple": [
            {
                "problema": "f(x) = 2x + 1. Domeniu?",
                "rezolvare": "D = ℝ (toată dreapta reală)",
                "explicatie": "Nu avem restricții (nu e fracție, radical etc.)",
            },
            {
                "problema": "f(x) = 1/(x-2). Domeniu?",
                "rezolvare": "D = ℝ \\ {2}",
                "explicatie": "Numitorul nu poate fi 0, deci x ≠ 2",
            },
        ],
        "greseli_frecvente": [
            "Uitarea restricțiilor de domeniu (numitor≠0, radical≥0)",
            "Confuzia domeniu/codomeniu",
        ],
    },

    "combinari": {
        "concept": "Combinări",
        "ce_este": (
            "Combinările numără câte moduri poți alege k obiecte din n, "
            "FĂRĂ să conteze ordinea."
        ),
        "analogie": "Câte echipe de 3 poți face din 10 jucători? Ordinea nu contează.",
        "formula": "C(n,k) = n! / (k! · (n-k)!)",
        "reguli": [
            "C(n,0) = C(n,n) = 1",
            "C(n,1) = n",
            "C(n,k) = C(n, n-k) (simetrie)",
            "Triunghiul lui Pascal: C(n,k) = C(n-1,k-1) + C(n-1,k)",
        ],
        "exemple": [
            {
                "problema": "C(5,2)",
                "rezolvare": "5!/(2!·3!) = 120/(2·6) = 10",
                "explicatie": "Câte perechi de 2 poți face din 5 elemente",
            },
            {
                "problema": "C(10,3)",
                "rezolvare": "10!/(3!·7!) = 720/6 = 120",
                "explicatie": "10·9·8 / (3·2·1) = 120",
            },
        ],
        "greseli_frecvente": [
            "Confuzia cu aranjamente (unde ordinea CONTEAZĂ)",
            "Greșeli la simplificarea factorialelor",
        ],
    },

    "probabilitate": {
        "concept": "Probabilitatea",
        "ce_este": (
            "Probabilitatea măsoară ȘANSA ca un eveniment să se producă. "
            "P(A) = cazuri favorabile / cazuri posibile."
        ),
        "analogie": "La un zar: P(6) = 1/6 pentru că 1 față din 6 arată 6.",
        "formula": "P(A) = |A| / |Ω|, unde 0 ≤ P(A) ≤ 1",
        "reguli": [
            "P(A∪B) = P(A) + P(B) - P(A∩B)",
            "Evenimente independente: P(A∩B) = P(A)·P(B)",
            "Eveniment complementar: P(Ā) = 1 - P(A)",
            "Probabilitate condiționată: P(A|B) = P(A∩B)/P(B)",
        ],
        "exemple": [
            {
                "problema": "Aruncăm 2 zaruri. P(suma=7)?",
                "rezolvare": "6/36 = 1/6",
                "explicatie": "Cazuri favorabile: (1,6)(2,5)(3,4)(4,3)(5,2)(6,1) = 6 din 36 total",
            },
        ],
        "greseli_frecvente": [
            "Confuzia 'sau' (adunare) cu 'și' (înmulțire)",
            "Uitarea scăderii intersecției la reuniune",
        ],
    },

    "ecuatie": {
        "concept": "Ecuații",
        "ce_este": (
            "O ecuație este o egalitate cu una sau mai multe necunoscute. "
            "A rezolva = a găsi valorile necunoscutei care verifică egalitatea."
        ),
        "analogie": "E ca o balanță: ce faci unui membru, trebuie să faci și celuilalt.",
        "formula": "ax + b = 0 ⟹ x = -b/a",
        "reguli": [
            "Grad 1: ax + b = 0 → x = -b/a",
            "Grad 2: ax² + bx + c = 0 → formula cu Δ",
            "Δ = b² - 4ac: Δ>0 → 2 soluții, Δ=0 → 1 soluție, Δ<0 → 0 soluții",
            "Viète: x₁+x₂ = -b/a, x₁·x₂ = c/a",
        ],
        "exemple": [
            {
                "problema": "3x + 6 = 0",
                "rezolvare": "x = -6/3 = -2",
                "explicatie": "Mutăm 6 în dreapta → 3x = -6 → x = -2",
            },
            {
                "problema": "x² - 5x + 6 = 0",
                "rezolvare": "Δ = 25-24 = 1, x₁ = 3, x₂ = 2",
                "explicatie": "a=1, b=-5, c=6. Δ=1>0 → 2 soluții",
            },
        ],
        "greseli_frecvente": [
            "Uitarea schimbării semnului la mutarea termenilor",
            "Greșirea formulei discriminantului",
        ],
    },

    "trigonometrie": {
        "concept": "Trigonometrie",
        "ce_este": (
            "Trigonometria studiază relațiile dintre unghiuri și laturi "
            "în triunghiuri. Funcțiile sin, cos, tan sunt fundamentale."
        ),
        "analogie": "Pe un cerc de rază 1, sin = proiecția pe verticală, cos = proiecția pe orizontală.",
        "formula": "sin²x + cos²x = 1",
        "reguli": [
            "sin²x + cos²x = 1",
            "tan x = sin x / cos x",
            "sin(a±b) = sin a·cos b ± cos a·sin b",
            "cos(a±b) = cos a·cos b ∓ sin a·sin b",
            "sin 2x = 2·sin x·cos x",
            "cos 2x = cos²x - sin²x",
        ],
        "exemple": [
            {
                "problema": "sin(30°) = ?",
                "rezolvare": "1/2",
                "explicatie": "Valoare din tabelul trigonometric standard",
            },
            {
                "problema": "cos(60°) = ?",
                "rezolvare": "1/2",
                "explicatie": "cos(60°) = sin(30°) = 1/2 (sunt complementare)",
            },
        ],
        "greseli_frecvente": [
            "Confuzia sin(30°) cu sin(60°)",
            "Uitarea semnului funcțiilor în cadranele II-IV",
        ],
    },

    "progresie": {
        "concept": "Progresii",
        "ce_este": (
            "O progresie este un șir de numere cu o regulă: "
            "aritmetică (adunăm rația) sau geometrică (înmulțim cu rația)."
        ),
        "analogie": "PA: 2,5,8,11... (adaug 3). PG: 2,6,18,54... (înmulțesc cu 3).",
        "formula": "PA: aₙ = a₁ + (n-1)·r\nPG: bₙ = b₁·qⁿ⁻¹",
        "reguli": [
            "PA: rația r = aₙ₊₁ - aₙ (constantă)",
            "PA: Sₙ = n·(a₁+aₙ)/2",
            "PG: rația q = bₙ₊₁/bₙ (constantă)",
            "PG: Sₙ = b₁·(qⁿ-1)/(q-1) pentru q≠1",
        ],
        "exemple": [
            {
                "problema": "PA: a₁=3, r=4. Găsește a₁₀.",
                "rezolvare": "a₁₀ = 3 + 9·4 = 39",
                "explicatie": "aₙ = a₁ + (n-1)·r = 3 + 9·4 = 39",
            },
        ],
        "greseli_frecvente": [
            "Confuzia n cu n-1 în formule",
            "Utilizarea formulei PA la PG și invers",
        ],
    },
}

# Aliases for lookup
ALIASES = {
    "derivate": "derivata",
    "derivatele": "derivata",
    "integrale": "integrala",
    "integralele": "integrala",
    "primitiva": "integrala",
    "limite": "limita",
    "limitele": "limita",
    "matrici": "matrice",
    "functia": "functie",
    "functii": "functie",
    "probabilitati": "probabilitate",
    "ecuatii": "ecuatie",
    "ecuatia": "ecuatie",
    "trigonometria": "trigonometrie",
    "sin": "trigonometrie",
    "cos": "trigonometrie",
    "progresii": "progresie",
    "aranjamente": "combinari",
    "permutari": "combinari",
}


def find_concept(text: str):
    """Find a matching concept from user text."""
    t = text.lower().strip()

    # Direct match
    for key in CONCEPTS:
        if key in t:
            return CONCEPTS[key]

    # Alias match
    for alias, key in ALIASES.items():
        if alias in t:
            return CONCEPTS.get(key)

    return None


def get_all_topics() -> list:
    """Return list of all available topics."""
    return [{"id": k, "name": v["concept"]} for k, v in CONCEPTS.items()]
