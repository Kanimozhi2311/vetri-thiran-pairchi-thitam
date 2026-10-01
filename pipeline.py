from .exporters import save_pdf
from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from ..models import ComicResponse, PromptRequest


def generate_comic(request: PromptRequest) -> ComicResponse:
    outline = generate_outline(request)
    if len(outline.panels) != 5:
        raise RuntimeError(
            f"The outline service returned {len(outline.panels)} panels; exactly 5 are required."
        )

    story = generate_story(request, outline)
    image_paths = [
        generate_image(panel.image_prompt, panel.panel_number)
        for panel in outline.panels
    ]
    image_urls = [f"/static/panels/{path.name}" for path in image_paths]
    layout = build_comic_layout(outline, story, image_urls)

    title = f"{request.character_name}: {outline.panels[0].title}"
    pdf_path = save_pdf(layout, title)

    return ComicResponse(
        title=title, panels=layout, pdf_url=f"/download/{pdf_path.name}"
    )
