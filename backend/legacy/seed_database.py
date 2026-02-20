"""
Script pentru popularea bazei de date PostgreSQL cu date inițiale
Rulează: python seed_database.py
"""

from app import app, db
from models import User, Exercise, Achievement
import json

# Exercițiile BAC 2020-2025
EXERCISES_DATA = [
    # SUBIECTUL I - Ecuații liniare
    {'id': 9, 'question': 'BAC 2024 Iulie - Rezolvă în mulțimea numerelor reale ecuația: 3x - 5 = 7', 'answer': '4', 'difficulty': 1, 'topic': 'Ecuații liniare', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 10, 'question': 'BAC 2023 Iulie - Rezolvă ecuația: x² - 9 = 0. Scrie soluțiile separate prin virgulă', 'answer': '-3,3', 'difficulty': 1, 'topic': 'Ecuații de gradul 2', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 11, 'question': 'BAC 2022 August - Rezolvă ecuația: 2x + 1 = x + 7', 'answer': '6', 'difficulty': 1, 'topic': 'Ecuații liniare', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 12, 'question': 'BAC 2021 Iulie - Rezolvă ecuația: x² - 4x + 4 = 0', 'answer': '2', 'difficulty': 2, 'topic': 'Ecuații de gradul 2', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 13, 'question': 'BAC 2020 Septembrie - Rezolvă ecuația: 5x = 35', 'answer': '7', 'difficulty': 1, 'topic': 'Ecuații liniare', 'subject': 1, 'points': 5, 'profile': 'BOTH'},

    # SUBIECTUL I - Funcții
    {'id': 14, 'question': 'BAC 2024 Model - Fie f: ℝ → ℝ, f(x) = 2x + 3. Calculează f(5)', 'answer': '13', 'difficulty': 1, 'topic': 'Funcții', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 15, 'question': 'BAC 2023 Model - Fie f: ℝ → ℝ, f(x) = x² - 2x. Calculează f(3)', 'answer': '3', 'difficulty': 2, 'topic': 'Funcții', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 16, 'question': 'BAC 2022 Iulie - Fie f: ℝ → ℝ, f(x) = 3x - 1. Calculează f(-2)', 'answer': '-7', 'difficulty': 1, 'topic': 'Funcții', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 17, 'question': 'BAC 2021 Model - Fie f: ℝ → ℝ, f(x) = x² + 4. Calculează f(0)', 'answer': '4', 'difficulty': 1, 'topic': 'Funcții', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 18, 'question': 'BAC 2020 Iulie - Fie f: ℝ → ℝ, f(x) = 4x + 2. Pentru ce valoare a lui x avem f(x) = 18?', 'answer': '4', 'difficulty': 2, 'topic': 'Funcții - Ecuații', 'subject': 1, 'points': 5, 'profile': 'BOTH'},

    # SUBIECTUL I - Geometrie analitică
    {'id': 19, 'question': 'BAC 2024 Iulie - Distanța între punctele A(1, 2) și B(4, 6) este...', 'answer': '5', 'difficulty': 2, 'topic': 'Geometrie analitică', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 20, 'question': 'BAC 2023 August - Coordonatele mijlocului segmentului AB, unde A(2, 4) și B(6, 8), sunt (x, y). Scrie doar x', 'answer': '4', 'difficulty': 2, 'topic': 'Geometrie analitică - Mijloc', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 21, 'question': 'BAC 2022 Model - Panta dreptei care trece prin A(0, 2) și B(3, 8) este...', 'answer': '2', 'difficulty': 2, 'topic': 'Geometrie analitică - Pantă', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 22, 'question': 'BAC 2021 August - Ecuația dreptei care trece prin origine și are panta 3 este y = mx. Care e m?', 'answer': '3', 'difficulty': 1, 'topic': 'Geometrie analitică - Ecuații', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 23, 'question': 'BAC 2020 Model - Distanța de la originea O(0, 0) la punctul A(3, 4) este...', 'answer': '5', 'difficulty': 2, 'topic': 'Geometrie analitică - Distanță', 'subject': 1, 'points': 5, 'profile': 'BOTH'},

    # SUBIECTUL I - Combinatorică
    {'id': 24, 'question': 'BAC 2024 Model - Calculează 4! (4 factorial)', 'answer': '24', 'difficulty': 1, 'topic': 'Combinatorică - Factorial', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 25, 'question': 'BAC 2023 Iulie - Câte permutări sunt ale mulțimii {1, 2, 3}?', 'answer': '6', 'difficulty': 2, 'topic': 'Combinatorică - Permutări', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 26, 'question': 'BAC 2022 Septembrie - Aruncăm un zar. Probabilitatea să obținem un număr par este... (scrie 0.5)', 'answer': '0.5', 'difficulty': 2, 'topic': 'Probabilități', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 27, 'question': 'BAC 2021 Iulie - Calculează C(5,2) = 5!/(2!×3!)', 'answer': '10', 'difficulty': 2, 'topic': 'Combinatorică - Combinări', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 28, 'question': 'BAC 2020 Iulie - Câte numere de 3 cifre distincte se pot forma cu cifrele 1, 2, 3, 4?', 'answer': '24', 'difficulty': 3, 'topic': 'Combinatorică - Aranjamente', 'subject': 1, 'points': 5, 'profile': 'BOTH'},

    # SUBIECTUL I - Limite
    {'id': 29, 'question': 'BAC 2024 Iulie - Calculează: lim(x→2) (3x + 1)', 'answer': '7', 'difficulty': 2, 'topic': 'Limite', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 30, 'question': 'BAC 2023 Model - Calculează: lim(x→1) (x² + 3)', 'answer': '4', 'difficulty': 1, 'topic': 'Limite', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 31, 'question': 'BAC 2022 Iulie - Calculează: lim(x→0) (5x + 10)', 'answer': '10', 'difficulty': 1, 'topic': 'Limite', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 32, 'question': 'BAC 2021 August - Calculează: lim(x→3) (x² - 2x)', 'answer': '3', 'difficulty': 2, 'topic': 'Limite', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 33, 'question': 'BAC 2020 Septembrie - Calculează: lim(x→-1) (2x + 5)', 'answer': '3', 'difficulty': 1, 'topic': 'Limite', 'subject': 1, 'points': 5, 'profile': 'BOTH'},

    # SUBIECTUL I - Derivate
    {'id': 34, 'question': 'BAC 2024 Model - Calculează derivata funcției f(x) = 5x. Scrie doar coeficientul', 'answer': '5', 'difficulty': 1, 'topic': 'Derivate', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 35, 'question': 'BAC 2023 Iulie - Calculează derivata funcției f(x) = x³. Scrie doar coeficientul lui x²', 'answer': '3', 'difficulty': 2, 'topic': 'Derivate', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 36, 'question': 'BAC 2022 August - O primitivă a funcției f(x) = 4 este F(x) = 4x + C. Care e valoarea constantei pentru F(0) = 5?', 'answer': '5', 'difficulty': 2, 'topic': 'Primitive', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 37, 'question': 'BAC 2021 Iulie - Calculează derivata funcției f(x) = 2x² + 3x. Care e valoarea lui f\'(1)?', 'answer': '7', 'difficulty': 3, 'topic': 'Derivate - Calcul', 'subject': 1, 'points': 5, 'profile': 'BOTH'},
    {'id': 38, 'question': 'BAC 2020 Model - Calculează ∫3 dx. Scrie doar coeficientul lui x', 'answer': '3', 'difficulty': 2, 'topic': 'Integrale', 'subject': 1, 'points': 5, 'profile': 'BOTH'},

    # SUBIECTUL II - Derivate
    {'id': 39, 'question': 'BAC 2024 Model - Calculează derivata funcției f(x) = 7x. Scrie doar coeficientul', 'answer': '7', 'difficulty': 1, 'topic': 'Derivate', 'subject': 2, 'points': 5, 'profile': 'BOTH'},
    {'id': 40, 'question': 'BAC 2023 Iulie - Calculează derivata funcției f(x) = x⁵. Scrie doar coeficientul lui x⁴', 'answer': '5', 'difficulty': 2, 'topic': 'Derivate', 'subject': 2, 'points': 5, 'profile': 'BOTH'},
    {'id': 41, 'question': 'BAC 2022 August - Fie f(x) = x³ - 3x. Calculează f\'(1)', 'answer': '0', 'difficulty': 2, 'topic': 'Derivate - Calcul', 'subject': 2, 'points': 5, 'profile': 'BOTH'},
    {'id': 42, 'question': 'BAC 2021 Iulie - Calculează derivata funcției f(x) = 3x² + 2x - 1. Care e f\'(0)?', 'answer': '2', 'difficulty': 2, 'topic': 'Derivate', 'subject': 2, 'points': 5, 'profile': 'BOTH'},
    {'id': 43, 'question': 'BAC 2020 Septembrie - Fie f(x) = x⁴. Calculează f\'(2)', 'answer': '32', 'difficulty': 3, 'topic': 'Derivate - Aplicații', 'subject': 2, 'points': 5, 'profile': 'BOTH'},

    # SUBIECTUL II - Limite
    {'id': 47, 'question': 'BAC 2024 Model - Calculează: lim(x→5) (2x - 3)', 'answer': '7', 'difficulty': 2, 'topic': 'Limite', 'subject': 2, 'points': 5, 'profile': 'BOTH'},
    {'id': 48, 'question': 'BAC 2023 Iulie - Calculează: lim(x→2) (x² + x)', 'answer': '6', 'difficulty': 2, 'topic': 'Limite', 'subject': 2, 'points': 5, 'profile': 'BOTH'},
    {'id': 49, 'question': 'BAC 2022 August - Calculează: lim(x→-1) (x³ + 1)', 'answer': '0', 'difficulty': 2, 'topic': 'Limite', 'subject': 2, 'points': 5, 'profile': 'BOTH'},
    {'id': 50, 'question': 'BAC 2021 Iulie - Calculează: lim(x→0) (3x² + 2x + 1)', 'answer': '1', 'difficulty': 2, 'topic': 'Limite', 'subject': 2, 'points': 5, 'profile': 'BOTH'},
    {'id': 51, 'question': 'BAC 2020 Model - Calculează: lim(x→4) (x - 2)', 'answer': '2', 'difficulty': 1, 'topic': 'Limite', 'subject': 2, 'points': 5, 'profile': 'BOTH'},

    # SUBIECTUL II - Integrale
    {'id': 52, 'question': 'BAC 2024 Iulie - Calculează ∫3x² dx. Scrie doar coeficientul lui x³', 'answer': '1', 'difficulty': 3, 'topic': 'Integrale', 'subject': 2, 'points': 5, 'profile': 'BOTH'},
    {'id': 53, 'question': 'BAC 2023 Model - Calculează ∫8x³ dx. Scrie doar coeficientul lui x⁴', 'answer': '2', 'difficulty': 3, 'topic': 'Integrale', 'subject': 2, 'points': 5, 'profile': 'BOTH'},
    {'id': 54, 'question': 'BAC 2022 Iulie - O primitivă a funcției f(x) = 6 este F(x) = 6x + C. Pentru F(1) = 10, care e C?', 'answer': '4', 'difficulty': 3, 'topic': 'Primitive', 'subject': 2, 'points': 5, 'profile': 'BOTH'},
    {'id': 60, 'question': 'BAC 2024 Iulie - Calculează ∫₀² 2x dx', 'answer': '4', 'difficulty': 3, 'topic': 'Integrale definite', 'subject': 2, 'points': 5, 'profile': 'BOTH'},
    {'id': 61, 'question': 'BAC 2023 August - Calculează ∫₁³ 3 dx', 'answer': '6', 'difficulty': 2, 'topic': 'Integrale definite', 'subject': 2, 'points': 5, 'profile': 'BOTH'},

    # SUBIECTUL III - M1 Matrice
    {'id': 65, 'question': 'BAC 2024 M1 - Calculează determinantul matricei A = [[3, 1], [2, 4]]', 'answer': '10', 'difficulty': 3, 'topic': 'Matrice - Determinanți', 'subject': 3, 'points': 5, 'profile': 'M1'},
    {'id': 66, 'question': 'BAC 2023 M1 - Fie A = [[2, 3], [4, 5]]. Calculează det(A)', 'answer': '-2', 'difficulty': 3, 'topic': 'Matrice - Determinanți', 'subject': 3, 'points': 5, 'profile': 'M1'},
    {'id': 67, 'question': 'BAC 2022 M1 - Calculează det([[5, 2], [3, 1]])', 'answer': '-1', 'difficulty': 3, 'topic': 'Matrice - Determinanți', 'subject': 3, 'points': 5, 'profile': 'M1'},
    {'id': 68, 'question': 'BAC 2024 M1 - Calculează det([[1,0,0],[0,2,0],[0,0,3]])', 'answer': '6', 'difficulty': 3, 'topic': 'Matrice - Determinanți 3×3', 'subject': 3, 'points': 5, 'profile': 'M1'},
    {'id': 71, 'question': 'BAC 2024 M1 - Fie A = [[1,2],[3,4]] și B = [[2,0],[1,1]]. Calculează (A+B)₁₁', 'answer': '3', 'difficulty': 3, 'topic': 'Matrice - Operații', 'subject': 3, 'points': 5, 'profile': 'M1'},

    # SUBIECTUL III - M1 Vectori
    {'id': 76, 'question': 'BAC 2024 M1 - Fie u=(2,3) și v=(1,4) în R². Calculează u·v', 'answer': '14', 'difficulty': 3, 'topic': 'Vectori - Produs scalar', 'subject': 3, 'points': 5, 'profile': 'M1'},
    {'id': 77, 'question': 'BAC 2023 M1 - Calculează produsul scalar (1,2,3)·(2,1,0)', 'answer': '4', 'difficulty': 3, 'topic': 'Vectori - Produs scalar', 'subject': 3, 'points': 5, 'profile': 'M1'},
    {'id': 79, 'question': 'BAC 2024 M1 - Calculează modulul vectorului v=(5,12)', 'answer': '13', 'difficulty': 3, 'topic': 'Vectori - Modul', 'subject': 3, 'points': 5, 'profile': 'M1'},
    {'id': 81, 'question': 'BAC 2024 M1 - Rezolvă sistemul: 2x+y=7, x+y=4. Care e x?', 'answer': '3', 'difficulty': 3, 'topic': 'Sisteme ecuații', 'subject': 3, 'points': 5, 'profile': 'M1'},

    # SUBIECTUL III - M2 Matrice simple
    {'id': 83, 'question': 'BAC 2024 M2 - Calculează suma elementelor matricei [[2,3],[1,4]]', 'answer': '10', 'difficulty': 1, 'topic': 'Matrice - Operații simple', 'subject': 3, 'points': 5, 'profile': 'M2'},
    {'id': 84, 'question': 'BAC 2023 M2 - Fie A = [[5,1],[2,3]]. Calculează a₁₁ + a₂₂', 'answer': '8', 'difficulty': 1, 'topic': 'Matrice - Elemente', 'subject': 3, 'points': 5, 'profile': 'M2'},
    {'id': 85, 'question': 'BAC 2022 M2 - Care e elementul de pe prima linie, coloana 2 în [[1,7],[3,4]]?', 'answer': '7', 'difficulty': 1, 'topic': 'Matrice - Elemente', 'subject': 3, 'points': 5, 'profile': 'M2'},
    {'id': 86, 'question': 'BAC 2024 M2 - Calculează 2×[[3,1],[2,4]]. Care e elementul (1,1)?', 'answer': '6', 'difficulty': 2, 'topic': 'Matrice - Înmulțire scalar', 'subject': 3, 'points': 5, 'profile': 'M2'},

    # SUBIECTUL III - M2 Vectori simpli
    {'id': 91, 'question': 'BAC 2024 M2 - Fie vectorul v=(7,3). Care e prima componentă?', 'answer': '7', 'difficulty': 1, 'topic': 'Vectori - Componente', 'subject': 3, 'points': 5, 'profile': 'M2'},
    {'id': 93, 'question': 'BAC 2024 M2 - Adună u=(2,3) și v=(1,4). Care e prima componentă a sumei?', 'answer': '3', 'difficulty': 2, 'topic': 'Vectori - Adunare', 'subject': 3, 'points': 5, 'profile': 'M2'},
    {'id': 97, 'question': 'BAC 2024 M2 - Calculează lungimea vectorului v=(3,4)', 'answer': '5', 'difficulty': 2, 'topic': 'Vectori - Modul', 'subject': 3, 'points': 5, 'profile': 'M2'},
    {'id': 99, 'question': 'BAC 2024 M2 - Fie I₂ matricea identitate 2×2. Care e suma elementelor?', 'answer': '2', 'difficulty': 1, 'topic': 'Matrice - Identitate', 'subject': 3, 'points': 5, 'profile': 'M2'},
]

