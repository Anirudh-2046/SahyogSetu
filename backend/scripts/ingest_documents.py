#!/usr/bin/env python3
"""
SahyogSetu Document Ingestion CLI Tool
Executes batch and single-document extraction, chunking, embedding, and vector indexing.
"""

import sys
import os
import argparse
import json

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.services.ingestion.ingestion_service import ingestion_service
from backend.services.vector.sqlite_vector_store import sqlite_vector_store
from backend.services.embeddings.embedding_service import embedding_service

def main():
    parser = argparse.ArgumentParser(description="SahyogSetu Legal Document Ingestion CLI")
    parser.add_argument(
        "--action",
        choices=["inventory", "ingest-all", "ingest-doc", "reindex", "status", "report", "search"],
        default="status",
        help="Action to perform",
    )
    parser.add_argument("--doc-id", type=str, help="Target document ID for ingest-doc or reindex")
    parser.add_argument("--force", action="store_true", help="Force reindexing even if already indexed")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of documents for ingest-all")
    parser.add_argument("--query", type=str, help="Search query string for testing vector retrieval")
    parser.add_argument("--jurisdiction", type=str, default="all", help="Jurisdiction filter for search")

    args = parser.parse_args()

    if args.action == "inventory":
        inv = ingestion_service.get_inventory()
        print("=" * 80)
        print(f"SAHYOGSETU DOCUMENT INVENTORY ({len(inv)} DOCUMENTS REGISTERED)")
        print("=" * 80)
        for item in inv:
            print(f"[{item['processing_status']:12s}] {item['doc_id']:45s} | {item['jurisdiction']:7s} | {item['pages']:3d}p | {item['title'][:40]}")
        print("=" * 80)

    elif args.action == "status":
        stat = ingestion_service.get_ingestion_status()
        print("=" * 80)
        print("SAHYOGSETU VECTOR DATABASE & INGESTION STATUS")
        print("=" * 80)
        print(json.dumps(stat, indent=2))

    elif args.action == "report":
        rep = ingestion_service.get_ingestion_report()
        print("=" * 80)
        print("SAHYOGSETU DOCUMENT INGESTION AUDIT REPORT")
        print("=" * 80)
        print(json.dumps(rep, indent=2))

    elif args.action == "ingest-doc":
        if not args.doc_id:
            print("Error: --doc-id is required for ingest-doc action.")
            sys.exit(1)
        res = ingestion_service.ingest_document(args.doc_id, force=args.force)
        print(json.dumps(res, indent=2))

    elif args.action == "reindex":
        if not args.doc_id:
            print("Error: --doc-id is required for reindex action.")
            sys.exit(1)
        res = ingestion_service.reindex_document(args.doc_id)
        print(json.dumps(res, indent=2))

    elif args.action == "ingest-all":
        print(f"Beginning batch ingestion (force={args.force}, limit={args.limit})...")
        res = ingestion_service.ingest_all(force=args.force, limit=args.limit)
        print("=" * 80)
        print(f"Batch ingestion complete: {res['indexed_count']} indexed, {res['skipped_count']} skipped, {res['missing_file_count']} missing.")
        print(f"Total chunks created: {res['total_chunks_created']} | Total vectors: {res['total_vectors_in_store']}")
        print("=" * 80)

    elif args.action == "search":
        if not args.query:
            print("Error: --query is required for search action.")
            sys.exit(1)
        q_emb = embedding_service.generate_embedding(args.query)
        filters = {}
        if args.jurisdiction != "all":
            filters["jurisdiction"] = args.jurisdiction
        hits = sqlite_vector_store.search(q_emb, top_k=5, filters=filters)
        print(f"\nSearch results for query: '{args.query}' (filters: {filters})")
        print("-" * 80)
        for h in hits:
            print(f"Score: {h['score']:.4f} | {h['chunk_id']} | {h['document_title']}")
            print(f"Section: {h['section']} | Rule: {h['rule']} | Pages: {h['page_start']}-{h['page_end']}")
            print(f"Source: {h['source_url']}")
            print(f"Text Snippet: {h['chunk_text'][:180]}...\n")

if __name__ == "__main__":
    main()
