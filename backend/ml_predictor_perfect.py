"""
Grade predictor antrenat pe Kaggle (notebook prezicere-note.ipynb).

Incarca artifact-ul grade_predictor_perfect.pkl (dict cu model sklearn,
feature_names, metrici) si reproduce exact extractia de features din notebook,
ca predictiile locale sa fie identice cu cele de la antrenare.
"""

import os
import pickle
from collections import defaultdict

import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin, clone
from sklearn.utils.validation import check_is_fitted

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODEL_PATH = os.path.join(_BASE_DIR, "models", "grade_predictor_perfect.pkl")

FEATURE_NAMES = [
    "total_attempts",
    "overall_accuracy",
    "subject1_acc",
    "subject2_acc",
    "subject3_acc",
    "avg_difficulty",
    "std_difficulty",
    "avg_time",
    "median_time",
    "std_time",
    "learning_trend",
    "consistency",
    "easy_acc",
    "medium_acc",
    "hard_acc",
    "expert_acc",
    "time_efficiency",
    "topic_diversity",
    "avg_topic_mastery",
    "topic_mastery_variance",
    "streak_ratio",
    "max_streak_ratio",
    "recent_accuracy",
    "difficulty_progression",
    "avg_correct_time",
    "attempt_density",
    "subject_balance",
    "hard_attempt_ratio",
    "fast_correct_ratio",
    "slow_wrong_ratio",
]


# Clasele de mai jos exista in pickle sub __main__ (definite in notebook);
# trebuie sa fie identice aici ca artifact-ul sa se poata deserializa.
class ClippedRegressor(BaseEstimator, RegressorMixin):
    def __init__(self, estimator=None, low=1.0, high=10.0):
        self.estimator = estimator
        self.low = low
        self.high = high

    def fit(self, X, y):
        self.estimator_ = clone(self.estimator)
        self.estimator_.fit(X, y)
        return self

    def predict(self, X):
        check_is_fitted(self, "estimator_")
        return np.clip(self.estimator_.predict(X), self.low, self.high)


class AsRegressor(RegressorMixin, BaseEstimator):
    def __init__(self, estimator):
        self.estimator = estimator

    def fit(self, X, y, **kwargs):
        self.estimator_ = clone(self.estimator).fit(X, y, **kwargs)
        return self

    def predict(self, X):
        return self.estimator_.predict(X)


class _ArtifactUnpickler(pickle.Unpickler):
    """Mapeaza clasele salvate din __main__ (notebook) la cele din acest modul."""

    def find_class(self, module, name):
        if name in ("AsRegressor", "ClippedRegressor"):
            return globals()[name]
        return super().find_class(module, name)


def safe_float(value, default=0.0):
    try:
        if value is None:
            return default
        value = float(value)
        if np.isfinite(value):
            return value
        return default
    except Exception:
        return default


def safe_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in {"true", "1", "yes", "da", "corect"}
    return bool(value)


def attempt_sort_key(item):
    keys = ["created_at", "timestamp", "date", "time", "attempted_at", "submitted_at"]
    for key in keys:
        if key in item and item[key] is not None:
            return str(item[key])
    return ""


def mean_or(values, default=0.0):
    return float(np.mean(values)) if len(values) else float(default)


def std_or(values, default=0.0):
    return float(np.std(values)) if len(values) else float(default)


