from typing import Optional
from fastapi import APIRouter, Query

from app.dependencies import HttpClient
from app.schemas.media import TrackListResponse
from app.services.search import search_youtube

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=TrackListResponse)
async def search(
    client: HttpClient,
    q: str = Query(..., min_length=1, description="Search query"),
    continuation: Optional[str] = Query(
        default=None,
        description=(
            "Continuation token for paginating results. "
            "Obtained from the `continuation_token` field of the previous response."
        ),
    ),
) -> TrackListResponse:
    return await search_youtube(query=q, client=client, continuation_token=continuation)