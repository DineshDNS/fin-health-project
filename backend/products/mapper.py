def map_recommendations_to_products(
    recommendations,
    risk_level,
    gst_compliant=True,
):
    """
    Maps recommendations to suitable bank / NBFC products.
    Returns EMPTY list if financing is not appropriate.
    """

    products = []

    # --------------------------------------------------
    # LOW RISK → No financing required
    # --------------------------------------------------
    if risk_level == "LOW":
        return []

    # --------------------------------------------------
    # MODERATE RISK → Bank-grade products
    # --------------------------------------------------
    if risk_level == "MODERATE":
        for r in recommendations:
            if r["category"] == "CASHFLOW_IMPROVEMENT":
                products.append({
                    "product_id": "BANK_OD_001",
                    "provider": "ABC Bank",
                    "product_type": "OVERDRAFT",
                    "linked_recommendation": r["id"],
                    "confidence_score": 0.75 if gst_compliant else 0.6,
                })

            if r["category"] == "CREDIT_READINESS":
                products.append({
                    "product_id": "BANK_TL_001",
                    "provider": "ABC Bank",
                    "product_type": "TERM_LOAN",
                    "linked_recommendation": r["id"],
                    "confidence_score": 0.7 if gst_compliant else 0.55,
                })

    # --------------------------------------------------
    # HIGH RISK → Recovery-focused NBFC products
    # --------------------------------------------------
    if risk_level == "HIGH":
        for r in recommendations:
            if r["category"] == "CASHFLOW_IMPROVEMENT":
                products.append({
                    "product_id": "NBFC_WC_001",
                    "provider": "Partner NBFC",
                    "product_type": "WORKING_CAPITAL",
                    "linked_recommendation": r["id"],
                    "confidence_score": 0.65,
                })

            if r["category"] == "CREDIT_READINESS":
                products.append({
                    "product_id": "NBFC_BRIDGE_001",
                    "provider": "Partner NBFC",
                    "product_type": "BRIDGE_LOAN",
                    "linked_recommendation": r["id"],
                    "confidence_score": 0.6,
                })

        # Fallback: ensure at least ONE recovery option
        if not products:
            products.append({
                "product_id": "NBFC_EMERGENCY_001",
                "provider": "Partner NBFC",
                "product_type": "EMERGENCY_CREDIT",
                "linked_recommendation": None,
                "confidence_score": 0.55,
            })

    # --------------------------------------------------
    # De-duplicate by product_id
    # --------------------------------------------------
    unique = {}
    for p in products:
        unique[p["product_id"]] = p

    return list(unique.values())
