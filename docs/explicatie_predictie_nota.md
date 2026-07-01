# Explicație completă — Sistemul de predicție a notei BAC

## 1. Tehnologii și limbaje folosite

| Componentă | Limbaj | Tehnologii |
|---|---|---|
| Antrenarea modelului | **Python** | scikit-learn, pandas, numpy, joblib (notebook Jupyter pe Kaggle) |
| Backend (API) | **Python** | FastAPI, PyMongo, pickle |
| Frontend (aplicația mobilă) | **TypeScript** | React Native + Expo |
| Baza de date | — | MongoDB (colecțiile `users`, `exercises`, `attempts`) |

## 2. Datele de antrenare

- **`synthetic_attempts.json`** — 8.750 de încercări de exerciții, generate sintetic pentru 150 de elevi cu profiluri diferite (slab / mediu / bun).
- **`student_grades.json`** — nota finală "reală" a fiecăruia din cei 150 de elevi (target-ul `y`, între 1 și 10).
- Fiecare încercare conține: `is_correct`, `time_spent`, `exercise_subject` (1/2/3), `exercise_difficulty` (1–4), `exercise_topic`, `timestamp`.

Problema este una de **regresie supervizată**: din comportamentul elevului în aplicație (X) prezicem nota la BAC (y).

## 3. Feature engineering — cele 30 de variabile

Din lista brută de încercări se calculează un **vector de 30 de features** per elev, grupate astfel:

- **Volum și acuratețe**: total încercări, acuratețe globală, acuratețe pe Subiectul 1/2/3, acuratețe pe fiecare nivel de dificultate (easy/medium/hard/expert).
- **Dinamica învățării**: `learning_trend` (acuratețea pe ultimele încercări minus primele — arată dacă elevul progresează), `difficulty_progression` (dacă abordează exerciții tot mai grele), `recent_accuracy` (ultimele 10).
- **Consistență**: deviația standard a acurateței pe ferestre de încercări, `streak_ratio` și `max_streak_ratio` (serii de răspunsuri corecte consecutive).
- **Timp**: timp mediu/median/deviație, `time_efficiency` (raportul timp pe răspunsuri corecte vs. greșite), `fast_correct_ratio` (răspunde repede ȘI corect), `slow_wrong_ratio` (răspunde încet ȘI greșit).
- **Acoperire**: `topic_diversity` (câte teme diferite a atins), `avg_topic_mastery`, `subject_balance` (cât de echilibrat lucrează pe cele 3 subiecte), `attempt_density` (log(1+n)).

De ce nu dăm direct încercările brute modelului? Pentru că elevii au număr diferit de încercări — features-urile transformă o listă de lungime variabilă într-un vector fix de 30 de numere, comparabil între elevi.

## 4. Antrenarea pe Kaggle (`prezicere-note.ipynb`)

1. **11 modele candidate** antrenate în paralel: Ridge, ElasticNet, SVR, KNN, Random Forest, Extra Trees, Gradient Boosting, HistGradientBoosting, MLP (rețea neuronală), XGBoost + un model "dummy" de referință.
2. Fiecare model e un **Pipeline sklearn**: scalare (StandardScaler/RobustScaler) → regresor → `ClippedRegressor` (limitează predicția la intervalul valid [1, 10]).
3. **Validare încrucișată repetată** (RepeatedKFold: 5 fold-uri × 3 repetări = 15 evaluări per model) — evită norocul unei singure împărțiri a datelor.
4. **Top-5 modele după RMSE** sunt combinate într-un **VotingRegressor** (media predicțiilor celor 5) — varianta cu stacking a fost și ea testată, dar voting a ieșit mai bine pe holdout.
5. **Rezultate pe setul de test (holdout, date nevăzute la antrenare)**:
   - R² = **0.974** (modelul explică 97,4% din variația notelor)
   - MAE = **0.275** (greșește în medie cu ±0,28 puncte din notă)
   - RMSE = **0.392**
6. Modelul final + lista de features + metricile se salvează ca **artifact pickle**: `grade_predictor_perfect.pkl`.

## 5. Integrarea în backend (FastAPI)

Fișiere cheie:
- `backend/models/grade_predictor_perfect.pkl` — modelul antrenat (8,6 MB).
- `backend/ml_predictor_perfect.py` — wrapper-ul care îl încarcă și face predicții.
- `backend/routers/ml.py` — endpoint-ul REST `GET /api/ml/predict-grade?user_id=X`.

Detalii tehnice importante (de știut la întrebări):

