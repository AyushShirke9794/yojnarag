
from src.retriever import SchemeRetriever
from src.bm25_retriever import BM25Retriever


class HybridRetriever:
    def __init__(self):
        print("Initializing hybrid retrieval system...")
        self.semantic = SchemeRetriever()
        self.keyword = BM25Retriever()

    def search(self, query, top_k=3, candidate_k=10, rrf_k=60):
        if not query.strip():
            raise ValueError("Search query cannot be empty.")

        if top_k <= 0 or candidate_k <= 0 or rrf_k <= 0:
            raise ValueError("Ranking parameters must be positive.")

        candidate_k = max(candidate_k, top_k)

        semantic_results = self.semantic.search(
            query, top_k=candidate_k
        )

        keyword_results = self.keyword.search(
            query, top_k=candidate_k
        )

        fused_scores = {}
        documents = {}
        retrieval_sources = {}

        for method, results in [
            ("FAISS", semantic_results),
            ("BM25", keyword_results)
        ]:
            for rank, result in enumerate(results, start=1):
                chunk_id = result["chunk_id"]

                fused_scores[chunk_id] = (
                    fused_scores.get(chunk_id, 0.0)
                    + 1.0 / (rrf_k + rank)
                )

                documents[chunk_id] = result
                retrieval_sources.setdefault(
                    chunk_id, []
                ).append(method)

        ranked_ids = sorted(
            fused_scores,
            key=lambda chunk_id: fused_scores[chunk_id],
            reverse=True
        )[:top_k]

        return [
            {
                "chunk_id": chunk_id,
                "source_file": documents[chunk_id]["source_file"],
                "page_number": documents[chunk_id]["page_number"],
                "scheme_id": documents[chunk_id]["scheme_id"],
                "verification_status": documents[chunk_id]["verification_status"],
                "rrf_score": fused_scores[chunk_id],
                "retrieved_by": retrieval_sources[chunk_id],
                "text": documents[chunk_id]["text"]
            }
            for chunk_id in ranked_ids
        ]


if __name__ == "__main__":
    retriever = HybridRetriever()

    question = "Who is eligible for PM-KISAN?"

    print(f"\nQuestion: {question}")

    results = retriever.search(question, top_k=5)

    for rank, result in enumerate(results, start=1):
        print(f"\n--- Hybrid Result {rank} ---")
        print(f"RRF score: {result['rrf_score']:.5f}")
        print(f"Retrieved by: {', '.join(result['retrieved_by'])}")
        print(f"Source: {result['source_file']}")
        print(f"Page: {result['page_number']}")
        print(f"Text: {result['text'][:600]}")
