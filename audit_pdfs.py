"""
audit_pdfs.py  -  Step 2 helper for the cooperative-chatbot project.

What it does for every PDF under RAW_DIR:
  1. computes SHA-256 (finds exact duplicates)
  2. counts pages and extractable characters
  3. flags scanned PDFs (little/no text layer)  -> need OCR
  4. flags garbled Hindi text (old non-Unicode fonts) -> need OCR or another source
  5. guesses 'volatile' from keywords (you confirm by hand)
  6. writes/updates manifest.csv, keeping any columns you filled in manually

Usage (local or Google Colab):
    pip install pymupdf
    python audit_pdfs.py --raw "data/raw" --manifest "data/manifest.csv"

Colab: mount Drive first, then point --raw at the Drive folder, e.g.
    from google.colab import drive; drive.mount('/content/drive')
    !python audit_pdfs.py --raw "/content/drive/MyDrive/coop_project/raw" \
                          --manifest "/content/drive/MyDrive/coop_project/manifest.csv"
"""
import argparse
import csv
import hashlib
import re
from datetime import date
from pathlib import Path

try:
    import pymupdf as fitz  # newer PyMuPDF
except ImportError:
    import fitz  # older PyMuPDF

COLUMNS = [
    "doc_id", "title", "module", "state", "doc_type", "language",
    "issuing_body", "source_url", "local_path", "date_retrieved",
    "version_or_year", "status", "volatile", "scanned", "sha256",
    "pages", "text_chars", "chars_per_page", "text_quality",
    "duplicate_of", "notes",
]

# Folder name -> module (matches the Drive folder layout we planned)
FOLDER_TO_MODULE = {
    "central": "laws", "haryana": "laws", "punjab": "laws", "jk": "laws",
    "pmfby": "pmfby", "kcc_finance": "finance_kcc", "grievance": "grievance",
    "schemes": "schemes_pacs",
}
FOLDER_TO_STATE = {"haryana": "Haryana", "punjab": "Punjab", "jk": "J&K",
                   "central": "Central", "pmfby": "Central",
                   "kcc_finance": "Central", "grievance": "Central"}

# Words in the file name that suggest the content changes often.
VOLATILE_HINTS = [
    "miss", "subvention", "interest", "circular", "notification", "premium",
    "rate", "season", "kharif", "rabi", "2025-26", "2026-27", "deadline",
]

SCANNED_CHARS_PER_PAGE = 100      # below this average => probably scanned
MIN_TEXT_PAGE_FRACTION = 0.6      # <60% of pages have text => probably scanned

DEVANAGARI = re.compile(r"[\u0900-\u097F]")
LETTERS = re.compile(r"[A-Za-z\u0900-\u097F\u0A00-\u0A7F]")


