# Viza 2 - Arhitectura Sistemului BAC Prep AI

## Cuprins
1. [Arhitectura generala](#1-arhitectura-generala)
2. [Structura bazei de date](#2-structura-bazei-de-date)
3. [Protocoale de comunicatie](#3-protocoale-de-comunicatie)
4. [Descrierea fluxurilor](#4-descrierea-fluxurilor)
5. [Componenta AI/ML](#5-componenta-aiml)

---

## 1. Arhitectura generala

### 1.1. Diagrama arhitecturala (3-tier + AI)

```
┌─────────────────────────────────────────────────────────────────┐
│                     FRONTEND (Client)                          │
│              Expo React Native + TypeScript                     │
│                                                                 │
│  ┌──────┐ ┌──────────┐ ┌──────────┐ ┌────┐ ┌──────────┐       │
│  │ Home │ │Exercises │ │Flashcards│ │Chat│ │ Streaks  │       │
│  └──┬───┘ └────┬─────┘ └────┬─────┘ └─┬──┘ └────┬─────┘       │
│     │          │            │          │          │              │
│  ┌──┴──────────┴────────────┴──────────┴──────────┴──────┐      │
│  │              HTTP Client (fetch API)                   │      │
│  │              API_BASE_URL: http://<server>:5000        │      │
│  └───────────────────────┬───────────────────────────────┘      │
└──────────────────────────┼──────────────────────────────────────┘
                           │ HTTP/REST (JSON)
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                     BACKEND (Server)                             │
│                   FastAPI + Python 3.12                          │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                    API Gateway (FastAPI)                    │  │
│  │  CORS middleware │ JWT Auth │ Request validation (Pydantic) │  │
│  └────────┬───────────────┬───────────────┬───────────────────┘  │
│           │               │               │                      │
│  ┌────────▼────┐  ┌───────▼──────┐  ┌─────▼──────┐              │
│  │   Routers   │  │   Services   │  │  AI Models │              │
│  │             │  │              │  │            │              │
│  │ /auth       │  │ Gamification │  │ Transformer│              │
│  │ /exercises  │  │ Recommender  │  │ (custom)   │              │
│  │ /solver     │  │ Adaptive     │  │            │              │
│  │ /chat       │  │ Math Tutor   │  │ Qwen+LoRA  │              │
│  │ /stats      │  │ Math Explain │  │ (fine-tune)│              │
│  │ /ml         │  │ Leagues      │  │            │              │
│  │ /gamificati.│  │ Tokenizer    │  │ Grade      │              │
│  │ /recommender│  │              │  │ Predictor  │              │
│  │ /daily-chal.│  │              │  │ (sklearn)  │              │
│  │ /leagues    │  │              │  │            │              │
│  │ /tokenizer  │  │              │  │ BPE Token. │              │
│  └─────────────┘  └──────────────┘  └────────────┘              │
│           │                                                      │
│  ┌────────▼──────────────────────────────────────────────────┐  │
│  │                    Database Layer                          │  │
│  │              PyMongo (MongoDB Driver)                      │  │
│  └───────────────────────┬───────────────────────────────────┘  │
└──────────────────────────┼──────────────────────────────────────┘
                           │ MongoDB Wire Protocol (port 27017)
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                     DATABASE (MongoDB)                            │
│                                                                  │
│  Collections:                                                    │
│  ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌────────────────────┐  │
│  │  users  │ │exercises │ │ attempts │ │ user_achievements  │  │
│  └─────────┘ └──────────┘ └──────────┘ └────────────────────┘  │
│  ┌─────────────────┐ ┌──────────┐ ┌────────────┐ ┌──────────┐  │
│  │exam_simulations │ │ leagues  │ │daily_chall.│ │chat_hist.│  │
│  └─────────────────┘ └──────────┘ └────────────┘ └──────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2. Tehnologii utilizate

| Componenta | Tehnologie | Versiune | Scop |
|------------|-----------|----------|------|
| Frontend | Expo React Native | SDK 52 | Aplicatie mobila cross-platform |
| Frontend Language | TypeScript | 5.x | Tipizare statica |
| Backend Framework | FastAPI | 0.110+ | API REST performant, async |
| Backend Language | Python | 3.12 | Logica server + AI/ML |
| Baza de date | MongoDB | 7.x | Stocare documente NoSQL |
| Driver DB | PyMongo | 4.x | Comunicare cu MongoDB |
| Autentificare | JWT (PyJWT) | - | Token-based auth |
| AI - Transformer | PyTorch | 2.x | Model custom de la zero |
| AI - Fine-tuning | HuggingFace + PEFT | - | LoRA pe Qwen2.5-Math |
| AI - Tokenizer | Custom BPE | - | Tokenizare matematica |
| ML - Predictie | scikit-learn | 1.x | Predictor nota BAC |

### 1.3. Structura directoarelor

```
bac-prep-ai/
├── frontend/                    # Aplicatia mobila
│   ├── app/
│   │   ├── (tabs)/              # 15 ecrane cu tab navigation
│   │   ├── _layout.tsx          # Root layout + providers
│   │   ├── onboarding.tsx       # Ecran onboarding
│   │   └── admin.tsx            # Panou admin
│   ├── components/              # 18 componente reutilizabile
│   ├── constants/               # Configurari (API, tema, tipografie)
│   ├── contexts/                # React Context (Toast, Sound)
│   └── hooks/                   # Custom hooks
├── backend/                     # Server API
│   ├── main.py                  # Entry point FastAPI
│   ├── database.py              # Conexiune MongoDB
│   ├── schemas.py               # Modele Pydantic (validare)
│   ├── routers/                 # 12 routere API
│   ├── models/                  # Modele date + ML artifacts
│   └── services/                # 7 servicii business logic
├── ai/                          # Componenta AI
│   ├── tokenizer/               # BPE tokenizer custom
│   ├── transformer/             # Transformer autoregresiv custom
│   └── finetune/                # Qwen2.5-Math + LoRA
├── data/                        # Date antrenament
│   ├── raw/                     # Date brute (242 exercitii)
│   ├── augmented/               # Date augmentate (5203 exercitii)
│   └── splits/                  # Train/Val/Test splits
│       ├── transformer/         # Format seq2seq
│       └── finetune/            # Format ChatML (JSONL)
└── scripts/                     # Pipeline date
    ├── collect_data.py
    ├── augment_data.py
    ├── generate_all_bac.py
    └── split_data.py
```

---

## 2. Structura bazei de date

### 2.1. Diagrama Entitate-Relatie (ERD)

```
┌──────────────────────┐         ┌──────────────────────┐
│       USERS          │         │     EXERCISES         │
├──────────────────────┤         ├──────────────────────┤
│ _id: int (PK)        │         │ _id: int (PK)        │
│ email: string (UQ)   │         │ question: string     │
│ username: string (UQ)│         │ answer: string       │
│ password_hash: string│         │ difficulty: int (1-5) │
│ profile: "M1"|"M2"  │         │ topic: string        │
│ xp: int             │         │ subject: int (1-3)   │
│ level: int           │         │ exercise_type: string│
│ current_streak: int  │         │ profile: "M1"|"M2"   │
│ best_streak: int     │         │ solution: string     │
│ streak_freezes: int  │         │ solution_steps: array│
│ last_activity: date  │         │ hints: array         │
│ created_at: datetime │         │ explanation: string  │
│ updated_at: datetime │         │ formula: string      │
└──────┬───────────────┘         │ latex: string        │
       │                         │ points: int          │
       │ 1:N                     └──────┬───────────────┘
       │                                │
       ▼                                │ 1:N
┌──────────────────────┐                │
│      ATTEMPTS        │◄───────────────┘
├──────────────────────┤
│ _id: int (PK)        │
│ user_id: int (FK)    │───→ USERS._id
│ exercise_id: int (FK)│───→ EXERCISES._id
│ user_answer: string  │
│ is_correct: boolean  │
│ time_spent: int (sec)│
│ created_at: datetime │
└──────────────────────┘

┌──────────────────────┐         ┌──────────────────────┐
│   ACHIEVEMENTS       │         │  USER_ACHIEVEMENTS   │
├──────────────────────┤         ├──────────────────────┤
│ _id: int (PK)        │◄────── │ achievement_id: int  │
│ name: string         │   1:N  │ user_id: int (FK)    │───→ USERS._id
│ description: string  │         │ unlocked_at: datetime│
│ icon: string         │         └──────────────────────┘
│ xp: int              │              (UQ: user_id + achievement_id)
│ category: string     │
└──────────────────────┘

┌──────────────────────┐         ┌──────────────────────────┐
│  EXAM_SIMULATIONS    │         │  DAILY_CHALLENGE_ATTEMPTS │
├──────────────────────┤         ├──────────────────────────┤
│ _id: int (PK)        │         │ user_id: int (FK)        │
│ user_id: int (FK)    │         │ date: string (YYYY-MM-DD)│
│ score_subject1: int  │         │ exercise_id: int         │
│ score_subject2: int  │         │ is_correct: boolean      │
│ score_subject3: int  │         │ attempt_count: int       │
│ total_score: int     │         │ submitted_at: datetime   │
│ time_spent: int      │         └──────────────────────────┘
│ completed: boolean   │              (UQ: user_id + date)
│ started_at: datetime │
│ completed_at: datetime│
└──────────────────────┘

┌──────────────────────┐         ┌──────────────────────┐
│      LEAGUES         │         │    CHAT_HISTORY      │
├──────────────────────┤         ├──────────────────────┤
│ user_id: int (FK)    │         │ user_id: int (FK)    │
│ week_start: datetime │         │ message: string      │
│ league: string       │         │ response: string     │
│ weekly_xp: int       │         │ intent: string       │
└──────────────────────┘         │ timestamp: datetime  │
  (UQ: user_id + week_start)     └──────────────────────┘

┌──────────────────────────────┐
│  USER_EXERCISE_HISTORY       │
│  (Adaptive Learning / SRS)   │
├──────────────────────────────┤
│ user_id: int (FK)            │
│ exercise_id: int (FK)        │
│ next_review: datetime        │
│ topic: string                │
└──────────────────────────────┘
  (UQ: user_id + exercise_id)
```

### 2.2. Descrierea colectiilor MongoDB

#### **users** - Utilizatorii aplicatiei
| Camp | Tip | Constrangeri | Descriere |
|------|-----|-------------|-----------|
| `_id` | int | PK, auto-increment | Identificator unic |
| `email` | string | UNIQUE, NOT NULL | Adresa email |
| `username` | string | UNIQUE, 3-80 chars | Nume utilizator |
| `password_hash` | string | NOT NULL | Parola hashuita (bcrypt) |
| `profile` | string | "M1" sau "M2" | Profilul BAC (Mate-Info / Tehnologic) |
| `xp` | int | >= 0, default 0 | Puncte experienta |
| `level` | int | >= 1 | Nivel calculat din XP |
| `current_streak` | int | >= 0 | Streak curent (zile consecutive) |
| `best_streak` | int | >= 0 | Cel mai lung streak |
| `streak_freezes` | int | >= 0, default 3 | Inghetari streak disponibile |
| `last_activity` | datetime | | Ultima activitate |
| `created_at` | datetime | auto | Data inregistrarii |

#### **exercises** - Exercitii BAC
| Camp | Tip | Constrangeri | Descriere |
|------|-----|-------------|-----------|
| `_id` | int | PK, auto-increment | Identificator unic |
| `question` | string | NOT NULL | Enuntul exercitiului |
| `answer` | string | NOT NULL | Raspunsul corect |
| `difficulty` | int | 1-5 | Nivel dificultate |
| `topic` | string | | Tema (ex: "Derivate") |
| `subject` | int | 1-3 | Subiectul BAC (I, II, III) |
| `exercise_type` | string | enum | Tipul: equation, derivative, limit, integral, matrix, vector, combinatorics, probability, geometry, function, sequence, trigonometry, complex_number |
| `profile` | string | "M1"/"M2"/"BOTH" | Profilul BAC |
| `solution_steps` | array | | Pasi rezolvare structurati |
| `hints` | array | | Indicii progresive |
| `latex` | string | | Formula LaTeX |

#### **attempts** - Incercari utilizatori
| Camp | Tip | Constrangeri | Descriere |
|------|-----|-------------|-----------|
| `_id` | int | PK | Identificator |
| `user_id` | int | FK → users | Utilizatorul |
| `exercise_id` | int | FK → exercises | Exercitiul |
| `user_answer` | string | | Raspunsul dat |
| `is_correct` | boolean | | Corectitudine |
| `time_spent` | int | secunde | Timp petrecut |
| `created_at` | datetime | auto | Timestamp |

### 2.3. Indexi MongoDB

```javascript
// users
db.users.createIndex({ "email": 1 }, { unique: true })
db.users.createIndex({ "username": 1 }, { unique: true })

// exercises
db.exercises.createIndex({ "topic": 1 })
db.exercises.createIndex({ "subject": 1 })
db.exercises.createIndex({ "profile": 1 })
db.exercises.createIndex({ "exercise_type": 1 })

// attempts
db.attempts.createIndex({ "user_id": 1 })
db.attempts.createIndex({ "exercise_id": 1 })
db.attempts.createIndex({ "created_at": -1 })

// user_achievements
db.user_achievements.createIndex({ "user_id": 1, "achievement_id": 1 }, { unique: true })

// user_exercise_history (SRS)
db.user_exercise_history.createIndex({ "user_id": 1, "exercise_id": 1 }, { unique: true })
db.user_exercise_history.createIndex({ "user_id": 1, "next_review": 1 })

// daily_challenge_attempts
db.daily_challenge_attempts.createIndex({ "user_id": 1, "date": 1 }, { unique: true })

// leagues
db.leagues.createIndex({ "week_start": 1, "league": 1 })
db.leagues.createIndex({ "user_id": 1, "week_start": 1 }, { unique: true })

// chat_history
db.chat_history.createIndex({ "user_id": 1, "timestamp": -1 })
```

---

## 3. Protocoale de comunicatie

### 3.1. Comunicatie Frontend ↔ Backend

| Aspect | Detalii |
|--------|---------|
| **Protocol** | HTTP/1.1 over TCP |
| **Format date** | JSON (application/json) |
| **Arhitectura API** | REST (Representational State Transfer) |
| **Autentificare** | JWT (JSON Web Token) - Bearer token |
| **Port server** | 5000 |
| **CORS** | Activat pentru toate originile (development) |

#### Structura request HTTP tipic:
```
POST /api/exercises/submit-answer HTTP/1.1
Host: 192.168.0.85:5000
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiI...

{
  "exercise_id": 42,
  "answer": "x = 2",
  "user_id": 1,
  "time_spent": 45
}
```

#### Structura response HTTP tipic:
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "correct": true,
  "correct_answer": "x = 2",
  "message": "Corect! +10 XP",
  "new_achievements": []
}
```

### 3.2. Comunicatie Backend ↔ MongoDB

| Aspect | Detalii |
|--------|---------|
| **Protocol** | MongoDB Wire Protocol (binary, over TCP) |
| **Port** | 27017 (default) |
| **Driver** | PyMongo 4.x (sincron) |
| **Conexiune** | Connection string: `mongodb://localhost:27017` |
| **Baza de date** | `bac_prep_ai` |

### 3.3. Comunicatie cu HuggingFace (AI models)

| Aspect | Detalii |
|--------|---------|
| **Protocol** | HTTPS |
| **Endpoint** | `https://huggingface.co/Qwen/Qwen2.5-Math-1.5B` |
| **Scop** | Download model pre-antrenat |
| **Format weights** | SafeTensors |
| **Frecventa** | O singura data (se cacheaza local) |

### 3.4. Endpoints API complete

#### Auth (`/api/auth`)
| Metoda | Endpoint | Descriere |
|--------|----------|-----------|
| POST | `/api/auth/register` | Inregistrare cont nou |
| POST | `/api/auth/login` | Autentificare |
| GET | `/api/auth/me` | Profil utilizator curent |
| PUT | `/api/auth/me` | Actualizare profil |
| POST | `/api/auth/refresh` | Reinnoiere token JWT |

#### Exercises (`/api/exercises`)
| Metoda | Endpoint | Descriere |
|--------|----------|-----------|
| GET | `/api/exercises` | Lista exercitii (cu filtre) |
| GET | `/api/exercises/{id}` | Exercitiu specific |
| GET | `/api/exercises/next` | Urmatorul exercitiu (adaptiv) |
| GET | `/api/exercises/quick-practice` | Exercitii teme slabe |
| POST | `/api/exercises/submit-answer` | Trimitere raspuns |
| GET | `/api/exercises/{id}/solution` | Rezolvare detaliata |
| GET | `/api/exercises/{id}/hints` | Indicii progresive |

#### Solver (`/api/solver`)
| Metoda | Endpoint | Descriere |
|--------|----------|-----------|
| POST | `/api/solver/solve` | Rezolvare cu AI |
| GET | `/api/solver/models` | Modele AI disponibile |

#### Chat (`/api/chat`)
| Metoda | Endpoint | Descriere |
|--------|----------|-----------|
| POST | `/api/chat` | Mesaj catre tutorul AI |
| GET | `/api/chat/knowledge` | Baza de cunostinte |

#### Statistics & ML (`/api/stats`, `/api/ml`)
| Metoda | Endpoint | Descriere |
|--------|----------|-----------|
| GET | `/api/stats` | Statistici de baza |
| GET | `/api/stats/detailed` | Statistici per subiect |
| GET | `/api/stats/analytics/detailed` | Analitica avansata |
| GET | `/api/ml/predict-grade` | Predictie nota BAC |
| GET | `/api/ml/insights` | Insights personalizate |

#### Gamification (`/api/gamification`)
| Metoda | Endpoint | Descriere |
|--------|----------|-----------|
| GET | `/api/gamification/stats` | XP, nivel, streak |
| GET | `/api/gamification/achievements` | Lista achievements |
| POST | `/api/gamification/streak/freeze` | Folosire streak freeze |

#### Other
| Metoda | Endpoint | Descriere |
|--------|----------|-----------|
| GET | `/api/recommender/exercises` | Recomandari personalizate |
| GET | `/api/daily-challenge` | Provocarea zilei |
| POST | `/api/daily-challenge/submit` | Raspuns provocare |
| GET | `/api/leagues` | Info liga utilizator |
| GET | `/api/leagues/leaderboard` | Clasament liga |

---

## 4. Descrierea fluxurilor

### 4.1. Flux de autentificare

```
┌────────┐                    ┌────────┐                 ┌────────┐
│Frontend│                    │ Backend│                 │MongoDB │
└───┬────┘                    └───┬────┘                 └───┬────┘
    │                             │                          │
    │  POST /api/auth/register    │                          │
    │  {email, username, pass}    │                          │
    │────────────────────────────>│                          │
    │                             │  Check email unique      │
    │                             │─────────────────────────>│
    │                             │  <── result              │
    │                             │<─────────────────────────│
    │                             │                          │
    │                             │  Hash password (bcrypt)  │
    │                             │  Insert user document    │
    │                             │─────────────────────────>│
    │                             │  <── created             │
    │                             │<─────────────────────────│
    │                             │                          │
    │                             │  Generate JWT (24h)      │
    │  {token, user}              │                          │
    │<────────────────────────────│                          │
    │                             │                          │
    │  Subsequent requests:       │                          │
    │  Authorization: Bearer JWT  │                          │
    │────────────────────────────>│                          │
    │                             │  Decode & verify JWT     │
    │                             │  Fetch user from DB      │
    │  {response data}            │                          │
    │<────────────────────────────│                          │
```

### 4.2. Flux de rezolvare exercitiu

```
┌────────┐                    ┌────────┐          ┌────────┐    ┌──────────┐
│Frontend│                    │ Backend│          │MongoDB │    │AI Models │
└───┬────┘                    └───┬────┘          └───┬────┘    └────┬─────┘
    │                             │                   │              │
    │  GET /api/exercises         │                   │              │
    │  ?profile=M1&subject=1      │                   │              │
    │────────────────────────────>│                   │              │
    │                             │  Query exercises  │              │
    │                             │──────────────────>│              │
    │  {exercises: [...]}         │  <── results      │              │
    │<────────────────────────────│<──────────────────│              │
    │                             │                   │              │
    │  [Utilizatorul rezolva]     │                   │              │
    │                             │                   │              │
    │  POST /submit-answer        │                   │              │
    │  {exercise_id, answer,      │                   │              │
    │   user_id, time_spent}      │                   │              │
    │────────────────────────────>│                   │              │
    │                             │  Fetch exercise   │              │
    │                             │──────────────────>│              │
    │                             │  <── exercise     │              │
    │                             │<──────────────────│              │
    │                             │                   │              │
    │                             │  Compare answers  │              │
    │                             │  (case-insensitive)              │
    │                             │                   │              │
    │                             │  Save attempt     │              │
    │                             │──────────────────>│              │
    │                             │                   │              │
    │                             │  Update XP (+10)  │              │
    │                             │──────────────────>│              │
    │                             │                   │              │
    │                             │  Update streak    │              │
    │                             │──────────────────>│              │
    │                             │                   │              │
    │                             │  Check achievem.  │              │
    │                             │──────────────────>│              │
    │                             │                   │              │
    │  {correct: true,            │                   │              │
    │   message: "Corect! +10 XP",│                  │              │
    │   new_achievements: [...]}  │                   │              │
    │<────────────────────────────│                   │              │
    │                             │                   │              │
    │  [Daca gresit → cere hint]  │                   │              │
    │  GET /{id}/hints?level=1    │                   │              │
    │────────────────────────────>│                   │              │
    │  {hints, formula, xp_cost}  │                   │              │
    │<────────────────────────────│                   │              │
```

### 4.3. Flux AI Solver (rezolvare cu AI)

```
┌────────┐              ┌────────┐           ┌─────────────┐    ┌──────────┐
│Frontend│              │ Backend│           │ Transformer │    │Qwen+LoRA │
│ (Chat) │              │ Router │           │  (custom)   │    │(finetune)│
└───┬────┘              └───┬────┘           └──────┬──────┘    └────┬─────┘
    │                       │                       │                │
    │ POST /api/solver/solve│                       │                │
    │ {question, model:     │                       │                │
    │  "transformer"}       │                       │                │
    │──────────────────────>│                       │                │
    │                       │                       │                │
    │                       │  if model="transformer":               │
    │                       │  1. Load BPE tokenizer│                │
    │                       │  2. Encode question   │                │
    │                       │  3. Build input:       │                │
    │                       │     <BOS> q <SEP>     │                │
    │                       │──────────────────────>│                │
    │                       │                       │                │
    │                       │                       │ Generate       │
    │                       │                       │ (top-k=30,    │
    │                       │                       │  temp=0.5)    │
    │                       │                       │                │
    │                       │  output tokens        │                │
    │                       │<──────────────────────│                │
    │                       │  4. Decode tokens     │                │
    │                       │  5. Parse answer+steps│                │
    │                       │                       │                │
    │                       │  if model="qwen":     │                │
    │                       │  1. Format ChatML     │                │
    │                       │     prompt            │                │
    │                       │──────────────────────────────────────>│
    │                       │                       │                │
    │                       │                       │  Generate with │
    │                       │                       │  LoRA adapters │
    │                       │  response text        │                │
    │                       │<──────────────────────────────────────│
    │                       │  2. Parse response    │                │
    │                       │                       │                │
    │ {answer, steps,       │                       │                │
    │  model_used,          │                       │                │
    │  confidence}          │                       │                │
    │<──────────────────────│                       │                │
```

### 4.4. Flux de recomandare personalizata

```
┌────────┐              ┌────────┐           ┌──────────┐
│Frontend│              │Recomm. │           │ MongoDB  │
└───┬────┘              │Service │           └────┬─────┘
    │                   └───┬────┘                │
    │ GET /recommender/     │                     │
    │ exercises?user_id=1   │                     │
    │──────────────────────>│                     │
    │                       │                     │
    │                       │  1. Get all attempts│
    │                       │    for user_id      │
    │                       │────────────────────>│
    │                       │  <── attempts       │
    │                       │<────────────────────│
    │                       │                     │
    │                       │  2. Calculate per-  │
    │                       │     topic accuracy  │
    │                       │                     │
    │                       │  3. Identify:       │
    │                       │  weak (< 60%)       │
    │                       │  strong (>= 60%)    │
    │                       │                     │
    │                       │  4. Priority query: │
    │                       │  P1: Unsolved from  │
    │                       │      weak topics    │
    │                       │────────────────────>│
    │                       │  <── exercises      │
    │                       │<────────────────────│
    │                       │                     │
    │                       │  P2: Harder from    │
    │                       │      strong topics  │
    │                       │────────────────────>│
    │                       │                     │
    │                       │  P3: Random unsolved│
    │                       │────────────────────>│
    │                       │                     │
    │ {exercises,           │                     │
    │  weak_topics,         │                     │
    │  strong_topics,       │                     │
    │  reason}              │                     │
    │<──────────────────────│                     │
```

### 4.5. Flux gamification (XP, Nivele, Achievements)

```
┌─────────────────────────────────────────────────────┐
│              SISTEM GAMIFICATION                     │
│                                                      │
│  Actiune utilizator          XP castigat             │
│  ─────────────────          ──────────               │
│  Raspuns corect              +10 XP                  │
│  Daily challenge corect      +25 XP (prima)          │
│  Daily challenge retry       +15 XP                  │
│  Hint nivel 2                -5 XP                   │
│  Hint nivel 3                -10 XP                  │
│                                                      │
│  ┌──────────────────────────────────┐                │
│  │        LEVEL SYSTEM              │                │
│  │                                  │                │
│  │  XP → Nivel → Nume nivel        │                │
│  │  0      1     Incepator          │                │
│  │  100    2     Explorator         │                │
│  │  250    3     ...                │                │
│  │  500    4     ...                │                │
│  │  ...    ...   ...                │                │
│  └──────────────────────────────────┘                │
│                                                      │
│  ┌──────────────────────────────────┐                │
│  │      STREAK SYSTEM               │                │
│  │                                  │                │
│  │  Activitate zilnica → streak++   │                │
│  │  Skip zi → streak = 0           │                │
│  │  (sau foloseste streak freeze)   │                │
│  │  3 freeze-uri disponibile        │                │
│  └──────────────────────────────────┘                │
│                                                      │
│  ┌──────────────────────────────────┐                │
│  │      ACHIEVEMENTS                │                │
│  │                                  │                │
│  │  Verificate dupa fiecare submit  │                │
│  │  Ex: "Prima rezolvare corecta"   │                │
│  │  Ex: "10 exercitii la rand"      │                │
│  │  Ex: "Streak de 7 zile"          │                │
│  └──────────────────────────────────┘                │
│                                                      │
│  ┌──────────────────────────────────┐                │
│  │      LEAGUE SYSTEM               │                │
│  │                                  │                │
│  │  Bronz → Argint → Aur →         │                │
│  │  Platina → Diamant               │                │
│  │                                  │                │
│  │  XP saptamanal → clasament       │                │
│  │  Reset weekly                    │                │
│  └──────────────────────────────────┘                │
└─────────────────────────────────────────────────────┘
```

---

## 5. Componenta AI/ML

### 5.1. Pipeline de date

```
┌─────────────────┐     ┌──────────────────┐     ┌────────────────┐
│  exercises_     │     │  augment_data.py  │     │ split_data.py  │
│  database.py    │────>│                   │────>│                │
│  (242 exercitii)│     │  Generare         │     │ Stratificat    │
│                 │     │  programatica     │     │ pe tip         │
└─────────────────┘     │  (5203 exercitii) │     │                │
                        └──────────────────┘     │ 80% train      │
                                                  │ 10% val        │
                                                  │ 10% test       │
                                                  └───────┬────────┘
                                                          │
                                          ┌───────────────┼───────────────┐
                                          ▼               ▼               ▼
                                   ┌────────────┐ ┌────────────┐ ┌────────────┐
                                   │transformer/│ │ finetune/  │ │  raw JSON  │
                                   │ train.json │ │ train.jsonl│ │ train.json │
                                   │ (seq2seq)  │ │ (ChatML)   │ │            │
                                   └────────────┘ └────────────┘ └────────────┘
```

### 5.2. Transformer custom (de la zero)

```
Arhitectura: Decoder-only autoregresiv (stil GPT-2)
Parametri: ~8.7M

Input token IDs
     │
     ▼
Token Embedding (7695 × 256) × sqrt(256)
     │
     ▼
+ Sinusoidal Positional Encoding (precalculat)
     │
     ▼
┌────────────────────────────────────────┐
│  TransformerBlock ×6 (Pre-Norm)        │
│                                        │
│  LayerNorm → Multi-Head Self-Attention │
│  (8 heads, d_k=32, causal mask)       │
│  + Residual connection                 │
│                                        │
│  LayerNorm → FFN (256→1024→256, GELU) │
│  + Residual connection                 │
└────────────────────────────────────────┘
     │
     ▼
LayerNorm final
     │
     ▼
Linear (256 → 7695)  →  Logits
     │
     ▼
Top-k sampling (k=30, temp=0.5)

Antrenament:
  - Optimizer: AdamW (lr=3e-4, betas=0.9/0.95)
  - Scheduler: Warmup 10% + Cosine Decay
  - Loss: CrossEntropy (ignore PAD)
  - Gradient clipping: max_norm=1.0
  - Device: MPS (Apple Silicon M4)
  - Rezultat: val_loss=0.2268, test_loss=0.2359
```

### 5.3. Qwen2.5-Math + LoRA (fine-tuning)

```
Model de baza: Qwen/Qwen2.5-Math-1.5B (1.5 miliarde parametri)

Metoda: LoRA (Low-Rank Adaptation)
  - Rank: 16
  - Alpha: 32
  - Target modules: q_proj, k_proj, v_proj, o_proj,
                    gate_proj, up_proj, down_proj
  - Parametri antrenabili: ~3.7M (0.24% din total)

Quantizare: 4-bit NF4 (reduce VRAM de la ~6GB la ~1.5GB)

Format date: ChatML
  <|im_start|>system
  Esti un asistent de matematica specializat pe exercitii BAC.
  <|im_end|>
  <|im_start|>user
  Rezolva ecuatia: 2x + 3 = 7
  <|im_end|>
  <|im_start|>assistant
  Pasul 1: 2x + 3 = 7
  Pasul 2: 2x = 4
  Pasul 3: x = 2
  Raspuns: x = 2
  <|im_end|>

Antrenament:
  - Platform: Kaggle (GPU T4 16GB)
  - Epoci: 3
  - Batch size: 4 (effective 16 cu gradient accumulation)
  - Optimizer: AdamW 8-bit (paged)
  - Mixed precision: FP16
```

### 5.4. Grade Predictor (ML clasic)

```
Model: Ensemble (scikit-learn)
Fisier: backend/models/grade_predictor_advanced.pkl
Input: Statistici utilizator (attempts, accuracy per subject)
Output: Nota prezisa BAC (1-10)
Minim date: 10 incercari pentru predictie
Formula fallback: 1 + (accuracy × 9)
```

### 5.5. BPE Tokenizer (custom, de la zero)

```
Tip: Byte Pair Encoding (BPE)
Vocab size: 7695 tokeni
Fisier: ai/tokenizer/math_bpe.json

Tokeni speciali:
  <PAD> = 0    (padding)
  <UNK> = 1    (necunoscut)
  <BOS> = 2    (inceput secventa)
  <EOS> = 3    (sfarsit secventa)
  <SEP> = 4    (separator)

Tokeni LaTeX protejati (nu se split):
  \frac, \int, \lim, \sqrt, \sum, \sin, \cos, ...

Tokeni matematici:
  +, -, *, /, =, <, >, (, ), [, ], {, }, ^, _, |
```
