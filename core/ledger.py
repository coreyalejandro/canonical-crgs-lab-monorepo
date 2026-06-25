"""
core/ledger.py — Merkle-style Append-Only Cryptographic Ledger

Phase 13 Build Contract — Section II.

Every human-in-the-loop event is SHA-256 hashed and appended to a
tamper-evident local log. Returns the entry hash for UI display.
"""

import hashlib
import json
import os
import time


class MerkleLedger:
    def __init__(self, filepath: str = "./output/audit/tlc_audit.log") -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.filepath = filepath

    def append_signature(
        self, event_type: str, user_id: str, payload: dict
    ) -> str:
        """
        Append a signed entry and return its SHA-256 hash.
        The log is append-only — no entry is ever modified.
        """
        entry = {
            "event":     event_type,
            "user":      user_id,
            "timestamp": time.time(),
            "payload":   payload,
        }
        entry_bytes = json.dumps(entry, sort_keys=True).encode("utf-8")
        entry_hash  = hashlib.sha256(entry_bytes).hexdigest()
        record = json.dumps({"hash": entry_hash, "data": entry})
        with open(self.filepath, "a") as fh:
            fh.write(record + "\n")
        return entry_hash
