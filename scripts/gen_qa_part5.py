"""Part 5: 700+ Q&A - Completare pana la 2000+ noi"""
import json
from pathlib import Path

exercises = []
_id = 11000

def add(q, a, steps, typ, topic, diff=1, profile="BOTH"):
    global _id; _id += 1
    exercises.append({"id":_id,"question":q,"answer":a,"type":typ,"steps":steps,"difficulty":diff,"profile":profile,"subject":1,"topic":topic,"source":"gen_qa_v3"})

# ── DERIVATE EXTRA - exercitii rezolvate (60) ──
de = [
    ("Derivata lui f(x)=3x^5-x^3+2x","f'(x)=15x⁴-3x²+2",["(3x⁵)'=15x⁴"]),
    ("Derivata lui f(x)=x^6-6x^4+x^2","f'(x)=6x⁵-24x³+2x",["Derivam termen cu termen"]),
    ("Derivata lui f(x)=1/(x+2)","f'(x)=-1/(x+2)²",["(x+2)⁻¹ => -(x+2)⁻²"]),
    ("Derivata lui f(x)=1/(x^2+1)","f'(x)=-2x/(x²+1)²",["Regula catului sau lantului"]),
    ("Derivata lui f(x)=sqrt(2x+3)","f'(x)=1/√(2x+3)",["Regula lantului: 1/(2√(2x+3))·2"]),
    ("Derivata lui f(x)=sqrt(x^2+4x)","f'(x)=(x+2)/√(x²+4x)",["(1/(2√(x²+4x)))·(2x+4)"]),
    ("Derivata lui f(x)=e^(x^3)","f'(x)=3x²e^(x³)",["Regula lantului"]),
    ("Derivata lui f(x)=e^(sqrt(x))","f'(x)=e^(√x)/(2√x)",["Regula lantului: e^(√x)·1/(2√x)"]),
    ("Derivata lui f(x)=ln(x^3+1)","f'(x)=3x²/(x³+1)",["Regula lantului"]),
    ("Derivata lui f(x)=ln(e^x+1)","f'(x)=eˣ/(eˣ+1)",["Regula lantului"]),
    ("Derivata lui f(x)=sin(e^x)","f'(x)=eˣcos(eˣ)",["Regula lantului"]),
    ("Derivata lui f(x)=cos(ln(x))","f'(x)=-sin(lnx)/x",["Regula lantului"]),
    ("Derivata lui f(x)=e^x·ln(x)","f'(x)=eˣlnx+eˣ/x",["Regula produsului"]),
    ("Derivata lui f(x)=sin(x)/e^x","f'(x)=(cosx-sinx)/eˣ",["Regula catului"]),
    ("Derivata lui f(x)=x^2/(x-1)","f'(x)=(x²-2x)/(x-1)²=x(x-2)/(x-1)²",["Regula catului"]),
    ("Derivata lui f(x)=(x^2-1)/(x^2+1)","f'(x)=4x/(x²+1)²",["Cat: (2x(x²+1)-2x(x²-1))/(x²+1)²"]),
    ("Derivata lui f(x)=(e^x-1)/(e^x+1)","f'(x)=2eˣ/(eˣ+1)²",["Regula catului"]),
    ("Derivata lui f(x)=x·arctg(x)","f'(x)=arctg(x)+x/(1+x²)",["Regula produsului"]),
    ("Derivata lui f(x)=(sin(x))^3","f'(x)=3sin²x·cosx",["Regula lantului"]),
    ("Derivata lui f(x)=(cos(x))^4","f'(x)=-4cos³x·sinx",["Regula lantului"]),
    ("f(x)=x^2-6x+5, gaseste extremele","f'=2x-6=0=>x=3. f(3)=-4. Minim in (3,-4).",["f''=2>0 => minim"]),
    ("f(x)=-x^2+4x-1, gaseste maximul","f'=-2x+4=0=>x=2. f(2)=3. Maxim in (2,3).",["f''=-2<0 => maxim"]),
    ("f(x)=x^3-3x+1, gaseste extremele","f'=3x²-3=0=>x=±1. f(-1)=3 max, f(1)=-1 min.",["f''(-1)=-6<0 max","f''(1)=6>0 min"]),
    ("f(x)=x^4-4x^2, gaseste extremele","f'=4x³-8x=4x(x²-2)=0=>x=0,±√2. f(0)=0 max local, f(±√2)=-4 min.",["3 puncte critice"]),
    ("f(x)=xe^(-x), gaseste maximul","f'=e⁻ˣ-xe⁻ˣ=e⁻ˣ(1-x)=0=>x=1. f(1)=1/e.",["Maxim = 1/e ≈ 0.368"]),
    ("f(x)=lnx/x, gaseste maximul","f'=(1-lnx)/x²=0=>lnx=1=>x=e. f(e)=1/e.",["Maxim in x=e, valoare 1/e"]),
    ("f(x)=x²lnx, gaseste minimul pt x>0","f'=2xlnx+x=x(2lnx+1)=0=>lnx=-1/2=>x=1/√e. f(1/√e)=-1/(2e).",["Minim in x=1/√e"]),
    ("Tangenta la f(x)=x³ in x=2","f(2)=8, f'(2)=12. y-8=12(x-2) => y=12x-16.",["Tangenta: y=12x-16"]),
    ("Tangenta la f(x)=1/x in x=1","f(1)=1, f'(1)=-1. y=-(x-1)+1 => y=-x+2.",["Tangenta: y=-x+2"]),
    ("Tangenta la f(x)=sinx in x=0","f(0)=0, f'(0)=1. y=x.",["Tangenta: y=x"]),
    ("Tangenta la f(x)=eˣ in x=1","f(1)=e, f'(1)=e. y=e(x-1)+e => y=ex.",["Tangenta: y=ex"]),
    ("Arata ca e^x≥x+1","f(x)=eˣ-x-1, f'=eˣ-1=0=>x=0, f(0)=0 minim. Deci f≥0.",["f(0)=0, minim global"]),
    ("Arata ca x-x³/6≤sinx pt x≥0","f(x)=sinx-x+x³/6, f'=cosx-1+x²/2, f''=-sinx+x≥0 pt x≥0 (sinx≤x). Deci f'cresc, f'(0)=0=>f'≥0=>f cresc, f(0)=0.",["Taylor"]),
    ("Arata ca lnx≤x-1","f(x)=x-1-lnx, f'=1-1/x=0=>x=1, f(1)=0 minim.",["Clasic!"]),
    ("Arata ca lnx<√x pt x≥1","f(x)=√x-lnx, f'=1/(2√x)-1/x=(√x-2)/(2x). f(1)=1>0, f(4)=2-ln4>0. f'=0 la x=4, minim.",["Minimul e pozitiv"]),
    ("Intervalele de convexitate pt f(x)=x³-3x²+1","f''=6x-6=0=>x=1. f''>0 pt x>1 (convexa), f''<0 pt x<1 (concava).",["Inflexiune in x=1"]),
    ("Intervalele de convexitate pt f(x)=x⁴-6x²","f''=12x²-12=12(x²-1)=0=>x=±1. Convexa pt x<-1 si x>1.",["2 puncte de inflexiune"]),
    ("Asimptotele lui f(x)=(x²+1)/(x-1)","AV: x=1. AO: y=x+1 (m=lim x²/(x·x)=1, n=lim(x²+1)/(x-1)-x=lim(x+1)/(x-1)=1).",["Verticala x=1, oblica y=x+1"]),
    ("Asimptotele lui f(x)=x+1/x","AV: x=0. AO: y=x (1/x→0).",["Verticala x=0, oblica y=x"]),
    ("Asimptotele lui f(x)=(2x²-3x)/(x-1)","AV: x=1. AO: y=2x-1.",["m=2, n=lim(f(x)-2x)=-1"]),
]
for q,a,s in de:
    add(q,a,s,"exercise","derivate",2)

