from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ingestion.models import IngestedDocument


class DocumentListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        documents = (
            IngestedDocument.objects
            .filter(user=request.user)
            .order_by("-uploaded_at")
        )

        response = []

        for doc in documents:
            item = {
                "id": doc.id,
                "file_name": doc.file.name.split("/")[-1],
                "detected_type": doc.detected_type,
                "uploaded_at": doc.uploaded_at,
            }

            parsed = doc.parsed_data or {}

            # ---- BANK ----
            if doc.detected_type == "BANK":
                item["summary"] = {
                    "total_credits": parsed.get("total_credits"),
                    "total_debits": parsed.get("total_debits"),
                    "closing_balance": parsed.get("closing_balance"),
                }

            # ---- GST ----
            elif doc.detected_type == "GST":
                item["summary"] = {
                    "taxable_value": parsed.get("taxable_value"),
                    "gst_paid": parsed.get("gst_paid"),
                    "expected_gst": parsed.get("expected_gst"),
                }

            # ---- PDF ----
            elif doc.detected_type == "PDF":
                item["summary"] = {
                    "llm_summary": parsed.get("llm_summary"),
                }

            response.append(item)

        return Response(response)
