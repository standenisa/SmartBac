from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING
from bson import ObjectId
import os
from datetime import datetime
from functools import lru_cache
import time

# Load environment variables
load_dotenv()

# ML Models - încercăm advanced, fallback la simplu
try:
    from ml_predictor_advanced import AdvancedGradePredictor as GradePredictor
    ML_ADVANCED = True
    print("✅ Folosim ML Predictor AVANSAT")
except ImportError:
    try:
        from ml_predictor import GradePredictor
        ML_ADVANCED = False
        print("⚠️ Folosim ML Predictor simplu")
    except ImportError:
        ML_ADVANCED = False
        GradePredictor = None
        print("⚠️ ML Predictor indisponibil")

# Import exerciții cu rezolvări
try:
    from exercises_with_solutions import exercises_with_solutions, get_solution
    SOLUTIONS_AVAILABLE = True
    print("✅ Exerciții cu rezolvări încărcate")
except ImportError:
    SOLUTIONS_AVAILABLE = False
    print("⚠️ Exerciții cu rezolvări indisponibile")

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/bac_prep_ai')

try:
    client = MongoClient(MONGODB_URI)
    db = client.get_database('bac_prep_ai')

    # Collections
    users_collection = db.users
    exercises_collection = db.exercises
    attempts_collection = db.attempts
    achievements_collection = db.achievements
    user_achievements_collection = db.user_achievements

    # Test connection
    client.admin.command('ping')
    print("✅ Conectat la MongoDB Atlas!")

    # Creare indexuri pentru performanță
    users_collection.create_index([('id', ASCENDING)], unique=True)
    users_collection.create_index([('email', ASCENDING)], unique=True, sparse=True)
    users_collection.create_index([('username', ASCENDING)], unique=True, sparse=True)
    exercises_collection.create_index([('id', ASCENDING)], unique=True)
    exercises_collection.create_index([('subject', ASCENDING), ('profile', ASCENDING)])
    exercises_collection.create_index([('difficulty', ASCENDING)])
    attempts_collection.create_index([('user_id', ASCENDING)])
    attempts_collection.create_index([('user_id', ASCENDING), ('exercise_id', ASCENDING)])
    attempts_collection.create_index([('user_id', ASCENDING), ('created_at', ASCENDING)])
    user_achievements_collection.create_index([('user_id', ASCENDING)])
    user_achievements_collection.create_index([('user_id', ASCENDING), ('achievement_id', ASCENDING)], unique=True)
    print("✅ Indexuri MongoDB create!")

except Exception as e:
    print(f"❌ Eroare conexiune MongoDB: {e}")
    db = None

# ML Predictor initialization
ml_predictor = None
if GradePredictor:
    print("🤖 Încărcare model ML...")
    ml_predictor = GradePredictor() if not ML_ADVANCED else GradePredictor(model_type='ensemble')

    model_paths = [
        'backend/models/grade_predictor_advanced.pkl',
        'backend/models/grade_predictor.pkl',
        'models/grade_predictor_advanced.pkl',
        'models/grade_predictor.pkl'
    ]

    model_loaded = False
    for model_path in model_paths:
        if os.path.exists(model_path):
            try:
                ml_predictor.load(model_path)
                print(f"✅ Model ML încărcat din: {model_path}")
                model_loaded = True
                break
            except Exception as e:
                print(f"⚠️ Eroare la încărcare {model_path}: {e}")

    if not model_loaded:
        print("⚠️ Model ML nu există. Rulează: python ml_predictor_advanced.py")

# ============================================
# HELPER FUNCTIONS
# ============================================

# Cache in-memory cu TTL
_cache = {}
CACHE_TTL = 300  # 5 minute

def cache_get(key):
    """Returnează valoarea din cache dacă nu a expirat"""
    if key in _cache:
        value, timestamp = _cache[key]
        if time.time() - timestamp < CACHE_TTL:
            return value
        del _cache[key]
    return None

def cache_set(key, value):
    """Salvează valoare în cache cu timestamp"""
    _cache[key] = (value, time.time())

def cache_invalidate(prefix=None):
    """Invalidează cache-ul (tot sau doar un prefix)"""
    if prefix is None:
        _cache.clear()
    else:
        keys_to_delete = [k for k in _cache if k.startswith(prefix)]
        for k in keys_to_delete:
            del _cache[k]

