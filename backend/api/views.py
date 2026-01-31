from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

import pandas as pd

from .models import (
    GSTRecord,
    BankStatement,
    FinancialHealthScore,
    FinancialDocument,
)
from .serializers import GSTRecordSerializer, BankStatementSerializer

from integrations.gst.service import fetch_gst_data
from integrations.gst.parser import normalize_gst_data
from integrations.banking.service import fetch_bank_data
from integrations.banking.parser import normalize_bank_data

from ml.features import compute_features
from ml.scoring import calculate_health_score, classify_risk
from ml.forecasting import cashflow_forecast

from ai.gpt_service import generate_financial_insights
from .utils.file_validation import validate_file, validate_text_pdf


# =========================
# AUTH
# =========================

@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email", "")

    if not username or not password:
        return Response(
            {"error": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    User.objects.create_user(
        username=username,
        password=password,
        email=email
    )

    return Response(
        {"message": "User created successfully"},
        status=status.HTTP_201_CREATED
    )


# =========================
# GST & BANK DATA (STRICT)
# =========================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def import_gst_data(request):
    gstin = request.data.get("gstin")

    raw_data = fetch_gst_data(gstin)
    normalized_data = normalize_gst_data(raw_data)

    record = GSTRecord.objects.create(
        user=request.user,
        **normalized_data
    )

    return Response(GSTRecordSerializer(record).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def import_bank_data(request):
    account_id = request.data.get("account_id")

    raw_data = fetch_bank_data(account_id)
    normalized_data = normalize_bank_data(raw_data)

    record = BankStatement.objects.create(
        user=request.user,
        **normalized_data
    )

    return Response(BankStatementSerializer(record).data)


# =========================
# FINANCIAL HEALTH (STRICT)
# =========================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def calculate_health(request):
    gst = GSTRecord.objects.filter(user=request.user).latest("created_at")
    bank = BankStatement.objects.filter(user=request.user).latest("created_at")

    features = compute_features(gst, bank)
    score = calculate_health_score(features)
    risk = classify_risk(score)

    FinancialHealthScore.objects.create(
        user=request.user,
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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def health_insights(request):
    language = request.data.get("language", "en")
    if language not in ["en", "hi", "ta"]:
        language = "en"

    latest = FinancialHealthScore.objects.filter(
        user=request.user
    ).latest("created_at")

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


# =========================
# CASH FLOW FORECAST (STRICT)
# =========================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cashflow_prediction(request):
    bank_records = BankStatement.objects.filter(
        user=request.user
    ).order_by("created_at")

    if bank_records.count() < 2:
        return Response(
            {"error": "Not enough historical data for forecasting"},
            status=status.HTTP_400_BAD_REQUEST
        )

    forecast = cashflow_forecast(bank_records)

    return Response(
        {
            "forecast_horizon": "3 months",
            "forecast": forecast
        },
        status=status.HTTP_200_OK
    )


# =========================
# FILE UPLOAD (STRICT)
# =========================

class FinancialUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "No file uploaded"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            ext = validate_file(file)

            if ext == ".pdf":
                validate_text_pdf(file)
            elif ext == ".csv":
                pd.read_csv(file)
            elif ext == ".xlsx":
                pd.read_excel(file)

            FinancialDocument.objects.create(
                user=request.user,
                file=file,
                file_type=ext.replace(".", "")
            )

            return Response(
                {"message": "File uploaded successfully"},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum

from .models import (
    FinancialHealthScore,
    BankStatement,
    GSTRecord,
    FinancialDocument,
)

class OverviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # ---- Health Score & Risk ----
        health = (
            FinancialHealthScore.objects
            .filter(user=user)
            .order_by("-created_at")
            .first()
        )

        # ---- Bank Data ----
        bank_agg = BankStatement.objects.filter(user=user).aggregate(
            inflow=Sum("total_inflow"),
            outflow=Sum("total_outflow"),
            loan_emi=Sum("loan_emi"),
        )

        # ---- GST Compliance ----
        gst_pending = GSTRecord.objects.filter(
            user=user, filing_status=False
        ).exists()

        # ---- Documents Coverage ----
        doc_count = FinancialDocument.objects.filter(user=user).count()

        # ---- Derived Metrics ----
        cash_flow_status = "Positive"
        if bank_agg["inflow"] and bank_agg["outflow"]:
            if bank_agg["inflow"] - bank_agg["outflow"] < 0:
                cash_flow_status = "Negative"

        response = {
            "health_score": health.score if health else None,
            "risk_level": health.risk_level if health else "Unknown",
            "cash_flow_status": cash_flow_status,
            "credit_exposure": bank_agg["loan_emi"] or 0,
            "compliance_status": "GST Pending" if gst_pending else "Compliant",
            "data_coverage": doc_count,
            "recommendations": [
                "Upload missing GST returns" if gst_pending else "GST filings are up to date",
                "Reduce loan EMI burden if possible",
                "Improve cash inflow consistency",
            ],
        }

        return Response(response)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import FinancialDocument

class DocumentListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        docs = FinancialDocument.objects.filter(user=request.user).order_by("-uploaded_at")

        data = [
            {
                "id": d.id,
                "file_name": d.file.name.split("/")[-1],
                "file_type": d.file_type,
                "uploaded_at": d.uploaded_at,
                "file_url": d.file.url,
            }
            for d in docs
        ]

        return Response(data)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import FinancialHealthScore, BankStatement

class AnalysisAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        health = (
            FinancialHealthScore.objects
            .filter(user=user)
            .order_by("-created_at")
            .first()
        )

        bank_data = BankStatement.objects.filter(user=user).order_by("created_at")

        cash_flow_trend = [
            {
                "month": b.month,
                "net_flow": b.total_inflow - b.total_outflow
            }
            for b in bank_data
        ]

        # ✅ FALLBACK (for early stage / demo / empty DB)
        if not cash_flow_trend:
            cash_flow_trend = [
                {"month": "Jan", "net_flow": 8000},
                {"month": "Feb", "net_flow": -3000},
                {"month": "Mar", "net_flow": 12000},
                {"month": "Apr", "net_flow": 5000},
            ]

        response = {
            "health_score": health.score if health else None,
            "risk_level": health.risk_level if health else "Unknown",
            "cash_flow_trend": cash_flow_trend,
            "insights": [
                "Cash flow shows month-to-month volatility",
                "Loan EMI obligations are affecting liquidity",
                "Improving receivables can increase the health score",
            ],
        }

        return Response(response)

