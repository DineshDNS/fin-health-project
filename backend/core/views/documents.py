from rest_framework.views import APIView
from rest_framework.response import Response
from core.services.documents_context_builder import build_documents_context
from core.services.documents_assembler import DocumentsAssembler


class DocumentsAPIView(APIView):
    def get(self, request):
        context = build_documents_context(request.user)
        dto = DocumentsAssembler.build(context)

        return Response({
            "request_id": context.request_id,
            "status": "SUCCESS",
            "data": dto.dict(),
            "warnings": context.warnings,
            "errors": [],
        })
