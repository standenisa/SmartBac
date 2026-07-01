"""
Photo Math Scanner — pipeline două modele pe Kaggle:
  1. OCR: Qwen2.5-VL (Kaggle via ngrok) — extrage textul din imagine
  2. Solve: DeepSeek-R1 (Kaggle via ngrok) — rezolvă exercițiul extras

Fără fallback — dacă ngrok e offline, returnează eroare clară.
"""

import re
import os
import base64
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/scanner", tags=["scanner"])

AI_NGROK_URL = os.getenv("AI_NGROK_URL", "")
VLM_NGROK_URL = os.getenv("VLM_NGROK_URL", "")

OFFLINE_MSG = "Modelul AI nu este online momentan. Pornește serverul pe Kaggle și încearcă din nou."


# ─── Qwen VL pe Kaggle (OCR din imagine) ───

def _ocr_qwen_vl(image_bytes: bytes) -> dict | None:
    """Trimite imaginea la Qwen2.5-VL pe Kaggle — endpoint /transcrie."""
    if not VLM_NGROK_URL:
        return None
    try:
        import httpx
        base = VLM_NGROK_URL.rstrip("/")
        url = base if base.endswith("/transcrie") else base + "/transcrie"
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        resp = httpx.post(url, json={"image_base64": b64}, timeout=60.0)
        if resp.status_code != 200:
            print(f"[scanner] Qwen VL HTTP {resp.status_code}")
            return None
        data = resp.json()
        if not data.get("success"):
            print(f"[scanner] Qwen VL error: {data.get('error', 'unknown')}")
            return None
        text = data.get("transcriere", "").strip()
        if not text:
            return None
        return {
            "extracted_text": text,
            "confidence": 0.9,  # valoare fixă — endpointul Kaggle nu returnează un scor real
            "model_used": "qwen_vl_kaggle",
        }
    except Exception as e:
        print(f"[scanner] Qwen VL error: {e}")
        return None


# ─── DeepSeek R1 pe Kaggle (rezolvare) ───

def _solve_with_deepseek(question: str) -> dict | None:
    if not AI_NGROK_URL:
        return None
    try:
        import httpx
        base = AI_NGROK_URL.rstrip("/")
        url = base if base.endswith("/ask") else base + "/ask"

        from routers.chat import _normalize_math_input
        normalized = _normalize_math_input(question)

        resp = httpx.post(url, json={"intrebare": normalized}, timeout=30.0)
        if resp.status_code != 200:
            return None

        data = resp.json()
        raspuns = data.get("raspuns", "").strip()
        if not raspuns:
            return None

        steps = []
        answer = ""
        step_re = re.compile(r"^(Pasul|Pas|Step|Etapa)\s*\d*\s*:?\s*", re.IGNORECASE)
        answer_re = re.compile(r"^(Răspuns|Raspuns|Rezultat|Answer)\s*:?\s*", re.IGNORECASE)

        for line in raspuns.split("\n"):
            stripped = line.strip()
            if not stripped or "Rezolvare pas cu pas" in stripped:
                continue
            if answer_re.match(stripped):
                answer = answer_re.sub("", stripped).strip()
                continue
            clean = step_re.sub("", stripped).strip()
            if clean and len(clean) >= 3:
                if any(c in clean for c in "😊😂🤔😎"):
                    continue
                parts = clean.split("=")
                if len(parts) == 2 and parts[0].strip() == parts[1].strip():
                    continue
                steps.append(clean)

        if not answer and steps:
            answer = steps[-1]
        if not steps:
            return None

        return {
            "answer": answer,
            "steps": steps[:6],
            "model_used": "deepseek_r1_kaggle",
            "structured": {
                "tip": "Exercițiu",
                "ce_avem": question,
                "ce_aplicam": "Rezolvare cu DeepSeek-R1 (model antrenat)",
                "pasi": [
                    {"pas": i + 1, "actiune": s,
                     "rezultat": s if any(c in s for c in "=<>≤≥±√∫²³") else ""}
                    for i, s in enumerate(steps[:6])
                ],
                "raspuns": answer,
                "verificare": "",
                "greseli_frecvente": [],
            },
        }
    except Exception as e:
        print(f"[scanner] DeepSeek error: {e}")
        return None


# ─── Endpoints ───

@router.post("/ocr")
async def ocr_image(file: UploadFile = File(...)):
    """Extrage text din imagine cu Qwen VL pe Kaggle."""
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Fișierul trebuie să fie o imagine.")

    if not VLM_NGROK_URL:
        return {"success": False, "extracted_text": "", "confidence": 0.0, "message": OFFLINE_MSG}

    image_bytes = await file.read()
    vlm = _ocr_qwen_vl(image_bytes)

    if vlm:
        return {
            "success": True,
            "extracted_text": vlm["extracted_text"],
            "raw_text": vlm["extracted_text"],
            "confidence": vlm["confidence"],
            "model_used": vlm["model_used"],
        }

    return {"success": False, "extracted_text": "", "confidence": 0.0, "message": OFFLINE_MSG}


class SolveTextRequest(BaseModel):
    question: str
    user_id: Optional[int] = 1


@router.post("/solve-text")
async def solve_text(req: SolveTextRequest):
    """Trimite textul extras la DeepSeek R1 pe Kaggle."""
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Textul nu poate fi gol.")

    if not AI_NGROK_URL:
        raise HTTPException(status_code=503, detail=OFFLINE_MSG)

    result = _solve_with_deepseek(req.question.strip())
    if result:
        return {"success": True, **result}

    raise HTTPException(status_code=503, detail=OFFLINE_MSG)
