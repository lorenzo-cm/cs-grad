from functools import lru_cache

from app.core.config import get_settings
from app.services.document_processor import (
    BaseDocumentProcessor,
    DoclingDocumentProcessor,
)


@lru_cache(maxsize=1)
def get_document_processor() -> BaseDocumentProcessor | None:
    settings = get_settings()
    if settings.DOCUMENT_PROCESSOR_TYPE in (None, "disabled"):
        return None
    return DoclingDocumentProcessor()
