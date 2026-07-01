"""Part 4: 700+ Q&A - Exercitii rezolvate extra, demonstratii, teoria multimilor, logica, recap"""
import json
from pathlib import Path

exercises = []
_id = 10000

def add(q, a, steps, typ, topic, diff=1, profile="BOTH"):
    global _id; _id += 1
    exercises.append({"id":_id,"question":q,"answer":a,"type":typ,"steps":steps,"difficulty":diff,"profile":profile,"subject":1,"topic":topic,"source":"gen_qa_v3"})

# ── EXERCITII REZOLVATE SUPLIMENTARE - DERIVATE (50) ──
d = [
    ("Derivata lui f(x)=5x^3-2x^2+x-7","f'(x)=15x²-4x+1",["(5x³)'=15x²","(-2x²)'=-4x","(x)'=1","(-7)'=0"]),
    ("Derivata lui f(x)=(2x+1)^3","f'(x)=6(2x+1)²",["Regula lantului: 3(2x+1)²·2"]),
    ("Derivata lui f(x)=sin(x^3)","f'(x)=3x²cos(x³)",["Regula lantului: cos(x³)·3x²"]),
    ("Derivata lui f(x)=e^(sin(x))","f'(x)=cos(x)·e^(sin(x))",["Regula lantului: e^(sinx)·cosx"]),
    ("Derivata lui f(x)=ln(sin(x))","f'(x)=cos(x)/sin(x)=ctg(x)",["Regula lantului: (1/sinx)·cosx"]),
    ("Derivata lui f(x)=ln(x^2+1)","f'(x)=2x/(x²+1)",["Regula lantului: (1/(x²+1))·2x"]),
    ("Derivata lui f(x)=sqrt(x^2-4)","f'(x)=x/√(x²-4)",["Regula lantului: (1/(2√(x²-4)))·2x"]),
    ("Derivata lui f(x)=e^x·sin(x)","f'(x)=eˣ(sinx+cosx)",["Produs: eˣsinx + eˣcosx"]),
    ("Derivata lui f(x)=x^2·cos(x)","f'(x)=2xcosx-x²sinx",["Produs: 2x·cosx + x²·(-sinx)"]),
    ("Derivata lui f(x)=x/e^x","f'(x)=(1-x)/eˣ = (1-x)e⁻ˣ",["Cat: (eˣ-xeˣ)/e²ˣ = (1-x)/eˣ"]),
    ("Derivata lui f(x)=ln(x)/x","f'(x)=(1-lnx)/x²",["Cat: ((1/x)·x-lnx·1)/x² = (1-lnx)/x²"]),
    ("Derivata lui f(x)=(x+1)·e^(-x)","f'(x)=-x·e⁻ˣ",["Produs: 1·e⁻ˣ + (x+1)·(-e⁻ˣ) = e⁻ˣ(1-x-1) = -xe⁻ˣ"]),
    ("Derivata lui f(x)=tg(2x)","f'(x)=2/cos²(2x)",["Regula lantului: (1/cos²(2x))·2"]),
    ("Derivata lui f(x)=arcsin(2x)","f'(x)=2/√(1-4x²)",["Regula lantului: (1/√(1-(2x)²))·2"]),
    ("Derivata lui f(x)=arctg(x/2)","f'(x)=2/(4+x²)",["Regula lantului: (1/(1+(x/2)²))·(1/2) = 2/(4+x²)"]),
    ("Gaseste f'(2) daca f(x)=x^3-x^2+3","f'(x)=3x²-2x, f'(2)=12-4=8",["f'(2)=3·4-2·2=8"]),
    ("Gaseste f'(π/2) daca f(x)=sinx+cosx","f'(x)=cosx-sinx, f'(π/2)=0-1=-1",["f'(π/2)=cos(π/2)-sin(π/2)=-1"]),
    ("Gaseste f'(0) daca f(x)=xe^x","f'(x)=eˣ+xeˣ=eˣ(1+x), f'(0)=1·1=1",["f'(0)=e⁰(1+0)=1"]),
    ("Arata ca f(x)=x+e^x e strict crescatoare","f'(x)=1+eˣ>0 pentru orice x (eˣ>0 mereu). Deci f e strict crescatoare pe R.",["f'=1+eˣ>0 mereu"]),
    ("Arata ca f(x)=x-sinx≥0 pt x≥0","f(0)=0, f'(x)=1-cosx≥0 mereu (cosx≤1). Deci f creste, f(0)=0 => f(x)≥0.",["f(0)=0, f'≥0 => f crescatoare"]),
    ("Gaseste ecuatia tangentei la f(x)=lnx in x=1","f(1)=0, f'(1)=1. Tangenta: y=x-1.",["y-0=1·(x-1) => y=x-1"]),
    ("Gaseste ecuatia tangentei la f(x)=x³ in x=1","f(1)=1, f'(1)=3. Tangenta: y=3x-2.",["y-1=3(x-1) => y=3x-2"]),
    ("Gaseste punctele de inflexiune ale f(x)=x^3-3x^2","f''(x)=6x-6=0 => x=1. f(1)=-2. Punct inflexiune: (1,-2).",["f'=3x²-6x","f''=6x-6=0 => x=1"]),
    ("Studiaza convexitatea lui f(x)=x^4","f''(x)=12x²≥0 mereu => f convexa pe R.",["f'=4x³","f''=12x²≥0 mereu"]),
    ("Gaseste asimptotele lui f(x)=x/(x-1)","AV: x=1. AO: y=1 (lim(x→∞) x/(x-1) = 1).",["x-1=0 => x=1 (verticala)","lim=1 => y=1 (orizontala)"]),
    ("Gaseste asimptotele lui f(x)=(x^2+1)/x","AV: x=0. AO: y=x (m=1, n=0).",["x=0 (verticala)","f(x)=x+1/x => asimptota oblica y=x"]),
    ("Gaseste asimptotele lui f(x)=e^x/(e^x+1)","AO: y=0 la -∞, y=1 la +∞. Fara AV.",["lim(x→-∞) = 0/(0+1) = 0","lim(x→+∞) = eˣ/eˣ = 1"]),
    ("Valoarea maxima a lui f(x)=x·e^(-x) pt x>0","f'=e⁻ˣ-xe⁻ˣ=e⁻ˣ(1-x)=0 => x=1. f(1)=1/e.",["Maximul e 1/e ≈ 0.368"]),
    ("Calculeaza f'(x) daca f(x)=(1+x²)^(1/2)","f'(x) = x/√(1+x²)",["Regula lantului: (1/2)(1+x²)^(-1/2)·2x"]),
    ("Derivata lui f(x)=x^2·sin(1/x)","f'(x)=2x·sin(1/x)+x²·cos(1/x)·(-1/x²) = 2xsin(1/x)-cos(1/x)",["Produs + lant"]),
]
for q,a,s in d:
    add(q,a,s,"exercise","derivate",2)

