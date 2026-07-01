"""Part 3: 500+ Q&A - Exercitii rezolvate, variante BAC, erori, conversatii extra"""
import json
from pathlib import Path

exercises = []
_id = 9000

def add(q, a, steps, typ, topic, diff=1, profile="BOTH"):
    global _id; _id += 1
    exercises.append({"id":_id,"question":q,"answer":a,"type":typ,"steps":steps,"difficulty":diff,"profile":profile,"subject":1,"topic":topic,"source":"gen_qa_v3"})

# ── EXERCITII REZOLVATE - DERIVATE (40) ──
ex_deriv = [
    ("Calculeaza derivata lui f(x)=2x^3-5x+1","f'(x) = 6x² - 5",["(2x³)'=6x²","(-5x)'=-5","(1)'=0"]),
    ("Calculeaza derivata lui f(x)=x^4-2x^2+x","f'(x) = 4x³ - 4x + 1",["(x⁴)'=4x³","(-2x²)'=-4x","(x)'=1"]),
    ("Calculeaza f'(1) daca f(x)=x^3-3x+2","f'(x)=3x²-3, f'(1)=3-3=0",["f'(x)=3x²-3","f'(1)=3·1-3=0"]),
    ("Calculeaza f'(0) daca f(x)=e^x+x^2","f'(x)=e^x+2x, f'(0)=1+0=1",["f'(x)=eˣ+2x","f'(0)=e⁰+0=1"]),
    ("Calculeaza f'(1) daca f(x)=ln(x)+x","f'(x)=1/x+1, f'(1)=1+1=2",["f'(x)=1/x+1","f'(1)=1+1=2"]),
    ("Gaseste punctele critice ale lui f(x)=x^3-3x","f'(x)=3x²-3=0 => x=±1",["3(x²-1)=0","x²=1 => x=1 sau x=-1"]),
    ("Gaseste minimul lui f(x)=x^2-4x+5","f'(x)=2x-4=0 => x=2, f(2)=1. Minimul e 1.",["f'(x)=2x-4=0 => x=2","f''=2>0 => minim","f(2)=4-8+5=1"]),
    ("Gaseste maximul lui f(x)=-x^2+6x-8","f'(x)=-2x+6=0 => x=3, f(3)=1. Maximul e 1.",["f'=-2x+6=0 => x=3","f''=-2<0 => maxim","f(3)=-9+18-8=1"]),
    ("Ecuatia tangentei la f(x)=x^2 in x=1","f(1)=1, f'(1)=2. Tangenta: y=2x-1.",["f(1)=1","f'(x)=2x, f'(1)=2","y-1=2(x-1) => y=2x-1"]),
    ("Ecuatia tangentei la f(x)=e^x in x=0","f(0)=1, f'(0)=1. Tangenta: y=x+1.",["f(0)=e⁰=1","f'(0)=e⁰=1","y-1=1(x-0) => y=x+1"]),
    ("Studiaza monotonia lui f(x)=x^3-12x","f'(x)=3x²-12=3(x²-4). f'=0 => x=±2. Cresc pe (-∞,-2)∪(2,+∞), desc pe (-2,2).",["f'(x)=3(x-2)(x+2)","f'>0 pt x<-2 sau x>2","f'<0 pt -2<x<2"]),
    ("Studiaza monotonia lui f(x)=x^4-4x^2","f'=4x³-8x=4x(x²-2). f'=0: x=0,±√2. Desc (-∞,-√2)∪(0,√2), cresc (-√2,0)∪(√2,+∞).",["f'=4x(x-√2)(x+√2)","Tabel de semn cu 3 puncte critice"]),
    ("Arata ca f(x)=e^x-x-1≥0","f'(x)=eˣ-1=0 => x=0. f''=eˣ>0 => minim. f(0)=1-0-1=0. Deci f(x)≥f(0)=0.",["f'(0)=0, f''(0)>0 => minim","f(0)=0 => f(x)≥0"]),
    ("Arata ca ln(x)≤x-1 pentru x>0","f(x)=x-1-lnx, f'(x)=1-1/x=0 => x=1. f''=1/x²>0 => minim. f(1)=0. Deci f(x)≥0.",["Minimul e in x=1","f(1)=1-1-0=0"]),
    ("Calculeaza derivata lui f(x)=(x^2+1)·e^x","f'(x)=(2x)eˣ+(x²+1)eˣ = eˣ(x²+2x+1) = eˣ(x+1)²",["Regula produsului","f' = eˣ(x+1)²"]),
    ("Calculeaza derivata lui f(x)=x·ln(x)-x","f'(x)=lnx+x·(1/x)-1 = lnx+1-1 = lnx",["f'=lnx+1-1=lnx"]),
    ("Calculeaza derivata lui f(x)=sin(x)·cos(x)","f'(x)=cos²x-sin²x = cos(2x)",["Regula produsului","Sau: f(x)=sin(2x)/2, f'=cos(2x)"]),
    ("Derivata lui f(x)=(x-1)/(x+1)","f'(x)=((x+1)-(x-1))/(x+1)² = 2/(x+1)²",["Regula catului"]),
    ("Derivata lui f(x)=x·sqrt(x)","f(x)=x^(3/2), f'(x)=(3/2)x^(1/2) = 3√x/2",["x·√x = x^(3/2)"]),
    ("Derivata lui f(x)=(ln(x))^2","f'(x) = 2·ln(x)·(1/x) = 2ln(x)/x",["Regula lantului: 2lnx · (lnx)'"]),
]
for q,a,s in ex_deriv:
    add(q,a,s,"exercise","derivate",2)

