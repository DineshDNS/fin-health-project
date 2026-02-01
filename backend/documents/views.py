from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import FinancialDocument
from .serializers import FinancialDocumentSerializer


from rest_framework.permissions import IsAuthenticated

class UploadDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()

        # 🔑 AUTO-DETECT FILE TYPE
        uploaded_file = request.FILES.get("file")
        if uploaded_file:
            data["file_type"] = uploaded_file.name.split(".")[-1].lower()

        serializer = FinancialDocumentSerializer(data=data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": "Document uploaded successfully"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DocumentListView(APIView):
    """
    List all uploaded documents
    """
    permission_classes = [AllowAny]

    def get(self, request):
        documents = FinancialDocument.objects.all().order_by("-id")
        serializer = FinancialDocumentSerializer(
            documents, many=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
