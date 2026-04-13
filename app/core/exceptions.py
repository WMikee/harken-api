from fastapi import HTTPException, status


class InvalidURLException(HTTPException):
    def __init__(self, detail: str = "Invalid or disallowed URL."):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )


class MediaUnavailableException(HTTPException):
    def __init__(self, detail: str = "Could not retrieve media information."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ExtractionException(HTTPException):
    def __init__(self, detail: str = "Failed to extract media information."):
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)


class SearchException(HTTPException):
    def __init__(self, detail: str = "Failed to retrieve search results."):
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)