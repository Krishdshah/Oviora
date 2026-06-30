"""
Oviora Hormone Intelligence
Report Generator

Generates JSON, Markdown, HTML and PDF reports.
"""

from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

from app.config import settings


class ReportGenerator:
    def to_json(self, report: dict) -> str:
        return json.dumps(report, indent=2, ensure_ascii=False)

    def to_markdown(self, report: dict) -> str:
        lines = [
            "# Oviora Hormone Intelligence Report",
            "",
            f"**Provider:** {report.get('provider','N/A')}",
            f"**Confidence:** {report.get('analysis',{}).get('confidence_score','N/A') if isinstance(report.get('analysis'),dict) else 'N/A'}",
            "",
            "## Biomarkers",
            "",
        ]
        parsed = report.get("parsed_report", {})
        for b in parsed.get("biomarkers", []):
            lines.append(
                f"- **{b['canonical_name']}**: {b.get('value')} {b.get('unit','')} ({b.get('status','unknown')})"
            )
        lines.extend([
            "",
            "## Missing Biomarkers",
            ", ".join(parsed.get("missing_biomarkers", [])) or "None",
            "",
            "## Medical Disclaimer",
            "This report is an AI-assisted clinical decision-support prototype and is **not** a medical diagnosis. Consult a qualified healthcare professional for interpretation and treatment decisions."
        ])
        return "\n".join(lines)

    def to_html(self, report: dict) -> str:
        md = self.to_markdown(report)
        body = md.replace("\n", "<br>")
        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Oviora Report</title>
<style>
body{{font-family:Arial,sans-serif;margin:40px;line-height:1.6}}
h1{{color:#4b3fbf}}
table{{border-collapse:collapse}}
</style>
</head>
<body>{body}</body>
</html>"""

    def to_pdf(self, report: dict, output_path: str | Path) -> Path:
        doc = SimpleDocTemplate(str(output_path))
        styles = getSampleStyleSheet()
        story = [
            Paragraph("Oviora Hormone Intelligence Report", styles["Heading1"]),
            Paragraph(
                "This report is an AI-assisted clinical decision-support prototype and is not a diagnosis.",
                styles["BodyText"],
            ),
        ]
        parsed = report.get("parsed_report", {})
        for b in parsed.get("biomarkers", []):
            story.append(
                Paragraph(
                    f"<b>{b['canonical_name']}</b>: {b.get('value')} {b.get('unit','')} ({b.get('status','unknown')})",
                    styles["BodyText"],
                )
            )
        doc.build(story)
        return Path(output_path)

    def save(self, report: dict, report_id: str) -> dict[str, str]:
        settings.REPORT_FOLDER.mkdir(parents=True, exist_ok=True)

        json_path = settings.REPORT_FOLDER / f"{report_id}.json"
        md_path = settings.REPORT_FOLDER / f"{report_id}.md"
        html_path = settings.REPORT_FOLDER / f"{report_id}.html"
        pdf_path = settings.REPORT_FOLDER / f"{report_id}.pdf"

        json_path.write_text(self.to_json(report), encoding="utf-8")
        md_path.write_text(self.to_markdown(report), encoding="utf-8")
        html_path.write_text(self.to_html(report), encoding="utf-8")
        self.to_pdf(report, pdf_path)

        return {
            "json": str(json_path),
            "markdown": str(md_path),
            "html": str(html_path),
            "pdf": str(pdf_path),
        }


report_generator = ReportGenerator()