# Achievements disponibile
ACHIEVEMENTS_DATA = [
    {'id': 'first_correct', 'name': 'Prima Victorie', 'description': 'Ai răspuns corect la primul exercițiu', 'icon': '🌟', 'xp': 10, 'category': 'general'},
    {'id': 'streak_3', 'name': 'În Formă', 'description': '3 răspunsuri corecte la rând', 'icon': '🔥', 'xp': 25, 'category': 'streak'},
    {'id': 'streak_5', 'name': 'Imbatabil', 'description': '5 răspunsuri corecte la rând', 'icon': '⚡', 'xp': 50, 'category': 'streak'},
    {'id': 'streak_10', 'name': 'Legendă', 'description': '10 răspunsuri corecte la rând', 'icon': '👑', 'xp': 100, 'category': 'streak'},
    {'id': 'exercises_10', 'name': 'Începător', 'description': 'Ai rezolvat 10 exerciții', 'icon': '📚', 'xp': 30, 'category': 'exercises'},
    {'id': 'exercises_50', 'name': 'Dedicat', 'description': 'Ai rezolvat 50 exerciții', 'icon': '🎯', 'xp': 100, 'category': 'exercises'},
    {'id': 'exercises_100', 'name': 'Expert', 'description': 'Ai rezolvat 100 exerciții', 'icon': '🏆', 'xp': 250, 'category': 'exercises'},
    {'id': 'accuracy_80', 'name': 'Precizie', 'description': 'Ai atins 80% acuratețe (minim 20 exerciții)', 'icon': '🎯', 'xp': 100, 'category': 'accuracy'},
]


