from groq import Groq
from dotenv import load_dotenv
load_dotenv()

import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_explanation(error, context, code=""):
    prompt = f"""
You are an expert compiler error assistant.

Analyze the error and code.

Error:
{error}

Code:
{code}

Context:
{context}

Give:
1. Clear explanation (simple)
2. Exact fix

Format:
Explanation:
Fix:
"""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # 🔥 best Groq model
            messages=[
                {"role": "system", "content": "You are a helpful programming assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        text = response.choices[0].message.content

        # Basic parsing
        explanation, fix, corrected = "", "", ""

        if "Fix:" in text:
            parts = text.split("Fix:")
            explanation = parts[0].replace("Explanation:", "").strip()
            rest = parts[1]

            if "Corrected Code:" in rest:
                fix, corrected = rest.split("Corrected Code:")
            else:
                fix = rest

        return explanation.strip(), fix.strip()

    except Exception as e:
        return "API Error", str(e), ""