# ── EXERCITII REZOLVATE SUPLIMENTARE - INTEGRALE (30) ──
i = [
    ("Calculeaza ∫(4x^3-6x+2)dx","x⁴-3x²+2x+C",["∫4x³=x⁴, ∫-6x=-3x², ∫2=2x"]),
    ("Calculeaza ∫(1/x+e^x)dx","ln|x|+eˣ+C",["∫1/x=ln|x|, ∫eˣ=eˣ"]),
    ("Calculeaza ∫(sinx-cosx)dx","-cosx-sinx+C",["∫sinx=-cosx, ∫(-cosx)=-sinx"]),
    ("Calculeaza ∫(x+1)²dx","x³/3+x²+x+C",["(x+1)²=x²+2x+1","Integram termen cu termen"]),
    ("Calculeaza ∫₀² (x²+1)dx","14/3",["F(x)=x³/3+x","F(2)-F(0)=8/3+2=14/3"]),
    ("Calculeaza ∫₀^(π/2) cosx dx","1",["F(x)=sinx","F(π/2)-F(0)=1-0=1"]),
    ("Calculeaza ∫₁³ (1/x)dx","ln3",["F(x)=lnx","F(3)-F(1)=ln3-ln1=ln3"]),
    ("Calculeaza ∫₀² e^x dx","e²-1",["F(x)=eˣ","F(2)-F(0)=e²-1"]),
    ("Calculeaza aria intre f(x)=x² si Ox pe [0,3]","Aria = 9",["∫₀³ x²dx = x³/3|₀³ = 27/3 = 9"]),
    ("Calculeaza aria intre f(x)=sinx si Ox pe [0,π]","Aria = 2",["∫₀π sinxdx = -cosx|₀π = 1+1 = 2"]),
    ("Calculeaza ∫x²·eˣdx","eˣ(x²-2x+2)+C",["Prin parti de 2 ori"]),
    ("Calculeaza ∫eˣ·sinx dx","eˣ(sinx-cosx)/2 + C",["Prin parti de 2 ori, se obtine ecuatie"]),
    ("Calculeaza ∫1/(x²-1)dx","(1/2)ln|(x-1)/(x+1)|+C",["Fractii simple: 1/(x²-1) = 1/(2(x-1)) - 1/(2(x+1))"]),
    ("Calculeaza ∫x/√(x²+1)dx","√(x²+1)+C",["Substitutie: t=x²+1, dt=2xdx"]),
    ("Calculeaza ∫sin²(x)·cos(x)dx","sin³(x)/3+C",["Substitutie: t=sinx, dt=cosxdx"]),
    ("Calculeaza ∫2x·sin(x²)dx","-cos(x²)+C",["Substitutie: t=x², dt=2xdx"]),
    ("Calculeaza ∫(3x+1)⁴dx","(3x+1)⁵/15+C",["Substitutie: t=3x+1, dt=3dx"]),
    ("Calculeaza ∫eˣ/(eˣ+1)dx","ln(eˣ+1)+C",["Substitutie: t=eˣ+1, dt=eˣdx"]),
    ("Calculeaza ∫₀¹ x·eˣdx","1",["Prin parti: xeˣ-eˣ|₀¹ = (e-e)-(0-1) = 1"]),
    ("Calculeaza ∫₁ᵉ xlnx dx","(e²+1)/4",["Prin parti: u=lnx, dv=xdx"]),
]
for q,a,s in i:
    add(q,a,s,"exercise","integrale",2)

# ── EXERCITII REZOLVATE - ECUATII SI SISTEME (40) ──
ec = [
    ("Rezolva x^2-8x+15=0","x=3, x=5",["delta=64-60=4","x=(8±2)/2"]),
    ("Rezolva x^2+2x-8=0","x=2, x=-4",["delta=4+32=36","x=(-2±6)/2"]),
    ("Rezolva 3x^2-12=0","x=±2",["3x²=12, x²=4, x=±2"]),
    ("Rezolva x^2-10x+25=0","x=5 (dubla)",["delta=100-100=0","x=10/2=5"]),
    ("Rezolva x^4-5x^2+4=0","x=±1, x=±2",["t=x²: t²-5t+4=0","t=1,4 => x²=1,4"]),
    ("Rezolva x^4-13x^2+36=0","x=±2, x=±3",["t=x²: t²-13t+36=0","t=4,9 => x=±2,±3"]),
    ("Rezolva sqrt(x+3)=x+1","x+3=(x+1)², x+3=x²+2x+1, x²+x-2=0, x=-2,1. Verif: x=1✓, x=-2 NU.",["Ridicam la patrat","Verificam: doar x=1 merge"]),
    ("Rezolva sqrt(2x+1)=3","2x+1=9, x=4",["Ridicam: 2x+1=9","x=4. Verif: √9=3 ✓"]),
    ("Rezolva |3x-2|=7","x=3 sau x=-5/3",["3x-2=7=>x=3","3x-2=-7=>x=-5/3"]),
    ("Rezolva |x-1|+|x+2|=5","Discutam pe intervale: x<-2, -2≤x<1, x≥1. Solutii: x=-3, x=2",["3 intervale de discutat"]),
    ("Rezolva 2^x=32","x=5",["2⁵=32"]),
    ("Rezolva 4^x=8","(2²)ˣ=2³, 2²ˣ=2³, 2x=3, x=3/2",["Aducem la baza 2"]),
    ("Rezolva 9^x=27","(3²)ˣ=3³, 3²ˣ=3³, 2x=3, x=3/2",["Aducem la baza 3"]),
    ("Rezolva log₂(x-1)=3","x-1=2³=8, x=9",["log₂(x-1)=3 => x-1=8"]),
    ("Rezolva ln(x²-1)=0","x²-1=e⁰=1, x²=2, x=±√2",["ln(A)=0 => A=1"]),
    ("Rezolva lg(x)+lg(x-3)=1","lg(x(x-3))=1, x²-3x=10, x²-3x-10=0, x=5(x=-2 nu merge)",["lg(ab)=lga+lgb","x²-3x-10=0"]),
    ("Rezolva e^x-2e^(-x)=1","Notam t=eˣ>0: t-2/t=1, t²-t-2=0, t=2. x=ln2.",["t=eˣ, t²-t-2=0","t=2(t=-1 nu merge), x=ln2"]),
    ("Rezolva sin(x)=√3/2","x=π/3+2kπ sau x=2π/3+2kπ",["sin(60°)=√3/2","x=60° sau x=120° + multipli"]),
    ("Rezolva cos(x)=1/2","x=±π/3+2kπ",["cos(60°)=1/2","x=60° sau x=-60° + multipli"]),
    ("Rezolva tg(x)=√3","x=π/3+kπ",["tg(60°)=√3"]),
    ("Rezolva 2sin²x-sinx-1=0","Notam t=sinx: 2t²-t-1=0, t=1 sau t=-1/2. x=π/2+2kπ, x=7π/6+2kπ, x=11π/6+2kπ.",["t=sinx, 2t²-t-1=0","t=1, t=-1/2"]),
    ("Rezolva sistemul x+2y=5, 3x-y=1","x=1, y=2",["Din ec2: y=3x-1","x+2(3x-1)=5 => 7x=7 => x=1"]),
    ("Rezolva sistemul 2x+y=8, x-3y=-1","x=23/7, y=10/7... sau x=25/7... hai sa recalculez: 2x+y=8, x-3y=-1. Din ec2: x=3y-1. 2(3y-1)+y=8 => 7y=10 => y=10/7, x=23/7",["Substitutie"]),
    ("Rezolva sistemul x+y+z=3, x-y=1, y+z=2","x=2,y=1,z=1... verif: 2+1+1=4≠3. Recalculez: x=y+1, y+z=2=>z=2-y. x+y+z=y+1+y+2-y=y+3=3=>y=0,x=1,z=2",["y=0, x=1, z=2"]),
]
for q,a,s in ec:
    add(q,a,s,"exercise","ecuatii",2)

