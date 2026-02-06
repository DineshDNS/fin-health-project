from django.http import JsonResponse
from django.views import View

from api.documents.models import DocumentHistory


class DocumentHistoryView(View):

    def get(self, request, document_id):
        history = DocumentHistory.objects.filter(
            document_id=document_id
        ).order_by("-timestamp")

        data = [
            {
                "action": h.action,
                "timestamp": h.timestamp,
            }
            for h in history
        ]

        return JsonResponse({
            "status": "SUCCESS",
            "data": data
        })
