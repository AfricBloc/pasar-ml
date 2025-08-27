from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from shared.config.settings import settings
from shared.logging.logger import logger
from resolute.api.routes import router as resolute_router
from contextlib import asynccontextmanager

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Resolute Engine started", extra={"env": settings.ENVIRONMENT})
    yield

app = FastAPI(
    title="Resolute Engine",
    description="Dispute resolution agent for Pasar",
    version="0.1",
    lifespan=lifespan
)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Resolute", "env": settings.ENVIRONMENT}

@app.middleware("http")
async def add_request_context(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.exception("Unhandled exception", extra={"path": request.url.path})
        return JSONResponse({"detail": "Internal Server Error"}, status_code=500)

# All API endpoints live in routes.py
app.include_router(resolute_router, prefix="/resolute", tags=["resolute"])