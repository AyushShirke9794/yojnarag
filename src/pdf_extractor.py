
import json
from pathlib import Path

import pymupdf


def extract_pdf(pdf_path: str, output_path: str):
    pdf = pymupdf.open(pdf_path)

    pages = []

    try:
        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text("text").strip()

            if text:
                pages.append({
                    "page_number": page_number,
                    "text": text
                })
    finally:
        pdf.close()

    result = {
        "source_file": Path(pdf_path).name,
        "total_pages_extracted": len(pages),
        "pages": pages
    }

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)

    print(f"Extracted {len(pages)} pages")
    print(f"Saved to: {output}")

    return result


if __name__ == "__main__":
    extract_pdf(
        "data/raw/pm_kisan.pdf",
        "data/processed/pm_kisan_text.json"
    )
