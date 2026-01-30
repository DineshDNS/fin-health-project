from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import GSTRecord, BankStatement, FinancialHealthScore
from .serializers import GSTRecordSerializer, BankStatementSerializer

from integrations.gst.service import fetch_gst_data
from integrations.gst.parser import normalize_gst_data
from integrations.banking.service import fetch_bank_data
from integrations.banking.parser import normalize_bank_data

from ml.features import compute_features
from ml.scoring import calculate_health_score, classify_risk

from ml.forecasting import cashflow_forecast


@api_view(["POST"])
def import_gst_data(request):
    gstin = request.data.get("gstin")

    raw_data = fetch_gst_data(gstin)
    normalized_data = normalize_gst_data(raw_data)

    record = GSTRecord.objects.create(**normalized_data)
    return Response(GSTRecordSerializer(record).data)


@api_view(["POST"])
def import_bank_data(request):
    account_id = request.data.get("account_id")

    raw_data = fetch_bank_data(account_id)
    normalized_data = normalize_bank_data(raw_data)

    record = BankStatement.objects.create(**normalized_data)
    return Response(BankStatementSerializer(record).data)


@api_view(["POST"])
def calculate_health(request):
    gst = GSTRecord.objects.latest("created_at")
    bank = BankStatement.objects.latest("created_at")

    features = compute_features(gst, bank)
    score = calculate_health_score(features)
    risk = classify_risk(score)

    record = FinancialHealthScore.objects.create(
        gst_record=gst,
        bank_record=bank,
        score=score,
        risk_level=risk
    )

    return Response({
        "score": score,
        "risk_level": risk,
        "features": features
    })

from ai.gpt_service import generate_financial_insights
from .models import FinancialHealthScore


@api_view(["POST"])
def health_insights(request):

    language = request.data.get("language", "en")
    if language not in ["en", "hi", "ta"]:
        language = "en"

    latest = FinancialHealthScore.objects.latest("created_at")

    payload = {
        "score": latest.score,
        "risk_level": latest.risk_level,
        "features": {
            "profit_margin": latest.gst_record.total_sales,
            "cash_flow_ratio": latest.bank_record.total_inflow,
            "emi_ratio": latest.bank_record.loan_emi,
            "tax_compliance": 1,
            "liquidity_ratio": latest.bank_record.average_balance
        }
    }

    insight = generate_financial_insights(payload, language)

    return Response({
        "language": language,
        "insight": insight
    })


@api_view(["GET"])
def cashflow_prediction(request):
    bank_records = BankStatement.objects.order_by("created_at")

    if bank_records.count() < 2:
        return Response({
            "error": "Not enough historical data for forecasting"
        }, status=400)

    forecast = cashflow_forecast(bank_records)

    return Response({
        "forecast_horizon": "3 months",
        "forecast": forecast
    })
