"""
BAC Prep AI - FastAPI Backend
Main application entry point (MongoDB)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
import os

from database import init_db, get_db, get_next_id, client
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    print("Starting BAC Prep AI Backend...")
    init_db()
    print("MongoDB indexes created.")
    yield
    # Shutdown
    client.close()
    print("MongoDB connection closed.")


app = FastAPI(
    title="BAC Prep AI",
    description="API pentru pregatirea examenului de Bacalaureat la matematica cu AI",
    version="3.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from routers.auth import router as auth_router
from routers.exercises import router as exercises_router
from routers.stats import router as stats_router
from routers.ml import router as ml_router
from routers.gamification import router as gamification_router
from routers.solver import router as solver_router
from routers.recommender import router as recommender_router
from routers.tokenizer import router as tokenizer_router
from routers.chat import router as chat_router

app.include_router(auth_router)
app.include_router(exercises_router)
app.include_router(stats_router)
app.include_router(ml_router)
app.include_router(gamification_router)
app.include_router(solver_router)
app.include_router(recommender_router)
app.include_router(tokenizer_router)
app.include_router(chat_router)


# ── Root endpoints ──

@app.get("/")
def root():
    return {
        "message": "BAC Prep AI - Backend Running!",
        "status": "online",
        "version": "3.0.0",
        "framework": "FastAPI",
        "database": "MongoDB",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/health")
def health_check():
    try:
        db = get_db()
        db.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


# ── User management (backward-compatible) ──

from fastapi import Depends, Query
from models.user import user_to_dict, create_user_doc


@app.post("/api/users", status_code=201)
def create_user(data: dict, db=Depends(get_db)):
    if db.users.find_one({"email": data.get("email")}):
        return {"error": "Email already exists"}
    if db.users.find_one({"username": data.get("username")}):
        return {"error": "Username already exists"}

    user_id = get_next_id("users")
    user_doc = create_user_doc(
        user_id,
        data.get("email"),
        data.get("username"),
        data.get("password", "default123"),
        data.get("profile", "M1"),
    )
    db.users.insert_one(user_doc)
    return {"success": True, "user": user_to_dict(user_doc)}


@app.get("/api/users/{user_id}")
def get_user(user_id: int, db=Depends(get_db)):
    user = db.users.find_one({"_id": user_id})
    if not user:
        return {"error": "User not found"}
    return user_to_dict(user)


@app.post("/api/set-profile")
def set_profile(data: dict, db=Depends(get_db)):
    user_id = data.get("user_id", 1)
    user = db.users.find_one({"_id": user_id})
    if not user:
        return {"error": "User not found"}
    db.users.update_one({"_id": user_id}, {"$set": {"profile": data.get("profile", "M1")}})
    return {"success": True, "profile": data.get("profile", "M1")}


@app.get("/api/get-profile")
def get_profile(user_id: int = Query(1), db=Depends(get_db)):
    user = db.users.find_one({"_id": user_id})
    return {"profile": user.get("profile") if user else None}


# ── Backward-compat alias ──
from routers.stats import get_analytics_detailed

app.get("/api/analytics/detailed", tags=["statistics"])(get_analytics_detailed)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
    )
