import pandas as pd

from documents.models import Document
from documents.validators import validate_file_format
from documents.detector import detect_document_type
from documents.extractors.pdf_extractor import extract_pdf_to_dataframe

from parsers.bank_parser import parse_bank_dataframe
from parsers.gst_parser import parse_gst_dataframe
from parsers.financial_parser import parse_financial_dataframe

from aggregation.services import get_cumulative_state
from aggregation.bank_aggregator import merge_bank
from aggregation.gst_aggregator import merge_gst
from scoring.services import compute_financial_health_score


def handle_document_upload(uploaded_file):
    """
    Full upload pipeline:
    1. Validate file format
    2. Extract structured data
    3. Detect document type
    4. Save document
    5. Parse document
    6. Merge into cumulative state
    7. Recompute global score
    """

    # 1️⃣ Validate file format
    file_format = validate_file_format(uploaded_file)

    # Always reset pointer before reading
    uploaded_file.seek(0)

    df = None
    columns = []
    sample_values = []

    # 2️⃣ Extract structured data
    if file_format == "CSV":
        df = pd.read_csv(uploaded_file)
        columns = list(df.columns)
        sample_values = df.iloc[:5, 0].dropna().tolist()

    elif file_format == "XLSX":
        df = pd.read_excel(uploaded_file)
        columns = list(df.columns)
        sample_values = df.iloc[:5, 0].dropna().tolist()

    elif file_format == "PDF":
        df = extract_pdf_to_dataframe(uploaded_file)

        if df is None or df.empty:
            raise ValueError(
                "Unable to extract structured data from PDF. "
                "Please upload a valid Bank, GST, or Financial document."
            )

        columns = list(df.columns)
        sample_values = df.iloc[:5, 0].dropna().tolist()

    else:
        raise ValueError("Unsupported file format.")

    # 3️⃣ Detect document type (BANK / GST / FIN)
    document_type, confidence_scores = detect_document_type(
        columns,
        sample_values
    )

    # 4️⃣ Save document (ONLY after successful detection)
    document = Document.objects.create(
        file=uploaded_file,
        file_format=file_format,
        document_type=document_type
    )

    # 5️⃣ Load cumulative state (single-user system)
    state = get_cumulative_state()

    # 6️⃣ Parse + merge based on document type
    if document_type == "BANK":
        if df is not None and not df.empty:
            parsed_data = parse_bank_dataframe(df)
            merge_bank(state, parsed_data)

    elif document_type == "GST":
        if df is not None and not df.empty:
            parsed_data = parse_gst_dataframe(df)
            merge_gst(state, parsed_data)

    elif document_type == "FIN":
        if df is not None and not df.empty:
            parsed_data = parse_financial_dataframe(df)
            # merge_financial(state, parsed_data)  # future hook

    # 7️⃣ Recompute global financial health score
    state.financial_health_score = compute_financial_health_score(state)
    state.save()

    # 8️⃣ Final response
    return {
        "document_id": document.id,
        "file_format": file_format,
        "document_type": document_type,
        "confidence_scores": confidence_scores,
    }
