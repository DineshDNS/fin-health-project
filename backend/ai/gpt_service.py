from openai import OpenAI
from .prompts import financial_insight_prompt
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_financial_insights(data, language="en"):
    prompt = financial_insight_prompt(data, language)

    response = client.responses.create(
        model="gpt-5",
        input=prompt,
    )

    return response.output_text
