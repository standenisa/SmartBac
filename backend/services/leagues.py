"""
Leagues Service - Weekly competitive tiers
5 tiers: Bronz, Argint, Aur, Diamant, Legenda
"""

from datetime import datetime, timedelta

LEAGUE_TIERS = [
    {"name": "Bronz", "color": "#CD7F32", "min_xp": 0, "emoji": "🥉"},
    {"name": "Argint", "color": "#C0C0C0", "min_xp": 100, "emoji": "🥈"},
    {"name": "Aur", "color": "#FFD700", "min_xp": 300, "emoji": "🥇"},
    {"name": "Diamant", "color": "#B9F2FF", "min_xp": 600, "emoji": "💎"},
    {"name": "Legenda", "color": "#CE82FF", "min_xp": 1000, "emoji": "👑"},
]

PROMOTION_COUNT = 5  # top 5 promote
DEMOTION_COUNT = 3   # bottom 3 demote


def get_week_start() -> str:
    """Get Monday of current week as string key."""
    today = datetime.utcnow().date()
    monday = today - timedelta(days=today.weekday())
    return monday.isoformat()


def get_week_end() -> datetime:
    """Get end of current week (next Monday 00:00 UTC)."""
    today = datetime.utcnow().date()
    monday = today - timedelta(days=today.weekday())
    next_monday = monday + timedelta(days=7)
    return datetime.combine(next_monday, datetime.min.time())


def get_user_league(db, user_id: int) -> dict:
    """Get user's current league info, rolling over last week's result."""
    week_start = get_week_start()

    entry = db.leagues.find_one({"user_id": user_id, "week_start": week_start})
    if not entry:
        entry = {
            "user_id": user_id,
            "week_start": week_start,
            "league": _rollover_league(db, user_id, week_start),
            "weekly_xp": 0,
        }
        db.leagues.insert_one(entry)

    return entry


def _rollover_league(db, user_id: int, week_start: str) -> str:
    """Carry over last week's league, applying the promotion/demotion zones."""
    prev = db.leagues.find_one(
        {"user_id": user_id, "week_start": {"$lt": week_start}},
        sort=[("week_start", -1)],
    )
    if not prev:
        return "Bronz"

    names = [tier["name"] for tier in LEAGUE_TIERS]
    tier_idx = names.index(prev["league"]) if prev["league"] in names else 0

    prev_league = {"week_start": prev["week_start"], "league": prev["league"]}
    rank = db.leagues.count_documents({**prev_league, "weekly_xp": {"$gt": prev["weekly_xp"]}}) + 1
    size = db.leagues.count_documents(prev_league)

    # weekly_xp > 0 so inactive users don't all tie at rank 1 and auto-promote
    if prev["weekly_xp"] > 0 and rank <= PROMOTION_COUNT:
        tier_idx = min(tier_idx + 1, len(LEAGUE_TIERS) - 1)
    elif size > DEMOTION_COUNT and rank > size - DEMOTION_COUNT:
        tier_idx = max(tier_idx - 1, 0)

    return names[tier_idx]


def get_league_tier_info(league_name: str) -> dict:
    """Get tier info by name."""
    for tier in LEAGUE_TIERS:
        if tier["name"] == league_name:
            return tier
    return LEAGUE_TIERS[0]


def get_leaderboard(db, league: str, limit: int = 30) -> list:
    """Get leaderboard for a league tier this week."""
    week_start = get_week_start()
    entries = list(db.leagues.find(
        {"week_start": week_start, "league": league},
        sort=[("weekly_xp", -1)],
        limit=limit,
    ))

    total = db.leagues.count_documents({"week_start": week_start, "league": league})
    usernames = {
        u["_id"]: u.get("username", "Anonim")
        for u in db.users.find({"_id": {"$in": [e["user_id"] for e in entries]}}, {"username": 1})
    }

    leaderboard = []
    for i, entry in enumerate(entries):
        leaderboard.append({
            "rank": i + 1,
            "user_id": entry["user_id"],
            "username": usernames.get(entry["user_id"], "Anonim"),
            "weekly_xp": entry["weekly_xp"],
            "zone": "promotion" if i < PROMOTION_COUNT else ("demotion" if total > DEMOTION_COUNT and i >= total - DEMOTION_COUNT else "safe"),
        })

    return leaderboard


def increment_weekly_xp(db, user_id: int, xp_amount: int):
    """Add XP to user's weekly league score."""
    entry = get_user_league(db, user_id)
    db.leagues.update_one({"_id": entry["_id"]}, {"$inc": {"weekly_xp": xp_amount}})


def get_user_rank(db, entry: dict) -> int:
    """Get user's rank within their league."""
    higher_count = db.leagues.count_documents({
        "week_start": entry["week_start"],
        "league": entry["league"],
        "weekly_xp": {"$gt": entry["weekly_xp"]},
    })
    return higher_count + 1
