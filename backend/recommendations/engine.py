from .rules import (
    negative_cashflow_rule,
    high_expense_ratio_rule,
    cashflow_volatility_rule,
    gst_compliance_gap_rule,
    gst_overpayment_rule,
    low_savings_ratio_rule,
    weak_liquidity_rule,
    ml_high_risk_rule,
    ml_moderate_risk_rule,
)

# Priority ranking for sorting
PRIORITY_ORDER = {
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3,
}


def generate_recommendations(bank=None, gst=None, fin=None, ml_result=None):
    """
    Orchestrates all recommendation rules,
    deduplicates results, and sorts by priority.
    """

    raw_recommendations = []

    rules = [
        lambda: negative_cashflow_rule(bank),
        lambda: high_expense_ratio_rule(bank),
        lambda: cashflow_volatility_rule(bank),

        lambda: gst_compliance_gap_rule(gst),
        lambda: gst_overpayment_rule(gst),

        lambda: low_savings_ratio_rule(fin),
        lambda: weak_liquidity_rule(fin),

        lambda: ml_high_risk_rule(ml_result),
        lambda: ml_moderate_risk_rule(ml_result),
    ]

    # -------------------------
    # Collect raw recommendations
    # -------------------------
    for rule in rules:
        rec = rule()
        if rec:
            raw_recommendations.append(rec)

    # -------------------------
    # Deduplicate by ID
    # -------------------------
    deduped = {}
    for rec in raw_recommendations:
        rec_id = rec["id"]

        # Keep the highest priority version if duplicates appear
        if rec_id not in deduped:
            deduped[rec_id] = rec
        else:
            existing = deduped[rec_id]
            if PRIORITY_ORDER[rec["priority"]] < PRIORITY_ORDER[existing["priority"]]:
                deduped[rec_id] = rec

    deduped_list = list(deduped.values())

    # -------------------------
    # Sort by priority → category → id
    # -------------------------
    deduped_list.sort(
        key=lambda r: (
            PRIORITY_ORDER.get(r["priority"], 99),
            r["category"],
            r["id"],
        )
    )

    return {
        "recommendations": deduped_list
    }
