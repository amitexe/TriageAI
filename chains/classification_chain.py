# chains/classification_chain.py

from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import GROQ_API_KEY, MODEL_NAME
from utils.logger import logger

DANGER_KEYWORDS = ["breach", "data loss", "security issue"]


def load_classifier_chain():
    try:
        prompt = ChatPromptTemplate.from_template("""
        Classify the following IT helpdesk ticket.

        Return the response in this JSON format:
        {{
            "urgency": one of ["low", "medium", "high", "critical"],
            "issue_type": one of ["hardware", "software", "network", "access", "other"]
        }}

        Ticket Summary:
        {summary}
        """)

        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=MODEL_NAME,
            temperature=0.2,
        )

        chain = prompt | llm | StrOutputParser()
        return chain
    except Exception as e:
        logger.error(f"Failed to load classifier chain: {e}")
        return None


def classify_ticket(summary: str) -> dict:
    try:
        chain = load_classifier_chain()
        if not chain:
            return {"urgency": "medium", "issue_type": "other"}

        response = chain.invoke({"summary": summary})
        return eval(response)  # parse JSON-style string into dict
    except Exception as e:
        logger.error(f"Classification error: {e}")
        return {"urgency": "medium", "issue_type": "other"}


def should_escalate(summary: str, metadata: dict, urgency: str) -> bool:
    if urgency == "critical":
        return True

    role = metadata.get("role", "").lower()
    if any(keyword in role for keyword in ["ceo", "cto", "chief", "founder"]):
        return True

    text = (summary + " " + str(metadata)).lower()
    if any(kw in text for kw in DANGER_KEYWORDS):
        return True

    return False
