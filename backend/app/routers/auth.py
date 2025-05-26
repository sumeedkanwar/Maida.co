from fastapi import APIRouter, Depends, HTTPException
from ..models import Token
from ..dependencies import verify_admin, get_db
from datetime import datetime
import secrets

router = APIRouter()

@router.post("/tokens")
async def create_token(isAdmin: bool = False, _=Depends(verify_admin)):
    token = secrets.token_urlsafe(32)
    db = get_db()
    db.tokens.insert_one({
        "token": token,
        "isAdmin": isAdmin,
        "createdAt": datetime.utcnow()
    })
    return {"token": token}

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