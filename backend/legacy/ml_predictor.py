import json
import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import os

class GradePredictor:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.is_trained = False
    
    def extract_features(self, attempts):
        """
        Extrage features din încercările unui student
        
        Returns:
            list: [total_attempts, accuracy, subject1_acc, subject2_acc, 
                   subject3_acc, avg_difficulty, avg_time]
        """
        if not attempts:
            return [0, 0, 0, 0, 0, 0, 0]
        
        # Total încercări
        total_attempts = len(attempts)
        
        # Acuratețe generală
        correct = sum(1 for a in attempts if a['is_correct'])
        accuracy = correct / total_attempts if total_attempts > 0 else 0
        
        # Acuratețe pe subiecte
        subjects = {1: [], 2: [], 3: []}
        for attempt in attempts:
            subject = attempt['exercise_subject']
            subjects[subject].append(attempt['is_correct'])
        
        subject1_acc = sum(subjects[1]) / len(subjects[1]) if subjects[1] else 0
        subject2_acc = sum(subjects[2]) / len(subjects[2]) if subjects[2] else 0
        subject3_acc = sum(subjects[3]) / len(subjects[3]) if subjects[3] else 0
        
        # Dificultate medie exerciții
        avg_difficulty = sum(a['exercise_difficulty'] for a in attempts) / total_attempts
        
        # Timp mediu per exercițiu
        avg_time = sum(a['time_spent'] for a in attempts) / total_attempts
        
        return [
            total_attempts,
            accuracy,
            subject1_acc,
            subject2_acc,
            subject3_acc,
            avg_difficulty,
            avg_time
        ]
    
    def load_training_data(self):
        """Încarcă datele de antrenare"""
        print("📂 Încărcare date de antrenare...")
        
        # Încarcă attempts
        with open('backend/data/synthetic_attempts.json', 'r', encoding='utf-8') as f:
            all_attempts = json.load(f)
        
        # Încarcă grades
        with open('backend/data/student_grades.json', 'r', encoding='utf-8') as f:
            student_grades = json.load(f)
        
        # Grupează attempts pe student
        students_attempts = {}
        for attempt in all_attempts:
            user_id = attempt['user_id']
            if user_id not in students_attempts:
                students_attempts[user_id] = []
            students_attempts[user_id].append(attempt)
        
        # Creează dataset X (features) și y (grades)
        X = []
        y = []
        
        for student in student_grades:
            user_id = student['user_id']
            grade = student['grade']
            
            if user_id in students_attempts:
                features = self.extract_features(students_attempts[user_id])
                X.append(features)
                y.append(grade)
        
        print(f"   ✓ {len(X)} studenți încărcați")
        
        return np.array(X), np.array(y)
    
    def train(self):
        """Antrenează modelul"""
        print("\n🤖 Antrenare model ML...")
        
        # Încarcă date
        X, y = self.load_training_data()
        
        # Split train/test (80/20)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"   📊 Train set: {len(X_train)} studenți")
        print(f"   📊 Test set: {len(X_test)} studenți")
        
        # Antrenare
        print("   🔄 Antrenare în curs...")
        self.model.fit(X_train, y_train)
        
        # Evaluare
        y_pred = self.model.predict(X_test)
        
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"\n   ✅ Model antrenat!")
        print(f"   📈 Metrici:")
        print(f"      RMSE: {rmse:.3f}")
        print(f"      MAE: {mae:.3f}")
        print(f"      R² Score: {r2:.3f}")
        
        self.is_trained = True
        
        # Feature importance
        feature_names = [
            'Total exerciții',
            'Acuratețe generală',
            'Acuratețe Subiect I',
            'Acuratețe Subiect II',
            'Acuratețe Subiect III',
            'Dificultate medie',
            'Timp mediu'
        ]
        
        importances = self.model.feature_importances_
        print(f"\n   🎯 Feature Importance:")
        for name, importance in sorted(zip(feature_names, importances), 
                                      key=lambda x: x[1], reverse=True):
            print(f"      {name}: {importance:.3f}")
        
        return rmse, mae, r2
    
    def predict(self, student_attempts):
        """
        Prezice nota unui student bazat pe încercările lui
        
        Args:
            student_attempts: Lista de attempts ale studentului
            
        Returns:
            dict: Predicție cu notă și breakdown
        """
        if not self.is_trained:
            raise Exception("Model not trained! Call train() first.")
        
        # Extrage features
        features = self.extract_features(student_attempts)
        
        # Predicție
        predicted_grade = self.model.predict([features])[0]
        
        # Calculează breakdown pe subiecte
        subjects = {1: [], 2: [], 3: []}
        for attempt in student_attempts:
            subject = attempt['exercise_subject']
            subjects[subject].append(attempt['is_correct'])
        
        subject_breakdown = {}
        for subject, results in subjects.items():
            if results:
                acc = sum(results) / len(results)
                estimated_points = acc * 30  # Fiecare subiect = 30 puncte
                subject_breakdown[f'subject_{subject}'] = {
                    'accuracy': round(acc * 100, 1),
                    'estimated_points': round(estimated_points, 1),
                    'max_points': 30
                }
        
        return {
            'predicted_grade': round(predicted_grade, 2),
            'confidence_interval': [
                round(max(1.0, predicted_grade - 0.5), 2),
                round(min(10.0, predicted_grade + 0.5), 2)
            ],
            'breakdown': subject_breakdown,
            'total_attempts': len(student_attempts)
        }
    
    def save(self, filepath='backend/models/grade_predictor.pkl'):
        """Salvează modelul antrenat"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"\n💾 Model salvat în: {filepath}")
    
    def load(self, filepath='backend/models/grade_predictor.pkl'):
        """Încarcă model salvat"""
        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)
        self.is_trained = True
        print(f"📂 Model încărcat din: {filepath}")


if __name__ == '__main__':
    # Antrenare model
    predictor = GradePredictor()
    predictor.train()
    predictor.save()
    
    print("\n🎉 Model ML gata de folosit!")
    print("   Acum poate prezice note BAC bazat pe performanța elevilor!")