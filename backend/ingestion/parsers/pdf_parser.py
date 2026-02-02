from PyPDF2 import PdfReader


def extract_pdf_text(path: str, max_chars: int = 5000) -> str:
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

        if len(text) >= max_chars:
            break

    return text.strip()
