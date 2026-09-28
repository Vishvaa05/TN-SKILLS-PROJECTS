def build_comic_layout(image_paths, full_story, outline):
    story_panels = [p for p in full_story.split("**Panel") if p.strip()]
    layout = []
    for idx, (image, text, panel_info) in enumerate(
        zip(image_paths, story_panels, outline), start=1
    ):
        lines = text.strip().splitlines()
        if lines and lines[0].strip().startswith(str(idx)):
            lines = lines[1:]
        layout.append({
            "panel": idx,
            "title": panel_info.get("title", f"Panel {idx}"),
            "image_path": image,
            "text": "\n".join(lines).strip(),
            "scene_description": panel_info.get("scene_description", ""),
        })
    return layout
