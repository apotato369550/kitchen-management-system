# Plan 07: Export Data Feature

## Objective
Add export functionality for all data modules (Raw Materials, Consumption, Production, Customers, Orders) to PDF and Excel spreadsheet formats.

## Requirements
- Export to PDF format
- Export to Excel (.xlsx) format
- One-click export from list views
- Maintain data integrity during export
- Include headers, timestamps, relevant metadata

## Tech Stack
- **openpyxl** - For Excel file generation
- **reportlab** - For PDF generation (alternative: weasyprint)
- **Django views** - Custom export views

## Implementation Structure

### 1. Dependencies
Add to `requirements.txt`:
```
openpyxl>=3.10.0
reportlab>=4.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

### 2. Create Export Service Module
**New File:** `core/services/export.py`

Functions needed:
- `export_to_excel()` - Generate Excel workbooks with data
- `export_to_pdf()` - Generate PDF reports with formatted tables
- `get_export_filename()` - Generate timestamped filenames
- Format-specific helpers for each data type

### 3. Create Export Views
**File to modify:** `core/views.py`

Add new views:
- `export_raw_materials_excel()` - Export raw materials list
- `export_raw_materials_pdf()` - Export raw materials PDF
- `export_consumption_excel()` - Export consumption history
- `export_consumption_pdf()` - Export consumption history PDF
- `export_products_excel()` - Export product types
- `export_products_pdf()` - Export product types PDF
- `export_production_excel()` - Export production history
- `export_production_pdf()` - Export production history PDF
- `export_customers_excel()` - Export customer list
- `export_customers_pdf()` - Export customer list PDF
- `export_orders_excel()` - Export purchase orders
- `export_orders_pdf()` - Export purchase orders PDF

All views should:
- Require authentication (`@login_required`)
- Get all relevant data with filters applied
- Return file download response
- Include proper headers and filenames

### 4. Add URL Routes
**File to modify:** `core/urls.py`

Pattern:
```python
# Raw Materials Exports
path('raw-materials/export/excel/', views.export_raw_materials_excel, name='export_raw_materials_excel'),
path('raw-materials/export/pdf/', views.export_raw_materials_pdf, name='export_raw_materials_pdf'),

# Similar patterns for all other modules
```

### 5. Update List View Templates
**Files to modify:** Each list template
- `core/templates/core/raw_materials/list.html`
- `core/templates/core/consumption/list.html`
- `core/templates/core/product_types/list.html`
- `core/templates/core/production/list.html`
- `core/templates/core/customers/list.html`
- `core/templates/core/orders/list.html`

Add buttons to each:
```html
<div class="flex gap-2">
    <a href="{% url 'export_raw_materials_excel' %}" class="px-3 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm font-medium">
        📊 Excel
    </a>
    <a href="{% url 'export_raw_materials_pdf' %}" class="px-3 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg text-sm font-medium">
        📄 PDF
    </a>
</div>
```

### 6. Excel Export Data Structure

For each export, include:
- **Header row** with column names
- **Data rows** with actual values
- **Footer row** with totals/counts where applicable
- **Formatting:**
  - Bold headers
  - Auto-column width
  - Date formatting (YYYY-MM-DD)
  - Proper number formatting
  - Border styling

### 7. PDF Export Data Structure

For each export, include:
- **Title** - Report name and date
- **Metadata** - Export date/time, exported by (username)
- **Summary statistics** - Count of records, totals
- **Table** with:
  - Header row with column names
  - Data rows
  - Proper pagination if needed
- **Footer** - Page numbers

### 8. Filter Preservation
- If user has filters applied before export, include them in the export
- For example: Export consumption history for specific material and date range
- Respect the current queryset with filters

### 9. Permissions & Security
- All exports require authentication
- Respects existing user permissions (management level access)
- No sensitive data exposed beyond normal view permissions

## Export Features by Module

### Raw Materials
- Name, Category, Unit
- Total records count

### Consumption History
- Date, Material Name, Category, Quantity, Unit
- Sum of quantities by material
- Date range if filtered

### Product Types
- Name, Description
- Total records count

### Production History
- Date, Product Type, Quantity, Contents Description
- Sum of quantities by product type
- Date range if filtered

### Customers
- Name, Contact Info
- Total customers count
- Associated orders count per customer

### Purchase Orders
- PO Number, Customer Name, Status, Created Date
- Items breakdown (Product, Qty Ordered, Qty Fulfilled)
- Overall fulfillment percentage
- Order updates/delivery history

## File Naming Convention
```
{module}_{export_type}_{timestamp}.{extension}

Examples:
- raw_materials_excel_2024-01-15_14-30-22.xlsx
- consumption_pdf_2024-01-15_14-30-22.pdf
- purchase_orders_excel_2024-01-15_14-30-22.xlsx
```

## Testing Checklist
✅ Excel exports open correctly in Excel/Sheets
✅ PDF exports display correctly
✅ Data accuracy matches database
✅ Large datasets export without timeout (500+ records)
✅ Filtered exports only include filtered data
✅ File downloads with correct filenames
✅ Dark mode doesn't affect export styling
✅ Mobile users can access export buttons
✅ Special characters in data don't break export

## Future Enhancements
- CSV export format
- Custom column selection
- Export templates/branding
- Scheduled automatic exports
- Email exports directly
- Export to Google Sheets
- Bulk export multiple modules at once

## Success Criteria
✅ All 6 modules have Excel and PDF export
✅ Exports include proper headers and formatting
✅ Files download with correct names
✅ Data accuracy verified
✅ UI buttons visible and functional
✅ No errors during export process
✅ Exports handle edge cases (empty data, special characters)