def get_exercises_map(exercise_ids=None):
    """Încarcă exercițiile într-un dict {id: exercise} - elimină N+1 queries"""
    if exercise_ids:
        exercises = exercises_collection.find({'id': {'$in': list(set(exercise_ids))}})
    else:
        exercises = exercises_collection.find({})
    return {ex['id']: ex for ex in exercises}

def serialize_doc(doc):
    """Convertește ObjectId în string pentru JSON"""
    if doc is None:
        return None
    if isinstance(doc, list):
        return [serialize_doc(d) for d in doc]
    if isinstance(doc, dict):
        doc = dict(doc)
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
        return doc
    return doc

# ============================================
# ENDPOINTS DE BAZĂ
# ============================================

@app.route('/')
def home():
    return jsonify({
        'message': 'BAC Prep AI - Backend Running! 🚀',
        'status': 'online',
        'version': '2.0.0',
        'database': 'MongoDB Atlas',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifică starea bazei de date"""
    try:
        client.admin.command('ping')
        exercises_count = exercises_collection.count_documents({})
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'exercises_count': exercises_count,
            'ml_model': 'loaded' if ml_predictor and hasattr(ml_predictor, 'is_trained') and ml_predictor.is_trained else 'not loaded'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 500

# ============================================
# EXERCISES ENDPOINTS
# ============================================

@app.route('/api/exercises', methods=['GET'])
def get_exercises():
    """Returnează exercițiile din baza de date cu filtrare opțională"""
    difficulty = request.args.get('difficulty', type=int)
    subject = request.args.get('subject', type=int)
    profile = request.args.get('profile')

    query = {}
    if difficulty:
        query['difficulty'] = difficulty
    if subject:
        query['subject'] = subject
    if profile:
        query['$or'] = [{'profile': profile}, {'profile': 'BOTH'}]

    exercises = list(exercises_collection.find(query))
    return jsonify(serialize_doc(exercises))

@app.route('/api/exercises/<int:exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    """Returnează un exercițiu specific"""
    exercise = exercises_collection.find_one({'id': exercise_id})
    if exercise:
        return jsonify(serialize_doc(exercise))
    return jsonify({'error': 'Exercise not found'}), 404

@app.route('/api/submit-answer', methods=['POST'])
def submit_answer():
    """Trimite un răspuns și salvează în baza de date"""
    data = request.json
    exercise_id = data.get('exercise_id')
    user_answer = data.get('answer', '').strip().lower()
    user_id = data.get('user_id', 1)
    time_spent = data.get('time_spent', 0)

    exercise = exercises_collection.find_one({'id': exercise_id})
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404

    correct_answer = exercise['answer'].strip().lower()
    is_correct = user_answer == correct_answer

    # Salvează încercarea în baza de date
    attempt = {
        'user_id': user_id,
        'exercise_id': exercise_id,
        'user_answer': user_answer,
        'is_correct': is_correct,
        'time_spent': time_spent,
        'created_at': datetime.utcnow()
    }
    attempts_collection.insert_one(attempt)

    # Actualizează streak-ul utilizatorului
    user = users_collection.find_one({'id': user_id})
    if user:
        if is_correct:
            new_streak = user.get('current_streak', 0) + 1
            best_streak = max(user.get('best_streak', 0), new_streak)
            users_collection.update_one(
                {'id': user_id},
                {'$set': {
                    'current_streak': new_streak,
                    'best_streak': best_streak,
                    'last_activity': datetime.utcnow()
                }}
            )
        else:
            users_collection.update_one(
                {'id': user_id},
                {'$set': {
                    'current_streak': 0,
                    'last_activity': datetime.utcnow()
                }}
            )

    # Verifică achievements noi
    new_achievements = check_achievements_for_user(user_id)

    return jsonify({
        'correct': is_correct,
        'correct_answer': exercise['answer'] if not is_correct else None,
        'message': '🎉 Corect!' if is_correct else '❌ Încercă din nou!',
        'new_achievements': new_achievements
    })

# ============================================
# STATISTICS ENDPOINTS
# ============================================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Returnează statisticile utilizatorului"""
    user_id = request.args.get('user_id', 1, type=int)

    attempts = list(attempts_collection.find({'user_id': user_id}))

    if not attempts:
        return jsonify({
            'total_attempts': 0,
            'correct_answers': 0,
            'accuracy': 0
        })

    correct = sum(1 for a in attempts if a.get('is_correct'))
    total = len(attempts)

    return jsonify({
        'total_attempts': total,
        'correct_answers': correct,
        'accuracy': round((correct / total) * 100, 2)
    })

@app.route('/api/stats/detailed', methods=['GET'])
def get_detailed_stats():
    """Returnează statistici detaliate pe subiecte (optimizat cu aggregation)"""
    user_id = request.args.get('user_id', 1, type=int)

    # Folosim MongoDB aggregation pipeline în loc de N+1 queries
    pipeline = [
        {'$match': {'user_id': user_id}},
        {'$lookup': {
            'from': 'exercises',
            'localField': 'exercise_id',
            'foreignField': 'id',
            'as': 'exercise'
        }},
        {'$unwind': '$exercise'},
        {'$group': {
            '_id': '$exercise.subject',
            'attempts': {'$sum': 1},
            'correct': {'$sum': {'$cond': ['$is_correct', 1, 0]}}
        }}
    ]

    results = list(attempts_collection.aggregate(pipeline))

    stats = {
        'total': {'attempts': 0, 'correct': 0},
        'subject_1': {'attempts': 0, 'correct': 0},
        'subject_2': {'attempts': 0, 'correct': 0},
        'subject_3': {'attempts': 0, 'correct': 0}
    }

    for r in results:
        subject_key = f'subject_{r["_id"]}'
        if subject_key in stats:
            stats[subject_key]['attempts'] = r['attempts']
            stats[subject_key]['correct'] = r['correct']
            stats['total']['attempts'] += r['attempts']
            stats['total']['correct'] += r['correct']

    # Calculează acuratețe
    for key in stats:
        if stats[key]['attempts'] > 0:
            stats[key]['accuracy'] = round(
                (stats[key]['correct'] / stats[key]['attempts']) * 100, 2
            )
        else:
            stats[key]['accuracy'] = 0

    return jsonify(stats)

# ============================================
# USER PROFILE ENDPOINTS
# ============================================

@app.route('/api/set-profile', methods=['POST'])
def set_profile():
    """Setează profilul utilizatorului (M1/M2)"""
    data = request.json
    user_id = data.get('user_id', 1)
    profile = data.get('profile')

    result = users_collection.update_one(
        {'id': user_id},
        {'$set': {'profile': profile}}
    )

    if result.matched_count > 0:
        return jsonify({'success': True, 'profile': profile})
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/get-profile', methods=['GET'])
def get_profile():
    """Returnează profilul utilizatorului"""
    user_id = request.args.get('user_id', 1, type=int)
    user = users_collection.find_one({'id': user_id})

    if user:
        return jsonify({'profile': user.get('profile')})
    return jsonify({'profile': None})

# ============================================
# SOLUTIONS ENDPOINTS
# ============================================

@app.route('/api/exercises/<int:exercise_id>/solution', methods=['GET'])
def get_exercise_solution(exercise_id):
    """Returnează rezolvarea completă pentru un exercițiu"""
    if SOLUTIONS_AVAILABLE:
        solution = get_solution(exercise_id)
        if solution:
            return jsonify({
                'success': True,
                'solution': solution
            })

    exercise = exercises_collection.find_one({'id': exercise_id})
    if exercise:
        return jsonify({
            'success': True,
            'solution': {
                'id': exercise['id'],
                'question': exercise['question'],
                'answer': exercise['answer'],
                'solution_steps': exercise.get('solution_steps', []),
                'hints': exercise.get('hints', []),
                'explanation': exercise.get('explanation', f'Răspunsul corect este: {exercise["answer"]}'),
                'formula': exercise.get('formula')
            }
        })

    return jsonify({'error': 'Exercise not found'}), 404

@app.route('/api/exercises/<int:exercise_id>/hints', methods=['GET'])
def get_exercise_hints(exercise_id):
    """Returnează indicii pentru un exercițiu"""
    if SOLUTIONS_AVAILABLE:
        solution = get_solution(exercise_id)
        if solution and solution.get('hints'):
            return jsonify({
                'success': True,
                'hints': solution['hints'],
                'formula': solution.get('formula')
            })

    exercise = exercises_collection.find_one({'id': exercise_id})
    if exercise and exercise.get('hints'):
        return jsonify({
            'success': True,
            'hints': exercise['hints'],
            'formula': exercise.get('formula')
        })

    return jsonify({
        'success': True,
        'hints': ['Gândește-te la formulele învățate'],
        'formula': None
    })

# ============================================
# ML PREDICTION ENDPOINTS
# ============================================

@app.route('/api/ml/predict-grade', methods=['GET'])
def predict_grade():
    """Prezice nota BAC bazat pe performanța utilizatorului"""
    user_id = request.args.get('user_id', 1, type=int)

    if not ml_predictor:
        return jsonify({
            'error': 'ml_unavailable',
            'message': 'Modelul ML nu este disponibil'
        }), 500

    attempts = list(attempts_collection.find({'user_id': user_id}))

    if len(attempts) < 10:
        return jsonify({
            'error': 'insufficient_data',
            'message': 'Rezolvă minim 10 exerciții pentru predicție',
            'required': 10,
            'current': len(attempts)
        }), 400

    if not ml_predictor.is_trained:
        return jsonify({
            'error': 'model_not_trained',
            'message': 'Modelul ML nu este antrenat'
        }), 500

    # Batch query: încarcă toate exercițiile odată (elimină N+1)
    exercise_ids = [a['exercise_id'] for a in attempts]
    exercises_map = get_exercises_map(exercise_ids)

    # Formatează datele pentru predictor
    formatted_attempts = []
    for attempt in attempts:
        exercise = exercises_map.get(attempt['exercise_id'])
        if exercise:
            formatted_attempts.append({
                'user_id': user_id,
                'exercise_id': exercise['id'],
                'exercise_subject': exercise['subject'],
                'exercise_difficulty': exercise['difficulty'],
                'exercise_topic': exercise['topic'],
                'is_correct': attempt['is_correct'],
                'time_spent': attempt.get('time_spent', 60),
                'timestamp': attempt['created_at'].isoformat() if attempt.get('created_at') else datetime.now().isoformat(),
                'profile': exercise['profile']
            })

    try:
        prediction = ml_predictor.predict(formatted_attempts)
        return jsonify({
            'success': True,
            'prediction': prediction,
            'message': 'Predicție generată cu succes'
        })
    except Exception as e:
        return jsonify({
            'error': 'prediction_failed',
            'message': str(e)
        }), 500

@app.route('/api/ml/model-info', methods=['GET'])
def model_info():
    """Informații despre modelul ML"""
    if not ml_predictor:
        return jsonify({
            'is_trained': False,
            'model_type': 'Unavailable',
            'message': 'Modelul ML nu este disponibil'
        })

    return jsonify({
        'is_trained': getattr(ml_predictor, 'is_trained', False),
        'model_type': 'Ensemble' if ML_ADVANCED else 'Random Forest',
        'is_advanced': ML_ADVANCED,
        'min_attempts_required': 10
    })

@app.route('/api/ml/insights', methods=['GET'])
def get_ml_insights():
    """Returnează insights personalizate"""
    user_id = request.args.get('user_id', 1, type=int)

    attempts = list(attempts_collection.find({'user_id': user_id}).sort('created_at', 1))

    if len(attempts) < 5:
        return jsonify({
            'success': False,
            'message': 'Rezolvă minim 5 exerciții pentru insights',
            'required': 5,
            'current': len(attempts)
        }), 400

    # Calculează statistici
    correct = sum(1 for a in attempts if a.get('is_correct'))
    accuracy = correct / len(attempts)

    # Batch query: încarcă toate exercițiile odată (elimină N+1)
    exercise_ids = [a['exercise_id'] for a in attempts]
    exercises_map = get_exercises_map(exercise_ids)

    # Grupează pe subiecte
    subjects = {1: [], 2: [], 3: []}
    for attempt in attempts:
        exercise = exercises_map.get(attempt['exercise_id'])
        if exercise:
            subjects[exercise['subject']].append(attempt.get('is_correct', False))

    subject_accs = {}
    for s, results in subjects.items():
        subject_accs[s] = sum(results) / len(results) if results else 0

    insights = []

    # Puncte forte
    best_subject = max(subject_accs.items(), key=lambda x: x[1] if x[1] > 0 else -1)
    if best_subject[1] > 0.7:
        insights.append({
            'type': 'strength',
            'icon': '💪',
            'message': f'Excelent la Subiectul {best_subject[0]}! ({best_subject[1]*100:.0f}% acuratețe)'
        })

    # Puncte slabe
    worst_subject = min(subject_accs.items(), key=lambda x: x[1] if x[1] > 0 else 1)
    if worst_subject[1] < 0.5 and worst_subject[1] > 0:
        insights.append({
            'type': 'focus',
            'icon': '🎯',
            'message': f'Concentrează-te pe Subiectul {worst_subject[0]} pentru îmbunătățire'
        })

    # Trend
    if len(attempts) >= 10:
        first_half = attempts[:len(attempts)//2]
        second_half = attempts[len(attempts)//2:]
        first_acc = sum(1 for a in first_half if a.get('is_correct')) / len(first_half)
        second_acc = sum(1 for a in second_half if a.get('is_correct')) / len(second_half)

        if second_acc > first_acc + 0.1:
            insights.append({
                'type': 'positive',
                'icon': '📈',
                'message': 'Progresezi excelent! Performanța ta se îmbunătățește constant.'
            })

    return jsonify({
        'success': True,
        'insights': insights,
        'stats': {
            'total_attempts': len(attempts),
            'accuracy': round(accuracy * 100, 1),
            'subject_accuracies': {f'subject_{k}': round(v*100, 1) for k, v in subject_accs.items()}
        }
    })

# ============================================
# GAMIFICATION ENDPOINTS
# ============================================

ACHIEVEMENTS_DEF = {
    'first_correct': {'name': 'Prima Victorie', 'description': 'Ai răspuns corect la primul exercițiu', 'icon': '🌟', 'xp': 10},
    'streak_3': {'name': 'În Formă', 'description': '3 răspunsuri corecte la rând', 'icon': '🔥', 'xp': 25},
    'streak_5': {'name': 'Imbatabil', 'description': '5 răspunsuri corecte la rând', 'icon': '⚡', 'xp': 50},
    'streak_10': {'name': 'Legendă', 'description': '10 răspunsuri corecte la rând', 'icon': '👑', 'xp': 100},
    'exercises_10': {'name': 'Începător', 'description': 'Ai rezolvat 10 exerciții', 'icon': '📚', 'xp': 30},
    'exercises_50': {'name': 'Dedicat', 'description': 'Ai rezolvat 50 exerciții', 'icon': '🎯', 'xp': 100},
    'exercises_100': {'name': 'Expert', 'description': 'Ai rezolvat 100 exerciții', 'icon': '🏆', 'xp': 250},
    'accuracy_80': {'name': 'Precizie', 'description': 'Ai atins 80% acuratețe (minim 20 exerciții)', 'icon': '🎯', 'xp': 100},
}

def check_achievements_for_user(user_id):
    """Verifică și acordă achievements noi pentru un utilizator"""
    user = users_collection.find_one({'id': user_id})
    if not user:
        return []

    attempts = list(attempts_collection.find({'user_id': user_id}))
    if not attempts:
        return []

    # Achievements deja deblocate
    unlocked = [ua['achievement_id'] for ua in user_achievements_collection.find({'user_id': user_id})]

    new_achievements = []
    correct_count = sum(1 for a in attempts if a.get('is_correct'))
    total_count = len(attempts)
    current_streak = user.get('current_streak', 0)

    # Prima victorie
    if correct_count >= 1 and 'first_correct' not in unlocked:
        new_achievements.append('first_correct')

    # Streak achievements
    if current_streak >= 3 and 'streak_3' not in unlocked:
        new_achievements.append('streak_3')
    if current_streak >= 5 and 'streak_5' not in unlocked:
        new_achievements.append('streak_5')
    if current_streak >= 10 and 'streak_10' not in unlocked:
        new_achievements.append('streak_10')

    # Exercise count achievements
    if total_count >= 10 and 'exercises_10' not in unlocked:
        new_achievements.append('exercises_10')
    if total_count >= 50 and 'exercises_50' not in unlocked:
        new_achievements.append('exercises_50')
    if total_count >= 100 and 'exercises_100' not in unlocked:
        new_achievements.append('exercises_100')

    # Accuracy achievement
    if total_count >= 20:
        accuracy = correct_count / total_count
        if accuracy >= 0.8 and 'accuracy_80' not in unlocked:
            new_achievements.append('accuracy_80')

    # Salvează achievements noi
    total_xp = 0
    for achievement_id in new_achievements:
        user_achievements_collection.insert_one({
            'user_id': user_id,
            'achievement_id': achievement_id,
            'unlocked_at': datetime.utcnow()
        })
        total_xp += ACHIEVEMENTS_DEF.get(achievement_id, {}).get('xp', 10)

    # Adaugă XP
    if total_xp > 0:
        users_collection.update_one(
            {'id': user_id},
            {'$inc': {'xp': total_xp}}
        )

    return [{'id': a, **ACHIEVEMENTS_DEF.get(a, {})} for a in new_achievements]

@app.route('/api/gamification/stats', methods=['GET'])
def get_gamification_stats():
    """Returnează statisticile de gamification"""
    user_id = request.args.get('user_id', 1, type=int)
    user = users_collection.find_one({'id': user_id})

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Calculează nivelul
    xp = user.get('xp', 0)
    xp_thresholds = [0, 100, 250, 500, 1000, 2000, 4000, 7000, 11000, 16000]
    level = 1
    for i, threshold in enumerate(xp_thresholds):
        if xp >= threshold:
            level = i + 1

    level_names = ['Începător', 'Novice', 'Elev', 'Student', 'Avansat', 'Expert', 'Master', 'Guru', 'Legendă', 'Campion']

    unlocked_count = user_achievements_collection.count_documents({'user_id': user_id})

    return jsonify({
        'success': True,
        'xp': xp,
        'level': level,
        'level_name': level_names[min(level - 1, 9)],
        'current_streak': user.get('current_streak', 0),
        'best_streak': user.get('best_streak', 0),
        'achievements_count': unlocked_count,
        'total_achievements': len(ACHIEVEMENTS_DEF)
    })

@app.route('/api/gamification/achievements', methods=['GET'])
def get_achievements():
    """Returnează toate achievements"""
    user_id = request.args.get('user_id', 1, type=int)

    unlocked = [ua['achievement_id'] for ua in user_achievements_collection.find({'user_id': user_id})]

    all_achievements = []
    for achievement_id, ach_def in ACHIEVEMENTS_DEF.items():
        all_achievements.append({
            'id': achievement_id,
            **ach_def,
            'unlocked': achievement_id in unlocked
        })

    all_achievements.sort(key=lambda x: (not x['unlocked'], x['name']))

    return jsonify({
        'success': True,
        'achievements': all_achievements,
        'unlocked_count': len(unlocked),
        'total_count': len(ACHIEVEMENTS_DEF)
    })

# ============================================
# USER MANAGEMENT ENDPOINTS
# ============================================

@app.route('/api/users', methods=['POST'])
def create_user():
    """Creează un utilizator nou"""
    data = request.json

    # Verifică dacă email-ul există deja
    if users_collection.find_one({'email': data.get('email')}):
        return jsonify({'error': 'Email already exists'}), 400

    if users_collection.find_one({'username': data.get('username')}):
        return jsonify({'error': 'Username already exists'}), 400

    # Generează ID nou
    last_user = users_collection.find_one(sort=[('id', -1)])
    new_id = (last_user['id'] + 1) if last_user else 1

    user = {
        'id': new_id,
        'email': data.get('email'),
        'username': data.get('username'),
        'profile': data.get('profile', 'M1'),
        'xp': 0,
        'current_streak': 0,
        'best_streak': 0,
        'created_at': datetime.utcnow(),
        'last_activity': datetime.utcnow()
    }

    users_collection.insert_one(user)

    return jsonify({
        'success': True,
        'user': serialize_doc(user)
    }), 201

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Returnează informații despre un utilizator"""
    user = users_collection.find_one({'id': user_id})
    if user:
        return jsonify(serialize_doc(user))
    return jsonify({'error': 'User not found'}), 404

# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    print('🚀 Starting BAC Prep AI Backend...')
    print('📍 Running on http://localhost:5000')
    print('🗄️ Database: MongoDB Atlas')
    app.run(debug=True, port=5000)
