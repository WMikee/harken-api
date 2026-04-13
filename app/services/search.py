from typing import Optional

import httpx

from app.schemas.media import TrackListResponse, TrackResponse
from app.core.exceptions import SearchException
from app.services.youtube.client import innertube_post
from app.services.youtube.parsers import (
    extract_continuation_token,
    parse_video_renderer,
)


async def search_youtube(
    query: str,
    client: httpx.AsyncClient,
    continuation_token: Optional[str] = None,
) -> TrackListResponse:
    payload = {"continuation": continuation_token} if continuation_token else {"query": query}

    data = await innertube_post("search", payload, client=client)

    videos, next_token = _parse_search_results(data)
    return TrackListResponse(
        results=videos,
        continuation_token=next_token,
        has_more=next_token is not None,
    )


def _parse_search_results(data: dict) -> tuple[list[TrackResponse], Optional[str]]:
    contents = _get_contents(data)
    videos: list[TrackResponse] = []
    continuation_token: Optional[str] = None

    for section in contents:
        item_section = section.get("itemSectionRenderer", {})
        items = item_section.get("contents", [])

        for item in items:
            renderer = item.get("videoRenderer")
            if renderer:
                video = parse_video_renderer(renderer)
                if video:
                    videos.append(video)

        token = extract_continuation_token(section)
        if token:
            continuation_token = token
            
    return videos, continuation_token


def _get_contents(data: dict) -> list:
    contents = (
        data.get("contents", {})
        .get("twoColumnSearchResultsRenderer", {})
        .get("primaryContents", {})
        .get("sectionListRenderer", {})
        .get("contents", [])
    )
    if contents:
        return contents

    for cmd in data.get("onResponseReceivedCommands", []):
        items = cmd.get("appendContinuationItemsAction", {}).get("continuationItems", [])
        if items:
            return items

    return []