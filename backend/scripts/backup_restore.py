"""
SahyogSetu Database Backup and Restore Utility
Provides online, non-blocking SQLite hot backups with SHA-256 checksum verification
and integrity checks for news.db and vectors.db.
"""

import os
import sys
import time
import shutil
import sqlite3
import hashlib
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.config import settings

logger = logging.getLogger("sahyogsetu.backup")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def calculate_sha256(filepath: str) -> str:
    """Calculates SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def verify_sqlite_integrity(db_path: str) -> bool:
    """Runs PRAGMA integrity_check on an SQLite database."""
    if not os.path.exists(db_path):
        return False
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check;")
        row = cursor.fetchone()
        conn.close()
        return bool(row and row[0] == "ok")
    except Exception as e:
        logger.error("Integrity check failed for %s: %s", db_path, e)
        return False


def hot_backup_sqlite(src_path: str, dst_path: str) -> Dict[str, Any]:
    """
    Performs hot online backup using SQLite's backup API.
    Zero data loss, non-blocking to active readers and writers.
    """
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    if not os.path.exists(src_path):
        return {"success": False, "error": f"Source {src_path} does not exist"}

    try:
        src_conn = sqlite3.connect(src_path)
        dst_conn = sqlite3.connect(dst_path)

        with dst_conn:
            src_conn.backup(dst_conn, pages=100)

        dst_conn.close()
        src_conn.close()

        # Check integrity of the newly created backup
        if not verify_sqlite_integrity(dst_path):
            return {"success": False, "error": f"Integrity check failed on backup {dst_path}"}

        file_size = os.path.getsize(dst_path)
        file_hash = calculate_sha256(dst_path)

        return {
            "success": True,
            "path": dst_path,
            "size_bytes": file_size,
            "sha256": file_hash,
        }
    except Exception as e:
        logger.error("Hot backup failed for %s: %s", src_path, e)
        return {"success": False, "error": str(e)}


def create_backup(target_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Creates a full timestamped snapshot of news.db and vectors.db.
    """
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_base = target_dir or os.path.join(settings.DB_DIR, "backups")
    snapshot_dir = os.path.join(backup_base, f"snapshot_{timestamp}")
    os.makedirs(snapshot_dir, exist_ok=True)

    dbs_to_backup = [
        {"name": "news.db", "src": settings.DATABASE_PATH},
        {"name": "vectors.db", "src": os.path.join(settings.DB_DIR, "vectors.db")},
    ]

    manifest = {
        "timestamp": timestamp,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "app_version": settings.APP_VERSION,
        "files": {},
        "status": "success",
    }

    all_ok = True
    for db_info in dbs_to_backup:
        name = db_info["name"]
        src = db_info["src"]
        dst = os.path.join(snapshot_dir, name)

        if not os.path.exists(src):
            logger.warning("Source database %s does not exist; skipping.", src)
            manifest["files"][name] = {"present": False, "note": "file not found on disk"}
            continue

        res = hot_backup_sqlite(src, dst)
        if res["success"]:
            manifest["files"][name] = {
                "present": True,
                "size_bytes": res["size_bytes"],
                "sha256": res["sha256"],
                "integrity": "ok",
            }
            logger.info("Successfully backed up %s (Size: %d bytes, SHA256: %s)", name, res["size_bytes"], res["sha256"][:12])
        else:
            all_ok = False
            manifest["files"][name] = {"present": True, "error": res["error"]}
            logger.error("Failed to backup %s: %s", name, res["error"])

    manifest["status"] = "success" if all_ok else "partial_failure"

    # Write manifest
    manifest_path = os.path.join(snapshot_dir, "backup_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    logger.info("Backup complete. Snapshot stored in %s", snapshot_dir)
    return {
        "snapshot_dir": snapshot_dir,
        "manifest": manifest,
        "success": all_ok,
    }


def restore_backup(snapshot_dir: str, target_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Restores news.db and vectors.db from a snapshot directory with SHA-256 verification.
    """
    manifest_path = os.path.join(snapshot_dir, "backup_manifest.json")
    if not os.path.exists(manifest_path):
        return {"success": False, "error": f"Manifest not found in {snapshot_dir}"}

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    dest_dir = target_dir or settings.DB_DIR
    os.makedirs(dest_dir, exist_ok=True)

    restore_report = {"files_restored": [], "errors": []}

    for name, meta in manifest.get("files", {}).items():
        if not meta.get("present"):
            continue

        src_file = os.path.join(snapshot_dir, name)
        dst_file = os.path.join(dest_dir, name)

        if not os.path.exists(src_file):
            restore_report["errors"].append(f"Backup file {src_file} missing from snapshot")
            continue

        # Verify integrity and checksum before restore
        curr_hash = calculate_sha256(src_file)
        if curr_hash != meta.get("sha256"):
            restore_report["errors"].append(f"Checksum mismatch for {name}: expected {meta.get('sha256')}, got {curr_hash}")
            continue

        if not verify_sqlite_integrity(src_file):
            restore_report["errors"].append(f"SQLite integrity check failed on {src_file}")
            continue

        # Safe atomic copy
        tmp_dst = dst_file + ".tmp_restore"
        shutil.copy2(src_file, tmp_dst)
        if os.path.exists(dst_file):
            os.replace(tmp_dst, dst_file)
        else:
            os.rename(tmp_dst, dst_file)

        logger.info("Successfully restored %s to %s", name, dst_file)
        restore_report["files_restored"].append(name)

    is_ok = len(restore_report["errors"]) == 0 and len(restore_report["files_restored"]) > 0
    restore_report["success"] = is_ok
    return restore_report


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        if len(sys.argv) < 3:
            print("Usage: python backup_restore.py restore <snapshot_dir>")
            sys.exit(1)
        res = restore_backup(sys.argv[2])
        print(json.dumps(res, indent=2))
        sys.exit(0 if res.get("success") else 1)
    else:
        res = create_backup()
        print(json.dumps(res["manifest"], indent=2))
        sys.exit(0 if res.get("success") else 1)
