from PyPDF2 import PdfReader


def extract_pdf_text(path: str, max_chars: int = 5000) -> str:
    try:
        reader = PdfReader(path)
    except Exception:
        return ""

    text = ""

    for page in reader.pages:
        try:
            page_text = page.extract_text()
        except Exception:
            page_text = None

        if page_text:
            text += page_text + "\n"

        if len(text) >= max_chars:
            break

    return text.strip()
