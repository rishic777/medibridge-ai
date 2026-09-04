"""OCR abstraction for uploaded lab reports / documents."""
from __future__ import annotations

from abc import ABC, abstractmethod

from app.core.config import settings
from app.core.logging import logger


class OCRProvider(ABC):
    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        raise NotImplementedError


class PaddleOCRProvider(OCRProvider):
    def extract_text(self, file_path: str) -> str:
        try:
            from paddleocr import PaddleOCR  # type: ignore

            ocr = PaddleOCR(use_angle_cls=True, lang="en")
            result = ocr.ocr(file_path, cls=True)
            lines = [line[1][0] for block in result for line in block]
            return "\n".join(lines)
        except ImportError:
            logger.warning("paddleocr not installed; returning empty OCR text. `pip install paddleocr paddlepaddle`.")
            return ""


class TesseractOCRProvider(OCRProvider):
    def extract_text(self, file_path: str) -> str:
        try:
            import pytesseract  # type: ignore
            from PIL import Image  # type: ignore

            return pytesseract.image_to_string(Image.open(file_path))
        except ImportError:
            logger.warning("pytesseract/Pillow not installed; returning empty OCR text.")
            return ""


class OCRService:
    def __init__(self, provider: OCRProvider | None = None):
        if provider is not None:
            self.provider = provider
        elif settings.OCR_PROVIDER == "tesseract":
            self.provider = TesseractOCRProvider()
        else:
            self.provider = PaddleOCRProvider()

    def extract_text(self, file_path: str) -> str:
        return self.provider.extract_text(file_path)