def seed_exercises():
    """Populează tabelul exercises"""
    print("📝 Adăugare exerciții...")

    for ex_data in EXERCISES_DATA:
        existing = Exercise.query.get(ex_data['id'])
        if not existing:
            exercise = Exercise(
                id=ex_data['id'],
                question=ex_data['question'],
                answer=ex_data['answer'],
                difficulty=ex_data['difficulty'],
                topic=ex_data['topic'],
                subject=ex_data['subject'],
                points=ex_data['points'],
                profile=ex_data['profile']
            )
            db.session.add(exercise)

    db.session.commit()
    print(f"✅ {len(EXERCISES_DATA)} exerciții adăugate!")


def seed_achievements():
    """Populează tabelul achievements"""
    print("🏆 Adăugare achievements...")

    for ach_data in ACHIEVEMENTS_DATA:
        existing = Achievement.query.get(ach_data['id'])
        if not existing:
            achievement = Achievement(
                id=ach_data['id'],
                name=ach_data['name'],
                description=ach_data['description'],
                icon=ach_data['icon'],
                xp=ach_data['xp'],
                category=ach_data['category']
            )
            db.session.add(achievement)

    db.session.commit()
    print(f"✅ {len(ACHIEVEMENTS_DATA)} achievements adăugate!")


def seed_demo_user():
    """Creează un utilizator demo"""
    print("👤 Creare utilizator demo...")

    existing = User.query.filter_by(email='demo@bacprep.ai').first()
    if not existing:
        user = User(
            email='demo@bacprep.ai',
            username='demo',
            profile='M1'
        )
        user.set_password('demo123')
        db.session.add(user)
        db.session.commit()
        print("✅ Utilizator demo creat! (email: demo@bacprep.ai, parola: demo123)")
    else:
        print("⚠️ Utilizatorul demo există deja")


def seed_all():
    """Populează toate tabelele"""
    print("\n🌱 Inițializare bază de date BAC Prep AI\n")
    print("=" * 50)

    # Creează tabelele
    db.create_all()
    print("✅ Tabele create!\n")

    # Populează datele
    seed_exercises()
    seed_achievements()
    seed_demo_user()

    print("\n" + "=" * 50)
    print("🎉 Baza de date a fost populată cu succes!")
    print("=" * 50)


if __name__ == '__main__':
    with app.app_context():
        seed_all()
