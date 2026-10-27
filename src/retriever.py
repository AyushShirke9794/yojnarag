
import json

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "intfloat/multilingual-e5-small"


class SchemeRetriever:
    def __init__(self):
        print("Loading FAISS index...")
        self.index = faiss.read_index(
            "data/vectorstore/faiss_5schemes.index"
        )

        with open(
            "data/vectorstore/metadata_5schemes.json",
            "r",
            encoding="utf-8"
        ) as file:
            metadata = json.load(file)

        self.chunks = metadata

        if self.index.d != 384:
            raise ValueError("Embedding dimension mismatch.")

        if self.index.ntotal != len(self.chunks):
            raise ValueError("FAISS index and metadata count mismatch.")

        print("Loading multilingual embedding model...")
        self.model = SentenceTransformer(MODEL_NAME)

    def search(self, query, top_k=3):
        if not query.strip():
            raise ValueError("Search query cannot be empty.")

        query_embedding = self.model.encode(
            ["query: " + query],
            convert_to_numpy=True
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype=np.float32
        )

        faiss.normalize_L2(query_embedding)

        k = min(top_k, self.index.ntotal)

        if k <= 0:
            return []

        scores, indices = self.index.search(
            query_embedding,
            k
        )

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index < 0:
                continue

            chunk = self.chunks[int(index)]

            results.append({
                "scheme_id": chunk["scheme_id"],
                "verification_status": chunk["verification_status"],
                "chunk_id": chunk["chunk_id"],
                "source_file": chunk["source_file"],
                "page_number": chunk["page_number"],
                "score": float(score),
                "text": chunk["text"]
            })

        return results


if __name__ == "__main__":
    retriever = SchemeRetriever()

    question = "Who is eligible for PM-KISAN?"

    print(f"\nQuestion: {question}")

    results = retriever.search(question, top_k=3)

    for rank, result in enumerate(results, start=1):
        print(f"\n--- Result {rank} ---")
        print(f"Similarity score: {result['score']:.4f}")
        print(f"Source: {result['source_file']}")
        print(f"Page: {result['page_number']}")
        print(f"Text: {result['text'][:600]}")
