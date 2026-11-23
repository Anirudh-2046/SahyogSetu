#!/usr/bin/env python3
"""
SahyogSetu Phase 13: Full Legal Corpus Reindexing Script
Reindexes all canonical documents from the updated OFFICIAL_DOCUMENT_REGISTRY
into backend/data/vectors.db with rich statutory structure and metadata.
"""

import sys
import os
import json
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.ingestion.ingestion_service import ingestion_service, MANIFEST_TO_OFFICIAL_MAP
from backend.services.vector.sqlite_vector_store import sqlite_vector_store

def reindex_all():
    print("=" * 80)
    print("SAHYOGSETU PHASE 13: STATUTORY CORPUS REINDEXING")
    print("=" * 80)

    target_doc_ids = [
        "mscs_act_2002_amendment_2023",
        "the_punjab_cooperative_societies_act_1961_amended_",
        "gazette_notification_of_the_2021_amendment",
        "haryana_co_operative_societies_act_1984_pdf",
        "act_1989_cooperation_gov_in_copy",
        "brief_on_model_byelaws_for_pacs",
        "model_bye_laws_explained_in_a_parliament_reply",
        "pacs_computerisation_guidelines",
        "cabinet_decision_pib",
        "kcc_master_circular_2018",
        "final_pmfby_operational_guidelines_2023_120125",
        "ots_the_punjab_state_agriculture_development_bank_",
    ]

    total_chunks = 0
    for doc_id in target_doc_ids:
        print(f"\nReindexing document: {doc_id}...")
        res = ingestion_service.reindex_document(doc_id)
        status = res.get("status")
        chunks = res.get("chunks_created", 0)
        total_chunks += chunks
        print(f"  Result: status={status}, chunks_created={chunks}")

    print("\n" + "=" * 80)
    print(f"REINDEXING COMPLETE: Total vectors in vectors.db = {sqlite_vector_store.count_vectors()}")
    print("=" * 80)

if __name__ == "__main__":
    reindex_all()