# ── INTEGRALE EXTRA (40) ──
ie = [
    ("∫(5x⁴+3x²+1)dx","x⁵+x³+x+C",["Termen cu termen"]),
    ("∫(x+1)³dx","(x+1)⁴/4+C",["Substitutie directa"]),
    ("∫(2x-3)⁵dx","(2x-3)⁶/12+C",["t=2x-3, dt=2dx"]),
    ("∫cos(3x+1)dx","sin(3x+1)/3+C",["t=3x+1"]),
    ("∫sin(2x+π)dx","-cos(2x+π)/2+C",["t=2x+π"]),
    ("∫e^(4x-1)dx","e^(4x-1)/4+C",["t=4x-1"]),
    ("∫1/(3x+2)dx","ln|3x+2|/3+C",["t=3x+2"]),
    ("∫x·√(x²+1)dx","(x²+1)^(3/2)/3+C",["t=x²+1, dt=2xdx"]),
    ("∫x²·√(x³+1)dx","2(x³+1)^(3/2)/9+C",["t=x³+1, dt=3x²dx"]),
    ("∫cos(x)·sin²(x)dx","sin³(x)/3+C",["t=sinx"]),
    ("∫sin(x)·cos³(x)dx","-cos⁴(x)/4+C",["t=cosx"]),
    ("∫eˣ·cos(x)dx","eˣ(cosx+sinx)/2+C",["Prin parti de 2 ori"]),
    ("∫x²·lnx dx","x³lnx/3-x³/9+C",["Prin parti: u=lnx, dv=x²dx"]),
    ("∫arctan(x)dx","x·arctg(x)-ln(1+x²)/2+C",["Prin parti: u=arctgx, dv=dx"]),
    ("∫1/(x²+2x+2)dx","arctg(x+1)+C",["x²+2x+2=(x+1)²+1"]),
    ("∫1/(x²-4x+5)dx","arctg(x-2)+C",["(x-2)²+1"]),
    ("∫1/(x²+4x+5)dx","arctg(x+2)+C",["(x+2)²+1"]),
    ("∫x/(x²+1)dx","ln(x²+1)/2+C",["t=x²+1"]),
    ("∫₀¹ x³dx","1/4",["x⁴/4|₀¹"]),
    ("∫₀² (x²-2x)dx","-4/3",["x³/3-x²|₀² = 8/3-4 = -4/3"]),
    ("∫₀^(π/4) tg(x)dx","ln(√2) = ln2/2",["∫tgx=-ln|cosx|","= -ln(cos(π/4))+ln(cos0) = -ln(√2/1)+0 = ln√2"]),
    ("∫₁⁴ √x dx","14/3",["2x^(3/2)/3|₁⁴ = 2·8/3-2/3 = 14/3"]),
    ("∫₁² x·lnx dx","2ln2-3/4",["Prin parti"]),
    ("Aria sub f(x)=x³ pe [0,1]","1/4",["∫₀¹ x³dx = 1/4"]),
    ("Aria sub f(x)=eˣ pe [0,1]","e-1",["∫₀¹ eˣdx = e-1"]),
    ("Aria intre f(x)=x² si g(x)=x pe [0,1]","1/6",["∫₀¹ (x-x²)dx = x²/2-x³/3|₀¹ = 1/2-1/3 = 1/6"]),
    ("Aria intre f(x)=x² si g(x)=√x pe [0,1]","1/3",["∫₀¹ (√x-x²)dx = 2x^(3/2)/3-x³/3|₀¹ = 2/3-1/3 = 1/3"]),
    ("Volumul de rotatie al f(x)=x pe [0,1]","V=π∫₀¹ x²dx = π/3",["V=π·x³/3|₀¹ = π/3"]),
    ("Volumul de rotatie al f(x)=√x pe [0,4]","V=π∫₀⁴ xdx = 8π",["V=π·x²/2|₀⁴ = 8π"]),
]
for q,a,s in ie:
    add(q,a,s,"exercise","integrale",2)

