"""
Generator de date avansat pentru BAC Prep AI
Generează date sintetice realiste pentru antrenarea modelului ML avansat
Include: patterns temporale, progression difficulty, topic mastery, streaks
"""

import json
import random
from datetime import datetime, timedelta
import os
import sys

# Import exercițiile
sys.path.append(os.path.dirname(__file__))
from exercises_with_solutions import exercises_with_solutions
from exercises_database import EXERCISES_WITH_SOLUTIONS

# Merge both sources (exercises_with_solutions takes priority for overlapping IDs)
_ids_seen = set()
exercises = []
for ex in exercises_with_solutions:
    exercises.append(ex)
    _ids_seen.add(ex["id"])
for ex in EXERCISES_WITH_SOLUTIONS:
    if ex["id"] not in _ids_seen:
        exercises.append(ex)
        _ids_seen.add(ex["id"])
print(f"Exercitii incarcate: {len(exercises)}")


def generate_student_profile():
    """Generează un profil detaliat de student cu abilități realiste"""

    # Distribuție realistă a nivelurilor
    level_weights = [0.25, 0.50, 0.25]  # 25% beginner, 50% intermediate, 25% advanced
    level = random.choices(['beginner', 'intermediate', 'advanced'], weights=level_weights)[0]

    profiles = {
        'beginner': {
            'level': 'beginner',
            'base_accuracy': random.uniform(0.25, 0.45),
            'learning_rate': random.uniform(0.002, 0.005),
            'consistency': random.uniform(0.3, 0.5),
            'subject_strengths': {
                1: random.uniform(0.3, 0.5),
                2: random.uniform(0.2, 0.4),
                3: random.uniform(0.2, 0.4)
            },
            'time_factor': random.uniform(1.3, 1.8),  # Petrece mai mult timp
            'streak_probability': 0.3,
            'study_regularity': random.uniform(0.3, 0.5)
        },
        'intermediate': {
            'level': 'intermediate',
            'base_accuracy': random.uniform(0.50, 0.72),
            'learning_rate': random.uniform(0.003, 0.007),
            'consistency': random.uniform(0.55, 0.75),
            'subject_strengths': {
                1: random.uniform(0.5, 0.75),
                2: random.uniform(0.45, 0.7),
                3: random.uniform(0.4, 0.65)
            },
            'time_factor': random.uniform(0.9, 1.2),
            'streak_probability': 0.5,
            'study_regularity': random.uniform(0.5, 0.75)
        },
        'advanced': {
            'level': 'advanced',
            'base_accuracy': random.uniform(0.75, 0.92),
            'learning_rate': random.uniform(0.001, 0.003),
            'consistency': random.uniform(0.8, 0.95),
            'subject_strengths': {
                1: random.uniform(0.75, 0.95),
                2: random.uniform(0.7, 0.9),
                3: random.uniform(0.65, 0.88)
            },
            'time_factor': random.uniform(0.6, 0.9),  # Mai rapid
            'streak_probability': 0.7,
            'study_regularity': random.uniform(0.7, 0.9)
        }
    }

    profile = profiles[level]

    # Adaugă preferințe de topic
    all_topics = list(set(ex.get('topic', 'General') for ex in exercises))
    num_strong_topics = random.randint(2, 5)
    profile['strong_topics'] = random.sample(all_topics, min(num_strong_topics, len(all_topics)))

    return profile


