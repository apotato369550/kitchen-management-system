# Core App - CLAUDE.md

## Purpose

The `core` app is the main application containing all business logic for the kitchen management system.

## Structure

```
core/
├── migrations/           # Database migrations
├── templates/
│   └── core/            # HTML templates (to be created)
├── static/
│   └── core/            # CSS, JS, images (to be created)
├── __init__.py
├── admin.py             # Django admin configuration
├── apps.py              # App configuration
├── models.py            # Database models (8 models)
├── views.py             # View functions (Hello World currently)
├── urls.py              # URL routing
├── forms.py             # Form classes (to be created)
└── tests.py             # Unit tests (to be written)
```

## Models

### Customer
- Stores customer information (name, contact info)
- Related to PurchaseOrder

### RawMaterial
- Library of raw materials with categories
- Categories: meat, vegetables, oil, miscellaneous
- Each has a unit of measurement (grams, pieces, heads, etc.)

### DailyConsumption
- Daily tracking of raw materials consumed
- Foreign key to RawMaterial
- Records date, quantity, and timestamp

### ProductType
- Library of product types (Food Pack, Platter, Bilao, etc.)
- Related to DailyProduction and PurchaseOrderItem

### DailyProduction
- Daily tracking of production output
- Foreign key to ProductType
- Records date, quantity, contents description

### PurchaseOrder
- Customer orders with status tracking
- Status: pending, in_progress, completed, cancelled
- Foreign key to Customer
- Related to PurchaseOrderItem and PurchaseOrderUpdate

### PurchaseOrderItem
- Line items for purchase orders
- Tracks quantity ordered vs. quantity fulfilled
- Foreign keys to PurchaseOrder and ProductType

### PurchaseOrderUpdate
- Comment-style update history for orders
- Tracks staggered deliveries
- Foreign key to PurchaseOrder
- Includes note and optional quantity delivered

## Views

### Current
- `index`: Simple "Hello World" response

### Planned
See `plans/04-raw-materials-production-tracker.md` and `plans/05-purchase-order-tracker.md` for detailed view implementations.

## URL Routing

Currently maps root `/` to index view.

Planned structure includes:
- Dashboard: `/`
- Raw materials: `/raw-materials/`
- Consumption: `/consumption/`
- Product types: `/product-types/`
- Production: `/production/`
- Customers: `/customers/`
- Orders: `/orders/`

## Templates

To be created with Tailwind CSS styling:
- Base template with navigation
- Dashboard/homepage
- CRUD templates for each model
- List views with filtering
- Form views with validation

## Forms

To be created using Django forms:
- RawMaterialForm
- DailyConsumptionForm
- ProductTypeForm
- DailyProductionForm
- CustomerForm
- PurchaseOrderForm (with inline formset for items)
- PurchaseOrderUpdateForm

## Admin Configuration

Register all models in admin.py for quick data management during development.

## Testing

Write tests for:
- Model methods and properties
- Form validation
- View permissions
- Data integrity
- Edge cases

## Key Design Decisions

1. **No Conversion Logic**: Raw materials and production are tracked independently with no automated relationship.

2. **UUID Primary Keys**: All models use UUID for Supabase compatibility.

3. **Soft Relationships**: No strict foreign key to track which raw materials went into which production output.

4. **Flexible Measurements**: Raw materials use string field for units to allow any measurement type.

5. **Status Enum**: Purchase orders use predefined status choices for consistency.

## Future Enhancements

- Data export functionality
- Reporting and analytics
- Bulk data entry
- Mobile-optimized views
- Print-friendly layouts