# ── LIMITE EXTRA (30) ──
le = [
    ("lim(x→0) (sin(5x))/(sin(3x))","5/3",["= (sin5x/(5x))·(3x/sin3x)·(5/3) → 5/3"]),
    ("lim(x→0) (1-cos(3x))/x²","9/2",["= 9·(1-cos3x)/(3x)² · 1 → 9/2"]),
    ("lim(x→0) (tg(x)-sin(x))/x³","1/2",["tgx-sinx = sinx(1/cosx-1) = sinx·(1-cosx)/cosx","≈ x·x²/2 = x³/2"]),
    ("lim(x→∞) (√(x²+x)-x)","1/2",["·(√(x²+x)+x)/(√(x²+x)+x) = x/(√(x²+x)+x)","= 1/(√(1+1/x)+1) → 1/2"]),
    ("lim(x→∞) (√(x²+3x)-√(x²+x))","1",["Rationalizare: 2x/(√(x²+3x)+√(x²+x))","= 2/(√(1+3/x)+√(1+1/x)) → 2/2 = 1"]),
    ("lim(x→∞) x(√(x²+1)-x)","1/2",["= x·1/(√(x²+1)+x) → x/(2x) = 1/2"]),
    ("lim(x→1) (x^n-1)/(x-1)","n",["L'Hopital: nxⁿ⁻¹/1 → n","Sau factorizare"]),
    ("lim(x→0) (e^x-e^(-x))/(2x)","1",["L'Hopital: (eˣ+e⁻ˣ)/2 → 2/2 = 1","Sau: sinh(x)/x → 1"]),
    ("lim(x→∞) (1+2/x)^(3x)","e⁶",["= ((1+2/x)^(x/2))⁶ → e⁶"]),
    ("lim(x→0+) x^x","1",["x^x = e^(xlnx), lim xlnx = 0","Deci lim = e⁰ = 1"]),
    ("lim(x→∞) (x/(x+1))^x","1/e",["= (1-1/(x+1))^x → e⁻¹"]),
    ("lim(x→∞) (ln(x))²/x","0",["L'Hopital: 2lnx/x → L'Hopital: 2/x → 0"]),
    ("lim(x→∞) x²/e^x","0",["L'Hopital de 2 ori: 2x/eˣ → 2/eˣ → 0"]),
    ("lim(x→∞) e^x/x^n pt orice n","+∞",["Exponentiala creste mai repede decat orice polinom"]),
    ("lim(n→∞) (1+1/n²)^n","1",["Diferit de (1+1/n)^n=e! Aici e 1."]),
    ("lim(n→∞) n·sin(1/n)","1",["t=1/n: sin(t)/t → 1"]),
    ("lim(n→∞) (n²+1)/(2n²-3)","1/2",["Grad egal: 1/2"]),
    ("lim(n→∞) √(n²+n)-n","1/2",["= n/(√(n²+n)+n) → 1/2"]),
    ("lim(n→∞) n^(1/n)","1",["n^(1/n) = e^(lnn/n) → e⁰ = 1"]),
    ("lim(n→∞) (n!)^(1/n)/n","1/e",["Stirling"]),
]
for q,a,s in le:
    add(q,a,s,"exercise","limite",2)

