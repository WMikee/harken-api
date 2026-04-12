from fastapi import HTTPException, status


class InvalidURLException(HTTPException):
    def __init__(self, detail: str = "URL inválida o dominio no permitido."):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )


class MediaUnavailableException(HTTPException):
    def __init__(self, detail: str = "No se pudo obtener información del media."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ExtractionException(HTTPException):
    def __init__(self, detail: str = "Error al extraer información del media."):
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)

