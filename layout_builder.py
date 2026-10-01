from typing import Any
from ..models import OutlineResponse, StoryResponse


def build_comic_layout(
    outline: OutlineResponse,
    story: StoryResponse,
    image_paths: list[str],
) -> list[dict[str, Any]]:
    story_by_number = {item.panel_number: item for item in story.panels}
    layout = []

    for index, panel in enumerate(outline.panels):
        panel_story = story_by_number.get(panel.panel_number)
        if panel_story is None:
            raise ValueError(f"Missing story for panel {panel.panel_number}.")
        if index >= len(image_paths):
            raise ValueError(f"Missing image for panel {panel.panel_number}.")
        layout.append({
            "panel_number": panel.panel_number,
            "title": panel.title,
            "scene_description": panel.scene_description,
            "image_prompt": panel.image_prompt,
            "image_url": image_paths[index],
            "caption": panel_story.caption,
            "narration": panel_story.narration,
            "dialogue": panel_story.dialogue,
        })
    return layout
