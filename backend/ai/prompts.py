def financial_insight_prompt(data, language="en"):

    if language == "hi":
        return f"""
आप एक वित्तीय सलाहकार हैं जो छोटे और मध्यम व्यवसायों के लिए सरल भाषा में सलाह देता है।

वित्तीय स्कोर: {data['score']} / 100
जोखिम स्तर: {data['risk_level']}

मुख्य वित्तीय संकेतक:
- लाभ मार्जिन: {data['features']['profit_margin']}
- कैश फ्लो अनुपात: {data['features']['cash_flow_ratio']}
- EMI अनुपात: {data['features']['emi_ratio']}
- टैक्स अनुपालन: {data['features']['tax_compliance']}
- तरलता अनुपात: {data['features']['liquidity_ratio']}

कृपया:
1. व्यवसाय की वित्तीय स्थिति समझाएँ
2. प्रमुख जोखिम बताएं
3. 3 व्यावहारिक सुधार सुझाव दें
4. सरल भाषा का प्रयोग करें
"""

    elif language == "ta":
        return f"""
நீங்கள் சிறு மற்றும் நடுத்தர தொழில்களுக்கு எளிய மொழியில் ஆலோசனை வழங்கும் நிதி ஆலோசகர்.

நிதி ஆரோக்கிய மதிப்பெண்: {data['score']} / 100
ஆபத்து நிலை: {data['risk_level']}

முக்கிய நிதி அளவுகோல்கள்:
- லாப விகிதம்: {data['features']['profit_margin']}
- பணப்புழக்க விகிதம்: {data['features']['cash_flow_ratio']}
- EMI விகிதம்: {data['features']['emi_ratio']}
- வரி இணக்கம்: {data['features']['tax_compliance']}
- திரவத்தன்மை விகிதம்: {data['features']['liquidity_ratio']}

தயவுசெய்து:
1. தொழிலின் நிதி நிலையை விளக்கவும்
2. முக்கிய ஆபத்துகளை குறிப்பிடவும்
3. 3 நடைமுறை முன்னேற்ற ஆலோசனைகள் வழங்கவும்
4. எளிய, தொழில்நுட்பமற்ற மொழியை பயன்படுத்தவும்
"""

    else:
        return f"""
You are a financial advisor for small and medium enterprises.

Financial Health Score: {data['score']} / 100
Risk Level: {data['risk_level']}

Key Metrics:
- Profit Margin: {data['features']['profit_margin']}
- Cash Flow Ratio: {data['features']['cash_flow_ratio']}
- EMI Ratio: {data['features']['emi_ratio']}
- Tax Compliance: {data['features']['tax_compliance']}
- Liquidity Ratio: {data['features']['liquidity_ratio']}

Please:
1. Explain the financial health clearly
2. Highlight key risks
3. Give 3 actionable improvement suggestions
4. Use simple, non-technical language
"""