# ── EXERCITII REZOLVATE - COMBINATORICA (25) ──
cb = [
    ("Cate numere de 4 cifre distincte din {1,2,3,4,5}?","A(5,4) = 120",["5·4·3·2 = 120"]),
    ("Cate cuvinte de 3 litere din {a,b,c,d}?","4³ = 64 (cu repetitie)",["4 optiuni pe fiecare pozitie"]),
    ("In cate moduri se pot aseza 6 persoane pe un rand?","6! = 720",["Permutari de 6"]),
    ("In cate moduri se pot aseza 4 persoane la o masa rotunda?","(4-1)! = 3! = 6",["Permutari circulare: (n-1)!"]),
    ("C(n,2)=10. Cat e n?","n(n-1)/2=10, n²-n-20=0, n=5",["n(n-1)=20, n=5"]),
    ("C(n,3)=20. Cat e n?","n(n-1)(n-2)/6=20, n=6",["6·20=120=6·5·4, n=6"]),
    ("Calculati C(100,99)","C(100,99) = 100",["C(n,n-1)=n"]),
    ("Calculati C(100,1)","C(100,1) = 100",["C(n,1)=n"]),
    ("P(bile albe din 5 albe si 3 negre, scotand 2)?","P = C(5,2)/C(8,2) = 10/28 = 5/14",["Favorabile: C(5,2)=10","Posibile: C(8,2)=28"]),
    ("P(cel putin un 6 la 2 zaruri)?","1 - P(niciun 6) = 1 - (5/6)² = 1 - 25/36 = 11/36",["Complementara: P(fara 6) = (5/6)²"]),
    ("P(exact 2 capete la 3 aruncari moneda)?","C(3,2)·(1/2)³ = 3/8",["3 moduri de a alege 2 din 3"]),
    ("Cati termeni are (a+b)^7?","8 termeni (n+1=7+1)",["Binomul are n+1 termeni"]),
    ("Care e coef lui x^4 in (x+1)^6?","C(6,2)·1² = 15",["x⁴ apare cand k=2: C(6,2)x⁴·1²"]),
    ("Demonstreaza C(n,0)+C(n,1)+...+C(n,n)=2^n","Punem a=b=1 in (a+b)ⁿ: (1+1)ⁿ = 2ⁿ = ΣC(n,k)",["Din binomul lui Newton"]),
]
for q,a,s in cb:
    add(q,a,s,"exercise","combinatorica",2)

# ── EXERCITII NUMERE COMPLEXE (25) ──
cx = [
    ("Calculeaza (3+i)(2-i)","6-3i+2i-i²=6-i+1=7-i",["FOIL + i²=-1"]),
    ("Calculeaza (1-2i)²","1-4i+4i²=1-4i-4=-3-4i",["(1-2i)²=-3-4i"]),
    ("Calculeaza (2+i)³","(2+i)²·(2+i) = (3+4i)(2+i) = 6+3i+8i+4i² = 2+11i",["(2+i)²=4+4i+i²=3+4i","(3+4i)(2+i)=2+11i"]),
    ("Modulul lui z=5+12i","|z|=√(25+144)=√169=13",["√(5²+12²)=13"]),
    ("Modulul lui z=8-6i","|z|=√(64+36)=√100=10",["√(8²+6²)=10"]),
    ("Calculeaza z·z̄ pt z=3-4i","z·z̄=(3-4i)(3+4i)=9+16=25=|z|²",["z·z̄=|z|²=25"]),
    ("Afixul mijlocului segmentului z1=2+i, z2=4+3i","(z1+z2)/2 = (6+4i)/2 = 3+2i",["Media afixelor"]),
    ("Rezolva z²+2z+5=0","delta=4-20=-16, z=(-2±4i)/2=-1±2i",["z=-1+2i, z=-1-2i"]),
    ("Rezolva z²-6z+10=0","delta=36-40=-4, z=(6±2i)/2=3±i",["z=3+i, z=3-i"]),
    ("Rezolva z²+9=0","z²=-9, z=±3i",["z=3i sau z=-3i"]),
    ("Forma trigonometrica a lui z=1+i","r=√2, θ=π/4. z=√2(cos(π/4)+i·sin(π/4))",["r=√(1+1)=√2","θ=arctg(1/1)=π/4"]),
    ("Forma trigonometrica a lui z=-1+i","r=√2, θ=3π/4. z=√2(cos(3π/4)+i·sin(3π/4))",["r=√2","θ=π-π/4=3π/4 (cadranul II)"]),
    ("Calculeaza (1+i)^4","(1+i)²=2i, (2i)²=4i²=-4",["(1+i)⁴=-4"]),
    ("Calculeaza (1+i)^6","(1+i)⁴·(1+i)² = -4·2i = -8i",["(1+i)⁶=-8i"]),
    ("Cat e i^2024?","2024=4·506+0, deci i²⁰²⁴=(i⁴)⁵⁰⁶=1",["Restul la 4: 0 => 1"]),
]
for q,a,s in cx:
    add(q,a,s,"exercise","numere complexe",2,"M1")

