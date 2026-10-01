from datetime import datetime
from pathlib import Path
import os
from fpdf import FPDF
from ..config import get_settings


def _clean_text(value: str) -> str:
    return (
        value.replace("\u2014", "-")
        .replace("\u2013", "-")
        .replace("\u2019", "'")
    )


def save_pdf(layout: list[dict], title: str) -> Path:
    settings = get_settings()
    settings.ensure_directories()
    filename = f"comic_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.pdf"
    output_path = settings.exports_dir / filename

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=12)

    for panel in layout:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        pdf.multi_cell(0, 10, _clean_text(f"Panel {panel['panel_number']}: {panel['title']}"))

        image_url = panel["image_url"]
        if image_url.startswith("/static/"):
            image_path = settings.root_dir / image_url.lstrip("/").replace("/", os.sep)
        else:
            image_path = Path(image_url)

        if image_path.exists():
            pdf.image(str(image_path), x=15, y=42, w=180, h=120)

        pdf.set_y(168)
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_x(15)
        pdf.multi_cell(180, 6, _clean_text(panel["scene_description"]))
        pdf.ln(3)

        pdf.set_x(15)
        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(180, 6, _clean_text(panel["caption"]))

        pdf.set_x(15)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(180, 6, _clean_text(panel["narration"]))
        pdf.ln(2)

        pdf.set_x(15)
        pdf.set_font("Helvetica", "I", 11)
        pdf.multi_cell(180, 6, _clean_text(panel["dialogue"]))

    pdf.output(str(output_path))
    return output_path
