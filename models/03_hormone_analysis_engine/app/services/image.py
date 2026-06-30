"""
Oviora Hormone Intelligence
Image Utilities

Image preprocessing to improve OCR accuracy.
"""

from __future__ import annotations

import cv2
import numpy as np


class ImageProcessor:
    @staticmethod
    def to_gray(image: np.ndarray) -> np.ndarray:
        if len(image.shape) == 2:
            return image
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def denoise(image: np.ndarray) -> np.ndarray:
        gray = ImageProcessor.to_gray(image)
        return cv2.fastNlMeansDenoising(gray)

    @staticmethod
    def enhance_contrast(image: np.ndarray) -> np.ndarray:
        gray = ImageProcessor.to_gray(image)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        return clahe.apply(gray)

    @staticmethod
    def adaptive_threshold(image: np.ndarray) -> np.ndarray:
        gray = ImageProcessor.to_gray(image)
        return cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            15,
        )

    @staticmethod
    def upscale(image: np.ndarray, scale: float = 2.0) -> np.ndarray:
        return cv2.resize(
            image,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_CUBIC,
        )

    @staticmethod
    def deskew(image: np.ndarray) -> np.ndarray:
        gray = ImageProcessor.to_gray(image)
        coords = np.column_stack(np.where(gray < 255))
        if len(coords) == 0:
            return image

        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)

        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(
            image,
            matrix,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE,
        )

    @staticmethod
    def quality_score(image: np.ndarray) -> float:
        gray = ImageProcessor.to_gray(image)
        return round(float(cv2.Laplacian(gray, cv2.CV_64F).var()), 2)

    def preprocess(self, image: np.ndarray) -> np.ndarray:
        image = self.deskew(image)
        image = self.denoise(image)
        image = self.enhance_contrast(image)
        image = self.adaptive_threshold(image)
        image = self.upscale(image)
        return image


image_processor = ImageProcessor()
