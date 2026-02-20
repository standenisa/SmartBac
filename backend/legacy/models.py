"""
Database Models pentru BAC Prep AI
SQLAlchemy models pentru Users, Exercises, Attempts, Achievements
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    """Model pentru utilizatori"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    profile = db.Column(db.String(10), default='M1')  # M1 (mate-info) sau M2 (tehnologic)

    # Gamification
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    current_streak = db.Column(db.Integer, default=0)
    best_streak = db.Column(db.Integer, default=0)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    attempts = db.relationship('Attempt', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    achievements = db.relationship('UserAchievement', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash și salvează parola"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifică parola"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convertește la dicționar pentru JSON"""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'profile': self.profile,
            'xp': self.xp,
            'level': self.level,
            'current_streak': self.current_streak,
            'best_streak': self.best_streak,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None
        }

    def __repr__(self):
        return f'<User {self.username}>'


class Exercise(db.Model):
    """Model pentru exerciții BAC"""
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.Integer, default=1)  # 1-5
    topic = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.Integer, nullable=False)  # 1, 2, 3 (Subiectul I, II, III)
    points = db.Column(db.Integer, default=5)
    profile = db.Column(db.String(10), default='BOTH')  # M1, M2, BOTH

    # Metadata
    year = db.Column(db.Integer)  # Anul BAC (2020-2025)
    session = db.Column(db.String(50))  # Iulie, August, Model, etc.

    # Solution details
    solution_steps = db.Column(db.Text)  # JSON string cu pașii rezolvării
    hints = db.Column(db.Text)  # JSON string cu hints
    explanation = db.Column(db.Text)
    formula = db.Column(db.String(255))

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    attempts = db.relationship('Attempt', backref='exercise', lazy='dynamic')

    def to_dict(self, include_solution=False):
        """Convertește la dicționar pentru JSON"""
        data = {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'difficulty': self.difficulty,
            'topic': self.topic,
            'subject': self.subject,
            'points': self.points,
            'profile': self.profile,
            'year': self.year,
            'session': self.session
        }
        if include_solution:
            import json
            data['solution_steps'] = json.loads(self.solution_steps) if self.solution_steps else []
            data['hints'] = json.loads(self.hints) if self.hints else []
            data['explanation'] = self.explanation
            data['formula'] = self.formula
        return data

    def __repr__(self):
        return f'<Exercise {self.id}: {self.topic}>'


class Attempt(db.Model):
    """Model pentru încercările utilizatorilor"""
    __tablename__ = 'attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False, index=True)

    user_answer = db.Column(db.String(255))
    is_correct = db.Column(db.Boolean, default=False)
    time_spent = db.Column(db.Integer, default=0)  # Secunde

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        """Convertește la dicționar pentru JSON"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'exercise_id': self.exercise_id,
            'user_answer': self.user_answer,
            'is_correct': self.is_correct,
            'time_spent': self.time_spent,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Attempt {self.id}: User {self.user_id} -> Ex {self.exercise_id}>'


class Achievement(db.Model):
    """Model pentru definițiile achievement-urilor"""
    __tablename__ = 'achievements'

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(10), default='🏆')
    xp = db.Column(db.Integer, default=10)
    category = db.Column(db.String(50), default='general')  # streak, exercises, accuracy, etc.

    # Relationships
    user_achievements = db.relationship('UserAchievement', backref='achievement', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'xp': self.xp,
            'category': self.category
        }

    def __repr__(self):
        return f'<Achievement {self.id}: {self.name}>'


class UserAchievement(db.Model):
    """Model pentru achievements deblocate de utilizatori"""
    __tablename__ = 'user_achievements'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    achievement_id = db.Column(db.String(50), db.ForeignKey('achievements.id'), nullable=False)

    # Timestamp
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Unique constraint - un user poate avea un achievement o singură dată
    __table_args__ = (db.UniqueConstraint('user_id', 'achievement_id', name='unique_user_achievement'),)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'achievement_id': self.achievement_id,
            'unlocked_at': self.unlocked_at.isoformat() if self.unlocked_at else None,
            'achievement': self.achievement.to_dict() if self.achievement else None
        }

    def __repr__(self):
        return f'<UserAchievement User {self.user_id} -> {self.achievement_id}>'


class ExamSimulation(db.Model):
    """Model pentru simulări de examen BAC"""
    __tablename__ = 'exam_simulations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Scoruri pe subiecte
    score_subject1 = db.Column(db.Float, default=0)
    score_subject2 = db.Column(db.Float, default=0)
    score_subject3 = db.Column(db.Float, default=0)
    total_score = db.Column(db.Float, default=0)

    # Timp
    time_spent = db.Column(db.Integer, default=0)  # Secunde
    completed = db.Column(db.Boolean, default=False)

    # Timestamps
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    # Relationship
    user = db.relationship('User', backref=db.backref('simulations', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'score_subject1': self.score_subject1,
            'score_subject2': self.score_subject2,
            'score_subject3': self.score_subject3,
            'total_score': self.total_score,
            'time_spent': self.time_spent,
            'completed': self.completed,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

    def __repr__(self):
        return f'<ExamSimulation {self.id}: User {self.user_id} - Score {self.total_score}>'
