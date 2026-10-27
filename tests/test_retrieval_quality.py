
from src.hybrid_retriever import HybridRetriever


TEST_QUESTIONS = [
    "Who is eligible for PM-KISAN?",
    "What financial benefits are provided under PM-KISAN?",
    "Which categories of farmers are excluded from PM-KISAN?",
    "How are PM-KISAN beneficiaries identified?",
    "What happens when agricultural land is inherited?"
]


def main():
    retriever = HybridRetriever()

    for number, question in enumerate(TEST_QUESTIONS, start=1):
        print("\n" + "=" * 65)
        print(f"QUESTION {number}: {question}")
        print("=" * 65)

        results = retriever.search(question, top_k=3)

        for rank, result in enumerate(results, start=1):
            print(f"\nResult {rank}")
            print(f"Page: {result['page_number']}")
            print(f"RRF Score: {result['rrf_score']:.5f}")
            print(f"Methods: {', '.join(result['retrieved_by'])}")
            print(f"Text: {result['text'][:350]}")


if __name__ == "__main__":
    main()