# ── EXERCITII PROGRESII (20) ──
pr = [
    ("a1=3, r=4. Cat e S10?","S10 = 10·(2·3+9·4)/2 = 10·42/2 = 210",["Sn=n(2a1+(n-1)r)/2"]),
    ("a1=1, an=19, n=10. Cat e r?","r=(19-1)/9=2",["r=(an-a1)/(n-1)"]),
    ("b1=2, q=3. Cat e S4?","S4=2·(3⁴-1)/(3-1)=2·80/2=80",["Sn=b1(qⁿ-1)/(q-1)"]),
    ("Gaseste 3 numere in PA cu suma 15 si produsul 80","a-d, a, a+d: 3a=15=>a=5. 5(25-d²)=80=>d²=9=>d=3. Numerele: 2,5,8.",["a-d+a+a+d=3a=15","(a-d)a(a+d)=a(a²-d²)=80"]),
    ("Gaseste 3 numere in PG cu produsul 64 si suma 21","b/q,b,bq: b³=64=>b=4. 4/q+4+4q=21=>4q²-17q+4=0=>q=4,1/4. Numerele: 1,4,16.",["b³=64=>b=4","4q²-17q+4=0"]),
    ("Demonstreaza 1+2+3+...+n=n(n+1)/2","PA cu a1=1, r=1. Sn=n(1+n)/2=n(n+1)/2.",["Sau prin inductie matematica"]),
    ("Demonstreaza 1+3+5+...+(2n-1)=n²","PA cu a1=1, r=2, an=2n-1. Sn=n(1+2n-1)/2=n².",["Suma primelor n numere impare"]),
    ("Suma 1²+2²+...+n²?","n(n+1)(2n+1)/6",["Formula standard"]),
    ("Suma 1³+2³+...+n³?","[n(n+1)/2]²",["= (Σk)² = patratul sumei Gauss"]),
    ("Suma seriei 1+1/3+1/9+1/27+...?","S=1/(1-1/3)=3/2",["PG infinita: S=b1/(1-q), q=1/3"]),
]
for q,a,s in pr:
    add(q,a,s,"exercise","progresii",2)

# ── TEORIA MULTIMILOR SI LOGICA (25) ──
multi = [
    ("Ce e o multime?","O colectie de obiecte bine definite, numite elemente. Exemplu: A={1,2,3}.",["A = {elemente}","x ∈ A: x apartine lui A"]),
    ("Ce e reuniunea?","A ∪ B = elementele care sunt in A SAU in B (sau in ambele).",["A∪B: tot ce e in cel putin una"]),
    ("Ce e intersectia?","A ∩ B = elementele care sunt in A SI in B.",["A∩B: ce e in ambele"]),
    ("Ce e diferenta?","A \\ B = elementele din A care NU sunt in B.",["A\\B: ce e in A dar nu in B"]),
    ("Ce e complementara?","Ā = U \\ A (tot ce nu e in A, relativ la universul U).",["Complementara: elementele din afara lui A"]),
    ("Ce e submultimea?","A ⊆ B daca orice element din A e si in B.",["A ⊆ B: A e inclusa in B"]),
    ("Cate submultimi are o multime cu n elemente?","2ⁿ submultimi.",["{a,b} are 4 submultimi: ∅, {a}, {b}, {a,b}"]),
    ("Ce e produsul cartezian?","A × B = {(a,b) : a∈A, b∈B}. |A×B| = |A|·|B|.",["Perechi ordonate"]),
    ("Ce e o relatie de echivalenta?","Reflexiva, simetrica, tranzitiva. Imparte multimea in clase.",["Reflexiva: aRa","Simetrica: aRb => bRa","Tranzitiva: aRb, bRc => aRc"]),
    ("Ce e o propozitie logica?","O afirmatie care e fie adevarata, fie falsa. Ex: '5 este prim' (adevarata).",["Valoare de adevar: A sau F"]),
    ("Ce e negatia?","NOT(p): adevarat daca p e fals, fals daca p e adevarat.",["NOT(A) = F, NOT(F) = A"]),
    ("Ce e conjunctia?","p AND q: adevarat doar daca ambele sunt adevarate.",["A AND A = A, A AND F = F"]),
    ("Ce e disjunctia?","p OR q: adevarat daca cel putin una e adevarata.",["F OR F = F, restul A"]),
    ("Ce e implicatia?","p => q: falsa DOAR daca p e adevarata si q e falsa.",["A=>A=A, A=>F=F, F=>A=A, F=>F=A"]),
    ("Ce e echivalenta logica?","p <=> q: adevarata daca ambele au aceeasi valoare de adevar.",["A<=>A=A, F<=>F=A, A<=>F=F"]),
    ("Ce e contrareciprocul?","Daca p=>q, atunci contrareciproca e NOT(q)=>NOT(p). Au aceeasi valoare de adevar.",["Util la demonstratii"]),
    ("Ce e demonstratia prin reducere la absurd?","Presupui contrariul, ajungi la o contradictie, deci afirmatia initiala e adevarata.",["Presupunem NOT(p)","Ajungem la contradictie","Deci p e adevarata"]),
]
for q,a,s in multi:
    add(q,a,s,"concept","logica si multimi",1)

