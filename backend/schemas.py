"""
Pydantic Schemas for request/response validation
BAC Prep AI - FastAPI
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ── Auth ──

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=6, max_length=128)
    profile: str = Field(default="M1", pattern="^(M1|M2)$")


class LoginRequest(BaseModel):
    email: str  # can be email or username
    password: str


class TokenResponse(BaseModel):
    success: bool = True
    token: str
    user: dict
    message: str = ""


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=80)
    profile: Optional[str] = Field(None, pattern="^(M1|M2)$")
    password: Optional[str] = Field(None, min_length=6)
    current_password: Optional[str] = None


# ── Exercises ──

class ExerciseFilter(BaseModel):
    difficulty: Optional[int] = Field(None, ge=1, le=5)
    subject: Optional[int] = Field(None, ge=1, le=3)
    profile: Optional[str] = Field(None, pattern="^(M1|M2|BOTH)$")
    exercise_type: Optional[str] = None
    topic: Optional[str] = None


class SubmitAnswerRequest(BaseModel):
    exercise_id: int
    answer: str
    user_id: int = 1
    time_spent: int = 0


class SubmitAnswerResponse(BaseModel):
    correct: bool
    correct_answer: Optional[str] = None
    message: str
    new_achievements: list = []


# ── Stats ──

class SubjectStats(BaseModel):
    attempts: int = 0
    correct: int = 0
    accuracy: float = 0


class DetailedStats(BaseModel):
    total: SubjectStats
    subject_1: SubjectStats
    subject_2: SubjectStats
    subject_3: SubjectStats


# ── ML ──

class PredictionResponse(BaseModel):
    success: bool = True
    prediction: dict
    message: str = ""


# ── Solver ──

class SolveRequest(BaseModel):
    question: str
    model: str = Field(default="transformer", pattern="^(transformer|qwen)$")


class SolveResponse(BaseModel):
    success: bool = True
    answer: str = ""
    steps: List[str] = []
    latex: Optional[str] = None
    model_used: str = ""
    confidence: Optional[float] = None


# ── Gamification ──

class GamificationStats(BaseModel):
    success: bool = True
    xp: int = 0
    level: int = 1
    level_name: str = "Incepator"
    current_streak: int = 0
    best_streak: int = 0
    achievements_count: int = 0
    total_achievements: int = 0


# ── Profile ──

class SetProfileRequest(BaseModel):
    user_id: int = 1
    profile: str = Field(pattern="^(M1|M2)$")


# ── Chat ──

class ChatRequest(BaseModel):
    message: str
    user_id: int = 1
    model: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    latex: Optional[str] = None
    model_used: str = "rule_based"


# ── Recommender ──

class RecommendationResponse(BaseModel):
    success: bool = True
    exercises: list = []
    reason: str = ""
