# vector_store/chroma_manager.py
import uuid
from typing import Dict, List, Optional
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from config import CHROMA_PERSIST_DIR
from utils.logger import logger


class ChromaManager:
    def __init__(self, collection_name: str = "ticket_knowledgebase"):
        try:
            embedder = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            self.db = Chroma(
                collection_name=collection_name,
                embedding_function=embedder,
                persist_directory=CHROMA_PERSIST_DIR,
            )
            logger.info(f"ChromaDB initialized: {collection_name}")
        except Exception as e:
            logger.error(f"ChromaDB init error: {e}")
            self.db = None

    # ---------- Ingestion ----------
    def add_ticket(self, summary: str, resolution: str, metadata: Dict):
        if not self.db:
            logger.error("ChromaDB unavailable - add_ticket skipped.")
            return
        try:
            uid = str(uuid.uuid4())
            doc = Document(
                page_content=f"{summary}\n\nResolution:\n{resolution}",
                metadata={**metadata, "id": uid},
            )
            self.db.add_documents([doc])
            logger.info(f"Ticket {uid} stored.")
        except Exception as e:
            logger.error(f"add_ticket error: {e}")

    # ---------- Similarity search ----------
    def get_similar_tickets(
        self,
        query: str,
        top_k: int = 3,
        filter_dict: Optional[Dict] = None,
    ) -> List[Dict]:
        """
        Returns a list of dicts: {content, metadata, score}
        filter_dict follows Chroma metadata syntax, e.g.:
            {"department": "Finance", "issue_type": "network"}
        """
        if not self.db:
            logger.error("ChromaDB unavailable - similarity search skipped.")
            return []

        try:
            docs_and_scores = self.db.similarity_search_with_score(
                query, k=top_k, filter=filter_dict or {}
            )
            results = [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": score,
                }
                for doc, score in docs_and_scores
            ]
            logger.info(
                f"Similarity search ⇒ {len(results)} hits | filter={filter_dict}"
            )
            return results
        except Exception as e:
            logger.error(f"similarity_search error: {e}")
            return []
