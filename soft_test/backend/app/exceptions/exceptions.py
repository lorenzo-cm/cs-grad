from fastapi import HTTPException

class BaseWordleException(HTTPException):
    def __init__(self, detail, status_code):
        super().__init__(
            status_code=status_code,
            detail=f"Item with ID {detail} not found"
        )