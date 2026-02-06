from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from api.documents.services.document_validator import DocumentValidator
from api.documents.services.replace_service import DocumentReplaceService


@method_decorator(csrf_exempt, name="dispatch")
class DocumentReplaceView(View):

    def post(self, request):
        try:
            document_id = request.POST.get("document_id")
            if not document_id:
                raise Exception("document_id is required")

            if "file" not in request.FILES:
                raise Exception("File is required")

            file = request.FILES["file"]

            year = request.POST.get("year")
            if not year:
                raise Exception("Year is required")

            # 🔥 USE DICT (same as upload flow)
            dto = {
                "type": request.POST.get("type"),
                "year": int(year),
                "month": request.POST.get("month") or None,
                "quarter": request.POST.get("quarter") or None,
                "source": request.POST.get("source") or None,
            }

            # 🔥 VALIDATE
            DocumentValidator.validate(dto, file)

            # 🔥 REPLACE
            new_doc = DocumentReplaceService.replace(document_id, dto, file)

            return JsonResponse({
                "status": "SUCCESS",
                "new_document_id": str(new_doc.id)
            })

        except Exception as e:
            print("REPLACE ERROR:", str(e))
            return JsonResponse({
                "status": "ERROR",
                "message": str(e)
            }, status=400)
