"""
Oviora Hormone Intelligence
OCR Service

Production-oriented OCR wrapper around PaddleOCR with
basic image preprocessing and PDF support.
"""

from __future__ import annotations

import os
from pathlib import Path

# Override HOME/USERPROFILE so PaddleX uses our local directory BEFORE imports
_model_dir = Path(__file__).resolve().parent.parent.parent.parent.parent / "backend" / "models" / "paddleocr"
_model_dir.mkdir(parents=True, exist_ok=True)
os.environ["HOME"] = str(_model_dir)
os.environ["USERPROFILE"] = str(_model_dir)
os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"

import cv2
import numpy as np
from paddleocr import PaddleOCR
from pdf2image import convert_from_path
from PIL import Image
from typing import Any

from app.config import settings
from app.logger import logger

class OCRService:
    def __init__(self) -> None:
        self.ocr = PaddleOCR(
            use_textline_orientation=True,
            lang=settings.OCR_LANGUAGE,
            device="gpu" if settings.OCR_USE_GPU else "cpu",
        )

    @staticmethod
    def preprocess(image: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.fastNlMeansDenoising(gray)
        gray = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def _pil_to_cv(image: Image.Image) -> np.ndarray:
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    def _extract(self, image: np.ndarray) -> list[dict[str, Any]]:
        processed = self.preprocess(image)
        result = self.ocr.ocr(processed)

        lines: list[dict[str, Any]] = []

        if not result:
            return lines

        for page in result:
            if page is None or not isinstance(page, dict):
                continue
            texts = page.get("rec_texts", [])
            scores = page.get("rec_scores", [])
            for text, score in zip(texts, scores):
                lines.append(
                    {
                        "text": str(text),
                        "confidence": float(score),
                    }
                )
        return lines

    def from_image(self, image_path: str | Path) -> list[dict[str, Any]]:
        logger.info("Running OCR on image: %s", image_path)
        img = cv2.imread(str(image_path))
        if img is None:
            raise FileNotFoundError(image_path)
        return self._extract(img)

    def from_pdf(self, pdf_path: str | Path) -> list[dict[str, Any]]:
        logger.info("Running OCR on PDF: %s", pdf_path)
        pages = convert_from_path(str(pdf_path), dpi=300)
        output: list[dict[str, Any]] = []

        for page_no, page in enumerate(pages, start=1):
            lines = self._extract(self._pil_to_cv(page))
            for line in lines:
                line["page"] = page_no
            output.extend(lines)

        return output

    def process(self, file_path: str | Path) -> list[dict[str, Any]]:
        suffix = Path(file_path).suffix.lower()
        if suffix == ".pdf":
            return self.from_pdf(file_path)
        return self.from_image(file_path)


ocr_service = OCRService()
