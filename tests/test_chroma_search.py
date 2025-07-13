# tests/test_chroma_search.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from vector_store.chroma_manager import ChromaManager

def search_demo():
    chroma = ChromaManager()

    query = "Cannot connect to Wi-Fi after Windows update."
    print("\n--- Unfiltered search ---")
    for hit in chroma.get_similar_tickets(query):
        print(f"{hit['score']:.4f} | {hit['metadata']}")

    filter_finance = {"department": "Finance"}
    print("\n--- Filter: department = Finance ---")
    for hit in chroma.get_similar_tickets(query, filter_dict=filter_finance):
        print(f"{hit['score']:.4f} | {hit['metadata']}")

if __name__ == "__main__":
    search_demo()
