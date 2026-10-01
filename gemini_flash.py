from ..config import get_settings
from ..models import OutlineResponse, PromptRequest


def _demo_outline(request: PromptRequest) -> OutlineResponse:
    beats = [
        ("The Spark", f"{request.character_name} discovers a strange clue in {request.setting}."),
        ("Into the Unknown", f"{request.character_name} follows the clue deeper into {request.setting}."),
        ("The Turning Point", f"A surprising obstacle forces {request.character_name} to rethink the plan."),
        ("The Brave Choice", f"{request.character_name} makes a courageous choice that changes everything."),
        ("A New Beginning", f"The mystery is resolved, leaving {request.character_name} with a memorable lesson."),
    ]
    return OutlineResponse(panels=[
        {
            "panel_number": i, "title": title, "scene_description": desc,
            "image_prompt": (
                f"{request.art_style} comic illustration, {request.tone} mood, "
                f"{request.character_name} in {request.setting}, {desc} "
                "cinematic composition, expressive character, clean comic linework, "
                "no text, no speech bubbles"
            ),
        }
        for i, (title, desc) in enumerate(beats, 1)
    ])


def generate_outline(request: PromptRequest) -> OutlineResponse:
    settings = get_settings()
    if settings.demo_mode:
        return _demo_outline(request)
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is required when DEMO_MODE=false.")

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=settings.gemini_api_key)
    prompt = f"""
Create a coherent five-panel comic outline.

User story prompt: {request.story_prompt}
Main character: {request.character_name}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}

Return exactly five panels. Each panel must contain:
- panel_number: 1 through 5
- title: short panel title
- scene_description: vivid but concise scene description
- image_prompt: detailed image-generation prompt matching the same character,
  setting, tone, and art style. Do not request readable text in the image.

Maintain continuity between panels and make the final panel resolve or meaningfully
advance the story.
""".strip()

    response = client.models.generate_content(
        model=settings.gemini_outline_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=OutlineResponse,
            temperature=0.9,
            max_output_tokens=2500,
        ),
    )
    if not response.text:
        raise RuntimeError("Gemini returned an empty outline.")
    return OutlineResponse.model_validate_json(response.text)
