# Capitolul 1 — Introducere

## 1.1 Tema de proiectare

Lucrarea de față prezintă proiectarea și dezvoltarea aplicației mobile **SmartBAC** — o platformă inteligentă de pregătire pentru examenul de Bacalaureat la Matematică, bazată pe inteligență artificială. Aplicația integrează multiple componente AI (model Transformer antrenat de la zero, fine-tuning pe model de limbaj mare cu LoRA, predicție notă cu ensemble ML, OCR pentru scanare exerciții) într-o experiență de învățare adaptivă și gamificată.

Tema se încadrează în domeniul aplicațiilor educaționale inteligente (Intelligent Tutoring Systems — ITS), la intersecția dintre procesarea limbajului natural (NLP), învățare automată (ML) și dezvoltare de aplicații mobile cross-platform.

## 1.2 Stadiul actual al problemei abordate

Pregătirea pentru examenul de Bacalaureat la Matematică reprezintă o provocare semnificativă pentru elevii din România. Conform statisticilor Ministerului Educației, rata de promovare la BAC oscilează în jurul valorii de 70%, iar matematica rămâne una dintre probele cu cele mai scăzute medii.

Soluțiile existente pe piață prezintă următoarele limitări:

| Soluție | Tip | Avantaje | Limitări |
|---------|-----|----------|----------|
| **Mathway** | Aplicație web/mobil | Rezolvare pas cu pas, interfață intuitivă | Nu este adaptat curriculumului românesc, nu oferă plan de studiu personalizat, fără gamificație |
| **Photomath** | Aplicație mobil (OCR) | Scanner exerciții excelent, gratuit | Doar rezolvare, fără tracked progress, fără adaptare la nivel, fără conținut BAC |
| **Khan Academy** | Platformă educațională | Conținut vast, progres tracked | Curriculum american, nu acoperă programa BAC România, fără AI tutor conversațional |
| **E-Bac.ro** | Platformă web | Conținut BAC românesc, exerciții oficiale | Fără AI, fără adaptare la nivel, interfață învechită, fără gamificație |
| **Meditații private** | Offline | Feedback personalizat, adaptare | Cost ridicat (50-150 RON/h), disponibilitate limitată, fără tracking progres |

**Tabelul 1.1** — Analiza comparativă a soluțiilor existente

SmartBAC se diferențiază prin combinarea tuturor avantajelor într-o singură aplicație:
- Conținut adaptat integral curriculumului BAC România (4.541 exerciții pe Subiectele I, II, III)
- Model AI antrenat specific pe exerciții BAC românești
- Învățare adaptivă care detectează automat punctele slabe ale elevului
- Scanner OCR pentru rezolvare din poze
- Gamificație completă (XP, nivele, streak-uri, ligi) pentru menținerea motivației
- Predicție notă BAC bazată pe performanța individuală

## 1.3 Scopul și Obiectivele proiectului

**Scopul proiectului** este dezvoltarea unei aplicații mobile inteligente care oferă pregătire personalizată și adaptivă pentru examenul de Bacalaureat la Matematică, utilizând tehnici moderne de inteligență artificială.

**Obiective:**

1. **Dezvoltarea unui pipeline complet de AI pentru rezolvarea exercițiilor matematice** — implementarea unui model Transformer de la zero (tokenizer BPE custom, arhitectură decoder-only), fine-tuning pe un model de limbaj mare (DeepSeek-R1 1.5B) cu LoRA, și integrarea unui solver rule-based deterministic, toate antrenate pe exerciții BAC reale.

2. **Implementarea unui sistem de învățare adaptivă și predicție** — proiectarea unui algoritm de spaced repetition (SM-2) combinat cu detecție automată a punctelor slabe, recomandări personalizate de exerciții și predicție a notei BAC folosind un model ML ensemble (R² = 0.966).

3. **Dezvoltarea unei aplicații mobile cross-platform complete** — implementarea a 16 ecrane funcționale în React Native cu Expo, backend FastAPI cu MongoDB, autentificare JWT, și design system coerent cu animații native.

4. **Integrarea unui sistem de gamificație** — implementarea mecanismelor de XP, 20 de nivele, streak-uri zilnice, achievements, ligi competitive săptămânale și daily challenges pentru creșterea motivației și retenției utilizatorilor.

## 1.4 Domeniul de aplicabilitate

Soluția propusă se adresează în principal elevilor de liceu din România (clasele IX-XII) care se pregătesc pentru examenul de Bacalaureat la Matematică, atât pentru profilul M1 (Matematică-Informatică) cât și M2 (Științele Naturii).

Aplicația poate fi utilizată și de:
- Profesori de matematică, ca instrument suplimentar de evaluare și monitorizare a progresului elevilor
- Elevi care doresc să-și consolideze cunoștințele de matematică, independent de examenul de BAC
- Persoane care susțin examenul de BAC ca privatist sau la a doua specialitate

Prin adaptarea conținutului și a modelelor AI, arhitectura aplicației poate fi extinsă și pentru alte materii de examen (Fizică, Chimie) sau alte sisteme educaționale.

## 1.5 Structura pe capitole

**Capitolul 2 — Considerații teoretice** prezintă fundamentele teoretice ale tehnologiilor utilizate: arhitectura Transformer, algoritmul BPE pentru tokenizare, metoda LoRA pentru fine-tuning eficient, algoritmul SM-2 pentru repetare spațiată, și modelele ensemble pentru predicție.

**Capitolul 3 — Proiectare și arhitectură** descrie arhitectura generală a sistemului, structura bazei de date MongoDB, diagrama bloc a componentelor și fluxurile de date între frontend, backend și modelele AI.

**Capitolul 4 — Dezvoltare și implementare** detaliază procesul de dezvoltare: pipeline-ul de date (colectare, augmentare, procesare), antrenarea modelelor AI, implementarea backend-ului și frontend-ului, și integrarea componentelor.

**Capitolul 5 — Rezultate și testare** prezintă rezultatele obținute: metricile de antrenare ale modelelor, performanța sistemului de predicție, capturi de ecran ale aplicației și evaluarea funcționalităților.

**Capitolul 6 — Concluzii** sintetizează concluziile generale, contribuțiile personale ale autorului și posibilitățile de dezvoltare ulterioară a proiectului.
