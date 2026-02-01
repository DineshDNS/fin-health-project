from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import FinancialDocument, DocumentParseResult
from .serializers import FinancialDocumentSerializer
from .utils.parser import parse_document


class UploadDocumentView(APIView):
    """
    Upload a financial document (PDF / CSV / XLSX)
    Automatically parses the document safely.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()

        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return Response(
                {"error": "File is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 🔑 Normalize file type
        data["file_type"] = uploaded_file.name.split(".")[-1].upper()

        serializer = FinancialDocumentSerializer(data=data)

        if serializer.is_valid():
            document = serializer.save(user=request.user)

            try:
                # 🔥 STEP 7: Parse document
                parsed_data = parse_document(document)

                DocumentParseResult.objects.create(
                    document=document,
                    rows=parsed_data.get("rows"),
                    columns=parsed_data.get("columns"),
                    text_length=parsed_data.get("text_length"),
                )

                document.processed = True

            except Exception as e:
                # Parsing error should not crash upload
                document.processing_error = str(e)
                document.processed = False

            document.save()

            return Response(
                {
                    "message": "Document uploaded and processed",
                    "document_id": document.id,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class DocumentListView(APIView):
    """
    List documents uploaded by the logged-in user
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        documents = FinancialDocument.objects.filter(
            user=request.user
        ).order_by("-uploaded_at")

        serializer = FinancialDocumentSerializer(documents, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
