def profitability_score(total_revenue, total_expenses):
    """
    Question 1: Is the business profitable?
    Max score: 30
    """

    if total_revenue > total_expenses:
        return {
            "score": 30,
            "risk": "LOW",
            "message": "Business is profitable"
        }

    if total_revenue == total_expenses:
        return {
            "score": 15,
            "risk": "MEDIUM",
            "message": "Business is breaking even"
        }

    return {
        "score": 0,
        "risk": "HIGH",
        "message": "Business is running at a loss"
    }
