import google.generativeai as genai
import os
from dotenv import load_dotenv
import json 

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-flash-latest")

def generate_summary(transcript):

    prompt = f"""
    Return ONLY JSON.

    Format:

    {{
      "summary": "...",
      "key_concepts": [
          "...",
          "..."
      ],
      "takeaways": [
          "...",
          "..."
      ]
    }}

    Transcript:

    {transcript}
    """

    response = model.generate_content(prompt)

    clean_text = response.text.strip()

    if clean_text.startswith("```json"):
        clean_text = clean_text.replace("```json", "")
        clean_text = clean_text.replace("```", "")

    return json.loads(clean_text)