#!/usr/bin/env python3
"""
extract_and_chunk.py  -  Step 3 of the cooperative-chatbot project.

Reads manifest.csv, and for every usable document:
  1. EXTRACT  text from the PDF (text layer) and OCR the pages that need it
  2. CLEAN    headers/footers, page numbers, hyphenation, line wraps
  3. CHUNK    by legal structure (Section/Rule) or by numbered headings,
              never mid-section when it can be avoided
  4. TAG      every chunk with metadata (state, module, section, pages, ...)
  5. REPORT   per-document quality flags + a sample file to read by hand

Outputs (in --out):
  pages/<doc_id>.json         raw per-page text (cached; OCR only runs once)
  chunks/<doc_id>.jsonl       chunks for one document
  chunks_all.jsonl            all chunks together (feed this to Step 4)
  processing_report.csv       one row per document, with quality flags
  review_samples.md           3 random chunks per document to read by eye

Colab setup (once per session):
    !apt-get -qq install tesseract-ocr tesseract-ocr-hin tesseract-ocr-pan
    !pip -q install pymupdf pytesseract pillow

Run:
    python extract_and_chunk.py --raw  "/content/drive/MyDrive/coop_project/raw" \
                                --manifest "/content/drive/MyDrive/coop_project/manifest.csv" \
                                --out "/content/drive/MyDrive/coop_project/processed"
Useful flags:  --mode text|ocr|all   --only doc_id1,doc_id2   --force   --rechunk   --workers 2
"""
import argparse
import csv
import io
import json
import random
import re
import sys
import unicodedata
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

try:
    import pytesseract
    if sys.platform == "win32":
        tess = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
        if tess.exists():
            pytesseract.pytesseract.tesseract_cmd = str(tess)
except ImportError:
    pass

try:
    import pymupdf as fitz
except ImportError:  # older PyMuPDF
    import fitz

SKIP_STATUS = {"excluded", "duplicate", "superseded"}
MIN_PAGE_CHARS = 50          # a page with less text than this gets OCR'd
OCR_DPI = 300
MAX_CHARS = 1200             # target upper size of a chunk
MIN_CHARS = 250              # tiny sections are merged with their neighbour
LANG_MAP = {"english": "eng", "hindi": "hin", "punjabi": "pan", "dogri": "hin"}

# ---------------------------------------------------------------- patterns
# "3. Registration of societies.—Where ..."   (Acts and Rules)
SEC_DASH = re.compile(
    r"^(\d{1,3}[A-Z]{0,2})\.\s+([A-Z(][^\n]{1,160}?)(?:\s*\.\s*[—–-]{1,2}|\s*[—–]{1,2}|\s*--)")
CHAPTER = re.compile(r"^(CHAPTER|PART)\s+[IVXLC\d]+[A-Z]?\b.*$")
SCHEDULE = re.compile(r"^(THE\s+)?([A-Z]+\s+)?(SCHEDULE|ANNEXURE|APPENDIX)\b.*$")
# guideline style:  "2.1 Eligibility"   or an ALL-CAPS heading line
NUM_HEAD = re.compile(r"^(\d{1,2}(?:\.\d{1,2}){0,3})\.?\s+([A-Z][^\n]{2,90})$")
CAPS_HEAD = re.compile(r"^[A-Z][A-Z0-9 ,&/()\-:]{4,80}$")
PAGE_NO = re.compile(r"^[\-–—\s]*(page\s*)?\d{1,4}(\s*(of|/)\s*\d{1,4})?[\-–—\s]*$", re.I)
CLAUSE = re.compile(r"^(\(\s*[0-9A-Za-z]{1,4}\s*\)|[•\u2022*]|\d+(\.\d+)*\.?\s)")
LIGATURES = {"\ufb01": "fi", "\ufb02": "fl", "\ufb00": "ff", "\u00ad": "", "\u00a0": " ",
             "\u200b": "", "\u200c": "", "\u200d": ""}


