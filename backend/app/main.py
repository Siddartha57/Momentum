import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.core.config import settings
from app.core.database import Base, engine
from app.models import entities  # noqa: F401
from app.services.scheduler import start_scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    docs_url="/docs" if settings.environment == "development" else None,
    redoc_url="/redoc" if settings.environment == "development" else None,
)

# CORS — allow frontend origin (production + dev)
origins = [
    settings.frontend_url,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
# Also allow any Vercel preview URLs
if settings.environment == "production":
    origins.append("https://*.vercel.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
scheduler = start_scheduler()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "app": settings.app_name, "environment": settings.environment}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
