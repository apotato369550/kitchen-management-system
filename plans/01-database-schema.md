# Database Schema Plan

## Authentication
Handled by Supabase Auth (not in Django models).

## Models

### Customer
- `id` (UUID, PK)
- `name` (string)
- `contact_info` (string, optional)
- `created_at` (timestamp)

### RawMaterial
- `id` (UUID, PK)
- `name` (string)
- `category` (enum: meat, vegetables, oil, miscellaneous)
- `unit` (string) - e.g., grams, pieces, heads

### DailyConsumption
- `id` (UUID, PK)
- `date` (date)
- `raw_material` (FK → RawMaterial)
- `quantity` (decimal)
- `created_at` (timestamp)

### ProductType
- `id` (UUID, PK)
- `name` (string) - e.g., "Food Pack", "Platter", "Bilao"
- `description` (string, optional)

### DailyProduction
- `id` (UUID, PK)
- `date` (date)
- `product_type` (FK → ProductType)
- `quantity` (integer)
- `contents_description` (text, optional)
- `created_at` (timestamp)

### PurchaseOrder
- `id` (UUID, PK)
- `customer` (FK → Customer)
- `status` (enum: pending, in_progress, completed, cancelled)
- `created_at` (timestamp)
- `updated_at` (timestamp)

### PurchaseOrderItem
- `id` (UUID, PK)
- `purchase_order` (FK → PurchaseOrder)
- `product_type` (FK → ProductType)
- `quantity_ordered` (integer)
- `quantity_fulfilled` (integer, default 0)

### PurchaseOrderUpdate
- `id` (UUID, PK)
- `purchase_order` (FK → PurchaseOrder)
- `note` (text) - comment-style update
- `quantity_delivered` (integer, optional) - for staggered fulfillment
- `created_at` (timestamp)

## Notes
- No conversion relationship between raw materials and production (per requirements)
- UUIDs used for Supabase compatibility
- PurchaseOrderUpdate enables the "comment thread" style tracking for staggered deliveries
