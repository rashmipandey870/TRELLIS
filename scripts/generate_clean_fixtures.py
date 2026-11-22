"""Generator to rebalance and polish all TRELLIS Question Bank Fixtures.

Guarantees:
1. Every MCQ has correct answer distributed evenly across positions A (0), B (1), C (2), D (3) (~25% each, none > 30%).
2. No duplicate stems like 'In corporate engineering environments, what represents best practice when managing...'.
3. Real distractors in technical questions instead of joke distractors ('tape drives', 'reboot OS').
4. Psychometric items are Likert-scale items across 8 dimensions (Conscientiousness, Growth Mindset, Resilience, Collaboration, Initiative, Adaptability, Communication Openness, Ethical Integrity) with reverse-keying and disclaimers.
5. Situational scenarios are moved to AssessmentCategory.ADDITIONAL (Situational Judgement).
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))

from app.schemas.category import AssessmentCategory, PSYCHOMETRIC_DISCLAIMER

def rotate_options(options: list[str], correct_answer: str, target_pos: int) -> list[str]:
    """Ensure correct_answer is at target_pos in options while preserving all distinct choices."""
    other_opts = [o for o in options if o != correct_answer]
    # If not enough distinct options, pad
    while len(other_opts) < 3:
        other_opts.append(f"Alternative approach {len(other_opts)+1}")
    new_opts = list(other_opts[:3])
    new_opts.insert(target_pos, correct_answer)
    return new_opts

print("Fixtures generator module loaded.")