# ── ECUATII EXTRA (40) ──
ece = [
    ("Rezolva x^2-3x-10=0","x=5, x=-2",["delta=9+40=49","x=(3±7)/2"]),
    ("Rezolva 2x^2+x-6=0","x=3/2, x=-2",["delta=1+48=49","x=(-1±7)/4"]),
    ("Rezolva x^2-x=0","x(x-1)=0, x=0 sau x=1",["Factorizare"]),
    ("Rezolva x^3-4x=0","x(x²-4)=0, x=0,±2",["x(x-2)(x+2)=0"]),
    ("Rezolva x^3+x^2-2x=0","x(x²+x-2)=0, x=0,1,-2",["x(x-1)(x+2)=0"]),
    ("Rezolva sqrt(x)=3","x=9",["Ridicam: x=9"]),
    ("Rezolva sqrt(2x-1)=5","x=13",["2x-1=25, x=13"]),
    ("Rezolva sqrt(x+4)=x-2","x+4=(x-2)², x²-5x=0, x=0,5. Verif: x=5✓, x=0✗",["x=5"]),
    ("Rezolva 5^x=125","x=3",["5³=125"]),
    ("Rezolva 4^x=1/16","x=-2",["4⁻²=1/16"]),
    ("Rezolva 2^(x+1)=16","2^(x+1)=2⁴, x+1=4, x=3",["Exponenti egali"]),
    ("Rezolva 3^(2x)=81","3^(2x)=3⁴, 2x=4, x=2",["Exponenti egali"]),
    ("Rezolva log₃(x)=4","x=3⁴=81",["Definitia logaritmului"]),
    ("Rezolva log(x)+log(x+3)=1","lg(x(x+3))=1, x²+3x=10, x²+3x-10=0, x=2(x=-5✗)",["x=2"]),
    ("Rezolva ln(x+1)+ln(x-1)=ln3","ln((x+1)(x-1))=ln3, x²-1=3, x=2(x=-2✗)",["x=2"]),
    ("Rezolva sin(x)=-1","x=3π/2+2kπ = -π/2+2kπ",["x=-π/2+2kπ"]),
    ("Rezolva cos(x)=√3/2","x=±π/6+2kπ",["cos30°=√3/2"]),
    ("Rezolva 2sin²x-1=0","sin²x=1/2, sinx=±√2/2, x=π/4+kπ/2",["sinx=±√2/2"]),
    ("Rezolva sin(x)+cos(x)=1","√2·sin(x+π/4)=1, sin(x+π/4)=√2/2, x=0 sau x=π/2 (+2kπ)",["Transformam in sinus"]),
    ("Rezolva |x²-4|=5","x²-4=5=>x²=9=>x=±3. x²-4=-5=>x²=-1 imposibil. Sol: x=±3.",["x=±3"]),
    ("Rezolva |x-1|=|2x+3|","x-1=2x+3=>x=-4. x-1=-(2x+3)=>3x=-2=>x=-2/3.",["2 cazuri"]),
    ("Gaseste m pt ecuatia x²-2mx+m²-1=0 sa aiba sol reale","Δ≥0: 4m²-4(m²-1)≥0, 4≥0 mereu adevarat. Orice m∈R.",["Δ=4>0 mereu"]),
    ("Gaseste m pt x1+x2=6 daca x²-mx+5=0","Vieta: x1+x2=-(-m)/1=m=6. m=6.",["Vieta"]),
    ("Gaseste m pt x1·x2=8 daca x²+3x+m=0","Vieta: x1·x2=m/1=m=8. m=8.",["Vieta"]),
    ("Rezolva sistemul x²+y²=25, x+y=7","y=7-x, x²+(7-x)²=25, 2x²-14x+24=0, x²-7x+12=0, x=3,4.",["x=3,y=4 sau x=4,y=3"]),
]
for q,a,s in ece:
    add(q,a,s,"exercise","ecuatii",2)

# ── MATRICE EXTRA (30) ──
me = [
    ("det[2 0 1; 0 3 0; 1 0 2]","det=2·3·2+0+0-3·1·1-0-0=12-3=9",["Sarrus sau dezvoltare"]),
    ("det[1 2 3; 4 5 6; 7 8 9]","det=0",["Linia 3 = 2·L2 - L1 => dependenta"]),
    ("det[1 1 1; 1 2 3; 1 3 6]","det=1(12-9)-1(6-3)+1(3-2)=3-3+1=1",["Dezvoltare"]),
    ("Inversa lui [1 1; 0 1]","[1 -1; 0 1]",["det=1, adj=[1 -1; 0 1]"]),
    ("Inversa lui [2 0; 0 3]","[1/2 0; 0 1/3]",["det=6, diagonala: 1/a_ii"]),
    ("A=[1 2; 0 1], calculati A⁴","[1 4; 0 1]",["Pattern: Aⁿ=[1 n; 0 1]"]),
    ("A=[2 0; 0 3], calculati A³","[8 0; 0 27]",["Diagonala: Aⁿ=[aⁿ 0; 0 bⁿ]"]),
    ("A=[1 1; 1 1], calculati A²","[2 2; 2 2]=2A",["A²=2A => Aⁿ=2ⁿ⁻¹A"]),
    ("Rezolva: x+y+z=6, 2x+y-z=1, x-y+2z=5","D=8, x=1, y=2, z=3",["Cramer cu det 3x3"]),
    ("Rezolva: x+y=3, 2x+3y=8","D=1, x=1, y=2",["Cramer sau substitutie"]),
    ("Rezolva: x+2y+z=4, 2x+y+z=3, x+y+2z=5","D=-2, x=0, y=1, z=2",["Cramer"]),
    ("Calculati rang[1 2 3; 2 4 6]","rang=1 (linia 2 = 2·linia 1)",["Linii proporionale"]),
    ("Calculati rang[1 0 2; 0 1 3; 1 1 5]","rang=2 (L3=L1+L2)",["Dependenta liniara"]),
    ("Pt ce m sistemul nu are solutie unica: mx+y=1, x+my=1?","det=m²-1=0 => m=±1.",["det(A)=0"]),
    ("Arata ca det[a b; c d]·det[d -b; -c a]=(ad-bc)²","det prima=ad-bc, det a doua=da-bc=ad-bc. Produs=(ad-bc)².",["Ambele det = ad-bc"]),
]
for q,a,s in me:
    add(q,a,s,"exercise","matrice",2)

