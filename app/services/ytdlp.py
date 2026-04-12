import asyncio
from typing import Any, cast

import yt_dlp
import yt_dlp.utils

from app.core.config import settings
from app.core.exceptions import ExtractionException, MediaUnavailableException
from app.schemas.media import TrackResponse, TrackMeta, ArtistInfo, AudioStream


def _build_ydl_opts() -> dict:
    return {
        "format": settings.YDL_FORMAT,
        "quiet": settings.YDL_QUIET,
        "no_warnings": True,
        "extract_flat": False,
    }


def _extract_info_sync(url: str) -> dict[str, Any]:
    with yt_dlp.YoutubeDL(_build_ydl_opts()) as ydl: # type: ignore
        try:
            info = ydl.extract_info(url, download=False)
        except yt_dlp.utils.DownloadError as e:
            raise ExtractionException(detail=str(e))

    if info is None:
        raise MediaUnavailableException()

    return cast(dict[str, Any], info)


async def extract_media(url: str) -> TrackResponse:
    loop = asyncio.get_running_loop()
    try:
        info = await loop.run_in_executor(None, _extract_info_sync, url)
    except (ExtractionException, MediaUnavailableException):
        raise
    except Exception as e:
        raise ExtractionException(detail=f"Unexpected error: {e}")

    meta = TrackMeta(
        id=info.get("id", info.get("display_id", "")),
        source_url=info.get("webpage_url") or info.get("original_url") or url,
        title=info.get("title", "Unknown"),
        artist=ArtistInfo(
            name=info.get("uploader", "Unknown"),
            id=info.get("channel_id"),
            url=info.get("channel_url"),
            followers=info.get("channel_follower_count"),
        ),
        thumbnail_url=info.get("thumbnail"),
        duration_seconds=info.get("duration"),
        upload_date=info.get("upload_date"),
        view_count=info.get("view_count"),
        like_count=info.get("like_count"),
        tags=info.get("tags", []),
        categories=info.get("categories", []),
    )

    stream_url = info.get("url")
    stream = AudioStream(url=stream_url) if stream_url else None

    return TrackResponse(meta=meta, stream=stream)