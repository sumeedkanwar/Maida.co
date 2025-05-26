from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):
    token: str
    isAdmin: bool
    createdAt: datetime


class Usage(BaseModel):
    token: str
    endpoint: str
    timestamp: datetime


class ModerationRequest(BaseModel):
    image_url: str  # For simplicity, we'll use image URLs instead of file uploads


class ModerationResponse(BaseModel):
    is_safe: bool
    categories: dict  # e.g., {"violence": 0.1, "nudity": 0.05, ...}
