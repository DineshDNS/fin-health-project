from datetime import datetime

ALLOWED_TYPES = {
        "BANK_STATEMENT",
        "GST_RETURN",
        "BALANCE_SHEET",
        "PROFIT_AND_LOSS",
    }

ALLOWED_EXTENSIONS = {".pdf", ".xlsx", ".csv"}


class DocumentValidator:

    @staticmethod
    def validate(dto, file):

        doc_type = dto.get("type")

        if doc_type not in ALLOWED_TYPES:
            raise ValueError("Invalid document type")

        filename = file.name.lower()
        ext = "." + filename.split(".")[-1]

        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError("Invalid file format")

        year = int(dto.get("year"))
        now = datetime.now()

        if year > now.year:
            raise ValueError("Future year not allowed")

        if doc_type == "BANK_STATEMENT" and not dto.get("month"):
            raise ValueError("Bank statement requires month")

        if doc_type == "GST_RETURN" and not dto.get("quarter"):
            raise ValueError("GST return requires quarter")
