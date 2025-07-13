# tests/test_chroma_ingest.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vector_store.chroma_manager import ChromaManager

def ingest_sample_tickets():
    chroma = ChromaManager()

    sample_tickets = [
        {
            "summary": "User cannot connect to office Wi-Fi after update.",
            "resolution": "Reset network adapter settings and reinstalled drivers.",
            "metadata": {"department": "IT", "urgency": "medium", "issue_type": "network"}
        },
        
        {
            "summary": "Email access denied for new joiner in HR team.",
            "resolution": "Provisioned access via Azure AD group assignment.",
            "metadata": {"department": "HR", "urgency": "high", "issue_type": "access"}
        },
        {
            "summary": "Laptop crashing during video calls.",
            "resolution": "Updated display and audio drivers. Issue resolved.",
            "metadata": {"department": "Finance", "urgency": "low", "issue_type": "hardware"}
        }
    ]

    for ticket in sample_tickets:
        chroma.add_ticket(ticket["summary"], ticket["resolution"], ticket["metadata"])

if __name__ == "__main__":
    ingest_sample_tickets()

