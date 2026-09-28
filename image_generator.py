import os
import re
from pathlib import Path
from dotenv import load_dotenv
from diffusers import StableDiffusionPipeline
import torch

load_dotenv()
MODEL_ID = os.getenv("HF_MODEL", "runwayml/stable-diffusion-v1-5")
OUTPUT_DIR = Path("static/panels")
_pipe = None

def _get_pipe():
    global _pipe
    if _pipe is None:
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        _pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=dtype)
        _pipe = _pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    return _pipe

def sanitize_filename(text: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9_-]+", "_", text).strip("_")
    return (name[:80] or "panel") + ".png"

def generate_image(prompt: str, filename: str | None = None) -> str:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filename = filename or sanitize_filename(prompt)
    image = _get_pipe()(prompt).images[0]
    path = OUTPUT_DIR / filename
    image.save(path)
    return str(path)
