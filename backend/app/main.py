from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os
from .dependencies import verify_token, verify_admin
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

# MongoDB connection with retry logic
def get_database():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
    client = MongoClient(mongo_uri, 
                        serverSelectionTimeoutMS=5000,
                        connectTimeoutMS=5000)
    try:
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        return client["moderation_db"]
    except Exception as e:
        print(f"Could not connect to MongoDB: {e}")
        return None

db = get_database()

# MongoDB connection
client = MongoClient("mongodb://mongodb:27017/")
db = client["moderation_db"]

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(moderation.router, prefix="/moderate", tags=["moderation"])

@app.on_event("startup")
async def startup_event():
    # Create indexes for tokens and usages collections
    db.tokens.create_index("token", unique=True)
    db.usages.create_index(["token", "timestamp"])

@app.on_event("shutdown")
async def shutdown_event():
    client.close()