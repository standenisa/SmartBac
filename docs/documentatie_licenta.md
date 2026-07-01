# SmartBAC — Aplicație Inteligentă de Pregătire pentru Bacalaureat la Matematică

**Proiect de Licență**

---

## Capitolul 1. Prezentarea Proiectului

### 1.1 Ce este SmartBAC

SmartBAC este o aplicație mobilă care ajută elevii de liceu să se pregătească pentru examenul de Bacalaureat la Matematică folosind inteligență artificială. Aplicația combină mai multe tehnologii AI într-o experiență de învățare completă:

- **Un model Transformer construit de la zero** (18.6 milioane de parametri) care rezolvă exerciții și generează explicații pas cu pas
- **Fine-tuning pe un LLM (DeepSeek-R1, 14B parametri)** cu LoRA pentru rezolvare avansată cu chain-of-thought reasoning
- **Scanner OCR** — faci poză la un exercițiu, AI-ul îl recunoaște și îl rezolvă
- **Chat AI Tutor** — explică concepte, rezolvă exerciții, detectează greșeli frecvente
- **Învățare adaptivă** — aplicația detectează ce topicuri sunt slabe și generează un plan personalizat
- **Predicție notă BAC** — model ensemble ML care estimează nota pe baza performanței
- **Gamificație completă** — XP, nivele, streak-uri, achievements, ligi, heatmap activitate

### 1.2 De ce am ales acest proiect

Pregătirea pentru BAC la matematică este o provocare pentru mulți elevi. Resursele existente (culegeri, meditații) nu oferă feedback personalizat și nu se adaptează nivelului fiecărui elev. SmartBAC rezolvă această problemă prin AI care:
- Se adaptează în timp real la nivelul elevului
- Oferă explicații pas cu pas pentru fiecare exercițiu
- Motivează prin gamificație (streak-uri, XP, competiție)
- Identifică punctele slabe și recomandă ce să studieze

### 1.3 Ce conține proiectul — pe scurt

| Componentă | Tehnologie | Ce face |
|-----------|-----------|---------|
| Frontend | React Native + Expo | Aplicație mobilă iOS/Android, 16 ecrane |
| Backend | FastAPI + MongoDB | API REST, 12 routere, autentificare JWT |
| Transformer custom | PyTorch, antrenat pe M4 | Rezolvă exerciții, generează pași |
| LLM Fine-tuned | DeepSeek-R1-Distill-Qwen-1.5B + LoRA | Rezolvare avansată cu `<think>` reasoning |
| Tokenizer BPE | Python from scratch | 8,192 tokeni, suport LaTeX + română |
| ML Predictor | scikit-learn ensemble (RF+GB+XGB+NN) | Predicție notă BAC (R²=0.966) |
| OCR | Qwen2.5-VL-3B pe Kaggle | Extragere text din poze cu exerciții |
| Solver | DeepSeek-R1 pe Kaggle | Rezolvare exerciții scanate |
| GPT Fallback | GPT-4o-mini (ascuns) | Fallback când modelele locale nu pot răspunde |
| Dataset | 4,541 exerciții | Cls 9-12, structură BAC (Subiecte I/II/III) |

### 1.4 Structura fișierelor proiectului

```
bac-prep-ai/
├── ai/
│   ├── tokenizer/          — BPE tokenizer (bpe.py, train_tokenizer.py)
│   ├── transformer/        — Model custom (model.py, attention.py, train.py)
│   └── finetune/           — LoRA fine-tuning (lora_config.py, train_mlx.py)
├── backend/
│   ├── main.py             — FastAPI entry point
│   ├── database.py         — PostgreSQL connection
│   ├── routers/            — 12 API routers (auth, exercises, chat, solver...)
│   ├── services/           — Business logic (gamification, adaptive, math_tutor...)
│   └── models/             — SQLAlchemy models
├── frontend/
│   ├── app/(tabs)/         — 15 ecrane (index, exercises, chat, scanner...)
│   ├── components/         — 13 componente reutilizabile
│   ├── constants/          — Design system (duo.ts, typography.ts)
│   ├── contexts/           — Auth, Toast, Sound providers
│   └── services/           — API layer cu auth headers
├── data/
│   ├── raw/                — Exerciții originale BAC
│   └── processed/          — exercises_merged.json (2,834 exerciții)
├── scripts/                — Generare date, augmentare, merge
└── notebooks/              — Training notebooks pentru Kaggle
```

