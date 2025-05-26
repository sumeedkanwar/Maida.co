import httpx
from fastapi import HTTPException
import os
from typing import Dict


async def check_image_safety(image_url: str) -> Dict[str, float]:
    api_key = os.getenv("SIGHTENGINE_API_KEY")
    api_secret = os.getenv("SIGHTENGINE_API_SECRET")

    if not api_key or not api_secret:
        raise HTTPException(
            status_code=500,
            detail="Moderation service credentials not configured"
        )

    params = {
        "api_key": api_key,
        "api_secret": api_secret,
        "url": image_url,
        "models": "nudity-2.0"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.sightengine.com/1.0/check.json", params=params)
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking image: {str(e)}")
