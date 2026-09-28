import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = os.getenv("GEMINI_PRO_MODEL", os.getenv("GEMINI_MODEL", "gemini-1.5-pro"))
model = genai.GenerativeModel(MODEL_NAME)

def generate_story(outline: list) -> str:
    formatted = "\n".join(f"{i+1}. {item}" for i, item in enumerate(outline))
    prompt = f"""You are a comic book writer.
Write a comic-style story with narration and character dialogue for every panel.

Panel Outline:
{formatted}

Guidelines:
- Use an engaging comic-book tone.
- Include narration and clearly marked dialogue.
- Keep every panel self-contained.
- Label sections as **Panel 1**, **Panel 2**, etc.
"""
    response = model.generate_content(prompt)
    return response.text
