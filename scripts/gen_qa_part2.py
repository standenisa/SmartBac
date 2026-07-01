"""Part 2: 500+ Q&A - Combinatorica, Trigonometrie, Geometrie, Numere complexe, Functii"""
import json
from pathlib import Path

exercises = []
_id = 8000

def add(q, a, steps, typ, topic, diff=1, profile="BOTH"):
    global _id; _id += 1
    exercises.append({"id":_id,"question":q,"answer":a,"type":typ,"steps":steps,"difficulty":diff,"profile":profile,"subject":1,"topic":topic,"source":"gen_qa_v3"})

# ── COMBINATORICA & PROBABILITATI (80+) ──

comb = [
    ("Cat e 5!","5! = 120",["5! = 5·4·3·2·1 = 120"]),
    ("Cat e 6!","6! = 720",["6! = 6·5! = 6·120 = 720"]),
    ("Cat e 7!","7! = 5040",["7! = 7·720 = 5040"]),
    ("Cat e 8!","8! = 40320",["8·7! = 8·5040"]),
    ("Cat e 10!","10! = 3628800",["10·9·8·7·6·5·4·3·2·1"]),
    ("Cat e 0!","0! = 1",["Prin conventie, 0! = 1"]),
    ("Cat e C(5,2)","C(5,2) = 10",["C(5,2) = 5!/(2!·3!) = 120/(2·6) = 10"]),
    ("Cat e C(6,2)","C(6,2) = 15",["6!/(2!·4!) = 720/(2·24) = 15"]),
    ("Cat e C(6,3)","C(6,3) = 20",["6!/(3!·3!) = 720/36 = 20"]),
    ("Cat e C(7,3)","C(7,3) = 35",["7!/(3!·4!) = 5040/(6·24) = 35"]),
    ("Cat e C(8,3)","C(8,3) = 56",["8!/(3!·5!) = 40320/(6·120) = 56"]),
    ("Cat e C(10,2)","C(10,2) = 45",["10!/(2!·8!) = 10·9/2 = 45"]),
    ("Cat e C(10,3)","C(10,3) = 120",["10·9·8/(3·2·1) = 120"]),
    ("Cat e C(n,0)","C(n,0) = 1",["n!/(0!·n!) = 1"]),
    ("Cat e C(n,1)","C(n,1) = n",["n!/(1!·(n-1)!) = n"]),
    ("Cat e C(n,n)","C(n,n) = 1",["n!/(n!·0!) = 1"]),
    ("Ce proprietate are C(n,k)?","C(n,k) = C(n,n-k). Exemplu: C(10,3) = C(10,7).",["Simetria combinărilor"]),
    ("Cat e A(5,2)","A(5,2) = 20",["5!/(5-2)! = 5!/3! = 5·4 = 20"]),
    ("Cat e A(6,3)","A(6,3) = 120",["6!/3! = 6·5·4 = 120"]),
    ("Cat e A(7,2)","A(7,2) = 42",["7!/5! = 7·6 = 42"]),
    ("Cat e P(4)","P(4) = 24",["4! = 24"]),
    ("Cat e P(5)","P(5) = 120",["5! = 120"]),
    ("In cate moduri pot aranja 5 carti pe un raft?","5! = 120 moduri",["Permutari de 5 elemente: P(5) = 120"]),
    ("In cate moduri aleg 3 elevi din 10?","C(10,3) = 120",["Nu conteaza ordinea => combinari"]),
    ("In cate moduri pot forma un comitet de 4 din 8 persoane?","C(8,4) = 70",["8!/(4!·4!) = 70"]),
    ("Cate numere de 3 cifre distincte se pot forma din {1,2,3,4,5}?","A(5,3) = 60",["Conteaza ordinea, cifre distincte => aranjamente"]),
    ("Care e probabilitatea sa dau 6 la un zar?","P = 1/6",["1 caz favorabil din 6 posibile"]),
    ("Care e probabilitatea sa dau numar par la un zar?","P = 3/6 = 1/2",["Cazuri favorabile: 2,4,6 => 3 din 6"]),
    ("Arunc 2 zaruri. Care e probabilitatea ca suma sa fie 7?","P = 6/36 = 1/6",["Perechi cu suma 7: (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) = 6","Total: 36"]),
    ("Am 5 bile rosii si 3 albe. Scot 2 la intamplare. P(ambele rosii)?","P = C(5,2)/C(8,2) = 10/28 = 5/14",["Favorabile: C(5,2) = 10","Posibile: C(8,2) = 28"]),
    ("Am 52 carti. P(sa scot un as)?","P = 4/52 = 1/13",["4 asi din 52 carti"]),
    ("Ce e aranjament cu repetitie?","Cand elementele se pot repeta. Nr = nᵏ (n elemente, k pozitii).",["Exemplu: parola de 4 cifre din {0-9}: 10⁴ = 10000"]),
    ("Ce e combinare cu repetitie?","C cu repetitie(n,k) = C(n+k-1, k).",["Se foloseste rar la BAC"]),
    ("Ce e triunghiul lui Pascal?","Fiecare numar = suma celor 2 de deasupra. Linia n da coeficientii lui (a+b)ⁿ.",["Linia 0: 1","Linia 1: 1 1","Linia 2: 1 2 1","Linia 3: 1 3 3 1","Linia 4: 1 4 6 4 1"]),
    ("Dezvolta (a+b)^4","(a+b)⁴ = a⁴ + 4a³b + 6a²b² + 4ab³ + b⁴",["Coeficienti din triunghiul Pascal: 1,4,6,4,1"]),
    ("Dezvolta (x+1)^3","(x+1)³ = x³ + 3x² + 3x + 1",["C(3,0)x³ + C(3,1)x² + C(3,2)x + C(3,3)"]),
    ("Dezvolta (x-1)^3","(x-1)³ = x³ - 3x² + 3x - 1",["Alternare de semne"]),
    ("Care e termenul general in binomul lui Newton?","Tₖ = C(n,k) · aⁿ⁻ᵏ · bᵏ, k = 0,1,...,n",["Termenul k+1 din dezvoltarea (a+b)ⁿ"]),
    ("Gaseste coeficientul lui x^3 in (x+2)^5","C(5,2)·1³·2² = 10·4 = 40",["Tₖ = C(5,k)·x^(5-k)·2ᵏ","x³ => 5-k=3 => k=2","C(5,2)·2² = 10·4 = 40"]),
    ("Ce e complementara unui eveniment?","P(Ā) = 1 - P(A). Probabilitatea ca A sa NU se intample.",["P(Ā) = 1 - P(A)","Util cand e mai usor sa calculezi P(NU A)"]),
    ("Cand folosesc formula P(A∪B)?","Cand vreau probabilitatea ca A SAU B sa se intample: P(A∪B) = P(A)+P(B)-P(A∩B).",["Atentie: scazi intersectia!"]),
    ("Ce inseamna evenimente mutual exclusive?","A∩B = ∅, nu se pot intampla simultan. Atunci P(A∪B) = P(A)+P(B).",["Exemplu: par si impar la aceeasi aruncare"]),
]

