import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.services.overview_assembler import build_overview_dto


# -------------------------------------------------------------------
# NOTE:
# - This view MUST remain thin.
# - No business logic here.
# - All intelligence comes from services.
# -------------------------------------------------------------------

class OverviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        GET /api/overview/

        Frontend-facing dashboard API.
        This endpoint MUST return only the OverviewDTO structure.
        """

        # -------------------------------------------------
        # 1. Fetch internal data (replace with real calls)
        # -------------------------------------------------
        # These should already exist in your project
        analysis = get_internal_analysis(request.user)
        overview_logic = get_overview_logic(request.user)

        # Example placeholders (REMOVE when wiring real logic)
        # analysis = {...}
        # overview_logic = {...}

        # -------------------------------------------------
        # 2. Build Overview DTO
        # -------------------------------------------------
        overview_dto = build_overview_dto(
            business_id=request.user.id,      # or request.user.business.id
            industry="Retail",                # fetch from business profile
            analysis=analysis,
            overview_logic=overview_logic,
        )

        # -------------------------------------------------
        # 3. Return API response (frozen contract)
        # -------------------------------------------------
        return Response(
            {
                "request_id": str(uuid.uuid4()),
                "status": "SUCCESS",
                "data": overview_dto.dict(),
                "warnings": [],
                "errors": [],
            },
            status=200,
        )
