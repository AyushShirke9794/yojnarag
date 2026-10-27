
from sentence_transformers import CrossEncoder

from src.hybrid_retriever import HybridRetriever


RERANKER_MODEL = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"


class RerankedRetriever:
    def __init__(self):
        print("Loading hybrid retriever...")
        self.hybrid = HybridRetriever()

        print("Loading cross-encoder reranker...")
        self.reranker = CrossEncoder(RERANKER_MODEL)

    def search(self, query, top_k=3, candidate_k=30):
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if top_k <= 0 or candidate_k <= 0:
            raise ValueError("top_k and candidate_k must be positive.")

        candidates = self.hybrid.search(
            query,
            top_k=max(top_k, candidate_k),
            candidate_k=max(top_k, candidate_k)
        )

        if not candidates:
            return []

        pairs = [
            (query, candidate["text"])
            for candidate in candidates
        ]

        scores = self.reranker.predict(pairs)

        for candidate, score in zip(candidates, scores):
            candidate["rerank_score"] = float(score)
        
        ranked = sorted(
            candidates,
            key=lambda item: item["rerank_score"],
            reverse=True
        )

        final_results = []

        for item in ranked[:top_k]:
            final_results.append({
                **item,
                "source_title": (
                    "PM-KISAN Operational Guidelines"
                ),
                "source_revision_date": "2020-03-29",
                "source_status": "historical_unverified_current",
                "citation": (
                    f"{item['source_file']}, "
                    f"page {item['page_number']}"
                )
            })

        return final_results


if __name__ == "__main__":
    retriever = RerankedRetriever()

    questions = [
        "Who is eligible for PM-KISAN?",
        "What financial benefits are provided under PM-KISAN?",
        "Which categories of farmers are excluded from PM-KISAN?",
        "How are PM-KISAN beneficiaries identified?",
        "What happens when agricultural land is inherited?"
    ]

    for question in questions:
        print("\n" + "=" * 65)
        print("QUESTION:", question)

        results = retriever.search(question, top_k=3)

        for rank, result in enumerate(results, start=1):
            print(f"\nResult {rank}")
            print("Page:", result["page_number"])
            print("Rerank score:", round(result["rerank_score"], 4))
            print("Text:", result["text"][:450])
