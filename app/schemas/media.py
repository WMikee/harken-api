from pydantic import BaseModel


class AudioStream(BaseModel):
    url: str
    expires_at: int | None = None


class ArtistInfo(BaseModel):
    name: str
    id: str | None = None
    url: str | None = None
    verified: bool = False
    followers: int | None = None


class TrackMeta(BaseModel):
    id: str
    source_url: str
    title: str
    artist: ArtistInfo
    thumbnail_url: str | None = None
    duration_seconds: int | None = None
    upload_date: str | None = None
    view_count: int | None = None
    like_count: int | None = None
    tags: list[str] = []
    categories: list[str] = []


class TrackResponse(BaseModel):
    meta: TrackMeta
    stream: AudioStream | None = None


class TrackListResponse(BaseModel):
    results: list[TrackResponse]
    continuation_token: str | None = None
    has_more: bool = False