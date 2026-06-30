#!/usr/bin/env python3
"""
Oviora Hormone Intelligence - Integration Test Script

Generates a mock report image, starts the FastAPI server,
uploads the image, triggers analysis, and displays the results.
"""

import sys
import time
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

def generate_mock_report(filename="test_report.png"):
    print("Generating mock report image...")
    # Create a white image
    img = Image.new("RGB", (600, 300), "white")
    draw = ImageDraw.Draw(img)
    
    # Text simulating a hormone panel laboratory report
    report_text = (
        "OVIORA HORMONE PANEL REPORT\n"
        "Patient: Jane Doe | Age: 28\n"
        "Date: 2026-06-30\n\n"
        "TSH: 2.5 uIU/mL\n"
        "LH: 8.5 mIU/mL\n"
        "FSH: 3.2 mIU/mL\n"
        "AMH: 3.5 ng/mL\n"
        "Testosterone: 45 ng/dL\n"
    )
    
    # Use default font (works everywhere without external dependencies)
    draw.text((30, 30), report_text, fill="black")
    img.save(filename)
    print(f"Mock report saved as: {filename}")

def run_test():
    report_file = "test_report.png"
    generate_mock_report(report_file)
    
    server_process = None
    try:
        # Start uvicorn server in a subprocess
        print("\nStarting FastAPI server in the background...")
        server_process = subprocess.Popen(
            [".venv/bin/python", "-m", "uvicorn", "app.main:app", "--port", "8000"],
            text=True
        )
        
        # Wait for server to boot up by querying health endpoint
        import requests
        print("Waiting for server to become ready (loading PaddleOCR models)...")
        ready = False
        for _ in range(30):
            try:
                r = requests.get("http://127.0.0.1:8000/health", timeout=1)
                if r.status_code == 200:
                    ready = True
                    break
            except requests.RequestException:
                pass
            time.sleep(1)
            
        if not ready:
            print("Error: Server failed to start in time.")
            return
            
        print("Server is ready!")

        # 1. Upload report image
        print("\nStep 1: Uploading report image to /upload...")
        with open(report_file, "rb") as f:
            upload_resp = requests.post(
                "http://127.0.0.1:8000/upload",
                files={"file": (report_file, f, "image/png")}
            )
        
        if upload_resp.status_code != 201:
            print(f"Upload failed: {upload_resp.text}")
            return
            
        upload_data = upload_resp.json()
        file_id = upload_data["file_id"]
        print(f"Upload successful. Received file ID: {file_id}")

        # 2. Analyze report
        print(f"\nStep 2: Triggering analysis for {file_id}...")
        analyze_resp = requests.post(f"http://127.0.0.1:8000/analyze/{file_id}")
        
        if analyze_resp.status_code != 200:
            print(f"Analysis failed: {analyze_resp.text}")
            return
            
        print("\nAnalysis successful! Full JSON response below:")
        print("=" * 80)
        import json
        print(json.dumps(analyze_resp.json(), indent=2))
        print("=" * 80)
        
    finally:
        # Shutdown server
        if server_process:
            print("\nShutting down backend server...")
            server_process.terminate()
            server_process.wait()
        
        # Cleanup mock file
        if Path(report_file).exists():
            Path(report_file).unlink()
            print("Cleaned up temporary test files.")

if __name__ == "__main__":
    run_test()
