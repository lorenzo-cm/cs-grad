import asyncio
from io import BytesIO
from typing import cast

from docling.datamodel.base_models import DocumentStream
from docling.document_converter import DocumentConverter

from app.services.document_processor.base import (
    BaseDocumentProcessor,
)

converter = DocumentConverter()


def docling_process_local(file_bytes: bytes) -> str:
    stream = DocumentStream(name="document.pdf", stream=BytesIO(file_bytes))
    result = converter.convert(stream)
    return cast(str, result.document.export_to_markdown())


class DoclingDocumentProcessor(BaseDocumentProcessor):
    """Runs Docling `DocumentConverter` in a worker thread (sync docling API)."""

    async def _do_process(
        self,
        file_bytes: bytes,
    ) -> str:
        return await asyncio.to_thread(docling_process_local, file_bytes)
