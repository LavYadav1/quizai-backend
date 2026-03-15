from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
import logging

from db.database import engine, Base
from routers import auth, quiz, scores, daily
from services.scheduler_service import start_scheduler, stop_scheduler

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting QuizAI Backend...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Database tables created")
    start_scheduler()
    yield
    # Shutdown
    stop_scheduler()
    logger.info("👋 Shutting down")


app = FastAPI(
    title="QuizAI Backend",
    description="AI-powered quiz platform for Indian students",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(quiz.router)
app.include_router(scores.router)
app.include_router(daily.router)


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "QuizAI API chal raha hai! 🚀"}

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}
