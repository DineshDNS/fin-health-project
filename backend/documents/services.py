import pandas as pd

from documents.models import Document
from documents.validators import validate_file_format
from documents.detector import detect_document_type
from documents.extractors.pdf_extractor import extract_pdf_to_dataframe

from parsers.bank_parser import parse_bank_dataframe
from parsers.gst_parser import parse_gst_dataframe
from parsers.financial_parser import parse_financial_dataframe

from analysis.models import DocumentAnalysis
from scoring.services import (
    compute_financial_health_score,
    determine_risk_level,
)


def handle_document_upload(uploaded_file):
    """
    Upload → detect → parse → analyze → persist analysis
    """

    # 1️⃣ Validate file format
    file_format = validate_file_format(uploaded_file)
    uploaded_file.seek(0)

    # 2️⃣ Read structured data
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
    sample_values = df.iloc[:5, 0].dropna().astype(str).tolist()

    # 3️⃣ Detect document type
    document_type, confidence_scores = detect_document_type(
        columns,
        sample_values
    )

    # 4️⃣ Save document
    document = Document.objects.create(
        file=uploaded_file,
        file_format=file_format,
        document_type=document_type
    )

    # 5️⃣ Parse document + build analysis payload
    analysis_data = {
        "document": document,
        "document_type": document_type,
    }

    if document_type == "BANK":
        parsed = parse_bank_dataframe(df)
        analysis_data.update({
            "total_credits": parsed["total_credits"],
            "total_debits": parsed["total_debits"],
            "net_cash_flow": parsed["net_cash_flow"],
            "expense_ratio": parsed["expense_ratio"],
            "cashflow_volatile": parsed["cashflow_volatile"],
        })

    elif document_type == "GST":
        parsed = parse_gst_dataframe(df)
        analysis_data.update({
            "taxable_value": parsed["taxable_value"],
            "gst_paid": parsed["gst_paid"],
            "expected_gst": parsed["expected_gst"],
            "compliance_gap": parsed["compliance_gap"],
            "is_compliant": parsed["is_compliant"],
        })

    elif document_type == "FIN":
        parsed = parse_financial_dataframe(df)
        # Placeholder – extend later

    # 6️⃣ Compute score + risk
    score = compute_financial_health_score(
        analysis_data,
        document_type
    )
    risk_level = determine_risk_level(score)

    analysis_data["financial_health_score"] = score
    analysis_data["risk_level"] = risk_level

    # 7️⃣ Persist analysis
    DocumentAnalysis.objects.create(**analysis_data)

    return {
        "document_id": document.id,
        "file_format": file_format,
        "document_type": document_type,
        "confidence_scores": confidence_scores,
    }
