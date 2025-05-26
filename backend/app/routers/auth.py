from fastapi import APIRouter, Depends, HTTPException
from ..models import Token
from ..dependencies import verify_admin, get_db
from datetime import datetime
import secrets

router = APIRouter()

@router.post("/token")
async def create_token(request: TokenRequest):
    db = get_db()
    if request.apiKey != "test-key":  # Replace with real API key validation
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    token = {"token": "test-token", "isAdmin": True}  # Generate real token
    db.tokens.insert_one(token)
    return token


@router.get("/verify")
async def verify_token(token: str):
    db = get_db()
    token_doc = db.tokens.find_one({"token": token})
    if not token_doc:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"valid": True}

@router.get("/tokens")
async def list_tokens(_=Depends(verify_admin)):
    db = get_db()
    tokens = list(db.tokens.find({}, {"_id": 0}))
    return tokens

@router.delete("/tokens/{token}")
async def delete_token(token: str, _=Depends(verify_admin)):
    db = get_db()
    result = db.tokens.delete_one({"token": token})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Token not found")
    return {"detail": "Token deleted"}