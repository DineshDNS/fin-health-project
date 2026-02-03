def classify_risk(score):
    if score >= 80:
        return "LOW"
    elif score >= 60:
        return "MODERATE"
    elif score >= 40:
        return "HIGH"
    return "CRITICAL"
