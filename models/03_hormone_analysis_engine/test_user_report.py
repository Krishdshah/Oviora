#!/usr/bin/env python3
"""
Oviora Hormone Intelligence - Test User Report

Bypasses the image OCR stage by directly feeding the exact OCR text
extracted from the ZRT Laboratory report to the parser, normalizer, 
rule engine, and Groq fallback.
"""

import json
from pathlib import Path
from unittest.mock import patch
from app.services.fallback import fallback_engine
from app.services.formatter import formatter

OCR_TEXT = [
    "TEST REPORT 8605 SW Creekside Place",
    "Beaverton, OR 97008",
    "Phone: 503-466-2445 Fax: 503-466-1636",
    "Samples Collected",
    "Serum - 08/12/19 08:00",
    "Samples Received",
    "08/16/2019",
    "Report Date",
    "08/18/2019",
    "# 2019 08 16 001 Se",
    "Ordering Provider:",
    "Dr Getuwell",
    "Patient Name: Female Serum Hormones Advanced",
    "Patient Phone Number: 555 555 5555",
    "Gender",
    "Female",
    "DOB",
    "7/1/1970 (49 yrs)",
    "Last Menses",
    "07/21/2019",
    "Menses Status",
    "Pre-menopausal - Irregular",
    "Height",
    "5 ft 8 in",
    "Weight",
    "155 lb",
    "Waist",
    "30 in",
    "BMI",
    "23.6",
    "TEST NAME RESULTS | 08/12/19 RANGE",
    "Serum Steroids/Peptides",
    "Estradiol 120 43-180 pg/mL Premeno-luteal or ERT",
    "Progesterone 5 3.3-22.5 ng/mL Premeno-luteal or PgRT",
    "Ratio: Pg/E2 42 L Pg/E2 (optimal 100-500)",
    "Testosterone 40 20-130 ng/dL Premeno-luteal or TRT",
    "DHEAS 110 40-290 µg/dL",
    "Cortisol 12.3 8.5-19.8 µg/dL (morning), 3.3-8.5 (eve/night)",
    "SHBG 95 15-120 nmol/L",
    "Serum Thyroids",
    "Free T4 0.8 0.7-2.5 ng/dL",
    "Free T3 2.8 2.4-4.2 pg/mL",
    "TSH 5 H 0.5-3.0 µU/mL",
    "TPOab 250 H <70 IU/mL",
    "Serum",
    "LH 10 0.5-12.8 U/L Premenopausal-luteal",
    "FSH 15 H 0.6-8.0 U/L Premenopausal-luteal",
    "Ferritin 25 16.0-145.7 ng/mL",
    "Therapies",
    "None"
]

def main():
    mock_ocr = [{"text": line, "confidence": 0.99} for line in OCR_TEXT]
    
    print("Testing ZRT Laboratory Report...")
    print("Running parser, biomarker normalizer, and LLM analyzer...")
    
    with patch("app.services.ocr.ocr_service.process", return_value=mock_ocr):
        result = fallback_engine.analyze_file("dummy_path.png")
        
    if not result.get("success"):
        print(f"Analysis failed: {result.get('error')}")
        return
        
    formatted = formatter.build(result)
    
    print("\n=== Finalized Structured Analysis Report ===")
    print(json.dumps(formatted, indent=2))
    print("============================================")
    
    print("\n=== Raw Analysis Result ===")
    print(json.dumps(result, indent=2))
    print("===========================")

if __name__ == "__main__":
    main()
