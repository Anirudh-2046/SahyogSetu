import csv
import json
import os
import sqlite3

def main():
    print("=== MANIFEST AUDIT ===")
    if os.path.exists("manifest.csv"):
        with open("manifest.csv", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        print(f"Total manifest rows: {len(rows)}")
        existing = []
        for r in rows:
            lp = r.get("local_path", "")
            exists = os.path.exists(lp) if lp else False
            if exists:
                existing.append((r["doc_id"], lp, os.path.getsize(lp)))
        print(f"Manifest files actually existing on disk: {len(existing)}")
        for doc_id, lp, sz in existing:
            print(f"  - {doc_id}: {lp} ({sz} bytes)")
    else:
        print("manifest.csv NOT found")

    print("\n=== PROCESSED DIR AUDIT ===")
    if os.path.exists("processed"):
        for root, dirs, files in os.walk("processed"):
            print(f"Dir: {root} -> {len(dirs)} subdirs, {len(files)} files")
            for f in files[:5]:
                p = os.path.join(root, f)
                print(f"   file: {f} ({os.path.getsize(p)} bytes)")

    print("\n=== VECTORS.DB CHUNKS AUDIT ===")
    db_path = os.path.join("backend", "data", "vectors.db")
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cur.fetchall()]
        print("Tables in vectors.db:", tables)
        for tbl in tables:
            cur.execute(f"SELECT count(*) FROM {tbl}")
            print(f"  {tbl} count: {cur.fetchone()[0]}")
        cur.execute("PRAGMA table_info(document_chunks)")
        cols = [c[1] for c in cur.fetchall()]
        print("Columns in document_chunks:", cols)
        cur.execute("SELECT chunk_id, doc_id, jurisdiction, section, document_title FROM document_chunks")
        rows = cur.fetchall()
        print(f"Total chunks retrieved: {len(rows)}")
        for r in rows:
            print(f"  {r[0]} | doc:{r[1]} | jur:{r[2]} | sec:{r[3]} | {r[4]}")
        conn.close()

    print("\n=== GOLD BENCHMARK AUDIT ===")
    gold_path = os.path.join("backend", "evaluation", "phase10", "gold_benchmark_dataset.json")
    if os.path.exists(gold_path):
        with open(gold_path, encoding="utf-8") as f:
            gold_data = json.load(f)
        print(f"Total queries in gold dataset: {len(gold_data)}")
        expected_docs = {}
        expected_secs = {}
        unsupported_count = 0
        for item in gold_data:
            doc = item.get("expected_document")
            sec = item.get("expected_section")
            if not doc:
                unsupported_count += 1
            else:
                expected_docs[doc] = expected_docs.get(doc, 0) + 1
            if sec:
                expected_secs[f"{doc} - Sec {sec}"] = expected_secs.get(f"{doc} - Sec {sec}", 0) + 1
        print(f"Unsupported / Abstention queries: {unsupported_count}")
        print("Expected documents distribution:")
        for d, cnt in expected_docs.items():
            print(f"  {d}: {cnt}")
        print(f"Total distinct expected sections: {len(expected_secs)}")
        for s, cnt in list(expected_secs.items())[:15]:
            print(f"  {s}: {cnt}")

    print("\n=== MANIFEST CENTRAL SCHEMES ===")
    if os.path.exists("manifest.csv"):
        with open("manifest.csv", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                doc_id = r["doc_id"]
                if any(k in doc_id for k in ["pacs", "pm", "pib", "kisan", "cabinet", "miss"]):
                    print(f"  {doc_id}: {r.get('title')}")

if __name__ == "__main__":
    main()