# ── EXERCITII REZOLVATE - INTEGRALE (30) ──
ex_int = [
    ("Calculeaza ∫(3x^2+2x-1)dx","x³+x²-x+C",["∫3x²=x³, ∫2x=x², ∫(-1)=-x"]),
    ("Calculeaza ∫(x^3-x)dx","x⁴/4-x²/2+C",["∫x³=x⁴/4, ∫x=x²/2"]),
    ("Calculeaza ∫(2e^x+3/x)dx","2eˣ+3ln|x|+C",["∫2eˣ=2eˣ, ∫3/x=3ln|x|"]),
    ("Calculeaza ∫(sin(x)+cos(x))dx","-cos(x)+sin(x)+C",["∫sinx=-cosx, ∫cosx=sinx"]),
    ("Calculeaza ∫₀¹ (3x²+1)dx","2",["F(x)=x³+x","F(1)-F(0)=1+1-0=2"]),
    ("Calculeaza ∫₀¹ x³dx","1/4",["F(x)=x⁴/4","F(1)-F(0)=1/4"]),
    ("Calculeaza ∫₁² (2x+1)dx","4",["F(x)=x²+x","F(2)-F(1)=(4+2)-(1+1)=6-2=4"]),
    ("Calculeaza ∫₀^π sin(x)dx","2",["F(x)=-cosx","F(π)-F(0)=1-(-1)=2"]),
    ("Calculeaza ∫₀¹ e^x dx","e-1",["F(x)=eˣ","F(1)-F(0)=e-1"]),
    ("Calculeaza ∫₁^e (1/x)dx","1",["F(x)=lnx","F(e)-F(1)=1-0=1"]),
    ("Calculeaza aria de sub f(x)=x² pe [0,2]","Aria = ∫₀² x²dx = x³/3|₀² = 8/3",["F(x)=x³/3","A = 8/3-0 = 8/3"]),
    ("Calculeaza aria de sub f(x)=sqrt(x) pe [0,4]","Aria = ∫₀⁴ √x dx = 2x√x/3|₀⁴ = 16/3",["F(x)=2x^(3/2)/3","A = 2·8/3 = 16/3"]),
    ("Calculeaza ∫x·e^(2x)dx","Prin parti: u=x, dv=e^(2x)dx. = (x/2)e^(2x) - e^(2x)/4 + C",["u=x, du=dx","v=e^(2x)/2","= xe^(2x)/2 - ∫e^(2x)/2 dx"]),
    ("Calculeaza ∫(x+1)^5 dx","(x+1)⁶/6 + C",["Substitutie: t=x+1"]),
    ("Calculeaza ∫2x/(x²+1)dx","ln(x²+1) + C",["Substitutie: t=x²+1, dt=2xdx"]),
    ("Calculeaza ∫cos(x)·e^(sin(x))dx","e^(sin(x)) + C",["Substitutie: t=sinx, dt=cosxdx"]),
    ("Calculeaza ∫1/(x²+4)dx","(1/2)arctg(x/2) + C",["∫1/(x²+a²)dx = (1/a)arctg(x/a)+C"]),
    ("Calculeaza ∫x/(x+1)dx","x - ln|x+1| + C",["x/(x+1) = 1 - 1/(x+1)","∫(1 - 1/(x+1))dx = x - ln|x+1| + C"]),
]
for q,a,s in ex_int:
    add(q,a,s,"exercise","integrale",2)

