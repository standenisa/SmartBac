# Capitolul 1 — Introducere

## 1.1 Tema de proiectare

Lucrarea de față prezintă proiectarea și dezvoltarea aplicației mobile **SmartBAC** — o platformă inteligentă de pregătire pentru examenul de Bacalaureat la Matematică, bazată pe inteligență artificială. Aplicația integrează multiple componente AI — model Transformer antrenat de la zero, fine-tuning pe model de limbaj mare cu LoRA, predicție notă cu ensemble ML, OCR pentru scanare exerciții — într-o experiență de învățare adaptivă și gamificată.

Tema se încadrează în domeniul aplicațiilor educaționale inteligente (Intelligent Tutoring Systems — ITS), la intersecția dintre procesarea limbajului natural (NLP), învățarea automată (ML) și dezvoltarea de aplicații mobile cross-platform.

Motivația principală a proiectului este democratizarea accesului la pregătire de calitate pentru examenul de Bacalaureat. În timp ce meditațiile private au costuri prohibitive (50-150 RON/oră) și disponibilitate limitată, SmartBAC oferă un tutor AI accesibil, disponibil 24/7, care se adaptează ritmului și nivelului fiecărui elev.

## 1.2 Stadiul actual al problemei abordate

Pregătirea pentru examenul de Bacalaureat la Matematică reprezintă o provocare semnificativă pentru elevii din România. Conform statisticilor Ministerului Educației, rata de promovare la BAC oscilează în jurul valorii de 70%, iar matematica rămâne una dintre probele cu cele mai scăzute medii.

Peisajul actual al soluțiilor digitale de pregătire prezintă următoarele caracteristici:

**Aplicații internaționale** precum Mathway, Photomath și Khan Academy oferă funcționalități avansate (rezolvare pas cu pas, OCR, conținut structurat), dar nu sunt adaptate curriculumului românesc și nu acoperă programa specifică BAC.

**Platforme românești** precum E-Bac.ro conțin exerciții oficiale BAC, dar nu integrează componente AI, nu oferă adaptare la nivelul individual al elevului și au interfețe învechite.

**Meditațiile private** rămân opțiunea preferată datorită feedback-ului personalizat, dar sunt limitate de cost, disponibilitate și lipsa unui sistem de tracking al progresului.

| Soluție | Tip | Avantaje | Limitări |
|---------|-----|----------|----------|
| **Mathway** | Aplicație web/mobil | Rezolvare pas cu pas, interfață intuitivă | Nu este adaptat curriculumului românesc, fără plan de studiu personalizat, fără gamificație |
| **Photomath** | Aplicație mobil (OCR) | Scanner exerciții excelent, gratuit | Doar rezolvare, fără tracking progres, fără adaptare la nivel, fără conținut BAC |
| **Khan Academy** | Platformă educațională | Conținut vast, progres tracked | Curriculum american, nu acoperă programa BAC România, fără AI tutor conversațional |
| **E-Bac.ro** | Platformă web | Conținut BAC românesc, exerciții oficiale | Fără AI, fără adaptare la nivel, interfață învechită, fără gamificație |
| **Meditații private** | Offline | Feedback personalizat, adaptare la nivel | Cost ridicat (50-150 RON/h), disponibilitate limitată, fără tracking progres |

**Tabelul 1.1** — Analiza comparativă a soluțiilor existente pentru pregătirea BAC Matematică

SmartBAC se diferențiază prin combinarea tuturor avantajelor într-o singură aplicație:
- Conținut adaptat integral curriculumului BAC România (4.541 exerciții pe Subiectele I, II, III)
- Model AI antrenat specific pe exerciții BAC românești (Transformer 18.6M parametri)
- Învățare adaptivă care detectează automat punctele slabe ale elevului (algoritmul SM-2)
- Scanner OCR pentru rezolvare din poze (Qwen2.5-VL)
- Gamificație completă (XP, nivele, streak-uri, ligi competitive) pentru menținerea motivației
- Predicție notă BAC bazată pe performanța individuală (ensemble ML, R² = 0.966)

