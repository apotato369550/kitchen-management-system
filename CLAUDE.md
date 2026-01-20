# CLAUDE.md

This file provides context and instructions for Claude when working on the "Cebu Best Value Trading" Kitchen Management System.

## Project Overview

**Name:** Cebu Best Value Trading Kitchen Management System
**Purpose:** A specialized kitchen management and purchase order tracking system for a food business.
**Core Philosophy:** **SLEEK AND SIMPLE.** The user's vision is paramount. Avoid feature creep, over-engineering, or unsolicited "AI ideas." Focus on fast data entry, mobile-friendliness, and a clean, minimalist design.

## Core Mandates

1.  **Strict Adherence to Vision:** Do not suggest new features unless explicitly asked. Implement exactly what is requested.
2.  **No Correlation (Yet):** Raw material inputs and production outputs are tracked separately. Do not attempt to build automated conversion logic between them.
3.  **Authentication:** No public signup. Admins create accounts.
4.  **User Roles:**
    *   **Admin:** Full access (User management + Operations). Can be a superuser.
    *   **Management:** Operations only (Raw materials, Production, Orders).
    *   **Viewer:** (Future use) Intended for read-only access. The group is created but not currently used in any views.

## Tech Stack

*   **Language:** Python 3.12+
*   **Framework:** Django 6.0
*   **Frontend:** Tailwind CSS
*   **Database:** PostgreSQL (primary deployment via Render, can connect to Supabase for local dev)
*   **Hosting:** **Render**
*   **Dependencies:** `django-axes` (security), `gunicorn` (server), `whitenoise` (static files), `dj-database-url` (db connection), `reportlab` (PDF), `openpyxl` (Excel).

## Project Structure

```text
/
├── accounts/                  # User management, login/logout, roles
├── core/                      # Main business logic (models, views, forms)
│   ├── services/              # Business logic services (e.g., export.py)
│   └── management/commands/   # Custom Django commands (test_data, create_superuser)
├── kitchen_management_system/ # Django project configuration (settings.py, urls.py)
├── plans/                     # Implementation documentation & roadmap
├── build.sh                   # Deployment build script for Render
├── render.yaml                # Infrastructure-as-code for Render
├── manage.py                  # Django CLI entry point
├── .env                       # Environment variables (local development)
└── requirements.txt           # Python dependencies
```

## Key Workflows & Commands

### 1. Development Server (Local)
Requires a `.env` file configured for a database (e.g., Supabase).
```bash
# Set up the database with initial groups and a default admin
python manage.py setup_auth

# Run the server
python manage.py runserver
```

### 2. Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Testing & Sample Data
A custom management command is available for comprehensive testing.
```bash
# Run all CRUD tests
python manage.py test_data_operations

# Populate the database with realistic sample data
python manage.py test_data_operations --populate

# Clear all sample data
python manage.py test_data_operations --clear-samples
```

## Database Schema (`core/models.py`)

All models use UUIDs for primary keys.

*   **`Customer`**: Basic contact info.
*   **`RawMaterial`**: Ingredients/Packaging (Name, Category, Unit).
*   **`DailyConsumption`**: Tracks usage of raw materials per day.
*   **`ProductType`**: Definition of sellable items (Food packs, Platters).
*   **`DailyProduction`**: Tracks output of products per day.
*   **`PurchaseOrder`**: Orders linked to a Customer. Supports staggered fulfillment.
*   **`PurchaseOrderItem`**: Line items in an order.
*   **`PurchaseOrderUpdate`**: Log of updates/partial deliveries for an order.

## Deployment (Render)

*   **Platform:** Render
*   **Configuration:** `render.yaml` defines the web service and database.
*   **Build Process:** `build.sh` script installs dependencies, collects static files, runs migrations, and creates user groups and a superuser.
*   **Continuous Deployment:** Pushing to the `main` branch on GitHub automatically triggers a new deployment on Render.
*   **Superuser Creation:** On first deploy, a superuser is created using credentials from environment variables set in `render.yaml` (`ADMIN_USERNAME`, `ADMIN_PASSWORD`, etc.).

## Current Status (v0.3.0)

*   **Completed:**
    *   Auth System (Admin/Management roles).
    *   Database Schema & Migrations for all 8 models.
    *   Full CRUD views for all models.
    *   Dark Mode UI with Tailwind CSS.
    *   Data Export to Excel & PDF for all modules.
    *   Robust `test_data_operations` command for testing and sample data.
    *   Deployment configuration for **Render**.
*   **Pending/In-Progress:**
    *   Refinement of UI for specific trackers (Plan 04 & 05).

## Data Model Constraints & Gotchas

The database schema has intentional design patterns and critical constraints documented in ARCHITECTURE.md § Constraints & Gotchas. Key gotchas:

**Cascade Delete Risks (7 total):**
- Deleting `RawMaterial` → cascades to all `DailyConsumption` records (history erased)
- Deleting `ProductType` → cascades to all `DailyProduction` + `PurchaseOrderItem` (breaks orders silently)
- Deleting `PurchaseOrder` → cascades to all `PurchaseOrderUpdate` (audit trail lost)
- Deleting `Customer` → cascades to all `PurchaseOrder`, items, updates (full cascade)

