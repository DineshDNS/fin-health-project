from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from api.documents.services.document_validator import DocumentValidator
from api.documents.services.upload_service import DocumentUploadService


@method_decorator(csrf_exempt, name="dispatch")
class DocumentUploadView(View):

    def post(self, request):
        try:
            # ---- REQUIRED FIELD ----
            year = request.POST.get("year")
            if not year:
                raise Exception("Year is required")

            if "file" not in request.FILES:
                raise Exception("File is required")

            # ---- NORMALIZED DTO ----
            dto = {
                "type": request.POST.get("type"),
                "year": int(year),
                "month": request.POST.get("month") or None,
                "quarter": request.POST.get("quarter") or None,

                # 🔥 CRITICAL FIX:
                # source MUST NOT be NULL (DB constraint)
                # normalize empty → empty string
                "source": request.POST.get("source") or "",
            }

            file = request.FILES["file"]

            # ---- VALIDATION ----
            DocumentValidator.validate(dto, file)

            # ---- UPLOAD ----
            document = DocumentUploadService.upload(dto, file)

            return JsonResponse({
                "status": "SUCCESS",
                "document_id": str(document.id)
            })

        except Exception as e:
            return JsonResponse({
                "status": "ERROR",
                "message": str(e)
            }, status=400)
