from ml.model import load_model
from ml.features import extract_ml_features
from ml_tracking.models import MLInference


def run_ml_inference(document, analysis_state):
    """
    Runs ML model and persists prediction.
    """

    model = load_model()
    features = extract_ml_features(analysis_state)

    probability = model.predict_proba([features])[0][1]

    predicted_risk = (
        "HIGH" if probability > 0.7
        else "MODERATE" if probability > 0.4
        else "LOW"
    )

    MLInference.objects.create(
        document=document,
        model_name="CreditRiskLogReg",
        model_version="v1.0",
        features=dict(zip([
            "expense_ratio",
            "net_cash_flow",
            "gst_compliance_gap",
            "cashflow_volatile",
            "savings_ratio",
            "closing_balance",
        ], features)),
        probability=probability,
        predicted_risk=predicted_risk,
    )

    return predicted_risk, probability
