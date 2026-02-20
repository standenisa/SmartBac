"""
Gamification Router - XP, levels, achievements, streaks
"""

from fastapi import APIRouter, Depends, HTTPException, Query

from database import get_db
from models.user import user_to_dict
from services.gamification import ACHIEVEMENTS_DEF, LEVEL_NAMES, XP_THRESHOLDS

router = APIRouter(prefix="/api/gamification", tags=["gamification"])


@router.get("/stats")
def get_gamification_stats(user_id: int = Query(1), db=Depends(get_db)):
    user = db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    xp = user.get("xp", 0) or 0
    level = 1
    for i, threshold in enumerate(XP_THRESHOLDS):
        if xp >= threshold:
            level = i + 1

    unlocked_count = db.user_achievements.count_documents({"user_id": user_id})

    return {
        "success": True,
        "xp": xp,
        "level": level,
        "level_name": LEVEL_NAMES[min(level - 1, len(LEVEL_NAMES) - 1)],
        "current_streak": user.get("current_streak", 0) or 0,
        "best_streak": user.get("best_streak", 0) or 0,
        "achievements_count": unlocked_count,
        "total_achievements": len(ACHIEVEMENTS_DEF),
    }


@router.get("/achievements")
def get_achievements(user_id: int = Query(1), db=Depends(get_db)):
    unlocked_ids = [
        ua["achievement_id"]
        for ua in db.user_achievements.find({"user_id": user_id})
    ]

    all_achievements = []
    for ach_id, ach_def in ACHIEVEMENTS_DEF.items():
        all_achievements.append({
            "id": ach_id,
            **ach_def,
            "unlocked": ach_id in unlocked_ids,
        })

    all_achievements.sort(key=lambda x: (not x["unlocked"], x["name"]))

    return {
        "success": True,
        "achievements": all_achievements,
        "unlocked_count": len(unlocked_ids),
        "total_count": len(ACHIEVEMENTS_DEF),
    }
