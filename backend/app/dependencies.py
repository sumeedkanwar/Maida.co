from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pymongo import MongoClient
import os
from datetime import datetime

security = HTTPBearer()


def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    return client["moderation_db"]


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    db = get_db()
    token = credentials.credentials
    token_doc = db.tokens.find_one({"token": token})
    if not token_doc:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    # Log usage
    db.usages.insert_one({
        "token": token,
        "endpoint": "any",
        "timestamp": datetime.utcnow()
    })
    return token_doc


async def verify_admin(token_doc: dict = Depends(verify_token)):
    if not token_doc.get("isAdmin"):
        raise HTTPException(status_code=403, detail="Admin access required")
    return token_doc