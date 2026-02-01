import json
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_llm_product_recommendations(payload, rule_products):
    # 🚫 LLM disabled OR no key → fallback immediately
    if not settings.USE_LLM_RECOMMENDATIONS or not settings.OPENAI_API_KEY:
        return [
            {
                "name": p["name"],
                "provider": p["provider"],
                "reason": "Recommended based on your current financial risk profile.",
                "suitability": "Medium",
            }
            for p in rule_products
        ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a conservative SME financial advisor in India. Return only JSON."
                },
                {
                    "role": "user",
                    "content": json.dumps({
                        "payload": payload,
                        "products": rule_products
                    })
                }
            ],
            temperature=0.2,
        )

        content = response["choices"][0]["message"]["content"]
        return json.loads(content)

    except Exception as e:
        # Quota, timeout, any error → graceful fallback
        return [
            {
                "name": p["name"],
                "provider": p["provider"],
                "reason": "Recommended based on your current financial risk profile.",
                "suitability": "Medium",
            }
            for p in rule_products
        ]
