from fastapi import APIRouter, Query
from starlette.concurrency import run_in_threadpool

from app.core.validators import validate_media_url
from app.schemas.media import TrackResponse
from app.services.ytdlp import extract_media

router = APIRouter(prefix="/resolve", tags=["resolve"])


@router.get(
    "",
    response_model=TrackResponse,
    summary="Resolve URL to audio source and metadata",
    description=(
        "Extracts the audio URL and metadata from a YouTube URL or another "
        "service supported by yt-dlp. The returned audio URL is temporary."
    ),
)
async def resolve_audio(
    url: str = Query(..., description="Public video or audio URL"),
) -> TrackResponse:
    await run_in_threadpool(validate_media_url, url)
    return await extract_media(url)