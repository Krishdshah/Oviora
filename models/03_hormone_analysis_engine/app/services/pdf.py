"""
Oviora Hormone Intelligence
PDF Utilities

Utilities for reading and converting PDF laboratory reports.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

import fitz  # PyMuPDF
from pdf2image import convert_from_path
from PIL import Image


class PDFProcessor:
    def page_count(self, pdf_path: str | Path) -> int:
        with fitz.open(pdf_path) as doc:
            return len(doc)

    def metadata(self, pdf_path: str | Path) -> dict:
        with fitz.open(pdf_path) as doc:
            return doc.metadata

    def to_images(
        self,
        pdf_path: str | Path,
        dpi: int = 300,
    ) -> List[Image.Image]:
        return convert_from_path(
            str(pdf_path),
            dpi=dpi,
        )

    def save_pages(
        self,
        pdf_path: str | Path,
        output_dir: str | Path,
        dpi: int = 300,
        fmt: str = "png",
    ) -> list[Path]:
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)

        pages = self.to_images(pdf_path, dpi=dpi)

        saved: list[Path] = []

        for i, page in enumerate(pages, start=1):
            filename = output / f"page_{i}.{fmt}"
            page.save(filename)
            saved.append(filename)

        return saved

    def extract_text(self, pdf_path: str | Path) -> str:
        text = []

        with fitz.open(pdf_path) as doc:
            for page in doc:
                text.append(page.get_text())

        return "\n".join(text)


pdf_processor = PDFProcessor()
