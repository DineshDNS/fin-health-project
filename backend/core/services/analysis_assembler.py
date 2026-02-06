from core.dto.enums import RiskLevel, SeverityLevel


# --------------------------------------------------
# UI HELPERS
# --------------------------------------------------

def _risk_to_ui(risk):
    if risk == RiskLevel.HIGH:
        return "danger"
    if risk == RiskLevel.MODERATE:
        return "warning"
    return "info"


def _pillar(data):
    return {
        "score": data.get("score", 0),
        "status": data.get("status", "INFO"),
        "drivers": data.get("drivers", []),
        "ui": {
            "severity": "info"
        }
    }


# --------------------------------------------------
# MAIN ASSEMBLER (DICT-BASED, SAFE)
# --------------------------------------------------

def build_analysis_dto(
    *,
    score,
    risk_level,
    ml_result,
    breakdown,
    risks,
    trends,
    impact_actions,
):

    breakdown = breakdown or {}
    trends = trends or {}

    # 🛡️ HARD SAFETY DEFAULTS
    breakdown.setdefault("liquidity", {})
    breakdown.setdefault("profitability", {})
    breakdown.setdefault("compliance", {})
    breakdown.setdefault("cashflow", {})

    trends.setdefault("cashflow", "STABLE")
    trends.setdefault("revenue", "STABLE")
    trends.setdefault("expense", "STABLE")

    return {
        "financial_health": {
            "overall_score": score,
            "risk_band": risk_level,
            "confidence": float(ml_result.get("confidence", 0.0)),
            "ui": {
                "severity": _risk_to_ui(risk_level)
            }
        },

        "health_breakdown": {
            "liquidity": _pillar(breakdown["liquidity"]),
            "profitability": _pillar(breakdown["profitability"]),
            "compliance": _pillar(breakdown["compliance"]),
            "cashflow": _pillar(breakdown["cashflow"]),
        },

        "risk_factors": risks or [],

        "trend_signals": {
            "cashflow_trend": trends["cashflow"],
            "revenue_trend": trends["revenue"],
            "expense_trend": trends["expense"],
            "ui": {
                "severity": "warning"
            }
        },

        "ml_explainability": {
            "risk_band": risk_level,
            "confidence": float(ml_result.get("confidence", 0.0)),
            "key_features": ml_result.get("key_features", []),
            "model_version": ml_result.get("model_version", "v1.0"),
        },

        "impact_simulation": impact_actions or [],
    }
