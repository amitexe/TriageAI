# chains/resolution_chain.py

from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import GROQ_API_KEY, MODEL_NAME
from utils.logger import logger


def get_weighted_match_score(match_metadata: dict, query_metadata: dict) -> int:
    score = 0
    if match_metadata.get("issue_type") == query_metadata.get("issue_type"):
        score += 2
    if match_metadata.get("department") == query_metadata.get("department"):
        score += 1
    if match_metadata.get("urgency") == query_metadata.get("urgency"):
        score += 1
    return score


def should_use_stored_resolution(match: dict, query_metadata: dict) -> bool:
    return (
        match["score"] < 1.0
        and get_weighted_match_score(match["metadata"], query_metadata) >= 2
    )


def load_resolution_chain():
    try:
        prompt = ChatPromptTemplate.from_template("""
        You are a smart IT assistant. Based on the following ticket summary, generate a helpful and actionable resolution.

        Ticket Summary:
        {summary}

        Additional Metadata:
        {metadata}
        """)

        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=MODEL_NAME,
            temperature=0.4,
        )

        chain = prompt | llm | StrOutputParser()
        return chain
    except Exception as e:
        logger.error(f"Failed to load GPT resolution chain: {e}")
        return None


def get_resolution(summary: str, metadata: dict, similar_tickets: list) -> str:
    try:
        # Try to use best match if it qualifies
        if similar_tickets:
            top_match = similar_tickets[0]
            if should_use_stored_resolution(top_match, metadata):
                logger.info("Using stored resolution from ChromaDB.")
                return top_match["content"].split("Resolution:\n")[-1].strip()

        # Else use Groq/GPT to generate a new one
        chain = load_resolution_chain()
        if not chain:
            return "Could not generate resolution (LLM unavailable)."

        return chain.invoke({"summary": summary, "metadata": str(metadata)})

    except Exception as e:
        logger.error(f"Error in resolution selection: {e}")
        return "Error occurred while generating resolution." 