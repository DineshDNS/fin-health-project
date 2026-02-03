from .features import extract_features


def predict_creditworthiness(model, analysis):
    features = extract_features(analysis)
    X = [list(features.values())]

    probability = model.predict_proba(X)[0][1]

    return {
        "approval_probability": round(float(probability), 2),
        "ml_risk_level": "LOW" if probability >= 0.7 else "HIGH"
    }