# ── EXERCITII REZOLVATE - LIMITE (30) ──
ex_lim = [
    ("Calculeaza lim(x→1) (x²-1)/(x-1)","lim = 2",["(x-1)(x+1)/(x-1) = x+1 → 2"]),
    ("Calculeaza lim(x→3) (x²-9)/(x-3)","lim = 6",["(x-3)(x+3)/(x-3) = x+3 → 6"]),
    ("Calculeaza lim(x→0) sin(3x)/x","lim = 3",["sin(3x)/x = 3·sin(3x)/(3x) → 3·1 = 3"]),
    ("Calculeaza lim(x→0) sin(5x)/sin(2x)","lim = 5/2",["= (sin5x/(5x))·(2x/sin2x)·(5x/2x) → 1·1·5/2"]),
    ("Calculeaza lim(x→0) (e^(3x)-1)/x","lim = 3",["= 3·(e^(3x)-1)/(3x) → 3·1 = 3"]),
    ("Calculeaza lim(x→∞) (2x²+3x)/(x²-1)","lim = 2",["Impartim la x²: (2+3/x)/(1-1/x²) → 2"]),
    ("Calculeaza lim(x→∞) (x+1)/(2x+3)","lim = 1/2",["Impartim la x: (1+1/x)/(2+3/x) → 1/2"]),
    ("Calculeaza lim(x→∞) (3x³-x)/(x³+2)","lim = 3",["Grad egal, raport coeficienti: 3/1 = 3"]),
    ("Calculeaza lim(x→∞) x/(x²+1)","lim = 0",["Grad numarator < grad numitor => 0"]),
    ("Calculeaza lim(x→∞) x²/(x+1)","lim = +∞",["Grad numarator > grad numitor => ∞"]),
    ("Calculeaza lim(x→0) (1+x)^(1/x)","lim = e",["Limita remarcabila fundamentala"]),
    ("Calculeaza lim(x→∞) (1+3/x)^x","lim = e³",["= ((1+3/x)^(x/3))³ → e³"]),
    ("Calculeaza lim(x→0) (e^x-1-x)/x²","lim = 1/2",["L'Hopital: (eˣ-1)/(2x)","L'Hopital: eˣ/2 → 1/2"]),
    ("Calculeaza lim(x→∞) (√(x²+x)-x)","lim = 1/2",["Rationalizare: x/(√(x²+x)+x)","= x/(x(√(1+1/x)+1)) → 1/2"]),
    ("Calculeaza lim(x→0) (1-cos(x))/x²","lim = 1/2",["Limita remarcabila"]),
    ("Calculeaza lim(x→0) tg(x)/x","lim = 1",["tg(x)/x = sinx/(x·cosx) → 1/1 = 1"]),
    ("Calculeaza lim(x→∞) ln(x)/x","lim = 0",["L'Hopital: (1/x)/1 = 1/x → 0"]),
    ("Calculeaza lim(x→∞) x/e^x","lim = 0",["L'Hopital: 1/eˣ → 0"]),
    ("Calculeaza lim(x→0+) x·ln(x)","lim = 0",["= ln(x)/(1/x), L'Hopital: (1/x)/(-1/x²) = -x → 0"]),
]
for q,a,s in ex_lim:
    add(q,a,s,"exercise","limite",2)