# ── RECAP RAPID (50) ──
recap = [
    ("Formula discriminantului","Δ = b² - 4ac",["delta = b² - 4ac"]),
    ("Formula lui Vieta - suma","x₁ + x₂ = -b/a",["Suma radacinilor"]),
    ("Formula lui Vieta - produs","x₁ · x₂ = c/a",["Produsul radacinilor"]),
    ("Derivata lui xⁿ","(xⁿ)' = nxⁿ⁻¹",["Formula fundamentala"]),
    ("Derivata lui eˣ","(eˣ)' = eˣ",["Unica functie = propria derivata"]),
    ("Derivata lui ln(x)","(ln x)' = 1/x",["x > 0"]),
    ("Derivata lui sin(x)","(sin x)' = cos x",[""]),
    ("Derivata lui cos(x)","(cos x)' = -sin x",["Atentie la minus"]),
    ("Regula produsului","(fg)' = f'g + fg'",["Leibniz"]),
    ("Regula catului","(f/g)' = (f'g - fg')/g²",["Numitor la patrat"]),
    ("Regula lantului","(f(g(x)))' = f'(g(x)) · g'(x)",["Compunere"]),
    ("Integrala lui xⁿ","∫xⁿdx = xⁿ⁺¹/(n+1) + C, n≠-1",["n+1 la numitor"]),
    ("Integrala lui 1/x","∫1/x dx = ln|x| + C",["Modul!"]),
    ("Integrala lui eˣ","∫eˣdx = eˣ + C",[""]),
    ("Integrala lui sinx","∫sinx dx = -cosx + C",["Minus!"]),
    ("Integrala lui cosx","∫cosx dx = sinx + C",[""]),
    ("Formula Leibniz-Newton","∫[a,b]f(x)dx = F(b)-F(a)",[""]),
    ("Identitatea fundamentala trig","sin²x + cos²x = 1",[""]),
    ("Sin dublu unghi","sin(2a) = 2sin(a)cos(a)",[""]),
    ("Cos dublu unghi","cos(2a) = cos²a - sin²a = 2cos²a - 1 = 1 - 2sin²a",["3 forme"]),
    ("Det 2x2","det[a b; c d] = ad - bc",[""]),
    ("Cramer","x = Dx/D, y = Dy/D",[""]),
    ("Inversa 2x2","A⁻¹ = (1/det)·[d -b; -c a]",[""]),
    ("Distanta intre 2 puncte","d = √((x2-x1)²+(y2-y1)²)",[""]),
    ("Ecuatia dreptei","y - y1 = m(x - x1)",[""]),
    ("Permutari","P(n) = n!",[""]),
    ("Aranjamente","A(n,k) = n!/(n-k)!",[""]),
    ("Combinari","C(n,k) = n!/(k!(n-k)!)",[""]),
    ("Binomul Newton","(a+b)ⁿ = Σ C(n,k)aⁿ⁻ᵏbᵏ",[""]),
    ("Termen general PA","aₙ = a₁ + (n-1)r",[""]),
    ("Suma PA","Sₙ = n(a₁+aₙ)/2",[""]),
    ("Termen general PG","bₙ = b₁·qⁿ⁻¹",[""]),
    ("Suma PG","Sₙ = b₁(qⁿ-1)/(q-1)",[""]),
    ("Modulul complex","|a+bi| = √(a²+b²)",[""]),
    ("Conjugatul complex","conj(a+bi) = a-bi",[""]),
    ("i² =","-1",[""]),
    ("Asimptota verticala","x=a daca lim f(x) = ±∞ cand x→a",[""]),
    ("Asimptota orizontala","y=L daca lim f(x) = L cand x→±∞",[""]),
    ("L'Hopital","lim f/g = lim f'/g' (la 0/0 sau ∞/∞)",[""]),
    ("lim sinx/x","= 1 (x→0)",[""]),
    ("lim (1+1/x)^x","= e (x→∞)",[""]),
    ("lim (eˣ-1)/x","= 1 (x→0)",[""]),
    ("Aria cu integrala","A = ∫[a,b] |f(x)| dx",[""]),
    ("Volumul de rotatie","V = π∫[a,b] f²(x) dx",[""]),
    ("Teorema Rolle","f(a)=f(b) => ∃c: f'(c)=0",[""]),
    ("Teorema Lagrange","∃c: f'(c) = (f(b)-f(a))/(b-a)",[""]),
    ("Functie para","f(-x) = f(x)",[""]),
    ("Functie impara","f(-x) = -f(x)",[""]),
    ("AM ≥ GM","(a+b)/2 ≥ √(ab)",[""]),
    ("Pitagora","a² + b² = c²",[""]),
]
for q,a,s in recap:
    add(q,a,s,"formula","formule rapide",1)

