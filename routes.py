from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from .config import get_settings
from .models import PromptRequest
from .services.image_generator import generate_image
from .services.pipeline import generate_comic


router = APIRouter()
templates = Jinja2Templates(directory="templates")
settings = get_settings()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html",
        context={"app_name": settings.app_name}
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    payload = PromptRequest(
        story_prompt=story_prompt, character_name=character_name,
        setting=setting, tone=tone, art_style=art_style
    )
    try:
        comic = generate_comic(payload)
    except Exception as exc:
        return templates.TemplateResponse(
            request=request, name="index.html",
            context={
                "app_name": settings.app_name,
                "error": str(exc),
                "form": payload.model_dump(),
            },
            status_code=500,
        )
    return templates.TemplateResponse(
        request=request, name="comic_preview.html",
        context={"app_name": settings.app_name, "comic": comic.model_dump()},
    )


@router.post("/generate-comic/json")
async def generate_comic_json(payload: PromptRequest):
    try:
        return JSONResponse(content=generate_comic(payload).model_dump())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/test-image")
async def test_image(prompt: str = Form(...)):
    if not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
    try:
        path = generate_image(prompt.strip(), panel_number=0)
        return {"image_url": f"/static/panels/{path.name}", "path": str(path)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, filename: str = ""):
    return templates.TemplateResponse(
        request=request, name="export_success.html",
        context={"app_name": settings.app_name, "filename": filename}
    )


@router.get("/download/{filename}", name="download_pdf")
async def download_pdf(filename: str):
    safe_name = filename.replace("/", "").replace("\\", "")
    pdf_path = settings.exports_dir / safe_name
    if not pdf_path.exists() or pdf_path.suffix.lower() != ".pdf":
        raise HTTPException(status_code=404, detail="PDF not found.")
    return FileResponse(
        path=pdf_path, media_type="application/pdf", filename=pdf_path.name
    )
