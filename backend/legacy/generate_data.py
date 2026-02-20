
import json
import random
from datetime import datetime, timedelta

# Import exercițiile din app.py
import sys
sys.path.append('.')
from app import exercises

def generate_student_profile():
    """Generează un profil de student cu abilități realiste"""
    profiles = [
        {
            'level': 'beginner',
            'base_accuracy': random.uniform(0.3, 0.5),
            'learning_rate': random.uniform(0.001, 0.003),
            'consistency': random.uniform(0.3, 0.6),
        },
        {
            'level': 'intermediate', 
            'base_accuracy': random.uniform(0.5, 0.75),
            'learning_rate': random.uniform(0.002, 0.005),
            'consistency': random.uniform(0.6, 0.85),
        },
        {
            'level': 'advanced',
            'base_accuracy': random.uniform(0.75, 0.95),
            'learning_rate': random.uniform(0.001, 0.002),
            'consistency': random.uniform(0.8, 0.95),
        }
    ]
    
    return random.choice(profiles)

def simulate_student_attempts(student_id, student_profile, num_attempts):
    """Simulează încercările unui student bazat pe profilul lui"""
    attempts = []
    current_accuracy = student_profile['base_accuracy']
    
    # Selectează exerciții random
    selected_exercises = random.sample(exercises, min(num_attempts, len(exercises)))
    
    for i, exercise in enumerate(selected_exercises):
        # Dificultatea exercițiului influențează probabilitatea de succes
        difficulty_factor = 1 - (exercise['difficulty'] - 1) * 0.15
        
        # Progresul în timp (învățare)
        progress_factor = 1 + (i * student_profile['learning_rate'])
        
        # Calcul probabilitate succes
        success_probability = min(
            current_accuracy * difficulty_factor * progress_factor,
            0.98
        )
        
        # Adaugă randomness (zile bune/rele)
        daily_variance = random.uniform(-0.1, 0.1)
        success_probability = max(0.05, min(0.98, success_probability + daily_variance))
        
        # Determină dacă răspunsul e corect
        is_correct = random.random() < success_probability
        
        # Timp de răspuns
        if is_correct:
            time_spent = random.randint(20, 120) * exercise['difficulty']
        else:
            time_spent = random.randint(60, 300) * exercise['difficulty']
        
        # Timestamp realist
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        timestamp = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
        
        attempts.append({
            'user_id': student_id,
            'exercise_id': exercise['id'],
            'exercise_subject': exercise['subject'],
            'exercise_difficulty': exercise['difficulty'],
            'exercise_topic': exercise['topic'],
            'is_correct': is_correct,
            'time_spent': time_spent,
            'timestamp': timestamp.isoformat(),
            'profile': exercise['profile']
        })
    
    return attempts

def calculate_student_grade(attempts):
    """Calculează nota BAC bazat pe performanță"""
    if not attempts:
        return 5.0
    
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
            subject_scores[subject] = (sum(results) / len(results)) * 30
        else:
            subject_scores[subject] = 0
    
    # Total puncte (max 90)
    total_points = sum(subject_scores.values())
    
    # Conversie în notă (1-10)
    grade = 1 + (total_points / 90) * 9
    
    # Adaugă variance
    grade += random.uniform(-0.5, 0.5)
    
    return max(1.0, min(10.0, round(grade, 2)))

def generate_dataset(num_students=100):
    """Generează dataset complet"""
    print(f"🤖 Generare date pentru {num_students} studenți...")
    
    all_attempts = []
    student_grades = []
    
    for student_id in range(1, num_students + 1):
        profile = generate_student_profile()
        num_attempts = random.randint(10, 80)
        
        student_attempts = simulate_student_attempts(
            student_id, 
            profile, 
            num_attempts
        )
        
        all_attempts.extend(student_attempts)
        
        grade = calculate_student_grade(student_attempts)
        
        student_grades.append({
            'user_id': student_id,
            'level': profile['level'],
            'total_attempts': len(student_attempts),
            'accuracy': sum(1 for a in student_attempts if a['is_correct']) / len(student_attempts),
            'grade': grade
        })
        
        if student_id % 10 == 0:
            print(f"  ✓ Generat {student_id}/{num_students} studenți")
    
    print(f"\n✅ Dataset generat:")
    print(f"   📊 {len(all_attempts)} încercări totale")
    print(f"   👥 {len(student_grades)} studenți")
    print(f"   📈 Nota medie: {sum(s['grade'] for s in student_grades) / len(student_grades):.2f}")
    
    return all_attempts, student_grades

def save_dataset(attempts, grades):
    """Salvează dataset-ul"""
    with open('backend/data/synthetic_attempts.json', 'w', encoding='utf-8') as f:
        json.dump(attempts, f, indent=2, ensure_ascii=False)
    
    with open('backend/data/student_grades.json', 'w', encoding='utf-8') as f:
        json.dump(grades, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Date salvate în:")
    print(f"   📁 backend/data/synthetic_attempts.json")
    print(f"   📁 backend/data/student_grades.json")

if __name__ == '__main__':
    import os
    os.makedirs('backend/data', exist_ok=True)
    
    attempts, grades = generate_dataset(num_students=100)
    save_dataset(attempts, grades)
    
    print("\n🎉 Gata! Acum ai date pentru ML!")