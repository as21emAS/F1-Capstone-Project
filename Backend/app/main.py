from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings

from app.api.v1.endpoints.races import router as races_router
from routes.health import router as health_router
from app.api.v1.endpoints.predictions import router as predictions_router
from app.api.v1.endpoints.standings import router as standings_router



# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="F1 Predictor API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(races_router, prefix="/api/races", tags=["races"])
app.include_router(health_router)  # add this after the other include_router
app.include_router(predictions_router, prefix="/api/predictions", tags=["predictions"])
app.include_router(standings_router,   prefix="/api/standings",   tags=["standings"])

@app.get("/health")
def health_check():
    return {"status": "ok", "version": settings.VERSION}

@app.get("/")
def root():
    return {"message": "F1 Predictor API", "docs": "/docs"}