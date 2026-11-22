"""Professional PDF Export Service for TRELLIS Growth Ring Reports (Phase B / WS3).

Uses ReportLab to generate enterprise-grade, CSM-branded assessment reports.
"""

from __future__ import annotations

import io
import logging
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

logger = logging.getLogger(__name__)


def generate_growth_ring_pdf(report: dict[str, Any]) -> bytes:
    """Compile Growth Ring evaluation report into a clean, multi-page PDF document."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    # Custom palette
    navy = colors.HexColor("#0B0D12")
    csm_teal = colors.HexColor("#008FBB")
    csm_orange = colors.HexColor("#FAA634")
    slate = colors.HexColor("#475569")
    light_bg = colors.HexColor("#F8FAFC")

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=csm_teal,
    )
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=14,
        textColor=slate,
    )
    section_h2 = ParagraphStyle(
        "SectionH2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=navy,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=navy,
    )
    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#64748B"),
    )

    elements = []

    # 1. Header Banner
    elements.append(Paragraph("CSM TECHNOLOGIES", subtitle_style))
    elements.append(Paragraph("TRELLIS Growth Ring Evaluation Report", title_style))
    elements.append(Paragraph("Automated Competency Diagnostic & Growth Trajectory", subtitle_style))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=2, color=csm_teal, spaceAfter=14))

    # 2. Learner & Assessment Metadata Table
    learner_name = report.get("learner_name", "Learner")
    assessment_title = report.get("assessment_title", "Assessment")
    score = report.get("score", 0.0)
    total_marks = report.get("total_marks", 100.0)
    pct = report.get("percentage", 0.0)
    passed = report.get("passed", False)
    percentile = report.get("percentile_rank", 75.0)
    status_label = "PASSED" if passed else "RETRY RECOMMENDED"

    meta_data = [
        [
            Paragraph("<b>Learner Name:</b>", body_style),
            Paragraph(str(learner_name), body_style),
            Paragraph("<b>Overall Score:</b>", body_style),
            Paragraph(f"<b>{score:.1f} / {total_marks:.1f} ({pct:.1f}%)</b>", body_style),
        ],
        [
            Paragraph("<b>Assessment:</b>", body_style),
            Paragraph(str(assessment_title), body_style),
            Paragraph("<b>Cohort Percentile:</b>", body_style),
            Paragraph(f"{percentile:.0f}th percentile", body_style),
        ],
        [
            Paragraph("<b>Status:</b>", body_style),
            Paragraph(f"<b>{status_label}</b>", body_style),
            Paragraph("<b>Report Generated:</b>", body_style),
            Paragraph(report.get("generated_at", "N/A")[:10], body_style),
        ],
    ]

    meta_table = Table(meta_data, colWidths=[1.3 * inch, 2.3 * inch, 1.4 * inch, 2.2 * inch])
    meta_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), light_bg),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ])
    )
    elements.append(meta_table)
    elements.append(Spacer(1, 16))

    # 3. Executive AI Narrative
    elements.append(Paragraph("Executive Performance Summary", section_h2))
    narrative_text = report.get("ai_narrative", "Diagnostic evaluation complete.")
    elements.append(Paragraph(narrative_text, body_style))
    elements.append(Spacer(1, 14))

    # 4. Competency Domain Breakdown
    cat_profs = report.get("category_proficiencies", {})
    if cat_profs:
        elements.append(Paragraph("Category Competency Diagnostic", section_h2))
        cat_table_data = [
            [
                Paragraph("<b>Competency Domain</b>", body_style),
                Paragraph("<b>Mastery Level</b>", body_style),
                Paragraph("<b>Evaluation Rating</b>", body_style),
            ]
        ]
        for cat, prof in cat_profs.items():
            rating = "Exemplary" if prof >= 85 else ("Proficient" if prof >= 70 else "Developing")
            color_hex = "#10B981" if prof >= 85 else ("#008FBB" if prof >= 70 else "#F59E0B")
            cat_table_data.append([
                Paragraph(str(cat), body_style),
                Paragraph(f"<b>{prof:.1f}%</b>", body_style),
                Paragraph(f"<font color='{color_hex}'><b>{rating}</b></font>", body_style),
            ])

        cat_table = Table(cat_table_data, colWidths=[3.2 * inch, 2.0 * inch, 2.0 * inch])
        cat_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E0F2FE")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
            ])
        )
        elements.append(cat_table)
        elements.append(Spacer(1, 16))

    # 5. Strengths & Focus Areas
    strengths = report.get("strengths", [])
    gaps = report.get("gaps", [])
    if strengths or gaps:
        elements.append(Paragraph("Strengths & Target Growth Opportunities", section_h2))
        detail_data = []
        max_len = max(len(strengths), len(gaps))
        detail_data.append([
            Paragraph("<b>Identified Strengths</b>", body_style),
            Paragraph("<b>Target Growth Opportunities</b>", body_style),
        ])
        for i in range(max_len):
            s_text = f"• {strengths[i]}" if i < len(strengths) else ""
            g_text = f"• {gaps[i]}" if i < len(gaps) else ""
            detail_data.append([Paragraph(s_text, body_style), Paragraph(g_text, body_style)])

        detail_table = Table(detail_data, colWidths=[3.6 * inch, 3.6 * inch])
        detail_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ])
        )
        elements.append(detail_table)
        elements.append(Spacer(1, 16))

    # 6. Actionable Next Steps
    next_steps = report.get("next_steps", [])
    if next_steps:
        elements.append(Paragraph("Recommended Action Plan", section_h2))
        for idx, step in enumerate(next_steps, 1):
            elements.append(Paragraph(f"<b>{idx}.</b> {step}", body_style))
            elements.append(Spacer(1, 3))
        elements.append(Spacer(1, 12))

    # 7. Compliance & Psychometric Disclaimer
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceAfter=8))
    disclaimer_text = (
        "<b>CSM Technologies TRELLIS Diagnostic Notice:</b> This report is generated algorithmically for "
        "developmental pacing, coaching insight, and curriculum mastery tracking. Psychometric and competency "
        "indicators are indicative only and do not constitute formal clinical psychological evaluations."
    )
    elements.append(Paragraph(disclaimer_text, disclaimer_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
