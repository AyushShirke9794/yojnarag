from src.rag_engine import YojanaRAG


questions = [
    "Who is eligible for PM-KISAN?",
    "What financial benefits are provided under PM-KISAN?",
    "Which categories of farmers are excluded from PM-KISAN?",
    "How are PM-KISAN beneficiaries identified?",
    "What happens when agricultural land is inherited?"
]


def main():
    rag = YojanaRAG()

    try:
        for index, question in enumerate(questions, start=1):
            print("\n" + "=" * 75)
            print(f"QUESTION {index}: {question}")
            print("=" * 75)

            answer = rag.answer(question)
            print("\n" + answer)

    finally:
        rag.close()


if __name__ == "__main__":
    main()
