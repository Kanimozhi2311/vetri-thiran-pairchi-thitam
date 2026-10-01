from app.models import PromptRequest
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.layout_builder import build_comic_layout


def request():
    return PromptRequest(
        story_prompt="A brave fox explores an enchanted forest.",
        character_name="Lumi", setting="forest",
        tone="dramatic", art_style="anime"
    )


def test_demo_outline_has_five_panels():
    outline = generate_outline(request())
    assert len(outline.panels) == 5
    assert outline.panels[0].panel_number == 1
    assert outline.panels[-1].panel_number == 5


def test_demo_story_matches_outline():
    outline = generate_outline(request())
    story = generate_story(request(), outline)
    assert len(story.panels) == 5
    assert [p.panel_number for p in story.panels] == [1, 2, 3, 4, 5]


def test_layout_joins_images_and_story():
    outline = generate_outline(request())
    story = generate_story(request(), outline)
    images = [f"/static/panels/panel-{i}.png" for i in range(1, 6)]
    layout = build_comic_layout(outline, story, images)
    assert len(layout) == 5
    assert layout[2]["image_url"] == "/static/panels/panel-3.png"
    assert layout[2]["dialogue"]
