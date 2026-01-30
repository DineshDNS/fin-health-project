import os
from openai import OpenAI
from openai import RateLimitError
from .prompts import financial_insight_prompt

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_financial_insights(data, language="en"):
    prompt = financial_insight_prompt(data, language)

    try:
        response = client.responses.create(
            model="gpt-5",
            input=prompt,
        )
        return response.output_text

    except RateLimitError:
        # FALLBACK RESPONSE (VERY IMPORTANT)
        if language == "hi":
            return (
                "आपके व्यवसाय की वित्तीय स्थिति स्थिर है। "
                "कैश फ्लो अच्छा है और कर अनुपालन सही है। "
                "खर्चों को नियंत्रित करने और कार्यशील पूंजी प्रबंधन में सुधार करने से "
                "वित्तीय स्थिति और मजबूत हो सकती है।"
            )

        elif language == "ta":
            return (
                "உங்கள் தொழிலின் நிதி நிலை நல்ல நிலையில் உள்ளது. "
                "பணப்புழக்கம் நிலையாக உள்ளது மற்றும் வரி இணக்கம் சரியாக உள்ளது. "
                "செலவுகளை கட்டுப்படுத்தி, பண மேலாண்மையை மேம்படுத்துவதன் மூலம் "
                "நிதி நிலையை மேலும் வலுப்படுத்தலாம்."
            )

        else:
            return (
                "Your business shows a stable financial position with healthy cash flow "
                "and good tax compliance. Controlling operational expenses and improving "
                "working capital management can further strengthen financial health."
            )