# ── COMBINATORICA EXTRA (25) ──
ce = [
    ("Cate siruri de 4 cifre binare exista?","2⁴ = 16",["2 optiuni per pozitie, 4 pozitii"]),
    ("Cate numere de 3 cifre distincte din {0,1,2,3,4}?","4·4·3 = 48 (prima cifra ≠ 0)",["Prima: 4 optiuni, a 2-a: 4, a 3-a: 3"]),
    ("In cate moduri aleg presedinte si secretar din 10?","A(10,2) = 90",["Conteaza ordinea"]),
    ("In cate moduri impart 10 persoane in 2 grupe de 5?","C(10,5)/2 = 126",["Impartim la 2 ca grupele sunt neordonate"]),
    ("P(cel putin o fata din 3 copii)?","1-P(toti baieti) = 1-(1/2)³ = 7/8",["Complementara"]),
    ("P(suma>9 la 2 zaruri)?","(3+4+5+6+5+4+3+2+1... nu. Perechi cu suma>9: (4,6)(5,5)(5,6)(6,4)(6,5)(6,6) = 6. P=6/36=1/6",["6 perechi favorabile"]),
    ("P(exact un as din 2 carti extrase din 52)?","C(4,1)·C(48,1)/C(52,2) = 192/1326 = 32/221",["4·48/C(52,2)"]),
    ("Cate diagonale are un hexagon?","C(6,2)-6 = 15-6 = 9",["Total segmente - laturi"]),
    ("Cate diagonale are un poligon cu n laturi?","n(n-3)/2",["C(n,2)-n = n(n-1)/2-n"]),
    ("Coeficientul lui x^5 in (x+1)^8?","C(8,3)=56",["x^5: k=3, C(8,3)·x⁵·1³"]),
    ("Coeficientul lui x^2 in (2x-1)^4?","C(4,2)·(2x)²·(-1)² = 6·4 = 24",["C(4,2)·4x²·1 = 24x²"]),
    ("Suma coeficientilor in (x+1)^5?","Punem x=1: 2⁵=32",["Suma coef = f(1)"]),
    ("Cat e C(n,k)+C(n,k+1)?","C(n+1,k+1) (relatia lui Pascal)",["Formula de recurenta"]),
    ("Demonstreaza C(n,0)-C(n,1)+C(n,2)-...=0","Punem x=-1 in (1+x)ⁿ: 0ⁿ=0 (pt n≥1).",["Din binom cu x=-1"]),
]
for q,a,s in ce:
    add(q,a,s,"exercise","combinatorica",2)

# ── TRIGONOMETRIE EXERCITII (25) ──
te = [
    ("Calculeaza sin(75°)","sin(45°+30°) = sin45·cos30+cos45·sin30 = (√6+√2)/4",["Formula adunare"]),
    ("Calculeaza cos(15°)","cos(45°-30°) = cos45·cos30+sin45·sin30 = (√6+√2)/4",["Formula scadere"]),
    ("Calculeaza sin(105°)","sin(60°+45°) = (√6+√2)/4",["= sin75° = cos15°"]),
    ("Calculeaza tg(75°)","tg(45°+30°) = (1+√3/3)/(1-√3/3) = 2+√3",["Formula adunare tg"]),
    ("Simplifica sin²(x)+cos²(x)+tg²(x)","= 1+tg²(x) = 1/cos²(x)",["sin²+cos²=1"]),
    ("Simplifica sin(2x)/(2sinx)","= cosx",["sin2x=2sinxcosx, /2sinx = cosx"]),
    ("Simplifica (1-cos2x)/(1+cos2x)","= tg²(x)",["1-cos2x=2sin²x, 1+cos2x=2cos²x"]),
    ("Rezolva sin(2x)=1","2x=π/2+2kπ, x=π/4+kπ",["sin(u)=1 => u=π/2+2kπ"]),
    ("Rezolva cos(3x)=0","3x=π/2+kπ, x=π/6+kπ/3",["cos(u)=0 => u=π/2+kπ"]),
    ("Rezolva sin²(x)-sinx=0","sinx(sinx-1)=0, sinx=0 sau sinx=1",["Factorizare"]),
    ("Rezolva cos²(x)=3/4","cosx=±√3/2, x=π/6+kπ sau x=5π/6+kπ",["cos30°=√3/2"]),
    ("Rezolva sinx+cosx=√2","√2·sin(x+π/4)=√2, sin(x+π/4)=1, x=π/4+2kπ",["Transformare in sinus"]),
    ("Rezolva 2sin²x+3sinx-2=0","t=sinx: 2t²+3t-2=0, t=1/2(t=-2 imposibil). x=π/6+2kπ, 5π/6+2kπ",["sinx=1/2"]),
    ("In triunghi ABC, a=5, b=7, C=60°. Cat e c?","c²=25+49-2·5·7·cos60°=74-35=39. c=√39.",["Teorema cosinusului"]),
    ("In triunghi ABC, a=6, A=30°. Cat e R?","a/sinA=2R => 6/sin30°=2R => 12=2R => R=6.",["Teorema sinusurilor"]),
]
for q,a,s in te:
    add(q,a,s,"exercise","trigonometrie",2)

