"""
core/ledger.py — Merkle-chained Append-Only Cryptographic Ledger

Phase 14 / v15 Build Contract — Section II.

Each entry's hash includes the previous entry's hash, forming a
tamper-evident chain. validate_chain() is called on boot to confirm
integrity before any pipeline execution.

Hash construction per entry:
  sha256(json({event, user, timestamp, payload, previous_hash}))

An empty chain has last_hash = None. The genesis entry uses
previous_hash = "0" * 64 (64-zero sentinel).
"""

import hashlib
import json
import os
import time


class MerkleLedger:
    def __init__(self, filepath: str = "./output/audit/tlc_audit.log") -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.filepath = filepath
        self.last_hash: str | None = self._load_last_hash()

    # ── Private ───────────────────────────────────────────────────────────────

    def _load_last_hash(self) -> str | None:
        """Read the final hash from an existing log so chaining survives restarts."""
        if not os.path.exists(self.filepath):
            return None
        last: str | None = None
        with open(self.filepath, "r") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    last = record.get("hash")
                except json.JSONDecodeError:
                    continue
        return last

    # ── Public ────────────────────────────────────────────────────────────────

    def append_signature(
        self, event_type: str, user_id: str, payload: dict
    ) -> str:
        """
        Append a Merkle-chained entry and return its SHA-256 hash.
        Each entry's hash includes the previous entry's hash.
        The log is append-only — no entry is ever modified.
        """
        previous_hash = self.last_hash if self.last_hash is not None else "0" * 64
        entry = {
            "event":         event_type,
            "user":          user_id,
            "timestamp":     time.time(),
            "payload":       payload,
            "previous_hash": previous_hash,
        }
        entry_bytes = json.dumps(entry, sort_keys=True).encode("utf-8")
        entry_hash  = hashlib.sha256(entry_bytes).hexdigest()
        record      = json.dumps({"hash": entry_hash, "data": entry})
        with open(self.filepath, "a") as fh:
            fh.write(record + "\n")
        self.last_hash = entry_hash
        return entry_hash

    def validate_chain(self) -> bool:
        """
        Walk every entry in the log and verify the Merkle chain.
        Returns True if the chain is intact.
        Raises ValueError with the offending entry index on first break.
        Called on boot before any pipeline execution.
        """
        if not os.path.exists(self.filepath):
            return True  # empty ledger is valid

        records: list[dict] = []
        with open(self.filepath, "r") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                records.append(json.loads(line))

        if not records:
            return True

        for i, record in enumerate(records):
            data       = record["data"]
            stored     = record["hash"]
            recomputed = hashlib.sha256(
                json.dumps(data, sort_keys=True).encode("utf-8")
            ).hexdigest()
            if recomputed != stored:
                raise ValueError(
                    f"Merkle chain broken at entry {i}: "
                    f"stored={stored[:16]}… recomputed={recomputed[:16]}…"
                )
            # Verify chaining: entry[i].previous_hash == entry[i-1].hash
            if i > 0:
                expected_prev = records[i - 1]["hash"]
                actual_prev   = data.get("previous_hash", "")
                if actual_prev != expected_prev:
                    raise ValueError(
                        f"Merkle chain link broken at entry {i}: "
                        f"expected previous_hash={expected_prev[:16]}… "
                        f"got {actual_prev[:16]}…"
                    )

        return True
