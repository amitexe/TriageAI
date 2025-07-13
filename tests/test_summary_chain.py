# tests/test_summary_chain.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chains.summarizer_chain import load_summarizer_chain

def test_summarizer():
    chain = load_summarizer_chain()
    if not chain:
        print("Failed to initialize summarizer chain.")
        return

    input_data = {
        "title": "Laptop not booting",
        "description": "My Dell laptop is stuck at the BIOS screen and won't proceed further.",
        "metadata": "User: John Doe, Department: Finance, Role: Analyst"
    }

    summary = chain.invoke(input_data)
    print("Summary Output:\n", summary)

if __name__ == "__main__":
    test_summarizer()
