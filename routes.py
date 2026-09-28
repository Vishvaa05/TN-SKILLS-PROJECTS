from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
)

from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
)

from fastapi.templating import (
    Jinja2Templates,
)

from app.config import TEMPLATES_DIR

from app.models import (
    PromptRequest,
)

from app.services.comic_service import (
    generate_comic,
)

from app.services.image_generator import (
    generate_image,
)


# ---------------------------------------------------------
# Router
# ---------------------------------------------------------

router = APIRouter()


# ---------------------------------------------------------
# Templates
# ---------------------------------------------------------

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


# ---------------------------------------------------------
# Homepage
# ---------------------------------------------------------

@router.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )


# ---------------------------------------------------------
# HTML comic generation
# ---------------------------------------------------------

@router.post(
    "/generate",
    response_class=HTMLResponse,
)
async def generate_form(
    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...),

    panels: int = Form(5),
):

    form_data = {
        "story_prompt": story_prompt,
        "character_name": character_name,
        "setting": setting,
        "tone": tone,
        "art_style": art_style,
        "panels": panels,
    }

    try:

        result = generate_comic(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
            panels=panels,
        )

        return templates.TemplateResponse(
            "comic_preview.html",
            {
                "request": request,
                **result,
            },
        )

    except Exception as exc:

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": str(exc),
                "form": form_data,
            },
            status_code=500,
        )


# ---------------------------------------------------------
# JSON API
# ---------------------------------------------------------

@router.post(
    "/generate-comic/json"
)
async def generate_json(
    payload: PromptRequest,
):

    try:

        result = generate_comic(
            **payload.model_dump()
        )

        return JSONResponse(
            content=result
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# ---------------------------------------------------------
# Image testing endpoint
# ---------------------------------------------------------

@router.post(
    "/test-image"
)
async def test_image(
    prompt: str = Form(...),
):

    try:

        image_url = generate_image(
            prompt,
            0,
        )

        return {
            "image_url": image_url
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# ---------------------------------------------------------
# Export success page
# ---------------------------------------------------------

@router.get(
    "/export-success",
    response_class=HTMLResponse,
)
async def export_success(
    request: Request,
    pdf_url: str = "",
):

    return templates.TemplateResponse(
        "export_success.html",
        {
            "request": request,
            "pdf_url": pdf_url,
        },
    )