**Fulfillment & Status Issues:**
- `PurchaseOrder.status` is NOT auto-updated when items change (status staleness)—must call `order.update_status_based_on_fulfillment()` manually
- `PurchaseOrderItem.quantity_fulfilled` can exceed `quantity_ordered` (over-fulfillment allowed, no validation)
- `PurchaseOrderUpdate.quantity_delivered` is informational only; views must manually sync to items

**Data Aggregation Gaps:**
- `DailyConsumption` has NO `unique_together` on (date, raw_material)—multiple records per pair allowed; aggregation implicit in views/exports
- `DailyProduction` has NO `unique_together` on (date, product_type)—same aggregation pattern

**Read-Only Domains:**
- `DailyConsumption` and `DailyProduction` are create-only (no edit endpoints); user must delete + recreate on error
- Consumption records cannot be edited after creation

See ARCHITECTURE.md § Constraints & Gotchas (lines 649–876) for detailed scenarios and file references.

---

## Permission & Role Model

**Role Hierarchy (ARCHITECTURE.md § Permission & Auth Model):**

| Role | Access | Enforcement |
|------|--------|------------|
| **Superuser** | All operations (user CRUD + ops) | `is_superuser=True` |
| **Admin Group** | User CRUD only | `@admin_required` decorator (4 views) |
| **Management Group** | Operational views (all CRUD, exports) | Decorator exists but NOT applied (@management_or_admin_required unused) |
| **Viewer Group** | Reserved for read-only (not yet implemented) | Decorator ready; enforcement pending |

**Current Enforcement Gap:**
- Superuser ✓ (can bypass group checks)
- Admin ✓ (enforced on user CRUD via `@admin_required`)
- Management ✗ (no enforcement; all @login_required views accessible to any user)
- Viewer ✗ (role created but never used in any views)

**Decorators Available:**
- `@login_required` — Applied to 40+ views (all operations, exports, profile)
- `@admin_required` — accounts/decorators.py:21; applied to user_list, user_create, user_edit, user_delete
- `@management_or_admin_required` — accounts/decorators.py:32; defined but not applied anywhere

**Template-Level Checks (cosmetic):**
- Admin menu visibility gated by `{% if user.is_superuser %}` (accounts/templates/accounts/base.html)
- No view-level enforcement prevents direct URL access by non-admins

See ARCHITECTURE.md § Permission & Auth Model (lines 452–526) for full access control matrix.

---

## View & Endpoint Architecture

The system has 40+ views organized into 7 domains (dashboard, auth, 6 operational). See ARCHITECTURE.md § Endpoint Architecture for full details.

**View Count by Domain:**
- Dashboard: 1 view
- Auth: 8 views (login, logout, profile, password, user CRUD)
- Raw Materials: 6 views (list, create, edit, delete, export Excel/PDF)
- Consumption: 5 views (history, create, delete, export Excel/PDF)
- Product Types: 6 views (list, create, edit, delete, export Excel/PDF)
- Production: 5 views (history, create, delete, export Excel/PDF)
- Customers: 7 views (list, detail, create, edit, delete, export Excel/PDF)
- Purchase Orders: 8 views (list, detail, create, update/fulfillment, status change, delete, export Excel/PDF)

**Fast Data Entry Pattern (Consumption & Production):**
- GET /consumption/add/ or /production/add/ shows form with date pre-filled to today
- User checks "Add Another" checkbox on POST
- Form validates, saves record, redirects back to form (cleared for next entry)
- No page navigation needed for bulk entry
- Template files: core/templates/core/consumption/form.html, core/templates/core/production/form.html

**Inline Formset Pattern (Purchase Orders):**
- GET /orders/create/ shows PurchaseOrderForm + empty PurchaseOrderItemFormSet (1 extra blank row)
- User selects customer, adds items inline (product_type + quantity_ordered)
- Single POST validates both form and formset
- On success: Creates PurchaseOrder + all items, redirects to detail page
- Items default quantity_fulfilled=0

**Export Pattern (All 12 exports):**
- All exports follow identical flow: retrieve data → transform to dict list → build export_data dict → call core/services/export.py service → return BytesIO
- Export views are at: /[domain]/export/excel/ and /[domain]/export/pdf/
- Service functions: export_to_excel(data_dict, headers), export_to_pdf(data_dict, headers)
- Files: core/services/export.py (lines 1–100+); export views in core/views.py (lines 604–950)

**Status Transitions (No Validation):**
- PurchaseOrder.status is ENUM [pending, in_progress, completed, cancelled]
- Any state → any state allowed via manual status change endpoint
- Exception: update_status_based_on_fulfillment() never changes 'cancelled' status (trap state)
- No state machine; no invalid sequence prevention

See ARCHITECTURE.md § Data Flow Patterns (lines 366–449) for detailed flow diagrams.

