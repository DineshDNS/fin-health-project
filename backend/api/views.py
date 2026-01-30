from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import GSTRecord, BankStatement
from .serializers import GSTRecordSerializer, BankStatementSerializer

@api_view(["POST"])
def import_gst_data(request):
    data = {
        "gstin": request.data.get("gstin"),
        "period": "2025-12",
        "total_sales": 1200000,
        "total_tax_paid": 216000,
        "filing_status": True
    }
    record = GSTRecord.objects.create(**data)
    return Response(GSTRecordSerializer(record).data)


@api_view(["POST"])
def import_bank_data(request):
    data = {
        "account_id": request.data.get("account_id"),
        "month": "2025-12",
        "total_inflow": 900000,
        "total_outflow": 820000,
        "average_balance": 150000,
        "loan_emi": 40000
    }
    record = BankStatement.objects.create(**data)
    return Response(BankStatementSerializer(record).data)
