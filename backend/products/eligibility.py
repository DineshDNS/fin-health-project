RISK_ORDER = {
    "LOW": 1,
    "MODERATE": 2,
    "HIGH": 3,
}


def risk_alignment_score(business_risk, product_min_risk):
    """
    Returns a score between 0 and 1 indicating
    how well the business risk aligns with product requirement.
    """
    diff = RISK_ORDER[business_risk] - RISK_ORDER[product_min_risk]

    if diff <= 0:
        return 1.0        # safer than required
    elif diff == 1:
        return 0.6
    else:
        return 0.3


def is_product_eligible(product, *, risk_level, gst_compliant):
    if RISK_ORDER[risk_level] > RISK_ORDER[product["min_risk_level"]]:
        return False

    if product["requires_gst_compliance"] and not gst_compliant:
        return False

    return True