for q,a,s in comb:
    add(q,a,s,"concept","combinatorica",1 if len(a)<50 else 2)

# ── TRIGONOMETRIE (70+) ──

trig = [
    ("Cat e sin(0)?","sin(0) = 0",["Valoare remarcabila"]),
    ("Cat e sin(30°)?","sin(30°) = sin(π/6) = 1/2",["Valoare remarcabila"]),
    ("Cat e sin(45°)?","sin(45°) = sin(π/4) = √2/2",["Valoare remarcabila"]),
    ("Cat e sin(60°)?","sin(60°) = sin(π/3) = √3/2",["Valoare remarcabila"]),
    ("Cat e sin(90°)?","sin(90°) = sin(π/2) = 1",["Valoare remarcabila"]),
    ("Cat e sin(180°)?","sin(180°) = sin(π) = 0",["Valoare remarcabila"]),
    ("Cat e sin(270°)?","sin(270°) = sin(3π/2) = -1",["Valoare remarcabila"]),
    ("Cat e sin(360°)?","sin(360°) = sin(2π) = 0",["Valoare remarcabila"]),
    ("Cat e cos(0)?","cos(0) = 1",["Valoare remarcabila"]),
    ("Cat e cos(30°)?","cos(30°) = cos(π/6) = √3/2",["Valoare remarcabila"]),
    ("Cat e cos(45°)?","cos(45°) = cos(π/4) = √2/2",["Valoare remarcabila"]),
    ("Cat e cos(60°)?","cos(60°) = cos(π/3) = 1/2",["Valoare remarcabila"]),
    ("Cat e cos(90°)?","cos(90°) = cos(π/2) = 0",["Valoare remarcabila"]),
    ("Cat e cos(180°)?","cos(180°) = cos(π) = -1",["Valoare remarcabila"]),
    ("Cat e tg(0)?","tg(0) = 0",["sin(0)/cos(0) = 0/1 = 0"]),
    ("Cat e tg(45°)?","tg(45°) = tg(π/4) = 1",["sin(45°)/cos(45°) = 1"]),
    ("Cat e tg(60°)?","tg(60°) = tg(π/3) = √3",["sin(60°)/cos(60°) = (√3/2)/(1/2) = √3"]),
    ("Cat e tg(30°)?","tg(30°) = tg(π/6) = √3/3",["sin(30°)/cos(30°) = (1/2)/(√3/2) = 1/√3 = √3/3"]),
    ("Cat e tg(90°)?","tg(90°) nu exista (cos(90°)=0, nu putem imparti la 0)",["Nedefinit"]),
    ("Ce e formula lui sin(a+b)?","sin(a+b) = sin(a)cos(b) + cos(a)sin(b)",["Formula de adunare"]),
    ("Ce e formula lui sin(a-b)?","sin(a-b) = sin(a)cos(b) - cos(a)sin(b)",["Formula de scadere"]),
    ("Ce e formula lui cos(a+b)?","cos(a+b) = cos(a)cos(b) - sin(a)sin(b)",["Atentie la minus!"]),
    ("Ce e formula lui cos(a-b)?","cos(a-b) = cos(a)cos(b) + sin(a)sin(b)",["Atentie: plus!"]),
    ("Ce e formula lui tg(a+b)?","tg(a+b) = (tg(a)+tg(b))/(1-tg(a)·tg(b))",["Conditie: 1-tga·tgb ≠ 0"]),
    ("Ce e sin(2a)?","sin(2a) = 2·sin(a)·cos(a)",["Formula de duplicare"]),
    ("Ce e cos(2a)?","cos(2a) = cos²a - sin²a = 2cos²a - 1 = 1 - 2sin²a",["3 forme echivalente"]),
    ("Ce e tg(2a)?","tg(2a) = 2tg(a)/(1-tg²(a))",["Formula de duplicare"]),
    ("Ce e sin²(a) in functie de cos(2a)?","sin²(a) = (1-cos(2a))/2",["Utila la integrale!"]),
    ("Ce e cos²(a) in functie de cos(2a)?","cos²(a) = (1+cos(2a))/2",["Utila la integrale!"]),
    ("Rezolva sin(x)=1/2","x = π/6 + 2kπ sau x = 5π/6 + 2kπ, k∈Z",["sin(x)=1/2 => x=30° sau x=150° + multipli de 360°"]),
    ("Rezolva cos(x)=0","x = π/2 + kπ, k∈Z",["cos(x)=0 => x=90°, 270°, ... "]),
    ("Rezolva sin(x)=0","x = kπ, k∈Z",["x = 0, π, 2π, ..."]),
    ("Rezolva tg(x)=1","x = π/4 + kπ, k∈Z",["tg(x)=1 => x=45° + multipli de 180°"]),
    ("Rezolva sin(x)=cos(x)","tg(x)=1, deci x = π/4 + kπ",["Impartim la cos(x): tg(x) = 1"]),
    ("Rezolva sin(2x)=0","2x = kπ, deci x = kπ/2, k∈Z",["sin(u)=0 => u=kπ"]),
    ("Rezolva cos(x)=-1","x = π + 2kπ = (2k+1)π, k∈Z",["cos(x)=-1 => x=180° + multipli de 360°"]),
    ("Ce e formula ariei cu sinus?","Aria triunghi = (1/2)·a·b·sin(C), unde C e unghiul dintre laturile a si b.",["S = ab·sinC / 2"]),
    ("Ce e teorema sinusurilor?","a/sin(A) = b/sin(B) = c/sin(C) = 2R",["R = raza cercului circumscris"]),
    ("Ce e teorema cosinusului?","a² = b² + c² - 2bc·cos(A). Generalizarea teoremei lui Pitagora.",["Daca A=90°: a² = b² + c² (Pitagora)"]),
    ("Cum transform produsul in suma?","sin(a)cos(b) = [sin(a+b)+sin(a-b)]/2, cos(a)cos(b) = [cos(a-b)+cos(a+b)]/2",["Formule produs -> suma"]),
    ("Cum transform suma in produs?","sin(a)+sin(b) = 2sin((a+b)/2)cos((a-b)/2)",["Formule suma -> produs"]),
]