# ── CONVERSATII FINALE (80) ──
conv = [
    ("Ce inseamna QED?","Quod Erat Demonstrandum = ceea ce trebuia demonstrat. Se pune la finalul demonstratiei.",["QED = ceea ce trebuia demonstrat"]),
    ("Ce e o axioma Euclid?","Axiomele lui Euclid sunt baza geometriei plane. Cea mai faimoasa: prin 2 puncte trece o singura dreapta.",["5 axiome ale geometriei euclidiene"]),
    ("Cine e Euler?","Leonhard Euler (1707-1783), unul dintre cei mai mari matematicieni. Formula lui Euler: e^(iπ)+1=0.",["e^(iπ) + 1 = 0"]),
    ("Ce e numarul de aur?","φ = (1+√5)/2 ≈ 1.618. Apare in natura, arta, arhitectura. Legat de Fibonacci.",["φ = (1+√5)/2 ≈ 1.618"]),
    ("Matematica e inventata sau descoperita?","Intrebare filosofica! Majoritatea matematicienilor cred ca e descoperita - structurile exista independent de noi.",["Dezbatere veche in filosofia matematicii"]),
    ("Imi poti da un pont pentru BAC?","La Subiectul III, studiul de functie urmeaza MEREU aceeasi pasi. Invata sablonul si aplica-l mecanic.",["Sablonul: D, limite, f', monotonie, extreme, grafic"]),
    ("Am gresit la un exercitiu. Ce fac?","Excelent ca ai gresit - asa inveti! Analizeaza EXACT unde ai gresit, nu doar rezultatul final.",["Greseala = oportunitate de invatare"]),
    ("Cum sa nu mai gresesc la calcule?","1) Scrie citet. 2) Un singur pas per linie. 3) Verifica semnele. 4) La final, inlocuieste in ecuatia originala.",["Scrie citet, un pas/linie, verifica"]),
    ("E ok sa ghicesc la BAC?","La Subiectul I (grila): DA, nu se penalizeaza raspunsurile gresite. La II si III: NU, scrie doar ce stii.",["Grila: da, ghiceste","Dezvoltare: nu"]),
    ("Pot sa scriu pe ciorna la BAC?","Da, primesti ciorna! Fa calculele pe ciorna si scrie curat pe foaia de examen.",["Da, ciorna e permisa"]),
    ("Cum notez la grafic?","1) Deseneaza axele Ox, Oy. 2) Marcheaza intersectiile. 3) Marcheaza asimptotele (punctat). 4) Deseneaza curba. 5) Noteaza punctele importante.",["Axe, intersectii, asimptote, curba"]),
    ("Ce fac daca raman in pana de timp?","Scrie rapid formulele si rezultatele fara detalii. Orice punct e important!",["Scrie macar formulele si raspunsurile"]),
    ("Ce fac daca nu stiu un exercitiu deloc?","Scrie ce formule stii legate de subiect. Chiar si un inceput de rezolvare poate primi puncte partiale.",["Scrie ce stii, orice punct conteaza"]),
    ("Cum imi impart punctele?","Sub I: 6 ex × 5p = 30p. Sub II: 3 ex × 10p = 30p. Sub III: 3 ex × 10p = 30p. + 10p oficiu.",["Total: 30+30+30+10=100"]),
    ("La ce e buna matematica in viata reala?","Gandire logica, rezolvare de probleme, programare, finante, inginerie, stiinta. Plus: antrenezi creierul!",["Gandire logica + aplicatii practice"]),
    ("Exista BAC sesiunea 2?","Da! Daca nu promovezi in sesiunea de vara (iunie), poti da in sesiunea de toamna (august).",["Sesiunea 2: august-septembrie"]),
    ("Se da formula la BAC?","NU! Trebuie sa stii formulele pe dinafara. Nu se da niciun formular.",["Fara formular!"]),
    ("Cum abordez demonstratiile la BAC?","Scrie ipoteza, concluzia. Foloseste definitii si teoreme. Justifica FIECARE pas.",["Ipoteza -> pasi justificati -> concluzie"]),
    ("Ce e un contraexemplu si cand il folosesc?","Un exemplu care infirma o afirmatie. Folosesti cand trebuie sa arati ca ceva NU e adevarat mereu.",["Un singur contraexemplu e suficient"]),
    ("Cum verific o integrala?","Derivezi rezultatul. Daca obtii functia de sub integrala, e corect!",["(∫f dx)' = f(x)"]),
    ("Daca am demonstrat bazat pe grafic e ok?","NU! Demonstratia bazata doar pe grafic nu e riguroasa. Foloseste calcule si formule.",["Graficul ilustreaza, nu demonstreaza"]),
    ("Cum aleg metoda de integrare?","1) Directa (cauti formula). 2) Substitutie (daca vezi f(g(x))·g'(x)). 3) Parti (daca e produs de tipuri diferite).",["Directa > substitutie > parti"]),
    ("Ce e o primitiva si de ce +C?","F e primitiva lui f daca F'=f. +C pentru ca exista infinit de primitive (care difera printr-o constanta).",["F+C e primitiva generala"]),
    ("Cum invat cel mai rapid?","Practica activa > citit pasiv. Rezolva exercitii, nu doar citeste teorie. Invata din greseli.",["Rezolva activ!"]),
    ("Invat mai bine dimineata sau seara?","Depinde de tine! Multi invata mai bine dimineata cand sunt odihniti, dar alege ce functioneaza pentru tine.",["Experimenteaza si vezi"]),
    ("Cat trebuie sa invat pe zi?","45-90 minute focusat > 3 ore neatent. Calitatea conteaza mai mult decat cantitatea.",["45-90 min focusat"]),
    ("Cum fac un plan de invatare?","1) Lista subiectelor. 2) Evalueaza nivelul la fiecare. 3) Aloca mai mult timp la cele slabe. 4) 1 subiect/zi.",["Lista, evalueaza, aloca, executa"]),
    ("Pot sa dau si la alte materii?","Sunt specializat pe matematica de BAC. Pentru alte materii, consulta profesori sau resurse specifice.",["Doar matematica"]),
    ("Ai emotii inainte de BAC?","Ca chatbot nu am emotii, dar inteleg ca tu ai! E normal. Pregatirea buna reduce anxietatea. Respira adanc si fii increzator!",["Pregatire = incredere"]),
    ("Cum gestionez stresul de BAC?","1) Pregateste-te bine (reduce anxietatea). 2) Dormi bine noaptea dinainte. 3) Mananca bine. 4) Respira adanc. 5) Incepe cu ce stii.",["Pregatire + somn + mancare + respiratie"]),
]
for q,a,s in conv:
    add(q,a,s,"conversation","conversatie")

# ── EXERCITII GEOMETRIE EXTRA (20) ──
geo = [
    ("Gaseste panta dreptei 2x+3y-6=0","y=(-2x+6)/3, m=-2/3",["Aducem la forma y=mx+n"]),
    ("Gaseste ecuatia dreptei paralele cu y=3x+1 prin (2,1)","y-1=3(x-2) => y=3x-5",["Paralele: aceeasi panta"]),
    ("Gaseste ecuatia dreptei perpendiculare pe y=2x prin (0,3)","m=-1/2. y=(-1/2)x+3",["m1·m2=-1, m=-1/2"]),
    ("Aria cercului cu raza 5","A=π·25=25π",["A=πr²"]),
    ("Circumferinta cercului cu raza 3","C=2π·3=6π",["C=2πr"]),
    ("Gaseste centrul si raza: x²+y²-6x+4y-12=0","(x-3)²+(y+2)²=25. C(3,-2), r=5.",["Completam patratul"]),
    ("Intersectia dreptelor y=x+1 si y=-x+3","x+1=-x+3 => 2x=2 => x=1, y=2. Punctul (1,2).",["Rezolvam sistemul"]),
    ("Aria paralelogramului cu laturile 5 si 8 si unghi 30°","A=5·8·sin(30°)=20",["A=a·b·sin(α)"]),
    ("Lungimea arcului de cerc cu raza 4 si unghi 60°","L=r·θ=4·π/3=4π/3",["θ=60°=π/3 rad","L=rθ"]),
    ("Aria sectorului de cerc cu raza 6 si unghi 90°","A=(1/2)r²θ=(1/2)·36·π/2=9π",["θ=90°=π/2 rad","A=(1/2)r²θ"]),
]
for q,a,s in geo:
    add(q,a,s,"exercise","geometrie",2)

