#!/usr/bin/env python3
"""
Batch Quotation Generator
Reads CSV file and generates .docx and .pdf quotations
Usage: python3 quotation_batch.py <path_to_csv_file>
"""

import sys
import csv
from datetime import datetime
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import subprocess

# Constants
COMPANY_NAME = "Cebu Best Value Trading Corp."
COMPANY_LOCATION = "Cebu City"
COMPANY_PHONE = "032-2670573"
COMPANY_MOBILE_SUN = "09325314857"
COMPANY_MOBILE_GLOBE = "09154657503"
SERVICES = "Sales    Installation    Service    Repair\nDuctworks"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "output"

def parse_csv(csv_path):
    """Parse CSV file into header and items."""
    with open(csv_path, 'r') as f:
        lines = f.readlines()

    # Find header and items sections
    header_section = None
    items_section = None

    header_start = None
    items_start = None

    for i, line in enumerate(lines):
        if line.strip() == "[ITEMS]":
            items_start = i
            break
        if header_start is None and not line.startswith('['):
            header_start = i

    if header_start is not None and items_start is not None:
        header_section = lines[header_start:items_start]
        items_section = lines[items_start + 1:]
    elif header_start is not None:
        header_section = lines[header_start:]
    else:
        raise ValueError("CSV format invalid. Expected [HEADER] or [ITEMS] markers.")

    # Parse header
    header = {}
    if header_section:
        reader = csv.DictReader(header_section)
        header_row = next(reader)
        header = {k: (v.strip() if v else None) for k, v in header_row.items()}

    # Parse items
    items = []
    if items_section:
        reader = csv.DictReader(items_section)
        current_item = None
        for row in reader:
            if not row.get('item_name') or not row['item_name'].strip():
                continue

            item_name = row['item_name'].strip()
            task_name = row.get('task_name', '').strip()
            task_cost = float(row.get('task_cost', 0)) if row.get('task_cost', '').strip() else 0
            quantity = float(row.get('quantity', 1)) if row.get('quantity', '').strip() else 1
            item_warranty = row.get('item_warranty', '').strip() or None

            # Check if new item or continuation
            if current_item is None or current_item['name'] != item_name:
                # Save previous item
                if current_item:
                    items.append(current_item)

                # Start new item
                current_item = {
                    'name': item_name,
                    'ac_brand': row.get('ac_brand', '').strip() or None,
                    'ac_model': row.get('ac_model', '').strip() or None,
                    'warranty': item_warranty,
                    'tasks': [],
                    'item_total': 0,
                }

            # Add task
            current_item['tasks'].append({
                'name': task_name,
                'cost': task_cost,
                'quantity': quantity,
            })
            current_item['item_total'] += task_cost * quantity

        # Add last item
        if current_item:
            items.append(current_item)

    return header, items

