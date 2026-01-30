import os
from PyPDF2 import PdfReader

ALLOWED_EXTENSIONS = [".csv", ".xlsx", ".pdf"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def validate_file(file):
    ext = os.path.splitext(file.name)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type")

    if file.size > MAX_FILE_SIZE:
        raise ValueError("File size exceeds 10MB")

    return ext


def validate_text_pdf(file):
    reader = PdfReader(file)
    extracted_text = ""

    for page in reader.pages:
        extracted_text += page.extract_text() or ""

    if not extracted_text.strip():
        raise ValueError("Scanned PDF detected. Upload text-based PDF only.")