def simulate_student_attempts_advanced(student_id, student_profile, num_attempts):
    """
    Simulează încercările unui student cu patterns realiste:
    - Learning progression
    - Time patterns (zile bune/rele)
    - Difficulty adaptation
    - Topic mastery
    - Streaks
    """
    attempts = []

    # Topic mastery tracking
    topic_attempts = {}
    topic_correct = {}

    # State pentru simulare
    current_streak = 0
    day_performance_modifier = 0  # Variație zilnică

    # Selectează exerciții (cu preferință pentru ordine crescătoare dificultate)
    available_exercises = exercises.copy()

    # Sortează partial după dificultate pentru simulare mai realistă
    if random.random() < 0.7:  # 70% șansă să înceapă cu exerciții mai ușoare
        available_exercises.sort(key=lambda x: x.get('difficulty', 2) + random.uniform(-0.5, 0.5))
    else:
        random.shuffle(available_exercises)

    selected_exercises = available_exercises[:min(num_attempts, len(available_exercises))]

    # Timestamp de start (în ultimele 60 de zile)
    base_date = datetime.now() - timedelta(days=60)
    current_date = base_date

    for i, exercise in enumerate(selected_exercises):
        # Update daily modifier (se schimbă la fiecare ~5 exerciții)
        if i % 5 == 0:
            day_performance_modifier = random.gauss(0, 0.1)
            # Regularity affect - studenții irregulari au variance mai mare
            if random.random() > student_profile['study_regularity']:
                day_performance_modifier *= 2

        # Calculează probabilitatea de succes
        base_prob = student_profile['base_accuracy']

        # Factor de dificultate
        difficulty = exercise.get('difficulty', 2)
        difficulty_factor = 1 - (difficulty - 1) * 0.12

        # Factor de progres (învățare în timp)
        progress_factor = 1 + (i * student_profile['learning_rate'])

        # Factor de consistență
        consistency_variance = random.gauss(0, 1 - student_profile['consistency'])

        # Factor de subject strength
        subject = exercise.get('subject', 1)
        subject_factor = student_profile['subject_strengths'].get(subject, 0.5) / 0.5

        # Factor de topic mastery
        topic = exercise.get('topic', 'General')
        if topic in topic_attempts:
            topic_acc = topic_correct.get(topic, 0) / topic_attempts[topic]
            topic_factor = 0.9 + topic_acc * 0.2  # Topic familiar = boost
        else:
            topic_factor = 0.95 if topic in student_profile.get('strong_topics', []) else 1.0

        # Factor de streak (momentum)
        streak_factor = 1.0
        if current_streak >= 3:
            streak_factor = 1 + min(current_streak * 0.02, 0.15)  # Max 15% boost

        # Calculează probabilitatea finală
        success_probability = (
            base_prob
            * difficulty_factor
            * progress_factor
            * subject_factor
            * topic_factor
            * streak_factor
            + consistency_variance * 0.1
            + day_performance_modifier
        )

        # Clamp
        success_probability = max(0.05, min(0.98, success_probability))

        # Determină rezultatul
        is_correct = random.random() < success_probability

        # Update streak
        if is_correct:
            current_streak += 1
        else:
            current_streak = 0

        # Update topic mastery
        topic_attempts[topic] = topic_attempts.get(topic, 0) + 1
        if is_correct:
            topic_correct[topic] = topic_correct.get(topic, 0) + 1

        # Calculează timpul
        base_time = 30 + difficulty * 20

        if is_correct:
            # Răspunsuri corecte: mai rapid, dar cu variance
            time_spent = int(base_time * student_profile['time_factor'] * random.uniform(0.5, 1.2))
        else:
            # Răspunsuri greșite: mai mult timp petrecut
            time_spent = int(base_time * student_profile['time_factor'] * random.uniform(1.0, 2.5))

        # Clamp time
        time_spent = max(10, min(600, time_spent))

        # Avansează timestamp-ul
        # Studenții regulari rezolvă mai des
        hours_gap = random.randint(1, 24) if random.random() < student_profile['study_regularity'] else random.randint(12, 72)
        current_date += timedelta(hours=hours_gap, minutes=random.randint(0, 59))

        attempts.append({
            'user_id': student_id,
            'exercise_id': exercise['id'],
            'exercise_subject': exercise.get('subject', 1),
            'exercise_difficulty': exercise.get('difficulty', 2),
            'exercise_topic': exercise.get('topic', 'General'),
            'is_correct': is_correct,
            'time_spent': time_spent,
            'timestamp': current_date.isoformat(),
            'profile': exercise.get('profile', 'BOTH'),
            'attempt_number': i + 1,
            'streak_at_attempt': current_streak if is_correct else 0
        })

    return attempts


def calculate_student_grade_advanced(attempts, profile):
    """Calculează nota BAC cu mai multă precizie"""
    if not attempts:
        return 4.0  # Nota minimă

    # Acuratețe generală
    correct = sum(1 for a in attempts if a['is_correct'])
    accuracy = correct / len(attempts)

    # Performanță pe subiecte
    subjects = {1: [], 2: [], 3: []}
    for attempt in attempts:
        subjects[attempt['exercise_subject']].append(attempt['is_correct'])

    subject_scores = {}
    for subject, results in subjects.items():
        if results:
            # Ponderăm ultimele rezultate mai mult (reflectă starea curentă)
            if len(results) > 5:
                recent_weight = 0.6
                old_weight = 0.4
                recent_acc = sum(results[-5:]) / 5
                old_acc = sum(results[:-5]) / len(results[:-5])
                weighted_acc = recent_acc * recent_weight + old_acc * old_weight
            else:
                weighted_acc = sum(results) / len(results)

            subject_scores[subject] = weighted_acc * 30  # Fiecare subiect = 30 puncte max
        else:
            subject_scores[subject] = 0

    # Total puncte (max 90)
    total_points = sum(subject_scores.values())

    # Bonus pentru consistență
    consistency_bonus = 0
    if len(attempts) >= 10:
        # Calculează variance în ultimele 10
        last_10_correct = [a['is_correct'] for a in attempts[-10:]]
        if sum(last_10_correct) >= 8:
            consistency_bonus = 0.3

    # Bonus pentru exerciții dificile rezolvate corect
    hard_exercises = [a for a in attempts if a['exercise_difficulty'] >= 3]
    if hard_exercises:
        hard_accuracy = sum(1 for a in hard_exercises if a['is_correct']) / len(hard_exercises)
        difficulty_bonus = hard_accuracy * 0.5
    else:
        difficulty_bonus = 0

    # Conversie în notă (1-10)
    base_grade = 1 + (total_points / 90) * 9

    # Aplică bonusuri și variance
    grade = base_grade + consistency_bonus + difficulty_bonus
    grade += random.gauss(0, 0.3)  # Variance naturală

    return max(1.0, min(10.0, round(grade, 2)))


