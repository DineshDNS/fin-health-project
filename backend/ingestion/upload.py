from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ingestion.models import IngestedDocument
from ingestion.parsers.common import read_tabular_file, get_file_extension

from ingestion.parsers.bank_parser import parse_bank_dataframe
from ingestion.parsers.gst_parser import parse_gst_dataframe
from ingestion.parsers.financial_parser import parse_financial_dataframe
from ingestion.parsers.pdf_parser import extract_pdf_text


class UploadDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("file")
        category = request.data.get("category")
        document_type = request.data.get("document_type")

        if not file or not category or not document_type:
            return Response(
                {"error": "file, category and document_type are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Normalize inputs
        category = category.upper()
        document_type = document_type.upper()

        # Save document first
        doc = IngestedDocument.objects.create(
            user=request.user,
            file=file,
            category=category,
            document_type=document_type,
        )

        ext = get_file_extension(doc.file.path)
        detected_type = "UNKNOWN"
        parsed = {}

        try:
            # =====================================================
            # TABULAR FILES (CSV / XLSX)
            # =====================================================
            if ext in [".csv", ".xlsx", ".xls"]:
                df = read_tabular_file(doc.file.path)
                columns = {c.lower().strip() for c in df.columns}

                # BANK STATEMENT
                if {"date", "debit", "credit", "balance"}.issubset(columns):
                    detected_type = "BANK"
                    parsed = parse_bank_dataframe(df)

                # GST RETURN
                elif (
                    {"taxable_value", "gst_amount"}.issubset(columns)
                    or {"total_taxable_value", "total_gst"}.issubset(columns)
                ):
                    detected_type = "GST"
                    parsed = parse_gst_dataframe(df)

                # FINANCIAL STATEMENT
                elif {"account", "amount"}.issubset(columns):
                    detected_type = "FIN"
                    parsed = parse_financial_dataframe(df)

                else:
                    detected_type = "UNKNOWN"
                    parsed = {"message": "Unrecognized tabular format"}

            # =====================================================
            # PDF FILES
            # =====================================================
            elif ext == ".pdf":
                text = extract_pdf_text(doc.file.path)
                text_lower = text.lower()

                # ---------- BANK PDF ----------
                if (
                    "bank statement" in text_lower
                    and "debit" in text_lower
                    and "credit" in text_lower
                ):
                    from ingestion.parsers.pdf_table_parser import (
                        extract_bank_table_from_pdf,
                    )

                    df = extract_bank_table_from_pdf(doc.file.path)
                    parsed = parse_bank_dataframe(df)
                    detected_type = "BANK"

                # ---------- GST PDF ----------
                elif (
                    "gst" in text_lower
                    and ("taxable value" in text_lower or "gst amount" in text_lower)
                ):
                    from ingestion.parsers.pdf_gst_table_parser import (
                        extract_gst_table_from_pdf,
                    )

                    df = extract_gst_table_from_pdf(doc.file.path)
                    parsed = parse_gst_dataframe(df)
                    detected_type = "GST"

                # ---------- FINANCIAL PDF ----------
                elif (
                    "profit and loss" in text_lower
                    or "statement of profit" in text_lower
                    or "revenue" in text_lower
                    or "expense" in text_lower
                ):
                    from ingestion.parsers.pdf_fin_table_parser import (
                        extract_financial_table_from_pdf,
                    )

                    df = extract_financial_table_from_pdf(doc.file.path)
                    parsed = parse_financial_dataframe(df)
                    detected_type = "FIN"

                # ---------- UNKNOWN PDF ----------
                else:
                    detected_type = "PDF"
                    parsed = {
                        "source": "pdf",
                        "text_length": len(text),
                        "preview": text[:1000],
                    }

            # =====================================================
            # UNSUPPORTED FILE
            # =====================================================
            else:
                return Response(
                    {"error": "Unsupported file type"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {"error": f"Parsing failed: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save parsing result
        doc.detected_type = detected_type
        doc.parsed_data = parsed
        doc.save()

        return Response(
            {
                "id": doc.id,
                "file_name": doc.file.name.split("/")[-1],
                "category": doc.category,
                "document_type": doc.document_type,
                "detected_type": doc.detected_type,
                "uploaded_at": doc.uploaded_at,
            },
            status=status.HTTP_201_CREATED,
        )
