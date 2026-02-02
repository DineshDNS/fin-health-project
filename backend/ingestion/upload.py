from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ingestion.models import IngestedDocument
from ingestion.parsers.common import read_tabular_file, get_file_extension
from ingestion.parsers.bank_parser import parse_bank_dataframe
from ingestion.parsers.gst_parser import parse_gst_dataframe
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
            if ext in [".csv", ".xlsx", ".xls"]:
                df = read_tabular_file(doc.file.path)
                columns = set(df.columns.str.lower())

                if {"date", "amount", "type"}.issubset(columns):
                    detected_type = "BANK"
                    parsed = parse_bank_dataframe(df)

                elif {"taxable_value", "gst_paid"}.issubset(columns):
                    detected_type = "GST"
                    parsed = parse_gst_dataframe(df)

            elif ext == ".pdf":
                detected_type = "PDF"
                text = extract_pdf_text(doc.file.path)
                parsed = {
                    "text_length": len(text),
                    "preview": text[:1000],
                }

        except Exception as e:
            return Response({"error": str(e)}, status=400)

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
