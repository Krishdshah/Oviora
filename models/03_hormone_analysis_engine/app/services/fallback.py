"""
Oviora Hormone Intelligence
Fallback Orchestrator

Coordinates graceful degradation across the pipeline.
"""

from __future__ import annotations

from typing import Any

from app.logger import logger
from app.services.ocr import ocr_service
from app.services.parser import parser
from app.services.llm import llm
from app.services.rule_engine import rule_engine


class FallbackEngine:
    def analyze_file(self, file_path: str) -> dict[str, Any]:
        stages = {
            "ocr": False,
            "parser": False,
            "llm": False,
            "rule_engine": False,
        }

        try:
            ocr_output = ocr_service.process(file_path)
            stages["ocr"] = True
        except Exception as exc:
            logger.exception("OCR failed: %s", exc)
            return {
                "success": False,
                "error": "OCR processing failed.",
                "stages": stages,
            }

        try:
            parsed = parser.parse(ocr_output)
            stages["parser"] = True
        except Exception as exc:
            logger.exception("Parser failed: %s", exc)
            return {
                "success": False,
                "error": "Report parsing failed.",
                "ocr_output": ocr_output,
                "stages": stages,
            }

        try:
            result = llm.generate(parsed)
            if result.get("provider") == "rule_engine":
                stages["rule_engine"] = True
            else:
                stages["llm"] = True
            return {
                "success": True,
                "provider": result.get("provider"),
                "analysis": result.get("content"),
                "parsed_report": parsed,
                "stages": stages,
            }
        except Exception as exc:
            logger.exception("Unexpected LLM failure: %s", exc)

        logger.warning("Using deterministic fallback.")

        stages["rule_engine"] = True

        return {
            "success": True,
            "provider": "rule_engine",
            "analysis": rule_engine.analyze(parsed),
            "parsed_report": parsed,
            "stages": stages,
        }


fallback_engine = FallbackEngine()
