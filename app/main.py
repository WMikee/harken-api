from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import resolve, search, recommendations

app = FastAPI()

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
