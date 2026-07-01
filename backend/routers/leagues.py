"""
Leagues Router - Weekly competitive leaderboards
"""

from fastapi import APIRouter, Depends, Query

from database import get_db
from services.leagues import (
    get_user_league,
    get_league_tier_info,
    get_leaderboard,
    get_user_rank,
    get_week_end,
    LEAGUE_TIERS,
)

router = APIRouter(prefix="/api/leagues", tags=["leagues"])


@router.get("")
def get_league_info(user_id: int = Query(1), db=Depends(get_db)):
    """Get user's league, rank, and leaderboard."""
    entry = get_user_league(db, user_id)
    tier = get_league_tier_info(entry["league"])
    rank = get_user_rank(db, entry)
    leaderboard = get_leaderboard(db, entry["league"])
    week_end = get_week_end()

    return {
        "success": True,
        "league": entry["league"],
        "tier": tier,
        "weekly_xp": entry["weekly_xp"],
        "rank": rank,
        "leaderboard": leaderboard,
        "week_reset": week_end.isoformat(),
        "all_tiers": LEAGUE_TIERS,
    }


@router.get("/leaderboard")
def get_league_leaderboard(
    league: str = Query("Bronz"),
    limit: int = Query(30, ge=1, le=100),
    db=Depends(get_db),
):
    """Get leaderboard for a specific league tier."""
    leaderboard = get_leaderboard(db, league, limit)
    tier = get_league_tier_info(league)

    return {
        "success": True,
        "league": league,
        "tier": tier,
        "leaderboard": leaderboard,
    }
