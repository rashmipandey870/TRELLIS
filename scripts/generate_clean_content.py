"""Generator script for 100% unique English & Communication and Situational Judgement questions (Phase C).

Produces:
- 40 English & Communication questions (grammar, vocab, reading comp, sentence correction, professional email)
- 50 Situational Judgement questions (50 unique scenarios with scored options)
- 48 Psychometric Likert questions (already verified 8-dimension profiles)
Total: 138 questions, 100% unique stems, balanced ~25% answer keys.
"""

import sys
from pathlib import Path

# Add backend to sys.path
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "backend"))

from app.schemas.category import AssessmentCategory, PSYCHOMETRIC_DISCLAIMER

# Read existing psychometric Likert items
from scripts.fixtures.communication_psychometric import COMMUNICATION_PSYCHOMETRIC_QUESTIONS as EXISTING

likert_items = [q for q in EXISTING if q.get("category") == "Psychometric"]
assert len(likert_items) == 48, f"Expected 48 Likert items, got {len(likert_items)}"

print(f"Preserved {len(likert_items)} Psychometric Likert items.")
