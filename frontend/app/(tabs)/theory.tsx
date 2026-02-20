import { useState } from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity, Modal } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

interface Topic {
  id: string;
  name: string;
  subject: number;
  icon: string;
  formulas: string[];
  theory: string;
  tips: string[];
}

const TOPICS: Topic[] = [
  // ============================================
  // SUBIECTUL I
  // ============================================
  {
    id: 'functia_grad1',
    name: 'Funcția de Gradul I',
    subject: 1,
    icon: '📈',
    formulas: [
      '--- FORMA GENERALĂ ---',
      'f: ℝ → ℝ, f(x) = ax + b, a,b ∈ ℝ, a ≠ 0',
      '--- MONOTONIA FUNCȚIEI ---',
      'Dacă a < 0 → f este strict descrescătoare',
      'Dacă a > 0 → f este strict crescătoare',
      '--- SEMNUL FUNCȚIEI ---',
      'Se rezolvă ecuația f(x) = 0 ⟹ x = -b/a',
      'x ∈ (-∞, -b/a): f(x) are semn contrar lui a',
      'x = -b/a: f(x) = 0',
      'x ∈ (-b/a, +∞): f(x) are semn a',
      '--- GRAFICUL ---',
      'Graficul este o dreaptă',
      'Intersecție cu Ox: (-b/a, 0)',
      'Intersecție cu Oy: (0, b)',
      'Panta dreptei: a',
    ],
    theory: 'Funcția de gradul I (liniară) este de forma f(x) = ax + b. Graficul ei este o dreaptă. Monotonia depinde de semnul lui a: crescătoare dacă a > 0, descrescătoare dacă a < 0.',
    tips: [
      'a > 0 → dreaptă urcătoare (crescătoare)',
      'a < 0 → dreaptă coborâtoare (descrescătoare)',
      'Zera funcției: x = -b/a',
    ],
  },
  {
    id: 'ecuatii_liniare',
    name: 'Ecuații Liniare',
    subject: 1,
    icon: '➕',
    formulas: [
      'ax + b = 0  →  x = -b/a',
      'ax + b = cx + d  →  x = (d-b)/(a-c)',
    ],
    theory: 'O ecuație liniară este o ecuație de gradul I în necunoscuta x. Pentru a o rezolva, izolăm necunoscuta în membrul stâng, mutând toți termenii cu x într-o parte și termenii liberi în cealaltă parte.',
    tips: [
      'Mută termenii cu x într-o parte',
      'Mută termenii liberi în cealaltă parte',
      'Împarte la coeficientul lui x',
    ],
  },
  {
    id: 'ecuatii_grad2',
    name: 'Ecuații de Gradul 2',
    subject: 1,
    icon: '✖️',
    formulas: [
      'ax² + bx + c = 0',
      'Δ = b² - 4ac',
      'x₁,₂ = (-b ± √Δ) / 2a',
      'Δ > 0: 2 soluții reale distincte',
      'Δ = 0: soluție dublă x = -b/2a',
      'Δ < 0: nu are soluții reale',
      'a² - b² = (a-b)(a+b)',
      '(a±b)² = a² ± 2ab + b²',
      'Relațiile lui Viète: x₁+x₂ = -b/a, x₁·x₂ = c/a',
    ],
    theory: 'Ecuațiile de gradul 2 se rezolvă folosind formula cu discriminant sau prin factorizare. Discriminantul Δ determină natura soluțiilor.',
    tips: [
      'Verifică mai întâi dacă e pătrat perfect',
      'Caută diferențe de pătrate: a²-b²',
      'Folosește Viète pentru verificare',
    ],
  },
  {
    id: 'functii',
    name: 'Funcții - Definiții',
    subject: 1,
    icon: '📊',
    formulas: [
      '--- NOTAȚII ---',
      'f: A → B, x → f(x)',
      'A = domeniul funcției',
      'B = codomeniul funcției',
      'f(x) = legea de corespondență',
      '--- GRAFICUL FUNCȚIEI ---',
      'A(x,y) ∈ Gf ⟺ f(x) = y',
      'f(prima coordonată) = a doua coordonată',
      'x = abscisa punctului',
      'y = ordonata punctului',
      '--- INTERSECȚII CU AXELE ---',
      'Gf ∩ Ox ⟹ y = 0 ⟹ f(x) = 0',
      'Gf ∩ Oy ⟹ x = 0 ⟹ y = f(0)',
      '--- INTERSECȚIA A DOUĂ GRAFICE ---',
      '1. Se rezolvă f(x) = g(x) pentru abscisă',
      '2. Se determină ordonata punctului',
      '--- COMPUNEREA FUNCȚIILOR ---',
      '(f ∘ g)(x) = f(g(x))',
    ],
    theory: 'O funcție f: A → B asociază fiecărui element din domeniul A exact un element din codomeniul B. Graficul funcției este mulțimea punctelor (x, f(x)).',
    tips: [
      'Pentru f(a), înlocuiește x cu a',
      'Intersecție cu Ox: rezolvă f(x) = 0',
      'Intersecție cu Oy: calculează f(0)',
    ],
  },
  {
    id: 'functii_proprietati',
    name: 'Funcții - Proprietăți',
    subject: 1,
    icon: '🔄',
    formulas: [
      '--- FUNCȚII PARE ȘI IMPARE ---',
      'f: A → ℝ, A mulțime simetrică (-x ∈ A, ∀x ∈ A)',
      'f pară ⟺ f(-x) = f(x), ∀x ∈ A',
      'f impară ⟺ f(-x) = -f(x), ∀x ∈ A',
      '--- FUNCȚII PERIODICE ---',
      'f: D → ℝ periodică cu perioada T dacă:',
      'f(x + T) = f(x), ∀x ∈ D și x + T ∈ D',
      'Perioada principală = cea mai mică T > 0',
      '--- IMAGINEA FUNCȚIEI ---',
      'Imf = {y ∈ B | ∃x ∈ A a.î. f(x) = y}',
      'sau Imf = f(A) = {f(x) | x ∈ A}',
      '--- FUNCȚII INJECTIVE ---',
      'f: A → B este injectivă dacă:',
      '1. f(x₁) = f(x₂) ⟹ x₁ = x₂',
      '2. x₁ ≠ x₂ ⟹ f(x₁) ≠ f(x₂)',
      '3. f este strict monotonă',
      'NU e injectivă: ∃x₁,x₂ ∈ A, x₁≠x₂ și f(x₁)=f(x₂)',
      '--- FUNCȚII SURJECTIVE ---',
      'f: A → B este surjectivă dacă:',
      '∀y ∈ B, ∃x ∈ A a.î. f(x) = y',
      'Echivalent: Imf = B',
      '--- FUNCȚII BIJECTIVE ---',
      'f: A → B este bijectivă dacă:',
      '1. f este injectivă și surjectivă',
      '2. ∀y ∈ B, ∃! x ∈ A a.î. f(x) = y',
      '--- FUNCȚII INVERSABILE ---',
      'f: A → B este inversabilă dacă f este bijectivă',
      '--- INVERSA UNEI FUNCȚII ---',
      'f⁻¹: B → A cu f(x) = y ⟺ x = f⁻¹(y)',
      'f(f⁻¹(x)) = x, x ∈ B',
      'f⁻¹(f(x)) = x, x ∈ A',
      '--- FUNCȚII MONOTONE ---',
      'f monoton crescătoare: x₁<x₂ ⟹ f(x₁)≤f(x₂)',
      'f monoton descrescătoare: x₁<x₂ ⟹ f(x₁)≥f(x₂)',
      'f strict crescătoare: x₁<x₂ ⟹ f(x₁)<f(x₂)',
      'f strict descrescătoare: x₁<x₂ ⟹ f(x₁)>f(x₂)',
    ],
    theory: 'Funcțiile pot avea diverse proprietăți: paritate (simetrie față de Oy), periodicitate, injectivitate (unicitate), surjectivitate (acoperire), bijectivitate (corespondență perfectă).',
    tips: [
      'Pară = simetrică față de Oy',
      'Impară = simetrică față de origine',
      'Strict monotonă ⟹ injectivă',
      'Bijectivă ⟹ inversabilă',
    ],
  },
  {
    id: 'geometrie_analitica',
    name: 'Geometrie Analitică',
    subject: 1,
    icon: '📐',
    formulas: [
      'd(A,B) = √[(x₂-x₁)² + (y₂-y₁)²]',
      'Mijloc M = ((x₁+x₂)/2, (y₁+y₂)/2)',
      'Panta m = (y₂-y₁)/(x₂-x₁)',
      'Ecuația dreptei: y - y₁ = m(x - x₁)',
      'Forma generală: ax + by + c = 0',
      'Drepte paralele: m₁ = m₂',
      'Drepte perpendiculare: m₁ · m₂ = -1',
      'Distanța punct-dreaptă: d = |ax₀+by₀+c|/√(a²+b²)',
    ],
    theory: 'Geometria analitică studiază figurile geometrice folosind coordonate. Distanța între două puncte se calculează cu teorema lui Pitagora.',
    tips: [
      'Tripletele pitagoreice: (3,4,5), (5,12,13), (8,15,17)',
      'Panta = variația lui y / variația lui x',
      'Dreapta prin origine: y = mx',
    ],
  },
  {
    id: 'trigonometrie_geometrie',
    name: 'Trigonometrie în Geometrie',
    subject: 1,
    icon: '📏',
    formulas: [
      '--- TEOREMA COSINUSULUI ---',
      'cos A = (AB² + AC² - BC²) / (2·AB·AC)',
      'cos B = (AB² + BC² - AC²) / (2·AB·BC)',
      'cos C = (AC² + BC² - AB²) / (2·AC·BC)',
      '--- TEOREMA SINUSURILOR ---',
      'BC/sin A = AC/sin B = AB/sin C = 2R',
      'R = raza cercului circumscris',
      '--- ARIA TRIUNGHIULUI ---',
      'A = (b·h)/2',
      'A = (l₁·l₂·sin α)/2',
      'A = √[p(p-a)(p-b)(p-c)] (Heron)',
      'p = (a+b+c)/2 (semiperimetru)',
      '--- RAZE ---',
      'R = (a·b·c)/(4A) - raza circumscrisă',
      'r = A/p - raza înscrisă',
    ],
    theory: 'Teorema cosinusului se aplică când cunoaștem toate laturile sau 2 laturi și unghiul dintre ele. Teorema sinusurilor se aplică în celelalte cazuri.',
    tips: [
      'Toate laturile cunoscute → teorema cosinusului',
      '2 laturi + unghi între ele → teorema cosinusului',
      'Altfel → teorema sinusurilor',
    ],
  },
  {
    id: 'functii_trig_inverse',
    name: 'Funcții Trigonometrice Inverse',
    subject: 1,
    icon: '🔃',
    formulas: [
      '--- ARCSIN ---',
      'arcsin x: [-1, 1] → [-π/2, π/2]',
      'arcsin(sin x) = x, ∀x ∈ [-π/2, π/2]',
      'sin(arcsin x) = x, ∀x ∈ [-1, 1]',
      'arcsin(-x) = -arcsin x, ∀x ∈ [-1, 1]',
      '--- ARCCOS ---',
      'arccos x: [-1, 1] → [0, π]',
      'arccos(cos x) = x, ∀x ∈ [0, π]',
      'cos(arccos x) = x, ∀x ∈ [-1, 1]',
      'arccos(-x) = π - arccos x, ∀x ∈ [-1, 1]',
      '--- ARCTG ---',
      'arctg x: ℝ → (-π/2, π/2)',
      'arctg(tg x) = x, ∀x ∈ (-π/2, π/2)',
      'tg(arctg x) = x, ∀x ∈ [-1, 1]',
      'arctg(-x) = -arctg x, ∀x ∈ ℝ',
      '--- ARCCTG ---',
      'arcctg x: ℝ → (0, π)',
      'arcctg(ctg x) = x, ∀x ∈ (0, π)',
      'ctg(arcctg x) = x, ∀x ∈ [-1, 1]',
      'arcctg(-x) = π - arcctg x, ∀x ∈ ℝ',
      '--- RELAȚII UTILE ---',
      'arcsin x + arccos x = π/2',
      'arctg x + arcctg x = π/2',
    ],
    theory: 'Funcțiile trigonometrice inverse sunt inversele funcțiilor trigonometrice restricționate pe intervale unde sunt bijective. Arcsin și arctg sunt funcții impare, arccos și arcctg nu sunt.',
    tips: [
      'arcsin și arctg sunt impare: f(-x) = -f(x)',
      'arccos(-x) = π - arccos(x)',
      'arcctg(-x) = π - arcctg(x)',
      'Domeniile și codomeniile sunt esențiale!',
    ],
  },
  {
    id: 'combinatorica',
    name: 'Combinatorică',
    subject: 1,
    icon: '🔢',
    formulas: [
      'n! = n × (n-1) × ... × 2 × 1',
      '0! = 1',
      'Permutări: Pₙ = n!',
      'Aranjamente: Aₙᵏ = n!/(n-k)!',
      'Combinări: Cₙᵏ = n!/[k!(n-k)!]',
      'Cₙᵏ = Cₙⁿ⁻ᵏ',
      'Cₙ⁰ = Cₙⁿ = 1',
      'Binomul lui Newton: (a+b)ⁿ = Σ Cₙᵏ·aⁿ⁻ᵏ·bᵏ',
    ],
    theory: 'Permutările = aranjamente ale tuturor elementelor. Aranjamentele = selecții ordonate. Combinările = selecții neordonate.',
    tips: [
      'Ordinea contează? → Aranjamente',
      'Ordinea nu contează? → Combinări',
      'Toate elementele? → Permutări',
    ],
  },
  {
    id: 'probabilitati',
    name: 'Probabilități',
    subject: 1,
    icon: '🎲',
    formulas: [
      'P(A) = cazuri favorabile / cazuri posibile',
      'P(A) ∈ [0, 1]',
      'P(Ā) = 1 - P(A)',
      'P(A∪B) = P(A) + P(B) - P(A∩B)',
      'A,B incompatibile: P(A∪B) = P(A) + P(B)',
      'A,B independente: P(A∩B) = P(A)·P(B)',
    ],
    theory: 'Probabilitatea măsoară șansa ca un eveniment să se întâmple. Se calculează ca raportul dintre numărul de cazuri favorabile și numărul total de cazuri posibile.',
    tips: [
      'Numără mai întâi cazurile totale',
      'Apoi numără cazurile favorabile',
      'Verifică: P trebuie să fie între 0 și 1',
    ],
  },

  // ============================================
  // SUBIECTUL II - ANALIZĂ MATEMATICĂ
  // ============================================
  {
    id: 'limite',
    name: 'Limite de Funcții',
    subject: 2,
    icon: '∞',
    formulas: [
      '--- LIMITE REMARCABILE (caz 0/0) ---',
      'lim (sin x)/x = 1, când x→0',
      'lim (tg x)/x = 1, când x→0',
      'lim (arcsin x)/x = 1, când x→0',
      'lim (arctg x)/x = 1, când x→0',
      '--- CAZ ∞·0 ---',
      'lim ln(1+aₙ)/aₙ = 1, când aₙ→0',
      'lim (bᵃⁿ-1)/aₙ = ln b, când aₙ→0',
      '--- CAZ 1^∞ ---',
      'lim (1+aₙ)^(1/aₙ) = e, când aₙ→0',
      '--- CAZ 0⁰ sau ∞⁰ ---',
      'lim aₙ^bₙ = lim e^(bₙ·ln aₙ)',
      'Criteriul radicalului: lim ⁿ√aₙ = lim aₙ₊₁/aₙ',
      '--- LIMITE LATERALE ---',
      'lₛ(x₀) = lim f(x) când x→x₀, x<x₀',
      'lᵈ(x₀) = lim f(x) când x→x₀, x>x₀',
      '∃ lim f(x) ⟺ lₛ = lᵈ',
    ],
    theory: 'Limita unei funcții descrie comportamentul funcției când x se apropie de o valoare. Pentru cazuri de nedeterminare (0/0, ∞/∞, etc.) folosim tehnici speciale.',
    tips: [
      'Caz ∞/∞: factor comun forțat sau L\'Hospital',
      'Caz ∞-∞: factor comun sau conjugata',
      'L\'Hospital: lim f/g = lim f\'/g\'',
    ],
  },
  {
    id: 'derivate',
    name: 'Derivate',
    subject: 2,
    icon: '📉',
    formulas: [
      '--- DERIVATE SIMPLE ---',
      '(c)\' = 0',
      '(x)\' = 1',
      '(xⁿ)\' = n·xⁿ⁻¹',
      '(√x)\' = 1/(2√x)',
      '(³√x)\' = 1/(3·³√x²)',
      '(ⁿ√x)\' = 1/(n·ⁿ√xⁿ⁻¹)',
      '(aˣ)\' = aˣ·ln a',
      '(eˣ)\' = eˣ',
      '(ln x)\' = 1/x',
      '(logₐx)\' = 1/(x·ln a)',
      '(sin x)\' = cos x',
      '(cos x)\' = -sin x',
      '(tg x)\' = 1/cos²x',
      '(ctg x)\' = -1/sin²x',
      '(arcsin x)\' = 1/√(1-x²)',
      '(arccos x)\' = -1/√(1-x²)',
      '(arctg x)\' = 1/(1+x²)',
      '(arcctg x)\' = -1/(1+x²)',
      '--- DERIVATE COMPUSE ---',
      '(u(x)ⁿ)\' = n·u(x)ⁿ⁻¹·u\'(x)',
      '(eᵘ⁽ˣ⁾)\' = eᵘ⁽ˣ⁾·u\'(x)',
      '(ln u(x))\' = u\'(x)/u(x)',
      '(sin u(x))\' = cos u(x)·u\'(x)',
      '(cos u(x))\' = -sin u(x)·u\'(x)',
      '--- REGULI ---',
      '(f+g)\' = f\' + g\'',
      '(f·g)\' = f\'·g + f·g\'',
      '(f/g)\' = (f\'·g - f·g\')/g²',
      '(f∘g)\' = f\'(g)·g\'',
    ],
    theory: 'Derivata măsoară rata de variație a unei funcții. Geometric, reprezintă panta tangentei la grafic într-un punct. Pentru funcții compuse se aplică regula lanțului.',
    tips: [
      'Derivează termen cu termen',
      'Constanta dispare (derivata = 0)',
      'Exponentul coboară și scade cu 1',
      'Pentru compuse: derivata exteriorului × derivata interiorului',
    ],
  },
  {
    id: 'integrale',
    name: 'Integrale',
    subject: 2,
    icon: '∫',
    formulas: [
      '--- PRIMITIVE DE BAZĂ ---',
      '∫0 dx = C',
      '∫1 dx = x + C',
      '∫xⁿ dx = xⁿ⁺¹/(n+1) + C, n≠-1',
      '∫1/x dx = ln|x| + C',
      '∫eˣ dx = eˣ + C',
      '∫aˣ dx = aˣ/ln a + C',
      '∫sin x dx = -cos x + C',
      '∫cos x dx = sin x + C',
      '∫1/cos²x dx = tg x + C',
      '∫1/sin²x dx = -ctg x + C',
      '∫1/√(1-x²) dx = arcsin x + C',
      '∫1/(1+x²) dx = arctg x + C',
      '--- PROPRIETĂȚI ---',
      '∫[f(x)+g(x)]dx = ∫f(x)dx + ∫g(x)dx',
      '∫k·f(x)dx = k·∫f(x)dx',
      '--- INTEGRALA DEFINITĂ ---',
      '∫ₐᵇ f(x)dx = F(b) - F(a)',
      '∫ₐᵇ f(x)dx = -∫ᵇₐ f(x)dx',
      '∫ₐᵃ f(x)dx = 0',
    ],
    theory: 'Integrala este operația inversă derivării. Integrala nedefinită include constanta C. Integrala definită calculează aria de sub grafic (formula Leibniz-Newton).',
    tips: [
      'Integrala = inversa derivării',
      'Nu uita constanta C la integrale nedefinite',
      'Formula Leibniz-Newton: F(b) - F(a)',
    ],
  },
  {
    id: 'aplicatii_integrale',
    name: 'Aplicații ale Integralei',
    subject: 2,
    icon: '📊',
    formulas: [
      '--- ARIA ---',
      'Aria sub grafic: A = ∫ₐᵇ |f(x)| dx',
      'Aria între două curbe: A = ∫ₐᵇ |f(x)-g(x)| dx',
      '--- VOLUMUL ---',
      'Vol. corp de rotație: V = π·∫ₐᵇ f²(x) dx',
      '(rotație în jurul axei Ox)',
    ],
    theory: 'Integrala definită are numeroase aplicații practice: calculul ariilor plane, volumelor corpurilor de rotație, lungimilor de arc, etc.',
    tips: [
      'Pentru arie, ia valoarea absolută a funcției',
      'Pentru volum, ridică funcția la pătrat și înmulțește cu π',
      'Atenție la limitele de integrare',
    ],
  },
  {
    id: 'studiu_functii',
    name: 'Studiul Funcțiilor',
    subject: 2,
    icon: '📈',
    formulas: [
      '--- MONOTONIE ---',
      'f\' > 0 pe I ⟹ f crescătoare pe I',
      'f\' < 0 pe I ⟹ f descrescătoare pe I',
      '--- EXTREME ---',
      'f\'(x₀) = 0 ⟹ x₀ punct critic',
      'f\'(x₀)=0, f\'\'(x₀)>0 ⟹ x₀ punct de minim',
      'f\'(x₀)=0, f\'\'(x₀)<0 ⟹ x₀ punct de maxim',
      '--- CONVEXITATE ---',
      'f\'\' > 0 ⟹ f convexă',
      'f\'\' < 0 ⟹ f concavă',
      'f\'\'(x₀) = 0 ⟹ punct de inflexiune',
      '--- ASIMPTOTE ---',
      'Verticală: x = a dacă lim f(x) = ±∞ când x→a',
      'Orizontală: y = b dacă lim f(x) = b când x→±∞',
      'Oblică: y = mx + n',
      'm = lim f(x)/x, n = lim [f(x) - mx]',
    ],
    theory: 'Studiul complet al unei funcții include: domeniu, paritate, limite, monotonie (derivata I), convexitate (derivata II), asimptote și grafic.',
    tips: [
      'Derivata I → monotonie și extreme',
      'Derivata II → convexitate și inflexiune',
      'Tabel de semn pentru derivate',
    ],
  },

  // ============================================
  // SUBIECTUL III - MATRICE, DETERMINANȚI
  // ============================================
  {
    id: 'matrice',
    name: 'Matrice',
    subject: 3,
    icon: '🔲',
    formulas: [
      '--- OPERAȚII ---',
      '(A+B)ᵢⱼ = aᵢⱼ + bᵢⱼ',
      '(k·A)ᵢⱼ = k·aᵢⱼ',
      '(A·B)ᵢⱼ = Σₖ aᵢₖ·bₖⱼ',
      '--- PROPRIETĂȚI ---',
      'A·B ≠ B·A (în general)',
      'A·Iₙ = Iₙ·A = A',
      '(A·B)ᵀ = Bᵀ·Aᵀ',
      '--- MATRICE SPECIALE ---',
      'Iₙ = matricea identitate',
      'O = matricea nulă',
      'Aᵀ = transpusa (linii ↔ coloane)',
      '--- INVERSA ---',
      'A·A⁻¹ = A⁻¹·A = Iₙ',
      'A⁻¹ = (1/det A)·A*',
      'A* = matricea adjunctă',
    ],
    theory: 'O matrice este un tablou dreptunghiular de numere. Înmulțirea matricelor se face linie × coloană. Două matrice se pot înmulți doar dacă nr. coloane A = nr. linii B.',
    tips: [
      'Adunarea: element cu element',
      'Înmulțirea: linie × coloană',
      'Verifică dimensiunile la înmulțire',
    ],
  },
  {
    id: 'determinanti',
    name: 'Determinanți',
    subject: 3,
    icon: '🔢',
    formulas: [
      '--- DETERMINANT 2×2 ---',
      'det|a b| = ad - bc',
      '   |c d|',
      '--- DETERMINANT 3×3 (Sarrus) ---',
      'det = a₁₁a₂₂a₃₃ + a₁₂a₂₃a₃₁ + a₁₃a₂₁a₃₂',
      '    - a₁₃a₂₂a₃₁ - a₁₁a₂₃a₃₂ - a₁₂a₂₁a₃₃',
      '--- PROPRIETĂȚI ---',
      'det(Aᵀ) = det(A)',
      'det(A·B) = det(A)·det(B)',
      'det(k·A) = kⁿ·det(A) (n = ordinul)',
      'det(A⁻¹) = 1/det(A)',
      'Linie/coloană de zerouri → det = 0',
      'Două linii/coloane egale → det = 0',
      'Matrice triunghiulară → det = produs diagonală',
    ],
    theory: 'Determinantul este un număr asociat unei matrice pătratice. Pentru 2×2 se calculează ad-bc. Pentru 3×3 se folosește regula lui Sarrus sau dezvoltarea după linie/coloană.',
    tips: [
      'Matrice triunghiulară: det = produs pe diagonală',
      'Simplifică prin operații elementare',
      'det = 0 ⟺ matricea nu e inversabilă',
    ],
  },
  {
    id: 'sisteme',
    name: 'Sisteme de Ecuații',
    subject: 3,
    icon: '🔗',
    formulas: [
      '--- METODA CRAMER ---',
      'Δ = det(A) - determinantul sistemului',
      'Δₓ = det cu coloana x înlocuită',
      'x = Δₓ/Δ',
      '--- CAZURI ---',
      'Δ ≠ 0: sistem compatibil determinat (soluție unică)',
      'Δ = 0, Δₓ ≠ 0: sistem incompatibil (fără soluții)',
      'Δ = 0, Δₓ = 0: sistem compatibil nedeterminat',
      '--- METODA GAUSS ---',
      'Transformăm în sistem triunghiular',
      'Rezolvăm de jos în sus',
      '--- RANG ---',
      'rang(A) = rang(A|B) = n → soluție unică',
      'rang(A) = rang(A|B) < n → ∞ soluții',
      'rang(A) ≠ rang(A|B) → fără soluții',
    ],
    theory: 'Un sistem de ecuații liniare se rezolvă prin metoda Cramer (cu determinanți), Gauss (eliminare) sau matriceal (A⁻¹·B). Natura soluțiilor depinde de ranguri.',
    tips: [
      'Cramer: calculează Δ, apoi Δₓ, Δᵧ',
      'Dacă Δ = 0, verifică compatibilitatea',
      'Gauss: fă zerouri sub diagonală',
    ],
  },
  {
    id: 'vectori',
    name: 'Vectori',
    subject: 3,
    icon: '➡️',
    formulas: [
      '--- OPERAȚII ---',
      'u + v = (u₁+v₁, u₂+v₂, u₃+v₃)',
      'k·u = (k·u₁, k·u₂, k·u₃)',
      '--- PRODUS SCALAR ---',
      'u·v = u₁v₁ + u₂v₂ + u₃v₃',
      'u·v = |u|·|v|·cos(u,v)',
      '--- MODULUL ---',
      '|v| = √(v₁² + v₂² + v₃²)',
      '--- PROPRIETĂȚI ---',
      'u ⊥ v ⟺ u·v = 0',
      'u ∥ v ⟺ u = k·v',
      'cos(u,v) = (u·v)/(|u|·|v|)',
      '--- PRODUS VECTORIAL ---',
      'u × v = (u₂v₃-u₃v₂, u₃v₁-u₁v₃, u₁v₂-u₂v₁)',
      '|u × v| = |u|·|v|·sin(u,v)',
    ],
    theory: 'Vectorii sunt mărimi caracterizate prin modul, direcție și sens. Produsul scalar este un număr, produsul vectorial este un vector perpendicular pe ambii factori.',
    tips: [
      'Perpendiculari: produs scalar = 0',
      'Paraleli: unul e multiplu al celuilalt',
      'Modulul = lungimea vectorului',
    ],
  },
  {
    id: 'polinoame',
    name: 'Polinoame',
    subject: 3,
    icon: '📝',
    formulas: [
      '--- GRAD ---',
      'grad(P·Q) = grad(P) + grad(Q)',
      'grad(P+Q) ≤ max(grad P, grad Q)',
      '--- ÎMPĂRȚIRE ---',
      'P = Q·C + R, grad(R) < grad(Q)',
      '--- RĂDĂCINI ---',
      'P(a) = 0 ⟺ a este rădăcină',
      'P(a) = 0 ⟺ (x-a) | P(x)',
      '--- VIÈTE (grad 2) ---',
      'x₁ + x₂ = -b/a',
      'x₁ · x₂ = c/a',
      '--- VIÈTE (grad 3) ---',
      'x₁+x₂+x₃ = -b/a',
      'x₁x₂+x₂x₃+x₃x₁ = c/a',
      'x₁x₂x₃ = -d/a',
    ],
    theory: 'Polinoamele sunt sume de termeni de forma aₖxᵏ. Teorema împărțirii cu rest și relațiile lui Viète sunt fundamentale pentru lucrul cu polinoame.',
    tips: [
      'Verifică rădăcinile prin înlocuire',
      'Folosește Viète pentru a găsi suma/produsul',
      'Factorizează când e posibil',
    ],
  },
];

