from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import httpx

from app.core.config import settings
from app.routers import resolve, search, recommendations

from app.services.youtube import client as youtube_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(
        headers=youtube_client.HEADERS,
        params=youtube_client.PARAMS,
        timeout=15.0,
    )
    yield
    await app.state.http_client.aclose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=["GET"]
)

app.include_router(resolve.router)
app.include_router(search.router)
app.include_router(recommendations.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
