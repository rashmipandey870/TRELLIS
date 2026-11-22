"""Canonical Assessment Categories and Disclaimers for TRELLIS (Phase B).

Defines the 7 enterprise policy categories + Additional:
1. Psychometric
2. Technical Knowledge
3. Coding
4. English & Communication
5. Quantitative Aptitude
6. Logical & Reasoning
7. Situational & Emotional Intelligence
8. Additional
"""

from __future__ import annotations

from enum import Enum


class AssessmentCategory(str, Enum):
    PSYCHOMETRIC = "Psychometric"
    TECHNICAL_KNOWLEDGE = "Technical Knowledge"
    CODING = "Coding"
    ENGLISH_COMMUNICATION = "English & Communication"
    QUANTITATIVE_APTITUDE = "Quantitative Aptitude"
    LOGICAL_REASONING = "Logical & Reasoning"
    SITUATIONAL_EI = "Situational & Emotional Intelligence"
    ADDITIONAL = "Additional"


PSYCHOMETRIC_DISCLAIMER = (
    "Indicative only, not clinical. This psychometric assessment is designed for "
    "professional development, coaching insight, and workplace preference mapping. "
    "It does not constitute psychological diagnosis or clinical psychometric profiling."
)