# ── EXERCITII REZOLVATE - MATRICE (25) ──
ex_mat = [
    ("Calculeaza det[1 2; 3 4]","det = 4-6 = -2",["ad-bc = 1·4-2·3 = -2"]),
    ("Calculeaza det[2 1; 5 3]","det = 6-5 = 1",["2·3-1·5 = 1"]),
    ("Calculeaza det[3 0; 0 3]","det = 9",["3·3-0·0 = 9"]),
    ("Calculeaza det[1 0 0; 0 2 0; 0 0 3]","det = 6",["Matrice diagonala: 1·2·3 = 6"]),
    ("Calculeaza det[1 1 1; 0 1 1; 0 0 1]","det = 1",["Matrice triunghiulara: 1·1·1 = 1"]),
    ("Calculeaza det[2 3 1; 0 1 2; 1 0 3]","det = 2(3-0)-3(0-2)+1(0-1) = 6+6-1 = 11",["Dezvoltare dupa prima linie"]),
    ("Inversa matricei [2 1; 1 1]","A⁻¹ = [1 -1; -1 2]",["det=2-1=1","A⁻¹ = (1/1)·[1 -1; -1 2]"]),
    ("Inversa matricei [1 2; 3 4]","A⁻¹ = (1/(-2))·[4 -2; -3 1] = [-2 1; 3/2 -1/2]",["det=-2","A⁻¹ = [4/-2 -2/-2; -3/-2 1/-2]"]),
    ("Rezolva cu Cramer: x+y=3, 2x-y=3","D=(-1-2)=-3, Dx=(−3−3)=−6, Dy=(3−6)=−3. x=2, y=1.",["D=-3, Dx=-6, Dy=-3","x=Dx/D=2, y=Dy/D=1"]),
    ("Rezolva: x+y=5, x-y=1","x=3, y=2",["Adunam: 2x=6 => x=3","y=5-3=2"]),
    ("Rezolva: 2x+3y=7, x-y=1","x=2, y=1",["Din ec.2: x=y+1","2(y+1)+3y=7 => 5y=5 => y=1","x=2"]),
    ("Calculeaza A² daca A=[1 1; 0 1]","A² = [1 2; 0 1]",["A·A = [1·1+1·0, 1·1+1·1; 0+0, 0+1] = [1 2; 0 1]"]),
    ("Calculeaza A³ daca A=[1 1; 0 1]","A³ = [1 3; 0 1]",["A³ = A²·A = [1 2; 0 1]·[1 1; 0 1] = [1 3; 0 1]"]),
    ("Cat e Aⁿ daca A=[1 1; 0 1]?","Aⁿ = [1 n; 0 1]",["Pattern: A² = [1 2; 0 1], A³ = [1 3; 0 1]","Prin inductie: Aⁿ = [1 n; 0 1]"]),
]
for q,a,s in ex_mat:
    add(q,a,s,"exercise","matrice",2)

# ── EXERCITII M3/M4 SPECIFICE (30) ──
m3m4 = [
    ("Rezolva ecuatia 5x-3=2x+6","3x=9, x=3",["5x-2x=6+3","3x=9","x=3"],"M3"),
    ("Rezolva 2(x-1)+3=x+4","x=3",["2x-2+3=x+4","x=3"],"M3"),
    ("Calculeaza det[1 3; 2 5]","det = 5-6 = -1",["1·5-3·2 = -1"],"M3"),
    ("Rezolva sistemul: x+y=4, 2x-y=5","x=3, y=1",["Adunam: 3x=9 => x=3","y=4-3=1"],"M3"),
    ("Calculeaza derivata lui f(x)=x^2+3x","f'(x) = 2x+3",["(x²)'=2x, (3x)'=3"],"M3"),
    ("Calculeaza ∫(x+2)dx","x²/2+2x+C",["∫x=x²/2, ∫2=2x"],"M3"),
    ("In ce punct are f(x)=x^2-6x+8 minim?","x=3, f(3)=-1",["f'=2x-6=0 => x=3","f(3)=9-18+8=-1"],"M3"),
    ("Calculeaza ∫₀² x dx","2",["x²/2|₀² = 4/2-0 = 2"],"M3"),
    ("Rezolva x^2-4=0","x=±2",["(x-2)(x+2)=0"],"M4"),
    ("Rezolva 3x+1=10","x=3",["3x=9, x=3"],"M4"),
    ("Cat e C(4,2)?","C(4,2) = 6",["4!/(2!·2!) = 24/4 = 6"],"M4"),
    ("Cat e suma 1+2+3+...+20?","210",["S = 20·21/2 = 210"],"M4"),
    ("Calculeaza perimetrul triunghiului cu varfuri A(0,0), B(3,0), C(0,4)","P = 3+4+5 = 12",["AB=3, AC=4, BC=√(9+16)=5"],"M4"),
    ("Aria triunghiului dreptunghic cu catetele 3 si 4?","Aria = 6",["A = 3·4/2 = 6"],"M4"),
    ("Rezolva inecuatia 2x-1>5","x > 3",["2x > 6","x > 3"],"M3"),
]
for q,a,s,p in m3m4:
    add(q,a,s,"exercise","exercitii profil",1,p)