def create_docx(header, items):
    """Create .docx file from parsed data."""
    doc = Document()

    # Set margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # Header
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title.add_run(COMPANY_NAME)
    title_run.bold = True
    title_run.font.size = Pt(14)

    # Location and contact
    header_para = doc.add_paragraph()
    header_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    header_para.add_run(f"{COMPANY_LOCATION}\n").font.size = Pt(11)
    contact = header_para.add_run(f"Telephone Number: {COMPANY_PHONE} || Mobile Number: Sun-{COMPANY_MOBILE_SUN} Globe-{COMPANY_MOBILE_GLOBE}")
    contact.font.size = Pt(9)

    # Services
    services_para = doc.add_paragraph()
    services_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    services_para.add_run(SERVICES).font.size = Pt(10)

    doc.add_paragraph()  # Spacing

    # Customer info
    info_table = doc.add_table(rows=5, cols=2)
    info_table.autofit = False

    date_str = header.get('date', datetime.today().strftime("%m/%d/%Y"))
    info_table.rows[0].cells[0].text = "Date:"
    info_table.rows[0].cells[1].text = date_str

    info_table.rows[1].cells[0].text = "To:"
    info_table.rows[1].cells[1].text = header.get('customer_name', '')

    if header.get('customer_location'):
        info_table.rows[2].cells[0].text = ""
        info_table.rows[2].cells[1].text = header['customer_location']

    attention_text = header.get('attention', '')
    if header.get('phone'):
        attention_text += f" - {header['phone']}"
    if attention_text:
        info_table.rows[3].cells[0].text = "Attention:"
        info_table.rows[3].cells[1].text = attention_text

    doc.add_paragraph()

    # Salutation
    doc.add_paragraph("Sir/Madame,")

    # Opening
    opening = doc.add_paragraph(
        "This is with reference to your request for quotation for the installation/repair of the "
        "following air-conditioner to be installed at:"
    )
    if header.get('installation_location'):
        opening.add_run(f" {header['installation_location']}")

    doc.add_paragraph("We are pleased to quote the following:")

    # Items section
    doc_type = header.get('doc_type', 'summary')
    if doc_type == "summary":
        doc.add_heading("Summary of Quotations", level=2)
    else:
        doc.add_heading("Job to be done:", level=2)

    grand_total = 0
    for i, item in enumerate(items, 1):
        # Item header
        item_header = doc.add_paragraph()
        item_header_run = item_header.add_run(f"{i}. {item['name']}")
        item_header_run.bold = True
        if item.get('ac_brand'):
            item_header.add_run(f" - {item['ac_brand']}")
        if item.get('ac_model'):
            item_header.add_run(f" {item['ac_model']}")

        # Tasks
        for j, task in enumerate(item['tasks'], 1):
            task_para = doc.add_paragraph(style="List Number")
            task_para.text = f"{task['name']}"
            if task['cost'] > 0:
                task_para.text += f" – ₱{task['cost']:,.0f}"
            if task['quantity'] > 1:
                task_para.text += f" × {task['quantity']} = ₱{task['cost'] * task['quantity']:,.0f}"

        # Item total
        total_para = doc.add_paragraph()
        total_para.paragraph_format.left_indent = Inches(0.5)
        total_run = total_para.add_run(f"Total Price – ₱ {item['item_total']:,.2f}")
        total_run.bold = True

        # Item warranty
        if item.get('warranty'):
            warranty_para = doc.add_paragraph(f"Warranty - {item['warranty']}")
            warranty_para.paragraph_format.left_indent = Inches(0.5)

        grand_total += item['item_total']

    # Grand total
    if len(items) > 1:
        doc.add_paragraph()
        grand_para = doc.add_paragraph()
        grand_run = grand_para.add_run(f"Total Price of All Items – ₱ {grand_total:,.2f}")
        grand_run.bold = True

    doc.add_paragraph()

    # Summary info
    if header.get('payment'):
        doc.add_paragraph(f"Terms of Payment: {header['payment']}")
    if header.get('warranty'):
        doc.add_paragraph(f"Warranty: {header['warranty']}")
    if header.get('exceptions'):
        doc.add_paragraph(f"Exception: {header['exceptions']}")

    # Closing
    doc.add_paragraph()
    doc.add_paragraph("Thank you very much for giving us the opportunity to quote and we hope to have the pleasure of serving you.")

    doc.add_paragraph()
    closing = doc.add_paragraph("Very Truly Yours,")
    closing.paragraph_format.space_after = Pt(36)

    # Signature block
    sig_table = doc.add_table(rows=2, cols=2)
    manager = header.get('manager', 'J.B Yap Jr.')
    sig_table.rows[0].cells[0].text = "Conforme:_______________"
    sig_table.rows[0].cells[1].text = manager
    sig_table.rows[1].cells[0].text = "Date:_______________"
    sig_table.rows[1].cells[1].text = ""

    return doc

def save_and_convert(doc, filename):
    """Save .docx and convert to .pdf."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    docx_path = OUTPUT_DIR / f"{filename}.docx"
    pdf_path = OUTPUT_DIR / f"{filename}.pdf"

    # Save docx
    doc.save(docx_path)
    print(f"  ✓ Saved: {docx_path}")

    # Convert to PDF
    try:
        subprocess.run(
            ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", str(OUTPUT_DIR), str(docx_path)],
            check=True,
            capture_output=True,
            timeout=60
        )
        print(f"  ✓ Converted: {pdf_path}")
    except subprocess.CalledProcessError as e:
        print(f"  ⚠ PDF conversion failed: {e.stderr.decode() if e.stderr else 'Unknown error'}")
    except FileNotFoundError:
        print("  ⚠ LibreOffice not found. PDF conversion skipped.")
    except subprocess.TimeoutExpired:
        print("  ⚠ PDF conversion timeout.")

def main():
    """Main execution flow."""
    if len(sys.argv) < 2:
        print("Usage: python3 quotation_batch.py <path_to_csv_file>")
        sys.exit(1)

    csv_path = Path(sys.argv[1])

    if not csv_path.exists():
        print(f"Error: File not found: {csv_path}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("  BATCH QUOTATION GENERATOR")
    print("=" * 60)

    try:
        print(f"\n  Reading: {csv_path}")
        header, items = parse_csv(csv_path)

        customer = header.get('customer_name', 'Unknown')
        date = header.get('date', datetime.today().strftime("%m/%d/%Y"))
        item_count = len(items)
        total = sum(item['item_total'] for item in items)

        print(f"  ✓ Parsed successfully")
        print(f"    Customer: {customer}")
        print(f"    Date: {date}")
        print(f"    Items: {item_count}")
        print(f"    Total: ₱{total:,.2f}\n")

        print("  Generating documents...")
        doc = create_docx(header, items)
        filename = f"{customer}-{date.replace('/', '_')}"
        save_and_convert(doc, filename)

        print(f"\n  ✓ Complete. Files saved to: {OUTPUT_DIR}\n")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