# ---------------------------------------------------------------- helpers
def norm_text(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    for k, v in LIGATURES.items():
        s = s.replace(k, v)
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", s)


def ocr_lang_for(row: dict) -> str:
    if row.get("ocr_lang"):                      # optional manual override column
        return row["ocr_lang"]
    lang = (row.get("language") or "").strip().lower()
    if lang == "english":
        return "eng"
    if lang in LANG_MAP:
        return LANG_MAP[lang] + "+eng"
    if row.get("text_quality") == "check_garbled":   # blank language + garbled text
        return "eng+pan"                              # probably legacy Punjabi font
    return "eng"


def needs_full_ocr(row: dict, trust_text_layer: bool) -> bool:
    if (row.get("scanned") or "").lower() == "yes" or row.get("text_quality") == "needs_ocr":
        return True
    return row.get("text_quality") == "check_garbled" and not trust_text_layer


# ---------------------------------------------------------------- 1. EXTRACT
def check_tesseract(langs: set):
    try:
        import pytesseract
        have = set(pytesseract.get_languages())
    except Exception as e:
        sys.exit(f"Tesseract/pytesseract not available ({e}).\n"
                 "In Colab run:  !apt-get -qq install tesseract-ocr tesseract-ocr-hin "
                 "tesseract-ocr-pan  &&  !pip -q install pytesseract pillow")
    missing = {p for l in langs for p in l.split("+")} - have
    if missing:
        sys.exit(f"Missing Tesseract language data: {sorted(missing)}. "
                 "Install e.g. tesseract-ocr-hin / tesseract-ocr-pan.")


def ocr_png(png: bytes, lang: str):
    import pytesseract
    from PIL import Image
    img = Image.open(io.BytesIO(png))
    d = pytesseract.image_to_data(img, lang=lang, output_type=pytesseract.Output.DICT)
    lines, confs = {}, []
    for i, w in enumerate(d["text"]):
        if not w.strip():
            continue
        lines.setdefault((d["block_num"][i], d["par_num"][i], d["line_num"][i]), []).append(w)
        try:
            c = float(d["conf"][i])
            if c >= 0:
                confs.append(c)
        except ValueError:
            pass
    out, prev = [], None
    for key in sorted(lines):
        if prev and key[:2] != prev[:2]:
            out.append("")                      # paragraph break
        out.append(" ".join(lines[key]))
        prev = key
    return "\n".join(out), (sum(confs) / len(confs) if confs else 0.0)


def extract_pages(row: dict, pdf: Path, args) -> list:
    doc = fitz.open(pdf)
    full = needs_full_ocr(row, args.trust_text_layer)
    pages, todo = [], []
    for i, page in enumerate(doc):
        txt = page.get_text("text") or ""
        pages.append({"page": i + 1, "text": txt, "method": "text", "conf": None})
        if full or len(txt.strip()) < MIN_PAGE_CHARS:
            todo.append(i)
    if todo:
        lang = ocr_lang_for(row)
        print(f"    OCR {len(todo)}/{len(pages)} pages (lang={lang})")
        BATCH = 8
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            for b in range(0, len(todo), BATCH):
                idx = todo[b:b + BATCH]
                pngs = [doc[i].get_pixmap(dpi=OCR_DPI, colorspace=fitz.csGRAY).tobytes("png")
                        for i in idx]
                for i, (text, conf) in zip(idx, ex.map(lambda p: ocr_png(p, lang), pngs)):
                    pages[i].update(text=text, method="ocr", conf=round(conf, 1))
    doc.close()
    return pages


# ---------------------------------------------------------------- 2. CLEAN
def clean_to_lines(pages: list) -> list:
    """Return [(page_no, line), ...] with headers/footers/page numbers removed."""
    per_page = []
    for p in pages:
        lines = [norm_text(l).rstrip() for l in p["text"].splitlines()]
        per_page.append((p["page"], lines))

    # repeated header/footer lines = same text (digits ignored) near top/bottom of many pages
    counter = Counter()
    for _, lines in per_page:
        ne = [l.strip() for l in lines if l.strip()]
        for l in set(ne[:2] + ne[-2:]):
            counter[re.sub(r"\d+", "#", l.lower())] += 1
    n = len(per_page)
    repeated = {k for k, c in counter.items() if n >= 6 and c / n >= 0.3 and len(k) < 100}

    out = []
    for page_no, lines in per_page:
        idx = [i for i, l in enumerate(lines) if l.strip()]
        edge = set(idx[:2] + idx[-2:])
        for i, l in enumerate(lines):
            s = l.strip()
            if i in edge and (PAGE_NO.match(s) or re.sub(r"\d+", "#", s.lower()) in repeated):
                continue
            if s and not re.search(r"\w", s):    # pure punctuation / OCR junk
                continue
            out.append((page_no, s))
    return out


# ---------------------------------------------------------------- 3. CHUNK
def is_guideline_heading(l: str) -> bool:
    if len(l) >= 100:
        return False
    if NUM_HEAD.match(l) and not l.endswith((".", ",", ";")):
        return True
    return bool(CAPS_HEAD.match(l))


def segment(lines: list, title: str):
    """Split into units by Section/Rule (legal docs) or numbered headings (guidelines)."""
    legal = sum(1 for _, l in lines if SEC_DASH.match(l)) >= 3
    word = "Rule" if ("rules" in title.lower() and "act" not in title.lower()) else "Section"
    units, cur, chapter = [], None, ""

    def new(label, ttl, page):
        nonlocal cur
        cur = {"label": label, "title": ttl, "chapter": chapter, "page": page, "lines": []}
        units.append(cur)

    new("Preamble", "", lines[0][0] if lines else 1)
    i = 0
    while i < len(lines):
        page, l = lines[i]
        m = SEC_DASH.match(l) if legal else None
        if CHAPTER.match(l) or SCHEDULE.match(l):
            chapter = l[:100]
            if i + 1 < len(lines) and CAPS_HEAD.match(lines[i + 1][1]):
                chapter += " - " + lines[i + 1][1][:100]
            new("Chapter heading", chapter, page)
            cur["lines"].append((page, l))
        elif m:
            new(f"{word} {m.group(1)}", m.group(2).strip(" ."), page)
            cur["lines"].append((page, l))
        elif not legal and is_guideline_heading(l):
            mm = NUM_HEAD.match(l)
            new(f"Para {mm.group(1)}" if mm else "Heading", (mm.group(2) if mm else l)[:100], page)
            cur["lines"].append((page, l))
        else:
            cur["lines"].append((page, l))
        i += 1
    return [u for u in units if any(x[1] for x in u["lines"])], ("legal" if legal else "guideline")


def unwrap(lines: list) -> list:
    """lines -> paragraphs [(text, page)], joining wrapped lines and hyphenation."""
    paras, cur, cur_page = [], "", None

    def flush():
        nonlocal cur
        if cur.strip():
            paras.append((cur.strip(), cur_page))
        cur = ""

    for page, s in lines:
        if not s:
            flush()
            continue
        if cur and cur.endswith("-") and s[:1].islower() and cur[-2:-1].isalpha():
            cur = cur[:-1] + s                       # re-join hyphenated word
        elif cur and not CLAUSE.match(s):
            cur += " " + s
        else:
            flush()
            cur, cur_page = s, page
    flush()
    return paras


def pack(paras: list, max_chars: int) -> list:
    """Greedy-pack paragraphs into pieces <= max_chars; split huge paragraphs on sentences."""
    pieces, buf, buf_pages = [], "", []

    def emit():
        nonlocal buf, buf_pages
        if buf.strip():
            pieces.append((buf.strip(), buf_pages[0], buf_pages[-1]))
        buf, buf_pages = "", []

    for text, page in paras:
        parts, was_split = [text], False
        if len(text) > max_chars:
            parts, was_split = re.split(r"(?<=[.;:।])\s+", text), True
        for k, part in enumerate(parts):
            if buf and len(buf) + len(part) + 2 > max_chars:
                emit()
            sep = " " if (was_split and k > 0) else "\n"
            buf += (sep if buf else "") + part
            buf_pages.append(page)
    emit()
    return pieces


def build_chunks(row: dict, pages: list) -> tuple:
    lines = clean_to_lines(pages)
    if not lines:
        return [], 0, "empty"
    units, mode = segment(lines, row.get("title", ""))
    sec_count = sum(1 for u in units if u["label"] not in ("Preamble", "Chapter heading", "Heading"))

    # turn units into pieces
    items = []
    for u in units:
        paras = unwrap(u["lines"])
        for k, (text, p0, p1) in enumerate(pack(paras, MAX_CHARS)):
            items.append({"label": u["label"] + (" (cont.)" if k else ""), "title": u["title"],
                          "chapter": u["chapter"], "text": text, "p0": p0, "p1": p1})

    # merge tiny neighbours
    merged, acc = [], None
    for it in items:
        if acc and len(acc["text"]) < MIN_CHARS and len(acc["text"]) + len(it["text"]) <= MAX_CHARS:
            acc["text"] += "\n" + it["text"]
            acc["labels"].append(it["label"])
            acc["p1"] = it["p1"]
        else:
            if acc:
                merged.append(acc)
            acc = {**it, "labels": [it["label"]]}
    if acc:
        merged.append(acc)

    by_page = {p["page"]: p for p in pages}
    chunks = []
    for n, c in enumerate(merged):
        used = [by_page[p] for p in range(c["p0"], c["p1"] + 1) if p in by_page]
        methods = {p["method"] for p in used} or {"text"}
        confs = [p["conf"] for p in used if p["conf"] is not None]
        labels = [l for l in c["labels"] if l != "Chapter heading"] or c["labels"]
        ctx = f'{row["title"]} ({row.get("state", "")})'
        if c["chapter"]:
            ctx += f' | {c["chapter"]}'
        ctx += f' | {", ".join(labels)}' + (f': {c["title"]}' if c["title"] else "")
        chunks.append({
            "chunk_id": f'{row["doc_id"]}::{n:04d}',
            "doc_id": row["doc_id"], "title": row["title"],
            "state": row.get("state", ""), "module": row.get("module", ""),
            "language": row.get("language", ""), "doc_type": row.get("doc_type", ""),
            "source_url": row.get("source_url", ""), "date_retrieved": row.get("date_retrieved", ""),
            "version_or_year": row.get("version_or_year", ""), "volatile": row.get("volatile", ""),
            "status": row.get("status", ""), "chapter": c["chapter"],
            "section_labels": labels, "section_title": c["title"],
            "page_start": c["p0"], "page_end": c["p1"],
            "extraction": "mixed" if len(methods) > 1 else methods.pop(),
            "ocr_conf": round(min(confs), 1) if confs else None,
            "n_chars": len(c["text"]), "text": c["text"],
            "embed_text": ctx + "\n" + c["text"],
        })
    return chunks, sec_count, mode


# ---------------------------------------------------------------- driver
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", default="", help="comma-separated doc_ids")
    ap.add_argument("--mode", choices=["all", "text", "ocr"], default="all",
                    help="text = documents with a usable text layer; "
                         "ocr = scanned or garbled documents; all = both")
    ap.add_argument("--force", action="store_true", help="redo extraction even if cached")
    ap.add_argument("--rechunk", action="store_true", help="use cached pages only (no OCR)")
    ap.add_argument("--workers", type=int, default=2, help="parallel OCR threads")
    ap.add_argument("--trust-text-layer", action="store_true",
                    help="do not OCR docs flagged check_garbled")
    args = ap.parse_args()

    raw, out = Path(args.raw), Path(args.out)
    for sub in ("pages", "chunks"):
        (out / sub).mkdir(parents=True, exist_ok=True)

    with open(args.manifest, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    only = {x.strip() for x in args.only.split(",") if x.strip()}
    todo = [r for r in rows if r["status"] not in SKIP_STATUS and not r.get("duplicate_of")
            and (not only or r["doc_id"] in only)]
    if args.mode != "all":
        todo = [r for r in todo if needs_full_ocr(r, args.trust_text_layer) == (args.mode == "ocr")]
    print(f"{len(todo)} documents to process "
          f"({len(rows) - len(todo)} skipped: excluded/duplicate/superseded)")

    if not args.rechunk:
        langs = {ocr_lang_for(r) for r in todo if needs_full_ocr(r, args.trust_text_layer)
                 or int(r.get("pages_no_text") or 0) > 0}
        if langs:
            check_tesseract(langs)

    report = []
    for n, row in enumerate(todo, 1):
        did = row["doc_id"]
        print(f"[{n}/{len(todo)}] {did}")
        pages_file = out / "pages" / f"{did}.json"
        pages = None
        if pages_file.exists() and not args.force:
            cached = json.loads(pages_file.read_text(encoding="utf-8"))
            if cached.get("sha256") == row.get("sha256"):
                pages = cached["pages"]
                print("    using cached pages")
        if pages is None:
            if args.rechunk:
                print("    no cache, skipped (--rechunk)")
                continue
            pdf = raw / row["local_path"]
            if not pdf.exists():
                print(f"    MISSING FILE {pdf}")
                report.append({"doc_id": did, "flags": "file_missing"})
                continue
            pages = extract_pages(row, pdf, args)
            pages_file.write_text(json.dumps({"sha256": row.get("sha256"), "pages": pages},
                                             ensure_ascii=False), encoding="utf-8")

        chunks, sec_count, mode = build_chunks(row, pages)
        with open(out / "chunks" / f"{did}.jsonl", "w", encoding="utf-8") as f:
            for c in chunks:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")

        ocr = [p for p in pages if p["method"] == "ocr"]
        confs = [p["conf"] for p in ocr if p["conf"]]
        mean_conf = round(sum(confs) / len(confs), 1) if confs else ""
        flags = []
        if confs and mean_conf < 75:
            flags.append("low_ocr_confidence")
        if any(p["conf"] is not None and p["conf"] < 60 for p in ocr):
            flags.append("some_pages_conf_below_60")
        if row.get("module") == "laws" and sec_count < 3 and len(pages) > 5:
            flags.append("no_section_structure_detected")
        if chunks and sum(c["n_chars"] for c in chunks) / len(pages) < 300:
            flags.append("very_little_text")
        if not chunks:
            flags.append("no_chunks")
        report.append({
            "doc_id": did, "state": row.get("state"), "module": row.get("module"),
            "pages": len(pages), "ocr_pages": len(ocr), "mean_ocr_conf": mean_conf,
            "mode": mode, "sections_detected": sec_count, "chunks": len(chunks),
            "avg_chunk_chars": round(sum(c["n_chars"] for c in chunks) / max(1, len(chunks))),
            "flags": ";".join(flags)})

    # combine + report + review samples (merges with earlier --mode runs in the same --out)
    cols = ["doc_id", "state", "module", "pages", "ocr_pages", "mean_ocr_conf", "mode",
            "sections_detected", "chunks", "avg_chunk_chars", "flags"]
    rep_path = out / "processing_report.csv"
    merged = {}
    if rep_path.exists():
        with open(rep_path, newline="", encoding="utf-8") as f:
            merged = {r["doc_id"]: r for r in csv.DictReader(f)}
    merged.update({r["doc_id"]: r for r in report})
    report = list(merged.values())

    allc = []
    for p in sorted((out / "chunks").glob("*.jsonl")):
        allc += [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines()]
    with open(out / "chunks_all.jsonl", "w", encoding="utf-8") as f:
        for c in allc:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    with open(rep_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(report)

    random.seed(1)
    with open(out / "review_samples.md", "w", encoding="utf-8") as f:
        f.write("# Chunks to read by eye (3 per document)\n\n")
        for r in report:
            docs = [c for c in allc if c["doc_id"] == r["doc_id"]]
            if not docs:
                continue
            f.write(f'## {r["doc_id"]}  [{r.get("flags", "")}]\n\n')
            for c in random.sample(docs, min(3, len(docs))):
                f.write(f'**{c["chunk_id"]}** | {", ".join(c["section_labels"])} | '
                        f'pages {c["page_start"]}-{c["page_end"]} | {c["extraction"]} | '
                        f'ocr_conf={c["ocr_conf"]}\n\n> ' + c["text"][:3000].replace("\n", "\n> ")
                        + "\n\n")

    flagged = [r for r in report if r.get("flags")]
    print(f"\nDone. {len(report)} documents, {len(allc)} chunks.")
    print(f"{len(flagged)} documents flagged - see processing_report.csv:")
    for r in flagged:
        print(f'  {r["doc_id"][:55]:55s} {r["flags"]}')


if __name__ == "__main__":
    main()
