from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import handle_document_upload
from .validators import FileValidationError


class DocumentUploadView(APIView):
    def post(self, request):
        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return Response(
                {"error": "No file uploaded."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            result = handle_document_upload(uploaded_file)

        except FileValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        except ValueError as e:   # 👈 THIS WAS MISSING
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": f"This document has been identified as a {result['document_type']}. Upload will proceed.",
                "file_format": result["file_format"],
                "document_type": result["document_type"],
                "confidence_scores": result.get("confidence_scores"),
            },
            status=status.HTTP_200_OK
        )
