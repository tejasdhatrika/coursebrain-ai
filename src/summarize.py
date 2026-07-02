import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_summary(transcript):

    prompt = f"""
    You are an expert educational assistant.

    Create:

    1. Lecture Summary
    2. Key Concepts
    3. Important Takeaways

    Transcript:

    {transcript}
    """

    response = model.generate_content(prompt)

    return response.text