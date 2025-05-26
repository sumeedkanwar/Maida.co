from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os
from .routers import auth, moderation


app = FastAPI(title="Image Moderation API", trailing_slash=False)


@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "Image Moderation API is running",
        "version": "1.0"
    }

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost",
        "http://localhost:80",
        "http://0.0.0.0:80"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_database():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
    client = MongoClient(
        mongo_uri,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000
    )
    try:
        client.admin.command('ping')
        return client["moderation_db"]
    except Exception as e:
        print(f"Could not connect to MongoDB: {e}")
        return None


# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(moderation.router, prefix="/moderate", tags=["moderation"])


@app.on_event("startup")
async def startup_event():
    db = get_database()
    if db:
        db.tokens.create_index("token", unique=True)
        db.usages.create_index(["token", "timestamp"])


@app.on_event("shutdown")
async def shutdown_event():
    pass
