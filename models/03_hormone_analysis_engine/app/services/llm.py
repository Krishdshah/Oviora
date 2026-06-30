"""
Oviora Hormone Intelligence
LLM Service

Primary: Google Gemini
Fallback: Groq
Final Fallback: Rule Engine
"""

from __future__ import annotations

import json
from typing import Any

from google import genai
from groq import Groq

from app.config import settings
from app.logger import logger
from app.services.rule_engine import rule_engine


SYSTEM_PROMPT = """
You are Oviora Hormone Intelligence.

Use ONLY the supplied structured JSON.
Do not diagnose disease.
Do not invent biomarkers.
Do not prescribe medication.
Return concise JSON-compatible clinical explanations.
"""


class LLMService:
    def __init__(self) -> None:
        self.gemini = (
            genai.Client(api_key=settings.GEMINI_API_KEY)
            if settings.GEMINI_API_KEY
            else None
        )

        self.groq = (
            Groq(api_key=settings.GROQ_API_KEY)
            if settings.GROQ_API_KEY
            else None
        )

        from app.config import BASE_DIR
        system_prompt_path = BASE_DIR / "system_prompt.txt"
        user_prompt_path = BASE_DIR / "user_prompt_template.txt"

        self.system_prompt = system_prompt_path.read_text(encoding="utf-8").strip() if system_prompt_path.exists() else SYSTEM_PROMPT
        self.user_prompt_template = user_prompt_path.read_text(encoding="utf-8").strip() if user_prompt_path.exists() else ""

    def _build_user_prompt(self, parsed_report: dict) -> str:
        if not self.user_prompt_template:
            return json.dumps(parsed_report, indent=2)

        biomarkers = parsed_report.get("biomarkers", [])

        # Format biomarkers list
        biomarkers_str = "\n".join([
            f"- {b['canonical_name']}: {b.get('value')} {b.get('unit','') or ''} ({b.get('status','unknown')})"
            for b in biomarkers
        ])

        # Derived metrics
        data = rule_engine._index(biomarkers)
        ratio = rule_engine.calculate_lh_fsh_ratio(data)
        derived_str = f"LH/FSH Ratio: {ratio}" if ratio else "None"

        # Abnormal findings
        abnormal = [
            f"- {b['canonical_name']}: {b.get('value')} {b.get('unit','') or ''} (Status: {b.get('status')})"
            for b in biomarkers if b.get("status") in ("high", "low")
        ]
        abnormal_str = "\n".join(abnormal) if abnormal else "None"

        # Missing biomarkers
        missing_str = ", ".join(parsed_report.get("missing_biomarkers", [])) or "None"

        # Metadata
        metadata = parsed_report.get("metadata", {})
        metadata_str = "\n".join([f"{k}: {v}" for k, v in metadata.items() if v]) or "None"

        # Reference ranges
        ranges = [
            f"- {b['canonical_name']}: {b.get('reference_range') or 'None'}"
            for b in biomarkers
        ]
        ranges_str = "\n".join(ranges)

        # Confidence
        parser_conf = parsed_report.get("overall_parser_confidence", 1.0)
        ocr_conf = rule_engine.confidence(biomarkers)
        overall_conf = round((parser_conf + ocr_conf) / 2, 3)

        prompt = self.user_prompt_template
        prompt = prompt.replace("{{PATIENT_METADATA}}", metadata_str)
        prompt = prompt.replace("{{BIOMARKERS}}", biomarkers_str)
        prompt = prompt.replace("{{DERIVED_METRICS}}", derived_str)
        prompt = prompt.replace("{{REFERENCE_RANGES}}", ranges_str)
        prompt = prompt.replace("{{ABNORMAL_FINDINGS}}", abnormal_str)
        prompt = prompt.replace("{{MISSING_BIOMARKERS}}", missing_str)
        prompt = prompt.replace("{{PARSER_CONFIDENCE}}", f"{parser_conf:.3f}")
        prompt = prompt.replace("{{OCR_CONFIDENCE}}", f"{ocr_conf:.3f}")
        prompt = prompt.replace("{{OVERALL_CONFIDENCE}}", f"{overall_conf:.3f}")

        return prompt

    def _clean_and_parse_json(self, text: str) -> dict:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())

    def _gemini(self, payload: dict) -> dict:
        if not self.gemini:
            raise RuntimeError("Gemini unavailable")

        user_prompt = self._build_user_prompt(payload)
        response = self.gemini.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=[
                self.system_prompt,
                user_prompt,
            ],
        )

        return {
            "provider": "gemini",
            "content": self._clean_and_parse_json(response.text),
        }

    def _groq(self, payload: dict) -> dict:
        if not self.groq:
            raise RuntimeError("Groq unavailable")

        user_prompt = self._build_user_prompt(payload)
        completion = self.groq.chat.completions.create(
            model=settings.GROQ_MODEL,
            temperature=settings.TEMPERATURE,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return {
            "provider": "groq",
            "content": self._clean_and_parse_json(completion.choices[0].message.content),
        }

    def generate(self, parsed_report: dict[str, Any]) -> dict[str, Any]:
        for attempt in range(settings.MAX_RETRIES):
            try:
                logger.info("Gemini attempt %d", attempt + 1)
                return self._gemini(parsed_report)
            except Exception as exc:
                logger.warning("Gemini failed: %s", exc)

        try:
            logger.info("Switching to Groq fallback")
            return self._groq(parsed_report)
        except Exception as exc:
            logger.error("Groq failed: %s", exc)

        logger.warning("Running deterministic rule engine fallback")

        return {
            "provider": "rule_engine",
            "content": rule_engine.analyze(parsed_report),
        }


llm = LLMService()
