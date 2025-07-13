# config.py
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHROMA_PERSIST_DIR = "data/chroma_db"
MODEL_NAME = os.getenv("MODEL_NAME", "llama3-8b-8192")
