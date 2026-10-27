
import json
import re
from pathlib import Path


def clean_text(text):
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_into_chunks(text, chunk_size=800, overlap=150):
    if chunk_size <= 0 or not 0 <= overlap < chunk_size:
        raise ValueError("Require chunk_size > overlap >= 0")

    text = clean_text(text)

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        if end < len(text):
            # Prefer a paragraph or sentence boundary.
            candidates = [
                text.rfind("\n\n", start + 1, end),
                text.rfind(". ", start + 1, end),
                text.rfind(" ", start + 1, end)
            ]

            boundary = next(
                (
                    position for position in candidates
                    if position > start + chunk_size // 2
                ),
                -1
            )

            if boundary != -1:
                end = boundary + 1

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = max(start + 1, end - overlap)

    return chunks


def chunk_document(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as file:
        document = json.load(file)

    chunks = []
    chunk_id = 0

    for page in document["pages"]:
        page_chunks = split_into_chunks(page["text"])

        for content in page_chunks:
            chunks.append({
                "chunk_id": f"pm_kisan_{chunk_id:04d}",
                "source_file": document["source_file"],
                "page_number": page["page_number"],
                "text": content
            })

            chunk_id += 1

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8") as file:
        json.dump(chunks, file, indent=2, ensure_ascii=False)

    print(f"Created {len(chunks)} improved text chunks")
    print(f"Saved to: {output}")


if __name__ == "__main__":
    chunk_document(
        "data/processed/pm_kisan_text.json",
        "data/processed/pm_kisan_chunks.json"
    )