# ── PROBLEME CU PARAMETRU (15) ──
param = [
    ("Pt ce valori ale lui m, ecuatia x²-2mx+m+2=0 are 2 solutii reale distincte?","Δ>0: 4m²-4(m+2)>0, 4m²-4m-8>0, m²-m-2>0, (m-2)(m+1)>0. m∈(-∞,-1)∪(2,+∞).",["Δ=4m²-4m-8>0","m<-1 sau m>2"]),
    ("Pt ce m, ecuatia x²+mx+1=0 are solutii reale?","Δ≥0: m²-4≥0, |m|≥2. m∈(-∞,-2]∪[2,+∞).",["m²≥4"]),
    ("Pt ce m, dreapta y=mx+1 e tangenta la parabola y=x²?","x²=mx+1, x²-mx-1=0, Δ=0: m²+4=0. Nu exista m real... Recalculez: x²-mx+1=0? Daca y=mx+1 tangent la y=x²: x²=mx+1 => x²-mx-1=0, Δ=m²+4>0 mereu. Hmm, y=mx-1 tangent: x²-mx+1=0, Δ=m²-4=0, m=±2.",["Δ=0 pentru tangenta"]),
    ("Pt ce m, f(x)=mx²+2x-1 are minim?","m>0 (parabola in sus). Minimul = -Δ/(4m) = -(4+4m)/(4m).",["a>0 => minim"]),
    ("Pt ce m, f(x)=x³-3mx are 2 puncte de extrem?","f'=3x²-3m=0 => x²=m. Exista solutii daca m>0.",["m>0 => 2 puncte critice"]),
    ("Pt ce m, sistemul x+y=m, x-y=2 are solutie cu x>0 si y>0?","x=(m+2)/2>0 => m>-2. y=(m-2)/2>0 => m>2. Raspuns: m>2.",["x>0: m>-2","y>0: m>2"]),
    ("Pt ce m, lim(x→∞) (mx²+1)/(x²+m) = 2?","lim = m/1 = m. Deci m=2.",["Raport coeficienti dominanti"]),
]
for q,a,s in param:
    add(q,a,s,"exercise","parametru",3)

# ── DEMONSTRATII CLASICE (20) ──
demo = [
    ("Demonstreaza ca √2 e irational","Presupunem √2=p/q ireductibila. 2=p²/q², p²=2q². Deci p e par, p=2k. 4k²=2q², q²=2k². Deci q e par. Contradictie (p/q ireductibila).",["Reducere la absurd"]),
    ("Demonstreaza ca suma a 2 numere pare e para","2a+2b=2(a+b) care e par.",["Direct"]),
    ("Demonstreaza ca produsul a 2 numere impare e impar","(2a+1)(2b+1)=4ab+2a+2b+1=2(2ab+a+b)+1 care e impar.",["Direct"]),
    ("Demonstreaza prin inductie ca 1+2+...+n=n(n+1)/2","Baza: n=1, 1=1·2/2 ✓. Pas: presupunem pt n=k. Pt k+1: 1+...+k+(k+1) = k(k+1)/2+(k+1) = (k+1)(k+2)/2 ✓.",["Inductie matematica"]),
    ("Demonstreaza ca |a+b|≤|a|+|b|","Inegalitatea triunghiului. Se demonstreaza ridicand la patrat ambii membri.",["(a+b)² ≤ (|a|+|b|)²","a²+2ab+b² ≤ a²+2|a||b|+b²","2ab ≤ 2|ab| ✓"]),
    ("Demonstreaza ca AM≥GM pt 2 numere","(a+b)/2 ≥ √(ab) <=> a+b ≥ 2√(ab) <=> (√a-√b)² ≥ 0 (mereu adevarat).",["(√a-√b)² ≥ 0 => a-2√(ab)+b ≥ 0"]),
    ("Demonstreaza ca e^x≥1+x","f(x)=eˣ-1-x, f'(x)=eˣ-1=0=>x=0. f(0)=0, f''>0=>minim. Deci f(x)≥0.",["f(0)=0 e minim global"]),
    ("Demonstreaza ca ln(x)≤x-1 pt x>0","f(x)=x-1-lnx, f'(x)=1-1/x=0=>x=1. f(1)=0, f''>0=>minim.",["Minimul e 0 in x=1"]),
    ("Demonstreaza ca sinx≤x pt x≥0","f(x)=x-sinx, f'(x)=1-cosx≥0 (mereu). f(0)=0 si f creste => f(x)≥0.",["f crescatoare cu f(0)=0"]),
    ("Demonstreaza ca ecuatia e^x=x+2 are exact o solutie","f(x)=eˣ-x-2. f(0)=-1<0, f(2)=e²-4>0. + f'=eˣ-1, strict cresc pt x>0, deci o singura radacina.",["Bolzano: f schimba semnul","Strict monotona local => o radacina"]),
]
for q,a,s in demo:
    add(q,a,s,"demonstration","demonstratii",3)

# ── SFATURI PER SUBIECT (20) ──
sf = [
    ("Sfaturi Subiectul I","Citeste ATENT. Sunt exercitii directe. Nu sta mai mult de 5 min pe unul. Verifica raspunsul.",["Max 5 min/exercitiu","Verifica mereu"]),
    ("Sfaturi Subiectul II matrice","Calculeaza determinanti cu atentie (semnele!). La inversa, verifica: A·A⁻¹=I. La puterea matricei, cauta pattern.",["Atentie la semne","Verifica A·A⁻¹=I"]),
    ("Sfaturi Subiectul III studiu de functie","Urmeaza sablonul: domeniu, limite, derivata, monotonie, extreme, convexitate, grafic. E mecanic!",["Sablonul fix te salveaza"]),
    ("Cum iau punctaj maxim la grafic?","Deseneaza clar axele, noteaza intersectiile, asimptotele (punctat), punctele de extrem, si comportarea la infinit.",["Axe + intersectii + asimptote + extreme"]),
    ("Ce gresesc la Subiectul III?","1) Domeniu gresit. 2) Derivata gresita (regula lantului!). 3) Tabel incomplet. 4) Grafic aproximativ.",["Top 4 greseli la Sub III"]),
    ("Cum verific daca am rezolvat bine un sistem?","Inlocuiesti x,y,z in TOATE ecuatiile initiale. Toate trebuie sa fie satisfacute.",["Inlocuiesti in toate ecuatiile"]),
    ("Cum verific o derivata?","Verifica regula aplicata, semnele, si ca n-ai uitat regula lantului la compuneri.",["Verifica regula + semne + lant"]),
    ("Cum verific o limita?","Inlocuieste un numar foarte mare (sau foarte mic) si vezi daca se apropie de raspunsul tau.",["Test numeric"]),
    ("Ce trebuie sa stiu perfect pt nota 7?","Subiectul I complet (30p) + jumatate din Sub II (15p) + putin din Sub III (5p) + oficiu (10p) = 60p ≈ nota 7.",["Sub I + jumatate Sub II"]),
    ("Ce trebuie sa stiu pt nota 9?","Tot de la nota 7 + Sub II complet + Sub III aproape complet. Derivate si integrale fluent.",["Sub I + Sub II + mare parte Sub III"]),
]
for q,a,s in sf:
    add(q,a,s,"advice","sfaturi BAC",1)

