from app.config import settings
from app.models import PanelOutline


def get_gemini_client():

    from google import genai

    if not settings.gemini_api_key:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Add it to your .env file."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_outline(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
    panels: int = 5,
) -> list[PanelOutline]:

    from google.genai import types

    client = get_gemini_client()

    prompt = f"""
You are an expert comic book story planner.

Create a coherent {panels}-panel comic outline.

USER STORY IDEA:
{story_prompt}

MAIN CHARACTER:
{character_name}

SETTING:
{setting}

TONE:
{tone}

ART STYLE:
{art_style}

Requirements:

1. Return exactly {panels} panels.
2. The story must have a clear beginning, middle and ending.
3. Keep the main character visually consistent.
4. Each panel must advance the story.
5. Give every panel a short title.
6. Give every panel a scene description.
7. Give every panel a detailed image generation prompt.
8. The image prompt must describe only the visual scene.
9. Do not put speech bubbles or written text inside image prompts.
10. Keep the requested art style consistent.
"""

    response = client.models.generate_content(
        model=settings.gemini_outline_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.9,
            response_mime_type="application/json",
            response_schema=list[PanelOutline],
        ),
    )

    if not response.parsed:

        raise RuntimeError(
            "Gemini did not return a valid comic outline."
        )

    return [
        PanelOutline.model_validate(panel)
        for panel in response.parsed
    ]