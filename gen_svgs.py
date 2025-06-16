import subprocess
import os

def convert_pdf_to_svg_inkscape(pdf_path, svg_path, page=1):
    try:
        subprocess.run([
            "inkscape.com",
            f"--pages={page}",
            "--export-type=svg",
            f"--export-filename={svg_path}",
            pdf_path
        ], check=True, capture_output=True, text=True)
        print(f"✅ Page {page} exported as SVG to {svg_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error converting page {page}: {e}")

# Example usage

folder = "C:/Repositories/CLIE"

pdf_path = f"{folder}/malla_EM.pdf"

for pag in range(1,5):
    svg_path = f"{folder}/malla_EM_{pag}.svg"    
    convert_pdf_to_svg_inkscape(pdf_path, svg_path, page=pag)