def generate_dataset_advanced(num_students=150, min_attempts=15, max_attempts=100):
    """Generează dataset complet cu date avansate"""
    print(f"\n{'='*60}")
    print("🤖 BAC Prep AI - Generare Date Avansate")
    print(f"{'='*60}")
    print(f"📊 Generez date pentru {num_students} studenți...")
    print(f"📝 Încercări per student: {min_attempts} - {max_attempts}")

    all_attempts = []
    student_grades = []

    level_distribution = {'beginner': 0, 'intermediate': 0, 'advanced': 0}

    for student_id in range(1, num_students + 1):
        profile = generate_student_profile()
        level_distribution[profile['level']] += 1

        # Număr variabil de încercări bazat pe profil
        if profile['level'] == 'advanced':
            num_attempts = random.randint(min_attempts + 20, max_attempts)
        elif profile['level'] == 'intermediate':
            num_attempts = random.randint(min_attempts + 10, max_attempts - 10)
        else:
            num_attempts = random.randint(min_attempts, max_attempts - 20)

        student_attempts = simulate_student_attempts_advanced(
            student_id,
            profile,
            num_attempts
        )

        all_attempts.extend(student_attempts)

        grade = calculate_student_grade_advanced(student_attempts, profile)

        # Calculează statistici pentru student
        correct = sum(1 for a in student_attempts if a['is_correct'])

        # Topic mastery
        topic_stats = {}
        for attempt in student_attempts:
            topic = attempt['exercise_topic']
            if topic not in topic_stats:
                topic_stats[topic] = {'total': 0, 'correct': 0}
            topic_stats[topic]['total'] += 1
            if attempt['is_correct']:
                topic_stats[topic]['correct'] += 1

        topic_mastery = {
            topic: stats['correct'] / stats['total']
            for topic, stats in topic_stats.items()
        }

        student_grades.append({
            'user_id': student_id,
            'level': profile['level'],
            'total_attempts': len(student_attempts),
            'accuracy': round(correct / len(student_attempts), 3),
            'grade': grade,
            'consistency': profile['consistency'],
            'topic_mastery': topic_mastery,
            'subjects_accuracy': {
                str(s): round(sum(1 for a in student_attempts if a['exercise_subject'] == s and a['is_correct']) /
                             max(1, sum(1 for a in student_attempts if a['exercise_subject'] == s)), 3)
                for s in [1, 2, 3]
            }
        })

        if student_id % 25 == 0:
            print(f"  ✓ Generat {student_id}/{num_students} studenți")

    # Statistici finale
    print(f"\n{'='*60}")
    print("📈 Statistici Dataset:")
    print(f"{'='*60}")
    print(f"   👥 Total studenți: {len(student_grades)}")
    print(f"   📝 Total încercări: {len(all_attempts)}")
    print(f"   📊 Media încercări/student: {len(all_attempts) / len(student_grades):.1f}")

    grades = [s['grade'] for s in student_grades]
    print(f"\n   📈 Distribuție Note:")
    print(f"      Media: {sum(grades)/len(grades):.2f}")
    print(f"      Min: {min(grades):.2f}")
    print(f"      Max: {max(grades):.2f}")

    print(f"\n   👤 Distribuție Niveluri:")
    for level, count in level_distribution.items():
        print(f"      {level.capitalize()}: {count} ({count/num_students*100:.1f}%)")

    return all_attempts, student_grades


def save_dataset_advanced(attempts, grades, suffix=''):
    """Salvează dataset-ul în format JSON"""

    # Creează directorul dacă nu există
    data_dir = 'backend/data'
    os.makedirs(data_dir, exist_ok=True)

    attempts_file = f'{data_dir}/synthetic_attempts{suffix}.json'
    grades_file = f'{data_dir}/student_grades{suffix}.json'

    with open(attempts_file, 'w', encoding='utf-8') as f:
        json.dump(attempts, f, indent=2, ensure_ascii=False)

    with open(grades_file, 'w', encoding='utf-8') as f:
        json.dump(grades, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Date salvate în:")
    print(f"   📁 {attempts_file} ({os.path.getsize(attempts_file) / 1024:.1f} KB)")
    print(f"   📁 {grades_file} ({os.path.getsize(grades_file) / 1024:.1f} KB)")


if __name__ == '__main__':
    # Generare dataset standard
    attempts, grades = generate_dataset_advanced(num_students=150)
    save_dataset_advanced(attempts, grades)

    print(f"\n{'='*60}")
    print("🎉 Date generate cu succes!")
    print("   Acum rulează: python ml_predictor_advanced.py")
    print(f"{'='*60}")