# ── ERORI SI CONFUZII FRECVENTE (40) ──
erori = [
    ("(x+y)^2 = x^2 + y^2?","NU! (x+y)² = x²+2xy+y². Ai uitat termenul 2xy.",["(x+y)² = x² + 2xy + y²","GRESIT: x² + y²"]),
    ("sqrt(a^2+b^2) = a+b?","NU! √(a²+b²) ≠ a+b. Radical din suma ≠ suma radicalilor.",["√(9+16) = √25 = 5","DAR 3+4 = 7 ≠ 5"]),
    ("(a/b)^2 = a^2/b^2?","DA, asta e corect! (a/b)² = a²/b².",["Corect!"]),
    ("sqrt(a·b) = sqrt(a)·sqrt(b)?","DA, pentru a,b≥0. √(ab) = √a·√b.",["Corect pentru a,b ≥ 0"]),
    ("ln(a+b) = ln(a)+ln(b)?","NU! ln(a+b) ≠ ln(a)+ln(b). Formula corecta: ln(ab) = ln(a)+ln(b).",["GRESIT: ln(a+b) = ln(a)+ln(b)","CORECT: ln(a·b) = ln(a)+ln(b)"]),
    ("ln(a·b) = ln(a)·ln(b)?","NU! ln(a·b) = ln(a)+ln(b) (suma, nu produs).",["GRESIT: ln(a)·ln(b)","CORECT: ln(a)+ln(b)"]),
    ("(fg)' = f'·g'?","NU! (fg)' = f'g+fg' (regula produsului).",["GRESIT: f'·g'","CORECT: f'g + fg'"]),
    ("(f/g)' = f'/g'?","NU! (f/g)' = (f'g-fg')/g² (regula catului).",["GRESIT: f'/g'","CORECT: (f'g-fg')/g²"]),
    ("(f+g)' = f'+g'?","DA! Derivata sumei = suma derivatelor. Asta e corect.",["Corect! Derivata e liniara"]),
    ("(e^x)' = x·e^(x-1)?","NU! Asta e regula pt xⁿ, nu pt eˣ. (eˣ)' = eˣ.",["Confuzie: (xⁿ)' = nxⁿ⁻¹","DAR: (eˣ)' = eˣ"]),
    ("∫e^x dx = e^x?","Aproape! ∫eˣdx = eˣ + C. Nu uita constanta!",["Nu uita +C la integrale nedefinite"]),
    ("sin(2x) = 2sin(x)?","NU! sin(2x) = 2sin(x)cos(x). Sin nu e liniara.",["GRESIT: 2sinx","CORECT: 2sinx·cosx"]),
    ("cos(a+b) = cos(a)+cos(b)?","NU! cos(a+b) = cos(a)cos(b)-sin(a)sin(b).",["Cosinus NU e aditiv"]),
    ("1/a + 1/b = 1/(a+b)?","NU! 1/a+1/b = (a+b)/(ab).",["GRESIT: 1/(a+b)","CORECT: (a+b)/(ab)"]),
    ("sqrt(x^2) = x?","Nu mereu! √(x²) = |x|. Daca x<0, √(x²) = -x.",["√(x²) = |x|","√((-3)²) = √9 = 3 = |-3|"]),
    ("Daca f'(x0)=0, e punct de extrem?","Nu neaparat! Trebuie sa verifici ca f' isi schimba semnul. Contraexemplu: f(x)=x³, f'(0)=0 dar nu e extrem.",["f'(x0)=0 e conditie necesara, nu suficienta","Verifici schimbarea de semn"]),
    ("Daca det(A)=0, sistemul nu are solutie?","Nu neaparat! Poate avea infinite solutii (nedeterminat) SAU nicio solutie (incompatibil).",["det=0 => Cramer nu merge","Poate fi: 0 solutii SAU ∞ solutii"]),
    ("La integrala definita pun +C?","NU! +C se pune DOAR la integrala nedefinita. La definita: F(b)-F(a), fara C.",["Definita: F(b)-F(a)","Nedefinita: F(x)+C"]),
    ("Pot simplifica a/(a+b) = 1/b?","NU! a nu se simplifica cu numitorul care e suma. a/(a+b) ≠ 1/b.",["Nu poti simplifica in suma","a/(a+b) ramane asa"]),
    ("x^0 = 0?","NU! x⁰ = 1 (pentru x≠0). Orice numar nenul la puterea 0 e 1.",["x⁰ = 1 (x≠0)","0⁰ e nedefinit"]),
    ("Pot scoate ln din integrala?","NU! ln(∫f dx) ≠ ∫ln(f)dx. Logaritmul nu se 'scoate' din integrala.",["Gresit!"]),
    ("La L'Hopital derivez numaratorul SI numitorul impreuna?","NU! Derivezi separat: lim f'/g', NU (f/g)'.",["L'Hopital: lim f(x)/g(x) = lim f'(x)/g'(x)","NU aplici regula catului"]),
    ("sin^(-1)(x) = 1/sin(x)?","NU! sin⁻¹(x) = arcsin(x). 1/sin(x) = csc(x).",["sin⁻¹ = arcsin (functia inversa)","1/sin = cosecanta"]),
    ("Derivata lui |x| e 1?","NU! |x|' = x/|x| = sgn(x). E 1 pt x>0 si -1 pt x<0. Nu exista in x=0.",["(|x|)' = 1 pt x>0","(|x|)' = -1 pt x<0","Nu exista in 0"]),
]
for q,a,s in erori:
    add(q,a,s,"error_analysis","erori comune",2)

