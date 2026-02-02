from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import FileResponse

from ingestion.models import IngestedDocument


class DocumentsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        docs = IngestedDocument.objects.filter(user=request.user)

        return Response([
            {
                "id": d.id,
                "file_name": d.file.name.split("/")[-1],

                # ABSOLUTE URL
                "file_url": request.build_absolute_uri(d.file.url),

                "category": d.get_category_display(),
                "document_type": d.get_document_type_display(),
                "uploaded_at": d.uploaded_at,
            }
            for d in docs
        ])



class DeleteDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        doc = IngestedDocument.objects.get(pk=pk, user=request.user)
        doc.file.delete()
        doc.delete()
        return Response({"success": True})
