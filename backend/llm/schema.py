from jsonschema import validate, ValidationError


LLM_OUTPUT_SCHEMA = {
    "type": "object",
    "required": [
        "executive_summary",
        "risk_explanation",
        "key_concerns",
        "action_plan",
        "confidence_note",
    ],
    "properties": {
        "executive_summary": {"type": "string"},

        "risk_explanation": {
            "type": "object",
            "required": ["overall_risk", "explanation"],
            "properties": {
                "overall_risk": {
                    "type": "string",
                    "enum": ["LOW", "MODERATE", "HIGH"]
                },
                "explanation": {"type": "string"}
            }
        },

        "key_concerns": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["area", "description"],
                "properties": {
                    "area": {
                        "type": "string",
                        "enum": [
                            "Cash Flow",
                            "Expenses",
                            "GST",
                            "Financial Stability",
                            "Creditworthiness"
                        ]
                    },
                    "description": {"type": "string"}
                }
            }
        },

        "action_plan": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "priority",
                    "recommendation",
                    "expected_outcome",
                    "timeframe"
                ],
                "properties": {
                    "priority": {
                        "type": "string",
                        "enum": ["HIGH", "MEDIUM", "LOW"]
                    },
                    "recommendation": {"type": "string"},
                    "expected_outcome": {"type": "string"},
                    "timeframe": {
                        "type": "string",
                        "enum": ["IMMEDIATE", "30_DAYS", "90_DAYS"]
                    }
                }
            }
        },

        "confidence_note": {"type": "string"}
    }
}