---

## Critical Implementation Gaps

**Fulfillment Sync Gap (CRITICAL):**
- `purchase_order_add_update` view logs updates but does NOT auto-sync fulfillment
- Workflow: User logs update with quantity_delivered → update saved informational only
- Required manual action: Admin reads update.quantity_delivered → updates item.quantity_fulfilled → calls order.update_status_based_on_fulfillment()
- File references: models.py:177–195 (PurchaseOrderUpdate), views.py:537–565 (purchase_order_add_update)

**No Model Signals:**
- No post_save hooks on PurchaseOrderItem to trigger status recalculation
- All business logic in views/forms; no model-level automation
- Status staleness can occur when items updated outside view layer

**No Edit Endpoints:**
- DailyConsumption: create-only (no edit, must delete + recreate)
- DailyProduction: create-only (same constraint)
- File references: urls.py (no /consumption/<uuid>/edit/ or /production/<uuid>/edit/ routes)

**Cascade Delete Risks (7):**
- RawMaterial delete → DailyConsumption records erased
- ProductType delete → DailyProduction + PurchaseOrderItem deleted (breaks orders)
- PurchaseOrder delete → PurchaseOrderUpdate deleted (audit trail lost)
- Customer delete → all PurchaseOrders + items + updates deleted
- All use `on_delete=CASCADE` (documented in models.py)

See ARCHITECTURE.md § Constraints & Gotchas (lines 649–876) for scenario details and line numbers.

---

## When Working on This Codebase

**Priority Reference Order:**
1. Read ARCHITECTURE.md § System Overview and relevant domain section
2. Use grep index (ARCHITECTURE.md § Grep Index, lines 879–952) to locate functions/models by pattern
3. Check models.py for data relationships and cascade behaviors
4. Check views.py for endpoint implementation and form handling
5. Check core/services/export.py for export patterns

**When Adding Views:**
- Follow existing pattern: form initialization → model.save() → redirect or re-render with errors
- Apply @login_required decorator (minimum); consider @management_or_admin_required for operational views
- Reference ARCHITECTURE.md § Endpoint Architecture for endpoint table format

**When Adding Models:**
- Define cascade behavior explicitly; document in Data Model Constraints & Gotchas section above
- Consider uniqueness constraints for (date, entity) pairs in time-series tables
- Avoid cascades that destroy audit trails (use on_delete=models.PROTECT for audit logs)
- Add model properties for computed values (e.g., overall_progress, is_fulfilled)

**When Adding Exports:**
- Use core/services/export.py service layer (export_to_excel, export_to_pdf)
- Follow standard pattern: retrieve data (with select_related) → transform to dict list → build export_data → call service → return HttpResponse
- Reference existing export views (lines 604–950 in views.py) for implementation template

**Testing & Sample Data:**
- Use `python manage.py test_data_operations --populate` to add realistic data
- Use `python manage.py test_data_operations --clear-samples` to clean up
- Use `python manage.py test_data_operations` to run CRUD tests

**Database Queries:**
- Use select_related() for FK lookups (efficiency: export views)
- Use annotate(order_count=Count(...)) for aggregations (export views)
- Avoid N+1 queries in loops; prefetch related data

---

## Interaction Guidelines for Claude

**DO:**
*   **Context Awareness:** Always check `core/models.py` and `core/views.py` before suggesting changes to business logic. Reference ARCHITECTURE.md for endpoint specs, constraints, and gotchas.
*   **Style:** Match existing Tailwind CSS usage and Django patterns. Follow conventions in existing views, forms, and templates.
*   **Deployment:** Be aware project is deployed on **Render**. Changes to `render.yaml` or `build.sh` will affect deployment.
*   **Reference Precision:** Cite file:line numbers when referencing implementation details (e.g., models.py:81–145 for PurchaseOrder).
*   **Constraint Documentation:** When adding features, update Data Model Constraints & Gotchas section if cascade or validation behavior changes.
*   **Query Efficiency:** Use select_related() and prefetch_related() to avoid N+1 queries. Reference export views for patterns.

**DON'T:**
*   **Suggest Refactoring:** Do not propose structural changes unless explicitly requested. Document what IS, not what could be.
*   **Add Hypothetical Features:** Implement exactly what is requested. No feature creep. Core Philosophy: SLEEK AND SIMPLE.
*   **Output `.env` Contents:** Never display environment variables or secrets.
*   **Assume Cascade Behavior:** Explicitly check models.py before modifying FK relationships. All current cascades are documented in Constraints section.
*   **Soften Language:** Use direct, technical language. Avoid hedging ("could," "might," "could improve").

**When Blocked:**
- If context is incomplete, ask for clarification rather than inventing details.
- If contradictions exist between existing docs and current code, ask before overwriting.
- If neither ARCHITECTURE.md nor git diffs are provided, request explicit instructions before proceeding.

*   **Safety:** Never output the contents of `.env`.
*   **Conciseness:** Be brief. The user values efficiency and clarity.