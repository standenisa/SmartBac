"""
Exerciții BAC cu rezolvări pas cu pas COMPLETE
Toate cele ~100 de exerciții cu soluții detaliate
"""

exercises_with_solutions = [
    # ============================================
    # SUBIECTUL I - ECUAȚII, FUNCȚII, GEOMETRIE
    # ============================================

    # ECUAȚII LINIARE ȘI DE GRADUL 2
    {
        'id': 9,
        'question': 'BAC 2024 Iulie - Rezolvă în mulțimea numerelor reale ecuația: 3x - 5 = 7',
        'answer': '4',
        'difficulty': 1,
        'topic': 'Ecuații liniare',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Scriem ecuația', 'result': '3x - 5 = 7'},
            {'step': 2, 'action': 'Adunăm 5 la ambele membre', 'result': '3x - 5 + 5 = 7 + 5'},
            {'step': 3, 'action': 'Simplificăm', 'result': '3x = 12'},
            {'step': 4, 'action': 'Împărțim la 3', 'result': 'x = 12 ÷ 3 = 4'}
        ],
        'hints': ['Mută termenii liberi în dreapta', 'Împarte la coeficientul lui x'],
        'explanation': 'Pentru ecuații de forma ax + b = c, izolăm pe x mutând b în partea dreaptă și împărțind la a.',
        'formula': 'ax + b = c → x = (c - b) / a'
    },
    {
        'id': 10,
        'question': 'BAC 2023 Iulie - Rezolvă ecuația: x² - 9 = 0. Scrie soluțiile separate prin virgulă',
        'answer': '-3,3',
        'difficulty': 1,
        'topic': 'Ecuații de gradul 2',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Scriem ecuația', 'result': 'x² - 9 = 0'},
            {'step': 2, 'action': 'Recunoaștem diferența de pătrate: a² - b² = (a-b)(a+b)', 'result': 'x² - 3² = 0'},
            {'step': 3, 'action': 'Factorizăm', 'result': '(x - 3)(x + 3) = 0'},
            {'step': 4, 'action': 'Aplicăm: produs = 0 ⟺ un factor = 0', 'result': 'x - 3 = 0 sau x + 3 = 0'},
            {'step': 5, 'action': 'Rezolvăm fiecare ecuație', 'result': 'x = 3 sau x = -3'}
        ],
        'hints': ['Este o diferență de pătrate', 'Folosește formula a² - b² = (a-b)(a+b)'],
        'explanation': 'Diferența de pătrate a² - b² se factorizează ca (a-b)(a+b). Apoi aplicăm proprietatea produsului nul.',
        'formula': 'a² - b² = (a - b)(a + b)'
    },
    {
        'id': 11,
        'question': 'BAC 2022 August - Rezolvă ecuația: 2x + 1 = x + 7',
        'answer': '6',
        'difficulty': 1,
        'topic': 'Ecuații liniare',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Scriem ecuația', 'result': '2x + 1 = x + 7'},
            {'step': 2, 'action': 'Scădem x din ambele părți', 'result': '2x - x + 1 = 7'},
            {'step': 3, 'action': 'Simplificăm termenii cu x', 'result': 'x + 1 = 7'},
            {'step': 4, 'action': 'Scădem 1 din ambele părți', 'result': 'x = 7 - 1 = 6'}
        ],
        'hints': ['Grupează termenii cu x într-o parte', 'Termenii liberi în cealaltă parte'],
        'explanation': 'În ecuațiile cu necunoscuta în ambii membri, grupăm termenii similari.',
        'formula': None
    },
    {
        'id': 12,
        'question': 'BAC 2021 Iulie - Rezolvă ecuația: x² - 4x + 4 = 0',
        'answer': '2',
        'difficulty': 2,
        'topic': 'Ecuații de gradul 2',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Scriem ecuația', 'result': 'x² - 4x + 4 = 0'},
            {'step': 2, 'action': 'Recunoaștem pătratul perfect: (a-b)² = a² - 2ab + b²', 'result': 'x² - 2·x·2 + 2² = 0'},
            {'step': 3, 'action': 'Scriem ca pătrat perfect', 'result': '(x - 2)² = 0'},
            {'step': 4, 'action': 'Extragem radicalul', 'result': 'x - 2 = 0'},
            {'step': 5, 'action': 'Rezolvăm', 'result': 'x = 2 (soluție dublă)'}
        ],
        'hints': ['Verifică dacă e pătrat perfect', 'Formula: (a-b)² = a² - 2ab + b²'],
        'explanation': 'Ecuația are discriminant Δ = 0, deci o singură soluție (rădăcină dublă).',
        'formula': '(a - b)² = a² - 2ab + b²'
    },
    {
        'id': 13,
        'question': 'BAC 2020 Septembrie - Rezolvă ecuația: 5x = 35',
        'answer': '7',
        'difficulty': 1,
        'topic': 'Ecuații liniare',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Scriem ecuația', 'result': '5x = 35'},
            {'step': 2, 'action': 'Împărțim ambii membri la 5', 'result': 'x = 35 ÷ 5'},
            {'step': 3, 'action': 'Calculăm', 'result': 'x = 7'}
        ],
        'hints': ['Împarte la coeficientul lui x'],
        'explanation': 'Ecuație simplă de forma ax = b, deci x = b/a',
        'formula': 'ax = b → x = b/a'
    },

    # FUNCȚII
    {
        'id': 14,
        'question': 'BAC 2024 Model - Fie f: ℝ → ℝ, f(x) = 2x + 3. Calculează f(5)',
        'answer': '13',
        'difficulty': 1,
        'topic': 'Funcții',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Scriem funcția', 'result': 'f(x) = 2x + 3'},
            {'step': 2, 'action': 'Înlocuim x cu 5', 'result': 'f(5) = 2 · 5 + 3'},
            {'step': 3, 'action': 'Calculăm înmulțirea', 'result': 'f(5) = 10 + 3'},
            {'step': 4, 'action': 'Calculăm suma', 'result': 'f(5) = 13'}
        ],
        'hints': ['Înlocuiește x cu valoarea dată', 'Respectă ordinea operațiilor'],
        'explanation': 'Pentru a calcula f(a), înlocuim x cu a în expresia funcției.',
        'formula': None
    },
    {
        'id': 15,
        'question': 'BAC 2023 Model - Fie f: ℝ → ℝ, f(x) = x² - 2x. Calculează f(3)',
        'answer': '3',
        'difficulty': 2,
        'topic': 'Funcții',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Scriem funcția', 'result': 'f(x) = x² - 2x'},
            {'step': 2, 'action': 'Înlocuim x cu 3', 'result': 'f(3) = 3² - 2·3'},
            {'step': 3, 'action': 'Calculăm 3²', 'result': 'f(3) = 9 - 2·3'},
            {'step': 4, 'action': 'Calculăm 2·3', 'result': 'f(3) = 9 - 6'},
            {'step': 5, 'action': 'Calculăm diferența', 'result': 'f(3) = 3'}
        ],
        'hints': ['Înlocuiește x cu 3', 'Calculează mai întâi puterea'],
        'explanation': 'Se înlocuiește x cu valoarea dată și se efectuează operațiile în ordinea corectă.',
        'formula': None
    },
    {
        'id': 16,
        'question': 'BAC 2022 Iulie - Fie f: ℝ → ℝ, f(x) = 3x - 1. Calculează f(-2)',
        'answer': '-7',
        'difficulty': 1,
        'topic': 'Funcții',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Scriem funcția', 'result': 'f(x) = 3x - 1'},
            {'step': 2, 'action': 'Înlocuim x cu -2', 'result': 'f(-2) = 3·(-2) - 1'},
            {'step': 3, 'action': 'Calculăm 3·(-2)', 'result': 'f(-2) = -6 - 1'},
            {'step': 4, 'action': 'Calculăm', 'result': 'f(-2) = -7'}
        ],
        'hints': ['Atenție la semnul numărului negativ', 'Pozitiv × Negativ = Negativ'],
        'explanation': 'La înmulțirea cu numere negative, atenție la regulile semnelor.',
        'formula': None
    },
    {
        'id': 17,
        'question': 'BAC 2021 Model - Fie f: ℝ → ℝ, f(x) = x² + 4. Calculează f(0)',
        'answer': '4',
        'difficulty': 1,
        'topic': 'Funcții',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Scriem funcția', 'result': 'f(x) = x² + 4'},
            {'step': 2, 'action': 'Înlocuim x cu 0', 'result': 'f(0) = 0² + 4'},
            {'step': 3, 'action': 'Calculăm 0²', 'result': 'f(0) = 0 + 4'},
            {'step': 4, 'action': 'Calculăm', 'result': 'f(0) = 4'}
        ],
        'hints': ['0 la orice putere este 0'],
        'explanation': '0² = 0, deci f(0) = 0 + 4 = 4',
        'formula': None
    },
    {
        'id': 18,
        'question': 'BAC 2020 Iulie - Fie f: ℝ → ℝ, f(x) = 4x + 2. Pentru ce valoare a lui x avem f(x) = 18?',
        'answer': '4',
        'difficulty': 2,
        'topic': 'Funcții - Ecuații',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Scriem condiția', 'result': 'f(x) = 18'},
            {'step': 2, 'action': 'Înlocuim f(x) cu expresia', 'result': '4x + 2 = 18'},
            {'step': 3, 'action': 'Scădem 2 din ambele părți', 'result': '4x = 18 - 2 = 16'},
            {'step': 4, 'action': 'Împărțim la 4', 'result': 'x = 16 ÷ 4 = 4'}
        ],
        'hints': ['Pune f(x) = 18 și rezolvă ecuația', 'Este o ecuație liniară simplă'],
        'explanation': 'Pentru a găsi x când f(x) = k, rezolvăm ecuația rezultată.',
        'formula': None
    },

    # GEOMETRIE ANALITICĂ
    {
        'id': 19,
        'question': 'BAC 2024 Iulie - Distanța între punctele A(1, 2) și B(4, 6) este...',
        'answer': '5',
        'difficulty': 2,
        'topic': 'Geometrie analitică',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Identificăm coordonatele', 'result': 'A(1, 2), B(4, 6)'},
            {'step': 2, 'action': 'Aplicăm formula distanței', 'result': 'd = √[(x₂-x₁)² + (y₂-y₁)²]'},
            {'step': 3, 'action': 'Calculăm diferențele', 'result': 'd = √[(4-1)² + (6-2)²] = √[3² + 4²]'},
            {'step': 4, 'action': 'Calculăm pătratele', 'result': 'd = √[9 + 16] = √25'},
            {'step': 5, 'action': 'Extragem radicalul', 'result': 'd = 5'}
        ],
        'hints': ['Folosește formula distanței', 'Este un triplet pitagoreic: 3, 4, 5'],
        'explanation': 'Formula distanței dintre două puncte derivă din teorema lui Pitagora.',
        'formula': 'd(A,B) = √[(x₂-x₁)² + (y₂-y₁)²]'
    },
    {
        'id': 20,
        'question': 'BAC 2023 August - Coordonatele mijlocului segmentului AB, unde A(2, 4) și B(6, 8), sunt (x, y). Scrie doar x',
        'answer': '4',
        'difficulty': 2,
        'topic': 'Geometrie analitică - Mijloc',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Identificăm coordonatele', 'result': 'A(2, 4), B(6, 8)'},
            {'step': 2, 'action': 'Formula mijlocului', 'result': 'M = ((x₁+x₂)/2, (y₁+y₂)/2)'},
            {'step': 3, 'action': 'Calculăm x-ul mijlocului', 'result': 'xₘ = (2+6)/2 = 8/2 = 4'},
            {'step': 4, 'action': 'Calculăm y-ul mijlocului', 'result': 'yₘ = (4+8)/2 = 12/2 = 6'},
            {'step': 5, 'action': 'Răspunsul cerut (doar x)', 'result': 'x = 4'}
        ],
        'hints': ['Mijlocul = media aritmetică a coordonatelor'],
        'explanation': 'Coordonatele mijlocului sunt mediile aritmetice ale coordonatelor capetelor.',
        'formula': 'M = ((x₁+x₂)/2, (y₁+y₂)/2)'
    },
    {
        'id': 21,
        'question': 'BAC 2022 Model - Panta dreptei care trece prin A(0, 2) și B(3, 8) este...',
        'answer': '2',
        'difficulty': 2,
        'topic': 'Geometrie analitică - Pantă',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Identificăm coordonatele', 'result': 'A(0, 2), B(3, 8)'},
            {'step': 2, 'action': 'Aplicăm formula pantei', 'result': 'm = (y₂ - y₁)/(x₂ - x₁)'},
            {'step': 3, 'action': 'Înlocuim valorile', 'result': 'm = (8 - 2)/(3 - 0)'},
            {'step': 4, 'action': 'Calculăm', 'result': 'm = 6/3 = 2'}
        ],
        'hints': ['Panta = variația lui y / variația lui x'],
        'explanation': 'Panta măsoară înclinarea dreptei: cu cât e mai mare, cu atât dreapta e mai abruptă.',
        'formula': 'm = (y₂ - y₁)/(x₂ - x₁)'
    },
    {
        'id': 22,
        'question': 'BAC 2021 August - Ecuația dreptei care trece prin origine și are panta 3 este y = mx. Care e m?',
        'answer': '3',
        'difficulty': 1,
        'topic': 'Geometrie analitică - Ecuații',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Dreapta trece prin origine O(0,0)', 'result': 'Ecuație: y = mx + n, cu n = 0'},
            {'step': 2, 'action': 'Panta dată este 3', 'result': 'm = 3'},
            {'step': 3, 'action': 'Ecuația dreptei', 'result': 'y = 3x'},
            {'step': 4, 'action': 'Răspuns', 'result': 'm = 3'}
        ],
        'hints': ['Dreapta prin origine are n = 0', 'Panta = coeficientul lui x'],
        'explanation': 'O dreaptă prin origine are ecuația y = mx, unde m este panta.',
        'formula': 'y = mx (dreaptă prin origine)'
    },
    {
        'id': 23,
        'question': 'BAC 2020 Model - Distanța de la originea O(0, 0) la punctul A(3, 4) este...',
        'answer': '5',
        'difficulty': 2,
        'topic': 'Geometrie analitică - Distanță',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Coordonatele', 'result': 'O(0, 0), A(3, 4)'},
            {'step': 2, 'action': 'Formula distanței', 'result': 'd = √[(3-0)² + (4-0)²]'},
            {'step': 3, 'action': 'Calculăm', 'result': 'd = √[9 + 16] = √25'},
            {'step': 4, 'action': 'Rezultat', 'result': 'd = 5'}
        ],
        'hints': ['Tripletul pitagoreic clasic: 3, 4, 5'],
        'explanation': 'Distanța de la origine la (a, b) este √(a² + b²).',
        'formula': 'd = √(x² + y²)'
    },

    # COMBINATORICĂ ȘI PROBABILITĂȚI
    {
        'id': 24,
        'question': 'BAC 2024 Model - Calculează 4! (4 factorial)',
        'answer': '24',
        'difficulty': 1,
        'topic': 'Combinatorică - Factorial',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Definiția factorialului', 'result': 'n! = n × (n-1) × ... × 2 × 1'},
            {'step': 2, 'action': 'Aplicăm pentru n = 4', 'result': '4! = 4 × 3 × 2 × 1'},
            {'step': 3, 'action': 'Calculăm pas cu pas', 'result': '4 × 3 = 12, apoi 12 × 2 = 24'},
            {'step': 4, 'action': 'Rezultat', 'result': '4! = 24'}
        ],
        'hints': ['Înmulțește toate numerele de la n la 1'],
        'explanation': 'Factorialul lui n este produsul tuturor numerelor naturale de la 1 la n.',
        'formula': 'n! = n × (n-1) × ... × 2 × 1'
    },
    {
        'id': 25,
        'question': 'BAC 2023 Iulie - Câte permutări sunt ale mulțimii {1, 2, 3}?',
        'answer': '6',
        'difficulty': 2,
        'topic': 'Combinatorică - Permutări',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Formula permutărilor', 'result': 'Pₙ = n!'},
            {'step': 2, 'action': 'n = 3 (trei elemente)', 'result': 'P₃ = 3!'},
            {'step': 3, 'action': 'Calculăm 3!', 'result': '3! = 3 × 2 × 1 = 6'},
            {'step': 4, 'action': 'Verificare', 'result': '{1,2,3}, {1,3,2}, {2,1,3}, {2,3,1}, {3,1,2}, {3,2,1}'}
        ],
        'hints': ['Numărul de permutări = n!'],
        'explanation': 'O permutare este o aranjare a tuturor elementelor în ordine diferită.',
        'formula': 'Pₙ = n!'
    },
    {
        'id': 26,
        'question': 'BAC 2022 Septembrie - Aruncăm un zar. Probabilitatea să obținem un număr par este... (scrie 0.5)',
        'answer': '0.5',
        'difficulty': 2,
        'topic': 'Probabilități',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Cazuri posibile', 'result': 'Zar: {1, 2, 3, 4, 5, 6} - 6 cazuri'},
            {'step': 2, 'action': 'Cazuri favorabile (numere pare)', 'result': '{2, 4, 6} - 3 cazuri'},
            {'step': 3, 'action': 'Formula probabilității', 'result': 'P = favorabile / posibile'},
            {'step': 4, 'action': 'Calculăm', 'result': 'P = 3/6 = 1/2 = 0.5'}
        ],
        'hints': ['Numere pare pe zar: 2, 4, 6'],
        'explanation': 'Probabilitatea = numărul de cazuri favorabile / numărul total de cazuri.',
        'formula': 'P(A) = n(A) / n(Ω)'
    },
    {
        'id': 27,
        'question': 'BAC 2021 Iulie - Calculează C(5,2) = 5!/(2!×3!)',
        'answer': '10',
        'difficulty': 2,
        'topic': 'Combinatorică - Combinări',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Formula combinărilor', 'result': 'C(n,k) = n! / (k! × (n-k)!)'},
            {'step': 2, 'action': 'Înlocuim n=5, k=2', 'result': 'C(5,2) = 5! / (2! × 3!)'},
            {'step': 3, 'action': 'Calculăm factorialele', 'result': '= 120 / (2 × 6)'},
            {'step': 4, 'action': 'Simplificăm', 'result': '= 120 / 12 = 10'}
        ],
        'hints': ['C(n,k) = numărul de moduri de a alege k din n'],
        'explanation': 'Combinările numără selecțiile fără a ține cont de ordine.',
        'formula': 'C(n,k) = n! / (k! × (n-k)!)'
    },
    {
        'id': 28,
        'question': 'BAC 2020 Iulie - Câte numere de 3 cifre distincte se pot forma cu cifrele 1, 2, 3, 4?',
        'answer': '24',
        'difficulty': 3,
        'topic': 'Combinatorică - Aranjamente',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Identificăm problema', 'result': 'Aranjamente (ordinea contează, fără repetiție)'},
            {'step': 2, 'action': 'Formula aranjamentelor', 'result': 'A(n,k) = n! / (n-k)!'},
            {'step': 3, 'action': 'Calculăm A(4,3)', 'result': 'A(4,3) = 4! / (4-3)! = 4! / 1!'},
            {'step': 4, 'action': 'Calculăm', 'result': '= 24 / 1 = 24'}
        ],
        'hints': ['Cifre distincte = fără repetiție', 'Ordinea contează în numere'],
        'explanation': 'Aranjamentele numără selecțiile ordonate fără repetiție.',
        'formula': 'A(n,k) = n! / (n-k)!'
    },

    # LIMITE
    {
        'id': 29,
        'question': 'BAC 2024 Iulie - Calculează: lim(x→2) (3x + 1)',
        'answer': '7',
        'difficulty': 2,
        'topic': 'Limite',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Funcția este polinom (continuă)', 'result': 'Putem înlocui direct'},
            {'step': 2, 'action': 'Înlocuim x = 2', 'result': 'lim = 3·2 + 1'},
            {'step': 3, 'action': 'Calculăm', 'result': '= 6 + 1 = 7'}
        ],
        'hints': ['Pentru polinoame, înlocuim direct valoarea'],
        'explanation': 'Funcțiile polinomiale sunt continue, deci limita = valoarea funcției în punct.',
        'formula': 'lim(x→a) f(x) = f(a) pentru funcții continue'
    },
    {
        'id': 30,
        'question': 'BAC 2023 Model - Calculează: lim(x→1) (x² + 3)',
        'answer': '4',
        'difficulty': 1,
        'topic': 'Limite',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Funcția este continuă', 'result': 'Înlocuim x = 1'},
            {'step': 2, 'action': 'Calculăm', 'result': '1² + 3 = 1 + 3 = 4'}
        ],
        'hints': ['Înlocuire directă pentru polinoame'],
        'explanation': 'Limita unui polinom într-un punct este valoarea polinomului în acel punct.',
        'formula': None
    },
    {
        'id': 31,
        'question': 'BAC 2022 Iulie - Calculează: lim(x→0) (5x + 10)',
        'answer': '10',
        'difficulty': 1,
        'topic': 'Limite',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Înlocuim x = 0', 'result': '5·0 + 10'},
            {'step': 2, 'action': 'Calculăm', 'result': '0 + 10 = 10'}
        ],
        'hints': ['Pentru x = 0, termenii cu x dispar'],
        'explanation': 'Termenul liber este limita când x → 0.',
        'formula': None
    },
    {
        'id': 32,
        'question': 'BAC 2021 August - Calculează: lim(x→3) (x² - 2x)',
        'answer': '3',
        'difficulty': 2,
        'topic': 'Limite',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Înlocuim x = 3', 'result': '3² - 2·3'},
            {'step': 2, 'action': 'Calculăm 3²', 'result': '9 - 2·3'},
            {'step': 3, 'action': 'Calculăm', 'result': '9 - 6 = 3'}
        ],
        'hints': ['Înlocuire directă'],
        'explanation': 'f(3) = 9 - 6 = 3',
        'formula': None
    },
    {
        'id': 33,
        'question': 'BAC 2020 Septembrie - Calculează: lim(x→-1) (2x + 5)',
        'answer': '3',
        'difficulty': 1,
        'topic': 'Limite',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Înlocuim x = -1', 'result': '2·(-1) + 5'},
            {'step': 2, 'action': 'Calculăm', 'result': '-2 + 5 = 3'}
        ],
        'hints': ['Atenție la semnul negativ'],
        'explanation': '2 × (-1) = -2',
        'formula': None
    },

    # DERIVATE ȘI PRIMITIVE
    {
        'id': 34,
        'question': 'BAC 2024 Model - Calculează derivata funcției f(x) = 5x. Scrie doar coeficientul',
        'answer': '5',
        'difficulty': 1,
        'topic': 'Derivate',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Funcția f(x) = 5x', 'result': 'Este o funcție liniară'},
            {'step': 2, 'action': 'Regula: (ax)\' = a', 'result': 'f\'(x) = 5'},
            {'step': 3, 'action': 'Coeficientul', 'result': '5'}
        ],
        'hints': ['Derivata lui ax este a'],
        'explanation': 'Derivata unei funcții liniare ax + b este constanta a.',
        'formula': '(ax)\' = a'
    },
    {
        'id': 35,
        'question': 'BAC 2023 Iulie - Calculează derivata funcției f(x) = x³. Scrie doar coeficientul lui x²',
        'answer': '3',
        'difficulty': 2,
        'topic': 'Derivate',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Funcția f(x) = x³', 'result': 'Aplicăm regula puterii'},
            {'step': 2, 'action': 'Regula: (xⁿ)\' = n·xⁿ⁻¹', 'result': 'f\'(x) = 3·x³⁻¹'},
            {'step': 3, 'action': 'Simplificăm', 'result': 'f\'(x) = 3x²'},
            {'step': 4, 'action': 'Coeficientul lui x²', 'result': '3'}
        ],
        'hints': ['Folosește regula puterii', 'Exponentul coboară și scade cu 1'],
        'explanation': 'Regula puterii: derivata lui xⁿ este n·xⁿ⁻¹',
        'formula': '(xⁿ)\' = n·xⁿ⁻¹'
    },
    {
        'id': 36,
        'question': 'BAC 2022 August - O primitivă a funcției f(x) = 4 este F(x) = 4x + C. Care e C pentru F(0) = 5?',
        'answer': '5',
        'difficulty': 2,
        'topic': 'Primitive',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Primitiva generală', 'result': 'F(x) = 4x + C'},
            {'step': 2, 'action': 'Condiția F(0) = 5', 'result': '4·0 + C = 5'},
            {'step': 3, 'action': 'Rezolvăm', 'result': '0 + C = 5'},
            {'step': 4, 'action': 'Rezultat', 'result': 'C = 5'}
        ],
        'hints': ['Înlocuiește x = 0 în primitivă'],
        'explanation': 'Constanta C se determină din condiții inițiale.',
        'formula': '∫a dx = ax + C'
    },
    {
        'id': 37,
        'question': 'BAC 2021 Iulie - Calculează derivata funcției f(x) = 2x² + 3x. Care e f\'(1)?',
        'answer': '7',
        'difficulty': 3,
        'topic': 'Derivate - Calcul',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Derivăm f(x) = 2x² + 3x', 'result': 'Derivăm termen cu termen'},
            {'step': 2, 'action': '(2x²)\' = 4x', 'result': 'Folosim (axⁿ)\' = n·a·xⁿ⁻¹'},
            {'step': 3, 'action': '(3x)\' = 3', 'result': 'Derivata funcției liniare'},
            {'step': 4, 'action': 'f\'(x) = 4x + 3', 'result': 'Derivata completă'},
            {'step': 5, 'action': 'f\'(1) = 4·1 + 3', 'result': '= 4 + 3 = 7'}
        ],
        'hints': ['Derivează termen cu termen', 'Apoi înlocuiește x = 1'],
        'explanation': 'Derivata sumei = suma derivatelor',
        'formula': '(f + g)\' = f\' + g\''
    },
    {
        'id': 38,
        'question': 'BAC 2020 Model - Calculează ∫3 dx. Scrie doar coeficientul lui x',
        'answer': '3',
        'difficulty': 2,
        'topic': 'Integrale',
        'subject': 1,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Integrala unei constante', 'result': '∫a dx = ax + C'},
            {'step': 2, 'action': 'Aplicăm pentru a = 3', 'result': '∫3 dx = 3x + C'},
            {'step': 3, 'action': 'Coeficientul lui x', 'result': '3'}
        ],
        'hints': ['Integrala constantei a este ax'],
        'explanation': 'Primitivarea unei constante: ∫a dx = ax + C',
        'formula': '∫a dx = ax + C'
    },

    # ============================================
    # SUBIECTUL II - DERIVATE AVANSATE, INTEGRALE
    # ============================================
    {
        'id': 39,
        'question': 'BAC 2024 Model - Calculează derivata funcției f(x) = 7x. Scrie doar coeficientul',
        'answer': '7',
        'difficulty': 1,
        'topic': 'Derivate',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'f(x) = 7x este liniară', 'result': '(ax)\' = a'},
            {'step': 2, 'action': 'f\'(x) = 7', 'result': 'Coeficient: 7'}
        ],
        'hints': ['Derivata funcției liniare'],
        'explanation': 'Derivata lui ax este constanta a.',
        'formula': '(ax)\' = a'
    },
    {
        'id': 40,
        'question': 'BAC 2023 Iulie - Calculează derivata funcției f(x) = x⁵. Scrie doar coeficientul lui x⁴',
        'answer': '5',
        'difficulty': 2,
        'topic': 'Derivate',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Regula puterii', 'result': '(xⁿ)\' = n·xⁿ⁻¹'},
            {'step': 2, 'action': 'Aplicăm pentru n = 5', 'result': 'f\'(x) = 5·x⁴'},
            {'step': 3, 'action': 'Coeficientul lui x⁴', 'result': '5'}
        ],
        'hints': ['Regula puterii'],
        'explanation': 'Exponentul devine coeficient și scade cu 1.',
        'formula': '(xⁿ)\' = n·xⁿ⁻¹'
    },
    {
        'id': 41,
        'question': 'BAC 2022 August - Fie f(x) = x³ - 3x. Calculează f\'(1)',
        'answer': '0',
        'difficulty': 2,
        'topic': 'Derivate - Calcul',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Derivăm f(x) = x³ - 3x', 'result': 'f\'(x) = 3x² - 3'},
            {'step': 2, 'action': 'Calculăm f\'(1)', 'result': 'f\'(1) = 3·1² - 3'},
            {'step': 3, 'action': 'Simplificăm', 'result': '= 3 - 3 = 0'}
        ],
        'hints': ['Derivată, apoi înlocuire'],
        'explanation': 'x = 1 este punct critic (derivata = 0).',
        'formula': None
    },
    {
        'id': 42,
        'question': 'BAC 2021 Iulie - Calculează derivata funcției f(x) = 3x² + 2x - 1. Care e f\'(0)?',
        'answer': '2',
        'difficulty': 2,
        'topic': 'Derivate',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Derivăm termen cu termen', 'result': 'f\'(x) = 6x + 2'},
            {'step': 2, 'action': 'Calculăm f\'(0)', 'result': 'f\'(0) = 6·0 + 2 = 2'}
        ],
        'hints': ['(3x²)\' = 6x, (2x)\' = 2, (-1)\' = 0'],
        'explanation': 'Derivata constantei este 0.',
        'formula': None
    },
    {
        'id': 43,
        'question': 'BAC 2020 Septembrie - Fie f(x) = x⁴. Calculează f\'(2)',
        'answer': '32',
        'difficulty': 3,
        'topic': 'Derivate - Aplicații',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Derivăm f(x) = x⁴', 'result': 'f\'(x) = 4x³'},
            {'step': 2, 'action': 'Calculăm f\'(2)', 'result': 'f\'(2) = 4·2³'},
            {'step': 3, 'action': '2³ = 8', 'result': 'f\'(2) = 4·8 = 32'}
        ],
        'hints': ['Derivează, apoi înlocuiește'],
        'explanation': '4 × 8 = 32',
        'formula': None
    },
    {
        'id': 44,
        'question': 'BAC 2024 Iulie - Calculează derivata funcției f(x) = (x + 1)². Care e f\'(1)?',
        'answer': '4',
        'difficulty': 3,
        'topic': 'Derivate - Funcții compuse',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Dezvoltăm (x + 1)²', 'result': 'f(x) = x² + 2x + 1'},
            {'step': 2, 'action': 'Derivăm', 'result': 'f\'(x) = 2x + 2'},
            {'step': 3, 'action': 'Calculăm f\'(1)', 'result': 'f\'(1) = 2·1 + 2 = 4'}
        ],
        'hints': ['Poți dezvolta sau folosi regula lanțului'],
        'explanation': 'Pentru (u)², derivata este 2u·u\'',
        'formula': '(a+b)² = a² + 2ab + b²'
    },
    {
        'id': 45,
        'question': 'BAC 2023 Model - Fie f(x) = x² · (x + 1). Calculează f\'(0)',
        'answer': '0',
        'difficulty': 3,
        'topic': 'Derivate - Produs',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Dezvoltăm f(x)', 'result': 'f(x) = x³ + x²'},
            {'step': 2, 'action': 'Derivăm', 'result': 'f\'(x) = 3x² + 2x'},
            {'step': 3, 'action': 'f\'(0) = 3·0² + 2·0', 'result': '= 0 + 0 = 0'}
        ],
        'hints': ['Dezvoltă produsul mai întâi'],
        'explanation': 'Alternativ: regula produsului (fg)\' = f\'g + fg\'',
        'formula': '(fg)\' = f\'g + fg\''
    },
    {
        'id': 46,
        'question': 'BAC 2022 Iulie - Calculează derivata funcției f(x) = 1/x. Care e f\'(1)?',
        'answer': '-1',
        'difficulty': 3,
        'topic': 'Derivate - Raport',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Scriem f(x) = x⁻¹', 'result': '1/x = x⁻¹'},
            {'step': 2, 'action': 'Aplicăm regula puterii', 'result': 'f\'(x) = -1·x⁻² = -1/x²'},
            {'step': 3, 'action': 'f\'(1) = -1/1²', 'result': '= -1'}
        ],
        'hints': ['1/x = x⁻¹'],
        'explanation': 'Regula puterii funcționează și pentru exponenți negativi.',
        'formula': '(1/x)\' = -1/x²'
    },
    {
        'id': 47,
        'question': 'BAC 2024 Model - Calculează: lim(x→5) (2x - 3)',
        'answer': '7',
        'difficulty': 2,
        'topic': 'Limite',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Funcție continuă', 'result': 'Înlocuim direct x = 5'},
            {'step': 2, 'action': 'Calculăm', 'result': '2·5 - 3 = 10 - 3 = 7'}
        ],
        'hints': ['Înlocuire directă'],
        'explanation': 'Polinoamele sunt continue.',
        'formula': None
    },
    {
        'id': 48,
        'question': 'BAC 2023 Iulie - Calculează: lim(x→2) (x² + x)',
        'answer': '6',
        'difficulty': 2,
        'topic': 'Limite',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Înlocuim x = 2', 'result': '2² + 2'},
            {'step': 2, 'action': 'Calculăm', 'result': '4 + 2 = 6'}
        ],
        'hints': ['Înlocuire directă'],
        'explanation': 'f(2) = 4 + 2 = 6',
        'formula': None
    },
    {
        'id': 49,
        'question': 'BAC 2022 August - Calculează: lim(x→-1) (x³ + 1)',
        'answer': '0',
        'difficulty': 2,
        'topic': 'Limite',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Înlocuim x = -1', 'result': '(-1)³ + 1'},
            {'step': 2, 'action': '(-1)³ = -1', 'result': '-1 + 1 = 0'}
        ],
        'hints': ['(-1)³ = -1'],
        'explanation': 'Puterea impară păstrează semnul.',
        'formula': None
    },
    {
        'id': 50,
        'question': 'BAC 2021 Iulie - Calculează: lim(x→0) (3x² + 2x + 1)',
        'answer': '1',
        'difficulty': 2,
        'topic': 'Limite',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Înlocuim x = 0', 'result': '3·0² + 2·0 + 1'},
            {'step': 2, 'action': 'Calculăm', 'result': '0 + 0 + 1 = 1'}
        ],
        'hints': ['Rămâne doar termenul liber'],
        'explanation': 'Termenul liber este limita când x → 0.',
        'formula': None
    },
    {
        'id': 51,
        'question': 'BAC 2020 Model - Calculează: lim(x→4) (x - 2)',
        'answer': '2',
        'difficulty': 1,
        'topic': 'Limite',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Înlocuim x = 4', 'result': '4 - 2 = 2'}
        ],
        'hints': ['Calcul direct'],
        'explanation': 'Funcție liniară continuă.',
        'formula': None
    },
    {
        'id': 52,
        'question': 'BAC 2024 Iulie - Calculează ∫3x² dx. Scrie doar coeficientul lui x³',
        'answer': '1',
        'difficulty': 3,
        'topic': 'Integrale',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Regula integrării', 'result': '∫xⁿ dx = xⁿ⁺¹/(n+1)'},
            {'step': 2, 'action': '∫3x² dx = 3·x³/3', 'result': '= x³ + C'},
            {'step': 3, 'action': 'Coeficientul lui x³', 'result': '1'}
        ],
        'hints': ['3/3 = 1'],
        'explanation': 'Primitiva lui xⁿ este xⁿ⁺¹/(n+1)',
        'formula': '∫xⁿ dx = xⁿ⁺¹/(n+1) + C'
    },
    {
        'id': 53,
        'question': 'BAC 2023 Model - Calculează ∫8x³ dx. Scrie doar coeficientul lui x⁴',
        'answer': '2',
        'difficulty': 3,
        'topic': 'Integrale',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': '∫8x³ dx = 8·x⁴/4', 'result': '= 2x⁴ + C'},
            {'step': 2, 'action': 'Coeficientul lui x⁴', 'result': '2'}
        ],
        'hints': ['8/4 = 2'],
        'explanation': '8 × (1/4) = 2',
        'formula': None
    },
    {
        'id': 54,
        'question': 'BAC 2022 Iulie - O primitivă a funcției f(x) = 6 este F(x) = 6x + C. Pentru F(1) = 10, care e C?',
        'answer': '4',
        'difficulty': 3,
        'topic': 'Primitive',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'F(x) = 6x + C', 'result': 'F(1) = 6·1 + C = 10'},
            {'step': 2, 'action': '6 + C = 10', 'result': 'C = 10 - 6 = 4'}
        ],
        'hints': ['Înlocuiește x = 1'],
        'explanation': 'Constanta C satisface condiția inițială.',
        'formula': None
    },
    {
        'id': 55,
        'question': 'BAC 2021 August - Calculează ∫(2x + 1) dx. Care e coeficientul lui x²?',
        'answer': '1',
        'difficulty': 3,
        'topic': 'Integrale',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Integrăm termen cu termen', 'result': '∫2x dx + ∫1 dx'},
            {'step': 2, 'action': '= 2·x²/2 + x + C', 'result': '= x² + x + C'},
            {'step': 3, 'action': 'Coeficientul lui x²', 'result': '1'}
        ],
        'hints': ['2/2 = 1'],
        'explanation': 'Integrala sumei = suma integralelor.',
        'formula': None
    },
    {
        'id': 56,
        'question': 'BAC 2020 Septembrie - Calculează ∫5 dx. Scrie doar coeficientul lui x',
        'answer': '5',
        'difficulty': 2,
        'topic': 'Integrale',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': '∫5 dx = 5x + C', 'result': 'Coeficientul: 5'}
        ],
        'hints': ['Integrala constantei'],
        'explanation': '∫a dx = ax + C',
        'formula': '∫a dx = ax + C'
    },
    {
        'id': 57,
        'question': 'BAC 2024 Model - Fie f(x) = x² - 4x. Funcția este descrescătoare pe (-∞, a). Care e a?',
        'answer': '2',
        'difficulty': 3,
        'topic': 'Studiu funcții',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Derivăm f(x) = x² - 4x', 'result': 'f\'(x) = 2x - 4'},
            {'step': 2, 'action': 'f descrescătoare ⟺ f\'(x) < 0', 'result': '2x - 4 < 0'},
            {'step': 3, 'action': 'Rezolvăm', 'result': '2x < 4, deci x < 2'},
            {'step': 4, 'action': 'Intervalul', 'result': '(-∞, 2), deci a = 2'}
        ],
        'hints': ['Funcția descrescătoare când derivata < 0'],
        'explanation': 'Semnul derivatei determină monotonia.',
        'formula': 'f\' < 0 ⟺ f descrescătoare'
    },
    {
        'id': 58,
        'question': 'BAC 2023 Iulie - Fie f(x) = -x² + 6x. Funcția are maxim în x = ?',
        'answer': '3',
        'difficulty': 3,
        'topic': 'Studiu funcții - Extreme',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Derivăm', 'result': 'f\'(x) = -2x + 6'},
            {'step': 2, 'action': 'Puncte critice: f\'(x) = 0', 'result': '-2x + 6 = 0'},
            {'step': 3, 'action': 'Rezolvăm', 'result': 'x = 3'},
            {'step': 4, 'action': 'Coef. lui x² < 0', 'result': 'Punct de maxim'}
        ],
        'hints': ['Derivata se anulează în punctele de extrem'],
        'explanation': 'Coeficientul lui x² este negativ, deci avem maxim.',
        'formula': None
    },
    {
        'id': 59,
        'question': 'BAC 2022 Model - Fie f(x) = x³ - 3x. Câte puncte de extrem are funcția?',
        'answer': '2',
        'difficulty': 4,
        'topic': 'Studiu funcții',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Derivăm', 'result': 'f\'(x) = 3x² - 3'},
            {'step': 2, 'action': 'f\'(x) = 0', 'result': '3x² - 3 = 0'},
            {'step': 3, 'action': 'Rezolvăm', 'result': 'x² = 1, deci x = ±1'},
            {'step': 4, 'action': 'Număr puncte extrem', 'result': '2'}
        ],
        'hints': ['Rezolvă f\'(x) = 0'],
        'explanation': 'Două soluții = două puncte de extrem.',
        'formula': None
    },
    {
        'id': 60,
        'question': 'BAC 2024 Iulie - Calculează ∫₀² 2x dx',
        'answer': '4',
        'difficulty': 3,
        'topic': 'Integrale definite',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Primitiva lui 2x', 'result': 'F(x) = x²'},
            {'step': 2, 'action': 'Formula Leibniz-Newton', 'result': '[x²]₀² = F(2) - F(0)'},
            {'step': 3, 'action': 'Calculăm', 'result': '2² - 0² = 4 - 0 = 4'}
        ],
        'hints': ['F(b) - F(a)'],
        'explanation': 'Integrala definită = F(capăt superior) - F(capăt inferior)',
        'formula': '∫ₐᵇ f(x)dx = F(b) - F(a)'
    },
    {
        'id': 61,
        'question': 'BAC 2023 August - Calculează ∫₁³ 3 dx',
        'answer': '6',
        'difficulty': 2,
        'topic': 'Integrale definite',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Primitiva lui 3', 'result': 'F(x) = 3x'},
            {'step': 2, 'action': 'F(3) - F(1)', 'result': '3·3 - 3·1 = 9 - 3'},
            {'step': 3, 'action': 'Rezultat', 'result': '6'}
        ],
        'hints': ['Integrala constantei pe [a,b] = c(b-a)'],
        'explanation': '∫ₐᵇ c dx = c(b-a)',
        'formula': None
    },
    {
        'id': 62,
        'question': 'BAC 2022 Iulie - Aria delimitată de f(x) = x și axa Ox pe [0, 2] este...',
        'answer': '2',
        'difficulty': 3,
        'topic': 'Integrale - Arii',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'Aria = ∫₀² x dx', 'result': 'Integrăm pe [0,2]'},
            {'step': 2, 'action': 'Primitiva lui x', 'result': 'F(x) = x²/2'},
            {'step': 3, 'action': 'Calculăm', 'result': '[x²/2]₀² = 4/2 - 0 = 2'}
        ],
        'hints': ['Aria = integrala funcției pozitive'],
        'explanation': 'Pentru f(x) ≥ 0, aria = integrala definită.',
        'formula': 'A = ∫ₐᵇ f(x) dx'
    },
    {
        'id': 63,
        'question': 'BAC 2021 Iulie - Soluția ecuației y\' = 3 este y = ax + C. Care e a?',
        'answer': '3',
        'difficulty': 3,
        'topic': 'Ecuații diferențiale',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'y\' = 3 înseamnă dy/dx = 3', 'result': 'Integrăm'},
            {'step': 2, 'action': 'y = ∫3 dx', 'result': 'y = 3x + C'},
            {'step': 3, 'action': 'Coeficientul a', 'result': 'a = 3'}
        ],
        'hints': ['Integrarea inversează derivarea'],
        'explanation': 'Soluția y\' = k este y = kx + C.',
        'formula': None
    },
    {
        'id': 64,
        'question': 'BAC 2020 Model - Soluția ecuației y\' = 2x este y = ax² + C. Care e a?',
        'answer': '1',
        'difficulty': 3,
        'topic': 'Ecuații diferențiale',
        'subject': 2,
        'points': 5,
        'profile': 'BOTH',
        'solution_steps': [
            {'step': 1, 'action': 'y\' = 2x', 'result': 'Integrăm'},
            {'step': 2, 'action': 'y = ∫2x dx', 'result': 'y = 2·x²/2 + C = x² + C'},
            {'step': 3, 'action': 'Coeficientul a', 'result': 'a = 1'}
        ],
        'hints': ['2/2 = 1'],
        'explanation': 'Primitiva lui 2x este x².',
        'formula': None
    },

    # ============================================
    # SUBIECTUL III - M1 (MATRICE, DETERMINANȚI, VECTORI)
    # ============================================
    {
        'id': 65,
        'question': 'BAC 2024 M1 - Calculează determinantul matricei A = [[3, 1], [2, 4]]',
        'answer': '10',
        'difficulty': 3,
        'topic': 'Matrice - Determinanți',
        'subject': 3,
        'points': 5,
        'profile': 'M1',
        'solution_steps': [
            {'step': 1, 'action': 'Formula det 2×2', 'result': 'det = a·d - b·c'},
            {'step': 2, 'action': 'Identificăm: a=3, b=1, c=2, d=4', 'result': 'det = 3·4 - 1·2'},
            {'step': 3, 'action': 'Calculăm', 'result': '= 12 - 2 = 10'}
        ],
        'hints': ['Diagonala principală - diagonala secundară'],
        'explanation': 'det([[a,b],[c,d]]) = ad - bc',
        'formula': 'det(A₂ₓ₂) = a₁₁·a₂₂ - a₁₂·a₂₁'
    },
    {
        'id': 66,
        'question': 'BAC 2023 M1 - Fie A = [[2, 3], [4, 5]]. Calculează det(A)',
        'answer': '-2',
        'difficulty': 3,
        'topic': 'Matrice - Determinanți',
        'subject': 3,
        'points': 5,
        'profile': 'M1',
        'solution_steps': [
            {'step': 1, 'action': 'det = a·d - b·c', 'result': '= 2·5 - 3·4'},
            {'step': 2, 'action': 'Calculăm', 'result': '= 10 - 12 = -2'}
        ],
        'hints': ['Atenție la semn'],
        'explanation': 'Determinantul poate fi negativ.',
        'formula': None
    },
    {
        'id': 67,
        'question': 'BAC 2022 M1 - Calculează det([[5, 2], [3, 1]])',
        'answer': '-1',
        'difficulty': 3,
        'topic': 'Matrice - Determinanți',
        'subject': 3,
        'points': 5,
        'profile': 'M1',
        'solution_steps': [
            {'step': 1, 'action': 'det = 5·1 - 2·3', 'result': '= 5 - 6 = -1'}
        ],
        'hints': ['5·1 = 5, 2·3 = 6'],
        'explanation': '5 - 6 = -1',
        'formula': None
    },
    {
        'id': 68,
        'question': 'BAC 2024 M1 - Calculează det([[1,0,0],[0,2,0],[0,0,3]])',
        'answer': '6',
        'difficulty': 3,
        'topic': 'Matrice - Determinanți 3×3',
        'subject': 3,
        'points': 5,
        'profile': 'M1',
        'solution_steps': [
            {'step': 1, 'action': 'Matrice diagonală', 'result': 'det = produsul diagonalei'},
            {'step': 2, 'action': 'det = 1 × 2 × 3', 'result': '= 6'}
        ],
        'hints': ['Pentru matrice diagonale: det = produs pe diagonală'],
        'explanation': 'Pentru matrice triunghiulare, det = produsul diagonalei.',
        'formula': None
    },
    {
        'id': 69,
        'question': 'BAC 2023 M1 - Fie A = [[2,1,0],[0,3,1],[0,0,1]]. Calculează det(A)',
        'answer': '6',
        'difficulty': 4,
        'topic': 'Matrice - Determinanți 3×3',
        'subject': 3,
        'points': 5,
        'profile': 'M1',
        'solution_steps': [
            {'step': 1, 'action': 'Matrice superior triunghiulară', 'result': 'det = produsul diagonalei'},
            {'step': 2, 'action': 'det = 2 × 3 × 1', 'result': '= 6'}
        ],
        'hints': ['Toate elementele sub diagonală sunt 0'],
        'explanation': 'Matrice triunghiulară → det = produs diagonală.',
        'formula': None
    },
    {
        'id': 70,
        'question': 'BAC 2022 M1 - Calculează det([[1,2,3],[0,1,2],[0,0,2]])',
        'answer': '2',
        'difficulty': 4,
        'topic': 'Matrice - Determinanți 3×3',
        'subject': 3,
        'points': 5,
        'profile': 'M1',
        'solution_steps': [
            {'step': 1, 'action': 'Matrice superior triunghiulară', 'result': 'det = produsul diagonalei'},
            {'step': 2, 'action': 'det = 1 × 1 × 2', 'result': '= 2'}
        ],
        'hints': ['Matrice triunghiulară'],
        'explanation': '1 × 1 × 2 = 2',
        'formula': None
    },
    {
        'id': 71,
        'question': 'BAC 2024 M1 - Fie A = [[1,2],[3,4]] și B = [[2,0],[1,1]]. Calculează (A+B)₁₁',
        'answer': '3',
        'difficulty': 3,
        'topic': 'Matrice - Operații',
        'subject': 3,
        'points': 5,
        'profile': 'M1',
        'solution_steps': [
            {'step': 1, 'action': 'Adunăm element cu element', 'result': 'A+B = [[1+2, 2+0], [3+1, 4+1]]'},
            {'step': 2, 'action': 'Calculăm', 'result': 'A+B = [[3, 2], [4, 5]]'},
            {'step': 3, 'action': 'Elementul (1,1)', 'result': '3'}
        ],
        'hints': ['Adunarea se face element cu element'],
        'explanation': 'La adunare, adunăm elementele de pe aceleași poziții.',
        'formula': None
    },
    {
        'id': 72,
        'question': 'BAC 2023 M1 - Calculează 3×[[1,0],[0,1]]. Care e elementul (2,2)?',
        'answer': '3',
        'difficulty': 2,
        'topic': 'Matrice - Înmulțire scalar',
        'subject': 3,
        'points': 5,
        'profile': 'M1',
        'solution_steps': [
            {'step': 1, 'action': 'Înmulțim fiecare element cu 3', 'result': '3×I₂ = [[3,0],[0,3]]'},
            {'step': 2, 'action': 'Elementul (2,2)', 'result': '3'}
        ],
        'hints': ['Înmulțirea cu scalar: fiecare element × k'],
        'explanation': '3 × matricea identitate = 3I',
        'formula': None
    },
    {
        'id': 73,
        'question': 'BAC 2022 M1 - Fie A = [[2,1],[0,3]]. Calculează A². Care e a₂₂?',
        'answer': '9',
        'difficulty': 4,
        'topic': 'Matrice - Puteri',
        'subject': 3,
        'points': 5,
        'profile': 'M1',
        'solution_steps': [
            {'step': 1, 'action': 'A² = A × A', 'result': '[[2,1],[0,3]] × [[2,1],[0,3]]'},
            {'step': 2, 'action': 'Elementul (2,2) = rândul 2 × coloana 2', 'result': '0·1 + 3·3'},
            {'step': 3, 'action': 'Calculăm', 'result': '= 0 + 9 = 9'}
        ],
        'hints': ['A² = A × A', 'Element (i,j) = rândul i × coloana j'],
        'explanation': 'La înmulțire: (A²)₂₂ = A₂₁·A₁₂ + A₂₂·A₂₂',
        'formula': None
    },
    {
        'id': 74,
        'question': 'BAC 2024 M1 - Calculează rangul matricei [[1,2],[2,4]]',
        'answer': '1',
        'difficulty': 4,
        'topic': 'Matrice - Rang',
        'subject': 3,
        'points': 5,
        'profile': 'M1',
        'solution_steps': [
            {'step': 1, 'action': 'Observăm că rândul 2 = 2 × rândul 1', 'result': '[2,4] = 2×[1,2]'},
            {'step': 2, 'action': 'Rândurile sunt liniar dependente', 'result': 'rang < 2'},
            {'step': 3, 'action': 'Există cel puțin un rând nenul', 'result': 'rang = 1'}
        ],
        'hints': ['Verifică dacă rândurile sunt proporționale'],
        'explanation': 'Rangul = numărul maxim de rânduri liniar independente.',
        'formula': None
    },
    {
        'id': 75,
        'question': 'BAC 2023 M1 - Care e rangul matricei identitate I₃ (3×3)?',
        'answer': '3',
        'difficulty': 2,
        'topic': 'Matrice - Rang',
        'subject': 3,
        'points': 5,
        'profile': 'M1',
        'solution_steps': [
            {'step': 1, 'action': 'I₃ = [[1,0,0],[0,1,0],[0,0,1]]', 'result': 'Toate rândurile independente'},
            {'step': 2, 'action': 'det(I₃) = 1 ≠ 0', 'result': 'rang = 3'}
        ],
        'hints': ['Matricea identitate are rang maxim'],
        'explanation': 'rang(Iₙ) = n',
        'formula': None
    },
    {
        'id': 76,
        'question': 'BAC 2024 M1 - Fie u=(2,3) și v=(1,4). Calculează u·v',
        'answer': '14',
        'difficulty': 3,
        'topic': 'Vectori - Produs scalar',
        'subject': 3,
        'points': 5,
        'profile': 'M1',
        'solution_steps': [
            {'step': 1, 'action': 'Formula produsului scalar', 'result': 'u·v = u₁v₁ + u₂v₂'},
            {'step': 2, 'action': 'Înlocuim', 'result': '= 2·1 + 3·4'},
            {'step': 3, 'action': 'Calculăm', 'result': '= 2 + 12 = 14'}
        ],
        'hints': ['Înmulțim component cu component și adunăm'],
        'explanation': 'Produsul scalar = suma produselor componentelor.',
        'formula': 'u·v = Σuᵢvᵢ'
    },
    {
        'id': 77,
        'question': 'BAC 2023 M1 - Calculează produsul scalar (1,2,3)·(2,1,0)',
        'answer': '4',
        'difficulty': 3,
        'topic': 'Vectori - Produs scalar',
        'subject': 3,
        'points': 5,
        'profile': 'M1',
        'solution_steps': [
            {'step': 1, 'action': 'u·v = u₁v₁ + u₂v₂ + u₃v₃', 'result': '= 1·2 + 2·1 + 3·0'},
            {'step': 2, 'action': 'Calculăm', 'result': '= 2 + 2 + 0 = 4'}
        ],
        'hints': ['Componenta cu 0 dispare'],
        'explanation': '1×2 + 2×1 + 3×0 = 4',
        'formula': None
    },
    {
        'id': 78,
        'question': 'BAC 2022 M1 - Pentru ce k vectorii (k,2) și (3,k) sunt perpendiculari?',
        'answer': '0',
        'difficulty': 4,
        'topic': 'Vectori - Ortogonalitate',
        'subject': 3,
        'points': 5,
        'profile': 'M1',
        'solution_steps': [
            {'step': 1, 'action': 'Vectori perpendiculari ⟺ u·v = 0', 'result': 'k·3 + 2·k = 0'},
            {'step': 2, 'action': 'Simplificăm', 'result': '3k + 2k = 0'},
            {'step': 3, 'action': 'Rezolvăm', 'result': '5k = 0, deci k = 0'}
        ],
        'hints': ['Perpendiculari ⟺ produs scalar = 0'],
        'explanation': 'u ⟂ v ⟺ u·v = 0',
        'formula': None
    },
    {
        'id': 79,
        'question': 'BAC 2024 M1 - Calculează modulul vectorului v=(5,12)',
        'answer': '13',
        'difficulty': 3,
        'topic': 'Vectori - Modul',
        'subject': 3,
        'points': 5,
        'profile': 'M1',
        'solution_steps': [
            {'step': 1, 'action': 'Formula modulului', 'result': '|v| = √(v₁² + v₂²)'},
            {'step': 2, 'action': 'Calculăm', 'result': '|v| = √(25 + 144) = √169'},
            {'step': 3, 'action': 'Rezultat', 'result': '|v| = 13'}
        ],
        'hints': ['5, 12, 13 este triplet pitagoreic'],
        'explanation': 'Modulul = lungimea vectorului.',
        'formula': '|v| = √(x² + y²)'
    },
    {
        'id': 80,
        'question': 'BAC 2023 M1 - Care e lungimea vectorului (1,1,1)?',
        'answer': '1.73',
        'difficulty': 3,
        'topic': 'Vectori - Modul',
        'subject': 3,
        'points': 5,
        'profile': 'M1',
        'solution_steps': [
            {'step': 1, 'action': '|v| = √(1² + 1² + 1²)', 'result': '= √(1 + 1 + 1) = √3'},
            {'step': 2, 'action': '√3 ≈ 1.732', 'result': '≈ 1.73'}
        ],
        'hints': ['√3 ≈ 1.73'],
        'explanation': '√3 = 1.732...',
        'formula': None
    },
    {
        'id': 81,
        'question': 'BAC 2024 M1 - Rezolvă sistemul: 2x+y=7, x+y=4. Care e x?',
        'answer': '3',
        'difficulty': 3,
        'topic': 'Sisteme ecuații',
        'subject': 3,
        'points': 5,
        'profile': 'M1',
        'solution_steps': [
            {'step': 1, 'action': 'Scădem ecuațiile', 'result': '(2x+y) - (x+y) = 7 - 4'},
            {'step': 2, 'action': 'Simplificăm', 'result': 'x = 3'}
        ],
        'hints': ['Metoda eliminării'],
        'explanation': 'Scăzând, y se elimină.',
        'formula': None
    },
    {
        'id': 82,
        'question': 'BAC 2023 M1 - Pentru sistemul x+2y=8, 3x+y=7, care e y?',
        'answer': '3.4',
        'difficulty': 4,
        'topic': 'Sisteme ecuații',
        'subject': 3,
        'points': 5,
        'profile': 'M1',
        'solution_steps': [
            {'step': 1, 'action': 'Din ec.1: x = 8 - 2y', 'result': 'Substituim în ec.2'},
            {'step': 2, 'action': '3(8-2y) + y = 7', 'result': '24 - 6y + y = 7'},
            {'step': 3, 'action': '-5y = -17', 'result': 'y = 17/5 = 3.4'}
        ],
        'hints': ['Metoda substituției'],
        'explanation': '17 ÷ 5 = 3.4',
        'formula': None
    },

    # ============================================
    # SUBIECTUL III - M2 (MATRICE SIMPLE, VECTORI SIMPLI)
    # ============================================
    {
        'id': 83,
        'question': 'BAC 2024 M2 - Calculează suma elementelor matricei [[2,3],[1,4]]',
        'answer': '10',
        'difficulty': 1,
        'topic': 'Matrice - Operații simple',
        'subject': 3,
        'points': 5,
        'profile': 'M2',
        'solution_steps': [
            {'step': 1, 'action': 'Identificăm elementele', 'result': '2, 3, 1, 4'},
            {'step': 2, 'action': 'Adunăm', 'result': '2 + 3 + 1 + 4 = 10'}
        ],
        'hints': ['Adună toate numerele din matrice'],
        'explanation': 'Suma = 2 + 3 + 1 + 4',
        'formula': None
    },
    {
        'id': 84,
        'question': 'BAC 2023 M2 - Fie A = [[5,1],[2,3]]. Calculează a₁₁ + a₂₂',
        'answer': '8',
        'difficulty': 1,
        'topic': 'Matrice - Elemente',
        'subject': 3,
        'points': 5,
        'profile': 'M2',
        'solution_steps': [
            {'step': 1, 'action': 'a₁₁ = elementul (1,1)', 'result': 'a₁₁ = 5'},
            {'step': 2, 'action': 'a₂₂ = elementul (2,2)', 'result': 'a₂₂ = 3'},
            {'step': 3, 'action': 'Suma', 'result': '5 + 3 = 8'}
        ],
        'hints': ['Elementele de pe diagonala principală'],
        'explanation': 'a₁₁ + a₂₂ = suma diagonalei.',
        'formula': None
    },
    {
        'id': 85,
        'question': 'BAC 2022 M2 - Care e elementul de pe linia 1, coloana 2 în [[1,7],[3,4]]?',
        'answer': '7',
        'difficulty': 1,
        'topic': 'Matrice - Elemente',
        'subject': 3,
        'points': 5,
        'profile': 'M2',
        'solution_steps': [
            {'step': 1, 'action': 'Linia 1: [1, 7]', 'result': 'Prima linie'},
            {'step': 2, 'action': 'Coloana 2 din linia 1', 'result': '7'}
        ],
        'hints': ['Linia 1, elementul al 2-lea'],
        'explanation': 'a₁₂ = 7',
        'formula': None
    },
    {
        'id': 86,
        'question': 'BAC 2024 M2 - Calculează 2×[[3,1],[2,4]]. Care e elementul (1,1)?',
        'answer': '6',
        'difficulty': 2,
        'topic': 'Matrice - Înmulțire scalar',
        'subject': 3,
        'points': 5,
        'profile': 'M2',
        'solution_steps': [
            {'step': 1, 'action': 'Înmulțim fiecare element cu 2', 'result': '[[2×3, 2×1], [2×2, 2×4]]'},
            {'step': 2, 'action': 'Rezultat', 'result': '[[6, 2], [4, 8]]'},
            {'step': 3, 'action': 'Elementul (1,1)', 'result': '6'}
        ],
        'hints': ['2 × 3 = 6'],
        'explanation': 'Fiecare element se înmulțește cu scalarul.',
        'formula': None
    },
    {
        'id': 87,
        'question': 'BAC 2023 M2 - Fie A = [[1,2],[3,4]]. Calculează (3A)₂₂',
        'answer': '12',
        'difficulty': 2,
        'topic': 'Matrice - Înmulțire scalar',
        'subject': 3,
        'points': 5,
        'profile': 'M2',
        'solution_steps': [
            {'step': 1, 'action': '3A = [[3,6],[9,12]]', 'result': 'Înmulțim cu 3'},
            {'step': 2, 'action': '(3A)₂₂ = 3 × a₂₂', 'result': '= 3 × 4 = 12'}
        ],
        'hints': ['3 × 4 = 12'],
        'explanation': '(kA)ᵢⱼ = k × aᵢⱼ',
        'formula': None
    },
    {
        'id': 88,
        'question': 'BAC 2022 M2 - Calculează 5×[[0,1],[1,0]]. Suma elementelor?',
        'answer': '10',
        'difficulty': 2,
        'topic': 'Matrice - Operații',
        'subject': 3,
        'points': 5,
        'profile': 'M2',
        'solution_steps': [
            {'step': 1, 'action': '5A = [[0,5],[5,0]]', 'result': 'Înmulțim cu 5'},
            {'step': 2, 'action': 'Suma', 'result': '0 + 5 + 5 + 0 = 10'}
        ],
        'hints': ['5 × (0+1+1+0) = 10'],
        'explanation': 'Suma elementelor × scalar = scalar × suma inițială.',
        'formula': None
    },
    {
        'id': 89,
        'question': 'BAC 2024 M2 - A=[[1,2],[3,4]], B=[[2,1],[1,2]]. Calculează (A+B)₁₂',
        'answer': '3',
        'difficulty': 2,
        'topic': 'Matrice - Adunare',
        'subject': 3,
        'points': 5,
        'profile': 'M2',
        'solution_steps': [
            {'step': 1, 'action': '(A+B)₁₂ = a₁₂ + b₁₂', 'result': '= 2 + 1'},
            {'step': 2, 'action': 'Calculăm', 'result': '= 3'}
        ],
        'hints': ['Se adună elementele de pe aceeași poziție'],
        'explanation': '2 + 1 = 3',
        'formula': None
    },
    {
        'id': 90,
        'question': 'BAC 2023 M2 - Fie A=[[5,0],[0,3]], B=[[1,2],[2,1]]. Care e (A+B)₂₂?',
        'answer': '4',
        'difficulty': 2,
        'topic': 'Matrice - Adunare',
        'subject': 3,
        'points': 5,
        'profile': 'M2',
        'solution_steps': [
            {'step': 1, 'action': '(A+B)₂₂ = a₂₂ + b₂₂', 'result': '= 3 + 1'},
            {'step': 2, 'action': 'Calculăm', 'result': '= 4'}
        ],
        'hints': ['3 + 1 = 4'],
        'explanation': 'Adunare element cu element.',
        'formula': None
    },
    {
        'id': 91,
        'question': 'BAC 2024 M2 - Fie vectorul v=(7,3). Care e prima componentă?',
        'answer': '7',
        'difficulty': 1,
        'topic': 'Vectori - Componente',
        'subject': 3,
        'points': 5,
        'profile': 'M2',
        'solution_steps': [
            {'step': 1, 'action': 'v = (7, 3)', 'result': 'Prima componentă = 7'}
        ],
        'hints': ['Primul număr din paranteză'],
        'explanation': 'În (a, b), a este prima componentă.',
        'formula': None
    },
    {
        'id': 92,
        'question': 'BAC 2023 M2 - Vectorul u=(2,5,8). Care e a doua componentă?',
        'answer': '5',
        'difficulty': 1,
        'topic': 'Vectori - Componente',
        'subject': 3,
        'points': 5,
        'profile': 'M2',
        'solution_steps': [
            {'step': 1, 'action': 'u = (2, 5, 8)', 'result': 'A doua componentă = 5'}
        ],
        'hints': ['Al doilea număr'],
        'explanation': 'Componentele se numără de la stânga la dreapta.',
        'formula': None
    },
    {
        'id': 93,
        'question': 'BAC 2024 M2 - Adună u=(2,3) și v=(1,4). Prima componentă a sumei?',
        'answer': '3',
        'difficulty': 2,
        'topic': 'Vectori - Adunare',
        'subject': 3,
        'points': 5,
        'profile': 'M2',
        'solution_steps': [
            {'step': 1, 'action': 'u + v = (2+1, 3+4)', 'result': '= (3, 7)'},
            {'step': 2, 'action': 'Prima componentă', 'result': '3'}
        ],
        'hints': ['Se adună component cu component'],
        'explanation': '2 + 1 = 3',
        'formula': None
    },
    {
        'id': 94,
        'question': 'BAC 2023 M2 - u=(5,2), v=(3,7). Calculează (u+v)₂',
        'answer': '9',
        'difficulty': 2,
        'topic': 'Vectori - Adunare',
        'subject': 3,
        'points': 5,
        'profile': 'M2',
        'solution_steps': [
            {'step': 1, 'action': '(u+v)₂ = u₂ + v₂', 'result': '= 2 + 7'},
            {'step': 2, 'action': 'Calculăm', 'result': '= 9'}
        ],
        'hints': ['A doua componentă a sumei'],
        'explanation': '2 + 7 = 9',
        'formula': None
    },
    {
        'id': 95,
        'question': 'BAC 2024 M2 - Înmulțește v=(3,5) cu k=2. Prima componentă?',
        'answer': '6',
        'difficulty': 2,
        'topic': 'Vectori - Înmulțire scalar',
        'subject': 3,
        'points': 5,
        'profile': 'M2',
        'solution_steps': [
            {'step': 1, 'action': '2v = (2×3, 2×5)', 'result': '= (6, 10)'},
            {'step': 2, 'action': 'Prima componentă', 'result': '6'}
        ],
        'hints': ['2 × 3 = 6'],
        'explanation': 'Fiecare componentă se înmulțește cu scalarul.',
        'formula': None
    },
    {
        'id': 96,
        'question': 'BAC 2023 M2 - Fie v=(1,2,3). Calculează (4v)₃',
        'answer': '12',
        'difficulty': 2,
        'topic': 'Vectori - Înmulțire scalar',
        'subject': 3,
        'points': 5,
        'profile': 'M2',
        'solution_steps': [
            {'step': 1, 'action': '(4v)₃ = 4 × v₃', 'result': '= 4 × 3'},
            {'step': 2, 'action': 'Calculăm', 'result': '= 12'}
        ],
        'hints': ['4 × 3 = 12'],
        'explanation': 'A treia componentă × 4.',
        'formula': None
    },
    {
        'id': 97,
        'question': 'BAC 2024 M2 - Calculează lungimea vectorului v=(3,4)',
        'answer': '5',
        'difficulty': 2,
        'topic': 'Vectori - Modul',
        'subject': 3,
        'points': 5,
        'profile': 'M2',
        'solution_steps': [
            {'step': 1, 'action': '|v| = √(3² + 4²)', 'result': '= √(9 + 16)'},
            {'step': 2, 'action': 'Calculăm', 'result': '= √25 = 5'}
        ],
        'hints': ['Triplet pitagoreic: 3, 4, 5'],
        'explanation': '3² + 4² = 25, √25 = 5',
        'formula': '|v| = √(x² + y²)'
    },
    {
        'id': 98,
        'question': 'BAC 2023 M2 - Care e modulul vectorului (0,5)?',
        'answer': '5',
        'difficulty': 1,
        'topic': 'Vectori - Modul',
        'subject': 3,
        'points': 5,
        'profile': 'M2',
        'solution_steps': [
            {'step': 1, 'action': '|v| = √(0² + 5²)', 'result': '= √(0 + 25)'},
            {'step': 2, 'action': 'Calculăm', 'result': '= √25 = 5'}
        ],
        'hints': ['√25 = 5'],
        'explanation': 'Prima componentă e 0, deci |v| = |5| = 5.',
        'formula': None
    },
    {
        'id': 99,
        'question': 'BAC 2024 M2 - Fie I₂ matricea identitate 2×2. Suma elementelor?',
        'answer': '2',
        'difficulty': 1,
        'topic': 'Matrice - Identitate',
        'subject': 3,
        'points': 5,
        'profile': 'M2',
        'solution_steps': [
            {'step': 1, 'action': 'I₂ = [[1,0],[0,1]]', 'result': 'Matricea identitate 2×2'},
            {'step': 2, 'action': 'Suma', 'result': '1 + 0 + 0 + 1 = 2'}
        ],
        'hints': ['Identitatea are 1 pe diagonală'],
        'explanation': 'Suma = numărul de 1 pe diagonală = n.',
        'formula': None
    },
    {
        'id': 100,
        'question': 'BAC 2023 M2 - În matricea identitate I₃, care e elementul a₁₁?',
        'answer': '1',
        'difficulty': 1,
        'topic': 'Matrice - Identitate',
        'subject': 3,
        'points': 5,
        'profile': 'M2',
        'solution_steps': [
            {'step': 1, 'action': 'În Iₙ, elementele diagonale = 1', 'result': 'a₁₁ este pe diagonală'},
            {'step': 2, 'action': 'Rezultat', 'result': 'a₁₁ = 1'}
        ],
        'hints': ['Diagonala matricei identitate conține doar 1'],
        'explanation': 'Iₙ are 1 pe diagonală și 0 în rest.',
        'formula': None
    }
]