# ── VARIANTE BAC - INTREBARI TIP EXAMEN (40) ──
bac_tip = [
    ("Suma solutiilor ecuatiei x^2-5x+6=0 este:","S = 5 (Vieta: -b/a = 5)",["x1+x2 = -(-5)/1 = 5"]),
    ("Produsul solutiilor ecuatiei x^2-5x+6=0 este:","P = 6 (Vieta: c/a = 6)",["x1·x2 = 6/1 = 6"]),
    ("Numarul solutiilor ecuatiei x^2+x+1=0 este:","0 solutii reale (delta = 1-4 = -3 < 0)",["delta < 0 => fara solutii in R"]),
    ("Valoarea lui C(5,2)+C(5,3) este:","C(5,2)+C(5,3) = 10+10 = 20 = C(6,3)",["Sau: C(5,2)+C(5,3) = C(6,3) = 20"]),
    ("Restul impartirii lui 7^100 la 10 este:","1",["7¹=7, 7²=49, 7³=343, 7⁴=2401","Ciclul: 7,9,3,1,7,9,3,1...","100/4=25 rest 0 => ultimul din ciclu = 1"]),
    ("Numarul de termeni ai dezvoltarii (x+y)^10 este:","11 termeni (n+1 = 10+1)",["Binomul lui Newton: n+1 termeni"]),
    ("Cate numere de 3 cifre se pot forma cu cifrele {1,2,3}?","27 (cu repetitie: 3³) sau 6 (fara: 3!)",["Cu repetitie: 3·3·3 = 27","Fara repetitie: 3! = 6"]),
    ("Probabilitatea de a obtine suma 4 la 2 zaruri","P = 3/36 = 1/12",["Perechi: (1,3),(2,2),(3,1) = 3","Total: 36"]),
    ("Determinantul matricei [a 0; 0 b] este:","det = ab",["Matrice diagonala: det = produsul diagonalei"]),
    ("Daca A = [1 2; 0 1], cat e det(A^3)?","det(A³) = (det A)³ = 1³ = 1",["det(A)=1","det(Aⁿ)=(det A)ⁿ"]),
    ("Lim(x→0) (x²+x)/x este:","lim = 1",["(x²+x)/x = x+1 → 1"]),
    ("Derivata functiei f(x)=x³+x in punctul x=1 este:","f'(1) = 4",["f'(x)=3x²+1","f'(1)=3+1=4"]),
    ("∫₀¹ (2x+1)dx este:","2",["F(x)=x²+x","F(1)-F(0)=2-0=2"]),
    ("Asimptota orizontala a lui f(x)=(2x+1)/(x+3) este:","y = 2",["lim(x→∞) (2x+1)/(x+3) = 2"]),
    ("Numarul de asimptote verticale ale lui f(x)=1/(x²-4) este:","2 (x=2 si x=-2)",["x²-4=0 => x=±2"]),
    ("Daca f(x)=x^3-3x, punctele critice sunt:","x = ±1",["f'(x)=3x²-3=3(x²-1)=0","x=±1"]),
    ("Matricea inversa a lui I (identitate) este:","I⁻¹ = I",["I·I = I"]),
    ("Cat e tr(A) daca A=[1 2; 3 4]?","tr(A) = 1+4 = 5",["Urma = suma elementelor diagonale"]),
    ("Daca z=3+4i, cat e |z|?","|z| = 5",["√(9+16) = √25 = 5"]),
    ("Conjugatul lui z=2-3i este:","z̄ = 2+3i",["Se schimba semnul partii imaginare"]),
]
for q,a,s in bac_tip:
    add(q,a,s,"exercise","variante BAC",2)

