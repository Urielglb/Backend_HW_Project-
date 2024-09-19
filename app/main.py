from typing import Any
from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from app.core.db import init_db

from app.core.config import settings

from app.api.routes.main import api_router

app = FastAPI()

app.title = "ATM Simple API"

app.version = "0.1"

app.on_event("startup")(init_db)


@app.get("/")
def read_root():
    return "Backend is running"


if settings.BACKEND_CORS_ORIGIN:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGIN
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_STR)
