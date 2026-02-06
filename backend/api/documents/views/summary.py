from django.http import JsonResponse
from django.views import View

from api.documents.assembler.summary_assembler import DocumentsSummaryAssembler


class DocumentsSummaryView(View):

    def get(self, request):
        data = DocumentsSummaryAssembler.build()

        return JsonResponse({
            "status": "SUCCESS",
            "data": data
        })
