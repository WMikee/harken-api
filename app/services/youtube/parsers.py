from typing import Optional
from app.schemas.media import ArtistInfo, TrackListResponse, TrackMeta, TrackResponse


def parse_video_renderer(renderer: dict) -> Optional[TrackResponse]:
    video_id = renderer.get("videoId")
    if not video_id:
        return None

    title = renderer.get("title", {}).get("runs", [{}])[0].get("text", "")

    thumbnails = renderer.get("thumbnail", {}).get("thumbnails", [])
    thumbnail = thumbnails[-1]["url"] if thumbnails else None

    owner_run = renderer.get("ownerText", {}).get("runs", [{}])[0]
    channel = owner_run.get("text", "")
    channel_id = (
        owner_run
        .get("navigationEndpoint", {})
        .get("browseEndpoint", {})
        .get("browseId")
    )

    duration = renderer.get("lengthText", {}).get("simpleText")
    views = renderer.get("viewCountText", {}).get("simpleText")
    published = renderer.get("publishedTimeText", {}).get("simpleText")

    return TrackResponse(
    meta=TrackMeta(
        id=video_id,
        source_url=f"https://www.youtube.com/watch?v={video_id}",
        title=title,
        artist=ArtistInfo(name=channel, id=channel_id),
        thumbnail_url=thumbnail,
        duration_seconds=_parse_duration(duration),
        upload_date=published,           
        view_count=_parse_views(views),
    ),
    stream=None,
    )


def extract_continuation_token(item: dict) -> Optional[str]:
    return (
        item.get("continuationItemRenderer", {})
        .get("continuationEndpoint", {})
        .get("continuationCommand", {})
        .get("token")
    )

def _parse_duration(text: Optional[str]) -> Optional[int]:
    if not text:
        return None
    parts = text.strip().split(":")
    try:
        parts = [int(p) for p in parts]
        if len(parts) == 2:
            return parts[0] * 60 + parts[1]
        if len(parts) == 3:
            return parts[0] * 3600 + parts[1] * 60 + parts[2]
    except ValueError:
        return None
    return None

def _parse_views(text: Optional[str]) -> Optional[int]:
    if not text:
        return None
    clean = text.lower().replace(",", "").replace(" views", "").strip()
    try:
        return int(clean)
    except ValueError:
        return None