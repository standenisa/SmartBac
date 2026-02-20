"""
Gamification Service - achievements, XP, levels
"""

from datetime import datetime

ACHIEVEMENTS_DEF = {
    "first_correct": {"name": "Prima Victorie", "description": "Ai raspuns corect la primul exercitiu", "icon": "star", "xp": 10},
    "streak_3": {"name": "In Forma", "description": "3 raspunsuri corecte la rand", "icon": "fire", "xp": 25},
    "streak_5": {"name": "Imbatabil", "description": "5 raspunsuri corecte la rand", "icon": "zap", "xp": 50},
    "streak_10": {"name": "Legenda", "description": "10 raspunsuri corecte la rand", "icon": "crown", "xp": 100},
    "exercises_10": {"name": "Incepator", "description": "Ai rezolvat 10 exercitii", "icon": "book", "xp": 30},
    "exercises_50": {"name": "Dedicat", "description": "Ai rezolvat 50 exercitii", "icon": "target", "xp": 100},
    "exercises_100": {"name": "Expert", "description": "Ai rezolvat 100 exercitii", "icon": "trophy", "xp": 250},
    "accuracy_80": {"name": "Precizie", "description": "Ai atins 80% acuratete (minim 20 exercitii)", "icon": "target", "xp": 100},
}

XP_THRESHOLDS = [0, 100, 250, 500, 1000, 2000, 4000, 7000, 11000, 16000]
LEVEL_NAMES = [
    "Incepator", "Novice", "Elev", "Student", "Avansat",
    "Expert", "Master", "Guru", "Legenda", "Campion",
]


def check_achievements_for_user(user_id: int, db) -> list:
    """Check and award new achievements for a user."""
    user = db.users.find_one({"_id": user_id})
    if not user:
        return []

    attempts = list(db.attempts.find({"user_id": user_id}))
    if not attempts:
        return []

    unlocked = [
        ua["achievement_id"]
        for ua in db.user_achievements.find({"user_id": user_id})
    ]

    new_achievements = []
    correct_count = sum(1 for a in attempts if a["is_correct"])
    total_count = len(attempts)
    current_streak = user.get("current_streak", 0) or 0

    # First correct
    if correct_count >= 1 and "first_correct" not in unlocked:
        new_achievements.append("first_correct")

    # Streak achievements
    if current_streak >= 3 and "streak_3" not in unlocked:
        new_achievements.append("streak_3")
    if current_streak >= 5 and "streak_5" not in unlocked:
        new_achievements.append("streak_5")
    if current_streak >= 10 and "streak_10" not in unlocked:
        new_achievements.append("streak_10")

    # Exercise count achievements
    if total_count >= 10 and "exercises_10" not in unlocked:
        new_achievements.append("exercises_10")
    if total_count >= 50 and "exercises_50" not in unlocked:
        new_achievements.append("exercises_50")
    if total_count >= 100 and "exercises_100" not in unlocked:
        new_achievements.append("exercises_100")

    # Accuracy achievement
    if total_count >= 20 and correct_count / total_count >= 0.8 and "accuracy_80" not in unlocked:
        new_achievements.append("accuracy_80")

    # Save new achievements and award XP
    total_xp = 0
    for ach_id in new_achievements:
        db.user_achievements.insert_one({
            "user_id": user_id,
            "achievement_id": ach_id,
            "unlocked_at": datetime.utcnow(),
        })
        total_xp += ACHIEVEMENTS_DEF.get(ach_id, {}).get("xp", 10)

    if total_xp > 0:
        db.users.update_one({"_id": user_id}, {"$inc": {"xp": total_xp}})

    return [{"id": a, **ACHIEVEMENTS_DEF.get(a, {})} for a in new_achievements]