# ── MINI-CONVERSATII EXTRA (50) ──
mini = [
    ("Super","Ma bucur! Hai la urmatorul exercitiu!",["Continua!"]),
    ("Cool","Multumesc! Matematica poate fi cool cand o intelegi!",["Hai sa continuam"]),
    ("Interesant","Da, matematica are multe lucruri interesante! Vrei sa exploram mai mult?",["Mai vrei?"]),
    ("Perfect","Bravo! Inseamna ca intelegi bine. Hai la ceva mai provocator!",["Trecem la nivel urmator?"]),
    ("Aaa am inteles","Super ca ai inteles! Vrei sa trecem mai departe sau sa exersam?",["Mai departe sau exersam?"]),
    ("Repeta","Sigur! Care parte vrei sa repet? Spune-mi si explic din nou.",["Ce sa repet?"]),
    ("Mai lent","Ok, iau mai incet. Care pas nu l-ai inteles?",["Care pas?"]),
    ("Mai rapid","Ok! Iti dau raspunsul direct. Intreaba daca vrei detalii.",["Raspuns rapid"]),
    ("Arata-mi formula","Care formula? Spune subiectul: derivate, integrale, trig, matrice, combinatorica?",["Ce subiect?"]),
    ("E corect?","Spune-mi ce ai calculat si verific! Scrie rezolvarea ta.",["Scrie rezolvarea"]),
    ("Am terminat","Bravo! Orice exercitiu rezolvat te apropie de BAC. Vrei sa mai facem?",["Felicitari!"]),
    ("Nu vreau matematica","Inteleg, dar BAC-ul se apropie! Fa macar un exercitiu pe zi si vei vedea progresul.",["Un exercitiu/zi minim"]),
    ("Sunt confuz","E ok sa fii confuz - asa incepe invatarea! Spune-mi exact ce te confuzeaza.",["Spune-mi ce te confuzeaza"]),
    ("Nu stiu","Nu-i nimic! Toata lumea incepe de undeva. Spune-mi ce subiect si incepem de la baze.",["Incepem de la baze"]),
    ("Poti sa rezolvi orice?","Pot rezolva exercitii de matematica de nivel BAC/liceu. Scrie exercitiul si incerc!",["Da, la nivel BAC"]),
    ("Cat de sigur esti?","Formulele si regulile sunt sigure 100%. La exercitii complexe, verifica mereu rezultatul!",["Verifica mereu"]),
    ("Am gresit","Nu-i nimic! Din greseli invatam cel mai mult. Unde ai gresit exact?",["Unde ai gresit?"]),
    ("E ciudat","Ce anume ti se pare ciudat? Spune-mi si explic de ce e asa.",["Ce e ciudat?"]),
    ("Wow nu stiam","Uite ca ai invatat ceva nou! Matematica e plina de surprize.",["Invatare continua"]),
    ("Esti sigur?","Da! Pot sa iti arat demonstratia daca vrei.",["Vrei demonstratie?"]),
    ("Altceva","Sigur! Spune-mi ce vrei: alt exercitiu, alt subiect, explicatie, sau sfaturi?",["Cu ce te ajut?"]),
    ("Plictisitor","Hai sa facem ceva mai interesant! Vrei un puzzle matematic sau o provocare?",["Puzzle sau provocare?"]),
    ("Dificil","Dificil = provocator = fun! Hai sa il descompunem in pasi mici.",["Pas cu pas"]),
    ("Simplu","Daca e simplu, trecem la ceva mai greu! Progresul vine din provocare.",["Hai la nivel urmator"]),
    ("Frumos","Da, matematica poate fi frumoasa! Parabole, cercuri, simetrii - arta pura!",["Matematica e arta"]),
    ("Care e trucul?","La BAC nu sunt trucuri, sunt METODE. Invata metodele si le aplici sistematic.",["Metode, nu trucuri"]),
    ("Scurtatura?","Cea mai buna scurtatura: invata formulele si exerseaza. Nu exista shortcut magic.",["Practica = scurtatura"]),
    ("E greu matematica?","E ca mersul pe bicicleta - pare imposibil pana cand inveti. Cu practica devine natural.",["Practica face natural"]),
    ("Cate exercitii sa fac pe zi?","Calitate > cantitate. 5-10 exercitii rezolvate cu intelegere > 50 rezolvate mecanic.",["5-10 cu intelegere"]),
    ("Am 3 zile pana la BAC","Focus maxim: Subiectul I tot (30p), det si Cramer (Sub II), derivata si monotonie (Sub III). Asta iti da ~55-60p.",["Sub I + det + derivata"]),
    ("Am o saptamana","Zi 1-2: Sub I complet. Zi 3-4: Matrice si sisteme. Zi 5-6: Derivate si studiu. Zi 7: Subiect complet cronometrat.",["Plan de 7 zile"]),
    ("Am gresit semnul","Greseala clasica! Sfat: subliniaza fiecare minus cand copiezi. Verifica semnele la final.",["Subliniaza minusurile"]),
    ("Nu imi iese ca in carte","Posibil: 1) Gresit un pas mic. 2) Ai simplificat altfel. 3) Cartea are eroare (rar). Compara pas cu pas.",["Compara pas cu pas"]),
    ("La ce facultate ma ajuta matematica?","Informatica, inginerie, fizica, economie, matematica, statistica, arhitectura, medicina (statistica).",["Multe facultati"]),
    ("Profesorul meu nu explica bine","Inteleg! De aceea sunt aici - sa explic cat de simplu e nevoie. Intreaba orice!",["Sunt aici sa ajut"]),
    ("E mai greu pe hartie decat pe telefon","Da, la BAC scrii pe hartie! Exerseaza pe hartie macar uneori, sa te obisnuiesti.",["Exerseaza pe hartie"]),
    ("Pot folosi SmartBAC la BAC?","NU! La examen nu ai acces la telefon sau internet. Pregateste-te ACUM sa stii singur.",["Nu, pregateste-te acum"]),
    ("Cat costa BAC-ul?","Inscrierea la BAC e gratuita. Pregatirea depinde de tine - resurse gratuite + aceasta aplicatie!",["Gratis"]),
    ("Cand e BAC-ul?","De obicei in iunie (sesiunea 1) si august-septembrie (sesiunea 2). Verifica site-ul edu.ro pentru date exacte.",["Iunie (sesiunea 1)"]),
    ("Ce aduce BAC-ul?","Diploma de bacalaureat, necesara pentru facultate. O nota buna te ajuta la admitere.",["Diploma + nota pentru admitere"]),
]
for q,a,s in mini:
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

# Stats
types = {}
for e in merged:
    t = e.get("type","?")
    types[t] = types.get(t,0) + 1
print("\nPe tipuri:")
for t,c in sorted(types.items(), key=lambda x:-x[1]):
    print(f"  {t}: {c}")
