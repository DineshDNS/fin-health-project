from dataclasses import dataclass

@dataclass
class DocumentUploadDTO:
    document_type: str
    year: int
    month: int | None
    quarter: str | None
    source: str
    filename: str
