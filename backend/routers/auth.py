"""
Auth Router - JWT authentication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
import jwt
from datetime import datetime, timedelta
import os

from database import get_db, get_next_id
from models.user import create_user_doc, user_to_dict, check_password, set_password
from schemas import RegisterRequest, LoginRequest, TokenResponse, UserUpdate

router = APIRouter(prefix="/api/auth", tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"


def generate_token(user_id: int, expires_in: int = 24) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=expires_in),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def get_current_user(token: str, db):
    """Decode token and return user document."""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token invalid sau expirat")
    user = db.users.find_one({"_id": payload["user_id"]})
    if not user:
        raise HTTPException(status_code=401, detail="Utilizator inexistent")
    return user


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(req: RegisterRequest, db=Depends(get_db)):
    if db.users.find_one({"email": req.email.lower()}):
        raise HTTPException(status_code=409, detail="Acest email este deja inregistrat")
    if db.users.find_one({"username": req.username}):
        raise HTTPException(status_code=409, detail="Acest username este deja folosit")

    user_id = get_next_id("users")
    user_doc = create_user_doc(user_id, req.email.lower(), req.username, req.password, req.profile)
    db.users.insert_one(user_doc)

    token = generate_token(user_id)
    return TokenResponse(
        token=token,
        user=user_to_dict(user_doc),
        message="Cont creat cu succes!",
    )


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db=Depends(get_db)):
    user = db.users.find_one({
        "$or": [
            {"email": req.email.lower()},
            {"username": req.email},
        ]
    })

    if not user or not check_password(user, req.password):
        raise HTTPException(status_code=401, detail="Email/username sau parola incorecta")

    db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_activity": datetime.utcnow()}},
    )

    token = generate_token(user["_id"])
    return TokenResponse(
        token=token,
        user=user_to_dict(user),
        message="Autentificare reusita!",
    )


@router.get("/me")
def get_me(authorization: str = "", db=Depends(get_db)):
    token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
    user = get_current_user(token, db)
    return {"success": True, "user": user_to_dict(user)}


@router.put("/me")
def update_me(req: UserUpdate, authorization: str = "", db=Depends(get_db)):
    token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
    user = get_current_user(token, db)

    updates = {}

    if req.username:
        existing = db.users.find_one({"username": req.username, "_id": {"$ne": user["_id"]}})
        if existing:
            raise HTTPException(status_code=409, detail="Acest username este deja folosit")
        updates["username"] = req.username

    if req.profile:
        updates["profile"] = req.profile

    if req.password:
        if not req.current_password or not check_password(user, req.current_password):
            raise HTTPException(status_code=400, detail="Parola curenta este incorecta")
        updates["password_hash"] = set_password(req.password)

    if updates:
        updates["updated_at"] = datetime.utcnow()
        db.users.update_one({"_id": user["_id"]}, {"$set": updates})

    updated_user = db.users.find_one({"_id": user["_id"]})
    return {"success": True, "message": "Profil actualizat!", "user": user_to_dict(updated_user)}


@router.post("/refresh")
def refresh(authorization: str = "", db=Depends(get_db)):
    token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
    user = get_current_user(token, db)
    new_token = generate_token(user["_id"])
    return {"success": True, "token": new_token}


@router.post("/logout")
def logout():
    return {"success": True, "message": "Deconectat cu succes!"}