def extract_features(attempts):
    """Portat 1:1 din notebookul de antrenare - nu modifica fara reantrenare."""
    attempts = sorted(attempts, key=attempt_sort_key)
    total = len(attempts)
    if total == 0:
        return np.zeros(len(FEATURE_NAMES), dtype=float)

    correct_values = np.array([1.0 if safe_bool(a.get("is_correct", False)) else 0.0 for a in attempts], dtype=float)
    difficulties = np.array([safe_float(a.get("exercise_difficulty", 2), 2) for a in attempts], dtype=float)
    times = np.array([max(safe_float(a.get("time_spent", 60), 60), 0.0) for a in attempts], dtype=float)
    subjects = [int(safe_float(a.get("exercise_subject", 1), 1)) for a in attempts]
    topics = [str(a.get("exercise_topic", "unknown")) for a in attempts]

    accuracy = mean_or(correct_values)
    subject_accs = []
    subject_counts = []
    for subject in [1, 2, 3]:
        vals = [correct_values[i] for i, s in enumerate(subjects) if s == subject]
        subject_accs.append(mean_or(vals, accuracy))
        subject_counts.append(len(vals))

    avg_diff = mean_or(difficulties, 2.0)
    std_diff = std_or(difficulties)
    avg_time = mean_or(times, 60.0)
    median_time = float(np.median(times)) if len(times) else 60.0
    std_time = std_or(times)

    if total >= 10:
        k = max(5, total // 5)
        learning_trend = mean_or(correct_values[-k:]) - mean_or(correct_values[:k])
        difficulty_progression = mean_or(difficulties[total // 2:]) - mean_or(difficulties[:total // 2])
    else:
        learning_trend = 0.0
        difficulty_progression = 0.0

    window = max(3, min(10, total // 4))
    if total >= window:
        window_accs = [mean_or(correct_values[i:i + window]) for i in range(0, total - window + 1, window)]
        consistency = max(0.0, 1.0 - std_or(window_accs))
    else:
        consistency = 0.5

    diff_accs = []
    for difficulty in [1, 2, 3, 4]:
        vals = [correct_values[i] for i, d in enumerate(difficulties) if int(round(d)) == difficulty]
        diff_accs.append(mean_or(vals, accuracy))

    correct_times = times[correct_values == 1.0]
    wrong_times = times[correct_values == 0.0]
    avg_correct_time = mean_or(correct_times, avg_time)
    avg_wrong_time = mean_or(wrong_times, avg_time)
    time_efficiency = avg_correct_time / avg_wrong_time if avg_wrong_time > 0 else 1.0

    topic_values = defaultdict(list)
    for topic, value in zip(topics, correct_values):
        topic_values[topic].append(value)
    topic_scores = [mean_or(v) for v in topic_values.values()]
    topic_diversity = min(len(topic_values) / 20.0, 1.0)
    avg_topic_mastery = mean_or(topic_scores, accuracy)
    topic_mastery_variance = std_or(topic_scores)

    current_streak = 0
    max_streak = 0
    for value in correct_values:
        if value == 1.0:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0

    recent_k = min(10, total)
    recent_accuracy = mean_or(correct_values[-recent_k:])
    streak_ratio = current_streak / total
    max_streak_ratio = max_streak / total
    attempt_density = np.log1p(total)
    subject_balance = 1.0 - np.std(np.array(subject_counts, dtype=float) / max(total, 1))
    hard_attempt_ratio = float(np.mean(difficulties >= 3)) if total else 0.0
    q25 = np.quantile(times, 0.25) if total else 0.0
    q75 = np.quantile(times, 0.75) if total else 0.0
    fast_correct_ratio = float(np.mean((times <= q25) & (correct_values == 1.0))) if total else 0.0
    slow_wrong_ratio = float(np.mean((times >= q75) & (correct_values == 0.0))) if total else 0.0

    features = np.array([
        total,
        accuracy,
        subject_accs[0],
        subject_accs[1],
        subject_accs[2],
        avg_diff,
        std_diff,
        avg_time,
        median_time,
        std_time,
        learning_trend,
        consistency,
        diff_accs[0],
        diff_accs[1],
        diff_accs[2],
        diff_accs[3],
        time_efficiency,
        topic_diversity,
        avg_topic_mastery,
        topic_mastery_variance,
        streak_ratio,
        max_streak_ratio,
        recent_accuracy,
        difficulty_progression,
        avg_correct_time,
        attempt_density,
        subject_balance,
        hard_attempt_ratio,
        fast_correct_ratio,
        slow_wrong_ratio,
    ], dtype=float)

    return np.nan_to_num(features, nan=0.0, posinf=0.0, neginf=0.0)


class PerfectGradePredictor:
    """Wrapper peste artifactul Kaggle, cu aceeasi interfata ca AdvancedGradePredictor."""

    def __init__(self):
        self.model = None
        self.model_name = None
        self.feature_names = list(FEATURE_NAMES)
        self.holdout_metrics = {}
        self.cv_results = []
        self.is_trained = False
        self.model_type = "kaggle"

    def load(self, filepath=DEFAULT_MODEL_PATH):
        with open(filepath, "rb") as f:
            artifact = _ArtifactUnpickler(f).load()

        self.model = artifact["model"]
        self.model_name = artifact.get("model_name", "unknown")
        self.feature_names = artifact.get("feature_names", list(FEATURE_NAMES))
        self.holdout_metrics = artifact.get("holdout_metrics", {})
        self.cv_results = artifact.get("cv_results", [])
        self.model_type = f"kaggle_{self.model_name}"
        self.is_trained = True

        if list(self.feature_names) != list(FEATURE_NAMES):
            raise ValueError("feature_names din artifact difera de extract_features local")

        print(f"Model Kaggle incarcat: {self.model_name} ({self.holdout_metrics})")

    def _confidence_margin(self, features_row):
        """Interval din variatia intre sub-modelele ensemble-ului, altfel din RMSE holdout."""
        estimators = getattr(self.model, "estimators_", None)
        if estimators:
            preds = []
            for est in estimators:
                try:
                    preds.append(float(est.predict(features_row)[0]))
                except Exception:
                    pass
            if len(preds) >= 2:
                return max(0.3, min(1.0, float(np.std(preds)) * 1.96))

        rmse = safe_float(self.holdout_metrics.get("rmse"), 0.0)
        if rmse > 0:
            return max(0.3, min(1.0, rmse * 1.96))
        return 0.5

    @staticmethod
    def _confidence_level(num_attempts):
        if num_attempts < 15:
            return "low"
        elif num_attempts < 30:
            return "medium"
        elif num_attempts < 50:
            return "high"
        return "very_high"

    def _generate_insights(self, features):
        f = dict(zip(FEATURE_NAMES, features))
        insights = []

        if f["learning_trend"] > 0.1:
            insights.append({"type": "positive", "message": "Progresezi foarte bine! Performanta ta se imbunatateste constant."})
        elif f["learning_trend"] < -0.1:
            insights.append({"type": "warning", "message": "Performanta pare sa scada. Ia o pauza si revino odihnit!"})

        if f["consistency"] > 0.8:
            insights.append({"type": "positive", "message": "Ai o performanta foarte consistenta. Continua asa!"})
        elif f["consistency"] < 0.5:
            insights.append({"type": "tip", "message": "Rezultatele variaza mult. Incearca sa exersezi mai regulat."})

        subject_accs = [f["subject1_acc"], f["subject2_acc"], f["subject3_acc"]]
        weakest = int(np.argmin(subject_accs)) + 1
        if min(subject_accs) < 0.5:
            insights.append({"type": "focus", "message": f"Concentreaza-te pe Subiectul {weakest} pentru imbunatatire."})

        if f["easy_acc"] < 0.5 and f["medium_acc"] < 0.5:
            insights.append({"type": "tip", "message": "Incepe cu exercitii mai usoare pentru a-ti construi increderea."})

        if f["topic_diversity"] < 0.3:
            insights.append({"type": "tip", "message": "Incearca sa rezolvi exercitii din mai multe topicuri diferite."})

        return insights

    def predict(self, student_attempts):
        if not self.is_trained:
            raise Exception("Modelul nu este incarcat!")

        features = extract_features(student_attempts)
        features_row = features.reshape(1, -1)

        predicted_grade = float(self.model.predict(features_row)[0])
        predicted_grade = max(1.0, min(10.0, predicted_grade))
        margin = self._confidence_margin(features_row)

        subjects = defaultdict(list)
        for attempt in student_attempts:
            subject = int(safe_float(attempt.get("exercise_subject", 1), 1))
            subjects[subject].append(1.0 if safe_bool(attempt.get("is_correct", False)) else 0.0)

        breakdown = {}
        for subject, results in sorted(subjects.items()):
            acc = mean_or(results)
            breakdown[f"subject_{subject}"] = {
                "accuracy": round(acc * 100, 1),
                "estimated_points": round(acc * 30, 1),
                "max_points": 30,
                "exercises_solved": len(results),
            }

        return {
            "predicted_grade": round(predicted_grade, 2),
            "confidence_interval": [
                round(max(1.0, predicted_grade - margin), 2),
                round(min(10.0, predicted_grade + margin), 2),
            ],
            "confidence_level": self._confidence_level(len(student_attempts)),
            "breakdown": breakdown,
            "total_attempts": len(student_attempts),
            "insights": self._generate_insights(features),
            "model_type": self.model_type,
        }

    def get_model_info(self):
        return {
            "model_type": self.model_type,
            "model_name": self.model_name,
            "is_trained": self.is_trained,
            "num_features": len(self.feature_names),
            "feature_names": list(self.feature_names),
            "holdout_metrics": self.holdout_metrics,
        }
