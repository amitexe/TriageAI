# chains/summarizer_chain.py

from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import GROQ_API_KEY, MODEL_NAME
from utils.logger import logger

def load_summarizer_chain():
    try:
        prompt = ChatPromptTemplate.from_template("""
        You are a very helpful IT assistant. Summarize the following helpdesk ticket in 2–3 sentences.

        Ticket Title: {title}
        Description: {description}
        Metadata: {metadata}
        """)

        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=MODEL_NAME,
            temperature=0.3
        )

        chain = prompt | llm | StrOutputParser()
        return chain

    except Exception as e:
        logger.error(f"Failed to load summarizer chain: {e}")
        return None
