"""
Tokenizer Router — encode/decode text via the BPE tokenizer.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.tokenizer import encode, decode, get_vocab_info

router = APIRouter(prefix="/api/tokenizer", tags=["tokenizer"])


class EncodeRequest(BaseModel):
    text: str


class EncodeResponse(BaseModel):
    success: bool = True
    tokens: list[int] = []
    num_tokens: int = 0


class DecodeRequest(BaseModel):
    ids: list[int]


class DecodeResponse(BaseModel):
    success: bool = True
    text: str = ""


@router.post("/encode", response_model=EncodeResponse)
def encode_text(req: EncodeRequest):
    try:
        ids = encode(req.text)
        return EncodeResponse(tokens=ids, num_tokens=len(ids))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.post("/decode", response_model=DecodeResponse)
def decode_ids(req: DecodeRequest):
    try:
        text = decode(req.ids)
        return DecodeResponse(text=text)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/info")
def tokenizer_info():
    return get_vocab_info()
