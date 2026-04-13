import httpx

from app.core.exceptions import SearchException

INNERTUBE_CONTEXT = {
    "client": {
        "clientName": "WEB",
        "clientVersion": "2.20240101.00.00",
        "hl": "es",
        "gl": "CO",
    }
}

HEADERS = { 
    "Content-Type": "application/json",
    "X-YouTube-Client-Name": "1",
    "X-YouTube-Client-Version": "2.20240101.00.00",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
} 

PARAMS = {"prettyPrint": "false"}

async def innertube_post(endpoint: str, payload: dict, client: httpx.AsyncClient) -> dict:
    url = f"https://www.youtube.com/youtubei/v1/{endpoint}"
    body = {"context": INNERTUBE_CONTEXT, **payload}

    try:
        response = await client.post(url, json=body)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise SearchException(detail=f"YouTube returned {e.response.status_code}.")
    except httpx.RequestError as e:
        raise SearchException(detail=f"Request to YouTube failed: {e}")