def risk_ui_summary(score, risk_level):
    mapping = {
        "LOW": {
            "headline": "Financial health looks good",
            "subtext": "Your business is financially stable",
            "severity": "success",
            "color": "green",
            "icon": "check-circle",
        },
        "MODERATE": {
            "headline": "Moderate financial risk detected",
            "subtext": "Some areas need attention",
            "severity": "warning",
            "color": "orange",
            "icon": "alert-triangle",
        },
        "HIGH": {
            "headline": "High financial risk detected",
            "subtext": "Immediate action is recommended",
            "severity": "danger",
            "color": "red",
            "icon": "alert-octagon",
        },
    }
    return mapping[risk_level]


def decorate_recommendation_ui(rec):
    priority_ui = {
        "HIGH": ("High Priority", "danger", "primary"),
        "MEDIUM": ("Medium Priority", "warning", "secondary"),
        "LOW": ("Low Priority", "info", "ghost"),
    }

    badge, severity, cta_type = priority_ui[rec["priority"]]

    rec["ui"] = {
        "badge": badge,
        "severity": severity,
        "icon": "trending-down",
        "cta": {
            "label": "Take Action",
            "type": cta_type,
        },
    }
    return rec


def decorate_product_ui(product):
    score = product["confidence_score"]

    if score >= 0.75:
        label, color = "Very Suitable", "green"
    elif score >= 0.5:
        label, color = "Suitable", "orange"
    else:
        label, color = "Low Suitability", "gray"

    product["confidence_label"] = label
    product["ui"] = {
        "confidence_bar_color": color,
        "cta": {
            "label": "Check Eligibility",
            "type": "primary",
        },
        "disclaimer": "Subject to bank approval",
    }
    return product
