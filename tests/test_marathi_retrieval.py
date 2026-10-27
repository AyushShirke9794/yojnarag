from src.rag_engine import YojanaRAG

question = (
    "\u092a\u0940\u090f\u092e-\u0915\u093f\u0938\u093e\u0928 "
    "\u092f\u094b\u091c\u0928\u0947\u0905\u0902\u0924\u0930\u094d\u0917\u0924 "
    "\u0936\u0947\u0924\u0915\u0931\u094d\u092f\u093e\u0902\u0928\u093e "
    "\u0915\u093f\u0924\u0940 \u0906\u0930\u094d\u0925\u093f\u0915 "
    "\u092e\u0926\u0924 \u092e\u093f\u0933\u0924\u0947?"
)

print("QUESTION UNICODE CHECK:")
print(question.encode("unicode_escape").decode("ascii"))

rag = YojanaRAG()

try:
    print("\nRETRIEVAL TEST (NO GEMINI API CALL)\n")

    results = rag.retriever.search(
        question,
        top_k=5,
        candidate_k=30
    )

    for index, item in enumerate(results, start=1):
        print(
            f"{index}. Page {item['page_number']} | "
            f"Chunk {item['chunk_id']}"
        )
        print(item["text"][:200].replace("\n", " "))
        print()

finally:
    rag.close()
