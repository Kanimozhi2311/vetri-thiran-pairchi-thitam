import hashlib
import re
from pathlib import Path
from PIL import Image, ImageDraw

from ..config import get_settings


def _safe_filename(prompt: str, panel_number: int) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", prompt.lower()).strip("-")[:45] or "panel"
    digest = hashlib.sha1(prompt.encode("utf-8")).hexdigest()[:10]
    return f"panel-{panel_number}-{slug}-{digest}.png"


def _demo_image(prompt: str, output_path: Path) -> None:
    settings = get_settings()
    image = Image.new("RGB", (settings.image_width, settings.image_height), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle(
        (12, 12, settings.image_width - 12, settings.image_height - 12),
        outline="black", width=5
    )
    draw.text((35, 35), "COMICCRAFT DEMO", fill="black")
    wrapped = "\n".join(
        prompt[i:i + 48] for i in range(0, min(len(prompt), 280), 48)
    )
    draw.text((35, 95), wrapped, fill="black", spacing=8)
    draw.text(
        (35, settings.image_height - 60),
        "Set IMAGE_PROVIDER to a real provider for AI images.",
        fill="black"
    )
    image.save(output_path)


def _local_diffusers(prompt: str, output_path: Path) -> None:
    import torch
    from diffusers import StableDiffusionPipeline

    settings = get_settings()
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    pipe = StableDiffusionPipeline.from_pretrained(
        settings.local_image_model, torch_dtype=dtype
    )
    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    image = pipe(
        prompt=prompt,
        negative_prompt="blurry, low quality, distorted anatomy, text, watermark, logo",
        width=settings.image_width, height=settings.image_height,
        num_inference_steps=settings.image_steps,
        guidance_scale=settings.image_guidance,
    ).images[0]
    image.save(output_path)


def _huggingface(prompt: str, output_path: Path) -> None:
    from huggingface_hub import InferenceClient

    settings = get_settings()
    if not settings.hf_token:
        raise RuntimeError("HF_TOKEN is required for IMAGE_PROVIDER=huggingface.")
    client = InferenceClient(model=settings.hf_image_model, token=settings.hf_token)
    image = client.text_to_image(prompt)
    image.save(output_path)


def generate_image(prompt: str, panel_number: int) -> Path:
    settings = get_settings()
    settings.ensure_directories()
    output_path = settings.panels_dir / _safe_filename(prompt, panel_number)

    if settings.demo_mode or settings.image_provider == "demo":
        _demo_image(prompt, output_path)
    elif settings.image_provider == "local":
        _local_diffusers(prompt, output_path)
    elif settings.image_provider == "huggingface":
        _huggingface(prompt, output_path)
    else:
        raise ValueError("IMAGE_PROVIDER must be one of: demo, local, huggingface.")
    return output_path