---

## Capitolul 2. Algoritmi Teoretici și Framework-uri

### 2.1 Transformer Architecture (Decoder-Only)

**Ce este:** Modelul Transformer este o arhitectură de rețea neuronală introdusă în 2017 (Vaswani et al., „Attention Is All You Need"). SmartBAC folosește varianta decoder-only (ca GPT), antrenată de la zero pe exerciții BAC.

**Cum funcționează — componentele:**

1. **Token Embedding** — transformă fiecare token (cuvânt/simbol) într-un vector de 384 numere
2. **Positional Encoding** — adaugă informație despre poziția tokenului în secvență folosind funcții sin/cos
3. **Multi-Head Self-Attention (8 capete)** — fiecare token „se uită" la toți tokenii anteriori și decide care sunt relevanți. Formula: `Attention(Q,K,V) = softmax(QK^T / √d_k) · V`. Masca cauzală previne accesul la tokeni viitori.
4. **Feed-Forward Network** — două straturi liniare cu activare GELU, dimensiune 1536
5. **Pre-Norm** — LayerNorm înainte de fiecare sub-strat (mai stabil decât Post-Norm original)
6. **8 blocuri stivuite** — fiecare bloc = Attention + FFN + residual connections

**Specificații model:**

| Parametru | Valoare |
|-----------|---------|
| Parametri totali | 18,577,920 |
| Vocabular | 5,850 tokeni |
| d_model | 384 |
| Capete atenție | 8 |
| Straturi | 8 |
| d_ff | 1,536 |
| Secvență max | 512 |
| Dropout | 0.1 |

**Cum se antrenează:** Next-token prediction cu teacher forcing. Modelul primește `<BOS> întrebare <SEP>` și învață să genereze `răspuns <SEP> pas1 <SEP> pas2 ... <EOS>`.

### 2.2 Byte Pair Encoding (BPE) — Tokenizer Custom

**Ce este:** BPE este un algoritm de compresie text care construiește vocabularul pornind de la caractere individuale și combinându-le iterativ.

**Algoritmul:**
1. Start: vocabular = toate caracterele unice din corpus
2. Numără perechile adiacente de tokeni
3. Unește cea mai frecventă pereche → token nou
4. Repetă 2-3 până la dimensiunea dorită (5,850)

**Adaptări pentru matematică:**
- 51 tokeni LaTeX protejați (`\frac`, `\int`, `\sin`, `\sqrt`, `\alpha` etc.) — nu se fragmentează niciodată
- 16 operatori matematici protejați (`+`, `-`, `=`, `^`, `(`, `)` etc.)
- Suport diacritice românești (ă, â, î, ș, ț)
- Acoperire: 100% (0 tokeni necunoscuți pe tot dataset-ul)

### 2.3 LoRA (Low-Rank Adaptation)

**Ce este:** LoRA este o metodă de fine-tuning eficientă care actualizează doar ~1% din parametrii unui model mare.

**Cum funcționează:** În loc să actualizăm matricea de greutăți W (dimensiune d×d), LoRA o descompune: `ΔW = A · B`, unde A are dimensiune d×r și B are r×d, cu r=16 (mult mai mic decât d). Astfel antrenăm doar 2·d·r parametri în loc de d².

**Ce am folosit:**
- Model base: DeepSeek-R1-Distill-Qwen-14B (quantizat 4-bit NF4)
- Rank: 16, Alpha: 32
- Format: `<think>` chain-of-thought (modelul „gândește" vizibil înainte de răspuns)
- Antrenat pe Kaggle GPU T4 x2

### 2.4 Algoritmul SM-2 (Spaced Repetition)

**Ce este:** SM-2 este algoritmul SuperMemo pentru repetare spațiată — decide CÂND să repete fiecare card.

**Cum funcționează:**
- Fiecare card are: ease factor (EF), interval, data review
- Răspuns bun → interval crește exponențial (1→3→7→14→30 zile)
- Răspuns slab → interval se resetează la 1 zi
- EF se ajustează: `EF' = EF + (0.1 - (5-q)(0.08 + (5-q)·0.02))`

Folosit în: ecranul de Flashcards (24 carduri pe 4 categorii: Algebră, Analiză, Geometrie, Trigonometrie).

### 2.5 Adaptive Learning System

**Ce face:** Alege automat următorul exercițiu optim pentru fiecare elev.

**Prioritizare (în ordine):**
1. Repetări scadente (spaced repetition)
2. Topicuri slabe (acuratețe < 50%)
3. Topicuri neexplorate
4. Dificultate progresivă

### 2.6 Grade Prediction (Ensemble ML)

**Ce face:** Prezice nota la BAC pe baza performanței din aplicație.

**Model:** Random Forest + Gradient Boosting ensemble
- Features: acuratețe per subiect, per topic, trend recent, timp rezolvare
- Output: notă estimată (1-10) + interval de încredere
- Necesită minim 10 exerciții rezolvate

### 2.7 Framework-uri

| Componentă | Framework | Rol |
|-----------|-----------|-----|
| Frontend | React Native 0.81 + Expo SDK 54 | UI cross-platform |
| Navigare | Expo Router 6 | Routing file-based |
| Animații | React Native Reanimated 4 | Animații native 60fps |
| Backend | FastAPI | API REST async |
| DB | MongoDB + PyMongo | Persistență date (NoSQL) |
| ML Training | PyTorch 2.0+ | Antrenare Transformer |
| Apple ML | MLX | Training pe Apple Silicon |
| LLM | Transformers + PEFT + TRL | Fine-tuning LoRA |
| OCR | Google Cloud Vision API | Text din imagini |

---

## Capitolul 3. Arhitectura Sistemului

### 3.1 Numele temei

**„SmartBAC — Aplicație mobilă inteligentă de pregătire pentru examenul de Bacalaureat la Matematică, bazată pe inteligență artificială"**

### 3.2 Ce ne-am propus

**Obiectiv principal:** O aplicație mobilă care folosește AI pentru pregătire personalizată la BAC Matematică.

**Obiective specifice:**
1. Model Transformer antrenat de la zero pentru rezolvare exerciții cu pași
2. Fine-tuning LLM cu LoRA pentru reasoning avansat (`<think>`)
3. OCR — scanare exerciții din poze
4. Învățare adaptivă cu SM-2 + detecție puncte slabe
5. Predicție notă BAC cu ML ensemble
6. Gamificație: XP, nivele, streak-uri, achievements, ligi
7. Plan de studiu AI personalizat

### 3.3 Metodologia

**Agile iterativ** în 5 faze:

**Faza 1 — Date:**
- Colectare exerciții BAC oficiale (2020-2024)
- Generare automată cu variații (scripts Python)
- Antrenare tokenizer BPE
- Rezultat: 2,834 exerciții cu soluții pas cu pas

**Faza 2 — Modele AI:**
- Implementare Transformer de la zero (PyTorch)
- Antrenare pe M4 Apple Silicon (60 epoci, ~60 min)
- Fine-tuning DeepSeek-R1 cu LoRA pe Kaggle
- Evaluare: BLEU, exact match

**Faza 3 — Backend:**
- FastAPI + PostgreSQL
- 12 routere REST + 7 servicii
- Integrare modele AI
- Autentificare JWT

**Faza 4 — Frontend:**
- React Native + Expo
- 15+ ecrane funcționale
- Design system custom (dark theme)
- Animații, componente reutilizabile

**Faza 5 — Testare & Polish:**
- Testare pe iOS real
- Optimizare performanță
- Iterare pe feedback

### 3.4 Diagrama bloc (arhitectura sistemului)

**Diagrama 1: Arhitectura generală**

```
┌────────────────────────────────────────────────────────────┐
│                      UTILIZATOR                            │
│                  (Elev liceu, cls 9-12)                     │
└────────────────────────┬───────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────┐
│              APLICAȚIE MOBILĂ (Frontend)                    │
│              React Native + Expo (iOS/Android)              │
│                                                            │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐  │
│  │🏠 Home │ │✏️ Exer.│ │🃏 Flash│ │🔥Streak│ │📷Scan  │  │
│  │Dashb.  │ │Rezolv. │ │ SM-2   │ │Heatmap │ │ OCR    │  │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘  │
│  ┌────────┐ ┌────────┐ ┌────────┐                        │
│  │🦉 Chat │ │🗺️ Plan │ │📊Pred. │  + Exam, Theory,      │
│  │AI Tutor│ │AI Study│ │ Nota   │  Pomodoro, Leagues...  │
│  └────────┘ └────────┘ └────────┘                        │
│                                                            │
│  services/api.ts → Auth headers automat (JWT Bearer)       │
└────────────────────────┬───────────────────────────────────┘
                         │  REST API (JSON)
                         ▼
┌────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                        │
│                                                            │
│  Routere:                                                  │
│  /api/auth     — Login, Register, JWT                      │
│  /api/exercises — CRUD, submit, hints, solution            │
│  /api/chat     — AI Tutor conversation                     │
│  /api/solver   — AI exercise solver                        │
│  /api/scanner  — OCR image processing                      │
│  /api/stats    — Performance analytics + heatmap           │
│  /api/ml       — Grade prediction + insights               │
│  /api/gamification — XP, levels, streaks, achievements     │
│  /api/leagues  — Weekly leaderboards                       │
│  /api/daily-challenge — Daily challenges                   │
│                                                            │
│  Servicii:                                                 │
│  AdaptiveLearning — SM-2 + weak topic detection            │
│  MathTutor        — Rule-based solver (10 tipuri)          │
│  MathExplainer    — Concepte cu explicații                  │
│  Recommender      — Content-based filtering                │
│  Gamification     — XP, levels, streaks                    │
│  Leagues          — Competiție săptămânală                  │
└───────┬────────────────┬─────────────────┬─────────────────┘
        │                │                 │
        ▼                ▼                 ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐
│  PostgreSQL  │ │Google Cloud  │ │    MODELE AI          │
│              │ │Vision API    │ │                      │
│ • Users      │ │              │ │ 1. Transformer Custom │
│ • Exercises  │ │ OCR:         │ │    18.6M params       │
│   (2,834)    │ │ Imagine →    │ │    PyTorch + MPS     │
│ • Attempts   │ │ Text matematic│ │                      │
│ • Streaks    │ │              │ │ 2. DeepSeek-R1+LoRA  │
│ • Achievem.  │ │              │ │    14B, 4-bit quant  │
│ • Leagues    │ │              │ │    <think> reasoning  │
│              │ │              │ │                      │
│              │ │              │ │ 3. ML Ensemble       │
│              │ │              │ │    Grade prediction   │
└──────────────┘ └──────────────┘ └──────────────────────┘
```

**Diagrama 2: Pipeline AI (rezolvare exercițiu)**

```
Utilizator scrie/scanează exercițiu
              │
              ▼
    ┌─────────────────┐
    │ Text exercițiu  │
    │ "Rezolvă x²-5x+6=0"
    └────────┬────────┘
             │
     ┌───────┼───────┐
     ▼       ▼       ▼
┌────────┐┌────────┐┌────────┐
│Math    ││Transf. ││DeepSeek│
│Tutor   ││Custom  ││+LoRA   │
│(reguli)││(18.6M) ││(14B)   │
│        ││        ││        │
│Detectie││BPE tok ││<think> │
│tip ex. ││Generate││Chain   │
│Rezolv. ││autoreg.││of      │
│pas cu  ││        ││Thought │
│pas     ││        ││        │
└───┬────┘└───┬────┘└───┬────┘
    │         │         │
    └────┬────┘─────────┘
         │
         ▼
┌─────────────────────┐
│  Răspuns structurat  │
│  • Pași de rezolvare │
│  • Răspuns final     │
│  • Explicații        │
└─────────────────────┘
```

**Diagrama 3: Pipeline date**

```
Exerciții BAC oficiale (2020-2024)
              │
              ▼
    scripts/collect_data.py
              │
              ▼
    data/raw/exercises_bac.json (242 exerciții)
              │
              ▼
    scripts/augment_data.py + generate_full_curriculum.py
    + generate_extra_exercises.py
              │
              ▼
    data/processed/exercises_merged.json (2,834 exerciții)
              │
    ┌─────────┼──────────┐
    ▼         ▼          ▼
┌────────┐┌────────┐┌────────┐
│Tokeniz.││Train/  ││Backend │
│BPE     ││Val/Test││Import  │
│5,850   ││80/10/10││exerc.  │
│tokeni  ││split   ││DB      │
└───┬────┘└───┬────┘└────────┘
    │         │
    ▼         ▼
┌────────┐┌────────┐
│math_bpe││Antren. │
│.json   ││model   │
│        ││60 epoci│
│        ││M4 MPS  │
└────────┘└────────┘
```

**Diagrama 4: Fluxul utilizatorului în aplicație**

```
Prima deschidere → Onboarding (alege profil M1/M2)
       │
       ▼
    Register/Login (email + parola, JWT)
       │
       ▼
    🏠 Home (Dashboard)
       │
       ├──→ ✏️ Exerciții → Rezolvă → Feedback (corect/greșit)
       │                         → Hints (3 nivele, cost XP)
       │                         → Soluție pas cu pas
       │
       ├──→ 🃏 Flashcards → Study mode → Flip card → Rate (SM-2)
       │
       ├──→ 📷 Scanner → Poză → OCR → Review text → AI Solve
       │
       ├──→ 🦉 Chat AI → Scrie întrebare → Răspuns structurat
       │
       ├──→ 🗺️ Plan AI → Maestrie topicuri → Sesiuni recomandate
       │
       ├──→ 📊 Predicție → Notă estimată + Insights
       │
       ├──→ 🔥 Streaks → Check-in zilnic → Heatmap activitate
       │
       └──→ ⚙️ Setări → Profil, Logout, Sunete, Despre
```

### 3.5 Descrierea blocurilor (1-2 pagini fiecare)

**Bloc A: Frontend — Aplicația mobilă**

Aplicația mobilă este dezvoltată cu React Native și Expo SDK 54, oferind o singură bază de cod pentru iOS și Android. Navigarea folosește Expo Router 6 cu routing file-based (fiecare fișier din `app/` devine un ecran automat).

Design system custom „DUO" cu temă dark profesională: 15 culori de accent (verde, albastru, roșu, orange etc.), 9 stiluri tipografice (Inter font, de la 11px caption la 28px heading), tokeni de design (border-radius 14/18/999, border-bottom 3px pentru efect de buton apăsat).

Ecrane principale:
- **Home** — salut personalizat, progress ring zilnic, XP bar, daily challenge cu countdown, learning path cu 8 lecții, quick actions
- **Exercises** — progress bar animat, heart system (3 vieți), filtru pe subiecte (I/II/III), input răspuns, 3 nivele de hints, feedback cu confetti/shake animation, modal soluție cu navigare pași
- **Flashcards** — 24 carduri pe 4 categorii, animație flip 3D cu Reanimated, rating calitate (Hard/OK/Easy), algoritm SM-2 pentru repetare spațiată
- **Streaks** — counter mare cu emoji, heatmap activitate stil GitHub (12 săptămâni), XP & Level cards, streak freeze, daily challenges, achievements grid
- **Scanner** — 3 faze (capture → review → solution), camera/galerie cu ImagePicker, OCR extraction cu badge acuratețe, editor text extras, solver AI
- **Chat AI** — mesaje bubble (user: verde, AI: card), typing indicator animat, răspunsuri structurate (pași, formule, soluții), suggestion chips
- **Study Plan AI** — hero stats (maestrie %, zile BAC, timp plan), recomandare AI bazată pe puncte slabe, sesiuni prioritizate (review/practice/theory/challenge), mastery grid pe topicuri cu bară progres
- **Analytics** — predicție notă (0-10) cu confidence interval, breakdown pe subiecte, learning insights

13 componente reutilizabile: DuoButton, AnimatedPressable, ProgressRing, HeartBar, StreakBadge, Toast, StudyHeatmap, ConfettiAnimation, XPPopup, SolutionView, Skeleton, EmptyState, ErrorState.

3 context providers: AuthContext (JWT, user state), ToastContext (notificări), SoundContext (sunete/haptics).

API service layer (`services/api.ts`) — wrapper peste fetch care adaugă automat Authorization Bearer header, parsează JSON, aruncă erori pe status != 200.

**Bloc B: Backend — API REST**

FastAPI (Python) cu arhitectură router + service. 12 routere REST:
- `auth` — register, login, /me (JWT cu bcrypt)
- `exercises` — CRUD, submit-answer, solution, hints, quick-practice
- `chat` — conversație cu AI tutor, detectare concept/exercițiu
- `solver` — rezolvare cu Transformer custom sau Qwen+LoRA
- `scanner` — OCR cu Google Cloud Vision, normalizare notație matematică
- `stats` — statistici generale, detaliate per subiect/topic, activity heatmap
- `ml` — predicție notă, model info, insights (puncte forte/slabe, trend)
- `gamification` — XP, levels (20 nivele), streaks, streak freeze, achievements (15+)
- `leagues` — ligi săptămânale, leaderboard, promovare/retrogradare
- `daily-challenge` — 3 provocări zilnice cu recompense
- `recommender` — recomandări personalizate content-based
- `tokenizer` — acces la tokenizer-ul BPE

7 servicii: AdaptiveLearning (SM-2 + prioritizare), MathTutor (solver rule-based, 10 tipuri exerciții), MathExplainer (dicționar concepte cu formule, reguli, exemple, greșeli frecvente), Recommender (content-based filtering), Gamification (XP calculus, level thresholds), Leagues (ranking săptămânal), Math Tutor (rezolvare deterministă pas cu pas).

PostgreSQL cu colecții: users, exercises (2,834), attempts, achievements, streaks, leagues.

**Bloc C: Modele AI**

3 modele complementare:

1. **Transformer Custom (18.6M parametri)** — decoder-only, 8 layers, antrenat de la zero pe PyTorch. Vocabular BPE de 5,850 tokeni adaptat matematic. Antrenat pe Apple M4 (MPS) în 60 epoci (~60 min). Format: `<BOS> question <SEP> answer <SEP> step1 <SEP> step2 <EOS>`. Best validation loss: 1.543.

2. **DeepSeek-R1-Distill-Qwen-14B + LoRA** — model pre-antrenat de 14B parametri, quantizat 4-bit (NF4). Fine-tuned cu LoRA (rank=16) pe 2,834 exerciții BAC. Format `<think>` chain-of-thought: modelul „gândește" vizibil înainte de răspunsul final. Antrenat pe Kaggle GPU T4 x2.

3. **Math Tutor Rule-Based** — solver deterministic fără ML. Detectează tipul exercițiului (ecuație, derivată, integrală, limită, determinant, combinări etc.) cu regex, apoi aplică reguli matematice explicite pas cu pas. Acoperă 10+ tipuri de exerciții. Avantaj: 100% corect pentru tipurile suportate, instantaneu, fără GPU.

**Bloc D: Pipeline de Date**

Dataset-ul final conține 2,834 exerciții cu soluții complete, acoperind materia de cls 9-12:
- Ecuații (gradul 1, 2, modul, iraționale, exponențiale, logaritmice)
- Derivate (elementare, produs, cât, lanț, trigonometrice, avansate)
- Integrale (nedefinite, definite, prin părți, substituție)
- Limite (infinit, factorizare, L'Hôpital, remarcabile)
- Matrice și determinanți (2×2, 3×3, inversă, rang)
- Numere complexe (operații, modul, conjugat, formă trigonometrică)
- Combinatorică (permutări, aranjamente, combinări, binom Newton)
- Probabilități (clasică, condiționată, distribuție binomială)
- Geometrie (plan, spațiu, analitică)
- Trigonometrie (valori, ecuații, formule, identități)
- Progresii (aritmetice, geometrice)
- Funcții (grad 1, 2, studiu complet, monotonie, extreme, asimptote)

Surse: exerciții BAC oficiale (2020-2024), generare programatică cu variații de parametri, augmentare automată.

---

## Capitolul 4. Detalii Tehnice

### 4.1 Antrenamentul Transformer

**Hiperparametri:**
- Optimizer: AdamW (lr=3e-4, betas=(0.9, 0.95), weight_decay=0.01)
- Scheduler: Warmup liniar 10% + Cosine Decay
- Gradient clipping: max_norm=1.0
- Batch size: 16, Secvență max: 512
- Epoci: 60, Device: Apple M4 (MPS)

**Rezultate antrenare:**
- Train loss: 6.17 → 0.146 (convergență excelentă)
- Validation loss: 4.77 → 1.543 (best la epoca 18)
- Test loss: 2.228

**Exemple generare:**
- Input: „Rezolvă ecuația: 2x + 3 = 7" → Output: „4 | Step 1: 2x = 4 | Step 2: x = 4" ✓
- Input: „Calculează det[[3,1],[2,4]]" → Output: „5 | Step 1: det = 2·4 - 1·1 = 5" (aproape corect)

### 4.2 Fine-tuning LoRA

**Format antrenare cu `<think>`:**
```
<|im_start|>system
Gândește pas cu pas în blocul <think>, apoi dă răspunsul.<|im_end|>
<|im_start|>user
Rezolvă x² - 5x + 6 = 0<|im_end|>
<|im_start|>assistant
<think>
a=1, b=-5, c=6
Δ = 25 - 24 = 1
x₁ = (5-1)/2 = 2, x₂ = (5+1)/2 = 3
</think>
Răspuns: x₁ = 2, x₂ = 3<|im_end|>
```

### 4.3 OCR Pipeline

1. Utilizator face poză → ImagePicker (Expo)
2. Imagine trimisă ca FormData → `/api/scanner/ocr`
3. Backend trimite la Google Cloud Vision (DOCUMENT_TEXT_DETECTION)
4. Post-procesare: Unicode superscripts → `^n`, simboluri → ASCII (`×→*`, `÷→/`, `√→sqrt`, `π→pi`)
5. Regex: `x2 → x^2` (artefact OCR comun)
6. Text returnat cu scor de confidence

### 4.4 Gamificație

| Feature | Detalii |
|---------|---------|
| XP | +10 per exercițiu corect, bonus streak |
| Nivele | 20 (Începător → Maestru BAC) |
| Streaks | Zile consecutive, freeze system |
| Hearts | 3 pe sesiune, -1 la greșit |
| Achievements | 15+ (prima ecuație, 7 zile streak, 100 ex...) |
| Ligi | Bronz→Argint→Aur→Diamant, leaderboard săptămânal |
| Daily Challenges | 3/zi cu XP bonus |
| Heatmap | Vizualizare activitate 12 săptămâni (stil GitHub) |

### 4.5 Securitate

- Autentificare JWT cu Bearer token
- Parole hash bcrypt
- API service layer centralizat — token adăugat automat la fiecare request
- Validare input cu Pydantic (backend)

---

## Capitolul 5. Concluzii

### 5.1 Realizări

SmartBAC integrează cu succes multiple tehnici AI într-o aplicație mobilă educațională completă:

1. **Model Transformer de la zero** (18.6M parametri) — demonstrează înțelegerea profundă a arhitecturii, de la tokenizer BPE la generare autoregresivă
2. **Fine-tuning eficient cu LoRA** pe LLM de 14B parametri — tehnici moderne de adaptare modele mari cu resurse limitate
3. **Pipeline ML complet** — colectare date → augmentare → tokenizer → antrenare → evaluare → deployment
4. **3 abordări AI complementare** — Transformer custom + LLM fine-tuned + solver rule-based
5. **Învățare adaptivă** — SM-2 + detecție puncte slabe + plan personalizat
6. **Gamificație completă** — XP, nivele, streak-uri, achievements, ligi, heatmap
7. **Aplicație completă** — 15+ ecrane, design system coerent, animații, cross-platform

### 5.2 Contribuții originale

- Transformer antrenat de la zero pentru matematică în limba română
- Tokenizer BPE cu protecție LaTeX și operatori matematici
- Format `<think>` chain-of-thought pentru transparența raționamentului
- Combinație unică: model custom + LLM + rule-based solver
- Dataset 2,834 exerciții BAC cu soluții complete cls 9-12
- Study heatmap + mastery tracking per topic

### 5.3 Limitări

- Modelul custom (18.6M) limitât la exerciții simple
- Dependență Google Cloud Vision pentru OCR
- Necesită internet pentru majoritatea funcțiilor
- Dataset relativ mic pentru training LLM

### 5.4 Direcții viitoare

- Suport offline cu SQLite
- OCR custom cu model ML (fără API extern)
- Extindere alte materii (Fizică, Chimie)
- Push notifications remindere studiu
- Export rapoarte progres (PDF)
- A/B testing gamificație
