from utils.normalization import normalize_column


# Confidence thresholds (type-specific)
MIN_CONFIDENCE_BY_TYPE = {
    "BANK": 3,
    "GST": 2,
    "FIN": 2,
}


# Bank semantic scorer
def _bank_score(columns):
    score = 0

    for col in columns:
        if "date" in col:
            score += 1
        elif "credit" in col or "credited" in col:
            score += 1
        elif "debit" in col or "debited" in col:
            score += 1
        elif "balance" in col:
            score += 1
        elif any(k in col for k in ["description", "narration", "transaction", "remarks"]):
            score += 1

    return score


# GST semantic scorer
def _gst_score(columns):
    score = 0

    for col in columns:
        if col == "period" or "month" in col or "return" in col:
            score += 1
        elif "taxable" in col and "value" in col:
            score += 1
        elif "gst" in col and "paid" in col:
            score += 1
        elif "gst" in col and any(k in col for k in ["expected", "payable", "due"]):
            score += 1
        elif "payment" in col and "ratio" in col:
            score += 1
        elif col in {"cgst", "sgst", "igst"}:
            score += 1

    return score


# Financial semantic scorer
def _financial_score(columns):
    score = 0

    for col in columns:
        if col in {"account", "accounts", "particulars", "description"}:
            score += 1
        elif "amount" in col or "total" in col or "value" in col:
            score += 1
        elif any(
            k in col
            for k in ["revenue", "income", "expense", "expenses", "profit", "loss"]
        ):
            score += 1

    return score


# Financial row-based fallback keywords
FIN_ROW_KEYWORDS = {
    "revenue",
    "sales",
    "income",
    "expense",
    "expenses",
    "profit",
    "loss",
    "ebitda",
    "total",
}


def _fin_row_signal(sample_values):
    if not sample_values:
        return False

    for val in sample_values:
        val = str(val).lower()
        if any(keyword in val for keyword in FIN_ROW_KEYWORDS):
            return True

    return False


# Main detection function
def detect_document_type(raw_columns, sample_values=None):
    normalized_columns = {
        normalize_column(col) for col in raw_columns if col
    }

    scores = {
        "BANK": _bank_score(normalized_columns),
        "GST": _gst_score(normalized_columns),
        "FIN": _financial_score(normalized_columns),
    }

    best_type = max(scores, key=scores.get)
    best_score = scores[best_type]
    required_score = MIN_CONFIDENCE_BY_TYPE[best_type]

    if best_score >= required_score:
        return best_type, scores

    if _fin_row_signal(sample_values):
        return "FIN", scores

    raise ValueError(
        "Unable to confidently identify the document type. "
        "Please upload a valid Bank, GST, or Financial document."
    )
