import re

def normalize_column(col: str) -> str:
    """
    Robust normalization for semantic column matching.
    Handles BOM, spaces, symbols, case, and variants.
    """
    if not col:
        return ""

    # Remove BOM if present
    col = col.replace("\ufeff", "")

    # Lowercase
    col = col.lower()

    # Strip whitespace
    col = col.strip()

    # Replace common separators with space
    col = re.sub(r"[-/]", " ", col)

    # Remove non-alphanumeric characters
    col = re.sub(r"[^a-z0-9\s]", "", col)

    # Collapse whitespace to underscore
    col = re.sub(r"\s+", "_", col)

    return col