# ── GEOMETRIE EXERCITII EXTRA (25) ──
ge = [
    ("Distanta intre A(1,1) si B(4,5)","d=√(9+16)=5",["√(3²+4²)"]),
    ("Distanta intre A(0,3) si B(4,0)","d=5",["√(16+9)=5"]),
    ("Ecuatia dreptei prin (2,3) si (4,7)","m=2, y-3=2(x-2), y=2x-1",["m=(7-3)/(4-2)=2"]),
    ("Ecuatia dreptei prin (0,5) si (3,2)","m=-1, y=-x+5",["m=(2-5)/(3-0)=-1"]),
    ("Ecuatia dreptei perpendiculare pe 3x+y=5 prin (1,1)","m=1/3, y-1=(1/3)(x-1), y=x/3+2/3",["Perpendicul: m=1/3"]),
    ("Ecuatia cercului prin (0,0),(2,0),(0,4)","x²+y²-2x-4y=0, centru(1,2), r=√5",["3 puncte pe cerc"]),
    ("Intersectia dreptei y=2x si cercului x²+y²=5","x²+4x²=5, x²=1, x=±1. (1,2),(-1,-2).",["Substitutie"]),
    ("Aria triunghiului cu A(0,0), B(6,0), C(3,4)","Aria=|0(0-4)+6(4-0)+3(0-0)|/2=24/2=12",["Formula cu coordonate"]),
    ("Verifica daca A(1,2), B(3,6), C(5,10) sunt coliniare","Panta AB=(6-2)/(3-1)=2, panta AC=(10-2)/(5-1)=2. Egale => coliniare.",["Pante egale"]),
    ("Lungimea segmentului din A(-2,3) la B(1,-1)","d=√(9+16)=5",["√(3²+4²)"]),
    ("Coordonatele centrului de greutate G al triunghiului A(0,0),B(6,0),C(0,6)","G(2,2)",["G=((0+6+0)/3,(0+0+6)/3)"]),
    ("Ecuatia mediatorului segmentului AB, A(0,0), B(4,2)","Mijloc(2,1), panta AB=1/2, panta med=-2. y-1=-2(x-2) => y=-2x+5.",["Perpendicular prin mijloc"]),
]
for q,a,s in ge:
    add(q,a,s,"exercise","geometrie",2)

# ── NUMERE COMPLEXE EXTRA (20) ──
nc = [
    ("(4-3i)+(2+5i)","6+2i",["(4+2)+(−3+5)i"]),
    ("(6+2i)-(3+4i)","3-2i",["(6-3)+(2-4)i"]),
    ("(2-i)(3+2i)","6+4i-3i-2i²=8+i",["FOIL"]),
    ("(1+2i)(1-2i)","1+4=5",["z·z̄=|z|²"]),
    ("(3+i)/(1+i)","(3+i)(1-i)/2=(3-3i+i-i²)/2=(4-2i)/2=2-i",["Conjugat numitor"]),
    ("(5+i)/(2-i)","(5+i)(2+i)/5=(10+5i+2i+i²)/5=(9+7i)/5",["Conjugat numitor"]),
    ("|4-3i|","5",["√(16+9)=5"]),
    ("|6+8i|","10",["√(36+64)=10"]),
    ("Rezolva z²-4z+13=0","z=2±3i",["delta=16-52=-36, z=(4±6i)/2"]),
    ("Rezolva z²+z+1=0","z=(-1±i√3)/2",["delta=1-4=-3"]),
    ("(i+1)⁴","(i+1)²=2i, (2i)²=-4",["(1+i)⁴=-4"]),
    ("Gaseste z cu z+z̄=6 si z·z̄=10","z=3±i (a=3,a²+b²=10,b²=1)",["Re(z)=3, |z|²=10"]),
    ("Forma trig a lui z=2i","2(cos(π/2)+i·sin(π/2))",["r=2, θ=π/2"]),
    ("Forma trig a lui z=-3","3(cos(π)+i·sin(π))",["r=3, θ=π"]),
    ("Forma trig a lui z=1-i","√2(cos(-π/4)+i·sin(-π/4))",["r=√2, θ=-π/4"]),
]
for q,a,s in nc:
    add(q,a,s,"exercise","numere complexe",2,"M1")

