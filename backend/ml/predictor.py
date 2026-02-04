import pandas as pd
from ml.features import extract_features

def predict_creditworthiness(model, bank=None, gst=None, fin=None):
    features = extract_features(bank=bank, gst=gst, fin=fin)

    X = pd.DataFrame([features])
    prob = model.predict_proba(X)[0][1]

    return {
        "ml_credit_score": round(prob * 100, 2),
        "ml_risk_level": (
            "LOW" if prob >= 0.7 else
            "MODERATE" if prob >= 0.4 else
            "HIGH"
        ),
        "confidence": round(prob, 3)
    }