1. **Deserializarea pickle**: notebook-ul a definit două clase proprii (`AsRegressor`, `ClippedRegressor`) care au fost serializate ca aparținând modulului `__main__`. La încărcare în backend, un `Unpickler` custom (`_ArtifactUnpickler.find_class`) remapează aceste referințe la clasele redefinite identic în `ml_predictor_perfect.py`. Fără asta, `pickle.load` ar da `AttributeError`.
2. **`extract_features` este portat 1:1 din notebook** — dacă features-urile calculate în producție ar diferi de cele de la antrenare (alt ordin, altă formulă), predicțiile ar fi fără sens. Orice modificare cere reantrenare.
3. **Fluxul unei cereri**:
   - se citesc încercările userului din MongoDB (`attempts`) + metadatele exercițiilor (`exercises` — subiect, dificultate, temă);
   - **sub 3 încercări** → mesaj "rezolvă minim 3 exerciții";
   - **3–9 încercări** → formulă simplă de fallback: `nota = 1 + accuracy × 9`;
   - **≥ 10 încercări** → vectorul de 30 features → `model.predict()` → nota.
4. **Intervalul de încredere** (MIN–MAX din aplicație): deviația standard a predicțiilor celor 5 sub-modele din VotingRegressor × 1,96 (interval ~95%). Dacă sub-modelele sunt de acord → interval îngust → încredere mare.
5. **Lanț de fallback complet**: model Kaggle → modelul vechi local (`AdvancedGradePredictor`) → formula simplă. Aplicația funcționează chiar dacă pkl-ul lipsește.
6. Răspunsul JSON conține: `predicted_grade`, `confidence_interval`, `confidence_level`, `breakdown` pe subiecte (puncte estimate din 30), `insights` (recomandări generate din features) și `model_type: "kaggle_voting_top"`.

## 6. Frontend (React Native / TypeScript)

- Ecranul `frontend/app/(tabs)/analytics.tsx` apelează `GET /api/ml/predict-grade` la deschidere.
- Afișează: gauge circular animat cu nota, chip-urile MIN/MAX (intervalul de încredere), "Performanță pe subiecte" (breakdown-ul), și insights-urile ca recomandări.
- Adresa backend-ului se rezolvă automat: pe telefon ia IP-ul Mac-ului din Expo (`hostUri`), pe web folosește `localhost:5001`.

## 7. Verificarea corectitudinii

Predicțiile modelului integrat au fost comparate cu notele reale din datele de antrenare:

| Elev | Nota reală | Nota prezisă |
|---|---|---|
| user 5 | 2.38 | 2.37 |
| user 3 | 6.60 | 6.66 |
| user 2 | 6.90 | 7.19 |
| user 4 | 8.41 | 8.47 |

## 8. Întrebări probabile la susținere + răspunsuri scurte

**De ce ensemble (Voting) și nu un singur model?**
Media mai multor modele diferite reduce varianța: erorile individuale (în direcții diferite) se compensează. Empiric, voting-ul peste top-5 a avut RMSE mai mic decât orice model individual.

**De ce ai limitat predicția la [1, 10]?**
Regresorii pot extrapola în afara intervalului valid al notelor (ex. 10,3). `ClippedRegressor` aplică `np.clip` ca garanție de domeniu.

**Cum ai evitat overfitting-ul?**
(1) Validare încrucișată repetată 5×3, (2) set de holdout complet separat pentru metricile finale, (3) compararea cu un model dummy de referință, (4) verificarea duplicatelor în date.

**De ce R² atât de mare — nu e suspect?**
Datele sunt sintetice, generate cu reguli consistente (profilul elevului determină comportamentul), deci relația features→notă e mai curată decât în date reale. Notebook-ul chiar are un flag `suspicious_accuracy` care verifică asta. Pe date reale ne-am aștepta la R² mai mic.

**De ce MongoDB și nu SQL?**
Datele sunt documente eterogene (exerciții cu structuri diferite per tip), schema flexibilă se potrivește, iar relațiile complexe lipsesc; agregările necesare se fac simplu în Python.

**Ce e pickle și ce risc are?**
Serializarea nativă Python a obiectelor (aici: pipeline-ul sklearn antrenat). Risc: execută cod la deserializare, deci se încarcă doar fișiere din surse proprii; și e sensibil la versiunea bibliotecilor (antrenat pe sklearn 1.6.1, rulat pe 1.7.2 — verificat că predicțiile rămân identice).

**De ce 10 încercări minim pentru model?**
Sub 10 încercări, features-urile statistice (trend, consistență, acuratețe pe dificultăți) sunt prea zgomotoase — modelul ar prezice din date nesemnificative. Formula simplă e mai onestă pentru utilizatori noi.
