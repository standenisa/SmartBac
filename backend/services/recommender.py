"""
Recommendation Engine Service
Content-based filtering using user performance data
"""

from collections import defaultdict
from models.exercise import exercise_to_dict


class RecommendationEngine:
    """Content-based exercise recommendation engine."""

    def __init__(self, db):
        self.db = db

    def get_user_profile(self, user_id: int) -> dict:
        """Build user performance profile across topics and difficulty levels."""
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$lookup": {
                "from": "exercises",
                "localField": "exercise_id",
                "foreignField": "_id",
                "as": "exercise",
            }},
            {"$unwind": "$exercise"},
        ]
        results = list(self.db.attempts.aggregate(pipeline))

        if not results:
            return {"topics": {}, "difficulties": {}, "total": 0}

        topic_stats = defaultdict(lambda: {"correct": 0, "total": 0})
        diff_stats = defaultdict(lambda: {"correct": 0, "total": 0})

        for row in results:
            topic = row["exercise"]["topic"]
            diff = row["exercise"]["difficulty"]
            topic_stats[topic]["total"] += 1
            diff_stats[diff]["total"] += 1
            if row["is_correct"]:
                topic_stats[topic]["correct"] += 1
                diff_stats[diff]["correct"] += 1

        topics = {}
        for topic, stats in topic_stats.items():
            topics[topic] = {
                **stats,
                "accuracy": stats["correct"] / stats["total"] if stats["total"] > 0 else 0,
            }

        difficulties = {}
        for diff, stats in diff_stats.items():
            difficulties[diff] = {
                **stats,
                "accuracy": stats["correct"] / stats["total"] if stats["total"] > 0 else 0,
            }

        return {
            "topics": topics,
            "difficulties": difficulties,
            "total": len(results),
        }

    def compute_exercise_score(self, exercise, profile, attempted_ids):
        """
        Score an exercise for recommendation.
        Higher score = more recommended.
        """
        score = 0.0

        # Penalty for already attempted
        if exercise["_id"] in attempted_ids:
            score -= 5.0

        topic_info = profile["topics"].get(exercise.get("topic"))

        if topic_info is None:
            # Never attempted this topic - high priority for coverage
            score += 3.0
        else:
            accuracy = topic_info["accuracy"]
            if accuracy < 0.5:
                score += 4.0 - accuracy * 2
            elif accuracy < 0.8:
                score += 2.0
            else:
                score += 0.5

        # Difficulty appropriateness
        diff_info = profile["difficulties"]
        max_mastered = max(
            (d for d, s in diff_info.items() if s["accuracy"] > 0.6),
            default=1,
        )
        target_diff = min(max_mastered + 1, 5)

        diff_distance = abs(exercise.get("difficulty", 1) - target_diff)
        score -= diff_distance * 0.5

        return score

    def recommend(self, user_id: int, count: int = 5) -> list[dict]:
        """Get top N recommended exercises."""
        profile = self.get_user_profile(user_id)

        attempted_ids = set(
            a["exercise_id"]
            for a in self.db.attempts.find({"user_id": user_id}, {"exercise_id": 1})
        )

        all_exercises = list(self.db.exercises.find())

        scored = [
            (ex, self.compute_exercise_score(ex, profile, attempted_ids))
            for ex in all_exercises
        ]
        scored.sort(key=lambda x: x[1], reverse=True)

        return [exercise_to_dict(ex) for ex, _ in scored[:count]]
