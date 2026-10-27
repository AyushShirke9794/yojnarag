
import json
import re

from rank_bm25 import BM25Okapi


class BM25Retriever:
    def __init__(self):
        with open(
            "data/vectorstore/metadata_5schemes.json",
            "r",
            encoding="utf-8"
        ) as file:
            metadata = json.load(file)

        self.chunks = metadata

        tokenized_corpus = [
            self.tokenize(chunk["text"])
            for chunk in self.chunks
        ]

        self.bm25 = BM25Okapi(tokenized_corpus)

    @staticmethod
    def tokenize(text):
        return re.findall(r"\w+", text.lower(), flags=re.UNICODE)

    def search(self, query, top_k=3):
        if not query.strip():
            raise ValueError("Search query cannot be empty.")

        if top_k <= 0:
            return []

        query_tokens = self.tokenize(query)
        scores = self.bm25.get_scores(query_tokens)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        results = []

        for index in ranked_indices:
            chunk = self.chunks[index]

            results.append({
                "scheme_id": chunk["scheme_id"],
                "verification_status": chunk["verification_status"],
                "chunk_id": chunk["chunk_id"],
                "source_file": chunk["source_file"],
                "page_number": chunk["page_number"],
                "score": float(scores[index]),
                "text": chunk["text"]
            })

        return results


if __name__ == "__main__":
    retriever = BM25Retriever()

    question = "Who is eligible for PM-KISAN?"

    print(f"\nQuestion: {question}")

    results = retriever.search(question, top_k=3)

    for rank, result in enumerate(results, start=1):
        print(f"\n--- Result {rank} ---")
        print(f"BM25 score: {result['score']:.4f}")
        print(f"Source: {result['source_file']}")
        print(f"Page: {result['page_number']}")
        print(f"Text: {result['text'][:600]}")
