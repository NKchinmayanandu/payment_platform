from fastapi import FastAPI
from app.core.config import settings
from contextlib import asynccontextmanager
from app.utils.logging import setup_logging


@asynccontextmanager
async def lifespan():
    setup_logging()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)
