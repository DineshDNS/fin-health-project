from scoring.features import extract_features
from scoring.rules import apply_credit_rules
from scoring.risk_engine import classify_risk


def compute_creditworthiness(state):
    features = extract_features(state)
    base_score, flags = apply_credit_rules(features)
    risk_level = classify_risk(base_score)

    return {
        "credit_score": base_score,
        "risk_level": risk_level,
        "risk_flags": flags,
        "features": features,  # for ML later
    }
