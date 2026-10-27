
import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "intfloat/multilingual-e5-small"


def build_vector_index():
    chunks_path = Path("data/processed/pm_kisan_chunks.json")
    index_path = Path("data/vectorstore/faiss.index")
    metadata_path = Path("data/vectorstore/metadata.json")

    with chunks_path.open("r", encoding="utf-8") as file:
        chunks = json.load(file)

    if not chunks:
        raise ValueError("No text chunks found.")

    print("Loading multilingual embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    # E5 expects the 'passage:' prefix for documents.
    texts = ["passage: " + chunk["text"] for chunk in chunks]

    print("Generating embeddings...")
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    embeddings = np.asarray(embeddings, dtype=np.float32)

    # Normalize for cosine similarity using inner product.
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    index_path.parent.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(index_path))

    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(
            {
                "embedding_model": MODEL_NAME,
                "chunks": chunks
            },
            file,
            indent=2,
            ensure_ascii=False
        )

    print(f"FAISS index created: {index.ntotal} vectors")
    print(f"Embedding dimensions: {dimension}")
    print(f"Saved index to: {index_path}")


if __name__ == "__main__":
    build_vector_index()
