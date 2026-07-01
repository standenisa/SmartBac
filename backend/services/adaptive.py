"""
Adaptive Learning Service - simplified SM-2-style spaced repetition
(fixed interval ladder scaled by ease factor)
Prioritizes: due reviews → weak topics → unexplored → progressive difficulty
"""

from datetime import datetime, timedelta
from typing import Optional

SM2_INTERVALS = [1, 3, 7, 14, 30]  # days
DEFAULT_EASE = 2.5


class AdaptiveLearning:
    def __init__(self, db):
        self.db = db

    def get_next_exercise(self, user_id: int) -> Optional[dict]:
        """Get the next best exercise for adaptive learning."""
        user = self.db.users.find_one({"_id": user_id})
        if not user:
            return None

        profile = user.get("profile", "M1")

        # 1. Spaced review due
        exercise = self._get_due_review(user_id, profile)
        if exercise:
            return exercise

        # 2. Weak topics (<50% accuracy)
        exercise = self._get_weak_topic_exercise(user_id, profile)
        if exercise:
            return exercise

        # 3. Unexplored topics
        exercise = self._get_unexplored_exercise(user_id, profile)
        if exercise:
            return exercise

        # 4. Progressive difficulty
        exercise = self._get_progressive_exercise(user_id, profile)
        if exercise:
            return exercise

        # Fallback: random exercise
        return self._get_random_exercise(profile)

    def _get_due_review(self, user_id: int, profile: str) -> Optional[dict]:
        now = datetime.utcnow()
        due_item = self.db.user_exercise_history.find_one(
            {"user_id": user_id, "next_review": {"$lte": now}},
            sort=[("next_review", 1)],
        )
        if due_item:
            exercise = self.db.exercises.find_one({
                "_id": due_item["exercise_id"],
                "$or": [{"profile": profile}, {"profile": "BOTH"}],
            })
            if exercise:
                return exercise
        return None

    def _topic_accuracy_pipeline(self, user_id: int) -> list:
        return [
            {"$match": {"user_id": user_id}},
            {"$group": {
                "_id": "$topic",
                "total": {"$sum": 1},
                "correct": {"$sum": {"$cond": [{"$gte": ["$quality", 3]}, 1, 0]}},
            }},
            {"$addFields": {"accuracy": {"$cond": [{"$gt": ["$total", 0]}, {"$divide": ["$correct", "$total"]}, 0]}}},
        ]

    def _seen_ids(self, user_id: int, topic: Optional[str] = None) -> list:
        query = {"user_id": user_id}
        if topic:
            query["topic"] = topic
        return [h["exercise_id"] for h in self.db.user_exercise_history.find(
            query, {"exercise_id": 1}
        )]

    def _get_weak_topic_exercise(self, user_id: int, profile: str) -> Optional[dict]:
        pipeline = self._topic_accuracy_pipeline(user_id) + [
            {"$match": {"accuracy": {"$lt": 0.5}, "total": {"$gte": 2}}},
            {"$sort": {"accuracy": 1}},
            {"$limit": 3},
        ]
        weak_topics = list(self.db.user_exercise_history.aggregate(pipeline))
        if not weak_topics:
            return None

        # Get recent topics to avoid 3+ consecutive
        recent = list(self.db.user_exercise_history.find(
            {"user_id": user_id}, sort=[("last_reviewed", -1)], limit=2
        ))
        recent_topics = [r.get("topic") for r in recent]

        for wt in weak_topics:
            topic = wt["_id"]
            # Topic mixing: skip if last 2 were same topic
            if len(recent_topics) >= 2 and all(t == topic for t in recent_topics):
                continue

            done_ids = self._seen_ids(user_id, topic)

            exercise = self.db.exercises.find_one({
                "_id": {"$nin": done_ids},
                "topic": topic,
                "$or": [{"profile": profile}, {"profile": "BOTH"}],
            })
            if exercise:
                return exercise
        return None

    def _get_unexplored_exercise(self, user_id: int, profile: str) -> Optional[dict]:
        seen_ids = self._seen_ids(user_id)
        return self.db.exercises.find_one({
            "_id": {"$nin": seen_ids},
            "$or": [{"profile": profile}, {"profile": "BOTH"}],
        })

    def _get_progressive_exercise(self, user_id: int, profile: str) -> Optional[dict]:
        pipeline = [
            {"$match": {"user_id": user_id, "quality": {"$gte": 3}}},
            {"$group": {"_id": None, "avg_diff": {"$avg": "$difficulty"}}},
        ]
        result = list(self.db.user_exercise_history.aggregate(pipeline))
        target_diff = min(5, int((result[0]["avg_diff"] if result else 1) + 0.5))

        seen_ids = self._seen_ids(user_id)
        return self.db.exercises.find_one({
            "_id": {"$nin": seen_ids},
            "difficulty": {"$gte": target_diff},
            "$or": [{"profile": profile}, {"profile": "BOTH"}],
        })

    def _get_random_exercise(self, profile: str) -> Optional[dict]:
        pipeline = [
            {"$match": {"$or": [{"profile": profile}, {"profile": "BOTH"}]}},
            {"$sample": {"size": 1}},
        ]
        result = list(self.db.exercises.aggregate(pipeline))
        return result[0] if result else None

    def record_attempt(self, user_id: int, exercise_id: int, is_correct: bool):
        """Record an attempt and update spaced repetition schedule."""
        exercise = self.db.exercises.find_one({"_id": exercise_id})
        if not exercise:
            return

        quality = 4 if is_correct else 1
        now = datetime.utcnow()

        existing = self.db.user_exercise_history.find_one({
            "user_id": user_id, "exercise_id": exercise_id,
        })

        if existing:
            repetition = existing.get("repetition", 0)
            ease_factor = existing.get("ease_factor", DEFAULT_EASE)

            if is_correct:
                repetition = min(repetition + 1, len(SM2_INTERVALS) - 1)
                ease_factor = max(1.3, ease_factor + 0.1 * (quality - 3))
            else:
                repetition = 0
                ease_factor = max(1.3, ease_factor - 0.2)

            interval_days = SM2_INTERVALS[repetition]
            next_review = now + timedelta(days=int(interval_days * ease_factor))

            self.db.user_exercise_history.update_one(
                {"_id": existing["_id"]},
                {"$set": {
                    "quality": quality,
                    "repetition": repetition,
                    "ease_factor": ease_factor,
                    "next_review": next_review,
                    "last_reviewed": now,
                }},
            )
        else:
            interval_days = SM2_INTERVALS[0]
            next_review = now + timedelta(days=interval_days)

            self.db.user_exercise_history.insert_one({
                "user_id": user_id,
                "exercise_id": exercise_id,
                "topic": exercise.get("topic", ""),
                "difficulty": exercise.get("difficulty", 1),
                "quality": quality,
                "repetition": 0 if not is_correct else 1,
                "ease_factor": DEFAULT_EASE,
                "next_review": next_review,
                "last_reviewed": now,
            })

    def get_weak_topics(self, user_id: int, count: int = 3) -> list:
        """Get the user's weakest topics."""
        pipeline = self._topic_accuracy_pipeline(user_id) + [
            {"$sort": {"accuracy": 1}},
            {"$limit": count},
        ]
        return list(self.db.user_exercise_history.aggregate(pipeline))
