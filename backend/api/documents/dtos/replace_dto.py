from dataclasses import dataclass

@dataclass
class DocumentReplaceDTO:
    old_document_id: str
    new_filename: str
