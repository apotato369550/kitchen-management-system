# Core App Context

## Overview
The `core` app contains the primary business logic, database models, and UI for the Kitchen Management System. It implements the two main pillars of the user's requirements:
1.  **Raw Materials & Production Tracking** (Non-correlated).
2.  **Purchase Order Management** (With staggered fulfillment).

## Database Models (`models.py`)

All models use **UUIDs** as primary keys for compatibility with Supabase/PostgreSQL.

### 1. Operations Tracking
*   **`RawMaterial`**: Inventory definitions (Meat, Veg, Oil, Misc) with units.
*   **`DailyConsumption`**: Records usage of raw materials on a specific date.
*   **`ProductType`**: Definitions of sellable items (Food Packs, Platters, etc.).
*   **`DailyProduction`**: Records output of products on a specific date.
*   **`Customer`**: Simple CRM (Name, Contact Info).

### 2. Order Management
*   **`PurchaseOrder`**: The parent order entity.
    *   **Status:** Pending, In Progress, Completed, Cancelled.
    *   **Logic:** Status auto-updates based on item fulfillment.
*   **`PurchaseOrderItem`**: Specific products within an order.
    *   Tracks `quantity_ordered` vs `quantity_fulfilled`.
*   **`PurchaseOrderUpdate`**: A log for staggered delivery/updates.
    *   Acts like "comments" but can also track partial `quantity_delivered`.

## Key Logic
*   **No Conversion:** There is *no* automatic deduction of raw materials when production is recorded. They are tracked independently.
*   **Staggered Fulfillment:** Orders are not binary (Done/Not Done). They progress as `PurchaseOrderItem`s are fulfilled via updates.

## Services
*   **`services/export.py`**: Handles data export to Excel and PDF.
    *   Uses `openpyxl` for Excel.
    *   Uses `reportlab` for PDF.

## Templates & UI
*   Uses **Tailwind CSS**.
*   **Dark Mode** is the default/supported theme.
*   **Dashboard:** Provides high-level summaries.

## Management Commands
*   `management/commands/test_data_operations.py`: A robust script for generating sample data and testing CRUD operations without polluting the main database permanently (supports cleanup).
