import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
You are a financial analyst assistant.

Rules:
- Summarize clearly in simple language
- Focus on financial meaning
- Avoid legal disclaimers
- Max 5 bullet points
"""


def summarize_document(text: str) -> dict:
    """
    Generates a short financial summary from PDF text.
    """

    if not text or len(text.strip()) < 200:
        return {
            "summary": "Document text is too short to summarize."
        }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Summarize this document:\n{text[:4000]}",
            },
        ],
        temperature=0.2,
    )

    summary = response.choices[0].message.content.strip()

    return {
        "summary": summary
    }