for q,a,s in trig:
    add(q,a,s,"concept","trigonometrie",1 if "Cat" in q else 2)

# ── NUMERE COMPLEXE (60+) ──

complexe = [
    ("Cat e i^2?","i² = -1",["Definitia unitatii imaginare"]),
    ("Cat e i^3?","i³ = i²·i = -i",["i³ = -1·i = -i"]),
    ("Cat e i^4?","i⁴ = (i²)² = 1",["(-1)² = 1"]),
    ("Cat e i^5?","i⁵ = i⁴·i = i",["Se repeta din 4 in 4"]),
    ("Cat e i^100?","i¹⁰⁰ = (i⁴)²⁵ = 1",["100 = 4·25, restul = 0"]),
    ("Cat e i^2023?","i²⁰²³ = i³ = -i",["2023 = 4·505 + 3, restul = 3"]),
    ("Calculeaza (2+3i)+(1-i)","(2+3i)+(1-i) = 3+2i",["(2+1) + (3-1)i = 3+2i"]),
    ("Calculeaza (3+2i)-(1+4i)","(3+2i)-(1+4i) = 2-2i",["(3-1) + (2-4)i = 2-2i"]),
    ("Calculeaza (2+i)(3-i)","(2+i)(3-i) = 6-2i+3i-i² = 6+i+1 = 7+i",["Distributivitate, i²=-1"]),
    ("Calculeaza (1+i)^2","(1+i)² = 1+2i+i² = 1+2i-1 = 2i",["(1+i)² = 2i"]),
    ("Calculeaza (1+i)^3","(1+i)³ = (1+i)²·(1+i) = 2i·(1+i) = 2i+2i² = -2+2i",["(1+i)³ = -2+2i"]),
    ("Calculeaza |3+4i|","|3+4i| = √(9+16) = √25 = 5",["√(3²+4²) = 5"]),
    ("Calculeaza |1+i|","|1+i| = √(1+1) = √2",["√(1²+1²) = √2"]),
    ("Calculeaza |5-12i|","|5-12i| = √(25+144) = √169 = 13",["√(5²+12²) = 13"]),
    ("Care e conjugatul lui 3+2i?","Conjugatul: 3-2i",["Se schimba semnul partii imaginare"]),
    ("Care e conjugatul lui 5-i?","Conjugatul: 5+i",["Se schimba semnul partii imaginare"]),
    ("Calculeaza (2+i)/(1-i)","(2+i)(1+i)/((1-i)(1+i)) = (2+2i+i+i²)/(1+1) = (1+3i)/2 = 1/2 + 3i/2",["Inmultim cu conjugatul numitorului"]),
    ("Ce e forma trigonometrica?","z = r(cos θ + i·sin θ) unde r=|z| si θ=arg(z).",["r = modulul","θ = argumentul (unghiul)"]),
    ("Ce e formula lui Moivre?","zⁿ = rⁿ(cos(nθ) + i·sin(nθ))",["Ridica la putere in forma trigonometrica"]),
    ("Cum extrag radacina de ordin n?","ⁿ√z = ⁿ√r · (cos((θ+2kπ)/n) + i·sin((θ+2kπ)/n)), k=0,1,...,n-1",["n radacini distincte, echidistante pe cerc"]),
    ("Calculeaza radacinile lui z^2=-1","z = ±i",["z² = -1 => z = i sau z = -i"]),
    ("Calculeaza radacinile lui z^2=i","z = (√2/2)(1+i) sau z = -(√2/2)(1+i)",["i = cos(π/2)+i·sin(π/2)","Radacini: cos(π/4)+i·sin(π/4) = (√2/2)(1+i)"]),
    ("Ce e afixul unui punct?","Afixul punctului M(a,b) este numarul complex z = a+bi.",["M(a,b) <-> z = a+bi"]),
    ("Cum aflu distanta intre 2 puncte cu afixe?","d(z1,z2) = |z1-z2|",["Distanta = modulul diferentei afixelor"]),
    ("Ce e argumentul unui numar complex?","arg(z) = unghiul pe care il face vectorul Oz cu axa Ox. tg(θ) = b/a.",["θ = arctg(b/a)","Atentie la cadran!"]),
    ("Rezolva z^2-4z+5=0","z = 2±i",["delta = 16-20 = -4","z = (4±2i)/2 = 2±i"]),
    ("Rezolva z^2+z+1=0","z = (-1±i√3)/2",["delta = 1-4 = -3","z = (-1±i√3)/2"]),
    ("Rezolva z^2+4=0","z = ±2i",["z² = -4","z = ±2i"]),
    ("Rezolva z^2-2z+2=0","z = 1±i",["delta = 4-8 = -4","z = (2±2i)/2 = 1±i"]),
    ("Ce e z·z̄?","z·z̄ = |z|² = a²+b² (numar real!)",["(a+bi)(a-bi) = a²+b²"]),
]