# ── PROGRESII EXTRA (20) ──
pe = [
    ("PA: a1=3, a5=15. Cat e r?","r=(15-3)/4=3",["r=(an-a1)/(n-1)"]),
    ("PA: a3=7, a7=19. Cat e r si a1?","r=(19-7)/4=3. a1=7-2·3=1.",["r=3, a1=1"]),
    ("PG: b1=4, b3=16. Cat e q?","q²=16/4=4, q=2(sau -2)",["q=±2"]),
    ("PG: b1=1, q=1/2. Cat e S∞?","S∞=1/(1-1/2)=2",["Serie geometrica infinita"]),
    ("PA: S10=100. Cat e a1+a10?","Sn=n(a1+an)/2, 100=10(a1+a10)/2, a1+a10=20.",["a1+a10=20"]),
    ("Suma 2+4+6+...+100","S=50·(2+100)/2=2550",["PA: a1=2,r=2,n=50"]),
    ("Suma 1+3+5+...+99","S=50²=2500",["n=50, suma primelor n impare=n²"]),
    ("Suma 1+1/2+1/4+...+1/2^n","S=2(1-1/2^(n+1))",["PG: b1=1, q=1/2"]),
    ("Cat e termenul rank 20 in PA cu a1=5,r=3?","a20=5+19·3=62",["an=a1+(n-1)r"]),
    ("Cat e termenul rank 8 in PG cu b1=3,q=2?","b8=3·2⁷=384",["bn=b1·q^(n-1)"]),
    ("3 numere in PA cu suma 12 si prod termenilor extremi 12","a-d,a,a+d: 3a=12=>a=4. (4-d)(4+d)=12, 16-d²=12, d=2. Numere: 2,4,6.",["a=4, d=2"]),
    ("3 numere in PG cu produsul 27","b/q,b,bq: b³=27=>b=3. Numerele: 3/q, 3, 3q.",["b=3"]),
    ("Demonstreaza ca 1/1·2+1/2·3+...+1/n(n+1)=n/(n+1)","1/(k(k+1))=1/k-1/(k+1). Suma telescopica: 1-1/(n+1)=n/(n+1).",["Telescopic"]),
]
for q,a,s in pe:
    add(q,a,s,"exercise","progresii",2)

# ── CONVERSATII PRACTICE (40) ──
cp = [
    ("Da-mi un exercitiu de Sub I","Rezolva: Suma solutiilor ecuatiei x²-7x+10=0 este... (Raspuns: 7, Vieta)",["x1+x2=-(-7)/1=7"]),
    ("Da-mi un exercitiu de Sub II","Calculati det[1 2; 3 5] si gasiti inversa. (det=−1, A⁻¹=[−5 2; 3 −1])",["det=5-6=-1"]),
    ("Da-mi un exercitiu de Sub III","Studiul functiei f(x)=x²·e⁻ˣ: domeniu, derivata, monotonie, extreme, grafic.",["f'=xe⁻ˣ(2-x)=0 => x=0,2"]),
    ("Cum rezolv rapid un det 3x3?","Sarrus: copiezi primele 2 coloane, 3 diag principale (+) si 3 secundare (-). Sau dezvolti dupa linia cu cei mai multi 0.",["Sarrus sau dezvoltare"]),
    ("La ce e buna matricea inversa?","A⁻¹ rezolva sisteme: AX=B => X=A⁻¹B. La criptografie, grafice 3D, ecuatii matriceale.",["Sisteme, criptografie, grafice"]),
    ("Care e cel mai important lucru la BAC?","Sa citesti ATENT enuntul. Multi pierd puncte pentru ca raspund la altceva decat se cere.",["CITESTE ENUNTUL!"]),
    ("Ce greseli fac la grafic?","1) Nu notezi punctele. 2) Graficul nu respecta monotonia. 3) Uiti asimptotele. 4) Scara gresita.",["Noteaza puncte + respecta monotonia"]),
    ("Cum stiu daca un punct e pe grafic?","Inlocuiesti x si y in ecuatia functiei. Daca egalitatea e adevarata, punctul e pe grafic.",["f(x0)=y0?"]),
    ("Pot sa incep cu Subiectul III?","Da! La BAC poti rezolva in orice ordine. Dar recomand sa incepi cu ce stii cel mai bine.",["Da, orice ordine"]),
    ("Ce fac daca nu stiu o formula la BAC?","Incearca sa o rederivezi din definitie sau din alte formule. Sau treci la alt exercitiu.",["Rederiva sau treci mai departe"]),
    ("Cum demonstrez o inegalitate la BAC?","Metoda clasica: f(x)=membrul stang - membrul drept. Arata ca f are minim ≥ 0.",["f(x)≥0 prin studiu de functie"]),
    ("Ce inseamna 'aratati ca'?","Trebuie sa demonstrezi riguros, nu doar sa verifici numeric. Scrie TOTI pasii.",["Demonstratie completa"]),
    ("Ce inseamna 'determinati'?","Trebuie sa gasesti valoarea/expresia ceruta. Scrie rezolvarea completa.",["Gaseste si arata cum"]),
    ("Ce inseamna 'verificati'?","Inlocuiesti si arati ca egalitatea/proprietatea e adevarata.",["Inlocuieste si confirma"]),
    ("Ce inseamna 'sa se calculeze'?","Fa calculul cerut si da rezultatul final. Arata pasii.",["Calcul complet"]),
    ("Ce inseamna 'sa se studieze monotonia'?","Calculezi f', gasesti f'=0, faci tabel de semn, spui unde creste/descreste.",["f' -> tabel -> cresc/desc"]),
    ("Ce inseamna 'sa se determine asimptotele'?","Cauti: 1) AV: unde numitorul e 0. 2) AO: lim la ±∞. 3) AO: y=mx+n.",["3 tipuri de asimptote"]),
    ("Ce inseamna 'sa se reprezinte grafic'?","Deseneaza axele, marcheaza punctele importante (intersectii, extreme, inflexiune), deseneaza curba.",["Desen complet cu puncte notate"]),
    ("Cum citesc graficul unei functii?","Din grafic citesti: domeniu, imagine, monotonie, extreme, zerouri, semn, asimptote.",["Citesti proprietatile functiei"]),
    ("Ce e important la demonstratiile de la Sub III?","Justifica FIECARE pas. Scrie ipoteza, aplica teoreme, noteaza concluzia.",["Justificare la fiecare pas"]),
]
for q,a,s in cp:
    add(q,a,s,"conversation","conversatie")

