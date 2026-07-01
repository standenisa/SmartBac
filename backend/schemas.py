"""
Pydantic Schemas for request/response validation
BAC Prep AI - FastAPI
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


# ── Auth ──

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=6, max_length=128)
    profile: str = Field(default="M1", pattern="^(M1|M2|M3|M4)$")


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
    profile: Optional[str] = Field(None, pattern="^(M1|M2|M3|M4)$")
    password: Optional[str] = Field(None, min_length=6)
    current_password: Optional[str] = None


# ── Exercises ──

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


# ── Chat ──

class ChatRequest(BaseModel):
    message: str
    user_id: int = 1
    model: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    latex: Optional[str] = None
    model_used: str = "rule_based"
