import pandas as pd
import traceback

from django.db import transaction

from documents.models import Document
from documents.validators import validate_file_format
from documents.detector import detect_document_type
from documents.extractors.pdf_extractor import extract_pdf_to_dataframe

from parsers.bank_parser import parse_bank_dataframe
from parsers.gst_parser import parse_gst_dataframe
from parsers.financial_parser import parse_financial_dataframe

from analysis.models import DocumentAnalysis
from scoring.services import compute_financial_health_score, determine_risk_level


def handle_document_upload(uploaded_file):
    """
    Upload pipeline (per-document analysis):
    1. Validate file format
    2. Extract structured data
    3. Detect document type
    4. Save document
    5. Parse document
    6. Compute score
    7. Persist DocumentAnalysis (CRITICAL)
    """

    # 1️⃣ Validate format
    file_format = validate_file_format(uploaded_file)
    uploaded_file.seek(0)

    # 2️⃣ Load dataframe
    if file_format == "CSV":
        df = pd.read_csv(uploaded_file)

    elif file_format == "XLSX":
        df = pd.read_excel(uploaded_file)

    elif file_format == "PDF":
        df = extract_pdf_to_dataframe(uploaded_file)
        if df is None or df.empty:
            raise ValueError("Unable to extract structured data from PDF")

    else:
        raise ValueError("Unsupported file format")

    columns = list(df.columns)
    sample_values = df.iloc[:5, 0].dropna().tolist()

    # 3️⃣ Detect document type
    document_type, confidence_scores = detect_document_type(
        columns,
        sample_values
    )

    # 4️⃣ Save document
    document = Document.objects.create(
        file=uploaded_file,
        file_format=file_format,
        document_type=document_type,
    )

    # 5️⃣ Parse document
    if document_type == "BANK":
        parsed = parse_bank_dataframe(df)

    elif document_type == "GST":
        parsed = parse_gst_dataframe(df)

    elif document_type == "FIN":
        parsed = parse_financial_dataframe(df)

    else:
        raise ValueError("Unknown document type")

    # 6️⃣ Compute score (per document)
    score = compute_financial_health_score(parsed, document_type)
    risk_level = determine_risk_level(score)

    # 7️⃣ Persist analysis (THIS WAS MISSING EARLIER)
    try:
        with transaction.atomic():

            if document_type == "BANK":
                DocumentAnalysis.objects.create(
                    document=document,
                    document_type="BANK",
                    total_credits=parsed.get("total_credits", 0),
                    total_debits=parsed.get("total_debits", 0),
                    net_cash_flow=parsed.get("net_cash_flow", 0),
                    expense_ratio=parsed.get("expense_ratio", 0),
                    cashflow_volatile=parsed.get("cashflow_volatile", False),
                    financial_health_score=score,
                    risk_level=risk_level,
                )

            elif document_type == "GST":
                DocumentAnalysis.objects.create(
                    document=document,
                    document_type="GST",
                    taxable_value=parsed.get("taxable_value", 0),
                    gst_paid=parsed.get("gst_paid", 0),
                    expected_gst=parsed.get("expected_gst", 0),
                    compliance_gap=parsed.get("compliance_gap", 0),
                    is_compliant=parsed.get("is_compliant", True),
                    financial_health_score=score,
                    risk_level=risk_level,
                )

            elif document_type == "FIN":
                DocumentAnalysis.objects.create(
                    document=document,
                    document_type="FIN",
                    financial_health_score=score,
                    risk_level=risk_level,
                )

    except Exception:
        print("❌ ERROR: Failed to create DocumentAnalysis")
        traceback.print_exc()
        raise

    # 8️⃣ Final response
    return {
        "document_id": document.id,
        "document_type": document_type,
        "file_format": file_format,
        "confidence_scores": confidence_scores,
    }
