from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import get_settings
from app.core.exceptions import AppException, app_exception_handler
from app.core.logging import configure_logging
from app.db.seed import ensure_admin_user
from app.db.seed_catalog import ensure_catalog_seed
from app.db.session import SessionLocal
from app.middleware.request_id import RequestIDMiddleware

settings = get_settings()
configure_logging(settings)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    db = SessionLocal()
    try:
        ensure_admin_user(db, settings)
        ensure_catalog_seed(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(AppException, app_exception_handler)
app.include_router(api_router, prefix=settings.api_v1_prefix)