# ── CONVERSATII EXTRA (60) ──
conv_extra = [
    ("Zi-mi o formula","Care formula? Spune subiectul (derivate, integrale, trig, etc.) si iti dau formula cu explicatie.",["Spune subiectul"]),
    ("Rezuma lectia de derivate","Derivata = viteza de variatie. Reguli: (xⁿ)'=nxⁿ⁻¹, (eˣ)'=eˣ, (sinx)'=cosx. Regula produsului, catului, lantului.",["Formule de baza + 3 reguli"]),
    ("Rezuma lectia de integrale","Integrala = inversa derivatei + aria. ∫xⁿ=xⁿ⁺¹/(n+1), ∫eˣ=eˣ. Metode: directa, substitutie, parti.",["Formule + 3 metode"]),
    ("Rezuma lectia de limite","Limita = unde se duce functia. Reguli: grad P vs Q, L'Hopital la 0/0 si ∞/∞, limita remarcabila sinx/x=1.",["Regula gradelor + L'Hopital + remarcabile"]),
    ("Rezuma lectia de matrice","Matrice = tabel de numere. Operatii: +, ·scalar, ·matrice. Det 2x2: ad-bc. Inversa: adj/det. Sisteme: Cramer.",["Operatii + det + inversa + Cramer"]),
    ("Ce invat prima data?","Incepe cu formulele de derivare (sunt baza). Apoi integrale. Apoi limite. Matricele separat.",["1. Derivate","2. Integrale","3. Limite","4. Matrice"]),
    ("Cat de greu e BAC-ul?","Depinde de profil si pregatire. Cu 2-3 luni de pregatire constanta, e foarte fezabil sa iei nota buna.",["M1 cel mai greu, M3/M4 mai accesibile","2-3 luni de pregatire sunt suficiente"]),
    ("Pot lua 10 fara meditatii?","Da, absolut! Cu disciplina, subiecte rezolvate zilnic, si intelegerea conceptelor poti lua 10 singur.",["Da, cu disciplina si exercitiu"]),
    ("Ce gresesc cel mai des elevii?","1) Greseli de calcul cu semne. 2) Uitarea regulii lantului. 3) (fg)'≠f'g'. 4) Lipsa +C. 5) Simplificari gresite.",["Top 5 greseli"]),
    ("Cum memorez formulele?","1) Scrie-le de mana de mai multe ori. 2) Foloseste-le in exercitii. 3) Fa flashcarduri. 4) Repeta inainte de somn.",["Scrie, aplica, repeta"]),
    ("Mai am o saptamana pana la BAC","Focus pe: 1) Subiectul I (cel mai usor, 30p sigure). 2) Matrice si det (Sub II). 3) Derivata si studiu de functie (Sub III basic).",["Subiectul I complet","Matrice de baza","Studiu de functie simplu"]),
    ("Mai am o luna pana la BAC","Perfect! Fa 1 subiect pe zi. Saptamana 1-2: reluare formule. Saptamana 3-4: subiecte complete cronometrate.",["1 subiect/zi","Reluare formule + subiecte complete"]),
    ("Am esuat un test","Nu conteaza un test! Important e ce inveti din greseli. Analizeaza ce ai gresit si exerseaza acele tipuri de exercitii.",["Analizeaza greselile","Exerseaza punctele slabe"]),
    ("Nu imi iese nimic","Ia o pauza scurta (10 min), apoi revino cu mintea proaspata. Incepe cu ceva usor pentru incredere.",["Pauza + incepe usor"]),
    ("Sunt obosit","E ok sa te odihnesti! Somnul ajuta la memorare. Revino maine cu energie.",["Odihna e parte din invatare"]),
    ("Cum fac un grafic?","1) Gasesti domeniul. 2) Intersectii cu axele. 3) Derivata → monotonie. 4) Asimptote. 5) Tabel de variatie. 6) Desenezi punctele si unesti.",["D, intersectii, monotonie, asimptote, grafic"]),
    ("Ce e o demonstratie?","Un lant logic de argumente care porneste de la ipoteze si ajunge la concluzie, folosind definitii si teoreme.",["Ipoteza -> argumente logice -> concluzie"]),
    ("Ce e o contraexemplu?","Un exemplu concret care arata ca o afirmatie e falsa. E suficient UN contraexemplu ca sa infirmi.",["Un singur contraexemplu e suficient"]),
    ("Ce e un corolar?","O consecinta directa a unei teoreme. Se demonstreaza imediat din teorema.",["Corolar = consecinta imediata"]),
    ("Ce e o axioma?","O afirmatie acceptata ca adevarata fara demonstratie. Stau la baza matematicii.",["Axioma = adevar fundamental, fara demonstratie"]),
    ("Testeaza-ma la derivate","Ok! Calculeaza f'(x) daca f(x) = x³·eˣ. Raspunde cand esti gata!",["Aplica regula produsului"]),
    ("Testeaza-ma la integrale","Ok! Calculeaza ∫(3x²+2x+1)dx. Raspunde cand esti gata!",["Integrezi termen cu termen"]),
    ("Testeaza-ma la limite","Ok! Calculeaza lim(x→∞) (2x²+1)/(x²-3). Raspunde cand esti gata!",["Imparti la x²"]),
    ("Testeaza-ma la matrice","Ok! Calculeaza det[3 1; 2 4]. Raspunde cand esti gata!",["ad-bc"]),
    ("Vreau un quiz","Hai! Intrebarea 1: Cat e derivata lui sin(2x)? A) cos(2x) B) 2cos(2x) C) -2cos(2x). Raspunde cu litera!",["Raspuns corect: B"]),
    ("Am raspuns B","Corect! 🎉 (sin(2x))' = 2cos(2x) prin regula lantului. Intrebarea 2: Cat e ∫e^x dx? A) xe^x B) e^x+C C) e^(x+1)",["Bravo!"]),
    ("Cum se noteaza derivata?","Se noteaza f'(x), sau df/dx, sau ẏ (punctul lui Newton). La ordinul 2: f''(x) sau d²f/dx².",["f'(x) = df/dx = ẏ"]),
    ("Cine a inventat calculul?","Newton si Leibniz, independent, in secolul 17. Leibniz a creat notatia ∫ si dx pe care o folosim azi.",["Newton si Leibniz, sec. XVII"]),
    ("La ce foloseste matematica?","Peste tot! Fizica, inginerie, informatica, economie, medicina (statistica), arhitectura... Matematica e limbajul stiintei.",["E baza tuturor stiintelor"]),
    ("E matematica grea?","Matematica e ca sportul - pare grea pana cand exersezi suficient. Cu practica constanta, devine naturala.",["Practica face perfect"]),
]
for q,a,s in conv_extra:
    add(q,a,s,"conversation","conversatie")

