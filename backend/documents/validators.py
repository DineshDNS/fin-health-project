import os

ALLOWED_EXTENSIONS = {
    ".csv": "CSV",
    ".xlsx": "XLSX",
    ".pdf": "PDF",
}


class FileValidationError(Exception):
    pass


def validate_file_format(uploaded_file):
    """
    Validates file extension and returns file format.
    Raises FileValidationError if invalid.
    """
    _, ext = os.path.splitext(uploaded_file.name.lower())

    if ext not in ALLOWED_EXTENSIONS:
        raise FileValidationError(
            "Invalid file format. Only CSV, XLSX, and PDF files are supported."
        )

    return ALLOWED_EXTENSIONS[ext]
