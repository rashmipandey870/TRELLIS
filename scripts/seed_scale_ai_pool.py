"""Seed 200+ distinct verified questions into AIQuestionPool across all fields and modes."""

import os
import sys
import uuid
import hashlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.api.deps import get_sync_engine
from app.models.practice import AIQuestionPool
from app.ai.providers.procedural import ProceduralAIProvider

def compute_hash(txt: str) -> str:
    clean = " ".join((txt or "").strip().lower().split())
    return hashlib.sha256(clean.encode("utf-8")).hexdigest()[:16]

def main():
    engine = get_sync_engine()
    session = Session(engine)
    procedural = ProceduralAIProvider()

    existing_hashes = set(session.execute(select(AIQuestionPool.question_hash)).scalars().all())
    print(f"Existing questions in pool: {len(existing_hashes)}")

    fields = ["Python", "Java", "SQL", "DSA", "Web Dev", "Cloud", "Data Analytics", "Aptitude"]
    diffs = ["EASY", "MEDIUM", "HARD"]
    inserted = 0

    # 1. Generate 160 MCQs (20 per field across difficulties)
    for field in fields:
        for diff in diffs:
            for i in range(8):
                mcq = procedural.generate_mcq(field=field, difficulty=diff, seen_hashes=existing_hashes)
                q_text = mcq.question
                q_hash = compute_hash(q_text)
                if q_hash in existing_hashes:
                    continue
                existing_hashes.add(q_hash)

                q_data = {
                    "title": mcq.title,
                    "question": q_text,
                    "statement": q_text,
                    "difficulty": diff,
                    "field": field,
                    "options": mcq.options,
                    "correct_answer": mcq.correct_answer,
                    "explanation": mcq.explanation,
                    "hints": mcq.hints,
                    "question_hash": q_hash,
                }

                entry = AIQuestionPool(
                    id=str(uuid.uuid4()),
                    field=field,
                    category="Technical Knowledge",
                    difficulty=diff,
                    mode="MCQ",
                    language=None,
                    title=mcq.title,
                    question_hash=q_hash,
                    question_data_json=q_data,
                    provenance_json={"provider": "procedural", "served_from": "pool", "verified": True},
                    is_used=False,
                    verified=True,
                )
                session.add(entry)
                inserted += 1

    # 2. Generate 60 Coding problems across languages
    langs = [("Python", "python"), ("Java", "java"), ("Web Dev", "javascript"), ("SQL", "sql")]
    for field, lang in langs:
        for diff in diffs:
            for i in range(5):
                code = procedural.generate_coding(field=field, difficulty=diff, language=lang, seen_hashes=existing_hashes)
                q_text = code.question
                q_hash = compute_hash(q_text)
                if q_hash in existing_hashes:
                    continue
                existing_hashes.add(q_hash)

                q_data = {
                    "title": code.title,
                    "question": q_text,
                    "statement": q_text,
                    "difficulty": diff,
                    "field": field,
                    "language": lang,
                    "starter_code": code.starter_code,
                    "reference_solution": code.reference_solution,
                    "test_cases": code.test_cases,
                    "constraints": code.constraints,
                    "examples": code.examples,
                    "explanation": code.explanation,
                    "hints": code.hints,
                    "question_hash": q_hash,
                }

                entry = AIQuestionPool(
                    id=str(uuid.uuid4()),
                    field=field,
                    category="Coding",
                    difficulty=diff,
                    mode="CODING",
                    language=lang,
                    title=code.title,
                    question_hash=q_hash,
                    question_data_json=q_data,
                    provenance_json={"provider": "procedural", "served_from": "pool", "verified": True},
                    is_used=False,
                    verified=True,
                )
                session.add(entry)
                inserted += 1

    session.commit()
    total = session.query(AIQuestionPool).count()
    print(f"Successfully inserted {inserted} new pool questions! Total pool count in database: {total}")
    session.close()

if __name__ == "__main__":
    main()