# ── ALGEBRA (25) ──
algebra = [
    ("Simplifica (x^2-4)/(x-2)","= (x-2)(x+2)/(x-2) = x+2, pt x≠2",["Factorizare la numarator"]),
    ("Simplifica (x^2-1)/(x+1)","= (x-1)(x+1)/(x+1) = x-1, pt x≠-1",["Factorizare diferenta de patrate"]),
    ("Descompune x^3-1","x³-1 = (x-1)(x²+x+1)",["Formula: a³-b³ = (a-b)(a²+ab+b²)"]),
    ("Descompune x^3+8","x³+8 = (x+2)(x²-2x+4)",["Formula: a³+b³ = (a+b)(a²-ab+b²)"]),
    ("Calculeaza (2+√3)(2-√3)","= 4-3 = 1",["(a+b)(a-b) = a²-b²"]),
    ("Rationalizeaza 1/(√2+1)","= (√2-1)/((√2+1)(√2-1)) = (√2-1)/1 = √2-1",["Inmultim cu conjugata"]),
    ("Rationalizeaza 2/(√3-1)","= 2(√3+1)/((√3-1)(√3+1)) = 2(√3+1)/2 = √3+1",["Inmultim cu conjugata"]),
    ("Ce e schema lui Horner?","Metoda rapida de impartire a unui polinom la (x-a) si de evaluare P(a).",["P(x) = (x-a)·Q(x) + P(a)","Util pt factorizare"]),
    ("Rezolva x^3-6x^2+11x-6=0","x=1 e radacina. Horner: (x-1)(x²-5x+6)=(x-1)(x-2)(x-3). Sol: 1,2,3.",["Incercam x=1: 1-6+11-6=0 ✓","Horner => x²-5x+6","Delta=1, x=2,3"]),
    ("Ce e gradul unui polinom?","Cea mai mare putere a lui x cu coeficient nenul. Grad(3x⁴-x+2) = 4.",["Exemplu: grad(x³+2x) = 3"]),
    ("Ce e teorema factorizarii?","Un polinom de grad n are exact n radacini (numarand multiplicitatile, in C).",["n radacini in C","Mai putine in R"]),
    ("Ce e discriminantul?","Δ = b²-4ac. Δ>0: 2 solutii reale, Δ=0: 1 solutie dubla, Δ<0: 0 solutii reale.",["delta = b² - 4ac"]),
]
for q,a,s in algebra:
    add(q,a,s,"concept","algebra",2)

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
