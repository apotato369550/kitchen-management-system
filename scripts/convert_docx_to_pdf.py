#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

def convert_docx_to_pdf():
    # Define paths
    docx_dir = Path(__file__).parent.parent / "data" / "docx_files"
    pdf_output_dir = Path(__file__).parent.parent / "data" / "pdfs"

    # Create output directory
    pdf_output_dir.mkdir(parents=True, exist_ok=True)

    # Find all .docx files in docx_files folder
    docx_files = list(docx_dir.glob("*.docx"))

    if not docx_files:
        print("No .docx files found.")
        return

    print(f"Found {len(docx_files)} .docx file(s). Converting...")

    for docx_file in docx_files:
        try:
            # Use LibreOffice to convert
            subprocess.run(
                ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", str(pdf_output_dir), str(docx_file)],
                check=True,
                capture_output=True
            )
            pdf_filename = docx_file.stem + ".pdf"
            print(f"✓ Converted: {docx_file.name} → {pdf_filename}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to convert {docx_file.name}: {e.stderr.decode()}")
        except FileNotFoundError:
            print("✗ LibreOffice not found. Install it with: sudo apt-get install libreoffice")
            return

    print(f"Conversion complete. PDFs saved to: {pdf_output_dir}")

if __name__ == "__main__":
    convert_docx_to_pdf()
