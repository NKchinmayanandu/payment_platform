from fastapi import FastAPI
from app.core.config import settings
from contextlib import asynccontextmanager
from app.utils.logging import setup_logging
from app.api.auth import router as auth_router 
from app.api.wallet import router as wallet_router
from app.api.transaction import router as transact_router
from app.api.analytics import router as analytics_router
@asynccontextmanager
async def lifespan(app:FastAPI):
    setup_logging()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.include_router(auth_router, prefix=settings.API_PREFIX) 
app.include_router(wallet_router,prefix=settings.API_PREFIX)
app.include_router(transact_router,prefix=settings.API_PREFIX)
app.include_router(analytics_router,prefix=settings.API_PREFIX)