## 1.3 Scopul și obiectivele proiectului

**Scopul proiectului** este dezvoltarea unei aplicații mobile inteligente care oferă pregătire personalizată și adaptivă pentru examenul de Bacalaureat la Matematică, utilizând tehnici moderne de inteligență artificială.

**Obiective:**

**O1. Dezvoltarea unui pipeline complet de AI pentru rezolvarea exercițiilor matematice.** Implementarea unui model Transformer de la zero (tokenizer BPE custom cu vocabular de 8.192 tokeni, arhitectură decoder-only cu 18.6M parametri), fine-tuning pe un model de limbaj mare (Qwen2.5-Math-1.5B) cu LoRA prin framework-ul MLX, și integrarea unui solver rule-based deterministic care acoperă 10+ tipuri de exerciții.

**O2. Implementarea unui sistem de învățare adaptivă și predicție.** Proiectarea unui algoritm de spaced repetition (SM-2) combinat cu detecție automată a punctelor slabe, recomandări personalizate de exerciții prin filtrare bazată pe conținut, și predicție a notei BAC folosind un model ML ensemble format din Random Forest, Gradient Boosting, XGBoost și Neural Network (R² = 0.966).

**O3. Dezvoltarea unei aplicații mobile cross-platform complete.** Implementarea a 16 ecrane funcționale în React Native cu Expo SDK 54, backend FastAPI cu MongoDB, autentificare JWT cu bcrypt, și design system coerent cu animații native la 60fps.

**O4. Integrarea unui sistem de gamificație complet.** Implementarea mecanismelor de XP, 20 de nivele, streak-uri zilnice cu freeze system, 15+ achievements, ligi competitive săptămânale (Bronz → Diamant) și daily challenges pentru creșterea motivației și retenției utilizatorilor.

## 1.4 Domeniul de aplicabilitate

Soluția propusă se adresează în principal elevilor de liceu din România (clasele IX-XII) care se pregătesc pentru examenul de Bacalaureat la Matematică, atât pentru profilul M1 (Matematică-Informatică) cât și M2 (Științele Naturii).

Aplicația poate fi utilizată și de:
- Profesori de matematică, ca instrument suplimentar de evaluare și monitorizare a progresului elevilor
- Elevi care doresc să-și consolideze cunoștințele de matematică, independent de examenul de BAC
- Persoane care susțin examenul de BAC ca privatist sau la a doua specialitate

Prin adaptarea conținutului și a modelelor AI, arhitectura aplicației poate fi extinsă și pentru alte materii de examen (Fizică, Chimie) sau alte sisteme educaționale din regiune.

## 1.5 Structura pe capitole

**Capitolul 2 — Considerații teoretice** prezintă fundamentele teoretice ale tehnologiilor utilizate: arhitectura Transformer și mecanismul de atenție, algoritmul BPE pentru tokenizare, metoda LoRA pentru fine-tuning eficient, algoritmul SM-2 pentru repetare spațiată, modelele ensemble pentru predicție și principiile gamificației în educație.

**Capitolul 3 — Proiectare și arhitectură** descrie arhitectura generală a sistemului pe 3 niveluri (frontend, backend, AI), structura bazei de date MongoDB cu 7 colecții, diagramele UML (cazuri de utilizare, secvență, componente) și fluxurile de date între componente.

**Capitolul 4 — Dezvoltare și implementare** detaliază procesul de dezvoltare: pipeline-ul de date (colectare, augmentare, procesare), antrenarea modelelor AI (Transformer custom și LoRA), implementarea backend-ului FastAPI și frontend-ului React Native, și sistemele de gamificație și învățare adaptivă.

**Capitolul 5 — Rezultate și testare** prezintă rezultatele obținute: metricile de antrenare ale modelelor, performanța sistemului de predicție, capturi de ecran ale aplicației funcționale și evaluarea end-to-end a funcționalităților.

**Capitolul 6 — Concluzii** sintetizează concluziile generale, contribuțiile personale ale autorului și posibilitățile de dezvoltare ulterioară a proiectului.
