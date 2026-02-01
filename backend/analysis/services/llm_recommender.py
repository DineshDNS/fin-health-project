import json
from django.conf import settings
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a senior SME financial advisor in India.

Rules:
- Explain recommendations clearly and conservatively
- Do NOT guarantee approvals or returns
- Do NOT invent new products
- Use simple, non-technical language
- Return STRICT JSON only
"""

def generate_llm_product_recommendations(payload, rule_products):
    """
    payload: structured financial + risk data
    rule_products: list of products from rule engine
    """

    if not rule_products:
        return []

    user_prompt = f"""
Based on the following SME financial assessment data,
generate up to {len(rule_products)} product recommendations.

Only explain the products already provided.
Do NOT add new products.

For each product return:
- name
- provider
- reason (1–2 sentences)
- suitability ("High", "Medium", or "Low")

Data:
{json.dumps(payload, indent=2)}

Products:
{json.dumps(rule_products, indent=2)}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )

        content = response.choices[0].message.content
        parsed = json.loads(content)

        # Hard validation
        validated = []
        for item in parsed:
            validated.append({
                "name": item["name"],
                "provider": item["provider"],
                "reason": item["reason"],
                "suitability": item["suitability"],
            })

        return validated

    except Exception as e:
        # FAIL SAFE → fallback to rule-based
        print("LLM ERROR:", str(e))
        return [
            {
                "name": p["name"],
                "provider": p["provider"],
                "reason": p.get("reason", "Recommended based on financial assessment."),
                "suitability": "Medium",
            }
            for p in rule_products
        ]