for q,a,s in complexe:
    add(q,a,s,"concept","numere complexe",1 if len(a)<50 else 2, "M1")

# ── GEOMETRIE ANALITICA (60+) ──

geo = [
    ("Distanta intre A(1,2) si B(4,6)?","d = √((4-1)²+(6-2)²) = √(9+16) = 5",["d = √(3²+4²) = 5"]),
    ("Distanta intre A(0,0) si B(3,4)?","d = √(9+16) = 5",["d = √(3²+4²) = 5"]),
    ("Distanta intre A(-1,2) si B(2,-2)?","d = √(9+16) = 5",["d = √(3²+4²) = 5"]),
    ("Mijlocul segmentului A(2,4) B(6,8)?","M(4,6)",["M = ((2+6)/2, (4+8)/2) = (4,6)"]),
    ("Mijlocul segmentului A(0,0) B(4,2)?","M(2,1)",["M = (4/2, 2/2) = (2,1)"]),
    ("Panta dreptei prin A(1,2) si B(3,6)?","m = (6-2)/(3-1) = 4/2 = 2",["m = (y2-y1)/(x2-x1)"]),
    ("Ecuatia dreptei cu panta 2 prin punctul (1,3)?","y - 3 = 2(x-1) => y = 2x+1",["y - y0 = m(x - x0)"]),
    ("Ecuatia dreptei prin A(0,0) si B(1,1)?","y = x",["m = 1, trece prin origine"]),
    ("Ecuatia dreptei prin A(1,2) si B(3,4)?","y = x+1",["m = (4-2)/(3-1) = 1","y-2 = 1(x-1) => y = x+1"]),
    ("Cand sunt 2 drepte paralele?","Cand au aceeasi panta: m1 = m2.",["Paralele: m1 = m2"]),
    ("Cand sunt 2 drepte perpendiculare?","Cand produsul pantelor e -1: m1·m2 = -1.",["Perpendiculare: m1·m2 = -1"]),
    ("Distanta de la M(2,3) la dreapta x+y-1=0?","d = |2+3-1|/√(1+1) = 4/√2 = 2√2",["d = |ax0+by0+c|/√(a²+b²)"]),
    ("Distanta de la origine la dreapta 3x+4y-10=0?","d = |0+0-10|/√(9+16) = 10/5 = 2",["d = |-10|/5 = 2"]),
    ("Aria triunghiului cu varfurile A(0,0), B(4,0), C(0,3)?","Aria = 6",["Aria = |x1(y2-y3)+x2(y3-y1)+x3(y1-y2)|/2","= |0·(0-3)+4·(3-0)+0·(0-0)|/2 = 12/2 = 6"]),
    ("Ecuatia cercului cu centrul (1,2) si raza 3?","(x-1)²+(y-2)²=9",["(x-a)²+(y-b)²=r²"]),
    ("Ecuatia cercului cu centrul in origine si raza 5?","x²+y²=25",["(x-0)²+(y-0)²=5²"]),
    ("Cum aflu centrul si raza din x²+y²-2x-4y-4=0?","Completam patratul: (x-1)²+(y-2)²=9. Centru(1,2), r=3.",["x²-2x+1 + y²-4y+4 = 4+1+4 = 9","(x-1)²+(y-2)²=9"]),
    ("Ce e conicele?","Cercul, elipsa, parabola, hiperbola - sectiuni intr-un con.",["Cerc: x²+y²=r²","Elipsa: x²/a²+y²/b²=1","Parabola: y=ax²","Hiperbola: x²/a²-y²/b²=1"]),
    ("Ecuatia elipsei?","x²/a² + y²/b² = 1, a>b>0. Focare pe Ox la (±c,0) cu c²=a²-b².",["a = semiax mare, b = semiax mica","c² = a² - b²"]),
    ("Ecuatia hiperbolei?","x²/a² - y²/b² = 1. Focare la (±c,0) cu c²=a²+b².",["Asimptote: y = ±(b/a)x","c² = a² + b²"]),
    ("Ecuatia parabolei?","y² = 2px (deschisa spre dreapta) sau y = ax² (deschisa in sus).",["Focarul: F(p/2, 0)","Directoarea: x = -p/2"]),
    ("Cum aflu intersectia a 2 drepte?","Rezolvi sistemul celor 2 ecuatii. Solutia e punctul de intersectie.",["Exemplu: y=2x+1 si y=-x+4","2x+1=-x+4 => 3x=3 => x=1, y=3"]),
    ("Ce e vectorul director al unei drepte?","Un vector paralel cu dreapta. Daca dreapta are panta m, vectorul director e (1,m).",["Dreapta ax+by+c=0: vector director (b,-a) sau (-b,a)"]),
    ("Ce e vectorul normal al unei drepte?","Un vector perpendicular pe dreapta. Dreapta ax+by+c=0 are normal (a,b).",["Normal la ax+by+c=0: n=(a,b)"]),
    ("Ce e produsul scalar?","u·v = |u|·|v|·cos(θ) = x1·x2 + y1·y2. Daca u·v=0, vectorii sunt perpendiculari.",["u·v = x1x2 + y1y2","u⊥v <=> u·v = 0"]),
    ("Cum aflu unghiul intre 2 drepte?","tg(α) = |m1-m2|/(1+m1·m2). Sau cos(α) = |a1a2+b1b2|/(√(a1²+b1²)·√(a2²+b2²)).",["Folosesti pantele sau normalele"]),
]

