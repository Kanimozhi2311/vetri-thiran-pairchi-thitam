from ..config import get_settings
from ..models import OutlineResponse, PanelStory, PromptRequest, StoryResponse


def _demo_story(request: PromptRequest, outline: OutlineResponse) -> StoryResponse:
    return StoryResponse(panels=[
        PanelStory(
            panel_number=panel.panel_number,
            caption=f"{request.setting.upper()} — {panel.title}",
            narration=(
                f"{request.character_name} moves through the moment with a "
                f"{request.tone} spirit. {panel.scene_description}"
            ),
            dialogue=(
                f'"We can do this," {request.character_name} says, '
                f'"one brave step at a time."'
            ),
        )
        for panel in outline.panels
    ])


def generate_story(request: PromptRequest, outline: OutlineResponse) -> StoryResponse:
    settings = get_settings()
    if settings.demo_mode:
        return _demo_story(request, outline)
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is required when DEMO_MODE=false.")

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=settings.gemini_api_key)
    prompt = f"""
Expand the following five-panel comic outline into polished comic narration and dialogue.

Character: {request.character_name}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}
Original story prompt: {request.story_prompt}

Outline:
{outline.model_dump_json(indent=2)}

Return exactly five panel story objects. For each panel provide:
- panel_number
- caption: brief ambient/cinematic caption
- narration: concise narration describing action and emotion
- dialogue: short natural dialogue, using the character name where useful

Keep the story continuous. Do not invent extra panels. Keep language family-friendly
and suitable for a general-audience comic.
""".strip()

    response = client.models.generate_content(
        model=settings.gemini_story_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=StoryResponse,
            temperature=0.95,
            max_output_tokens=3500,
        ),
    )
    if not response.text:
        raise RuntimeError("Gemini returned an empty story.")
    return StoryResponse.model_validate_json(response.text)
