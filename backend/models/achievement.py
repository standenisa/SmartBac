"""Achievement helpers for MongoDB documents"""


def achievement_to_dict(doc):
    """Convert a MongoDB achievement document to API response dict."""
    if not doc:
        return None
    return {
        "id": doc["_id"],
        "name": doc["name"],
        "description": doc["description"],
        "icon": doc.get("icon", "trophy"),
        "xp": doc.get("xp", 10),
        "category": doc.get("category", "general"),
    }


def user_achievement_to_dict(doc, achievement_doc=None):
    """Convert a MongoDB user_achievement document to API response dict."""
    if not doc:
        return None
    result = {
        "user_id": doc["user_id"],
        "achievement_id": doc["achievement_id"],
        "unlocked_at": doc["unlocked_at"].isoformat() if doc.get("unlocked_at") else None,
    }
    if achievement_doc:
        result["achievement"] = achievement_to_dict(achievement_doc)
    return result
