# ARCHITECTURE.md

**Purpose:** Comprehensive, greppable system architecture documentation for Cebu Best Value Trading Kitchen Management System. This document captures data models, endpoints, workflows, and system constraints at the implementation level.

---

## TABLE OF CONTENTS

1. [System Overview](#system-overview)
2. [Data Model Architecture](#data-model-architecture)
3. [Endpoint Architecture](#endpoint-architecture)
4. [Data Flow Patterns](#data-flow-patterns)
5. [Permission & Auth Model](#permission--auth-model)
6. [Export Architecture](#export-architecture)
7. [Constraints & Gotchas](#constraints--gotchas)
8. [Grep Index](#grep-index)

---

## SYSTEM OVERVIEW

**Tech Stack:**
- Python 3.12, Django 6.0
- PostgreSQL (Render/Supabase)
- Tailwind CSS (dark mode enabled)
- ReportLab (PDF), openpyxl (Excel)

**Core Principle:** Intentional isolation between input (consumption/production) and sales (orders) domains. No automated correlation between raw material tracking and order fulfillment.

**Database:** All models use UUID primary keys. All FK relationships use `on_delete=CASCADE` (documented exceptions noted below).

---

## DATA MODEL ARCHITECTURE

### 1. ISOLATED DOMAIN: Raw Materials → Consumption

```
RawMaterial (core/models.py:18)
├─ Fields: id (UUID), name (CharField), category (ENUM), unit (CharField), created_at
├─ Relationships: 1:N → DailyConsumption
├─ Constraints: No uniqueness on name; category is ENUM [meat, vegetables, oil, miscellaneous]
├─ Cascade: DELETE cascades to DailyConsumption (history erased)
└─ Validation: None at model level

DailyConsumption (core/models.py:38)
├─ Fields: id (UUID), date, raw_material (FK), quantity (Decimal), created_at
├─ Relationships: N:1 → RawMaterial
├─ Constraints: NO unique_together on (date, raw_material)
├─ Validation: No negative quantity check
├─ Edge Case: Multiple records allowed per (date, material) pair; aggregation is implicit
└─ Note: No edit endpoint; create-only domain
```

**Key Property:** `RawMaterial.consumptions` reverse relation links all historical consumption.

---

### 2. ISOLATED DOMAIN: ProductType → Production

```
ProductType (core/models.py:53)
├─ Fields: id (UUID), name (CharField), description (TextField, optional)
├─ Relationships: 1:N → DailyProduction, 1:N → PurchaseOrderItem
├─ Constraints: No uniqueness on name
├─ Cascade: DELETE cascades to DailyProduction AND PurchaseOrderItem (⚠️ breaks orders)
└─ Validation: None at model level

DailyProduction (core/models.py:65)
├─ Fields: id (UUID), date, product_type (FK), quantity (Integer), contents_description (optional), created_at
├─ Relationships: N:1 → ProductType
├─ Constraints: NO unique_together on (date, product_type)
├─ Validation: No negative quantity check
├─ Edge Case: Multiple records per (date, product) pair; aggregation is implicit
└─ Note: No edit endpoint; create-only domain
```

**Key Property:** `ProductType.productions` reverse relation links all historical production.

---

### 3. RELATIONAL DOMAIN: Customer → Orders → Items

```
Customer (core/models.py:5)
├─ Fields: id (UUID), name (CharField), contact_info (CharField, optional), created_at
├─ Relationships: 1:N → PurchaseOrder
├─ Constraints: No uniqueness on name
├─ Cascade: DELETE cascades to all PurchaseOrders (full deletion)
├─ Validation: None at model level
└─ Edit: Full CRUD support

PurchaseOrder (core/models.py:81)
├─ Fields: id (UUID), customer (FK), status (ENUM), created_at, updated_at
├─ Relationships: N:1 → Customer, 1:N → PurchaseOrderItem, 1:N → PurchaseOrderUpdate
├─ Status Enum: [pending, in_progress, completed, cancelled]
├─ Properties:
│  ├─ po_number: f"PO-{str(id)[:8].upper()}" (e.g., "PO-A1B2C3D4")
│  ├─ overall_progress: (sum(items.fulfilled) / sum(items.ordered)) * 100
│  ├─ is_fully_fulfilled: all(item.is_fulfilled)
│  └─ items_count: items.count()
├─ Status Update Logic: order.update_status_based_on_fulfillment()
│  └─ Sets status to 'completed' if all items fulfilled
│  └─ Sets status to 'in_progress' if any fulfillment > 0
│  └─ Sets status to 'pending' if no fulfillment
│  └─ Never changes 'cancelled' status
├─ ⚠️ CRITICAL: Status NOT auto-updated on item changes; must call method explicitly
├─ Cascade: DELETE cascades to PurchaseOrderItem and PurchaseOrderUpdate (audit trail lost)
└─ Edit: Full CRUD + update/status change endpoints

PurchaseOrderItem (core/models.py:146)
├─ Fields: id (UUID), purchase_order (FK), product_type (FK), quantity_ordered (Integer), quantity_fulfilled (Integer, default=0)
├─ Relationships: N:1 → PurchaseOrder, N:1 → ProductType
├─ Properties:
│  ├─ fulfillment_percentage: (quantity_fulfilled / quantity_ordered) * 100
│  ├─ is_fulfilled: quantity_fulfilled >= quantity_ordered
│  └─ remaining_quantity: max(0, quantity_ordered - quantity_fulfilled)
├─ ⚠️ CRITICAL: NO constraint enforcing quantity_fulfilled ≤ quantity_ordered (over-fulfillment allowed)
├─ Validation: No checks at model or form level
├─ Cascade: FK to ProductType uses CASCADE (deleting product type orphans this item)
└─ Edit: No direct edit endpoint; only edited via inline formset in order creation

PurchaseOrderUpdate (core/models.py:177)
├─ Fields: id (UUID), purchase_order (FK), note (TextField), quantity_delivered (Integer, optional), created_at
├─ Relationships: N:1 → PurchaseOrder
├─ Purpose: Audit log of delivery events and fulfillment notes
├─ ⚠️ CRITICAL: quantity_delivered is informational only, NOT auto-synced to PurchaseOrderItem.quantity_fulfilled
├─ Manual Sync: Views must read update.quantity_delivered and manually update item.quantity_fulfilled
├─ Cascade: DELETE (parent PurchaseOrder) cascades to all updates (audit trail erased)
└─ No direct edit; only created via purchase_order_add_update view
```

**Key Relationships:**
```
Customer ──1:N──→ PurchaseOrder ──1:N──→ PurchaseOrderItem ──N:1──→ ProductType
                       │
                       └──1:N──→ PurchaseOrderUpdate
```

---

## ENDPOINT ARCHITECTURE

### AUTH ENDPOINTS

#### `accounts/views.py`

**Decorator Summary:**
- `@login_required`: 2 views (profile_view, change_password_view)
- `@admin_required`: 4 views (user_list, user_create, user_edit, user_delete)
- `@management_or_admin_required`: 0 views (decorator exists but unused; reserved for Viewer enforcement)

| Endpoint | View | Method | Purpose | Permission | Notes |
|----------|------|--------|---------|------------|-------|
| `/accounts/login/` | login_view | GET, POST | Authenticate user | None (redirects if logged in) | Uses CustomAuthenticationForm (Tailwind styled) |
| `/accounts/logout/` | logout_view | GET, POST | Terminate session | @login_required | Redirects to login |
| `/accounts/profile/` | profile_view | GET | View user details | @login_required | Any logged-in user |
| `/accounts/profile/change-password/` | change_password_view | GET, POST | Update password | @login_required | Uses CustomPasswordChangeForm, keeps session active |
| `/accounts/users/` | user_list | GET | List all users with roles | @admin_required | Superuser/Admin group only |
| `/accounts/users/create/` | user_create | GET, POST | Create new user + assign role | @admin_required | Uses UserCreateForm; assigns group on save |
| `/accounts/users/<int:pk>/edit/` | user_edit | GET, POST | Update user + role | @admin_required | Uses UserEditForm; detects current group |
| `/accounts/users/<int:pk>/delete/` | user_delete | GET, POST | Remove user (prevents self-delete) | @admin_required | Shows confirm page |

**Key Forms:**
- `CustomAuthenticationForm(username, password)` — Tailwind-styled login
- `UserCreateForm(username, first_name, last_name, email, password1, password2, role)` — Extends UserCreationForm
- `UserEditForm(username, first_name, last_name, email, is_active, role)` — Detects group on init
- `CustomPasswordChangeForm(old_password, new_password1, new_password2)` — Tailwind-styled

---

### DASHBOARD ENDPOINT

| Endpoint | View | Method | Purpose | Permission | Notes |
|----------|------|--------|---------|------------|-------|
| `/` | dashboard | GET | System overview + quick actions | @login_required | Shows counts for all domains; no role checks |

---

### RAW MATERIALS DOMAIN

**Endpoints:** `core/views.py` (views 47–660)

| Endpoint | View | Method | Purpose | Params | Returns | Notes |
|----------|------|--------|---------|--------|---------|-------|
| `/raw-materials/` | raw_material_list | GET | List materials, filterable | `category` (filter) | HTML table + mobile cards | @login_required; desktop/mobile responsive |
| `/raw-materials/add/` | raw_material_create | GET, POST | Create material | Form: name, category, unit | Redirect to list | @login_required |
| `/raw-materials/<uuid:pk>/edit/` | raw_material_edit | GET, POST | Update material | Form: name, category, unit | Redirect to list | @login_required; pre-fills current values |
| `/raw-materials/<uuid:pk>/delete/` | raw_material_delete | GET, POST | Confirm + remove material | (none, form action) | Redirect to list | @login_required; shows confirm page |
| `/raw-materials/export/excel/` | export_raw_materials_excel | GET | Export to .xlsx | (none) | BytesIO (Excel file) | @login_required; calls export_to_excel service |
| `/raw-materials/export/pdf/` | export_raw_materials_pdf | GET | Export to .pdf | (none) | BytesIO (PDF file) | @login_required; calls export_to_pdf service |

**Form:** `RawMaterialForm` (core/forms.py)
- Fields: name (CharField), category (ChoiceField), unit (CharField)
- No custom validation

**Export Headers:** Name, Category, Unit

**Data Source:** `RawMaterial.objects.all()` (for export views)

---

### CONSUMPTION DOMAIN

**Endpoints:** `core/views.py` (views 124–700)

| Endpoint | View | Method | Purpose | Params/Form | Returns | Notes |
|----------|------|--------|---------|------------|---------|-------|
| `/consumption/` | consumption_history | GET | View consumption records, filterable | `date_from`, `date_to`, `category` (filters) | HTML table + mobile cards | @login_required; shows 10 recent records below |
| `/consumption/add/` | consumption_create | GET, POST | Record material usage | Form: date, raw_material, quantity; Param: `add_another` | Redirect to create (if add_another) or to history | @login_required; date defaults to today; supports bulk entry |
| `/consumption/<uuid:pk>/delete/` | consumption_delete | GET, POST | Remove consumption record | (form action) | Redirect to history | @login_required |
| `/consumption/export/excel/` | export_consumption_excel | GET | Export records to .xlsx | (none) | BytesIO (Excel file) | @login_required |
| `/consumption/export/pdf/` | export_consumption_pdf | GET | Export records to .pdf | (none) | BytesIO (PDF file) | @login_required |

**Form:** `DailyConsumptionForm` (core/forms.py)
- Fields: date (DateField), raw_material (ModelChoiceField), quantity (DecimalField, step=0.01)
- Custom init: Sets date to today if not provided
- No negative quantity validation

**Export Headers:** Date, Material, Category, Quantity, Unit

**Data Source:** `DailyConsumption.objects.select_related('raw_material')` (for export)

**UX Pattern:** Fast data entry with "Add Another" checkbox allows rapid sequential recording without page navigation.

---

### PRODUCT TYPES DOMAIN

**Endpoints:** `core/views.py` (views 200–760)

| Endpoint | View | Method | Purpose | Params | Returns | Notes |
|----------|------|--------|---------|--------|---------|-------|
| `/product-types/` | product_type_list | GET | List products | (none) | HTML table + mobile cards | @login_required |
| `/product-types/add/` | product_type_create | GET, POST | Create product | Form: name, description | Redirect to list | @login_required |
| `/product-types/<uuid:pk>/edit/` | product_type_edit | GET, POST | Update product | Form: name, description | Redirect to list | @login_required |
| `/product-types/<uuid:pk>/delete/` | product_type_delete | GET, POST | Confirm + remove product | (form action) | Redirect to list | @login_required; ⚠️ cascades to orders |
| `/product-types/export/excel/` | export_products_excel | GET | Export to .xlsx | (none) | BytesIO (Excel file) | @login_required |
| `/product-types/export/pdf/` | export_products_pdf | GET | Export to .pdf | (none) | BytesIO (PDF file) | @login_required |

**Form:** `ProductTypeForm` (core/forms.py)
- Fields: name (CharField), description (TextField, optional)
- No custom validation

**Export Headers:** Name, Description

**Data Source:** `ProductType.objects.all()`

**⚠️ CASCADE GOTCHA:** Deleting a ProductType cascades to all PurchaseOrderItems. Orders lose line items silently.

---

### PRODUCTION DOMAIN

**Endpoints:** `core/views.py` (views 269–820)

| Endpoint | View | Method | Purpose | Params/Form | Returns | Notes |
|----------|------|--------|---------|------------|---------|-------|
| `/production/` | production_history | GET | View production records, grouped by date | `date_from`, `date_to`, `product_type` (filters) | HTML (grouped by date DESC) + mobile | @login_required; grouped by date; 10 recent below |
| `/production/add/` | production_create | GET, POST | Record production output | Form: date, product_type, quantity, contents_description; Param: `add_another` | Redirect to create (if add_another) or to history | @login_required; date defaults to today; supports bulk entry |
| `/production/<uuid:pk>/delete/` | production_delete | GET, POST | Remove production record | (form action) | Redirect to history | @login_required |
| `/production/export/excel/` | export_production_excel | GET | Export to .xlsx | (none) | BytesIO (Excel file) | @login_required |
| `/production/export/pdf/` | export_production_pdf | GET | Export to .pdf | (none) | BytesIO (PDF file) | @login_required |

**Form:** `DailyProductionForm` (core/forms.py)
- Fields: date (DateField), product_type (ModelChoiceField), quantity (IntegerField), contents_description (TextField, optional)
- Custom init: Sets date to today if not provided
- No negative quantity validation

**Export Headers:** Date, Product, Quantity, Contents

**Data Source:** `DailyProduction.objects.select_related('product_type')`

**UX Pattern:** Same as consumption—fast data entry with "Add Another" checkbox.

---

### CUSTOMERS DOMAIN

**Endpoints:** `core/views.py` (views 361–880)

| Endpoint | View | Method | Purpose | Params | Form Fields | Returns | Notes |
|----------|------|--------|---------|--------|------------|---------|-------|
| `/customers/` | customer_list | GET | List customers, searchable | `search` (name filter) | (none) | HTML table + mobile cards | @login_required |
| `/customers/add/` | customer_create | GET, POST | Create customer | (none) | name, contact_info | Redirect to list | @login_required |
| `/customers/<uuid:pk>/` | customer_detail | GET | View customer + related orders | (none) | (none) | HTML detail + orders table | @login_required; shows linked PurchaseOrders |
| `/customers/<uuid:pk>/edit/` | customer_edit | GET, POST | Update customer | (none) | name, contact_info | Redirect to detail | @login_required |
| `/customers/<uuid:pk>/delete/` | customer_delete | GET, POST | Confirm + remove customer | (form action) | (none) | Redirect to list | @login_required; ⚠️ cascades to all orders |
| `/customers/export/excel/` | export_customers_excel | GET | Export to .xlsx | (none) | (none) | BytesIO (Excel file) | @login_required |
| `/customers/export/pdf/` | export_customers_pdf | GET | Export to .pdf | (none) | (none) | BytesIO (PDF file) | @login_required |

**Form:** `CustomerForm` (core/forms.py)
- Fields: name (CharField), contact_info (CharField, optional)
- No custom validation

**Export Headers:** Name, Contact, Orders (count)

**Data Source:** `Customer.objects.annotate(order_count=Count('purchase_orders'))`

**⚠️ CASCADE GOTCHA:** Deleting a Customer cascades to all PurchaseOrders + items + updates.

---

### PURCHASE ORDERS DOMAIN

**Endpoints:** `core/views.py` (views 454–950)

#### List & Create

| Endpoint | View | Method | Purpose | Params | Form/Formset | Returns | Notes |
|----------|------|--------|---------|--------|------------|---------|-------|
| `/orders/` | purchase_order_list | GET | List orders, filterable | `status`, `customer`, `date_from`, `date_to` | (none) | HTML table + mobile cards | @login_required; shows status badges + progress % |
| `/orders/create/` | purchase_order_create | GET, POST | Create new order | (none) | PurchaseOrderForm + PurchaseOrderItemFormSet (inline) | Redirect to detail page (new order) | @login_required; supports adding items in same submission |

**PurchaseOrderForm Fields:** customer (ModelChoiceField)

**PurchaseOrderItemFormSet:**
- Parent: PurchaseOrder
- Child: PurchaseOrderItem
- Fields per item: product_type (ModelChoiceField), quantity_ordered (IntegerField, min=1)
- Extra: 1 blank row for adding new items
- Can delete: True

**Create Flow:**
1. User selects customer
2. User adds 1+ items (product + qty)
3. POST validation checks both form and formset
4. On success: Saves PurchaseOrder + all items, redirects to detail page
5. Items default quantity_fulfilled=0

---

#### Detail & Updates

| Endpoint | View | Method | Purpose | Params | Returns | Notes |
|----------|------|--------|---------|--------|---------|-------|
| `/orders/<uuid:pk>/` | purchase_order_detail | GET | View order + items + fulfillment progress | (none) | HTML detail page | @login_required; shows items table with fulfillment %, updates history |
| `/orders/<uuid:pk>/update/` | purchase_order_add_update | GET, POST | Log delivery update | (none) | PurchaseOrderUpdateForm (note + quantity_delivered) | Redirect to detail | @login_required; ⚠️ does NOT auto-sync item fulfillment |
| `/orders/<uuid:pk>/status/` | purchase_order_change_status | GET, POST | Change order status manually | (none) | Status selector (dropdown) | Redirect to detail | @login_required; allows arbitrary transitions |
| `/orders/<uuid:pk>/delete/` | purchase_order_delete | GET, POST | Confirm + remove order | (form action) | (none) | Redirect to list | @login_required; cascades to items + updates |

**PurchaseOrderUpdateForm Fields:**
- note (TextField, required)
- quantity_delivered (IntegerField, optional)

**⚠️ CRITICAL FLOW ISSUE:** `purchase_order_add_update` logs the update but does NOT automatically update item fulfillment. View layer or admin must manually:
1. Read PurchaseOrderUpdate.quantity_delivered
2. Update PurchaseOrderItem.quantity_fulfilled
3. Call PurchaseOrder.update_status_based_on_fulfillment()

---

#### Exports

| Endpoint | View | Method | Purpose | Params | Returns | Notes |
|----------|------|--------|---------|--------|---------|-------|
| `/orders/export/excel/` | export_orders_excel | GET | Export orders to .xlsx | (none) | BytesIO (Excel file) | @login_required |
| `/orders/export/pdf/` | export_orders_pdf | GET | Export orders to .pdf | (none) | BytesIO (PDF file) | @login_required |

**Export Headers:** PO Number, Customer, Status, Items, Progress (%), Created Date

**Data Source:** `PurchaseOrder.objects.select_related('customer')` (calculated items/progress in view)

---

## DATA FLOW PATTERNS

### Pattern 1: Fast Data Entry (Consumption & Production)

```
User Flow:
  GET /consumption/add/ → Form (date pre-filled to today)
  User fills: material, quantity
  User checks "Add Another"
  POST → Validate form → Save DailyConsumption → Redirect to /consumption/add/ (cleared)
  User enters next record → Repeat

UX Benefit: Rapid sequential entry without page navigation
Template: core/templates/core/consumption/form.html
         core/templates/core/production/form.html
```

### Pattern 2: Inline Order Item Editing (Purchase Orders)

```
User Flow:
  GET /orders/create/ → Form (customer) + empty formset (1 extra row)
  User selects customer
  User adds items: [Product A, 10], [Product B, 5]
  User clicks "Add More" button (JS adds blank row)
  POST → Validate PurchaseOrderForm + PurchaseOrderItemFormSet
  On success:
    - Create PurchaseOrder
    - Create PurchaseOrderItem for each row (quantity_fulfilled defaults to 0)
    - Redirect to /orders/<new_id>/
  On error: Re-render form with error messages

Form Files: core/forms.py (lines 148-155)
           core/templates/core/orders/form.html
```

### Pattern 3: Staggered Fulfillment (Manual)

```
Order State:
  Day 1: Create PO with 10 items (status='pending', fulfillment=0%)
  Day 1: Add delivery update (quantity_delivered=3, note="First batch")
  Action Required: Manually update item.quantity_fulfilled = 3
  Action Required: Call order.update_status_based_on_fulfillment()
             → status changes to 'in_progress', progress=30%

  Day 2: Add delivery update (quantity_delivered=4, note="Second batch")
  Action Required: Manually update item.quantity_fulfilled = 7

  Day 3: Add delivery update (quantity_delivered=3, note="Final batch")
  Action Required: Manually update item.quantity_fulfilled = 10
  Action Required: Call order.update_status_based_on_fulfillment()
             → status changes to 'completed', progress=100%

⚠️ Current Gap: purchase_order_add_update view logs update but does NOT perform manual sync
              Admin must manually update fulfillment after each delivery
```

### Pattern 4: Export (All Domains)

```
Standard Flow (12 export views):
  GET /[domain]/export/excel/ (or /pdf/)
    ↓
  View retrieves data from model (with select_related for efficiency)
    ↓
  View transforms to list of dicts: [{'Header1': val, 'Header2': val}, ...]
    ↓
  View builds export_data dict:
    {
      'title': 'Raw Materials Report',
      'sheet_name': 'Materials' (Excel only),
      'data': [...],
      'summary': {'Total': count, ...}
    }
    ↓
  View calls service: export_to_excel(export_data) or export_to_pdf(export_data)
    ↓
  Service returns BytesIO with formatted output
    ↓
  View returns HttpResponse with content-type + filename

Service Functions: core/services/export.py (lines 1-100+)
```

---

## PERMISSION & AUTH MODEL

### Role Hierarchy

```
Superuser (is_superuser=True)
  └─ Has all permissions
  └─ Can access: Admin menu (user CRUD) + all operational views
  └─ Can bypass group checks (but still requires @login_required)

Admin Group (django.contrib.auth.Group, name='Admin')
  └─ Created by setup_auth command (accounts/management/commands/setup_auth.py)
  └─ Permissions: All user CRUD operations
  └─ Can access: User management endpoints (@admin_required)
  └─ Cannot access: By default, but @admin_required checks is_superuser OR user.groups.filter(name='Admin')

Management Group (django.contrib.auth.Group, name='Management')
  └─ Created by setup_auth command
  └─ Permissions: All operational views (CRUD for all domains, exports)
  └─ Can access: All @login_required views (no additional group check enforced)
  └─ Note: Decorator exists (@management_or_admin_required) but not applied

Viewer Group (django.contrib.auth.Group, name='Viewer')
  └─ Created by setup_auth command
  └─ Permissions: Reserved for read-only access (not yet implemented)
  └─ Can access: Currently same as Management (no enforcement)
  └─ Decorator: @management_or_admin_required ready to gate read-only views
```

### Decorator Enforcement

**`@login_required`** (Django built-in)
- Applied to: 40 views (all operational + exports + profile)
- Effect: Redirects to /accounts/login/ if user not authenticated
- File: Imported from django.contrib.auth.decorators

**`@admin_required`** (custom)
- Location: accounts/decorators.py:21
- Applied to: 4 views (user_list, user_create, user_edit, user_delete)
- Check: `if not (user.is_superuser or user.groups.filter(name='Admin'))`
- Effect: Raises PermissionDenied (403) if check fails

**`@management_or_admin_required`** (custom)
- Location: accounts/decorators.py:32
- Applied to: 0 views (reserved for future Viewer enforcement)
- Check: `if not (user.groups.filter(name__in=['Management', 'Admin']))`
- Effect: Raises PermissionDenied (403) if check fails

### Current Access Control Matrix

| View Category | Permission Check | Accessible By | Notes |
|---|---|---|---|
| **Dashboard** | @login_required only | Any logged-in user | No role filtering |
| **Raw Materials (6 views)** | @login_required only | Any logged-in user | Management/Admin intended, not enforced |
| **Consumption (3 views)** | @login_required only | Any logged-in user | Management/Admin intended, not enforced |
| **Product Types (4 views)** | @login_required only | Any logged-in user | Management/Admin intended, not enforced |
| **Production (3 views)** | @login_required only | Any logged-in user | Management/Admin intended, not enforced |
| **Customers (5 views)** | @login_required only | Any logged-in user | Management/Admin intended, not enforced |
| **Orders (6 views)** | @login_required only | Any logged-in user | Management/Admin intended, not enforced |
| **Exports (12 views)** | @login_required only | Any logged-in user | Management/Admin intended, not enforced |
| **User CRUD (4 views)** | @admin_required | Superuser or Admin group | Enforced in view decorator |
| **Profile/Password** | @login_required only | Any logged-in user | Own profile only (checked in view) |

### Template-Level Permission Checks

**File:** accounts/templates/accounts/base.html

- **Admin Menu:** `{% if user.is_superuser %}` (lines ~100, ~187)
  - Visible to superusers only
  - Contains link to `/accounts/users/`
- **Dashboard:** No role checks; all users see same view

**Gap:** Template checks are cosmetic. No view-level enforcement prevents non-superuser from accessing /accounts/users/ directly (only @admin_required decorator stops it).

---

## EXPORT ARCHITECTURE

### Service Layer: `core/services/export.py`

#### Function: `export_to_excel(data_dict, headers)`

**Signature:**
```python
def export_to_excel(data_dict: dict, headers: list) -> BytesIO
```

**Input Data Structure:**
```python
{
    'title': str,               # e.g., "Raw Materials Report"
    'sheet_name': str,          # e.g., "Materials"
    'data': [
        {'Header1': val1, 'Header2': val2, ...},
        {'Header1': val1, 'Header2': val2, ...},
    ],
    'summary': {                # Optional summary stats
        'Total Records': count,
        'Total Quantity': sum,
    }
}
```

**Output:** BytesIO object containing .xlsx workbook

**Features:**
- Headers: Bold, blue background, auto-fitted columns
- Data rows: Standard formatting
- Summary section: Below data with key statistics
- Timestamp: Included in sheet

#### Function: `export_to_pdf(data_dict, headers)`

**Signature:**
```python
def export_to_pdf(data_dict: dict, headers: list) -> BytesIO
```

**Input:** Same as `export_to_excel`

**Output:** BytesIO object containing .pdf

**Features:**
- Title: Bold, centered at top
- Date stamp: Report generation date
- Table: Styled with borders, alternating row shading
- Summary: Below table
- Footer: Page numbers

#### Function: `get_export_filename(module_name, export_format)`

**Signature:**
```python
def get_export_filename(module_name: str, export_format: str) -> str
```

**Returns:** `f"{module_name}_{export_format}_YYYY-MM-DD_HH-MM-SS"`

**Example:** `raw_materials_excel_2025-01-20_14-50-30`

---

### Export Views: Pattern & Implementation

**All 12 export views follow identical pattern:**

1. **Retrieve data** with efficient queries:
   ```python
   materials = RawMaterial.objects.all()
   ```

2. **Transform to list of dicts:**
   ```python
   data = [
       {
           'Name': m.name,
           'Category': m.get_category_display(),
           'Unit': m.unit,
       }
       for m in materials
   ]
   ```

3. **Build export dictionary:**
   ```python
   export_data = {
       'title': 'Raw Materials Report',
       'sheet_name': 'Materials',
       'data': data,
       'summary': {'Total Materials': len(data)}
   }
   ```

4. **Call service & return:**
   ```python
   file_bytes = export_to_excel(export_data)
   response = HttpResponse(file_bytes, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
   response['Content-Disposition'] = f'attachment; filename="{get_export_filename("raw_materials", "excel")}.xlsx"'
   return response
   ```

---

### Export Views Summary

| Module | Excel View | PDF View | Data Source | Headers | Row Count |
|--------|-----------|---------|-------------|---------|-----------|
| Raw Materials | export_raw_materials_excel (604) | export_raw_materials_pdf (635) | RawMaterial.all() | Name, Category, Unit | len(materials) |
| Consumption | export_consumption_excel (662) | export_consumption_pdf (697) | DC.select_related('rm') | Date, Material, Category, Qty, Unit | len(records) |
| Products | export_products_excel (726) | export_products_pdf (756) | ProductType.all() | Name, Description | len(products) |
| Production | export_production_excel (782) | export_production_pdf (814) | DP.select_related('pt') | Date, Product, Qty, Contents | len(records) |
| Customers | export_customers_excel (842) | export_customers_pdf (874) | C.annotate(orders) | Name, Contact, Orders | len(customers) |
| Orders | export_orders_excel (902) | export_orders_pdf (937) | PO.select_related('c') | PO#, Customer, Status, Items, Progress%, Created | len(orders) |

---

## CONSTRAINTS & GOTCHAS

### 1. CRITICAL: Status Staleness

**Issue:** `PurchaseOrder.status` is NOT auto-updated when items change.

**Scenario:**
```python
order = PurchaseOrder.objects.get(...)  # status='pending'
item = order.items.first()

# User fulfills entire item
item.quantity_fulfilled = item.quantity_ordered
item.save()

# BUT:
order.status  # Still 'pending' if accessed from cache—STALE
order.overall_progress  # Stale calculation
```

**Root Cause:** No signal handler on PurchaseOrderItem.post_save. No auto-call to `order.update_status_based_on_fulfillment()`.

**Fix:** View layer must explicitly call after item updates:
```python
order.update_status_based_on_fulfillment()
order.save()
```

**Files Affected:**
- models.py:81-145 (PurchaseOrder class definition + update_status_based_on_fulfillment method)
- views.py:537-565 (purchase_order_add_update view—should call update_status after syncing fulfillment)

---

### 2. CRITICAL: Over-fulfillment Allowed

**Issue:** `PurchaseOrderItem.quantity_fulfilled` can exceed `quantity_ordered`.

**Example:**
```python
item = PurchaseOrderItem.objects.create(
    purchase_order=order,
    product_type=product,
    quantity_ordered=5,
    quantity_fulfilled=10  # ✓ Succeeds (no validation)
)
```

**Impact:**
- fulfillment_percentage = (10/5)*100 = 200%
- is_fulfilled = True (10 >= 5)
- remaining_quantity = max(0, 5-10) = 0 (clipped)
- overall_progress can show >100%

**No Validation:** No model-level validator, no form clean() check, no signal validation.

**Design Question:** Is this intentional (allow over-delivery) or unintended? CLAUDE.md does not address.

---

### 3. CASCADE DELETES: ProductType → Orders

**Issue:** Deleting a ProductType cascades to all PurchaseOrderItems + silently breaks orders.

**Scenario:**
```python
product = ProductType.objects.get(name='Food Pack')
product.delete()  # CASCADE

# NOW:
order = PurchaseOrder.objects.get(...)
order.items.count()  # Returns 0 (orphaned)
order.overall_progress  # Returns 0 (no items)
order.is_fully_fulfilled  # Returns False
```

**Audit Impact:** No warning. Orders lose line items silently.

**Better Design:** Use `on_delete=models.PROTECT` for ProductType FK in PurchaseOrderItem.

**File:** models.py:146-176 (PurchaseOrderItem definition, line ~161 FK definition)

---

### 4. CASCADE DELETES: PurchaseOrder → Audit Trail

**Issue:** Deleting a PurchaseOrder cascades to all PurchaseOrderUpdates, destroying fulfillment history.

**Scenario:**
```python
order.delete()  # Cascades to all updates

# Fulfillment history lost—no way to know what was delivered
```

**Better Design:** Use `on_delete=models.PROTECT` or soft-delete for audit logs.

**File:** models.py:177-195 (PurchaseOrderUpdate definition, FK relation)

---

### 5. DUPLICATE RECORDS: No Uniqueness Constraint

**Models:** DailyConsumption, DailyProduction

**Issue:** Multiple records allowed per (date, material/product) pair.

**Scenario:**
```
2025-01-20, Chicken Breast: 5 kg (record 1)
2025-01-20, Chicken Breast: 3 kg (record 2)
2025-01-20, Chicken Breast: 2 kg (record 3)
Total: 10 kg (implicit aggregation in views/exports)
```

**No Constraint:** No `unique_together` at model level. Database allows all.

**Impact:** Aggregation logic is delegated to views/exports. No single source of truth at DB level.

**Files:**
- models.py:38-51 (DailyConsumption, no unique_together)
- models.py:65-79 (DailyProduction, no unique_together)

---

### 6. EDIT GAP: DailyConsumption Read-Only

**Issue:** Consumption records can only be created, not edited.

**Views:**
- `consumption_create` ✓ (create)
- `consumption_delete` ✓ (delete)
- `consumption_edit` ✗ (missing)

**Impact:** User must delete and recreate record if mistake made.

**Files:** views.py (consumption_* functions), urls.py (no /consumption/<uuid>/edit/ route)

---

### 7. STATUS TRANSITIONS: No Validation

**Issue:** PurchaseOrder can transition between any statuses arbitrarily.

**Invalid Transitions Allowed:**
```python
order.status = 'completed'
order.status = 'pending'  # Can revert arbitrarily
order.save()
```

**No State Machine:** No validation preventing invalid sequences (e.g., completed → pending).

**Only Rule:** `update_status_based_on_fulfillment()` never changes 'cancelled' status (trap state).

**File:** models.py:81-145 (PurchaseOrder.update_status_based_on_fulfillment method)

---

### 8. FULFILLMENT SYNC: Manual Required

**Issue:** `PurchaseOrderUpdate.quantity_delivered` does NOT auto-sync to `PurchaseOrderItem.quantity_fulfilled`.

**Expected (but not implemented):**
```
User logs update: quantity_delivered=3
  ↓
System auto-updates: item.quantity_fulfilled += 3
  ↓
System calls: order.update_status_based_on_fulfillment()
```

**Actual (current):**
```
User logs update: quantity_delivered=3
  ↓
Update is saved (informational only)
  ↓
Admin must manually read update.quantity_delivered
  ↓
Admin must manually update item.quantity_fulfilled
  ↓
Admin must manually call update_status_based_on_fulfillment()
```

**Workaround Required:** View layer or admin interface must perform manual sync.

**Files:**
- models.py:177-195 (PurchaseOrderUpdate definition—quantity_delivered unused)
- views.py:537-565 (purchase_order_add_update—logs update but does NOT sync)

---

### 9. CUSTOMER DELETION CASCADES

**Issue:** Deleting a Customer cascades to all PurchaseOrders + items + updates.

**Scenario:**
```python
customer.delete()  # Deletes all orders + fulfillment history
```

**Better Design:** Use `on_delete=models.PROTECT` to prevent deletion of customers with active orders.

**File:** models.py:81-95 (PurchaseOrder.customer FK definition)

---

### 10. NO ROLE ENFORCEMENT ON OPERATIONAL VIEWS

**Issue:** All operational views enforce only `@login_required`, not role-based access.

**Implication:**
- Any logged-in user can access all CRUD views (consumption, production, orders, customers)
- No decorator enforces Management group
- Viewer role exists but is unused

**Current Decorators Available:**
- `@admin_required` — Applied to user CRUD only
- `@management_or_admin_required` — Defined but unused

**Solution:** Apply `@management_or_admin_required` to all operational views (not yet done).

**Files:**
- decorators.py:21-30 (@admin_required)
- decorators.py:32-40 (@management_or_admin_required)
- views.py (40+ operational views not using management decorator)

---

## GREP INDEX

**Quick Navigation by Pattern:**

### Models
```bash
grep -n "^class " core/models.py
  # RawMaterial:18, DailyConsumption:38, ProductType:53, DailyProduction:65
  # Customer:5, PurchaseOrder:81, PurchaseOrderItem:146, PurchaseOrderUpdate:177
```

### Views (Core)
```bash
grep -n "^def " core/views.py | head -50
  # dashboard:20, raw_material_list:47, consumption_history:124, production_history:269
  # customer_list:361, purchase_order_list:454, purchase_order_detail:524
  # export_*:604–950
```

### Export Service
```bash
grep -n "^def " core/services/export.py
  # export_to_excel, export_to_pdf, get_export_filename
```

### Decorators
```bash
grep -n "^def " accounts/decorators.py
  # admin_required:21, management_or_admin_required:32
```

### Forms
```bash
grep -n "^class " core/forms.py
  # RawMaterialForm, DailyConsumptionForm, ProductTypeForm, DailyProductionForm
  # CustomerForm, PurchaseOrderForm, PurchaseOrderItemForm, PurchaseOrderItemFormSet
  # PurchaseOrderUpdateForm, UserCreateForm, UserEditForm
```

### URL Routes
```bash
grep -n "path(" core/urls.py
  # 68 total routes across 6 domains + exports
```

### Auth Routes
```bash
grep -n "path(" accounts/urls.py
  # 8 routes: login, logout, user CRUD, profile, password
```

### Status Machine
```bash
grep -n "update_status_based_on_fulfillment\|STATUSES\|status =" core/models.py
  # PurchaseOrder status definition, update method
```

### Cascade Deletes
```bash
grep -n "on_delete=CASCADE" core/models.py
  # All FK relations: DailyConsumption→RawMaterial, PurchaseOrderItem→PurchaseOrder, etc.
```

### Permission Checks
```bash
grep -rn "@login_required\|@admin_required\|@management_or_admin_required" core/ accounts/
  # View decorator applications
```

### Fast Data Entry Pattern
```bash
grep -n "add_another" core/views.py core/forms.py core/templates/core/consumption/ core/templates/core/production/
  # consumption_create:151, production_create:312, form templates
```

---

## QUICK REFERENCE

### Environment Variables Required
```
DATABASE_URL = PostgreSQL connection string
DEBUG = False (production)
SECRET_KEY = Django secret
ALLOWED_HOSTS = Domain list
```

### Setup Commands
```bash
python manage.py setup_auth          # Create groups (Admin, Management, Viewer)
python manage.py migrate             # Apply migrations
python manage.py createsuperuser     # Create admin user
python manage.py test_data_operations --populate  # Add sample data
```

### Key Files Summary

| File | Purpose | Key Content |
|------|---------|-------------|
| core/models.py | 8 model definitions | All business entities, relationships, properties |
| core/views.py | 40+ view functions | All CRUD + exports, @login_required |
| core/urls.py | 68 URL routes | Path patterns for all endpoints |
| core/forms.py | 11+ form classes | ModelForms, formsets, custom forms |
| core/services/export.py | Export service | export_to_excel, export_to_pdf, get_export_filename |
| accounts/decorators.py | Custom decorators | @admin_required, @management_or_admin_required |
| accounts/views.py | 8 auth views | login, logout, user CRUD, profile, password |
| accounts/urls.py | 8 auth routes | Auth endpoint patterns |

---

**Document Version:** 1.0 (2025-01-20)
**Last Reviewed:** Initial synthesis from agent investigation
**Next Review:** After Phase 2 documentation updates
