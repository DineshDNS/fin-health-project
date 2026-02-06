from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UISeverity(BaseModel):
    severity: str


class DocumentPeriod(BaseModel):
    year: int
    month: Optional[int] = None
    quarter: Optional[str] = None


class FileMetaDTO(BaseModel):
    file_name: str
    file_size_kb: int
    mime_type: str


class UploadDocumentRequestDTO(BaseModel):
    document_type: str
    period: DocumentPeriod
    source: str
    file_meta: FileMetaDTO


class ReplaceDocumentRequestDTO(BaseModel):
    replace_document_id: str
    document_type: str
    period: DocumentPeriod
    file_meta: FileMetaDTO


class DeleteDocumentRequestDTO(BaseModel):
    document_id: str
    reason: str
