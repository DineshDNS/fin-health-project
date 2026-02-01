import os
import pandas as pd
from PyPDF2 import PdfReader


def parse_document(document):
    if document is None:
        raise ValueError("parse_document received None")

    if not document.file:
        raise ValueError("Document has no file")

    path = document.file.path

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    ext = os.path.splitext(path)[1].lower()

    if ext == ".csv":
        return parse_csv(path)

    elif ext in [".xlsx", ".xls"]:
        return parse_excel(path)

    elif ext == ".pdf":
        return parse_pdf(path)

    else:
        raise ValueError(f"Unsupported file type: {ext}")


def parse_csv(path):
    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("CSV file is empty")

    if df.columns.size == 0:
        raise ValueError("CSV has no columns")

    return {
        "rows": len(df),
        "columns": list(df.columns),
        "data": df.to_dict(orient="records")
    }


def parse_excel(path):
    df = pd.read_excel(path)

    if df.empty:
        raise ValueError("Excel file is empty")

    return {
        "rows": len(df),
        "columns": list(df.columns),
        "data": df.to_dict(orient="records")
    }


def parse_pdf(path):
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    if not text.strip():
        raise ValueError("PDF contains no readable text")

    return {
        "text": text[:5000]  # limit size
    }
