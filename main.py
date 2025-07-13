# main.py

from chains.summarizer_chain import load_summarizer_chain
from vector_store.chroma_manager import ChromaManager
from chains.resolution_chain import get_resolution
from chains.classification_chain import classify_ticket, should_escalate
from utils.logger import logger


def run_pipeline(title: str, description: str, metadata: dict):
    try:
        print("\n--- INPUT ---")
        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f"Metadata: {metadata}")

        # Step 1: Summarize
        summarizer = load_summarizer_chain()
        summary = summarizer.invoke({
            "title": title,
            "description": description,
            "metadata": str(metadata)
        })
        print("\n--- SUMMARY ---")
        print(summary)

        # Step 2: Search ChromaDB
        chroma = ChromaManager()
        similar_tickets = chroma.get_similar_tickets(summary, top_k=3)

        # Step 3: Get Resolution (reuse or GPT)
        resolution = get_resolution(summary, metadata, similar_tickets)
        print("\n--- RESOLUTION ---")
        print(resolution)

        # Step 4: Classify
        classification = classify_ticket(summary)
        print("\n--- CLASSIFICATION ---")
        print(classification)

        # Step 5: Escalation Check
        is_escalated = should_escalate(summary, metadata, classification["urgency"])
        print("\n--- ESCALATION ---")
        print("🚨 ESCALATED" if is_escalated else "No escalation")

        # Final Output
        return {
            "summary": summary,
            "resolution": resolution,
            "classification": classification,
            "escalation": is_escalated,
        }

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    # Example ticket input
    title = "Data loss detected after update"
    description = (
        "After installing the latest software patch, several user folders disappeared. "
        "The backup sync also failed. Need urgent help recovering data."
    )
    metadata = {
        "user": "Amit Dandu",
        "department": "Engineering",
        "role": "CTO",
    }

    run_pipeline(title, description, metadata)
