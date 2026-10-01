# ComicCraft — AI Comic Story Creator

A complete FastAPI + Jinja2 application implementing the supplied ComicCraft specification: five-panel outline generation, story/dialogue generation, image generation, panel layout, PDF export, browser UI, and JSON APIs.

## Quick start

```powershell
cd ComicCraft
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 and API docs at http://127.0.0.1:8000/docs.

For a no-key smoke test, leave `DEMO_MODE=true` and `IMAGE_PROVIDER=demo`.

## Real AI

Set `DEMO_MODE=false` and add `GEMINI_API_KEY`. Gemini model IDs are configurable; the defaults use `gemini-2.5-flash` and `gemini-2.5-pro`.

For images choose either:

```env
IMAGE_PROVIDER=local
```

for local Diffusers (GPU recommended), or:

```env
IMAGE_PROVIDER=huggingface
HF_TOKEN=your_token
```

for Hugging Face hosted inference.

## Tests

```powershell
pytest -q
```

The tests use demo mode and do not require paid AI services.

## Structure

```text
ComicCraft/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   └── services/
│       ├── __init__.py
│       ├── exporters.py
│       ├── gemini_flash.py
│       ├── gemini_pro.py
│       ├── image_generator.py
│       ├── layout_builder.py
│       └── pipeline.py
├── static/
│   ├── css/style.css
│   ├── js/app.js
│   ├── panels/.gitkeep
│   └── exports/.gitkeep
├── templates/
│   ├── comic_preview.html
│   ├── export_success.html
│   └── index.html
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   └── test_services.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

The supplied documentation names Gemini 1.5 Flash/Pro and `runwayml/stable-diffusion-v1-5`. This implementation preserves that architecture but makes model IDs configurable and uses the current Google GenAI SDK.
