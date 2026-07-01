"""
Advanced ML Predictor pentru BAC Prep AI
- Multiple algoritmi: Random Forest, XGBoost, Gradient Boosting, Neural Network
- Ensemble Learning cu voting/stacking
- Cross-validation și model selection
- Feature engineering avansat
"""

import json
import pickle
import numpy as np
from collections import defaultdict
import warnings

# Sklearn imports
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    VotingRegressor,
    StackingRegressor
)
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    KFold
)
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    mean_absolute_error
)
import os

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Try to import XGBoost (optional)
try:
    from xgboost import XGBRegressor
    XGBOOST_AVAILABLE = True
except Exception as e:
    XGBOOST_AVAILABLE = False
    print(f"XGBoost nu este disponibil: {e}. Folosind alternativă.")


class AdvancedGradePredictor:
    """
    Predictor avansat cu multiple modele și ensemble learning
    """

    FEATURE_NAMES = [
        'total_attempts', 'overall_accuracy',
        'subject1_acc', 'subject2_acc', 'subject3_acc',
        'avg_difficulty', 'avg_time',
        'learning_trend', 'consistency',
        'easy_acc', 'medium_acc', 'hard_acc', 'expert_acc',
        'time_efficiency', 'topic_diversity',
        'avg_topic_mastery', 'topic_mastery_variance',
        'streak_ratio', 'max_streak', 'recent_accuracy',
        'difficulty_progression', 'avg_correct_time'
    ]

    def __init__(self, model_type='ensemble'):
        """
        Args:
            model_type: 'random_forest', 'xgboost', 'gradient_boosting',
                       'neural_network', 'ensemble', 'stacking'
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = []
        self.training_metrics = {}
        self.feature_importances = {}

        self._init_models()

    def _init_models(self):
        """Inițializează toate modelele disponibile"""

        # Random Forest optimizat
        self.rf_model = RandomForestRegressor(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features='sqrt',
            random_state=42,
            n_jobs=-1
        )

        # Gradient Boosting
        self.gb_model = GradientBoostingRegressor(
            n_estimators=150,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            min_samples_split=5,
            random_state=42
        )

        # XGBoost (dacă disponibil)
        if XGBOOST_AVAILABLE:
            self.xgb_model = XGBRegressor(
                n_estimators=150,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                verbosity=0
            )
        else:
            self.xgb_model = None

        # Neural Network
        self.nn_model = MLPRegressor(
            hidden_layer_sizes=(64, 32, 16),
            activation='relu',
            solver='adam',
            alpha=0.001,
            learning_rate='adaptive',
            max_iter=500,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1
        )

        # Ridge Regression (pentru stacking)
        self.ridge_model = Ridge(alpha=1.0)

    @staticmethod
    def _group_by_subject(attempts):
        """Grupează rezultatele (is_correct) pe subiecte 1-3."""
        subjects = {1: [], 2: [], 3: []}
        for attempt in attempts:
            subject = attempt.get('exercise_subject', 1)
            subjects[subject].append(attempt['is_correct'])
        return subjects

    def extract_advanced_features(self, attempts):
        """
        Extrage features avansate din încercările studentului

        Returns:
            numpy array cu 20+ features
        """
        if not attempts:
            return np.zeros(len(self.FEATURE_NAMES))

        # === FEATURES DE BAZĂ (7) ===
        total_attempts = len(attempts)
        correct = sum(1 for a in attempts if a['is_correct'])
        overall_accuracy = correct / total_attempts

        # Acuratețe pe subiecte
        subjects = self._group_by_subject(attempts)

        subject1_acc = np.mean(subjects[1]) if subjects[1] else 0
        subject2_acc = np.mean(subjects[2]) if subjects[2] else 0
        subject3_acc = np.mean(subjects[3]) if subjects[3] else 0

        # Dificultate și timp
        difficulties = [a.get('exercise_difficulty', 2) for a in attempts]
        times = [a.get('time_spent', 60) for a in attempts]

        avg_difficulty = np.mean(difficulties)
        avg_time = np.mean(times)

        # === FEATURES AVANSATE ===

        # 1. Trend de învățare (ultimele 5 vs primele 5)
        if len(attempts) >= 10:
            first_5_acc = np.mean([a['is_correct'] for a in attempts[:5]])
            last_5_acc = np.mean([a['is_correct'] for a in attempts[-5:]])
            learning_trend = last_5_acc - first_5_acc
        else:
            learning_trend = 0

        # 2. Variabilitate performanță (consistență)
        if len(attempts) >= 5:
            # Moving average accuracy
            window_accs = []
            window_size = min(5, len(attempts) // 2)
            for i in range(0, len(attempts) - window_size + 1, window_size):
                window = attempts[i:i+window_size]
                window_accs.append(np.mean([a['is_correct'] for a in window]))
            consistency = 1 - np.std(window_accs) if window_accs else 1
        else:
            consistency = 0.5

        # 3. Performanță pe nivele de dificultate
        diff_performance = {1: [], 2: [], 3: [], 4: []}
        for a in attempts:
            diff = a.get('exercise_difficulty', 2)
            diff_performance[diff].append(a['is_correct'])

        easy_acc = np.mean(diff_performance[1]) if diff_performance[1] else 0
        medium_acc = np.mean(diff_performance[2]) if diff_performance[2] else 0
        hard_acc = np.mean(diff_performance[3]) if diff_performance[3] else 0
        expert_acc = np.mean(diff_performance[4]) if diff_performance[4] else 0

        # 4. Time efficiency (răspunsuri corecte rapide)
        correct_times = [a.get('time_spent', 60) for a in attempts if a['is_correct']]
        wrong_times = [a.get('time_spent', 60) for a in attempts if not a['is_correct']]

        avg_correct_time = np.mean(correct_times) if correct_times else 60
        avg_wrong_time = np.mean(wrong_times) if wrong_times else 120
        time_efficiency = avg_correct_time / avg_wrong_time if avg_wrong_time > 0 else 1

        # 5. Topic mastery (câte topicuri diferite a rezolvat)
        topics = set(a.get('exercise_topic', 'unknown') for a in attempts)
        topic_diversity = len(topics) / 20  # Normalizat la numărul estimat de topicuri

        # Topic-specific accuracy
        topic_accs = defaultdict(list)
        for a in attempts:
            topic_accs[a.get('exercise_topic', 'unknown')].append(a['is_correct'])

        topic_mastery_scores = [np.mean(accs) for accs in topic_accs.values()]
        avg_topic_mastery = np.mean(topic_mastery_scores) if topic_mastery_scores else 0
        topic_mastery_variance = np.std(topic_mastery_scores) if len(topic_mastery_scores) > 1 else 0

        # 6. Streak analysis
        current_streak = 0
        max_streak = 0
        for a in attempts:
            if a['is_correct']:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0

        streak_ratio = max_streak / total_attempts

        # 7. Recent performance (ultimele 10 exerciții)
        recent_attempts = attempts[-10:] if len(attempts) >= 10 else attempts
        recent_accuracy = np.mean([a['is_correct'] for a in recent_attempts])

        # 8. Difficulty progression (încearcă exerciții mai grele în timp?)
        if len(attempts) >= 10:
            first_half_diff = np.mean([a.get('exercise_difficulty', 2) for a in attempts[:len(attempts)//2]])
            second_half_diff = np.mean([a.get('exercise_difficulty', 2) for a in attempts[len(attempts)//2:]])
            difficulty_progression = second_half_diff - first_half_diff
        else:
            difficulty_progression = 0

        features = [
            # Bază (7)
            total_attempts,
            overall_accuracy,
            subject1_acc,
            subject2_acc,
            subject3_acc,
            avg_difficulty,
            avg_time,
            # Avansate (15)
            learning_trend,
            consistency,
            easy_acc,
            medium_acc,
            hard_acc,
            expert_acc,
            time_efficiency,
            topic_diversity,
            avg_topic_mastery,
            topic_mastery_variance,
            streak_ratio,
            max_streak,
            recent_accuracy,
            difficulty_progression,
            avg_correct_time
        ]

        self.feature_names = list(self.FEATURE_NAMES)

        return np.array(features)

    def load_training_data(self):
        """Încarcă și procesează datele de antrenare"""
        print("Încărcare date de antrenare...")

        attempts_path = os.path.join(_BASE_DIR, 'data', 'synthetic_attempts.json')
        grades_path = os.path.join(_BASE_DIR, 'data', 'student_grades.json')

        if not os.path.exists(attempts_path):
            raise FileNotFoundError("Nu găsesc fișierele de date!")

        with open(attempts_path, 'r', encoding='utf-8') as f:
            all_attempts = json.load(f)

        with open(grades_path, 'r', encoding='utf-8') as f:
            student_grades = json.load(f)

        # Grupează attempts pe student
        students_attempts = defaultdict(list)
        for attempt in all_attempts:
            user_id = attempt['user_id']
            students_attempts[user_id].append(attempt)

        # Creează dataset cu features avansate
        X = []
        y = []

        for student in student_grades:
            user_id = student['user_id']
            grade = student['grade']

            if user_id in students_attempts:
                features = self.extract_advanced_features(students_attempts[user_id])
                X.append(features)
                y.append(grade)

        print(f"   {len(X)} studenți încărcați cu {len(self.feature_names)} features")

        return np.array(X), np.array(y)

    def _cross_validate(self, model, X, y):
        """Cross-validation 5-fold; returnează (r2_mean, r2_std, rmse_mean, rmse_std)."""
        kfold = KFold(n_splits=5, shuffle=True, random_state=42)
        cv_scores = cross_val_score(model, X, y, cv=kfold, scoring='r2')
        cv_rmse = cross_val_score(
            model, X, y, cv=kfold,
            scoring='neg_root_mean_squared_error'
        )
        return cv_scores.mean(), cv_scores.std(), -cv_rmse.mean(), cv_rmse.std()

    def train(self, X=None, y=None):
        """Antrenează modelul selectat cu cross-validation"""
        print(f"\nAntrenare model: {self.model_type.upper()}")

        # Încarcă date dacă nu sunt furnizate
        if X is None or y is None:
            X, y = self.load_training_data()

        # Scalare features
        X_scaled = self.scaler.fit_transform(X)

        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )

        print(f"   Train: {len(X_train)} | Test: {len(X_test)}")

        # Selectează și antrenează modelul
        if self.model_type == 'random_forest':
            self.model = self.rf_model

        elif self.model_type == 'gradient_boosting':
            self.model = self.gb_model

        elif self.model_type == 'xgboost':
            if XGBOOST_AVAILABLE:
                self.model = self.xgb_model
            else:
                print("   XGBoost indisponibil, folosesc Gradient Boosting")
                self.model = self.gb_model

        elif self.model_type == 'neural_network':
            self.model = self.nn_model

        elif self.model_type == 'ensemble':
            # Voting ensemble
            estimators = [
                ('rf', self.rf_model),
                ('gb', self.gb_model),
                ('nn', self.nn_model)
            ]
            if XGBOOST_AVAILABLE:
                estimators.append(('xgb', self.xgb_model))

            self.model = VotingRegressor(estimators=estimators)

        elif self.model_type == 'stacking':
            # Stacking ensemble
            base_estimators = [
                ('rf', self.rf_model),
                ('gb', self.gb_model)
            ]
            if XGBOOST_AVAILABLE:
                base_estimators.append(('xgb', self.xgb_model))

            self.model = StackingRegressor(
                estimators=base_estimators,
                final_estimator=self.ridge_model,
                cv=5
            )
        else:
            self.model = self.rf_model

        # Antrenare
        print("   Antrenare în curs...")
        self.model.fit(X_train, y_train)

        # Evaluare pe test set
        y_pred = self.model.predict(X_test)

        # Metrici
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Cross-validation scores
        cv_r2_mean, cv_r2_std, cv_rmse_mean, cv_rmse_std = self._cross_validate(self.model, X_scaled, y)

        self.training_metrics = {
            'rmse': rmse,
            'mae': mae,
            'r2': r2,
            'cv_r2_mean': cv_r2_mean,
            'cv_r2_std': cv_r2_std,
            'cv_rmse_mean': cv_rmse_mean,
            'cv_rmse_std': cv_rmse_std
        }

        print("\n   Model antrenat!")
        print("   Metrici Test Set:")
        print(f"      RMSE: {rmse:.3f}")
        print(f"      MAE: {mae:.3f}")
        print(f"      R² Score: {r2:.3f}")
        print("\n   Cross-Validation (5-fold):")
        print(f"      R² Mean: {cv_r2_mean:.3f} ± {cv_r2_std:.3f}")
        print(f"      RMSE Mean: {cv_rmse_mean:.3f} ± {cv_rmse_std:.3f}")

        self.is_trained = True

        # Feature importance (dacă disponibilă)
        self._compute_feature_importance()

        return self.training_metrics

    def _compute_feature_importance(self):
        """Calculează importanța features"""
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
        elif hasattr(self.model, 'named_estimators_'):
            # Pentru ensemble, facem media
            all_importances = []
            for name, est in self.model.named_estimators_.items():
                if hasattr(est, 'feature_importances_'):
                    all_importances.append(est.feature_importances_)
            if all_importances:
                importances = np.mean(all_importances, axis=0)
            else:
                return
        else:
            return

        self.feature_importances = dict(zip(self.feature_names, importances))

        print("\n   Top 10 Feature Importance:")
        sorted_features = sorted(
            self.feature_importances.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        for name, importance in sorted_features:
            print(f"      {name}: {importance:.4f}")

    def predict(self, student_attempts):
        """
        Prezice nota BAC cu confidence interval
        """
        if not self.is_trained:
            raise Exception("Modelul nu este antrenat!")

        features = self.extract_advanced_features(student_attempts)
        features_scaled = self.scaler.transform([features])

        predicted_grade = self.model.predict(features_scaled)[0]

        # Calculează confidence interval bazat pe variance
        # Pentru ensemble, folosim variance între modele
        predictions_variance = 0.3  # Default

        if hasattr(self.model, 'named_estimators_'):
            individual_preds = []
            for name, est in self.model.named_estimators_.items():
                try:
                    pred = est.predict(features_scaled)[0]
                    individual_preds.append(pred)
                except Exception:
                    pass
            if individual_preds:
                predictions_variance = np.std(individual_preds)

        # Confidence interval (95%)
        confidence_margin = max(0.3, min(1.0, predictions_variance * 1.96))

        # Subject breakdown
        subjects = self._group_by_subject(student_attempts)

        subject_breakdown = {}
        for subject, results in subjects.items():
            if results:
                acc = np.mean(results)
                estimated_points = acc * 30
                subject_breakdown[f'subject_{subject}'] = {
                    'accuracy': round(acc * 100, 1),
                    'estimated_points': round(estimated_points, 1),
                    'max_points': 30,
                    'exercises_solved': len(results)
                }

        # Insights bazate pe features
        insights = self._generate_insights(features, student_attempts)

        return {
            'predicted_grade': round(max(1.0, min(10.0, predicted_grade)), 2),
            'confidence_interval': [
                round(max(1.0, predicted_grade - confidence_margin), 2),
                round(min(10.0, predicted_grade + confidence_margin), 2)
            ],
            'confidence_level': self._get_confidence_level(len(student_attempts)),
            'breakdown': subject_breakdown,
            'total_attempts': len(student_attempts),
            'insights': insights,
            'model_type': self.model_type
        }

    def _get_confidence_level(self, num_attempts):
        """Returnează nivelul de încredere bazat pe numărul de încercări"""
        if num_attempts < 15:
            return 'low'
        elif num_attempts < 30:
            return 'medium'
        elif num_attempts < 50:
            return 'high'
        else:
            return 'very_high'

    def _generate_insights(self, features, attempts):
        """Generează insights personalizate"""
        insights = []

        # Learning trend
        learning_trend = features[7]  # index pentru learning_trend
        if learning_trend > 0.1:
            insights.append({
                'type': 'positive',
                'message': 'Progresezi foarte bine! Performanța ta se îmbunătățește constant.'
            })
        elif learning_trend < -0.1:
            insights.append({
                'type': 'warning',
                'message': 'Performanța pare să scadă. Ia o pauză și revino odihnit!'
            })

        # Consistency
        consistency = features[8]
        if consistency > 0.8:
            insights.append({
                'type': 'positive',
                'message': 'Ai o performanță foarte consistentă. Continuă așa!'
            })
        elif consistency < 0.5:
            insights.append({
                'type': 'tip',
                'message': 'Rezultatele variază mult. Încearcă să exersezi mai regulat.'
            })

        # Subject weaknesses
        subject_accs = [features[2], features[3], features[4]]
        weakest_subject = np.argmin(subject_accs) + 1
        if min(subject_accs) < 0.5:
            insights.append({
                'type': 'focus',
                'message': f'Concentrează-te pe Subiectul {weakest_subject} pentru îmbunătățire.'
            })

        # Difficulty progression
        if features[9] < 0.5 and features[10] < 0.5:  # easy_acc și medium_acc
            insights.append({
                'type': 'tip',
                'message': 'Începe cu exerciții mai ușoare pentru a-ți construi încrederea.'
            })

        # Topic diversity
        if features[14] < 0.3:  # topic_diversity
            insights.append({
                'type': 'tip',
                'message': 'Încearcă să rezolvi exerciții din mai multe topicuri diferite.'
            })

        return insights

    def compare_models(self, X=None, y=None):
        """Compară toate modelele disponibile"""
        print("\nComparare modele ML...")

        if X is None or y is None:
            X, y = self.load_training_data()

        X_scaled = self.scaler.fit_transform(X)

        models = {
            'Random Forest': self.rf_model,
            'Gradient Boosting': self.gb_model,
            'Neural Network': self.nn_model
        }

        if XGBOOST_AVAILABLE:
            models['XGBoost'] = self.xgb_model

        results = {}

        for name, model in models.items():
            print(f"\n   Testing {name}...")
            r2_mean, r2_std, rmse_mean, rmse_std = self._cross_validate(model, X_scaled, y)

            results[name] = {
                'r2_mean': r2_mean,
                'r2_std': r2_std,
                'rmse_mean': rmse_mean,
                'rmse_std': rmse_std
            }

            print(f"      R²: {r2_mean:.3f} ± {r2_std:.3f}")
            print(f"      RMSE: {rmse_mean:.3f} ± {rmse_std:.3f}")

        # Găsește cel mai bun model
        best_model = max(results.items(), key=lambda x: x[1]['r2_mean'])
        print(f"\n   Cel mai bun model: {best_model[0]}")

        return results

    def save(self, filepath=os.path.join(_BASE_DIR, 'models', 'grade_predictor_advanced.pkl')):
        """Salvează modelul și scalerul"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        save_data = {
            'model': self.model,
            'scaler': self.scaler,
            'model_type': self.model_type,
            'feature_names': self.feature_names,
            'training_metrics': self.training_metrics,
            'feature_importances': self.feature_importances
        }

        with open(filepath, 'wb') as f:
            pickle.dump(save_data, f)

        print(f"\nModel salvat în: {filepath}")

    def load(self, filepath=os.path.join(_BASE_DIR, 'models', 'grade_predictor_advanced.pkl')):
        """Încarcă model salvat"""
        with open(filepath, 'rb') as f:
            save_data = pickle.load(f)

        self.model = save_data['model']
        self.scaler = save_data['scaler']
        self.model_type = save_data['model_type']
        self.feature_names = save_data['feature_names']
        self.training_metrics = save_data.get('training_metrics', {})
        self.feature_importances = save_data.get('feature_importances', {})
        self.is_trained = True

        print(f"Model încărcat: {self.model_type}")

    def get_model_info(self):
        """Returnează informații despre model"""
        return {
            'model_type': self.model_type,
            'is_trained': self.is_trained,
            'num_features': len(self.feature_names),
            'feature_names': self.feature_names,
            'training_metrics': self.training_metrics,
            'top_features': dict(sorted(
                self.feature_importances.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]) if self.feature_importances else {}
        }


if __name__ == '__main__':
    warnings.filterwarnings('ignore')

    print("BAC Prep AI - Advanced ML Training")

    predictor = AdvancedGradePredictor(model_type='ensemble')

    predictor.compare_models()

    print("\nAntrenare model ENSEMBLE final...")

    predictor.train()
    predictor.save()

    print("\nModel Info:")
    info = predictor.get_model_info()
    for key, value in info.items():
        print(f"   {key}: {value}")

    print("\nModel avansat gata de folosit!")