def sha256_of(path: Path, chunk=1024 * 1024) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def analyse_pdf(path: Path) -> dict:
    """Return page count, text size and a scanned / quality verdict."""
    info = {"pages": 0, "text_chars": 0, "chars_per_page": 0,
            "scanned": "unknown", "text_quality": "unknown"}
    try:
        doc = fitz.open(path)
    except Exception as e:  # corrupted or encrypted
        info["text_quality"] = f"cannot_open: {e}"
        return info

    if doc.needs_pass:
        info["text_quality"] = "encrypted"
        return info

    pages = doc.page_count
    total_chars, text_pages = 0, 0
    sample = []
    for i, page in enumerate(doc):
        txt = page.get_text("text") or ""
        n = len(txt.strip())
        total_chars += n
        if n >= 50:
            text_pages += 1
        if len(sample) < 8 and n > 0 and i % max(1, pages // 8) == 0:
            sample.append(txt)
    doc.close()

    cpp = total_chars / pages if pages else 0
    frac = text_pages / pages if pages else 0
    scanned = cpp < SCANNED_CHARS_PER_PAGE or frac < MIN_TEXT_PAGE_FRACTION

    info.update(pages=pages, text_chars=total_chars,
                chars_per_page=round(cpp, 1),
                scanned="yes" if scanned else "no")

    # Quality check on sampled text: garbled legacy-font Hindi shows up as
    # lots of letters but almost no proper Devanagari / very odd symbols.
    joined = " ".join(sample)
    letters = LETTERS.findall(joined)
    if scanned:
        info["text_quality"] = "needs_ocr"
    elif letters:
        weird = sum(1 for c in joined if ord(c) > 127 and not DEVANAGARI.match(c)
                    and not re.match(r"[\u0A00-\u0A7F\u2010-\u203A\u00A0-\u00FF]", c))
        weird_ratio = weird / max(1, len(joined))
        info["text_quality"] = "check_garbled" if weird_ratio > 0.15 else "ok"
    return info


def guess_volatile(name: str) -> str:
    n = name.lower()
    return "yes" if any(k in n for k in VOLATILE_HINTS) else "no"


def make_doc_id(rel: Path, used: set) -> str:
    base = re.sub(r"[^a-z0-9]+", "_", rel.stem.lower()).strip("_")[:50]
    cand, k = base, 2
    while cand in used:
        cand = f"{base}_{k}"
        k += 1
    used.add(cand)
    return cand


def load_manifest(path: Path) -> dict:
    rows = {}
    if path.exists():
        with open(path, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r.get("local_path"):
                    rows[r["local_path"]] = r
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True, help="folder holding the PDFs")
    ap.add_argument("--manifest", required=True, help="manifest.csv path")
    args = ap.parse_args()

    raw = Path(args.raw)
    manifest_path = Path(args.manifest)
    existing = load_manifest(manifest_path)
    used_ids = {r["doc_id"] for r in existing.values() if r.get("doc_id")}
    first_seen = {}   # sha256 -> doc_id, for duplicate detection

    pdfs = sorted(p for p in raw.rglob("*") if p.suffix.lower() == ".pdf")
    print(f"Found {len(pdfs)} PDFs under {raw}")

    out = []
    for p in pdfs:
        rel = str(p.relative_to(raw)).replace("\\", "/")
        row = existing.get(rel, {c: "" for c in COLUMNS})
        row = {c: row.get(c, "") for c in COLUMNS}  # normalise columns

        top = rel.split("/")[0].lower()
        row["local_path"] = rel
        row["doc_id"] = row["doc_id"] or make_doc_id(Path(rel), used_ids)
        row["module"] = row["module"] or FOLDER_TO_MODULE.get(top, "")
        row["state"] = row["state"] or FOLDER_TO_STATE.get(top, "")
        row["date_retrieved"] = row["date_retrieved"] or date.today().isoformat()
        row["status"] = row["status"] or "needs_check"
        row["title"] = row["title"] or p.stem.replace("_", " ")
        # only guess volatile if you haven't set it yourself
        row["volatile"] = row["volatile"] or guess_volatile(p.name)

        row["sha256"] = sha256_of(p)
        row.update({k: v for k, v in analyse_pdf(p).items()})

        if row["sha256"] in first_seen:
            row["duplicate_of"] = first_seen[row["sha256"]]
        else:
            first_seen[row["sha256"]] = row["doc_id"]
            row["duplicate_of"] = ""
        out.append(row)
        print(f"  {rel:60s} pages={row['pages']:<4} scanned={row['scanned']:<7} "
              f"quality={row['text_quality']}")

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(out)

    dups = [r for r in out if r["duplicate_of"]]
    scanned = [r for r in out if r["scanned"] == "yes"]
    bad = [r for r in out if r["text_quality"] not in ("ok", "needs_ocr")]
    print("\nSummary")
    print(f"  total PDFs      : {len(out)}")
    print(f"  duplicates      : {len(dups)}  (delete these)")
    print(f"  scanned/needs OCR: {len(scanned)}")
    print(f"  need a look     : {len(bad)}  (garbled / encrypted / cannot open)")
    print(f"Manifest written to {manifest_path}")


if __name__ == "__main__":
    main()