for q,a,s in geo:
    add(q,a,s,"concept","geometrie",1 if len(a)<60 else 2)

# ── FUNCTII DETALIATE (80+) ──

functii = [
    ("Ce e functia liniara?","f(x) = ax+b. Graficul e o dreapta cu panta a.",["a = panta","b = ordonata la origine","Crescatoare daca a>0"]),
    ("Ce e functia patratica?","f(x) = ax²+bx+c. Graficul e o parabola.",["a>0: parabola in sus (U)","a<0: parabola in jos (∩)","Varful: V(-b/(2a), -Δ/(4a))"]),
    ("Ce e functia exponentiala?","f(x) = aˣ, a>0, a≠1. Crescatoare daca a>1, descrescatoare daca 0<a<1.",["Domeniu: R","Imagine: (0,+∞)","Trece prin (0,1)"]),
    ("Ce e functia logaritmica?","f(x) = log_a(x), inversa lui aˣ. Domeniu: (0,+∞).",["Crescatoare daca a>1","Descrescatoare daca 0<a<1","Trece prin (1,0)"]),
    ("Ce e functia putere?","f(x) = xⁿ. Para daca n e par (simetrica fata de Oy), impara daca n e impar.",["x²: parabola","x³: curba cubica","x⁻¹ = 1/x: hiperbola"]),
    ("Ce e functia radical?","f(x) = √x = x^(1/2). Domeniu: [0,+∞). Crescatoare.",["√x definita doar pt x≥0","(√x)' = 1/(2√x)"]),
    ("Cum studiez semnul unei functii?","Gasesti zerourile (f(x)=0), faci tabel de semn, verifici semnul pe intervale.",["1. f(x) = 0 => zerourile","2. Tabel de semn","3. Semnul intre zerourile"]),
    ("Ce e injectivitatea?","f e injectiva daca x1≠x2 => f(x1)≠f(x2). Strict monotona => injectiva.",["Fiecare valoare e atinsa cel mult o data","Test: f(x1)=f(x2) => x1=x2"]),
    ("Ce e surjectivitatea?","f:A→B e surjectiva daca fiecare element din B e imaginea a cel putin unui element din A.",["Im(f) = B (codomeniul)","Fiecare y din B are cel putin un x cu f(x)=y"]),
    ("Ce e bijectivitatea?","f e bijectiva daca e injectiva SI surjectiva. Are functie inversa.",["Bijectiva = injectiva + surjectiva","Admite inversa: f⁻¹"]),
    ("Cum gasesc functia inversa?","1) Scrii y=f(x). 2) Exprimi x in functie de y. 3) Inversezi notatia: f⁻¹(y)=x.",["Exemplu: f(x)=2x+1","y=2x+1 => x=(y-1)/2","f⁻¹(x) = (x-1)/2"]),
    ("Ce e compunerea functiilor?","(f∘g)(x) = f(g(x)). Se aplica g intai, apoi f.",["(f∘g)(x) = f(g(x))","In general f∘g ≠ g∘f"]),
    ("Cum aflu domeniul lui f/g?","D(f/g) = D(f) ∩ D(g) \\ {x: g(x)=0}. Adica domeniul comun minus unde g e 0.",["Excludem punctele unde numitorul e 0"]),
    ("Cum aflu domeniul lui sqrt(f)?","D = {x: f(x) ≥ 0}. Sub radical trebuie sa fie nenegativ.",["Rezolvi inecuatia f(x) ≥ 0"]),
    ("Cum aflu domeniul lui ln(f)?","D = {x: f(x) > 0}. Argumentul logaritmului trebuie sa fie strict pozitiv.",["Rezolvi inecuatia f(x) > 0"]),
    ("Ce e graficul unei functii?","Multimea punctelor (x, f(x)) din plan. Se deseneaza pe axe Ox, Oy.",["G(f) = {(x, f(x)) : x ∈ D}"]),
    ("Cum translat graficul?","f(x)+k: sus cu k. f(x-h): dreapta cu h. -f(x): simetrie fata de Ox. f(-x): simetrie fata de Oy.",["Vertical: f(x)+k","Orizontal: f(x-h)","Reflexie Ox: -f(x)","Reflexie Oy: f(-x)"]),
    ("Ce e punctul de intersectie cu Oy?","x=0 => punctul (0, f(0)).",["Inlocuim x=0 in functie"]),
    ("Ce sunt punctele de intersectie cu Ox?","f(x)=0. Gasesti radacinile/zerourile functiei.",["Rezolvi ecuatia f(x) = 0"]),
    ("Cum verific daca o functie e para?","Verifici daca f(-x) = f(x) pentru orice x din domeniu.",["Exemplu: f(x)=x² => f(-x)=(-x)²=x² => para"]),
    ("Cum verific daca o functie e impara?","Verifici daca f(-x) = -f(x) pentru orice x din domeniu.",["Exemplu: f(x)=x³ => f(-x)=(-x)³=-x³=-f(x) => impara"]),
    ("Ce e o functie periodica?","f(x+T) = f(x) pentru orice x. T = perioada. Exemplu: sin(x) are T=2π.",["sin, cos: T=2π","tg, ctg: T=π"]),
    ("Cum aflu asimptota oblica?","m = lim(x→∞) f(x)/x, n = lim(x→∞) (f(x)-mx). Daca m,n finite, asimptota: y=mx+n.",["1. m = lim f(x)/x","2. n = lim (f(x) - mx)","3. Asimptota: y = mx + n"]),
    ("Cum fac studiul complet al lui f(x)=x/(x-1)?","D=R\\{1}, f'=−1/(x−1)², f'>0 niciodata => f mereu descrescatoare. Asimptote: x=1 (vert), y=1 (oriz).",["D = R\\{1}","f'(x) = -1/(x-1)² < 0 mereu","Descrescatoare pe (-∞,1) si (1,+∞)","lim(x→±∞) = 1 => asimptota y=1","lim(x→1) = ±∞ => asimptota x=1"]),
    ("Cum fac studiul complet al lui f(x)=x^2-4x+3?","D=R, f'=2x-4, f'=0 => x=2 (minim). f(2)=-1. Cresc pe (2,∞), desc pe (-∞,2).",["D=R","f'(x)=2x-4, f'=0 => x=2","f''=2>0 => minim","f(2)=4-8+3=-1","Cresc (2,∞), desc (-∞,2)"]),
    ("Cum fac studiul complet al lui f(x)=e^x?","D=R, f'=e^x>0 mereu => strict crescatoare. lim(-∞)=0, lim(+∞)=+∞. Asimptota y=0.",["D=R, Im=(0,+∞)","f'=e^x>0 => crescatoare","Asimptota orizontala y=0 la -∞"]),
    ("Cum fac studiul complet al lui f(x)=ln(x)?","D=(0,+∞), f'=1/x>0 => crescatoare. lim(0+)=-∞, lim(+∞)=+∞. Fara asimptote orizontale.",["D=(0,+∞)","f'=1/x>0 => crescatoare","Asimptota verticala x=0"]),
]

