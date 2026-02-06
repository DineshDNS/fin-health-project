from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from api.documents.services.delete_service import DocumentDeleteService


@method_decorator(csrf_exempt, name="dispatch")
class DocumentDeleteView(View):

    def post(self, request):
        try:
            document_id = request.POST.get("document_id")
            if not document_id:
                raise Exception("document_id is required")

            doc = DocumentDeleteService.delete(document_id)

            return JsonResponse({
                "status": "SUCCESS",
                "deleted_document_id": str(doc.id)
            })

        except Exception as e:
            return JsonResponse({
                "status": "ERROR",
                "message": str(e)
            }, status=400)
