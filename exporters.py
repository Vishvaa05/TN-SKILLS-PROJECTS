import os
from datetime import datetime
from pathlib import Path
from fpdf import FPDF

EXPORT_FOLDER = Path("static/exports")

def save_pdf(layout):
    EXPORT_FOLDER.mkdir(parents=True, exist_ok=True)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()
        pdf.set_font("Helvetica", "", 14)
        pdf.cell(0, 10, f"Panel {panel['panel']}: {panel.get('title', '')}",
                 ln=True, align="C")

        image_path = panel["image_path"]
        if os.path.exists(image_path):
            pdf.image(image_path, x=10, y=30, w=pdf.w - 20, h=100)
        else:
            pdf.set_y(30)
            pdf.multi_cell(0, 10, f"Image missing: {image_path}")

        pdf.set_y(145)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, panel.get("text", "") or panel.get("scene_description", ""))

    filename = f"comic_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    path = EXPORT_FOLDER / filename
    pdf.output(str(path))
    return str(path)