export default function TheoryScreen() {
  const [selectedSubject, setSelectedSubject] = useState<number | null>(null);
  const [selectedTopic, setSelectedTopic] = useState<Topic | null>(null);

  const filteredTopics = selectedSubject
    ? TOPICS.filter(t => t.subject === selectedSubject)
    : TOPICS;

  return (
    <ScrollView style={styles.container}>
      {/* Topic Detail Modal */}
      <Modal
        visible={selectedTopic !== null}
        animationType="slide"
        transparent={true}
        onRequestClose={() => setSelectedTopic(null)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <ScrollView showsVerticalScrollIndicator={false}>
              {selectedTopic && (
                <>
                  {/* Header */}
                  <View style={styles.modalHeader}>
                    <Text style={styles.modalIcon}>{selectedTopic.icon}</Text>
                    <Text style={styles.modalTitle}>{selectedTopic.name}</Text>
                    <TouchableOpacity
                      style={styles.closeButton}
                      onPress={() => setSelectedTopic(null)}
                    >
                      <Text style={styles.closeButtonText}>×</Text>
                    </TouchableOpacity>
                  </View>

                  {/* Theory */}
                  <View style={styles.theoryBox}>
                    <Text style={styles.sectionLabel}>📖 Teorie</Text>
                    <Text style={styles.theoryText}>{selectedTopic.theory}</Text>
                  </View>

                  {/* Formulas */}
                  <View style={styles.formulasBox}>
                    <Text style={styles.sectionLabel}>📐 Formule</Text>
                    {selectedTopic.formulas.map((formula, index) => (
                      <View key={index} style={[
                        styles.formulaItem,
                        formula.startsWith('---') && styles.formulaHeader
                      ]}>
                        <Text style={[
                          styles.formulaText,
                          formula.startsWith('---') && styles.formulaHeaderText
                        ]}>
                          {formula.replace(/---/g, '').trim()}
                        </Text>
                      </View>
                    ))}
                  </View>

                  {/* Tips */}
                  <View style={styles.tipsBox}>
                    <Text style={styles.sectionLabel}>💡 Tips & Trucuri</Text>
                    {selectedTopic.tips.map((tip, index) => (
                      <View key={index} style={styles.tipItem}>
                        <Text style={styles.tipBullet}>•</Text>
                        <Text style={styles.tipText}>{tip}</Text>
                      </View>
                    ))}
                  </View>
                </>
              )}
            </ScrollView>
          </View>
        </View>
      </Modal>

      {/* Header */}
      <LinearGradient
        colors={['#8b5cf6', '#6366f1']}
        style={styles.header}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <Text style={styles.headerTitle}>📚 Teorie & Formule</Text>
        <Text style={styles.headerSubtitle}>Tot ce trebuie să știi pentru BAC</Text>
      </LinearGradient>

      {/* Subject Filter */}
      <View style={styles.filterContainer}>
        <ScrollView horizontal showsHorizontalScrollIndicator={false}>
          <TouchableOpacity
            style={[styles.filterChip, selectedSubject === null && styles.filterChipActive]}
            onPress={() => setSelectedSubject(null)}
          >
            <Text style={[styles.filterChipText, selectedSubject === null && styles.filterChipTextActive]}>
              Toate
            </Text>
          </TouchableOpacity>
          {[1, 2, 3].map(subj => (
            <TouchableOpacity
              key={subj}
              style={[styles.filterChip, selectedSubject === subj && styles.filterChipActive]}
              onPress={() => setSelectedSubject(subj)}
            >
              <Text style={[styles.filterChipText, selectedSubject === subj && styles.filterChipTextActive]}>
                Subiectul {subj}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      {/* Topics Grid */}
      <View style={styles.topicsContainer}>
        {filteredTopics.map((topic) => (
          <TouchableOpacity
            key={topic.id}
            style={styles.topicCard}
            onPress={() => setSelectedTopic(topic)}
          >
            <View style={[
              styles.topicIconContainer,
              topic.subject === 1 && styles.subject1,
              topic.subject === 2 && styles.subject2,
              topic.subject === 3 && styles.subject3,
            ]}>
              <Text style={styles.topicIcon}>{topic.icon}</Text>
            </View>
            <Text style={styles.topicName}>{topic.name}</Text>
            <Text style={styles.topicSubject}>Subiectul {topic.subject}</Text>
            <View style={styles.topicMeta}>
              <Text style={styles.topicMetaText}>
                {topic.formulas.filter(f => !f.startsWith('---')).length} formule
              </Text>
            </View>
          </TouchableOpacity>
        ))}
      </View>

      {/* Quick Reference Card */}
      <View style={styles.quickRefCard}>
        <Text style={styles.quickRefTitle}>⚡ Formule de Memorat</Text>

        <View style={styles.quickRefSection}>
          <Text style={styles.quickRefLabel}>Derivate:</Text>
          <Text style={styles.quickRefFormula}>(xⁿ)' = n·xⁿ⁻¹   |   (eˣ)' = eˣ   |   (ln x)' = 1/x</Text>
        </View>

        <View style={styles.quickRefSection}>
          <Text style={styles.quickRefLabel}>Integrale:</Text>
          <Text style={styles.quickRefFormula}>∫xⁿdx = xⁿ⁺¹/(n+1)   |   ∫eˣdx = eˣ   |   ∫1/x dx = ln|x|</Text>
        </View>

        <View style={styles.quickRefSection}>
          <Text style={styles.quickRefLabel}>Trigonometrie:</Text>
          <Text style={styles.quickRefFormula}>sin²x + cos²x = 1   |   tg x = sin x/cos x</Text>
        </View>

        <View style={styles.quickRefSection}>
          <Text style={styles.quickRefLabel}>Determinant 2×2:</Text>
          <Text style={styles.quickRefFormula}>det = ad - bc (diagonala principală - secundară)</Text>
        </View>

        <View style={styles.quickRefSection}>
          <Text style={styles.quickRefLabel}>Arie triunghi:</Text>
          <Text style={styles.quickRefFormula}>A = bh/2   |   A = √[p(p-a)(p-b)(p-c)]</Text>
        </View>
      </View>

      <View style={{ height: 100 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f7fa',
  },
  header: {
    paddingTop: 60,
    paddingBottom: 30,
    paddingHorizontal: 24,
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: '800',
    color: 'white',
    marginBottom: 8,
  },
  headerSubtitle: {
    fontSize: 16,
    color: 'rgba(255,255,255,0.9)',
  },
  filterContainer: {
    paddingVertical: 16,
    paddingHorizontal: 20,
  },
  filterChip: {
    backgroundColor: 'white',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 20,
    marginRight: 8,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  filterChipActive: {
    backgroundColor: '#eff6ff',
    borderColor: '#8b5cf6',
  },
  filterChipText: {
    fontSize: 14,
    color: '#6b7280',
    fontWeight: '600',
  },
  filterChipTextActive: {
    color: '#8b5cf6',
  },
  topicsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    paddingHorizontal: 16,
    gap: 12,
  },
  topicCard: {
    width: '47%',
    backgroundColor: 'white',
    borderRadius: 16,
    padding: 16,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 8,
    elevation: 2,
  },
  topicIconContainer: {
    width: 56,
    height: 56,
    borderRadius: 28,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  subject1: {
    backgroundColor: '#dbeafe',
  },
  subject2: {
    backgroundColor: '#dcfce7',
  },
  subject3: {
    backgroundColor: '#fef3c7',
  },
  topicIcon: {
    fontSize: 28,
  },
  topicName: {
    fontSize: 14,
    fontWeight: '700',
    color: '#1f2937',
    textAlign: 'center',
    marginBottom: 4,
  },
  topicSubject: {
    fontSize: 11,
    color: '#6b7280',
    marginBottom: 8,
  },
  topicMeta: {
    backgroundColor: '#f3f4f6',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  topicMetaText: {
    fontSize: 10,
    color: '#6b7280',
    fontWeight: '600',
  },
  quickRefCard: {
    backgroundColor: '#1f2937',
    margin: 20,
    borderRadius: 16,
    padding: 20,
  },
  quickRefTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: 'white',
    marginBottom: 16,
  },
  quickRefSection: {
    marginBottom: 12,
  },
  quickRefLabel: {
    fontSize: 12,
    color: '#9ca3af',
    marginBottom: 4,
  },
  quickRefFormula: {
    fontSize: 13,
    color: '#fcd34d',
    fontWeight: '600',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: 'white',
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    maxHeight: '90%',
    padding: 24,
  },
  modalHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  modalIcon: {
    fontSize: 32,
    marginRight: 12,
  },
  modalTitle: {
    flex: 1,
    fontSize: 22,
    fontWeight: '800',
    color: '#1f2937',
  },
  closeButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#f3f4f6',
    justifyContent: 'center',
    alignItems: 'center',
  },
  closeButtonText: {
    fontSize: 24,
    color: '#6b7280',
  },
  sectionLabel: {
    fontSize: 14,
    fontWeight: '700',
    color: '#6b7280',
    marginBottom: 12,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  theoryBox: {
    backgroundColor: '#f0fdf4',
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
  },
  theoryText: {
    fontSize: 15,
    color: '#166534',
    lineHeight: 22,
  },
  formulasBox: {
    backgroundColor: '#eff6ff',
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
  },
  formulaItem: {
    backgroundColor: 'white',
    padding: 10,
    borderRadius: 8,
    marginBottom: 6,
  },
  formulaHeader: {
    backgroundColor: '#dbeafe',
    marginTop: 8,
  },
  formulaText: {
    fontSize: 14,
    color: '#1e40af',
  },
  formulaHeaderText: {
    fontWeight: '700',
    color: '#1e3a8a',
    textAlign: 'center',
  },
  tipsBox: {
    backgroundColor: '#fef3c7',
    padding: 16,
    borderRadius: 12,
  },
  tipItem: {
    flexDirection: 'row',
    marginBottom: 8,
  },
  tipBullet: {
    fontSize: 14,
    color: '#92400e',
    marginRight: 8,
  },
  tipText: {
    flex: 1,
    fontSize: 14,
    color: '#78350f',
    lineHeight: 20,
  },
});