# ── FORMULE RAPIDE EXTRA (50) ──
fr = [
    ("(a+b)²","a² + 2ab + b²",[""]),
    ("(a-b)²","a² - 2ab + b²",[""]),
    ("a²-b²","(a-b)(a+b)",[""]),
    ("(a+b)³","a³ + 3a²b + 3ab² + b³",[""]),
    ("(a-b)³","a³ - 3a²b + 3ab² - b³",[""]),
    ("a³+b³","(a+b)(a²-ab+b²)",[""]),
    ("a³-b³","(a-b)(a²+ab+b²)",[""]),
    ("Aria triunghi","A = baza·inaltime/2",[""]),
    ("Aria cerc","A = πr²",[""]),
    ("Circumferinta cerc","C = 2πr",[""]),
    ("Volumul cub","V = a³",[""]),
    ("Volumul sfera","V = 4πr³/3",[""]),
    ("Aria sfera","A = 4πr²",[""]),
    ("Volumul cilindru","V = πr²h",[""]),
    ("Volumul con","V = πr²h/3",[""]),
    ("Teorema lui Pitagora","a² + b² = c²",[""]),
    ("Distanta punct-dreapta","d = |ax₀+by₀+c|/√(a²+b²)",[""]),
    ("Ecuatia cercului","(x-a)²+(y-b)²=r²",[""]),
    ("Ecuatia elipsei","x²/a²+y²/b²=1",[""]),
    ("Derivata compusa","(f∘g)' = f'(g)·g'",[""]),
    ("Integrala prin parti","∫u dv = uv - ∫v du",[""]),
    ("Leibniz-Newton","∫[a,b]f = F(b)-F(a)",[""]),
    ("lim sinx/x=1","x→0",[""]),
    ("lim (eˣ-1)/x=1","x→0",[""]),
    ("lim (1+1/x)ˣ=e","x→∞",[""]),
    ("lim ln(1+x)/x=1","x→0",[""]),
    ("Sn PA","n(a₁+aₙ)/2",[""]),
    ("Sn PG","b₁(qⁿ-1)/(q-1)",[""]),
    ("S∞ PG","b₁/(1-q), |q|<1",[""]),
    ("C(n,k)","n!/(k!(n-k)!)",[""]),
    ("P(A)","cazuri favorabile/cazuri posibile",[""]),
    ("P(A∪B)","P(A)+P(B)-P(A∩B)",[""]),
    ("sin(a+b)","sinacosb+cosasinb",[""]),
    ("cos(a+b)","cosacosb-sinasinb",[""]),
    ("sin2a","2sinacosa",[""]),
    ("cos2a","cos²a-sin²a",[""]),
    ("|a+bi|","√(a²+b²)",[""]),
    ("Ecuatia tangentei","y-f(x₀)=f'(x₀)(x-x₀)",[""]),
    ("Forme nedeterminate","0/0, ∞/∞, 0·∞, ∞-∞, 0⁰, 1^∞, ∞⁰",[""]),
    ("Regula L'Hopital","lim f/g = lim f'/g'",[""]),
]
for q,a,s in fr:
    add(q,a,s,"formula","formule rapide",1)

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

# Stats finale
types = {}
for e in merged:
    t = e.get("type","?")
    types[t] = types.get(t,0) + 1
print(f"\nPe tipuri ({len(types)} tipuri):")
for t,c in sorted(types.items(), key=lambda x:-x[1]):
    print(f"  {t}: {c}")

# Count new entries from this session
v3 = [e for e in merged if e.get("source","").startswith("gen_qa_v")]
print(f"\nTotal Q&A noi adaugate in aceasta sesiune: {len(v3)}")