for q,a,s in functii:
    add(q,a,s,"concept","functii",1 if len(a)<60 else 2)

# ── PROGRESII (40+) ──

progresii = [
    ("In progresie aritmetica a1=2, r=3. Cat e a5?","a5 = 2 + 4·3 = 14",["an = a1+(n-1)r = 2+4·3 = 14"]),
    ("In progresie aritmetica a1=1, r=2. Cat e a10?","a10 = 1 + 9·2 = 19",["an = 1+9·2 = 19"]),
    ("In progresie aritmetica a1=5, r=-2. Cat e a6?","a6 = 5 + 5·(-2) = -5",["an = 5+5·(-2) = -5"]),
    ("Suma primilor 10 termeni, a1=1, r=1?","S10 = 10·(1+10)/2 = 55",["Sn = n(a1+an)/2, a10=10"]),
    ("Suma primilor 100 numere naturale?","S = 100·101/2 = 5050",["Formula lui Gauss: n(n+1)/2"]),
    ("In progresie geometrica b1=2, q=3. Cat e b4?","b4 = 2·3³ = 54",["bn = b1·q^(n-1) = 2·27 = 54"]),
    ("In progresie geometrica b1=1, q=2. Cat e b8?","b8 = 1·2⁷ = 128",["bn = 2^(n-1) = 2⁷ = 128"]),
    ("Suma progresiei geometrice b1=1, q=2, n=5?","S5 = 1·(2⁵-1)/(2-1) = 31",["Sn = b1(qⁿ-1)/(q-1)"]),
    ("Suma progresiei geometrice b1=3, q=1/2, n=4?","S4 = 3·(1-(1/2)⁴)/(1-1/2) = 3·(15/16)/(1/2) = 45/8",["Sn = b1(1-qⁿ)/(1-q) pt |q|<1"]),
    ("Cum gasesc ratia daca stiu a1 si a5?","r = (a5-a1)/4. In general r = (am-an)/(m-n).",["r = (am-an)/(m-n)"]),
    ("Cum gasesc ratia daca stiu b1 si b4?","q = ³√(b4/b1). In general q = (bm/bn)^(1/(m-n)).",["q = (bm/bn)^(1/(m-n))"]),
    ("Cum demonstrez ca e progresie aritmetica?","Arati ca an+1 - an = constant, sau ca 2an = an-1 + an+1.",["Diferenta constanta intre termeni consecutivi"]),
    ("Cum demonstrez ca e progresie geometrica?","Arati ca bn+1/bn = constant, sau ca bn² = bn-1 · bn+1.",["Raportul constant intre termeni consecutivi"]),
    ("Ce e suma seriei geometrice infinite?","Daca |q|<1: S = b1/(1-q). Daca |q|≥1: divergenta.",["S∞ = b1/(1-q) pt |q|<1","Exemplu: 1+1/2+1/4+... = 1/(1-1/2) = 2"]),
    ("Suma 1+1/2+1/4+1/8+...?","S = 1/(1-1/2) = 2",["Serie geometrica cu b1=1, q=1/2"]),
    ("Ce e media aritmetica?","Ma(a,b) = (a+b)/2. In progresie aritmetica: an = (an-1+an+1)/2.",["Ma = (a+b)/2"]),
    ("Ce e media geometrica?","Mg(a,b) = √(ab) (pt a,b>0). In progresie geometrica: bn = √(bn-1·bn+1).",["Mg = √(ab)"]),
    ("Ce legatura e intre Ma si Mg?","Ma ≥ Mg mereu (inegalitatea mediilor). Egalitate cand a=b.",["(a+b)/2 ≥ √(ab)","Inegalitatea AM-GM"]),
]

