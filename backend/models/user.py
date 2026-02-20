"""User helpers for MongoDB documents"""

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


def create_user_doc(user_id, email, username, password, profile="M1"):
    """Create a user document for MongoDB insertion."""
    return {
        "_id": user_id,
        "email": email,
        "username": username,
        "password_hash": generate_password_hash(password),
        "profile": profile,
        "xp": 0,
        "level": 1,
        "current_streak": 0,
        "best_streak": 0,
        "last_activity": datetime.utcnow(),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }


def user_to_dict(doc):
    """Convert a MongoDB user document to API response dict."""
    if not doc:
        return None
    return {
        "id": doc["_id"],
        "email": doc["email"],
        "username": doc["username"],
        "profile": doc.get("profile", "M1"),
        "xp": doc.get("xp", 0),
        "level": doc.get("level", 1),
        "current_streak": doc.get("current_streak", 0),
        "best_streak": doc.get("best_streak", 0),
        "created_at": doc["created_at"].isoformat() if doc.get("created_at") else None,
        "last_activity": doc["last_activity"].isoformat() if doc.get("last_activity") else None,
    }


def set_password(password):
    """Hash a password."""
    return generate_password_hash(password)


def check_password(doc, password):
    """Verify password against stored hash."""
    return check_password_hash(doc["password_hash"], password)
