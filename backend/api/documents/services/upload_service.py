import pandas as pd

from api.documents.models import Document
from analysis.models import DocumentAnalysis

from parsers.bank_parser import parse_bank_dataframe
from parsers.gst_parser import parse_gst_dataframe
from parsers.financial_parser import parse_financial_dataframe


class DocumentUploadService:

    @staticmethod
    def upload(dto, file):

        # ---------------------------------------
        # 1. Save document
        # ---------------------------------------
        document = Document.objects.create(
            type=dto["type"],
            year=dto["year"],
            month=dto.get("month"),
            quarter=dto.get("quarter"),
            source=dto.get("source"),
            file=file,
            status="UPLOADED"
        )

        # ---------------------------------------
        # 2. Clear old analysis
        # ---------------------------------------
        DocumentAnalysis.objects.all().delete()

        # ---------------------------------------
        # 3. Load dataframe
        # ---------------------------------------
        try:
            path = document.file.path

            if path.endswith(".csv"):
                df = pd.read_csv(path)
            elif path.endswith(".xlsx"):
                df = pd.read_excel(path)
            else:
                df = None

        except Exception as e:
            print("File read failed:", str(e))
            df = None

        # ---------------------------------------
        # 4. Run parser + SAVE ANALYSIS (KEY FIX)
        # ---------------------------------------
        try:

            if document.type == "BANK_STATEMENT" and df is not None:
                parsed = parse_bank_dataframe(df)

                DocumentAnalysis.objects.create(
                    document=document,  # ⭐ REQUIRED
                    document_type="BANK",
                    total_credits=parsed.get("total_credits", 0),
                    total_debits=parsed.get("total_debits", 0),
                    net_cash_flow=parsed.get("net_cash_flow", 0),
                    expense_ratio=parsed.get("expense_ratio", 0),
                    cashflow_volatile=parsed.get("cashflow_volatile", False),
                )

            elif document.type == "GST_RETURN" and df is not None:
                parsed = parse_gst_dataframe(df)

                DocumentAnalysis.objects.create(
                    document=document,  # ⭐ REQUIRED
                    document_type="GST",
                    taxable_value=parsed.get("taxable_value", 0),
                    gst_paid=parsed.get("gst_paid", 0),
                    expected_gst=parsed.get("expected_gst", 0),
                    compliance_gap=parsed.get("compliance_gap", 0),
                    is_compliant=parsed.get("is_compliant", True),
                )

            elif document.type in ["BALANCE_SHEET", "PROFIT_AND_LOSS"] and df is not None:
                parsed = parse_financial_dataframe(df)

                DocumentAnalysis.objects.create(
                    document=document,  # ⭐ REQUIRED
                    document_type="FIN",
                    total_assets=parsed.get("total_assets"),
                    total_liabilities=parsed.get("total_liabilities"),
                    savings_ratio=parsed.get("savings_ratio"),
                    current_ratio=parsed.get("current_ratio"),
                )

        except Exception as e:
            print("Analysis generation failed:", str(e))

        return document
