import os
import google.generativeai as genai

def explain_decision(summary: str):
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return "Explanation unavailable"

    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-pro")
    return model.generate_content(summary).text