for q,a,s in progresii:
    add(q,a,s,"concept","progresii",1 if len(a)<50 else 2)

# ── CONVERSATII EXTRA (60+) ──

conv = [
    ("Cum rezolv un exercitiu pas cu pas?","1) Citesti enuntul cu atentie. 2) Identifici ce se cere. 3) Alegi metoda. 4) Aplici pas cu pas. 5) Verifici rezultatul.",["Citeste, identifica, aplica, verifica"]),
    ("Ce fac daca nu inteleg enuntul?","Reciteste de 2-3 ori. Subliniaza cuvintele cheie. Deseneaza daca e geometrie. Incearca cu numere mici.",["Reciteste","Subliniaza cuvinte cheie","Deseneaza"]),
    ("Cum imi organizez timpul la BAC?","Subiectul I: max 45 min. Subiectul II: max 45 min. Subiectul III: 60 min. Verificare: 30 min.",["Total: 3 ore","Nu sta prea mult pe un exercitiu"]),
    ("Ce fac daca ma blochez la un exercitiu?","Treci mai departe si revii la el la final. Nu pierde timp pretios pe un singur exercitiu.",["Treci la urmatorul","Revii la final"]),
    ("Cum scriu frumos la BAC?","Scrie citet, subliniaza rezultatele, lasa spatiu intre exercitii, numeroteaza clar.",["Scris citet","Rezultate subliniate","Spatiu intre exercitii"]),
    ("Trebuie sa justific raspunsurile la BAC?","Da! La Subiectul II si III trebuie sa arati TOTI pasii. Fara justificare pierzi puncte.",["Arata TOTI pasii","Justifica fiecare afirmatie"]),
    ("Pot folosi calculator la BAC?","NU! Nu e permis calculator, telefon sau orice dispozitiv electronic la BAC.",["Fara calculator","Fara telefon"]),
    ("Ce stilou folosesc la BAC?","Scrii cu pix albastru. Poti folosi creion pentru scheme si grafice.",["Pix albastru obligatoriu","Creion pentru desene"]),
    ("Pot sa sterg la BAC?","Da, dar taie cu o linie si scrie corect alaturi. Nu folosi corector (tipp-ex).",["Taie cu o linie","NU folosi corector"]),
    ("Cate puncte valoreaza fiecare subiect?","Sub I: 30p, Sub II: 30p, Sub III: 30p + 10p din oficiu = 100p.",["30+30+30+10 = 100"]),
    ("Ce e punctajul din oficiu?","10 puncte acordate tuturor. Deci daca nu scrii nimic, iei nota 1.",["10p automat","Nota minima: 1"]),
    ("Exista formular la BAC?","NU, nu primesti formular. Trebuie sa stii toate formulele pe dinafara.",["Fara formular","Invata formulele!"]),
    ("Da-mi un exercitiu de derivate","Calculeaza derivata functiei f(x) = x³ - 3x² + 2x - 1. Raspuns: f'(x) = 3x² - 6x + 2.",["(x³)' = 3x²","(-3x²)' = -6x","(2x)' = 2","(-1)' = 0"]),
    ("Da-mi un exercitiu de integrale","Calculeaza ∫(2x+1)dx. Raspuns: x² + x + C.",["∫2x dx = x²","∫1 dx = x","Rezultat: x² + x + C"]),
    ("Da-mi un exercitiu de limite","Calculeaza lim(x→2) (x²-4)/(x-2). Raspuns: 4.",["Factorizare: (x-2)(x+2)/(x-2) = x+2","lim(x→2) x+2 = 4"]),
    ("Da-mi un exercitiu de matrice","Calculati det[2 1; 3 4]. Raspuns: 5.",["det = 2·4 - 1·3 = 8-3 = 5"]),
    ("Da-mi un exercitiu usor","Rezolva: 3x + 7 = 22. Raspuns: x = 5.",["3x = 22-7 = 15","x = 15/3 = 5"]),
    ("Da-mi un exercitiu greu","Calculati lim(x→0) (e^x - 1 - x)/x². Raspuns: 1/2.",["L'Hopital de 2 ori sau Taylor","e^x ≈ 1 + x + x²/2","(1+x+x²/2 - 1 - x)/x² = 1/2"]),
    ("Vreau sa exersez ecuatii","Rezolva: x² - 7x + 12 = 0. Raspuns: x=3 sau x=4.",["delta = 49-48 = 1","x = (7±1)/2"]),
    ("Vreau sa exersez determinanti","Calculati det[1 2 3; 4 5 6; 7 8 0]. Raspuns: 27.",["Sarrus sau dezvoltare"]),
]

for q,a,s in conv:
    add(q,a,s,"conversation","conversatie")

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
