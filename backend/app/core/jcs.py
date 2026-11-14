"""TRELLIS RFC 8785 JSON Canonicalization Scheme (JCS) & Hash Utilities.

RFC 8785 guarantees bit-for-bit deterministic serialization of JSON structures
independent of dictionary key insertion order, whitespace, or platform-specific
formatting variations.
"""

from __future__ import annotations

import hashlib
from typing import Any

import canonicaljson


def rfc8785_canonicalize(data: Any) -> bytes:
    """Serialize data into canonical JSON bytes strictly according to RFC 8785.

    - Lexicographically sorted member keys
    - Minimal whitespace (no trailing spaces, compact ':' and ',')
    - UTF-8 byte stream output
    """
    return canonicaljson.encode_canonical_json(data)


def compute_data_hash(payload: Any) -> str:
    """Compute deterministic SHA-256 hex digest of an RFC 8785 canonicalized evidence payload."""
    canonical_bytes = rfc8785_canonicalize(payload)
    return hashlib.sha256(canonical_bytes).hexdigest()


def compute_block_hash(
    org_id: str,
    employee_pseudonym: str,
    seq_num: int,
    prev_hash: str,
    data_hash: str,
) -> str:
    """Compute the immutable block hash for an entry in the Evidence Ledger.

    Formula (Section 23 / ADR-0003):
    Hash_n = SHA256(org_id || employee_pseudonym || seq_num || prev_hash || data_hash)
    """
    message = f"{org_id}:{employee_pseudonym}:{seq_num}:{prev_hash}:{data_hash}".encode()
    return hashlib.sha256(message).hexdigest()
